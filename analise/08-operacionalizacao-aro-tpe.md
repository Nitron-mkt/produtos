# Operacionalização do aro de vedação em TPE — Linha Pote com Travas

**Decisão:** aprovado pela diretoria em 06/09/2026, sobre veto técnico registrado do
`curador-portfolio` (parecer em `06-gaxeta-tpe-potes-hermeticos.md` §revisão 4).
**Produto:** especificado em `07-especificacao-lacre-tpe.md`.
**Este documento:** como fazer acontecer — ferramental, montagem, gente, ERP, cronograma, dinheiro.

---

## 1. O que estamos operacionalizando

Um **aro de vedação em TPE**, de seção constante, comprado em bobina de um extrusor de perfil,
cortado no comprimento, fechado em anel e alojado num canal usinado na face de vedação das tampas
que já existem.

**Uma seção. Quatro comprimentos de corte. Nenhum molde de tampa novo.**

| Tampa | PI | Produtos servidos | Peças/ano | Perímetro | Corte |
|---|---|---|---:|---:|---:|
| RET-C 22×14 | **816** | Raso 1,1 L (233) + Alto 2,2 L (156) | 155.949 | 67,7 cm | 69,1 cm |
| RET-D 26×18 | **799** | Raso 2,3 L (234) + Alto 4,3 L (151) | 80.346 | 82,7 cm | 84,4 cm |
| QUA-3770 20×19 | **575** | Quadrado 1,8 L | 68.257 | 73,3 cm | 74,8 cm |
| UF-215 25×16,5 | **924** | Ultraforte 2,1 L | 42.020 | 78,0 cm | 79,6 cm |
| | | **total** | **346.572** | | |

Confirmado pelo BOM (`TPRLPI`, `DISTINCT` por par PA/PI — a tabela é registro por ordem, não
estrutura mestre): o **PI 816 é o mesmo** nas duas referências que ele serve. Um canal usinado
nele atende Raso 1,1 L e Alto 2,2 L de uma vez.

---

## 2. A notícia boa que o BOM deu: a operação de montagem já existe

O maior risco operacional que este projeto parecia ter era criar um posto de montagem novo para
componente avulso. **Não cria.**

O `215.012.003` (Ultraforte 2,1 L) já é montado com **três** componentes:

| PI | Descrição | Peso | Cav. | Custo |
|---|---|---:|---:|---:|
| 923 | CORPO DO POTE ULTRAFORTE 2 LTS COM TRAVAS | 146 g | 1 | R$ 0,521 |
| 924 | TAMPA DO POTE ULTRAFORTE 2 LTS COM TRAVAS | 55 g | 1 | R$ 0,232 |
| **928** | **TRAVAS POTE ULTRA FORTE** | **16 g** | **4** | **R$ 0,077** |

**A fábrica já monta uma peça pequena avulsa nesta mesma família, em 42.020 unidades por ano.**
O posto existe, a operação existe, e o pessoal sabe fazer. O aro é o quarto componente numa linha
que já monta três — e o terceiro nas outras.

Isso muda o risco de "criar capacidade nova" para "estender capacidade existente", que é uma
conversa completamente diferente com a Produção.

---

## 3. Rota escolhida e as que foram descartadas

| Rota | Investimento em molde | Custo/peça | Veredito |
|---|---|---|---|
| **Fita extrudada em bobina, cortada e fechada** | **1 ferramenta de perfil** | R$ 0,15–0,25 | ✅ **escolhida** |
| Aro injetado em TPE, molde por tamanho | 4 moldes de 4–8 cav | R$ 0,08–0,12 | ❌ é o que o projeto existe para evitar |
| Molde de família com postiços trocáveis | 1 molde + 4 postiços | R$ 0,10–0,15 | ❌ ~R$ 80–140 k, não paga para 4 tamanhos |
| Sobreinjeção 2K na tampa | 4 moldes bimaterial novos | R$ 0,05 | ❌ R$ 400 k+, e contamina o refugo na fonte |
| Linha própria de extrusão | R$ 350–700 k | — | ❌ rodaria 7% de um turno |

