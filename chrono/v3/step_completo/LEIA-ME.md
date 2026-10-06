# As 3 peças completas — um sólido cada

| arquivo | o que é | sólidos |
|---|---|---|
| `Chrono_M01_Valvula_Dias__CHAPA_DE_PROVA.step` | válvula com a mesa, os 31 dias, o rebaixo, as 2 molas, o poste e o furo | 1 |
| `Chrono_M02_Rodinha_Meses.step` | rodinha dos 12 meses | 1 |
| `Chrono_M03_Ponteira.step` | ponteira com a janela, o MÊS e o ícone | 1 |

Os três abrem direto: 1 sólido, B-rep válido, nenhuma aresta abaixo de 0,05 mm e
nenhuma face abaixo de 0,002 mm². Conferido com `python3 qualidade.py step_completo`.

## ⚠️ Leia antes de usar a M01

**O corpo da válvula neste arquivo é uma CHAPA DE PROVA**, não a peça injetada:
disco de Ø38,00 com a mesma saída de 1,5°, da face de baixo (Y 35,40) à face de
topo (Y 37,23). O STL da válvula real saiu da sessão quando o container foi
recriado e não é recuperável daqui.

O que está **exato** nesse arquivo: os datums (eixo em X 61,97 / Z 102,68, face de
topo em Y 37,23, face de baixo em Y 35,40) e **tudo o que o Chrono acrescenta** —
mesa, numerais, rebaixo, molas, poste, furo. É o que está em revisão.

O que **não** está: a saia e os pés da válvula, abaixo de Y 35,40.

## O que vai para a ferramenta é a pasta `../step/`

Lá a M01 é uma **receita de 4 passos** sobre o CAD da válvula que já existe:

```
válvula final = (((CAD da válvula + 1_SOMAR) − 2_SUBTRAIR) + 3_SOMAR) − 4_SUBTRAIR
```

1. `Chrono_v3_M01_1_SOMAR_enchimento_mesa_dias`
2. `Chrono_v3_M01_2_SUBTRAIR_rebaixo_com_detentes`
3. `Chrono_v3_M01_3_SOMAR_poste`
4. `Chrono_v3_M01_4_SUBTRAIR_furo_passante`

A ordem importa: o enchimento entra antes do rebaixo (senão o rebaixo não tem o
que cortar) e o poste entra depois (senão o rebaixo raspa as molas).

**É assim de propósito.** O molde da tampa não pode ser mexido, e a receita
garante que a geometria já ferramentada saia bit a bit igual à do CAD mestre —
coisa que nenhuma reconstrução minha garante. Aplicada no CAD da válvula, a
receita produz exatamente esta peça, com o corpo certo no lugar da chapa de prova.

Para a M02 e a M03 não há essa distinção: as duas são peças novas inteiras, e os
arquivos das duas pastas são o mesmo sólido.
