---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-16T22:16:32-03:00"
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
    - {path: AGENTS.md, relationship: context, representation: prose, function: prompt-instruction, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/AGENTS.md, relationship: context, representation: prose, function: prompt-instruction, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/factory.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "create_app: parâmetros, instalação do middleware e composição de routers", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/middleware_autenticacao.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/perfil_estudante.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "criar_router: consulta por ID, edição, perfil completo e exclusão atual", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/dados_contato.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/sessoes.py, relationship: supporting, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/main.py, relationship: supporting, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/autenticacao_sessao.py, relationship: supporting, representation: source-code, function: schema-contract, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/perfil_estudante.py, relationship: supporting, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "EditarPerfil e ConsultarPerfilEstudante", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/dados_contato.py, relationship: supporting, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/ports.py, relationship: supporting, representation: source-code, function: schema-contract, format: Python, analysis_scope: selected-section, locator: RepositorioUsuario, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_api_middleware_autenticacao.py, relationship: primary, representation: source-code, function: test, format: Python, analysis_scope: selected-section, locator: "testes de perfil próprio/alheio e dados de contato, chamadas diretas de dispatch", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_api_perfil_estudante.py, relationship: primary, representation: source-code, function: test, format: Python, analysis_scope: selected-section, locator: ConsultarPerfilRotaTestCase, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_api_dados_contato.py, relationship: primary, representation: source-code, function: test, format: Python, analysis_scope: selected-section, locator: "helper de Request e AtualizarDadosContatoRotaTestCase", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_integracao_isolamento_dados_estudantes.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_integracao_rejeicao_requisicoes_sem_credenciais_validas.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/fixtures/perfis_integracao.py, relationship: supporting, representation: source-code, function: data-fixture, format: Python, analysis_scope: selected-section, locator: "docstring, imports, IDs e definição de PerfilIntegracaoFake", content_state: working-tree, revision: null, availability: available}
    - {path: docs/contrato-credenciais-sessao.md, relationship: supporting, representation: prose, function: schema-contract, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: docs/requisitos-seguranca.md, relationship: supporting, representation: prose, function: documentation, format: Markdown, analysis_scope: selected-section, locator: "autenticação, sessão, autorização e seção 9", content_state: working-tree, revision: null, availability: available}
    - {path: docs/requisitos_funcionais.md, relationship: supporting, representation: prose, function: documentation, format: Markdown, analysis_scope: selected-section, locator: RF13, content_state: working-tree, revision: null, availability: available}
    - {path: docs/requisitos_nao_funcionais.md, relationship: supporting, representation: prose, function: documentation, format: Markdown, analysis_scope: selected-section, locator: RNF04, content_state: working-tree, revision: null, availability: available}
    - {path: docs/matriz_testes.md, relationship: supporting, representation: prose, function: documentation, format: Markdown, analysis_scope: selected-section, locator: "RF02, especialmente CT-RF02-06", content_state: working-tree, revision: null, availability: available}
    - {path: docs/configuracao-ambiente.md, relationship: context, representation: prose, function: documentation, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: flake.nix, relationship: supporting, representation: source-code, function: configuration, format: Nix, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: nix/tests.nix, relationship: primary, representation: source-code, function: configuration, format: Nix, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: nix/backend.nix, relationship: supporting, representation: source-code, function: configuration, format: Nix, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: nix/backend-python-packages.nix, relationship: supporting, representation: source-code, function: build, format: Nix, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: .github/workflows/ci.yml, relationship: supporting, representation: structured-data, function: configuration, format: YAML, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: prompts/README.md, relationship: context, representation: prose, function: documentation, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: prompts/backend/20261010-183257-isolamento-dados-estudantes-integracao-v004.md, relationship: context, representation: prose, function: documentation, format: Markdown, analysis_scope: selected-section, locator: "frontmatter até dimensões de decisão: solicitação, linhagem, escopo e critérios", content_state: working-tree, revision: null, availability: available}
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/ambientes, prompts/revisao, prompts/requisitos]
  confidence: high
  rationale: "O objeto principal é a integração HTTP de autorização do backend; o ajuste Nix é habilitador da cobertura."
