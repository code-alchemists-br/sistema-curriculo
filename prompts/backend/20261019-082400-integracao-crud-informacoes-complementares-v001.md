---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-19T08:24:00-03:00"
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
    - path: "github:code-alchemists-br/sistema-curriculo#398"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: whole-file
      locator: "título, descrição, planejamento WBS 1.7.1.*, 1.7.2.*, 1.8.1.* e critérios de aceite"
      content_state: external
      revision: "consultada em 2026-10-19; sem identificador imutável"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771"
      availability: available
    - path: docs/matriz_rastreabilidade.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "linhas 44-59 (RF01 e RF02 associados a WBS 1.7.1.*, 1.7.2.*, 1.8.1.* e card #398)"
      content_state: commit
      revision: "5266771"
      availability: available
    - path: src/backend/api/documento.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771"
      availability: available
    - path: src/backend/api/curso.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "linhas 50-75 e 300-320 (montagem dos routers de documentos complementares e cursos)"
      content_state: commit
      revision: "5266771"
      availability: available
    - path: src/backend/application/cadastro_documento.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771"
      availability: available
    - path: src/backend/application/exclusao_documento.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771"
      availability: available
    - path: src/backend/application/cadastro_curso.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771"
      availability: available
    - path: src/backend/domain/secao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "linhas 13-45 (SecaoCurriculo.DOCUMENTOS_COMPLEMENTARES)"
      content_state: commit
      revision: "5266771"
      availability: available
    - path: src/backend/tests/test_integracao_isolamento_experiencias.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "linhas 186-285 (padrão arquitetural de harness de teste ASGI integrado com sessão sintética e middleware ativo)"
      content_state: commit
      revision: "5266771"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A decisão abrange a estratégia de testes integrados e oráculos para as rotas e casos de uso de informações complementares (documentos e cursos) no backend."
classification:
  sphere: engineering
  concerns: [testing, architecture, security]
  decision_kind: design
  scope: component
  lifecycle: verification
  urgency: normal
  uncertainty: low
  reversibility: high
  risk: low
---

# Análise de decisão — Testes de Integração para CRUD de Informações Complementares (Issue #398)

## Solicitação original

GitHub Issue #398: `[F11.7] Criar teste de integração para o CRUD de informações complementares, incluindo resposta inválida.`
Planejamento: WBS 1.7.1.*, 1.7.2.*, 1.8.1.*.
Início: 2026-10-19. Entrega: 2026-10-25.
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.

## Informações complementares

1. Diretriz de ambientes Nix (`AGENTS.md` e `src/backend/AGENTS.md`): Testes de integração devem ser executados estritamente através do ambiente `nix develop .#tests` utilizando `python3 -m unittest`.
2. Restrição de isolamento e oráculos: O teste integrado deve cobrir as operações de criação (upload/cadastro) e exclusão, além de cenários negativos e respostas inválidas (401 para falta de credencial, 404 para ID inexistente ou IDOR alheio, 409 para duplicidade e 422 para violações de schema ou regras de domínio).
3. Padrão arquitetural estabelecido: Conforme demonstrado em `test_integracao_isolamento_experiencias.py` e `test_integracao_recusa_perfil_alheio.py`, testes de integração HTTP exercitam a aplicação ASGI completa gerada por `create_app` com middleware de autenticação ativo e casos de uso reais da camada `application`, mantendo repositórios e armazenadores de teste com estado em memória para evitar acoplamento com infraestruturas externas frágeis.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Estado | Inexistente | v001 inicial | Criação da análise para a Issue #398 | Estabelece escopo e desenho técnico da suíte integrada |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `github:code-alchemists-br/sistema-curriculo#398` | primary | prose | documentation | GitHub issue | whole-file | external / 2026-10-19 |
| `AGENTS.md` | context | prose | prompt-instruction | Markdown | whole-file | commit `5266771` |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | Markdown | whole-file | commit `5266771` |
| `docs/matriz_rastreabilidade.md` | context | prose | documentation | Markdown | linhas 44-59 | commit `5266771` |
| `src/backend/api/documento.py` | primary | source-code | production | Python | whole-file | commit `5266771` |
| `src/backend/api/curso.py` | primary | source-code | production | Python | whole-file | commit `5266771` |
| `src/backend/api/factory.py` | supporting | source-code | production | Python | linhas 50-75 e 300-320 | commit `5266771` |
| `src/backend/application/cadastro_documento.py` | supporting | source-code | production | Python | whole-file | commit `5266771` |
| `src/backend/application/exclusao_documento.py` | supporting | source-code | production | Python | whole-file | commit `5266771` |
| `src/backend/application/cadastro_curso.py` | supporting | source-code | production | Python | whole-file | commit `5266771` |
| `src/backend/domain/secao_curriculo.py` | supporting | source-code | production | Python | linhas 13-45 | commit `5266771` |
| `src/backend/tests/test_integracao_isolamento_experiencias.py` | supporting | source-code | test | Python | linhas 186-285 | commit `5266771` |

