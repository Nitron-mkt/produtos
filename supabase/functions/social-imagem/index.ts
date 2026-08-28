// social-imagem — gera os CENÁRIOS do post com o GPT e hospeda no bucket público `social`.
//
// Lê social_post com status=briefing_pronto, consulta quantos slots de cenário o modelo
// do Canva pede (social_modelo.slots_cenario) e gera um por slot.
//
// Modelo com slots_cenario = 0 (Modelo 01, 02 e 03) NÃO chama a OpenAI: o post é montado
// só com foto real de produto. A função promove direto para imagem_aprovada, custo zero.
//
// O GPT gera SÓ o cenário. O produto entra como foto real, no Canva. Ver SOCIAL.md.
//
// Segredos: OPENAI_API_KEY. SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY vêm do runtime.

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

// gpt-image-1 NÃO aceita 1080x1350. Só 1024x1024, 1024x1536 e 1536x1024.
// O tamanho certo vem da FORMA DO SLOT, não do canal: o slot do Modelo 04 é um
// círculo 741x741, e retrato 2:3 nele perde as laterais no recorte. Por isso
// social_modelo.cenario_size manda, e o canal é só fallback.
function tamanhoPara(canal: string): string {
  if (canal.includes("story") || canal.includes("reels")) return "1024x1536";
  if (canal.includes("feed")) return "1024x1536";
  return "1024x1024";
}

// Reforço de negativa: um recipiente na cena é o defeito mais caro — o consumidor
// acha que é o produto vendido. Pessoa só é liberada no Modelo 04.
function negativa(permitePessoa: boolean): string {
  const base =
    " Sem texto, sem letras, sem logotipo, sem marca d'água, e sem nenhum pote, vasilha, " +
    "recipiente, caixa ou embalagem visível na cena. Deixe uma área contínua vazia e " +
    "desobstruída, com margem folgada nas bordas porque o Canva vai recortar.";
  return permitePessoa ? base : `${base} Sem pessoas, sem rostos e sem mãos.`;
}

async function patch(id: number, campos: Record<string, unknown>) {
  const r = await fetch(`${SUPABASE_URL}/rest/v1/social_post?id=eq.${id}`, {
    method: "PATCH",
    headers: { ...rest, Prefer: "return=minimal" },
    body: JSON.stringify(campos),
  });
  if (!r.ok) console.error(`patch ${id} falhou: ${r.status} ${await r.text()}`);
}

// Falha de upload não é culpa do briefing e a imagem já foi paga — por isso
// ela não consome tentativa, ao contrário de uma recusa da OpenAI.
class ErroUpload extends Error {}

