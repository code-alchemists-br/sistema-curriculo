---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v002"
status: proposed
created_at: "2026-10-18T21:05:35-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261017-223527-atualizacao-classificacoes-associacao-curriculo-vaga-v001.md
  supersedes: prompts/backend/20261017-223527-atualizacao-classificacoes-associacao-curriculo-vaga-v001.md
  change_type: reassessment
  secondary_change_types: [correction, enrichment]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: "code-alchemists-br/sistema-curriculo#132"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: selected-section
      locator: "título, corpo e estado consultados via gh issue view"
      content_state: external
      revision: "consulta em 2026-10-18; issue aberta"
      availability: available
    - path: "Solicitação do usuário — revisão técnica para #132"
      relationship: primary
      representation: prose
      function: documentation
      format: mensagem de usuário
      analysis_scope: whole-file
      locator: "solicitação, regras de negócio, escopo e entregável desta revisão"
      content_state: external
      revision: "entrada desta versão"
      availability: available
    - path: "code-alchemists-br/sistema-curriculo#541"
      relationship: supporting
      representation: prose
      function: documentation
      format: GitHub pull request
      analysis_scope: metadata-only
      locator: "estado, base, branch e data de merge consultados via gh pr view"
      content_state: external
      revision: "consulta em 2026-10-18; merged em 2026-10-18"
      availability: available
    - path: prompts/backend/20261017-223527-atualizacao-classificacoes-associacao-curriculo-vaga-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "solicitação, artefatos, propostas, pendências, HTTP, persistência e handoff"
      content_state: working-tree
      revision: "arquivo não rastreado, lido no estado atual do workspace"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: selected-section
      locator: "restrições gerais, Nix, escopo e documentação"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: prompts/README.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: "organização e finalidade das subpastas"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF12, RN02-RN04 e detalhamentos ainda necessários"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: docs/matriz_testes.md
      relationship: supporting
      representation: prose
      function: test
      format: Markdown
      analysis_scope: selected-section
      locator: "CT-RF12-01..09, CT-RF12-C01..C07 e autenticação relacionada"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RNF04 e RNF05"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: docs/Arquitetura/ADR-002-autenticacao-autorizacao-propriedade.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "identidade autenticada, propriedade, local da verificação, falhas e verificações"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: docs/contrato-credenciais-sessao.md
      relationship: supporting
      representation: prose
      function: schema-contract
      format: Markdown
      analysis_scope: selected-section
      locator: "identidade em request.state, comportamento HTTP e testes de rotas protegidas"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: docs/configuracao-ambiente.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "DATABASE_URL e PostgreSQL"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/domain/associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "enum, agregado, invariantes, normalização e adição"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/application/associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "entrada, criação, ownership, duplicidade e persistência"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioCurriculo e RepositorioAssociacaoCurriculoVaga"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/application/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "CurriculoNaoEncontrado usado pelo fluxo de propriedade"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "map classes, PKs e conversões de/para o agregado"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "consulta pelo par, salvamento, flush e ausência de commit"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261017_0004_criar_associacoes_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python/Alembic
      analysis_scope: whole-file
      locator: "schema e constraints da associação e de suas classificações"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/api/middleware_autenticacao.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "autenticação por cookie, request.state e checagem de rotas de currículo"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/api/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "obter_principal e tratamento de identidade na borda HTTP"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "injeção do autenticador e registro dos routers; ausência de router de associação"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/main.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "engine/readiness e autenticador indisponível fornecido à aplicação padrão"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/tests/test_domain_associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: "invariantes atuais e ausência de testes de remoção"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/tests/test_application_associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "criação, propriedade, ausência, duplicidade e doubles dos repositórios"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/tests/test_infrastructure_repositorio_associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "consultas, conversões, flush, colisões e ausência de commit"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/tests/test_persistencia_associacao_curriculo_vaga_integracao.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "round-trip, duplicidade e rollback em SQLite"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/tests/test_integracao_recusa_curriculo_alheio.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "padrão de integração entre middleware, autorização, executores e snapshots de persistência"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/tests/test_api_middleware_autenticacao.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "401 sem sessão, 403 por UUID de currículo alheio e identidade em request.state"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/tests/test_api_perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "principal ausente, recurso próprio e autorização de outro estudante"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
    - path: src/backend/tests/test_api_formacao_academica.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "principal obtido de request.state e tradução de domínio para 422"
      content_state: commit
      revision: "26dc294e1a0b74a1149d765e8248332203f3748b"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories:
    - prompts/backend
    - prompts/requisitos
    - prompts/revisao
    - prompts/ambientes
    - prompts/frontend
    - prompts/templates
  confidence: high
  rationale: "Revisão da mesma linhagem, cujo objeto é a implementação no Domain, Application e persistência do backend."
classification:
  sphere: engineering
  concerns: [domain, architecture, security]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: high
---

# Análise de decisão — Atualização de classificações da associação currículo-vaga (#132)

## Solicitação original

