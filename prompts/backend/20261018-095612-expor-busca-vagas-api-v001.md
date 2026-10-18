---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-18T09:56:12-03:00"
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
    - path: src/backend/application/consulta_vagas.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "46a7a75d03ac9c9fec0eb2b109ba76f52d507a14"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "L525-L560"
      content_state: commit
      revision: "46a7a75d03ac9c9fec0eb2b109ba76f52d507a14"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "46a7a75d03ac9c9fec0eb2b109ba76f52d507a14"
      availability: available
    - path: src/backend/api/documentacao_openapi.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "46a7a75d03ac9c9fec0eb2b109ba76f52d507a14"
      availability: available
    - path: src/backend/api/middleware_autenticacao.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "46a7a75d03ac9c9fec0eb2b109ba76f52d507a14"
      availability: available
    - path: docs/contratos_integracao_grupo2.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Seções 2, 3 e 4"
      content_state: commit
      revision: "46a7a75d03ac9c9fec0eb2b109ba76f52d507a14"
      availability: available
    - path: src/frontend/features/listar-vagas/api/cliente-vagas-grupo2.ts
      relationship: context
      representation: source-code
      function: production
      format: typescript
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "46a7a75d03ac9c9fec0eb2b109ba76f52d507a14"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories:
    - prompts/backend
    - prompts/requisitos
    - prompts/qualidade
  confidence: high
  rationale: "A decisão trata da especificação da interface HTTP de consulta de vagas em FastAPI (src/backend/api/vagas.py) e sua integração na fábrica ASGI da aplicação backend."
classification:
  sphere: engineering
  concerns:
    - architecture
    - integration
    - security
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: low
  reversibility: easy
  risk: low
---

# Análise de decisão — Exposição de resultados de busca de vagas via API HTTP

## Solicitação original

