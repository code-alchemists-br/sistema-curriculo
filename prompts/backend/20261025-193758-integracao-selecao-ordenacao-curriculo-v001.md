---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-25T19:37:58-03:00"
lineage:
  mode: initial
  root: null
  supersedes: null
  change_type: initial
  secondary_change_types: []
  decision_impact: initial
subjects:
  kind: repository
  files:
    - path: src/backend/tests/fixtures/curriculos_autenticados_integracao.py
      relationship: primary
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: 8b87ae9d78636e7bf7879128d985333f9e817ef8
      availability: available
    - path: src/backend/application/selecao_itens_versao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: 8b87ae9d78636e7bf7879128d985333f9e817ef8
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/ambientes, prompts/revisao]
  confidence: high
  rationale: "Especificação de integração da API, aplicação e persistência de currículo; precedentes de testes autenticados estão em backend. Ambiente é suporte, não resultado."
classification:
  sphere: engineering
  concerns: [integration, data, security]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: medium
---

# Análise de decisão — integração da seleção e ordenação de currículo

## Solicitação original

Título literal do card: **"Criar teste de integração para seleção e ordenação de itens no currículo."**

O pedido integral de análise está preservado no apêndice A. A instrução final é literal: **"Não implemente nada."** Esta entrega é somente especificação revisável; não é o teste implementado nem evidência de aprovação dele.

## Informações complementares

O usuário forneceu a skill `decision-analysis-v4`, seu caminho `.agents/skills/decision-analysis-v4/SKILL.md` e seu conteúdo. Esse conteúdo foi confrontado por leitura com o arquivo local. Aplicadas suas referências `classification-taxonomy.md`, `output-schema.md`, `output-routing.md` e `artifact-classification.md`. Nova análise, do zero, conforme pedido; documentos anteriores são evidência histórica, não linhagem desta análise. Nenhuma entrada posterior identificada.

## Mudanças desde a versão anterior

Nenhum identificado — modo `initial`, v001.

## Artefatos analisados

Estado comum às linhas abaixo: working tree inicialmente limpo, branch `test-selecao-ordenacao-curriculo`, HEAD `8b87ae9d78636e7bf7879128d985333f9e817ef8`. Arquivos não alterados pela análise. `P` = primary; `S` = supporting; `C` = context. Recortes explícitos evitam atribuir leitura integral a arquivos apenas pesquisados. Os dois objetos principais também constam no frontmatter; o inventário completo de evidências está nesta tabela.

