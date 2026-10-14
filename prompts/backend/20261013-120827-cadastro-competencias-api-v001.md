---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-13T12:08:27-03:00"
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
    - path: src/backend/domain/itens_perfil.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "protocolos de repositório e gerador de ID, linhas 185–258"
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: src/backend/application/cadastro_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: src/backend/api/experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/metadata.py
      relationship: supporting
      representation: source-code
      function: configuration
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261012_0005_criar_experiencias_profissionais.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: mermaid-markdown
      analysis_scope: selected-section
      locator: "entidade COMPETENCIA e relações com USUARIO e CURRICULO_COMPETENCIA"
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF01–RF04"
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Problema enriquecido e escopo sobre itens reutilizáveis"
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "A decisão define domínio, Application, persistência SQLAlchemy, migration e interface HTTP do backend; requisitos apenas fornecem contexto funcional."
classification:
  sphere: engineering
  concerns: [domain, architecture, data]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — Cadastro de competências técnicas e comportamentais pela API

## Solicitação original

> Faça a análise para implementar no backend o cadastro de competências técnicas e comportamentais pela API. Deve incluir o endpoint de criação, validação do payload, conversão para DTO/comando, chamada do caso de uso, persistência por meio do repositório e resposta HTTP apropriada — sem expor entidades de domínio. Também precisa de testes unitários cobrindo o fluxo e suas regras, como dados obrigatórios e possíveis duplicidades.

## Informações complementares

