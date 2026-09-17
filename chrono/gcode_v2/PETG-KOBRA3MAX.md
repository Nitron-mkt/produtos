# PETG na Kobra 3 Max — por que descolava, e o que mudou

Você estava imprimindo **PETG** com um perfil de **PLA**, numa mesa configurada como
**255 × 255** quando a Max tem **420 × 420**. Lavar a base não ia resolver isso — e
pelo que você descreveu, a base já estava limpa.

## As três coisas que descolavam a peça

| | Estava (PLA) | Agora (PETG) | Por quê |
|---|---|---|---|
| **Mesa** | 60 / 65 °C | **80 °C** | PETG só agarra acima de ~70. A 60 ele encosta e solta. É o maior fator, isolado. |
| **Bico** | 205 / 210 °C | **240 / 245 °C** | O rótulo do seu CR-PETG diz **230–250**. A 210 o PETG mal escoa: sai pouco material e ele não solda na chapa nem na camada de baixo. |
| **Ventoinha** | **100%** | **30–45%**, desligada nas 4 primeiras | Esta é a que descola **no meio da impressão**. PETG resfriado a 100% contrai e as bordas levantam puxando a peça. |

E mais duas correções de máquina:

| | Estava | Agora |
|---|---|---|
| Mesa | 255 × 255 × 260 (Kobra 3 comum) | **420 × 420 × 500** (Max) |
| Onde a peça cai | X 127,5 Y 127,5 | **X 210 Y 210 — o centro real da Max** |

Imprimir a 127,5/127,5 numa mesa de 420 joga a peça bem fora do centro. Numa mesa
grande a borda aquece menos e o nivelamento é menos fiel ali — sozinho já atrapalha.

Confira no painel que a sua Max é mesmo **420 × 420 × 500**. Se for outro número me
diga que eu recentro; a peça tem 45 mm, então ela cabe em qualquer caso, o que muda
é só ficar no meio.

## Ajustes finos que vieram junto

| | Estava | Agora | Por quê |
|---|---|---|---|
| Multiplicador de extrusão | 1,00 | **0,95** | PETG infla mais que PLA na mesma vazão |
| Retração | 1,5 mm a 35 mm/s | **1,2 mm a 30 mm/s** | PETG odeia retração rápida: entope e faz fio |
| Preenchimento | 35 mm/s | **30 mm/s** | PETG solda melhor devagar |
| Camada fina demais | espera 20 s | **25 s** | com ventoinha baixa, camada pequena precisa de mais tempo |

## Ordem para hoje

1. **`Kobra3Max_PETG_0_Teste_Primeira_Camada.gcode`** — 10 min. Cinco quadrados de
   28 mm numa camada só, agora **centrados em 210/210**. Olhe o cordão: fios fundidos
   sem vão entre eles = certo; vão aparecendo = baixar o Z offset de 0,02 em 0,02.
2. Depois os três: válvula (56 min), rodinha (17 min), ponteira (13 min).

## O que NÃO fazer com PETG

- **Não tirar a peça com a mesa quente.** A 80 °C o PETG está colado de verdade;
  espere a mesa baixar de 50 °C e ela solta quase sozinha. Forçar quente arranca o PEI.
- **Não aumentar mais a ventoinha** achando que melhora o acabamento. Em PETG, mais
  ventoinha é menos adesão entre camadas e mais empeno.
- **Não usar cola** na chapa texturizada com a mesa a 80 °C. Em PETG cola serve de
  **desmoldante**, não de adesivo — é para a peça *não* fundir com a chapa lisa.
- **Não deixar o rolo aberto.** PETG puxa umidade e imprime estalando, com fio e
  bolha. Se o rolo está aberto há semanas, seque antes de culpar a máquina.

## Se ainda descolar depois disso

Nessa ordem: mesa para **85 °C** · Z offset **0,02 mais baixo** · e só então o arquivo
com raft. Mas com mesa a 80 e ventoinha a 30% a chance de precisar é pequena.

## Tudo numa mesa só

`Kobra3Max_PETG_TUDO_numa_mesa.gcode` — **1 h 25 min, 5,40 g**. As três peças na
mesma mesa, com aba de 8 mm em cada.

Sobra bem de espaço na Max: o conjunto ocupa **X 149,9 a 266,4 · Y 159,6 a 262,0**,
centro em (208, 211) — ou seja, tudo no terço central da mesa, que é onde ela aquece
e nivela melhor. Folgas entre as peças **já contando a aba**: 13,5 · 7,6 · 13,2 mm.

Conferido pelo percurso da primeira camada (`../stl_v2/chapa_max_primeira_camada.png`),
não pelo rótulo de objeto do gcode: as três aparecem separadas, com os 12 entalhes da
rodinha e o ícone na ponteira já visíveis.

### Duas ressalvas honestas

**PETG faz fio entre peças.** Com três peças, o bico viaja entre elas a cada camada e
vai deixar teia. Não estraga nada — sai com pinça e um sopro de ar quente — mas
imprimindo separado não acontece.

**Se uma soltar, pode derrubar as outras.** É o risco de qualquer mesa cheia. Como a
causa de descolar era o perfil de PLA e não o arranjo, com mesa a 80 °C e ventoinha a
30% isso deixa de ser provável — mas na primeira rodada com o perfil novo eu imprimiria
**a válvula sozinha** primeiro. Ela é a peça de risco (toca a chapa por só 11 mm² de
face plana) e é a mais demorada. Se ela sair limpa, a mesa cheia sai.