| Caminho | Relação | Representação | Função | Formato | Recorte examinado | Estado/revisão |
|---|---|---|---|---|---|---|
| `AGENTS.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `src/backend/AGENTS.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/decision-analysis-v4/SKILL.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/decision-analysis-v4/references/classification-taxonomy.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/decision-analysis-v4/references/output-schema.md` | C | prose | schema-contract | Markdown | integral | working-tree/HEAD |
| `.agents/skills/decision-analysis-v4/references/output-routing.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/decision-analysis-v4/references/artifact-classification.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/backend-domain-orchestration-v2/SKILL.md` | C | prose | prompt-instruction | Markdown | escopo e gate | working-tree/HEAD |
| `.agents/skills/backend-domain-orchestration-v2/references/clean-boundary.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/backend-domain-orchestration-v2/references/backend-fit-check.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/backend-adapters-drivers-v2/SKILL.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/backend-adapters-drivers-v2/references/outer-boundary.md` | C | prose | prompt-instruction | Markdown | fronteiras | working-tree/HEAD |
| `.agents/skills/backend-adapters-drivers-v2/references/backend-fit-check.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/cross-cutting-implementation-v1/SKILL.md` | C | prose | prompt-instruction | Markdown | escopo e gate | working-tree/HEAD |
| `.agents/skills/cross-cutting-implementation-v1/references/scope-boundary.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/cross-cutting-implementation-v1/references/cross-cutting-fit-check.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/frontend-implementation-v3/SKILL.md` | C | prose | prompt-instruction | Markdown | escopo e gate | working-tree/HEAD |
| `.agents/skills/frontend-implementation-v3/references/scope-boundary.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/frontend-implementation-v3/references/frontend-fit-check.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/nix-environment-implementation-v1/SKILL.md` | C | prose | prompt-instruction | Markdown | escopo e gate | working-tree/HEAD |
| `.agents/skills/nix-environment-implementation-v1/references/nix-scope-boundary.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/nix-environment-implementation-v1/references/nix-fit-check.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/integration-system-testing-v1/SKILL.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/integration-system-testing-v1/references/test-scope-boundary.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/integration-system-testing-v1/references/test-fit-check.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/integration-system-testing-v1/references/implementation-protocol.md` | C | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `docs/configuracao-ambiente.md` | C | prose | documentation | Markdown | integral | working-tree/HEAD |
| `docs/requisitos_funcionais.md` | S | prose | documentation | Markdown | RF03, RF05–09, RF13–15 e pendências | working-tree/HEAD |
| `docs/requisitos_nao_funcionais.md` | S | prose | documentation | Markdown | RNF04, RNF05, RNF07 e verificação | working-tree/HEAD |
| `docs/requisitos-seguranca.md` | S | prose | documentation | Markdown | resultados de busca: sessão, propriedade, currículo | working-tree/HEAD |
| `docs/Arquitetura/ADR-002-autenticacao-autorizacao-propriedade.md` | S | prose | documentation | Markdown | identidade, propriedade, 401/403/404 e testes | working-tree/HEAD |
| `docs/contrato-credenciais-sessao.md` | S | prose | schema-contract | Markdown | credencial, rotas protegidas e precedência | working-tree/HEAD |
| `docs/modelagem_der.md` | S | diagram-model | documentation | Mermaid/Markdown | currículo e seis relações de itens | working-tree/HEAD |
| `docs/matriz_rastreabilidade.md` | S | prose | documentation | Markdown | RF03/05/07/14/15 e #400 | working-tree/HEAD |
| `docs/matriz_testes.md` | S | prose | documentation | Markdown | convenções e CT-RF03/05/13/14 | working-tree/HEAD |
| `docs/previa-curriculo.md` | S | prose | schema-contract | Markdown | integral | working-tree/HEAD |
| `docs/exportacao-pdf-docx.md` | C | prose | documentation | Markdown | situação e limites da exportação | working-tree/HEAD |
| `docs/mapeamento_jornadas.md` | S | prose | documentation | Markdown | §6.5 | working-tree/HEAD |
| `docs/casos-de-uso-v2.md` | C | prose | documentation | Markdown | busca currículo/ordem/seleção | working-tree/HEAD |
| `docs/wireframes/07-revisao.md` | C | prose | documentation | Markdown | busca currículo/ordem/seleção | working-tree/HEAD |
| `docs/wireframes/08-visualizacao-curriculo.md` | C | prose | documentation | Markdown | busca currículo/ordem/seleção | working-tree/HEAD |
| `prompts/README.md` | C | prose | documentation | Markdown | integral | working-tree/HEAD |
| `prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md` | S | prose | documentation | Markdown | alternativas, contrato, validação e handoffs | working-tree/HEAD |
| `prompts/backend/20261017-180000-persistir-ordem-secoes-curriculo-v001.md` | S | prose | documentation | Markdown | decisão, riscos, validação e handoffs | working-tree/HEAD |
| `prompts/backend/20261017-160000-itens-por-secao-previa-versao-curriculo-v001.md` | S | prose | documentation | Markdown | decisão, limites e validação | working-tree/HEAD |
| `src/backend/domain/curriculo.py` | P | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/domain/secao_curriculo.py` | P | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/domain/value_objects.py` | S | source-code | production | Python | ReferenciaCurriculo e tipos de IDs | working-tree/HEAD |
| `src/backend/domain/itens_perfil.py` | S | source-code | production | Python | chaves de ordenação de formação/experiência | working-tree/HEAD |
| `src/backend/application/ports.py` | P | source-code | schema-contract | Python | ConsultaProprietarioItem, ItemPerfil, ConsultaItemPerfil | working-tree/HEAD |
| `src/backend/application/selecao_itens_versao_curriculo.py` | P | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/application/versao_curriculo.py` | P | source-code | production | Python | AtualizarOrdemSecoesCurriculo e entrada | working-tree/HEAD |
| `src/backend/application/previa_versao_curriculo.py` | P | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/application/exclusao_experiencia_profissional.py` | C | source-code | production | Python | busca por exclusão/referência | working-tree/HEAD |
| `src/backend/api/itens_versao_curriculo.py` | P | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/api/versao_curriculo.py` | P | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/api/previa_versao_curriculo.py` | P | source-code | production | Python | DTO, conversão e rota | working-tree/HEAD |
| `src/backend/api/listagem_versoes_curriculo.py` | S | source-code | production | Python | resumo e rota | working-tree/HEAD |
| `src/backend/api/middleware_autenticacao.py` | P | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/api/factory.py` | P | source-code | production | Python | parâmetros, instalação de middleware e routers | working-tree/HEAD |
| `src/backend/main.py` | P | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/infrastructure/security/autenticador_sessao.py` | S | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_sessao.py` | S | source-code | production | Python | consulta ativa, filtros, revogação | working-tree/HEAD |
| `src/backend/infrastructure/persistence/sqlalchemy/curriculo.py` | P | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py` | P | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_formacao_academica.py` | C | source-code | production | Python | assinaturas e filtros de exclusão | working-tree/HEAD |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_experiencia_profissional.py` | C | source-code | production | Python | assinaturas e filtros de exclusão | working-tree/HEAD |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_projeto_academico.py` | C | source-code | production | Python | assinaturas encontradas na busca | working-tree/HEAD |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_competencia.py` | C | source-code | production | Python | assinaturas encontradas na busca | working-tree/HEAD |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_idioma.py` | C | source-code | production | Python | assinaturas encontradas na busca | working-tree/HEAD |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_documento.py` | C | source-code | production | Python | assinaturas e filtros de exclusão | working-tree/HEAD |
| `src/backend/infrastructure/persistence/alembic/env.py` | S | source-code | configuration | Python | integral | working-tree/HEAD |
| `alembic.ini` | S | structured-data | configuration | INI | integral | working-tree/HEAD |
| `nix/tests.nix` | S | source-code | configuration | Nix | integral | working-tree/HEAD |
| `nix/backend.nix` | S | source-code | configuration | Nix | integral | working-tree/HEAD |
| `nix/backend-python-packages.nix` | S | source-code | configuration | Nix | integral | working-tree/HEAD |
| `nix/quality.nix` | C | source-code | configuration | Nix | composição de ferramentas | working-tree/HEAD |
| `.github/workflows/ci.yml` | C | structured-data | configuration | YAML | gates backend e integração | working-tree/HEAD |
| `src/backend/tests/fixtures/curriculos_autenticados_integracao.py` | P | source-code | test | Python | integral | working-tree/HEAD |
| `src/backend/tests/fixtures/credenciais_sessao.py` | S | source-code | test | Python | símbolos, preparação e Alembic em subprocesso | working-tree/HEAD |
| `src/backend/tests/fixtures/perfis_integracao.py` | S | source-code | data-fixture | Python | seed/leitura híbrida e símbolos | working-tree/HEAD |
| `src/backend/tests/fixtures/curriculo_exportacao.py` | S | source-code | data-fixture | Python | cabeçalho, IDs, DTO e símbolos | working-tree/HEAD |
| `src/backend/tests/fixtures/massa_teste_curriculos.py` | S | source-code | data-fixture | Python | origem JSON, DTO e símbolos | working-tree/HEAD |
| `src/backend/tests/fixtures/__init__.py` | C | source-code | test | Python | metadados de descoberta, não conteúdo | working-tree/HEAD |
| `src/backend/tests/test_integracao_recusa_curriculo_alheio.py` | P | source-code | test | Python | integral | working-tree/HEAD |
| `src/backend/tests/test_application_selecao_itens_versao_curriculo.py` | S | source-code | test | Python | doubles e métodos de cenário | working-tree/HEAD |
| `src/backend/tests/test_api_itens_versao_curriculo.py` | S | source-code | test | Python | doubles, métodos, testes de DTO | working-tree/HEAD |
| `src/backend/tests/test_api_ordem_secoes_curriculo.py` | S | source-code | test | Python | integral | working-tree/HEAD |
| `src/backend/tests/test_infrastructure_curriculo_ordem_secoes.py` | S | source-code | test | Python | integral | working-tree/HEAD |
| `src/backend/tests/test_infrastructure_repositorio_curriculo.py` | S | source-code | test | Python | sessão simulada e métodos de cenário | working-tree/HEAD |
| `src/backend/tests/test_application_previa_versao_curriculo.py` | S | source-code | test | Python | doubles e métodos de cenário | working-tree/HEAD |
| `src/backend/tests/test_domain_ordem_secoes_curriculo.py` | S | source-code | test | Python | métodos de cenário | working-tree/HEAD |
| `src/backend/tests/test_domain_secao_curriculo.py` | S | source-code | test | Python | métodos de cenário | working-tree/HEAD |
| `src/backend/tests/test_integracao_crud_informacoes_complementares.py` | C | source-code | test | Python | doubles, composição e cenários | working-tree/HEAD |
| `src/backend/tests/test_integracao_rejeicao_referencia_curriculo.py` | S | source-code | test | Python | classe, repositório em memória e cenários | working-tree/HEAD |
| `src/backend/tests/test_integracao_isolamento_dados_estudantes.py` | C | source-code | test | Python | harness e composição encontrados na busca | working-tree/HEAD |
| `src/backend/tests/test_integracao_isolamento_experiencias.py` | C | source-code | test | Python | harness encontrado na busca | working-tree/HEAD |
| `src/backend/tests/test_integracao_recusa_perfil_alheio.py` | C | source-code | test | Python | harness encontrado na busca | working-tree/HEAD |
| `src/backend/tests/test_integracao_rejeicao_requisicoes_sem_credenciais_validas.py` | S | source-code | test | Python | skips explícitos e classes | working-tree/HEAD |
| `src/backend/tests/test_integracao_composicao_credenciais_sessao.py` | S | source-code | test | Python | composição e skip C02 | working-tree/HEAD |
| `src/backend/tests/test_integracao_contrato_credenciais_sessao.py` | S | source-code | test | Python | fixture e guarda aiosqlite | working-tree/HEAD |
| `src/backend/tests/test_integracao_persistencia_sessao.py` | S | source-code | test | Python | fixture e guarda aiosqlite | working-tree/HEAD |
| `src/backend/tests/test_integracao_persistencia_dados_pessoais.py` | C | source-code | test | Python | SQLite/create_all | working-tree/HEAD |
| `src/backend/tests/test_persistencia_associacao_curriculo_vaga_integracao.py` | C | source-code | test | Python | SQLite/create_all | working-tree/HEAD |
| `src/backend/tests/integracao_repositorio_associacao_curriculo_vaga.py` | C | source-code | test | Python | SQLite/create_all e nome fora de discover | working-tree/HEAD |
| `src/backend/tests/test_fixture_perfis_integracao.py` | C | source-code | test | Python | SQLite/create_all | working-tree/HEAD |
| `src/backend/tests/test_integracao_storage_204.py` | C | source-code | test | Python | classe de armazenamento local | working-tree/HEAD |

Migrations examinadas: todas as declarações `revision` e `down_revision` por busca e AST, sem importar scripts nessa inspeção estática (o comando Alembic posterior carrega os scripts). Cada linha abaixo é um arquivo efetivamente inspecionado. Representação `source-code`, formato Python, função `schema-contract`, relação S, recorte `selected-section` (identificadores/arestas), estado working-tree/HEAD. As cinco assinaladas com DDL tiveram também `upgrade`/`downgrade` lidos integralmente.

| Caminho em `src/backend/infrastructure/persistence/alembic/versions/` | Revision | Down revision | Recorte adicional |
|---|---|---|---|
| `20260916_0001_criar_usuarios.py` | 20260916_0001 | null | — |
| `20261005_0002_criar_curriculos.py` | 20261005_0002 | 20260916_0001 | **DDL** |
| `20261007_0003_criar_curriculo_itens.py` | 20261007_0003 | 20261005_0002 | **DDL** |
| `20261012_0004_criar_sessoes.py` | 20261012_0004 | 20261007_0003 | — |
| `20261012_0005_criar_experiencias_profissionais.py` | 20261012_0005 | 20261012_0004 | — |
| `20261014_0006_criar_competencias.py` | 20261014_0006 | 20261012_0005 | — |
| `20261014_0007_adicionar_dados_contato_usuario.py` | 20261014_0007 | 20261014_0006 | — |
| `20261013_0004_adicionar_dados_consulta_estudante.py` | 20261013_0004 | 20261014_0007 | — |
| `20261014_0007_criar_formacoes_academicas.py` | 20261014_0008 | 20261014_0007 | — |
| `20261014_0007_unificar_ramos_schema.py` | 20261014_0009 | (20261013_0004, 20261014_0008) | merge preservado |
| `20261015_0009_criar_idiomas.py` | 20261015_0009 | 20261014_0008 | — |
| `20261015_0010_criar_certificacoes.py` | 20261015_0010 | (20261014_0009, 20261015_0009) | merge preservado |
| `20261015_0011_exclusao_logica_formacoes_academicas.py` | 20261015_0011 | 20261015_0010 | duplicada |
| `20261015_0011_criar_cursos.py` | 20261015_0011 | 20261015_0010 | duplicada; DDL também lido |
| `20261015_0012_criar_projetos_academicos.py` | 20261015_0012 | 20261015_0011 | duplicada |
| `20261015_0012_criar_links_profissionais.py` | 20261015_0012 | 20261015_0011 | duplicada; DDL também lido |
| `20261016_0013_criar_documentos.py` | 20261016_0013 | 20261015_0012 | — |
| `20261017_0014_exclusao_logica_experiencias_profissionais.py` | 20261017_0014 | 20261016_0013 | — |
| `20261017_0015_adicionar_ordem_secoes_curriculos.py` | 20261017_0015 | 20261017_0014 | **DDL** |
| `20261017_0004_criar_associacoes_curriculo_vaga.py` | 20261017_0004 | 20261007_0003 | ramo terminal separado |

### Limites da evidência dos artefatos

Não houve acesso a GitHub, rede, banco compartilhado nem frontend. Não se infere estado de branches remotas por nomes. O título foi fornecido pelo usuário; a referência #400 existe na matriz, mas não fornece descrição nem aceite adicional. Busca não substitui leitura integral: recortes de contexto acima sustentam apenas as afirmações explicitadas. Nenhuma análise anterior foi adotada como verdade do estado atual.

## Problema enriquecido

### Resultado desejado

Especificar teste executável que integre seleção de referências de perfil, desseleção e persistência da ordem de seções por currículo, com positivos, negativos, controles, SQL independente e spies. Separadamente verificar a ordenação automática dos itens na prévia. Não inventar reordenação manual de itens, operação não encontrada.

### Atores e interesses

Estudantes A/B: seleção própria e isolamento. Executor: comandos e oráculos concretos. Revisor: distinguir verde, skip, caracterização e limitação. Produto: decidir lacunas de comportamento, sem que o teste as resolva implicitamente.

### (a) Fatos encontrados — caminhos e trechos

#### F1. Busca e proveniência local

Comandos de leitura: `find . -name AGENTS.md -o -name AGENTS.override.md`; `rg --files`; buscas `rg -n -i` nos documentos; `git status --short`, `git log --all --oneline --regexp-ignore-case --grep=...`, histórico de arquivos e `git show --stat` dos merges. Encontradas somente instruções de raiz, backend e frontend; nenhuma instrução adicional em `prompts`, `.agents`, `nix` ou migrations. Frontend não foi avaliado.

Busca case-insensitive literal em `docs prompts`, contagem de **arquivos** retornados (`rg -i -l "$termo" docs prompts | wc -l`, antes de criar este documento):

| Termo | Arquivos | Resultados relevantes lidos |
|---|---:|---|
| seleção | 35 | análise de seleção; matriz RF03/05 e #400 |
| selecionar | 22 | requisitos, análises de currículo |
| desselecionar | 2 | prompts de seleção e recusa de currículo; **nenhum documento em docs** |
| ordem | 92 | domínio, persistência de seções, projeção em prompts |
| ordenação | 22 | formação/experiência, matriz e prompts |
| posição | 71 | busca literal também encontra “exposição”, “composição” e “sobreposição”; não é prova de posição persistida |
| seção | 36 | RF05, prévia e prompts |
| item | 50 | seleção, prévia e fixtures |
| currículo | 102 | requisitos, DER e análises |
| prévia | 41 | contrato JSON e exportação |

Busca adicional `rg -n -i 'ordena.*itens|posicao|posição|desselecionar' docs`: retorna, entre outros, `docs/mapeamento_jornadas.md:145`, “ordenar os itens conforme a necessidade do currículo”; `docs/previa-curriculo.md:7`, “listas ordenadas”; muitos falsos positivos de composição/exposição; **nenhuma ocorrência de “desselecionar” em docs**. `rg --files prompts | rg -i 'integra.*sele|sele.*orden'` retornou vazio antes desta escrita: nenhuma análise com esse nome foi presumida. Não significa ausência de conteúdo relacionado em outros nomes.

Busca de `ConsultaProprietarioItem|ConsultaItemPerfil|def obter_proprietario|def obter_item` em `src/backend/infrastructure` e `application/ports.py`: encontra as duas portas em `ports.py:769,803`, **nenhuma implementação concreta dessas consultas em infrastructure**. A mesma busca em backend encontra doubles de testes, inclusive `ConsultasItensDouble`. Repositórios específicos existem, mas não implementam automaticamente essas portas.

Tentativas de leitura por nomes não confirmados retornaram vazio/erro e foram descartadas: `.github/workflows/quality.yml` não existe (workflow real descoberto: `ci.yml`); `application/exclusao_formacao_academica.py` não existe com esse nome. Nenhuma conclusão foi baseada nesses nomes ausentes.

#### F2. Histórico Git — trabalhos identificados, sem confundir card e PR

| Trabalho | Evidência local | Como foi identificado |
|---|---|---|
| Modelo de currículo | `ee79135`, `feat(backend): add curriculum domain model` | histórico de `domain/curriculo.py` |
| Edição/persistência inicial | `440d120`, `910a0fc`, `d877b79`; merge `388fa9e`, PR #158, branch task-113 | mensagens e histórico dos arquivos |
| Criação | `9a8328f`, `26c66f8`, `a68aaa7`; merge `5d5b185`, PR #159, branch task-109 | `git show --stat 5d5b185` inclui aplicação, mapping, factory e router |
| Seleção | `a2c6be0`, `69a1623`, `c18340f`; merge `118974f`, PR #166, branch task-117 | merge diz “Implementar seleção de itens”; stat inclui router, porta, migration, repositório e testes |
| Prévia | `cbd5729`, `8d2a8cb`; merge `1abd0e1`, PR #445, branch task-120 | stat inclui `previa_versao_curriculo.py` nas duas camadas e testes |
| Ordem automática formação | `0c208c4`, merge `4e53db5`, PR #503, task183 | mensagem “expor ordenação de formações na prévia #183” |
| Ordem automática experiência | `78313ac`, merge `6243341`, PR #507, task185 | mensagem “expor ordenação de experiências na prévia #185” |
| Propriedade da referência | `de40f96` | histórico do agregado, mensagem “validar propriedade da referência selecionada no domínio” |
| Projeção por seção | `d0571d8`, merge `d8cf58d`, PR #537, task-213 | mensagens “projetar itens selecionados da prévia por seção” |
| Persistência da ordem de seções | `e5bfa01`, merge `6e1c62a`, PR #538, task-211 | mensagens e histórico do agregado |
| Atualização da ordem | `7f30fc9`, merge `46a7a75`, PR #543, task-212 | stat confirma caso de uso, rota, factory e teste de contrato |

Esses vínculos derivam de nomes/mensagens/stat, não de coincidência numérica. `docs/matriz_rastreabilidade.md` liga #400 a RF03/RF05/RF14/RF15; isso é registro documental do card, não prova de PR ou de aceite. A análise usa somente a árvore atual para oráculos executáveis.

#### F3. Item, seleção e ordem são conceitos distintos

`domain/value_objects.py`, `ReferenciaCurriculo`: “aceita apenas identificadores dos seis tipos de itens”. `api/itens_versao_curriculo.py`, `TipoItem`, e `sqlalchemy/curriculo.py`, `_TIPOS_POR_CLASSE`, fornecem o mesmo vocabulário:

| Tipo público | ID de domínio | Conteúdo na prévia |
|---|---|---|
| `formacao_academica` | FormacaoAcademicaId(UUID) | `formacoes` |
| `experiencia_profissional` | ExperienciaProfissionalId(UUID) | `experiencias` |
| `projeto_academico` | ProjetoAcademicoId(UUID) | `projetos` |
| `competencia` | CompetenciaId(UUID) | `competencias` |
| `idioma` | IdiomaId(UUID) | `idiomas` |
| `documento` | DocumentoId(UUID) | `documentos` |

Dados pessoais não são referências selecionáveis (`PreviaVersaoCurriculo.itens_por_secao` os exclui). Cursos, certificações e links não fazem parte do Literal nem da união `ItemPerfil`, mesmo que existam recursos próprios para cadastro. Não ampliar tipos por analogia.

Seleção é **referência**, não cópia: `Curriculo._referencias: set[ReferenciaCurriculo]`; propriedade retorna `frozenset`; repositório grava pares tipo/UUID. Não há posição de item. O mesmo UUID sob tipos diferentes tem identidade tipada diferente. A resposta POST ordena pares por `(tipo, str(item_id))` para determinismo; isso não é uma escolha manual de apresentação.

`domain/secao_curriculo.py`, trecho `ORDEM_PADRAO_SECOES`: `dados-pessoais`, `formacao-academica`, `experiencias-profissionais`, `projetos-academicos`, `competencias`, `idiomas`, `documentos-complementares`. `Curriculo.ordem_secoes` nasce com essa tupla; `definir_ordem_secoes` exige cada seção exatamente uma vez: `len(ordem) != len(set(ordem)) or set(ordem) != set(SecaoCurriculo)` provoca `RegraDeDominioViolada`. Ordem pertence a cada currículo, inclusive quando seções estão vazias e quando dados pessoais mudam de lugar. O domínio não fixa dados pessoais na primeira posição.

Ordem automática dentro da seção na prévia (`application/previa_versao_curriculo.py`):

- Formações: `ordenar_formacoes`, sustentado pelo próprio consumidor de currículo, usa situação (em andamento, concluída, interrompida), data de referência decrescente (início para andamento; fim ou início nos demais), início decrescente e UUID textual. Fonte: `domain/itens_perfil.py:240–286`.
- Experiências: início decrescente; no empate, sem fim antes; depois fim mais recente e UUID. Fonte: `_chave_ordenacao_experiencia` e `ordenar_experiencias` no mesmo arquivo; chamada explícita na prévia.
- Projetos, competências, idiomas e documentos: campo textual `titulo`, `descricao`, `idioma`, `nome_arquivo`, respectivamente, usando `casefold()` e UUID para desempate (`_ordenar_por_texto`).

Isso não é transposição de regras do perfil: o caso de uso de **prévia de currículo** importa e aplica essas funções. Não foi encontrada operação para usuário reordenar itens dentro da seção.

#### F4. Persistência e integridade

`sqlalchemy/curriculo.py`: `curriculos` tem PK `id`, FK não nula `usuario_id -> usuarios.id`, `titulo_versao`, `layout`, `is_public`, `ordem_secoes`. Ordem é `Text`, `nullable=False`, identificadores separados por vírgula; `ordem_secoes_para_texto` e `texto_para_ordem_secoes` convertem sem ordenar novamente. Não há tabela de posições de seção nem coluna numérica de posição.

`CurriculoItemRegistro`: PK composta `(curriculo_id, tipo, item_id)`, FK apenas para currículo. Migration `20261007_0003_criar_curriculo_itens.py`: `sa.PrimaryKeyConstraint("curriculo_id", "tipo", "item_id")`; não há FK para os itens nem constraint de proprietário ou CHECK do tipo. A docstring “cujas tabelas ainda não existem” é histórica: hoje há repositórios específicos; sua existência não cria FKs retroativamente.

Migration `20261017_0015_adicionar_ordem_secoes_curriculos.py`: coluna texto não nula com ordem padrão congelada no servidor. `20261005_0002_criar_curriculos.py` cria o currículo antes das referências. Fonte física para esta integração é migration + modelo ORM; DER é conceitual e diverge (ver achados).

`RepositorioCurriculoSqlAlchemy.obter_por_id` lê currículo e seleções; `atualizar` copia campos escalares, sincroniza diferença das seleções e dá `flush`, sem commit. `_sincronizar_itens` compara conjuntos e só insere/remove diferenças. Commit pertence à composição externa.

`Curriculo.incluir_referencia`: duplicata -> “Item já está incluído no currículo.”; `remover_referencia`: ausência -> “Item não está incluído no currículo.”. Não são operações idempotentes na implementação. Inclusão/remoção não altera `ordem_secoes`; não existe reposicionamento, lacuna ou estabilidade de posições de item para testar. Ordem de iteração do conjunto não é contrato.

#### F5. Contrato por operação — implementado versus documentado

Base **V** = `/estudantes/{usuario_id}/curriculos/{curriculo_id}`; **L** = `/estudantes/{usuario_id}/curriculos`. UUIDs vêm do caminho; pessoa chega ao caso de uso pelo caminho, mas o middleware, se instalado, compara essa pessoa com a sessão. Não chega do corpo. Todas as operações usam `RepositorioCurriculoSqlAlchemy` na composição recomendada, pela porta `RepositorioCurriculo`.

| Operação / fonte implementada | Entrada | Caso de uso / consultas | Sucesso | Falhas tratadas pelo handler, após validação |
|---|---|---|---|---|
| POST `V/itens`, `api/itens_versao_curriculo.py` | JSON `{"tipo": <Literal de seis>, "item_id": UUID}` | SelecionarItemVersaoCurriculo; currículo, ConsultaProprietarioItem, agregado, atualizar | 201 `{"curriculo_id": UUID, "itens": [{"tipo":...,"item_id":...}]}`; lista de seleção completa ordenada por tipo/UUID | currículo ausente/alheio: 404 `Versão de currículo não encontrada.`; item ausente/alheio: 404 `Item do perfil não encontrado.`; domínio: 422 `str(erro)`; executor None: 503 `Seleção indisponível.` |
| DELETE `V/itens/{tipo}/{item_id}`, mesmo módulo | tipo Literal e UUID no caminho | DesselecionarItemVersaoCurriculo; currículo, remover referência, atualizar; **não consulta item/dono** | 204 vazio | currículo ausente/alheio: 404 mesma mensagem; referência não selecionada: 422 `Item não está incluído no currículo.`; executor None: 503 `Desseleção indisponível.` |
| PUT `V/ordem-secoes`, `api/versao_curriculo.py` | `{"ordem_secoes": [sete SecaoCurriculo]}`; `extra="forbid"`, min=max=7 | AtualizarOrdemSecoesCurriculo; currículo, domínio, atualizar | 204 vazio | currículo ausente/alheio: 404 mesma mensagem; permutação inválida que passa DTO: 422 `A ordem das seções deve conter cada seção exatamente uma vez.`; executor None: 503 `Atualização da ordem indisponível.` |
| GET `V/previa`, `api/previa_versao_curriculo.py` | UUIDs de caminho | GerarPreviaVersaoCurriculo; currículo, usuário, ConsultaItemPerfil | 200 DTO: currículo/título/layout, estudante com contato e seis listas de itens | currículo ausente/alheio ou usuário ausente/excluído: 404 mesma mensagem de currículo; executor None: 503 `Prévia indisponível.` |
| GET `L`, `api/listagem_versoes_curriculo.py` | UUID da pessoa | ListarVersoesCurriculo; listar_por_usuario | 200 `{"versoes": [{"id", "titulo_versao", "layout", "is_public", "total_itens"}]}`; vazio se nenhuma versão | executor None: 503 `Listagem indisponível.`; não contém ordem nem IDs dos itens |

Falhas comuns, de **outras camadas**: sem cookie/sessão inválida -> 401 `{"detail":"Sessão ausente ou inválida."}`; pessoa no caminho diferente da sessão -> 403 `{"detail":"A sessão não pode acessar este recurso."}`; UUID/tipo/corpo inválido -> 422 da validação FastAPI/Pydantic. Não inventar 409, 400 ou erro de item inexistente no DELETE. Falhas inesperadas de banco, driver ou mapeamento não são traduzidas por esses handlers em um contrato de falha específico.

**Documentado**: RF03 centraliza informações; RF05 organiza seções; RF07 visualiza; RF13 autentica; RF14 múltiplos currículos (`docs/requisitos_funcionais.md`). `docs/matriz_testes.md`, CT-RF05-02: “Currículo reflete a estrutura e a ordem de seções escolhidas”; CT-RF03-03: somente informações de A. `docs/previa-curriculo.md` define GET, listas ordenadas e 404/422/503, sem campo de ordem de seções. `docs/contrato-credenciais-sessao.md` define 401/403 e cookie exclusivo. Os prompts de seleção/persistência propõem contratos; não são aceite de produto e contêm pendências históricas.

**Só implementado ou detalhado no código**: payload/status precisos de seleção e remoção, 422 de duplicidade/remoção ausente, extras ignorados na seleção, sete seções exatas e extra proibido na ordem. `test_api_ordem_secoes_curriculo.py` inspeciona OpenAPI desses detalhes, sem fazer chamada HTTP. Não existe descrição do card detalhando-os como aceite; os critérios integrados que os exercitam serão **inferidos dos artefatos**, não atribuídos ao card.

#### F6. Propriedade, existência e precedência

Seleção (`application/selecao_itens_versao_curriculo.py`): primeiro currículo; `if curriculo is None or curriculo.usuario_id != entrada.usuario_id`, 404 de currículo; depois `obter_proprietario(referencia)`; `None` -> ItemNaoEncontrado; dono diferente -> domínio `ReferenciaDeOutroProprietario`, convertido pelo caso para ItemNaoEncontrado; depois duplicidade no conjunto; finalmente atualizar/flush. Item ausente e alheio têm mesmo status **e mesmo detail**. Currículo ausente e alheio também, dentro dessa camada.

Desseleção e ordem só verificam currículo e invariantes locais. Nenhum desses casos verifica existência atual do item na fonte. ConsultaProprietarioItem delega existência e dono à implementação; contrato não recebe dono do cliente. Para **cada um dos seis tipos**, busca em infrastructure não encontrou adapter concreto de ConsultaProprietarioItem nem ConsultaItemPerfil. Repositórios de formação/experiência têm consulta por ID/dono, inclusive variante para excluídas; documentos têm obter_por_id ativo; competências/idiomas/projetos têm operações próprias. Nenhum desses fatos demonstra a composição das duas portas polimórficas de currículo.

Na aplicação recomendada a sequência observável é:

1. Middleware valida cookie `__Host-sessao`; autenticador real calcula SHA-256 e repositório de sessão filtra hash, expiração, revogação e faz relação com usuário ativo (`repositorio_sessao.py`: `UsuarioRegistro.deleted_at.is_(None)`). Sem cookie ou conta excluída -> 401 antes do handler/executor.
2. Com sessão válida, middleware compara UUID de pessoa no caminho. Outra pessoa -> 403 antes do framework validar corpo ou chamar executor. UUID de pessoa malformado não é reconhecido por essa guarda e chega à validação 422.
3. FastAPI valida caminho/corpo. Tipo desconhecido, UUID inválido, ordem com tamanho diferente de sete, seção desconhecida, número em vez de seção, extras no PUT -> 422 sem caso de uso.
4. Handler válido verifica executor None -> 503. Portanto corpo inválido precede 503; executor ausente precede consulta de propriedade do currículo. Uma composição sem autenticação não serve para afirmar precedência de 401/403.
5. Caso de uso: propriedade/existência do currículo -> existência/propriedade do item na seleção -> invariantes de duplicidade/remoção/permutação -> atualização. Lista com sete entradas conhecidas mas repetidas chega ao domínio; duplicata com currículo ausente produz 404 antes de 422 de domínio.

“Recurso alheio indistinguível de inexistente” não vale indiscriminadamente: `/estudantes/B/...` com sessão A produz 403, exista ou não aquele currículo. `/estudantes/A/curriculos/<de B>` e `<ausente>` produzem o mesmo 404 no caso de uso. Não comparar essas duas composições de erro como se fossem o mesmo oráculo.

Identificador de dono extra: DTO de seleção não configura extra=forbid; Pydantic ignora `usuario_id` no corpo. `test_integracao_recusa_curriculo_alheio.py:test_s6_caracteriza_extras_ignorados_sem_trocar_proprietario` já caracteriza sucesso sem trocar dono. PUT de ordem usa `extra="forbid"`: mesmo extra produz 422 antes do executor, já caracterizado em S6 específico. DELETE usa pessoa do caminho; query/corpo extra não substituem esse parâmetro. Token em Bearer/query/corpo não autentica (`docs/contrato-credenciais-sessao.md`, middleware).

#### F7. Leitura observável e composição real

`GerarPreviaVersaoCurriculo` relê cada referência e omite item `None`, de outro dono ou com ID diferente; não altera referências persistidas. Portanto prévia vazia não prova seleção vazia. A listagem conta referências persistidas, não itens efetivamente resolvidos. Asserções precisam do SQL bruto e do agregado relido, além do DTO.

`PreviaVersaoCurriculo.itens_por_secao`: `for secao in ORDEM_PADRAO_SECOES if itens.get(secao)`. Usa a **ordem padrão**, mesmo que `curriculo.ordem_secoes` tenha sido personalizada; omite seções sem itens e dados pessoais. `PreviaVersaoCurriculoResposta` e sua conversão não expõem `ordem_secoes` nem sequência global de seções. Listagem tampouco expõe ordem. Logo API atual permite provar seleção e ordem automática dos itens na prévia, **não** ordem personalizada das seções nela.

`api/factory.py`: argumentos `selecionar_item_versao_curriculo`, `desselecionar_item_versao_curriculo`, `atualizar_ordem_secoes_curriculo` e prévia são opcionais, padrão None; registra os routers; só instala `MiddlewareAutenticacaoSessao` quando autenticador é passado. `main.py:75`: `create_app(autenticador_sessao=AutenticadorSessaoIndisponivel(), verificador_persistencia=..., lifespan=...)`. Existe autenticação instalada em produção, mas o autenticador é indisponível; não existe binding produtivo desses casos, repositórios e portas de item. DATABASE_URL só compõe readiness. Não afirmar “produção sem middleware”; não ativar nada nesta fatia.

Composição recomendada deve invocar `create_app` com autenticação persistida real e três casos reais, mais listagem/prévia reais para oráculos de leitura. É composição de teste, não certificação de `main.app`, login produtivo ou transação de produção.

#### F8. Inventário de harnesses, fixtures e cobertura existente

Não se presume que “integracao” no nome implique banco real. Classificação por fronteiras efetivamente presentes:

| Artefato real | O que oferece/prova | Limite e reaproveitamento |
|---|---|---|
| `fixtures/curriculos_autenticados_integracao.py` | BancoCurriculosAutenticadosIntegracao; SQLite em arquivo temporário, migrations, FK ON, usuários A/B, dois currículos e idiomas já selecionados, token A real, create_app com oito casos; AsyncMock(wraps) por executor; requisitar ASGI HTTPS; snapshot de tabelas em outra AsyncSession, commit antes da leitura | Base recomendada. ConsultasItensDouble contém só três idiomas. Preflight detecta somente revision duplicada; usa upgrade `heads`, não garante uma head. Ampliar somente suporte de teste para este cenário |
| `fixtures/credenciais_sessao.py` | BancoCredenciaisSessao; diretório e URL próprios, Alembic em subprocesso com env filtrado, head única e upgrade head; seed de conta/senha; utilitários de sessão e solicitar_asgi | Reaproveitar padrão de validação de grafo/URL/cleanup, não copiar uma suíte inteira. Identifica melhor o head, mas exige preparação adicional de credenciais |
| `fixtures/perfis_integracao.py` | popular_perfis_fake, ler_perfis_fake; usuários/currículos SQL síncrono, formação/experiência em memória, referências reconstruídas de cenário | Híbrida, não prova referências persistidas; não é harness ASGI migrado; não usar como oráculo desta fatia |
| `fixtures/curriculo_exportacao.py` | obter_curriculo_exportacao_fixture, IDs estáveis, entidades e dados de apresentação | Sem banco/migrations/auth; útil para exemplos de conteúdo, não para persistência |
| `fixtures/massa_teste_curriculos.py` | obter_curriculos_massa_teste; lê `docs/massa_teste_curriculos.json`, constrói seis tipos e prévia | Dados de domínio/documentação; JSON foi identificado pelo código, não analisado integralmente; não assumir negativos/ordens apropriados sem lê-lo na implementação |
| `test_integracao_recusa_curriculo_alheio.py` | S1 oito controles positivos; S2 dono do caminho (403); S3 objeto de B sob A (404); S4 ausente/alheio iguais; S5 item de B/ausente (idioma) 404; S6 extras; S7–10 sem cookie, revogada, expirada, desconhecida; snapshots e spies | Integração com banco migrado quando disponível; não cobre seis tipos nem fluxo seleção+ordem+remoção, duplicata e inválidos de ordem em conjunto. Ignorado no baseline desta análise; não contabilizar como proteção executada |
| `test_integracao_rejeicao_referencia_curriculo.py` | repositório em memória, caso de edição real, entrada ASGI; 404/422 | Prova colaboração API/aplicação, não seleção nem SQL |
| `test_integracao_isolamento_dados_estudantes.py`, `test_integracao_recusa_perfil_alheio.py`, `test_integracao_isolamento_experiencias.py` | repositórios de estado em memória e autenticadores doubles | Precedentes de integração por colaboração, não banco migrado; não transportar suas regras |
| `test_integracao_crud_informacoes_complementares.py` | create_app, autenticador multiusuário double, repositórios documento/curso e storage fake | Integração entre camadas em memória, não adaptadores de itens de currículo |
| `test_integracao_contrato_credenciais_sessao.py`, `test_integracao_persistencia_sessao.py` | BancoCredenciaisSessao; sessões persistidas/contrato quando aiosqlite e grafo suportam | Reaproveitar convenções, não repetir login/logout completos nesta fatia |
| `test_integracao_composicao_credenciais_sessao.py` | distingue produção da composição montada; C02 explicitamente ignorado por falta de composição produtiva | Limite deve permanecer explícito |
| `test_integracao_rejeicao_requisicoes_sem_credenciais_validas.py` | API/middleware; dois skips “a aplicação ainda não compõe persistência de sessões” | Não retirar skips de outros trabalhos |
| `test_integracao_persistencia_dados_pessoais.py`, `test_fixture_perfis_integracao.py` | SQLite síncrono, `Base.metadata.create_all` | Precedente legado, **inadequado** para requisito atual de migration até head |
| `test_persistencia_associacao_curriculo_vaga_integracao.py` | SQLite e metadata.create_all | Outro recurso, não fonte de regras de currículo |
| `integracao_repositorio_associacao_curriculo_vaga.py` | Async SQLite + create_all; módulo sem prefixo test_, CI executa explicitamente | Não entra no discover padrão, não extrapolar baseline para esse módulo |
| `test_integracao_storage_204.py` | armazenamento local, por classe encontrada | Não foi escolhido como harness de currículo; recorte limitado, não se atribui cobertura de seleção |

Cobertura abaixo é predominantemente **unitária**, apesar de nomes infrastructure/API:

- `test_application_selecao_itens_versao_curriculo.py`: repositório spy e consulta stub; seis tipos, proprietário, ausência, duplicata, remoção e atualização. Não prova banco/HTTP.
- `test_api_itens_versao_curriculo.py`: executores doubles, chamada direta dos handlers/DTO; conversão dos seis tipos e 201/204/404/422/503. Não prova middleware nem persistência.
- `test_infrastructure_repositorio_curriculo.py`: sessão simulada, diff de seleção, leitura, flush, exclusão, listagem; não é banco real.
- `test_infrastructure_curriculo_ordem_secoes.py`: metadata, SimpleNamespace e op mockada; texto, default, migration declarada, conversão e invalidade. Não executa DDL.
- `test_domain_ordem_secoes_curriculo.py`, `test_domain_secao_curriculo.py`: invariantes de permutação/padrão; sem banco/API.
- `test_api_ordem_secoes_curriculo.py`: somente OpenAPI, 204, enum e tamanho sete/extra proibido; não executa a operação integrada.
- `test_application_previa_versao_curriculo.py`: doubles; grupos, ordenação, omissão de itens ausentes/alheios/inconsistentes e ausência de escrita. Novo cenário deve verificar ligação com seleção SQL, não repetir todas as combinações de sort puro.

#### F9. Ambiente, baseline e bloqueios preexistentes

`AGENTS.md` e `docs/configuracao-ambiente.md`: Nix obrigatório; git fora de Nix; integração em `.#tests`; unitários em backend. `integration-system-testing-v1/references/test-scope-boundary.md`: “Exercita colaboração real entre pelo menos duas unidades ou uma fronteira técnica relevante”; endpoint com banco de teste é integração; controller mockado é unidade. Não exige necessariamente processo HTTP nem navegador. `docs/matriz_testes.md` define positivo/negativo/exceção e cenários independentes; recusa de currículo usa métodos e subtestes; não existe obrigação de um único fluxo monolítico.