A fita ganha porque **desacopla o número de tamanhos do número de ferramentas.** É a única rota em
que acrescentar a 5ª, 10ª ou 18ª tampa custa só um comprimento de corte diferente.

**Nunca migrar para 2K sem refazer a análise de refugo.** Na fita, o refugo de injeção da tampa
continua mono-PP porque o TPE entra na montagem. Em 2K, ele nasce contaminado — e aí o ciclo de
moído entra na conta.

---

## 4. Ferramental: o canal nas tampas

### O que precisa ser feito em cada molde

| PI | Máquina hoje | Cav. | O que fazer |
|---|---|---|---|
| 816 | 200 tf (inj. 1, 2, 3, 5, 19) | **2** | canal nas duas cavidades — atenção ao balanceamento |
| 799 | 160–200 tf (inj. 1, 6, 7–10, 42, 43) | 1 | canal |
| 575 | 150–160 tf (inj. 6, 7, 9, 11, 12, 36, 42, 43) | 1 | canal |
| 924 | 160 tf | 1 | canal — **sem apontamento desde 2020, confirmar com o PCP antes** |

⚠️ **O canal não se usina, solda-se.** Um rebaixo na peça é uma saliência no aço. Duas rotas:

- **Solda TIG/laser + reusinagem + repolimento** — mais barata, irreversível, com risco de trinca
  na zona termicamente afetada em aço temperado.
- **Postiço trocável na face de vedação** — mais cara, **reversível**, e permite voltar à tampa sem
  canal se o piloto reprovar.

**Recomendação: postiço no PI 816 (o piloto), solda nos demais** depois que o piloto aprovar. Pagar
a reversibilidade só onde ela ainda tem valor de opção.

### Os dois riscos de ferramentaria

1. **Rechupe na face visível.** O canal cria transição de espessura, e transição marca a face
   oposta — o topo da tampa. **66% do faturamento dessas famílias é transparente.** Prever aço de
   alta condutividade (BeCu/Moldmax) no postiço como contingência de tryout, e incluir inspeção
   visual sob luz rasante no critério de aprovação do piloto.
2. **A Tampa C não tem folga de tonelagem.** `AD_TONELAGEMMIN/MAX` do PI 816 = 200/200, e ela roda
   em máquinas de exatamente 200 tf. O canal **não aumenta a área projetada**, então a tonelagem
   não muda — mas não há para onde correr se algo mudar. Confirmar no tryout, não depois.

**Pergunta a fazer à ferramentaria antes de aprovar orçamento** (a ferramentaria é o gargalo real
da casa, por registro do próprio projeto): *quantas semanas de bancada por molde, e o que sai da
fila para isto entrar?*

---

## 5. O processo de montagem

### Fluxo do posto

```
  bobina de fita          tampa injetada (do estoque de PI)
        │                             │
        ▼                             ▼
  ┌───────────┐                 ┌───────────┐
  │ 1. medir  │                 │ 4. fixar  │
  │  e cortar │                 │  na jiga  │
  └─────┬─────┘                 └─────┬─────┘
        │  aro cortado                │
        └──────────────┬──────────────┘
                       ▼
              ┌──────────────────┐
              │ 5. assentar o    │  pressiona o pé no canal,
              │    aro no canal  │  contornando o perímetro
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │ 6. fechar junta  │  solda térmica em cunha,
              │    em cunha 30°  │  no meio de um lado reto
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │ 7. inspeção 100% │  aro assentado? junta fechada?
              │    visual        │  sobra ou falta no perímetro?
              └────────┬─────────┘
                       ▼
                tampa com aro → montagem do PA
```

### Tempo padrão e as três configurações possíveis

| Configuração | s/peça | Horas/ano | **Operadores FTE** | R$/peça (MO) |
|---|---:|---:|---:|---:|
| Manual, sem jiga (pior caso) | 40 | 3.851 | **2,19** | R$ 0,222 |
| **Manual com jiga de corte e solda** | **25** | **2.407** | **1,37** | **R$ 0,139** |
| Semiautomática (aplicador + solda em ciclo) | 10 | 963 | **0,55** | R$ 0,056 |