classification:
  sphere: engineering
  concerns: [integration, security, reliability]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: high
---

# Análise de decisão — Recusa de perfil alheio com middleware ativo

## Solicitação original

Texto do usuário preservado literalmente:

```text
$decision-analysis-v4 para analisar a task:
“Criar teste de integração que recusa acesso a perfil alheio após o middleware estar ativo”.

Produza uma análise decisória que determine o escopo e oriente a implementação futura. Não implemente código nesta etapa.

Leia os AGENTS.md aplicáveis e siga o esquema, o roteamento e o versionamento da skill. Verifique se existe análise anterior da mesma demanda antes de escolher entre initial e revision.

Contexto observado no projeto, a confirmar na análise:
- create_app, em src/backend/api/factory.py, instala MiddlewareAutenticacaoSessao somente quando recebe autenticador_sessao.
- src/backend/main.py chama create_app() sem esse autenticador.
- O middleware valida o cookie __Host-sessao e instala request.state.usuario_id.
- PUT /estudantes/{usuario_id} e PUT /estudantes/{usuario_id}/dados-contato recusam identidade alheia com 403.
- GET /estudantes/{usuario_id} faz a comparação de propriedade no handler e mascara perfil alheio com 404.
- Os testes de isolamento de currículos ainda usam Authorization Bearer, não injetam autenticador e mantêm expectedFailure. Não representam cobertura do middleware ativo.
- nix/tests.nix disponibiliza apenas Git; a execução de integração exige avaliar a disponibilidade declarada de Python e das dependências, sem recorrer a ferramentas globais.

Examine prioritariamente:
- src/backend/api/factory.py
- src/backend/api/middleware_autenticacao.py
- src/backend/api/perfil_estudante.py
- src/backend/api/dados_contato.py
- src/backend/api/sessoes.py
- src/backend/main.py
- src/backend/application/autenticacao_sessao.py
- Os casos de uso e as portas efetivamente envolvidos nas rotas escolhidas.
- src/backend/tests/test_api_middleware_autenticacao.py
- src/backend/tests/test_api_perfil_estudante.py
- src/backend/tests/test_api_dados_contato.py
- src/backend/tests/test_integracao_isolamento_dados_estudantes.py
- src/backend/tests/test_integracao_rejeicao_requisicoes_sem_credenciais_validas.py
- src/backend/tests/fixtures/perfis_integracao.py
- docs/contrato-credenciais-sessao.md
- docs/requisitos-seguranca.md
- docs/requisitos_funcionais.md
- docs/requisitos_nao_funcionais.md
- docs/matriz_testes.md, especialmente CT-RF02-06
- docs/configuracao-ambiente.md
- flake.nix, nix/tests.nix e as dependências Nix pertinentes.

Decisões a resolver:
1. Delimitar “acesso a perfil alheio”: recomendar cobertura de consulta e atualização do perfil; avaliar dados de contato conforme CT-RF02-06. Não ampliar automaticamente para todos os recursos do estudante.
2. Comparar teste integrado via create_app com middleware real, casos de uso reais e portas determinísticas em memória versus integração adicional com autenticador e persistência reais. Explicitar o que cada alternativa comprova e seu custo.
3. Distinguir a composição necessária ao teste da ativação do middleware no entrypoint de produção. Tratar eventual alteração de main.py como handoff separado, salvo evidência de que faz parte desta task.
4. Decidir entre novo módulo de integração e evolução de módulo existente, evitando duplicação e alteração de análises históricas.
5. Definir o menor ajuste necessário no ambiente tests para executar a cobertura escolhida.

Direção recomendada para avaliação:
- Exercitar a aplicação ASGI criada pela fábrica oficial, atravessando middleware, roteamento, handlers e casos de uso.
- Usar estudantes A e B distintos e cookie sintético que o autenticador associe exclusivamente a A.
- Não injetar request.state manualmente, substituir dispatch ou chamar diretamente handlers como prova de integração.
- Se usar doubles, limitá-los às portas externas e declarar que isso não valida persistência de sessões nem login completo.
- Usar entradas válidas para que erros de validação não sejam confundidos com recusa de autorização.

Defina critérios de aceite verificáveis:
- A consulta o próprio perfil com sucesso; A tenta consultar B e recebe exatamente 404, sem dados privados de B.
- A altera o próprio perfil com sucesso; A tenta alterar B e recebe exatamente 403, preservando o estado de B.
- Aplicar o equivalente a dados de contato se incluídos no escopo.
- Sem cookie ou com cookie inválido, as operações selecionadas retornam exatamente 401.
- As recusas ocorrem antes da execução do caso de uso protegido, comprovadas por observação ou instrumentação sem substituir sua lógica.
- O controle positivo comprova que as dependências estão disponíveis: 422, 503 e qualquer erro genérico não contam como autorização correta.
- A identidade vem do cookie validado; o UUID no caminho apenas seleciona o alvo.
- Os cenários entregues executam sem skip ou expectedFailure.
- O transporte de teste captura o corpo completo e funciona com BaseHTTPMiddleware; avaliar os helpers ASGI antigos antes de reutilizá-los.
- Toda função e classe adicionada possui documentação sobre o que faz, como faz e para que existe.
- Testes de integração executam em nix develop .#tests; unitários pertinentes, se houver mudança de comportamento, em .#backend.

Entregue:
- Fatos, hipóteses e lacunas separados, com caminhos e recortes examinados.
- Comparação das alternativas e recomendação justificada.
- Lista dos arquivos a criar ou alterar na implementação futura.
- Matriz de cenários com método, rota, identidade, status esperado e efeitos proibidos.
- Estratégia e comandos de validação compatíveis com o Nix.
- Handoffs e limites explícitos, incluindo ambiente de testes e composição de produção quando necessários.

Não confunda os testes antigos de currículos com cobertura já existente desta task nem uniformize 403 e 404: preserve a política atual de cada operação.
```