`nix/tests.nix` importa `backend-python-packages.nix` e adiciona `ps.aiosqlite`; lista comum: FastAPI, Uvicorn, SQLAlchemy, Alembic, Psycopg, pydantic-settings. `nix/backend.nix` usa somente lista comum, **sem aiosqlite**. Inspeção executada em `nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 python3 -c '<inspeção de importlib.util e AST>'`: módulos `fastapi`, `sqlalchemy`, `alembic`, `aiosqlite`, `psycopg` encontrados, todos True. Não houve instalação ou alteração de ambiente. Nenhuma necessidade atual de editar `nix/tests.nix`.

Baseline solicitado, execução real:

```sh
nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src
```

Primeira tentativa no sandbox: não iniciou suíte, `error: opening lock file "/nix/var/nix/db/big-lock": Read-only file system`. Reexecutada com escalonamento solicitado pelo mecanismo de permissão, sem mudar comando ou ambiente. Resultado exit 0: **Ran 955 tests in 15.040s; OK (skipped=33)**. São 922 resultados não ignorados, 33 skips; não chamar os 955 de aprovados. Conjunto de identidades de falhas = **∅**; conjunto de identidades de erros = **∅**. Esta é a referência por identidade para “não introduzir erros novos”, não apenas um total. Saída padrão não lista identidades/motivos dos 33 skips; não inventar sua distribuição exata. Ausência de aiosqlite no backend e skips explícitos foram constatados separadamente por inspeção, não por inferência dos pontos/s da saída.

