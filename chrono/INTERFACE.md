# Chrono — datador em três peças sobre o molde existente

Deliverable: `chrono-datador-aneis.html` (apresentação).
Scripts de medição: `medicao/` · geometria vetorizada usada no desenho: `medicao/geo.json`.

## Origem

Três malhas STL binárias fornecidas em 31/08/2026, montagem `Mont pote com valvula`,
cavidade 1 do `Pote 025 Pequeno`:

| Peça | Triângulos | Envelope (mm) | Volume | Massa PP 0,905 |
|---|---|---|---|---|
| Tampa | 147.764 | 122,15 × 185,07 × 9,02 | 26.285 mm³ | 23,79 g |
| Corpo | 100.998 | 122,71 × 203,29 × 37,46 | 37.889 mm³ | 34,29 g |
| Válvula (prova) | 45.864 | 44,16 × 38,09 × 5,67 | 2.258 mm³ | 2,04 g |

Parede constante medida em tampa e corpo: **0,91–0,92 mm**.
Capacidade do corpo até a borda: **0,58 L**.

## O assento (poço da válvula) — é a interface do datador

Coordenadas relativas ao centro do poço (X = 61,97 · Z = 102,68 no sistema do STL).
"12 h" = +Z (lado do respiro). "6 h" = −Z (lado da aba de dedo da válvula).

| Elemento | Cota medida |
|---|---|
| Furo do poço, trecho reto | Ø38,54 · Y 33,00 → 37,00 |
| Rasgos radiais a 3 h e 9 h | abrem para Ø44,62 · Y 33,5 → 37,0 |
| Rebaixo cônico de topo | Ø38,71 @ Y 37,00 → Ø48,48 @ 37,60 → Ø50,05 @ 38,00 |
| Fundo do poço | topo Y 32,15 · fundo 31,24 |
| Ressalto do respiro (12 h) | topo em Y 35,20 |
| Furo de respiro | Ø8,12 · centro a 12,18 mm do centro do poço, a 12 h |
| Ponto de injeção no fundo | Ø1,78 · a 4,96 mm do centro, a 6 h |
| Plano de rótulo (painel) | Y 38,24 (fundo 37,33) |
| Banda periférica (apoia no aro do corpo) | Y 38,75 / 37,84 — aro do corpo em 37,84 |
| Aro de empilhamento (ponto mais alto) | Y 39,72 |
| Face de topo da válvula hoje | Y 37,23 (−1,01 do plano de rótulo) |
| Face interna da válvula | Y 35,40 (parede 1,83) |

Tolerância de leitura da malha: ±0,03 mm. **Cotas de conferência, não de ferramentaria.**

## As três peças propostas

| Peça | Cotas | Massa |
|---|---|---|
| Pino / travinha | casca = envelope da válvula · cubo Ø11,6 (barbela Ø12,6) · colar Ø24,4/Ø28,4 · 31+12 detentes | 2,30 g |
| Anel de dia | Ø41,0 / Ø28,6 × 0,95 · 31 × 11,613° · passo 3,53 mm | 0,58 g |
| Anel de mês | Ø24,2 / Ø12,0 × 0,95 · 12 × 30,000° · passo 4,74 mm | 0,30 g |

Topo dos anéis em Y 38,18 — 0,06 mm abaixo do plano de rótulo, 1,54 mm abaixo do aro.
Datador 3,18 g contra 2,04 g da válvula: **+1,14 g por tampa**.

## Pendências que bloqueiam

1. Confirmar que o assento é idêntico em todos os tamanhos de tampa da família.
   Sem isso não existem "3 moldes" — existe um datador por pote.
2. Este corpo é de 0,58 L. A regra de litragem do projeto (até 600 ml: −31,5%,
   2 de 22 refs subindo) diz para entrar pela maior tampa da família, não por esta.
3. Datador e válvula ocupam o mesmo poço: é um ou outro no mesmo SKU.
4. Contraste dos números tem de vir de acabamento de molde (caractere polido em campo
   texturizado), não de tampografia.

## Nota de sessão

O MCP do Sankhya não subiu nesta sessão — nenhum número de ERP foi consultado.
Faturamento, margem, litragem, safra, cores e ocupação citados na apresentação são
conclusões já documentadas em `CLAUDE.md`, citadas e não recalculadas.
Nada foi gravado em `pdp_lancamento`.
