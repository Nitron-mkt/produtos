# Aro de vedação — projeto simples

**Escopo:** só os potes com travas. 4 aros, 6 referências de produto.
**Diagnóstico da fábrica:** os potes são PP e **vazam em todo o perímetro** — não há elemento de
vedação nenhum. PP rígido contra PP rígido, com tolerância de injeção, não sela.
**Este documento substitui `09-projeto-borrachas-tpe.md`** na parte de como o aro se fixa.

---

## 1. A ideia em uma frase

Um **perfil em U** que se calça na ponta da saia da tampa, como um friso, com uma **aba de
vedação** que encosta na parede interna do pote.

**Nenhuma usinagem de molde. Nenhuma peça nova injetada. Reversível.**

---

## 2. Como funciona

```
   ┌──────────────────────────────────┐  ← tampa
   │                                  │
   └────┐                        ┌────┘
        │                        │
        │ saia da tampa          │
        │                        │
     ═══╧════                ════╧═══
    ┃  U   ┃                  ┃  U   ┃   ← aro em U calçado na ponta da saia
    ┃      ┃                  ┃      ┃
     ╲aba              aba    ╱
      ●                      ●             ← aba encosta na parede interna
      ┃                      ┃
   ═══╹══════════════════════ ╹═══  ← parede interna do pote

              CORTE DA SEÇÃO DO ARO

              ← largura ~2,8 →
            ┌───────────────────┐
            │  ╔═════════════╗  │  ← fundo do U
            │  ║   ▲     ▲   ║  │     garras internas (2 pares)
     aba →  │  ║  saia da    ║  │     mordem a saia da tampa
    0,55mm  ╲  ║   tampa     ║  │
       35°   ╲ ║   entra     ║  │  profundidade do U: 4,0 mm
              ●╚═════════════╝  │
               └───────────────┘
               ↑
          ponta de contato — encosta na parede do pote
```

**Três coisas acontecendo ao mesmo tempo:**

1. **O U aperta a saia** e segura o aro na tampa — por atrito, sem cola.
2. **A aba encosta na parede interna** do pote e faz a vedação.
3. **A pressão interna empurra a aba contra a parede** — quanto mais precisa vedar, melhor veda.
   A aba é inclinada para dentro do pote exatamente para isso.

---

## 3. Por que esta rota e não a que eu tinha proposto antes

| | Canal usinado na tampa | **Aro em U calçado** |
|---|---|---|
| Modificação de molde | solda + usinagem em 5 moldes | **nenhuma** |
| Investimento em ferramental | R$ 26.000 – 63.000 | **R$ 0** |
| Fila de ferramentaria | 5 moldes, semanas | **nenhuma** |
| Reversível se não funcionar | não — o aço já foi soldado | **sim, é só tirar o aro** |
| Risco de rechupe na face visível | sim, e 66% do faturamento é transparente | **não existe** |
| Pode testar | depois do rework | **esta semana, com perfil comercial** |

**A retenção não é problema.** O U apertando a saia com 0,15 mm de interferência gera 400–500 N de
força de aperto e mais de 200 N de atrito, contra um aro que pesa 2 gramas. Ele não sai sozinho —
sai se o consumidor puxar de propósito, o que é aceitável e até desejável (permite lavar separado).

---

## 4. A seção do aro — uma só, para as quatro tampas

| Cota | Valor | Depende de medir? |
|---|---|---|
| **Abertura interna do U** | **espessura da saia − 0,15 mm** | 🔲 **sim — medição 1** |
| Profundidade do U | 4,0 mm | não |
| Parede do U | 0,8 mm | não |
| Largura externa | espessura da saia + 1,6 mm | 🔲 decorre da medição 1 |
| Garras internas | 2 pares, 30° | não |
| **Espessura da aba de vedação** | **0,55 mm** | não |
| Comprimento livre da aba | 2,2 mm | não |
| Ângulo da aba (repouso) | 35° para dentro do pote | não |
| **Interferência da aba contra a parede** | **0,6 a 0,8 mm** | 🔲 **sim — medição 2** |
| Massa linear | ~2,6 g/m | não |

Referência para a medição 1, para você já ir com números na cabeça:

| Se a saia tiver | abertura do U | largura externa |
|---|---|---|
| 1,0 mm | 0,85 mm | 2,60 mm |
| 1,2 mm | 1,05 mm | 2,80 mm |
| 1,5 mm | 1,35 mm | 3,10 mm |

⚠️ **Interferência maior do que eu havia especificado antes.** No documento 09 eu tinha posto
0,50 mm, supondo que a folga tampa/corpo fosse pequena. **Como vaza no perímetro inteiro, a folga
é maior** — por isso 0,6 a 0,8 mm. A medição 2 fecha esse número.

---

## 5. Material

**TPV base PP, shore A 55 ± 5.**

| Por quê | |
|---|---|
| Base PP | volta para o ciclo de moído sem contaminar (o ativo de R$ 2,63 M/ano) |
| Shore 55 | rígido o bastante para o U segurar, flexível o bastante para a aba vedar |
| TPV e não TPE-S | **compression set.** TPE-S cansa sob carga e o pote "afrouxa depois de um tempo" — é literalmente a reclamação dos concorrentes |
| Contato com alimento | exigir carta do **grau específico**, não da família |

