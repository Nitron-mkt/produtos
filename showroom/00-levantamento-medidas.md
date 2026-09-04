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

## Derivados

- Área bruta de piso: 7,515 × 13,345 = **100,3 m²**
- Área do pilar: 0,67 × 0,245 = 0,16 m² → **área útil ≈ 100,1 m²**
- Perímetro fechado (3 paredes): 13,345 + 7,50 + 13,345 = **34,19 m**
  (confere com a soma do croqui, 20,7 + 13,2 = 33,9, dentro de 0,3 m)
- Perímetro total com a frente: **41,72 m**
- Face de parede a 3,40 m: fechada **116,2 m²** · total 141,8 m²
- Volume: **341 m³**
- Largura livre no miolo com prateleira de 0,60 m nas duas laterais: **6,32 m**

## Nomenclatura convencionada

Não é orientação magnética — é só para não trocar as paredes na modulação.

- **Frente** — face de 7,53 m, presumida aberta (acesso/vitrine)
- **Fundo** — face de 7,50 m, oposta
- **Lateral norte** — 13,35 m, é a que tem o pilar a 6,50 m da frente
- **Lateral sul** — 13,35 m, pano corrido sem acidente registrado

## Malha modular — o que a geometria aceita

| Passo | Fundo 7,50 | Lateral 13,35 | Trecho até o pilar 6,50 | Total 3 faces |
|---|---|---|---|---|
| 1,00 m | 7 + 0,50 | 13 + 0,35 | 6 + 0,50 | 33 módulos |
| **1,25 m** | **6 exatos** | 10 + 0,85 | 5 + 0,25 | 26 módulos |
| 1,50 m | **5 exatos** | 8 + 1,35 | 4 + 0,50 | 22 módulos |

O passo definitivo depende da largura do módulo Nitron-mob, ainda não definida.

## Pendências antes de modular

1. Comprimento total na trena (única cota estrutural derivada).
2. O volume de 0,67 × 0,245 m é pilar que avança, prumada ou nicho embutido?
3. Posição de porta, janela e vitrine — a frente aberta é presunção.
4. Teto (laje/forro/aparente), rebaixos, vigas, pontos de força e quadro elétrico.
5. O que já existe hoje no showroom: balcão, depósito, atendimento, banheiro.
6. Dimensões e fixação do módulo Nitron-mob.

## Saída

`01-planta-base.html` — planta cotada em escala, desdobramento de paredes e opções de malha.