Warnings observados: depreciação Starlette de HTTP_422_UNPROCESSABLE_ENTITY, slow tasks asyncio e warning de teste da política de IA inválida; não foram falhas. Não corrigidos. O baseline é informativo e inclui módulos integrados descobertos pelo runner legado, conforme comando explicitamente solicitado; isso não autoriza executar o novo integrado em backend.

Gate realizado após baseline:

```sh
nix develop .#quality --command ruff check src/backend
```

Exit 0: **All checks passed!**. Sem I001, nenhuma correção. `.github/workflows/ci.yml` confirma Ruff no job backend-lint e discover no job backend-tests; o job de integração atual chama explicitamente módulo de associações em tests. Não alterar CI nesta fatia.

Leitura de migrations por AST: duplicadas `20261015_0011` (cursos e exclusão lógica de formações) e `20261015_0012` (links e projetos). Identificadores terminais do grafo declarado: `20261017_0004`, `20261017_0015`; com duplicatas, isso **não** é um DAG Alembic válido com duas heads bem definidas.

Consulta real `nix develop .#tests --command alembic heads`, exit 0, emitiu **UserWarning do Alembic** para cada revision duplicada e imprimiu:

```text
20261015_0011
20261015_0012
20261017_0004 (head)
20261017_0015 (head)
```

Não tratar exit 0 como grafo saudável. Nenhum upgrade foi tentado na análise. Nenhuma migration foi corrigida. Não se executou o cenário inexistente nem o experimento temporário. Foram comparados por AST um plano de quatro arquivos e o plano mínimo recomendado de dois arquivos (unicidade, referências, DFS sem ciclo, preservação das tuplas existentes e head única `20261015_0012_links`); isso **não** prova DDL nem equivale a `alembic history`/upgrade sem warnings. A consulta Alembic original gerou 20 arquivos de bytecode não rastreados em versions/__pycache__; foram identificados como outputs desta consulta e removidos, preservando o estado inicial. Comandos futuros devem usar PYTHONDONTWRITEBYTECODE=1 também nas consultas Alembic.

### Hipóteses

H1: a fatia pode caracterizar comportamento implementado sem inventar contrato. H2: migrations com só metadados temporariamente encadeados poderão executar SQLite; falta demonstração por upgrade real. H3: preparar banco por caso será aceitável; não há medição de custo por banco nesta análise. Todas são hipóteses técnicas, não fatos do card.

### (b) Lacunas — opções, recomendação e decisão necessária

| ID / lacuna delimitada pelos artefatos examinados | Opções viáveis | Recomendação justificada | Produto? / informação exata para fechar |
|---|---|---|---|
| L1. Card sem descrição/aceite | caracterizar o código e título; pedir aceite antes de qualquer teste | Caracterização rotulada, critérios de teste inferidos com fonte; não afirmar aceite | Sim para aceite final: fornecer descrição, escopo de “ordenar itens” e critérios de aceite assinados/aprovados |
| L2. Reordenação manual de itens ausente | interpretar ordem de seções e sort automático existente; abrir implementação futura de posições por item | Primeira: única fatia que usa operações existentes; atende título sem fabricar endpoint | Produto deve confirmar se título queria ordem manual; fornecer operação, persistência, limites e oráculos se sim |
| L3. Prévia não reflete ordem personalizada de seções | provar ordem por agregado+SQL e sort automático por prévia; aguardar correção produtiva para prova visual | Primeira, com limite explícito; não chamar SQL de prova da apresentação | Técnico para teste atual; produto/contrato para corrigir: definir campo/ordem global e tratamento de seções vazias/dados pessoais |
| L4. Adaptadores das duas consultas de itens ausentes para os seis tipos | mapa tipado double; adapters produtivos em outra demanda; adapter SQL só de teste | Mapa double explícito já adotado no harness, sem inventar integração produtiva | Técnico nesta fatia. Para prova completa: fornecer bindings reais por tipo e semântica de excluídos; não implementar aqui |
| L5. Política geral de alteração/exclusão de item selecionado não fechada | referência viva/omitir ausente; snapshot; impedir exclusão; preservar soft-deleted selecionado por tipo | Caracterizar apenas filtro da prévia e preservação da referência; política futura em handoff | Sim. Fornecer matriz por tipo: alteração, exclusão lógica/física, conteúdo anterior/atual, restauração e seleção posterior |
| L6. Limites de itens e garantia concorrente ausentes | sem limite adicional como implementação; definir quantidade por tipo/total; limite técnico | Não criar teste de limite arbitrário nem de concorrência nesta entrega | Sim para negócio: números e comportamento; técnico posterior para concorrência/isolamento e condição de disputa |
| L7. Política uniforme de campos extras não definida | manter seleção ignora e ordem proíbe; padronizar estrito; padronizar tolerante | Caracterizar diferenças atuais, sem elevar a padrão geral | Produto/contrato se padronizar: quais campos são aceitos/ignorados/recusados e compatibilidade |
| L8. Grafo original inválido | testes implementados com skip honesto; experimento temporário autorizado; aguardar correção definitiva | Executar original e registrar bloqueio; depois experimento temporário de 2 arquivos, sem corrigir grafo permanentemente | Técnico, com autorização de execução futura conforme pedido; correção definitiva exige demanda separada |
| L9. Harness de currículo usa upgrade heads e só detecta duplicatas | usar como está e falhar em múltiplas heads; acrescentar preflight dedicado e exigir head; migrar para BancoCredenciaisSessao | Ampliar suporte **exclusivo de teste** para preflight completo e upgrade head, preservando consumers atuais | Técnico. Precisar de leitura atual das fixtures ao executar; nenhuma decisão de produto |
| L10. Composição produtiva não permite executar operações do tema | testar factory explícita; aguardar bindings produtivos | Factory com limite declarado, sem tocar main | Técnico. Para prova de produção: entrega separada com autenticação persistida, casos, repositórios, transação e consultas de item ligados |
| L11. Custo por banco não medido | banco novo por teste/subcaso; reuso com reset; cópia de banco migrado | Banco novo, simples e precedente existente; medir, não otimizar antecipadamente | Técnico. Fornecer medição monotônica de migração/seed/caso e máquina/versões; sem threshold de desempenho inventado |
| L12. Nenhum relatório durável obrigatório para esta fatia | PR com comandos/contagens/diffs; doc novo de evidência; editar matrizes | Mínimo: este documento versionado e PR com execução; não criar outro doc por hábito | Técnico/processo. Produto/revisor pode exigir evidência permanente e indicar destino/retensão |

Política parcialmente definida **não** é ausência total: `ports.py` menciona formação excluída ainda selecionada na prévia/exportação; o adapter futuro deve incluí-la se referência e dono conferirem. Isso não define todos os seis tipos nem torna a porta concreta. Não importar idempotência de associação/vaga (RN05) ou exclusão de perfil para currículo.

### Perguntas em aberto

As decisões de produto L1/L2/L3/L5/L6/L7 não impedem escrever a caracterização limitada recomendada; impedem declarar aceite de comportamento novo ou prova visual da ordem personalizada. Não se solicita resposta para inventar operações ausentes. Nenhuma fonte essencial ao desenho técnico ficou inacessível; por isso status `proposed`, não `pending` para a fatia limitada.

### Escopo

Somente arquivos de teste/fixtures dedicados ao currículo, SQL local migrado, ASGI, autenticação já implementada, caracterizações e relatório honesto. Plano de experimento temporário de ambiente/metadados para execução posterior; nenhuma execução de tal experimento nesta análise.

### Fora do escopo

Código produtivo, rotas, domínio, portas, adapters de itens, main/factory produtivos, middleware, regras novas, frontend, CI, correção permanente de Nix/migrations, concorrência, PostgreSQL, exportação binária, falhas de banco e implantação. Não consertar descobertas para obter verde.

### Critérios de sucesso

