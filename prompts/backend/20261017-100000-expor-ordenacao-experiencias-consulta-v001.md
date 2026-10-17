---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-17T10:00:00-03:00"
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
    - path: prompts/backend/20261016-140000-ordenacao-experiencias-profissionais-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "6f3a032"
      availability: available
    - path: src/backend/application/previa_versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "6f3a032"
      availability: available
    - path: src/backend/api/previa_versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "ExperienciaPreviaResposta, PreviaVersaoCurriculoResposta, criar_router"
      content_state: commit
      revision: "6f3a032"
      availability: available
    - path: prompts/backend/20261016-100000-expor-ordenacao-formacoes-consulta-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "6f3a032"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "6f3a032"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "6f3a032"
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

# Análise de decisão — expor a ordenação de experiências na resposta de consulta

## Solicitação original

Issue GitHub nº 185: `[F3.4] Expor a ordenação de experiências na resposta de
consulta; cobrir o contrato da rota.` Continuação da issue nº 184, que criou a
regra de domínio `ordenar_experiencias`. Decisão do responsável: remover
`_ordenar_por_periodo` somente se ela deixar de ser utilizada.

## Artefatos analisados

- Não existe rota de listagem de experiências; a única consulta que as devolve
  é a prévia de versão de currículo,
  `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/previa`.
- `GerarPreviaVersaoCurriculo` ordenava experiências por
  `_ordenar_por_periodo` (início decrescente e identificador), última
  utilização dessa função após a issue nº 183.
- `ExperienciaPreviaResposta` já expõe `id`, `inicio` e `fim`; o término nulo
  identifica a experiência em andamento.

## Problema enriquecido

### Resultado desejado

A resposta de consulta da prévia apresenta as experiências na ordem definida
pelo domínio, e o contrato da rota que transporta essa ordem fica coberto por
teste.

### Escopo

- Substituir `_ordenar_por_periodo` por `ordenar_experiencias` na prévia.
- Remover `_ordenar_por_periodo`, que deixa de ter qualquer uso no código e
  nos testes.
- Teste de Application com experiências de mesmo início, uma em andamento e
  outra encerrada.
- Testes da rota: preservação da ordem recebida com datas e término nulo, e
  esquema OpenAPI de `experiencias`.

### Fora do escopo

- Rota dedicada de listagem de experiências.
- Ordenação manual prevista no wireframe 05.

## Decisão recomendada nesta versão

A Application delega a ordem das experiências ao domínio, como já faz com as
formações, e a rota apenas projeta a sequência recebida. Com isso, nenhuma
seção com período é ordenada na Application, e `_ordenar_por_periodo` é
removida por não ter mais chamadas; menções em análises anteriores permanecem
como registro histórico.

## Riscos e efeitos de segunda ordem

- A resposta só muda para experiências com o mesmo início: a em andamento
  passa a vir antes da encerrada, independentemente do identificador.
- Uma futura listagem dedicada deve reutilizar `ordenar_experiencias`.

## Validação da decisão

- A prévia devolve, para mesmo início, a experiência em andamento antes da
  encerrada, mesmo quando a encerrada tem o menor identificador.
- O handler preserva identificadores e datas, inclusive término nulo, na ordem
  recebida.
- O OpenAPI declara `experiencias` como lista de `ExperienciaPreviaResposta`
  com `id`, `inicio` e `fim` obrigatórios e `fim` anulável.

## Síntese

A prévia passa a expor as experiências pela regra de domínio, a função de
ordenação da Application que ficou sem uso é removida, e o contrato da rota que
carrega essa ordem fica protegido por testes.