Implementar a Issue #128 ("Expor resultados de busca de vagas"), abrangendo suas subtarefas:
- **[F7.5] (#241)**: Expor o estado vazio da busca de vagas com o filtro usado pelo estudante (`GET /vagas`).
- **[F7.6] (#242)**: Expor o estado de erro da busca de vagas sem enviar detalhes internos ao cliente (`GET /vagas`).

## Informações complementares

- "Na importação dos códigos de status HTTP do FastAPI/Starlette, certifique-se de usar status.HTTP_422_UNPROCESSABLE_CONTENT caso utilize 422 em alguma validação, evitando advertências de deprecação do Starlette."
- O caso de uso `ConsultarVagas` e as exceções canônicas de aplicação (`ErroIntegracaoVagas`, `RespostaInvalidaVagas`, `TimeoutIntegracaoVagas`) já foram implementados e validados na Issue #126.
- A camada de infraestrutura já dispõe do adaptador `ClienteApiVagasGrupo2Http` e a suíte dispõe do dublê `DoubleApiVagasGrupo2`.

## Mudanças desde a versão anterior

Nenhuma — versão inicial da análise para a Issue #128.

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/application/consulta_vagas.py` | supporting | source-code | production | python | whole-file | commit 46a7a75d |
| `src/backend/application/ports.py` | supporting | source-code | production | python | selected-section (L525-L560) | commit 46a7a75d |
| `src/backend/api/factory.py` | supporting | source-code | production | python | whole-file | commit 46a7a75d |
| `src/backend/api/documentacao_openapi.py` | supporting | source-code | production | python | whole-file | commit 46a7a75d |
| `src/backend/api/middleware_autenticacao.py` | supporting | source-code | production | python | whole-file | commit 46a7a75d |
| `docs/contratos_integracao_grupo2.md` | context | prose | documentation | markdown | selected-section (Seções 2, 3 e 4) | commit 46a7a75d |
| `src/frontend/features/listar-vagas/api/cliente-vagas-grupo2.ts` | context | source-code | production | typescript | whole-file | commit 46a7a75d |

### Limites da evidência dos artefatos

Os arquivos examinados estão completos e sincronizados na árvore de trabalho local baseada no commit `46a7a75d03ac9c9fec0eb2b109ba76f52d507a14`.

## Problema enriquecido

### Resultado desejado
Disponibilizar um endpoint HTTP `GET /vagas` limpo, resiliente e padronizado em FastAPI, que permita aos estudantes pesquisar oportunidades externas utilizando termo textual e filtros opcionais. Quando a pesquisa não encontrar registros, a API deve retornar sucesso (HTTP 200) com lista vazia preservando o termo e os filtros informados (subtarefa #241). Quando houver falhas de comunicação com a integração externa, a API deve responder com erros HTTP controlados (502/504) apresentando mensagens seguras e sem vazar stack traces, URLs internas ou informações confidenciais (subtarefa #242).

### Atores e interesses
- **Estudante autenticado**: Deseja consultar vagas relevantes com segurança e clareza, recebendo feedback inteligível mesmo quando não houver vagas ou quando o serviço externo estiver indisponível.
- **Frontend do sistema**: Necessita de um contrato JSON estável e previsível para renderizar o estado preenchido, o estado vazio com opção de ajustar filtros e o estado de erro com mensagem segura.
- **Desenvolvedores e Operação**: Necessitam de baixo acoplamento entre a borda HTTP e a camada Application, com rastreabilidade, testes unitários determinísticos e conformidade arquitetural estrita.

### Evidências e fatos observados
1. O caso de uso `ConsultarVagas` reside em `src/backend/application/consulta_vagas.py` e recebe `ConsultarVagasEntrada(termo=..., filtros=...)`, retornando `list[VagaExternaDto]`.
2. Em falhas de integração, a camada Application lança:
   - `TimeoutIntegracaoVagas`: herda de `ErroIntegracaoVagas` e preserva `termo` e `filtros`.
   - `RespostaInvalidaVagas`: herda de `ErroIntegracaoVagas` para payloads corrompidos.
   - `ErroIntegracaoVagas`: base hierárquica para indisponibilidades genéricas.
3. A fábrica ASGI `create_app` em `src/backend/api/factory.py` injeta executores via protocolos abstratos e inclui routers modulares tipados.
4. O middleware de autenticação protege rotas privadas contra requisições anônimas exigindo `request.state.usuario_id`.

### Hipóteses
- O endpoint `GET /vagas` opera dentro do escopo protegido por autenticação do estudante, alinhado aos demais recursos do sistema.
- A transmissão dos filtros via query parameters atende à idempotência e semântica do método HTTP GET.

### Perguntas em aberto
Nenhuma. O escopo e os contratos estão claramente delimitados pela Issue #128 e sub-issues #241 e #242.

### Escopo
- Criação de `src/backend/api/vagas.py` contendo os DTOs Pydantic de resposta (`VagaResposta`, `ResultadoBuscaVagasResposta`), o protocolo `ConsultaVagasExecutor` e a fábrica de router `criar_router`.
- Tratamento explícito do estado vazio ([F7.5]) com status HTTP 200 OK e preservação fiel de `termo` e `filtros`.
- Tratamento explícito de erros ([F7.6]) traduzindo `TimeoutIntegracaoVagas` em HTTP 504 e `RespostaInvalidaVagas`/`ErroIntegracaoVagas` em HTTP 502, com mensagens genéricas e seguras.
- Inclusão do router e da tag `TAG_VAGAS` na fábrica `create_app` e em `documentacao_openapi.py`.
- Criação de testes unitários isolados com dublês em memória em `src/backend/tests/test_api_vagas.py`.
- Uso de `status.HTTP_422_UNPROCESSABLE_CONTENT` caso validação retorne 422.

### Fora do escopo
- Modificações no modelo de domínio de currículo ou regras de persistência relacional.
- Modificações no caso de uso `ConsultarVagas` já concluído na Issue #126.
- Modificações em componentes de frontend ou em pacotes Nix.
- Testes de integração de sistema com serviços externos reais.

### Critérios de sucesso
- Endpoint `GET /vagas` responde com 200 OK e lista de vagas quando a busca é bem-sucedida.
- Endpoint `GET /vagas` responde com 200 OK, `total: 0`, `vagas: []` e ecoa `termo` e `filtros` quando nenhuma vaga é encontrada ([F7.5]).
- Falhas de tempo limite retornam 504 Gateway Timeout e falhas de contrato/rede retornam 502 Bad Gateway com mensagem segura e sem vazamento interno ([F7.6]).
- Ausência de autenticação resulta em HTTP 401 Unauthorized.
- Router registrado com sucesso no OpenAPI da fábrica ASGI.
- 100% dos testes unitários passando em `nix develop .#backend`.
- Linters e formatador aprovados em `nix develop .#quality`.

## Restrições aplicáveis

- **AGENTS.md raiz e src/backend/AGENTS.md**: Clean Architecture estrita, separação entre Interface e Application, uso de docstrings triplas explicativas (*O que faz*, *Como faz*, *Qual finalidade atende*) e tags de proveniência `# Proveniência: decision-analysis ...`.
- **Prevenção de Deprecação**: Usar `status.HTTP_422_UNPROCESSABLE_CONTENT` ao invés de `HTTP_422_UNPROCESSABLE_ENTITY`.
- **Higiene do Repositório**: NUNCA versionar arquivos `.pyc` ou diretórios `__pycache__`.

## Classificação comentada

- **Esfera primária (`engineering`)**: Refere-se à implementação de um adapter de interface HTTP conectando a camada de aplicação ao mundo externo.
- **Preocupações (`architecture`, `integration`, `security`)**: Respeita os limites da Clean Architecture, encapsula a integração externa de vagas e impede o vazamento de dados internos de segurança ou infraestrutura.
- **Tipo de decisão (`design`)**: Define o desenho do endpoint, seus DTOs de transporte e o mapeamento de respostas/erros.

## Decisão de roteamento

- Diretório selecionado: `prompts/backend`
- Justificativa: Trata-se de funcionalidade exclusiva da camada de API do backend, alinhada aos precedentes de endpoints HTTP do repositório.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | Alta | Máxima fidelidade aos requisitos das subtarefas #241 e #242 | Garante conformidade com os critérios de aceite e estabilidade da API |
| `security` | Alta | Zero vazamento de detalhes internos ou exceções técnicas | Protege a infraestrutura e credenciais do sistema contra enumeração ou exposição indevida |
| `simplicity` | Alta | Adapter fino sem regras de negócio embutidas | Mantém a Clean Architecture e facilita manutenção |
| `user-value` | Média | Respostas compreensíveis e preservação de filtros de busca | Permite ao usuário refinar pesquisas sem perder contexto |

## Alternativas consideradas

- **Alternativa A (Recomendada)**: Criar `src/backend/api/vagas.py` com o endpoint `GET /vagas`, DTOs tipados `VagaResposta` e `ResultadoBuscaVagasResposta`, protocolo `ConsultaVagasExecutor`, injeção em `create_app` na fábrica ASGI, mapeamento seguro do estado vazio ([F7.5]) e sanitização de exceções em HTTP 504/502 ([F7.6]).
- **Alternativa B**: Acoplar diretamente o handler HTTP à implementação concreta `ConsultarVagas` e ao cliente externo sem protocolo de injeção, delegando o tratamento de erros a um handler genérico global.
- **Alternativa C**: Aninhar a busca de vagas sob o recurso de currículo (`GET /curriculos/{id}/vagas`), forçando a amarração prévia a um currículo existente.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | Alta | +2 | -1 | 0 | Alta | Alternativa A cumpre diretamente as especificações de #241 e #242 |
| `security` | Alta | +2 | -2 | 0 | Alta | Alternativa A intercepta exceções específicas e emite mensagens puras |
| `simplicity` | Alta | +2 | 0 | -1 | Alta | Alternativa A mantém a rota simples e desacoplada |
| `user-value` | Média | +2 | -1 | -1 | Alta | Alternativa A permite busca direta por termo e filtros arbitrários |

## Histórico e decisão atual

### Decisão da versão anterior
Nenhuma (versão inicial).

### Decisão recomendada nesta versão
Adotar integralmente a **Alternativa A**:
1. Criar `src/backend/api/vagas.py` expondo `GET /vagas`.
2. Modelar `VagaResposta` e `ResultadoBuscaVagasResposta` com Pydantic.
3. Definir `ConsultaVagasExecutor(Protocol)` para injeção limpa de dependência.
4. Mapear estado vazio para HTTP 200 OK preservando termo e filtros ([F7.5]).
5. Interceptar `TimeoutIntegracaoVagas` (HTTP 504) e `RespostaInvalidaVagas`/`ErroIntegracaoVagas` (HTTP 502) com detalhes limpos ([F7.6]).
6. Conectar na fábrica `src/backend/api/factory.py` e documentar a tag `Vagas` em `src/backend/api/documentacao_openapi.py`.
7. Criar suíte completa de testes unitários isolados em `src/backend/tests/test_api_vagas.py`.

### Impacto da revisão
Decisão inicial que viabiliza a conclusão da fatia vertical de busca de vagas externas no backend.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | maximized | Satisfação plena de [F7.5] e [F7.6] | Testes unitários cobrindo estado vazio e cenários de erro |
| `security` | maximized | Ausência total de vazamento de stack traces e detalhes técnicos | Interceptação e sanitização das exceções de integração |
| `simplicity` | prioritized | Isolamento estrito entre transporte e lógica de aplicação | Protocolo tipado e DTOs puros |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `modifiability` | Aceitável | Separação em módulo exclusivo `vagas.py` facilita futuras expansões |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `security` | Exposição de detalhes internos em erros | Alta | Sistema e usuários |
| `correctness` | Perda de filtros em buscas vazias | Média | Estudantes e frontend |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `security` | Mensagens de erro resumidas não indicam causa raiz ao cliente | Diagnóstico detalhado pelo cliente | Totalmente aceitável (diagnóstico cabe a logs do servidor) |

## Riscos e efeitos de segunda ordem

- *Risco*: O cliente externo pode demorar a responder sob alta carga.
  *Mitigação*: O timeout já é tratado na camada de aplicação e o endpoint converte seguramente em HTTP 504 sem travar a thread.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Resposta vazia preserva filtros | Resposta 200 com termo e filtros originais intactos | Teste unitário em `test_api_vagas.py` | Filtros retornando nulos ou vazios |
| Erros não vazam detalhes | Resposta 502/504 contendo somente mensagem controlada | Teste unitário com injeção de exceção de integração | Detalhes internos ou stack traces visíveis no JSON |
| Swagger OpenAPI íntegro | Rota `/vagas` registrada com documentação de tags | Teste unitário de OpenAPI em `create_app` | Rota ausente da especificação OpenAPI |

## Handoffs e atividades posteriores

- Implementação do endpoint e testes via `$backend-adapters-drivers-v2`.
- Validação no ambiente Nix (`#backend` e `#quality`).
- Abertura de Pull Request para `dev`.

## Síntese

A análise estabelece o design técnico completo para a exposição da busca de vagas na API HTTP do backend, atendendo expressamente às exigências funcionais de preservação de filtros no estado vazio ([F7.5]) e segurança contra vazamento de informações em erros ([F7.6]), em total conformidade com a Clean Architecture.

Arquivo criado em prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md. Avalie se o local escolhido é de fato o mais adequado.