Seleção, ordenação e positivos/negativos são exigências **definidas pelo pedido do usuário**. Todos os critérios específicos S/P/N abaixo são **inferidos do título + artefatos**, com fonte implementada ou documentada identificada; não são critérios de aceite inventados para o card. Sucesso da implementação futura requer ao menos um positivo de seleção e de ordem e negativos correspondentes **executados**, não só ignorados. Se apenas skips forem possíveis, entregar código descoberto/executável e relatar prova pendente, sem declarar objetivo de execução aprovado.

## Restrições aplicáveis

Skill de análise permite “A única escrita permitida é um novo artefato Markdown de análise”. Respeitada. AGENTS raiz/backend: Nix, Clean Architecture, migrations como evolução do schema, docstrings de cada função/classe com o que/como/finalidade. Handoffs futuros devem incluir docstrings em helpers, doubles, spies, métodos de setup/cleanup e cenários. Git/gh fora do Nix. Sem delegação a agentes: divisão abaixo é de responsabilidades futuras, não execução paralela autorizada.

## Classificação comentada

`engineering`, `integration/data/security`: testar colaboração real e preservação do estado, não decidir funcionalidade do produto. `design` da suíte; escopo de componente backend. Risco médio de falsa prova (doubles/skip/normalização) e baixo risco operacional por alvo descartável. Incerteza média por migrations e lacunas de produto. Reversibilidade fácil para testes e análise.

## Decisão de roteamento

Subpastas imediatas inventariadas: `backend`, `ambientes`, `frontend`, `templates`, `revisao`, `requisitos`. Escolhida `prompts/backend`, onde estão seleção, prévia, persistência de seções e a análise que originou o harness autenticado. `ambientes` é secundária; `revisao` não é determinada pelo tipo da atividade; `templates` não cabe por ser um prompt. `prompts/README.md` exige Markdown, objetivo, contexto e nome descritivo; não há AGENTS local. Confiança alta. Nova linhagem v001; não altera anteriores.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | alta | integração real + SQL independente | evita que agregado normalizado esconda escrita |
| security | alta | controles positivos e camadas distintas | recusa deve ter causa demonstrável |
| observability | alta | distinguir pass/skip/bloqueio | verde de runner não equivale a prova |
| simplicity | média | reaproveitar harness existente | limitar duplicação e custo de preparação |

## Alternativas consideradas

**A — ampliar integração ASGI com SQLite migrado e consultas de item em doubles explícitos.** Reusar BancoCurriculosAutenticadosIntegracao e helpers; ler agregado e SQL bruto em sessões independentes; testar API de seleção/ordem/prévia. Executável condicionada ao grafo; experimento temporário isola o bloqueio. Melhor adequação ao requisito completo de negativos/spies/SQL.

**B — integração direta caso de uso + repositório + SQLite migrado.** Viável como teste de persistência e domínio, sem HTTP/autenticação. Poderia executar seleção/ordem sem fábrica, mas negativos de middleware/framework exigiriam uma segunda composição e suíte. Não satisfaz sozinha a entrega pedida; custa mais se completada por uma matriz ASGI separada.

**C — especificação ASGI com repositório em memória e autenticação double.** Viável como integração entre unidades e precedentes existentes; rápida, mas não demonstra estado persistido em outra sessão/SQL bruto. Serve complemento, não substituto. Para esta entrega, restrição dura elimina C como solução única. Esperar composição produtiva/adapters completos também é opção de produto futura, mas não é necessário para A; implementar esses componentes agora violaria escopo.

## Perfil de pagamento comparativo

Escala ordinal, não somar.

| Dimensão | Prioridade | A | B | C | Confiança | Base |
|---|---|---|---|---|---|---|
| correctness | alta | +2 | +1 | -1 | alta | SQL e HTTP em A; SQL sem entrada em B; sem SQL em C |
| security | alta | +2 | 0 | +1 | alta | middleware e sessão real versus faltantes/doubles |
| observability | alta | +2 | +1 | 0 | alta | spies, snapshot, bloqueio explícito |
| simplicity | média | +1 | 0 | +2 | média | harness A já existe, C mais leve mas insuficiente |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### (c) Recomendações — decisão nesta versão

Adotar A, sob a interpretação explícita de L2. Escrever um fluxo positivo encadeado e matriz negativa em métodos separados, sem exigir encadear todos os negativos. Reutilizar cobertura S1–S10 existente como regressão; acrescentar o que falta e reforçar controles onde a exigência do usuário é mais forte. Não repetir toda a suíte de invariantes unitárias.

### Estrutura concreta proposta

Arquivos **novos** (não existem na inspeção):

- `src/backend/tests/test_integracao_selecao_ordenacao_curriculo.py`: `SelecaoOrdenacaoCurriculoIntegracaoTestCase(unittest.IsolatedAsyncioTestCase)`, fluxo positivo e negativos de integridade/ordem, proteção por camada e sessão excluída.
- `src/backend/tests/fixtures/selecao_ordenacao_curriculo.py`: dados dos seis tipos, builders tipados, extensão dedicada da composição, preflight completo, leitura de agregado+SQL, helpers de controle/spies. Não importar testes como bibliotecas.

Arquivo existente a alterar **somente se indispensável para reaproveitamento sem duplicação**: `src/backend/tests/fixtures/curriculos_autenticados_integracao.py`, para parametrizar consultas/seed ou extração mínima do mecanismo de migration. Preferir extensão/composição na fixture nova e manter a semântica dos consumidores atuais. É permitido mudar apenas o suporte de teste; não inventar métodos em produto. `fixtures/credenciais_sessao.py` serve de referência do processo Alembic, não alvo obrigatório.

Todo trecho novo deve conter `Proveniência: decision-analysis prompts/backend/20261025-193758-integracao-selecao-ordenacao-curriculo-v001.md#v001`. Comentário e docstrings não substituem nomes de comportamento.

#### Dados e preparação concreta

Reusar IDs A/B e currículos A/B do harness (`UUID(int=101/102)`, `201/202`), itens idioma existentes `301/302/303` e ausente `399`. Emitir sessão B com `CriadorSessaoSeguro(banco.repo_sessoes).criar(USUARIO_B)` e confirmar commit; token A já existe. Não falsificar autenticador. Adicionar currículo A2 com `CurriculoId(UUID(int=204))` e mesmo dono A, seleção e ordem próprias; não mudar CURRICULO_NOVO reservado `203` do harness. Isolamento A2 é distinto do isolamento A/B.

Fixture nova contém mapa tipado **por classe de ID**, com entidade válida de cada um dos seis tipos por A e B e pelo menos duas por seção para os testes de sort. IDs sintéticos sugeridos: `UUID(int=1000 + 100*t + i)`, `t=1..6` na ordem da tabela F3, `i=1..4`; reservar `i=90` para ausente. `i=1/2` pertencem a A, `3/4` a B. Um idioma A já selecionado pelo harness continua no conjunto esperado até removê-lo explicitamente; não assumir currículo inicial vazio. Builders devem seguir assinaturas atuais lidas na implementação; usar enumerações reais e Periodo, nunca instâncias sem validação. Valores de conteúdo propostos (dados de teste, **não fatos do produto**): projetos “Zeta”/“alfa”; competências “Zeta”/“alfa”; idiomas “Zeta”/“alfa”; documentos “Zeta.pdf”/“alfa.pdf”; dois textos iguais com IDs diferentes em um subcaso de desempate. Formações: andamento início 2024-02-01 e concluída fim 2025-12-01; experiências: mesmo início 2024-01-01, uma sem fim e outra com fim 2025-01-01. Resultados esperados são listas explícitas de IDs, não chamadas das funções de sort produtivas para gerar o próprio oráculo.

Adicionar entidade própria não selecionada em cada mapa para provar filtro da seleção. O mapa das duas portas é double observado, não banco de itens. Não semear tabelas específicas só para aparentar adaptação real.

Banco: arquivo SQLite único por teste/subcaso e migrations até **head único**; nunca create_all. FK ON por conexão; URL local criada pela fixture, nunca DATABASE_URL herdada. Aplicar migrations em subprocesso com ambiente mínimo como BancoCredenciaisSessao, ou thread serializada como harness existente, mas preservar URL/restauração em finally. Confirmar `alembic_version` na head esperada e tabela/coluna de seleção/ordem antes de semear. Em caso de erro inesperado de DDL, não converter em skip.

Isolamento: `try/finally`/cleanup para fechar patch stack, sessão, engine e diretório mesmo com SkipTest/assertion. Banco novo por método e por variante independente de matriz. Fluxo positivo conserva um banco entre etapas intencionalmente. Negativos podem usar `subTest`, mas não herdar estado entre variantes. Não paralelizar mutação de DATABASE_URL global.

#### Protocolo comum de prova, obrigatório em cada negativo

1. Estabelecer **controle positivo pareado** no mesmo currículo/mesma operação, não simplesmente outra rota que funcionou. Para dono B atacando A, controle é sessão A sobre o mesmo currículo A; para item B, provar B selecionando aquele item no currículo B **e** A selecionando item próprio no currículo A. Para currículo ausente, não existe sucesso literalmente sobre ID ausente: documentar impossibilidade lógica; controle é a mesma operação no currículo A existente (ou criar aquele ID pela fixture em banco pareado e controlado). Não mascarar essa exceção de pré-condição.
2. Para credencial expirada/revogada/conta excluída, provar operação em estado ativo **antes** da invalidação no mesmo recurso; quando a operação altera estado, recompor precondição por operação válida inversa ou banco pareado com mesmos IDs. Para duplicata, a primeira seleção 201 é controle; para remoção ausente, selecionar/remover 204 no mesmo item/currículo e depois repetir. Para ordem inválida, aplicar permutação válida 204 ao mesmo currículo antes de tentar variante. Para 503, mesma operação/recurso em factory com executor ligado é controle.
3. Resetar todos os spies e listas de consultas **depois do controle**, sem substituir o delegado. Fazer snapshot `antes` **após** a preparação/invalidação. Snapshot deve incluir todas as colunas e todas as linhas de `curriculos` e `curriculo_itens`, de A/A2/B, ordenando linhas só para comparação; contar currículos e referências.
4. Executar ASGI real por `requisitar`, sem chamar endpoint diretamente. Verificar status e JSON/detalhe por camada. Não comparar correlação aleatória. Não exigir texto interno do framework inteiro: para 422 de DTO, verificar `loc`/`type` relevante e ausência de execução.
5. Verificar executor: zero chamadas/awaits em 401/403/422 de framework/503; exatamente um call+await no caso que alcança domínio/aplicação; nenhum outro executor. Spy deve ser `AsyncMock(wraps=caso.executar)`/delegante. Conferir DTO (pessoa, currículo, referência/ordem). Nas recusas de currículo, consultas de dono/item zero; nas de item/duplicidade, consulta de dono uma; DELETE/ordem zero consultas de dono por contrato.
6. Confirmar sessão do fluxo (sem rollback que esconda escrita), como snapshot existente; abrir **outra AsyncSession** para SQL bruto com `select(CurriculoRegistro.__table__)` e `select(CurriculoItemRegistro.__table__)`. Comparar antes/depois byte/valor por coluna, inclusive texto `ordem_secoes`; não comparar só número de itens. Abrir sessão independente também para `RepositorioCurriculoSqlAlchemy.obter_por_id` e verificar referências e tupla de ordem. SQL bruto não é substituído pelo agregado.
7. Garantir B e A2 intactos, ausência de marcadores privados de B no corpo de erro, e contas/sessões não alteradas pela operação (quando snapshot dessas tabelas for incluído, estabelecer referência depois da invalidação intencional). Não afirmar que essas consultas provam toda a privacidade do sistema.

#### Cenários positivos propostos

Todos: origem do critério **inferido**; fontes que já definem comportamento indicadas. Camadas comuns: ASGI/FastAPI + middleware + sessão real + caso de uso + domínio + repositório + SQLite migrado; consultas de item são doubles. “P” é identificador desta especificação, não ID de aceite existente.

| ID / objetivo | Pré-condições | Passos | Resultado/verificações | Fonte / natureza da base |
|---|---|---|---|---|
| P1 `test_fluxo_seleciona_seis_tipos_ordena_secoes_e_desseleciona` | A/B ativos, A2, mapas tipados; snapshots iniciais | selecionar cada tipo próprio via POST em ordem deliberadamente diferente de tipo/ID; repetir com segundo item por seção; GET prévia/listagem; PUT ordem invertida; reler SQL+agregado; remover um selecionado por tipo via DELETE; reler tudo | cada POST 201 com conjunto completo sem duplicatas e resposta ordenada; banco contém par tipo/ID; prévia contém só selecionados resolvidos, listas ordenadas como F3; total_itens da listagem igual linhas; PUT/DELETE 204; ordem invertida preservada em SQL+agregado depois de remover; demais referências/conteúdo/metadados/dono estáveis; B/A2 intactos em cada etapa | F3–F7; domínio/casos/router/repo; RF03/05/07 e CT-RF03-03/05-02 para intenção, precisão do oráculo só implementada |
| P2 `test_repetir_ordem_valida_preserva_texto_e_selecao` | currículo A próprio, seleção conhecida, ordem já alterada | PUT mesma ordem duas vezes; reler em nova sessão após cada | 204 em ambas; sem mudança de seleção/campos; mesmo texto da ordem. Não exigir ausência de flush nem chamar idempotência de negócio aprovada | AtualizarOrdemSecoesCurriculo + setter + repo; caracterização da implementação |
| P3 `test_selecao_em_a_nao_altera_b_nem_segunda_versao_a` | A/A2/B com seleções/ordens diferentes, mesmo item próprio pode existir em A2 | POST/PUT/DELETE somente A; ler A2 e B e snapshots brutos após cada | operações só mudam seleção/ordem de A; seleção em uma versão não é global ao perfil | PK composta e repo filtrado, RF14 e matriz CT-RF03-02; cenário inferido |
| P4 `test_previa_caracteriza_item_resolvido_atual_e_omite_ausente` | referência selecionada e banco confirmado; mapa próprio ativo | GET controle; substituir conteúdo da entidade no double mantendo ID/dono; GET; retirar entrada do double; GET; reler SQL | alteração do double muda conteúdo retornado; ausência omite item sem remover referência SQL, contagem listagem permanece referência; limite: só reação do consumidor, não política produtiva de exclusão | GerarPreviaVersaoCurriculo e L5; caracterização, não aceite de exclusão |

