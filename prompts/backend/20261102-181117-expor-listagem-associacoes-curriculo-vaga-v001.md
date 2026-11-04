---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-11-02T18:11:17-03:00"
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
    - path: "code-alchemists-br/sistema-curriculo#244"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: whole-file
      locator: "título, descrição e critério de aceite"
      content_state: external
      revision: "consultada em 2026-11-02"
      availability: available
    - path: "Solicitação do usuário nesta sessão"
      relationship: primary
      representation: prose
      function: documentation
      format: mensagem
      analysis_scope: whole-file
      locator: null
      content_state: external
      revision: "2026-11-02"
      availability: available
    - path: "AGENTS.md"
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/AGENTS.md"
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "prompts/README.md"
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md"
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "escopo, contratos e handoffs relativos à #244"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "prompts/backend/20261019-191822-consulta-paginada-associacoes-estudante-v002.md"
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "escopo, testes e handoffs relativos à #244"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/application/consulta_associacao_curriculo_vaga.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/application/ports.py"
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioAssociacaoCurriculoVaga"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/domain/associacao_curriculo_vaga.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/infrastructure/persistence/sqlalchemy/repositorio_associacao_curriculo_vaga.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "listar_por_usuario"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/api/factory.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "assinatura de create_app e registro de routers"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/api/middleware_autenticacao.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ROTAS_PUBLICAS, request.state.usuario_id e dispatch"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/api/experiencia_profissional.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "_usuario_autenticado e criar_router"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/api/listagem_versoes_curriculo.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "DTOs e contrato de rota de listagem existente"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/api/vagas.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "uso de request.state e tradução de falha de composição"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/api/documentacao_openapi.py"
      relationship: supporting
      representation: source-code
      function: configuration
      format: Python
      analysis_scope: selected-section
      locator: "tags e segurança OpenAPI por cookie"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/main.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "fábrica de sessões e composição de create_app"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/infrastructure/persistence/sqlalchemy/acesso_estudante.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "adapter por chamada com async_sessionmaker"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/tests/test_api_vagas.py"
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "testes isolados da fronteira HTTP"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/tests/integracao_repositorio_associacao_curriculo_vaga.py"
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "src/backend/tests/fixtures/curriculos_autenticados_integracao.py"
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "banco temporário, sessão autenticada e requisição ASGI"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "docs/requisitos_funcionais.md"
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF12"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "docs/modelagem_der.md"
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "Associação currículo-vaga"
      content_state: commit
      revision: "103accf"
      availability: available
    - path: "docs/Arquitetura/ADR-002-autenticacao-autorizacao-propriedade.md"
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "autenticação, identidade e propriedade"
      content_state: commit
      revision: "103accf"
      availability: available
---

# Análise de decisão — Expor listagem paginada de associações currículo-vaga (#244)

## Solicitação original

> **Objetivo:** expor via HTTP a listagem de associações com currículo, vaga e classificações.
>
> Reutilizar o caso de uso `ListarAssociacoesCurriculoVaga` da #243, já integrado. Implementar somente a exposição HTTP, com DTO mínimo e composição conforme os padrões atuais. Obter a identidade do estudante pela sessão autenticada, nunca por identificador controlado pelo cliente. Garantir isolamento por proprietário, paginação, classificações corretas e tratamento de erros. Não inventar campos ou funcionalidades ausentes do modelo; preservar Clean Architecture, DDD, ports e adapters. Criar testes pertinentes de contrato HTTP, autenticação, autorização e paginação. Sem refatorações desnecessárias, mudanças de outras issues, formatação ampla ou documentos adicionais.
>
> Base informada: branch `feature/244-listagem-associacoes`, `dev` no commit `103accf`. A #243 está implementada e integrada. Nesta etapa: somente análise; aguardar aprovação para implementar.

## Informações complementares

