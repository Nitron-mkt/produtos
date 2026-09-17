# A impressora parou de imprimir — como descobrir de quem é a culpa

Dois arquivos, nesta ordem. São pequenos (a Ponteira, ~13 min). O objetivo não é
ter peça boa, é **separar arquivo de máquina**.

## PROVA_1.gcode
É uma **cópia byte a byte** de `Chrono_3_de_3_Ponteira.gcode` — o arquivo em PLA
que já imprimiu na sua máquina. Não mudei nada. Rode com **PLA**, o mesmo que
estava rodando quando funcionou.

- **Imprimiu** → a máquina está boa. O problema está nos meus arquivos PETG. Vá ao PROVA_2.
- **Não imprimiu** → a máquina mudou. Não adianta eu mexer em gcode. Pule para "Se o PROVA_1 falhar".

## PROVA_2.gcode
É o **mesmo arquivo**, com exatamente **3 linhas** diferentes — só as temperaturas:

| linha | PROVA_1 | PROVA_2 |
|---|---|---|
| 96 | `G9111 bedTemp=65 extruderTemp=210` | `G9111 bedTemp=80 extruderTemp=245` |
| 2075 | `M104 S205` | `M104 S240` |
| 2076 | `M140 S60` | `M140 S80` |

Tudo o mais — velocidade, fluxo, cooler, retração, brim — é o do PLA. Rode com
**PETG**. A peça vai sair feia (cooler a 100% é demais para PETG); não importa.

- **Imprimiu** → a máquina aceita PETG e aceita as temperaturas. Então o defeito
  está em alguma outra coisa que eu mudei no perfil PETG, e dá para achar mudando
  uma de cada vez.
- **Não imprimiu** → a recusa é ligada à temperatura/material, não ao meu fatiamento.

---

## Se o PROVA_1 falhar (a máquina)

Na ordem, do mais provável ao menos:

1. **Desligue na tomada, espere 30 s, ligue.** Arquivo recusado várias vezes deixa
   a Kobra 3 num estado travado que só o corte de energia limpa.
2. **Z offset.** Eu te mandei baixar "de 0,02 em 0,02" para colar melhor. Se foi longe
   demais, o bico encosta na mesa, o Klipper aborta e às vezes nem começa.
   Volte o Z offset para o valor de fábrica e refaça o auto-nivelamento.
3. **Entupimento.** Se o PETG rodou com temperatura de PLA (205–210 °C) em algum momento,
   provavelmente carbonizou no bico. Aqueça a 250 °C e faça extrusão manual de 50 mm:
   se não sai filamento parelho, é entupimento — troque o bico ou faça cold pull.
4. **O pen drive / cartão.** Formate em **FAT32**, copie um arquivo só, ejete pelo
   sistema antes de tirar. Arquivo copiado pela metade some do menu ou é recusado.
5. **Atualização de firmware.** Se a impressora se atualizou sozinha, o formato aceito
   pode ter mudado. Nesse caso o teste definitivo é o próximo item.

## O teste que me tira do caminho

Instale o **Anycubic Slicer Next** (ou o Anycubic Slicer), abra
`chrono/stl_v2/Chrono_M03_Ponteira.stl`, escolha o perfil PETG da Kobra 3 e fatie lá.
Se **esse** arquivo imprimir, o problema é meu gcode e eu conserto com o que você
me contar. Se **nem ele** imprimir, é máquina, e nenhum arquivo que eu gerar vai
resolver.
