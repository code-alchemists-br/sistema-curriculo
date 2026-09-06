# Contrato da análise de entrada

1. Resolva um único caminho no workspace e leia a análise integralmente.
2. Exija `artifact: decision-analysis`, esquema 4.0 ou posterior compatível, versão, status, linhagem, subjects, routing e classification.
3. Exija problema, escopo, não objetivos, critérios, restrições, decisão, trade-offs, validação e handoffs.
4. Para análise antiga ou incompleta, solicite revisão com `$decision-analysis-v4`.

## Status, linhagem e atualidade

- `proposed`: a invocação explícita aprova somente a versão e fatia elegível.
- `no-decision-required`: prossiga apenas com regras e resultado suficientes.
- `pending` ou desconhecido: não implemente.

Leia `root` e `supersedes`; não troque silenciosamente por versão posterior encontrada em `prompts`. Compare `subjects.files` ao estado atual. Mudança material exige revisão; mudanças independentes devem ser preservadas.

## Instruções adicionais

| Categoria | Tratamento |
|---|---|
| Clarificação de regra, orquestração ou teste unitário | Incorpore. |
| Restrição interna compatível | Incorpore. |
| Mudança material | Solicite revisão. |
| Teste de integração ou superior | Handoff para `$integration-system-testing-v1`. |
| Adapter, driver, frontend ou transversal | Não implemente; faça handoff. |
| Contradição com `AGENTS.md` | Rejeite e explique. |

Extraia comportamento, regras, fluxo, portas, unidades testáveis, critérios, trade-offs e handoffs. Não invente regra, porta, contrato ou nível de teste.