- A issue #244 está aberta e seu critério solicita que a alteração seja verificável isoladamente, inclua testes pertinentes e seja revisável em cerca de dez minutos.
- A análise da #243 v001 delimitou explicitamente endpoints HTTP para a #244; a v002 acrescentou teste de persistência e também manteve a API fora do escopo.
- O repositório está na branch informada, com `HEAD` e `dev` em `103accf` e working tree limpa no momento da inspeção.
- A chamada atual de listagem já aceita `UsuarioId`, `offset` e `limit`. O filtro pelo proprietário, ordenação e busca de classificações estão no adapter existente.
- A solicitação não fixa URI, defaults de paginação, limite máximo, metadata de página nem detalhes de currículo/vaga. Esta análise recomenda não criar tais dados/políticas: exigir `offset` e `limit`, não impor teto novo, retornar apenas IDs existentes e classificações e omitir total/metadata que o caso de uso não calcula.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Análise da demanda | Nenhuma análise identificada para a #244 | Análise inicial v001 | A #243 direcionou a exposição HTTP para esta issue | Delimita rota e composição sem repetir o caso de uso |
| Estado do sistema | A #243 não fornecia resposta HTTP | A #243 está integrada em `dev` 103accf | A base declarada foi confirmada | Endpoint deve adaptar contratos existentes, não reimplementar consulta |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `code-alchemists-br/sistema-curriculo#244` | primary | prose | documentação | GitHub issue | título, descrição e aceite | externa, consultada em 2026-11-02 |
| Solicitação do usuário nesta sessão | primary | prose | documentação | mensagem | integral | externa, 2026-11-02 |
| `AGENTS.md`, `src/backend/AGENTS.md` | context | prose | prompt-instruction | Markdown | arquivos integrais | commit 103accf |
| `prompts/README.md` | context | prose | documentation | Markdown | arquivo integral | commit 103accf |
| `prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md` | supporting | prose | documentation | Markdown | escopo, contratos e handoffs da #244 | commit 103accf |
| `prompts/backend/20261019-191822-consulta-paginada-associacoes-estudante-v002.md` | supporting | prose | documentation | Markdown | escopo, testes e handoffs da #244 | commit 103accf |
| `src/backend/application/consulta_associacao_curriculo_vaga.py` | supporting | source-code | production | Python | caso de uso | commit 103accf |
| `src/backend/application/ports.py` | supporting | source-code | schema-contract | Python | port `RepositorioAssociacaoCurriculoVaga` | commit 103accf |
| `src/backend/domain/associacao_curriculo_vaga.py` | supporting | source-code | production | Python | agregado, enum e normalização | commit 103accf |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_associacao_curriculo_vaga.py` | supporting | source-code | production | Python | `listar_por_usuario` | commit 103accf |
| `src/backend/api/factory.py` | supporting | source-code | production | Python | injeção e inclusão de routers | commit 103accf |
| `src/backend/api/documentacao_openapi.py` | supporting | source-code | configuration | Python | tags e segurança OpenAPI por cookie | commit 103accf |
| `src/backend/api/middleware_autenticacao.py` | supporting | source-code | production | Python | rotas privadas e principal em `request.state` | commit 103accf |
| `src/backend/api/experiencia_profissional.py`, `src/backend/api/vagas.py` | supporting | source-code | production | Python | leitura de principal, validação e indisponibilidade | commit 103accf |
| `src/backend/api/listagem_versoes_curriculo.py` | supporting | source-code | production | Python | padrão de DTO/listagem e ressalva de identidade na URL | commit 103accf |
| `src/backend/main.py`, `src/backend/infrastructure/persistence/sqlalchemy/acesso_estudante.py` | supporting | source-code | production | Python | composição de runtime e adapter de sessão curta | commit 103accf |
| `src/backend/tests/test_api_vagas.py`, `src/backend/tests/integracao_repositorio_associacao_curriculo_vaga.py`, `src/backend/tests/fixtures/curriculos_autenticados_integracao.py` | supporting | source-code | test | Python | testes de fronteira, consulta SQL, sessão e ASGI | commit 103accf |
| `docs/requisitos_funcionais.md`, `docs/modelagem_der.md`, `docs/Arquitetura/ADR-002-autenticacao-autorizacao-propriedade.md` | context | prose | documentation | Markdown | RF12, modelo de associação e propriedade/autenticação | commit 103accf |

### Limites da evidência dos artefatos

A branch e o commit foram conferidos localmente. A issue apresenta descrição curta e não define a URI ou o schema HTTP. A análise anterior da #243 é evidência de fronteira, não uma especificação da #244. O DER e o agregado mostram IDs e classificações, mas não dados descritivos de vaga; a consulta existente devolve apenas agregados de associação. Nenhuma API de detalhes de vaga foi assumida.

## Problema enriquecido

### Resultado desejado

Permitir ao estudante consultar, por HTTP autenticado e em páginas, as associações entre seus currículos e vagas, juntamente com as classificações persistidas, usando o caso de uso já integrado na #243.

### Atores e interesses

- Estudante autenticado: consultar somente associações pertencentes aos próprios currículos.
- Cliente HTTP: obter um contrato pequeno, estável e paginável.
- Backend: preservar isolamento, integridade de classificações e fronteiras arquiteturais.

### Evidências e fatos observados

- `ListarAssociacoesCurriculoVagaEntrada` recebe `UsuarioId`, `offset` e `limit`; rejeita offset não inteiro/negativo e limit não inteiro/positivo.
- `RepositorioAssociacaoCurriculoVaga.listar_por_usuario` é a porta existente.
- O adapter SQLAlchemy filtra por `CurriculoRegistro.usuario_id`, ordena por `(curriculo_id, vaga_id)`, aplica offset/limit e carrega classificações dos pares devolvidos.
- `AssociacaoCurriculoVaga` só contém `curriculo_id`, `vaga_id` e classificações. Os valores do enum existentes são `interesse`, `compatibilidade` e `candidatura`; o domínio garante que candidatura implica interesse.
- O middleware valida a sessão, instala o UUID em `request.state.usuario_id` e protege todas as rotas que não estão em `ROTAS_PUBLICAS`. Endpoints podem obter o principal no request state, padrão usado por outras rotas.
- A fábrica `create_app` recebe executores opcionais e registra routers. O OpenAPI aplica o esquema de cookie às rotas privadas.
- `main.py` cria a fábrica de sessões do banco, compõe autenticação e injeta serviços em `create_app`; `AcessarEstudanteSqlAlchemy` demonstra o padrão de abrir sessão curta por chamada.
- Testes existentes da #243 exercitam isolamento/paginação no repositório, mas não cobrem o contrato HTTP nem sua composição com sessão autenticada.
- RF12 aprova as classificações e a associação manual; não define detalhes de paginação nem uma resposta HTTP.

### Hipóteses

- Um caminho sem UUID do estudante, sob `/estudantes/atual`, expressa a coleção própria e evita aceitar identidade do cliente.
- `offset` e `limit` serão query parameters inteiros obrigatórios, com offset não negativo e limit positivo, encaminhados sem transformação ao caso de uso. Isso evita inventar defaults, teto ou convenção global.
- A resposta será um objeto `{ "associacoes": [...] }`, seguindo o formato de listas já usado pela API, com `curriculo_id`, `vaga_id` e `classificacoes` apenas.
- Como classificações são expostas por conjunto imutável, a lista HTTP será serializada em ordem estável pelo valor textual. A regra de inclusão de interesse na candidatura permanece exclusivamente no domínio.
- A execução sem banco configurado manterá a indisponibilidade explícita; o router deverá responder 503 quando o executor não estiver composto.

### Perguntas em aberto

Nenhuma que impeça uma proposta mínima. Defaults e limite máximo não são definidos pelo requisito nem pelo caso de uso; a recomendação é não os inventar e exigir `offset`/`limit`. Se o produto quiser parâmetros opcionais ou teto de página, isso requer decisão explícita posterior.

### Escopo

- Adicionar adapter HTTP de listagem com DTOs mínimos e mapeamento do agregado para valores públicos.
- Obter a identidade somente de `request.state.usuario_id`.
- Registrar o router na fábrica, documentar sua tag e marcar a operação como protegida pelo esquema de sessão já existente.
- Compor o caso de uso com o repositório SQLAlchemy usando sessão de curta duração na entrada de runtime, seguindo o adapter por chamada já existente.
- Preservar filtragem pelo proprietário no repositório existente e erro explícito quando a composição não estiver disponível.
- Cobrir o contrato, principal, ausência de sessão, isolamento A/B, paginação, ordenação e classificações com testes unitários e HTTP integrado.

### Fora do escopo

- Alterar ou duplicar `ListarAssociacoesCurriculoVaga`, a porta, o agregado, a query de persistência ou migrations.
- Aceitar `usuario_id` da URL, query string ou corpo como identidade.
- Buscar título/dados do currículo, dados externos da vaga, score ou qualquer outro atributo não existente no agregado/caso de uso.
- Adicionar contagem total, links de navegação, cursor, defaults ou teto de paginação sem requisito.
- Alterar criação, atualização, remoção, histórico ou interface frontend da associação.
- Refatorar a autenticação/middleware ou modificar regras de outras issues.

### Critérios de sucesso

- GET autenticado é registrado na API sem UUID de estudante controlado pelo cliente e usa o principal validado da sessão como `UsuarioId` do caso de uso.
- Sem sessão válida, a rota responde 401; um parâmetro de identidade fornecido pelo cliente não altera o principal. Sem executor, responde 503.
- `offset` e `limit` são validados na fronteira; valores inválidos ou ausentes respondem 422 e parâmetros válidos chegam inalterados ao caso de uso.
- A resposta 200 inclui somente os três campos definidos pelo agregado; associações são ordenadas conforme retorno do caso de uso e classificações têm valores corretos e ordem determinística. Página vazia retorna coleção vazia.
- Um teste HTTP integrado com estudantes A/B comprova que uma sessão A nunca recebe associação de currículo B, inclusive em páginas sucessivas; filtro por dono ocorre antes da janela conforme implementação da #243.
- O router é composto no `create_app` e na entrada de runtime; aplicação sem persistência continua declarando ausência sem resposta de sucesso falsa.

## Restrições aplicáveis

- Clean Architecture: API transforma HTTP/DTOs; Application e Domain permanecem inalterados; persistência e lifecycle de sessão ficam em adapters/composição externa.
- DDD: não expor entidade de domínio diretamente nem replicar a invariância de classificação no controller.
- Segurança: confiar apenas na identidade instalada pelo autenticador e manter verificação de proprietário no backend.
- Não fazer migração: modelo e tabelas de associação/classificação já existem.
- Cada função, classe e DTO novo requer docstring equivalente explicando responsabilidade, fluxo e finalidade.
- Executar ferramentas do backend por Nix: testes unitários em `.#backend`; testes HTTP integrados em `.#tests`; Ruff restrito aos arquivos Python da tarefa no ambiente Nix que o disponibiliza (`.#quality`).
- Não criar commit, push ou PR.

