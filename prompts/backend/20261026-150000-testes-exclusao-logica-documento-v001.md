---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-26T15:00:00-03:00"
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
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_documento.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d023070"
      availability: available
    - path: src/backend/application/exclusao_documento.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d023070"
      availability: available
    - path: src/backend/application/download_documento.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d023070"
      availability: available
    - path: src/backend/tests/test_integracao_crud_informacoes_complementares.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: selected-section
      locator: "doubles de sessão e repositório de documento e teste de exclusão alheia (por busca de linhas)"
      content_state: commit
      revision: "d023070"
      availability: partial
    - path: "GitHub issue #206 (F4.16)"
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
      revision: "d023070"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d023070"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "Cobre com testes a exclusão lógica de documentos complementares já implementada, na linhagem de documentos de prompts/backend."
classification:
  sphere: engineering
  concerns: [security, quality]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: low
  reversibility: easy
  risk: low
---

# Análise de decisão — testes da exclusão lógica e do isolamento de documentos

## Solicitação original

```text
[F4.16] Aplicar exclusão lógica do documento complementar e testar que outro estudante não o acessa.
WBS: 1.3.2.3, 1.3.3.1–1.3.3.4 — Início: 2026-10-19 — Entrega: 2026-10-25
Responsável único: @mariacarolinayamamoto
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Modo de trabalho pedido: a assistente escreve os arquivos e o usuário faz os commits.
- O card é de outra pessoa do grupo; o usuário o assumiu com a comunicação ao grupo por conta dele.
- Esta análise é independente das anteriores e não as revisa.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `d023070` (cabeça da `dev` na consulta).
- O corpo da issue #206 repete o título e não traz critérios.
- Os testes do repositório usam sessão substituída: o SQL é inspecionado, **não executado** contra banco real.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

Comprovar por testes que a exclusão lógica de documentos complementares funciona em todas as camadas e que um estudante nunca acessa nem remove o documento de outro.

### Evidências e fatos observados

1. A exclusão lógica já existe: rota `DELETE /documentos/{id}`, caso de uso `ExcluirDocumento` e o adapter, que faz `UPDATE … SET deleted_at` somente em registros ainda ativos.
2. Os testes do caso de uso e da rota cobrem exclusão de documento alheio e inexistente (404), e há um teste de integração de exclusão alheia.
3. Nenhum teste da suíte exercita `RepositorioDocumentoSqlAlchemy`: o filtro de documento ativo e o UPDATE de exclusão não eram verificados.
4. O download de documento (`BaixarDocumento`) recusa documento excluído, alheio ou inexistente.
5. Não havia cenário que combinasse duas sessões e provasse, de ponta a ponta, que após a exclusão ninguém baixa o arquivo.

### Hipóteses

- **H1.** O código de produção já cumpre o card; falta cobertura de testes no adapter e no fluxo de ponta a ponta.
- **H2.** Testar o adapter com sessão substituída e inspeção do SQL gerado (UPDATE, condição de ativo e instante com fuso) é suficiente em testes unitários.
- **H3.** Um teste com a aplicação ASGI, o middleware de sessão de dois estudantes e os casos de uso reais prova o isolamento e o efeito da exclusão.

### Perguntas em aberto

1. A exclusão lógica deve também remover o arquivo físico do storage, ou mantê-lo para recuperação?
2. Há prazo de retenção para documentos excluídos logicamente?

### Escopo

- Testes do repositório SQLAlchemy de documentos e do isolamento de ponta a ponta entre dois estudantes.

### Fora do escopo

- Mudar o código de produção; remoção do arquivo físico; purga de registros excluídos.

### Critérios de sucesso

- O adapter grava, lê só documento ativo e exclui por UPDATE de `deleted_at`, sem DELETE e sem reexcluir.
- Outro estudante recebe 404 ao baixar e ao excluir, e o documento continua disponível ao dono.
- Depois da exclusão, ninguém baixa o documento; excluir duas vezes dá 404 na segunda.
- Sem sessão, 401. A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Testes unitários com doubles; docstring e proveniência em todo trecho novo (`AGENTS.md`).

## Classificação comentada

- `uncertainty: low` e `risk: low`: só acrescenta testes, sem alterar código de produção.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `security` | 1 | Isolamento entre estudantes comprovado | Dado pessoal do estudante |
| `simplicity` | 1 | Só testes, revisáveis em cerca de 10 minutos | Critério de aceite |

## Alternativas consideradas

**Estado atual.** A lógica existe, mas o adapter e o fluxo completo não têm testes.

**Alternativa A — Testes do adapter com sessão substituída e teste de ponta a ponta com dois estudantes (recomendada).**

**Alternativa B — Testes com banco real (SQLite em memória).** Verificam o SQL de verdade, mas exigem montar o schema e ficam mais lentos; cabem a uma suíte de integração.

**Alternativa C — Não acrescentar testes e fechar o card.** Zero custo, mas deixa o adapter sem verificação.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `security` | 1 | +1 | +1 | -1 | média | C não prova o isolamento de ponta a ponta |
| `simplicity` | 1 | +1 | -1 | +1 | média | B exige schema e banco |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada nesta linhagem.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**. Status `proposed`: aprovação humana.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `security` | prioritized | Isolamento provado com duas sessões | Testes de ponta a ponta |
| `simplicity` | prioritized | Sem mudar código de produção | Só arquivos de teste |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `quality` | Adapter coberto | Testes do SQL gerado e do instante de exclusão |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `security` | Regressão silenciosa no filtro de documento ativo | Média | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | SQL inspecionado, não executado em banco | Fidelidade | Aceitável: banco real fica para a suíte de integração |

## Riscos e efeitos de segunda ordem

- **Testes acoplados ao texto do SQL.** Mitigação: as asserções checam só as condições essenciais (tabela, `deleted_at IS NULL`).
- **Importação entre arquivos de teste.** O cenário reaproveita doubles do teste de integração existente; mudar aquele arquivo pode exigir ajuste aqui.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| O adapter exclui logicamente | UPDATE de `deleted_at`, sem DELETE | Teste com sessão substituída | Outra instrução |
| Só o ativo é lido | `deleted_at IS NULL` na consulta | Teste com sessão substituída | Filtro ausente |
| Isolamento | 404 ao baixar e ao excluir pelo outro estudante | Teste de ponta a ponta | Status diferente |
| Efeito da exclusão | Ninguém baixa após excluir | Teste de ponta a ponta | Download após exclusão |

## Handoffs e atividades posteriores

- **Grupo:** decidir as perguntas 1 e 2 (arquivo físico e retenção).
- **Integração:** cobrir o adapter com banco real na suíte de integração.

## Síntese

A exclusão lógica de documentos já estava implementada, mas o adapter SQLAlchemy não tinha nenhum teste e não havia cenário que provasse, de ponta a ponta, o isolamento entre dois estudantes. A decisão acrescenta esses testes sem mudar o código de produção. A principal incerteza é se o arquivo físico deve ser removido junto.