Nenhum identificado.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem | Nenhuma | v001 | Análise inicial | Não há revisão a comparar. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/domain/itens_perfil.py` | Principal | Código-fonte | Produção | Python | Arquivo completo | Working tree baseado em `376eb7d` |
| `src/backend/application/ports.py` | Principal | Código-fonte | Produção | Python | Protocolos análogos | Working tree baseado em `376eb7d` |
| `src/backend/application/cadastro_experiencia_profissional.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree baseado em `376eb7d` |
| `src/backend/api/experiencia_profissional.py` e `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Arquivos completos | Working tree baseado em `376eb7d` |
| `src/backend/infrastructure/persistence/sqlalchemy/experiencia_profissional.py` e `repositorio_experiencia_profissional.py` | Apoio | Código-fonte | Produção | Python | Arquivos completos | Working tree baseado em `376eb7d` |
| `src/backend/infrastructure/persistence/sqlalchemy/metadata.py` e migration `20261012_0005_criar_experiencias_profissionais.py` | Apoio | Código/configuração | Contrato de schema | Python | Arquivos completos | Working tree baseado em `376eb7d` |
| `docs/modelagem_der.md` | Apoio | Modelo de diagrama | Contrato de schema | Mermaid/Markdown | Competência e relações | Working tree baseado em `376eb7d` |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF01–RF04 | Working tree baseado em `376eb7d` |
| `prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md` | Contexto | Prosa | Documentação | Markdown | Limites dos itens de perfil | Working tree baseado em `376eb7d` |

### Limites da evidência dos artefatos

O DER prevê apenas `descricao` e `nivel` para competência, sem categoria e sem unicidade. Nenhum requisito define vocabulário de níveis, tamanho dos campos ou a equivalência que caracteriza duplicidade. A solicitação, porém, exige distinguir competências técnicas e comportamentais e tratar duplicidades; a decisão abaixo explicita hipóteses mínimas e deve ser revisada se o produto definir taxonomia ou política diferente.

## Problema enriquecido

### Resultado desejado

Permitir que o estudante autenticado registre uma competência reutilizável, técnica ou comportamental, com descrição e nível válidos. A criação deve devolver uma representação HTTP pública, persistir o item em tabela própria e impedir repetição semântica da mesma competência para o mesmo proprietário.

### Atores e interesses

- O estudante precisa registrar habilidades que poderá reutilizar em versões de currículo.
- A API precisa aceitar somente formato válido e obter o proprietário da autenticação, não do corpo ou da rota controlável pelo cliente.
- O domínio precisa preservar campos obrigatórios e a classificação técnica/comportamental sem depender de HTTP ou ORM.
- A Application precisa coordenar geração de identidade, regra de duplicidade e persistência por portas.
- A infraestrutura precisa garantir a unicidade também sob concorrência.

### Evidências e fatos observados

- `Competencia` já existe como entidade imutável com `CompetenciaId`, `UsuarioId`, `descricao` e `nivel`, mas não valida seus textos e não registra categoria.
- Não há caso de uso, porta, adapter, tabela, migration, endpoint ou teste de cadastro de competência.
- O DER prevê que `USUARIO` possua muitas competências e que uma competência possa ser referenciada por currículo.
- RF01 exige o cadastro de competências; a jornada de informações complementares prevê inclusão de habilidades.
- O fluxo mais recente de experiência usa `POST /experiencias-profissionais`, principal autenticado em `request.state.usuario_id`, entrada de Application, executor injetado, DTO de resposta e `201`; este é o padrão mais atual e seguro disponível.
- O adapter de experiência separa registro SQLAlchemy, conversões puras e repositório com `flush`, enquanto a migration cria a tabela a partir do modelo Code First.

### Hipóteses

- `categoria` é obrigatória e tem somente `tecnica` ou `comportamental`; sem ela, a solicitação não teria representação persistível nem resposta verificável.
- `descricao` e `nivel` são textos obrigatórios; o nível permanece texto livre enquanto não houver vocabulário de produto aprovado.
- Duas competências são duplicadas quando pertencem ao mesmo estudante e têm a mesma categoria e descrição normalizada por remoção das extremidades, redução de espaços internos e comparação sem distinção de maiúsculas/minúsculas. O nível não diferencia competências distintas.
- A rota utilizará a autenticação já disponibilizada pelo middleware e seguirá o padrão de experiência, em vez de aceitar `usuario_id` controlado pelo cliente.

### Perguntas em aberto

- O produto deseja categorias adicionais, múltiplas categorias por competência ou uma taxonomia administrável?
- A equivalência de duplicidade deve ignorar acentos e pontuação, além de caixa e espaços?
- Quais limites máximos de descrição e nível atendem UI, banco e integrações?
- A composição de produção já dispõe de sessão/Unidade de Trabalho para injetar o novo repositório no app ASGI, ou esta entrega continuará expondo 503 quando o executor não for composto?

### Escopo

- Evoluir o modelo de domínio de competência com categoria explícita e invariantes de textos obrigatórios.
- Criar comando/DTO interno, caso de uso, porta de repositório e gerador de `CompetenciaId`.
- Criar modelo SQLAlchemy, mapeadores, repositório, registro na metadata e migration Code First para `competencias`.
- Expor `POST /competencias`, com payload validado, principal autenticado, `201`, DTO de resposta e traduções seguras de erro.
- Impor e testar a duplicidade por proprietário, categoria e descrição normalizada, inclusive com restrição única no banco.
- Cobrir domínio, Application, API e adapter com testes unitários isolados.

### Fora do escopo

- Listar, editar, excluir ou selecionar a competência em uma versão de currículo.
- Alterar a política de autenticação ou confiar em `usuario_id` no payload/rota.
- Criar categorias além de técnica e comportamental, sugestão automática, IA ou classificação por texto livre.
- Definir uma taxonomia de níveis, endpoints públicos, migração de dados inexistentes ou testes de integração/E2E.

### Critérios de sucesso

- Um POST autenticado válido cria e responde `201` com `id`, `descricao`, `nivel` e `categoria`, sem serializar a entidade de domínio.
- Payload ausente, tipo/categoria inválidos ou campo obrigatório vazio não alcançam persistência e recebem erro de cliente apropriado (`422`).
- Duplicidade semântica para o mesmo estudante recebe `409`; a mesma descrição para outro estudante ou outra categoria permanece permitida.
- A Application depende somente de domínio e portas; ORM, sessão e FastAPI ficam fora dela e do domínio.
- A tabela possui FK para usuário e unicidade equivalente à regra de duplicidade; o adapter faz `flush`, não `commit`.
- Os testes são unitários, determinísticos e executáveis no ambiente Nix de backend.

## Restrições aplicáveis

- Clean Architecture e DDD do repositório: o domínio não depende de API, ORM ou banco; Application não depende de Infrastructure ou API; a composição fica na camada externa.
- Persistência relacional é Code First, com modelo SQLAlchemy, migration versionada e mapeamento na infraestrutura.
- A API não expõe entidade de domínio; recebe DTO HTTP e converte para comando/entrada da Application.
- Invariantes ficam próximas ao modelo: a entidade valida texto/categoria; duplicidade entre registros é coordenada pelo caso de uso através do repositório e reforçada no banco.
- Todas as funções, classes e DTOs novos exigem docstrings que expliquem o que fazem, como fazem e sua finalidade.
- Testes unitários do backend devem usar `nix develop .#backend`.