> Faça uma análise decisória exclusivamente para a issue #132:
>
> "Implementar atualização de classificações da associação currículo-vaga"
>
> NÃO implemente código.
> NÃO altere código existente.
> NÃO faça commit.
> NÃO faça push.
> NÃO redesenhe a arquitetura.
>
> CONTEXTO
>
> A issue #131 já definiu e implementou o Domain de associação currículo-vaga:
>
> - `AssociacaoCurriculoVaga`
> - `ClassificacaoAssociacao`
> - `VagaId`
> - regra `CANDIDATURA => INTERESSE`
> - classificações sem duplicação
> - associação exige pelo menos uma classificação
>
> A issue #130 está implementada no PR #541 e definiu:
>
> - uma única associação por `(curriculo_id, vaga_id)`;
> - chave composta `(curriculo_id, vaga_id)`;
> - criação duplicada rejeitada;
> - alterações posteriores das classificações pertencem à #132;
> - port/repository de associação já existe na implementação da #130.
>
> Use como contexto autoritativo da #130:
>
> `prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md`
>
> OBJETIVO
>
> Determinar exatamente o comportamento da atualização das classificações de uma associação já existente.
>
> Primeiro investigue no repositório:
>
> - requisitos funcionais;
> - matriz de testes;
> - prompts anteriores;
> - documentação;
> - Domain atual;
> - Application existente;
> - issue #132;
> - referências cruzadas às issues #130, #131 e #132.
>
> Consulte também:
>
> `gh issue view 132 --repo code-alchemists-br/sistema-curriculo`
>
> QUESTÕES QUE A ANÁLISE DEVE RESPONDER
>
> 1. Qual deve ser o comando/caso de uso de atualização?
>
> 2. A atualização opera:
>    - substituindo o conjunto completo de classificações;
>    - adicionando/removendo individualmente;
>    - ou existem comandos separados?
>
> 3. O que acontece ao adicionar uma classificação que já existe?
>
> 4. O que acontece ao remover uma classificação que não existe?
>
> 5. O que acontece ao tentar remover `INTERESSE` quando a associação contém `CANDIDATURA`?
>
> 6. A operação deve rejeitar qualquer estado final em que exista:
>    `CANDIDATURA` sem `INTERESSE`?
>
> 7. O que acontece ao tentar remover a última classificação da associação?
>
> 8. A associação pode permanecer sem classificações?
>    Confronte isso com o Domain da #131.
>
> 9. Como identificar a associação?
>    Considere a decisão da #130 de chave composta:
>    `(curriculo_id, vaga_id)`.
>
> 10. Como validar ownership?
>      O estudante deve poder alterar somente associações pertencentes aos
>      seus próprios currículos.
>
> 11. Qual comportamento para:
>     - currículo inexistente;
>     - currículo de outro usuário;
>     - associação inexistente?
>
> 12. Quais erros pertencem ao Domain e quais pertencem à Application?
>
> 13. Quais traduções HTTP são coerentes com os padrões existentes do projeto?
>
> 14. Quais mudanças são necessárias no port/repository criado pela #130?
>
> 15. É necessário carregar e reconstruir `AssociacaoCurriculoVaga` para
>     executar a alteração, evitando reproduzir regras de Domain na Application?
>
> 16. Como garantir persistência atômica das classificações?
>
> 17. Existe algum risco de concorrência relevante?
>
> IMPORTANTE
>
> Não invente requisitos silenciosamente.
>
> Para cada decisão:
>
> - diferencie evidência explícita;
> - inferência arquitetural;
> - decisão ainda ausente.
>
> Se alguma regra não estiver documentada, proponha a alternativa mais coerente
> com o Domain e a divisão das issues, mas marque claramente como decisão proposta.
>
> PREFERÊNCIAS DE MODELAGEM A SEREM AVALIADAS, NÃO ASSUMIDAS
>
> Considere especialmente se é mais coerente:
>
> - rejeitar remoção de `INTERESSE` enquanto houver `CANDIDATURA`;
> - rejeitar remoção da última classificação;
> - tratar adição de classificação já existente como idempotente;
> - tratar remoção de classificação inexistente como idempotente ou erro.
>
> Não aceite essas opções automaticamente. Confronte-as com os requisitos e padrões do projeto.
>
> ESCOPO
>
> A #132 NÃO deve:
>
> - criar novas associações;
> - alterar a unicidade definida na #130;
> - implementar busca de vagas;
> - integrar Grupo 2;
> - alterar autenticação;
> - implementar histórico das issues futuras;
> - remover a regra `CANDIDATURA => INTERESSE`.
>
> SAÍDA
>
> Gere uma nova análise versionada em `prompts/backend/`.
>
> A análise deve terminar com:
>
> - decisão recomendada;
> - regras de negócio consolidadas;
> - fluxo de Application;
> - mudanças necessárias em ports/repository;
> - erros esperados;
> - traduções HTTP;
> - testes necessários;
> - pendências reais, se existirem;
> - handoff claro para implementação.
>
> Não implemente código nesta etapa.

## Informações complementares

### Entrada desta revisão — texto literal do usuário

> Estamos na branch `feature/132-atualizacao-classificacoes-associacao`, criada a partir da versão atualizada de `dev`.
>
> Quero preparar a implementação da tarefa #132, que trata da atualização das classificações de uma associação entre currículo e vaga.
>
> **Nesta etapa, faça somente a análise técnica. Não implemente código e não altere arquivos de produção ou testes.**
>
> Leia a análise existente:
>
> `prompts/backend/20261017-223527-atualizacao-classificacoes-associacao-curriculo-vaga-v001.md`
>
> Em seguida, valide suas decisões contra o estado atual do repositório, especialmente:
>
> - O agregado de domínio `AssociacaoCurriculoVaga` e o enum `ClassificacaoAssociacao`.
> - O caso de uso e o repositório implementados na tarefa #130.
> - O mapeamento SQLAlchemy e a migração da associação.
> - `docs/Arquitetura/ADR-002-autenticacao-autorizacao-propriedade.md`.
> - `docs/contrato-credenciais-sessao.md`.
> - `src/backend/api/middleware_autenticacao.py`.
> - Os padrões atuais de autorização, tratamento de erros e testes de integração.
>
> ### Regras de negócio que precisam ser respeitadas
>
> 1. Uma associação é identificada pelo par `(curriculo_id, vaga_id)`.
> 2. `CANDIDATURA` implica `INTERESSE`.
> 3. Adicionar uma classificação já existente deve ser idempotente.
> 4. Remover uma classificação inexistente deve ser idempotente.
> 5. Remover `CANDIDATURA` deve preservar `INTERESSE`.
> 6. Não deve ser permitido remover `INTERESSE` enquanto `CANDIDATURA` estiver presente.
> 7. Não deve ser permitido deixar uma associação sem classificações.
> 8. Somente o proprietário do currículo pode modificar a associação.
> 9. A identidade do usuário deve vir do mecanismo de autenticação existente, sem confiar em um `usuario_id` enviado pelo cliente.
> 10. A implementação deve respeitar a arquitetura existente e evitar duplicação de regras de negócio.
>
> ### Entregável
>
> Compare a análise v001 com o código e a documentação atuais. Identifique decisões desatualizadas, dependências já resolvidas, arquivos que precisam ser alterados, testes necessários e eventuais impedimentos reais.
>
> Crie uma nova versão da análise, **v002**, em `prompts/backend/`, seguindo o padrão de nomes e o histórico de versões do projeto. Não sobrescreva a v001.
>
> Não invente contratos de API nem crie uma nova infraestrutura de autenticação. Se algum detalhe não puder ser confirmado pelo repositório, registre-o como pendência explícita.
>
> Ao terminar, apresente um resumo das decisões atualizadas e o caminho do arquivo v002 criado. Não execute a implementação nesta etapa.

### Estado da issue e do código no momento desta revisão

