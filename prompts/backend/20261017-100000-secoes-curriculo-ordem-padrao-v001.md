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
  decision_impact: initial
subjects:
  kind: mixed
  files:
    - path: src/backend/domain/revisao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "enumeração SecaoRevisao e ordem das seções (por busca de linhas)"
      content_state: commit
      revision: "6f3a032e1dca9869cc5c75c7079001a818bb9c43"
      availability: partial
    - path: src/backend/domain/value_objects.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "classe ReferenciaCurriculo e tipos de item permitidos (por busca de linhas)"
      content_state: commit
      revision: "6f3a032e1dca9869cc5c75c7079001a818bb9c43"
      availability: partial
    - path: src/backend/domain/__init__.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "6f3a032e1dca9869cc5c75c7079001a818bb9c43"
      availability: available
    - path: docs/wireframes/08-visualizacao-curriculo.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "6f3a032e1dca9869cc5c75c7079001a818bb9c43"
      availability: available
    - path: "GitHub issue #209 (F5.1)"
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
  rationale: "Decide uma peça de domínio do backend (vocabulário e ordem de seções do currículo), na linhagem de versões de currículo de prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, delivery]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: low
---

# Análise de decisão — seções do currículo e ordem padrão

## Solicitação original

```text
Descrição: Definir enumeração de seções suportadas pelo currículo e ordem padrão.
WBS: 1.4.1., 1.4.2. — Início: 2026-10-19 — Entrega: 2026-10-25
Responsável único: @regazzio
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Modo de trabalho pedido: a assistente escreve os arquivos e o usuário faz os commits.
- A task é a base de F5.3 (#211, persistir a ordem das seções) e F5.4 (#212, expor a atualização da ordem).
- Esta análise é independente das anteriores e não as revisa.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `6f3a032e1dca9869cc5c75c7079001a818bb9c43` (cabeça da `dev` na consulta), lido por `git show origin/dev:<caminho>`.
- O corpo da issue #209 foi visto somente pelo texto colado pelo usuário; as issues #211, #212 e #213 foram vistas só pelo título.
- Os modelos de currículo (F5.6 e F5.7) não foram lidos; a ordem aqui proposta não foi validada com quem os define.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

Existir, no domínio, um vocabulário fechado das seções que um currículo pode apresentar e uma ordem padrão, para que persistência (#211), atualização de ordem (#212) e consulta (#213) compartilhem a mesma definição.

### Atores e interesses

- **Estudante:** ver o currículo numa ordem previsível.
- **Equipe de backend e front-end:** um único vocabulário de seções.
- **Responsáveis pelos modelos (F5.6 e F5.7):** poder opinar na ordem padrão.

### Evidências e fatos observados

1. Já existe `SecaoRevisao` com seis seções (dados pessoais, formação, experiências, competências, projetos, idiomas), cujos valores textuais coincidem com os do front-end (`revisao_curriculo.py`).
2. `ReferenciaCurriculo` aceita apenas seis tipos de item: formação, experiência, projeto, competência, idioma e documento (`value_objects.py`).
3. A prévia já agrupa o conteúdo por seção, incluindo documentos (`previa_versao_curriculo.py`).
4. O wireframe 08 apresenta identificação, formação, experiência e habilidades e demais informações complementares (`08-visualizacao-curriculo.md`).
5. `Curriculo.layout` é texto livre; não há ainda conceito de ordem de seções no agregado.

### Hipóteses

- **H1.** Criar um tipo novo, `SecaoCurriculo`, sem alterar `SecaoRevisao`, para não mudar a ordem nem os testes da revisão.
- **H2.** Incluir `DOCUMENTOS_COMPLEMENTARES`, por ser tipo de referência válido e já ter seção na prévia.
- **H3.** A ordem padrão é uma tupla explícita: dados pessoais, formação, experiências, projetos, competências, idiomas, documentos.
- **H4.** Cursos, certificações e links ficam fora até o `Curriculo` aceitar referências desses tipos.
- **H5.** Os valores textuais seguem o formato já usado (`kebab-case` sem acento), porque serão persistidos e expostos.

### Perguntas em aberto

1. A ordem padrão (projetos antes de competências) está de acordo com os modelos de F5.6 e F5.7?
2. Documentos complementares devem ser seção apresentada no currículo ou apenas anexo?
3. A `SecaoRevisao` deve ser unificada com `SecaoCurriculo` em task futura, ajustando a ordem da revisão?

### Escopo

- Enumeração `SecaoCurriculo` e constante `ORDEM_PADRAO_SECOES` no domínio, exportadas por `backend.domain`.
- Testes unitários de identificadores, ordem, cobertura, imutabilidade e conversão.

### Fora do escopo

- Persistir a ordem (#211), expor sua atualização (#212) e a consulta (#213).
- Validar permutações de ordem personalizada; unificar com `SecaoRevisao`.
- Seções de curso, certificação e link.

### Critérios de sucesso

- Cada seção tem identificador textual estável.
- A ordem padrão contém cada seção uma única vez.
- Uma seção nova no Enum sem entrar na ordem padrão faz um teste falhar.
- Os valores de `SecaoRevisao` pertencem ao vocabulário de `SecaoCurriculo`.
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Domain não depende de Application, Infrastructure, API ou frameworks (`src/backend/AGENTS.md`).
- Docstring (o que faz, como faz, finalidade) em toda classe e função (`AGENTS.md`).
- Testes unitários independentes de banco, rede e framework.
- Proveniência em todo trecho novo.

## Classificação comentada

- `uncertainty: medium`: a ordem e a inclusão de documentos dependem dos modelos ainda não lidos.
- `reversibility: easy` e `risk: low`: peça pequena, sem persistência nem migration.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `simplicity` | 1 | Só domínio, sem banco nem rota | Cabe numa revisão de 10 minutos |
| `modifiability` | 1 | Mudar a ordem padrão em um único ponto | #211, #212 e #213 dependem dela |
| `correctness` | 2 | Sem seção omitida ou repetida | Evita currículo com seção perdida |

## Alternativas consideradas

**Estado atual.** Só existe `SecaoRevisao`, ligada à revisão; não há vocabulário de seções do currículo nem ordem padrão.

**Alternativa A — Tipo novo `SecaoCurriculo` e tupla de ordem explícita (recomendada).** Não altera a revisão; a ordem é decisão visível.

**Alternativa B — Reaproveitar `SecaoRevisao` como vocabulário do currículo.** Evita duplicação, mas mistura a revisão com a apresentação e obrigaria a mudar a ordem da revisão e seus testes.

**Alternativa C — Usar a ordem de declaração do Enum como ordem padrão.** Menos código, mas reordenar a apresentação viraria efeito colateral de mexer na declaração.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `simplicity` | 1 | +1 | +1 | +1 | média | As três são pequenas |
| `modifiability` | 1 | +1 | -1 | 0 | média | B acopla revisão e apresentação |
| `correctness` | 2 | +1 | 0 | 0 | média | A tem teste de cobertura da ordem |

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
| `simplicity` | prioritized | Uma enumeração e uma tupla | Sem camadas adicionais |
| `modifiability` | prioritized | Ordem alterada em um ponto | Tupla explícita |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `correctness` | Sem omissão nem repetição | Teste compara a ordem ao conjunto da enumeração |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `modifiability` | Cada card de F5 redefine suas seções | Média | Equipe de backend |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | Duas enumerações de seção convivem (`SecaoRevisao` e `SecaoCurriculo`) | `modifiability` | Aceitável: um teste garante a coerência dos valores |

## Riscos e efeitos de segunda ordem

- **Ordem divergente entre revisão e currículo.** A revisão põe competências antes de projetos; a ordem padrão põe projetos antes. Mitigação: pergunta 3 registrada.
- **Ordem padrão contestada pelos modelos.** Mitigação: a tupla é um único ponto de alteração.
- **Conflitos de integração.** Alterações em `domain/__init__.py` costumam conflitar com outras tarefas; resolver ao integrar a `dev`.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Identificadores estáveis | Mapa completo igual ao esperado | Teste de domínio | Valor renomeado |
| Ordem sem omissão nem repetição | Conjunto igual ao Enum | Teste de domínio | Seção ausente na ordem |
| Coerência com a revisão | Valores de `SecaoRevisao` contidos em `SecaoCurriculo` | Teste de domínio | Divergência de vocabulário |

## Handoffs e atividades posteriores

- **`$backend-domain-orchestration-v2`:** #211 e #212 usarão `SecaoCurriculo` e `ORDEM_PADRAO_SECOES` para persistir e atualizar a ordem; validar permutações de ordem personalizada ao expor a atualização.
- **Modelos (F5.6 e F5.7):** confirmar a ordem padrão e a seção de documentos.

## Síntese

O backend não tem um vocabulário das seções do currículo nem uma ordem padrão, e as próximas tasks de F5 precisam dos dois. A decisão cria `SecaoCurriculo` e `ORDEM_PADRAO_SECOES` no domínio, sem tocar a revisão, com testes que impedem seção omitida ou repetida. As incertezas são a ordem exata e a seção de documentos, ainda não confirmadas com os modelos.