## Classificação comentada

Esfera primária `engineering`, decisão de design e implementação local do backend. As preocupações são arquitetura, segurança e integração: o principal é expor uma consulta de negócio já existente; segurança trata o vínculo com sessão e proprietário como restrição de implementação, não amplia a funcionalidade.

## Decisão de roteamento

- Local selecionado: `prompts/backend`.
- Candidatas imediatas inventariadas: `backend`, `frontend`, `ambientes`, `requisitos`, `revisao` e `templates`.
- Confiança: alta.
- Justificativa: a decisão é sobre uma interface HTTP FastAPI e sua composição com Application/Infrastructure do backend. `prompts/README.md` confirma o destino. Não existe `AGENTS.md` nem `AGENTS.override.md` específico em `prompts`.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | alta | usar o use case e o contrato do agregado sem transformação semântica | impede inconsistência entre HTTP e domínio |
| security | alta | identidade autenticada e nenhuma associação alheia | os dados são privados por proprietário |
| simplicity | alta | DTO com somente IDs e classificações | evita contrato ou dependência externa novos |
| modifiability | média | manter composição e lifecycle de sessão nos adapters | conserva Clean Architecture |
| reliability | média | páginas estáveis, erros explícitos e sem falsa resposta de sucesso | protege cliente e operação |