## Informações complementares

A mensagem seguinte fornece a skill e seu caminho, sem alterar o problema. A consulta anterior do usuário, literalmente: “Para a task Criar teste de integração que recusa acesso a perfil alheio após o middleware estar ativo, analise o projeto (código e documentação) e me de um prompt para decision analysis que indique o que fazer.” A resposta anterior era um prompt preparatório, não uma análise versionada.

## Mudanças desde a versão anterior

Nenhum identificado — modo initial. A busca textual e por nomes em prompts/backend não identificou análise desta task. A v004 de isolamento refere-se à Issue #150, explicitamente a currículos e falhas esperadas; serve como contexto relacionado e não é substituída. Esta decisão cobre perfil com middleware ativo e não revisa retrospectivamente aquela entrega.

## Artefatos analisados

O inventário estruturado em `subjects.files` registra individualmente caminho, relação, representação, função, formato, recorte, estado e disponibilidade. A tabela abaixo apresenta os grupos para leitura; os recortes individuais do inventário prevalecem.

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| AGENTS.md; src/backend/AGENTS.md; prompts/README.md | context | prose | prompt-instruction/documentation | Markdown | completos | working-tree; revision null |
| src/backend/api/{factory,middleware_autenticacao,perfil_estudante,dados_contato}.py | primary | source-code | production | Python | conforme inventário individual | working-tree; revision null |
| src/backend/api/sessoes.py; src/backend/main.py | supporting | source-code | production | Python | completos | working-tree; revision null |
| src/backend/application/{autenticacao_sessao,perfil_estudante,dados_contato,ports}.py | supporting | source-code | production/schema-contract | Python | conforme inventário individual | working-tree; revision null |
| src/backend/tests/test_api_{middleware_autenticacao,perfil_estudante,dados_contato}.py | primary | source-code | test | Python | cenários de propriedade e controles, conforme inventário | working-tree; revision null |
| src/backend/tests/test_integracao_{isolamento_dados_estudantes,rejeicao_requisicoes_sem_credenciais_validas}.py | supporting | source-code | test | Python | completos | working-tree; revision null |
| src/backend/tests/fixtures/perfis_integracao.py | supporting | source-code | data-fixture | Python | cabeçalho, imports, IDs e estrutura | working-tree; revision null |
| docs/{contrato-credenciais-sessao,requisitos-seguranca,requisitos_funcionais,requisitos_nao_funcionais,matriz_testes,configuracao-ambiente}.md | supporting/context | prose | schema-contract/documentation | Markdown | conforme inventário individual | working-tree; revision null |
| flake.nix; nix/{tests,backend,backend-python-packages}.nix | primary/supporting | source-code | configuration/build | Nix | completos | working-tree; revision null |
| .github/workflows/ci.yml | supporting | structured-data | configuration | YAML | completo | working-tree; revision null |
| prompts/backend/20261010-183257-isolamento-dados-estudantes-integracao-v004.md | context | prose | documentation | Markdown | frontmatter, solicitação, escopo e critérios | working-tree; revision null |