## Classificação comentada

É uma decisão de engenharia de componente, com preocupações de domínio (conceito e invariantes de competência), arquitetura (fronteiras entre HTTP, Application e persistência) e dados (tabela e unicidade). O risco é médio: o fluxo é análogo ao de experiência, mas categoria e equivalência de duplicidade ainda não são requisitos detalhados.

## Decisão de roteamento

`prompts/backend` é o destino escolhido porque a análise orienta mudanças em Domain, Application, API, infraestrutura SQLAlchemy e migration. `prompts/requisitos` foi considerada por conter RF01, mas não é o objeto principal da decisão.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| correctness | Alta | Priorizar | Campos, categoria, proprietário e unicidade devem representar a regra sem ambiguidades. |
| security | Alta | Satisfazer | A identidade deve vir do principal autenticado; duplicidade não pode vazar dados de outro usuário. |
| modifiability | Alta | Priorizar | O fluxo precisa manter portas e adapters substituíveis para evoluir níveis e categorias. |
| reliability | Média | Satisfazer | A regra de unicidade precisa sobreviver a requisições concorrentes. |
| simplicity | Média | Priorizar | Um recurso e tabela próprios evitam uma generalização prematura. |
| delivery-speed | Média | Satisfazer | Reusar o padrão de experiência reduz incerteza e torna testes locais diretos. |

## Alternativas consideradas

**Alternativa A — Recurso de competência próprio, categoria explícita, chave normalizada e repositório dedicado (recomendada).** Criar `CategoriaCompetencia` (por exemplo, `StrEnum` ou value object), evoluir `Competencia`, criar `CadastrarCompetenciaEntrada`, `CadastrarCompetencia`, `RepositorioCompetencia` e `GeradorCompetenciaId`. O repositório consulta a chave normalizada, persiste o registro SQLAlchemy `competencias` e o banco garante `UNIQUE(usuario_id, categoria, descricao_normalizada)`. A rota `POST /competencias` obtém `usuario_id` de `request.state`, converte o DTO e responde com DTO público. É coerente com o modelo e com o fluxo autenticado atual.

**Alternativa B — Recurso próprio, mas sem categoria e sem unicidade persistida.** Reutiliza os campos já presentes (`descricao`, `nivel`) e deixa a duplicidade para futura edição/listagem. É menor no curto prazo, mas não representa a distinção técnica/comportamental pedida nem cumpre o critério de possíveis duplicidades; falha o limiar de correção.