## Alternativas consideradas

**A — Reutilizar um caminho com `/{usuario_id}` na URL, como a listagem de currículos existente.** Rejeitada: embora reaproveite um padrão de rota, conflita diretamente com a exigência desta issue e com ADR-002 de não confiar em identificadores do cliente.

**B — `GET /estudantes/atual/associacoes-curriculo-vaga`, com `offset` e `limit` obrigatórios.** Recomendada: comunica que a coleção pertence ao principal, não carrega UUID de usuário e se alinha ao caminho `/estudantes/atual` já existente. O router compõe o DTO e chama o use case; um adapter por chamada faz a sessão e a composição runtime.

**C — `GET /associacoes-curriculo-vaga`, também usando somente a sessão.** Viável e igualmente seguro se o principal vier do request state, mas expressa menos claramente a propriedade da coleção e não segue a forma local de endpoint de estudante atual.

Em qualquer alternativa viável, a resposta conterá os identificadores existentes do currículo e da vaga e os valores de classificação. Não inclui dados de currículo/vaga ausentes do agregado nem metadata sem suporte no caso de uso.

## Perfil de pagamento comparativo

Escala ordinal: `+2` melhora forte, `+1` melhora moderada, `0` neutro, `-1` piora moderada, `-2` piora forte. Valores comparam o efeito esperado, não são somados.

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| correctness | alta | -2 | +2 | +1 | alta | A aceita identidade que o requisito proíbe; B/C usam sessão |
| security | alta | -2 | +2 | +2 | alta | middleware autentica rotas privadas; handler encaminha principal |
| simplicity | alta | +1 | +1 | +2 | média | C usa rota mais curta; B mantém sentido de proprietário explícito |
| modifiability | média | 0 | +2 | +1 | média | B encaixa o padrão `estudantes/atual` e não altera rotas legadas |
| reliability | média | 0 | +2 | +1 | média | query validada na fronteira e repositório conserva filtro/ordem/página |

