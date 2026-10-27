---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-25T14:00:00-03:00"
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
    - path: src/backend/domain/decisao_recomendacao.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "cac53a7"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "portas RepositorioDecisaoRecomendacao, RepositorioCurriculo e Relogio (por busca de linhas)"
      content_state: commit
      revision: "cac53a7"
      availability: partial
    - path: src/backend/application/revisao_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "cac53a7"
      availability: available
    - path: src/backend/api/revisao_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "cac53a7"
      availability: available
    - path: "GitHub issue #228 (F6.8)"
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
      revision: "cac53a7"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "cac53a7"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "Expõe, por HTTP, a decisão do estudante persistida na análise 20261023-170000, na linhagem de revisão de currículo de prompts/backend."
classification:
  sphere: engineering
  concerns: [security, domain, delivery]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: time-critical
  uncertainty: medium
  reversibility: easy
  risk: medium
---

# Análise de decisão — expor a decisão do estudante sobre recomendações

## Solicitação original

```text
[F6.8] Expor a decisão do estudante sobre uma recomendação e testar autorização.
WBS: 1.4.3., 1.4.4. — Início: 2026-10-26 — Entrega: 2026-11-01
Responsável único: @regazzio
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Modo de trabalho pedido: a assistente escreve os arquivos e o usuário faz os commits.
- Esta análise usa a persistência da análise `20261023-170000-persistir-decisao-recomendacao-v001.md` (F6.7) e a rota da revisão (F6.6), sem revisá-las.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `cac53a7` (cabeça da `dev` na consulta).
- O corpo da issue #228 repete o título; **não está confirmado** o formato esperado das rotas nem o que o card entende por "testar autorização".
- A persistência real não foi exercitada: os testes usam um repositório em memória.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

O estudante autenticado aceita ou rejeita uma recomendação da revisão de uma versão própria e consulta o que já decidiu; ninguém decide ou consulta sobre versão alheia, e erros da revisão não podem ser "rejeitados".

### Evidências e fatos observados

1. A tabela, o value object `DecisaoRecomendacao` e o repositório de decisões existem (F6.7).
2. A revisão devolve pendências com severidade `aviso` (recomendação) ou `erro`, e já recusa versão ausente ou alheia com `CurriculoNaoEncontrado` (F6.6).
3. Rotas sob `/estudantes/{usuario_id}/curriculos` são protegidas pelo middleware, que exige sessão e recusa outro estudante na URL (403).
4. A porta `Relogio` existe e fornece o instante da decisão.

### Hipóteses

- **H1.** `PUT /estudantes/{usuario_id}/curriculos/{curriculo_id}/recomendacoes/{codigo}` com corpo `{"decisao": "aceita"|"rejeitada"}` registra a decisão; `GET …/recomendacoes` lista as decisões da versão.
- **H2.** O caso de uso de registro reaproveita a revisão: versão ausente ou alheia falha com `CurriculoNaoEncontrado`, e o código só vale se for um aviso da revisão **atual**; senão, `RecomendacaoNaoEncontrada` (404 também para um erro, sem distinguir de código inexistente).
- **H3.** O instante vem da porta `Relogio`, nunca do cliente.
- **H4.** Decidir de novo o mesmo código substitui a decisão anterior (regra da persistência).
- **H5.** A consulta confere a versão no repositório de currículos, sem calcular a revisão.
- **H6.** A resposta de decisões expõe código, decisão e instante, sem versão nem identificadores internos.

### Perguntas em aberto

1. Uma decisão sobre uma recomendação que deixou de existir (o estudante já incluiu o item) deve continuar listada?
2. A revisão (`GET …/revisao`) deve passar a trazer a decisão junto de cada aviso?
3. Rejeitar uma recomendação deve escondê-la nas próximas revisões?

### Escopo

- Casos de uso de registro e consulta, rotas, DTOs, registro na fábrica e testes de autorização.

### Fora do escopo

- Alterar o resultado da revisão com base nas decisões; composição real com banco e sessão.

### Critérios de sucesso

- Registro e consulta funcionam para o dono; a decisão grava o instante do relógio.
- Recomendação inexistente ou erro: 404; decisão fora das opções: 422.
- Versão alheia: 404; outro estudante na URL: 403; sem sessão: 401; sem executor: 503; nada é gravado nos casos de recusa.
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Adapter sem regra de negócio; regra no caso de uso; testes de rota com a Application real sobre doubles de portas; docstring e proveniência em todo trecho novo (`AGENTS.md`).

## Classificação comentada

- `risk: medium`: envolve autorização sobre dados do estudante.
- `uncertainty: medium`: o card não define o formato das rotas.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `security` | 1 | Nenhuma decisão ou consulta sobre versão alheia | Dado pessoal do estudante |
| `correctness` | 1 | Só avisos da revisão atual podem ser decididos | Evita decisões sem sentido |
| `simplicity` | 2 | Reaproveitar revisão, persistência e relógio | Revisão em cerca de 10 minutos |

## Alternativas consideradas

**Estado atual.** A decisão pode ser persistida, mas não há como o estudante registrá-la ou consultá-la.

**Alternativa A — Registro com validação pela revisão e consulta separada (recomendada).**

**Alternativa B — Aceitar qualquer código e validar só o formato.** Mais simples, mas permite decisões sobre erros e códigos inventados.

**Alternativa C — Incluir a decisão dentro do resultado da revisão (`GET …/revisao`).** Entrega tudo junto, mas altera um contrato já publicado e mistura consulta e escrita.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `security` | 1 | +1 | +1 | +1 | média | As três usam a propriedade da versão |
| `correctness` | 1 | +1 | -2 | +1 | média | B aceita erro e código inventado |
| `simplicity` | 2 | 0 | +1 | -1 | média | C altera contrato publicado |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

A F6.7 decidiu a persistência por versão e código; esta análise a expõe por HTTP.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**. Status `proposed`: aprovação humana, em especial sobre as perguntas 1 a 3.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `security` | prioritized | Propriedade verificada no caso de uso e na URL | Testes 401, 403 e 404 |
| `correctness` | prioritized | Só aviso vigente é decidido | Testes de erro e de código inexistente |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | Reaproveitar o existente | Revisão, repositório e relógio já existiam |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `security` | Acesso às decisões de outro estudante | Alta | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `correctness` | Cada decisão recalcula a revisão | Eficiência | Aceitável: a revisão é uma regra pura sobre poucos itens |

## Riscos e efeitos de segunda ordem

- **Decisão sobre aviso que deixou de existir.** Fica gravada e listada; pergunta 1.
- **Composição real ausente.** No sistema em execução as rotas respondem 503 até a composição montar os casos de uso com banco, sessão e relógio.
- **Conflitos de integração.** `api/factory.py` e `application/__init__.py` são alterados por quase toda tarefa.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Só aviso vigente é decidido | 404 para erro e código inventado, sem gravar | Testes do caso de uso | Decisão gravada |
| Autorização | 401, 403 e 404 sem gravação | Testes de rota com middleware | Acesso permitido |
| Instante do relógio | Decisão com o instante configurado | Testes do caso de uso e da rota | Instante do cliente |
| Substituição | Uma decisão por código | Teste do caso de uso | Duas decisões |

## Handoffs e atividades posteriores

- **Grupo:** decidir as perguntas 2 e 3 (decisão dentro da revisão e efeito de rejeitar).
- **Composição:** montar `RegistrarDecisaoRecomendacao` com a revisão real, o repositório SQLAlchemy e um `Relogio`.

## Síntese

A decisão do estudante sobre recomendações já podia ser persistida, mas não havia como registrá-la nem consultá-la. A decisão expõe um PUT e um GET, reaproveitando a revisão para só aceitar decisão sobre avisos vigentes e a persistência da F6.7, com o instante vindo do relógio e testes de autorização (401, 403 e 404). A principal incerteza é o formato exato que o card esperava.
