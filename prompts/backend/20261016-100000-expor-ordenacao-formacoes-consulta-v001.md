---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-16T10:00:00-03:00"
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
    - path: prompts/backend/20261015-150000-ordenacao-formacoes-academicas-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "a08488c"
      availability: available
    - path: src/backend/application/previa_versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "a08488c"
      availability: available
    - path: src/backend/api/previa_versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "FormacaoPreviaResposta, PreviaVersaoCurriculoResposta, criar_router"
      content_state: commit
      revision: "a08488c"
      availability: available
    - path: docs/wireframes/04-formacao.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "a08488c"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "a08488c"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "a08488c"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend]
  confidence: high
  rationale: "A decisão altera a orquestração da prévia no backend e o contrato coberto da sua rota."
classification:
  sphere: engineering
  concerns: [domain, architecture]
  decision_kind: design
  scope: component
  lifecycle: evolution
  urgency: normal
  uncertainty: low
  reversibility: easy
  risk: low
---

# Análise de decisão — expor a ordenação de formações na resposta de consulta

## Solicitação original

Issue GitHub nº 183: `[F3.2] Expor a ordenação de formações na resposta de
consulta; cobrir o contrato da rota.` Continuação da issue nº 182, que criou a
regra de domínio `ordenar_formacoes`.

## Artefatos analisados

- Não existe rota de listagem de formações; a API de formação oferece apenas
  cadastro, edição e exclusão.
- A única consulta que devolve formações é a prévia de versão de currículo,
  `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/previa`.
- `GerarPreviaVersaoCurriculo` ordenava formações por `_ordenar_por_periodo`,
  que considera somente a data de início.
- `FormacaoPreviaResposta` já expõe `id`, `status`, `inicio` e `fim`, campos
  suficientes para o cliente reconhecer a ordem aplicada.

## Problema enriquecido

### Resultado desejado

A resposta de consulta da prévia apresenta as formações na ordem definida pelo
domínio, e o contrato da rota que transporta essa ordem fica coberto por teste.

### Escopo

- Substituir, apenas para formações, `_ordenar_por_periodo` por
  `ordenar_formacoes` na prévia.
- Teste de Application com formações de todas as situações fora de ordem.
- Testes da rota: preservação da ordem recebida com situação e datas, e esquema
  OpenAPI de `formacoes`.

### Fora do escopo

- Rota dedicada de listagem de formações do estudante; depende de porta de
  listagem, caso de uso e card próprio.
- Ordenação de experiências (issues nº 184 e 185).

## Alternativas consideradas

### Alternativa A — aplicar a regra de domínio na prévia existente

Mantém a mudança pequena, reutiliza o único contrato de consulta já publicado e
elimina a divergência entre a prévia e a regra de domínio.

### Alternativa B — criar `GET` de listagem de formações

Atende à lista prevista no wireframe 04, mas exige nova porta de repositório,
caso de uso, rota e testes de infraestrutura, excedendo o tamanho da tarefa.

## Decisão recomendada nesta versão

Adotar a Alternativa A. A Application delega a ordem ao domínio e a rota apenas
projeta a sequência recebida, sem reordenar. `_ordenar_por_periodo` permanece
para experiências até as tarefas correspondentes.

## Riscos e efeitos de segunda ordem

- Clientes que dependiam da ordem apenas por início verão concluídas e
  interrompidas após as em andamento.
- Quando a listagem dedicada for criada, ela deve reutilizar
  `ordenar_formacoes` para manter a mesma ordem.

## Validação da decisão

- A prévia devolve em andamento, concluídas pelo término mais recente e
  interrompidas por último, para seleção fora de ordem.
- O handler preserva identificadores, situações e datas na ordem recebida.
- O OpenAPI declara `formacoes` como lista de `FormacaoPreviaResposta` com
  `id`, `status`, `inicio` e `fim` obrigatórios.

## Síntese

A prévia passa a expor as formações pela regra de domínio de situação e data, e
o contrato da rota que carrega essa ordem fica protegido por testes.