⚠️ **Não peça "borracha" ao fornecedor.** No mercado isso significa EPDM ou NBR vulcanizado, que
não é compatível com o moído de PP. Peça **"perfil extrudado em TPV base PP"**.

---

## 6. Os quatro aros

| Aro | Tampa (PI) | Produtos | Perímetro da saia 🔲 | Corte (−1,5%) 🔲 |
|---|---|---|---|---|
| **A1** | 816 | Raso 1,1 L (233) + Alto 2,2 L (156) | 🔲 medir | 🔲 |
| **A2** | 799 | Raso 2,3 L (234) + Alto 4,3 L (151) | 🔲 medir | 🔲 |
| **A3** | 575 | Quadrado 1,8 L (3770) | 🔲 medir | 🔲 |
| **A4** | 924 | Ultraforte 2,1 L (215) | 🔲 medir | 🔲 |

**Quatro aros cobrem seis produtos** — a tampa 816 serve Raso 1,1 L e Alto 2,2 L, a 799 serve Raso
2,3 L e Alto 4,3 L. Confirmado pelo BOM, não por inferência.

Corte **1,5% menor** que o perímetro: o aro monta esticado, o que o mantém assentado e deixa a
junta sob compressão em vez de tração — junta tracionada é junta que vaza.

**Junta:** corte em cunha a 30°, solda térmica, sempre no meio de um lado reto, nunca no canto.

---

## 7. As três medições — meia hora, hoje

Tudo com paquímetro e um pedaço de fio de solda.

| # | O que medir | Como | Para que |
|---|---|---|---|
| **1** | **Espessura da saia da tampa** | Paquímetro na ponta da saia, 4 pontos | Define a abertura do U |
| **2** | **Folga entre a saia da tampa e a parede do pote**, com a tampa travada | Paquímetro, ou calibrador de folga, 4 pontos | Define a interferência da aba |
| **3** | **Perímetro da saia**, nas 4 tampas | Fio de solda contornando a saia, esticar e medir na trena | Define o comprimento de corte |

**Enquanto isso:** confirmar que a saia tem **pelo menos 5 mm de altura livre**, para o U de 4 mm
se calçar. Se a saia for mais curta que isso, me avise — muda a profundidade do U.

---

## 8. Teste desta semana, R$ 200

Não precisa esperar fornecedor nem ferramenta:

1. Comprar **perfil de vedação em U** de esquadria ou de borda de chapa (existe em loja de material
   de construção e em autopeças, como friso de vedação de porta).
2. Calçar na saia de 3 tampas de produção de cada família.
3. Fechar o pote, encher 80% com água e corante, **inverter 24 h** sobre papel-toalha branco.
4. Medir a força de fechar e de abrir, com e sem o aro.
5. Abrir e fechar 50 vezes e ver se o aro sai do lugar.

Use as abas **E1-Vazamento** e **Travas** de `ensaios/protocolo-ensaio-estanqueidade.xlsx`.

**O que este teste responde:** se o conceito veda, se a tampa continua fácil de abrir, e se o aro
fica no lugar. Se as três derem certo, o resto é só cotar o perfil na cota certa.

---

## 9. Custo estimado

| | Manual | Com jiga simples |
|---|---:|---:|
| Material (2,6 g/m, TPV a R$ 60/kg) | R$ 0,11 – 0,13 | R$ 0,11 – 0,13 |
| Montagem (calçar o aro) | R$ 0,08 (15 s) | R$ 0,04 (7 s) |
| **Total por peça** | **R$ 0,19 – 0,21** | **R$ 0,15 – 0,17** |
| **Custo anual (346.572 peças)** | **≈ R$ 69.000** | **≈ R$ 55.000** |

Calçar um U é mais rápido que assentar um aro em canal — a estimativa de montagem caiu de 25 s
para ~15 s. **Cronometrar 50 peças no piloto** para trocar a estimativa por medição.

### Investimento

| Item | Valor |
|---|---|
| Teste de bancada | R$ 200 |
| Ferramenta de perfil do extrusor (matriz + calibrador) | R$ 8.000 – 20.000 |
| Jiga de corte e solda | R$ 8.000 – 25.000 |
| Ensaios e homologação | R$ 3.000 – 8.000 |
| **Total** | **R$ 19.000 – 53.000** |

**Sem molde. Sem ferramentaria.** Contra R$ 54–135 k da rota com canal usinado.

---

## 10. Plano B, se a retenção falhar

Se no teste de 50 ciclos o aro sair do lugar, há duas saídas antes de partir para usinar molde:

1. **Aumentar a interferência do U** de 0,15 para 0,25 mm e adicionar um terceiro par de garras.
2. **Um ressalto na saia** — este sim é rework de molde, mas é um **rebaixo raso de 0,3 mm** para
   a garra do U travar, muito mais simples que um canal de vedação completo.

Só depois disso a rota do canal usinado volta à mesa.

---

## Resumo

1. **Aro em U calçado na saia da tampa.** Zero molde, zero ferramentaria, reversível.
2. **Uma seção, quatro comprimentos**, seis produtos atendidos.
3. **TPV base PP shore A 55** — não "borracha", não TPE-S barato.
4. **Três medições de meia hora** e o desenho fecha.
5. **Teste de R$ 200 esta semana** responde se funciona, antes de gastar qualquer coisa.
6. **R$ 19–53 k de investimento**, R$ 0,19–0,21 por peça.
