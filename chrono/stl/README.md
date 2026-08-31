# Chrono · datador — arquivos STL

Gerados em 31/08/2026 a partir da malha real de `prova valvula-1`.
Unidade **milímetro**. **Sistema de coordenadas idêntico ao dos STL originais**
(eixo do poço em X 61,97 · Z 102,68 · Y é a vertical, mesmo datum da tampa),
então os quatro arquivos abrem já montados junto com `Tampa Pote 025 Pequeno_Cav-1`
e `Corpo Pote 025 Pequeno_Cav-1`.

| Arquivo | Conteúdo | Triângulos | Volume | Massa PP |
|---|---|---|---|---|
| `Chrono_01_Pino_Travinha.stl` | casca da válvula truncada em Y 37,23 + cubo + colar + 4 molas de detente + marcas de leitura | 56.242 | 2.390,6 mm³ | 2,16 g |
| `Chrono_02_Anel_Dia.stl` | anel Ø41,0/Ø28,6 × 0,95 · 31 números gravados 0,30 · 24 serrilhas · 31 encaixes | 45.562 | 604,3 mm³ | 0,55 g |
| `Chrono_03_Anel_Mes.stl` | anel Ø24,2/Ø12,0 × 0,95 · 12 números gravados 0,30 · 12 divisores · 12 encaixes | 20.548 | 306,0 mm³ | 0,28 g |
| `Chrono_04_Datador_Montado.stl` | os três na posição de montagem, para conferência | 122.352 | — | 2,99 g |

Datador **2,99 g** contra **2,04 g** da válvula que ele substitui: **+0,95 g por tampa**.

## Verificação feita

- As três peças são **watertight** (malha fechada, orientação consistente).
- **Interferência entre elas: 0,0000 mm³** nas três combinações.
- **Interferência com a tampa:** anel de dia 0,0000 · anel de mês 0,0000 ·
  pino **1,6357 mm³** — que é **exatamente** a interferência da válvula original
  contra a mesma tampa. Ou seja, o pino não acrescenta nenhuma interferência nova:
  o 1,64 mm³ é o aperto de encaixe que a válvula já tem hoje nos rasgos a 3 h e 9 h.

## Duas mudanças de projeto que a modelagem obrigou

1. **A aba de dedo da válvula, a 6 h, teve de sair.** Ela sobe até Y 38,24 e ocupa
   exatamente o espaço dos anéis (Y 37,25–38,20). O pino trunca a casca em Y 37,23.
   Toda a interface do assento fica abaixo disso, então o encaixe não muda — mas
   **o datador perde a aba de saque que a válvula tem hoje**. Se a peça precisar sair
   para lavar, esse recurso tem de ser definido; o lugar natural é o rasgo da orelha,
   a 3 h ou 9 h, contra o perfil do rebaixo cônico.
2. **A retenção é por canaleta, não por barbela sobre a face do anel.** Não há altura
   para uma cabeça de encaixe acima do anel sem passar do plano de rótulo. O cubo tem
   canaleta Ø10,6 (Y 37,58–37,82) e o colar tem canaleta Ø27,4 na face externa; cada
   anel leva uma saliência interna de 0,4 mm que estala dentro dela. Tudo cabe dentro
   dos 0,95 mm de espessura do anel e o topo fica raso em Y 38,20.

## Detentes

O par de molas tem de estar afastado de **um múltiplo do passo do anel**, senão
só uma delas encaixa. Com 31 posições (número ímpar), duas molas a 180° nunca
casam as duas. No arquivo estão a **15 passos** (174,19°) no anel de dia e a
**6 passos** (180°) no de mês.

- Molas no pino: calota de 0,15 de altura, base Ø0,60, em r 15,2 (dia) e r 7,0 (mês).
- Encaixes nos anéis: calota de 0,25 de profundidade, base Ø0,70, nos mesmos raios.
- Altura da mola e pré-carga axial são **cotas de tryout**, não de desenho.

## Ressalvas

Isto é **malha de conceito**, não modelo de ferramentaria. Não tem ângulo de saída,
raios de canto, contração, linha de fecho, ponto de injeção nem extração definidos.
Serve para conferir encaixe, proporção, legibilidade e montagem — e para imprimir
protótipo. Para orçamento, o desenho vem da ferramentaria a partir daqui.

Um teste que já vale a pena com estes arquivos: **imprimir e tentar ler os números**.
Gravado 0,30 mm em peça de uma cor só, o número quase não aparece de cima — é o
motivo de o contraste ter de vir do acabamento do molde (caractere polido em campo
texturizado), e não de tinta.

Gerado por `../medicao/gerar_stl.py` (trimesh + manifold3d).