### Limites da evidência dos artefatos

Os arquivos do repositório inspecionados encontram-se disponíveis no commit `5266771`. A issue #398 foi consultada via GitHub CLI em 2026-10-19 e delimitada aos requisitos funcionais RF01 e RF02 (matriz de rastreabilidade).

## Problema enriquecido

### Resultado desejado

Implementar uma suíte de testes de integração robusta, determinística e rápida para o CRUD de informações complementares (`src/backend/tests/test_integracao_crud_informacoes_complementares.py`), exercitando os fluxos HTTP ASGI reais de documentos complementares (`POST /documentos` e `DELETE /documentos/{id}`) e cursos complementares (`POST /cursos`), incluindo oráculos rigorosos para respostas válidas e inválidas (401, 404, 409, 422).

### Atores e interesses

- **Estudante Autenticado (Ator A):** Deseja cadastrar documentos complementares (comprovantes, certificados em PDF/imagem) e cursos, consultá-los e excluí-los quando necessário, sem que outros usuários possam interferir.
- **Outro Estudante (Ator B):** Não deve sofrer interferência em seus documentos ou cursos por requisições de outros usuários (prevenção de IDOR e vazamento de dados).
- **Time de Engenharia e Qualidade:** Exige garantia de que as rotas de transporte, middlewares de segurança e casos de uso de aplicação funcionem integrados, rejeitando payloads inválidos e mantendo isolamento de inquilinos.

### Evidências e fatos observados

1. O domínio define `SecaoCurriculo.DOCUMENTOS_COMPLEMENTARES` e a entidade `Curso` como curso complementar (`itens_perfil.py`).
2. O endpoint `POST /documentos` recebe `CadastroDocumentoRequisicao(nome_arquivo, tipo_arquivo, conteudo_base64)` e responde 201 com `DocumentoResposta(id, usuario_id, nome_arquivo, tipo_arquivo, url_armazenamento)`.
3. O endpoint `DELETE /documentos/{documento_id}` remove logicamente o documento e responde 204. Se o documento não existir ou pertencer a outro usuário, responde 404 para evitar enumeração de recursos (IDOR).
4. O endpoint `POST /cursos` recebe `CadastroCursoRequisicao(nome, instituicao, carga_horaria)` e responde 201 com `CursoResposta(id, usuario_id, nome, instituicao, carga_horaria)`. Se houver curso duplicado para o usuário e instituição, responde 409 Conflict.
5. Em ambos os routers, a ausência de identidade na sessão resulta em 401 Unauthorized.
6. Dados malformados ou incompletos acionam a validação de fronteira (Pydantic/FastAPI) gerando 422 Unprocessable Entity; violações de regras de negócio (`RegraDeDominioViolada`) geram 422 Unprocessable Content.

### Hipóteses

- O teste integrado ASGI com injeção de `create_app` exercita integralmente o pipeline (middleware de autenticação, desserialização Pydantic, handlers FastAPI, orquestração de casos de uso e domínio), sem necessidade de rodar servidor HTTP externo ou banco de dados externo compartilhado.
- Testes unitários já existentes focam em componentes individuais com stubs isolados; a suíte de integração preenche a lacuna de validação de fluxo entre camadas para informações complementares.

### Perguntas em aberto

Nenhuma. Os contratos de API, DTOs, casos de uso e oráculos estão completamente implementados e estabilizados no código de produção.

### Escopo

