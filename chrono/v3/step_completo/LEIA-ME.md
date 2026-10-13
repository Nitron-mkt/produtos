# Os 3 arquivos finais

| arquivo | o que é | sólido |
|---|---|---|
| `Chrono_M01_Valvula_Dias__CORPO_DE_PROVA.step` | válvula com os 31 dias, o rebaixo, as 2 molas, o poste e o furo | 1 |
| `Chrono_M02_Rodinha_Meses.step` | rodinha dos 12 meses | 1 |
| `Chrono_M03_Ponteira.step` | ponteira com a janela, o MÊS e o ícone | 1 |

Cada um abre como **um sólido fechado**, não como conjunto de superfícies.

## O fechamento, conferido item por item

`python3 fechamento.py step_completo` — dez checagens por arquivo, todas passam:

| | |
|---|---|
| 1 | o texto do STEP declara `MANIFOLD_SOLID_BREP` e `CLOSED_SHELL`, e nenhum `OPEN_SHELL` ou `SHELL_BASED_SURFACE_MODEL` |
| 2 | exatamente **1 sólido** e **1 casca** |
| 3 | a casca é fechada — nenhuma aresta livre |
| 4 | **toda aresta é usada por exatamente 2 faces** (costura completa) |
| 5 | `BRepCheck_Analyzer` válido |
| 6 | volume positivo — a peça não está do avesso |
| 7 | sem auto-intersecção |
| 8 | tesselada a 0,01 mm a malha é watertight e bate com o volume do B-rep |
| 9 | ida e volta (exportar → reimportar): volume e caixa iguais a 1,4·10⁻¹⁴ mm |
| 10 | o **leitor de STEP** devolve `TopAbs_SOLID` — não composto, não casca |

E o porteiro de arestas (`python3 qualidade.py step_completo`), que é o que pegou
o problema do arquivo que abriu "fatiado":

```
                                               sol. aresta min  curtas  face min  micro
Chrono_M01_Valvula_Dias__CORPO_DE_PROVA.step     1     0,1000      0     0,01004    0   ok
Chrono_M02_Rodinha_Meses.step                    1     0,0710      0     0,01002    0   ok
Chrono_M03_Ponteira.step                         1     0,1000      0     0,01001    0   ok
```

Nenhuma aresta abaixo de 0,05 mm, nenhuma face abaixo de 0,002 mm². A menor
aresta do conjunto tem **0,0710 mm**; a que desmanchava a costura na importação
tinha 0,0015 mm.

Cada arquivo leva o próprio nome **dentro** dele (`PRODUCT`), então o SolidWorks
mostra "Chrono M01 - valvula com os dias" na árvore, e não "Open CASCADE
translator". É ali que a informação sobrevive a um "salvar como".

## ⚠️ A M01: o corpo é de prova

O corpo abaixo da face de topo **não é a válvula injetada**: é um disco de Ø38,00
com a mesma saída, de Y 35,40 a 37,23. Está escrito na descrição dentro do
arquivo, não só no nome.

**Exato nesse arquivo:** os datums (eixo em X 61,97 / Z 102,68, face de topo
Y 37,23, face de baixo Y 35,40) e **tudo o que o Chrono acrescenta** — os 31
numerais, o rebaixo, as 2 molas, o poste e o furo. É o que está em revisão, e
está com superfície exata e selecionável.

**Não está:** a saia, os pés e os lóbulos da válvula, abaixo de Y 35,40.

### Por que a válvula não entra aqui

A válvula nunca existiu como superfície exata — ela chegou como malha. Levar
malha para STEP produz sólido facetado, e isso foi testado, não suposto:

| triângulos | erro máximo | arquivo |
|---|---|---|
| 6.000 | 1,04 mm | 15,2 MB |
| 12.000 | 0,15 mm | 30,6 MB |
| sem perda | 0 | ~150 MB |

O relevo dos numerais tem **0,10 mm**: um arquivo com 0,15 mm de erro apaga
exatamente o que está em revisão. E a tentativa de montar só a válvula facetada
(10.000 triângulos) com o Chrono exato **não fecha** — a casca costurada sai
inválida e os booleanos colapsam.

**A válvula de verdade vai em STL**, que é o formato em que ela sempre existiu:

- `../stl/Chrono_v4_M01_COM_VALVULA.stl` — a peça inteira
- `../stl/Chrono_v4_CONJUNTO_COM_VALVULA.stl` — as três montadas
- `../stl/Chrono_v4_M00_Valvula_recuperada.stl` — só a válvula

### O caminho certo para a ferramenta

A pasta `../step/` tem a M01 como **receita de 4 passos** sobre o CAD da válvula
que a ferramentaria já tem:

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

Aplicada no CAD mestre, a receita produz esta mesma peça com o corpo certo — e é
o único jeito de a geometria já ferramentada sair **bit a bit igual**. Os quatro
arquivos passam no mesmo fechamento: 1 sólido, leitor devolve SOLID, sem aresta
livre.

## O portador enterrado

O `1_SOMAR` tem, além do enchimento, um **anel de r 13,00 a 18,60 que começa
0,30 mm abaixo da face de topo e termina na face**. Ele não aparece na peça
(topo coplanar com a face, parede dentro dos 1,83 mm da chapa) e serve só para os
31 numerais saírem costurados num sólido só — sem ele o arquivo abre com 44
corpos soltos. Por isso esse anel não tem ângulo de saída: ele nunca é superfície
de molde. Depois de somado à válvula, some.
