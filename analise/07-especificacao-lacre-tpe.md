# Especificação do lacre de vedação em TPE — Linha Pote com Travas

> ## ⛔ STATUS: NÃO APROVADO PARA EXECUÇÃO
>
> O `curador-portfolio` vetou o projeto em 06/09/2026 (parecer em
> `06-gaxeta-tpe-potes-hermeticos.md`, revisão 4). **Nada aqui autoriza gastar dinheiro.**
> Estão explicitamente vetados: rework de molde, compra de ferramenta de perfil, cotação formal
> com extrusores e abertura de cadastro de fornecedor.
>
> **Por que este documento existe assim mesmo:** escrever a especificação custa zero, e ela é
> exatamente o que precisa estar pronto se o ensaio de bancada devolver o resultado que reabre o
> caso (§8). Sem ela, reabrir significa recomeçar do zero três meses depois.
>
> **E uma coisa que ele NÃO é:** este documento não é pré-requisito do ensaio. O ensaio mede o
> produto atual, sem lacre nenhum. Ver §7.

---

## 1. Por que a fita não pode ser chapada de 1 mm

Esta é a correção mais importante do documento, e ela é aritmética, não opinião.

A força de fechamento **não é uma variável de projeto** — ela é o que as travas de PP já
existentes conseguem entregar, e elas não mudam. Um clip de PP injetado desse porte entrega
tipicamente **20 a 60 N**.

| Tipo de perfil | Força por cm de perímetro | Exigido na tampa 22×14 (67,7 cm) | Cabe? |
|---|---|---|---|
| Fita maciça 1 mm | 2 – 5 N/cm | **135 – 340 N** | **não** |
| **Lábio de parede fina** | 0,5 – 1,5 N/cm | **34 – 100 N** | **no limite** |

A fita chapada exige de 3 a 6 vezes mais força do que a trava tem. Ela não vedaria: ou a tampa
não fecha, ou fecha sem comprimir o suficiente, ou a trava rompe por fadiga.

**O lábio de parede fina é a mesma bobina, o mesmo material e a mesma extrusão** — muda só a
ferramenta de perfil, que é definida antes de qualquer produção. Custo de acertar agora: zero.
Custo de descobrir depois: o projeto inteiro.

---

## 2. O perfil

```
        ← 4,2 ±0,15 →
     ┌──────────────────┐  ─┬─
     │   lábio 0,7 mm   │   │  1,4 mm  ← comprime 20–30% ao fechar
     └───────┐  ┌───────┘  ─┼─
             │  │           │  0,8 mm  ← colo
          ┌──┴──┴──┐       ─┼─
          │ ▲    ▲ │        │  1,2 mm  ← pé com barbas, entra em canal de 1,00 mm
          └────────┘       ─┴─
           ← 1,20 →
```

| Parâmetro | Valor | Tolerância | Por quê |
|---|---|---|---|
| Material | **TPE-S (SEBS)**, shore A 45–55 | ±5 shore | É o CODPROD 997 Karinprene já cadastrado. SEBS é blenda base PP — compatível com o parque e com o moído, ao contrário de Tritan e PET |
| Largura do pé | 1,20 mm | +0,05 / −0,02 | Interferência de 20% em canal de 1,00 mm |
| Altura do pé | 1,20 mm | ±0,10 | |
| Barbas | 2 pares, ângulo 30° | — | **Retenção mecânica. Nunca adesivo** — ver §5 |
| Altura do lábio | 1,40 mm | ±0,10 | ⚠️ **valor provisório — depende da medição de curso livre da trava** (§7) |
| Parede do lábio | 0,70 mm | ±0,05 | É o que baixa a força de fechamento ao que a trava tem |
| Altura total | 3,40 mm | ±0,15 | |
| Massa linear | ~2,5 g/m | ±10% | Base de todo o custeio |
| Cor | natural ou preto | — | Preto só nos SKUs `.012.003`; natural nos demais |

