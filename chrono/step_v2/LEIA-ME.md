# Chrono datador — arquivos CAD para a ferramentaria

## Sobre o `.x_t`

**Não consigo gerar `.x_t` aqui.** `.x_t` é Parasolid, o núcleo proprietário da
Siemens. Só quem tem licença do kernel escreve esse formato — não existe gerador
livre, e este ambiente não tem CAD comercial instalado.

O que eu gerei foi **STEP (AP214)**, que é o formato neutro equivalente: sólido
B-rep de verdade, com cilindro, plano e revolução analíticos — **não é malha**.

**Qualquer CAD converte STEP em `.x_t` num clique:** NX, Solid Edge, SolidWorks,
Creo, Inventor, Fusion 360 — abre o `.step` e salva como `.x_t`. Se a
ferramentaria pediu `.x_t` só porque é o padrão da casa, mande o STEP que eles
fazem a conversão em 10 segundos, sem perda: os dois são B-rep.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `Chrono_M02_Rodinha_Meses.step` | peça completa, sólido fechado |
| `Chrono_M03_Ponteira.step` | peça completa, sólido fechado |
| `Chrono_M01a_SUBTRAIR_1_rebaixo.step` | ← ver receita abaixo |
| `Chrono_M01b_SOMAR_2_poste_mesa_dias_detentes.step` | ← ver receita abaixo |
| `Chrono_M01c_SUBTRAIR_3_furo_passante.step` | ← ver receita abaixo |

Todos no **mesmo sistema de coordenadas dos STL**, com o centro do poço da válvula
em X 61,97 / Z 102,68 e a face de topo da válvula em Y 37,23. Unidade: milímetro.
Basta importar por cima do CAD da tampa que tudo cai no lugar, sem alinhar nada.

## Por que a M01 vem em três arquivos

A metade de baixo da válvula **não é desenho meu** — ela foi replicada do STL da
peça que vocês já injetam, para garantir que o balancim e a vedação não mudam. STL
é malha: não dá para virar sólido B-rep sem redesenhar. Então, em vez de entregar
uma M01 facetada e inútil para ferramenta, entrego **só o que o Chrono acrescenta**,
como sólido de verdade, para ser aplicado sobre o CAD original da válvula.

**Receita, nesta ordem:**

```
válvula final = (( CAD original da válvula  −  M01a_rebaixo )
                                            +  M01b_poste_mesa_dias_detentes )
                                            −  M01c_furo_passante
```

⚠️ **A ordem importa.** O rebaixo sai **antes** do acréscimo porque as duas molas
de detente nascem no **fundo** do rebaixo — se subtrair o rebaixo depois, elas são
raspadas junto.

`M01b` vem com 4 sólidos soltos (mesa+dias, poste, e as 2 molas de detente). É
assim mesmo: eles se fundem ao corpo da válvula na operação de soma.

## Conferência

A receita foi verificada contra a peça validada `Chrono_M01_Valvula_Dias.stl`:

| | volume | desvio médio | desvio máx |
|---|---|---|---|
| M02 STEP × STL | −0,033% | 0,0003 mm | 0,0036 mm |
| M03 STEP × STL | −0,002% | 0,0001 mm | 0,0032 mm |
| receita M01 × STL | +0,002% | 0,0001 mm | 0,0049 mm |

Os desvios são tesselação, não geometria. (Em 300.000 pontos amostrados na M01,
**2** passam de 0,02 mm, os dois na parede do furo Ø6,00 no encontro com o chanfro
— é faceta do STL, o STEP é o lado limpo.)

Todos os cinco arquivos passam no `BRepCheck_Analyzer` do OpenCASCADE: **B-rep válido**.

Para refazer: `python3 medicao_v2/step.py tudo`, conferir com
`confere_step.py` e `confere_m01.py`.