P1 já prova ordenação automática dos itens na leitura, sem alegar nova operação manual. Não repetir todas as combinações de comparadores já cobertas por unidade; pelo menos um par invertido por seção, um desempate e exclusão de não selecionado dão sensibilidade ao encadeamento. Não testar ordem de chaves JSON como ordem de seções. Se se decidir caracterizar `itens_por_secao`, exigir ordem padrão explicitamente e rotular a divergência, nunca assert de ordem personalizada que o método não produz.

#### Matriz negativa proposta

Todos: origem **inferido**; objetivo = recusar/ocultar condição indicada sem alterar estado; aplicar integralmente protocolo pareado anterior. Cada linha constitui método separado ou variante isolada; nomes abaixo são propostos. Base implementada F5/F6 salvo fonte adicional. “Exec” é spy do caso da operação atacada; demais spies zero. S/D/O = POST seleção, DELETE desseleção, PUT ordem.

| ID / método proposto | Pré-condição específica e passos | Esperado / camada | Controle positivo e fonte |
|---|---|---|---|
| N1 `test_sessao_b_recusada_no_caminho_a` | B ativo tenta S/D/O em `/estudantes/A/curriculos/A` com payload válido; D aponta selecionado | 403 mensagem do middleware; Exec=0; consultas=0 | sessão A, mesmos IDs/operação e corpos; middleware `_usuario_id_recurso_estudante`; contrato de sessão define 403 |
| N2 `test_curriculo_alheio_sob_pessoa_autenticada_e_inexistente` | B ativo chama S/D/O em caminho de pessoa B mas currículo A; comparar a currículo ausente; depois orientação simétrica A/currículo B | 404 `Versão de currículo não encontrada.` nos dois, Exec=1; dono/item=0; SQL idêntico | dono legítimo no mesmo currículo e operação; ausente usa controle existente ou banco pareado explícito; guardas dos três casos reais |
| N3 `test_item_alheio_ou_ausente_por_tipo` | A sobre A tenta selecionar cada tipo com ID de B e ID não mapeado, não selecionados | 404 `Item do perfil não encontrado.` iguais; Exec=1; consulta proprietário=1; SQL/ordem intactos | B seleciona mesmo item B em B; A seleciona próprio em A; ConsultaProprietarioItem double e tradução de ReferenciaDeOutroProprietario |
| N4 `test_selecao_duplicada_nao_altera_banco` | selecionar item válido 201 em A; reset spies; repetir POST mesmo tipo/ID com mapa próprio ainda presente | 422 `Item já está incluído no currículo.`; Exec=1; dono=1; zero linha adicional e campos iguais | primeiro POST do mesmo recurso é controle; Curriculo.incluir_referencia; não inventar 409 |
| N5 `test_desselecao_ausente_nao_altera_banco` | mesmo item selecionado/removido legitimamente; tentar DELETE de novo | 422 `Item não está incluído no currículo.`; Exec=1; sem consultar item; estado intacto | DELETE anterior 204 no mesmo currículo/item; Curriculo.remover_referencia; não inventar 404 de item |
| N6 `test_tipo_ou_uuid_invalido_na_selecao_e_remocao` | cookie válido, currículo A; substituir tipo por `curso`/`hobby` ou UUID por `nao-uuid`; JSON S sem tipo/item_id ou inválido | 422 framework; Exec=0; nenhuma consulta de item | S/D com tipo/UUID válidos nos mesmos recursos; Literal/UUID/DTO; cada variante isolada |
| N7 `test_ordem_com_secao_desconhecida_ou_valor_invalido` | ordem válida controle; substituir uma entrada por `hobbies`, por número -1, ou enviar objeto/null em vez de lista | 422 framework enum/lista; Exec=0; texto original intacto | PUT com sete seções válidas; DTO SecaoCurriculo; não criar “posição negativa” inexistente |
| N8 `test_ordem_incompleta_ou_extensa` | depois de controle, remover uma seção; variante lista vazia; variante oito entradas | 422 framework comprimento; Exec=0 | PUT válido no mesmo A; Field min=max=7 |
| N9 `test_ordem_repetida_com_sete_entradas` | sete nomes válidos, repetir um e omitir outro mantendo tamanho sete | 422 detail de domínio de permutação; Exec=1; consultas dono=0 | PUT válido antes; _validar_ordem_secoes; distingue framework de domínio |
| N10 `test_dono_extra_na_ordem_e_ignorado_na_selecao` | S com usuario_id=B extra comparado ao controle sem extra; O com mesmo extra | **S retorna 201**, dono A e resultado igual ao controle; caracterização, não negativo de recusa. O retorna 422 extra_forbidden, Exec=0, SQL intacto | controles S/O válidos no mesmo currículo; BaseModel versus ConfigDict extra forbid; S6 existente. Não forçar S a recusar |
| N11 `test_credenciais_invalidas_interrompem_operacoes` | para cada S/D/O: sem cookie, token desconhecido, expirado, revogado; preparar estado em SQL e commit; tentar com payload válido | 401 detail uniforme; Exec=0; SQL currículo/seleção/ordem igual; Bearer/query/corpo válido não salva ausência de cookie | controle válido antes de invalidar, mesma operação/recurso; contrato credenciais, AutenticadorSessaoPersistida, repo sessão |
| N12 `test_conta_excluida_interrompe_operacoes` | S/D/O funcionam com A ativa; marcar UsuarioRegistro.deleted_at com UTC e commit, snapshot pós-exclusão; reapresentar token emitido | 401 detail uniforme, Exec=0; não tratar como 404 de currículo; nenhuma escrita pelas operações | controle ativo anterior no mesmo recurso/operação; filtro UsuarioRegistro.deleted_at e contrato de sessão; não chamar caso de exclusão de perfil para não importar efeitos de outro recurso |
| N13 `test_executor_ausente_com_autenticacao_ativa` | autenticação persistida mantida, caso da operação omitido em nova factory; payload válido | 503 específico de S/D/O; Exec=0; snapshot idêntico | mesma factory/dependências/recurso, caso ligado produz sucesso; handlers None. Não usar main indisponível para forçar 503 |
| N14 `test_precedencia_recusa_na_camada_correta` | variantes isoladas: sem cookie+corpo inválido; cookie B+caminho A+corpo inválido; cookie A+executor None+corpo inválido; currículo ausente+ordem duplicada de tamanho sete | respectivamente 401 Exec0; 403 Exec0; 422 framework Exec0; 404 currículo Exec1. Snapshot intacto em todos | controle válido mesma operação/recurso conforme protocolo, middleware/DTO/handler/caso; primeira prioridade sem misturar composições |

N6 inclui UUID de currículo e de pessoa malformado como variantes de formato: com cookie válido da pessoa correta onde parseável, 422 e zero executor. Não exigir detalhe de pessoa do middleware para UUID impossível de extrair. N11/N12 aplicam-se a todos os três métodos, não apenas POST. Nas recusas de prévia (opcional como regressão de leitura), usar mesma regra de controle, Exec da prévia e snapshot; não são substituto dos negativos S/D/O.

Reaproveitamento e custo: executar a suíte S1–S10 já existente como regressão e evitar duplicar toda a matriz de oito rotas no novo arquivo. O novo arquivo restringe-se a três operações e aos seis tipos, integridade, ordem, conta excluída e fluxo. Caso se reutilizem negativos antigos como parte da evidência requerida, conferir pareamento: atualmente S1 é controle separado e S5 remete a ele; **não satisfaz literalmente o controle por negativo no mesmo recurso**. Novo helper deve parear os controles relevantes; não declarar que cobertura antiga sozinha cumpre exigência ampliada.

Banco por teste/subcaso: custo estimado por estrutura, não medido, é `T ≈ N_bancos*(T_upgrade+T_seed+T_engine+T_cleanup)+N_requests*T_ASGI`. P1 usa um banco para muitas transições; cada negativo isolado um ou dois bancos para controle equivalente; matriz expandida pode demandar dezenas de migrations (N3 sozinho tem 12 recusas e controles por tipo). Orçamento inicial **estimado**, não limiar de aceite: centenas de milissegundos a poucos segundos por banco local; medir na primeira execução com `time.perf_counter`, reportar mediana/faixa. Se ficar caro, estudar snapshot/cópia de banco migrado em outra decisão, sem remover isolamento nem usar create_all.

### Impacto da revisão

Nenhum identificado — análise inicial. A recomendação permite implementar testes sem corrigir o backend e delimita explicitamente o que falta para prova produtiva.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | observa seleção e texto da ordem antes de qualquer normalização | snapshot bruto + agregado em nova sessão |
| security | prioritized | distingue entrada, propriedade do objeto e item | middleware/casos e spies delegantes |
| observability | prioritized | não confunde skip com aprovação | baseline e preflight explícitos |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| simplicity | dois arquivos de teste novos, reaproveitamento do harness | não construir aplicação paralela nem adapters produtivos |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | aceitar resposta sem persistência ou ordem normalizada | alta | estudantes/revisores |
| security | falso negativo porque rota sempre falha | alta | estudantes/equipe |
| observability | reportar skips como evidência executada | alta | revisão e entrega |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness/security | banco por variante e controles pareados | tempo de execução | aceitar e medir, não otimizar sem dado |
| simplicidade | consultas de itens em doubles | abrangência da prova | aceitar somente com limite explícito por tipo |
| observability | duas rodadas, original e experimento temporário | esforço operacional | necessário para distinguir bloqueio da cadeia original |

## Riscos e efeitos de segunda ordem

### Achados de backend — não corrigidos

1. **DER versus schema:** `docs/modelagem_der.md` apresenta seis tabelas associativas `CURRICULO_FORMACAO` etc., com FKs para itens; código/migration usam única `curriculo_itens` sem FKs de item. DER também não inclui ordem_secoes. Para efeito físico observado, modelo+migrations são mais confiáveis (executados/persistidos, AGENTS backend os define como fonte Code First); DER permanece intenção conceitual. Não importar suas FKs para o teste.
2. **Ordem personalizada versus prévia:** CT-RF05-02 pede ordem escolhida refletida no currículo; persistência existe; `itens_por_secao` usa padrão e DTO não transporta ordem. Código atual é mais confiável para caracterização HTTP; matriz orienta expectativa de produto, que permanece não demonstrável. Não escolher silenciosamente uma fonte nem “corrigir” o teste para ocultar a divergência.
3. **Jornada fala em ordenar itens**, `docs/mapeamento_jornadas.md:145`, mas não há operação manual equivalente em currículo. Sort automático da prévia existe. Documento genérico de jornada é menos preciso que contrato executável para escopo técnico; produto deve confirmar L2.
4. **Docstrings antigas de router dizem autenticação pendente**, mas factory aceita middleware e main já injeta autenticador indisponível. Código de composição atual governa a conclusão; comentários históricos não provam ausência de middleware. Persistência da sessão produtiva continua não composta.
5. **Segurança de item depende de portas sem adapter:** isolamento integrado com doubles prova reação do consumidor, não verificação real contra tabelas. Banco impede referência a currículo ausente, mas não item inexistente/de outro dono se escrita fora do caso de uso. Risco delimitado, sem implementar adapter aqui.
6. **Duas duplicatas e ramos terminais nas migrations:** teste que exige head original não pode demonstrar schema original saudável; não corrigir permanentemente. Warning Alembic com exit 0 é bloqueio, não sucesso.
7. **Política de exclusão parcial:** porta de prévia menciona formação excluída selecionada; comportamento dos demais tipos não foi uniformemente definido. Não extrapolar documento/experiência para todos.
8. **Extras divergentes:** seleção ignora dono extra, ordem o recusa. É comportamento atual verificável, não necessariamente vulnerabilidade: caminho é confrontado com sessão. Teste sem middleware não prova essa proteção. Nenhuma troca de dono é aceita pelos casos em estudo.
9. **Composição main não prova o fluxo:** middleware existe com autenticador indisponível e executores ausentes; rodar factory montada não certifica produção. Baseline verde tampouco cobre testes ignorados nem módulo integrado fora do discover.
10. **Normalização pode esconder dado:** agregado retorna frozenset; prévia filtra inexistentes/alheios e ordena; por isso SQL bruto é obrigatório. Não usar prévia como único teste de imutabilidade após recusa.

Não houve correção destes achados. Riscos fora da prova: condições concorrentes/lost update, atomicidade produtiva sob exceção, PostgreSQL, frontend, cookies em navegador real, login/deploy de produção, adaptadores reais de itens e geradores de exportação. Ausência de adaptação não é contornada escrevendo um SQL adapter de teste e chamando-o produtivo.

## Validação da decisão

### Execução futura, primeiro no estado original

Após aprovação desta versão e criação dos testes:

```sh
git status --short
git diff -- nix flake.nix flake.lock src/backend/infrastructure/persistence/alembic/versions
git diff --cached -- nix flake.nix flake.lock src/backend/infrastructure/persistence/alembic/versions
nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest -v backend.tests.test_integracao_selecao_ordenacao_curriculo
nix develop .#quality --command ruff check src/backend
```

