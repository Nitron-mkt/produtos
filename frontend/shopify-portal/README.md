# Portal Nitron no tema Shopify

Versão em seção de tema do artefato "Portal Nitron".

| Arquivo | Vai para o tema em |
|---|---|
| `sections/portal-nitron.liquid` | `sections/` |
| `templates/index.json` | `templates/` — **substitui a página inicial**: a home passa a ser só o portal dividido |
| `templates/page.portal.json` | `templates/` (opcional: o mesmo portal como página separada) |
| `assets/portal-institucional.jpg`, `assets/portal-loja.jpg` | `assets/` (fallback quando nenhuma imagem é escolhida no editor) |
| `assets/nitron-logo.png` | não precisa: o logo é do cabeçalho do tema |

O cabeçalho, a navegação e o rodapé do artefato **não** entram: no site eles já vêm do tema.

## Como publicar (rota segura)
1. Duplicar o tema ativo (nunca editar o tema publicado direto).
2. Subir os 4 arquivos na cópia.
3. Decisão tomada em 12/11/2026: o portal **é a página inicial**. Antes de trocar o
   `templates/index.json`, guardar o original da cópia como `templates/index.loja-antiga.json`
   para poder voltar.
4. Conferir a prévia no celular e no desktop e então publicar a cópia.
