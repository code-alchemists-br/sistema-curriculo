---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-15T16:02:31-03:00"
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
    - path: "github:code-alchemists-br/sistema-curriculo#126"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: selected-section
      locator: "título, descrição, subtarefas #237 a #240 e requisitos associados"
      content_state: external
      revision: "consultada em 2026-10-15; sem identificador imutável"
      availability: partial
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: fe383e4
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: fe383e4
      availability: available
    - path: docs/contratos_integracao_grupo2.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "seções 1 a 4, Contrato 2 (modelo de vaga) e Contrato 3 (resposta de vagas)"
      content_state: commit
      revision: fe383e4
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "linhas 525 a 560 (VagaExternaDto e Protocol BuscadorVagas)"
      content_state: commit
      revision: fe383e4
      availability: available
    - path: src/backend/tests/doubles/api_vagas_grupo2.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: fe383e4
      availability: available
    - path: nix/backend-python-packages.nix
      relationship: supporting
      representation: source-code
      function: configuration
      format: Nix
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: fe383e4
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/ambientes]
  confidence: high
  rationale: "A análise define a orquestração do caso de uso de consulta de vagas e a implementação do adaptador HTTP correspondente às subtarefas da issue #126 no backend."
classification:
  sphere: engineering
  concerns: [architecture, integration, resiliency]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: low
  reversibility: moderate
  risk: low
---

# Análise de decisão — Implementação da consulta de vagas via API externa (Issue #126)

## Solicitação original

