# Mercado endereçável em Rondônia por CNAE — e a correção da análise anterior

**Data:** 02/09/2026
**Fonte interna:** Sankhya produção — compradores de 12 M (set/25–ago/26), marca própria, recorte oficial
(empresas 1/2/14, `STATUSNOTA='L'`, `TIPMOV IN ('V','D')`, `ATUALFIN<>0`, intercompany fora, `CODTAB` 84 e 3 excluídas).
**Fonte externa:** IBGE / **CEMPRE 2024**, SIDRA tabela **9528** (unidades locais por classe da CNAE 2.0, nível UF)
e tabela **9529** (faixas de pessoal ocupado, nível grupo). Variável 706.

---

## 1. Resposta curta

Cruzando o CNAE dos nossos compradores com o cadastro de estabelecimentos do IBGE,
**Rondônia não está sub-atendida — está atendida acima da média.**

- Existem **10.014 estabelecimentos em RO** nas 12 classes de CNAE onde a Nitron
  concentra 82% dos clientes. Desses, só **~2.298 têm 5 ou mais pessoas ocupadas**.
- A Nitron tem **23 clientes PJ** nessas classes = **0,230% de penetração**, contra
  **0,144%** em estados de distância comparável. **Rondônia está 1,6× acima do benchmark.**
- Nas duas classes que são o núcleo da casa, RO está **2,9× e 2,3×** acima do benchmark.
  Em minimercados, **18,1× acima**. O espaço que resta está em classes adjacentes onde
  não vendemos lá — e soma **+6 clientes**.
- **O gap endereçável de RO é negativo: −8,8 clientes.**

**Isso corrige a análise de 02/09** (`06-filial-cd-rondonia.md`), que estimava
**+416 clientes** de gap na região. Aquele número era artefato de contar pessoa física.
Ver §6.

**O estado sub-atendido da região é o Amazonas**, não Rondônia: 0,029% de penetração,
**0,20× o benchmark**, gap de **+20 clientes**. E Manaus não é servível por rodovia
a partir de Ouro Preto do Oeste.

---

## 2. A descoberta que reorganiza tudo: pessoa física não é canal

`TGFPAR.CNAE` está preenchido em apenas 9,8% do cadastro, o que parecia inviabilizar a
análise. **Não é falha de cadastro.** Entre PJ a cobertura de CNAE é **~99%** em todas as
UFs; entre PF é **zero**, porque PF não tem CNAE. A maioria dos "clientes" é pessoa física:

| Brasil, 12 M | Clientes | Faturamento | R$/cliente/ano | Ticket por nota |
|---|---|---|---|---|
| **PJ** | **3.376** | **R$ 81.976.543** | **R$ 24.282** | R$ 5.255 (R$ 10.670 na região alvo) |
| PF | 13.973 | R$ 293.235 | **R$ 21** | **R$ 20** |

**13.973 registros de PF somam R$ 293 k — 0,36% do faturamento, a R$ 21 por ano cada,
em notas de R$ 20.** É venda de balcão, amostra e funcionário. Não é revenda, não é
canal, e não existe no CEMPRE.

> **A base de clientes real da Nitron é 3.376 PJ, não 17.349.**
> Toda métrica de "número de clientes" deste projeto precisa ser lida por PJ.

E a proporção de PF **varia enormemente por UF** — 24% em Rondônia contra 85% na Bahia.
É por isso que qualquer comparação de contagem de clientes entre estados sem separar
PF de PJ produz o resultado errado.

---

## 3. Onde a Nitron realmente vende — as 12 classes de CNAE

