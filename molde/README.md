# Tampa de Correr — modelo 3D paramétrico

Conceito de tampa com **porta de correr** e **duas juntas de TPE** para a plataforma
**Aro Comum** (aro 105 × 206 mm, R14 — a base do Porta Sabão 008).

A abertura vive **dentro da mesa da tampa**, cercada por gargalo e junta própria — por isso
o abraço no aro continua inteiro, 590 mm, ao contrário da tampa deslizante do estudo original,
que interrompia a canaleta em 67 mm para o cursor poder sair.

> **Status: conceito.** Nada aqui foi validado em molde, ensaio ou tryout, e nada foi
> gravado em `pdp_lancamento`. Ver *Pendências*.

---

## Como regenerar

```bash
cd molde
python3 pecas.py       # STL das 6 peças + web/geo.js (blob do visualizador)
python3 secao.py       # web/secao-aa.svg e secao-bb.svg — cortes cotados
python3 build_html.py  # ../analise/06-tampa-portinhola.html (artefato completo)
python3 preview.py     # PNGs de conferência (rasterizador próprio, sem dependência)
```

Python 3 puro, sem dependência externa. **`pecas.py` é a fonte única das cotas**: STL, render
3D, cortes, tabelas de cota e o dimensionamento da trava saem do mesmo dicionário `P`.

| Arquivo | Papel |
|---|---|
| `geo.py` | kernel: contorno arredondado, varredura de perfil com amplitude local, prismas em X e Y, loft, STL |
| `pecas.py` | **as cotas** + as seis peças + métricas, forças e tensões |
| `secao.py` | cortes A-A (vedação) e B-B (trava) |
| `preview.py` | rasterizador z-buffer para conferir a malha sem abrir CAD |
| `stl/` | `corpo`, `tampa`, `cursor`, `trava`, `junta_aro`, `junta_boca` — binário, mm, Z para cima |

---

## Por que TPE muda o projeto inteiro

A versão anterior vedava com um lábio flexível de PP em interferência de 0,35 mm. Funciona —
até o polipropileno relaxar. **PP sob deformação constante perde tensão**: o lábio continua
encostando, com menos pressão a cada mês. É a explicação mais provável para as duas únicas
quedas dentro da plataforma de válvula, `176.024.001` e `210.024.001`, que caem 57% e 39%
**com a melhor margem da família**.

Um elastômero comprimido 29% perde força nas primeiras semanas e depois **estabiliza**. É por
isso que todo pote que alega hermeticidade tem borracha.

O custo é um segundo material na casa — e a regra que protege os **R$ 2,63 M/ano** do ciclo de
moído é que o refugo seja mono-resina. Por isso a junta entra **montada, não bi-injetada**.

---

## As três coisas que vedam

**1 · Junta do aro — 590 mm, aperto 0,40 mm (29%).**
Anel de TPE 1,4 × 1,4 mm numa canaleta na face inferior da mesa. O topo do aro entra 0,40 mm
nele e para quando a mesa encosta no aro: **o aperto é geometria**, não depende de força de
trava nem de quanto o consumidor apertou. A canaleta tem 15% de folga de volume, então o
elastômero nunca fica hidraulicamente preso. Abre para baixo — **saída reta, sem gaveta**.
O lábio de PP que antes vedava virou guia: centra a tampa e protege a junta no encaixe.

**2 · Junta da boca — 251 mm, comprimida só no fim do curso.**
O cursor corre 56 mm sobre **quatro patins de 0,55 mm**, apoiados em duas pistas elevadas;
nessa altura passa 0,15 mm acima da junta, sem encostar. As pistas têm folga exatamente onde
os quatro patins pousam na posição fechada, então **os quatro descem juntos** — o cursor não
inclina em nenhum ponto do curso e a junta vê compressão, nunca arrasto. Junta que arrasta,
desgasta.

**3 · As duas travas de correr — 130 N aplicados com 23 N de dedo.**
Comprimir 590 mm de elastômero a 29% custa ~130 N. Ninguém fecha isso empurrando a tampa —
e é por isso que todo pote hermético tem trava, não encaixe.

---

## A trava, dimensionada

A lingueta entra sob a aba do corpo e sua ponta sobe **0,55 mm em 8 mm** de avanço: rampa de
**2,9°**, vantagem mecânica ≈ 14×. E 2,9° está muito abaixo do ângulo de atrito PP-PP (~16°),
então a trava é **autotravante** — não volta com vibração nem com o pote deitado na sacola.

