// social-qa — gate automático de qualidade dos CENÁRIOS gerados, por visão.
//
// Lê social_post com status=imagem_hospedada e avalia CADA cenário gerado contra o
// briefing. Todos precisam passar: um slot ruim estraga a arte inteira.
//
// A regra de "sem pessoa" é por modelo — o Modelo 04 é lifestyle e exige pessoa.
// Vem de social_modelo.permite_pessoa, não está chumbada aqui.
//
// Este é o QA da imagem CRUA. O QA da arte MONTADA é do revisor-social, na sessão do
// Claude, porque só lá se vê texto estourando box e logo tampado. Ver SOCIAL.md.
//
// Segredos: ANTHROPIC_API_KEY.

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

function instrucao(permitePessoa: boolean, promessa: string): string {
  const itemPessoa = permitePessoa
    ? "3. (não se aplica a este modelo — pessoa é esperada aqui)"
    : "3. Aparece pessoa, rosto, mão ou parte de corpo.";

  return `Você avalia se uma imagem serve como CENÁRIO de fundo para um post da Nitron,
fabricante de utilidades domésticas plásticas.

A imagem é só o fundo do slot. A marca será aplicada no Canva depois, e em alguns
modelos uma foto real do produto entra por cima.

Reprove se qualquer item abaixo for verdadeiro:
1. Aparece qualquer pote, vasilha, recipiente, caixa, jarra ou embalagem na cena — mesmo
   ao fundo, mesmo desfocado. O consumidor confundiria com o produto vendido.
2. Aparece texto, letra, número, logotipo ou marca d'água.
${itemPessoa}
4. Não existe área contínua vazia e desobstruída onde o produto possa ser colocado.
5. A imagem tem artefato evidente de geração — perspectiva impossível, textura derretida,
   linha de bancada que não fecha, membro deformado.
6. A cena não corresponde ao briefing pedido.
7. O assunto principal está colado na borda. O Canva recorta o slot, e o que está na
   borda se perde.

E agora o item mais importante, o de coerência:

8. A cena NÃO entrega a promessa abaixo, ou contradiz ela.

PROMESSA VISUAL (o que a legenda promete que a imagem mostre):
${promessa}

Julgue o item 8 contra a PROMESSA, não contra o briefing técnico. Eles podem divergir, e
quando divergem é a promessa que vale — ela é o que o consumidor vai ler junto da imagem.

Dois modos clássicos de falhar o item 8:
- A promessa fala de um problema a resolver (bagunça, canto sem uso, falta de espaço) e a
  cena mostra tudo arrumado e resolvido. A cena então comunica o oposto.
- A promessa nomeia um objeto que a cena não mostra e não sugere. O leitor procura o objeto
  na imagem e não acha.

Responda SOMENTE com JSON, sem cercas de código:
{"veredito":"aprovado"|"reprovado","item":<número do item que falhou ou null>,
 "correcao":"<instrução concreta para reescrever o prompt, ou null>"}`;
}

async function patch(id: number, campos: Record<string, unknown>) {
  const r = await fetch(`${SUPABASE_URL}/rest/v1/social_post?id=eq.${id}`, {
    method: "PATCH",
    headers: { ...rest, Prefer: "return=minimal" },
    body: JSON.stringify(campos),
  });
  if (!r.ok) console.error(`patch ${id} falhou: ${r.status} ${await r.text()}`);
}

async function logQa(
  postId: number,
  slot: number,
  veredito: string,
  item: unknown,
  correcao: unknown,
  bruto: unknown,
) {
  const r = await fetch(`${SUPABASE_URL}/rest/v1/social_qa`, {
    method: "POST",
    headers: { ...rest, Prefer: "return=minimal" },
    body: JSON.stringify({
      post_id: postId,
      etapa: `imagem_crua_s${slot}`,
      avaliador: MODELO,
      veredito,
      item_falhou: item == null ? null : `item ${item}`,
      correcao: correcao ?? null,
      bruto,
    }),
  });
  if (!r.ok) console.error(`social_qa insert falhou: ${r.status} ${await r.text()}`);
}

