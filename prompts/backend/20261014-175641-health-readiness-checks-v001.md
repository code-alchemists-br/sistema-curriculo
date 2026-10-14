---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-14T17:56:41-03:00"
lineage:
  mode: initial
  root: null
  supersedes: null
  change_type: initial
  secondary_change_types: []
  decision_impact: initial
subjects:
  kind: file-set
  files:
    - path: src/backend/api/factory.py
      relationship: primary
      representation: code
      function: entry-point
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/middleware_autenticacao.py
      relationship: primary
      representation: code
      function: middleware
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py
      relationship: supporting
      representation: code
      function: persistence
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/ambientes]
  confidence: high
  rationale: "Trata-se de endpoints HTTP e checagem de conectividade de persistência pertencentes ao backend para observabilidade e prontidão operacional."
classification:
  sphere: engineering
  concerns: [observability, reliability, architecture]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: time-critical
  uncertainty: low
  reversibility: easy
  risk: low
---

# Análise de decisão — Endpoints de Health Check e Readiness Check do Backend

## Solicitação original

Implementar os endpoints de Health Check (issue #178 - [F2.5]) e Readiness Check (issue #179 - [F2.6]) do backend seguindo rigorosamente a Clean Architecture, o AGENTS.md e o GUIA-DE-USO-DAS-SKILLS-v001.md:
1. Gerar a análise de decisão versionada em prompts/backend/ usando o fluxo da skill $decision-analysis-v4.
2. Criar a rota GET /health sem expor dados sensíveis ou detalhes de ambiente, retornando 200 OK.
3. Criar a rota GET /ready validando a conectividade com a persistência (query leve assíncrona no SQLAlchemy) e retornando 503 Service Unavailable em caso de falha de banco.
4. Implementar testes unitários para ambas as rotas usando doubles/mocks conforme as regras do repositório.
5. Garantir que todas as docstrings sigam o formato obrigatório (o que faz, como faz, qual finalidade atende).
6. Validar a execução da suíte de testes e o linter ruff no ambiente Nix (nix develop .#backend).

## Informações complementares

- Issue #178: "[F2.5] Criar health check sem dados sensíveis para dependências da aplicação." (WBS: 1.2.2.4, 1.7.2.1–1.7.2.3, 1.8.1.4).
- Issue #179: "[F2.6] Criar readiness check que falha quando a persistência não estiver disponível." (WBS: 1.2.2.4, 1.7.2.1–1.7.2.3, 1.8.1.4).
- Regra de Clean Architecture do `src/backend/AGENTS.md`: a camada de API não deve depender diretamente de classes concretas de banco de dados nem introduzir vazamento de dados de infraestrutura ou ambiente.
- O `MiddlewareAutenticacaoSessao` em `src/backend/api/middleware_autenticacao.py` intercepta requisições privadas; endpoints de sondagem operacional (`/health` e `/ready`) devem ser explicitamente públicos.

## Mudanças desde a versão anterior

Nenhum — versão inicial da análise.

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/api/factory.py` | Primária | Código | Composição ASGI | Python | Linhas 1 a 149 | Working tree |
| `src/backend/api/middleware_autenticacao.py` | Primária | Código | Middleware Auth | Python | Linhas 1 a 102 | Working tree |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py` | Apoio | Código | Persistência | Python | Linhas 1 a 69 | Working tree |

### Limites da evidência dos artefatos

Os arquivos foram examinados integralmente no working tree atual. O middleware de autenticação define `ROTAS_PUBLICAS` de forma explícita via `frozenset`. A fábrica `create_app` orquestra a injeção de dependências e a adição de rotas por meio de funções `criar_router_*`.

## Problema enriquecido

### Resultado desejado
Prover duas sondas HTTP operacionais desacopladas e seguras:
1. `GET /health` (Liveness): confirma que o processo web está ativo e apto a processar requisições, devolvendo `200 OK` e `{"status": "ok"}` sem detalhes internos de ambiente ou infraestrutura.
2. `GET /ready` (Readiness): confirma que a aplicação possui conectividade com a camada de persistência através de um contrato injetável e teste leve (`SELECT 1`). Devolve `200 OK` e `{"status": "ready"}` em caso positivo, ou `503 Service Unavailable` em caso de falha de conexão ou ausência de serviço.

### Atores e interesses
- **Orquestradores de Infraestrutura / Probes (Kubernetes, Docker, Load Balancer):** necessitam saber se o container pode receber tráfego (`/ready`) ou se deve ser reiniciado (`/health`).
- **Segurança da Informação:** exige que nenhuma informação confidencial (nomes de banco, credenciais, host, versões internas de pacotes ou variáveis de ambiente) seja exposta na resposta.
- **Desenvolvedores e Testes:** necessitam testar ambas as rotas de forma isolada, determinística e sem dependência de banco de dados real em testes unitários.

### Evidências e fatos observados
1. Atualmente, o backend não possui rotas de `/health` ou `/ready` registradas.
2. Todas as rotas não listadas em `ROTAS_PUBLICAS` sofrem interceptação pelo `MiddlewareAutenticacaoSessao`, retornando `401 Unauthorized` se não houver cookie de sessão válido.
3. O padrão de Clean Architecture do backend exige que routers de API recebam dependências tipadas via `Protocol`, tornando o roteador testável com doubles em memória.

### Hipóteses
- Uma query SQL simples (`SELECT 1`) executada assincronamente via `AsyncSession` é suficiente e segura para validar a disponibilidade do banco relacional sem sobrecarregar o pool de conexões.
- Sondas operacionais não devem exigir autenticação de sessão.

### Perguntas em aberto
Nenhuma identificada. Os critérios da WBS e dos cards #178 e #179 são objetivos.

### Escopo
- Criação de `src/backend/api/health.py` contendo o protocolo `VerificadorConectividadePersistencia`, DTOs de resposta e o roteador `criar_router(verificador_conectividade: VerificadorConectividadePersistencia | None) -> APIRouter`.
- Adição de `("GET", "/health")` e `("GET", "/ready")` em `ROTAS_PUBLICAS` em `src/backend/api/middleware_autenticacao.py`.
- Integração do novo roteador na fábrica `src/backend/api/factory.py` recebendo opcionalmente o verificador de persistência.
- Implementação do adaptador concreto `VerificadorConectividadePersistenciaSqlAlchemy` em `src/backend/infrastructure/persistence/sqlalchemy/verificador_conectividade.py` que executa `SELECT 1` assincronamente.
- Testes unitários cobrindo `/health` (200), `/ready` com sucesso (200), `/ready` com falha (503) e `/ready` sem verificador (503).

### Fora do escopo
- Implementação de métricas Prometheus ou telemetria OpenTelemetry.
- Alteração de regras de negócio, tabelas ou migrações do Alembic.
- Criação de testes de integração ponta a ponta com banco real (pertencem à skill `$integration-system-testing-v1`).

### Critérios de sucesso
1. `GET /health` responde `200` com `{"status": "ok"}` e nenhuma informação sensível.
2. `GET /ready` responde `200` com `{"status": "ready"}` quando o banco responde.
3. `GET /ready` responde `503` com `{"detail": "Persistência indisponível."}` quando o banco falha ou o verificador está ausente.
4. Requisições em `/health` e `/ready` não exigem autenticação mesmo com o middleware de sessão ativo.
5. 100% de conformidade com as docstrings explicativas e testes unitários passando no Nix.

## Restrições aplicáveis

- **AGENTS.md (Root):** Execução de testes e linters obrigatoriamente via `nix develop .#backend`.
- **src/backend/AGENTS.md:** Clean Architecture; o domínio e a API não devem se acoplar a implementações concretas de infraestrutura; docstrings completas (o que faz, como faz, qual finalidade atende).
- **GUIA-DE-USO-DAS-SKILLS-v001.md:** A implementação da camada transversal/borda é governada pela skill de Cross-Cutting.

## Classificação comentada

- **Esfera primária:** `engineering` — construção técnica de mecanismos de observabilidade operacional.
- **Preocupações:** `observability`, `reliability`, `architecture` — endpoints de integridade de sistema que suportam a resiliência da aplicação.
- **Tipo de decisão:** `design` — definição da fronteira arquitetural entre o router FastAPI e a sonda de persistência.
- **Risco:** `low` — alteração aditiva com impacto mínimo nas rotas funcionais existentes.

## Decisão de roteamento

- **Pasta escolhida:** `prompts/backend`
- **Pastas consideradas:** `prompts/backend`, `prompts/ambientes`
- **Justificativa:** Trata-se de código de aplicação e infraestrutura Python localizado em `src/backend/api` e `src/backend/infrastructure`.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `simplicity` | Alta | Máxima simplicidade | Health checks devem ser leves e sem chances de falha interna não tratada |
| `security` | Alta | Zero vazamento de segredos | Atende ao requisito da issue #178 de não vazar dados de ambiente |
| `modifiability` | Média | Desacoplamento via Protocol | Permite testar o router sem levantar um PostgreSQL/SQLite real |
| `reliability` | Alta | Detecção precisa de falha | Readiness deve acusar prontamente indisponibilidade do banco (503) |

## Alternativas consideradas

### Alternativa A: Endpoints de `/health` e `/ready` isolados em `api/health.py` com abstração `VerificadorConectividadePersistencia` (Recomendada)
Cria um roteador dedicado em `api/health.py`. O endpoint `/ready` depende exclusivamente de um `Protocol` assíncrono. Em `infrastructure/persistence/sqlalchemy/` implementa-se o adaptador com `AsyncSession`. A fábrica `create_app` expõe o parâmetro opcional.

### Alternativa B: Acoplamento direto com a sessão SQLAlchemy no router FastAPI
O router recebe diretamente um `AsyncSession` ou `sessionmaker` do SQLAlchemy e executa `session.execute(text("SELECT 1"))` no próprio handler HTTP.
*Inviável:* Viola a Clean Architecture do `src/backend/AGENTS.md`, acoplando o router de transporte à biblioteca de persistência e dificultando testes unitários rápidos.

### Alternativa C: Rota única `/health` acumulando checagem de banco e sistema
Cria apenas `/health` e falha se o banco estiver fora.
*Inviável:* Viola a separação exigida pelas issues distintas #178 (liveness/dependências gerais) e #179 (readiness da persistência). Se a aplicação estiver iniciando o banco, o orquestrador mataria o container prematuramente.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A (Protocol desacoplado) | Alternativa B (Acoplamento direto) | Alternativa C (Rota única) | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `simplicity` | Alta | +1 | +2 | +1 | Alta | Clean Architecture vs código procedural |
| `security` | Alta | +2 | +1 | +2 | Alta | Sem vazamento de detalhes técnicos |
| `modifiability` | Média | +2 | -1 | 0 | Alta | Facilidade de mock e substituição de banco |
| `reliability` | Alta | +2 | +1 | -1 | Alta | Separação entre liveness e readiness |

## Histórico e decisão atual

### Decisão da versão anterior
Nenhuma (versão inicial).

### Decisão recomendada nesta versão
Adotar a **Alternativa A**:
1. Criar `src/backend/api/health.py` com endpoints `/health` e `/ready`, recebendo a porta de capacidade `VerificadorConectividadePersistencia | None`.
2. Registrar `/health` e `/ready` no conjunto `ROTAS_PUBLICAS` de `src/backend/api/middleware_autenticacao.py`.
3. Criar `src/backend/infrastructure/persistence/sqlalchemy/verificador_conectividade.py` implementando a porta com `AsyncSession.execute(text("SELECT 1"))`.
4. Atualizar `src/backend/api/factory.py` para receber `verificador_conectividade` e registrar o roteador.
5. Criar suíte de testes unitários em `src/backend/tests/test_api_health.py` e `src/backend/tests/test_infrastructure_verificador_conectividade.py`.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `security` | Priorizada | Respostas mínimas e seguras (`{"status": "ok"}`) sem vazar dados de ambiente | Requisito explícito da issue #178 |
| `reliability` | Priorizada | Retorno preciso de status 503 quando a persistência falha | Requisito explícito da issue #179 |
| `modifiability` | Priorizada | Testabilidade total com doubles unitários | Padrão arquitetural estabelecido em `AGENTS.md` |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | Máximo 2 arquivos novos concisos | O código de transporte e o de persistência possuem menos de 50 linhas cada |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `security` | Vazamento de senhas, host ou ambiente em respostas de erro | Alta | Sistema e compliance |
| `reliability` | O balanceador direcionar tráfego para containers sem banco disponível | Alta | Usuários finais |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `modifiability` | Criação de um Protocol explícito em vez de chamada direta a banco | Leve aumento de linhas de código | Perfeitamente aceitável e exigido pelo padrão |

## Riscos e efeitos de segunda ordem

- **Risco:** O middleware de autenticação bloquear as rotas operacionais.
  - **Mitigação:** Adicionar explicitamente as tuplas `("GET", "/health")` e `("GET", "/ready")` em `ROTAS_PUBLICAS` com teste unitário validando a ausência de bloqueio 401.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Health check não vaza dados | Resposta contém exclusivamente chave `status` | Teste unitário de payload | Presença de chaves com host, versão ou stack |
| Readiness check acusa falha no banco | Erro na query gera HTTP 503 | Teste unitário com double simulando exceção | Retorno de 200 ou 500 não tratado |
| Rotas liberadas sem cookie de sessão | Requisição sem cookie passa pelo middleware | Teste com middleware ativo | Retorno de 401 Unauthorized |

## Handoffs e atividades posteriores

1. Implementar `src/backend/api/health.py`.
2. Atualizar `src/backend/api/middleware_autenticacao.py`.
3. Implementar `src/backend/infrastructure/persistence/sqlalchemy/verificador_conectividade.py`.
4. Atualizar `src/backend/api/factory.py`.
5. Implementar testes unitários em `src/backend/tests/`.
6. Validar linters e testes com `nix develop .#backend`.

## Síntese

A análise estabelece a implementação desacoplada dos endpoints `/health` e `/ready` no FastAPI com validação assíncrona da persistência relacional, sem exposição de dados sensíveis e com total proteção arquitetural contra acoplamento indevido.
