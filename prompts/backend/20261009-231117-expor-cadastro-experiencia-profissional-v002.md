---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v002"
status: pending
created_at: "2026-10-09T23:11:17-03:00"
lineage:
  mode: revision
  root: prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md
  supersedes: prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md
  change_type: scope-change
  secondary_change_types: [enrichment, reassessment]
  decision_impact: reopened
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/api/projeto_academico.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/application/cadastro_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/domain/itens_perfil.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ExperienciaProfissional e __post_init__"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ExperienciaProfissionalId, UsuarioId e Periodo"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/tests/test_api_projeto_academico.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/tests/test_application_cadastro_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/tests/test_domain_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF01, RF02, RF03 e RF13"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: docs/requisitos-seguranca.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "seções 1, 2.1, 2.2 e 2.6"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: docs/mapeamento_jornadas.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "seção 6.5, UC04"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: markdown/mermaid
      analysis_scope: selected-section
      locator: "EXPERIENCIA_PROFISSIONAL"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261005_0002_criar_curriculos.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/frontend]
  confidence: high
  rationale: "O card trata o endpoint e a composição de um caso de uso do backend; requisitos e segurança são evidências de apoio."
classification:
  sphere: engineering
  concerns: [integration, security, implementation]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: high
  reversibility: moderate
  risk: high
---

# Análise de decisão — expor cadastro de experiência profissional no backend

## Solicitação original

Versão v001: “$decision-analysis-v4 Implementar cadastro de experiências profissionais com relação às camadas de casos de uso e domain. Use doubles de teste apropriados para testes unitários.”

## Informações complementares

Nova solicitação, preservada literalmente: “$decision-analysis-v4 Fa;a uma analise para o card Expor cadastro de experiência profissional no backend. Inclua os testes unitarios adequados”

