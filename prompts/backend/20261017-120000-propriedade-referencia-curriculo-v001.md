---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-17T12:00:00-03:00"
lineage:
  mode: initial
  root: null
  supersedes: null
  change_type: initial
  secondary_change_types: []
  decision_impact: initial
subjects:
  kind: mixed
  files:
    - path: src/backend/application/selecao_itens_versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "6f3a032e1dca9869cc5c75c7079001a818bb9c43"
      availability: available
    - path: src/backend/domain/curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "agregado Curriculo, incluir_referencia e remover_referencia (linhas 1-110)"
      content_state: commit
      revision: "6f3a032e1dca9869cc5c75c7079001a818bb9c43"
      availability: partial
    - path: src/backend/domain/exceptions.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "6f3a032e1dca9869cc5c75c7079001a818bb9c43"
      availability: available
    - path: src/backend/tests/test_application_selecao_itens_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: selected-section
      locator: "doubles e nomes dos testes de seleção (linhas 1-130 e lista de nomes)"
      content_state: commit
      revision: "6f3a032e1dca9869cc5c75c7079001a818bb9c43"
      availability: partial
    - path: "GitHub issue #210 (F5.2)"
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: external
      revision: null
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "6f3a032e1dca9869cc5c75c7079001a818bb9c43"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "6f3a032e1dca9869cc5c75c7079001a818bb9c43"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "Decide onde mora a regra de propriedade da referência selecionada, na linhagem de seleção de itens de prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, security]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: low
  reversibility: easy
  risk: low
---

# Análise de decisão — propriedade da referência selecionada no domínio

## Solicitação original