| Classe | Clientes PJ | % acum. do total PJ | R$/cliente/ano | Descrição |
|---|---|---|---|---|
| **47598** | **643** | 19,0% | 18.422 | Varejo de artigos de uso doméstico n.e. |
| **47130** | **539** | 35,0% | 13.940 | Varejo de mercadorias em geral s/ predom. alimentos |
| 47555 | 397 | 46,8% | 20.528 | Tecidos, cama, mesa e banho |
| 47121 | 265 | 54,6% | 11.525 | Minimercados, mercearias, armazéns |
| 47113 | 247 | 61,9% | 18.230 | Hiper e supermercados |
| 47890 | 165 | 66,8% | 16.545 | Outros produtos novos n.e. |
| 47814 | 123 | 70,5% | 22.488 | Vestuário e acessórios |
| 47440 | 99 | 73,4% | 61.134 | Ferragens, madeira e material de construção |
| 47610 | 99 | 76,3% | 40.679 | Livros, jornais, revistas e papelaria |
| 47636 | 99 | 79,3% | 21.693 | Artigos recreativos e esportivos |
| 46494 | 91 | 82,0% | **168.536** | Atacado de artigos de uso pessoal e doméstico n.e. |
| 47725 | 69 | 84,0% | 25.327 | Cosméticos, perfumaria e higiene pessoal |

**2.836 clientes = 82,3% de todos os 3.376 PJ** (89,9% dos que têm CNAE). Essas 12 classes
são o **conjunto núcleo** usado como definição de mercado endereçável.
Divisões 46 e 47 respondem por 96,6% do faturamento — a Nitron vende para comércio, ponto.

---

## 4. Quantos estabelecimentos desses CNAEs existem em Rondônia

| | Estabelecimentos |
|---|---|
| Total de unidades locais em RO, todos os CNAEs | **75.246** |
| **Nas 12 classes núcleo** | **10.014** |
| ↳ com 0 a 4 pessoas ocupadas (micro/MEI) | 77% |
| ↳ **com 5 ou mais pessoas ocupadas** | **23% → ~2.298** |

Abertura das 12 classes em RO:

| Classe | Estab. RO | Clientes PJ | Penetração RO | Penetração benchmark | RO / bench | Gap |
|---|---|---|---|---|---|---|
| 47814 vestuário | 2.606 | 1 | 0,04% | 0,049% | 0,8× | +0,3 |
| 47440 ferragens/constr. | 2.046 | 0 | 0,00% | 0,025% | — | +0,5 |
| 47121 minimercados | 1.708 | 3 | 0,18% | 0,010% | **18,1×** | −2,8 |
| 47890 outros prod. novos | 1.189 | 0 | 0,00% | 0,083% | — | +1,0 |
| 47113 hiper/super | 498 | 1 | 0,20% | 0,039% | 5,2× | −0,8 |
| 47725 cosméticos | 387 | 0 | 0,00% | 0,010% | — | +0,0 |
| 47636 recreativos | 351 | 0 | 0,00% | 0,304% | — | +1,1 |
| 47555 cama/mesa/banho | 328 | 0 | 0,00% | 0,610% | — | +2,0 |
| 47610 papelaria | 303 | 0 | 0,00% | 0,220% | — | +0,7 |
| **47598 uso doméstico** | **240** | **12** | **5,00%** | 1,714% | **2,9×** | **−7,9** |
| 46494 atacado dom. | 190 | 0 | 0,00% | 0,282% | — | +0,5 |
| **47130 variedades** | **168** | **6** | **3,57%** | 1,563% | **2,3×** | **−3,4** |
| **TOTAL** | **10.014** | **23** | **0,230%** | **0,144%** | **1,6×** | **−8,8** |

*Benchmark = BA + CE + GO + PB + PE (estados distantes da fábrica, fora do Norte/CO):
323 clientes PJ núcleo em 224.048 estabelecimentos.*

**A leitura importante está na estrutura, não no total.** Nas duas classes que são o
núcleo do negócio — 47598 e 47130 — Rondônia já está colhida: **12 dos 240** varejistas de
artigos de uso doméstico do estado e **6 das 168** lojas de variedades já compram da Nitron.
Isso é 5,0% e 3,6% de penetração, contra 1,7% e 1,6% do benchmark.

