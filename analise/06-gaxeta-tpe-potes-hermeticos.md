# Projeto Gaxeta TPE — transformar a linha Pote com Travas em hermética

**Fonte do dado interno:** Sankhya produção — TGFCAB/TGFITE/TGFPRO/TGFCUS/TGFTAB/TGFNTA
**Recorte:** empresas 1/2/14, STATUSNOTA='L', TIPMOV V/D, ATUALFIN<>0, sem transferências
intercompany, **sem CODTAB 84 (Avon) e sem CODTAB 3 (exportação)**
**Janela:** 12 meses móveis até 06/09/2026
**Dimensões:** catálogo `produto.nitron.com.br` (páginas 41–52), conferidas contra a descrição do ERP

> **Ideia original (Marketing):** bobina de fita TPE extrudada, seção constante ~1 mm, cortada no
> comprimento e aplicada em todas as tampas da linha com trava — para não fazer um molde por tampa.
>
> **Veredito da revisão 1:** a ideia central está certa e é a rota mais barata que existe para
> esse objetivo. Três coisas dentro dela precisam mudar — a **seção do perfil**, a **rota de
> suprimento** e a **ordem dos testes**. Seções 3, 5 e 6.

---

## ⚠️ REVISÃO 2 — o dado de mercado derruba a premissa comercial

A revisão 1 assumiu que "hermético" é um claim raro que sustenta prêmio de preço, apoiada na
afirmação do CLAUDE.md de que **só 3% dos anúncios diziam "hermético"**.

**Essa afirmação estava errada, e o erro era de acento.** A contagem original usou
`ILIKE '%hermetico%'`, sem acento, e achou 7. Com `~* 'herm[ée]tic'`, são **164 de 267 — 61,4%**.
Verificado duas vezes em consultas independentes; CLAUDE.md corrigido no mesmo commit.

Isso não é um detalhe. **A premissa comercial inteira do projeto era essa.** Quatro cortes
independentes, todos na mesma direção:

| Corte | n | Resultado |
|---|---|---|
| "Hermético" no mercado | 267 potes | **61,4% já dizem** — table stakes, não diferencial |
| R$/litro com claim vs sem, única faixa com contraste | 5 | **−3,5%** |
| R$/pote, 22 kits plásticos, com gaxeta vs sem | 22 | **−0,8%** |
| **Mesma marca (Vie idéale): kit com silicone vs kit com trava** | 1 par | **−17%** — a versão com gaxeta é a mais barata |

**Não há evidência de que a gaxeta sustente preço. Há evidência fraca de que ela o reduza.**

E o dado de uso é pior que o de preço. Em 600 avaliações coletadas (`pdp_ml_review`):

| Anúncio | Trava | Gaxeta | "não veda" (% das negativas) |
|---|---|---|---|
| Amobox Kit 12 | não | não | 27,1% |
| **Electrolux Kit 12** | não | **silicone** | **25,6%** |
| **Plasútil Kit 12 travas** | **sim** | não | **0%** |
| **Plasútil porta-frios travas** | **sim** | não | **0%** |

**A gaxeta não é o que resolve — a trava é.** A Electrolux tem vedação de silicone e reclama-se
dela quase tanto quanto do produto que não tem nada; os dois produtos com trava e sem gaxeta têm
zero reclamação de vedação. **A Nitron já tem a peça que resolve o problema percebido.**

### A tesoura — e por que ela reorganiza o projeto

O Plasútil porta-frios veda ("ele veda muito") e paga um preço por isso: **32,3% das suas
negativas são sobre dificuldade de abrir** — "precisa fazer muita força", "travas laterais
quebraram".

Isso conecta com a conta de engenharia da §3.2 por outro caminho e chega ao mesmo lugar:

> **A força que veda é a mesma força que trava o produto na mão do consumidor.**
> Adicionar gaxeta a uma trava existente move o produto para o quadrante do Plasútil —
> vedação melhor, abertura pior, trava sob tensão maior — sem molde redesenhado para a nova força.