1. Criação do arquivo de teste de integração `src/backend/tests/test_integracao_crud_informacoes_complementares.py`.
2. Cobertura integrada para Documentos Complementares:
   - `POST /documentos` com sessão válida e payload correto (status 201, validação dos campos retornados e persistência de metadados e binário).
   - `POST /documentos` sem sessão ou com sessão inválida (status 401).
   - `POST /documentos` com payload vazio/campos obrigatórios ausentes (status 422).
   - `POST /documentos` com conteúdo Base64 corrompido ou tipo de arquivo proibido (status 422).
   - `DELETE /documentos/{documento_id}` com sessão válida e proprietário legítimo (status 204, exclusão efetiva).
   - `DELETE /documentos/{documento_id}` sem sessão válida (status 401).
   - `DELETE /documentos/{documento_id}` com ID inexistente (status 404).
   - `DELETE /documentos/{documento_id}` com ID pertencente a outro estudante (status 404, garantia anti-IDOR).
3. Cobertura integrada para Cursos Complementares:
   - `POST /cursos` com sessão válida e payload correto (status 201, verificação dos campos retornados).
   - `POST /cursos` com carga horária omitida/nula (status 201).
   - `POST /cursos` sem autenticação (status 401).
   - `POST /cursos` duplicado para o mesmo estudante e instituição (status 409).
   - `POST /cursos` com valores inválidos de domínio como nome vazio ou carga horária negativa (status 422).
   - `POST /cursos` com tipo inválido de carga horária (status 422).
4. Execução e validação no ambiente Nix `nix develop .#tests`.

### Fora do escopo

- Alterações no código de produção de `src/backend/api/`, `application/` ou `domain/`.
- Testes unitários isolados de funções ou classes que já possuem suítes unitárias.
- Alterações em migrations Alembic ou infraestrutura de banco de dados PostgreSQL de produção.
- Testes de frontend ou CI/CD.

### Critérios de sucesso

- Todos os cenários de teste passam com sucesso através de `python3 -m unittest` no ambiente `nix develop .#tests`.
- 100% de conformidade com a convenção de docstring tripartita (*O que faz*, *Como faz*, *Qual finalidade atende*) e comentário de proveniência.
- Inspeção estática de qualidade `ruff check` no ambiente `nix develop .#quality` limpa sem violações.

## Restrições aplicáveis

- **Uso obrigatório do Nix (`AGENTS.md`):** Testes de integração devem rodar no ambiente `tests` (`nix develop .#tests --command bash -c "PYTHONPATH=src python3 -m unittest ..."`).
- **Clean Architecture & DDD (`src/backend/AGENTS.md`):** O teste não deve quebrar o encapsulamento do domínio nem expor credenciais ou segredos em asserções.
- **Rastreabilidade:** Comentário de proveniência obrigatório no topo do arquivo de teste criado apontando para este documento de decisão.

## Classificação comentada

- **Esfera:** `engineering` — Desenvolvimento de testes automatizados de integração de software.
- **Preocupações:** `[testing, architecture, security]` — Qualidade e oráculos de teste, preservação dos limites arquiteturais e segurança de autorização/anti-IDOR.
- **Tipo de decisão:** `design` — Desenho da estratégia de teste e matriz de casos de teste.
- **Escopo:** `component` — Componente de testes do backend para informações complementares.
- **Ciclo de vida:** `verification` — Validação de conformidade do software construído.
- **Urgência:** `normal` — Planejada na sprint semanal (F11.7).
- **Incerteza:** `low` — Código de produção, rotas e casos de uso já estão implementados e mapeados.
- **Reversibilidade:** `high` — Adição puramente em arquivos de teste.
- **Risco:** `low` — Não altera código de produção.

## Decisão de roteamento

O artefato foi alocado em `prompts/backend/` pois trata especificamente da arquitetura de testes e cobertura de endpoints do backend Python em `src/backend`.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| Fidelidade ao transporte real ASGI | 1 (Alta) | Executar pipeline ASGI completo com middleware de autenticação | Garante que filtros de cabeçalhos, cookies e middlewares de segurança funcionam como em produção |
| Cobertura de respostas inválidas | 2 (Alta) | Validar 401, 404, 409 e 422 em múltiplos cenários | Atende estritamente à descrição da issue #398 e critérios de segurança |
| Isolamento e determinismo | 3 (Média) | Zero dependência de banco de dados externo ou rede | Testes rápidos, confiáveis e executáveis em qualquer máquina sem flakiness |