- A issue #132 permanece aberta e seu corpo atual contém somente o título da tarefa e a instrução genérica de implementar a fatia vertical com testes unitários pertinentes; não define rota, método HTTP, payload nem códigos de sucesso.
- O PR #541 que implementa a criação da associação está **merged**. O checkout está no commit `26dc294e1a0b74a1149d765e8248332203f3748b`, merge do PR, na branch declarada pelo usuário. Assim, a dependência de #130 deixou de ser uma implementação pendente.
- A v001 estava não rastreada no workspace e foi preservada. Ela registra como base técnica um commit anterior à integração da #130 e trata várias regras agora informadas pelo usuário como propostas em aberto.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Estado da #130/#541 | A v001 registrou #130/PR #541 como abertos no momento da consulta e tratou a implementação como dependência contextual | PR #541 está merged e o caso de criação, port, adapter, mapping e migration estão no commit-base atual | O estado atual do repositório substitui a observação histórica da v001 | Decisão para #132 parte de implementação concreta e existente |
| Regras de idempotência e remoção | Adição repetida, remoção ausente, remoção de interesse com candidatura e remoção da última eram propostas pendentes | O usuário exige idempotência, proibição de quebrar `CANDIDATURA => INTERESSE` e proibição de associação vazia | Entrada complementar explícita desta revisão | Decisões de domínio deixam de depender de aprovação futura de produto |
| Autenticação | A v001 dizia que não havia identidade autenticada comum disponível para expor a operação | ADR, contrato de sessão, middleware, `request.state.usuario_id` e testes de principal/autorização estão presentes; porém `main.app` ainda recebe `AutenticadorSessaoIndisponivel` | Infraestrutura de autenticação existe, mas a composição operacional padrão não a ativa com um autenticador funcional | Não criar infraestrutura; identidade da futura borda deve ser a identidade validada pelo middleware; a exposição por HTTP continua condicionada |
| Interface HTTP | A v001 vinculou a ausência de API à ausência de autenticação | Não há router de associação em `api/factory.py` e a issue não define contrato HTTP | Separar a pendência de contrato da existência do mecanismo de identidade | Não definir rota, verbo, corpo nem resposta; uma API utilizável depende de decisão explícita e composição funcional |
| Banco e transação | A v001 declarou o banco-alvo desconhecido e a composição transacional não localizada | A documentação de ambiente identifica PostgreSQL; o adapter atual faz `flush` sem commit e a composição padrão examinada não injeta repositories/casos de uso ou boundary transacional da associação | Evidência atual mais específica | Banco-alvo conhecido, mas atomicidade de produção e lock de concorrência ainda dependem de um boundary transacional não demonstrado |
| Schema e migration | Mudanças de classificação poderiam parecer exigir schema novo | As tabelas, PKs compostas e FK já suportam linhas de classificações por associação | Revisão do mapping e migration da #130 | Não há mudança de schema necessária para adicionar/remover valores já representáveis |
| Artefatos | A v001 analisou o checkout anterior à integração do PR #541 | Esta revisão leu os arquivos rastreados no commit `26dc294...`, mais ADR, contrato de sessão, middleware, composição, padrões de testes e issue atual | A branch foi atualizada | Reavaliação técnica; nenhum arquivo de produção ou teste foi alterado |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `code-alchemists-br/sistema-curriculo#132` | Primário | prose | documentation | GitHub issue | Título, corpo e estado | Externo; aberta na consulta atual |
| `code-alchemists-br/sistema-curriculo#541` | Apoio | prose | documentation | GitHub pull request | Estado, base, head e merge | Externo; merged para `dev` |
| Solicitação do usuário para revisão técnica | Primário | prose | documentation | Mensagem | Texto literal preservado acima, incluindo as dez regras | Externo; entrada desta versão |
| `prompts/backend/20261017-223527-atualizacao-classificacoes-associacao-curriculo-vaga-v001.md` | Primário | prose | documentation | Markdown | Solicitação, hipóteses, propostas, alternativas e handoff | Working tree, não rastreado |
| `AGENTS.md` e `src/backend/AGENTS.md` | Contexto | prose | prompt-instruction | Markdown | Regras gerais e arquitetura/testes backend | Commit `26dc294...` |
| `docs/requisitos_funcionais.md`, `docs/requisitos_nao_funcionais.md` e `docs/matriz_testes.md` | Apoio | prose | documentation/test | Markdown | RF12, RN03, RNF04/RNF05, CT-RF12 e detalhamentos pendentes | Commit `26dc294...` |
| `src/backend/domain/associacao_curriculo_vaga.py` e `src/backend/tests/test_domain_associacao_curriculo_vaga.py` | Apoio | source-code | production/test | Python | Agregado, enum, invariantes e testes atuais | Commit `26dc294...` |
| `src/backend/application/associacao_curriculo_vaga.py`, `src/backend/application/ports.py`, `src/backend/application/versao_curriculo.py` e `src/backend/tests/test_application_associacao_curriculo_vaga.py` | Apoio | source-code | production/test/schema-contract | Python | Caso de criação, contracts, ownership e exceção de currículo ausente | Commit `26dc294...` |
| `src/backend/infrastructure/persistence/sqlalchemy/associacao_curriculo_vaga.py`, `src/backend/infrastructure/persistence/sqlalchemy/repositorio_associacao_curriculo_vaga.py` e `src/backend/infrastructure/persistence/alembic/versions/20261017_0004_criar_associacoes_curriculo_vaga.py` | Apoio | source-code | production | Python/Alembic | Mapping, adapter e schema atual | Commit `26dc294...` |
| `src/backend/tests/test_infrastructure_repositorio_associacao_curriculo_vaga.py` e `src/backend/tests/test_persistencia_associacao_curriculo_vaga_integracao.py` | Apoio | source-code | test | Python | Contrato do adapter, round-trip, constraints e rollback | Commit `26dc294...` |
| `docs/Arquitetura/ADR-002-autenticacao-autorizacao-propriedade.md`, `docs/contrato-credenciais-sessao.md` e `src/backend/api/middleware_autenticacao.py` | Apoio | prose/source-code | documentation/schema-contract/production | Markdown/Python | Principal autenticado, ownership e comportamento de falhas | Commit `26dc294...` |
| `src/backend/api/perfil_estudante.py`, `src/backend/api/factory.py` e `src/backend/main.py` | Apoio | source-code | production | Python | Extração de principal, registro de routers e composição ativa | Commit `26dc294...` |
| `src/backend/tests/test_api_middleware_autenticacao.py`, `src/backend/tests/test_api_perfil_estudante.py`, `src/backend/tests/test_api_formacao_academica.py` e `src/backend/tests/test_integracao_recusa_curriculo_alheio.py` | Apoio | source-code | test | Python | Padrões HTTP/auth, principal, status e integração com propriedade | Commit `26dc294...` |
| `docs/configuracao-ambiente.md` | Contexto | prose | documentation | Markdown | URL de banco e PostgreSQL | Commit `26dc294...` |
| `prompts/README.md` | Contexto | prose | documentation | Markdown | Organização e finalidade das pastas de prompts | Commit `26dc294...` |

