# Contrato da análise de entrada

1. Resolva um único caminho dentro do workspace e leia a análise integralmente.
2. Exija `artifact: decision-analysis`, esquema 4.0 ou posterior compatível, versão, status, linhagem, subjects, routing e classification.
3. Exija problema, escopo, fora do escopo, critérios, restrições, decisão, trade-offs, validação e handoffs.
4. Para análise antiga ou incompleta, solicite revisão com `$decision-analysis-v4`.

## Status e linhagem

- `proposed`: a invocação explícita aprova somente a versão e a fatia elegível.
- `no-decision-required`: prossiga apenas com resultado e critérios suficientes.
- `pending` ou status desconhecido: não implemente.

Leia `root` e `supersedes`. Se existir versão posterior da linhagem sob `prompts`, não a adote silenciosamente; peça a referência exata pretendida.

## Atualidade

Compare `subjects.files` e o conteúdo atual, respeitando relação, recorte, estado, revisão e disponibilidade. Se mudança material invalidar decisão ou critério, solicite revisão. Preserve alterações independentes.

## Instruções adicionais

| Categoria | Tratamento |
|---|---|
| Clarificação funcional ou de teste unitário | Incorpore. |
| Restrição compatível | Incorpore sem ampliar o escopo. |
| Mudança material | Solicite revisão da análise. |
| Teste de integração ou superior | Registre handoff para `$integration-system-testing-v1`. |
| Outra camada ou preocupação transversal | Não implemente; registre handoff. |
| Contradição com `AGENTS.md` | Rejeite e explique. |

Extraia resultado de tela, escopo, não objetivos, decisão, critérios, unidades testáveis, trade-offs e handoffs. Não invente comportamento, contrato ou estratégia de teste.
