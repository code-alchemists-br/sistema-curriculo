---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-23T10:00:00-03:00"
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
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "cd4ee46"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "Cidade, Endereco, Telefone e DadosContato (por busca de linhas)"
      content_state: commit
      revision: "cd4ee46"
      availability: partial
    - path: src/backend/tests/fixtures/curriculo_exportacao.py
      relationship: supporting
      representation: source-code
      function: data-fixture
      format: python
      analysis_scope: selected-section
      locator: "contato do estudante na função obter_curriculo_exportacao_fixture"
      content_state: commit
      revision: "cd4ee46"
      availability: partial
    - path: "GitHub issue #222 (F6.2)"
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
  rationale: "Estende a regra de revisão de campos obrigatórios (prompts/backend, 20261015-165611) com a completude de identificação e contato."
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

# Análise de decisão — completude de identificação e contato na revisão

## Solicitação original

```text
[F6.2] Implementar regra de completude para identificação e contato.
WBS: 1.4.3., 1.4.4. — Início: 2026-10-26 — Entrega: 2026-11-01
Responsável único: @regazzio
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Modo de trabalho pedido: a assistente escreve os arquivos e o usuário faz os commits.
- Esta análise estende, sem revisar, a análise `20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md`, cuja pergunta 3 era se cidade, LinkedIn e Lattes deveriam gerar aviso.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `cd4ee46` (cabeça da `dev` na consulta).
- O corpo da issue #222 repete o título e não traz critérios além do padrão; **o que o card espera por "completude" não foi confirmado**. Esta análise registra uma interpretação.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

A revisão aponta o que falta na identificação e no contato do estudante, distinguindo o que impede o currículo (erro) do que apenas melhora (aviso).

### Evidências e fatos observados

1. A revisão já gera `CONTATO_AUSENTE` (erro) quando `Usuario.dados_contato` é `None` (`revisao_curriculo.py`).
2. Nome e e-mail são value objects que rejeitam vazio na construção; portanto, a identificação nunca está incompleta em um `Usuario` válido (`value_objects.py`, `usuario.py`).
3. `DadosContato` exige endereço e ao menos um telefone; cidade, LinkedIn e Lattes são opcionais.
4. A fixture compartilhada tem LinkedIn e Lattes e não tem cidade; outro teste (documento renderizado) afirma que a cidade da fixture é ausente.

### Hipóteses

- **H1.** Extrair a regra para `_revisar_identificacao_e_contato(usuario)`, isolada das regras de seção.
- **H2.** Sem contato: somente `CONTATO_AUSENTE` (erro), sem avisos sobre campos de um contato inexistente.
- **H3.** Com contato: `CIDADE_AUSENTE` (aviso) se não há cidade, e `LINK_PROFISSIONAL_AUSENTE` (aviso) se não há nem LinkedIn nem Lattes; um dos dois basta.
- **H4.** Nome e e-mail não geram regra, por já serem garantidos pelo domínio.
- **H5.** A fixture compartilhada não é alterada; os testes da revisão derivam dela um estudante com cidade.

### Perguntas em aberto

1. O card espera outras verificações de identificação (por exemplo, nome completo com sobrenome)?
2. Cidade e links devem mesmo ser avisos, ou nada deve ser recomendado?
3. Formato de URL do LinkedIn e do Lattes deve ser verificado nesta regra?

### Escopo

- Regra de identificação e contato e seus testes; ajuste dos testes da revisão que esperavam currículo sem pendências.

### Fora do escopo

- Formação e experiência (F6.3); datas (F6.4); recomendações de seção vazia (F6.5); rota e persistência.

### Critérios de sucesso

- Sem contato: um erro. Com contato e sem cidade: um aviso. Sem os dois links: um aviso. Com um link: nenhum.
- Avisos não reprovam o currículo e vêm em ordem estável.
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Regras ficam no domínio, sem depender de banco ou rota; docstring e proveniência em todo trecho novo (`AGENTS.md`).

## Classificação comentada

- `uncertainty: medium`: o card não detalha a completude esperada.
- `reversibility: easy` e `risk: low`: regra pura, sem persistência.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `simplicity` | 1 | Revisável em cerca de 10 minutos | Critério de aceite |
| `user-value` | 2 | Avisos úteis, sem bloquear sem motivo | Evita frustrar o estudante |

## Alternativas consideradas

**Estado atual.** Só existe o erro de contato ausente.

**Alternativa A — Avisos para cidade e links, em função própria (recomendada).** Pequena e sem bloquear.

**Alternativa B — Tratar cidade e links como erro.** Reprovaria currículos válidos por campos opcionais.

**Alternativa C — Não acrescentar nada.** Zero risco, mas a regra de contato fica sem recomendações.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `simplicity` | 1 | +1 | +1 | +1 | média | Todas pequenas |
| `user-value` | 2 | +1 | -1 | 0 | baixa | B bloqueia por campo opcional |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

A análise de 15/10 deixou a questão de cidade, LinkedIn e Lattes em aberto.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**. Status `proposed`: aprovação humana, em especial sobre as perguntas 1 e 2.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `simplicity` | prioritized | Uma função e dois avisos | Testes isolados |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `user-value` | Não bloquear por campo opcional | Cidade e links são avisos |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `user-value` | Currículos sem cidade ou links sem qualquer orientação | Baixa | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | Sem validação de formato de URL | `user-value` | Aceitável: pergunta 3 registrada |

## Riscos e efeitos de segunda ordem

- **Novos avisos em currículos existentes.** Quem não tem cidade ou links passa a ver avisos; não reprova.
- **Interpretação diferente do card.** Mitigação: perguntas registradas; a regra está em uma função isolada.
- **Conflitos de integração.** As regras F6.3 a F6.5 também alteram `revisao_curriculo.py`.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Avisos não reprovam | `aprovado` verdadeiro | Testes de domínio | Reprovação por aviso |
| Um link basta | Sem pendência com um dos links | Teste de domínio | Aviso indevido |
| Sem contato, só o erro | Pendência única | Teste de domínio | Avisos extras |

## Handoffs e atividades posteriores

- **F6.3, F6.4 e F6.5:** novas regras no mesmo arquivo, uma por PR.

## Síntese

A revisão só apontava a ausência do contato. A decisão separa a regra de identificação e contato em uma função e acrescenta dois avisos que não reprovam (cidade e links profissionais), mantendo o erro quando não há contato algum. A principal incerteza é o que o card chama de completude.