**Alternativa C — Tabela/repositório genérico para todos os itens complementares.** Modela competência, idioma, curso, certificação e links como registros genéricos com JSON ou tipo discriminado. Pode parecer reaproveitável, mas cada item tem campos, regras e operações distintas, enquanto os próximos contratos ainda não foram definidos. Introduz acoplamento e migração complexa sem benefício demonstrado; viola a preferência de não antecipar abstrações.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| correctness | Alta | +2 | -2 | 0 | Alta | Solicitação exige categoria e duplicidade; DER e entidade identificam competência como item próprio. |
| security | Alta | +1 | 0 | 0 | Média | Padrão autenticado de experiência fornece proprietário confiável; a regra de duplicidade é por usuário. |
| modifiability | Alta | +2 | -1 | -1 | Alta | Portas e adapters existentes seguem separação por conceito; generalização mistura evoluções independentes. |
| reliability | Média | +2 | -2 | +1 | Média | Índice único protege corrida; ausência de restrição não a protege. |
| simplicity | Média | +1 | +2 | -2 | Alta | A é uma extensão direta do padrão; C amplia prematuramente o modelo. |
| delivery-speed | Média | +1 | +2 | -2 | Média | B remove trabalho essencial; A reaproveita padrões e C exige desenho transversal. |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma — análise inicial.

### Decisão recomendada nesta versão

Adotar a Alternativa A. Implementar competência como recurso de perfil dedicado e autenticado, com `categoria` explícita (`tecnica` ou `comportamental`), `descricao` e `nivel` obrigatórios. A entidade deve validar os campos de valor local; o caso de uso deve construir uma chave canônica de descrição, consultar a porta de repositório e falhar com exceção de Application `CompetenciaJaCadastrada` antes de salvar. O adapter deve ainda traduzir violação da restrição única na gravação para a mesma falha, protegendo a corrida entre consulta e `flush`.

O endpoint recomendado é `POST /competencias`. Seu DTO deve aceitar somente `descricao`, `nivel` e `categoria`; extrair o proprietário de `request.state.usuario_id`; converter para `CadastrarCompetenciaEntrada`; e devolver `CompetenciaResposta` com UUIDs simples e campos públicos. A ausência de principal deve resultar em `401`, executor não composto em `503`, violação de payload/domínio em `422`, duplicidade em `409` e sucesso em `201`.

A tabela `competencias` deve conter `id`, `usuario_id` (FK), `categoria`, `descricao`, `descricao_normalizada` e `nivel`. `descricao_normalizada` é detalhe de persistência e de verificação, não parte da resposta HTTP. A migration deve ser gerada/versionada a partir do mapeamento Code First e a metadata deve importar o registro. O gerador UUID4 existente só atende `CurriculoId`; criar gerador análogo específico para `CompetenciaId` em vez de retornar identidade do tipo errado.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | Representação inequívoca de tipo e ausência de duplicata por proprietário. | Solicitação e RF01; categoria é hipótese explícita necessária. |
| modifiability | prioritized | Mudanças futuras de nível/categoria não atravessam HTTP, ORM e domínio indiscriminadamente. | Fronteiras e padrão de Application/adapter existente. |
| reliability | prioritized | Requisições concorrentes não criam duplicatas lógicas. | Chave única no banco complementa consulta pela porta. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| security | Identidade não é controlada pelo cliente e erro não revela dados alheios. | Rota usa principal do middleware; conflito é genérico e delimitado ao próprio usuário. |
| simplicity | Não criar modelo genérico antes de existirem regras comuns comprovadas. | Uma entidade/tabela/repositório por competência reaproveita o padrão já existente. |
| delivery-speed | Fluxo pode ser desenvolvido e testado sem banco ou servidor nos testes unitários. | Doubles em domínio/Application/API e `AsyncSession` mockada no adapter. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | Competências técnicas e comportamentais ficam indistintas ou duplicadas no mesmo perfil. | Alta | Estudantes, prévia e exportação futuras. |
| reliability | Duas requisições simultâneas podem criar registros equivalentes. | Média | Estudantes e manutenção de dados. |
| security | Um cliente poderia cadastrar em nome de outro usuário se o dono viesse do payload/rota. | Alta | Todos os estudantes. |
| modifiability | ORM/API passam a conter regra de domínio, elevando custo de evolução. | Média | Equipe de backend. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness e reliability | Campo técnico de chave normalizada, consulta extra e índice único. | simplicity | Aceitável: elimina ambiguidade e corrida sem expor o campo. |
| modifiability | Novos protocolo, DTOs, mapeadores e testes. | delivery-speed | Aceitável: são fronteiras requeridas pelo escopo e seguem padrão existente. |
| security | Rota depende do middleware e pode responder 401/503 até a composição estar disponível. | delivery-speed | Aceitável: evita contrato inseguro por `usuario_id` do cliente. |