**A altura do lábio é a única cota que não pode ser fechada hoje.** Ela é limitada pelo curso
livre da trava, que ninguém mediu. Medir custa um paquímetro (§7). Especificar antes de medir é
como o projeto erraria.

---

## 3. O canal na tampa — e por que ele custa mais do que parece

| Parâmetro | Valor |
|---|---|
| Largura | 1,00 mm +0,03 / −0,00 |
| Profundidade | 1,25 mm ±0,05 |
| Raio de canto do canal | ≥ 3 mm (o perfil não faz curva fechada sem enrugar) |
| Posição | face de vedação da tampa, contínua, sem interrupção |

⚠️ **O canal não se usina — solda-se.** Um rebaixo na peça é uma **saliência no aço**. Nos moldes
existentes isso significa solda TIG ou laser na face de vedação, reusinagem do perfil e
repolimento, em aço temperado, com risco de trinca na zona termicamente afetada. A alternativa
limpa é **postiço trocável**, mais caro mas reversível.

⚠️ **Risco de rechupe.** O canal cria transição de espessura, e transição de espessura marca a
face oposta — que aqui é o topo visível da tampa. **66% do faturamento dessas famílias é
transparente**, onde rechupe se vê de longe. Prever aço de alta condutividade (BeCu/Moldmax) no
postiço como contingência de tryout.

---

## 4. Comprimentos de corte — uma bobina, 17 cortes

É isto que torna a ideia original correta: os perímetros variam de 43 a 111 cm, e **isso é
comprimento de corte, não geometria diferente**. Uma seção serve a linha inteira.

| Tampa | Perímetro | **Corte (perímetro + 2%)** | Produtos servidos |
|---|---:|---:|---|
| RET-A 14,0×10,0 | 45,1 cm | **46,0 cm** | Raso 270 ml + Alto 460 ml |
| RET-B 17,0×11,0 | 52,6 cm | **53,7 cm** | Raso 500 ml + Alto 850 ml + 157 + 158 |
| **RET-C 22,0×14,0** | 67,7 cm | **69,1 cm** | Raso 1,1 L + Alto 2,2 L |
| **RET-D 26,0×18,0** | 82,7 cm | **84,4 cm** | Raso 2,3 L + Alto 4,3 L |
| QUA-3790 12,0×11,0 | 43,2 cm | **44,1 cm** | Quadrado 360 ml |
| QUA-3780 16,0×14,0 | 56,4 cm | **57,5 cm** | Quadrado 860 ml |
| **QUA-3770 20,0×19,0** | 73,3 cm | **74,8 cm** | Quadrado 1,8 L |
| QUA-3760 25,0×24,0 | 92,1 cm | **94,0 cm** | Quadrado 3,7 L |
| RED-2290 ⌀13,5 | 48,9 cm | **49,9 cm** | Redondo 450 ml |
| RED-2280 ⌀17,5 | 63,9 cm | **65,2 cm** | Redondo 1,1 L |
| RED-2270 ⌀22,5 | 80,8 cm | **82,4 cm** | Redondo 2,3 L |
| **UF-215 25,0×16,5** | 78,0 cm | **79,6 cm** | Ultraforte 2,1 L |
| UF-216 30,0×20,0 | 94,0 cm | **95,9 cm** | Ultraforte 4 L + tela |
| UF-217 35,0×24,0 | 110,9 cm | **113,1 cm** | Ultraforte 6,9 L |
| VAL-176 / VAL-210 / DIV-212 | **medir** | — | Não constam no catálogo |

Os 2% são a folga da junta em cunha. **Ajustar no tryout** — este é um número de partida, não uma
cota validada.

Perímetros calculados como 2·(C+L) com desconto de 6% pelo raio de canto, a partir das dimensões
de catálogo. **Conferir na peça física antes de qualquer encomenda.**

---

## 5. A junta é o ponto de vazamento mais provável do projeto

Um anel cortado tem uma emenda, e é nela que vaza. Tratar como item de projeto, não como detalhe
de montagem:

