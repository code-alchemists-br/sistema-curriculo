---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-09T19:26:04-03:00"
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
      analysis_scope: selected-section
      locator: "campos do agregado, validação e leitura de referências (linhas 1-80 e uso por listagem)"
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: partial
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "classes RepositorioCurriculo e GeradorCurriculoId (linhas 245-300) e lista de portas (por listagem)"
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: partial
    - path: src/backend/application/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 1-140 (CurriculoNaoEncontrado, edição e criação de versão)"
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: partial
    - path: src/backend/api/versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 40-100 (DTOs de requisição e resposta) e 160-230 (rota de criação e fim do router)"
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: partial
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 24-140 (modelos CurriculoRegistro e CurriculoItemRegistro e mapeadores)"
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: partial
    - path: src/backend/application/__init__.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 50-110 (importações) e fim do __all__ (por leitura de conflito)"
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: partial
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF02, RF14 e RF15 (por busca textual)"
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: partial
    - path: docs/casos-de-uso-v2.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "caso de uso Gerenciar versões (linhas 110-113, por busca textual)"
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: partial
    - path: docs/wireframes/02-painel-inicial.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: available
    - path: prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: available
    - path: prompts/backend/20261008-183601-previa-versao-curriculo-v001.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: external
      revision: null
      availability: available
    - path: .agents/skills/backend-domain-orchestration-v2/SKILL.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: available
    - path: .agents/skills/backend-adapters-drivers-v2/SKILL.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "118974fd2e51424573f2e15cc8705d06136a351c"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "O propósito é decidir a construção de uma fatia de backend (porta, caso de uso, adapter e rota de leitura) sobre o agregado Curriculo; a linhagem relacionada de versões de currículo está em prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, data, security]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: medium
---

# Análise de decisão — listagem de versões de currículo

## Solicitação original

Texto literal fornecido pelo usuário:

```text
Implementar listagem de versões de currículo
#111, Inclua os testes unitários pertinentes.

Como estou com pressa, pode ir mexendo, mas vamos por etapa e etapa, vc faz a etapa 1 eu commito, e vamos indo, fechou?
```

## Informações complementares

Insumos literais registrados na conversa (grafia preservada):

