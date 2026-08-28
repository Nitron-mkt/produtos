-- Agendamento das duas Edge Functions do fluxo de social media.
--
-- NÃO APLICAR antes de setar os secrets OPENAI_API_KEY e ANTHROPIC_API_KEY no projeto.
-- Cron sem secret = erro 500 a cada 5 minutos poluindo net._http_response.
--
-- O bloco reaproveita o header Authorization de um job já existente, então a chave
-- nunca é escrita neste arquivo nem aparece em log de conversa.

do $$
declare
  auth  text;
  base  text := 'https://bwbeieumxcuomtrvlqxs.supabase.co/functions/v1';
begin
  select (regexp_match(command, 'Bearer ([A-Za-z0-9_.\-]+)'))[1]
    into auth
    from cron.job
   where jobname = 'fila-processar-1min'
   limit 1;

  if auth is null then
    raise exception 'header Authorization não encontrado em fila-processar-1min — confira o jobname';
  end if;

  -- gera o cenário: de 5 em 5 minutos, 3 posts por tick
  perform cron.schedule('social-imagem-5min', '*/5 * * * *', format(
    $f$select net.http_post(
      url := '%s/social-imagem?n=3',
      headers := jsonb_build_object('Content-Type','application/json','Authorization','Bearer %s'),
      body := '{}'::jsonb,
      timeout_milliseconds := 170000);$f$, base, auth));

  -- QA do cenário: deslocado 2 minutos, para avaliar o que acabou de ser gerado
  perform cron.schedule('social-qa-5min', '2-59/5 * * * *', format(
    $f$select net.http_post(
      url := '%s/social-qa?n=5',
      headers := jsonb_build_object('Content-Type','application/json','Authorization','Bearer %s'),
      body := '{}'::jsonb,
      timeout_milliseconds := 120000);$f$, base, auth));
end $$;

-- Conferir:
--   select jobname, schedule, active from cron.job where jobname like 'social-%';
-- Desligar sem apagar:
--   update cron.job set active = false where jobname like 'social-%';