## Histórico e decisão atual

### Decisão da versão anterior

Não há análise anterior da #244. As análises v001/v002 da #243 decidiram a consulta da Application e do repositório e excluíram a exposição HTTP para esta issue.

### Decisão recomendada nesta versão

Implementar a alternativa B como adaptação, não como nova regra: criar router sob `/estudantes/atual/associacoes-curriculo-vaga`, exigir `offset` e `limit` válidos, ler `request.state.usuario_id` e chamar `ListarAssociacoesCurriculoVaga` com `UsuarioId`. Projetar o resultado para `{associacoes: [{curriculo_id, vaga_id, classificacoes}]}`; valores de enum são strings estáveis. Não incluir títulos, detalhes de vaga, total, defaults ou teto.

Na composição, acrescentar o executor injetável no `create_app` e registrar o router/tag. Para a aplicação de runtime, seguir `AcessarEstudanteSqlAlchemy`: um adapter de infraestrutura abre sessão curta por chamada, cria `RepositorioAssociacaoCurriculoVagaSqlAlchemy`, delega ao caso de uso existente e fecha a sessão. `main.py` injeta esse adapter somente quando a fábrica de sessões existir; sem banco, mantém o executor ausente e o 503 existente como semântica de indisponibilidade.

### Impacto da revisão

Não aplicável: primeira análise da issue. A decisão limita-se à borda HTTP e à composição necessária para executar a consulta integrada da #243.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| security | prioritized | sessão é a única fonte da identidade e o backend mantém o filtro do dono | middleware e adapter existente |
| correctness | prioritized | contrato HTTP projeta somente fatos existentes e preserva paginação da Application | caso de uso e agregado em 103accf |
| simplicity | prioritized | uma resposta mínima e nenhuma nova consulta, regra ou schema | campos disponíveis no agregado |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| isolamento | nenhuma associação de outro estudante na saída | principal da sessão chega ao use case, que consulta port filtrado por dono |
| paginação | página válida, ordenada e sem duplicar metadata inexistente | encaminhar offset/limit ao port e preservar ordem devolvida |
| minimização | resposta só com currículo_id, vaga_id e classificações | são os campos presentes no agregado |
| disponibilidade | sem persistência, erro explícito | executor ausente resulta em 503, sem fallback vazio |
| classificação | enum em strings estáveis, candidatura inclui interesse | projeção do agregado respeita valores e normalização existentes |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| security | consulta de dados privados com identidade controlada pelo cliente ou vazamento entre estudantes | alta | estudantes e operadores |
| correctness | API deixa de representar as classificações persistidas ou a página pedida | média | cliente e estudante |
| simplicity | DTO agrega detalhes não disponíveis ou repete dados já consultados | média | consumidores e manutenção |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| segurança e lifecycle correto | criar adapter de sessão curta e registrá-lo em `main.py` | mais um ponto de composição | aceitável, segue adapter existente e habilita a rota real |
| contrato simples | consumidor envia ambos `offset` e `limit`; sem total embutido | conveniência do cliente | aceitável enquanto não há defaults ou contagem aprovados |
| serialização determinística | ordenar strings de classificação na resposta | preservação da ordem interna do conjunto | aceitável: conjunto não possui ordem contratual |

