# Projeto das borrachas de vedação — Linha Pote com Travas

**Motivo:** a fábrica ensaiou os potes da categoria e **eles não vedam**. O aro deixa de ser
upgrade opcional e passa a corrigir uma lacuna funcional medida.
**Escopo:** 4 borrachas, uma por geometria de tampa, atendendo 6 referências de produto.
**Este documento substitui a §2 de `07-especificacao-lacre-tpe.md`** — ver §2 abaixo, a arquitetura
mudou.

---

## 1. Primeiro, uma correção de nomenclatura que evita receber a peça errada

Você pediu "borrachas", e vou usar a palavra. Mas **não peça "borracha" ao fornecedor.**

Borracha, no mercado, significa elastômero **vulcanizado** — EPDM, NBR, SBR. É um material
termofixo, que **não é compatível com o ciclo de moído de PP** e cujos graus comuns não são
food-grade sem especificar. Se você mandar uma cotação pedindo "borracha de vedação", é isso que
vai chegar.

O que este projeto especifica é **elastômero termoplástico (TPE/TPV)** — funciona como borracha,
mas é termoplástico, extrudável, base PP, e volta para o ciclo de moído sem destruí-lo.

**Na cotação, escreva: "perfil extrudado em TPV base PP" ou "TPE-S (SEBS)".** Nunca "borracha".

---

## 2. A decisão que muda o projeto: vedação RADIAL, não axial

### O que a conta diz

A especificação anterior (`07`) colocava o aro na **face de vedação da tampa**, comprimindo contra
a borda do pote — vedação **axial**. Refiz o dimensionamento com mais cuidado e **ela não fecha**:

| Tampa | Perfil | Força exigida da trava | Trava de PP entrega | |
|---|---|---:|---:|---|
| RET-C | bulbo maciço | 237 N | 20–60 N | ❌ |
| RET-C | **lábio fino 0,7 mm** | **68 N** | 20–60 N | ❌ **também não cabe** |
| RET-D | lábio fino 0,7 mm | 83 N | 20–60 N | ❌ |
| QUA-3770 | lábio fino 0,7 mm | 73 N | 20–60 N | ❌ |
| UF-215 | lábio fino 0,7 mm | 78 N | 20–60 N | ❌ |

⚠️ **Correção ao documento 07:** eu havia escrito que o lábio fino "cabe no limite". Com o cálculo
refeito, **não cabe em nenhuma das quatro tampas.** Vedação axial exigiria trava nova — o que é
outro projeto, com molde novo.

### A saída: vedar contra a parede, não contra a borda

Se o aro for alojado num canal na **saia lateral da tampa**, comprimindo radialmente contra a
**parede interna do pote**, três coisas mudam de uma vez:

1. **A força não passa pela trava.** É radial e auto-equilibrada pelo próprio corpo do pote. A
   trava volta a fazer só o que já faz: segurar a tampa no lugar.
2. **O arqueamento da tampa deixa de importar.** A tampa pode fletir no meio do vão que a saia
   continua encostada na parede — que é rígida e restringida pelo corpo. Isto é decisivo, porque
   arqueamento entre travas é a causa mais provável do resultado "não veda" do seu ensaio.
3. **A tesoura abrir/vedar se desarma.** O risco nº 1 do projeto — vedar melhor e ficar duro de
   abrir, como o concorrente com 32,3% de reclamação sobre abertura — some, porque não estamos
   aumentando a compressão sobre a trava.

### Mas o perfil radial também tem que ser fino

| Perfil radial | Contato | Força radial | **Força de inserir a tampa** |
|---|---:|---:|---:|
| Face plana maciça 1,0 mm | 1,0 mm | 282–345 N | **141–172 N** ❌ ninguém fecha |
| Lábio fino 0,3 mm | 0,3 mm | 85–103 N | **42–52 N** ⚠️ no limite |
| **Aba flexível 0,55 mm** | 0,3 mm | 37–45 N | **30–36 N** ✅ |

**A aba flexível é a única que resolve os dois lados**, e tem uma propriedade que as outras não
têm: **auto-energização**. A aba é montada inclinada para dentro do pote; qualquer pressão interna
a empurra *contra* a parede, aumentando a vedação. Quanto mais o pote precisa vedar, melhor ele
veda — sem custo de força na hora de fechar.

