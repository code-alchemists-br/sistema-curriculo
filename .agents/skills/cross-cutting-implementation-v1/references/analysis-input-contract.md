# Contrato da análise de entrada

## Artefato

1. Resolva um único caminho no workspace e leia a análise integralmente.
2. Exija `artifact: decision-analysis`, esquema 4.0 ou posterior compatível, versão, status, linhagem, subjects, routing e classification.
3. Exija problema, escopo, não objetivos, critérios, restrições, decisão, trade-offs, validação e handoffs.
4. Para análise antiga ou incompleta, solicite revisão com `$decision-analysis-v4`.

## Status, linhagem e atualidade

- `proposed`: a invocação explícita aprova somente versão e fatia elegível.
- `no-decision-required`: prossiga somente com concern, modo e critérios suficientes.
- `pending` ou desconhecido: não implemente.

Leia `root` e `supersedes`; não troque silenciosamente por versão posterior encontrada em `prompts`. Compare `subjects.files` ao estado atual. Mudança material exige revisão; alterações independentes devem ser preservadas.

## Modo

Classifique como `evaluation-only`, `implementation-only` ou `evaluation-and-implementation`. Se a análise pedir “avaliar” sem autorizar remediação, não escreva código. Se pedir implementar sem baseline, faça somente a inspeção necessária para executar com segurança.

## Evidência mínima por concern

- observabilidade: sinais/eventos, pontos de emissão, campos/contexto, destino lógico e critérios de qualidade;
- resiliência: modo de falha, fronteira, timeout/budget, segurança de repetição, fallback e resultado esperado;
- segurança: ativo, ameaça, fronteira de confiança, controle esperado e condição de sucesso;
- autorização: sujeitos, ações, recursos, contexto, matriz/policy, pontos de enforcement e comportamento de negação.

Ausência que obrigue a inventar política material torna a demanda `ambiguous` ou `pending`.

## Instruções adicionais

| Categoria | Tratamento |
|---|---|
| Clarificação do concern ou critério | Incorpore. |
| Restrição segura compatível | Incorpore. |
| Mudança de policy, ameaça, budget, limiar ou escopo | Solicite revisão. |
| Funcionalidade de outra área | Não implemente; faça handoff. |
| Teste superior à unidade | Handoff para `$integration-system-testing-v1`. |
| Operação externa/live | Exija autorização própria; não presuma. |
| Contradição com `AGENTS.md` | Rejeite e explique. |

Extraia concern, modo, resultado, baseline, pontos de integração, policy, dados sensíveis, falhas, critérios, testes unitários e handoffs. Não invente decisões ausentes.
