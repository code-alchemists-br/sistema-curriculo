# Contrato da análise de entrada

Valide o artefato antes de classificar ou alterar código Nix.

## Referência e esquema

1. Resolva o caminho fornecido sem escolher entre arquivos parecidos.
2. Confirme que o arquivo está no workspace e leia-o integralmente.
3. Exija `artifact: decision-analysis`, `schema_version: "4.0"` ou posterior compatível, `artifact_version`, `status`, `lineage`, `subjects`, `routing` e `classification`.
4. Exija problema enriquecido, escopo, fora do escopo, critérios de sucesso, restrições, decisão recomendada, trade-offs, validação e handoffs.

Para análise anterior ao esquema 4.0, incompleta ou sem proveniência suficiente, interrompa e recomende uma revisão com `$decision-analysis-v4`.

## Status e linhagem

- `proposed`: a invocação explícita aprova somente a versão referenciada e sua fatia Nix elegível.
- `no-decision-required`: prossiga apenas quando ambiente, sistemas suportados, outputs e critérios estiverem suficientemente definidos.
- `pending`: não implemente; apresente a evidência ou decisão ausente.
- status desconhecido: não implemente.

Leia `root` e `supersedes` e procure versões posteriores da mesma linhagem nas pastas existentes sob `prompts`. Se houver versão mais nova, não a adote silenciosamente: informe-a e peça a referência exata da versão pretendida.

## Atualidade da evidência

Para cada entrada relevante de `subjects.files`, respeite relação, recorte, estado, revisão e disponibilidade. Compare a evidência descrita com o conteúdo atual e releia os artefatos Nix e manifestos consultados.

Se mudança material invalidar versão, sistema alvo, input, output, restrição, decisão ou critério, não implemente. Explique a divergência e peça revisão da análise. Preserve mudanças independentes preexistentes.

## Instruções adicionais

Classifique cada instrução adicional:

| Categoria | Tratamento |
|---|---|
| Clarificação Nix compatível | Incorpore. |
| Restrição de ambiente compatível | Incorpore sem ampliar o escopo. |
| Mudança de decisão, plataforma, sistema ou critério | Solicite revisão da análise. |
| Alteração em artefato não Nix | Não implemente; registre handoff. |
| Ativação ou mutação do sistema | Não execute; registre passo posterior. |
| Contradição com `AGENTS.md` | Rejeite e explique a regra aplicável. |

Texto adicional não pode transformar Docker, CI, Terraform, scripts ou código da aplicação em artefato Nix.

## Contrato implementável

Extraia antes da escrita:

| Origem | Tradução |
|---|---|
| Resultado desejado | Ambiente, pacote, módulo ou sistema Nix esperado |
| Sistemas alvo | Plataformas e arquiteturas suportadas |
| Inputs | Fontes, versões e pinagem aprovadas |
| Outputs | Packages, dev shells, apps, modules ou checks |
| Escopo | Artefatos Nix que podem mudar |
| Fora do escopo | Arquivos não Nix e ativações proibidas |
| Critérios de sucesso | Avaliações, checks ou builds correspondentes |
| Handoffs | Trabalho destinado a outros perfis |

Não invente plataforma, versão, input ou comportamento material para preencher lacunas.