Base: 1.760 h/ano por operador, R$ 20/h carregado, 346.572 peças.

**A jiga semiautomática economiza R$ 28.881/ano** contra a manual com jiga — ela se paga em cerca
de um ano e é a diferença entre 1,4 e 0,6 pessoa. **Cotar as duas juntas desde o início**, e
decidir com o tempo real medido no piloto, não com esta estimativa.

⚠️ **Este é o maior componente de incerteza do custo.** O tempo de 25 s é estimativa de engenharia,
não medição. A primeira coisa a fazer no piloto é cronometrar 50 peças.

### A junta é o ponto crítico do posto

É onde vaza, e é a operação que mais depende de habilidade. Três regras não negociáveis:

1. **Corte em cunha a 30°**, nunca topo a topo.
2. **Solda térmica com temperatura e tempo controlados por jiga.** Cianoacrilato serve para
   protótipo e **não sobrevive a lava-louças** — não vai para produção.
3. **Junta sempre no meio de um lado reto, nunca no canto**, e **marcada na jiga**, para que a
   inspeção saiba onde olhar em toda peça.

---

## 6. Cadastro no ERP

O cadastro precisa existir antes do piloto, senão não há como apontar produção nem custear.

### Itens a criar

| # | Item | Grupo | Unid. | Observação |
|---|---|---|---|---|
| 1 | `FITA TPE VEDACAO 1,2x3,4mm SHORE 45 - NATURAL` | 3000500 Outros MP | **KG** | matéria-prima em bobina |
| 2 | `FITA TPE VEDACAO 1,2x3,4mm SHORE 45 - PRETO` | 3000500 Outros MP | KG | só se houver SKU preto no escopo |
| 3 | `ARO VEDACAO TPE - TAMPA 22x14 (816)` | 2000000 PI | PC | consome fita, sai do posto |
| 4 | `ARO VEDACAO TPE - TAMPA 26x18 (799)` | 2000000 PI | PC | |
| 5 | `ARO VEDACAO TPE - TAMPA QUADRADA 20x19 (575)` | 2000000 PI | PC | |
| 6 | `ARO VEDACAO TPE - TAMPA ULTRAFORTE (924)` | 2000000 PI | PC | |

**Não reaproveitar o CODPROD 997.** Ele é `TPE DUREZA 45 - KARINPRENE`, resina granulada em KG,
com um único movimento em seis anos (100 kg em remessa para beneficiamento à Tanamu, 12/11/2020),
`CUSGER = 0` e `DTATUAL` de 01/01/1900. A fita é outro item, de outro fornecedor, com outra
especificação. Manter o 997 como está.

**Criar o PI de aro por tamanho, em vez de consumir fita direto no PA.** Custa quatro cadastros e
compra três coisas: custo por tamanho, rastreabilidade de lote de fita até o pote, e apontamento
da operação de montagem. Sem ele, o custo do aro se dilui e ninguém sabe quanto custou de verdade.

### Estrutura

Incluir cada aro no `TPRLPI` do PA correspondente, com `TIPOPI = 'E'` e `CONTROLEPI` = cor,
seguindo exatamente o padrão do `PI 928` no `215.012.003`. **O PI 928 é o modelo a copiar** — é um
componente pequeno avulso já estruturado e funcionando.

Fator de consumo: metros de fita por aro, conforme a coluna "Corte" da §1, mais a perda de setup.

### Campos de engenharia — preencher, ao contrário do que é hábito

`AD_TONELAGEMMIN/MAX` e `AD_QTDCAVIDADE` estão preenchidos em 60% e 78% do grupo PI, e em
praticamente zero do grupo PA. **O aro é PI: preencher.** É o que permite que a próxima análise de
capacidade encontre o dado onde ele deve estar.

---

## 7. Suprimento