async function umaImagem(prompt: string, tamanho: string, permitePessoa: boolean) {
  const resp = await fetch("https://api.openai.com/v1/images/generations", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${OPENAI_KEY}` },
    body: JSON.stringify({
      model: MODELO,
      prompt: `${prompt}${negativa(permitePessoa)}`,
      size: tamanho,
      quality: "high",
      n: 1,
    }),
  });

  if (!resp.ok) throw new Error(`openai ${resp.status}: ${(await resp.text()).slice(0, 400)}`);

  const b64 = (await resp.json())?.data?.[0]?.b64_json;
  if (!b64) throw new Error("resposta da OpenAI sem b64_json");
  return Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
}

async function subir(bytes: Uint8Array, arquivo: string) {
  const up = await fetch(`${SUPABASE_URL}/storage/v1/object/${BUCKET}/${arquivo}`, {
    method: "POST",
    headers: {
      // apikey é obrigatório: se a chave do projeto não for JWT legado, o Storage
      // recusa o Bearer com 403 "Invalid Compact JWS". Verificado em 28/08/2026.
      apikey: SERVICE_KEY,
      Authorization: `Bearer ${SERVICE_KEY}`,
      "Content-Type": "image/png",
      "x-upsert": "true",
    },
    body: bytes,
  });
  if (!up.ok) throw new ErroUpload(`storage ${up.status}: ${(await up.text()).slice(0, 300)}`);
  return `${SUPABASE_URL}/storage/v1/object/public/${BUCKET}/${arquivo}`;
}

// Trava de concorrencia. O cron de 5 em 5 minutos e uma chamada manual podem pegar
// o MESMO post: aconteceu em 28/08/2026 e o social-qa avaliou duas vezes. No QA isso
// e log duplicado; aqui seria PAGAR DUAS GERACOES. O UPDATE filtrado por status é a
// trava: quem conseguir mudar briefing_pronto -> gerando_imagem leva o post, e o
// outro worker recebe zero linhas e desiste.
async function tentarPegar(id: number): Promise<boolean> {
  const r = await fetch(
    `${SUPABASE_URL}/rest/v1/social_post?id=eq.${id}&status=eq.briefing_pronto`,
    {
      method: "PATCH",
      headers: { ...rest, Prefer: "return=representation" },
      body: JSON.stringify({ status: "gerando_imagem" }),
    },
  );
  if (!r.ok) {
    console.error(`trava ${id} falhou: ${r.status} ${await r.text()}`);
    return false;
  }
  return ((await r.json()) as unknown[]).length > 0;
}

async function processar(post: Record<string, any>) {
  const modelo = post.social_modelo;
  const slots = modelo?.slots_cenario ?? 0;

  // Sem modelo cadastrado não dá para saber quantos cenários gerar.
  if (!modelo) {
    await patch(post.id, {
      status: "briefing_reprovado",
      erro: `modelo '${post.modelo ?? "(vazio)"}' não está em social_modelo`,
    });
    return { id: post.id, ok: false, erro: "modelo desconhecido" };
  }

  // Modelo 01, 02, 03: arte feita só com foto real. Nenhuma chamada paga.
  if (slots === 0) {
    await patch(post.id, { status: "imagem_aprovada", erro: null });
    return { id: post.id, ok: true, pulou: "modelo não usa cenário", custo: 0 };
  }

  const prompts: string[] = post.prompts_cenario?.length
    ? post.prompts_cenario
    : post.prompt_imagem
    ? [post.prompt_imagem]
    : [];

  if (prompts.length < slots) {
    await patch(post.id, {
      status: "briefing_reprovado",
      erro: `${post.modelo} pede ${slots} cenário(s), o briefing trouxe ${prompts.length}`,
    });
    return { id: post.id, ok: false, erro: "prompts insuficientes" };
  }

  // Só a partir daqui existe custo. Pega a trava antes de gastar.
  if (!(await tentarPegar(post.id))) {
    return { id: post.id, ok: true, pulou: "outro worker pegou o post" };
  }

  const tentativa = (post.tentativas_imagem ?? 0) + 1;
  const cenarios: { slot: number; url: string }[] = [];

  for (let i = 0; i < slots; i++) {
    try {
      const bytes = await umaImagem(
        prompts[i],
        modelo.cenario_size ?? tamanhoPara(post.canal ?? ""),
        modelo.permite_pessoa === true,
      );
      const url = await subir(bytes, `${post.id}-v${tentativa}-s${i + 1}.png`);
      cenarios.push({ slot: i + 1, url });
    } catch (e) {
      const upload = e instanceof ErroUpload;
      // Recusa da OpenAI consome tentativa: sem isso o cron reprocessa o mesmo
      // briefing ruim de 5 em 5 minutos para sempre. Falha de upload não consome:
      // a imagem já foi paga e o problema é de infraestrutura, não do briefing.
      const gasta = upload ? (post.tentativas_imagem ?? 0) : tentativa;
      await patch(post.id, {
        tentativas_imagem: gasta,
        erro: `slot ${i + 1}: ${String(e).slice(0, 400)}`,
        status: !upload && gasta >= MAX_TENTATIVAS ? "parado_revisao_humana" : "briefing_pronto",
        cenarios: cenarios.length ? cenarios : null,
      });
      return { id: post.id, ok: false, erro: String(e).slice(0, 200), gerados: cenarios.length };
    }
  }

  await patch(post.id, {
    cenarios,
    imagem_gpt_url: cenarios[0].url,
    tentativas_imagem: tentativa,
    status: "imagem_hospedada",
    erro: null,
  });

  return { id: post.id, ok: true, slots: cenarios.length, tentativa };
}

// Resgate de orfao: se a funcao morrer entre pegar a trava e gravar o resultado,
// o post fica preso em gerando_imagem para sempre. Uma geracao nao passa de poucos
// minutos, entao qualquer coisa parada ali ha mais de 10 minutos volta para a fila.
async function resgatarOrfaos() {
  const limite = new Date(Date.now() - 10 * 60 * 1000).toISOString();
  const r = await fetch(
    `${SUPABASE_URL}/rest/v1/social_post` +
      `?status=eq.gerando_imagem&atualizado_em=lt.${limite}`,
    {
      method: "PATCH",
      headers: { ...rest, Prefer: "return=representation" },
      body: JSON.stringify({ status: "briefing_pronto", erro: "resgatado: travado em gerando_imagem" }),
    },
  );
  if (!r.ok) {
    console.error(`resgate falhou: ${r.status} ${await r.text()}`);
    return 0;
  }
  return ((await r.json()) as unknown[]).length;
}

Deno.serve(async (req: Request) => {
  if (!OPENAI_KEY) {
    return new Response(
      JSON.stringify({ erro: "OPENAI_API_KEY não configurada nos secrets do projeto" }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }

  const n = Number(new URL(req.url).searchParams.get("n") ?? "3");
  const resgatados = await resgatarOrfaos();

  const fila = await fetch(
    `${SUPABASE_URL}/rest/v1/social_post` +
      `?status=eq.briefing_pronto&tentativas_imagem=lt.${MAX_TENTATIVAS}` +
      `&select=id,canal,modelo,prompt_imagem,prompts_cenario,tentativas_imagem,` +
      `social_modelo(codigo,slots_cenario,permite_pessoa,cenario_size)` +
      `&order=data_prevista.asc.nullslast&limit=${n}`,
    { headers: rest },
  );

  if (!fila.ok) {
    return new Response(JSON.stringify({ erro: `fila ${fila.status}: ${await fila.text()}` }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }

  const posts = await fila.json();
  const resultados = [];
  for (const post of posts) resultados.push(await processar(post)); // serial: rate limit de imagem é baixo

  return new Response(JSON.stringify({ processados: resultados.length, resgatados, resultados }), {
    headers: { "Content-Type": "application/json" },
  });
});