### Limites da evidência dos artefatos

Inspeção estática do working tree, cujo HEAD observado é `254707b3d3a285aa4b91768c6a4bd35717b775cd`; não foram executados testes, builds ou avaliação Nix. `revision: null` evita afirmar equivalência individual dos arquivos com um commit. A consulta de Git anterior à escrita indicou working tree limpo. Recortes não demonstram ausência absoluta de outros testes nem validam os adapters concretos de sessão. Nenhuma issue remota foi consultada; o título fornecido pelo usuário é a identificação desta task.

## Problema enriquecido

### Resultado desejado

Adicionar cobertura integrada e ativa contra acesso cruzado a perfil, demonstrando que a aplicação oficialmente composta autentica por cookie, recusa alvo alheio e permite operações próprias. A prova deve atravessar middleware e roteamento e observar estado e execução de casos de uso.

### Atores e interesses

- Estudante A precisa consultar e editar seu perfil e contato.
- Estudante B precisa preservar seus dados privados e seu estado.
- Mantenedores precisam de falhas precisas quando composição, transporte ou autorização regressarem.

### Evidências e fatos observados

1. `factory.py:create_app` instala o middleware apenas com `autenticador_sessao`; `main.py` não fornece a dependência. A task pode compor a fábrica em teste sem alterar o entrypoint.
2. `middleware_autenticacao.py:dispatch` lê `COOKIE_SESSAO`, delega validação, retorna 401 quando ausente/inválido e instala o UUID validado em state. O reconhecimento de perfil por caminho cobre PUT, não GET. O middleware retorna 403 para PUT de perfil/contato alheio antes de encaminhar a requisição.
3. `perfil_estudante.py:consultar` recebe principal via dependência e devolve 404 com `Perfil não encontrado.` para ID alheio antes do executor. Edição tem também guarda local de identidade. Não uniformizar o status com o do middleware.
4. `EditarPerfil` consulta por ID/e-mail e atualiza o agregado; `ConsultarPerfilEstudante` consulta por ID; `AtualizarDadosContato` consulta e persiste novo estado. A porta `RepositorioUsuario` basta para controlar esses efeitos em memória.
5. Os testes unitários examinados chamam `dispatch` ou handlers diretamente; comprovam regras isoladas, sem provar o encadeamento ASGI. O módulo antigo de isolamento testa currículos, envia Bearer, não instala o autenticador e usa quatro expectedFailure.
6. O teste antigo de rejeição importa `backend.main.app`, usa expectedFailure/skip e permanece dependente de composição ausente. Sua documentação de inexistência do validador não pode ser usada como fato atual sobre todo o código.
7. CT-RF02-06 exige 403 e preservação dos dados de B para PUT de perfil ou contato; sem sessão, 401. RF13 exige autenticação e RNF04 limita consulta/alteração a usuários autorizados.
8. O contrato aceita 403 ou ocultação por 404 segundo o recurso; define cookie exclusivo. Sua descrição conceitual de Depends não justifica reescrever o middleware existente nesta task. Seu inventário de DELETE por ID diverge da rota atual `/estudantes/atual`; exclusão não integra esta decisão.
9. `nix/tests.nix` declara apenas Git. `backend.nix` obtém Python com bibliotecas de `backend-python-packages.nix` (FastAPI, Uvicorn, SQLAlchemy, Alembic, Psycopg e pydantic-settings). Há fonte reutilizável de dependências, sem necessidade de pytest.
10. O workflow atual descobre todos os testes backend em `.#backend`, incluindo módulos de integração pelo padrão de descoberta. Isso não cumpre a separação formal exigida pelos AGENTS para integração e exige handoff explícito de CI.

