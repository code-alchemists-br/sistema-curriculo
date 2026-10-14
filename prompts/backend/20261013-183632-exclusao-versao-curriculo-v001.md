---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-13T18:36:32-03:00"
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
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "classe RepositorioCurriculo (obter_por_id, atualizar, salvar e listar_por_usuario) e GeradorCurriculoId"
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: partial
    - path: src/backend/application/versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 1-80 (CurriculoNaoEncontrado e caso de uso de edição)"
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: partial
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "modelos CurriculoRegistro e CurriculoItemRegistro (linhas 24-120)"
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: partial
    - path: src/backend/api/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 105-165 (criar_router e rota de edição)"
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: partial
    - path: src/backend/api/middleware_autenticacao.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: available
    - path: src/backend/domain/associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 1-60 (agregado de associação entre currículo e vaga)"
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: partial
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF02, RF12, RF14 e RF15; item sobre tratamento das associações ao excluir currículo (por busca textual)"
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: partial
    - path: prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: available
    - path: prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: available
    - path: .agents/skills/backend-domain-orchestration-v2/SKILL.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: available
    - path: .agents/skills/backend-adapters-drivers-v2/SKILL.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "fea8f24f505e9256de826f1ebcc8ceabe854ba03"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "O propósito é decidir a construção de uma fatia de backend (porta, caso de uso, adapter e rota) sobre o agregado Curriculo; a linhagem relacionada de versões de currículo está em prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, data, security]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: costly
  risk: medium
---

# Análise de decisão — exclusão de versão de currículo

## Solicitação original

Texto literal fornecido pelo usuário:

```text
os PR ja foram aceitos, estamos livres pra trabalhar, faz a 115, dos mesmos moldes, e depois me ajude a revisar o codigo
```

