# Os arquivos .step

| arquivo | corpo da válvula | passa no portão? |
|---|---|---|
| `Chrono_M01_Valvula_Dias_COM_VALVULA.step` | **a válvula injetada**, facetada | 8 de 10 — leia abaixo |
| `Chrono_M01_Valvula_Dias__CORPO_DE_PROVA.step` | disco Ø38 no lugar dela | **10 de 10** |
| `Chrono_M02_Rodinha_Meses.step` | — | **10 de 10** |
| `Chrono_M03_Ponteira.step` | — | **10 de 10** |

Os quatro são **um sólido fechado cada**, e nos quatro o leitor de STEP devolve
`TopAbs_SOLID` — não composto, não casca, não conjunto de superfícies.

## A M01 com a válvula: abra esta primeiro, mas leia isto

A válvula nunca existiu como superfície exata — ela chegou como malha. Aqui ela
entra como **sólido de faces planas**, e o que o Chrono acrescenta entra por cima
com **superfície exata**: os 31 numerais, o rebaixo, as 2 molas, o poste e o furo
são cilindro, cone e spline de verdade, selecionáveis e cotáveis.

Erro do corpo facetado contra a malha original da válvula: **máximo 0,039 mm,
médio 0,007 mm**. Conferido contra uma montagem independente, feita só com
booleano de malha: desvio máximo **0,049 mm**, volume dentro de 0,41%, fechada.
A geometria está certa.

**O risco, dito com número:** o booleano entre as facetas da válvula e as
superfícies exatas do Chrono cria aresta curta onde uma faceta tangencia uma
superfície de corte. São **231 arestas abaixo de 0,05 mm, a menor com 0,0023 mm**
— a mesma ordem de grandeza do arquivo que abriu "fatiado" no SolidWorks (763
abaixo de 0,01 mm, a menor com 0,0015). Tentei limpar com `ShapeFix_Wireframe`:
a 0,02 mm sobram 189 arestas curtas; a 0,06 mm caem para 18 **mas o sólido fica
inválido**, com face de área negativa. Não há conserto que mantenha a peça válida.

**Então:** abra este arquivo. Se ele vier fatiado, não é o projeto — é esse
defeito, e aí o caminho é o `__CORPO_DE_PROVA` mais a receita de 4 passos.

## A M01 corpo de prova

Mesmo Chrono, com um disco de Ø38,00 no lugar da válvula, de Y 35,40 a 37,23.
Passa nas dez checagens. Serve para medir a geometria do Chrono com exatidão —
nenhuma faceta, nenhuma aresta curta: a menor tem 0,10 mm.

## O caminho certo para a ferramenta

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
que cortar) e o poste entra depois (senão o rebaixo raspa as molas). Aplicada no
CAD mestre, produz a mesma peça com o corpo exato — e é o único jeito de a
geometria já ferramentada sair **bit a bit igual**. Os quatro passam nas dez.

## As dez checagens (`python3 fechamento.py step_completo`)

| | |
|---|---|
| 1 | declara `MANIFOLD_SOLID_BREP` e `CLOSED_SHELL`, sem `OPEN_SHELL` nem `SHELL_BASED_SURFACE_MODEL` |
| 2 | exatamente 1 sólido e 1 casca |
| 3 | casca fechada, nenhuma aresta livre |
| 4 | toda aresta usada por exatamente 2 faces |
| 5 | `BRepCheck_Analyzer` válido |
| 6 | volume positivo |
| 7 | sem auto-intersecção |
| 8 | malha a 0,01 mm watertight e batendo com o volume do B-rep |
| 9 | ida e volta: volume e caixa iguais |
| 10 | o leitor de STEP devolve `TopAbs_SOLID` |

Mais o porteiro de arestas (`python3 qualidade.py step_completo`): nenhuma aresta
abaixo de 0,05 mm e nenhuma face abaixo de 0,002 mm².

## O portador enterrado

O `1_SOMAR` tem, além do enchimento, um **anel de r 13,00 a 18,60 que começa
0,30 mm abaixo da face de topo e termina na face**. Não aparece na peça (topo
coplanar com a face, parede dentro dos 1,83 mm da chapa) e serve só para os 31
numerais saírem costurados num sólido só — sem ele o arquivo abre com 44 corpos
soltos. Por isso esse anel não tem ângulo de saída: nunca é superfície de molde.
