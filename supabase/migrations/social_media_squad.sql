-- Squad de social media — tabelas de estado do fluxo Claude → n8n → OpenAI → Canva
-- Projeto: bwbeieumxcuomtrvlqxs (integracao-crm-sankhya)
-- Prefixo social_ para não colidir com as ~130 tabelas do CRM.
-- Aplicada em 28/08/2026 via MCP do Supabase. Ver SOCIAL.md.

create table if not exists social_post (
  id                bigserial primary key,

  -- pauta (estrategista-conteudo)
  marca             text not null default 'NITRON',   -- brand kit do Canva
  canal             text not null,                    -- instagram_feed | instagram_story | instagram_reels | facebook_feed
  formato           text not null,                    -- estatico | carrossel | reels
  data_prevista     date,
  pauta             text not null,
  angulo            text,                             -- gancho; cite o vetor quando houver (ex.: 'V1 Válvula')
  codprod           integer,
  referencia        text,                             -- SEMPRE completa: 233.012.001 — nunca truncar para 233
  evidencia         text not null,                    -- o dado com número que sustenta a pauta

  -- copy (redator-legenda)
  legenda           text,
  hashtags          text[],
  cta               text,
  claim_check       jsonb,                            -- {claims:[], veredito:, motivo:, substituicao:}

  -- briefing visual (diretor-arte)
  prompt_imagem     text,
  foto_produto_url  text,                             -- produto_foto.link_principal — foto REAL do SKU
  template_ref      text,                             -- design mestre do Canva

  -- execução (n8n + montador-canva)
  imagem_gpt_url    text,                             -- cenário gerado, em bucket público
  canva_design_id   text,
  arte_url          text,

  status            text not null default 'planejado',
  tentativas_imagem integer not null default 0,
  erro              text,                             -- ultima falha tecnica (geracao, upload, QA)

  criado_por        text,
  criado_em         timestamptz not null default now(),
  atualizado_em     timestamptz not null default now(),

  constraint social_post_status_ck check (status in (
    'planejado','copy_pronta','briefing_pronto',
    'imagem_gerada','imagem_hospedada','imagem_aprovada','imagem_reprovada',
    'arte_montada','aprovado_maquina','publicado',
    'briefing_reprovado','copy_reprovada','arte_reprovada',
    'parado_revisao_humana','descartado'
  )),
  constraint social_post_tentativas_ck check (tentativas_imagem between 0 and 3),
  constraint social_post_evidencia_ck   check (length(trim(evidencia)) > 0)
);

comment on table social_post is
  'Estado de cada post de social. Fluxo em SOCIAL.md. Post sem evidencia nao entra.';

create index if not exists social_post_fila_idx
  on social_post (status, data_prevista);

-- log de cada avaliação (QA por visão e revisor-social)
create table if not exists social_qa (
  id            bigserial primary key,
  post_id       bigint not null references social_post(id) on delete cascade,
  etapa         text not null,        -- imagem_crua | arte_montada
  avaliador     text not null,        -- claude-sonnet-5 (n8n) | revisor-social | humano
  veredito      text not null,        -- aprovado | reprovado
  item_falhou   text,                 -- item da checklist
  correcao      text,                 -- instrução concreta, não "está ruim"
  bruto         jsonb,
  criado_em     timestamptz not null default now(),
  constraint social_qa_veredito_ck check (veredito in ('aprovado','reprovado'))
);

create index if not exists social_qa_post_idx on social_qa (post_id, criado_em desc);

-- RLS: igual às pdp_* — ligado, e só política de SELECT.
-- Escrita acontece pelo service_role (n8n, server-side) ou pelo MCP.
alter table social_post enable row level security;
alter table social_qa   enable row level security;

drop policy if exists social_post_sel on social_post;
create policy social_post_sel on social_post
  for select to anon, authenticated using (true);

drop policy if exists social_qa_sel on social_qa;
create policy social_qa_sel on social_qa
  for select to anon, authenticated using (true);

-- atualizado_em
create or replace function social_post_touch() returns trigger
language plpgsql as $fn$
begin
  new.atualizado_em := now();
  return new;
end;
$fn$;

drop trigger if exists social_post_touch_tg on social_post;
create trigger social_post_touch_tg before update on social_post
  for each row execute function social_post_touch();