Interpretação: o foco passa da criação do núcleo Domain/Application para a exposição do cadastro por uma interface do backend. A solicitação também pede que a análise identifique os testes unitários adequados; não pede sua implementação ou execução.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Objetivo | Criar domínio, caso de uso e portas | Expor o cadastro no backend | Novo card amplia o limite até a API | Escopo muda para interface, segurança e composição |
| Estado do código | Entidade, caso de uso e portas eram trabalho futuro | Esses elementos e testes unitários já existem em `388fa9e` | Reavaliação do repositório na branch `task94` | O trabalho anterior passa a ser pré-requisito atendido |
| API de experiências | Fora do escopo | Não encontrada | O novo card demanda uma fronteira HTTP | É necessário decidir contrato e identidade do ator |
| Persistência concreta | Fora do escopo | Porta existe, adapter e migration específicos não foram encontrados | A exposição pode significar apenas rota ou fluxo persistente | Escopo de produção continua incerto |
| Testes | Doubles para domínio e Application | Testes existentes cobrem domínio/Application; novos testes de handler são necessários | Complemento explícito do usuário | Testes de rota unitários entram no card |
| Decisão | Cadastro interno recomendado | Reaberta até definir autenticação e persistência esperadas | RF13 exige autenticação para dados pessoais | Não recomendar exposição sem identidade confiável |
| Roteamento | `prompts/backend` | `prompts/backend` | O assunto permanece no backend | Sem mudança de pasta |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo: solicitação, escopo e decisão | Commit `388fa9e` |
| `src/backend/api/projeto_academico.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo; padrão atual de router, DTOs, resposta e erros | Commit `388fa9e` |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo; composição e executores opcionais | Commit `388fa9e` |
| `src/backend/application/cadastro_experiencia_profissional.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo; entrada, execução, geração de ID e porta | Commit `388fa9e` |
| `src/backend/domain/itens_perfil.py` | Apoio | Código-fonte | Produção | Python | Entidade `ExperienciaProfissional` e validação dos textos | Commit `388fa9e` |
| `src/backend/domain/value_objects.py` | Apoio | Código-fonte | Produção | Python | IDs tipados e `Periodo` | Commit `388fa9e` |
| `src/backend/tests/test_api_projeto_academico.py` | Apoio | Código-fonte | Teste | Python | Arquivo completo; testes diretos do handler com doubles | Commit `388fa9e` |
| `src/backend/tests/test_application_cadastro_experiencia_profissional.py` | Apoio | Código-fonte | Teste | Python | Arquivo completo; sucesso e falha antes de salvar | Commit `388fa9e` |
| `src/backend/tests/test_domain_experiencia_profissional.py` | Apoio | Código-fonte | Teste | Python | Arquivo completo; textos obrigatórios e período | Commit `388fa9e` |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF01, RF02, RF03 e RF13 | Commit `388fa9e` |
| `docs/requisitos-seguranca.md` | Apoio | Prosa | Documentação | Markdown | Visão de proteção de dados e autenticação | Commit `388fa9e` |
| `docs/mapeamento_jornadas.md` | Apoio | Prosa | Documentação | Markdown | Seção 6.5 / UC04 | Commit `388fa9e` |
| `docs/modelagem_der.md` | Apoio | Diagrama/modelo | Contrato de schema | Markdown/Mermaid | Entidade e campos de experiência | Commit `388fa9e` |
| `src/backend/infrastructure/persistence/sqlalchemy/curriculo.py` | Apoio | Código-fonte | Produção | Python | Modelo ORM existente, usado como referência de mapeamento | Commit `388fa9e` |
| `src/backend/infrastructure/persistence/alembic/versions/20261005_0002_criar_curriculos.py` | Apoio | Código-fonte | Produção | Python | Migration existente, usada como referência Code First/Alembic | Commit `388fa9e` |
| `AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Arquivo completo; Nix, testes e documentação | Commit `388fa9e` |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Arquivo completo; arquitetura, domínio e testes backend | Commit `388fa9e` |

### Limites da evidência dos artefatos

A análise usa o estado committed `388fa9e` da branch `task94`, cujo working tree estava limpo. A busca pelo backend mostrou modelo e migration de currículo, mas não identificou modelo ORM, migration ou adapter de repositório para experiência profissional. Não foi examinada uma especificação de contrato HTTP aprovada para UC04. A API de projeto é uma convenção existente, não prova de que a identidade via `usuario_id` na URL satisfaz RF13. A migration foi examinada como referência; não se inferiu dela um desenho completo de sessão/transação.

## Problema enriquecido

### Resultado desejado

Disponibilizar o cadastro de uma experiência profissional pela API do backend, usando o caso de uso existente, sem expor a entidade diretamente, preservando as invariantes e garantindo que o registro seja associado ao estudante autenticado. O endpoint deve ter testes unitários próprios.

### Atores e interesses

- Estudante: registrar dados profissionais e receber confirmação com a experiência criada.
- API: validar e converter a entrada HTTP, invocar Application e mapear erros para respostas estáveis.
- Application: preservar a orquestração já existente e receber identidade confiável e dados tipados.
- Infraestrutura: persistir a entidade se o card exigir comportamento funcional com armazenamento real.
- Equipe: limitar o escopo do card e evitar que a rota exponha cadastro sem controle de acesso.

### Evidências e fatos observados

- UC04 descreve organização, cargo, período e descrição e prevê múltiplas experiências.
- RF01 exige cadastro de experiências; RF02 menciona consulta, edição e exclusão; RF03 prevê centralização para uso nos currículos.
- RF13 exige autenticação para acesso às informações pessoais e aos currículos.
- O domínio já tem `ExperienciaProfissional`, com identidade e proprietário tipados, textos essenciais não vazios e `Periodo`.
- A Application já tem `CadastrarExperienciaProfissional`, entrada tipada, geração de ID e persistência assíncrona por porta.
- Testes unitários de domínio e Application já usam valores determinísticos e doubles sem banco.
- A rota de projeto acadêmico demonstra DTOs, router com executor injetável, status 201/422/503 e teste direto do handler com caso de uso e repositório double.
- `create_app` recebe executores opcionais e não constrói por si só adapters ou sessões de banco.
- Não foi encontrado endpoint nem adapter/migration de experiência no estado examinado.

### Hipóteses

- O novo card pretende adicionar somente o endpoint de criação; os comportamentos de consulta, edição e exclusão continuam em cards próprios, apesar de RF02.
- A forma da rota pode acompanhar as rotas atuais de itens do estudante, mas a identidade usada deve vir de principal autenticado ou dependência equivalente, não de um UUID arbitrário aceito como prova de propriedade.
- Campos de entrada são `empresa`, `cargo`, `descricao`, `data_inicio` e `data_fim` opcional, conforme entidade/DER. Limites de tamanho ainda não estão definidos.
- O caso de uso existente permanece responsável por domínio e porta; a API não acessa banco diretamente.
- A necessidade de migration e adapter depende de o aceite exigir persistência real ou apenas exposição do contrato com dependências compostas externamente.

### Perguntas em aberto

- O card inclui persistência Code First e composição do adapter, ou apenas endpoint e contrato HTTP?
- O projeto terá, neste card, uma dependência de identidade autenticada capaz de fornecer `UsuarioId` ao handler? Qual interface e mecanismo de sessão devem ser usados?
- O usuário espera que o endpoint esteja operacional ao importar `main.app`, ou a injeção do caso de uso permanece responsabilidade do ambiente externo?
- Quais limites máximos de texto devem constar no DTO, se houver?

### Escopo

Proposta para o card, sujeita à resposta sobre autenticação e armazenamento:

- Criar DTO de requisição e resposta, router `POST` e registro do router em `create_app`.
- Converter datas para `Periodo`, mapear os dados para `CadastrarExperienciaProfissionalEntrada` e devolver DTO público, sem serializar a entidade.
- Obter a identidade do estudante da fronteira autenticada.
- Traduzir entrada inválida/regra de domínio para 422 e dependência indisponível para o comportamento definido pelo projeto.
- Adicionar testes unitários do handler/API com executor real e doubles determinísticos, mantendo os testes Domain/Application existentes.
- Se persistência real for aceite do card: incluir ORM, migration Alembic, adapter e composição externa, preservando Code First e Clean Architecture.

### Fora do escopo

- Consulta/listagem, edição e remoção, salvo inclusão explícita no aceite.
- Alterar invariantes ou criar regra de negócio nova sem requisito aprovado.
- Inventar limites de tamanho, enumerações ou normalização de textos.
- Fazer chamadas de rede, banco real ou testes end-to-end no conjunto de testes unitários.
- Confiar em `usuario_id` enviado pelo cliente como autenticação/autorização.

### Critérios de sucesso

- A rota é registrada no app e invoca `CadastrarExperienciaProfissional` pela fronteira de Application.
- A resposta contém somente campos públicos e reflete a experiência criada, sem DTO ou entidade de domínio cruzar a API sem conversão.
- O `UsuarioId` usado no cadastro vem de identidade autenticada confiável, conforme RF13.
- Dados aceitos constroem `Periodo` válido e são validados no DTO/domínio em suas respectivas fronteiras.
- Testes unitários cobrem sucesso e mapeamento da resposta, indisponibilidade do executor, violação de domínio com 422 e ausência de persistência após falha; cobrem também conversão/validação de datas e associação ao usuário autenticado.
- Os testes são determinísticos e isolados de banco e rede. Se persistência estiver no card, o aceite da migration/modelo e adapter requer testes próprios no escopo de infraestrutura, sem confundi-los com os testes unitários do handler.

## Restrições aplicáveis

- RF13 exige autenticação para acesso a informações pessoais. A API não pode tratar um identificador arbitrário de URL como autenticação.
- Clean Architecture: API converte transporte e orquestra a chamada, sem acesso direto ao banco ou regras de negócio; dependências apontam para dentro.
- Entidades e value objects não são DTOs de HTTP.
- Persistência relacional, se incluída, segue ORM Code First e migration gerenciada por Alembic.
- Toda função/classe/DTO alterado ou criado deve documentar o que faz, como faz e a finalidade.
- Testes unitários backend pertencem ao ambiente `nix develop .#backend`; testes de integração ou nível superior usam `nix develop .#tests`.
- Esta análise não implementa nem executa testes.

