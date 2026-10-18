---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-16T14:00:00-03:00"
lineage:
  mode: initial
  root: null
  supersedes: null
  change_type: initial
  secondary_change_types: []
  decision_impact: new
subjects:
  kind: mixed
  files:
    - path: src/backend/domain/itens_perfil.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "ExperienciaProfissional, ordenar_formacoes"
      content_state: commit
      revision: "0c208c4"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "Periodo"
      content_state: commit
      revision: "0c208c4"
      availability: available
    - path: src/backend/application/previa_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "_ordenar_por_periodo"
      content_state: commit
      revision: "0c208c4"
      availability: available
    - path: prompts/backend/20261015-150000-ordenacao-formacoes-academicas-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "0c208c4"
      availability: available
    - path: docs/wireframes/05-experiencias.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "0c208c4"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "0c208c4"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "0c208c4"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "A decisão define uma regra do domínio do backend; a documentação de produto não especifica a ordem automática."
classification:
  sphere: engineering
  concerns: [domain]
  decision_kind: design
  scope: component
  lifecycle: evolution
  urgency: normal
  uncertainty: low
  reversibility: easy
  risk: low
---

# Análise de decisão — ordenação estável de experiências profissionais

## Solicitação original

Issue GitHub nº 184: `[F3.3] Definir a ordenação estável de experiências por
data de início; cobrir empate no teste de domínio.` Decisão de produto
informada pelo responsável: no empate de início, a experiência sem término (em
andamento) vem primeiro; `_ordenar_por_periodo` da prévia deve ser mantida.

## Artefatos analisados

- `ExperienciaProfissional` possui `Periodo(inicio, fim)`, com `fim` opcional
  para experiências em andamento, e não possui campo de situação.
- `ordenar_formacoes` (issue nº 182) estabeleceu o padrão de função pura de
  domínio com chave em tupla e desempate por identificador.
- A prévia de currículo ordena experiências por `_ordenar_por_periodo`, na
  Application, pelo início decrescente e identificador.
- Wireframe 05 e jornada §6.5 citam a ação "Ordenar" manual, mas não definem
  ordem automática.

## Problema enriquecido

### Resultado desejado

Uma regra única, no domínio, que produza sempre a mesma sequência de
experiências para a mesma coleção, independentemente da ordem de entrada.

### Escopo

- Função de domínio `ordenar_experiencias` em `domain/itens_perfil.py`,
  exportada pelo pacote `backend.domain`.
- Testes de domínio cobrindo início, desempate por andamento e término, e
  empate total.

### Fora do escopo

- Aplicar a regra na prévia e cobrir o contrato da rota (issue nº 185).
- Remover `_ordenar_por_periodo`, mantida por decisão do responsável.
- Ordenação manual prevista no wireframe, que exigiria persistir posições.

## Decisão recomendada nesta versão

Ordenar pela chave composta:

1. Data de início decrescente.
2. Experiência sem término antes das encerradas.
3. Data de término decrescente entre encerradas.
4. Identificador textual crescente, garantindo ordem total e estável.

### Alternativa descartada — desempatar diretamente pelo identificador

Reproduz exatamente a prévia atual, mas pode colocar uma experiência encerrada
acima da atual quando ambas começaram no mesmo dia, contrariando a decisão de
produto.

## Riscos e efeitos de segunda ordem

- Até a issue nº 185, a prévia continua com `_ordenar_por_periodo`; as ordens
  só divergem para experiências com o mesmo início.

## Validação da decisão

- Início mais recente aparece primeiro.
- Término não altera a ordem quando os inícios diferem.
- Mesmo início: em andamento antes de encerrada.
- Mesmo início entre encerradas: término mais recente primeiro.
- Empate total produz a mesma sequência para várias permutações da entrada.
- Coleção vazia devolve tupla vazia.

## Síntese

Experiências passam a ter uma ordenação de domínio estável: início mais recente
primeiro e, no empate, em andamento antes de encerradas, com desempate final
por identificador.
