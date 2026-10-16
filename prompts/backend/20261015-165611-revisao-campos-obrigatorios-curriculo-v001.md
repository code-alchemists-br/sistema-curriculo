---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-15T16:56:11-03:00"
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
    - path: src/frontend/features/validate-curriculum/model/validacao-curriculo.ts
      relationship: primary
      representation: source-code
      function: production
      format: typescript
      analysis_scope: selected-section
      locator: "linhas 1-150 (schemas Zod, seções obrigatórias, tipos de resultado e função validarCurriculo)"
      content_state: commit
      revision: "fe383e4c9c0b87838ce2c7c389e7d68fe98a0c5b"
      availability: partial
    - path: src/backend/application/previa_versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 1-80 (PreviaVersaoCurriculo e entrada do caso de uso)"
      content_state: commit
      revision: "fe383e4c9c0b87838ce2c7c389e7d68fe98a0c5b"
      availability: partial
    - path: src/backend/domain/itens_perfil.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "declarações das entidades e das validações de construção (por busca de linhas)"
      content_state: commit
      revision: "fe383e4c9c0b87838ce2c7c389e7d68fe98a0c5b"
      availability: partial
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "declarações de Cidade, Endereco, Telefone e DadosContato (por busca de linhas)"
      content_state: commit
      revision: "fe383e4c9c0b87838ce2c7c389e7d68fe98a0c5b"
      availability: partial
    - path: src/backend/domain/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "declaração do dataclass Usuario e campo dados_contato (por busca de linhas)"
      content_state: commit
      revision: "fe383e4c9c0b87838ce2c7c389e7d68fe98a0c5b"
      availability: partial
    - path: src/backend/domain/__init__.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fe383e4c9c0b87838ce2c7c389e7d68fe98a0c5b"
      availability: available
    - path: src/backend/tests/fixtures/curriculo_exportacao.py
      relationship: supporting
      representation: source-code
      function: data-fixture
      format: python
      analysis_scope: selected-section
      locator: "classe CurriculoExportacaoFixture e função obter_curriculo_exportacao_fixture (por busca de linhas)"
      content_state: commit
      revision: "fe383e4c9c0b87838ce2c7c389e7d68fe98a0c5b"
      availability: partial
    - path: docs/wireframes/07-revisao.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "linha 12 (indicar campos obrigatórios ausentes ou inválidos e a seção; por busca textual)"
      content_state: commit
      revision: "fe383e4c9c0b87838ce2c7c389e7d68fe98a0c5b"
      availability: partial
    - path: docs/mapeamento_jornadas.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "linhas 38, 114, 165 e 197 (por busca textual)"
      content_state: commit
      revision: "fe383e4c9c0b87838ce2c7c389e7d68fe98a0c5b"
      availability: partial
    - path: "GitHub issue #119 e #221 (F6.1)"
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
      revision: "fe383e4c9c0b87838ce2c7c389e7d68fe98a0c5b"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fe383e4c9c0b87838ce2c7c389e7d68fe98a0c5b"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "Decide a construção de uma fatia de backend (regra de domínio, caso de uso e rota de leitura) sobre a prévia do currículo; a linhagem de versões de currículo está em prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, user-experience, delivery]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: time-critical
  uncertainty: medium
  reversibility: easy
  risk: low
---

# Análise de decisão — revisão de campos obrigatórios do currículo

## Solicitação original

```text
vamos fazer a tarefa 119
Implementar revisão de campos obrigatórios do currículo e  Inclua os testes unitários pertinentes.
Mas vamos fazer diferente, me perdi no proprio codigo, vamos voltar no sistema antigo, vc manda se tenho q criar ou alterar e manda o codigo, e eu faço daqui, quero tambem que vc explique melhor
```

O texto da issue #119 é: "Tarefa da fatia vertical atribuída a @regazzio. Inclua os testes unitários pertinentes." Não há critérios de aceite adicionais.

## Informações complementares

