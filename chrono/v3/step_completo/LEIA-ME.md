# Os 3 arquivos .step — sem facetas

| arquivo | faces triangulares | passa no portão |
|---|---|---|
| `Chrono_M01_Valvula_Dias.step` | **3** | **11 de 11** |
| `Chrono_M02_Rodinha_Meses.step` | **1** | **11 de 11** |
| `Chrono_M03_Ponteira.step` | **0** | **11 de 11** |

Antes era 8.730 faces triangulares na M01. Era isso que aparecia fatiado na
tela: o corpo da válvula vinha de uma malha, e malha em STEP é triângulo.

## Por que o anterior vinha fatiado

A válvula nunca existiu como superfície exata — ela chegou como STL. Levar
malha para STEP produz sólido facetado: ele abre, é um sólido de verdade, mas
**aparece com os triângulos**, que foi o que o projetista viu no aro e nas
orelhas.

## O que mudou

O corpo da válvula foi **medido e refeito com superfície exata** — plano,
cilindro, cone e esfera. Todas as cotas saíram de cortes do STL em 9 ângulos:

| | |
|---|---|
| face de baixo | Y 35,400 |
| face de topo | Y 37,230 |
| diâmetro externo | Ø38,09 (r 19,042) |
| quebra do aro | 0,10 a 45,000° na aresta de cima |
| orelhas | 2 esferas **R1,878** em r 20,22, Y 34,69, a 0° e 180° |

As orelhas são esferas e isso não é chute: a largura tangencial medida bate com
2R em todas as 9 alturas conferidas (3,756 mm no equador, Y 32,811 a 36,568).

Tudo o que o Chrono acrescenta continua com **superfície exata**: os 31
numerais, o rebaixo, as 2 molas, o poste e o furo são cilindro, cone e spline de
verdade, selecionáveis e cotáveis.

## ⚠️ O que não está na M01

**A saia e os pinos da válvula, tudo abaixo de Y 35,400.** Medi para saber se
dava para refazer com superfície exata: não dá. A seção da peça **varia
continuamente com o ângulo** — de 21,08 a 48,17 mm² ao longo da volta —, então
não é um corpo de revolução nem uma união de setores girados. Refazer isso seria
inventar a peça do cliente, e o desvio da minha melhor tentativa chegou a 0,9 mm.

O que está lá é exato; o que falta está declarado.

## Para ter a válvula inteira E sem faceta

A pasta `../step/` tem a M01 como **receita de 4 passos** sobre o CAD da válvula
que a ferramentaria já tem. É uma sequência de booleanos no SolidWorks:

```
válvula final = (((CAD da válvula + 1_SOMAR) − 2_SUBTRAIR) + 3_SOMAR) − 4_SUBTRAIR
```

1. `Chrono_v3_M01_1_SOMAR_enchimento_e_dias` — enchimento da concha das 12 h,
   portador enterrado e os 31 numerais
2. `Chrono_v3_M01_2_SUBTRAIR_rebaixo_com_detentes`
3. `Chrono_v3_M01_3_SOMAR_poste`
4. `Chrono_v3_M01_4_SUBTRAIR_furo_passante`

A ordem importa: o enchimento entra antes do rebaixo (senão o rebaixo não tem o
que cortar) e o poste entra depois (senão o rebaixo raspa as molas).

Esse é o único caminho que dá as duas coisas ao mesmo tempo — a válvula completa
**e** sem faceta —, porque a superfície exata da válvula só existe no CAD dela.
E é também o único que garante que a geometria já ferramentada saia bit a bit
igual. Os quatro arquivos passam nas onze checagens.

A válvula inteira, para ver e conferir, está em `../stl/` como STL.

## As onze checagens (`python3 fechamento.py step_completo`)

| | |
|---|---|
| 1 | declara `MANIFOLD_SOLID_BREP` e `CLOSED_SHELL`, sem `OPEN_SHELL` nem `SHELL_BASED_SURFACE_MODEL` |
| 2 | exatamente 1 sólido e 1 casca |
| 3 | casca fechada, nenhuma aresta livre |
| 4 | toda aresta usada por exatamente 2 faces (aresta degenerada, como o polo de uma esfera, não conta) |
| 5 | `BRepCheck_Analyzer` válido |
| 6 | volume positivo |
| 7 | sem auto-intersecção |
| 8 | malha a 0,01 mm watertight e batendo com o volume do B-rep |
| 9 | ida e volta: volume e caixa iguais |
| 10 | o leitor de STEP devolve `TopAbs_SOLID` |
| 11 | **não é sopa de triângulo**: menos de 100 faces planas de 3 arestas |

Mais o porteiro de arestas (`python3 qualidade.py step_completo`): a menor aresta
dos três arquivos tem **0,0710 mm**; a que desmanchava a costura tinha 0,0015.

## O portador enterrado

O `1_SOMAR` tem, além do enchimento, um **anel de r 13,00 a 18,60 que começa
0,30 mm abaixo da face de topo e termina na face**. Não aparece na peça e serve
só para os 31 numerais saírem costurados num sólido só — sem ele o arquivo abre
com 44 corpos soltos. Por isso não tem ângulo de saída: nunca é superfície de
molde.