## Riscos e efeitos de segunda ordem

- Uma rota documentada apenas na fábrica, sem o adapter injetado no `main.py`, responderia 503 no runtime com banco disponível; a composição runtime faz parte desta proposta.
- Não existe teto de `limit` definido. A proposta não inventa um, mas um cliente pode solicitar página grande; se o produto exigir proteção por máximo, decidir e validar esse limite separadamente.
- Adicionar `usuario_id` como query param, mesmo ignorado, não deve ser documentado nem encaminhado; os testes devem demonstrar que só o principal prevalece.
- Ordem de uma coleção de classificações não é fornecida pelo agregado. Serialização deve ordenar pelos valores do enum para evitar resposta variável.
- Dados externos da vaga podem não estar mais disponíveis; a listagem não deve consultar o Grupo 2 nem fabricar detalhes ausentes.
- Exceções inesperadas de persistência devem continuar visíveis como erro de servidor; não adicionar catch-all nem resposta vazia de sucesso.
- Caso a aceitação exija que `main.app` responda à listagem sem `DATABASE_URL`, isso conflita com a política existente de indisponibilidade explícita e requer decisão adicional.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Rota usa identidade autenticada | entrada observada contém `UsuarioId` do middleware, sem argumento de usuário do cliente | teste unitário do router e HTTP com sessão | qualquer origem do usuário fora de `request.state` |
| Sem sessão não há acesso | request sem cookie chega a 401 antes do use case | teste HTTP integrado | executor chamado sem sessão válida |
| Isolamento e paginação permanecem corretos no HTTP | dados A/B e páginas consecutivas em banco descartável | chamada ASGI com autenticação persistida e adapter real | associação de B aparece para A ou linha de B desloca página A |
| Contrato HTTP é mínimo e estável | JSON contém só campos aprovados, enums corretos e página vazia | assertions de resposta e OpenAPI | campo sem modelo ou ausência de classificação persistida |
| Erros de entrada/composição são explícitos | inválidos 422, ausência de principal 401 e executor ausente 503 | testes de fronteira | valor inválido chega ao caso de uso ou falha vira lista vazia |
| Adapter runtime não mantém sessão global | sessão criada/fechada por chamada | teste unitário do adapter e integração HTTP | sessão compartilhada entre chamadas ou não fechada |

## Handoffs e atividades posteriores

- Aguardar aprovação explícita desta versão proposta antes de implementar.
- Implementação: adapter HTTP e DTO; composição em `api/factory.py`, documentação OpenAPI e `main.py`; executor SQLAlchemy por chamada, sem alteração no caso de uso ou repository.
- Testes unitários da API e do executor: ambiente `nix develop .#backend`.
- Teste HTTP integrado de contrato, autenticação, proprietário e paginação com banco local descartável: ambiente `nix develop .#tests`, reutilizando a fixture de sessão/ASGI existente.
- Ruff limitado aos arquivos Python da mudança, via ambiente Nix de qualidade.
- Não há handoff para frontend, migrations, mudança de domínio ou padronização global de paginação.

## Síntese

A #244 deve expor a consulta já implementada pela #243 sem refazer Application ou persistência. A rota recomendada usa o caminho de estudante atual, obtém identidade exclusivamente da sessão e delega filtro de proprietário e paginação ao caso de uso existente. O DTO expõe somente os IDs presentes no agregado e suas classificações; não inclui detalhes de currículo/vaga nem contagem inexistente. Para que a rota funcione no runtime, a composição deve abrir uma sessão curta por chamada, seguindo o adapter SQLAlchemy já usado pelo acesso. O contrato de paginação exige offset e limit e não inventa teto. A decisão é `proposed` e aguarda aprovação.