- Modo de trabalho pedido: a assistente envia caminho, ação (criar ou alterar), código e explicação; o usuário aplica, roda testes e faz os commits.
- O front-end já valida seções obrigatórias (dados pessoais, formação, experiências e competências), e projetos como opcionais com campos mínimos (`validacao-curriculo.ts`). O resultado da validação do front-end lista seções com status e mensagens e libera ou bloqueia prévia e exportação.
- O card F6.1 (#221) pede um contrato de resultado da revisão com **código, seção, mensagem e severidade**; os cards F6.2 a F6.6 detalham regras e ordenação (por título, não lidos em detalhe). Eles têm datas posteriores (26/10 a 01/11) e o mesmo responsável.
- Esta análise é independente das anteriores e não as revisa.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `fe383e4c9c0b87838ce2c7c389e7d68fe98a0c5b` (cabeça da `dev` na consulta), lido por `git show origin/dev:<caminho>`.
- As validações das entidades de item foram identificadas por busca de linhas, sem leitura integral dos arquivos.
- Os cards F6.2 a F6.8 foram vistos somente pelo título; seu corpo não foi lido.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

O estudante (e o front-end) conseguem consultar, para uma versão própria, **quais seções obrigatórias estão incompletas**, cada pendência com código estável, seção, mensagem e severidade, em ordem previsível, para orientar a correção antes da prévia e da exportação.

### Atores e interesses

- **Estudante:** saber o que falta antes de exportar (wireframe 07).
- **Front-end:** consumir um contrato estável, coerente com a validação que já existe na interface.
- **Equipe de backend:** regra no domínio, sem duplicar o que as entidades já garantem.

### Evidências e fatos observados

1. As entidades `FormacaoAcademica`, `ExperienciaProfissional`, `ProjetoAcademico`, `Competencia` e `Idioma` já validam seus campos na construção (texto preenchido, enumerações, tamanhos). Portanto, um item existente nunca tem campo em branco; a lacuna possível é **a ausência de itens na seção** (`itens_perfil.py`).
2. `Usuario.dados_contato` é opcional; quando presente, `DadosContato` exige endereço e ao menos um telefone. Nome e e-mail são value objects obrigatórios (`usuario.py`, `value_objects.py`).
3. A prévia (`PreviaVersaoCurriculo`) já reúne o estudante e as tuplas de itens por seção, filtradas por dono e ordenadas, e levanta `CurriculoNaoEncontrado` para versão ausente ou alheia (`previa_versao_curriculo.py`).
4. O front-end trata como obrigatórias as seções dados pessoais, formação, experiências e competências, e como opcionais projetos (`validacao-curriculo.ts`). Os identificadores de seção são `dados-pessoais`, `formacao-academica`, `experiencias-profissionais` e `competencias`.
5. O wireframe 07 pede "indicar campos obrigatórios ausentes ou inválidos e a seção correspondente".
6. A fixture de exportação fornece um currículo completo e válido, reutilizável nos testes (`curriculo_exportacao.py`).
7. As skills exigem núcleo antes dos adapters, adapter sem regra de negócio, testes de rota com o caso de uso substituído por double, comentário de proveniência e docstring em toda função e classe. O CI roda `ruff check` (F e I) e a suíte.

### Hipóteses

- **H1.** A revisão é uma **consulta**: não altera estado, não persiste nada e não exige migration nem adapter novo.
- **H2.** A regra vive no **domínio** como função pura `revisar_curriculo`, que recebe o estudante e as tuplas de itens por seção, sem depender da Application.
- **H3.** Regras desta fatia, todas de **ausência**: `CONTATO_AUSENTE`, `FORMACAO_AUSENTE`, `EXPERIENCIA_AUSENTE` e `COMPETENCIA_AUSENTE` com severidade `erro`; `PROJETO_AUSENTE` e `IDIOMA_AUSENTE` com severidade `aviso` (recomendação).
- **H4.** Os identificadores de seção seguem os do front-end, acrescidos de `projetos-academicos` e `idiomas`.
- **H5.** A ordem do resultado é determinística: severidade (erro antes de aviso), depois a ordem das seções e depois o código.
- **H6.** `aprovado` é verdadeiro quando não há pendência de severidade `erro`; avisos não reprovam.
- **H7.** O caso de uso reaproveita a prévia, de modo que versão ausente ou alheia produz `CurriculoNaoEncontrado` (404) e dados alheios nunca entram na revisão.
- **H8.** A rota é `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/revisao`, com 200, 404 e 503, em módulo próprio.
- **H9.** Consistência de datas, persistência da decisão do estudante e bloqueio efetivo da exportação ficam fora (cards posteriores).

### Perguntas em aberto

1. A seção de experiências deve ser **erro** (como no front-end) ou **aviso**, para estudantes sem experiência?
2. A exportação deve ser bloqueada quando `aprovado` for falso (hoje o front-end bloqueia)?
3. Cidade, LinkedIn e Lattes devem gerar aviso de recomendação?
4. Os códigos de pendência (`CONTATO_AUSENTE` etc.) estão aceitos como contrato público?

### Escopo

- Domínio: seção, severidade, pendência, resultado e a função `revisar_curriculo`.
- Application: caso de uso `RevisarVersaoCurriculo` sobre a prévia.
- API: rota `GET .../revisao`, DTOs e registro em `factory.py`.
- Testes unitários de cada camada.

### Fora do escopo

- Persistência, histórico e decisão do estudante (F6.7 e F6.8).
- Regras de consistência de datas (F6.4) e painel de revisão no front-end (F6.15).
- Bloqueio da exportação; autenticação nova; composição com o banco.

### Critérios de sucesso

- Currículo completo: `aprovado` verdadeiro e sem pendências.
- Cada seção obrigatória vazia gera exatamente uma pendência de erro com código, seção e mensagem; seções opcionais vazias geram aviso.
- Contato ausente gera `CONTATO_AUSENTE`.
- A ordem do resultado é estável e independente da ordem de entrada.
- Versão ausente ou alheia resulta em 404, sem revisar.
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Domain não depende de Application, Infrastructure, API ou frameworks; Application não depende de Infrastructure nem da API; regras não ficam em controllers (`src/backend/AGENTS.md`).
- Docstring (o que faz, como faz, finalidade) em toda função e classe (`AGENTS.md`).
- Testes unitários com doubles; proveniência em todo trecho novo (skills).
- CI: `ruff check` com as regras `F` e `I` e a suíte unitária.

## Classificação comentada

- `uncertainty: medium`: a issue não traz critérios; as regras vêm do front-end e do wireframe.
- `reversibility: easy` e `risk: low`: consulta sem persistência nem migration.
- `urgency: time-critical`: há prazo de entrega próximo.

## Decisão de roteamento

Roteada para `prompts/backend`, onde estão as análises de versões de currículo. Candidatas: `prompts/backend` e `prompts/requisitos`; esta foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | 1 | Pendências corretas e ordem estável | O front-end e o estudante agem sobre o resultado |
| `simplicity` | 1 | Sem persistência, migration ou adapter novo | Prazo curto |
| `modifiability` | 2 | Novas regras entram sem mudar a rota | Os cards F6.2 a F6.6 acrescentarão regras |
| `user-value` | 2 | Coerente com a validação do front-end | Evita mensagens contraditórias |

## Alternativas consideradas

**Estado atual.** A validação existe só no front-end; o back-end não tem como informar o que falta.

**Alternativa A — Função de domínio + caso de uso sobre a prévia + rota GET (recomendada).** Sem persistência; reaproveita a propriedade e a leitura da prévia.

**Alternativa B — Validar na camada de API.** Menos arquivos, mas coloca regra de negócio em controller, o que a arquitetura proíbe, e não é reutilizável.

**Alternativa C — Persistir o resultado da revisão.** Permite histórico e decisão do estudante, mas exige tabela, migration e adapter, que são escopo dos cards F6.7 e F6.8.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | 1 | +1 | 0 | +1 | média | A e C testam a regra isolada; B mistura regra e transporte |
| `simplicity` | 1 | +1 | +1 | -2 | média | C exige persistência |
| `modifiability` | 2 | +1 | -2 | +1 | média | B não reaproveita a regra |
| `user-value` | 2 | +1 | +1 | +1 | baixa | O resultado é o mesmo para o estudante |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**, em três etapas: (1) Domínio, com a função `revisar_curriculo` e seus tipos; (2) Application, com `RevisarVersaoCurriculo` sobre a prévia; (3) Interface, com `GET .../revisao`. Status `proposed`: aprovação humana, em especial sobre as perguntas 1 e 2.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | prioritized | Pendências e ordem corretas | Testes de cada regra e da ordenação |
| `simplicity` | prioritized | Sem banco novo | Reaproveita a prévia |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `modifiability` | Novas regras sem alterar a rota | Regras em uma função de domínio |
| `user-value` | Coerência com o front-end | Mesmos identificadores e seções obrigatórias |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | Estudante exporta currículo incompleto ou recebe orientação errada | Média | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | Sem histórico nem decisão do estudante | `user-value` | Aceitável: cards F6.7 e F6.8 |
| `simplicity` | Só regras de ausência | `correctness` | Aceitável: as entidades já garantem os campos de cada item |

## Riscos e efeitos de segunda ordem

- **Regra divergente do front-end.** Se o front-end mudar as seções obrigatórias, o resultado diverge. Mitigação: mesmos identificadores e pergunta 1 registrada.
- **Estudante sem experiência bloqueado.** Mitigação: severidade única por regra, fácil de alterar.
- **Conflitos de integração.** Alterações em `domain/__init__.py` e `api/factory.py` costumam conflitar com outras tarefas; resolver ao integrar a `dev`.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Currículo completo é aprovado | Sem pendências | Teste de domínio com a fixture | Pendência indevida |
| Cada ausência gera sua pendência | Código, seção e severidade corretos | Testes de domínio por regra | Regra faltante ou duplicada |
| Ordem estável | Mesma saída para entradas equivalentes | Teste de domínio | Ordem dependente da entrada |
| Versão alheia é recusada | `CurriculoNaoEncontrado` | Teste do caso de uso com double | Revisão de dado alheio |
| Rota traduz o resultado | 200, 404 e 503 | Teste da rota com double | Status diferente |

## Handoffs e atividades posteriores

- **`$backend-domain-orchestration-v2`:** função e tipos de domínio, caso de uso e testes unitários.
- **`$backend-adapters-drivers-v2`:** rota, DTOs, registro em `factory.py` e testes.
- **Front-end:** consumir a rota e unificar com a validação local.
- **Próximas fatias:** consistência de datas, persistência da decisão (F6.7 e F6.8), bloqueio da exportação, avisos de recomendação (cidade, links).

## Síntese

O back-end não sabe dizer o que falta num currículo. A decisão cria uma regra de domínio pura que confere a ausência das seções obrigatórias e do contato, um caso de uso que a aplica à prévia da versão e uma rota de leitura. Não há banco nem adapter novo, porque as entidades já garantem os campos de cada item. A principal incerteza é a severidade da seção de experiências e se a revisão deve bloquear a exportação.
