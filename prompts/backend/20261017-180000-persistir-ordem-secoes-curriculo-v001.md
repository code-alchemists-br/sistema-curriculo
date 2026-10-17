---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-17T18:00:00-03:00"
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
      revision: "2d3a929"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "registro CurriculoRegistro e mapeadores (linhas 1-110)"
      content_state: commit
      revision: "2d3a929"
      availability: partial
    - path: src/backend/infrastructure/persistence/alembic/versions/20261017_0014_exclusao_logica_experiencias_profissionais.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "2d3a929"
      availability: available
    - path: src/backend/domain/secao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "2d3a929"
      availability: available
    - path: src/backend/tests/test_infrastructure_curriculo_mapping.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "2d3a929"
      availability: available
    - path: "GitHub issue #211 (F5.3)"
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
      revision: "2d3a929"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "2d3a929"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "Decide como o agregado de currículo e a persistência guardam a ordem explícita das seções, na linhagem de versões de currículo de prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, data, delivery]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: low
---

# Análise de decisão — persistência da ordem explícita das seções do currículo

## Solicitação original

```text
[F5.3] Persistir a ordem explícita das seções no currículo e cobrir o mapeamento.
WBS: 1.4.1., 1.4.2. — Início: 2026-10-19 — Entrega: 2026-10-25
Responsável único: @regazzio
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Modo de trabalho pedido: a assistente escreve os arquivos e o usuário faz os commits.
- Esta análise é independente das anteriores e não as revisa. Ela usa `SecaoCurriculo` e `ORDEM_PADRAO_SECOES`, definidos pela análise `20261017-100000-secoes-curriculo-ordem-padrao-v001.md`.
- A task F5.4 (#212), que expõe a atualização da ordem, depende desta.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `2d3a929` (cabeça da `dev` na consulta).
- O corpo da issue #211 foi visto somente pelo texto colado pelo usuário.
- O comportamento da migration contra um banco real **não foi executado**; os testes simulam as operações do Alembic.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

Cada versão de currículo guarda a ordem em que suas seções são apresentadas; versões novas e já existentes têm a ordem padrão até alguém definir outra, e a ordem sobrevive à gravação e à leitura.

### Evidências e fatos observados

1. O agregado `Curriculo` não tem conceito de ordem de seções; a ordem padrão existe só como constante (`secao_curriculo.py`).
2. A tabela `curriculos` tem as colunas `id`, `usuario_id`, `titulo_versao`, `layout` e `is_public`; a última migration é a `20261017_0014`.
3. O teste do mapeamento da tabela compara as colunas da migration de criação com a metadata atual, o que passa a divergir ao acrescentar uma coluna.
4. Os testes de repositório usam registros simulados com as colunas lidas pelo mapeador.
5. As migrations anteriores adicionam colunas com `op.add_column`, testadas por simulação das operações.

### Hipóteses

- **H1.** O agregado ganha `ordem_secoes: tuple[SecaoCurriculo, ...]`, com a ordem padrão como valor inicial, e a invariante de conter cada seção exatamente uma vez.
- **H2.** O agregado ganha `definir_ordem_secoes`, que valida antes de aplicar; a rota que a expõe é a F5.4 (#212).
- **H3.** A ordem é gravada em **uma coluna de texto** `ordem_secoes` em `curriculos`, com os identificadores separados por vírgula, portável entre PostgreSQL e SQLite dos testes.
- **H4.** A coluna é não nula e tem valor padrão no servidor igual à ordem padrão, de modo que as versões existentes a recebem sem etapa de preenchimento.
- **H5.** A migration congela o texto da ordem padrão; o modelo ORM o calcula a partir do domínio, e um teste garante que os dois coincidem.
- **H6.** Texto desconhecido ou ordem incompleta no banco falham alto (`ValueError` ou violação de domínio), em vez de serem ignorados.

### Perguntas em aberto

1. Uma tabela própria de seções seria preferível a uma coluna de texto (por exemplo, para consultas por seção)?
2. Se a ordem padrão mudar no futuro, as versões já gravadas devem manter a ordem antiga (comportamento atual) ou migrar?
3. A ordem deve poder omitir seções vazias ou ocultar seções?

### Escopo

- Domínio: campo, invariante e `definir_ordem_secoes`.
- Infraestrutura: coluna, migration, mapeadores de criação, leitura e atualização.
- Testes de domínio e de mapeamento; ajuste dos testes que descreviam as colunas anteriores.

### Fora do escopo

- Rota ou caso de uso para alterar a ordem (F5.4, #212).
- Ocultar seções; aplicar a ordem na prévia ou na exportação.

### Critérios de sucesso

- Versão nova e versão antiga têm a ordem padrão; uma ordem definida é gravada e lida igual.
- Ordem inválida é recusada pelo domínio e não altera o agregado.
- A coluna e a migration coincidem e a migration é reversível.
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Mapeamentos ORM ficam na infraestrutura e o schema muda por migrations versionadas (`src/backend/AGENTS.md`).
- Invariantes ficam no domínio; docstring e proveniência em todo trecho novo.

## Classificação comentada

- `uncertainty: medium`: a migration não foi executada contra banco real.
- `reversibility: moderate`: a migration é reversível, mas o rollback descarta ordens personalizadas.
- `risk: low`: coluna aditiva com valor padrão.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `simplicity` | 1 | Revisável em 10 minutos | Critério de aceite |
| `correctness` | 1 | Ordem sempre completa e sem repetição | Evita seção perdida ao exportar |
| `modifiability` | 2 | Poder evoluir para outra forma de guardar a ordem | A F5.4 e futuras tasks dependem |

## Alternativas consideradas

**Estado atual.** O currículo não guarda ordem de seções.

**Alternativa A — Coluna de texto `ordem_secoes` em `curriculos` (recomendada).** Uma coluna aditiva, sem tabela nova.

**Alternativa B — Tabela própria de ordem (uma linha por seção).** Permite consultas por seção e posições, mas exige tabela, chave composta, sincronização e mais testes.

**Alternativa C — Coluna JSON/ARRAY.** Mais expressiva, mas depende de tipos específicos do banco e dificulta os testes com SQLite.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `simplicity` | 1 | +1 | -2 | 0 | média | B exige tabela e sincronização |
| `correctness` | 1 | +1 | +1 | +1 | média | A validação fica no domínio nas três |
| `modifiability` | 2 | 0 | +1 | 0 | baixa | B permite consultas por seção |

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
| `simplicity` | prioritized | Uma coluna aditiva | Sem tabela nem sincronização |
| `correctness` | prioritized | Ordem sempre válida | Invariante no agregado e falha alta na leitura |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `modifiability` | Poder trocar a forma de guardar | O mapeamento está isolado em duas funções |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | Currículo exportado sem uma seção ou com seção duplicada | Média | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | Sem consulta SQL por seção; ordem guardada como texto | `modifiability` | Aceitável: nenhuma consulta por seção é prevista |

## Riscos e efeitos de segunda ordem

- **Migration não executada contra banco real.** Mitigação: o valor padrão no servidor evita etapa de preenchimento; conferir `alembic upgrade head` em ambiente de teste antes do deploy.
- **Duas migrations com o mesmo pai.** Outra task pode abrir uma migration depois da `0014`; conferir cabeças múltiplas antes do PR.
- **Ordem padrão mudar.** Versões já gravadas mantêm a ordem antiga; pergunta 2 registrada.
- **Conflitos de integração.** Alterações em `domain/curriculo.py` e nos mapeadores podem conflitar com tarefas paralelas.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Ordem inválida é recusada | Violação de domínio sem alterar o agregado | Teste de domínio | Ordem inválida aceita |
| Ordem sobrevive à gravação e à leitura | Mesma ordem nos dois sentidos | Testes de mapeamento | Ordem diferente |
| Coluna e migration coincidem | Tipo, obrigatoriedade e padrão iguais | Teste da metadata e da migration | Divergência |
| Dado corrompido falha alto | `ValueError` ou violação de domínio | Testes de mapeamento | Leitura silenciosa |

## Handoffs e atividades posteriores

- **F5.4 (#212):** caso de uso e rota para alterar a ordem, usando `definir_ordem_secoes`.
- **Ambiente de teste:** aplicar `alembic upgrade head` e `downgrade -1` para conferir a migration.

## Síntese

O currículo não guardava a ordem de apresentação das seções. A decisão faz o agregado manter uma ordem completa e sem repetição, com a ordem padrão como início, e a grava numa coluna de texto aditiva em `curriculos`, com valor padrão que cobre as versões existentes. A rota para alterar a ordem fica para a F5.4. A principal incerteza é que a migration não foi executada contra um banco real.