### Limites da evidência dos artefatos

- O corpo atual da issue #132 só confirma a tarefa e a exigência geral de testes unitários. As dez regras desta versão são requisitos explícitos da mensagem do usuário, não texto da issue.
- O ADR-002 permite que negação de propriedade use 403 ou 404 conforme o contrato, desde que a política da operação seja consistente. Não há contrato HTTP de associação que resolva essa escolha.
- A autenticação por sessão, o middleware e os contratos estão implementados e testados; contudo, `src/backend/main.py` fornece à aplicação padrão `AutenticadorSessaoIndisponivel`. Logo, existência do mecanismo não comprova que uma rota de associação pudesse autenticar usuários na composição padrão atual.
- A documentação de configuração define PostgreSQL como banco configurável; os testes de persistência da associação usam SQLite em memória. Não foi executado teste contra PostgreSQL nesta análise.
- O adapter de associação atual não faz commit nem rollback. A composição de transação do fluxo de atualização não está presente na factory examinada; a atualização atômica em produção precisa respeitar um boundary transacional que ainda não está demonstrado.
- A leitura de `prompts/backend/20261017-223527-...-v001.md` é de um arquivo não rastreado no workspace; a referência a estado antigo de branch/PR é histórica e não descreve o checkout atual.

## Problema enriquecido

### Resultado desejado

Modificar classificações de associação já existente, identificada exclusivamente pelo par `(curriculo_id, vaga_id)`, obedecendo às regras explícitas do usuário, com propriedade verificada pelo ator autenticado, domínio como autoridade das invariantes e persistência sem duplicar ou alterar o agregado por fora.

### Atores e interesses

- Estudante autenticado: modifica apenas associações de currículos que possui e pode repetir operações sem criar erro nem efeito duplicado.
- Application: valida ownership antes de buscar a associação, direciona uma intenção de adição ou remoção ao agregado e só persiste estado alterado válido.
- Domain: protege o conjunto não vazio, o enum fechado e a relação candidatura/interesse.
- Repository/adapter: carrega o agregado por sua identidade composta e grava apenas a mudança das classificações, deixando commit/rollback ao boundary transacional externo.
- API/composição: quando houver contrato, extrai o principal validado pela sessão existente; não aceita `usuario_id` de rota/corpo/query como identidade autenticada.

### Evidências e fatos observados

1. **Requisito do usuário:** as dez regras no texto complementar acima são obrigatórias para esta análise e implementação.
2. **Documentação existente:** RF12 descreve criação manual e classificação; RN03 determina que candidatura implique interesse e que a condição sobreviva a alterações. A matriz CT-RF12-03 exige remover candidatura preservando interesse e CT-RF12-04 exige adicionar compatibilidade sem perder candidatura/interesse.
3. **Domain #131 presente:** `AssociacaoCurriculoVaga` possui identificadores tipados, conjunto interno, enum fechado, rejeita construção sem classificações, acrescenta interesse ao receber candidatura e expõe `frozenset`. Já possui `adicionar_classificacao`; não há método de remoção.
4. **Application/repository #130 presentes:** `CriarAssociacaoCurriculoVaga` recebe `UsuarioId`, consulta o currículo antes do par, traduz ausência ou ownership alheio para `CurriculoNaoEncontrado`, rejeita associação duplicada e chama `salvar`. O port possui apenas `existe_por_par` e `salvar`; o adapter usa o par como chave da consulta, grava raiz e classificações em `flush` e não confirma a transação.
5. **Persistência #130 presente:** a raiz usa PK `(curriculo_id, vaga_id)`; classificações usam PK `(curriculo_id, vaga_id, classificacao)` e FK composta à raiz. `para_associacao` já reconstrói o agregado a partir da raiz e das classificações. O modelo relacional já suporta as três operações de alteração sem novo campo ou tabela.
6. **Autenticação:** o middleware valida cookie e instala UUID em `request.state.usuario_id`; `obter_principal` valida esse estado e devolve 401 se ausente/inválido. O middleware verifica 403 em caminhos `/estudantes/{uuid}/curriculos...`; handlers de perfil e formação usam o principal da sessão. A aplicação principal, entretanto, injeta um autenticador indisponível.
7. **HTTP e composição:** `api/factory.py` registra routers por dependências, mas não tem router nem executores da associação. A issue #132 não documenta endpoint, verbo, request ou response.
8. **Erros:** handlers existentes mapeiam violações de domínio a 422 e ausência de recurso a 404; o middleware responde 401 para sessão inválida e 403 para a checagem de proprietário no padrão de rota suportado. O ADR permite 403 ou 404 para falha de ownership dependendo da consistência do contrato.
9. **Testes:** há testes unitários de Domain, Application e adapter; persistência usa SQLite e já verifica round-trip, chave composta e rollback. Testes de API exercitam ausência de principal, ownership e mapeamento de erros. Há padrão de integração com middleware, database fixture e snapshots para recusa de currículo alheio.
10. **Banco/transação:** configuração documenta PostgreSQL como banco da aplicação; testes locais de persistência da associação são SQLite. O repository não possui controle transacional próprio, e não foi encontrada composição que forneça o ciclo de unidade de trabalho da associação.

### Hipóteses

- **Decisão proposta de implementação:** dois casos de uso orientados à intenção, um para adicionar e outro para remover uma classificação. A operação é individual; não há requisito de substituição em lote.
- **Inferência arquitetural:** associação ausente depois de confirmar que o currículo pertence ao ator deve gerar erro específico de Application, sem criação implícita ou chamada ao domínio.
- **Inferência arquitetural:** a Application pode reaproveitar a sequência de ownership do caso de criação; `CurriculoNaoEncontrado` permanece uniforme para currículo ausente ou alheio.
- **Hipótese técnica a validar na implementação:** leitura, lock, mutação, escrita e confirmação devem ocorrer no mesmo escopo de transação. A infraestrutura atual não demonstra esse escopo na composição padrão.

### Perguntas em aberto

- **Contrato HTTP:** método, rota, formato de entrada/saída e status de sucesso não são definidos pela issue nem pelos artefatos revisados. Não devem ser escolhidos nesta decisão.
- **Exposição por API:** não está confirmado se a #132 inclui registrar endpoint ou somente entregar Domain/Application/persistência; isso depende do contrato de interface que não foi fornecido.
- **Composição executável:** o autenticador fornecido pela aplicação padrão é indisponível e não há composição dos repositories/casos de uso da associação nessa factory. Se a entrega exigir uma rota funcional em execução, é necessário decidir como integrá-la à composição já existente sem criar autenticação nova.
- **Concorrência:** a recomendação de serializar atualizações concorrentes pelo registro-raiz no PostgreSQL depende de haver transaction scope ativo até o commit; a composition testada não confirma esse boundary.