## Classificação comentada

`engineering` domina: a decisão expõe um caso de uso existente na API. `integration` cobre o acoplamento entre handler e executor/composição; `security` é decisiva porque se trata de informação profissional pessoal e RF13 exige autenticação; `implementation` cobre contrato HTTP e testes. A incerteza é alta porque o card não define autenticação nem se inclui armazenamento operacional. O risco é alto pelo possível acesso indevido a dados pessoais.

## Decisão de roteamento

Destino escolhido: `prompts/backend`. As candidatas observadas foram `prompts/backend`, `prompts/requisitos` e `prompts/frontend`. Backend é a pasta semântica mais específica para endpoint, composição e testes; requisitos sustenta a necessidade, e frontend não é o objeto do card. A instrução local de `prompts/backend` foi procurada e não havia `AGENTS.md` ou `AGENTS.override.md` nessa pasta; aplicam-se as regras da raiz.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Security | Muito alta | Obrigatório atender RF13 | A experiência é dado pessoal e pertence a um usuário |
| Correctness | Alta | Priorizar | Datas e propriedade precisam chegar corretas ao caso de uso |
| Interoperability | Alta | Priorizar | Contrato HTTP deve se integrar ao executor já existente |
| Simplicity | Média | Satisfazer | Reusar domínio e Application já implementados |
| Delivery-speed | Média | Otimizar após segurança | Rota e testes podem ser pequenos se composição for esclarecida |