### Hipóteses

- H1: o escopo de integração entre componentes, sem banco, satisfaz esta task; o título não exige autenticação persistida nem login completo.
- H2: Python e o conjunto compartilhado do backend permitem executar a nova suíte em tests; a resolução efetiva do ambiente deve ser verificada na implementação.
- H3: é possível manter transporte ASGI local sem nova biblioteca. Os helpers antigos entregam disconnect imediatamente após o request; sua compatibilidade com resposta transmitida por BaseHTTPMiddleware não está demonstrada.

### Perguntas em aberto

Nenhuma exige resposta do usuário para propor a decisão. A compatibilidade do transporte é investigação técnica de implementação. Se o aceite externo exigir banco ou login completo, reabrir a escolha de fidelidade.

### Escopo

GET de perfil por ID, PUT de perfil por ID e PUT de dados de contato por ID. Incluir contato porque compartilha a fronteira de autorização e está explicitamente no CT-RF02-06. Usar `ConsultarPerfilEstudante`, `EditarPerfil` e `AtualizarDadosContato` reais, middleware real, domínio real e repositório de usuários em memória observável. Autenticador determinístico na porta associa apenas o token sintético conhecido a A.

### Fora do escopo

Ativar main.py, login/logout completos, banco e migrations, expiração/revogação persistida, CSRF, novas regras de autorização, DELETE, perfil completo `/me/perfil`, currículos e demais recursos. Não atualizar módulos antigos ou análises históricas incidentalmente. Não alegar cobertura de segurança do deployment a partir desta composição de teste.

### Critérios de sucesso

Cada operação tem controle próprio 200, recusa cruzada no status exato e dois controles 401. Todos executam sem skip/expectedFailure. Entradas de escrita são válidas e equivalentes entre controle positivo e negativo. Nenhuma recusa chama o caso de uso protegido; nenhum dado privado de B aparece; nenhuma escrita altera B ou A no cenário negado. State é instalado somente pelo middleware. A aplicação contém o middleware configurado e o autenticador recebe o cookie correto.

## Restrições aplicáveis

Nesta etapa, escrever somente este novo Markdown. Implementação futura respeita Clean Architecture/DDD; doubles implementam portas externas. Toda função/classe nova, inclusive helpers e métodos internos, documenta responsabilidade, abordagem e finalidade. Integração executa exclusivamente em `.#tests`; unitários em `.#backend`. Git/gh ficam fora de Nix. Não usar ferramentas globais, substituir a política 403/404 ou aceitar qualquer status >=400 como sucesso.

## Classificação comentada

Engineering domina; integration, security e reliability descrevem o problema. Objeto mixed porque demanda de cobertura e comportamento de arquivos têm igual relevância. Escopo component: backend. Risco high corresponde ao impacto de acesso indevido a dados pessoais, apesar de a mudança proposta ser reversível. Incerteza medium decorre de transporte e ambiente ainda não exercitados.

## Decisão de roteamento

Inventário real das subpastas imediatas: backend, ambientes, frontend, templates, revisao e requisitos. Escolher `prompts/backend`, pois a decisão entrega cobertura do backend. Ambientes é candidata secundária para um habilitador; revisao e requisitos não descrevem tão bem o propósito. Não foram encontrados AGENTS locais em prompts nem AGENTS.override.md no inventário aplicável. As regras da raiz e prompts/README.md governam a saída.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | Alta | Status, ausência de execução e efeitos exatos | Evita falsos positivos por 422/503 ou bloqueio total |
| security | Alta | Limiar de propriedade e origem autenticada | Protege dados e identidade do ator |
| reliability | Alta | Determinismo e transporte completo | Evita testes instáveis ou sem corpo observado |
| simplicity | Média | Menor composição que prove o requisito | Reduz manutenção e dependências |
| delivery-speed | Média | Cobertura executável com pouco preparo | Evita adiar a proteção por infraestrutura desnecessária |