### Escopo

- Operações de domínio e Application para adição/remoção unitária das classificações em associação já existente.
- Ownership do currículo e consulta pelo par composto.
- Expansão do port e adapter para carregar e persistir as classificações alteradas.
- Testes unitários dos comportamentos e teste de persistência/rollback pertinente.
- Documentação dos cenários novos na matriz de testes e alinhamento dos detalhamentos RF12, se esses documentos permanecerem como fonte normativa.

### Fora do escopo

- Criar associação, mudar unicidade/chave composta, adotar ID técnico, alterar migration sem necessidade de schema ou transformar criação duplicada em atualização.
- Modificar busca/integração de vagas, regras externas de candidatura ou histórico.
- Criar autenticação nova, confiar em identidade recebida do cliente ou alterar o contrato de credenciais/sessão.
- Definir endpoint, payload ou status HTTP não documentado.
- Alterar comportamento do middleware geral ou reestruturar composition da aplicação sem decisão/escopo separado; registrar a integração necessária como handoff.

### Critérios de sucesso

- Todos os dez comportamentos explicitamente informados são cobertos por testes determinísticos de Domain/Application.
- Remoção inválida não modifica o agregado nem persiste estado parcial.
- Ownership é validado antes de consultar o repository de associação.
- Association lookup/update sempre usa ambos os IDs; não cria associação caso ausente.
- Repositório reconstrói e persiste o agregado sem reproduzir regras de negócio e sem alterar a raiz.
- Não há migração desnecessária nem contrato HTTP inventado.
- Toda escrita confirmada é atômica; a concorrência não perde mutações quando o boundary transacional estiver definido.

## Restrições aplicáveis

- Regras explícitas do usuário prevalecem sobre as hipóteses/propostas da v001: idempotência em adição e remoção, preservação da relação candidatura/interesse e proibição de estado vazio.
- Preservar identidade composta da #130 e separar criação de atualização.
- Aplicar invariantes na raiz do agregado conforme Clean Architecture/DDD do `src/backend/AGENTS.md`; nem Application nem adapter devem implementar regras duplicadas de domínio.
- Identidade deve ser proveniente do middleware/mecanismo de sessão existente; nenhuma identidade enviada pelo cliente substitui `request.state.usuario_id`.
- Não alterar código de produção/testes nesta atividade; a única escrita permitida aqui é este Markdown de análise.
- Alterações de schema, caso se provem necessárias, exigem mapping Code First e migration; a evidência atual indica que não são necessárias.
- Um eventual endpoint privado deve permanecer protegido pelo mecanismo padrão; rotas públicas não devem ser adicionadas para a feature.

## Classificação comentada

- `sphere: engineering`: a decisão é sobre implementação e arquitetura do backend.
- `concerns: domain, architecture, security`: invariantes, fronteiras entre Domain/Application/adapter e identidade/ownership.
- `decision_kind: design`, `scope: component`, `lifecycle: delivery`.
- Incerteza média: as decisões de negócio estão definidas, mas contrato HTTP e boundary operacional permanecem desconhecidos.
- Risco alto: falha de ownership exporia/modificaria dados de outro estudante; estado inválido ou atualização parcial corromperia associação.

## Decisão de roteamento

`prompts/backend` é mantida por continuidade da linhagem e aderência semântica: a análise cobre Domain, Application, ports e persistência backend. `prompts/requisitos` seria candidata apenas para uma decisão predominantemente normativa; `prompts/revisao` não é adequada apenas por ser revisão de versão. As demais pastas imediatas são menos específicas ao objeto. Não foi localizado `AGENTS.md` próprio em `prompts/backend`.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | Maximizada | Regras explícitas sempre preservadas em cada transição | Evita estado vazio ou candidatura sem interesse |
| security | Priorizada | Nenhuma consulta/mutação de associação antes de confirmar ownership | Protege dados privados e limita enumeração |
| reliability | Priorizada | Persistência de mudança atômica; sem estado parcial | Evita classificações divergentes entre Domain e banco |
| user-value | Priorizada | Operações repetidas não falham nem alteram duplicadamente | Idempotência exigida pelo usuário |
| simplicity | Satisfeita | Não criar API, migration ou abstração sem requisito comprovado | Reduz escopo e evita contrato inventado |
| modifiability | Satisfeita | Reutilizar agregado e repository existentes | Evita bifurcação das regras da associação |

## Alternativas consideradas

### A — Substituir o conjunto completo

Receber e persistir o conjunto final em uma única chamada. É tecnicamente possível com o agregado existente, mas não corresponde aos requisitos de idempotência descritos como operações de adicionar/remover; também exigiria que chamador conhecesse todo o estado e definiria comportamento para classificações omitidas. Não recomendada.

### B — Casos de uso separados de adição e remoção unitárias (recomendada)

Cada caso recebe ator, `CurriculoId`, `VagaId` e uma classificação. A Application confirma ownership, busca o agregado por par, invoca o mutador correspondente e grava somente se houve alteração. O Domain mantém as regras de idempotência e dependência, sem um comando batch ou semântica genérica.

### C — Um caso de uso genérico com ação

Um caso recebe o mesmo par e classificação, mais uma ação `adicionar/remover`. Pode reduzir repetição de orquestração, mas combina intenções e tratamento de erros distintos num contrato único. Só deve ser considerado se uma convenção do projeto vier a exigir isso; não há evidência atual para preferi-lo.

### D — Expor também uma rota HTTP agora

A autenticação por sessão e os padrões de router existem, então não é necessário criar nova infraestrutura. Porém a issue e a documentação não fornecem path, verbo, DTO, semântica de resposta nem status de sucesso; além disso, a composição padrão injeta autenticador indisponível e não fornece executores da associação. Não é uma alternativa viável sem decisões adicionais, e não se deve inventar o contrato.

## Perfil de pagamento comparativo

Escala ordinal: `+2` melhora forte, `+1` melhora moderada, `0` neutro/desconhecido, `-1` piora moderada e `-2` piora forte. Não somar os valores.

