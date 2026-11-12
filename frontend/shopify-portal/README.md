# Portal Nitron no tema Shopify

Versão em seção de tema do artefato "Portal Nitron".

| Arquivo | Vai para o tema em |
|---|---|
| `sections/portal-nitron.liquid` | `sections/` |
| `templates/page.portal.json` | `templates/` (modelo de página "portal") |
| `assets/portal-institucional.jpg`, `assets/portal-loja.jpg` | `assets/` (fallback quando nenhuma imagem é escolhida no editor) |
| `assets/nitron-logo.png` | não precisa: o logo é do cabeçalho do tema |

O cabeçalho, a navegação e o rodapé do artefato **não** entram: no site eles já vêm do tema.

## Como publicar (rota segura)
1. Duplicar o tema ativo (nunca editar o tema publicado direto).
2. Subir os 4 arquivos na cópia.
3. Opção A, página própria: criar uma página "Portal" usando o modelo `page.portal`.
   Opção B, home: no editor de temas, Página inicial > Adicionar seção > "Portal Nitron".
4. Conferir a prévia no celular e no desktop e então publicar a cópia.