E fecha um achado que estava aberto no CLAUDE.md sem explicação: as refs `176.024.001` e
`210.024.001` (**trava + válvula**) são as **únicas duas quedas** (−57% e −39%) numa plataforma que
cresce +49,9%. A hipótese **"trava + vedação extra = duro de abrir"** agora tem suporte externo
independente, e é mais econômica que as duas que estavam registradas (conflito funcional da
válvula, creep do PE). **A Nitron pode já ter rodado este experimento duas vezes e perdido as duas.**

### O que sobrevive

1. **O teste de bancada de §6.1 — e agora ele vale mais, não menos.** A pergunta mudou: não é só
   "a trava fecha?", é **"quanto sobe a força de abrir?"**. Mesmo protocolo, mesmos R$ 200,
   uma medição a mais. É a única coisa que decide isto empiricamente em vez de por analogia.
2. **Os achados de custo da §9**, que independem da gaxeta e provavelmente valem mais que ela.
3. **A rota técnica**, se algum dia houver razão para vedar: perfil de lábio fino, fita comprada
   em bobina, rework de molde. Isso continua correto e barato — o que falta é motivo.

### O que não sobrevive

- O business case de "+6% de preço paga a gaxeta". **Não há base de mercado para o +6%.**
  Sem prêmio, a gaxeta é custo puro: R$ 69,3 k/ano nas 4 tampas prioritárias, **−4 pontos de MB**.
- O claim "hermético" como diferencial de gôndola. Seis em cada dez concorrentes já o usam.

**Recomendação desta revisão: não aprovar o projeto como upgrade de linha.** Rodar o teste de
R$ 200 para medir a tesoura abrir/vedar — o resultado interessa de qualquer forma, porque explica
176/210 e informa qualquer mexida futura em trava. Decidir depois, com o número na mão.
Parecer do `curador-portfolio` pendente; nada gravado em `pdp_lancamento`.

---

## 1. O universo — 18 tampas, não 80 SKUs

A primeira coisa que o dado mostra é que o problema é bem menor do que parece. A linha com trava
tem ~80 SKUs vendendo, mas **só 18 geometrias de tampa**, porque cor não muda tampa e porque
**Raso e Alto compartilham a mesma boca**:

| Boca (C×L cm) | Corpo raso | Corpo alto | Mesma tampa? |
|---|---|---|---|
| 14,0 × 10,0 | 231 — 270 ml | 154 — 460 ml | sim |
| 17,0 × 11,0 | 232 — 500 ml | 155 — 850 ml | sim |
| 22,0 × 14,0 | 233 — 1,1 L | 156 — 2,2 L | sim |
| 26,0 × 18,0 | 234 — 2,3 L | 151 — 4,3 L | sim |

Isso é o achado que torna o projeto barato: **4 tampas cobrem 8 corpos**, e as refs 157 (Tomatinho)
e 158 (Feijão) usam a boca 17×11 do 155. Uma intervenção por tampa serve dois produtos.

### Faturamento 12 M por geometria de tampa

