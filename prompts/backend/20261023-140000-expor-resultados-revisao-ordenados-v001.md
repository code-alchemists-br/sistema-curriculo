---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-23T14:00:00-03:00"
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
    - path: src/backend/api/revisao_versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/factory.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "registro do router de revisão e parâmetro revisar_versao_curriculo (por busca de linhas)"
      content_state: working-tree
      revision: null
      availability: partial
    - path: src/backend/domain/revisao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "cd4ee46"
      availability: available
    - path: src/backend/application/revisao_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "cd4ee46"
      availability: available
    - path: "GitHub issue #226 (F6.6)"
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
      revision: "cd4ee46"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "cd4ee46"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "Publica a rota da revisão de campos obrigatórios (prompts/backend, 20261015-165611), cuja regra e caso de uso já estão na dev."
classification:
  sphere: engineering
  concerns: [delivery, user-experience]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: time-critical
  uncertainty: low
  reversibility: easy
  risk: low
---

# Análise de decisão — expor os resultados da revisão ordenados

## Solicitação original

```text
[F6.6] Expor resultados da revisão ordenados por severidade e seção.
WBS: 1.4.3., 1.4.4. — Início: 2026-10-26 — Entrega: 2026-11-01
Responsável único: @regazzio
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Modo de trabalho pedido: a assistente escreve os arquivos e o usuário faz os commits.
- Esta análise complementa, sem revisar, a análise `20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md`, que definiu a rota `GET …/revisao`.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código de domínio e de aplicação corresponde ao commit `cd4ee46` (cabeça da `dev` na consulta); os arquivos da rota e do `factory.py` são os da árvore de trabalho, ainda não commitados.
- O corpo da issue #226 repete o título e não traz critérios além do padrão.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

O cliente consulta `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/revisao` e recebe o veredito e as pendências já na ordem em que deve apresentá-las: erros antes de avisos e, dentro de cada grupo, pela ordem das seções.

### Evidências e fatos observados

1. A ordenação por severidade, seção e código já é feita no domínio (`revisar_curriculo`), e o caso de uso `RevisarVersaoCurriculo` está na `dev`.
2. A rota que expõe o resultado foi escrita na task 119, mas os arquivos entraram vazios no PR #486; o conteúdo ficou em uma branch local e nunca foi publicado.
3. O `factory.py` mudou muito desde então (tags do Swagger, vagas, saúde), exigindo reintegrar o registro da rota.

### Hipóteses

- **H1.** A rota não reordena: preserva a ordem do domínio, que é a fonte única dessa regra.
- **H2.** A rota usa a tag do Swagger "Versões de currículo", como as demais rotas de versão.
- **H3.** Versão ausente ou alheia responde 404 e a falta do executor responde 503, como nas outras rotas.

### Perguntas em aberto

1. O cliente precisa de um campo adicional (por exemplo, contagem de erros e avisos)?
2. A resposta deve incluir a posição de cada pendência, ou a ordem da lista basta?

### Escopo

- Rota `GET …/revisao`, DTOs de resposta, registro no `create_app`, teste da ordem na resposta e demais testes da rota.

### Fora do escopo

- Novas regras de revisão (F6.2 a F6.5); decisão do estudante sobre recomendações (F6.7 e F6.8).

### Critérios de sucesso

- A resposta traz erros antes de avisos e, no grupo, as seções na ordem do domínio.
- 404 para versão ausente ou alheia; 503 sem executor; rota registrada e documentada.
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Adapter sem regra de negócio; testes da rota com o caso de uso substituído por double; docstring e proveniência em todo trecho novo (`AGENTS.md`).

## Classificação comentada

- `uncertainty: low` e `risk: low`: a regra e o caso de uso já existem e são testados; a rota só traduz o resultado.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `simplicity` | 1 | Revisável em cerca de 10 minutos | Critério de aceite |
| `correctness` | 1 | Ordem estável e igual à do domínio | O cliente apresenta o que recebe |

## Alternativas consideradas

**Estado atual.** O resultado só existe dentro da Application; o cliente não consegue consultá-lo.

**Alternativa A — Rota que preserva a ordem do domínio (recomendada).** Uma única fonte da regra de ordenação.

**Alternativa B — Reordenar na rota.** Duplica a regra e pode divergir do domínio.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Confiança | Base |
|---|---:|---:|---:|---|---|
| `simplicity` | 1 | +1 | 0 | alta | B acrescenta código na rota |
| `correctness` | 1 | +1 | -1 | alta | B duplica a regra |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

A análise de 15/10 definiu a rota `GET …/revisao`; esta publica o que ficou pendente.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**. Status `proposed`: aprovação humana.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | prioritized | Ordem única e testada | Teste que compara a resposta com a regra real |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | Cerca de 10 minutos | A rota só traduz o resultado |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | Pendências apresentadas fora de ordem | Baixa | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | Sem campos extras na resposta | `user-value` | Aceitável: perguntas 1 e 2 registradas |

## Riscos e efeitos de segunda ordem

- **Conflitos de integração.** O `factory.py` é alterado por quase toda tarefa; resolver ao integrar a `dev`.
- **Rota sem composição real.** No sistema em execução a rota responde 503 até o executor ser composto com banco e sessão.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Ordem entregue igual à do domínio | Sequência de códigos esperada | Teste da rota com a regra real | Ordem diferente |
| 404, 503 e registro | Status e rota no OpenAPI | Testes da rota e da fábrica | Status diferente |

## Handoffs e atividades posteriores

- **F6.7 e F6.8:** decisão do estudante sobre recomendações, sobre os códigos de aviso entregues por esta rota.

## Síntese

A regra de revisão e o caso de uso já existiam, mas o cliente não tinha como consultá-los. A decisão publica a rota que devolve o veredito e as pendências na ordem do domínio, com um teste que prova a ordem de erros antes de avisos e por seção. A principal incerteza é se o cliente precisa de campos além do veredito e da lista.