O título da tarefa, informado pelo usuário por captura de tela da lista de issues, é "Implementar exclusão de versão de currículo" (#115).

## Informações complementares

Insumos literais registrados na conversa (grafia preservada):

- Resposta do usuário sobre a ordem das tarefas restantes: a #115 foi indicada como a mais rápida pela assistente e o usuário pediu que ela fosse feita ("faz a 115, dos mesmos moldes").
- Sobre tarefas anteriores, tomado como preferência por entregas pequenas: "descricao menor, dá? to achando muito grande esse PR"
- Modo de trabalho combinado nas tarefas 117, 120 e 111: escrita direta, etapa por etapa, com o commit feito pelo usuário a cada etapa.
- O texto da issue #115 não foi lido: a GitHub CLI não está disponível neste ambiente e o usuário informou somente o título e o número.
- A base é a `dev` na cabeça `fea8f24`, que já contém a seleção de itens (#117), a prévia (#120), a listagem (#111) e o middleware de autenticação por sessão.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/application/ports.py` | primary | source-code | production | python | `RepositorioCurriculo` e `GeradorCurriculoId` | commit `fea8f24` |
| `src/backend/application/versao_curriculo.py` | primary | source-code | production | python | linhas 1-80 | commit `fea8f24` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py` | primary | source-code | production | python | arquivo inteiro | commit `fea8f24` |
| `src/backend/infrastructure/persistence/sqlalchemy/curriculo.py` | primary | source-code | production | python | modelos | commit `fea8f24` |
| `src/backend/api/versao_curriculo.py` | supporting | source-code | production | python | linhas 105-165 | commit `fea8f24` |
| `src/backend/api/middleware_autenticacao.py` | primary | source-code | production | python | arquivo inteiro | commit `fea8f24` |
| `src/backend/api/factory.py` | supporting | source-code | production | python | arquivo inteiro | commit `fea8f24` |
| `src/backend/domain/associacao_curriculo_vaga.py` | supporting | source-code | production | python | linhas 1-60 | commit `fea8f24` |
| `docs/requisitos_funcionais.md` | supporting | prose | documentation | markdown | RF02, RF12, RF14, RF15 e item de associações | commit `fea8f24` |
| `prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md` | supporting | prose | documentation | markdown | arquivo inteiro | commit `fea8f24` |
| `prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md` | supporting | prose | documentation | markdown | arquivo inteiro | commit `fea8f24` |
| `.agents/skills/backend-domain-orchestration-v2/SKILL.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `fea8f24` |
| `.agents/skills/backend-adapters-drivers-v2/SKILL.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `fea8f24` |
| `AGENTS.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `fea8f24` |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `fea8f24` |

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `fea8f24f505e9256de826f1ebcc8ceabe854ba03`, cabeça da `dev` na consulta, lido no working tree da branch `task-115`, criada a partir dela.
- Arquivos com recorte parcial sustentam somente os fatos dos trechos indicados.
- O texto da issue #115 não foi lido; seus critérios de aceite podem diferir das hipóteses abaixo.
- A inexistência de persistência para as associações entre currículo e vaga baseia-se na listagem dos modelos e das revisões do Alembic, vistas por nome de arquivo; o conteúdo dos modelos de sessão e experiência não foi lido.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md` e suas referências; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

O estudante consegue excluir uma versão de currículo própria, e a versão deixa de aparecer na listagem, na edição, na seleção de itens e na prévia. Versão inexistente ou de outro estudante é recusada sem efeito e sem revelar a diferença. A entrega atravessa Application, Infrastructure e Interface, com testes unitários.

### Atores e interesses

- **Estudante dono da versão:** remover versões que não usa mais (RF14, caso de uso "Gerenciar versões").
- **Outro estudante:** não pode excluir versão alheia (RNF04, RF13).
- **Equipe de associações currículo–vaga:** precisa definir o que acontece com associações quando o currículo é excluído (item em aberto nos requisitos).
- **Frontend:** consome a rota e atualiza a lista de versões.
- **Equipe de backend e líder técnico:** fronteiras entre camadas e tamanho do PR.

### Evidências e fatos observados

1. `RepositorioCurriculo` declara `obter_por_id`, `atualizar`, `salvar` e `listar_por_usuario`; não há operação de remoção (`src/backend/application/ports.py`).
2. As linhas de seleção de itens ficam em `curriculo_itens`, com chave estrangeira para `curriculos` (`fk_curriculo_itens_curriculo_id_curriculos`) e sem `ON DELETE CASCADE` declarado nos modelos lidos; portanto excluir uma versão com linhas de seleção exige apagá-las antes (`curriculo.py`, análise da tarefa 117).
3. A tabela `curriculos` não tem coluna de exclusão lógica (`deleted_at`); a exclusão lógica existe somente para usuário (`curriculo.py`, `domain/usuario.py`).
4. O adapter `atualizar` recarrega o registro por chave primária e falha com `LookupError` se ele não existe; a edição trata ausência e propriedade alheia como `CurriculoNaoEncontrado` (404) (`repositorio_curriculo.py`, `application/versao_curriculo.py`).
5. As rotas de versão vivem em `/estudantes/{usuario_id}/curriculos[/{curriculo_id}]` e o `PUT` da edição ocupa o caminho com `curriculo_id`; a exclusão pode usar o método `DELETE` no mesmo caminho (`api/versao_curriculo.py`).
6. O middleware de autenticação, quando instalado, exige sessão ativa em todas as rotas privadas e, para qualquer método sob `/estudantes/{uuid}/curriculos`, exige que o UUID da rota seja o do estudante autenticado (403 caso contrário); portanto a nova rota é protegida sem alterar handlers (`api/middleware_autenticacao.py`).
7. Existe agregado de associação currículo–vaga no domínio (`AssociacaoCurriculoVaga`), mas nenhuma persistência dele foi identificada; os requisitos listam como ponto em aberto o "tratamento das associações quando um currículo for excluído" (`docs/requisitos_funcionais.md`).
8. RF14 prevê excluir currículos e RF02 prevê consultar, editar e excluir as informações cadastradas.
9. As skills de implementação exigem núcleo antes dos adapters, adapter sem criar porta ou regra de negócio, testes de rota com o caso de uso substituído por double e comentário de proveniência em todo trecho novo; o CI roda `ruff check` (regras `F` e `I`) e a suíte unitária.

### Hipóteses

- **H1.** A exclusão é **física**: remove a versão e suas linhas de seleção; não há lixeira nem recuperação nesta fatia.
- **H2.** A porta ganha `excluir(curriculo)`, que recebe o agregado localizado pelo caso de uso, no mesmo estilo de `atualizar`.
- **H3.** Ordem no adapter: apagar as linhas de `curriculo_itens` da versão e, depois, a versão, com `flush` ao final e sem `commit`; o adapter falha com `LookupError` se a versão não existe mais, como em `atualizar`.
- **H4.** O caso de uso `ExcluirVersaoCurriculo` localiza a versão, trata ausência e propriedade alheia com a mesma falha `CurriculoNaoEncontrado`, e só então chama `excluir`; não devolve conteúdo.
- **H5.** A rota é `DELETE /estudantes/{usuario_id}/curriculos/{curriculo_id}`, em módulo próprio, respondendo 204; 404 para versão ausente ou alheia; 503 sem executor injetado. Excluir duas vezes resulta em 404 na segunda (não idempotente), coerente com a edição.
- **H6.** Sem regra de domínio nova: qualquer versão própria pode ser excluída, inclusive pública ou com itens selecionados.
- **H7.** O tratamento de associações com vagas é **handoff**: nenhuma persistência de associação existe; quando existir, a exclusão da versão precisará removê-las ou ser bloqueada (decisão da equipe de associações).
- **H8.** Sem migration: usa as tabelas existentes e a ordem de remoção resolve a chave estrangeira.

### Perguntas em aberto

1. Os critérios de aceite da issue #115 coincidem com H1 a H8?
2. A exclusão deve ser física (H1) ou lógica, com recuperação? Exclusão lógica exigiria coluna, migration e filtro em leitura e listagem.
3. Excluir versão que tem associações com vagas (futuro) deve apagar as associações ou ser recusado?
4. Excluir a última versão do estudante é permitido? (H6 assume que sim.)
5. A segunda exclusão deve ser 404 (H5) ou 204 idempotente?

### Escopo

- Método `excluir` na porta `RepositorioCurriculo`, entrada `ExcluirVersaoCurriculoEntrada` e caso de uso `ExcluirVersaoCurriculo`.
- Método correspondente no adapter SQLAlchemy, removendo linhas de seleção e versão.
- Rota `DELETE /estudantes/{usuario_id}/curriculos/{curriculo_id}`, executor, registro em `factory.py`.
- Testes unitários de cada camada com doubles.

### Fora do escopo

- Exclusão lógica, lixeira e recuperação; migration.
- Tratamento de associações currículo–vaga e de itens do perfil (a exclusão da versão não remove itens, que pertencem ao perfil).
- Composição de engine, sessão e transação reais; testes de integração com banco real.
- Alterações no middleware de autenticação.

### Critérios de sucesso

- Excluir uma versão própria remove a versão e suas linhas de seleção, e solicita a remoção uma única vez.
- Versão inexistente e versão de outro estudante geram a mesma falha, sem chamar `excluir`.
- O adapter apaga as linhas de seleção antes da versão e não faz commit; falhas de banco são propagadas.
- A rota responde 204, 404 e 503 conforme o contrato; nenhum dado é exposto.
- A suíte unitária do ambiente `backend` e o `ruff check` passam, sem banco, rede ou relógio reais.

## Restrições aplicáveis

- Domain não depende de Application, Infrastructure, API ou ORM; Application não depende de Infrastructure nem da API; regras de negócio não ficam em controllers nem repositórios (`src/backend/AGENTS.md`).
- Portas pertencem à camada interna e são implementadas por adapters; a composição ocorre na camada externa (`src/backend/AGENTS.md`).
- Persistência com ORM Code First; sem scripts SQL manuais; mapeamentos na infraestrutura (`src/backend/AGENTS.md`).
- Testes unitários no ambiente `backend`, com doubles; docstring (o que faz, como faz, finalidade) em toda função e classe (`AGENTS.md`).
- Núcleo antes dos adapters; adapter não cria porta nem regra; testes de rota substituem o caso de uso por double; proveniência em todo trecho novo (skills de implementação).
- O CI executa `ruff check` com as regras `F` e `I` além da suíte unitária.
- Propriedade do recurso verificada e acesso a recurso de outro usuário negado (RNF04, RF13).

## Classificação comentada

- `sphere: engineering`: construção técnica de funcionalidade prevista em RF14.
- `concerns: domain, data, security`: a operação é destrutiva e depende de ordem de remoção por causa da chave estrangeira; um erro de propriedade permitiria apagar versão alheia.
- `decision_kind: design`, `scope: component`, `lifecycle: delivery`, `urgency: normal`.
- `uncertainty: medium`: o texto da issue não foi lido e a política de exclusão (física ou lógica) é hipótese.
- `reversibility: costly`: a exclusão física não tem recuperação; migrar depois para exclusão lógica exigiria migration e ajuste das leituras.
- `risk: medium`: a gravidade de apagar versão alheia é alta, mas a verificação de propriedade no caso de uso e o middleware de autenticação a mitigam.

## Decisão de roteamento

Roteada para `prompts/backend`, pasta das análises relacionadas de versões de currículo. Candidatas: `prompts/backend` e `prompts/requisitos`; esta foi descartada porque a análise não levanta nem refina requisitos. Confiança alta. Não há `AGENTS.md` ou `AGENTS.override.md` específico em `prompts/` (verificado em análises anteriores; não refeito aqui).

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `security` | 1 | Só o dono exclui; ausência e posse alheia indistinguíveis | RNF04 e RF13; a operação é destrutiva |
| `correctness` | 1 | Remoção na ordem correta, sem violar a chave estrangeira nem deixar linhas órfãs | Integridade de `curriculo_itens` |
| `simplicity` | 2 | PR revisável, sem migration nem refatoração do domínio | Preferência do usuário por entregas menores |
| `modifiability` | 2 | Não impedir exclusão lógica ou tratamento de associações depois | Pontos em aberto nos requisitos |
| `time-to-value` | 3 | Entrega em três etapas testáveis | Fatias verticais com revisão por camada |

## Alternativas consideradas

**Estado atual.** Há criação, edição, seleção de itens, listagem e prévia, mas nenhuma forma de remover uma versão.

**Alternativa A — Exclusão física com remoção explícita das linhas de seleção (recomendada).** Application: `excluir(curriculo)` na porta e `ExcluirVersaoCurriculo`. Infrastructure: apagar `curriculo_itens` da versão e depois a versão, com `flush`. Interface: `DELETE .../curriculos/{curriculo_id}`, 204/404/503. Sem migration.

**Alternativa B — Exclusão lógica.** Acrescentar `deleted_at` (ou `excluida`) a `curriculos`, migration, filtro em `obter_por_id` e `listar_por_usuario`, e método de domínio de exclusão. Permite recuperação e preserva futuras associações, mas altera leituras já entregues, o esquema e o domínio, e aumenta o PR.

**Alternativa C — Exclusão física confiando em `ON DELETE CASCADE`.** Acrescentar a cascata à chave estrangeira por migration e apagar somente a versão. Menos código no adapter, mas altera o esquema aprovado, depende do banco para a regra e não é verificável por testes unitários.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `security` | 1 | +1 | +1 | +1 | média | As três verificam a propriedade no caso de uso |
| `correctness` | 1 | +1 | +1 | 0 | média | A e B têm a ordem de remoção ou a ocultação verificáveis em teste unitário; C delega ao banco |
| `simplicity` | 2 | +1 | -2 | 0 | média | B muda esquema, domínio e leituras; C exige migration; A não toca o esquema |
| `modifiability` | 2 | 0 | +1 | -1 | baixa | B abre espaço para recuperação; C prende a regra ao banco |
| `time-to-value` | 3 | +1 | -1 | 0 | média | A é a menor entrega testável |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**, em três etapas na mesma branch: (1) Application, com `excluir` na porta, a entrada e o caso de uso, mais testes com a porta substituída por double; (2) Infrastructure, com o método no adapter e seus testes com sessão simulada; (3) Interface, com a rota `DELETE`, o executor e o registro em `factory.py`, mais testes com o caso de uso substituído por double. O tratamento de associações com vagas fica como handoff (H7). O status é `proposed`: a decisão exige aprovação humana, em especial sobre as perguntas 1, 2 e 3.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `security` | prioritized | Versão alheia nunca é excluída | Teste do caso de uso com versão de outro proprietário, sem chamada a `excluir` |
| `correctness` | prioritized | Linhas de seleção removidas antes da versão | Teste do adapter que registra a ordem das chamadas à sessão |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | PR revisável, sem migration | Um método de porta, um caso de uso, um método de adapter e uma rota |
| `time-to-value` | Cada etapa testável isoladamente | Etapas por camada com suíte própria |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `security` | Versão de outro estudante apagada | Alta | Estudantes donos das versões |
| `correctness` | Violação da chave estrangeira ou linhas de seleção órfãs | Média | Estudantes e equipe de backend |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | Exclusão irreversível, sem lixeira | `user-value` | Aceitável nesta fatia; sujeito à pergunta 2 |
| `simplicity` | Associações currículo–vaga ficam sem tratamento | `correctness` | Aceitável porque nenhuma persistência de associação existe ainda; handoff registrado |
| `simplicity` | Segunda exclusão responde 404 | `user-value` | Aceitável por coerência com a edição; sujeito à pergunta 5 |

## Riscos e efeitos de segunda ordem

- **Perda de dados definitiva.** Sem recuperação, uma exclusão por engano é irreversível. Mitigação: a confirmação é responsabilidade do cliente; avaliar exclusão lógica se o requisito aparecer.
- **Associações futuras.** Quando a persistência de associações existir, excluir a versão pode deixar associações órfãs ou violar chave estrangeira. Mitigação: handoff e revisão desta decisão.
- **Chave estrangeira.** Se a ordem de remoção estiver errada, o banco recusa a exclusão. Mitigação: teste da ordem no adapter; teste de integração em banco real como handoff.
- **Condição de corrida.** Duas exclusões simultâneas: a segunda falha com `LookupError` no adapter, hoje sem tradução. Mitigação: aceitável nesta fatia; tratar na composição.
- **Conflito com outras tarefas.** Outras tarefas alteram `ports.py`, `application/__init__.py` e `api/factory.py`. Mitigação: conflito aditivo, resolvido ao integrar a `dev`.
- **Composição.** Sem composição real, a rota responde 503 no app completo.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Só o dono exclui | `excluir` não é chamado para versão ausente ou alheia | Teste do caso de uso com spy | Qualquer exclusão observada |
| Exclusão solicitada uma vez para versão própria | Uma chamada a `excluir` com o agregado | Teste do caso de uso com spy | Zero ou mais de uma chamada |
| Linhas de seleção antes da versão | Ordem das chamadas à sessão | Teste do adapter com sessão simulada | Versão removida antes das linhas |
| Versão inexistente no adapter falha | `LookupError` e nenhuma remoção | Teste do adapter | Remoção silenciosa |
| Rota traduz o resultado | 204, 404 e 503 | Teste da rota com double do caso de uso | Status diferente do contrato |
| Funciona em banco real | Remoção respeitando a chave estrangeira | Teste de integração no ambiente `tests` | Violação de chave ou linhas órfãs |

## Handoffs e atividades posteriores

- **`$backend-domain-orchestration-v2`:** `excluir` na porta, `ExcluirVersaoCurriculoEntrada`, caso de uso `ExcluirVersaoCurriculo` e testes unitários com a porta substituída por double.
- **`$backend-adapters-drivers-v2`:** método no adapter SQLAlchemy, módulo de rota, executor, registro em `factory.py` e testes unitários dessas unidades.
- **Equipe de associações currículo–vaga:** decidir e implementar o tratamento das associações quando um currículo é excluído, quando houver persistência.
- **`$integration-system-testing-v1`:** teste de integração da exclusão contra banco real, incluindo a ordem da chave estrangeira.
- **Composição:** engine, sessão, transação e injeção do caso de uso.
- **Próximas fatias:** exclusão lógica com recuperação, se for requisito; tradução da falha de corrida em erro de negócio.
- **Rastreabilidade:** conferir se os comentários `# Proveniência` do código usam o nome definitivo deste arquivo.

## Síntese

A versão já pode ser criada, editada, listada e ter itens selecionados, mas não removida. A decisão acrescenta `excluir` à porta existente e mantém a regra de propriedade no caso de uso, com a mesma falha para ausência e posse alheia; o adapter remove as linhas de seleção antes da versão para respeitar a chave estrangeira, sem migration; a rota `DELETE` herda a proteção do middleware de autenticação. A principal incerteza é a política de exclusão, física ou lógica, e a principal pendência externa é o tratamento das associações com vagas, que ainda não têm persistência.