| Tampa | Fat. 12 M | Unid. | Perímetro | Preço méd. | MB | Lucro bruto | Litragem na janela? |
|---|---:|---:|---:|---:|---:|---:|:--|
| **RET-C 22,0×14,0** | **R$ 774.211** | 155.949 | 67,7 cm | 4,96 | 47,7% | R$ 369.123 | **1,1 L e 2,2 L — as duas** |
| **RET-D 26,0×18,0** | **R$ 628.778** | 80.346 | 82,7 cm | 7,83 | 35,3% | R$ 222.143 | 2,3 L sim · 4,3 L não |
| RET-B 17,0×11,0 | R$ 618.670 | 170.465 | 52,6 cm | 3,63 | 50,1% | R$ 309.799 | não (500/850 ml) |
| **QUA-3770 20,0×19,0** | **R$ 326.047** | 68.257 | 73,3 cm | 4,78 | 40,6% | R$ 132.436 | **1,8 L** |
| **UF-215 25,0×16,5** | **R$ 285.918** | 42.020 | 78,0 cm | 6,80 | 45,2% | R$ 129.183 | **2,1 L** |
| UF-216 30,0×20,0 | R$ 251.633 | 24.625 | 94,0 cm | 10,22 | 39,4% | R$ 99.039 | não (4 L) |
| RET-A 14,0×10,0 | R$ 239.360 | 81.138 | 45,1 cm | 2,95 | 60,8% | R$ 145.645 | não (270/460 ml) |
| RED-2270 ⌀22,5 | R$ 230.424 | 40.882 | 80,8 cm | 5,64 | **24,6%** | R$ 56.642 | 2,3 L sim, **mas MB 24,6%** |
| UF-217 35,0×24,0 | R$ 228.190 | 13.409 | 110,9 cm | 17,02 | 60,2% | R$ 137.277 | não (6,9 L) |
| QUA-3780 16,0×14,0 | R$ 194.512 | 52.431 | 56,4 cm | 3,71 | 48,9% | R$ 95.132 | não (860 ml) |
| QUA-3760 25,0×24,0 | R$ 184.506 | 25.816 | 92,1 cm | 7,15 | 46,4% | R$ 85.620 | limite (3,7 L) |
| RED-2280 ⌀17,5 | R$ 118.351 | 28.120 | 63,9 cm | 4,21 | 52,3% | R$ 61.944 | 1,1 L, volume baixo |
| QUA-3790 12,0×11,0 | R$ 95.206 | 39.373 | 43,2 cm | 2,42 | 56,8% | R$ 54.039 | não (360 ml) |
| KIT-190 (3 pçs) | R$ 54.252 | 3.950 | usa A+B+C | 13,73 | 60,7% | R$ 32.908 | herda |
| DIV-212 600 ml | R$ 41.559 | 5.645 | ~52,6 cm* | 7,36 | 70,5% | R$ 29.309 | não |
| RED-2290 ⌀13,5 | R$ 38.095 | 12.892 | 48,9 cm | 2,95 | 38,0% | R$ 14.491 | não (450 ml) |
| VAL-176 600 ml | R$ 31.234 | 7.542 | ~52,6 cm* | 4,14 | 65,2% | R$ 20.374 | não |
| VAL-210 788 ml | R$ 15.504 | 1.826 | ~52,6 cm* | 8,49 | 60,7% | R$ 9.405 | não |
| **TOTAL** | **R$ 4.356.450** | **854.686** | | | **46,0%** | **R$ 2.004.508** | |

\* perímetro estimado — as refs 176, 210 e 212 não têm dimensão no catálogo consultado. Medir na
fábrica antes de encomendar fita.

Perímetro calculado como 2·(C+L) com desconto de 6% pelo raio de canto. Confirmar com a peça física.

---

## 2. Por onde começar — as 4 tampas prioritárias

Cruzando faturamento com a **janela de litragem** (a regra mais forte do projeto: 1,1–3,5 L cresce
+28,9% e +56,5%; abaixo de 1 L cai −31,5%), o recorte é claro:

| Prioridade | Tampa | Produtos servidos | Fat. 12 M | Peças/ano |
|---|---|---|---:|---:|
| 1 | RET-C 22×14 | Raso 1,1 L (233) + Alto 2,2 L (156) | R$ 774.211 | 155.949 |
| 2 | RET-D 26×18 | Raso 2,3 L (234) + Alto 4,3 L (151) | R$ 628.778 | 80.346 |
| 3 | QUA-3770 20×19 | Quadrado 1,8 L | R$ 326.047 | 68.257 |
| 4 | UF-215 25×16,5 | Ultraforte 2,1 L | R$ 285.918 | 42.020 |
| | **soma** | | **R$ 2.014.954** | **346.572** |

**4 tampas = 46% do faturamento da linha com trava.** Todas na janela de litragem que cresce.