## Alternativas consideradas

**A — Estado atual:** regras unitárias e testes antigos de lacuna. Custo imediato nulo, mas não comprova a integração solicitada. Inviável como entrega final.

**B — Integração ASGI com portas em memória:** fábrica, middleware, routers e três casos de uso reais; autenticador e repositório determinísticos. Novo módulo focado em perfil. Prova transporte do cookie, composição e autorização, controles positivos e efeitos da aplicação. Não prova hash do token, consulta persistida, expiração, revogação, emissão do cookie nem login.

**C — Integração com autenticador e persistência reais adicionais:** preserva a matriz de B e acrescenta sessões/usuários persistidos, configuração isolada do ORM e controle de relógio. Oferece fidelidade adicional à validação da sessão, com mais preparação, recursos e diagnóstico. Viável como estratégia futura, condicionada a inspeção dos adapters concretos; não há evidência suficiente aqui para especificar suas APIs. Login completo continua sendo acréscimo separado, não consequência automática de C.

Criar novo módulo é preferível a converter o de currículos: mantém linguagem de perfil e oráculos exatos, sem misturar a linhagem anterior. Evitar duplicar um harness se já houver helper compatível e compartilhável; não generalizar helpers antes de comprovar necessidade.

## Perfil de pagamento comparativo

Escala ordinal relativa ao estado atual; não somar. C representa o benefício esperado após implementação validada, com confiança menor pela inspeção limitada de infraestrutura.

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| correctness | Alta | 0 | +2 | +2 | Alta para B; média para C | B e C exercitam o encadeamento hoje ausente |
| security | Alta | 0 | +1 | +2 | Média | C acrescenta autenticador/persistência reais; B cobre autorização integrada |
| reliability | Alta | 0 | +2 | +1 | Média | B controla portas; C exige isolamento de infraestrutura |
| simplicity | Média | 0 | -1 | -2 | Alta | B acrescenta módulo e ambiente; C adiciona ciclo de banco/sessões |
| delivery-speed | Média | 0 | -1 | -2 | Média | C exige preparação além do requisito de propriedade |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado nesta linhagem. A decisão relacionada da Issue #150 mantém seu contexto histórico de currículos com falhas esperadas.

### Decisão recomendada nesta versão

Adotar B. Criar `src/backend/tests/test_integracao_recusa_perfil_alheio.py` com unittest.IsolatedAsyncioTestCase, três casos de uso reais compartilhando repositório em memória e autenticador determinístico injetado por create_app. O cookie conhecido deve produzir A; token diferente retorna None; não aceitar Bearer como credencial.

Usar observação transparente de `executar` nos objetos reais (por exemplo, spy com wraps e inspeção de awaits), mantendo a lógica original. O spy não é executor substituto nem decide respostas. Comparar contadores/histórico antes e depois de cada request; para negativos, confirmar ausência de novas chamadas nos três executores. Apenas ausência de consulta ao repositório não basta como prova literal de ausência de execução do caso de uso. Snapshots de domínio devem copiar valores de perfil/contato, evitando comparação de referências mutáveis. Casos são isolados, com usuários e repositório novos por teste.

O transporte preferido é ASGI em memória, com scheme HTTPS para representar cookie Secure. Declarar versão ASGI HTTP suportada e manter receive compatível com a emissão completa da resposta, sem desconectar prematuramente; capturar todos os fragmentos até more_body falso. Confirmar JSON e marcador privado no controle positivo antes de confiar em sua ausência nos negativos. Se o harness local exigir complexidade desproporcional, reavaliar cliente ASGI e declarar sua dependência em Nix; não recorrer a biblioteca global ou ao helper antigo sem validação.

No ambiente tests, importar `nix/backend-python-packages.nix` e declarar `pkgs.python3.withPackages` com esse conjunto, seguindo o padrão já usado pelo backend. Não copiar listas nem acrescentar pytest/httpx antecipadamente. Esse é o menor ajuste de arquivos com dependências centralizadas e sem mudança na política de ambientes.

