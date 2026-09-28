# Chrono v3 — o que mudou, e o que eu decidi por conta

Revisão sobre os apontamentos de moldabilidade. Tudo refeito em B-rep
(OpenCASCADE), não em malha — é o que permite raio de canto e saída de verdade.

---

## 1. Saída de extração

**1,5° em toda parede vertical** (a faixa pedida era 1 a 3). Convenção: molde
abre em +Y, partição na face de baixo de cada peça — logo parede externa
**estreita para cima** e furo **alarga para cima**.

Medido face a face na peça pronta, com o auditor conferido contra um cilindro
reto (tem de reprovar) e um cone de 1,5° (tem de passar):

| | parede vertical antes | depois |
|---|---|---|
| M01 (só o que o Chrono acrescenta) | 45,6 mm² | **0,0 mm²** |
| M02 rodinha | 234,5 mm² · 21,8% | **0,0 mm²** |
| M03 ponteira | 234,7 mm² · 29,0% | **0,0 mm²** |

Os 167 mm² de parede vertical que sobram na M01 são **do corpo da válvula
original**, que já está ferramentado e não é nosso.

O que estava sem saída e ganhou: rebaixo, poste, furo passante, mesa, aro
externo e interno da rodinha, 12 entalhes de unha, contorno da gota, janela,
chanfro da janela, fendas do pino, drenos e o furo interno do pino.

## 2. Cantos abaulados

| onde | raio |
|---|---|
| contorno da gota, topo | 0,30 |
| contorno da gota, base · borda da janela · faces da rodinha · topo da mesa | 0,15 |
| canto piso/parede do rebaixo (côncavo, é o que enche primeiro) | 0,15 |
| **pé do poste** | **0,15** |
| contorno de cada caractere, em planta | 0,06 |

**O pé do poste não levou 0,30 e isso é medido, não arbitrado:** a folga radial
para a rodinha é 0,20 e a face de baixo dela passa a 0,02 mm do piso. Com raio
0,30 a concordância chegaria a Ø13,585 na altura crítica e encostaria na
rodinha. Com 0,15 sobram 0,125 mm. Se quiserem 0,30, o furo da rodinha tem de
abrir para Ø13,90.

Achado no caminho: o corte do rebaixo parava exatamente em Ø13,20, o mesmo
diâmetro nominal do poste. Com o poste ganhando saída, sobrava uma **aleta de
0,03 mm de espessura por 0,60 de altura** entre os dois. O corte agora entra
até Ø10,00, bem dentro do poste.

## 3. Escala dos dias

Você estava certo: o vão extra em 1..9 é o espaço do zero que sobrou. Agora o
que é igual é o **vão entre as bordas**: **5,81° entre todos os 31**.

Consequência que preciso registrar: **o passo do dia deixa de ser constante.**
O centro do dia 9 anda de 182,9° para 162,6°. Para o Chrono tanto faz — o dia
não tem detente, quem alinha é a mão e quem lê é o olho. Mas fecha a porta para
um dia detentado no futuro. Se preferirem passo constante, é uma linha.

## 4. O rebaixo do anexo 01

Não era o rebaixo da rodinha — era a **concha das 12 h aflorando no piso dele**.
A cunha foi enchida de ponta a ponta, da face de baixo (Y 35,40) até a face
(37,23), e o piso ficou plano.

Medi antes de encher: o fundo da concha só desce até **Y 36,214** e a face de
baixo da válvula naquela região **não passa de 35,400** em lugar nenhum. Então o
enchimento não acrescenta nada por baixo, não fecha vazio nenhum, e a parede
naquela cunha passa a ter **1,83 mm — a mesma do resto da chapa**. Era antes que
estava fina e irregular.

## 5. Detente

- calota de **Ø2,00 de base e 0,25 de altura** (esfera R 2,125), contra Ø0,84 e 0,18
- **centrada na faixa do rebaixo, em r 10,10** — meio exato entre o poste (6,60)
  e a parede (13,60); antes estava em 7,80, encostada no poste
- as 12 covinhas da rodinha usam a **mesma esfera, invertida**