**RED-2270 (2,3 L, R$ 230 k) fica fora da primeira onda** apesar de estar na janela: MB de 24,6%,
a pior das 18, puxada pelo 2270.012.003 preto (custo R$ 5,80 contra R$ 2,95 do transparente).
Gaxeta não conserta margem de 24,6% — essa referência precisa de investigação de custo antes,
não de upgrade de produto. Fica como achado aberto (seção 9).

**RET-B (17×11, R$ 618.670) é a segunda maior da linha e fica de fora** por litragem: 500 ml e
850 ml estão na faixa que cai 31,5%. Contrariar a regra de litragem aqui custaria a onda inteira.
Se o piloto der certo, RET-B entra na segunda onda pelo argumento de marmita/lancheira — que é
uso onde "não vaza" vale mais do que o volume sugere. Não antes.

---

## 3. A fita — o que está certo e o que precisa mudar

### 3.1 O que está certo: uma seção serve todas as tampas ✅

Os perímetros vão de 43,2 cm a 110,9 cm. **Isso é comprimento de corte, não geometria diferente.**
Uma única seção extrudada, cortada em 18 comprimentos, cobre a linha inteira. A intuição está
correta e é o núcleo do projeto: elimina a necessidade de um molde de gaxeta por tampa.

### 3.2 O que precisa mudar: a fita não pode ser chapada de 1 mm ⚠️

Aqui está o erro que estragaria o projeto na bancada. Uma fita maciça de 1 mm precisa de muita
força para deformar, e a força de fechamento **é fornecida pelas travas, que já existem e não
mudam**.

A conta: vedação de líquido a baixa pressão pede ~2–5 N por cm de perímetro com perfil maciço.
Em RET-C (67,7 cm) isso é **135 a 340 N** de força de fechamento distribuída. Um clip de PP
injetado entrega tipicamente 20–60 N. **Com uma ou duas travas, não chega perto.**

Um **lábio de vedação de parede fina** (0,6–0,8 mm) pede 0,5–1,5 N/cm — em RET-C, **34 a 100 N**.
Isso está dentro do que as travas atuais podem dar. É a diferença entre o projeto funcionar e não
funcionar, e não custa nada: é a mesma bobina, mesma extrusão, mesmo material, outra ferramenta
de perfil.

**Perfil recomendado para orçar:**

| Parâmetro | Valor | Por quê |
|---|---|---|
| Material | TPE-S (SEBS) shore A 45–55 | é o CODPROD 997 Karinprene já cadastrado; SEBS é base PP, compatível com o parque |
| Pé de encaixe | 1,15–1,25 mm sobre canal de 1,00 mm | interferência de 15–25% segura sem cola |
| Altura do lábio | 1,2–1,6 mm acima da face | **limitada pelo curso livre da trava — medir antes (§6.1)** |
| Parede do lábio | 0,6–0,8 mm | é o que baixa a força de fechamento para o que a trava tem |
| Deflexão de projeto | 20–30% da altura | faixa onde TPE-S veda sem deformação permanente |
| Massa linear | ~2,5 g/m | base de todo o custeio abaixo |

Barbas (dentes) no pé, não cola: **adesivo não sobrevive a lava-louças e micro-ondas**, e uma
gaxeta que descola vira reclamação de campo e devolução — exatamente o risco que a lição nº 7 do
CLAUDE.md descreve (peça removível não carrega função de segurança). O encaixe tem que ser
mecânico.

### 3.3 Onde a fita mora: **rework de molde, não molde novo**

A fita precisa de um canal na tampa. Isso **não é um molde novo** — é usinar um sulco no postiço
da tampa que já existe. Ordem de grandeza: **R$ 5–12 k por molde**, contra R$ 80–250 k de um
molde novo. É a diferença entre este projeto e "fazer tampa nova", e é por isso que ele cabe.

O canal na tampa não muda tonelagem nem material da peça, e a gaxeta entra na **montagem**, não
na injeção. O impacto de processo é pequeno — mas está sendo verificado com o engenheiro de molde
contra o apontamento real (resultado entra na revisão 2 deste documento).

---

## 4. A conta

### 4.1 Custo por peça