| Item | Definição |
|---|---|
| Consumo | **637 kg/ano** · 254.832 m/ano · **0,64 t** |
| Embalagem | bobina de **1.000 a 2.000 m** (a 500 m seriam 510 bobinas/ano — movimentação demais) |
| Frequência | 2 a 4 entregas/ano |
| Fornecedor | extrusor de perfil de vedação (esquadria/automotivo) — mercado maduro no Brasil |
| **Segunda fonte** | **homologada antes da produção, não depois** — fonte única foi o que reprovou o Tritan |
| Ferramenta de perfil | **ativo da Nitron**, ainda que fisicamente no fornecedor |

⚠️ **0,64 t/ano é volume pequeno para o setor.** A Nitron não será cliente estratégico de ninguém.
Consequências a negociar no contrato, não a descobrir depois: lote mínimo, prazo de reposição, e o
compromisso de que a ferramenta é nossa.

⚠️ **Não há âncora interna de custo.** Os R$ 45–70/kg são estimativa de mercado. O primeiro
orçamento real substitui todo o custeio deste documento.

### Recebimento

| Ensaio | Frequência | Critério |
|---|---|---|
| Dureza shore A | por lote | 45–55, 3 pontos por bobina |
| Cotas do perfil (projetor) | por lote | conforme `07-especificacao-lacre-tpe.md` §2 |
| Massa linear | por lote | 2,5 g/m ±10% |
| **Retração 24 h a 60 °C** | **por lote** | **≤ 1,0%** — 3% em 88 cm são 2,6 cm e a junta abre |
| Carta de conformidade ANVISA para contato com alimento | **antes da 1ª amostra** | grau específico, não família |

---

## 8. Qualidade do produto

**Inspeção 100% visual no posto** (§5, passo 7): aro assentado no canal em todo o perímetro, junta
fechada, sem sobra nem falta.

**Ensaio por lote de produção**, usando `ensaios/protocolo-ensaio-estanqueidade.xlsx`:

| Ensaio | Frequência | Critério |
|---|---|---|
| E1 — vazamento 24 h invertido | 5 conjuntos por lote | zero mancha, perda < 0,10 g |
| E3 — 200 ciclos de abre-fecha | 3 por lote inicial, depois trimestral | mantém E1, **aro não sai do canal** |
| E4 — 20 ciclos de lava-louças | trimestral | aro no lugar, retração ≤1%, mantém E1 |
| E5 — 30 dias sob trava a 40 °C | na homologação e a cada troca de fornecedor | mantém E1, força de abrir estável |

**O E3 é o que reprova o conceito de aro solto.** Uma única saída do canal em 200 ciclos condena a
retenção mecânica — pela lição nº 7 do projeto, peça removível não carrega função.

### Sobre o que escrever na embalagem

A fábrica confirmou que **hoje nenhum pote da categoria é vendido como hermético** e não há claim
impresso. Quando houver aro e ensaio, a recomendação continua sendo **"não vaza" / "à prova de
vazamentos"**, não "hermético":

- É exatamente o que o E1 comprova, e o ensaio arquivado é o lastro que o art. 36 do CDC pede.
- "Hermético" é dito por **61,4% dos anúncios de pote** do mercado — não diferencia nada.
- A **Sanremo**, em plástico com válvula, escreve "válvula micro ondas" e evita o claim.

Se o E2 (vapor, 7 dias) também aprovar, "hermético" fica tecnicamente de pé — mas continua sendo
escolha de risco, porque não há norma que defina o termo. **Levar ao jurídico antes da arte.**

---

## 9. O refugo — a disciplina que não pode falhar

| | |
|---|---|
| Refugo de **injeção** da tampa | **continua mono-PP** — a fita entra na montagem, a injetora nunca vê TPE ✅ |
| Refugo **pós-montagem** (tampa já com aro) | carrega TPE a **1,8–4,5% da massa da tampa** |
| SEBS em PP | **mecanicamente tolerável** — é blenda base PP, diferente de Tritan e PET |
| **SEBS em PP clarificado** | ❌ **névoa e géis visíveis.** O óleo interfere na nucleação do clarificante |