async function avaliarSlot(url: string, briefing: string, permitePessoa: boolean, promessa: string) {
  const resp = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": ANTHROPIC_KEY!,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: MODELO,
      max_tokens: 1024,
      messages: [{
        role: "user",
        content: [
          { type: "image", source: { type: "url", url } },
          {
            type: "text",
            text: `${instrucao(permitePessoa, promessa)}\n\nBriefing técnico do slot (secundário):\n${briefing}`,
          },
        ],
      }],
    }),
  });

  if (!resp.ok) throw new Error(`anthropic ${resp.status}: ${(await resp.text()).slice(0, 300)}`);

  const json = await resp.json();
  // Nunca assuma que content[0] é o bloco de texto: se vier qualquer outro tipo de bloco
  // antes, content[0].text é undefined e o parse quebra com "resposta não-JSON" — o que
  // aconteceu em 28/08/2026. Junte todos os blocos de texto.
  const texto: string = (json?.content ?? [])
    .filter((b: Record<string, unknown>) => b?.type === "text")
    .map((b: Record<string, string>) => b.text ?? "")
    .join("\n")
    .trim();
  try {
    // O modelo às vezes embrulha em cerca de código apesar da instrução.
    const parsed = JSON.parse(texto.replace(/```json\s*|```/g, "").trim());
    return { parsed, uso: json?.usage ?? null };
  } catch {
    throw new Error(
      `QA devolveu resposta não-JSON. stop_reason=${json?.stop_reason} ` +
        `blocos=${(json?.content ?? []).map((b: Record<string, string>) => b?.type).join(",")} ` +
        `texto=${texto.slice(0, 200)}`,
    );
  }
}

async function avaliar(post: Record<string, any>) {
  const permitePessoa = post.social_modelo?.permite_pessoa === true;
  const prompts: string[] = post.prompts_cenario?.length
    ? post.prompts_cenario
    : post.prompt_imagem
    ? [post.prompt_imagem]
    : [];

  const cenarios: { slot: number; url: string }[] = post.cenarios?.length
    ? post.cenarios
    : post.imagem_gpt_url
    ? [{ slot: 1, url: post.imagem_gpt_url }]
    : [];

  if (!cenarios.length) {
    await patch(post.id, { status: "briefing_reprovado", erro: "sem cenário para avaliar" });
    return { id: post.id, ok: false, erro: "sem cenário" };
  }

  const reprovas: string[] = [];

  for (const c of cenarios) {
    let r;
    try {
      r = await avaliarSlot(
        c.url,
        prompts[c.slot - 1] ?? prompts[0] ?? "",
        permitePessoa,
        post.promessa_visual ?? "(promessa não preenchida — reprove pelo item 8)",
      );
    } catch (e) {
      await patch(post.id, { erro: `slot ${c.slot}: ${String(e).slice(0, 400)}` });
      return { id: post.id, ok: false, erro: String(e).slice(0, 200) };
    }

    const aprovado = r.parsed.veredito === "aprovado";
    await logQa(post.id, c.slot, aprovado ? "aprovado" : "reprovado", r.parsed.item, r.parsed.correcao, r.uso);
    if (!aprovado) reprovas.push(`slot ${c.slot}: ${r.parsed.correcao ?? `item ${r.parsed.item}`}`);
  }

  if (!reprovas.length) {
    await patch(post.id, { status: "imagem_aprovada", erro: null });
    return { id: post.id, ok: true, veredito: "aprovado", slots: cenarios.length };
  }

  // Reprovou. Volta para geração se ainda tem tentativa; senão para de queimar crédito.
  const estourou = (post.tentativas_imagem ?? 0) >= MAX_TENTATIVAS;
  await patch(post.id, {
    status: estourou ? "parado_revisao_humana" : "briefing_pronto",
    erro: estourou ? `QA reprovou ${MAX_TENTATIVAS}x — ${reprovas.join(" | ")}` : reprovas.join(" | "),
  });

  return { id: post.id, ok: true, veredito: "reprovado", estourou, reprovas };
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
      `?status=eq.imagem_hospedada` +
      `&select=id,imagem_gpt_url,cenarios,prompt_imagem,prompts_cenario,tentativas_imagem,` +
      `promessa_visual,` +
      `social_modelo(codigo,permite_pessoa)` +
      `&order=atualizado_em.asc&limit=${n}`,
    { headers: rest },
  );

  if (!fila.ok) {
    return new Response(JSON.stringify({ erro: `fila ${fila.status}: ${await fila.text()}` }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }

  const posts = await fila.json();
  const resultados = await Promise.all(posts.map(avaliar));

  return new Response(JSON.stringify({ avaliados: resultados.length, resultados }), {
    headers: { "Content-Type": "application/json" },
  });
});
