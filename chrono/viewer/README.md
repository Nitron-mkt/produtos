# Visualizador 3D do datador

`datador.html` + `malhas.js`, publicado como Artifact. Gira o aro dos meses e a seta
dos dias, explode o conjunto, corta ao meio e liga/desliga cada peça e a tampa.

As malhas vão **embutidas** em `malhas.js`, não como arquivo à parte: o Artifact só
serve tipos de mídia padrão da web, e `.bin`/`.stl` não passam. Formato: posições em
`uint16` sobre a caixa de cada peça (50 mm / 65535 = **0,0008 mm** de passo, bem
abaixo de qualquer cota do projeto) e índices em `uint16`. 1,91 MB no total, contra
5,3 MB do mesmo conteúdo em float32.

A tampa entra recortada num disco de Ø58 em torno do eixo da válvula — o resto do
disco da tampa é material que não diz nada sobre o encaixe e custaria 4× mais malha.

Cinemática, que é o que o visualizador existe para mostrar:

```
aro dos meses (M02):  rotation.y = +(mes-1) × 30°
seta (M03):           rotation.y = −(dia-1) × 360/31°
```

Os dois sinais são opostos porque o mês é lido contra um **índice fixo na válvula**
(o aro é que gira até o mês certo), e o dia é lido pela **seta que gira** contra os
números fixos. São dois graus de liberdade independentes — é por isso que a travinha
gira solta no poste em vez de ser travada nele.

Regerar `malhas.js`: o bloco `pack()` em `../medicao_v2/` (veja o histórico do commit
que criou este diretório) lê os STL de `../stl_v2/`, quantiza e grava o arquivo.