Perfil de ~2,8 mm² a 0,90 g/cm³ = **2,5 g/m**. Fita TPE extrudada entregue em bobina:
**R$ 45–70/kg** (central R$ 55).

| Tampa | Perímetro | Material/peça | Mão de obra/peça | **Total/peça** |
|---|---:|---:|---:|---:|
| RET-C | 0,677 m | R$ 0,093 | R$ 0,05–0,15 | **R$ 0,14–0,25** |
| RET-D | 0,827 m | R$ 0,114 | R$ 0,05–0,15 | **R$ 0,16–0,27** |
| QUA-3770 | 0,733 m | R$ 0,101 | R$ 0,05–0,15 | **R$ 0,15–0,26** |
| UF-215 | 0,780 m | R$ 0,107 | R$ 0,05–0,15 | **R$ 0,16–0,26** |

Mão de obra assume aplicação com jiga: 15–25 s/peça manual, 6–8 s semi-automatizada.
**Confirmar com Produção — é a maior incerteza do custeio.**

### 4.2 Quanto o preço precisa subir (tampa RET-C, MB atual 47,7%)

| Gaxeta | Preço +0% | **+6%** | +10% | +15% |
|---|---|---|---|---|
| R$ 0,15 | 44,7% | **47,8%** | 49,7% | 51,9% |
| R$ 0,20 | 43,7% | **46,9%** | 48,8% | 51,0% |
| R$ 0,35 | 40,6% | 44,0% | 46,0% | 48,4% |

**+6% de preço devolve a margem ao patamar de hoje.** Acima disso, seria margem incremental.

> ⚠️ **Revisão 2: o radar de concorrência respondeu e a resposta é não.** Não há evidência de
> prêmio de preço para gaxeta ou para o claim (delta −3,5%, −0,8% e −17% em três cortes).
> **Sem o degrau, a coluna que vale é a de +0%: a MB cai de 47,7% para 43,7%.** As linhas
> abaixo ficam como registro do que seria necessário, não como projeção.

### 4.3 Investimento e payback

| Item | Faixa |
|---|---|
| Rework de 4 moldes de tampa (canal) | R$ 20.000 – 48.000 |
| Ferramenta de perfil do extrusor (matriz + calibrador) | R$ 8.000 – 20.000 |
| Jiga de corte, aplicação e solda de junta | R$ 15.000 – 40.000 |
| Ensaio, homologação, amostragem | R$ 5.000 – 12.000 |
| **Total** | **R$ 48.000 – 120.000** |

Com +10% de preço nas 4 tampas: receita incremental **R$ 201.500/ano**, custo de gaxeta
**R$ 69.300/ano** (346.572 peças × R$ 0,20), margem incremental **R$ 132.200/ano**.

**Payback: 4 a 11 meses.**

### 4.4 O que este projeto não faz — e é o melhor argumento a favor dele

A taxa de acerto de lançamento da última safra foi de **0,7%** — 2 SKUs em 278. A recomendação nº 1
do projeto de portfólio é lançar menos e melhor.

**Este projeto não lança SKU nenhum.** Ele sobe o valor de 346 mil peças/ano que já vendem, para
mais de mil clientes que já compram. Não divide demanda (lição da cor), não cria estoque de
segurança novo, não precisa de EAN, arte, foto, catálogo e gôndola novos.

**Com uma condição, que é uma decisão de gestão, não de engenharia: a versão com gaxeta
SUBSTITUI a atual, não convive com ela.** Se virar "linha hermética" ao lado da "linha normal",
o projeto duplica 4 tampas em SKU, divide a demanda de cada uma pela metade e reproduz exatamente
o erro de 2022 — com o agravante de que o consumidor não consegue distinguir as duas na gôndola.
**Substituir, não somar.**

---

## 5. Suprimento — a Nitron não deve extrudar essa fita

O consumo anual, mesmo no cenário máximo (as 18 tampas, 855 mil peças, 555 km de fita):

**1.387 kg/ano. Uma tonelada e meia.**