```text
[F5.2] Validar no domínio que uma referência selecionada pertence ao estudante dono do currículo.
WBS: 1.4.1., 1.4.2. — Início: 2026-10-19 — Entrega: 2026-10-25
Responsável único: @regazzio
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Modo de trabalho pedido: a assistente escreve os arquivos e o usuário faz os commits.
- Esta análise é independente das anteriores e não as revisa; a decisão original da seleção de itens (task 117) colocou essa verificação na Application.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `6f3a032e1dca9869cc5c75c7079001a818bb9c43` (cabeça da `dev` na consulta), lido por `git show origin/dev:<caminho>`.
- O corpo da issue #210 foi visto somente pelo texto colado pelo usuário.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

A regra de que uma versão de currículo só reúne itens do próprio estudante é uma invariante do domínio, protegida no agregado `Curriculo`, e não apenas uma verificação solta na orquestração.

### Evidências e fatos observados

1. Hoje o caso `SelecionarItemVersaoCurriculo` consulta o dono do item por porta e compara com o usuário solicitante; o domínio não conhece essa regra (`selecao_itens_versao_curriculo.py`).
2. `Curriculo.incluir_referencia` protege somente a duplicidade; a documentação do agregado afirma que ele não valida propriedade transagregados (`curriculo.py`).
3. O agregado não pode consultar outros agregados; o dono do item só é conhecido por quem orquestra a consulta.
4. O adaptador de persistência reconstitui o agregado chamando `incluir_referencia` e não deve revalidar propriedade ao ler do banco (`infrastructure/persistence/sqlalchemy/curriculo.py`).
5. Os testes do caso de uso já cobrem item inexistente, item de outro usuário (sem atualizar) e item duplicado.
6. O front-end e a API tratam item ausente e item alheio com a mesma resposta (`ItemNaoEncontrado`), para não revelar que o item existe.

### Hipóteses

- **H1.** O domínio recebe o proprietário já resolvido pela Application e valida a igualdade com o dono do agregado, sem consultar nada.
- **H2.** Novo método `Curriculo.incluir_referencia_do_proprietario(referencia, proprietario_do_item)` e nova exceção `ReferenciaDeOutroProprietario`, subclasse de `RegraDeDominioViolada`.
- **H3.** `incluir_referencia` permanece como está, para a reconstituição pelo adaptador.
- **H4.** A propriedade é verificada antes da duplicidade, para não revelar a composição por item alheio.
- **H5.** O caso de uso mantém a ausência do item como `ItemNaoEncontrado` e traduz `ReferenciaDeOutroProprietario` para a mesma falha, preservando o contrato da API.

### Perguntas em aberto

1. A reconstituição pelo adaptador deve, no futuro, usar um caminho próprio em vez de `incluir_referencia`?

### Escopo

- Domínio: nova exceção, novo método do agregado e exportação.
- Application: uso do novo método e tradução da falha, sem mudar o contrato externo.
- Testes unitários do domínio; os testes existentes do caso de uso continuam válidos.

### Fora do escopo

- Alterar API, persistência, portas ou a política de exclusão.
- Validar propriedade na desseleção (a referência só existe se passou pela inclusão).

### Critérios de sucesso

- Item do dono é incluído; item de outro estudante é recusado com `ReferenciaDeOutroProprietario` sem alterar a versão.
- A falha por propriedade prevalece sobre a duplicidade.
- O contrato da API (`ItemNaoEncontrado`) permanece igual.
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Regras e invariantes ficam no domínio, no ponto mais próximo dos dados; o domínio não consulta outros agregados nem depende da Application (`src/backend/AGENTS.md`).
- Docstring (o que faz, como faz, finalidade) e proveniência em todo trecho novo.

## Classificação comentada

- `uncertainty: low`, `reversibility: easy` e `risk: low`: mudança pequena e coberta por testes existentes.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | 1 | Item alheio nunca entra na versão | Evita expor dado de outro estudante |
| `simplicity` | 1 | Mudança revisável em 10 minutos | Critério de aceite da issue |
| `modifiability` | 2 | Contrato externo preservado | API e front-end não mudam |

## Alternativas consideradas

**Estado atual.** A verificação está na Application; o domínio não protege a invariante.

**Alternativa A — Novo método no agregado que recebe o proprietário (recomendada).** Mantém o agregado sem consultar outros agregados e move a regra para o domínio; a Application só resolve o dono e traduz a falha.

**Alternativa B — Mudar a assinatura de `incluir_referencia` para exigir o proprietário.** Regra única, mas quebra a reconstituição pelo adaptador e todos os testes existentes do agregado.

**Alternativa C — Serviço de domínio separado.** Também resolve, mas adiciona um tipo sem benefício demonstrável para uma comparação simples.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | 1 | +1 | +1 | +1 | média | As três protegem a invariante |
| `simplicity` | 1 | +1 | -1 | 0 | média | B altera chamadores; C cria tipo novo |
| `modifiability` | 2 | +1 | -1 | 0 | média | B afeta a reconstituição |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada nesta linhagem; a decisão da task 117 colocou a verificação na Application.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**. Status `proposed`: aprovação humana.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | prioritized | Invariante no domínio | Testes do método |
| `simplicity` | prioritized | Um método e uma exceção | Sem mudar portas nem API |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `modifiability` | Contrato externo preservado | A Application traduz a falha para `ItemNaoEncontrado` |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | Nova entrada no domínio sem a verificação de propriedade | Média | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `modifiability` | Dois métodos de inclusão no agregado | `simplicity` | Aceitável: um é para reconstituição, outro para seleção |

## Riscos e efeitos de segunda ordem

- **Chamada direta ao método antigo.** Quem usar `incluir_referencia` em fluxo de seleção contorna a regra. Mitigação: o caso de uso usa o novo método; pergunta 1 registrada.
- **Conflitos de integração.** Alterações em `domain/__init__.py` costumam conflitar com outras tarefas; resolver ao integrar a `dev`.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Item do dono entra | Referência presente | Teste de domínio | Falha indevida |
| Item alheio é recusado sem alterar | `ReferenciaDeOutroProprietario` e composição vazia | Teste de domínio | Item entra |
| Propriedade antes da duplicidade | Falha específica ao repetir com dono alheio | Teste de domínio | Mensagem de duplicidade |
| Contrato da API preservado | `ItemNaoEncontrado` para item alheio | Testes existentes do caso de uso | Teste existente falha |

## Handoffs e atividades posteriores

- **`$backend-domain-orchestration-v2`:** nenhuma etapa adicional; a mudança de Application é parte desta entrega.
- **Futuro:** considerar caminho próprio de reconstituição no adaptador (pergunta 1).

## Síntese

A regra de que a versão só reúne itens do próprio estudante estava apenas na orquestração. A decisão a leva ao agregado `Curriculo`, que passa a recusar item de outro proprietário, sem consultar outros agregados: a Application continua resolvendo o dono e traduzindo a falha para o contrato já existente.