Todo o espaço positivo (**+6,1 clientes**) está em classes onde temos **zero** cliente em RO:
cama/mesa/banho, recreativos, papelaria, atacado doméstico, ferragens. São classes onde a
Nitron converte em outros estados mas nunca trabalhou em Rondônia — **problema de cobertura
comercial, não de estoque local.**

---

## 5. A região inteira, e o teto contra o break-even do CD

| UF | Clientes PJ núcleo | Estab. núcleo | Penetração | vs benchmark | Gap |
|---|---|---|---|---|---|
| **MT** | 50 | 25.752 | 0,194% | **1,35×** | −13 |
| **RO** | 23 | 10.014 | 0,230% | **1,60×** | −9 |
| **AC** | 6 | 4.744 | 0,126% | 0,88× | −1 |
| **AM** | 6 | 20.458 | **0,029%** | **0,20×** | **+20** |
| **Região alvo** | **85** | **60.968** | **0,139%** | 0,97× | **+3** |
| Benchmark | 323 | 224.048 | 0,144% | 1,00× | — |

**A região alvo, somada, está na penetração do benchmark.** O gap endereçável é **+3 clientes**.
Todo ele está no Amazonas — e Manaus depende da BR-319, que não é rota confiável de caminhão
a partir de Ouro Preto do Oeste.

### O teto, e o que o CD exigiria

Região alvo: 60.968 estabelecimentos núcleo, R$ 16.056 por cliente PJ/ano.

| Se a região chegasse à penetração de… | Penetração | Clientes | Gap | Receita implícita | Paga o CD? |
|---|---|---|---|---|---|
| Benchmark (BA/CE/GO/PB/PE) | 0,144% | 88 | +3 | R$ 1,41 M | **não** |
| **São Paulo (mercado de casa)** | 0,367% | 224 | +139 | **R$ 3,60 M** | sim, no limite |
| Sergipe (melhor UF do país) | 0,511% | 311 | +226 | R$ 5,00 M | sim |

O break-even do CD (custo fixo de R$ 960 k/ano, MB 55,4%) é **R$ 3,42 M**.

> **O CD só fecha se RO+AC+MT+AM atingirem a penetração de São Paulo** — o mercado onde a
> fábrica está, onde há representante em rua desde sempre e onde o frete é de um dia.
> Esse é o tamanho da aposta que o CD embute.

E o teto acima é otimista: assume que os 139 clientes novos faturam como os 85 atuais
(R$ 16.056/ano). Cliente novo em praça nova fatura menos, não mais.

---

## 6. O que estava errado na análise anterior

`06-filial-cd-rondonia.md` §3 media penetração como **clientes ativos por 100 mil habitantes**
e concluiu **2,24 na região contra 6,12 no benchmark — 2,7× de sub-penetração, gap de +416
clientes**. Aquela contagem somava PF e PJ.

Refeita só com PJ:

| Bloco | PJ núcleo / 100 mil hab |
|---|---|
| Home (SP/RJ/MG/ES) | 2,03 |
| Benchmark (ex-home, ex-Norte/CO) | 0,82 |
| **Região alvo (RO/AC/MT/AM)** | **0,79** |
| **Rondônia** | **1,32** |

**A sub-penetração desaparece.** A região está em 0,79 contra 0,82 do benchmark, e Rondônia
sozinha está em 1,32 — acima. Os 2,7× de diferença eram a mistura de PF: 24% dos
compradores de RO são PF contra 85% na Bahia, e cada PF vale R$ 21 por ano.

### Números da análise anterior que ficam corrigidos

| Item | Antes (PF+PJ) | **Correto (PJ)** |
|---|---|---|
| Clientes ativos na região | 241 | **105** |
| Cadastrados ativos na região | 1.996 | **539** (399 em CNAE núcleo) |
| Cadastrados sem compra em 12 M | 1.755 | **434** |
| Dormentes 1–3 anos | 303 | **119** |
| LTV dos dormentes 1–3 anos | R$ 3.379.019 | **R$ 3.375.025** (era 99,9% PJ) |
| Dormentes 3+ anos | 266 | **147** |
| Nunca compraram | 1.186 | **168** |
| Teto por penetração | 657 ativos (+416) | **88 (+3)** no benchmark · 224 (+139) no teto de SP |