## Alternativas consideradas

### A — Expor somente a rota com identidade confiável, deixando adapter em outro card

Adicionar DTO/router/factory e teste unitário; o executor é fornecido por injeção. É a menor entrega alinhada ao texto “expor cadastro”. Só é viável se existir uma dependência autenticada confiável e se a ausência de adapter/composição persistente estiver explicitamente fora do aceite. No estado atual, `create_app` deixa executores opcionais e a rota análoga retorna 503 quando ausentes.

### B — Entregar fluxo funcional completo: rota, identidade autenticada, adapter, migration e composição

Adiciona a rota e conecta o caso de uso a armazenamento Code First. Atende melhor a interpretação de cadastro persistente disponível no app, mas amplia o card porque sessão/transação e dependência de autenticação ainda não foram definidas.

### C — Repetir o padrão atual de rota com `usuario_id` livre no path

É mais rápido e parecido com endpoints existentes, mas não demonstra identidade autenticada e conflita com RF13. Inviável como comportamento liberável para dados pessoais, embora exista como padrão histórico do código.

### D — Adiar a rota até definir autenticação e aceite de persistência

Evita publicar um fluxo que não satisfaz segurança e evita implementar uma rota que pode permanecer indisponível. É a única escolha segura enquanto as duas respostas em aberto faltarem; não entrega o card ainda.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | A | B | C | D | Confiança | Base |
|---|---:|---:|---:|---:|---:|---|---|
| Security | Muito alta | +1* | +1* | -2 | +2 | Alta | RF13; *só com identidade autenticada real |
| Correctness | Alta | +1* | +2* | 0 | 0 | Média | Caso de uso pronto; persistência concreta ausente |
| Interoperability | Alta | +1 | +2 | +1 | 0 | Média | Router atual e composição por executor |
| Simplicity | Média | +2 | -1 | +2 | +1 | Alta | B incorpora adapter/migration/composição |
| Delivery-speed | Média | +2* | -1 | +2 | -2 | Média | A só funciona se identidade e executor existirem |

Os efeitos condicionais de A e B não constituem recomendação sem resolver as condições. A tabela usa escala ordinal e não soma valores.

## Histórico e decisão atual

### Decisão da versão anterior

Em v001, recomendou-se criar entidade/caso de uso/portas e deixar API, autenticação, ORM, migration e adapter como handoffs. Essa decisão foi executada no estado atual para domínio e Application: arquivos correspondentes e testes estão presentes em `388fa9e`.

### Decisão recomendada nesta versão

`status: pending`. A evidência confirma que a camada API deve chamar o caso de uso existente e que testes unitários do handler devem seguir o padrão de doubles. Porém, não há base para escolher entre A e B: o texto do card não esclarece se “expor” significa somente endpoint ou cadastro persistente operacional; além disso, RF13 impede decidir a identidade do estudante como um valor livre do cliente. Enquanto isso não for esclarecido, D é a decisão provisória de segurança: não liberar endpoint sem identidade autenticada confiável. Após esclarecimento, preferir A se adapter/composição e autenticação já estiverem garantidos fora do card; caso contrário, rever para B ou separar dependências em cards explícitos.

A pergunta mínima para destravar é: **este card inclui autenticação confiável e persistência operacional, ou depende de ambas já estarem entregues por outras atividades?**

### Impacto da revisão