## Riscos e efeitos de segunda ordem

- Categoria binária pode precisar de migração se o produto introduzir outras classificações; usar valores textuais controlados reduz a migração de tipo, mas não dispensa revisão da regra.
- Normalização sem remover acentos ou pontuação pode permitir variantes que a equipe considere duplicadas; normalização agressiva, por outro lado, pode colapsar nomes legítimos. A política deve ser confirmada antes de ampliar a equivalência.
- Uma restrição única exige que o adapter reconheça a violação específica sem transformar indisponibilidade do banco em falso conflito; erros não identificados devem propagar para o tratamento operacional, não virar `409`.
- A tabela habilita o futuro adapter de `ConsultaProprietarioItem` e prévia para competências, mas esses comportamentos não devem ser incluídos nesta atividade.
- A `create_app()` atual recebe executores prontos e o `main.py` não compõe sessão/repositório; criar a rota não garante persistência no processo ASGI padrão até que a composição externa seja resolvida.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Categoria binária é suficiente | Aprovação do responsável de produto ou wireframe/contrato atualizado. | Revisão de requisito antes de codificar enum. | Necessidade de categoria múltipla ou terceira categoria. |
| Chave de duplicidade é adequada | Casos com caixa/espaços e categorias distintas aprovados. | Testes unitários de caso de uso e adapter. | Produto considerar variações com acento/pontuação iguais ou diferentes. |
| Fronteiras preservam arquitetura | Imports e testes demonstram domínio/Application sem FastAPI ou SQLAlchemy. | Testes unitários e inspeção de dependências no ambiente Nix. | ORM/HTTP aparecerem em módulos internos. |
| Persistência é atômica | Migration e modelo possuem FK e índice único; adapter traduz somente conflito reconhecido. | Testes de mapeamento/repositório com sessão mockada e teste de migration posterior. | Duas execuções concorrentes resultarem em mais de um registro. |
| Contrato HTTP é seguro | Testes da rota verificam principal autenticado, 401, 409, 422, 503 e 201. | Chamada direta do handler com doubles, como em experiência. | Rota aceitar ou refletir `usuario_id` do cliente. |

## Handoffs e atividades posteriores

- Confirmar com produto a taxonomia de categoria, limites de tamanho e equivalência final de duplicidade antes da implementação.
- Compor `CadastrarCompetencia` com sessão, repositório e gerador no ponto externo que criar a aplicação, caso a meta seja habilitar persistência no `main.py` e não apenas disponibilizar a rota injetável.
- Depois do cadastro, implementar listagem/edição/exclusão e integrar a competência ao adapter real de consulta de itens de perfil, em cards separados.
- Executar migration e testes de integração no ambiente `tests` quando houver infraestrutura de banco destinada a esse nível; esta análise não autoriza essa execução.

## Síntese

O cadastro deve ser uma fatia vertical de backend dedicada a `Competencia`, não uma generalização dos itens complementares. A decisão recomenda categoria explícita, invariantes locais, deduplicação por proprietário com chave canônica e garantia única no banco, além de rota autenticada que converte DTO para comando e devolve DTO público. A principal incerteza é a política de produto para categoria e equivalência de duplicidade; ela é isolada para validação antes de codificar.