**O que não muda:** o faturamento (R$ 1,69 M), a margem (55,4%), o crescimento (+4,1%),
o ICMS (+4,77 pontos ao localizar), a geografia (Ouro Preto do Oeste é o melhor hub),
o precedente Extrema, e a recomendação de **não abrir o CD nesta rodada**.

**O que muda para pior:** o CD já não fechava com gap de +416; com gap de +3 no benchmark,
ele exige a penetração de São Paulo para empatar. A tese fica mais fraca, não mais forte.

**O que se confirma:** a Fase 1 — atacar os dormentes — sobrevive intacta, porque o
**LTV de R$ 3,38 M era 99,9% PJ**. São **119 empresas**, não 303 registros, e continua sendo
a jogada mais barata disponível.

---

## 7. O que fazer com isso

1. **Trocar a métrica do projeto.** Toda contagem de cliente passa a ser PJ. "17.349 clientes"
   virou 3.376. Isso muda taxa de acerto de lançamento, cobertura por linha e clientes por SKU
   em toda a base de conclusões.
2. **A Fase 1 continua sendo o certo, com alvo corrigido:** 119 PJ dormentes (R$ 3,38 M de LTV)
   + 168 PJ cadastrados que nunca compraram. Total endereçável imediato: **287 empresas** na
   região, sem depender de CD.
3. **O crescimento em RO não vem de mais lojas de utilidades — elas já são clientes.**
   Vem de (a) classes adjacentes onde temos zero cliente no estado — cama/mesa/banho,
   papelaria, recreativos, ferragens — e (b) **mais faturamento por cliente existente**,
   que é o caminho de sortimento, não de logística.
4. **Amazonas é a única frente de penetração real da região** (+20 clientes, 0,20× o benchmark,
   4,3 M de habitantes). E ele não se resolve por Ouro Preto do Oeste. Se a discussão é onde
   colocar esforço no Norte, o Amazonas merece um estudo próprio — provavelmente com
   distribuidor local em Manaus, não CD próprio.
5. **Preencher o CNAE dos PJ sem CNAE** é barato (consulta de CNPJ) e destrava esse tipo de
   análise por cidade, não só por UF. Hoje faltam ~2% dos PJ.

---

## 8. Limitações

- **CEMPRE conta estabelecimentos formais, não compradores potenciais.** Uma loja de material
  de construção existe no CNAE 47440 mas pode nunca comprar utilidade doméstica. A penetração
  comparada resolve parte disso (o benchmark tem o mesmo viés), mas o TAM absoluto de
  10.014 é teto formal, não demanda.
- **O ano do CEMPRE é 2024**; os dados da Nitron são de set/25 a ago/26. Defasagem de ~1 ano.
- **A faixa de porte vem do nível grupo** (tabela 9529), não classe — a proporção de 23% com
  5+ ocupados é aplicada proporcionalmente às classes, não medida em cada uma.
- **O benchmark de 5 UFs** (BA/CE/GO/PB/PE) tem 323 clientes PJ núcleo. Em classes pequenas o
  denominador fica fino: a penetração de 47725 no benchmark sai de **1 cliente**, então o
  "+0,0" daquela linha não tem significado estatístico.
- **A comparação assume que o benchmark é o alvo certo.** Se a Nitron está sub-penetrada em
  todo o Brasil fora de SP — e o dado sugere que está, 0,144% contra 0,367% de SP — então
  bater o benchmark é uma meta modesta. O teto de SP é o número ambicioso, e é o que a §5 usa.
- **Não medi CNAE por município.** A tabela 9528 tem nível municipal; dá para refazer isso por
  cidade de RO se a decisão precisar desse corte.
