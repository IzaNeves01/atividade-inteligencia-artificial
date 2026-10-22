# Matriz de decisão

Cada regra compara respostas da entrevista e soma pontos a uma trilha. A trilha com mais pontos vence; em caso de empate vale a trilha ligada à atividade diária escolhida.

Abreviações: **Mat** = afinidade matemática, **Ativ** = atividade diária, **Ferr** = ferramenta, **Ent** = entrega de valor.

| Regra | Condição | Trilha | Pontos |
|---|---|---|---|
| R01 | Ativ = back-end | Back-end | +4 |
| R02 | Ent = regras de negócio | Back-end | +3 |
| R03 | Ativ = back-end e Ferr = Python, Java ou SQL | Back-end | +2 |
| R04 | Ativ = front-end | Front-end & UI/UX | +4 |
| R05 | Ent = produto e Ferr = JavaScript | Front-end & UI/UX | +3 |
| R06 | Ativ = front-end e Ent = produto | Front-end & UI/UX | +2 |
| R07 | Ativ = analisar dados | Ciência de Dados | +4 |
| R08 | Mat = Alta e Ent = análise/modelos | Ciência de Dados | +3 |
| R09 | Mat = Alta e Ferr = Python | Ciência de Dados | +2 |
| R10 | Mat = Baixa e Ativ = analisar dados | Ciência de Dados −2 / Eng. de Dados +2 | ±2 |
| R11 | Ativ = pipelines de dados | Engenharia de Dados | +4 |
| R12 | Ent = dados confiáveis | Engenharia de Dados | +3 |
| R13 | Ativ = pipelines e Ferr = Python ou SQL | Engenharia de Dados | +2 |
| R14 | Ativ = segurança | Cibersegurança | +4 |
| R15 | Ent = segurança | Cibersegurança | +3 |
| R16 | Ent = segurança e Ferr = Linux/Redes | Cibersegurança | +2 |
| R17 | Ativ = automação CI/CD | DevOps & SRE | +4 |
| R18 | Ativ = automação e Ferr = Linux/Redes | DevOps & SRE | +2 |
| R19 | Ativ = automação e Ent = infraestrutura | DevOps & SRE | +2 |
| R20 | Ativ = nuvem | Cloud | +4 |
| R21 | Ativ = nuvem e Ent = infraestrutura | Cloud | +3 |
| R22 | Ativ = mobile | Mobile | +4 |
| R23 | Ativ = mobile e Ent = produto | Mobile | +2 |
| R24 | Ativ = mobile e Ferr = Java/Kotlin/Swift ou JavaScript | Mobile | +2 |
| R25 | Ativ = testes | QA | +4 |
| R26 | Ent = qualidade | QA | +3 |
| R27 | Ativ = testes e Ferr = Python, JavaScript ou Java/Kotlin/Swift | QA | +1 |
| R28 | Ativ = negócios/ágil | Product Management | +4 |
| R29 | Ent = estratégia | Product Management | +3 |
| R30 | Ativ = negócios e Ferr = Nenhuma/Iniciante | Product Management | +2 |
| R31 | Regra de decisão: soma os pontos e declara a trilha vencedora | todas | — |
| R32 | Regra de justificativa: lista os motivos da trilha vencedora | — | — |

## Separação entre Cientista e Engenheiro de Dados

- A atividade diária já distingue as duas (R07 x R11).
- A entrega separa as duas: modelos e IA (R08) x dados confiáveis (R12).
- Matemática alta reforça Ciência de Dados (R08, R09); matemática baixa transfere pontos para Engenharia de Dados (R10).