| Dimensão | Prioridade | A: substituir conjunto | B: casos separados | C: ação genérica | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| correctness | Maximizada | +1 | +2 | +2 | Alta | B/C expressam a intenção unitária, enquanto A depende de conjunto completo enviado pelo cliente |
| user-value | Priorizada | 0 | +2 | +1 | Alta | Regras do usuário são formuladas como adicionar/remover classificações |
| simplicity | Satisfeita | +1 | 0 | +1 | Média | A tem uma operação; B mantém intenção explícita; C reduz superfície mas combina fluxos |
| security | Priorizada | 0 | 0 | 0 | Alta | Todas dependem da mesma verificação de proprietário e principal confiável |
| modifiability | Satisfeita | 0 | +1 | 0 | Média | B preserva invariantes distintas de remoção e adição no agregado existente |
| reliability | Priorizada | +1 | +1 | +1 | Média | Todas dependem de transação externa e tratamento concorrente apropriado |

## Histórico e decisão atual

### Decisão da versão anterior

A v001 recomendava dois comandos de adição/remoção, idempotência, remoção sem cascata de candidatura e rejeição de associação vazia. Essas semânticas estavam descritas como propostas a aprovar. Também supunha ausência de mecanismo de identidade comum e banco de produção desconhecido. A identidade composta, separação de criação e reutilização do Domain/repository estavam alinhadas à #130/#131, mas no momento atual a #130 já está integrada.

### Decisão recomendada nesta versão

Manter duas intenções de Application: adicionar uma classificação e remover uma classificação. A associação só é localizada pelo par completo. O agregado existente deve ganhar operação de remoção; ambas as mutações devem manter idempotência e invariantes no Domain. A Application confirma propriedade do currículo antes da consulta da associação, usa a exceção de currículo já existente para ausência/propriedade alheia, gera erro Application específico para associação ausente e persiste somente estado alterado.

Não há alteração de schema necessária. O adapter deve carregar/reconstruir a raiz com `para_associacao` e atualizar as linhas de classificação dentro do mesmo escopo transacional; não deve inserir a raiz nem fazer commit/rollback. A transação e serialização concorrente exigem boundary explícito; para PostgreSQL, recomenda-se lock da linha-raiz por chave composta enquanto a mutação estiver em curso.

Não criar endpoint nem definir método, rota, request, response ou status de sucesso nesta análise. Se a #132 exigir API, deve haver decisão/contrato explícito e composição funcional de autenticação/executores antes da exposição.

### Impacto da revisão

`revised`: regras anteriormente propostas passam a ser requisitos explícitos, o PR #541 está mergeado, o modelo de persistência já existe e autenticação possui mecanismo estabelecido. Permanece aberta a integração HTTP e o transaction boundary da composição em execução; não se reabre o desenho do agregado de criação.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | maximized | Cada operação mantém conjunto não vazio e `CANDIDATURA => INTERESSE` | Requisitos do usuário e RN03; invariante já no agregado |
| security | prioritized | Atualização apenas após identificar principal autenticado e validar propriedade | ADR-002, contrato de sessão, middleware e caso de criação |
| reliability | prioritized | Mudança de classificações transacional, com no-op sem escrita | Repository existente faz flush sem commit; requer boundary externo |
| user-value | prioritized | Repetições de adição/remoção são seguras e não perdem classificações correlatas | Regra explícita do usuário |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| simplicity | Sem atualização em lote, migração ou endpoint sem contrato | Comandos unitários e reutilização dos artefatos existentes |
| modifiability | Não duplicar regra nem mudar identidade do agregado | Mutadores na raiz, lookup por chave composta |
| interoperability | Nenhum formato HTTP novo sem contrato | HTTP permanece pendente; core Application não depende de transporte |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | Persistir associação vazia ou candidatura sem interesse | Alta | Estudante e consumidores do agregado |
| security | Usuário alterar associação vinculada a currículo de terceiro | Alta | Proprietários dos currículos |
| reliability | Escrita parcial ou atualizações concorrentes sobrescreverem estado | Alta | Estudante e consistência persistida |
| user-value | Repetição de operação idempotente produzir erro ou duplicidade | Média | Estudante e clientes que repetem requisições |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | Recusa explícita de remover interesse com candidatura até candidatura ser removida | Conveniência de remoção implícita em cascata | Aceitável; regra é explícita e não apaga outra intenção |
| correctness | Recusa de remover a última classificação | Liberdade para deixar associação vazia | Aceitável; usuário proíbe estado vazio |
| reliability | Lock/transaction scope pode serializar alterações do mesmo par | Throughput de atualizações concorrentes da mesma associação | Aceitável, sujeito a validar boundary no PostgreSQL |
| simplicity | Não disponibilizar chamada HTTP até haver contrato e composição funcional | Disponibilidade imediata da operação para cliente web | Aceitável enquanto a pendência for registrada, não ocultada |

## Riscos e efeitos de segunda ordem

- **Contrato implícito por convenção:** usar uma rota existente ou inventar um verbo/status para preencher a ausência de contrato produz API não aprovada. Manter a pendência e limitar esta análise ao core.
- **Autenticação não ativa na composição padrão:** `main.py` fornece `AutenticadorSessaoIndisponivel`; uma rota registrada sem corrigir/fornecer composition funcional sempre negaria usuários. Não criar outra autenticação nem tratar esse placeholder como principal válido.
- **Identidade forjada:** receber `usuario_id` da entrada do cliente e encaminhá-lo à Application quebraria ADR-002. A borda deve usar principal validado em `request.state`; a Application recebe `UsuarioId` tipado por entrada interna.
- **Ownership antes da associação:** buscar o par antes de validar o currículo pode revelar existência. Manter ordem do caso de criação: ler currículo, comparar `usuario_id`, encerrar em caso de ausência/alheio e somente então consultar associação.
- **Regra duplicada no adapter/Application:** decidir remoção de candidatura ou última classificação fora do agregado cria inconsistência. Todas as transições devem passar pelo Domain.
- **Reconstrução de agregado corrompido:** `para_associacao` passa registros pelo enum e construtor, que normaliza candidatura incluindo interesse. Persistência previamente inválida pode ser corrigida incidentalmente numa atualização; não introduzir normalização paralela no adapter e considerar teste de comportamento se dados legados forem encontrados.
- **Atomicidade sem boundary:** `flush` não equivale a commit; leitura, lock, remoção/inserção das linhas e confirmação devem pertencer à mesma unidade transacional.
- **Lost update:** duas alterações simultâneas do mesmo par podem sobrescrever classificações se cada uma reconstruir snapshot sem serialização. A chave natural fornece linha-raiz para `SELECT FOR UPDATE` no PostgreSQL, desde que a transação permaneça aberta até a gravação.
- **Docs desatualizados:** requisitos ainda listam retirada de interesse sob candidatura e consulta/alteração como detalhamentos pendentes; a nova mensagem resolve os comportamentos centrais, então a matriz e detalhamentos devem ser alinhados no trabalho autorizado posterior.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Regras de idempotência e remoção estão satisfeitas | Estado do agregado após repetir operações e exceções em transições inválidas | Testes unitários do Domain | Qualquer remoção inválida altera o agregado, ou repetição não é no-op |
| Application aplica ownership primeiro | Ordem das chamadas ao repository e entrada de ator derivada internamente | Testes unitários com spies; teste de API quando contrato existir | Consulta da associação ocorre para currículo ausente/alheio ou principal vem do payload |
| Identidade composta é usada em leitura e escrita | SQL/argumentos do adapter incluem ambos os identificadores | Testes unitários do adapter e persistência | Consulta/alteração depende apenas de `vaga_id` ou apenas de `curriculo_id` |
| Persistência mantém as classificações após atualização e rollback | Snapshots persistidos antes/depois e após falha | Teste de persistência com banco de teste e transaction scope real | Raiz órfã, estado parcial, commit dentro do adapter ou dados divergentes |
| Concorrência não perde alterações confirmadas | Duas atualizações simultâneas no PostgreSQL configurado | Teste de integração no ambiente do componente apropriado; confirmar boundary/lock | Uma classificação confirmada desaparece ou o teste só passa em SQLite sem lock |
| API futura usa autenticação e erro coerentes | Contrato aprovado, principal da sessão, códigos e conteúdo seguro | Testes de rota com `create_app`, principal autenticado, sessão ausente/inválida e ator alheio | Contrato incompatível, identidade do cliente aceita ou default runtime não autenticável |

