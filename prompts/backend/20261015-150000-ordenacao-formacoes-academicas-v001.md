---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-15T15:00:00-03:00"
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
      locator: "FormacaoAcademica, StatusFormacaoAcademica"
      content_state: commit
      revision: "fe383e4"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "Periodo"
      content_state: commit
      revision: "fe383e4"
      availability: available
    - path: src/backend/application/previa_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "_ordenar_por_periodo"
      content_state: commit
      revision: "fe383e4"
      availability: available
    - path: docs/wireframes/04-formacao.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fe383e4"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fe383e4"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fe383e4"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "A decisão define uma regra do domínio do backend; a documentação de produto não especifica a ordem."
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

# Análise de decisão — ordenação estável de formações acadêmicas

## Solicitação original

Issue GitHub nº 182: `[F3.1] Definir a ordenação estável de formações por
situação e data; cobrir empate no teste de domínio.` Decisão de produto
informada pelo responsável: priorizar as formações em andamento, da data de
início mais recente para a mais antiga, e depois as terminadas, do término mais
recente para o mais antigo.

## Artefatos analisados

- `FormacaoAcademica` possui `status` (`em_andamento`, `concluido`,
  `interrompido`) e `Periodo(inicio, fim)`, com `fim` obrigatório apenas para
  formações concluídas.
- A prévia de currículo ordena formações somente pela data de início, na camada
  de Application, sem considerar a situação.
- Wireframes e jornadas citam período e situação de conclusão, mas não definem
  a ordem de apresentação.

## Problema enriquecido

### Resultado desejado

Uma regra única, no domínio, que produza sempre a mesma sequência de formações
para a mesma coleção, independentemente da ordem de entrada.

### Escopo

- Função de domínio `ordenar_formacoes` em `domain/itens_perfil.py`.
- Testes de domínio cobrindo situação, datas, período aberto e empate total.

### Fora do escopo

- Expor a ordenação na resposta de consulta (issue nº 183, F3.2).
- Substituir `_ordenar_por_periodo` da prévia de currículo.
- Ordenação de experiências (issue nº 184, F3.3).

## Decisão recomendada nesta versão

Ordenar pela chave composta:

1. Prioridade da situação: em andamento (0), concluída (1), interrompida (2).
2. Data de referência decrescente: início para formações em andamento; término
   para concluídas e interrompidas, recorrendo ao início quando a interrompida
   não tiver término.
3. Data de início decrescente.
4. Identificador textual crescente, garantindo ordem total e estável.

A prioridade fica em um mapa explícito em vez de depender da ordem de
declaração do enum, para que reordenar membros do vocabulário não altere a
apresentação. A função é pura, aceita qualquer iterável e devolve tupla.

### Alternativa descartada — ordenar apenas pela data de início

É a regra atual da prévia, mas coloca uma conclusão recente abaixo de uma
formação em andamento e não usa o término, que representa melhor a relevância
de uma formação concluída.

## Riscos e efeitos de segunda ordem

- Até a F3.2, a prévia continua usando a regra antiga; as duas ordens podem
  divergir para formações concluídas ou interrompidas.
- A posição das interrompidas após as concluídas é uma extensão da decisão de
  produto e pode ser revista sem impacto estrutural.

## Validação da decisão

- Em andamento antiga aparece antes de concluída e interrompida recentes.
- Em andamento ordena pelo início, ignorando previsão de término.
- Concluídas ordenam pelo término mais recente.
- Interrompida sem término usa o início.
- Mesmo término desempata pelo início mais recente.
- Empate total produz a mesma sequência para várias permutações da entrada.
- Coleção vazia devolve tupla vazia.

## Síntese

Formações passam a ter uma ordenação de domínio estável: em andamento primeiro
pelo início mais recente, depois concluídas e interrompidas pelo término mais
recente, com desempate por início e identificador.
