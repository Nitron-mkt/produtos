// social-qa — gate automático de qualidade do CENÁRIO gerado, por visão.
//
// Substitui o passo que seria do n8n. Lê social_post com status=imagem_hospedada,
// manda a imagem para a API da Anthropic com visão e pergunta se ela serve como
// cenário — sem produto, sem texto, com área livre para a foto real entrar.
//
// Este é o QA da imagem CRUA. O QA da arte MONTADA é do revisor-social, na sessão
// do Claude, porque só lá se vê texto estourando box e logo tampado. Ver SOCIAL.md.
//
// Segredos necessários: ANTHROPIC_API_KEY.

import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const ANTHROPIC_KEY = Deno.env.get("ANTHROPIC_API_KEY");

const MODELO = "claude-sonnet-5";
const MAX_TENTATIVAS = 2;

const rest = {
  "Content-Type": "application/json",
  apikey: SERVICE_KEY,
  Authorization: `Bearer ${SERVICE_KEY}`,
};

const INSTRUCAO = `Você avalia se uma imagem serve como CENÁRIO de fundo para um post da Nitron,
fabricante de utilidades domésticas plásticas.

A imagem é só o fundo. Uma foto real do produto será composta por cima dela, e a marca
será aplicada no Canva depois.

Reprove se qualquer item abaixo for verdadeiro:
1. Aparece qualquer pote, vasilha, recipiente, caixa, jarra ou embalagem na cena — mesmo
   ao fundo, mesmo desfocado. O consumidor confundiria com o produto vendido.
2. Aparece texto, letra, número, logotipo ou marca d'água.
3. Aparece pessoa, rosto, mão ou parte de corpo.
4. Não existe área contínua vazia e desobstruída onde o produto possa ser colocado.
5. A imagem tem artefato evidente de geração — perspectiva impossível, textura derretida,
   linha de bancada que não fecha.
6. A cena não corresponde ao briefing pedido.

Responda SOMENTE com JSON, sem cercas de código:
{"veredito":"aprovado"|"reprovado","item":<número do item que falhou ou null>,
 "correcao":"<instrução concreta para reescrever o prompt, ou null>"}`;

async function patch(id: number, campos: Record<string, unknown>) {
  const r = await fetch(`${SUPABASE_URL}/rest/v1/social_post?id=eq.${id}`, {
    method: "PATCH",
    headers: { ...rest, Prefer: "return=minimal" },
    body: JSON.stringify(campos),
  });
  if (!r.ok) console.error(`patch ${id} falhou: ${r.status} ${await r.text()}`);
}

async function logQa(postId: number, veredito: string, item: unknown, correcao: unknown, bruto: unknown) {
  const r = await fetch(`${SUPABASE_URL}/rest/v1/social_qa`, {
    method: "POST",
    headers: { ...rest, Prefer: "return=minimal" },
    body: JSON.stringify({
      post_id: postId,
      etapa: "imagem_crua",
      avaliador: MODELO,
      veredito,
      item_falhou: item == null ? null : `item ${item}`,
      correcao: correcao ?? null,
      bruto,
    }),
  });
  if (!r.ok) console.error(`social_qa insert falhou: ${r.status} ${await r.text()}`);
}

async function avaliar(post: Record<string, any>) {
  const resp = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": ANTHROPIC_KEY!,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: MODELO,
      max_tokens: 512,
      messages: [{
        role: "user",
        content: [
          { type: "image", source: { type: "url", url: post.imagem_gpt_url } },
          { type: "text", text: `${INSTRUCAO}\n\nBriefing pedido:\n${post.prompt_imagem}` },
        ],
      }],
    }),
  });

  if (!resp.ok) {
    const detalhe = (await resp.text()).slice(0, 400);
    await patch(post.id, { erro: `anthropic ${resp.status}: ${detalhe}` });
    return { id: post.id, ok: false, erro: `anthropic ${resp.status}` };
  }

  const json = await resp.json();
  const texto: string = json?.content?.[0]?.text ?? "";

  let parsed: { veredito?: string; item?: unknown; correcao?: unknown } = {};
  try {
    // O modelo às vezes embrulha em cerca de código apesar da instrução.
    parsed = JSON.parse(texto.replace(/```json\s*|```/g, "").trim());
  } catch {
    await patch(post.id, { erro: `QA devolveu resposta não-JSON: ${texto.slice(0, 200)}` });
    return { id: post.id, ok: false, erro: "resposta não-JSON" };
  }

  const aprovado = parsed.veredito === "aprovado";
  await logQa(post.id, aprovado ? "aprovado" : "reprovado", parsed.item, parsed.correcao, json?.usage ?? null);

  if (aprovado) {
    await patch(post.id, { status: "imagem_aprovada", erro: null });
    return { id: post.id, ok: true, veredito: "aprovado" };
  }

  // Reprovou. Volta para geração se ainda tem tentativa; senão para de queimar crédito.
  const estourou = (post.tentativas_imagem ?? 0) >= MAX_TENTATIVAS;
  await patch(post.id, {
    status: estourou ? "parado_revisao_humana" : "briefing_pronto",
    erro: estourou ? `QA reprovou ${MAX_TENTATIVAS}x: ${parsed.correcao ?? "sem detalhe"}` : null,
  });

  return { id: post.id, ok: true, veredito: "reprovado", estourou, correcao: parsed.correcao };
}

Deno.serve(async (req: Request) => {
  if (!ANTHROPIC_KEY) {
    return new Response(
      JSON.stringify({ erro: "ANTHROPIC_API_KEY não configurada nos secrets do projeto" }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }

  const n = Number(new URL(req.url).searchParams.get("n") ?? "5");

  const fila = await fetch(
    `${SUPABASE_URL}/rest/v1/social_post` +
      `?status=eq.imagem_hospedada&imagem_gpt_url=not.is.null` +
      `&select=id,imagem_gpt_url,prompt_imagem,tentativas_imagem` +
      `&order=atualizado_em.asc&limit=${n}`,
    { headers: rest },
  );

  if (!fila.ok) {
    return new Response(
      JSON.stringify({ erro: `fila ${fila.status}: ${await fila.text()}` }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }

  const posts = await fila.json();
  const resultados = await Promise.all(posts.map(avaliar));

  return new Response(JSON.stringify({ avaliados: resultados.length, resultados }), {
    headers: { "Content-Type": "application/json" },
  });
});