## Handoffs e atividades posteriores

### Implementação core da #132

1. Adicionar ao `AssociacaoCurriculoVaga` a operação de remoção e manter no agregado os invariantes de não vazio, idempotência e candidatura implica interesse; documentar a alteração conforme docstrings do backend.
2. Acrescentar testes unitários de Domain para duplicata em adição, classificação ausente em remoção, remoção de candidatura preservando interesse, rejeição de remover interesse sob candidatura, rejeição da última classificação e estado inalterado em falha.
3. Criar casos de uso de intenção de adicionar e remover; receber IDs tipados e ator; confirmar existência/propriedade do currículo antes de consultar o par; tratar associação ausente sem criar uma nova.
4. Expandir `RepositorioAssociacaoCurriculoVaga` para obter agregado por par e persistir sua atualização. A ausência e idempotência devem manter o fluxo explícito; evitar duplicar invariantes na Application.
5. Alterar o adapter para consultar por chave composta, usar `para_associacao` existente e gravar somente as linhas de classificações necessárias. A migration e o mapping atual bastam para a modelagem; não acrescentar migration sem requisito de schema.
6. Definir/usar boundary transacional fora do repository. Confirmar lock da linha-raiz no PostgreSQL e cobertura do escopo até commit antes de declarar robustez concorrente.
7. Atualizar doubles e testes unitários de Application e adapter. Adicionar teste de persistência da atualização e rollback que prove o estado completo, não somente o `flush`.
8. Alinhar `docs/matriz_testes.md` e detalhamentos de `docs/requisitos_funcionais.md` às regras explícitas antes de considerar a matriz normativa atualizada.

### API e integração (somente após decisão de contrato)

- Não alterar autenticação nem aceitar principal vindo da requisição externa. Reutilizar middleware/sessão e identidade validada em `request.state.usuario_id`.
- A issue não diz se API integra a #132. Se incluir endpoint, definir previamente path, verbo, entrada, resposta e status de sucesso; depois registrar router e executores na composition. A composição padrão atual usa autenticador indisponível e precisaria receber configuração funcional já existente.
- A resposta 401 para ausência/invalidez de sessão é definida pelo middleware. O middleware dá 403 quando reconhece UUID alheio em `/estudantes/{uuid}/curriculos...`; no caso de aplicação, `CurriculoNaoEncontrado` já mascara ausência/alheio. A escolha 403/404 para rota futura deve seguir um contrato consistente com ADR-002, não ser fixada nesta análise.
- Para API aprovada, adicionar testes de rota da identidade própria, sessão ausente/inválida, ator alheio, tentativa de passar `usuario_id` no corpo e mapeamentos de erro. Se integrar persistência/middleware, seguir o padrão de teste de integração existente e executar no ambiente Nix `tests`.

## Síntese

### Decisão recomendada

Implementar no core duas intenções unitárias, adicionar e remover classificação, reutilizando o agregado, a porta e o adapter já criados na #130. Localizar somente pelo par `(curriculo_id, vaga_id)`, validar primeiro que o ator autenticado é proprietário do currículo, aplicar todas as regras no Domain e gravar apenas mudança válida. Adição repetida e remoção ausente são no-ops; remover candidatura preserva interesse; remover interesse com candidatura e remover a última classificação são recusados. A associação não pode ficar vazia.

### Regras de negócio consolidadas

| Regra | Base |
|---|---|
| A identidade da associação é o par `(curriculo_id, vaga_id)` | Decisão implementada pela #130 e PK composta |
| `CANDIDATURA` implica `INTERESSE` em todo estado | RN03 e agregado #131 |
| Adicionar classificação já presente é idempotente | Regra explícita do usuário |
| Remover classificação ausente é idempotente | Regra explícita do usuário |
| Remover candidatura não remove interesse nem outras classificações | Regra explícita do usuário e CT-RF12-03 |
| Remover interesse enquanto candidatura existir é proibido | Regra explícita do usuário |
| Remover a última classificação é proibido; associação vazia é inválida | Regra explícita do usuário e construtor do Domain |
| Somente proprietário do currículo pode alterar; verificar ownership antes do par | Regra explícita, ADR-002 e padrão da Application #130 |
| Identidade vem do mecanismo existente, não do cliente | Regra explícita, contrato de sessão e middleware |
| Regras do agregado não se repetem em Application/adapter | `src/backend/AGENTS.md` e estrutura atual |
| Nenhuma rota/payload/status de sucesso é decidido sem contrato | Issue #132 e artefatos sem contrato HTTP de associação |
| Nenhuma migration é esperada para persistir classificações já modeladas | Mapping, PK composta e migration #130 |

### Fluxo de Application