| Grandeza | Valor | Base |
|---|---|---|
| Aperto da junta do aro | 130 N | TPE 45A a 29%, 590 mm, 0,22 N/mm |
| Aperto da junta da boca | 55 N | aplicado pelos patins |
| Por trava | 65 N | 2 travas, faces longas |
| Rampa | 2,9° | autotravante |
| Dedo para travar / destravar | 23 N / 16 N | atrito ajuda a segurar, atrapalha a soltar |
| Carga de projeto | 195 N | 3× a força de fechamento |
| Lingueta | 24 × 3,2 mm · braço 3,64 mm | engate 1,61 mm |
| Tensão de flexão | 17,3 MPa | PP escoa a ~30 MPa — folga de 1,7× |
| Cisalhamento | 2,5 MPa | PP resiste a ~25 MPa |

**Duas travas, uma em cada face longa, no meio do vão.** Não é estética: é onde a tampa
flexiona. Nas faces curtas o vão é de 105 mm e os raios de canto já enrijecem; nas longas são
206 mm que a junta empurra para cima.

---

## Ferramentaria

| Peça | Material | Área proj. | Fech. | Massa | Saída negativa |
|---|---|---|---|---|---|
| Corpo AC-21 | PP | 214,6 cm² | ≈ 75 t | 116,0 g | aba: **2 gavetas** nas faces longas — ou extração forçada, a ensaiar |
| Tampa | PP | 214,6 cm² | ≈ 75 t | 49,7 g | trilho da trava: **2 gavetas retas** em Y · lábio do trilho da porta 0,40 mm: extração forçada |
| Cursor | PP | 60,8 cm² | ≈ 21 t | 10,1 g | nenhuma |
| Trava de correr | PP | 9,5 cm² | ≈ 4 t | 0,78 g (×2) | nenhuma — 8 cavidades |
| Juntas (molde família) | TPE 45A | — | — | 0,90 + 0,38 g | anéis montados |

Conjunto: **178,6 g em 7 peças**, 4 cliques de montagem (cursor, 2 travas, 2 juntas).

**Montada, não bi-injetada.** A bi-injeção (2K) sobremolda o elastômero direto na tampa —
acabamento superior, zero montagem — e exige injetora de dois canhões com mesa rotativa, que
este parque não tem. Pior: o refugo passa a ser **PP contaminado com TPE**. A rota escolhida é
o anel injetado à parte, em molde família, com o Karinprene shore 45 que já está cadastrado
(`CODPROD 997`) e nunca foi comprado. O PP continua mono-resina.

**Ponto de injeção.** A mesa tem um furo de 62 × 64 mm no meio. Todo furo gera linha de solda
a jusante, e linha de solda é a região mais fraca e mais permeável da peça. Nenhuma pode cair
sobre a canaleta da junta. Simulação de preenchimento antes de cortar aço.

---

## Claim

Com junta de elastômero, "hermético" deixa de ser retórica — desde que exista o ensaio; o
art. 36 do CDC cobra o dado técnico de quem alega.

**Sustentável com ensaio:** hermético *com a porta fechada* (perda de massa, 30 dias) · não
vaza deitado (24 h em cada face) · continua vedando depois de guardado (30 dias a 40 °C —
mede o *compression set*, que governa a vida da junta) · a trava não abre na queda (3 × 1,0 m
com 80% de carga).

**Não escrever sem ciclagem:** "hermético" sem qualificar (com a porta aberta é um pote
aberto) · "conserva a vácuo" (não há válvula) · micro-ondas fechado · "mantém crocância por X
dias".

---

## Pendências

1. **Medir a força da junta com a resina real.** Todo o dimensionamento da trava sai de
   **0,22 N/mm**, ordem de grandeza de catálogo. Se o real for o dobro, a força de dedo vai de
   23 para 46 N e a trava fica dura demais. Anel piloto + célula de carga, antes do aço.
2. **O aro tem de sair do desenho, não do cadastro.** O cadastro do 008 diz 20,7 cm; a
   plataforma foi desenhada em 20,6. Um milímetro é mais de duas vezes o aperto da junta.
3. **Ciclagem da junta da boca** — 5.000 ciclos com estanqueidade medida no início, meio e fim.
   A junta do aro é comprimida e liberada; a da boca vê o cursor descer e subir em cima dela.
   **É o elo mais fraco do produto.**
4. **Compression set do Karinprene a 40 °C** — 30 dias sob aperto, medir o retorno.
5. **Dois materiais mudam a conta do moído.** A rota de anel montado protege o ciclo, mas cria
   um segundo fluxo de refugo que precisa ser separado no chão de fábrica. Se a separação
   falhar, a perda não é o TPE — é o PP contaminado.
6. **O veredito vigente de Potes é "só kit"** (`pdp_linha`, score 8). Cinco moldes para um SKU
   avulso contraria isso; a versão compatível é a tampa servir os quatro corpos do aro comum.
7. **Payback de cinco moldes com 0,7% de acerto** na última safra. Este modelo mostra que a
   peça funciona; não mostra que ela se paga.
