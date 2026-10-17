---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-17T16:00:00-03:00"
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
    - path: src/backend/application/previa_versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f4f9a1d"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "portas ConsultaProprietarioItem, ItemPerfil e ConsultaItemPerfil (linhas 700-765)"
      content_state: commit
      revision: "f4f9a1d"
      availability: partial
    - path: src/backend/domain/secao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f4f9a1d"
      availability: available
    - path: "GitHub issue #213 (F5.5)"
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
      revision: "f4f9a1d"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f4f9a1d"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "Decide um ajuste de leitura sobre a prévia do currículo, na linhagem de versões de currículo de prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, delivery]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: high
  reversibility: easy
  risk: low
---

# Análise de decisão — projeção dos itens selecionados por seção

## Solicitação original

```text
[F5.5] Criar consulta que projeta o currículo com somente as referências selecionadas.
WBS: 1.4.1., 1.4.2. — Início: 2026-10-19 — Entrega: 2026-10-25
Responsável único: @regazzio
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

Decisão do usuário nesta conversa: tratar o card como um pequeno ajuste na prévia existente, sem criar adaptador de banco.

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

- O código-fonte corresponde ao commit `f4f9a1d` (cabeça da `dev` na consulta).
- O texto do card repete o título e não traz critérios de aceite além do padrão; o que a #213 espera **não foi confirmado** com o autor do card. Esta análise registra uma interpretação.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

Quem consome a prévia obtém os itens **selecionados** do currículo já agrupados por seção, na ordem padrão de seções, sem repetir essa decisão.

### Evidências e fatos observados

1. `GerarPreviaVersaoCurriculo` já lê somente as referências selecionadas, descarta item ausente ou de outro estudante e devolve tuplas ordenadas por tipo (`previa_versao_curriculo.py`).
2. A ordem padrão e o vocabulário de seções existem no domínio (`ORDEM_PADRAO_SECOES` e `SecaoCurriculo`), mas a prévia não os usa.
3. Não há adaptador de infraestrutura para `ConsultaItemPerfil` nem para `ConsultaProprietarioItem`; os repositórios de projeto, competência e idioma não têm leitura por id.

### Hipóteses

- **H1.** O card está, em sua maior parte, coberto pela prévia; o que falta é um modelo de leitura agrupado por seção na ordem padrão.
- **H2.** Um método `PreviaVersaoCurriculo.itens_por_secao()` devolve, na ordem padrão, apenas as seções com itens selecionados; os dados pessoais ficam de fora por não serem itens.
- **H3.** Não se cria adaptador de banco nesta entrega.

### Perguntas em aberto

1. O autor do card espera outra coisa (por exemplo, a consulta de infraestrutura)?
2. Os dados pessoais devem entrar na projeção como seção própria?
3. A ordem deve vir da ordem padrão ou de uma ordem definida pelo estudante (#211 e #212)?

### Escopo

- Método `itens_por_secao` na prévia e seus testes unitários.

### Fora do escopo

- Adaptadores de infraestrutura das portas de consulta; ordem personalizada pelo estudante; mudanças na rota.

### Critérios de sucesso

- Devolve só seções com itens, na ordem padrão, com o conteúdo exato da prévia.
- Prévia sem itens devolve projeção vazia.
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Application não depende de Infrastructure nem da API; docstring e proveniência em todo trecho novo (`AGENTS.md`, `src/backend/AGENTS.md`).

## Classificação comentada

- `uncertainty: high`: o objetivo do card não foi confirmado.
- `reversibility: easy` e `risk: low`: método puro, sem persistência.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `simplicity` | 1 | Revisável em 10 minutos | Critério de aceite do card |
| `modifiability` | 2 | Ordem decidida em um único ponto | #211 e #212 mudarão a fonte da ordem |

## Alternativas consideradas

**Estado atual.** A prévia devolve tuplas por tipo; cada consumidor decidiria a ordem das seções.

**Alternativa A — Método `itens_por_secao` na prévia (recomendada).** Pequeno, puro e testável; centraliza a ordem.

**Alternativa B — Não alterar nada e considerar o card coberto.** Zero risco, mas deixa a decisão de ordem para cada consumidor.

**Alternativa C — Criar o adaptador de banco de `ConsultaItemPerfil`.** Resolve a lacuna de infraestrutura, mas é uma entrega grande, que toca áreas de outras pessoas e não cabe no critério de 10 minutos.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `simplicity` | 1 | +1 | +1 | -2 | média | C exige três leituras novas e testes |
| `modifiability` | 2 | +1 | -1 | 0 | baixa | B espalha a ordem entre consumidores |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**. Status `proposed`: aprovação humana, em especial sobre as perguntas 1 e 3.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `simplicity` | prioritized | Um método puro | Sem portas nem persistência |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `modifiability` | Ordem em um ponto | O método usa `ORDEM_PADRAO_SECOES` |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `modifiability` | Cada consumidor repete a ordem das seções | Baixa | Equipe de backend |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | A lacuna de infraestrutura permanece | Valor de ponta a ponta | Aceitável: fica para entrega própria |

## Riscos e efeitos de segunda ordem

- **Interpretação errada do card.** Mitigação: perguntas 1 a 3 registradas; o método é pequeno e removível.
- **Ordem personalizada futura.** Quando #211 e #212 existirem, a fonte da ordem muda; o método é o ponto único a ajustar.
- **Conflitos de integração.** Alterações em `application/previa_versao_curriculo.py` podem conflitar com tarefas de ordenação.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Ordem padrão respeitada | Sequência de seções esperada | Teste unitário | Ordem diferente |
| Seção vazia omitida | Seções sem itens ausentes | Teste unitário | Título vazio na saída |
| Conteúdo fiel | Itens iguais aos da prévia | Teste unitário | Item acrescentado ou perdido |

## Handoffs e atividades posteriores

- **Decisão do time:** confirmar com o autor do card o que a #213 espera (pergunta 1).
- **Futuro:** adaptadores de `ConsultaItemPerfil` e `ConsultaProprietarioItem` em infraestrutura.

## Síntese

A prévia já projeta só as referências selecionadas, mas devolve tuplas por tipo e deixa a ordem das seções para cada consumidor. A decisão acrescenta `itens_por_secao`, que as agrupa na ordem padrão e omite seções vazias, sem tocar em infraestrutura. A principal incerteza é se o card esperava mais do que isso.
