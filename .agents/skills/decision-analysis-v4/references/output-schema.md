# Esquema do artefato de análise v4

Produza em português, salvo pedido contrário. Preserve valores controlados em inglês.

```md
---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "vNNN"
status: proposed | pending | no-decision-required
created_at: YYYY-MM-DD
lineage:
  mode: initial | revision
  root: null | caminho-do-v001
  supersedes: null | caminho-da-versao-anterior
  change_type: initial | enrichment | correction | scope-change | reassessment
  secondary_change_types: []
  decision_impact: initial | unchanged | strengthened | revised | reopened | invalidated
subjects:
  kind: demand-only | single-file | file-set | directory | repository | diff | mixed
  files:
    - path: caminho-relativo-ou-identificador
      relationship: primary | supporting | context
      representation: valor-controlado
      function: valor-controlado
      format: formato-ou-linguagem
      analysis_scope: whole-file | selected-section | diff | metadata-only
      locator: null | linhas-secao-ou-diff
      content_state: working-tree | staged | commit | external | unknown
      revision: null | referencia
      availability: available | partial | unavailable
routing:
  root: prompts
  selected_directory: prompts/<pasta-existente>
  considered_directories: [prompts/<candidata>]
  confidence: high | medium | low
  rationale: "justificativa curta"
classification:
  sphere: valor-controlado
  concerns: [valores-controlados]
  decision_kind: valor-controlado
  scope: valor-controlado
  lifecycle: valor-controlado
  urgency: valor-controlado
  uncertainty: valor-controlado
  reversibility: valor-controlado
  risk: valor-controlado
---

# Análise de decisão — <título>

## Solicitação original

## Informações complementares

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|

Use `Nenhum — análise baseada somente na demanda` quando `subjects.kind: demand-only`.

### Limites da evidência dos artefatos

Informe conteúdo parcial, indisponibilidade, recorte limitado ou ausência de referência de versão.

## Problema enriquecido

### Resultado desejado
### Atores e interesses
### Evidências e fatos observados
### Hipóteses
### Perguntas em aberto
### Escopo
### Fora do escopo
### Critérios de sucesso

## Restrições aplicáveis

## Classificação comentada

## Decisão de roteamento

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|

## Alternativas consideradas

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|

## Histórico e decisão atual

### Decisão da versão anterior
### Decisão recomendada nesta versão
### Impacto da revisão

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|

## Riscos e efeitos de segunda ordem

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|

## Handoffs e atividades posteriores

## Síntese
```

## Regras

- A saída deve revelar quando arquivos sustentaram a análise e distinguir objeto principal de apoio.
- Não alegue análise de conteúdo quando `analysis_scope: metadata-only` ou `availability: unavailable`.
- Uma revisão deve ser compreensível isoladamente sem esconder linhagem ou mudança nos arquivos.
- Solicitação, complementos, interpretações e conteúdo observado permanecem distinguíveis.
- O roteamento faz parte da rastreabilidade.
- `status: proposed` exige aprovação humana; `pending` indica evidência material ausente.