É o mesmo princípio de um retentor de eixo ou da borracha de porta de geladeira, em miniatura.

---

## 3. O perfil

```
                    PAREDE INTERNA DO POTE
                    ║
     tampa          ║
   ────────┐        ║
           │        ║
    canal  │▓▓▓▓▓▓▓▓│                 ▓ = pé com barbas, dentro do canal
   ────────┤▓▓▓▓▓▓▓▓│
           │    ╲   ║
   saia    │     ╲  ║  ← aba flexível, inclinada ~35° para BAIXO
   da      │      ╲ ║     (para dentro do pote)
   tampa   │       ╲║
           │        ▓  ← ponta em contato com a parede
           │        ║
           │        ║   pressão interna ↑ empurra a aba contra a parede
```

| Cota | Valor | Tolerância |
|---|---|---|
| Largura do pé (dentro do canal) | **1,80 mm** | +0,05 / −0,02 |
| Altura do pé | **1,40 mm** | ±0,10 |
| Barbas de retenção | 2 pares, 30° | — |
| Espessura da aba | **0,55 mm** | ±0,05 |
| Comprimento livre da aba | **2,20 mm** | ±0,10 |
| Ângulo da aba (em repouso) | **35°** para o interior do pote | ±3° |
| **Interferência radial de projeto** | **0,50 mm** | ±0,15 |
| Altura total da seção | 3,10 mm | ±0,15 |
| Massa linear | ~2,3 g/m | ±10% |

**Canal na saia da tampa:** 1,60 mm de largura × 1,45 mm de profundidade. O pé de 1,80 mm entra
com 12% de interferência e fica retido pelas barbas. **Sem adesivo, nunca.**

### O que a interferência de 0,50 mm precisa tolerar

Este é o ponto de atenção da arquitetura radial, e precisa ser dito com clareza:

⚠️ **A parede interna do pote tem ângulo de saída de desmoldagem** — tipicamente 1° a 2°. Isso
significa que **o diâmetro interno muda com a profundidade**, e a compressão da aba depende de onde
exatamente a tampa para. Uma variação de 2 mm na profundidade de encaixe, com 1,5° de saída,
muda o raio em ~0,05 mm — 10% da interferência de projeto.

Três consequências práticas:

1. **Medir o ângulo de saída real na região onde a aba vai trabalhar**, em peça de produção, antes
   de fechar a cota de interferência. É a medição nº 1 da §7.
2. **A aba flexível tolera essa variação muito melhor que um bulbo maciço** — é exatamente por isso
   que ela é a escolha certa. Uma aba de 2,2 mm absorve ±0,15 mm de variação sem mudar
   materialmente a força.
3. **A profundidade de encaixe da tampa é definida pela trava**, que é repetível. Isso trabalha a
   nosso favor.

---

## 4. Material — e por que provavelmente não é o TPE que estava no cadastro

| Material | Compatível com moído PP | Food grade | Temp. máx | Compression set | Custo |
|---|:--:|:--:|---|---|---|
| **TPV base PP (Santoprene e similares)** | ✅ | ✅ | **~120 °C** | **bom** | médio |
| TPE-S / SEBS (Karinprene) | ✅ | ✅ | ~90 °C | **médio** ⚠️ | baixo |
| Silicone (LSR/HCR) | ❌ | ✅ | 200 °C | ótimo | alto |
| EPDM / NBR ("borracha") | ❌ | ⚠️ grau | 120 °C | bom | baixo |

**Recomendação: TPV base PP, shore A 55 ±5.**

O motivo é **compression set** — a capacidade de voltar à forma depois de ficar comprimido. Um
pote fechado passa semanas no armário com a vedação sob carga. TPE-S shore 45 tem set relativamente
alto: ele "cansa" e não volta. **É exatamente o modo de falha que os consumidores descrevem nas
avaliações dos concorrentes** — *"as tampas afrouxaram"*, *"só vedou no primeiro dia"*. Especificar
TPE-S barato é comprar esse problema.

TPV custa mais por quilo, mas o consumo total do projeto é **~590 kg/ano**. A diferença de material
entre TPE-S e TPV no projeto inteiro é da ordem de R$ 10–15 mil/ano — menos que o risco de uma
vedação que morre em três meses.

**Duas perguntas que decidem o material, e que eu não sei responder:**

