# Sinalização do showroom Nitron Mob

`gerar.py` escreve os seis artboards (`*.dc.html`) e o `canvas.json` a partir dos
vetores oficiais do kit de marca (marca.nitron.com.br → nitron-logos.zip). Nenhum
logo é redesenhado: símbolo, lettering e assinatura são os paths do `.ai`; o lockup
horizontal é composto com as proporções lidas do lockup vertical (assinatura a 75%
do lettering, gap 7,96/40,78).

O arquivo `sinalizacao-showroom-nitron-mob.html` é o canvas publicado (Claude Design).
Para alterar: editar `gerar.py`, rodar, resemear com o helper do skill `design`, republicar.

Peças e medidas reais (escala 2 px/mm nos artboards de peça):
- Testeira 754 × 200 mm, uma por vão, base a 1.900 mm em hastes nos nós de topo
- Faixa de prateleira 754 × 40 mm, uma por vão, em todas as prateleiras
- Stopper 100 × 150 mm, duas faces, uma por ponta de parede
- Wobbler Ø 100 mm, só nos 25 SKUs acima de R$ 500 mil
- Manifesto na parede do prédio acima da parede de entrada (teto a 3.400)

O verde: o manual diz #1EA7AC; a instrução do marketing foi #08a9b1. O ajuste
"verde" do canvas troca em tudo de uma vez. Decidir antes da arte-final.