**Regra de chão de fábrica, e ela é binária: tampa com aro que for refugada vai para a corrente
PRETA. Nunca para a transparente, nunca para a branca.**

Os moídos já são segregados por cor no cadastro (branco, preto, marrom, transparente, azul, alto
impacto), então a infraestrutura existe. O que não existe é o hábito — **a Nitron não tem hoje
nenhum material não-PP circulando**, então esta é a primeira vez que uma segregação errada tem
consequência. Tratar como item de treinamento do posto, com cartaz no local, não como nota de
procedimento.

Contexto para dimensionar a preocupação: o moído é **476 t/ano compradas** contra ~24 t geradas
internamente, e as tampas em questão pesam ~24 t/ano. Contaminar não destrói o ativo de
R$ 2,63 M — mas a fábrica **vende 180 t/ano de moído**, e essa saída um refugo contaminado
desvaloriza.

---

## 10. Cronograma

| Fase | Semanas | O que acontece | Porta de decisão |
|---|---|---|---|
| **0 — Bancada** | 1–2 | Curso livre da trava · **força de abrir com perfil de 0/1,0/1,5/2,0 mm** · contagem de travas por tampa | 🚦 **PORTA 1** |
| **1 — Especificação** | 3–4 | Fecha a altura do lábio com o número medido · desenho final do perfil | |
| **2 — Fornecedor** | 4–8 | Cotação com 3 extrusores · amostras de 50 m em shore 45 e 55 · carta ANVISA · 2ª fonte | |
| **3 — Validação da fita** | 8–10 | Repete a bancada com a fita real · define método de junta | |
| **4 — Ferramental piloto** | 10–16 | **Postiço no PI 816** · tryout · inspeção de rechupe | |
| **5 — Piloto** | 16–20 | 5.000 peças · **cronometrar 50** · ensaios E1/E3/E4 · cadastro no ERP | 🚦 **PORTA 2** |
| **6 — Escalonamento** | 20–32 | PI 799, 575, 924 · jiga definitiva · treinamento do posto | |

**Nada da fase 2 em diante começa antes da Porta 1.** A fase 0 custa R$ 200 e uma semana, e é ela
que define a única cota que ainda está aberta no desenho do perfil.

---

## 11. Investimento e custo

### Investimento

| Item | Faixa |
|---|---|
| Bancada (fase 0) | R$ 200 |
| Ferramenta de perfil (matriz + calibrador) | R$ 8.000 – 20.000 |
| Postiço no PI 816 (reversível, piloto) | R$ 8.000 – 18.000 |
| Canal nos PI 799, 575, 924 (solda + usinagem + tryout) | R$ 18.000 – 45.000 |
| Jiga de corte, aplicação e solda | R$ 15.000 – 40.000 |
| Ensaios, homologação, amostragem, carta ANVISA | R$ 5.000 – 12.000 |
| **Total** | **R$ 54.000 – 135.000** |

### Custo por peça

| Tampa | Material | MO (25 s) | **Total** | MO (10 s) | **Total c/ jiga** |
|---|---:|---:|---:|---:|---:|
| RET-C | R$ 0,093 | R$ 0,139 | **R$ 0,232** | R$ 0,056 | **R$ 0,149** |
| RET-D | R$ 0,114 | R$ 0,139 | **R$ 0,253** | R$ 0,056 | **R$ 0,169** |
| QUA-3770 | R$ 0,101 | R$ 0,139 | **R$ 0,240** | R$ 0,056 | **R$ 0,156** |
| UF-215 | R$ 0,107 | R$ 0,139 | **R$ 0,246** | R$ 0,056 | **R$ 0,163** |
| **Custo anual** | | | **R$ 83.174** | | **R$ 54.293** |

### O que precisa ser verdade para pagar

Sem aumento de preço, o aro consome **R$ 83 k/ano** (ou R$ 54 k com a jiga) e derruba a MB da
RET-C de 47,7% para ~43,7%.