- **O pote vai ao micro-ondas com a tampa fechada?** Se sim, TPE-S de 90 °C é marginal e TPV é
  obrigatório.
- **Vai à lava-louças?** 65–70 °C, ambos aguentam, mas o detergente alcalino extrai óleo do TPE-S
  mais que do TPV.

**Exigir do fornecedor, antes da primeira amostra:** carta de conformidade para contato com
alimento do **grau específico** (não da família), e dado de **compression set (ASTM D395, 22 h a
70 °C) ≤ 30%**.

---

## 5. As quatro borrachas

⚠️ **Os perímetros abaixo são calculados a partir das dimensões de catálogo e servem para cotar,
não para produzir.** O aro vai num canal na saia, cujo perímetro é menor que o externo do produto.
**Medir antes de encomendar** — procedimento na §7.

| # | Borracha | Tampa (PI) | Produtos | Perímetro externo | **Perímetro do canal (estimado)** | **Corte (−1,5%)** |
|---|---|---|---|---:|---:|---:|
| **B1** | ARO 22×14 | **816** | Raso 1,1 L (233) + Alto 2,2 L (156) | 677 mm | ~653 mm | **643 mm** |
| **B2** | ARO 26×18 | **799** | Raso 2,3 L (234) + Alto 4,3 L (151) | 827 mm | ~803 mm | **791 mm** |
| **B3** | ARO 20×19 | **575** | Quadrado 1,8 L (3770) | 733 mm | ~709 mm | **698 mm** |
| **B4** | ARO 25×16,5 | **924** | Ultraforte 2,1 L (215) | 780 mm | ~756 mm | **745 mm** |

**Quatro borrachas cobrem seis referências de produto**, porque a tampa 816 serve Raso 1,1 L e
Alto 2,2 L, e a 799 serve Raso 2,3 L e Alto 4,3 L — confirmado pelo BOM (`TPRLPI`), não por
inferência.

### ⚠️ Correção ao documento 07: o corte é MENOR que o perímetro, não maior

O `07-especificacao-lacre-tpe.md` especificava corte = perímetro **+2%**, correto para um aro
solto num canal axial. **Para vedação radial está errado.**

Um aro radial deve ser montado com **pré-tensão de 1% a 2%** — cortado *menor* que o canal e
esticado na montagem. É prática consagrada em o-rings, e compra três coisas:

- o aro **se auto-assenta** no canal e não sai;
- a **junta fica sob compressão**, e não sob tração — que é o que a faz vazar;
- absorve a tolerância de comprimento do corte.

**Nunca passar de 3% de pré-tensão:** acima disso a seção afina por efeito de Poisson e a
interferência radial cai justamente onde ela é necessária.

---

## 6. A junta

Continua sendo o ponto de vazamento mais provável, mas a arquitetura radial **melhora a situação**:
a pré-tensão mantém a junta comprimida em vez de tracionada.

| Item | Definição |
|---|---|
| Corte | **cunha (scarf) a 30°**, nunca topo a topo |
| União | **solda térmica em jiga**, temperatura e tempo controlados |
| Posição | meio de um lado reto — **nunca no canto**, e marcada na jiga |
| Inspeção | 100% visual: junta fechada, sem degrau, sem falha de material |
| Critério de ensaio | E1 sem vazamento com a **junta posicionada para baixo** no teste de inversão |

Cianoacrilato serve para protótipo. **Não vai para produção** — não sobrevive a lava-louças.

---

## 7. O que precisa ser medido antes de encomendar — nesta ordem

Nenhuma destas medições precisa de ferramenta nova, e todas juntas levam menos de um dia.

| # | Medição | Como | Por que trava a encomenda |
|---|---|---|---|
| **1** | **Perímetro real do canal**, nas 4 tampas | Fio de solda fino contornado no canal, esticado e medido com trena | Define o comprimento de corte. Errar 1% já compromete a junta |
| **2** | **Ângulo de saída da parede interna** do pote, na faixa onde a aba trabalha | Paquímetro de profundidade, 3 alturas | Define a tolerância da interferência (§3) |
| **3** | **Diâmetro/vão interno do pote** na altura de trabalho, e o vão externo da saia da tampa | Paquímetro, 4 pontos | A diferença entre os dois **é** a folga que a aba tem que vencer |
| **4** | **Profundidade de encaixe** da tampa, travada | Paquímetro | Confirma onde a aba trabalha |
| **5** | **Onde vaza hoje** — canto ou meio do lado? | Repetir o ensaio com corante e fotografar o papel | ⚠️ **Ver abaixo** |