## Alternativas consideradas

- **Alternativa A (Recomendada): Harness ASGI integrado com `create_app` e repositórios em memória com estado:** Constrói a aplicação via fábrica oficial com middleware ativo, executores reais da Application e adaptadores em memória de alta fidelidade.
- **Alternativa B: Testes contra banco de dados SQLite real via ORM:** Utiliza SQLite em memória com SQLAlchemy para persistência. Embora viável para persistência pura, adiciona complexidade desnecessária para storage binário (documentos) e acoplamento com transações de ORM quando o foco da issue é a integração de ponta a ponta do CRUD e respostas inválidas da API.
- **Alternativa C: Apenas testes unitários dos handlers com mocks puros (stubs):** Não atende ao propósito da issue #398 de ser um teste de integração, pois não cobriria o roteamento, middlewares ASGI nem a tradução de exceções da aplicação em códigos HTTP.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A (Recomendada) | Alternativa B (SQLite) | Alternativa C (Mocks unitários) | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Fidelidade ASGI | 1 | Excelente (pipeline real) | Excelente (pipeline real) | Fraca (chama handler isolado) | Alta | Padrão comprovado em `test_integracao_isolamento_experiencias.py` |
| Cobertura de erros HTTP | 2 | Completa (401, 404, 409, 422) | Completa | Parcial | Alta | Código dos handlers e middlewares |
| Simplicidade e velocidade | 3 | Alta (<0.5s sem I/O) | Média (DDL de tabelas) | Alta | Alta | Execução em memória |

## Histórico e decisão atual

### Decisão da versão anterior
Nenhuma (versão inicial).

### Decisão recomendada nesta versão
Adotar a **Alternativa A**, criando `src/backend/tests/test_integracao_crud_informacoes_complementares.py` com composição oficial via `create_app`, autenticador de sessão determinístico (suportando Estudante A e Estudante B para validação de IDOR), repositórios e armazenador com estado em memória, exercitando todos os caminhos felizes e respostas inválidas para documentos e cursos complementares.

### Impacto da revisão
Permite a entrega imediata e com alta qualidade da Issue #398 [F11.7].

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Cobertura de segurança e autorização | Priorizada | Garantia de rejeição 401/404 em acessos indevidos e IDOR | Contrato do middleware e handlers de documento |
| Robustez de validação | Priorizada | Garantia de rejeição 422 em payloads defeituosos ou inválidos | Validações Pydantic e regras de domínio |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Tempo de execução | < 1 segundo | Testes 100% em memória sem I/O de disco ou rede |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Segurança | Vazamento de arquivos ou documentos de terceiros via IDOR | Crítica | Usuários da plataforma |
| Estabilidade da API | Quebra não detectada na validação de payloads | Alta | Clientes frontend e integradores |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Isolamento em memória | Não exercita drivers de disco do S3/GCS no teste | Teste de infraestrutura de nuvem | Alta (testes de storage real pertencem a nível operacional) |

## Riscos e efeitos de segunda ordem

- Risco de dessincronização de campos de DTO caso a API sofra refatoração futura: Mitigado pois o teste consome diretamente a fábrica `create_app` e os DTOs do projeto.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Testes cobrem todas as respostas e passam | Relatório do `python3 -m unittest` no ambiente `tests` | Execução via Nix develop | Falha ou erro de asserção |
| Ausência de regressões | Todos os 100+ testes do backend continuam verdes | Execução da suíte completa | Quebra de qualquer teste existente |

## Handoffs e atividades posteriores

- Execução da skill especializada `$integration-system-testing-v1` para criar `src/backend/tests/test_integracao_crud_informacoes_complementares.py`.
- Criação de Pull Request associado à Issue #398 contra a branch `dev`.

## Síntese

A análise valida que o teste de integração para o CRUD de informações complementares (Issue #398) deve exercitar o pipeline ASGI de ponta a ponta com autenticação por sessão, cobrindo criação, leitura/verificação e exclusão de documentos e cursos complementares, com ênfase especial em oráculos de respostas inválidas (401, 404, 409, 422).
