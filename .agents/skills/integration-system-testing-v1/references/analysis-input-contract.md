# Contrato da análise de entrada

Valide o artefato antes de classificar ou alterar testes.

## Referência e esquema

1. Resolva o caminho fornecido sem escolher entre arquivos parecidos.
2. Confirme que o arquivo está no workspace e leia-o integralmente.
3. Exija `artifact: decision-analysis`, `schema_version: "4.0"` ou posterior compatível, `artifact_version`, `status`, `lineage`, `subjects`, `routing` e `classification`.
4. Exija problema enriquecido, escopo, fora do escopo, critérios de sucesso, restrições, decisão recomendada, trade-offs, validação e handoffs.

Para análise anterior ao esquema 4.0, incompleta ou sem proveniência suficiente, interrompa e recomende uma revisão com `$decision-analysis-v4`.

## Status e linhagem

- `proposed`: a invocação explícita aprova somente a versão referenciada e sua fatia elegível.
- `no-decision-required`: prossiga apenas quando alvo, nível, cenário e oráculo estiverem suficientemente definidos.
- `pending`: não implemente; apresente a evidência ou decisão ausente.
- status desconhecido: não implemente.

Leia `root` e `supersedes` e procure versões posteriores da mesma linhagem nas pastas existentes sob `prompts`. Se houver versão mais nova, não a adote silenciosamente: informe-a e peça a referência exata da versão pretendida.

## Atualidade da evidência

Para cada entrada relevante de `subjects.files`, respeite relação, recorte, estado, revisão e disponibilidade. Compare a evidência descrita com o sistema e a suíte atuais. Releia interfaces, contratos, runners, fixtures e configurações que poderão ser usados.

Se mudança material invalidar comportamento, contrato, ambiente, oráculo, decisão ou critério, não implemente. Explique a divergência e peça revisão da análise. Preserve mudanças independentes preexistentes.

## Instruções adicionais

Classifique cada instrução adicional:

| Categoria | Tratamento |
|---|---|
| Clarificação de cenário, dado ou oráculo compatível | Incorpore. |
| Restrição segura de execução | Incorpore sem ampliar o escopo. |
| Mudança de nível, comportamento, limiar ou critério | Solicite revisão da análise. |
| Teste unitário ou alteração no produto | Não implemente; registre handoff. |
| CI, deploy ou ambiente externo | Não execute; registre handoff. |
| Contradição com `AGENTS.md` | Rejeite e explique a regra aplicável. |

Uma instrução adicional não autoriza alvo externo, carga destrutiva ou mudança de produção sem autorização específica correspondente.

## Contrato de teste implementável

Extraia antes da escrita:

| Origem | Tradução |
|---|---|
| Resultado ou risco | O que o teste deve demonstrar |
| Nível | Integração, contrato, sistema, aceitação, E2E ou não funcional |
| Sistema sob teste | Componentes e fronteiras reais envolvidos |
| Cenário e dados | Pré-condições, estímulo e massa sintética |
| Oráculo | Saída, estado ou medição esperada |
| Ambiente | Alvo isolado e dependências controladas |
| Critérios de sucesso | Asserções e limiares aprovados |
| Segurança da execução | Intensidade, isolamento e cleanup |
| Handoffs | Unitários, mudanças de produto ou operações externas |

Para testes não funcionais, não invente workload, concorrência, duração, percentil, SLA, matriz de acesso, falha injetada ou limiar de aprovação.