O escopo anterior de domínio/Application foi atendido no estado examinado. Esta revisão muda o foco para API e testa uma fronteira nova; reabre a decisão porque surgiram uma exigência explícita de autenticação (RF13) e a ausência de adapter/composição. Não invalida o desenho interno anterior.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Security | prioritized | Evitar cadastro de experiência sob identidade arbitrária | RF13 exige autenticação; mecanismo concreto não está evidenciado |
| Correctness | prioritized | Passar datas e proprietário corretos para o caso existente | Domínio e Application presentes; contrato HTTP não existe |
| Interoperability | prioritized | Integrar API ao caso existente por injeção | Padrão de `projeto_academico.py` e `factory.py` |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Simplicity | Não duplicar regra existente | Reutilizar o caso de uso e os value objects; não replicar validação na API |
| Testability | Unitários determinísticos sem serviço real | Handler chamado diretamente com executor real e repository/gerador doubles |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Security | Um cliente pode tentar cadastrar dados em nome de outro estudante | Alta | Estudantes e responsáveis pelo sistema |
| Correctness | Datas, campos ou vínculo de proprietário chegam inconsistentes | Média | Estudantes e consumidores dos currículos |
| Interoperability | Rota existe, mas executor não está ligado ou responde 503 | Média | Clientes da API e equipe |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Security | Dependência autenticada e teste do vínculo do ator elevam o escopo | Delivery-speed | Necessário diante de RF13 |
| Correctness | Conversão explícita das datas e erros tipados | Simplicity | Aceitável; reutiliza `Periodo` existente |
| Interoperability | Registro em factory e, se aplicável, adapter/migration | Delivery-speed | Aceitável somente se persistência operacional fizer parte do aceite |

## Riscos e efeitos de segunda ordem

- Copiar a rota de projeto sem autenticação perpetuaria uma lacuna existente em vez de atender RF13.
- Criar só router e DTO sem injetar executor torna a rota indisponível no app padrão; isso pode ser uma interface registrada sem cadastro funcional.
- Se persistência for adicionada sem alinhar limites de transação, erros do adapter podem escapar sem tradução adequada.
- Limites máximos arbitrários podem divergir do produto; não devem ser copiados sem decisão de requisitos.
- RF02 abrange consulta, edição e exclusão, mas UC04 descreve mais operações que o cadastro. Misturar tudo no card ampliaria escopo sem solicitação explícita.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| O card é somente exposição HTTP | Critérios de aceite do card confirmam rota e não exigem banco operacional | Revisar descrição/aceite do card | Exigência de persistência real muda a escolha para B |
| Há identidade autenticada confiável | Contrato existente que deriva `UsuarioId` da sessão | Revisão de API/auth e teste com principal controlado | Somente UUID do path/body implica bloqueio de liberação |
| Os dados e datas são convertidos corretamente | DTO e handler mantêm campos requeridos e `Periodo` válido | Testes unitários da requisição e handler | Data final anterior ao início aceita ou usuário divergente |
| O erro de domínio não persiste | Executor real com repositório spy | Teste unitário direto do endpoint | Spy registra entidade após erro |
| Endpoint está composto no app | Router registrado e executor efetivamente injetado na configuração-alvo | Teste unitário da factory/configuração | Endpoint retorna 503 na configuração que deveria operar |
| Migration/adapter fazem parte do card | Aceite define armazenamento durável e Code First | Revisão do card e arquitetura | Persistência durável é necessária e não está no escopo |

## Handoffs e atividades posteriores

- Produto/gestão do card: confirmar se persistência e composição operacional pertencem a este card.
- Segurança/API: identificar mecanismo autenticado que fornece o estudante da sessão e aplicar autorização de propriedade; não inferir mecanismo novo nesta análise.
- Backend, após destravar: implementar DTO/router/factory e testes unitários; se aplicável, implementar ORM, migration e adapter.
- Produto: definir limites de empresa, cargo e descrição caso sejam requisitos do contrato.
- Cards posteriores: consulta, edição e exclusão de experiência, caso permaneçam no escopo RF02.

## Síntese

A análise anterior já resultou em entidade, caso de uso, portas e testes de domínio/Application. O card atual deve focar a API e acrescentar testes unitários do handler, reutilizando o caso existente. Ainda não há decisão responsável sobre liberação: RF13 exige identidade autenticada, enquanto a implementação atual não evidencia esse vínculo; também falta confirmar se o card inclui persistência real, cujo adapter e migration não foram encontrados. Até esclarecer esses dois pontos, manter a decisão pendente e não publicar uma rota que aceite identidade arbitrária. Se autenticação e armazenamento estiverem garantidos por outras atividades, limitar o card à exposição HTTP injetável; se não, definir explicitamente os componentes faltantes no escopo.
