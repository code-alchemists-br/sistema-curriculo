---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-24T10:56:07-03:00"
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
    - {"path":"AGENTS.md","relationship":"context","representation":"prose","function":"prompt-instruction","format":"markdown","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/AGENTS.md","relationship":"context","representation":"prose","function":"prompt-instruction","format":"markdown","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":".agents/skills/decision-analysis-v4/SKILL.md","relationship":"context","representation":"prose","function":"prompt-instruction","format":"markdown","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":".agents/skills/decision-analysis-v4/references/classification-taxonomy.md","relationship":"context","representation":"prose","function":"prompt-instruction","format":"markdown","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":".agents/skills/decision-analysis-v4/references/output-schema.md","relationship":"context","representation":"prose","function":"prompt-instruction","format":"markdown","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":".agents/skills/decision-analysis-v4/references/output-routing.md","relationship":"context","representation":"prose","function":"prompt-instruction","format":"markdown","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":".agents/skills/decision-analysis-v4/references/artifact-classification.md","relationship":"context","representation":"prose","function":"prompt-instruction","format":"markdown","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":".agents/skills/integration-system-testing-v1/SKILL.md","relationship":"context","representation":"prose","function":"prompt-instruction","format":"markdown","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":".agents/skills/integration-system-testing-v1/references/test-scope-boundary.md","relationship":"context","representation":"prose","function":"prompt-instruction","format":"markdown","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":".agents/skills/integration-system-testing-v1/references/analysis-input-contract.md","relationship":"context","representation":"prose","function":"prompt-instruction","format":"markdown","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":".agents/skills/integration-system-testing-v1/references/test-fit-check.md","relationship":"context","representation":"prose","function":"prompt-instruction","format":"markdown","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"prompts/README.md","relationship":"context","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"whole-file","locator":"organização e convenções","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"docs/requisitos_funcionais.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"RF01–RF03, RF13 e definições pendentes","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"docs/requisitos-seguranca.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"2: autenticação; 3: autorização; 4.10–4.16: retenção, exclusão e privacidade","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"docs/contrato-credenciais-sessao.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"contrato integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"docs/modelagem_der.md","relationship":"supporting","representation":"diagram-model","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"USUARIO, SESSAO e relações","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"docs/matriz_testes.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"objetivo, convenções, RF01, RF02 e ocorrências de perfil","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"docs/matriz_rastreabilidade.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"linhas RF02/RF13 e divergência de cobertura RF02","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"docs/casos-de-uso-v2.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"visão geral, atores, diagrama e identificação de UC01/UC02","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"docs/configuracao-ambiente.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"integral, em especial utilização do Nix e execução local","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"docs/Arquitetura/ADR-002-autenticacao-autorizacao-propriedade.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"contexto, decisão, RBAC, verificação e pendências","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"fatos, perguntas, critérios, alternativas e exclusão","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"prompts/backend/20261015-120000-expor-exclusao-perfil-estudante-v001.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"solicitação, decisão de produto, escopo e validação","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"prompts/backend/20261018-131822-validacao-contrato-credenciais-cards-80-82-v001.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"cenários, ambiente, achados, validação e handoffs","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"prompts/backend/20261019-082400-integracao-crud-informacoes-complementares-v001.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"escopo, testes integrados, ambiente e validação","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"prompts/backend/20260916-cadastro-acesso-estudante-v002.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"escopo, critérios, restrições e roteamento","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"prompts/backend/20261013-004854-expor-consulta-dados-pessoais-estudante-v007.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"frontmatter e fontes de autenticação","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/api/cadastro_acesso.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"DTOs, router e handlers","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/api/perfil_estudante.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"DTOs, principal e todos os handlers","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/api/middleware_autenticacao.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"rotas públicas, dispatch, autorização e extração de UUID","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/api/factory.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"assinatura de create_app, defaults, instalação do middleware e routers","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/main.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"engine, lifespan e composição exportada","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/application/cadastro_estudante.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"entrada e executar","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/application/acesso_estudante.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"entrada, falha e executar","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/application/perfil_estudante.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"entradas e casos EditarPerfil, ExcluirPerfil e ConsultarPerfilEstudante","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/application/perfil_completo.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"entrada e AtualizarPerfilCompleto","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/application/ports.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"RepositorioUsuario, GeradorUsuarioId e contratos de I/O","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/application/autenticacao_sessao.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"ConsultaSessaoAtiva e AutenticadorSessao","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/application/sessoes.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"portas de criação, persistência e revogação","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/domain/usuario.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"agregado e transições","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/domain/value_objects.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"UsuarioId, Nome, Email, Cidade, Endereco, Telefone, DadosContato e HashSenha","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"todos os métodos","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/sqlalchemy/repositorio_sessao.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"consulta ativa, salvar e revogar","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/sqlalchemy/usuario.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"mapping e conversões","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/sqlalchemy/sessao.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"mapping","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/security/autenticador_sessao.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"autenticar","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/security/autenticador_sessao_indisponivel.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"fallback","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/security/senhas.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"scrypt, derivar e conferir","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/security/tokens_sessao.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"criação e revogação","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/alembic/env.py","relationship":"primary","representation":"source-code","function":"production","format":"python","analysis_scope":"selected-section","locator":"URL, metadata e execução","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/alembic/versions/20260916_0001_criar_usuarios.py","relationship":"supporting","representation":"source-code","function":"schema-contract","format":"python","analysis_scope":"selected-section","locator":"upgrade e identificadores","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/alembic/versions/20261012_0004_criar_sessoes.py","relationship":"supporting","representation":"source-code","function":"schema-contract","format":"python","analysis_scope":"selected-section","locator":"upgrade e identificadores","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/alembic/versions/20261014_0007_adicionar_dados_contato_usuario.py","relationship":"supporting","representation":"source-code","function":"schema-contract","format":"python","analysis_scope":"selected-section","locator":"upgrade e identificadores","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/alembic/versions/20261013_0004_adicionar_dados_consulta_estudante.py","relationship":"supporting","representation":"source-code","function":"schema-contract","format":"python","analysis_scope":"selected-section","locator":"upgrade e identificadores","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/alembic/versions/20261015_0011_criar_cursos.py","relationship":"supporting","representation":"source-code","function":"schema-contract","format":"python","analysis_scope":"selected-section","locator":"declarações revision/down_revision","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/alembic/versions/20261015_0011_exclusao_logica_formacoes_academicas.py","relationship":"supporting","representation":"source-code","function":"schema-contract","format":"python","analysis_scope":"selected-section","locator":"declarações revision/down_revision","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_links_profissionais.py","relationship":"supporting","representation":"source-code","function":"schema-contract","format":"python","analysis_scope":"selected-section","locator":"declarações revision/down_revision","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_projetos_academicos.py","relationship":"supporting","representation":"source-code","function":"schema-contract","format":"python","analysis_scope":"selected-section","locator":"declarações revision/down_revision","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/alembic/versions/20261016_0013_criar_documentos.py","relationship":"supporting","representation":"source-code","function":"schema-contract","format":"python","analysis_scope":"selected-section","locator":"declarações revision/down_revision","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/alembic/versions/20261017_0004_criar_associacoes_curriculo_vaga.py","relationship":"supporting","representation":"source-code","function":"schema-contract","format":"python","analysis_scope":"selected-section","locator":"declarações revision/down_revision","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/infrastructure/persistence/alembic/versions/20261017_0015_adicionar_ordem_secoes_curriculos.py","relationship":"supporting","representation":"source-code","function":"schema-contract","format":"python","analysis_scope":"selected-section","locator":"declarações revision/down_revision","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_domain_perfil_estudante.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"integral: edição, exclusão e idempotência","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_application_perfil_estudante.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"classes EditarPerfilTestCase, ExcluirPerfilTestCase, ConsultarPerfilEstudanteTestCase","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_application_cadastro_estudante.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"nomes dos testes de cadastro e duplicidade","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_api_acesso_estudante.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"doubles, chamada direta e emissão de cookie","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_api_perfil_estudante.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"estrutura/nome dos casos; corpos da classe de exclusão","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_infrastructure_repositorio_usuario.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"nomes dos testes e declarações de doubles/transações","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_integracao_recusa_perfil_alheio.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"harness, matriz A/B e asserções","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_integracao_persistencia_dados_pessoais.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"integral: create_all e roundtrip","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_integracao_persistencia_sessao.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"estrutura, M01–M03/P01–P03 e dependências","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_integracao_contrato_credenciais_sessao.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"setup, controles, asserts, lista H/R e corpo H08/H09","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_integracao_composicao_credenciais_sessao.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"C01, subprocesso e skip C02","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_integracao_crud_informacoes_complementares.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"docstring, doubles e nomes dos testes","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_integracao_rejeicao_requisicoes_sem_credenciais_validas.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"skips de composição produtiva","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_main.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"integral: engine e lifecycle","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/fixtures/credenciais_sessao.py","relationship":"supporting","representation":"source-code","function":"data-fixture","format":"python","analysis_scope":"selected-section","locator":"preflight, BancoCredenciaisSessao, preparar, snapshot, requisitar, resposta e solicitar_asgi","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/fixtures/perfis_integracao.py","relationship":"supporting","representation":"source-code","function":"data-fixture","format":"python","analysis_scope":"selected-section","locator":"primeiras 120 linhas: seed híbrido e leitura","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"nix/tests.nix","relationship":"supporting","representation":"executable-script","function":"build","format":"nix","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"nix/backend.nix","relationship":"supporting","representation":"executable-script","function":"build","format":"nix","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"nix/backend-python-packages.nix","relationship":"supporting","representation":"executable-script","function":"build","format":"nix","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"alembic.ini","relationship":"supporting","representation":"structured-data","function":"configuration","format":"ini","analysis_scope":"whole-file","locator":"integral","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":".github/workflows/ci.yml","relationship":"context","representation":"structured-data","function":"configuration","format":"yaml","analysis_scope":"selected-section","locator":"jobs backend-lint, backend-tests e backend-integration-tests","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"docs/requisitos_nao_funcionais.md","relationship":"supporting","representation":"prose","function":"documentation","format":"markdown","analysis_scope":"selected-section","locator":"RNF04, RNF08, verificações e pendências","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_application_acesso_estudante.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"whole-file","locator":"sucesso, ausência, senha incorreta e perfil excluído com stubs","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_application_perfil_completo.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"selected-section","locator":"AtualizarPerfilCompletoTestCase, linhas 106–185","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
    - {"path":"src/backend/tests/test_infrastructure_senhas.py","relationship":"supporting","representation":"source-code","function":"test","format":"python","analysis_scope":"whole-file","locator":"derivação e conferência scrypt reais","content_state":"working-tree","revision":"cd4ee467441ead48b0673741e9544f380cde5929","availability":"available"}
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/ambientes, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "Cenário de integração do backend, com HTTP, perfil, sessão e persistência; precedentes correlatos em backend e suporte Nix secundário."
classification:
  sphere: engineering
  concerns: [integration, security, privacy]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: medium
---

# Análise de decisão — cenário integrado do ciclo de vida do perfil autorizado

## Solicitação original

A transcrição literal da demanda está no apêndice A. O título fornecido é: "Criar cenário de integração para cadastro, consulta, edição e exclusão de perfil autorizado". A instrução final é: "Não implemente nada."

## Informações complementares

Análise nova por solicitação explícita, sem herdar decisões de análises anteriores como fatos atuais. As análises encontradas são fontes de contexto e de decisões históricas, confrontadas com o código da branch. A repetição da mesma demanda durante a sessão não mudou o escopo. A skill foi fornecida em `.agents/skills/decision-analysis-v4/SKILL.md` e lida com suas referências. Não houve consulta ao GitHub nem à rede.

## Mudanças desde a versão anterior

Nenhum identificado — `initial`, primeira versão desta linhagem de cenário de ciclo de vida. Existem análises de cadastro, consulta, exclusão e contrato de sessão; elas não são versões anteriores desta demanda.

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `AGENTS.md` | context | prose | prompt-instruction | markdown | whole-file: integral | working-tree @ cd4ee46 |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | markdown | whole-file: integral | working-tree @ cd4ee46 |
| `.agents/skills/decision-analysis-v4/SKILL.md` | context | prose | prompt-instruction | markdown | whole-file: integral | working-tree @ cd4ee46 |
| `.agents/skills/decision-analysis-v4/references/classification-taxonomy.md` | context | prose | prompt-instruction | markdown | whole-file: integral | working-tree @ cd4ee46 |
| `.agents/skills/decision-analysis-v4/references/output-schema.md` | context | prose | prompt-instruction | markdown | whole-file: integral | working-tree @ cd4ee46 |
| `.agents/skills/decision-analysis-v4/references/output-routing.md` | context | prose | prompt-instruction | markdown | whole-file: integral | working-tree @ cd4ee46 |
| `.agents/skills/decision-analysis-v4/references/artifact-classification.md` | context | prose | prompt-instruction | markdown | whole-file: integral | working-tree @ cd4ee46 |
| `.agents/skills/integration-system-testing-v1/SKILL.md` | context | prose | prompt-instruction | markdown | whole-file: integral | working-tree @ cd4ee46 |
| `.agents/skills/integration-system-testing-v1/references/test-scope-boundary.md` | context | prose | prompt-instruction | markdown | whole-file: integral | working-tree @ cd4ee46 |
| `.agents/skills/integration-system-testing-v1/references/analysis-input-contract.md` | context | prose | prompt-instruction | markdown | whole-file: integral | working-tree @ cd4ee46 |
| `.agents/skills/integration-system-testing-v1/references/test-fit-check.md` | context | prose | prompt-instruction | markdown | whole-file: integral | working-tree @ cd4ee46 |
| `prompts/README.md` | context | prose | documentation | markdown | whole-file: organização e convenções | working-tree @ cd4ee46 |
| `docs/requisitos_funcionais.md` | supporting | prose | documentation | markdown | selected-section: RF01–RF03, RF13 e definições pendentes | working-tree @ cd4ee46 |
| `docs/requisitos-seguranca.md` | supporting | prose | documentation | markdown | selected-section: 2: autenticação; 3: autorização; 4.10–4.16: retenção, exclusão e privacidade | working-tree @ cd4ee46 |
| `docs/contrato-credenciais-sessao.md` | supporting | prose | documentation | markdown | selected-section: contrato integral | working-tree @ cd4ee46 |
| `docs/modelagem_der.md` | supporting | diagram-model | documentation | markdown | selected-section: USUARIO, SESSAO e relações | working-tree @ cd4ee46 |
| `docs/matriz_testes.md` | supporting | prose | documentation | markdown | selected-section: objetivo, convenções, RF01, RF02 e ocorrências de perfil | working-tree @ cd4ee46 |
| `docs/matriz_rastreabilidade.md` | supporting | prose | documentation | markdown | selected-section: linhas RF02/RF13 e divergência de cobertura RF02 | working-tree @ cd4ee46 |
| `docs/casos-de-uso-v2.md` | supporting | prose | documentation | markdown | selected-section: visão geral, atores, diagrama e identificação de UC01/UC02 | working-tree @ cd4ee46 |
| `docs/configuracao-ambiente.md` | supporting | prose | documentation | markdown | selected-section: integral, em especial utilização do Nix e execução local | working-tree @ cd4ee46 |
| `docs/Arquitetura/ADR-002-autenticacao-autorizacao-propriedade.md` | supporting | prose | documentation | markdown | selected-section: contexto, decisão, RBAC, verificação e pendências | working-tree @ cd4ee46 |
| `prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md` | supporting | prose | documentation | markdown | selected-section: fatos, perguntas, critérios, alternativas e exclusão | working-tree @ cd4ee46 |
| `prompts/backend/20261015-120000-expor-exclusao-perfil-estudante-v001.md` | supporting | prose | documentation | markdown | selected-section: solicitação, decisão de produto, escopo e validação | working-tree @ cd4ee46 |
| `prompts/backend/20261018-131822-validacao-contrato-credenciais-cards-80-82-v001.md` | supporting | prose | documentation | markdown | selected-section: cenários, ambiente, achados, validação e handoffs | working-tree @ cd4ee46 |
| `prompts/backend/20261019-082400-integracao-crud-informacoes-complementares-v001.md` | supporting | prose | documentation | markdown | selected-section: escopo, testes integrados, ambiente e validação | working-tree @ cd4ee46 |
| `prompts/backend/20260916-cadastro-acesso-estudante-v002.md` | supporting | prose | documentation | markdown | selected-section: escopo, critérios, restrições e roteamento | working-tree @ cd4ee46 |
| `prompts/backend/20261013-004854-expor-consulta-dados-pessoais-estudante-v007.md` | supporting | prose | documentation | markdown | selected-section: frontmatter e fontes de autenticação | working-tree @ cd4ee46 |
| `src/backend/api/cadastro_acesso.py` | primary | source-code | production | python | selected-section: DTOs, router e handlers | working-tree @ cd4ee46 |
| `src/backend/api/perfil_estudante.py` | primary | source-code | production | python | selected-section: DTOs, principal e todos os handlers | working-tree @ cd4ee46 |
| `src/backend/api/middleware_autenticacao.py` | primary | source-code | production | python | selected-section: rotas públicas, dispatch, autorização e extração de UUID | working-tree @ cd4ee46 |
| `src/backend/api/factory.py` | primary | source-code | production | python | selected-section: assinatura de create_app, defaults, instalação do middleware e routers | working-tree @ cd4ee46 |
| `src/backend/main.py` | primary | source-code | production | python | selected-section: engine, lifespan e composição exportada | working-tree @ cd4ee46 |
| `src/backend/application/cadastro_estudante.py` | primary | source-code | production | python | selected-section: entrada e executar | working-tree @ cd4ee46 |
| `src/backend/application/acesso_estudante.py` | primary | source-code | production | python | selected-section: entrada, falha e executar | working-tree @ cd4ee46 |
| `src/backend/application/perfil_estudante.py` | primary | source-code | production | python | selected-section: entradas e casos EditarPerfil, ExcluirPerfil e ConsultarPerfilEstudante | working-tree @ cd4ee46 |
| `src/backend/application/perfil_completo.py` | primary | source-code | production | python | selected-section: entrada e AtualizarPerfilCompleto | working-tree @ cd4ee46 |
| `src/backend/application/ports.py` | primary | source-code | production | python | selected-section: RepositorioUsuario, GeradorUsuarioId e contratos de I/O | working-tree @ cd4ee46 |
| `src/backend/application/autenticacao_sessao.py` | primary | source-code | production | python | selected-section: ConsultaSessaoAtiva e AutenticadorSessao | working-tree @ cd4ee46 |
| `src/backend/application/sessoes.py` | primary | source-code | production | python | selected-section: portas de criação, persistência e revogação | working-tree @ cd4ee46 |
| `src/backend/domain/usuario.py` | primary | source-code | production | python | selected-section: agregado e transições | working-tree @ cd4ee46 |
| `src/backend/domain/value_objects.py` | primary | source-code | production | python | selected-section: UsuarioId, Nome, Email, Cidade, Endereco, Telefone, DadosContato e HashSenha | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py` | primary | source-code | production | python | selected-section: todos os métodos | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_sessao.py` | primary | source-code | production | python | selected-section: consulta ativa, salvar e revogar | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/sqlalchemy/usuario.py` | primary | source-code | production | python | selected-section: mapping e conversões | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/sqlalchemy/sessao.py` | primary | source-code | production | python | selected-section: mapping | working-tree @ cd4ee46 |
| `src/backend/infrastructure/security/autenticador_sessao.py` | primary | source-code | production | python | selected-section: autenticar | working-tree @ cd4ee46 |
| `src/backend/infrastructure/security/autenticador_sessao_indisponivel.py` | primary | source-code | production | python | selected-section: fallback | working-tree @ cd4ee46 |
| `src/backend/infrastructure/security/senhas.py` | primary | source-code | production | python | selected-section: scrypt, derivar e conferir | working-tree @ cd4ee46 |
| `src/backend/infrastructure/security/tokens_sessao.py` | primary | source-code | production | python | selected-section: criação e revogação | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/alembic/env.py` | primary | source-code | production | python | selected-section: URL, metadata e execução | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/alembic/versions/20260916_0001_criar_usuarios.py` | supporting | source-code | schema-contract | python | selected-section: upgrade e identificadores | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/alembic/versions/20261012_0004_criar_sessoes.py` | supporting | source-code | schema-contract | python | selected-section: upgrade e identificadores | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/alembic/versions/20261014_0007_adicionar_dados_contato_usuario.py` | supporting | source-code | schema-contract | python | selected-section: upgrade e identificadores | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/alembic/versions/20261013_0004_adicionar_dados_consulta_estudante.py` | supporting | source-code | schema-contract | python | selected-section: upgrade e identificadores | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/alembic/versions/20261015_0011_criar_cursos.py` | supporting | source-code | schema-contract | python | selected-section: declarações revision/down_revision | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/alembic/versions/20261015_0011_exclusao_logica_formacoes_academicas.py` | supporting | source-code | schema-contract | python | selected-section: declarações revision/down_revision | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_links_profissionais.py` | supporting | source-code | schema-contract | python | selected-section: declarações revision/down_revision | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_projetos_academicos.py` | supporting | source-code | schema-contract | python | selected-section: declarações revision/down_revision | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/alembic/versions/20261016_0013_criar_documentos.py` | supporting | source-code | schema-contract | python | selected-section: declarações revision/down_revision | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/alembic/versions/20261017_0004_criar_associacoes_curriculo_vaga.py` | supporting | source-code | schema-contract | python | selected-section: declarações revision/down_revision | working-tree @ cd4ee46 |
| `src/backend/infrastructure/persistence/alembic/versions/20261017_0015_adicionar_ordem_secoes_curriculos.py` | supporting | source-code | schema-contract | python | selected-section: declarações revision/down_revision | working-tree @ cd4ee46 |
| `src/backend/tests/test_domain_perfil_estudante.py` | supporting | source-code | test | python | selected-section: integral: edição, exclusão e idempotência | working-tree @ cd4ee46 |
| `src/backend/tests/test_application_perfil_estudante.py` | supporting | source-code | test | python | selected-section: classes EditarPerfilTestCase, ExcluirPerfilTestCase, ConsultarPerfilEstudanteTestCase | working-tree @ cd4ee46 |
| `src/backend/tests/test_application_cadastro_estudante.py` | supporting | source-code | test | python | selected-section: nomes dos testes de cadastro e duplicidade | working-tree @ cd4ee46 |
| `src/backend/tests/test_api_acesso_estudante.py` | supporting | source-code | test | python | selected-section: doubles, chamada direta e emissão de cookie | working-tree @ cd4ee46 |
| `src/backend/tests/test_api_perfil_estudante.py` | supporting | source-code | test | python | selected-section: estrutura/nome dos casos; corpos da classe de exclusão | working-tree @ cd4ee46 |
| `src/backend/tests/test_infrastructure_repositorio_usuario.py` | supporting | source-code | test | python | selected-section: nomes dos testes e declarações de doubles/transações | working-tree @ cd4ee46 |
| `src/backend/tests/test_integracao_recusa_perfil_alheio.py` | supporting | source-code | test | python | selected-section: harness, matriz A/B e asserções | working-tree @ cd4ee46 |
| `src/backend/tests/test_integracao_persistencia_dados_pessoais.py` | supporting | source-code | test | python | selected-section: integral: create_all e roundtrip | working-tree @ cd4ee46 |
| `src/backend/tests/test_integracao_persistencia_sessao.py` | supporting | source-code | test | python | selected-section: estrutura, M01–M03/P01–P03 e dependências | working-tree @ cd4ee46 |
| `src/backend/tests/test_integracao_contrato_credenciais_sessao.py` | supporting | source-code | test | python | selected-section: setup, controles, asserts, lista H/R e corpo H08/H09 | working-tree @ cd4ee46 |
| `src/backend/tests/test_integracao_composicao_credenciais_sessao.py` | supporting | source-code | test | python | selected-section: C01, subprocesso e skip C02 | working-tree @ cd4ee46 |
| `src/backend/tests/test_integracao_crud_informacoes_complementares.py` | supporting | source-code | test | python | selected-section: docstring, doubles e nomes dos testes | working-tree @ cd4ee46 |
| `src/backend/tests/test_integracao_rejeicao_requisicoes_sem_credenciais_validas.py` | supporting | source-code | test | python | selected-section: skips de composição produtiva | working-tree @ cd4ee46 |
| `src/backend/tests/test_main.py` | supporting | source-code | test | python | selected-section: integral: engine e lifecycle | working-tree @ cd4ee46 |
| `src/backend/tests/fixtures/credenciais_sessao.py` | supporting | source-code | data-fixture | python | selected-section: preflight, BancoCredenciaisSessao, preparar, snapshot, requisitar, resposta e solicitar_asgi | working-tree @ cd4ee46 |
| `src/backend/tests/fixtures/perfis_integracao.py` | supporting | source-code | data-fixture | python | selected-section: primeiras 120 linhas: seed híbrido e leitura | working-tree @ cd4ee46 |
| `nix/tests.nix` | supporting | executable-script | build | nix | whole-file: integral | working-tree @ cd4ee46 |
| `nix/backend.nix` | supporting | executable-script | build | nix | whole-file: integral | working-tree @ cd4ee46 |
| `nix/backend-python-packages.nix` | supporting | executable-script | build | nix | whole-file: integral | working-tree @ cd4ee46 |
| `alembic.ini` | supporting | structured-data | configuration | ini | whole-file: integral | working-tree @ cd4ee46 |
| `.github/workflows/ci.yml` | context | structured-data | configuration | yaml | selected-section: jobs backend-lint, backend-tests e backend-integration-tests | working-tree @ cd4ee46 |
| `docs/requisitos_nao_funcionais.md` | supporting | prose | documentation | markdown | selected-section: RNF04, RNF08, verificações e pendências | working-tree @ cd4ee46 |
| `src/backend/tests/test_application_acesso_estudante.py` | supporting | source-code | test | python | whole-file: sucesso, ausência, senha incorreta e perfil excluído com stubs | working-tree @ cd4ee46 |
| `src/backend/tests/test_application_perfil_completo.py` | supporting | source-code | test | python | selected-section: AtualizarPerfilCompletoTestCase, linhas 106–185 | working-tree @ cd4ee46 |
| `src/backend/tests/test_infrastructure_senhas.py` | supporting | source-code | test | python | whole-file: derivação e conferência scrypt reais | working-tree @ cd4ee46 |

O estado dos arquivos da tabela é `working-tree`, sem modificações no início da investigação, baseado no HEAD `cd4ee467441ead48b0673741e9544f380cde5929`. A branch observada por `git branch --show-current` é `test-integracao-perfil-autorizado`. A origem em `dev` é declaração do usuário; não foi inferida de igualdade de nomes ou números de tarefas.

Histórico adicional: metadados de commits e listas de arquivos de `git show --stat`, histórico dos caminhos de cadastro/acesso/perfil/repositório e intervalos entre pais dos merges, descritos em F01. Relação: supporting; representação: structured-data; função: documentation; formato: metadados Git; recorte: mensagens, pais e arquivos alterados; estado: commit, hashes expressos em F01. Nenhuma descrição remota de PR/card foi obtida.

### Limites da evidência dos artefatos

O inventário diferencia leitura de código, recortes documentais e leitura somente de nomes de testes. Não equivale a auditoria exaustiva de todo o repositório ou de todos os corpos de testes. Buscas locais foram por perfil, usuário, acesso, sessão, autorização, papéis, retenção, exclusão e integração em `docs/`, `prompts/` e backend. Ausência significa "não localizada no recorte pesquisado", nunca prova universal de inexistência.

As seções de análises antigas que descrevem o estado antigo são evidência histórica, não prova da branch atual. Resultados de comandos abaixo são observações desta sessão, ancoradas nas configurações lidas. O novo cenário não existe nesta entrega: não pode ser declarado executado. Nenhuma migration foi aplicada nesta análise; nenhum ambiente ou backend foi corrigido.

## Problema enriquecido

### Resultado desejado

Especificar um teste executável que prove a colaboração real entre HTTP ASGI, middleware, casos de uso de perfil/acesso, scrypt, emissão/validação de sessão, repositórios SQLAlchemy e SQLite migrado, seguindo a mesma conta desde cadastro até exclusão. A especificação deve permitir execução futura sem inventar aceites de produto.

### Atores e interesses

Estudante proprietário: manter e retirar o próprio perfil de uso. Equipe de testes: demonstrar persistência e autorização com controles positivos. Backend: receber achados sem correções embutidas. Responsável pelo card/produto: confirmar critérios que o título não fornece.

### Evidências e fatos observados — (a) fatos encontrados

Os trechos entre aspas ou em código nesta seção são recortes dos caminhos indicados. "Definido" indica documento; "implementado" indica comportamento do código; a seleção de um comportamento para este novo cenário permanece critério **inferido**, pois o card não tem aceite fornecido.

#### F01 — Histórico local e identificação dos trabalhos

| Trabalho localizado | Evidência local e caminho | Identificação e limite |
|---|---|---|
| Caso de uso de cadastro | `484e148`: "add student registration use case"; cria `src/backend/application/cadastro_estudante.py` e seu teste | Merge `9c87dba`, mensagem "Merge pull request #47", segundo pai `484e148`. PR identificado pelos pais e arquivos, sem atribuir número de card. |
| Persistência assíncrona de usuário | `8a33757`: "add asynchronous user persistence"; aparece no histórico de `src/backend/application/cadastro_estudante.py` e do repositório | Evidência de evolução da persistência, não de autenticação pronta em produção. |
| Login e API de cadastro/acesso | `dfaedf0`: "add student access use case", altera `application/acesso_estudante.py`; `61d025b`: "add secure credential verification"; `33fdc5a`: "add student registration and access endpoints", cria `api/cadastro_acesso.py` | Intervalo `227ebd5^1..227ebd5^2` contém esses commits e `cbc9014`; merge `227ebd5` diz PR #52. "task-27" no nome da branch não é PR #27. |
| Edição e exclusão de domínio/Application | `2c955c4`: "implementar edição e exclusão de perfil"; arquivos `application/perfil_estudante.py`, entidade então em `domain/entities.py`, testes e análise | Segundo pai do merge `88f08a4`, PR #56. |
| API inicial de edição/exclusão | `599f2c1`: "editar ou excluir perfil de estudante via api"; histórico de `api/perfil_estudante.py` | Segundo pai do merge `9e5a9da`, PR #69. Diferenciar de `6ab1bb5`, PR #68 (`17a7445`), cujo stat mostra somente frontend, apesar da mensagem semelhante. |
| Emissão de sessão no login | `13979d8`: "emite token de sessão no login"; altera handler, emissor, repositório e migration de sessões | Merge `d98e3a7`, PR #461, segundo pai `69afd44` (ajuste de imports). Não atribuir card ao número do PR. |
| Middleware e autenticador persistido | `4b2f89a`: "protege rotas com sessão persistida"; cria middleware/autenticador | Segundo pai do merge `b39ea23`, PR #464. |
| Consulta segura de dados pessoais | `91157e9`: "consulta segura de dados pessoais"; altera `api/perfil_estudante.py`, Application, mapping e teste SQLite | Intervalo dos pais de `8d18c5b` contém `91157e9`, merge intermediário e imports; mensagem identifica PR #473. |
| Atualização integral | `9e00e47`: "expor atualizacao completa do perfil"; aparece no histórico de router/repositório | Evidência pelo caminho, sem PR adicional afirmado sem verificação dos pais. |
| Exclusão autenticada atual | `171fabb`: "expor exclusão do perfil do estudante autenticado #90"; corpo cita mudança para `/estudantes/atual` e invalidação por `deleted_at` | Intervalo `2286d03^1..2286d03^2` contém `171fabb` e `411bb7a`; merge identifica PR #477. A referência #90 é corroborada pela solicitação em `prompts/backend/20261015-120000-expor-exclusao-perfil-estudante-v001.md`; não se confunde com PR #90. |
| Testes de autorização e contrato | `25603d8`: "recusa a perfil alheio com middleware ativo", merge PR #506 (`6f3a032`); `eca8708`: "contrato credenciais sessao #391" | Localizados por mensagem e arquivos de teste atuais. Não converter #391 em PR #391. |
| Contrato atualizado | `f30d034`: "align credential session contract with implementation"; merge `11e9389` identifica PR #545 | Sustenta necessidade de ler contrato atual em vez de assumir comportamento de versões antigas. |

A matriz `docs/matriz_rastreabilidade.md`, linha RF02, menciona "#369 – CRUD de perfil". Isso é rastreabilidade documental de card, não ligação comprovada a esta branch ou a um PR. Nenhuma fonte lida forneceu descrição ou aceite oficial do card solicitado.

#### F02 — Requisitos e significado de perfil/autorização

- `docs/requisitos_funcionais.md`: RF02, "consultar, editar e excluir as informações cadastradas"; RF13, "exigir autenticação para acesso às informações pessoais". RF01/RF03 centralizam informações do estudante, mas não especificam todos os contratos HTTP.
- `src/backend/domain/usuario.py`: "aggregate root da conta e identidade do usuário"; campos `id, nome, email, hash_senha, deleted_at, dados_contato`. Não há um agregado separado de "perfil autorizado".
- `docs/requisitos-seguranca.md`, RF-AUTZ-02, prevê "papéis de usuário comum e administrador"; a matriz preliminar de permissões "deverá ser validada durante a implementação". Há conceitos documentais de USER/ADMIN, não se pode afirmar que nenhum artefato fala em papéis.
- `docs/Arquitetura/ADR-002-autenticacao-autorizacao-propriedade.md`, §9: "este ADR não considera RBAC como uma funcionalidade já implementada"; contratos atuais "não atribuem um papel ou conjunto de permissões à identidade autenticada".
- `docs/contrato-credenciais-sessao.md`: "A sessão não concede papel ou permissão por si só." Exige conta existente e ativa, sessão conhecida, não revogada e não expirada. `Usuario`, `SessaoRegistro`, porta `AutenticadorSessao`, autenticador e middleware lidos não implementam roles/escopos; busca nesses componentes não encontrou mecanismo RBAC.
- `api/perfil_estudante.py`: consulta exige `principal_id == usuario_id`, edição por ID compara UUID autenticado, edição completa e exclusão usam diretamente principal. Portanto sessão válida de qualquer pessoa não autoriza acessar outro perfil. O mecanismo implementado para este perfil é identidade de sessão **mais propriedade**, sem papel administrativo.
- A expressão exata "perfil autorizado" não recebeu definição própria nos artefatos inspecionados. Interpretá-la como proprietário com sessão válida é recomendação R01, sustentada pelos mecanismos acima, não transcrição de aceite.

Em `docs/requisitos_nao_funcionais.md`, RNF04 exige consulta/alteração por usuários autorizados, mas registra regras a detalhar; RNF08 deixa metas mensuráveis a definir. Esses documentos sustentam a preocupação de segurança e a ausência de SLA, sem fornecer aceite específico da jornada.

#### F03 — Contrato por operação e origem da identidade

Todos os casos abaixo usam `RepositorioUsuario`, concretizado por `RepositorioUsuarioSqlAlchemy`; cadastro usa `existe_por_email/salvar`, consulta `obter_por_id`, edição `obter_por_id/obter_por_email/atualizar`, exclusão `obter_por_id/atualizar`. O adapter executa `flush`; "A composição externa possui sessão, commit e rollback" (`repositorio_usuario.py`). Casos de uso de perfil não recebem token ou papel e não autenticam por si mesmos.

| Operação implementada | Identidade, entrada e saída | Sucesso e falhas implementadas | Documento versus implementação |
|---|---|---|---|
| Cadastro: `POST /estudantes` → `CadastrarEstudante` | Público em `ROTAS_PUBLICAS`. ID gerado por `GeradorUsuarioId`, não vem do corpo. JSON `{nome,email,senha}`; resposta `{id,nome,email}`. | 201; 409 `EmailJaCadastrado`; 422 DTO/VO inválido; 503 cadastro/derivador ausente. | RF-AUT-01 e contrato definem cadastro email/senha, hash e limites de senha. Formato exato de resposta, demais limites e tradução 409 estão no handler `api/cadastro_acesso.py`, não em aceite do card. |
| Sessão: `POST /acessos` → `AcessarEstudante` + `CriadorSessaoSeguro` | Público. JSON `{email,senha}`; busca pelo email e ID retornado da conta validada, então cria sessão. Corpo de resposta vazio; token somente em Set-Cookie. | 204; 401 email inexistente/inválido estruturalmente, senha incorreta ou conta excluída; 422 limites/campos do DTO; 503 acesso/criador ausente. | Definido em `docs/contrato-credenciais-sessao.md`, implementado em `api/cadastro_acesso.py`, `application/acesso_estudante.py` e `security/tokens_sessao.py`. |
| Consulta: `GET /estudantes/{usuario_id}` → `ConsultarPerfilEstudante` | UUID no caminho serve para comparar; entrada do caso usa `UsuarioId(principal_id)`. Sem corpo. Resposta exata: `{nome,email,telefones,cidade,linkedin,curriculo_lattes}`. Não inclui id, endereço, hash, senha, token ou estado interno. | 200; 401 sem principal/sessão inválida; 404 alvo alheio, ausente ou excluído no caso; 422 UUID malformado com sessão válida; 503 caso ausente após validar propriedade. | RF02/RF13 e ADR definem acesso próprio; projeção e statuses específicos estão em `api/perfil_estudante.py`. Análises históricas de consulta têm decisões próprias; contrato geral 403 tem divergência F09. |
| Edição identitária: `PUT /estudantes/{usuario_id}` → `EditarPerfil` | UUID no caminho comparado ao principal; JSON `{nome,email}`; resposta `{id,nome,email}`. Caso recebe o ID do caminho somente depois da igualdade. Não altera hash/ID. | 200; 401 ausência/sessão inválida; 403 proprietário diferente (middleware e handler); 404 ausente; 409 excluído ou email de outro ID; 422 DTO/VO; 503 caso ausente. | Contrato de sessão define propriedade desta rota; campos, invariantes e falhas específicos estão no código e análise de edição. |
| Edição completa: `PUT /estudantes/me/perfil` → `AtualizarPerfilCompleto` | ID somente de `request.state.usuario_id`; JSON com `nome,email,endereco,cidade,telefones`, links opcionais. Resposta `{id,nome,email,endereco,cidade,telefones,linkedin,curriculo_lattes}`. | 200; 401; 404 ausente; 409 excluído/email de outro dono; 422; 503 executor ausente. | Explicitamente definida em `docs/matriz_testes.md`, CT-RF02-05; código em `api/perfil_estudante.py` e `application/perfil_completo.py`. Links ausentes são limpos. |
| Exclusão: `DELETE /estudantes/atual` → `ExcluirPerfil` | ID somente do principal; não há ID de dono no corpo/caminho. Sem corpo necessário. Remove cookie, retorna corpo vazio. | 204; 401 ausência/sessão inválida; 404 perfil ausente se caso alcançado; 503 executor ausente. Não há tradução para 409 nesta rota. | Análise `20261015-120000-expor-exclusao-perfil-estudante-v001.md` registra decisão de produto de soft delete próprio sem ID; contrato de sessão define invalidação; código confirma. |

Status acima são falhas explicitamente tratadas ou validação do framework, não promessa de catálogo completo de erros. Falhas de banco não têm política/status específico definido nos handlers; exceções não tratadas podem chegar como erro da aplicação, e não devem ganhar um HTTP "esperado" inventado no teste.

Em edição identitária, a verificação de executor ausente ocorre antes da checagem local de principal, mas com middleware ativo a falta de sessão é barrada antes de ambas. Para GET alheio o handler nega antes de testar executor ausente. A ordem importa para não confundir 401/404/503 de composições diferentes.

A rota separada de contato `PUT /estudantes/{usuario_id}/dados-contato` aparece na fábrica e middleware. Não é necessário exercitá-la para preencher o título: o PUT completo já reúne dados pessoais. Não se importam suas regras nem regras de itens profissionais para este ciclo.

#### F04 — Validação e credenciais

- `api/cadastro_acesso.py`: `nome` 1–200, `email` 3–320, `senha` 8–1024 caracteres. Mesmos limites de email/senha no login. O código não exige combinação de letras, números ou símbolos.
- `domain/value_objects.py`: `Email` usa `strip().lower()` e regex `[^@\s]+@[^@\s]+\.[^@\s]+`; `Nome` remove espaços externos e rejeita vazio. Não prova entrega/verificação de email.
- `CadastrarEstudante` recusa email existente antes de gerar ID; `EditarPerfil` e `AtualizarPerfilCompleto` permitem manter email do mesmo ID e recusam o de outro. Mapping/migration têm `uq_usuarios_email`. Corrida de unicidade e tradução de erro SQL não estão definidas pelo handler.
- `AtualizarPerfilCompletoRequisicao`: endereço 1–500, cidade 1–120, lista de 1–5 telefones, links opcionais até 300; `DadosContato` exige telefone e normaliza links vazios para None, sem validar URL; `Telefone` rejeita vazio sem impor máscara/país. Não inferir regras de formação/projeto.
- `security/senhas.py`: `_CUSTO = 2**14`, bloco 8, paralelismo 1, salt 16 bytes, comparação `hmac.compare_digest`. É custo real deliberado de derivação, não sleep artificial ou hash rápido de teste. O contrato diz saída 64 bytes; a chamada de código usa o padrão de `hashlib.scrypt` sem explicitar `dklen`. Não há SLA de duração. Os seeds de `BancoCredenciaisSessao.preparar` usam scrypt real.
- `tokens_sessao.py`: 32 bytes aleatórios → Base64 URL-safe sem padding, persiste só SHA-256; validade de 8 horas. `repositorio_sessao.py` faz JOIN com usuário ativo a cada validação.
- `docs/contrato-credenciais-sessao.md`: cookie `__Host-sessao`, `Path=/; Max-Age=28800; Secure; HttpOnly; SameSite=Lax`, sem Domain, sem renovação por atividade. `solicitar_asgi` existente usa `scheme="https"`.

#### F05 — Encadeamento real

`CadastrarEstudante.executar` cria `Usuario` e chama salvar; o handler retorna DTO e não chama criador de sessão nem emite cookie. `POST /acessos` separado valida email/senha, cria sessão e emite cookie. Portanto o cenário precisa cadastrar → fazer login → usar cookie; cadastro não autentica automaticamente. Sem commit externo o flush não comprova durabilidade em outra sessão.

#### F06 — Efeito da exclusão, camada a camada

| Aspecto | Definido ou implementado, com trecho/fonte | Consequência verificável |
|---|---|---|
| Estado da conta | `Usuario.excluir`: `replace(self, deleted_at=excluido_em)`; `ExcluirPerfil` atualiza somente na primeira transição | Linha e dados permanecem; `deleted_at` passa a não nulo. Não há DELETE SQL de usuário neste fluxo. |
| Sessões existentes | Contrato: "Exclusão lógica da conta invalida todas as sessões"; repositório: `UsuarioRegistro.deleted_at.is_(None)` | Todos os tokens da conta deixam de autenticar; não depende de gravar `revogada_em`. As linhas de sessão permanecem no fluxo lido. |
| Cookie atual | Handler `resposta.delete_cookie(...secure=True, httponly=True, samesite="lax")` | Set-Cookie de expiração; não confundir remoção do cliente com invalidação de todos os tokens no servidor. |
| GET seguinte | Middleware recusa sessão vinculada a conta excluída com 401; caso de consulta, se chamado diretamente com excluído, lança `PerfilNaoEncontrado` → 404 no handler | Fluxo integrado com token antigo deve verificar 401. 404 do caso não é o status desse fluxo. |
| PUT seguinte, nas duas variantes | Middleware recusa antes do caso com 401; casos isolados lançam `PerfilExcluido`, traduzido em 409 | Mesmo cuidado de precedência. |
| Login seguinte | `AcessarEstudante`: `usuario is None or usuario.excluido or not ...confere(...)` → `CredenciaisInvalidas` | 401 uniforme sem novo cookie/sessão; usar email atual depois da edição. |
| Repetição do DELETE | `ExcluirPerfil`: `if usuario.excluido: return usuario`; domínio preserva primeira data. Middleware invalida token anterior | Idempotência do caso já tem unitário; repetição HTTP com token antigo é 401, não 204. Sem cookie também 401. |
| Reutilizar email atual da conta excluída | `existe_por_email` não filtra `deleted_at`; constraint única sobre email; cadastro recusa existência | Comportamento atual: 409. Política de produto não definida; caracterização possível, sem afirmar reserva eterna. O email antigo liberado por edição é questão diferente. |
| Dados relacionados | `ExcluirPerfil` acessa somente repositório de usuário; update copia colunas do agregado, não percorre outros recursos. DER mostra relações | Esse fluxo não implementa cascata/purga de itens, currículos, documentos, backups. Política para eles permanece L04; não derivar regras a partir de outro DELETE. |

#### F07 — Composição realmente exportada

`main.py` chama:
```python
app = create_app(
    autenticador_sessao=AutenticadorSessaoIndisponivel(),
    verificador_persistencia=_verificador_persistencia,
    lifespan=_ciclo_vida_aplicacao,
)
```

`AutenticadorSessaoIndisponivel.autenticar` retorna sempre `None`. `factory.py` instala `MiddlewareAutenticacaoSessao` quando o parâmetro não é None, e registra routers mesmo com executores opcionais ausentes. Os defaults de cadastrar/acessar/editar/excluir/consultar/atualizar completo/criador de sessão são None.

Assim, a composição de produção atual **instala autenticação fechada**, não autenticação persistida operacional. Não injeta casos de cadastro, login, consulta, edição ou exclusão. Com entrada válida, cadastro e login públicos recebem 503; rotas privadas do perfil recebem 401, inclusive com cookie. A engine de `main.py`, quando há DATABASE_URL, atende à readiness, não compõe repositórios e casos do perfil. Ativar autenticação aqui não é tarefa do cenário.

`test_integracao_composicao_credenciais_sessao.py`, C01, já caracteriza fallback original; C02 é explicitamente ignorado por produto. A execução observada de C01 passou. O fluxo novo em `create_app(...)` no harness prova os componentes injetados, não `backend.main:app`, nem a política produtiva de transações.

#### F08 — Cobertura encontrada e sobreposição a evitar

| Fonte | Nível/mecanismo lido | Cobertura que pode ser afirmada e limite |
|---|---|---|
| `test_domain_perfil_estudante.py` | Unitário puro | Edição preserva ID/hash/original; excluído não edita; exclusão preserva primeiro instante. |
| `test_application_perfil_estudante.py`, classes de perfil | Unitário com repositório spy e relógio stub | Edição válida, email próprio/conflito, ausente/excluído; exclusão inicial/repetida/ausente; consulta ativa/ausente/excluída. Não prova SQL ou HTTP. |
| `test_application_cadastro_estudante.py` | Testes unitários localizados por nomes | Declara sucesso e duplicidade sem gerar/salvar. Corpos não foram auditados nesta análise; não declarar cobertura integrada com base no nome. |
| `test_application_acesso_estudante.py` | Unitário com repositório/verificador stubs | Sucesso; conta ausente; senha incompatível; conta excluída não chega ao verificador. Não testa SQL/scrypt juntos. |
| `test_application_perfil_completo.py` | Caso real com repositório em memória | Atualização de todos os campos em uma persistência; conflito de email, ausente e excluído sem gravação. Não prova transação SQL. |
| `test_infrastructure_senhas.py` | Unitário de adapter com scrypt real | Senha original aceita, incorreta recusada e hash malformado seguro. Não usa banco ou HTTP. |
| `test_api_acesso_estudante.py` | Handler chamado diretamente, executor/emissor stubs | Emissão/transporte de cookie isolados; não prova cadastro/login no banco. |
| `test_api_perfil_estudante.py` | Doubles; exclusão chama endpoint diretamente | Exclusão pelo principal, cookie removido, 503/404/401 e rota sem UUID. Nomes de testes também declaram consulta/projeção, erros de edição e PUT completo; inventário desses nomes não prova persistência. |
| `test_infrastructure_repositorio_usuario.py` | Mapper/AsyncSession doubles; nomes e assertions transacionais inspecionados | Consultar/atualizar/flush e ausência de commit local; não substitui banco real. |
| `test_integracao_recusa_perfil_alheio.py` | API ASGI + casos reais, autenticação determinística e repositório em memória | GET próprio 200/alheio 404, PUT próprio 200/alheio 403, sem/inválido 401, spies e preservação de B. É integração entre componentes, mas sem sessão/banco reais. |
| `test_integracao_persistencia_dados_pessoais.py` | SQLite real síncrono, `Base.metadata.create_all` | Roundtrip de contato e perfil legado sem contato em sessão nova. Não testa cadeia migrada, HTTP, cadastro nem exclusão. Seu create_all não deve ser copiado. |
| `test_integracao_persistencia_sessao.py` | SQLite migrado assíncrono, `BancoCredenciaisSessao` | M01–M03/P01–P03 declaram schema/constraints/FK, criação/autenticação, expiração e rollback. Nesta execução todos os seis ficaram ignorados pelo preflight de revisões duplicadas. |
| `test_integracao_contrato_credenciais_sessao.py` | ASGI, repositórios reais, banco migrado, scrypt e tempo controlado | H01–H10 e R01–R03: login/cookie, recusas, consulta/edição própria, identidade e logout. H08 marca `deleted_at` diretamente no banco e testa GET de tokens A1/A2 com controle B. Não passa pelo cadastro HTTP nem pelo DELETE de perfil. Estado de execução depende do grafo; não contar como prova verde só por existir. |
| `test_integracao_composicao_credenciais_sessao.py` | Subprocesso da app exportada | C01 caracteriza composição fechada; C02 ignorado por ausência de composição produtiva. |
| `test_integracao_crud_informacoes_complementares.py` | ASGI + casos reais + adapters em memória | Precedente de "integração" sem DB e testes independentes por operação. Não estabelece regras de perfil ou obrigação de formato de jornada. |

Nenhum teste localizado conecta **cadastro HTTP → login → edição → DELETE real de perfil**, com releitura durável após cada transição. Esse é o ganho incremental proposto. Evitar replicar a matriz inteira de tokens expirados, revogados, métodos alternativos de transporte ou todas as entradas inválidas já cobertas; essas suítes continuam como regressão. O título do novo card não exige reimplementar todos os níveis de teste.

#### F09 — Divergências e fonte mais confiável para cada pergunta

| Divergência | Evidências | Fonte adotada para caracterizar o runtime e por quê |
|---|---|---|
| Cadastro parece autenticar automaticamente no planejamento | Fluxograma de `requisitos-seguranca.md` §2.3: "Conta criada" → "Usuário autenticado"; handler de cadastro não emite sessão, login separado o faz | Código atual e contrato de credenciais são mais específicos/executáveis para encadeamento. Fluxograma continua intenção geral, não aceite HTTP. |
| Papéis previstos versus mecanismo disponível | RF-AUTZ-02/USER/ADMIN versus ADR-002 §9 e ausência no modelo/contratos lidos | ADR aceito e código atual descrevem estágio implementado. Não implementar RBAC nem chamar sessão de papel. |
| "Falha de propriedade = 403" geral versus consulta de perfil | Contrato de sessão generaliza 403; GET em `api/perfil_estudante.py` devolve 404; teste integrado A/B espera 404; ADR admite mascaramento por operação | Handler + teste específico têm maior precisão para GET; registrar divergência documental, sem trocar para 403 silenciosamente. |
| Exclusão idempotente versus segundo DELETE com cookie antigo | Domínio/caso retornam estado excluído sem mudar data; sessão ativa filtra usuário excluído | Ambas fontes são verdadeiras em camadas diferentes. HTTP com middleware real espera 401; não forjar principal para obter 204. |
| DER mais amplo que schema entregue | DER USUARIO inclui tentativas/bloqueio/created_at/updated_at; ORM atual não os declara. DER SESSAO omite token_hash; migration/ORM incluem | Mapping e migrations executáveis para schema atual; DER para intenção de modelo, sem afirmar que há bloqueio de login implementado. |
| Análise antiga descreve falta de Python/aiosqlite | `20261018-131822-validacao-contrato-credenciais-cards-80-82-v001.md`, A03; `nix/tests.nix` atual tem Python + aiosqlite | Configuração atual e sondagem executada prevalecem: dependências presentes. Não copiar diagnóstico histórico para esta branch. |
| Matriz resumida de RF02 defasada | `docs/matriz_rastreabilidade.md` §"Divergência na cobertura resumida de RF02" registra resumo 01–04 versus seção 01–06 em matriz_testes | Seção detalhada atual contém CT-RF02-05/06. Não converter CT de competência/experiência em política de exclusão de conta. |
| Segurança planejada mais ampla que implementação | Requisitos preveem verificação de email, recuperação, rate limit; contrato atual explicita ausência de rate limit e CSRF/Origin | Não reivindicar esses controles no cenário; abrir achado de segurança separado. |

#### F10 — Ambiente e bloqueios observados

`nix/tests.nix`: `pkgs.python3.withPackages (ps: backendPythonPackages ps ++ [ ps.aiosqlite ])`. `backend-python-packages.nix` lista FastAPI, Uvicorn, SQLAlchemy, Alembic, Psycopg e pydantic-settings. `backend.nix` usa a mesma lista base. O driver SQLite assíncrono é acréscimo de tests; não está na lista base lida. Não há provisão de servidor PostgreSQL em tests.nix. Psycopg presente não é prova de um banco PostgreSQL preparado.

Sondagem real no Nix tests:
```text
Python 3.14.7
aiosqlite 0.21.0
```
Comando: `nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -c 'import sys, aiosqlite; print(sys.version); print(aiosqlite.__version__)'`, exit 0.

`alembic.ini` aponta para `src/backend/infrastructure/persistence/alembic`; `env.py` exige DATABASE_URL e usa engine assíncrona/metadata, sem importar main. A migration inicial de usuarios cria id/nome/email/hash; contato é adicionado por `20261014_0007_adicionar_dados_contato_usuario.py`; `20261013_0004_adicionar_dados_consulta_estudante.py` acrescenta deleted_at. A de sessões cria FK e token_hash único, não token claro.

Inspeção das declarações e comando `nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m alembic heads` (exit 0 com warnings) mostraram:
```text
Revision 20261015_0011 is present more than once
Revision 20261015_0012 is present more than once
20261015_0011
20261015_0012
20261017_0004 (head)
20261017_0015 (head)
```
Duplicatas: cursos/exclusão lógica de formações compartilham 0011; links/projetos compartilham 0012, nos caminhos do inventário. Associação e ordem de seções terminam em ramos distintos. Saída com exit 0 não valida o grafo: `upgrade head` requer head inequívoca. Não foi aplicada migration nem feita linearização aqui.

`fixtures/credenciais_sessao.py` tem preflight AST que reconhece Assign e AnnAssign de revision e emite SkipTest com os pares conflitantes; depois exige uma única head e executa `upgrade head`. Isso explica os seis skips observados, sem atribuí-los à ausência de aiosqlite.

### Hipóteses

H1: um harness novo pode reutilizar transporte, inspeção e isolamento existentes e compor os casos faltantes sem alterar produto. H2: com grafo temporário inequívoco o SQLite aceita as migrations necessárias; não foi provado por execução nesta análise. H3: proprietário com sessão válida corresponde à intenção do título; a seleção precisa de confirmação no aceite, mas tem apoio técnico suficiente para proposta.

### Perguntas em aberto — (b) lacunas

Cada lacuna é ausência de definição localizada, não afirmação de comportamento desejado. A coluna "falta fornecer" é a informação exata necessária para encerrá-la.

| ID | Lacuna | Opções viáveis | Recomendação e justificativa | Natureza / falta fornecer |
|---|---|---|---|---|
| L01 | Não há descrição/aceite do card; #369 aparece só na matriz | Obter texto oficial; ou implementar proposta técnica como critérios inferidos | Propor a caracterização integrada do título, sem declarar aceite oficial. A matriz não identifica inequivocamente esta tarefa | **Produto**: descrição/aceites, identificador inequívoco do card e eventual vínculo com commits/PRs. |
| L02 | "Perfil autorizado" não é termo definido | Dono com sessão válida; algum futuro papel/permissão; conta aprovada/verificada | Dono ativo com sessão válida e propriedade, pois é o mecanismo implementado e aceito no ADR. Não adicionar papel, aprovação de conta ou verificação de email | **Produto** para significado oficial; **técnica** para caracterizar implementação atual. Fornecer ator, regra de elegibilidade e recursos autorizados caso a intenção seja diferente. |
| L03 | Título não escolhe qual edição de perfil nem campos exigidos | PUT identitário; PUT completo; ambos no fluxo | Cobrir ambos em duas subetapas da edição, porque coexistem no router e o completo é explicitamente previsto em CT-RF02-05. Não incluir itens profissionais | **Técnica** para proposta de cobertura; produto confirma abrangência oficial. Fornecer rota/campos de aceite se desejar recorte menor. |
| L04 | Política de retenção/purga e destino dos relacionados não está detalhada | Retenção temporária e purga; anonimização; preservação por obrigação | Deixar política fora do oráculo. Verificar somente soft delete implementado; não inventar prazo nem cascata | **Produto/governança**: prazos/finalidades por usuários, itens, sessões, arquivos, backups, logs/caches; responsáveis e procedimento de descarte. Prazo de logs não é prazo da conta. |
| L05 | Reutilização do email de conta excluída não tem decisão de produto | Reservar; liberar por purga/anonimização; liberar imediatamente | Caracterizar 409 atual com controle de email novo, sem transformar isso em política permanente; nova política exige outro trabalho | **Produto**: momento e condições de reutilização, vínculo de identidade e dados antigos. |
| L06 | Não há convenção única exigindo fluxo encadeado versus testes por operação | Um fluxo; casos independentes; fluxo central mais matriz lateral | Um método de teste encadeado com checkpoints fail-fast; existentes mostram formatos distintos. O título enumera uma jornada e o valor novo é a continuidade da mesma conta | **Técnica**. Aprovar essa estrutura na invocação futura; fornecer convenção oficial se existir fora do recorte local. |
| L07 | Composição produtiva não permite executar jornada autenticada; transação HTTP não definida | Aguardar wiring de produção; compor no harness; corrigir produção | Compor no harness e declarar limite, pois corrigir produto foi excluído | **Técnica** para teste; handoff backend para runtime. Para certificar produção faltam wiring real, sessão por request e política de commit/rollback e falhas. |
| L08 | Grafo Alembic inválido impede banco migrado original | Ignorar com motivo; executar sob linearização temporária autorizada; esperar correção permanente | Registrar ambos os estados: original bloqueado/ignorado; experimento temporário para prova de componentes com schema migrado. Jamais contar o segundo como prova do grafo original | **Técnica**, autorização temporária já dada pelo usuário. Falta execução futura com diff completo; correção permanente é handoff. |
| L09 | Não há exigência nem alvo PostgreSQL descartável fornecido para esta jornada | SQLite migrado local; repetição em PostgreSQL isolado | SQLite obrigatório; não criar variante PostgreSQL sem necessidade. Não certificar equivalência de dialetos | **Técnica**. Para incluir PostgreSQL: fornecer harness/banco efêmero, URL exclusivamente de teste, isolamento/limpeza e autorização de alvo. |
| L10 | Não há exigência de documento de evidência para este card | Resumo no PR; documento de validação; ambos | Mínimo: esta análise + código futuro + texto do PR com resultados/diffs. Precedente de contrato de sessão propõe documento específico para vários cards, mas não impõe isso a toda integração | **Técnica/processo**. Se houver obrigação externa, fornecer template/destino e responsável; a skill de testes exclui relatórios gerados sem convenção explícita. |
| L11 | Falhas SQL, concorrência e atomicidade do HTTP não têm oráculos específicos deste perfil | Definir política antes de testar falhas; caracterizar sucessos apenas | Não incluir injeção de falhas ou inventar status, pois o escopo é ciclo autorizado e o adapter só flush | **Backend/produto** para política; fornecer status, limites de transação, tratamento de unicidade concorrente e garantias de recuperação. |
| L12 | Elegibilidade de mudanças temporárias de migrations/Nix é exceção à fronteira normal da skill de testes | Executor direto para exceção; mesma skill com autorização explícita e descarte | Mesma skill pode realizar a fatia de testes e o experimento estritamente temporário autorizado nesta solicitação; nenhuma correção produtiva versionada. Se seu gate considerar mudança inseparável/proibida, executar apenas a fatia elegível e devolver experimento a executor direto | **Processo/técnica**: a aprovação da análise não autoriza correções permanentes. Reafirmar a exceção na invocação futura e reportar veredito do gate antes de escrever. |
| L13 | Limite de duração não definido para teste com scrypt | Custo real; hash substituto; benchmark separado | Manter custo real e medir duração informativamente; nenhum limite numérico de performance | **Técnica**; produto só precisa fornecer SLA/condições se quiser aceite de performance. |

### Escopo

Definição revisável do cenário integrado de API com componentes reais, dados sintéticos, banco local migrado, persistência durável, controles de autorização e comportamento pós-exclusão implementado. Somente este Markdown é produzido agora.

### Fora do escopo

Código de testes nesta entrega; correções de backend, rotas, migrations permanentes, ambiente permanente, main/factory, contratos, autenticação de produção, frontend, novas regras de segurança/negócio, RBAC, recuperação de senha, purga, falhas de banco e publicação externa.

### Critérios de sucesso

Todos os critérios de **seleção do cenário** são **inferidos do título e das fontes F02–F10**, não aceites oficiais. A evidência específica define o comportamento do sistema, mas não prova que o card o exigiu.

C1: mesma identidade criada por HTTP é consultada, editada e excluída por sessão emitida pelo login. C2: cada transição é confirmada após commit em outra AsyncSession. C3: recusas têm controles positivos reais, não rotas sempre fechadas. C4: saída pública respeita DTOs e não expõe segredos. C5: exclusão lógica bloqueia tokens e novo login conforme contrato, sem promessa de eliminação física. C6: execução aprovada distingue-se de skip e declara composição/dialeto/grafo usados. C7: testes e infraestrutura permanente permanecem fora desta entrega e o executor futuro preserva todas as restrições.

## Restrições aplicáveis

- `AGENTS.md` raiz e `src/backend/AGENTS.md` lidos antes das atividades correspondentes; busca de AGENTS/override não encontrou instrução adicional em docs/prompts/testes. Clean Architecture, DDD e documentação de funções/classes também se aplicam ao futuro harness.
- Desenvolvimento via Nix; testes integrados em tests, regressão informativa no comando backend solicitado, lint em quality. Git fora do Nix.
- Skill atual permite escrever exatamente um Markdown novo, sem implementação. Não executar os patches temporários nesta análise.
- Nenhum uso de `create_all`, schema SQL manual ou backend falso para substituir fronteiras reais exigidas. Serviços externos e banco compartilhado não são alvos.
- Teste ignorado não é prova; veredito de aceite oficial permanece não verificável sem L01.

## Classificação comentada

`engineering`, decisão `design`, escopo `component`, ciclo `design`, preocupações `integration/security/privacy`. Risco médio da decisão de teste: reversível, mas pode criar falsa evidência de proteção/eliminação. As lacunas de política de privacidade têm impacto maior e ficam explicitamente sem decisão nesta fatia.

## Decisão de roteamento

Inventário real das subpastas imediatas de prompts: `backend, ambientes, frontend, templates, revisao, requisitos`. Selecionada `prompts/backend`: objeto é a integração HTTP/Application/persistência do perfil; análises de exclusão, contrato de sessão e CRUD integrado já estão ali. `ambientes` é candidata secundária para suporte Nix, que não é resultado desta demanda; `requisitos` seria apropriada à decisão de política pendente, não ao teste. `revisao` não ganha preferência por haver inspeção de código. Confiança alta. Nenhuma pasta nova ou alteração de análise histórica.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | Alta | Priorizar continuidade real + releitura | Evita confundir flush, mocks ou status isolado com ciclo integrado persistido |
| security | Alta | Satisfazer identidade/propriedade e bloqueio real | Recusa só vale com controle que demonstra rota funcional |
| privacy | Alta | Satisfazer projeção e limites explícitos | Soft delete não certifica eliminação de dados |
| simplicity | Média | Conter massa/harness e evitar matrizes repetidas | Custo scrypt e manutenção de fixtures |
| operability | Alta | Comando reprodutível, skip explícito e cleanup | Ambiente/grafo atuais possuem limites observados |

## Alternativas consideradas

**A — manter somente testes existentes.** Executável como baseline, porém sem continuidade de cadastro a DELETE de perfil e sem prova do novo cenário. Não satisfaz o objetivo incremental.

**B — fluxo encadeado ASGI com banco migrado, componentes reais e composição própria (recomendada).** Um método percorre cadastro/login/consulta/duas edições/exclusão; assertions intermediárias e controles B; reaproveita utilitários existentes sem afirmar que a fixture já compõe cadastro/exclusão.

**C — testes integrados independentes por operação com banco migrado.** Viável e diagnósticos mais localizados, mas cada teste semeia o estado anterior e não demonstra que os resultados de uma etapa alimentam a seguinte. Pode complementar no futuro, não é a melhor resposta ao título.

**D — fluxo pela main.app atual.** Inviável como prova positiva sem mudança de produto: F07 mostra 503/401. Caracterização já existe em C01, não repetir nem corrigir wiring.

## Perfil de pagamento comparativo

Escala ordinal relativa ao ganho desta demanda: +2 forte, +1 moderado, 0 neutro/desconhecido, -1 piora, -2 piora forte. Sem somar valores.

| Dimensão | Prioridade | A: existentes | B: encadeado real | C: independentes reais | Confiança | Base |
|---|---|---|---|---|---|---|
| correctness | Alta | -2 | +2 | +1 | Alta | F08, lacuna de continuidade |
| security | Alta | 0 | +2 | +1 | Alta | F06/F08, tokens emitidos e invalidação após DELETE |
| privacy | Alta | 0 | +1 | +1 | Média | DTOs e soft delete, sem política de purga |
| simplicity | Média | +2 | -1 | -1 | Média | Harness novo, migrações e custo scrypt |
| operability | Alta | +1 | +1 | +1 | Média | Mesmo bloqueio Alembic; B exige execução completa e C mais bancos preparados |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado nesta linhagem. Decisões de produto históricas de exclusão são fontes F06, não aprovação automática desta proposta.

### Decisão recomendada nesta versão — (c) recomendações

**R01:** adotar B e chamar o cenário de `test_cadastro_consulta_edicao_exclusao_do_proprio_perfil_com_sessao_valida`. "Autorizado" será proprietário com conta ativa e sessão persistida válida; cadastro permanece público. Confiança alta para caracterização, aceite oficial pendente de L01/L02.

**R02:** um único fluxo fail-fast; não usar subTest que permita seguir usando token/ID inválido depois de falhar etapa fundamental. Podem existir subTest apenas para mensagens diagnósticas de negativas independentes, sem mascarar falha do pré-requisito.

**R03:** testar ambos os PUTs como subetapas da edição: o identitário confirma caminho+principal e preservação de hash; o completo cobre contato e CT-RF02-05. Não repetir matriz inteira de entradas inválidas ou recursos alheios. A escolha é técnica/inferida; produto pode restringir em revisão.

**R04:** usar SQLite em arquivo temporário, por cenário, migrations até a única head do grafo efetivamente usado e releituras em sessões novas. Com grafo original inválido, skip explícito; executar de verdade somente depois do ajuste temporário autorizado, registrando que a cadeia original não foi certificada.

### Estrutura concreta e reaproveitamento

Arquivos futuros, sem os criar nesta análise:

1. `src/backend/tests/test_integracao_ciclo_vida_perfil_autorizado.py`: classe `CicloVidaPerfilAutorizadoIntegracaoTestCase(unittest.IsolatedAsyncioTestCase)`; um método com o nome R01; helpers de asserção sem mostrar segredos.
2. `src/backend/tests/fixtures/ciclo_vida_perfil_autorizado.py`: `BancoCicloVidaPerfilAutorizado`, composição por request, UUID e relógio UTC, observadores delegantes e dados do cenário. Somente suporte de teste.

Reutilizar de `fixtures/credenciais_sessao.py` o preflight `verificar_revisoes_unicas`, `ativar_chaves_estrangeiras`, `BancoCredenciaisSessao` (métodos de execução Alembic, snapshot, inspeção e fechar), `solicitar_asgi`, `RespostaCredenciais` e hash utilitário. Usar composição/subclasse dedicada que **não chame o seed de preparar**: esse método insere A/B diretamente e impediria provar cadastro HTTP. Não mudar o comportamento da fixture compartilhada para acomodar este cenário.

O preparo novo reproduz a sequência pública já lida: preflight → consultar heads → exigir uma head → upgrade head → engine com FK por conexão → async_sessionmaker. Checar `alembic_version` igual à head obtida; não hardcodar a head temporária como contrato de produto.

A fixture `perfis_integracao.py` é híbrida, síncrona e semeia usuários/currículos; não deve criar a conta sob teste. Pode servir de precedente de dados sintéticos, sem reutilizar seed ou alegar que contém login/sessão real.

Em cada operação HTTP, abrir uma nova AsyncSession, montar repositórios reais e compor por `create_app`:
- `CadastrarEstudante(usuarios, GeradorUsuarioIdUUID4)`;
- `AcessarEstudante(usuarios, DerivadorSenhaScrypt())`;
- `ConsultarPerfilEstudante(usuarios)`, `EditarPerfil(usuarios)`, `AtualizarPerfilCompleto(usuarios)`;
- `ExcluirPerfil(usuarios, RelogioUTC)`;
- `CriadorSessaoSeguro(sessoes)` e `AutenticadorSessaoPersistida(sessoes)`.

Gerador UUID4 e relógio UTC são implementações mínimas das portas **no harness**, usando `uuid4()` e `datetime.now(timezone.utc)`; não fabricam regras ou respostas. Não foi localizado adapter pronto para essas duas portas no recorte de infraestrutura lido. É possível usar relógio fixo como precedente da fixture, mas não necessário: preferir UTC real e asserções de monotonicidade do estado, sem dormir nem impor duração. Não modificar main/factory.

Usar observadores que deleguem aos casos reais para contar chamadas em negativas, seguindo `ObservadorPerfil`. Não trocar autenticação, repositórios, hash ou casos por doubles. O request ASGI existente usa HTTPS sintético, sem servidor/rede; testar transporte real de cookie no scope, sem injetar `request.state` nem dependency override. Guardar tokens somente em memória e passá-los no cookie; esse harness não prova comportamento de cookie jar de navegador.

Compor dentro da sessão de escrita e realizar commit **no harness** depois da resposta ASGI, como no precedente; rollback em exceções e fechamento sempre. Relê-se o estado em outra sessão só após commit. Esse arranjo não prova commit produtivo antes da resposta nem atomicidade de entrega de cookie sob falha SQL.

Registrar cleanup com addAsyncCleanup antes de preparar o banco. Descartar engine antes de remover diretório, inclusive quando migration/asserção falha. Banco e estado novos a cada teste; não depender da ordem de unittest. Nenhuma DATABASE_URL herdada: subprocesso Alembic recebe somente URL do arquivo temporário e ambiente filtrado, como precedente.

### Dados e oráculos do fluxo recomendado

Dados sintéticos propostos, não requisitos de produto:
- A: `{"nome":"Pessoa A Integração","email":"perfil.a@example.test","senha":"Senha-Teste-123"}`.
- B (controle independente): `{"nome":"Pessoa B Controle","email":"perfil.b@example.test","senha":"Senha-Teste-123"}`.
- Edição identitária A: `{"nome":"Pessoa A Editada","email":"perfil.a.editado@example.test"}`.
- Edição completa A: mesmo nome/email editados; `endereco="Rua de Teste, 10"`, `cidade="São Paulo"`, `telefones=["+55 11 99999-0001"]`, `linkedin="https://www.linkedin.com/in/perfil-a-teste"`, `curriculo_lattes="http://lattes.cnpq.br/123456789"`.
- Controle de email novo C, somente na caracterização E8: `perfil.c@example.test`, nome "Pessoa C Controle", mesma senha sintética.

Não impor os UUIDs do seed antigo. Capturar id da resposta de cadastro, validar como UUID e usar esse mesmo ID em todas as etapas; confirmar correspondência no banco. Comparações de hash/token devem gerar mensagem booleana redigida, nunca dump de rows/headers.

Origem de todos os critérios do cenário abaixo: **inferido**. A coluna "sustentação" diferencia comportamento definido em documento (D) e implementado em código (I).

| Etapa / objetivo | Pré-condições | Passos | Resultado esperado e checkpoints | Sustentação / origem |
|---|---|---|---|---|
| E0 — banco válido e controles disponíveis | Ambiente tests, grafo único/inequívoco efetivamente usado | Migrar banco vazio até head, inspecionar versão/colunas. Cadastrar B por POST e fazer login B | 201 com DTO público e ID; login 204 com cookie válido; GET B 200; snapshots novos confirmam conta e sessão de B. Se pré-requisito faltar, skip com motivo, nunca sucesso | D: AGENTS/Code First; I: fixture de credenciais. Critério **inferido** |
| E1 — criar a conta sob teste | Banco isolado; email A livre; middleware ativo | POST /estudantes com A, sem cookie; reler banco e sessões em sessão nova | 201 e chaves exatas id/nome/email; conta ativa, hash scrypt verificável e diferente da senha; contato inicialmente nulo, zero sessões de A; sem Set-Cookie. Não fazer login implícito | D: RF-AUT-01 e contrato; I: cadastro/VO/mapping. **Inferido** |
| E2 — obter sessões A1 e A2 | Conta A ativa persistida | Duas vezes POST /acessos com A; guardar cookies opacos separadamente | Cada login 204 vazio e atributos contratuais; duas linhas com hashes distintos SHA-256, mesma identidade e datas de validade; tokens em claro não persistidos. GET com A1 e A2 retorna A, confirmando validade anterior ao DELETE | D: contrato permite múltiplas sessões/8h; I: emissor/repo. **Inferido** |
| E3 — consultar dados e recusar leitura sem sessão | A1 válida; perfil A ativo; controle positivo GET A já funcional | GET A com A1; depois mesma rota sem cookie; snapshots antes/depois | 200 com DTO exato nome/email de A, telefones=[], opcionais null; não expor id/endereço/hash/senha/token. Sem cookie: 401 uniforme; consulta não chamada e snapshot intacto. Repetir GET A com A1 200 como controle da mesma rota | D: RF13/contrato/ADR; I: DTO/handler/middleware. **Inferido** |
| E4a — edição identitária persistida e recusa anônima | A1/A2 válidas | PUT /estudantes/{idA} sem cookie com payload válido; então com A1 | Sem cookie 401, sem chamada/efeito; com A1 200 com id/nome/email editados. Releitura nova confirma nome/email, ID/hash preservados; GET A1 200 reflete edição. Login positivo com email editado 204 prova acesso pelo dado atual (guardar A3 se emitido). Não usar email antigo no teste de login pós-delete | D: contrato de propriedade; I: EditarPerfil/handler/repo. **Inferido** |
| E4b — edição integral persistida | Mesmo A ativo; E4a aprovada | PUT /estudantes/me/perfil sem cookie com payload completo válido; depois com A1; GET A | Sem cookie 401 sem efeitos; com A1 200 e DTO completo; contato/nome/email em nova sessão correspondem aos enviados; ID/hash preservados; GET 200 contém projeção consultável. Endereço pode existir no PUT/DB e deve continuar omitido no GET | D: CT-RF02-05; I: AtualizarPerfilCompleto/DTO/mapper. **Inferido** |
| E5 — excluir pela identidade autenticada | A1/A2 (e A3, se criado) funcionaram antes; B ativa | DELETE /estudantes/atual sem cookie; confirmar intacto; depois com A1 | Sem cookie 401 e exclusão não chamada. Com A1: 204 vazio e Set-Cookie expirando sessão; caso recebeu idA. Nova sessão: A existe com deleted_at não nulo e demais campos preservados; B intacta; sessões de A continuam armazenadas. DELETE bem-sucedido é controle positivo da recusa anterior | D: decisão histórica explícita de exclusão e contrato; I: ExcluirPerfil/handler/repo. **Inferido** |
| E6 — revogar acesso efetivo depois da exclusão | E5 persistida; guardar A1/A2 independentemente da remoção do cookie | Reenviar cada token antigo em GET A, PUT A e PUT completo A; reler após cada negativa. Executar GET B e ambos PUT próprios de B com payload válido como controles positivos, preservando identidade/hash de B | A: 401 "Sessão ausente ou inválida.", nenhum caso de perfil chamado, estado pós-delete intacto. B: 200 e efeitos persistidos onde se aplica. Não esperar 404/409 dos casos que o middleware não alcança. Prova de mais de uma sessão invalidada deriva de tokens que antes funcionaram | D: contrato/invalidação; I: JOIN em repo e middleware. **Inferido** |
| E7 — novo login e repetição do DELETE | A excluída, B ativa | POST /acessos com email **editado atual** de A e senha correta; controle login B. Repetir DELETE com A1 e A2; ao final DELETE B com seu cookie válido | Login A 401 uniforme "E-mail ou senha não conferem.", sem Set-Cookie/nova sessão; B 204 e sessão nova persistida. DELETE A repetido 401, primeira data/campos preservados, nenhuma nova exclusão; DELETE B 204 comprova rota operacional no mesmo app/harness. Comparar estado de A antes de excluir B e depois por filtro de idA | D: contrato de login/conta excluída; I: acesso e middleware. **Inferido** |
| E8 — caracterizar reserva atual do email, sem política nova | A ainda existe excluída; email atual conhecido | POST /estudantes com email editado de A e dados válidos; controle POST C com email novo | A: 409 "Já existe uma conta cadastrada com este e-mail.", nenhum usuário/sessão adicional para esse email; C: 201 com conta persistida. Classificar este checkpoint como **caracterização atual**, sem afirmar que é política de produto definitiva | I: existe_por_email + cadastro + unique; L05 documenta ausência normativa. **Inferido** |

E0–E8 compõem o mesmo método e o mesmo banco. B é controle, não segundo perfil sob exclusão de A. Para PUTs positivos de B usar payload com o próprio email B para não criar conflito; PUT completo deve ter endereço/cidade/telefone sintéticos válidos. Antes/depois de cada recusa comparar snapshot de usuários e sessões sem imprimir segredos; em login positivo B haverá nova sessão esperada, por isso comparar o snapshot da recusa antes de executar o positivo.

E8 é caracterização recomendada porque os artefatos implementam o comportamento. Não aguarda política para registrar o atual; se produto rejeitar cristalizá-lo em teste, retirar por revisão desta análise, sem substituir pelo comportamento oposto. E6/E7 são contrato já definido de invalidação e não dependem de inventar política.

Não incluir de novo a matriz completa de perfil alheio: F08 já mostra 404/403 por operação. Controles de B nesta jornada provam isolamento após exclusão e distinguem negação específica de falha global. Não acrescentar critérios sobre formação, projeto, currículo ou arquivos relacionados.

### Recursos ausentes, skips e honestidade da prova

- Driver ausente: seguir import guard existente que só captura ModuleNotFoundError de `aiosqlite`; usar skipUnless com motivo explícito. Não capturar erros arbitrários de import como skip.
- Duplicatas: reutilizar preflight com SkipTest indicando pares. Para múltiplas heads conhecidas, acrescentar verificação dedicada no novo harness com motivo "grafo Alembic preexistente com múltiplas heads: ..."; não modificar o helper compartilhado para ocultar falhas.
- Python/runner Nix indisponível impede iniciar o comando; relatar **não executado por ambiente**, não fingir que unittest emitiu skip. Não recorrer ao Python global.
- Falha de uma migration depois do preflight, falha HTTP, timeout, integridade ou asserção inesperada devem ser erro/falha, nunca skip genérico.
- Não há teste PostgreSQL obrigatório nesta proposta. Se uma variante for aprovada depois, ela deve ser opt-in, ignorada com motivo quando seu alvo isolado não for fornecido; não conectar automaticamente a DATABASE_URL herdada.
- Resultado do método novo: **executado e aprovado** somente se todos os checkpoints, inclusive controles positivos, rodarem e passarem. Um `OK (skipped=1)` é **ignorado**, não prova parcial da jornada; falha numa etapa significa cenário reprovado, não certificado até aquela etapa.
- Distinguir no resumo: total descoberto; executados/aprovados; falhas; erros; ignorados por ambiente/grafo; ignorados por produto. Precedente C02 é ignorado-produto, não ambiente. Nenhum skip pode constar na coluna aprovado.
- Não prova: main.app operacional; transação de produção/entrega de cookie sob falha SQL; PostgreSQL; rede TLS/navegador; recuperação/verificação de email; RBAC; concorrência; desempenho; retenção, anonimização ou eliminação física em banco/arquivos/backups/logs.

### Alterações temporárias autorizadas para execução futura

Não realizadas nesta análise. A autorização expressa do usuário permite experimento temporário de Nix e linearização Alembic; não converte defeitos preexistentes em escopo de correção.

**Preflight obrigatório, Git fora do Nix:**
```bash
git status --short
git diff -- nix/ flake.nix flake.lock src/backend/infrastructure/persistence/alembic/versions/
git diff --cached -- nix/ flake.nix flake.lock src/backend/infrastructure/persistence/alembic/versions/
```
Se já houver alteração staged, unstaged ou arquivo não rastreado do usuário nesses caminhos, **parar e informar**, sem restaurar/sobrescrever. Repetir checagem antes de restaurar; interromper se aparecer mudança concorrente. O status inicial observado nesta análise estava limpo.

`nix/tests.nix` já tem Python do backend e aiosqlite: **não precisa mudar hoje**. Se o estado futuro não os oferecer, pode ajustar somente temporariamente para a lista backend + aiosqlite observada, sempre sob Nix. Não alterar flake.nix/flake.lock nem adicionar dependência permanente. Registrar diff completo mesmo que a alteração pareça pequena; quando não houver patch, escrever "não necessário; diff vazio".

Plano técnico proposto de linearização temporária, mantendo corpos upgrade/downgrade e mudando apenas identificadores/arestas em **cinco arquivos** sob `src/backend/infrastructure/persistence/alembic/versions/`:

| Arquivo | Alteração temporária proposta | Justificativa |
|---|---|---|
| `20261015_0011_exclusao_logica_formacoes_academicas.py` | revision `20261015_0011` → `20261015_0011b`; down_revision `20261015_0010` → `20261015_0011` | Rodar depois de cursos e distinguir IDs |
| `20261015_0012_criar_links_profissionais.py` | down_revision `20261015_0011` → `20261015_0011b` | Incluir exclusão de formações na cadeia |
| `20261015_0012_criar_projetos_academicos.py` | revision `20261015_0012` → `20261015_0012b`; down_revision `20261015_0011` → `20261015_0012` | Rodar projetos depois de links, sem colisão |
| `20261016_0013_criar_documentos.py` | down_revision `20261015_0012` → `20261015_0012b` | Incluir ambos 0012 antes de documentos |
| `20261017_0004_criar_associacoes_curriculo_vaga.py` | down_revision `20261007_0003` → `20261017_0015` | Incorporar ramo solto depois do tronco, deixando uma head |

Esta ordem é recomendação técnica para o experimento, não correção aprovada do histórico produtivo. Antes de aplicar, reler corpos e dependências dos arquivos, validar inexistência de ciclo, executar heads e exigir **uma** head sem warnings. Se outras mudanças da branch invalidarem o plano, parar e pedir revisão; não editar DDL para obter verde.

Antes da reversão copiar para o resumo **os diffs completos**, não só diffstat:
```bash
git diff -- nix/tests.nix src/backend/infrastructure/persistence/alembic/versions/
```

Restaurar somente alterações próprias com caminhos explícitos (não usar git restore .):
```bash
git restore -- src/backend/infrastructure/persistence/alembic/versions/20261015_0011_exclusao_logica_formacoes_academicas.py src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_links_profissionais.py src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_projetos_academicos.py src/backend/infrastructure/persistence/alembic/versions/20261016_0013_criar_documentos.py src/backend/infrastructure/persistence/alembic/versions/20261017_0004_criar_associacoes_curriculo_vaga.py
```
Se e somente se houve patch próprio de Nix, também `git restore -- nix/tests.nix`. Não realizar staging/commits de patches temporários.

No finally do procedimento, restaurar mesmo após teste vermelho e verificar:
```bash
git status --short
git diff --exit-code -- nix/ flake.nix flake.lock src/backend/infrastructure/persistence/alembic/versions/
git diff --cached --exit-code -- nix/ flake.nix flake.lock src/backend/infrastructure/persistence/alembic/versions/
```
Status final não pode listar arquivos em `nix/`, `flake.nix`, `flake.lock` nem no diretório real de `alembic/versions/` acima. A autorização não cobre descartar trabalho alheio. A execução com grafo alterado prova componentes sob **schema migrado do grafo temporário**; após restore, a cadeia original continua bloqueada. Registrar isso mesmo que todos os testes passem.

### Impacto da revisão

Nenhum identificado — decisão inicial. Sem implementação, mudança de produto ou alteração de análises anteriores.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | Continuidade e durabilidade da mesma conta | F03/F08; H1/H2 ainda dependem de execução |
| security | prioritized | Sessões reais que funcionavam deixam de funcionar após DELETE | F06 e contrato; controles B |
| privacy | prioritized | DTOs exatos e distinção entre retirada de uso e purga | F03/F06/L04 |

Nenhuma dimensão é declarada maximized: não há comparação exaustiva ou prova de ótimo.

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| operability | Execução local reproduzível com motivo explícito para bloqueio | Nix tests, banco efêmero migrado e comandos definidos |
| simplicity | Um teste e um harness dedicado; reutilizar transporte e preflight | Evita fixtures genéricas novas e matriz de sessão repetida |

## Achados de backend — sem correções nesta entrega

| ID | Achado e fonte | Consequência / encaminhamento |
|---|---|---|
| A01 | Composição de `main.py` usa fallback e não injeta casos do perfil/acesso, F07 | Jornada produtiva indisponível; wiring e transações em tarefa backend própria |
| A02 | Revisões duplicadas 0011/0012 e duas heads, F10 | Migração original não certificável; saneamento permanente fora do escopo |
| A03 | Cadastro não emite sessão versus fluxograma de segurança, F05/F09 | Especificar login separado; eventual mudança de UX/contrato exige decisão própria |
| A04 | 403 genérico de contrato versus 404 de GET alheio, F09 | Alinhar documentação específica sem alterar teste para uma generalização incorreta |
| A05 | Retenção e dados relacionados não têm política detalhada, L04 | Soft delete retém dados pessoais/hash e linhas de sessão; não anunciar exclusão física/compliance |
| A06 | Email de conta excluída continua reservado na implementação, F06/L05 | Caracterização 409, política futura de reutilização a decidir |
| A07 | RBAC planejado não implementado, F02; controles de rate limit/CSRF/Origin ausentes declarados no contrato | Não alegar cobertura de papéis ou proteção de abuso; tarefas de segurança separadas |
| A08 | Commit/rollback externo e falhas SQL sem contrato HTTP específico, F03/L11 | Verde sob harness não garante atomicidade produtiva; nenhuma correção no adapter |
| A09 | DER diverge de mapping de usuário/sessão, F09 | Revisar modelo documental em atividade própria |
| A10 | Cookie Secure versus guia local de Uvicorn HTTP, contrato/configuração | Harness HTTPS sintético não prova envio de cookie em navegador no setup HTTP; não remover Secure |
| A11 | Idempotência interna não significa repetição HTTP 204, F06 | Documentar camadas; não bypassar middleware para cumprir expectativa inventada |
| A12 | Descoberta ampla do job "unitários" inclui arquivos integrados em `tests/`, CI lido | Comando backend é regressão informativa solicitada; não reclassificar tudo como unitário nem ampliar CI nesta tarefa |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | Verde de testes isolados não detecta falha no encadeamento real | Alta | Equipe e estudante |
| security | 401 constante pode parecer autorização correta | Alta | Estudante e revisão |
| privacy | Confundir soft delete com eliminação cria promessa sem evidência | Alta | Produto e titulares dos dados |
| operability | Skips ou grafo temporário apresentados como prova original | Alta | CI e aceite |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | Um fluxo pode falhar cedo e não exercitar etapas posteriores | Diagnóstico por operação | Aceito com checkpoints claros e unitários existentes |
| security | B e duas sessões A aumentam requests/scrypt | simplicity/performance | Aceito sem benchmark ou timeout de negócio inventado |
| operability | Experimento temporário e restauração documentada | delivery-speed | Aceito sem certificar cadeia original |
| privacy | Aceite de retenção permanece aberto | time-to-value | Necessário para não inventar política |

## Riscos e efeitos de segunda ordem

Caracterização de 409/401 pode ser confundida com política imutável; marcar origem e revisar quando contrato mudar. Compartilhar fixture inadequada pode pré-criar a conta e invalidar a prova de cadastro; não chamar o seed existente. ORM identity map pode esconder falta de commit; reler em sessão nova. Remoção do cookie pode esconder token ainda válido no servidor; reenviar A1/A2 guardados. Positivo de GET não comprova PUT/DELETE; controles são específicos por operação. Não logar senha/token/hash/headers, inclusive em falha de assertion ou diffs de snapshot. Patch de migrations pode esconder defeito permanente; publicar diff completo e restituir grafo original.

## Validação da decisão

### Baseline real desta análise

Estado inicial: `git status --short` vazio no HEAD informado. Nix no sandbox inicialmente falhou antes dos comandos com `opening lock file "/nix/var/nix/db/big-lock": Read-only file system`. Os comandos foram repetidos com a escalada prevista pelo ambiente; nenhuma dependência/arquivo do projeto foi alterado.

1. Comando informativo solicitado:
```bash
nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src
```
Resultado real: **942 testes, 13.000 s, 0 falhas, 0 erros, 33 ignorados, exit 0**. Houve warnings de depreciação Starlette e de tarefas asyncio; não foram erros. Não reutilizar baseline de 781 mencionado em análise antiga.

2. Precedentes executados no ambiente correto:
```bash
nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest -v backend.tests.test_integracao_persistencia_sessao backend.tests.test_integracao_composicao_credenciais_sessao
```
Resultado real: **8 descobertos, 1 executado/aprovado (C01), 7 ignorados, 0 falhas/erros, 1.322 s, exit 0**. Seis skips por duplicatas Alembic, com pares expressos em F10; um skip C02: "produção não compõe login, criador, revogador nem autenticador persistido". Nenhum dos seis é prova de persistência.

3. Gate `nix develop .#quality --command ruff check src/backend` executado após o baseline e repetido após a execução integrada: ambos **All checks passed!**, exit 0. Nenhuma correção I001 necessária. A consulta heads e sondagem de dependências não rodaram testes nem alteraram código.

4. Cenário novo E0–E8: **não implementado e não executado**, por escopo explícito. Linearização temporária e alterações Nix: **não realizadas; diff vazio**. Esta análise não entrega aceite verde da jornada.

5. Validação final do artefato pelo Python de `nix develop .#tests`: 86 fontes registradas existem, sem caminhos duplicados ou placeholders e com cercas Markdown equilibradas; exit 0. Gate Ruff final repetido: **All checks passed!**, exit 0. Essa verificação estrutural do documento não executa nem aprova o cenário proposto.

### Comandos e critérios para o executor futuro

Depois de implementar os dois arquivos de teste, com Nix tests e banco descartável:
```bash
nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest -v backend.tests.test_integracao_ciclo_vida_perfil_autorizado
nix develop .#quality --command ruff check src/backend
```
Executar primeiro no estado original para registrar skips/bloqueios. Se autorizado e preflight limpo, aplicar o plano temporário, executar o **mesmo comando** e exigir método executado, todos os checkpoints aprovados e zero skip no cenário. Rodar lint ao final de cada execução, inclusive quando o teste falha/é ignorado.

Executar a regressão informativa completa no comando exato de baseline acima e comparar com 0 falhas/0 erros. Descoberta deve incluir novo teste; contagem/skips podem mudar por arquivos novos ou grafo temporário, e a diferença deve ser explicada por nomes/motivos. Não aceitar novos erros como "baseline". Não omitir testes antigos para obter verde. Não repetir/broaden testes sem mudança ou falha que justifique.

Se Ruff apontar I001 em arquivos criados/alterados do teste:
```bash
nix develop .#quality --command ruff check --select I --fix <arquivos-apontados>
nix develop .#quality --command ruff check src/backend
```
Outros defeitos preexistentes fora da fatia devem ser relatados; não expandir correção de produto. A análise atual, limitada a Markdown, não executou autofix.

Capturar resultados e diffs temporários, restaurar em finally, confirmar status limpo nas áreas protegidas. Depois da restauração, lint completo final; uma repetição do cenário original pode voltar a skip e deve ser registrada como tal, sem invalidar nem exagerar a prova limitada feita no experimento.

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| H1: harness viável sem mudar produto | Teste E0–E8 executado com casos/repos reais | Comando tests e checkpoints em sessões novas | Necessidade de hook/alteração de produção |
| H2: schema migrável no experimento | Head única sem warnings; upgrade head real; alembic_version confere | Preflight + Alembic pelo mesmo Python | DDL incompatível ou novas duplicatas; não usar create_all |
| H3: intenção do título | Aceite do responsável | L01/L02, proposta de critérios inferidos explícita | Papel, aprovação ou rota pretendida diferente |
| Sem regressão nova | Baseline/resultado por nome e contagem | Suite backend e Ruff após execuções | Erro novo ou teste omitido |
| Cleanup | Diff completo antes e status final sem áreas protegidas | Git fora Nix, restore de alterações próprias | Mudança alheia/concorrente ou resíduo |

## Handoffs e atividades posteriores

### Aderência à skill de implementação

Foram lidos `.agents/skills/integration-system-testing-v1/SKILL.md`, `references/test-scope-boundary.md`, `analysis-input-contract.md` e `test-fit-check.md`. Trechos determinantes: "Exercita colaboração real entre pelo menos duas unidades ou uma fronteira técnica relevante"; "Testar endpoint com banco real de teste é integração"; "Não implemente ... funcionalidade ou correção em código de produção". A skill só pode ser invocada explicitamente com referência inequívoca à análise; invocação de versão proposed aprova somente a fatia elegível.

**Fatia de testes elegível: valid como proposta de handoff**, sujeita ao gate de atualidade da skill na execução futura. Evidências independentes: (1) E0–E8 cruzam HTTP, Application, adapter e DB real; (2) artefatos novos exclusivamente em tests/fixtures, alvo SQLite temporário e oráculos de código/contrato definidos. Os quatro pontos do fit-check são atendidos pela fatia proposta: resultado é teste, nível integrado, oráculos verificáveis e alvo local seguro. Não é teste unitário de caso com mocks; não exige construir rota inexistente.

Classificação: E0–E8 `integration` + API por interface real; recusas de sessão avaliam `non-functional` de segurança implementada, sem limiar de performance; não certificar `system-acceptance-e2e` da aplicação produtiva. Unitários existentes são contexto, sem trabalho novo de unitários. Correções A01–A12 são `product-change`/documentação; CI e infra permanentes são `external-test-operations`.

A exceção de ambiente/migrations é L12: usuário a autorizou expressamente como experimento reversível. Ela não é autorização genérica da skill para corrigir produto. O executor deve anunciar a fatia e a exceção, preservar os diffs e restaurar; se o gate considerar inseparável com alteração produtiva, reportar e encaminhar o experimento a executor direto sem expandir o código do produto.

| Responsável / atividade | Entrega e caminhos | Ambiente/comando | Limite |
|---|---|---|---|
| Executor futuro com `$integration-system-testing-v1` e caminho exato deste v001 | Dois arquivos propostos em tests e fixtures; comentário `Proveniência: decision-analysis prompts/backend/20261024-105607-cenario-integracao-ciclo-vida-perfil-autorizado-v001.md#v001` em código novo | tests para cenário; backend para regressão informativa; quality para Ruff | Invocação futura explícita; esta análise não implementa |
| Mesmo executor ou executor direto para L12 | Somente patches temporários Nix/migrations listados e sua reversão | Nix apropriado para ferramentas; Git fora Nix | Nunca entregar patch de produto permanente |
| Responsável pelo card/produto | Fornecer L01/L02, confirmar L03 e decidir L04/L05 | Artefato local/descrição de card | Sem inferir número de PR |
| Backend | Avaliar composição/transações, grafo e divergências A01–A12 em tarefas próprias | backend, fora desta fatia | Sem correções para fazer testes passarem |
| Responsável pelo PR/registro | Resultados, critérios inferidos, limites, skips e diffs completos temporários | Texto do PR, sem publicação nesta análise | Documento adicional não necessário por padrão; se exigido, definir handoff separado L10 |

Recomenda-se o mínimo de documentação: **este artefato decisório e texto do PR futuro**, além dos comentários de proveniência nos testes. A análise de contrato de sessão anterior é precedente de registro documental específico, mas não obriga novo arquivo em docs para este card. A skill de testes exclui relatórios gerados sem convenção explícita. Não inventar `docs/validacao-perfil.md` nem delegar publicação externa.

O resumo/PR futuro deve conter: HEAD; análise/versão; comando; Python/driver/dialeto; estado do grafo original e temporário; total e nomes de executados/ignorados/falhos; resultado de cada checkpoint; baseline real e diferenças; Ruff; diff completo de cada patch temporário (ou "não necessário"); comandos de restore e status final; limites de produção/privacidade; aceite oficial não verificável sem L01. Não imprimir tokens, hashes ou credenciais.

## Síntese

Proposta inicial de jornada integrada com conta criada por HTTP, login separado, duas sessões válidas, leitura, edições identitária/completa e exclusão lógica, seguida de recusas com controles positivos. A composição real de produção e a cadeia original de migrations não são certificadas. Dependências de tests estão presentes; duplicatas e duas heads persistem. Apenas a análise Markdown é entregue; aceite oficial e política de retenção/reutilização de email continuam pendentes nas lacunas identificadas.

## Apêndice A — insumo literal do usuário

```text
$decision-analysis-v4 Implementar "Criar cenário de integração para cadastro, consulta, edição e exclusão de perfil autorizado". O resultado esperado é um teste de integração executável. Antes de decidir o que ele contém, descubra o que o projeto define e implementa para o ciclo de vida do perfil do estudante, o que significa "perfil autorizado" neste projeto e quais componentes o teste pode usar. Esta é uma análise nova, iniciada do zero.

## Regra principal: não presumir

Todo fato deve vir de um artefato lido (histórico Git, código, testes, migrations, documentação de segurança, requisitos, matrizes de teste, configuração de ambiente), com o caminho indicado. O que nenhum artefato definir deve ser registrado como lacuna, nunca como fato.

- Separe em seções distintas: **(a) fatos encontrados**, com caminho e trecho; **(b) lacunas**, ou seja, o que nenhum artefato define; **(c) recomendações**, que são suas, com justificativa.
- Para cada lacuna, apresente as opções viáveis, recomende uma e marque se depende de decisão de produto ou se pode ser tomada tecnicamente com base no que existe.
- Quando artefatos divergirem (código, documentação, requisitos, testes), aponte a divergência, diga qual fonte parece mais confiável e por quê, sem escolher em silêncio.
- Não transponha para o perfil regras de outros recursos (formação, projeto, currículo, documentos) sem que um artefato de perfil as sustente.

## Ponto de partida

Parta exclusivamente do estado atual desta branch, criada a partir da `dev`. Não presuma a existência de nenhum teste, cenário, análise ou documentação sobre o ciclo de vida do perfil. Descubra por inspeção o que existe: o que existir entra como fato (e deve ter a cobertura avaliada), o que não existir entra como lacuna.

## Texto do card

Somente o título foi fornecido: "Criar cenário de integração para cadastro, consulta, edição e exclusão de perfil autorizado". Não há descrição nem critérios de aceite. **Não invente critérios.** Derive o que for possível do título e dos artefatos, marque a origem de cada critério como "inferido" e liste exatamente o que precisa ser fornecido para fechar cada lacuna.

## Fontes a analisar

1. **Histórico Git local.** A CLI do GitHub e a rede podem não estar disponíveis; **não dependa delas**. Localize por inspeção (merges "Merge pull request #N", squashes com sufixo "(#N)", mensagens e histórico dos arquivos) os trabalhos que criaram o cadastro de conta ou perfil, o acesso (login) e a sessão, a consulta de dados pessoais, a edição do perfil e a exclusão do perfil. Número de card não é número de PR: não infira a ligação apenas pela coincidência de números, e registre como identificou cada trabalho.
2. **Documentação pertinente**, localizada por busca (não presumida): requisitos funcionais e de segurança ligados a cadastro, consulta, edição e exclusão de perfil, autenticação, autorização, retenção e privacidade dos dados pessoais; o contrato de credenciais de sessão; o DER; matrizes ou planos de teste em `docs/`; e análises anteriores em `prompts/` sobre qualquer um desses temas.
3. **Código atual relacionado**: as rotas e os handlers de perfil e de acesso, os casos de uso, as entidades e portas, os repositórios, as migrations da tabela de usuários e da de sessões, o middleware de autenticação, a composição da aplicação (`main.py` e `factory.py`) e os testes existentes, unitários e integrados, que tocam esses temas.

## O que levantar

- **O ciclo de vida do perfil, operação por operação** (cadastro, consulta, edição e exclusão): método, caminho, de onde vem o identificador do dono (caminho, corpo, sessão), caso de uso, repositório, status HTTP de sucesso e de cada falha, formato de entrada e de saída, regras de validação (por exemplo e-mail único, formato de senha) e o mecanismo de autorização de cada operação (middleware, caso de uso ou ambos). Registre separadamente o que está **definido em documento** e o que está **só implementado sem definição**.
- **O que "perfil autorizado" significa neste projeto.** Pode significar a pessoa dona do perfil com sessão válida, ou existir algum outro conceito (papéis, permissões, escopo). Descubra se há qualquer conceito de papel ou permissão no código e na documentação, e **não presuma que existe**. Se apenas a posse da sessão autoriza, registre isso como fato e diga se o cenário deve cobrir apenas esse caso. Se o termo não estiver definido, trate como lacuna com as interpretações viáveis e uma recomendação.
- **Como o cadastro e a autenticação se encadeiam.** Em que momento a conta é criada, como a sessão é obtida antes de consultar, editar e excluir, e se o cadastro já emite sessão ou exige login separado.
- **O efeito da exclusão.** O que o código e a documentação definem sobre o estado da conta depois de excluída, o que acontece com as sessões ativas, com o acesso seguinte (consulta, edição, novo login) e com a repetição da exclusão; se o mesmo e-mail pode ser cadastrado de novo; e o que acontece com os dados relacionados. Registre apenas o que estiver definido ou implementado e trate o restante como lacuna, sem inventar o comportamento esperado.
- **A composição real.** Como a aplicação que sobe (`main.py`, `factory.py`) instala a autenticação e os casos de uso de perfil, com qual autenticador, e se o cadastro, o login, a consulta, a edição e a exclusão de perfil estão realmente ligados na composição de produção. **Não presuma o estado**: leia o código atual e registre o que a composição de produção faz, e o que isso implica para o que o cenário consegue provar. Recomende como o teste deve compor a aplicação (por exemplo, montando-a no próprio teste com componentes reais) e qual limite declarar sobre a composição de produção.
- **Cobertura existente:** o que os testes atuais já cobrem sobre o ciclo de vida do perfil, em que nível (unitário com doubles ou integração com banco real) e o que ainda não é coberto, para o cenário novo não repetir cobertura sem necessidade.
- **O que "cenário de integração" significa no projeto.** Procure em `docs/` e `prompts/` a definição, convenções e precedentes de cenário, matriz ou roteiro de teste de integração, e o formato esperado (um fluxo encadeado do início ao fim ou testes independentes por operação). Se nada definir, trate como lacuna e recomende. O título sugere um **cenário encadeado** (cadastro, consulta, edição, exclusão); avalie se isso deve ser um único fluxo com asserções entre as etapas, e quais verificações adicionais são necessárias (por exemplo o estado persistido em cada etapa, conferido por outra sessão de banco, e o comportamento depois da exclusão).
- **O ambiente de testes integrados:** o que `nix develop .#tests` oferece hoje, como os testes integrados existentes são organizados e executados, como o banco é preparado (SQLite e, se houver, PostgreSQL) e como o hash de senha é tratado nos testes (custo de tempo, se for deliberadamente lento).
- **Bloqueios de execução preexistentes:** verifique por inspeção e registre, **sem tratá-los como escopo e sem corrigi-los**, o estado da cadeia de migrations do Alembic (revisões duplicadas ou múltiplas heads), das dependências do ambiente `.#tests` (Python, driver SQLite assíncrono) e de qualquer rota do ciclo do perfil que não esteja implementada ou composta.

## Escopo

Definir o **cenário de integração executável** que percorre cadastro, consulta, edição e exclusão do perfil por uma pessoa autorizada, com componentes reais e banco migrado: etapas, dados, verificações, resultados esperados, fixtures, forma de execução e limites do que prova.

Fora do escopo: alterar rotas, casos de uso, persistência, middleware, contrato ou composição; corrigir defeitos de back-end encontrados (registre-os como achados); ativar autenticação na composição de produção; front-end; novas regras de negócio ou de segurança; alterações permanentes de ambiente.

## Instruções

- Para cada decisão que os artefatos não resolverem, recomende uma opção com justificativa e marque se depende de produto.
- Derive as etapas e as verificações do cenário dos documentos e do código. Cada etapa deve ter objetivo, pré-condições, passos, resultado esperado, a fonte que o sustenta e a origem do critério (definido ou inferido). Considere, apenas se algum artefato os definir ou implementar: cadastro; obtenção de sessão; consulta com dados corretos e sem expor segredos (hash de senha, token); edição com efeito persistido; exclusão; recusa de consulta, edição e novo acesso depois da exclusão; repetição da exclusão; e recusa de acesso sem sessão. Inclua um **controle positivo** em cada etapa em que uma recusa for verificada, para provar que a recusa vem da regra e não de uma rota que sempre falha. O que não estiver definido entra como lacuna, e a análise deve dizer se o cenário registra o comportamento atual como caracterização ou aguarda decisão.
- Defina a estrutura: nomes e localização dos arquivos conforme a convenção, reaproveitamento de fixtures existentes (verifique quais existem na base e **não presuma** que existem), preparação do banco (migrations aplicadas até o head, nunca `create_all`), isolamento entre testes, dependências do ambiente e como os testes que dependem de recurso ausente são ignorados com motivo explícito, sem gerar erro quando o ambiente não os suporta.
- **Honestidade da prova.** Um teste ignorado não é prova. Diga como o resultado distingue "executado e aprovado" de "ignorado por ambiente", e o que o cenário não prova (por exemplo, a composição de produção, o comportamento sob falha de banco, a retenção ou eliminação física dos dados).
- Registre achados de back-end (divergências entre código, documentação e contrato, comportamentos não definidos, riscos de segurança ou de privacidade) em seção própria, sem corrigi-los.
- Indique a divisão de trabalho. **Leia o contrato de escopo da skill `integration-system-testing-v1` e confirme, com evidência, se esta fatia é elegível**; se não for, ou se outra skill ou um executor direto for mais adequado, registre isso como lacuna de processo. Especifique nomes de arquivos, ambientes e comandos, para o executor não precisar inventá-los. Diga também se o resultado precisa de um registro em documento ou se basta o texto do PR, e recomende o mínimo, de acordo com os precedentes do projeto.
- **Alterações temporárias de ambiente.** Registre que, para executar o cenário, o executor poderá aplicar alterações temporárias em `nix/tests.nix` (Python do backend e o driver SQLite assíncrono necessário) e, se a cadeia do Alembic estiver com revisões duplicadas, uma linearização temporária das migrations. Ambas devem ser revertidas com `git restore` ao final, com os diffs completos copiados para o resumo, e `git status --short` não pode listar nenhum arquivo em `nix/`, `flake.nix`, `flake.lock` ou `alembic/versions/`. Se já houver mudanças do usuário nesses caminhos, a execução não deve restaurá-las: deve parar e informar.
- Defina o roteamento do artefato de análise (pasta em `prompts/`) conforme a organização existente.
- Registre na validação: a execução do cenário em `nix develop .#tests`; a execução informativa da suíte completa em `nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src`, que não pode gerar erros novos em relação ao baseline observado (registre o baseline real); e o gate de lint do CI ao final de cada execução: `nix develop .#quality --command ruff check src/backend` (se falhar por I001, corrigir com `nix develop .#quality --command ruff check --select I --fix <arquivos-apontados>` e repetir o gate completo).
- Não implemente nada.
```