### Impacto da revisão

Nenhum identificado — primeira versão; decisão proposta, ainda sem implementação ou aprovação registrada.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | Encadeamento e efeitos verificáveis | Guardas reais e controles próprios |
| reliability | prioritized | Isolamento sem banco ou relógio real | Portas determinísticas e harness validado |
| simplicity | prioritized | Menor preparo que C | Fábrica e casos de uso já disponíveis |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| security | Autenticação anterior ao acesso; propriedade preservada | Cookie conhecido, 401/403/404, ausência de dados e efeitos |
| delivery-speed | Nova suíte executável com dependências declaradas | Novo módulo e reutilização do conjunto Python existente |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | Teste aprova 503/422 ou não detecta execução indevida | Alta | Mantenedores e estudantes |
| reliability | Corpo vazio por disconnect simula ausência de vazamento | Alta | Mantenedores |
| security | Regressão permite consultar/alterar B | Alta | Titular de B |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| reliability/simplicity | Não verificar autenticador e banco reais nesta task | security, em amplitude de cobertura | Aceito somente declarando o limite e handoff |
| correctness | Instrumentar executores e comparar snapshots | simplicity | Necessário para provar execução e efeitos |
| reliability | Acrescentar Python/dependências a tests | delivery-speed | Necessário para execução reproduzível |

## Riscos e efeitos de segunda ordem

- Guards locais podem manter 403 mesmo se o middleware deixar de comparar proprietário. A suíte deve também comprovar instalação/uso do autenticador; a prova específica de interrupção em dispatch permanece nos unitários existentes. Não confundir camadas da garantia.
- Autenticador que devolve A para todo token oculta cookie inválido; usar mapa fechado e histórico de tokens.
- Resposta 404 pode vir de rota inexistente: o mesmo padrão com A precisa retornar 200 e dados esperados.
- Snapshots incompletos podem perder mudanças de contato; comparar todos os campos relevantes, identidade e credencial sem imprimir segredos.
- O fixture híbrido existente depende de SQLAlchemy e persistência para usuários/currículos; não importar seu ciclo de banco apenas para dois perfis em memória. Reutilizar convenções sintéticas ou VOs pertinentes após inspeção adicional.
- A CI atual mistura níveis; uma suíte nova descoberta por backend não comprova execução no ambiente exigido para integração.

## Validação da decisão

Matriz mínima de 12 cenários, parametrizáveis com subTest sem perder identificação individual:

| Método | Rota | Identidade | Status | Evidência e efeitos proibidos |
|---|---|---|---:|---|
| GET | /estudantes/A | Cookie válido A | 200 | DTO de A e marcador presente; consulta real para A; sem B |
| GET | /estudantes/B | Cookie válido A | 404 | detail genérico; sem chamada dos casos de uso, dados de B ou mudanças |
| GET | /estudantes/B | Sem cookie | 401 | Sem casos de uso, dados privados ou mudanças |
| GET | /estudantes/B | Cookie inválido | 401 | Token observado pelo autenticador; sem casos de uso, dados ou mudanças |
| PUT | /estudantes/A | Cookie válido A | 200 | Nome/e-mail novos em A; B preservado; executor real com A |
| PUT | /estudantes/B | Cookie válido A | 403 | Nenhum executor invocado; snapshot de A e B preservado |
| PUT | /estudantes/B | Sem cookie | 401 | Nenhum executor invocado; A e B preservados |
| PUT | /estudantes/B | Cookie inválido | 401 | Nenhum executor invocado; A e B preservados |
| PUT | /estudantes/A/dados-contato | Cookie válido A | 200 | Contato de A atualizado; B preservado; executor real com A |
| PUT | /estudantes/B/dados-contato | Cookie válido A | 403 | Nenhum executor invocado; A e B preservados |
| PUT | /estudantes/B/dados-contato | Sem cookie | 401 | Nenhum executor invocado; A e B preservados |
| PUT | /estudantes/B/dados-contato | Cookie inválido | 401 | Nenhum executor invocado; A e B preservados |