Runner deve importar dependências opcionais com guarda específica **antes** dos imports que dependem delas, sem `ImportError` genérico que esconda bug. Se Python/framework/SQLAlchemy/Alembic/aiosqlite necessário não existir, marcar `SkipTest` com módulo e comando de ambiente. Ambiente atual oferece todos; não há justificativa para skip de dependência nele. Erro de sintaxe, schema, assertion, SQL inesperado ou caso de uso não vira skip.

Preflight da fixture nova: AST identifica revision duplicada, parent inexistente, ciclo e terminais; para duplicatas/múltiplas heads preexistentes esperadas, `SkipTest` explícito antes do banco. Não alterar helpers produtivos. `alembic heads`/`history` também devem capturar stderr e não aceitar UserWarning. Sem grafo válido, nenhum `create_all` como fallback. Registro deve separar `executed/pass`, `failed/error`, `skipped/environment`, `blocked/setup`; exit 0 com todos skips é **nenhuma prova de comportamento**.

O cenário ainda não existe; os comandos acima **não foram executados nesta análise**. Primeira execução original provavelmente reportará a duplicata, mas só o resultado real poderá confirmar skip e contagem. Registrar identidades e motivos de cada cenário ignorado com `-v`.

### Experimento temporário autorizado para execução posterior

Executar somente depois da rodada original e sob autorização da atividade de implementação/execução, nunca nesta análise. Se `git status`/diff/cached indicar qualquer alteração preexistente do usuário em `nix/`, `flake.nix`, `flake.lock` ou `src/backend/infrastructure/persistence/alembic/versions/`, **parar e informar**, sem restaurar, stashear ou sobrescrever. Usar apenas banco novo descartável; revisão renomeada não serve para migrar banco existente.

**Nix:** estado atual já fornece Python backend+aiosqlite; diff esperado é vazio. Somente se inspeção futura constatar ausência, mudança temporária restrita a `nix/tests.nix`: importar `./backend-python-packages.nix` e compor `pkgs.python3.withPackages (ps: backendPythonPackages ps ++ [ ps.aiosqlite ])`, como a versão atual já faz. Não alterar backend-python-packages, flake ou lock; não instalar globalmente. Registrar diff integral se houver; removê-lo ao final.

**Alembic:** plano mínimo proposto de **dois arquivos**, só identificadores/arestas; os dois merges existentes em tupla permanecem byte a byte. Introduz-se uma nova aresta de merge no down_revision de cursos para reunir os ramos terminais, sem criar arquivo ou DDL. “Linearização” aqui significa convergir para uma head, preservando os merges, não transformar todo o histórico em uma lista sem forks. Proposta validada por AST **em memória**, ainda não aplicada:

| Arquivo relativo a `src/backend/infrastructure/persistence/alembic/versions/` | Alteração exata |
|---|---|
| `20261015_0011_criar_cursos.py` | revision `20261015_0011` -> `20261015_0011_cursos`; down_revision `20261015_0010` -> `("20261017_0015", "20261017_0004")` |
| `20261015_0012_criar_links_profissionais.py` | revision `20261015_0012` -> `20261015_0012_links`; down_revision `20261015_0011` -> `20261015_0011_cursos` |

Resultado: o ramo que passa por sessões, pelos merges originais, exclusão lógica de formação, projetos e documentos termina em ordem de seções; o outro termina em associações. Cursos renomeado passa a depender dos dois terminais e links renomeado depende de cursos. Uma head `20261015_0012_links`. Exclusão lógica de formações e projetos preservam seus IDs originais e suas arestas. Cursos e links só possuem FK para usuários (DDL lido), já disponível nos ancestrais; não se inventa dependência DDL circular.

Justificativa de minimalidade: são necessários ao menos dois arquivos, um por par de revisions duplicadas; este plano atinge esse limite inferior. Uma alternativa também válida é renomear cursos/links e reencadear projetos/sessões, em quatro arquivos, com head 20261017_0015, sem nova tupla de merge. Foi rejeitada por tocar mais arquivos; o pedido preserva merges existentes e não proíbe introduzir aresta de merge. Se o executor receber restrição adicional de não criar nenhuma tupla nova, essa alternativa exige nova delimitação explícita, não mudança silenciosa do plano. Não alterar `upgrade`, `downgrade`, imports, nomes de tabelas/constraints ou dados; não mudar docstrings só para ajustar cabeçalho histórico.

Validação obrigatória do experimento:

1. Parsear AST dos arquivos, extrair Assign e AnnAssign de revision/down_revision; comprovar unicidade, toda referência existente, DFS sem ciclo e **uma única head**. Comparar AST anterior/posterior retirando apenas essas atribuições e exigir igualdade, além de diff restrito às **quatro atribuições em dois arquivos** da tabela. Verificar literalmente as duas tuplas de merge preexistentes, sem alteração. Não alterar o plano com base em mero número de versão cronológica.
2. `nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 alembic heads` e `nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 alembic history`: exit 0, head única e **nenhum warning Alembic**. Capturar stdout/stderr completos e inspecionar `UserWarning`, `alembic.util` e mensagens de revisão duplicada. Aviso Nix de árvore modificada é separado e não conta como warning Alembic.
3. Rodar cenário em `.#tests` com banco migrado até `head` e conferir `alembic_version`. Rodar regressão `backend.tests.test_integracao_recusa_curriculo_alheio` também em tests se a fixture compartilhada foi alterada; ao fim de cada execução de testes rodar gate Ruff. Guardar contagens/identidades pass/skip/error reais e tempos, não prometer resultado.
4. Repetir baseline informativo completo em backend conforme comando abaixo, comparar falhas/erros por identidade com ∅/∅; diferenças de skips por ambiente/experimento devem ser explicadas. Qualquer falha nova de teste sobre metadados históricos também deve ser relatada como falha do experimento; não editar teste antigo nem DDL para torná-lo verde.
5. Antes de restaurar, copiar **diff completo** de cada arquivo temporário para o resumo/PR, com marcas de original versus experimento, comandos e saídas. Este documento contém plano, não diffs aplicados; nesta análise os diffs temporários são vazios.
6. Em `finally`, restaurar somente caminhos explicitamente autorizados (e apenas se eram limpos no preflight). Git fora do Nix:

```sh
git restore -- src/backend/infrastructure/persistence/alembic/versions/20261015_0011_criar_cursos.py src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_links_profissionais.py
# Somente se nix/tests.nix foi temporariamente alterado e estava limpo:
git restore -- nix/tests.nix
git status --short
git diff --exit-code -- nix flake.nix flake.lock src/backend/infrastructure/persistence/alembic/versions
git diff --cached --exit-code -- nix flake.nix flake.lock src/backend/infrastructure/persistence/alembic/versions
```

Não usar `git restore .`, não tocar alterações do usuário e não restaurar a suíte nova. Os comandos de diff cobrindo a pasta inteira de versions e todo nix devem sair 0. `git status --short` pode listar testes/análise, mas **nenhum arquivo desses caminhos protegidos**, inclusive não rastreados. Se alterações inesperadas surgirem durante a rodada, parar a restauração automática e informar para preservar trabalho alheio. Diffs vazios finais são condição necessária para concluir experimento.

O segundo resultado prova componentes **sob grafo temporário**, não validade da cadeia original. Após restaurar, o bloqueio original deve continuar descrito; não alegar que a suite se tornou executável com prova completa no checkout original.

### Baseline, gates e evidência final

```sh
nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src
nix develop .#quality --command ruff check src/backend
```

Baseline real desta análise: 955, zero falhas, zero erros, 33 skips. Comparar por **identidades** de falhas/erros: qualquer identidade nova é regressão, ainda que total final coincida. Na futura execução usar também saída verbose ou `TestResult` para listar identidades; não adicionar runner permanente só para isso. Novos testes podem aumentar total e skips no backend sem constituir regressão; isso não os aprova. Gate obrigatório depois de cada rodada de teste. Se I001 surgir **nos arquivos apontados**, executar `nix develop .#quality --command ruff check --select I --fix <arquivos-apontados>` e repetir gate completo. Se apontar arquivo produtivo preexistente, não corrigir silenciosamente: preservar escopo e reportar. Nesta análise gate já passou sem nenhuma edição.

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| seleção persiste por currículo | linhas exatas e agregado em outra sessão | P1/P3 | status sem linha ou mudança em B/A2 |
| ordem persiste sem mudar seleção | texto exato e tupla relida | P1/P2 | default reaparece/perda de referências |
| leitura reflete seleção/sort automático | DTO com IDs explícitos | P1/P4 | não selecionado aparece ou ordem diverge |
| recusa vem da camada prevista | spy+consulta de item+status+SQL | N1–N14 | executor chamado antes da guarda ou qualquer escrita |
| experimento só muda grafo | diff+AST+heads/history sem warnings | plano temporário | DDL diferente ou warning Alembic |
| checkout preservado | status e diffs normal/cached protegidos | após cleanup | qualquer resíduo Nix/migration |
| nenhuma regressão nova | identidades comparadas a ∅/∅ | baseline completo e lint | qualquer falha/erro novo ou Ruff falhando |

## Handoffs e atividades posteriores

### Inventário e adequação das skills locais

Foram encontrados **sete** diretórios de skills em `.agents/skills`. Cada contrato de escopo e teste de adequação foi lido (caminhos na tabela de artefatos). Não há skill genérica presumida só pelo nome da pasta.

| Skill / evidência do contrato e adequação | Veredito para esta fatia |
|---|---|
| `decision-analysis-v4`: somente novo Markdown; método e roteamento nas referências lidas | **valid para esta análise**, invocada explicitamente; não implementa o teste |
| `integration-system-testing-v1`: SKILL permite fixtures/harness exclusivamente de teste; test-scope-boundary define integração e segurança já implementada; test-fit-check exige resultado de teste, fronteira real, oráculo e alvo seguro | **valid para testes limitados A**: quatro respostas positivas, ASGI+caso+SQL reais, SQLite descartável, oráculos explícitos. Produto/correção de migrations excluídos. Exige futura invocação explícita com este caminho/v001 e leitura do analysis-input-contract antes de escrever |
| `backend-domain-orchestration-v2`: clean-boundary e backend-fit-check exigem unidade interna isolada, proíbem testes superiores | **mismatch**: cases/domínio não serão implementados nem isolados |
| `backend-adapters-drivers-v2`: outer-boundary/backend-fit-check só unidade externa isolada; repository com banco real é integração | **mismatch**: nenhum adapter novo; SQL real cruza fronteira |
| `cross-cutting-implementation-v1`: scope-boundary encaminha autorização por API para testes superiores; fit-check exige testes unitários e mecanismo a implementar/avaliar | **mismatch**: validar autenticação integrada existente não autoriza alterar segurança |
| `frontend-implementation-v3`: scope-boundary/fit-check excluem testes superiores e backend | **mismatch**: nenhum cliente/tela no escopo |
| `nix-environment-implementation-v1`: nix-scope-boundary/fit-check exigem resultado exclusivamente Nix | **mismatch para a suíte**; eventual alteração temporária em tests.nix é uma fatia Nix separável e condicionada, hoje desnecessária |

Não existe lacuna de processo para a suíte: há skill elegível. Existe limite de processo para metadados **produtivos** das migrations: nem a skill de testes (que proíbe corrigir produto) nem a de Nix (que só permite artefatos Nix) cobre essa mutação. O pedido desta análise já exige **planejar** experimento temporário; para executar depois, a invocação deve autorizar expressamente a exceção limitada de quatro atribuições nesses dois arquivos, restauração/diffs e alvo descartável, além da fatia da skill de testes. Isso não é permissão para correção permanente. Não pedir nova aprovação genérica para os testes após sua invocação explícita; autorização deve ser concreta sobre esta versão.

Divisão de trabalho sequencial recomendada:

1. Executor de testes: dois arquivos propostos em `src/backend/tests`, ambiente tests; validação A e regressão pertinente; não toca produto. Novo código de teste com docstrings e proveniência.
2. Executor do experimento temporário, com instrução explícita: grafo e, só se necessário, tests.nix; ambientes tests/quality; restaura os caminhos e fornece diffs completos. Não delegar implicitamente essa responsabilidade a skill de unidade.
3. Responsáveis de produto/backend em outras demandas: L1/L2/L3/L5/L6/L7, adaptadores de item, composição e correção permanente das migrations. São handoffs, não pré-requisitos inventados para escrever a caracterização A.

Registro mínimo recomendado: este documento em prompts e descrição de PR contendo cenário, limites, nomes de arquivos, comandos, contagens/identidades, skips/motivos e diffs temporários completos. `prompts/README.md` e análises anteriores versionam decisões; a skill de testes diz que relatórios são outputs e não devem ser versionados sem convenção/finalidade aprovada. Evidências de responsividade em docs são precedentes específicos, não obrigação automática para backend. Não editar matriz nem criar relatório extra por suposição.

## Síntese

Decisão proposta: integrar ASGI, autenticação persistida, três operações reais, repositório e SQLite migrado; ampliar o harness existente com dados dos seis tipos, controle pareado, spies e SQL independente. Demonstrar ordem personalizada no agregado/banco e sort automático dos itens na prévia. Principal incerteza de execução: DDL sob cadeia original inválida; principal lacuna de produto: se o título pretendia ordem manual de itens ou apresentação personalizada de seções. Nenhum desses comportamentos ausentes será inventado ou implementado nesta análise.

## Apêndice A — entrada original do usuário (literal)