Implementar a Issue #126: "Implementar consulta de vagas via API externa", cobrindo suas quatro subtarefas decompostas:
- [F7.1] (#237): Definir DTO interno de vaga, separado do JSON recebido do Grupo 2.
- [F7.2] (#238): Mapear uma resposta válida do Grupo 2 para o DTO interno e testar campos ausentes.
- [F7.3] (#239): Mapear JSON inválido para erro de integração compreensível ao usuário.
- [F7.4] (#240): Mapear tempo limite da integração para erro transitório sem perder filtros de busca.

## Informações complementares

Refinamentos técnicos operacionais fornecidos para a execução:
1. O ambiente Nix `.#backend` não possui `pytest`; utiliza exclusivamente a biblioteca padrão `unittest`. Todos os comandos de teste devem ser executados via:
   `PYTHONPATH=src nix develop .#backend --command python -m unittest src/backend/tests/test_arquivo.py`
2. O ambiente Nix atual do backend (`nix/backend-python-packages.nix`) não inclui `httpx`.
   Portanto, a implementação do cliente HTTP assíncrono deve optar entre:
   - Opção A (Recomendada sem alteração no Nix): Implementar o cliente HTTP assíncrono utilizando a biblioteca padrão do Python (`urllib.request` ou `http.client` encapsulado via `asyncio.to_thread`), ou injetar um protocolo/transporte abstrato.
   - Opção B: Alterar a declaração do Nix para incluir `httpx` através da skill `nix-environment-implementation-v1`.
3. Verificação de linters via Ruff no Nix (`.#quality`) direcionada à pasta do backend:
   `nix develop .#quality --command ruff check src/backend` e `nix develop .#quality --command ruff format --check src/backend`.

## Mudanças desde a versão anterior

Nenhuma — esta é a versão inicial (`v001`) da linhagem.

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| Issue #126 | primary | prose | documentation | GitHub issue | título, descrição e subtarefas #237 a #240 | externa, consultada em 2026-10-15 |
| `AGENTS.md` | context | prose | prompt-instruction | Markdown | arquivo completo | commit `fe383e4` |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | Markdown | arquivo completo | commit `fe383e4` |
| `docs/contratos_integracao_grupo2.md` | supporting | prose | documentation | Markdown | seções 1 a 4 (Contratos 2 e 3) | commit `fe383e4` |
| `src/backend/application/ports.py` | supporting | source-code | production | Python | linhas 525 a 560 (`VagaExternaDto` e `BuscadorVagas`) | commit `fe383e4` |
| `src/backend/tests/doubles/api_vagas_grupo2.py` | supporting | source-code | test | Python | arquivo completo (double e exceções) | commit `fe383e4` |
| `nix/backend-python-packages.nix` | supporting | source-code | configuration | Nix | arquivo completo (dependências Python) | commit `fe383e4` |

### Limites da evidência dos artefatos

O contrato em `docs/contratos_integracao_grupo2.md` é uma especificação alinhada entre as equipes do Grupo 1 e Grupo 2. A porta `BuscadorVagas` e o `VagaExternaDto` já estão presentes em `src/backend/application/ports.py` (fruto da issue #124 anterior). A ausência de `httpx` no arquivo de pacotes Nix é um fato observado diretamente em `nix/backend-python-packages.nix`.

## Problema enriquecido

### Resultado desejado

Disponibilizar na camada Application o caso de uso e exceções canônicas para busca de vagas, e na camada Infrastructure o adaptador HTTP concreto que consome a API externa do Grupo 2, realizando o mapeamento defensivo do JSON recebido, tratando campos opcionais ausentes/nulos, traduzindo respostas inválidas para mensagens claras ao usuário e convertendo timeouts em erros transitórios com preservação dos parâmetros e filtros de busca originais.

### Atores e interesses

- **Estudante:** Realizar buscas de vagas sem interrupções catastróficas, com mensagens amigáveis em caso de falha externa e capacidade de tentar novamente sem perder os filtros preenchidos.
- **Application (Clean Architecture):** Depender unicamente da porta abstrata `BuscadorVagas`, sem conhecimento de HTTP, JSON bruto ou nomes específicos do Grupo 2.
- **Adaptador de Infraestrutura:** Isolar a complexidade de rede, HTTP e serialização externa, entregando DTOs canônicos e levantando exceções tipadas de aplicação.
- **Equipe de Desenvolvimento:** Manter a consistência do ambiente Nix sem adicionar dependências desnecessárias ou quebrar a suíte de testes existente com `unittest`.

### Evidências e fatos observados

- O contrato do Grupo 2 retorna um array de objetos de vaga contendo:
  - Campos obrigatórios: `id: str`, `titulo: str`, `empresa: str`, `descricao: str`, `requisitos: list[str]`.
  - Campos opcionais: `localizacao: str | None`, `modalidade: str | None`, `url_candidatura: str | None`.
- O `VagaExternaDto` da Application define:
  `id: str`, `titulo: str`, `empresa: str`, `descricao: str`, `requisitos: tuple[str, ...]`, `localizacao: str`, `modalidade: str`, `url_candidatura: str`.
- O ambiente Nix não possui `pytest` nem `httpx`. Possui Python 3 com toda a biblioteca padrão (`urllib.request`, `http.client`, `asyncio`, `json`, `unittest`).

### Hipóteses

- O uso de `asyncio.to_thread` com `urllib.request` é suficiente, seguro e de baixo custo operacional para requisições HTTP assíncronas do backend, dispensando a necessidade de modificar o arquivo de pacotes Nix do projeto.
- Testes unitários do adaptador podem utilizar um protocolo de transporte injetável ou `unittest.mock` para simular cenários de 200, 500, timeout e JSON malformado sem tráfego de rede.

### Perguntas em aberto

Nenhuma. As restrições de ambiente e as 4 subtarefas da issue estão plenamente especificadas.

### Escopo

1. Implementar o caso de uso de aplicação `ConsultarVagas` (ou `ServicoConsultaVagas`) em `src/backend/application/consulta_vagas.py`.
2. Definir as exceções de integração na camada Application:
   - `ErroIntegracaoVagas` (base com `termo: str` e `filtros: dict[str, Any]`).
   - `RespostaInvalidaVagas` (para JSON malformado, HTTP 5xx ou campos essenciais ausentes).
   - `TimeoutIntegracaoVagas` / `IndisponibilidadeIntegracaoVagas` (para timeout/falha de conexão, preservando `termo` e `filtros`).
3. Implementar o adaptador de infraestrutura em `src/backend/infrastructure/integrations/cliente_vagas_grupo2.py` (implementando `BuscadorVagas`):
   - Mapeamento defensivo do JSON do Grupo 2 para `VagaExternaDto`.
   - Normalização de campos opcionais (`None` -> `""`, lista ausente -> `()`).
   - Captura de timeouts e conversão em `TimeoutIntegracaoVagas`.
   - Captura de falhas de schema/decodificação e conversão em `RespostaInvalidaVagas`.
4. Testes unitários com `unittest` para aplicação e adaptador.

### Fora do escopo

- Alteração da configuração do Nix (já que a biblioteca padrão cobre perfeitamente a necessidade).
- Interface web / frontend (Issue #128 posterior).
- Persistência ou associação automática de vagas a currículos.

### Critérios de sucesso

- Todos os cenários das 4 subtarefas cobertos com testes unitários passando em `nix develop .#backend --command python -m unittest ...`.
- Nenhuma dependência externa adicionada ao ambiente Nix.
- Docstrings completas (triplas) e tags de proveniência em todos os símbolos.
- Linter `ruff` sem apontamentos em `nix develop .#quality`.

## Restrições aplicáveis

- **Uso estrito do Nix:** Testes e linters executados via Nix; Git executado fora do Nix.
- **Clean Architecture:** `src/backend/application` não deve importar bibliotecas de I/O de rede (`urllib`, `http.client`).
- **Framework de Testes:** Uso exclusivo de `unittest` padrão da biblioteca Python.

## Classificação comentada

- **Esfera:** `engineering`.
- **Preocupações:** `architecture` (Clean Architecture e separação de portas/adaptadores), `integration` (API externa do Grupo 2), `resiliency` (tratamento defensivo de timeouts e respostas inválidas).
- **Incerteza:** `low` (especificações claras e contratos documentados).
- **Risco:** `low` (adaptador isolado sem impacto em persistência de dados).

## Decisão de roteamento

- Raiz: `prompts`.
- Subpasta selecionada: `prompts/backend`.
- Justificativa: Trata-se de implementação direta da camada de aplicação e infraestrutura backend.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| Aderência ao Nix | Alta | Não exigir novas dependências se a biblioteca padrão atender | Evita retrabalho de infraestrutura e reavaliação de ambiente |
| Resiliência a falhas externas | Alta | Não quebrar o backend com exceções de transporte brutas | Usuário deve receber erro amigável e manter filtros |
| Desacoplamento da camada Application | Alta | Zero imports de infraestrutura em Application | Conformidade com ADR-001 e Clean Architecture |

## Alternativas consideradas

### Alternativa 1: Biblioteca padrão (`urllib.request` via `asyncio.to_thread`) no adaptador
- Utiliza a biblioteca nativa do Python, sem necessidade de alterar o Nix.
- Encapsula a chamada síncrona de I/O em uma thread assíncrona com `asyncio.to_thread`.
- Permite injeção de função de transporte ou mock simples nos testes.

### Alternativa 2: Incluir `httpx` no Nix via `nix-environment-implementation-v1`
- Exige análise de decisão prévia para ambientes Nix, edição de `nix/backend-python-packages.nix` e atualização do lockfile/ambiente.
- Adiciona overhead desnecessário para uma integração HTTP simples de consulta.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa 1 (Stdlib urllib + asyncio) | Alternativa 2 (httpx no Nix) | Confiança | Base |
|---|---:|---:|---:|---|---|
| Aderência ao Nix existente | Alta | Excelente (zero alterações) | Pobre (exige alteração de Nix) | Alta | Inspeção do Nix |
| Performance/Adequação assíncrona | Média | Boa (thread pool nativo do asyncio) | Ótima (cliente assíncrono nativo) | Alta | Prática Python |
| Simplicidade de testes | Alta | Excelente (transporte simulável via unittest) | Boa (mock transport) | Alta | Experiência de testes |

## Histórico e decisão atual

### Decisão da versão anterior
Nenhuma (versão inicial).

### Decisão recomendada nesta versão
Adotar a **Alternativa 1**:
1. Implementar o cliente HTTP assíncrono na infraestrutura utilizando a biblioteca padrão (`urllib.request` / `urllib.error`) encapsulada em `asyncio.to_thread`, com suporte a injeção de função/transporte para testes determinísticos.
2. Definir o timeout configurável com valor padrão de `5.0` segundos.
3. Definir a hierarquia de exceções de integração na camada Application, com suporte à preservação dos campos `termo` e `filtros`.
4. Implementar testes unitários completos com `unittest`.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Aderência ao ambiente | Maximizada | Nenhuma mudança no Nix necessária | `nix/backend-python-packages.nix` já possui o necessário |
| Resiliência de busca | Priorizada | Preservação dos filtros do estudante em caso de timeout | Requisito da subtarefa #240 |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Eficiência I/O | Não bloquear o event loop | `asyncio.to_thread` delega a execução síncrona para o pool de workers |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Estabilidade de ambiente | Quebra de CI ou incompatibilidade de pacotes Nix | Alta | Desenvolvedores e pipeline de CI |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Independência de libs externas | Pequeno overhead de thread pool em requisições de I/O | Complexidade de dependências | Plenamente aceitável |

## Riscos e efeitos de segunda ordem

- **Risco:** Timeout da API externa travar a thread por tempo excessivo.
- **Mitigação:** Configurar timeout estrito explícito em `urllib.request.urlopen(..., timeout=5.0)`.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Mapeamento de campos ausentes seguro | Testes com payloads contendo nulos e chaves ausentes passando | `python -m unittest` | KeyError ou AttributeError no mapeamento |
| Preservação de filtros no timeout | Exceção capturada contendo termo e filtros originais | Teste de unidade com simulação de timeout | Exceção sem parâmetros originais |

## Handoffs e atividades posteriores

1. Handoff para `$backend-domain-orchestration-v2`: Criação das exceções de aplicação e caso de uso `ConsultarVagas`.
2. Handoff para `$backend-adapters-drivers-v2`: Implementação do adaptador `ClienteApiVagasGrupo2Http` e mapeadores em `infrastructure`.

## Síntese

Decisão tomada para implementar a consulta de vagas da Issue #126 utilizando a porta `BuscadorVagas` já existente, definindo exceções de aplicação que preservam o contexto de busca e implementando o adaptador HTTP na infraestrutura com a biblioteca padrão (`urllib.request` + `asyncio.to_thread`), garantindo conformidade com o ambiente Nix e testes unitários via `unittest`.