### A medição 5 é a que mais me falta

Você disse que os potes foram testados e não vedam. **Não sei onde eles vazam**, e isso é a única
coisa que ainda pode mudar o projeto:

- **Vaza no meio dos lados longos** → é arqueamento da tampa. **A arquitetura radial resolve**, e
  este projeto está certo como está.
- **Vaza nos cantos** → é geometria de canto, raio pequeno demais, ou a tampa não assenta.
  **A radial ajuda menos**, e talvez seja preciso aumentar a interferência só nos cantos ou revisar
  o raio da tampa.
- **Vaza no perímetro inteiro, uniformemente** → a folga tampa/corpo é maior que o previsto, e a
  interferência de 0,50 mm pode ser insuficiente. Muda a cota, não a arquitetura.

Se você tiver o relatório do ensaio — mesmo que seja uma foto do papel-toalha — me mande. Nos três
casos a arquitetura radial continua sendo a escolha certa; o que muda é a cota de interferência,
que ainda dá tempo de ajustar antes da matriz do extrusor ser cortada.

---

## 8. Plano de validação

Antes de comprometer ferramenta, com perfil comercial aproximado (perfil de vedação de esquadria,
~R$ 200):

| Etapa | O que provar | Critério |
|---|---|---|
| 1 | O aro radial **veda** onde o produto atual falha | E1 aprovado, 5 de 5 |
| 2 | A força de **inserir e remover** a tampa é aceitável | ≤ 45 N, e ≤ 1,3× a força atual |
| 3 | O aro **não sai do canal** | 200 ciclos, zero saídas |
| 4 | Sobrevive à **lava-louças** | 20 ciclos, retração ≤ 1%, mantém E1 |
| 5 | **Não cansa** sob carga | 30 dias fechado a 40 °C, mantém E1 |

A planilha `ensaios/protocolo-ensaio-estanqueidade.xlsx` já tem as abas de E1, E3, E4, E5 e
Travas. **Use a coluna "Força ABRIR" da aba Travas para registrar também a força de inserir** —
na arquitetura radial é ela que importa, não a de fechar.

**A etapa 5 é a que reprova material barato.** É onde o TPE-S de compression set alto falha e o
TPV passa.

---

## 9. O que muda no projeto de operacionalização

`08-operacionalizacao-aro-tpe.md` continua valendo em quase tudo — posto de montagem, cadastro no
ERP, suprimento, refugo, cronograma. Três ajustes:

| Item | Muda para |
|---|---|
| **Onde fica o canal** | Na **saia lateral** da tampa, não na face de vedação |
| **Ferramentaria** | O canal na saia é um **rebaixo em superfície lateral** — mais simples que na face, e **sem risco de rechupe no topo visível** ✅ |
| **Montagem** | O aro é **esticado 1,5% e assentado**, não pressionado. Operação mais rápida, provavelmente abaixo dos 25 s estimados |
| **Material** | **TPV base PP shore A 55**, não TPE-S shore 45 |

O ponto do rechupe é um ganho real: mover o canal da face para a saia **elimina o risco nº 4** da
tabela de riscos do documento 08, que era marca visível em peça transparente.

---

## 10. Resumo executivo

1. **Não peça "borracha".** Peça **perfil extrudado em TPV base PP**.
2. **A vedação é radial, contra a parede interna do pote** — não axial contra a borda. A axial não
   fecha: exige 68–83 N de uma trava que entrega 20–60 N.
3. **O perfil é uma aba flexível de 0,55 mm inclinada 35°**, com auto-energização: quanto maior a
   pressão interna, melhor veda. Força de inserir de 30–36 N.
4. **Quatro borrachas cobrem seis referências.**
5. **O corte é 1,5% MENOR que o canal**, não maior — pré-tensão, ao contrário do que o documento 07
   dizia.
6. **Material é TPV shore A 55**, não TPE-S 45, por causa de compression set — que é exatamente o
   modo de falha "afrouxou depois de um tempo".
7. **Cinco medições, menos de um dia**, antes de encomendar. A mais importante é **onde o pote
   vaza hoje**.