Nas 4 tampas prioritárias: **655 kg/ano**. Para efeito de comparação, a fábrica compra **2.605 t de
resina por ano** — a fita seria **0,05% da massa** que entra na casa.

Uma linha de extrusão de perfil (extrusora, calibrador, banho, puxador, bobinadeira) custa
R$ 350–700 k e rodaria **308 h/ano — 15% de um único turno**, no cenário máximo. No cenário
prioritário, 7%.

**Conclusão: comprar a fita pronta em bobina, de um extrusor de perfil de vedação.** O Brasil tem
dezenas deles atendendo esquadria e automotivo, acostumados a perfil de TPE/EPDM em bobina, e o
volume da Nitron é pequeno para o setor — o que significa preço de tabela, não de projeto, mas
também significa que **a Nitron não é cliente estratégico de ninguém**. Consequências a tratar no
contrato:

- **Exigir segunda fonte homologada desde o piloto.** Resina de fonte única foi o que reprovou o
  Tritan; não repetir o erro com a fita.
- Negociar lote mínimo compatível com 650 kg/ano — provavelmente 1 a 2 entregas por ano.
- Especificar a ferramenta de perfil como **propriedade da Nitron**, mesmo produzida no
  fornecedor. É o ativo que permite trocar de extrusor sem refazer o desenvolvimento.

### 5.1 O ciclo de moído: este projeto passa no teste que reprovou Tritan e PET

O moído vale **R$ 2,63 M/ano** e só funciona porque o refugo é mono-resina. Três razões pelas quais
a gaxeta não ameaça esse ativo — as duas primeiras são estruturais, a terceira está em verificação:

1. **A gaxeta entra na montagem, não na injeção.** O refugo de injeção da tampa continua mono-PP e
   segue para o moinho normalmente. Só o refugo *pós-montagem* carrega TPE.
2. **A massa é irrisória:** 2,5 g/m contra uma tampa de dezenas de gramas — a gaxeta é bem menos de
   1% da massa do conjunto.
3. **SEBS é compatível com PP** (é formulado com PP e óleo). Diferente de Tritan ou PET, que
   contaminam de verdade.

O engenheiro de molde está quantificando o volume de refugo pós-montagem em risco. Entra na
revisão 2.

---

## 6. O plano — e por que ele começa com R$ 200, não com R$ 100 mil

### 6.1 Semana 1 — o teste que decide tudo, antes de gastar em ferramenta

Existe uma pergunta que mata ou aprova o projeto, e ela é respondida em bancada, com peça de
produção e material de loja de material de construção:

> **A trava atual ainda fecha com 1,2–1,6 mm de gaxeta no caminho — e com que força?**

As travas foram projetadas para tampa apoiada direto na borda. Somando altura de gaxeta, ou sobra
curso (o projeto anda) ou não sobra (o projeto muda de rota e vira alteração da própria trava,
que é outro custo).

**Protocolo, custo abaixo de R$ 200:**

1. Pegar 5 tampas de produção de cada uma das 4 prioritárias.
2. Colar na face de vedação um perfil comercial de EPDM/TPE de esquadria (1,5 mm), fita dupla-face
   fina, junta em cunha num lado reto.
3. Tentar fechar. **Medir:** fecha? com que força (dinamômetro de gancho)? a trava deforma?
4. **Medir a força de ABRIR, com e sem gaxeta** — acrescentado na revisão 2, e hoje é a medição
   mais importante do protocolo. É a tesoura: 32,3% das negativas do concorrente que veda bem são
   sobre abertura dura. Se a força de abrir subir muito, o projeto está reprovado por uso, não
   por custo — e isso provavelmente explica a queda de 176 e 210.
5. Encher com água colorida até 80%, inverter 24 h sobre papel-toalha branco. Fotografar.
6. Repetir com 2,0 mm e com 1,0 mm para achar a altura máxima que a trava aceita.
7. **Medir o curso livre da trava** com paquímetro, tampa fechada sem gaxeta — é o número que
   define a altura do lábio no desenho do perfil.

