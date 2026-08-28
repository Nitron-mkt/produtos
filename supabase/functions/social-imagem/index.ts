// social-imagem — gera o CENÁRIO do post com o GPT e hospeda no bucket público `social`.
//
// Substitui o passo que seria do n8n. Lê social_post com status=briefing_pronto,
// chama a API de imagem da OpenAI com o prompt escrito pelo diretor-arte, e grava
// o PNG em social/{id}-v{tentativa}.png devolvendo a URL pública.
//
// O GPT gera SÓ o cenário. O produto entra depois, como foto real, no Canva.
// Ver SOCIAL.md.
//
// Segredos necessários: OPENAI_API_KEY. SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY
// são injetados pelo runtime.

import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const OPENAI_KEY = Deno.env.get("OPENAI_API_KEY");

const MODELO = "gpt-image-1";
const BUCKET = "social";
const MAX_TENTATIVAS = 2;

const rest = {
  "Content-Type": "application/json",
  apikey: SERVICE_KEY,
  Authorization: `Bearer ${SERVICE_KEY}`,
};

// gpt-image-1 NÃO aceita 1080x1350. Os tamanhos são 1024x1024, 1024x1536 e 1536x1024.
// Geramos em retrato 2:3 e o Canva faz o recorte final para 4:5 ou 9:16.
function tamanhoPara(canal: string): string {
  if (canal.includes("story") || canal.includes("reels")) return "1024x1536";
  if (canal.includes("feed")) return "1024x1536";
  return "1024x1024";
}

// Reforço de negativa: o modelo às vezes ignora a proibição na primeira passada,
// e um recipiente na cena é o defeito mais caro (o consumidor acha que é o produto).
const NEGATIVA =
  " Sem texto, sem letras, sem logotipo, sem marca d'água, sem pessoas, sem mãos, " +
  "e sem nenhum pote, vasilha, recipiente, caixa ou embalagem visível na cena. " +
  "A área central deve ficar completamente vazia e desobstruída.";

async function patch(id: number, campos: Record<string, unknown>) {
  const r = await fetch(`${SUPABASE_URL}/rest/v1/social_post?id=eq.${id}`, {
    method: "PATCH",
    headers: { ...rest, Prefer: "return=minimal" },
    body: JSON.stringify(campos),
  });
  if (!r.ok) console.error(`patch ${id} falhou: ${r.status} ${await r.text()}`);
}

async function gerar(post: Record<string, any>) {
  const tentativa = (post.tentativas_imagem ?? 0) + 1;

  const resp = await fetch("https://api.openai.com/v1/images/generations", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${OPENAI_KEY}`,
    },
    body: JSON.stringify({
      model: MODELO,
      prompt: `${post.prompt_imagem}${NEGATIVA}`,
      size: tamanhoPara(post.canal ?? ""),
      quality: "high",
      n: 1,
    }),
  });

  if (!resp.ok) {
    const detalhe = (await resp.text()).slice(0, 500);
    // Estoura a tentativa mesmo em erro técnico: sem isso o cron reprocessa
    // o mesmo post de 5 em 5 minutos para sempre.
    await patch(post.id, {
      tentativas_imagem: tentativa,
      erro: `openai ${resp.status}: ${detalhe}`,
      status: tentativa >= MAX_TENTATIVAS ? "parado_revisao_humana" : "briefing_pronto",
    });
    return { id: post.id, ok: false, erro: `openai ${resp.status}` };
  }

  const json = await resp.json();
  const b64 = json?.data?.[0]?.b64_json;
  if (!b64) {
    await patch(post.id, {
      tentativas_imagem: tentativa,
      erro: "resposta da OpenAI sem b64_json",
      status: tentativa >= MAX_TENTATIVAS ? "parado_revisao_humana" : "briefing_pronto",
    });
    return { id: post.id, ok: false, erro: "sem b64_json" };
  }

  const bytes = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
  const arquivo = `${post.id}-v${tentativa}.png`;

  const up = await fetch(`${SUPABASE_URL}/storage/v1/object/${BUCKET}/${arquivo}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${SERVICE_KEY}`,
      "Content-Type": "image/png",
      "x-upsert": "true",
    },
    body: bytes,
  });

  if (!up.ok) {
    const detalhe = (await up.text()).slice(0, 300);
    await patch(post.id, { erro: `storage ${up.status}: ${detalhe}` });
    return { id: post.id, ok: false, erro: `storage ${up.status}` };
  }

  const url = `${SUPABASE_URL}/storage/v1/object/public/${BUCKET}/${arquivo}`;
  await patch(post.id, {
    imagem_gpt_url: url,
    tentativas_imagem: tentativa,
    status: "imagem_hospedada",
    erro: null,
  });

  return { id: post.id, ok: true, url, tentativa };
}

Deno.serve(async (req: Request) => {
  if (!OPENAI_KEY) {
    return new Response(
      JSON.stringify({ erro: "OPENAI_API_KEY não configurada nos secrets do projeto" }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }

  const n = Number(new URL(req.url).searchParams.get("n") ?? "3");

  const fila = await fetch(
    `${SUPABASE_URL}/rest/v1/social_post` +
      `?status=eq.briefing_pronto&tentativas_imagem=lt.${MAX_TENTATIVAS}` +
      `&prompt_imagem=not.is.null` +
      `&select=id,canal,formato,prompt_imagem,tentativas_imagem` +
      `&order=data_prevista.asc.nullslast&limit=${n}`,
    { headers: rest },
  );

  if (!fila.ok) {
    return new Response(
      JSON.stringify({ erro: `fila ${fila.status}: ${await fila.text()}` }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }

  const posts = await fila.json();
  const resultados = [];
  for (const post of posts) resultados.push(await gerar(post)); // serial: rate limit de imagem é baixo

  return new Response(JSON.stringify({ processados: resultados.length, resultados }), {
    headers: { "Content-Type": "application/json" },
  });
});
