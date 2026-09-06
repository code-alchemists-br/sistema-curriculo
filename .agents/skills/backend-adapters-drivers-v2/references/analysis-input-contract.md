# Contrato da análise de entrada

1. Resolva um único caminho no workspace e leia a análise integralmente.
2. Exija `artifact: decision-analysis`, esquema 4.0 ou posterior compatível, versão, status, linhagem, subjects, routing e classification.
3. Exija problema, escopo, não objetivos, critérios, restrições, decisão, trade-offs, validação e handoffs.
4. Para análise antiga ou incompleta, solicite revisão com `$decision-analysis-v4`.

## Status, linhagem e atualidade

- `proposed`: a invocação explícita aprova somente a versão e fatia elegível.
- `no-decision-required`: prossiga apenas com interface, contratos e resultado suficientes.
- `pending` ou desconhecido: não implemente.

Leia `root` e `supersedes`; não troque silenciosamente por versão posterior encontrada em `prompts`. Compare `subjects.files` ao estado atual. Mudança material exige revisão; alterações independentes devem ser preservadas.

## Instruções adicionais

| Categoria | Tratamento |
|---|---|
| Clarificação de adapter, driver ou teste unitário | Incorpore. |
| Restrição externa local compatível | Incorpore. |
| Mudança material | Solicite revisão. |
| Teste de integração ou superior | Handoff para `$integration-system-testing-v1`. |
| Domínio, orquestração ou nova porta | Handoff para `$backend-domain-orchestration-v2`. |
| Frontend ou transversal | Não implemente; faça handoff. |
| Contradição com `AGENTS.md` | Rejeite e explique. |

Extraia comportamento externo, contratos internos, interfaces, mapeamentos, unidades testáveis, critérios e handoffs. Não invente regra, caso de uso, porta, protocolo ou nível de teste.