**Registrar junto:** quantas travas tem cada tampa e onde ficam. É a variável que mais pesa no
risco 7.2 e não está no ERP.

### 6.2 Semanas 2–4 — perfil e fornecedor

- Fechar o desenho do perfil com o número medido em 6.1 (altura do lábio) — não antes.
- Cotar com 3 extrusores de perfil de vedação. Pedir amostra de 50 m de cada em shore 45 e 55.
- Definir o método de junta: solda térmica em jiga, corte em cunha, ou sobreposição. **A junta é
  o ponto de vazamento mais provável de todo o projeto** — tratar como item de projeto, não como
  detalhe de montagem.
- Repetir o teste 6.1 com a fita real.

### 6.3 Semanas 5–10 — piloto em RET-C, só nela

Rework do molde de RET-C (22×14). É simultaneamente a de maior faturamento (R$ 774 k), a menor
entre as prioritárias — portanto a que menos arqueia — e a única cuja litragem está na janela boa
**nos dois corpos** (1,1 L e 2,2 L). É o melhor piloto que existe nesta linha.

Aprovar por ensaio (§6.5) antes de encostar nas outras três.

### 6.4 Semanas 11–20 — RET-D, QUA-3770, UF-215

Só depois do piloto aprovado. Se RET-C reprovar por arqueamento, **RET-D e UF-215 provavelmente
reprovam também** (são maiores) e a onda muda para tampas menores — RET-B e QUA-3780 —, aceitando
sair da janela de litragem em troca de vedação que funciona. Essa é a decisão de contingência;
tomar com o dado do piloto na mão.

### 6.5 O ensaio que sustenta o claim

Não há norma ABNT para "hermético" em utilidades domésticas. É **claim publicitário sob o CDC, e o
art. 36, parágrafo único, obriga o fornecedor a manter em seu poder os dados fáticos e técnicos que
sustentam a alegação.** Sem protocolo documentado e arquivado, o claim é risco jurídico, não
atributo de produto.

Protocolo interno mínimo (o engenheiro de molde está detalhando a versão executável):

| Ensaio | Critério |
|---|---|
| Inversão com água colorida, 24 h, 80% de enchimento | zero gotejamento em 20/20 amostras |
| Queda de 80 cm cheio pela metade, tampa para baixo | não abre, não vaza |
| 500 ciclos de abre-fecha, depois reteste de inversão | mantém aprovação |
| 50 ciclos de lava-louças a 65 °C, depois reteste | gaxeta não solta, não deforma, mantém aprovação |
| Micro-ondas 3 min com tampa destravada, 20 ciclos | sem deformação do lábio |

**Sobre a palavra na embalagem:** dos 267 anúncios coletados no ML, **só 8 dizem "hermético" (3%)**,
e a Sanremo — que faz plástico com válvula — evita o termo e escreve "válvula micro ondas".
Recomendação: usar **"não vaza" / "à prova de vazamentos"**, que é exatamente o que o ensaio de
inversão comprova, em vez de "hermético", que promete barreira a gás e ar e não é o que uma gaxeta
de lábio em tampa com trava entrega. Claim verificável é claim defensável.

---

## 7. Riscos, do mais provável ao menos

### 7.1 A trava não fecha com a gaxeta 🔴 **maior risco**
Curso projetado sem gaxeta. **Mitigação: é o teste de §6.1, custa R$ 200 e roda antes de qualquer
compromisso.** Se reprovar, a rota vira alteração da trava — outro custo, outro projeto.

### 7.2 A tampa arqueia entre as travas 🔴
Vedação por gaxeta exige força distribuída. Tampa grande com uma ou duas travas flete no meio do
vão e abre uma fresta que 0,4 mm de deflexão não fecha. **Quanto maior a tampa e menos travas,
menor a chance** — o que inverte parcialmente o ranking de faturamento e é a razão de o piloto ser
a menor das prioritárias. Contar as travas de cada tampa é item de §6.1.

### 7.3 A junta da fita vaza 🟡
Anel cortado tem emenda, e é lá que vaza. Tratar como item de projeto: solda térmica em jiga, corte
em cunha, junta posicionada no meio de um lado reto (nunca no canto).

