---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-23T19:00:00-03:00"
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
      revision: "d1df2ab"
      availability: available
    - path: src/backend/application/revisao_versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d1df2ab"
      availability: available
    - path: src/backend/domain/itens_perfil.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "StatusFormacaoAcademica, FormacaoAcademica e ExperienciaProfissional (por busca de linhas)"
      content_state: commit
      revision: "d1df2ab"
      availability: partial
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "classe Periodo (por busca de linhas)"
      content_state: commit
      revision: "d1df2ab"
      availability: partial
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "porta Relogio (por busca de linhas)"
      content_state: commit
      revision: "d1df2ab"
      availability: partial
    - path: "GitHub issue #224 (F6.4)"
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
  rationale: "Estende a regra de revisão (prompts/backend, 20261015-165611) com a consistência de datas de formação e experiência."
classification:
  sphere: engineering
  concerns: [domain, correctness]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: medium
---

# Análise de decisão — consistência de datas na revisão do currículo

## Solicitação original

```text
[F6.4] Implementar regra de consistência de datas em formação e experiência.
WBS: 1.4.3., 1.4.4. — Início: 2026-10-26 — Entrega: 2026-11-01
Responsável único: @regazzio
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Modo de trabalho pedido: a assistente escreve os arquivos e o usuário faz os commits.
- Esta análise estende, sem revisar, a análise `20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md`, que deixou a consistência de datas fora do escopo (F6.4).

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `d1df2ab` (cabeça da `dev` na consulta).
- O corpo da issue #224 repete o título e não traz critérios; **os casos de inconsistência abaixo são interpretação minha**, a confirmar com o grupo.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

A revisão aponta datas de formação e experiência que, mesmo válidas isoladamente, são incoerentes com o dia de hoje, distinguindo o que é impossível (erro) do que parece desatualizado (aviso).

### Evidências e fatos observados

1. O `Periodo` já impede término anterior ao início, na criação do item.
2. A formação concluída já exige data final (`FormacaoAcademica`).
3. Nada compara as datas com o dia atual, e o domínio não pode ler o relógio do sistema.
4. A porta `Relogio` existe na Application e já é usada por outros casos de uso.
5. A fixture compartilhada tem uma formação "em andamento" com término previsto em 2025-12-20.

### Hipóteses

- **H1.** A regra recebe `hoje` por parâmetro (`revisar_curriculo(..., hoje)`), e o caso de uso o obtém da porta `Relogio`, mantendo o domínio puro.
- **H2.** Formação **concluída** com término no futuro é **erro**.
- **H3.** Experiência com **início no futuro** é **erro**.
- **H4.** Formação **em andamento** com término já passado é **aviso** (a situação provavelmente ficou desatualizada); término previsto no futuro é legítimo.
- **H5.** Há **tolerância de um dia** nos dois sentidos, para não gerar falso alarme por diferença de fuso horário (o relógio entrega UTC; o estudante está em UTC-3).
- **H6.** No máximo uma pendência por tipo de problema, mesmo com vários itens afetados.
- **H7.** Formação interrompida e experiência com término futuro não são apontadas.

### Perguntas em aberto

1. Formação com início no futuro (matrícula já feita) deve gerar aviso?
2. Experiência com término futuro (contrato com data prevista) deve gerar aviso?
3. Sobreposição de períodos de experiência deve ser apontada?
4. A tolerância de um dia é suficiente?

### Escopo

- Regra de datas no domínio, parâmetro `hoje`, relógio no caso de uso e testes.

### Fora do escopo

- Sobreposição de períodos; datas de projetos, idiomas ou documentos; persistência e rota.

### Critérios de sucesso

- Cada caso de H2 a H4 gera exatamente a pendência esperada, com os limites de um e dois dias.
- Datas coerentes não geram pendência, nem os casos de H7.
- O domínio não lê o relógio do sistema.
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Domínio independente de relógio (`src/backend/AGENTS.md`); a data vem de uma porta; docstring e proveniência em todo trecho novo.

## Classificação comentada

- `uncertainty: medium`: o card não define os casos de inconsistência.
- `risk: medium`: a assinatura de `revisar_curriculo` e o construtor do caso de uso mudam; não há composição real afetada ainda.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | 1 | Sem falso alarme nem omissão nos limites | O estudante age sobre o aviso |
| `simplicity` | 1 | Revisável em cerca de 10 minutos | Critério de aceite |
| `testability` | 2 | Domínio sem relógio do sistema | Testes determinísticos |

## Alternativas consideradas

**Estado atual.** Só o `Periodo` valida datas, e apenas a ordem entre início e fim.

**Alternativa A — `hoje` por parâmetro, relógio no caso de uso (recomendada).** Domínio puro e determinístico.

**Alternativa B — O domínio lê `date.today()`.** Menos código, mas quebra a independência do relógio e torna os testes frágeis.

**Alternativa C — Parâmetro `hoje` opcional (sem ele, a regra de datas não roda).** Evita mudar chamadores, mas um chamador pode esquecer e desligar a regra em silêncio.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | 1 | +1 | +1 | -1 | média | C pode desligar a regra sem aviso |
| `simplicity` | 1 | 0 | +1 | +1 | média | A muda a assinatura e os testes |
| `testability` | 2 | +1 | -2 | +1 | alta | B depende do relógio do sistema |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

A análise de 15/10 deixou a consistência de datas para a F6.4.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**. Status `proposed`: aprovação humana, em especial sobre as perguntas 1 a 4.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | prioritized | Limites testados em um e dois dias | Testes de domínio com `hoje` fixo |
| `simplicity` | prioritized | Regra isolada em uma função | Sem persistência nem rota |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `testability` | Sem relógio do sistema | `hoje` entra por parâmetro e pela porta `Relogio` |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | Currículo com datas impossíveis exportado sem alerta | Média | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `testability` | Mudança de assinatura e de construtor | `simplicity` | Aceitável: só testes e um caso de uso usam |

## Riscos e efeitos de segunda ordem

- **Falso aviso em dados reais.** Formação "em andamento" com término previsto já passado passa a receber aviso; é só aviso e não reprova.
- **Fuso horário.** A tolerância de um dia cobre a diferença entre UTC e o horário do estudante; limites exatos têm teste.
- **Composição futura.** Quem montar o caso de uso real precisará injetar um `Relogio`.
- **Conflitos de integração.** `revisao_curriculo.py` é alterado por outras tarefas de revisão.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Erros e avisos corretos | Código, seção e severidade esperados | Testes de domínio | Pendência errada |
| Limites e tolerância | Sem pendência a 1 dia; pendência a 2 dias | Teste de limites | Limite deslocado |
| Domínio sem relógio | `hoje` recebido por parâmetro | Revisão do código e testes | Leitura do relógio |
| Caso de uso usa o relógio injetado | Resultado muda com o relógio | Teste da Application | Resultado igual |

## Handoffs e atividades posteriores

- **Composição:** injetar um `Relogio` real ao montar `RevisarVersaoCurriculo`.
- **Decisão do grupo:** perguntas 1 a 3 (início futuro de formação, término futuro de experiência e sobreposição).

## Síntese

A revisão aceitava qualquer data coerente consigo mesma, mesmo uma formação concluída no futuro ou uma experiência que ainda não começou. A decisão acrescenta uma regra de datas que compara os períodos com o dia de hoje, recebido por parâmetro (vindo da porta `Relogio` no caso de uso), com erro para o impossível, aviso para o provavelmente desatualizado e tolerância de um dia para o fuso. A principal incerteza é quais casos o card considera inconsistência.