1. Receber entrada interna tipada com ator autenticado, `CurriculoId`, `VagaId` e `ClassificacaoAssociacao`; não expor `usuario_id` do cliente como autoridade.
2. Obter currículo. Se não existir ou pertencer a outro usuário, lançar `CurriculoNaoEncontrado` e não consultar associação.
3. Buscar associação existente pelo par completo. Se ausente, lançar erro específico da Application; não criar.
4. Invocar o mutador apropriado no agregado. O Domain normaliza adição de candidatura e decide idempotência/validade de remoção.
5. Se operação não alterou estado, retornar sucesso de Application sem persistência. Não definir aqui status HTTP de sucesso.
6. Se alterou, solicitar atualização do agregado ao port. Toda falha de persistência deve propagar e rollback deve ocorrer no boundary externo.

### Mudanças necessárias em ports/repository

- Port atual tem apenas `existe_por_par` e `salvar`; manter ambos para criação e acrescentar leitura do agregado por par e atualização de associação existente.
- Reutilizar a conversão `para_associacao` já existente; carregar as classificações relacionadas e reconstruir a raiz antes da mutação.
- Atualizar linhas dependentes usando os dois IDs; não inserir de novo a raiz, alterar identidade ou fazer upsert.
- Preservar PK composta de classificação; não duplicar regra de enum/dependência no banco ou adapter.
- Adapter executa `flush`, não commit/rollback. A unidade externa deve garantir atomicidade do ciclo de alteração e, se necessário, serialização por raiz no PostgreSQL.
- Ausência de mudança idempotente deve evitar escrita sempre que o estado não for alterado.

### Erros esperados

| Camada | Erro | Ocorrência | Tratamento interno |
|---|---|---|---|
| Domain | `RegraDeDominioViolada` | Classificação inválida, remoção de interesse com candidatura, remoção da última | Não persistir; estado do agregado deve permanecer válido |
| Application | `CurriculoNaoEncontrado` existente | Currículo inexistente ou que não pertence ao ator | Encerrar antes de consultar associação |
| Application | Erro específico novo para associação não encontrada | Currículo próprio, mas par ausente | Não fazer criação implícita |
| Adapter | Erro de persistência/flush | Falha SQL ou constraint não mapeada como regra de negócio | Propagar ao boundary; rollback, sem sucesso fictício |
| API futura | Não autenticado | Cookie ausente ou inválido | Middleware responde 401 antes do handler |
| API futura | Falha de propriedade | Principal não corresponde ao recurso conforme rota/contrato | 403 ou 404 conforme contrato consistente com ADR-002; não decidido aqui |

### Traduções HTTP

- 401 para ausência ou invalidez de sessão: definido no middleware existente.
- 422 para violação de regra de domínio é padrão observado nos handlers; usar somente quando houver endpoint aprovado.
- 404 para currículo/associação ausente é compatível com handlers e com a exceção de Application; 403 para proprietário diferente também aparece no middleware. ADR-002 admite ambas as políticas conforme contrato. Não fixar status de associação sem contrato.
- Adição duplicada e remoção ausente são sucesso idempotente no core; status, corpo e formato da resposta HTTP permanecem pendentes.
- Falhas de banco não devem virar sucesso ou resposta genérica sem observabilidade; 503 somente se o boundary já reconhecer indisponibilidade conforme padrão aplicável.

### Testes necessários

**Unitários de Domain (`src/backend/tests/test_domain_associacao_curriculo_vaga.py`):**

- adicionar classificação existente não duplica nem muda estado;
- remover classificação ausente não muda estado;
- remover candidatura preserva interesse e demais classificações;
- remover interesse sob candidatura rejeita sem alterar estado;
- remover a última classificação rejeita sem alterar estado;
- nenhuma transição produz candidatura sem interesse ou associação vazia.

**Unitários de Application (`src/backend/tests/test_application_associacao_curriculo_vaga.py`):**

- atualização válida pelo proprietário lê e persiste o agregado certo;
- currículo ausente/alheio falha antes de consultar associação ou escrever;
- associação ausente produz erro Application e não cria;
- identidade de entrada controla ownership, sem `usuario_id` do cliente;
- operação idempotente não solicita escrita;
- falha de repository propaga sem sucesso fictício.

**Unitários de adapter e integração de persistência:**

- consulta e escrita usam `(curriculo_id, vaga_id)`;
- mapping reconstrói classificações existentes; atualização não reinsere raiz nem duplica classificação;
- falha no flush/commit seguida de rollback preserva snapshot anterior completo;
- testar persistência das remoções e adições, além dos round-trips/criação já cobertos.
- Testes unitários do backend devem rodar no ambiente Nix `backend`; testes integrados que exercitam migrations/persistência/composição devem rodar no ambiente Nix `tests`, conforme AGENTS.

**API, caso o escopo seja confirmado posteriormente:**

- principal vindo da sessão, sessão ausente/inválida, owner e ator alheio;
- tentativa de enviar identidade diferente pelo cliente não altera identidade autenticada;
- status/DTO apenas conforme contrato aprovado; garantir ausência de alteração SQL em recusas.

### Pendências reais

1. Confirmar se a #132 inclui endpoint HTTP. Caso sim, obter contrato de rota, verbo, request, response e status de sucesso; o repositório e a issue não os definem.
2. Confirmar composition executável para autenticador, executores e repository. O mecanismo/middleware existe, mas `main.app` injeta `AutenticadorSessaoIndisponivel` e a factory atual não registra associação.
3. Definir e provar o transaction boundary de produção que cubra lock, leitura, mutação, flush e commit. A documentação identifica PostgreSQL, mas o teste atual usa SQLite e não valida locking concorrente.
4. Atualizar requisitos/matriz aos comportamentos agora explicitados. Isso é documentação pendente, não impedimento para implementar a lógica do agregado.

### Handoff claro para implementação

Implementar somente o core com Domain, Application, port, adapter e testes; não alterar autenticação, não criar rota ou contrato HTTP por suposição e não acrescentar migration sem mudança de schema demonstrada. Resolver atomicidade no boundary externo já existente ou registrar bloqueio concreto se ele não existir. Após confirmação de contrato e composition de autenticação funcional, uma atividade autorizada pode expor e testar a API.

## Síntese final

A v002 corrige a v001 onde o estado atual mudou e transforma as regras fornecidas pelo usuário em requisitos, não hipóteses. O suporte #130 está integrado e o schema existente atende à atualização. A implementação de núcleo tem caminho técnico claro, com duas intenções e regras no agregado. O que ainda impede definir uma entrega HTTP completa não é falta de mecanismo de autenticação no código, mas ausência de contrato de API e de composição operacional funcional para autenticador/repository/transação.

Arquivo criado em `prompts/backend/20261018-210535-atualizacao-classificacoes-associacao-curriculo-vaga-v002.md`. Avalie se o local escolhido é de fato o mais adequado.