- **Corte em cunha (scarf) a 30°**, nunca topo a topo — a cunha dá área de contato e tolera
  variação de comprimento.
- **Solda térmica em jiga**, com temperatura e tempo controlados. Cola cianoacrilato é aceitável
  para protótipo e **inaceitável em produção** — não sobrevive a lava-louças.
- **Posicionar a junta no meio de um lado reto.** Nunca no canto, onde já há deformação.
- Marcar a posição da junta na jiga para que a inspeção saiba sempre onde olhar.

**Adesivo em nenhuma hipótese para fixar o perfil no canal.** Uma gaxeta que descola em campo
vira devolução, e viola a lição nº 7 do projeto: peça removível não carrega função. A retenção é
mecânica, pelas barbas.

---

## 6. Critérios de recebimento da bobina

| Ensaio | Frequência | Critério |
|---|---|---|
| Dureza shore A | por lote | 45–55, 3 pontos por bobina |
| Cotas do perfil (projetor de perfil) | por lote | conforme §2 |
| Massa linear | por lote | 2,5 g/m ±10% |
| Retração após 24 h a 60 °C | por lote | **≤ 1,0%** — crítico: 3% em 88 cm são 2,6 cm, e a junta abre |
| Carta de conformidade ANVISA, contato com alimento | **por fornecedor, antes da 1ª amostra** | grau específico, não a família |
| Segunda fonte homologada | antes da produção | **exigência, não preferência** — resina de fonte única foi o que reprovou o Tritan |

**Ferramenta de perfil como ativo da Nitron**, ainda que fisicamente no extrusor. É o que permite
trocar de fornecedor sem refazer o desenvolvimento.

### Suprimento: comprar, nunca extrudar

Consumo máximo, com as 18 tampas e 855 mil peças: **1.387 kg/ano**. Contra 2.605 t de resina que
a fábrica compra — **0,05% da massa da casa**. Uma linha de extrusão custa R$ 350–700 k para rodar
**15% de um único turno**. Comprar fita pronta em bobina de um extrusor de perfil de vedação é a
única rota racional.

---

## 7. O que precisa ser medido antes de fechar este desenho

Duas cotas deste documento são provisórias, e ambas dependem de uma medição de bancada que **não
precisa de lacre nenhum para acontecer**:

| Cota provisória | Medição que a fecha | Custo |
|---|---|---|
| Altura do lábio (1,40 mm) | Curso livre da trava fechada, com paquímetro | paquímetro |
| Viabilidade do conceito inteiro | **Quanto a força de ABRIR sobe** com perfil de 1,0 / 1,5 / 2,0 mm | ~R$ 200 de perfil de esquadria |

A segunda é a que decide. No concorrente que veda bem (Plasútil porta-frios), **32,3% das
avaliações negativas são sobre abrir duro e trava quebrando**. A força que veda é a mesma que
trava o produto na mão do consumidor. Se a força de abrir subir muito já em 1,0 mm, este
documento inteiro está reprovado por uso — e provavelmente explica por que as refs `176.024.001`
e `210.024.001` (trava + válvula) são as **únicas duas quedas** numa plataforma que cresce 49,9%.

Ambas as medições estão na aba **Travas** de `ensaios/protocolo-ensaio-estanqueidade.xlsx`.

---

## 8. O que reabriria o caso

O veto cai se um destes dois for **medido**, não estimado:

1. **Teste de preço real:** mesma SKU, dois preços, mesmo canal, 8 semanas, na base de 1.121
   clientes do `233.012.001`, mostrando disposição a pagar ≥ +6%. Análise de anúncio de
   concorrente já foi feita e deu delta zero a negativo — não conta.
2. **Ou:** a medição de §7 mostrando que a força de abrir **não sobe**, **combinada** com falha do
   produto atual no ensaio de vedação. Nesse cenário o lacre deixa de ser upgrade opcional e vira
   correção de conformidade — outro business case, com outro ônus da prova.

Enquanto nenhum dos dois existir, este documento fica na gaveta.