Todos os negativos devem verificar ausência de dados privados de B, inclusive respostas de escrita. O cookie válido permanece de A quando o alvo muda para B. Usar nome/e-mail sintéticos válidos sem colisão e endereço/telefone aceitos pelo domínio. Não enviar propriedade alternativa no corpo fora do contrato; a divergência entre principal A e alvo B já demonstra a resistência à troca de identidade pela URL.

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| B satisfaz o aceite | Matriz completa passa com middleware real | Execução integrada | Aceite exigir sessão persistida/login |
| Transporte é confiável | Corpo positivo completo e todos os eventos finais recebidos | Exercitar GET e PUT autorizados | Corpo vazio, timeout ou disconnect prematuro |
| Ambiente é suficiente | Python e dependências vêm do Nix declarado | Comando em tests e inspeção do ambiente | Dependência ausente ou Python herdado da máquina |
| Negativos não executam aplicação | Histórico de await não cresce | Spies transparentes e snapshots | Executor é chamado mesmo sem escrita |

Comandos futuros, da raiz, após os ajustes declarativos do ambiente e criação do módulo:

```bash
nix develop .#tests --command python -m unittest discover -s src/backend/tests -t src -p test_integracao_recusa_perfil_alheio.py -v
nix develop .#tests --command python -m unittest discover -s src/backend/tests -t src -p 'test_integracao_*.py' -v
```

Executar primeiro o módulo novo. A segunda verificação delimita regressões nas integrações existentes; registrar honestamente seus expectedFailure/skip legados, que não são aceitos no módulo novo. Não ampliar a bateria após os checks pertinentes sem nova mudança ou falha que o justifique.

Caso implementação descubra necessidade de alterar comportamento produtivo, incluir/executar unitários pertinentes no ambiente backend e reavaliar escopo. Exemplo de regressão dirigida das guardas atuais:

```bash
nix develop .#backend --command python -m unittest discover -s src/backend/tests -t src -p test_api_middleware_autenticacao.py -v
```

Esta análise não executou esses comandos; não declara aprovação técnica de código ainda inexistente.

## Handoffs e atividades posteriores

| Arquivo/atividade | Ação futura | Limite e finalidade |
|---|---|---|
| src/backend/tests/test_integracao_recusa_perfil_alheio.py | Criar módulo com 12 cenários, portas em memória, instrumentação e transporte | Entrega central; sem executores falsos nem state manual |
| nix/tests.nix | Reutilizar conjunto Python compartilhado e adicionar runtime | Habilitador necessário, sem editar nesta análise |
| nix/backend-python-packages.nix | Reutilizar, sem alteração prevista | Não adicionar cliente HTTP sem necessidade demonstrada |
| .github/workflows/ci.yml | Separar seleção de unitários e integração; executar integração em tests | Handoff de CI necessário para automatizar cumprimento dos ambientes; não basta duplicar descoberta total no backend |
| src/backend/main.py e composição externa | Analisar ativação real de autenticação com dependências concretas | Atividade separada; a nova suíte não a entrega |
| Autenticador/persistência de sessões | Planejar integração real com relógio e banco isolados, se requerida | Prova adicional de hash, expiração, revogação e conta excluída |
| Módulos antigos de currículos/rejeição | Avaliar atualização posterior de Bearer e expectedFailure obsoletos | Linhagens e aceites próprios; não os converter nesta task |
| Documentação de segurança | Reconciliar inventários históricos com rotas e composição atuais | Não reescrever contratos incidentalmente |

Nenhuma alteração de produção, configuração, CI ou testes foi realizada nesta etapa.

## Síntese

Propor novo teste integrado de perfil e contato pela fábrica oficial, com middleware e casos de uso reais, autenticador/repositório em memória e oráculos 200/401/403/404 precisos. Preparar o ambiente tests com dependências compartilhadas e encaminhar separação da CI. A principal incerteza é a compatibilidade do transporte ASGI e do ambiente ainda não executados; não impede a decisão de escopo, mas deve ser resolvida antes de considerar a implementação validada.