Uma diferença proposital: cada uma é referida à **sua própria face** (piso 36,63
e face de baixo da rodinha 36,65). Assim a folga de montagem de 0,02 mm se
mantém e o par não trava. Folga mínima medida no conjunto: **0,017 mm** — que é
o que um detente tem de ter.

Nenhuma das duas é undercut: a barriga da esfera fica abaixo da face, a calota
só estreita para cima e sai sozinha do molde.

## 6. Letras e números

**0,10 mm de auto relevo, 1,50 mm de altura de caractere, em tudo** — dias,
meses e MÊS.

⚠️ **Duas leituras que eu tive de fazer, e que você confirma ou corrige:**

**a) "espessura 1,5 mm" eu li como altura do caractere, não espessura do traço.**
Um traço de 1,5 mm exigiria caractere de ~8 mm de altura; a faixa da mesa tem
4,55 mm. Não cabe. Com 1,50 de caractere o traço sai em **0,28 mm**. Se o que
você quis foi traço mínimo, me diga o valor que eu engrosso a fonte.

**b) A saída do caractere é 15°, não 1,5°.** Com 0,10 de relevo, 1,5° dá **2,6
micra** de recuo — o aço não guarda isso. 15° custam 0,027 mm por lado e a letra
continua legível. Se a casa trabalha com outro número para letra rasa, é um
parâmetro.

**E um aviso honesto:** a 0,10 mm de relevo os números ficam **bem mais discretos**
que os 0,25/0,30 de antes. No 3D dá para ler, mas em peça injetada cinza vai
depender de contraste de acabamento (fundo texturizado e topo polido, ou o
contrário). Se a leitura for prioridade sobre o ciclo, 0,15 já muda bastante.

## 7. Ponteira

- **"D" removido**
- **"M" virou "MÊS"**, em auto relevo (4 contornos, com o acento)
- **ícone da Nitron de gravado para auto relevo**

Para não piorar o orçamento de altura, o corpo da lâmina passou de 1,60 para
**1,50** e o relevo devolve os 0,10. **O envelope não mudou:** topo em Y 39,950,
os mesmos +0,188 mm sobre o ponto mais alto da tampa. Mesma coisa na rodinha
(1,50 de corpo + 0,10 de numeral).

## 8. Conferido

| | |
|---|---|
| interferência M01×M02, M01×M03, M02×M03 | 0,0000 mm³ |
| folga do detente | 0,017 mm |
| folga ponteira × rodinha | 0,100 mm |
| encaixe da farpa | 0,40 mm (inalterado) |
| folga poste × furo da rodinha | 0,242 mm |
| folga pino × furo, no ponto mais estreito | 0,100 mm |
| topo do conjunto | Y 39,950 · +0,188 sobre a tampa |
| massa | 2,907 g (v2: 2,908 g) |
| B-rep dos 6 arquivos | válido no BRepCheck |

## 9. Os arquivos

STEP em `v3/step/`. A M01 continua em receita, agora com 4 passos **e a ordem
importa**:

```
válvula final = (((CAD original + M01a) − M01b) + M01c) − M01d
```

1. **somar** `v3_M01a_SOMAR_1_enchimento_e_mesa`
2. **subtrair** `v3_M01b_SUBTRAIR_2_rebaixo`
3. **somar** `v3_M01c_SOMAR_3_poste_detentes_dias` (56 sólidos soltos: poste,
   2 detentes e os 53 contornos dos 31 numerais)
4. **subtrair** `v3_M01d_SUBTRAIR_4_furo_passante`

O enchimento entra antes do rebaixo (senão o rebaixo não tem o que cortar) e os
detentes entram depois (senão o rebaixo raspa as molas).

`v3_M02_Rodinha_Meses` e `v3_M03_Ponteira` são peças inteiras, um sólido cada.
Os STL em `v3/stl/` são para ver e imprimir — neles os numerais da M01 são
prisma reto, porque a tesselação do OCC não fecha nesses 53 sólidos de 0,2 mm.
**A saída de 15° dos caracteres vive no STEP**, que é o que vai para a ferramenta.
