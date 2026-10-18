---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-17T14:00:00-03:00"
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
    - path: src/backend/domain/curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d688812"
      availability: available
    - path: src/backend/api/versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "DTOs de edição e criação e handler PUT (linhas 1-200)"
      content_state: commit
      revision: "d688812"
      availability: partial
    - path: src/backend/application/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "caso de uso de edição (por busca de linhas)"
      content_state: commit
      revision: "d688812"
      availability: partial
    - path: src/frontend/features/alternar-modelo-curriculo/ui/AlternadorModeloCurriculo.tsx
      relationship: supporting
      representation: source-code
      function: production
      format: typescript
      analysis_scope: selected-section
      locator: "tipo ModeloApresentacaoCurriculo e opções (linhas 1-30)"
      content_state: commit
      revision: "d688812"
      availability: partial
    - path: "GitHub issue #216 (F5.8)"
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
      revision: "d688812"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d688812"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "Decide o vocabulário de modelos e a recusa de modelo desconhecido na edição da versão, na linhagem de versões de currículo de prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, user-experience]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: low
---

# Análise de decisão — modelo do currículo na edição da versão

## Solicitação original

```text
[F5.8] Expor seleção do modelo na edição da versão e rejeitar modelo desconhecido.
WBS: 1.4.1., 1.4.2. — Início: 2026-10-19 — Entrega: 2026-10-25
Responsável único: @regazzio
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Modo de trabalho pedido: a assistente escreve os arquivos e o usuário faz os commits.
- Esta análise é independente das anteriores e não as revisa.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `d688812` (cabeça da `dev` na consulta), lido do disco e por `git show origin/dev:<caminho>`.
- O corpo da issue #216 foi visto somente pelo texto colado pelo usuário; os cards dos modelos (F5.6 e F5.7) não foram lidos.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

A edição da versão permite escolher o modelo de apresentação entre os modelos suportados e recusa qualquer outro, e a API publica quais são.

### Evidências e fatos observados

1. `Curriculo.layout` é texto livre; o agregado "deixa layout como texto porque seus valores ainda não foram definidos" (`curriculo.py`).
2. A API valida apenas presença e tamanho (1 a 100 caracteres) de `layout` na criação e na edição (`api/versao_curriculo.py`).
3. O front-end oferece dois modelos, `classico` e `compacto`, no tipo `ModeloApresentacaoCurriculo` (`AlternadorModeloCurriculo.tsx`).
4. A violação de domínio na edição já é traduzida para HTTP 422 pela rota.
5. Vários testes existentes editam a versão com o texto `moderno`, que não é um modelo existente; um teste constrói versão com `padrao` e a fixture de exportação usa `padrao_fatec`.
6. O adaptador de persistência reconstitui o agregado a partir do banco por construção direta.

### Hipóteses

- **H1.** Os modelos suportados são exatamente `classico` e `compacto`, o vocabulário já presente no front-end.
- **H2.** Enumeração `ModeloCurriculo` no domínio, validada em `Curriculo.editar_versao`, que recusa modelo desconhecido com `RegraDeDominioViolada` (422).
- **H3.** A validação vale somente para a **edição**: construir ou reconstituir uma versão com outro texto continua permitido, para não quebrar versões já gravadas nem a criação.
- **H4.** O DTO de edição tipa `layout` com a enumeração, de modo que a fronteira recusa o valor (422) e o OpenAPI lista os modelos aceitos; a Application continua recebendo texto simples.
- **H5.** O campo permanece chamado `layout`, para não alterar o contrato existente.
- **H6.** Os testes que editavam com `moderno` passam a usar `compacto`.

### Perguntas em aberto

1. A criação da versão também deve recusar modelo desconhecido? (Hoje não; ver H3.)
2. Os modelos suportados são só `classico` e `compacto`, ou haverá outros (F5.6 e F5.7)?
3. O campo deve ser renomeado para `modelo` em contrato futuro?

### Escopo

- Domínio: `ModeloCurriculo`, validação em `editar_versao` e exportação.
- API: tipo do campo `layout` no corpo da edição.
- Testes novos e ajuste de `moderno` para `compacto` nos testes de edição.

### Fora do escopo

- Validar o modelo na criação; migração de versões já gravadas; renomear o campo; mudar a prévia ou a exportação.

### Critérios de sucesso

- A edição aceita `classico` e `compacto` e recusa qualquer outro texto sem alterar a versão.
- O corpo da API recusa modelo desconhecido e o OpenAPI lista os modelos.
- Versões já existentes com outro texto continuam carregáveis.
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Invariantes ficam no domínio; formato e tipo são validados na fronteira (`src/backend/AGENTS.md`).
- Docstring (o que faz, como faz, finalidade) e proveniência em todo trecho novo.

## Classificação comentada

- `uncertainty: medium`: o conjunto de modelos depende de F5.6 e F5.7, não lidos.
- `reversibility: easy` e `risk: low`: mudança pequena, sem migration.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | 1 | Modelo desconhecido nunca é gravado pela edição | Evita versão que o sistema não sabe apresentar |
| `simplicity` | 1 | Mudança revisável em 10 minutos | Critério de aceite da issue |
| `modifiability` | 2 | Novo modelo adicionado em um único ponto | Os modelos podem crescer |

## Alternativas consideradas

**Estado atual.** O modelo é texto livre e qualquer valor é aceito.

**Alternativa A — Enumeração no domínio, validação na edição e tipo no DTO (recomendada).** A regra fica no domínio; a fronteira recusa cedo e documenta os valores.

**Alternativa B — Validar apenas no DTO da API.** Menos código, mas a regra de negócio fica na fronteira e não protege outros chamadores do domínio.

**Alternativa C — Validar também na construção do agregado.** Cobre a criação, mas quebra a reconstituição de versões já gravadas e vários testes.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | 1 | +1 | 0 | +1 | média | B não protege o domínio; C protege também a criação |
| `simplicity` | 1 | +1 | +1 | -1 | média | C afeta construção e reconstituição |
| `modifiability` | 2 | +1 | -1 | +1 | média | Em B a regra fica fora do domínio |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**. Status `proposed`: aprovação humana, em especial sobre as perguntas 1 e 2.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | prioritized | Edição só com modelos suportados | Testes de domínio e do DTO |
| `simplicity` | prioritized | Uma enumeração e uma validação | Sem migration nem mudança de contrato de campo |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `modifiability` | Novo modelo em um ponto | Basta acrescentar o valor à enumeração |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | Versões com modelo inexistente que o front não renderiza | Média | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | A criação ainda aceita modelo livre | `correctness` | Aceitável: pergunta 1 registrada para decisão do time |

## Riscos e efeitos de segunda ordem

- **Cliente que enviava outro texto na edição.** Passa a receber 422. Mitigação: o front só oferece `classico` e `compacto`.
- **Modelos novos.** Exigem acrescentar o valor à enumeração e coordenar com o front-end.
- **Conflitos de integração.** Alterações em `domain/__init__.py` costumam conflitar com outras tarefas; resolver ao integrar a `dev`.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Edição aceita os modelos suportados | Modelo gravado | Teste de domínio | Falha indevida |
| Modelo desconhecido recusado sem alterar | `RegraDeDominioViolada` e estado intacto | Teste de domínio | Estado alterado |
| Fronteira recusa e documenta | `ValidationError` e enumeração no OpenAPI | Testes da API | Valor aceito ou ausente do esquema |
| Versões antigas carregam | Construção com outro texto | Teste de domínio | Falha ao construir |

## Handoffs e atividades posteriores

- **Decisão do time:** pergunta 1 (criação) e pergunta 2 (conjunto de modelos).
- **Front-end:** enviar `classico` ou `compacto` e tratar o 422.

## Síntese

O modelo do currículo era texto livre e qualquer valor era aceito na edição. A decisão cria o vocabulário `ModeloCurriculo` (clássico e compacto), faz o domínio recusar na edição qualquer outro e tipa o corpo da API para recusar cedo e publicar os modelos no OpenAPI, sem migration e preservando versões já gravadas. A criação fica de fora por decisão do time.