- Resposta do usuário sobre o que pode ser feito enquanto o pull request da tarefa 120 não for aprovado: "entao bora, Implementar listagem de versões de currículo #111".
- Sobre tarefas anteriores, tomado como preferência por entregas pequenas: "descricao menor, dá? to achando muito grande esse PR"
- Mensagem do gestor reproduzida pelo usuário em conversa anterior: "No começo as coisas não estavam muito bem definidas, mas agora as funcionalidades já são claras. Os time serão reorganizados para lidar com slices verticais agora ao invés de horizontais. Isso só afeta backend. Frontend fica do mesmo jeito"
- O texto da issue #111 não foi lido: a GitHub CLI não está disponível neste ambiente e o usuário informou somente o título e o número.
- A branch será criada a partir da `dev` (cabeça `118974f`), que já contém a seleção de itens (tarefa 117, PR #166). A prévia (tarefa 120) ainda não está na `dev`; esta análise não depende dela.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/domain/curriculo.py` | primary | source-code | production | python | campos, validação e leitura de referências | commit `118974f` |
| `src/backend/application/ports.py` | primary | source-code | production | python | `RepositorioCurriculo` e `GeradorCurriculoId` | commit `118974f` |
| `src/backend/application/versao_curriculo.py` | supporting | source-code | production | python | linhas 1-140 | commit `118974f` |
| `src/backend/api/versao_curriculo.py` | primary | source-code | production | python | DTOs e rota de criação | commit `118974f` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py` | primary | source-code | production | python | arquivo inteiro | commit `118974f` |
| `src/backend/infrastructure/persistence/sqlalchemy/curriculo.py` | primary | source-code | production | python | modelos e mapeadores | commit `118974f` |
| `src/backend/application/__init__.py` | supporting | source-code | production | python | importações e `__all__` | commit `118974f` |
| `docs/requisitos_funcionais.md` | supporting | prose | documentation | markdown | RF02, RF14, RF15 | commit `118974f` |
| `docs/casos-de-uso-v2.md` | supporting | prose | documentation | markdown | Gerenciar versões | commit `118974f` |
| `docs/wireframes/02-painel-inicial.md` | context | prose | documentation | markdown | arquivo inteiro | commit `118974f` |
| `prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md` | supporting | prose | documentation | markdown | arquivo inteiro | commit `118974f` |
| `prompts/backend/20261008-183601-previa-versao-curriculo-v001.md` | context | prose | documentation | markdown | arquivo inteiro | externo à `dev` (branch `task-120`) |
| `.agents/skills/backend-domain-orchestration-v2/SKILL.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `118974f` |
| `.agents/skills/backend-adapters-drivers-v2/SKILL.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `118974f` |
| `AGENTS.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `118974f` |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `118974f` |

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `118974fd2e51424573f2e15cc8705d06136a351c`, lido por `git show origin/dev:<caminho>`, pois a árvore de trabalho estava, no momento da análise, na branch `task-120` com um merge em andamento.
- Arquivos com recorte parcial sustentam somente os fatos dos trechos indicados.
- O texto da issue #111 não foi lido. Seus critérios de aceite podem diferir das hipóteses abaixo.
- Os documentos de requisitos e casos de uso não detalham o conteúdo da listagem: a definição dos campos retornados é hipótese.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md` e suas referências; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

O estudante consegue listar todas as versões de currículo que possui, para escolher qual abrir, editar, visualizar ou exportar. A resposta traz, por versão, os dados que identificam e descrevem a versão, sem o conteúdo dos itens. Versões de outros estudantes nunca aparecem. A entrega atravessa Application, Infrastructure e Interface, com testes unitários.

### Atores e interesses

- **Estudante dono das versões:** ver e escolher entre versões para objetivos diferentes (caso de uso "Gerenciar versões"; RF14; RF15).
- **Outro estudante:** suas versões não podem aparecer na lista de terceiros (RNF04, RF13).
- **Frontend:** consome a lista para montar a seleção de versão.
- **Equipe de backend e líder técnico:** fronteiras entre camadas e tamanho do PR.

### Evidências e fatos observados

1. `RepositorioCurriculo` declara somente `obter_por_id`, `atualizar` e `salvar`; não há consulta por proprietário (`src/backend/application/ports.py`).
2. O adapter carrega uma versão por vez: `obter_por_id` lê o registro por chave primária e, em seguida, as linhas de `curriculo_itens` da versão para reconstruir as referências por `para_curriculo` (`repositorio_curriculo.py`, `curriculo.py`).
3. `CurriculoRegistro` tem `usuario_id` como chave estrangeira não nula para `usuarios`; `CurriculoItemRegistro` tem chave primária composta (`curriculo_id`, `tipo`, `item_id`) e chave estrangeira para `curriculos`. Não há coluna de data de criação em `curriculos` (`curriculo.py`).
4. O agregado `Curriculo` guarda `titulo_versao`, `layout`, `is_public` e expõe `referencias` como `frozenset`; a ordem das referências não é definida (`src/backend/domain/curriculo.py`).
5. `CurriculoNaoEncontrado` agrupa ausência e propriedade alheia; a criação de versão não verifica a existência do proprietário (a chave estrangeira barra dono inexistente), decisão registrada na análise de criação (`application/versao_curriculo.py`, `api/versao_curriculo.py`).
6. A rota de criação já ocupa `POST /estudantes/{usuario_id}/curriculos`; a listagem pode usar o mesmo caminho com o método `GET`. Os casos de uso de versão devolvem o agregado à API, que o converte em DTO de resposta, `VersaoCurriculoResposta`, com `id`, `titulo_versao`, `layout` e `is_public` (`api/versao_curriculo.py`).
7. RF14 prevê que cada estudante crie, consulte, edite e exclua múltiplos currículos; RF15 prevê selecionar qual currículo será exportado ou associado a uma vaga. O caso de uso "Gerenciar versões" prevê versões para objetivos diferentes (`docs/requisitos_funcionais.md`, `docs/casos-de-uso-v2.md`).
8. O wireframe do painel inicial trata um único currículo (estado vazio, em preenchimento e concluído) e não descreve uma lista de versões (`docs/wireframes/02-painel-inicial.md`).
9. A tarefa 115 (exclusão de versão) também alterará `RepositorioCurriculo` e o adapter; haverá conflito textual entre as duas, sem dependência funcional (conversa).
10. As skills de implementação exigem núcleo antes dos adapters, adapter sem criar porta ou regra de negócio, testes de rota com o caso de uso substituído por double e comentário de proveniência em todo trecho novo.

### Hipóteses

- **H1.** A listagem é uma **consulta**: não altera estado e não chama `atualizar` nem `salvar`.
- **H2.** Cada elemento da resposta traz `id`, `titulo_versao`, `layout`, `is_public` e `total_itens` (quantidade de itens selecionados); **não** traz o conteúdo dos itens, que pertence à prévia (tarefa 120).
- **H3.** A porta `RepositorioCurriculo` ganha `listar_por_usuario(usuario_id) -> tuple[Curriculo, ...]`, devolvendo agregados no mesmo contrato de `obter_por_id`, isto é, **com** as referências carregadas. Isso evita agregados incompletos que apagariam a seleção se fossem reaproveitados em uma edição.
- **H4.** O adapter lê as versões do proprietário em uma consulta e as linhas de seleção de todas elas em uma segunda consulta, agrupando por versão, sem consulta por versão (evita N+1).
- **H5.** A ordem é determinística e definida no caso de uso: título (sem diferenciar caixa) e identificador como desempate, já que não há data de criação.
- **H6.** Sem paginação nem filtros nesta fatia: a quantidade de versões por estudante é pequena.
- **H7.** Estudante sem versões, ou inexistente, recebe lista vazia (200), sem consulta ao repositório de usuário e sem 404, para não revelar a existência de contas e por coerência com a criação (fato 5).
- **H8.** Como defesa em profundidade, o caso de uso descarta qualquer versão cujo proprietário não seja o solicitante, mesmo que o adapter a devolva.
- **H9.** A rota é `GET /estudantes/{usuario_id}/curriculos`, em módulo próprio, respondendo 200 com um objeto `{"versoes": [...]}` (envelope que permite evoluir para paginação sem quebrar clientes), e 503 sem executor injetado.
- **H10.** Sem alteração de esquema: nenhuma migration; a listagem usa as tabelas `curriculos` e `curriculo_itens` existentes.

### Perguntas em aberto

1. Os critérios de aceite da issue #111 coincidem com H1 a H10?
2. `total_itens` deve estar na resposta (H2) ou a listagem deve conter só os dados escalares da versão?
3. A ordem por título (H5) atende, ou o cliente espera "mais recentes primeiro"? Neste caso seria preciso uma coluna de criação e uma migration, em outra tarefa.
4. Versões com `is_public` verdadeiro serão listadas para outros usuários no futuro (por exemplo, busca por recrutadores)? Nesta fatia a listagem é restrita ao dono.
5. Há necessidade de paginação ou de filtro por título ou visibilidade?
6. Estudante com exclusão lógica (`deleted_at`) deve receber lista vazia ou 404? A decisão H7 ignora o estado de exclusão.

### Escopo

- Método `listar_por_usuario` na porta `RepositorioCurriculo`, entrada `ListarVersoesCurriculoEntrada` e caso de uso `ListarVersoesCurriculo`.
- Método correspondente no adapter SQLAlchemy.
- Rota `GET /estudantes/{usuario_id}/curriculos`, DTOs de resposta e registro em `factory.py`.
- Testes unitários de cada camada com doubles.

### Fora do escopo

- Paginação, filtros e busca; ordenação por data; migration.
- Conteúdo dos itens (tarefa 120) e exclusão de versão (tarefa 115).
- Autenticação, sessão e autorização; composição de engine e sessão reais.
- Testes de integração com banco real.

### Critérios de sucesso

- A listagem de um estudante devolve apenas versões dele, em ordem determinística, cada uma com título, layout, visibilidade e quantidade de itens.
- Estudante sem versões recebe lista vazia, sem erro.
- Uma versão de outro proprietário devolvida pelo adapter não aparece no resultado do caso de uso.
- A operação não chama `atualizar` nem `salvar`.
- O adapter devolve agregados com as referências carregadas e usa uma consulta de versões e uma de seleções.
- A rota responde 200 e 503 conforme o contrato; nenhuma entidade de domínio é exposta.
- A suíte unitária do ambiente `backend` e o `ruff check` passam, sem banco, rede ou relógio reais.

## Restrições aplicáveis

- Domain não depende de Application, Infrastructure, API ou ORM; Application não depende de Infrastructure nem da API; regras de negócio não ficam em controllers nem repositórios (`src/backend/AGENTS.md`).
- Portas pertencem à camada interna e são implementadas por adapters; a composição ocorre na camada externa (`src/backend/AGENTS.md`).
- Entradas externas viram DTOs antes do caso de uso; entidades de domínio não são expostas pela API (`src/backend/AGENTS.md`).
- Testes unitários no ambiente `backend`, com doubles; docstring (o que faz, como faz, finalidade) em toda função e classe (`AGENTS.md`).
- Núcleo antes dos adapters; adapter não cria porta nem regra; testes de rota substituem o caso de uso por double; proveniência em todo trecho novo (skills de implementação).
- O CI executa `ruff check` com as regras `F` e `I` (ordem e uso de imports) além da suíte unitária.
- Propriedade do recurso verificada e acesso a recurso de outro usuário negado (RNF04, RF13).

## Classificação comentada

- `sphere: engineering`: construção técnica de funcionalidade prevista em RF14 e RF15.
- `concerns: domain, data, security`: leitura em lote do agregado com suas referências; o erro mais grave seria listar versões de terceiros.
- `decision_kind: design`, `scope: component`, `lifecycle: delivery`, `urgency: normal`.
- `uncertainty: medium`: o texto da issue não foi lido e a forma da resposta é hipótese.
- `reversibility: easy`: é uma consulta sem migration; o contrato da resposta ainda não tem cliente.
- `risk: medium`: a gravidade de listar versões alheias é alta, mas a defesa em profundidade (H8) e a ausência de composição real a reduzem.

## Decisão de roteamento

Roteada para `prompts/backend`, pasta das análises relacionadas de versões de currículo. Candidatas: `prompts/backend` e `prompts/requisitos`; esta foi descartada porque a análise não levanta nem refina requisitos. Confiança alta. Não há `AGENTS.md` ou `AGENTS.override.md` específico em `prompts/` (verificado em análises anteriores; não refeito aqui).

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `security` | 1 | Nenhuma versão de outro estudante aparece | RNF04 e RF13 |
| `correctness` | 1 | Agregados completos e ordem determinística | Evita seleção apagada se o agregado for reaproveitado |
| `simplicity` | 2 | PR revisável, sem refatorar o domínio | Preferência do usuário por entregas menores |
| `modifiability` | 2 | Contrato permite paginação e novos campos | O cliente e a tarefa de exclusão evoluirão |
| `performance` | 3 | Sem consulta por versão | Evita N+1 sem otimização prematura |

## Alternativas consideradas

**Estado atual.** O repositório só obtém uma versão por identidade; não existe forma de listar as versões de um estudante.

**Alternativa A — Estender `RepositorioCurriculo` com `listar_por_usuario` (recomendada).** Application: método na porta, `ListarVersoesCurriculoEntrada` e `ListarVersoesCurriculo`, que filtra por proprietário e ordena. Infrastructure: método no adapter com duas consultas (versões e seleções) reutilizando `para_curriculo`. Interface: `GET .../curriculos` em módulo próprio.

**Alternativa B — Porta de leitura separada, com modelo de leitura leve.** Nova porta `ConsultaVersoesCurriculo.listar_por_usuario` devolvendo resumos (id, título, layout, visibilidade, contagem), com uma consulta agregada e sem reconstruir agregados. Menos dados lidos e leitura independente do agregado, mas adiciona porta, tipo de resumo e consulta própria, sem reaproveitar os mapeadores.

**Alternativa C — Listar na camada de API chamando o repositório.** Elimina o caso de uso, mas faz a API acessar persistência e decidir propriedade e ordem. É inviável por restrição de arquitetura.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `security` | 1 | +1 | +1 | -2 | média | A e B filtram no caso de uso; C deixa a decisão na borda |
| `correctness` | 1 | +1 | 0 | -1 | média | A mantém o contrato de agregado completo; B devolve resumos sem agregado; C não tem teste de fluxo |
| `simplicity` | 2 | +1 | -1 | +1 | média | B soma uma porta e um tipo; C não cria caso de uso |
| `modifiability` | 2 | 0 | +1 | -2 | baixa | B isola o modelo de leitura; C engessa a API |
| `performance` | 3 | 0 | +1 | 0 | baixa | B evita carregar linhas de seleção quando a contagem basta, mas a diferença é pequena para poucas versões |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**, em três etapas na mesma branch: (1) Application, com o método na porta, a entrada e o caso de uso, mais testes com a porta substituída por double; (2) Infrastructure, com o método no adapter e seus testes com sessão simulada; (3) Interface, com a rota, os DTOs e o registro em `factory.py`, mais testes com o caso de uso substituído por double. A resposta traz o resumo da versão (H2), em lista vazia quando não há versões (H7). O status é `proposed`: a decisão exige aprovação humana, em especial sobre as perguntas 1 e 2.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `security` | prioritized | Versão de outro estudante nunca é listada | Teste do caso de uso com versões de proprietários diferentes |
| `correctness` | prioritized | Agregados completos e ordem estável | Testes do adapter para reconstrução das referências e do caso de uso para a ordem |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | PR revisável, sem refatorar o domínio | Um método de porta, um caso de uso, um método de adapter e uma rota |
| `modifiability` | Contrato extensível | Envelope `{"versoes": [...]}` aceita paginação futura |
| `performance` | Sem consulta por versão | Duas consultas fixas no adapter |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `security` | Versões de outro estudante exibidas na lista | Alta | Estudantes donos das versões |
| `correctness` | Agregado sem referências devolvido pela listagem e depois reaproveitado em edição, apagando a seleção | Alta | Estudantes donos das versões |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `correctness` | A listagem carrega as linhas de seleção, mesmo que só a contagem seja exibida | `performance` | Aceitável: uma consulta extra, com poucas versões por estudante |
| `simplicity` | Sem paginação, filtros nem ordenação por data | `user-value` | Aceitável nesta fatia; sujeito às perguntas 3 e 5 |
| `simplicity` | Alteração da porta `RepositorioCurriculo`, tocando um contrato compartilhado | `modifiability` | Aceitável: o único adapter é o SQLAlchemy e os doubles dos testes não precisam do método novo |

## Riscos e efeitos de segunda ordem

- **Conflito com a tarefa 115.** Exclusão e listagem alteram a mesma porta, o mesmo adapter e os mesmos testes de infraestrutura. Mitigação: conflito aditivo, resolvido ao integrar a `dev` após a primeira a ser aceita.
- **Conflito com a tarefa 120.** Ambas alteram `application/__init__.py` e `api/factory.py`. Mitigação: idem.
- **Protocol sem o método até a Etapa 2.** O adapter herda de `RepositorioCurriculo`; entre a Etapa 1 e a Etapa 2, uma chamada a `listar_por_usuario` no adapter devolveria `None` em silêncio. Mitigação: nada chama a listagem em produção antes da Etapa 3 e da composição; as etapas vão no mesmo pull request.
- **Estudante inexistente indistinguível de estudante sem versões.** Escolha deliberada (H7); pode dificultar depuração de cliente.
- **Ordem por título.** Sem data de criação, a ordem pode surpreender; ver pergunta 3.
- **Volume.** Sem paginação, uma conta com muitas versões carregaria todas. Mitigação: envelope extensível e nova decisão quando houver volume.
- **Dados pessoais.** A resposta contém apenas dados da própria versão; rota restrita ao dono por path, sem autenticação ainda (handoff).

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| A listagem é somente leitura | `atualizar` e `salvar` nunca chamados | Teste do caso de uso com spy | Qualquer escrita observada |
| Só versões do solicitante aparecem | Versão de outro proprietário descartada | Teste do caso de uso com spy que devolve versões misturadas | Versão alheia presente |
| Ordem determinística | Mesma saída para entradas em ordens diferentes | Teste do caso de uso | Saída dependente da ordem do repositório |
| Sem versões produz lista vazia | Resultado vazio sem erro | Teste do caso de uso | Falha ou `None` |
| O adapter carrega referências em lote | Agregados com referências; duas consultas | Teste do adapter com sessão simulada | Consulta por versão ou agregados sem referências |
| A rota traduz o resultado | 200 com envelope, 503 sem executor | Teste da rota com double do caso de uso | Status ou formato diferente do contrato |
| Funciona em banco real | Consultas com `IN` e agrupamento | Teste de integração no ambiente `tests` | Divergência entre adapter e banco |

## Handoffs e atividades posteriores

- **`$backend-domain-orchestration-v2`:** método `listar_por_usuario` na porta, `ListarVersoesCurriculoEntrada`, caso de uso `ListarVersoesCurriculo` e testes unitários com a porta substituída por double.
- **`$backend-adapters-drivers-v2`:** implementação do método no adapter SQLAlchemy, módulo de rota, DTOs de resposta, registro em `factory.py` e testes unitários dessas unidades.
- **`$cross-cutting-implementation-v1`:** autenticação e autorização com identidade da sessão.
- **`$integration-system-testing-v1`:** testes de integração do adapter contra banco real.
- **Composição:** engine, sessão e transação; injeção do caso de uso.
- **Próximas fatias:** exclusão de versão (tarefa 115); paginação e filtros; data de criação e ordenação por recência (exige migration); prévia (tarefa 120).
- **Rastreabilidade:** conferir se os comentários `# Proveniência` do código usam o nome definitivo deste arquivo.

## Síntese

O agregado e o adapter já sabem carregar uma versão por identidade; falta a consulta por proprietário. A decisão estende a porta existente com `listar_por_usuario`, mantém o contrato de agregado completo, e coloca no caso de uso a garantia de que só aparecem versões do solicitante e de que a ordem é estável. A rota devolve um resumo por versão em um envelope extensível. A principal incerteza é o texto da issue, não lido, e a principal exigência de segurança é que nenhuma versão alheia apareça, o que o caso de uso garante mesmo se o adapter falhar.