```text
$decision-analysis-v4 Implementar "Criar teste de integração para seleção e ordenação de itens no currículo.". O resultado esperado é um teste de integração executável, com **cenários positivos e negativos**. Antes de decidir o que ele contém, descubra o que o projeto define e implementa para selecionar itens do perfil num currículo e para ordená-los (ou ordenar suas seções), o que "item", "seleção" e "ordenação" significam neste projeto, como a propriedade e a existência dos itens são verificadas e o que o ferramental de teste disponível consegue provar. Esta é uma análise nova, iniciada do zero.

## Regra principal: não presumir

Todo fato deve vir de um artefato lido (histórico Git, código, testes, migrations, documentação de segurança, requisitos, DER, configuração de ambiente), com o caminho indicado. O que nenhum artefato definir deve ser registrado como lacuna, nunca como fato.

- Separe em seções distintas: **(a) fatos encontrados**, com caminho e trecho; **(b) lacunas**, ou seja, o que nenhum artefato define; **(c) recomendações**, que são suas, com justificativa.
- Para cada lacuna, apresente as opções viáveis, recomende uma e marque se depende de decisão de produto ou se pode ser tomada tecnicamente com base no que existe.
- Quando artefatos divergirem (código, documentação, requisitos, testes), aponte a divergência, diga qual fonte parece mais confiável e por quê, sem escolher em silêncio.
- Não transponha para currículo regras de outros recursos (perfil, formação, projeto, vagas, documentos) sem que um artefato sobre currículo as sustente.

## Ponto de partida

Parta exclusivamente do estado atual desta branch, criada a partir da `dev`. Não presuma a existência de nenhuma rota, caso de uso, teste, fixture, cenário ou análise sobre seleção ou ordenação de itens. Descubra por inspeção o que existe: o que existir entra como fato (com a cobertura avaliada), o que não existir entra como lacuna. **Inventarie os harnesses e fixtures de teste de integração que de fato existem na base** e não presuma nomes.

## Texto do card

Somente o título foi fornecido: "Criar teste de integração para seleção e ordenação de itens no currículo.". Não há descrição nem critérios de aceite. **Não invente critérios.** Derive o que for possível do título e dos artefatos, marque a origem de cada critério como "inferido" e liste exatamente o que precisa ser fornecido para fechar cada lacuna. O título e o pedido do usuário exigem **cobertura de seleção, de ordenação e de cenários positivos e negativos**: isso é requisito da entrega.

## Fontes a analisar

1. **Histórico Git local.** A CLI do GitHub e a rede podem não estar disponíveis; **não dependa delas**. Localize por inspeção (merges "Merge pull request #N", squashes com sufixo "(#N)", mensagens, nomes de branch e histórico dos arquivos) os trabalhos que criaram o currículo, a seleção de itens, a ordenação e a prévia. Número de card não é número de PR: não infira a ligação apenas pela coincidência de números, e registre como identificou cada trabalho.
2. **Documentação pertinente**, localizada por busca (não presumida): requisitos funcionais e não funcionais ligados a currículo, seleção de conteúdo, ordem de seções e itens, prévia e exportação; requisitos de segurança e propriedade de recursos; o contrato de credenciais de sessão; o DER; matrizes de rastreabilidade e de teste; e análises anteriores em `prompts/`. Registre os termos buscados (por exemplo seleção, selecionar, desselecionar, ordem, ordenação, posição, seção, item, currículo, prévia) e o que cada busca retornou, **inclusive resultados vazios**.
3. **Código atual relacionado**: entidades e value objects de currículo, itens e seções; casos de uso; portas; repositórios; modelo e migrations (colunas, constraints, chaves primárias, chaves estrangeiras, colunas de posição); rotas, handlers e DTOs; middleware de autenticação; composição da aplicação (`main.py` e `factory.py`); e os testes existentes, unitários e integrados, que toquem o tema.

## O que levantar

- **O que são "item", "seleção" e "ordenação" neste projeto.** Descubra, somente com base nos artefatos: quais tipos de item podem ser selecionados num currículo e como cada item é identificado; o que significa selecionar (registro de uma referência, cópia de dados ou outro); se existe ordem entre **seções**, entre **itens dentro de uma seção**, ou ambas; como a ordem é representada e persistida (coluna de posição, lista ordenada, outro); e se a ordem pertence a cada currículo. **Se o título abranger algo que não existe** (por exemplo ordenação de itens dentro de uma seção), registre como lacuna e diga como o título deve ser interpretado; não invente a operação.
- **O contrato por operação.** Para cada operação que seleciona, desseleciona, ordena ou lê seleção e ordem: método, caminho, de onde vem o identificador da pessoa (sessão, caminho, corpo), identificadores do currículo e do item, caso de uso, repositório, formato de entrada e de saída, status de sucesso e **de cada falha tratada**. Separe o que está **definido em documento** do que está **só implementado**.
- **Propriedade e existência dos itens.** Como o código verifica que o currículo pertence à pessoa e que o item **existe e pertence à mesma pessoa**; em qual camada cada recusa acontece (middleware, validação do framework, caso de uso, porta de consulta de item, repositório); e se a resposta para recurso de outra pessoa é **indistinguível** da resposta para recurso inexistente. Registre o que acontece com identificador de dono enviado pelo cliente. **Descubra se existem adaptadores concretos para as portas usadas na verificação dos itens (por tipo)**; se algum não existir, registre como lacuna e diga o que o teste pode usar no lugar (por exemplo doubles) e o que a prova deixa de cobrir.
- **Regras de integridade e de ordem.** Duplicidade de seleção, limites, remoção de item que já foi selecionado, o que acontece com a seleção quando o item é alterado ou excluído, o que acontece com a ordem ao selecionar e ao desselecionar (reposicionamento, lacunas, estabilidade), valores de ordem inválidos, seções ou itens desconhecidos ou repetidos na lista de ordenação, e qualquer invariante do domínio. Registre apenas o que estiver definido ou implementado; o restante é lacuna, sem inventar o comportamento esperado.
- **Precedência dos erros entre camadas.** Autenticação, validação do framework, propriedade do currículo, existência e propriedade do item, regras de domínio e indisponibilidade de executor: em que ordem são avaliadas e qual camada responde, para o cenário não misturar oráculos de composições diferentes.
- **Efeito observável.** Como a seleção e a ordem aparecem na leitura (por exemplo prévia ou listagem): se existe leitura que as reflita, o que ela devolve e se depende de adaptadores que podem não existir. Diga se o teste deve verificar o efeito por essa leitura, apenas pelo banco, ou ambos, e o que cada uma prova.
- **A composição real.** Como a aplicação que sobe (`main.py`, `factory.py`) instala a autenticação e os casos de seleção e ordenação, e se estão realmente ligados na composição de produção. **Não presuma o estado**: leia o código atual e registre o que a composição faz e o que isso implica para o que o cenário consegue provar. Recomende como o teste deve compor a aplicação e qual limite declarar sobre a composição de produção.
- **Cobertura existente:** o que os testes atuais já cobrem sobre seleção e ordenação, em que nível (unitário com doubles ou integração com banco real) e o que falta, para o cenário novo não repetir cobertura sem necessidade.
- **O que "teste de integração" significa no projeto.** Procure em `AGENTS.md`, nas referências das skills de teste, em `docs/` e em `prompts/` a classificação de níveis, as convenções e os precedentes (fluxo encadeado ou casos independentes). Avalie qual nível é viável com o que existe (por exemplo chamada ASGI atravessando middleware, caso de uso, repositório e banco migrado) e diga o que cada nível prova e o que não prova.
- **O ambiente de testes integrados:** o que `nix develop .#tests` oferece hoje, como os testes integrados existentes são organizados e executados, como o banco é preparado e como a autenticação é montada nos testes existentes.
- **Bloqueios de execução preexistentes:** verifique por inspeção e registre, **sem tratá-los como escopo e sem corrigi-los**, o estado da cadeia de migrations do Alembic (revisões duplicadas ou múltiplas heads), das dependências do ambiente `.#tests` e de qualquer operação do tema que não esteja implementada ou composta. Execute apenas comandos de leitura e um **baseline informativo** da suíte do backend, registrando comando, ambiente, resultado e contagens, sem alterar nada.

## Escopo

Definir o **teste de integração executável** de seleção e ordenação de itens no currículo, cobrindo cenários positivos e negativos: etapas, dados, verificações, resultados esperados, fixtures, forma de execução e limites do que prova.

Fora do escopo: alterar rotas, casos de uso, persistência, middleware, contrato ou composição; implementar operação ou adaptador que não exista; corrigir defeitos de back-end encontrados (registre-os como achados); ativar autenticação na composição de produção; front-end; novas regras de negócio ou de segurança; alterações permanentes de ambiente.

## Instruções

- Para cada decisão que os artefatos não resolverem, recomende uma opção com justificativa e marque se depende de produto.
- **Cobertura positiva e negativa obrigatória.** Cada cenário deve ter objetivo, pré-condições, passos, resultado esperado, a fonte que o sustenta, a origem do critério (definido ou inferido) e a camada exercitada. Considere, **apenas se algum artefato os definir ou implementar**:
  - **Positivos:** selecionar item válido de cada tipo relevante; selecionar vários itens; desselecionar; ordenar seções (e itens, se existir) e reler a ordem persistida; ordem refletida na leitura (prévia ou listagem), se existir; repetição ou idempotência, se definida; encadeamento seleção, ordenação e remoção; isolamento (as operações da pessoa A não alteram o currículo, a seleção nem a ordem da pessoa B).
  - **Negativos de propriedade:** B tentando selecionar, desselecionar ou ordenar em currículo de A; A selecionando **item de B** no próprio currículo; currículo inexistente; item inexistente; identificador de dono enviado pelo cliente que não pode alterar o proprietário.
  - **Negativos de integridade e de ordem:** seleção duplicada; item de tipo desconhecido; desselecionar item não selecionado; ordenação com seção ou item desconhecido, repetido ou faltante; valores de ordem inválidos; qualquer outra recusa que o domínio ou o framework implemente.
  - **Negativos de autenticação:** sem cookie, token desconhecido, sessão expirada, sessão revogada e conta excluída, conforme o contrato de credenciais.
  - **Controles e provas:** todo cenário negativo deve ter um **controle positivo** no mesmo recurso e na mesma operação, para provar que a recusa vem da regra e não de uma rota que sempre falha. Cada negativo deve provar que o **estado persistido não mudou**, por leitura em **outra sessão de banco e por consulta bruta às tabelas** (a leitura pelo agregado pode normalizar ou esconder diferenças de seleção e de posição), e deve verificar por spies delegantes se o caso de uso foi ou não chamado, conforme a camada que recusa. O que não estiver definido entra como lacuna, e a análise deve dizer se o cenário registra o comportamento atual como caracterização (rotulada como tal) ou aguarda decisão. Não force status que o código não produz.
- Defina a estrutura: nomes e localização dos arquivos conforme a convenção, reaproveitamento dos harnesses **que de fato existem na base** (verifique, não presuma), preparação do banco (migrations aplicadas até o head, nunca `create_all`), isolamento entre testes, dependências do ambiente e como os testes que dependem de recurso ausente são ignorados com motivo explícito, sem gerar erro quando o ambiente não os suporta. Diga se o fluxo positivo encadeado e a matriz negativa devem ser métodos separados e estime o custo de preparar um banco por teste.
- **Honestidade da prova.** Um teste ignorado não é prova. Diga como o resultado distingue "executado e aprovado" de "ignorado por ambiente", e o que o cenário não prova (por exemplo a composição de produção, concorrência, PostgreSQL, comportamento sob falha de banco, e a verificação de itens contra adaptadores que não existam).
- Registre achados de back-end (divergências entre código, documentação e contrato, comportamentos não definidos, riscos de segurança ou de privacidade) em seção própria, sem corrigi-los.
- Indique a divisão de trabalho. **Leia o contrato de escopo e o teste de adequação de cada skill inventariada em `.agents/skills` e confirme, com evidência, se esta fatia é elegível a alguma delas**; se nenhuma cobrir, registre como lacuna de processo e indique o que o usuário precisaria autorizar explicitamente. Especifique nomes de arquivos, ambientes e comandos, para o executor não precisar inventá-los. Diga também se o resultado precisa de um registro em documento ou se basta o texto do PR, e recomende o mínimo, de acordo com os precedentes do projeto.
- **Alterações temporárias de ambiente.** Registre que, para executar o cenário, o executor poderá aplicar alterações temporárias em `nix/tests.nix` (somente se o ambiente não oferecer Python do backend e o driver SQLite assíncrono) e, se a cadeia do Alembic estiver com revisões duplicadas ou múltiplas heads, uma **linearização temporária** das migrations. Proponha o plano concreto, arquivo por arquivo, alterando **somente identificadores e arestas** (nunca DDL), com o **menor número possível de arquivos**, **preservando os pontos de merge existentes** (`down_revision` em tupla) e com verificação por AST de unicidade, referências existentes, ausência de ciclo e uma única head, e por `alembic heads` e `alembic history` **sem warnings do Alembic** (não confundir avisos do Nix sobre árvore modificada com warnings do Alembic). Ambas as alterações devem ser revertidas por `git restore` com caminhos explícitos (nunca `git restore .`) ao final, com os diffs completos copiados para o resumo, e `git status --short` e `git diff --exit-code` (inclusive `--cached`) sem nenhum arquivo em `nix/`, `flake.nix`, `flake.lock` ou `alembic/versions/`. Se já houver mudanças do usuário nesses caminhos, a execução não deve restaurá-las: deve parar e informar. Recomende executar primeiro no estado original, para registrar skips e bloqueios, e depois sob o experimento temporário, deixando claro que o segundo prova os componentes sob o grafo temporário e não a cadeia original.
- Defina o roteamento do artefato de análise (pasta em `prompts/`) conforme a organização existente.
- Registre na validação: a execução do cenário em `nix develop .#tests`; a execução informativa da suíte completa em `nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src`, que não pode gerar erros novos em relação ao baseline observado (registre o baseline real, comparado por identidade de teste e não só por total); e o gate de lint do CI ao final de cada execução: `nix develop .#quality --command ruff check src/backend` (se falhar por I001, corrigir com `nix develop .#quality --command ruff check --select I --fix <arquivos-apontados>` e repetir o gate completo).
- Não implemente nada.
```
