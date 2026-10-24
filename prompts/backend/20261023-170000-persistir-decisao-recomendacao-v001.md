---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-23T17:00:00-03:00"
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
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "códigos e severidades das pendências (por busca de linhas)"
      content_state: commit
      revision: "d1df2ab"
      availability: partial
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "CurriculoRegistro e CurriculoItemRegistro (linhas 1-160)"
      content_state: commit
      revision: "d1df2ab"
      availability: partial
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_documento.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d1df2ab"
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261017_0015_adicionar_ordem_secoes_curriculos.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d1df2ab"
      availability: available
    - path: "GitHub issue #227 (F6.7)"
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
      revision: "d1df2ab"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d1df2ab"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "Decide como persistir a decisão do estudante sobre recomendações da revisão, na linhagem de revisão de currículo de prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, data]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: low
---

# Análise de decisão — persistência da decisão sobre recomendações

## Solicitação original

```text
[F6.7] Persistir a decisão de aceitar ou rejeitar uma recomendação com data técnica.
WBS: 1.4.3., 1.4.4. — Início: 2026-10-26 — Entrega: 2026-11-01
Responsável único: @regazzio
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Modo de trabalho pedido: a assistente escreve os arquivos e o usuário faz os commits.
- A rota que expõe a decisão é o card F6.8 (#228), que depende desta persistência.
- Esta análise é independente das anteriores e não as revisa.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `d1df2ab` (cabeça da `dev` na consulta).
- O corpo da issue #227 repete o título; **não está confirmado** se a decisão vale por versão de currículo ou por estudante, nem se "data técnica" exige UTC.
- A migration não foi executada contra banco real; os testes simulam as operações do Alembic.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

O estudante pode aceitar ou rejeitar cada recomendação (aviso) da revisão de uma versão, e a escolha, com a data e hora técnicas, fica gravada e pode ser lida depois.

### Evidências e fatos observados

1. As recomendações são as pendências de severidade `aviso` da revisão, identificadas por um código estável (`PROJETO_AUSENTE`, `IDIOMA_AUSENTE`, `CIDADE_AUSENTE`, `LINK_PROFISSIONAL_AUSENTE`).
2. Não há tabela nem entidade para decisões do estudante.
3. A exclusão de versão remove primeiro as linhas de `curriculo_itens` e depois a versão; qualquer nova tabela que referencie `curriculos` não pode travar essa exclusão.
4. A última migration é a `20261017_0015`; nenhuma outra foi aberta depois dela.
5. Os adapters existentes gravam e leem por sessão externa com `flush`, sem commit.

### Hipóteses

- **H1.** A decisão pertence a **uma versão de currículo**, e há uma única decisão por par versão e código; decidir de novo substitui a anterior.
- **H2.** Domínio: enumeração `DecisaoEstudante` (`aceita`, `rejeitada`) e value object `DecisaoRecomendacao` (versão, código, decisão e instante com fuso).
- **H3.** Tabela `decisoes_recomendacao`, com chave primária composta (versão e código), decisão em texto, instante com fuso e chave estrangeira para `curriculos` com `ON DELETE CASCADE`, para que excluir a versão não deixe decisões órfãs nem exija mudança no repositório de currículos.
- **H4.** Porta `RepositorioDecisaoRecomendacao` com `salvar` (substitui) e `listar_por_curriculo`.
- **H5.** O instante é o momento técnico informado por quem orquestra, exigido com fuso; um instante sem fuso lido do banco é tratado como UTC.
- **H6.** Que só avisos podem ser decididos (e que o código existe na revisão) é regra do caso de uso da F6.8, e não desta persistência.

### Perguntas em aberto

1. A decisão deve valer por versão de currículo (H1) ou por estudante?
2. Aceitar uma recomendação deve alterar o currículo, ou só registrar a escolha?
3. A data técnica deve ser sempre UTC e gerada pelo servidor?

### Escopo

- Domínio, porta, tabela, migration, mapeamento, repositório SQLAlchemy e testes.

### Fora do escopo

- Caso de uso e rota (F6.8); validação de que o código é um aviso vigente; efeito da decisão na revisão.

### Critérios de sucesso

- Uma decisão por versão e código, substituída ao decidir de novo.
- A decisão e o instante com fuso voltam iguais à leitura.
- Excluir a versão remove suas decisões (cascata).
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Mapeamento ORM na infraestrutura e schema por migration versionada; domínio sem dependência de banco (`src/backend/AGENTS.md`).
- Docstring e proveniência em todo trecho novo.

## Classificação comentada

- `uncertainty: medium`: o card não define o escopo da decisão.
- `reversibility: moderate`: a migration é reversível, mas o rollback descarta as decisões gravadas.
- `risk: low`: tabela nova e aditiva.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | 1 | Uma decisão por par; nada órfão | Evita duplicidade e travar a exclusão |
| `simplicity` | 1 | Revisável em cerca de 10 minutos | Critério de aceite |
| `modifiability` | 2 | A F6.8 usa a porta sem mudar o schema | Ela depende desta entrega |

## Alternativas consideradas

**Estado atual.** A revisão não guarda o que o estudante decidiu.

**Alternativa A — Tabela própria com chave composta e cascata (recomendada).**

**Alternativa B — Coluna JSON em `curriculos` com as decisões.** Menos tabelas, mas altera a tabela existente, dificulta consultas e mistura dados.

**Alternativa C — Tabela com chave própria (UUID) e índice único em versão e código.** Permite identificar a decisão, mas acrescenta um identificador sem uso.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | 1 | +1 | 0 | +1 | média | A chave composta impõe a unicidade |
| `simplicity` | 1 | +1 | 0 | 0 | média | C acrescenta identificador sem uso |
| `modifiability` | 2 | +1 | -1 | 0 | baixa | B altera uma tabela já em uso |

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
| `correctness` | prioritized | Uma decisão por par e sem órfãos | Chave composta e `ON DELETE CASCADE` |
| `simplicity` | prioritized | Tabela aditiva e porta pequena | Sem alterar `curriculos` |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `modifiability` | A F6.8 sem mudar o schema | A porta já oferece salvar e listar |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | Decisões duplicadas ou exclusão de versão bloqueada | Média | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | Sem histórico de decisões anteriores (a nova substitui) | `user-value` | Aceitável: o card pede a decisão vigente |

## Riscos e efeitos de segunda ordem

- **Migration não executada contra banco real.** Mitigação: conferir `alembic upgrade head` e `downgrade -1` em ambiente de teste.
- **Duas migrations com o mesmo pai.** Conferir cabeças múltiplas antes do PR.
- **Cascata só no banco.** Em bancos que não impõem chaves estrangeiras por padrão (como o SQLite dos testes), a cascata não age; o PostgreSQL de produção a aplica.
- **Escopo da decisão por versão.** Se for por estudante, o schema muda; pergunta 1.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Valores válidos e instante com fuso | Recusa de valor inválido | Testes de domínio | Valor aceito |
| Tabela e migration coincidem | Colunas, chave e cascata iguais | Testes de metadata e migration | Divergência |
| Uma decisão por par | Atualização em vez de nova linha | Testes do repositório | Linha duplicada |
| Dado corrompido falha alto | `ValueError` ou violação de domínio | Testes de mapeamento | Leitura silenciosa |

## Handoffs e atividades posteriores

- **F6.8 (#228):** caso de uso e rota para registrar e consultar a decisão, validando que o código é um aviso da revisão e a propriedade da versão.

## Síntese

A revisão apontava recomendações, mas não havia onde guardar o que o estudante decidiu. A decisão cria o value object e a tabela `decisoes_recomendacao`, com uma decisão por versão e código, instante com fuso e cascata na exclusão da versão, além de porta e repositório para gravar e listar. A principal incerteza é se a decisão vale por versão ou por estudante.