### 7.4 O mercado não paga os +6% 🔴 **confirmado — não paga**
Não é mais risco, é resultado. Três cortes independentes dão delta de −3,5%, −0,8% e −17%.
Sem prêmio, a gaxeta é custo puro e a MB cai 4 pontos. **Ver revisão 2.**

### 7.4b A gaxeta piora a abertura 🔴 **novo — hoje é o maior risco de uso**
32,3% das negativas do concorrente que veda bem são sobre abrir duro e trava quebrando. A gaxeta
aumenta a compressão sobre travas que não foram redesenhadas. **Medição acrescentada em §6.1.**

### 7.5 A gaxeta solta em campo 🟡
Vira devolução e reclamação. **Mitigação: encaixe mecânico por interferência, nunca adesivo**,
e os 50 ciclos de lava-louças no ensaio.

### 7.6 Mão de obra de montagem 🟡
É o maior componente de incerteza do custo por peça. Se a aplicação manual não descer de 25 s/peça,
o custo vai para R$ 0,35 e o degrau de preço sobe de 6% para 10%. **Cotar a jiga junto com o
perfil, não depois.**

### 7.7 Fonte única de fita 🟢
Homologar segunda fonte desde o piloto e manter a ferramenta de perfil como ativo da Nitron.

---

## 8. Pendências antes de gravar em `pdp_lancamento`

| # | Pergunta | Com quem |
|---|---|---|
| 1 | Quantas travas tem cada tampa e onde ficam? | Fábrica — medição |
| 2 | Qual o curso livre da trava fechada, em mm? | Fábrica — §6.1 |
| 3 | O molde de cada tampa aceita usinagem de canal, ou o postiço é o próprio corpo? | Ferramentaria |
| 4 | Dimensões reais das refs 176, 210 e 212 (não estão no catálogo) | Fábrica |
| 5 | Qual o tempo real de aplicação manual da gaxeta? | Produção |
| 6 | O mercado paga o prêmio? Quanto? | radar-concorrência — em apuração |
| 7 | O refugo pós-montagem com TPE ameaça o moído? Quanto? | engenheiro-molde — em apuração |

---

## 9. Achados abertos que este levantamento produziu

- **RED-2270 (Redondo 2,3 L) tem MB de 24,6%** contra 46,0% da média da linha — a pior das 18
  tampas. A causa aparente é o custo do preto: `2270.012.003` custa **R$ 5,80** contra **R$ 2,95**
  do transparente `2270.012.001`, quase o dobro pelo mesmo pote. Fatura R$ 99 k/ano. Vale mais
  investigar esse custo do que colocar gaxeta nele.
- **RET-D tem MB de 35,3%**, bem abaixo dos 47,7% de RET-C, com a mesma família e o mesmo processo.
  Mesmo padrão: `151.012.003` preto a R$ 8,87 contra R$ 5,36 do transparente.
  **O preto custa caro em toda a linha com trava e ninguém explicou por quê** — é margem grande
  em jogo, transversal a várias famílias.
- **`216.NIT.003` tem custo de R$ 16,51** contra R$ 5,02 do `216.012.003` — mesmo produto,
  3,3× o custo, 2 clientes, R$ 15,5 k/ano. Provável erro de cadastro de custo.
- **`233`, `234`, `232`, `231`, `156`, `155`, `151`, `154` (referências curtas, sem sufixo)
  faturam R$ 415 k somados para 1 a 5 clientes cada.** São as private label da lição nº 2 do
  CLAUDE.md. Não confundir com as `.012.001` de canal. Se o projeto avançar, decidir explicitamente
  se a gaxeta vai para as private label — é conversa com cliente, não decisão interna.

---

*Revisão 2 — 06/09/2026. Radar de concorrência concluído (600 avaliações em
`pdp_ml_review`, run 264292); engenheiro de molde em apuração. Nada gravado em `pdp_lancamento` até o parecer do
curador-portfolio.*
