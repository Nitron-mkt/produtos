# Showroom Nitron — levantamento de medidas

Transcrição do croqui manual de campo (foto recebida em 04/09/2026), para o projeto
**Nitron-mob PDV**. Cotas em metros.

## Cotas do croqui

| Cota | Valor | Onde | Origem |
|---|---|---|---|
| Frente | 7,53 m | largura na face de acesso | medida (croqui) |
| Fundo | 7,50 m | largura na parede oposta | medida (croqui) |
| Lateral, trecho 1 | 6,50 m | da frente até o pilar | medida (croqui) |
| Lateral, trecho 2 | 6,60 m | do pilar até o fundo | medida (croqui) |
| Pilar — avanço | 0,67 m | quanto entra no salão | anotado "6,70 cm", lido como 67 cm — **confirmar** |
| Pilar — face | 0,245 m | quanto ocupa da parede | anotado "24,5" — **confirmar** |
| Pé-direito | 3,40 m | piso ao teto | "3,40 altura"; a conta 2,07 + 1,32 = 3,39 ao lado parece a mesma medida em duas etapas de trena — **confirmar** |
| Comprimento total | 13,35 m | frente ao fundo | **derivado** (6,50 + 0,245 + 6,60), não medido |
| Porta | ≈ 2,00 m | lateral norte, de 0 a 2,00 m (encostada na esquina da frente) | marcada sobre a planta; proporção do traço deu 2,11 m, informado "quase 2 metros" — **confirmar** |
| Caixa | ≈ 3,40 m | lateral norte, de 2,40 a 5,80 m da frente | marcada sobre a planta; profundidade não informada — **confirmar** |

## Derivados

- Área bruta de piso: 7,515 × 13,345 = **100,3 m²**
- Área do pilar: 0,67 × 0,245 = 0,16 m² → **área útil ≈ 100,1 m²**
- Perímetro fechado (3 paredes): 13,345 + 7,50 + 13,345 = **34,19 m**
- Perímetro total com a frente: **41,72 m**
- **Parede livre para módulo: 27,45 m** = lateral sul 13,35 + fundo 7,50 + norte livre 6,60
  (93,3 m² de face a 3,40 m). A frente, se for parede cheia, soma +7,53 m
- Ocupação da lateral norte: porta 0→2,00 · folga 0,40 · caixa 2,40→5,80 ·
  folga 0,70 · pilar 6,50→6,745 · **pano livre 6,745→13,35 (6,60 m)**
- Volume: **341 m³**
- Largura livre no miolo com prateleira de 0,60 m nas duas laterais: **6,32 m**

## Nomenclatura convencionada

Não é orientação magnética — é só para não trocar as paredes na modulação.

- **Frente** — face de 7,53 m; **vedação a definir** (a porta está na lateral norte, não aqui)
- **Fundo** — face de 7,50 m, oposta
- **Lateral norte** — 13,35 m, tem a porta, o caixa e o pilar
- **Lateral sul** — 13,35 m, pano corrido; **é a parede de impacto**: a primeira que
  se vê ao entrar pela porta da lateral norte

## Malha modular — o que a geometria aceita

Contado sobre a parede **livre**, não a bruta.

| Passo | Lateral sul 13,35 | Fundo 7,50 | Norte livre 6,60 | Total |
|---|---|---|---|---|
| 1,00 m | 13 + 0,35 | 7 + 0,50 | 6 + 0,60 | 26 módulos |
| **1,25 m** | 10 + 0,85 | **6 exatos** | 5 + 0,35 | 21 módulos |
| 1,50 m | 8 + 1,35 | **5 exatos** | 4 + 0,60 | 17 módulos |
| 1,10 m | 12 + 0,15 | 6 + 0,90 | **6 exatos** | 24 módulos |

O passo definitivo depende da largura do módulo Nitron-mob, ainda não definida.

## Pendências antes de modular

1. Comprimento total na trena (única cota estrutural derivada).
2. A frente de 7,53 m é parede cheia, vitrine ou vão? Se for parede, o estoque de
   módulo sobe de 27,45 para 34,98 m — o maior ganho disponível.
3. O caixa é móvel ou está preso por elétrica/hidráulica/alvenaria?
4. Sentido de abertura da porta e folha única ou dupla (vão de 2,00 m abrindo para
   dentro varre ~1 m do salão).
5. Teto (laje/forro/aparente), rebaixos, vigas, pontos de força e quadro elétrico.
6. Dimensões e fixação do módulo Nitron-mob.

## Saída

`01-planta-base.html` — planta cotada em escala, desdobramento de paredes e opções de malha.