| Cenário | O que precisa |
|---|---|
| Manual, 25 s | **+4,7% de preço** para margem neutra |
| Com jiga, 10 s | **+3,0% de preço** para margem neutra |

**O radar de concorrência não encontrou evidência de prêmio de preço** (delta −3,5%, −0,8% e −17%
em três cortes). Isso continua registrado como o risco central do projeto, e não foi resolvido —
foi decidido por cima.

**A forma mais barata de resolvê-lo é um teste de preço real**, que **não atrasa nada** e pode
rodar em paralelo à fase 2: mesma SKU, dois preços, mesmo canal, 8 semanas, na base de 1.121
clientes do `233.012.001`. Custa uma tabela de preço e a paciência de esperar oito semanas, e
substitui toda a especulação acima por um número da própria casa.

---

## 12. Riscos e o que fazer com cada um

| # | Risco | Grau | Mitigação |
|---|---|---|---|
| 1 | **A força de abrir sobe e o produto fica ruim de usar** | 🔴 | **Porta 1.** É o modo de falha do concorrente que veda bem (32,3% das negativas). Se subir >1,5×, reduzir lábio ou parar |
| 2 | **O mercado não paga o prêmio** | 🔴 | Teste de preço real em paralelo (§11). Não resolvido, decidido por cima |
| 3 | A tampa arqueia entre travas e não veda | 🟡 | Piloto no PI 816, a menor das quatro. Contar travas na fase 0 |
| 4 | Rechupe na face visível (66% transparente) | 🟡 | Aço de alta condutividade no postiço; inspeção sob luz rasante no tryout |
| 5 | A junta vaza | 🟡 | Cunha 30° + solda em jiga + posição marcada + inspeção 100% |
| 6 | Tempo de montagem maior que 25 s | 🟡 | Cronometrar 50 peças no piloto. Jiga semiauto cotada desde já |
| 7 | Refugo com TPE contamina moído transparente | 🟡 | Regra binária: refugo com aro → corrente preta. Cartaz no posto |
| 8 | Ferramentaria não tem fila | 🟡 | Perguntar antes de aprovar orçamento: quantas semanas, e o que sai |
| 9 | Fonte única de fita | 🟢 | 2ª fonte homologada antes da produção; ferramenta é ativo Nitron |
| 10 | PI 924 sem apontamento desde 2020 | 🟢 | Confirmar com o PCP antes de mexer nesse molde |

---

## 13. As duas portas

**🚦 PORTA 1 — semana 2, custo R$ 200.** Mede a força de abrir com perfil de 0, 1,0, 1,5 e 2,0 mm.
- Sobe pouco (<1,3×) → segue com a altura de lábio medida.
- Sobe muito (>1,5×) → **para, ou muda a rota** para alteração da trava. Nenhum dinheiro gasto.
- Bônus: o resultado explica, de um jeito ou de outro, por que as refs `176.024.001` e
  `210.024.001` (trava + válvula) são as únicas duas quedas numa plataforma que cresce 49,9%.

**🚦 PORTA 2 — semana 20, após o piloto de 5.000 peças no PI 816.**
- Aprova em E1/E3/E4, sem rechupe, tempo ≤30 s → escalona para as outras três tampas.
- Reprova → o postiço é reversível e a tampa volta ao que era. Perda limitada ao piloto.

Fora dessas duas portas, executar sem reabrir a discussão.

---

## 14. Próximo passo, esta semana

1. **Comprar 3 m de perfil de vedação de esquadria de 1,5 mm e fita dupla-face** — loja de material
   de construção, ~R$ 200.
2. **Separar 5 tampas de produção** de cada uma das quatro famílias.
3. **Rodar a aba `Travas`** de `ensaios/protocolo-ensaio-estanqueidade.xlsx`.
4. **Perguntar à ferramentaria** quantas semanas de bancada por molde, e o que sai da fila.
5. **Perguntar ao PCP** onde o PI 924 (tampa Ultraforte) é produzido hoje.

Nada além disso antes da Porta 1.
