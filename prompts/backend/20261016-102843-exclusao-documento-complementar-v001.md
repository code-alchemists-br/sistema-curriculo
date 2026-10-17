---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-16T10:28:43-03:00"
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
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: Markdown/Mermaid ER
      analysis_scope: selected-section
      locator: "Tabela DOCUMENTO e campos de metadados"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/itens_perfil.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "Documento e DocumentoId"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "DocumentoId e UsuarioId"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "Portas de repositório e contratos"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "Registro de routers na aplicação"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/metadata.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "Registro de metadata ORM"
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend]
  confidence: high
  rationale: "A demanda trata de regras de negócio, aplicação e infraestrutura/API exclusivas do backend do sistema de currículo."
classification:
  sphere: backend
  concerns: [business-rules, api, persistence]
  decision_kind: feature-decomposition
  scope: subsystem
  lifecycle: design
  urgency: normal
  uncertainty: low
  reversibility: reversible
  risk: low
---

# Análise de decisão — exclusão de documento complementar

## Solicitação original

Implementar a exclusão de documento complementar (Issue #108). Disponibilizar endpoint autenticado `DELETE /documentos/{id}` para permitir que estudantes excluam documentos complementares (comprovantes, certificados em PDF/imagem) de seu perfil. A exclusão deve validar a propriedade do documento (apenas o titular pode excluir), tratar exclusão no repositório relacional, garantir que o status `204 No Content` seja retornado em caso de sucesso e produzir respostas estáveis para documento inexistente (`404 Not Found`) ou não autenticado (`401 Unauthorized`), com suíte completa de testes unitários isolados.

## Informações complementares

Nenhuma identificada.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Criação inicial | N/A | v001 | Análise de decisão inicial para a Issue #108 | Inicia a linhagem de decisão da exclusão de documento complementar |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `docs/modelagem_der.md` | supporting | diagram-model | schema-contract | Markdown/Mermaid ER | Tabela DOCUMENTO e campos | working-tree |
| `src/backend/domain/itens_perfil.py` | primary | source-code | production | Python | Documento e DocumentoId | working-tree |
| `src/backend/domain/value_objects.py` | supporting | source-code | production | Python | Value objects DocumentoId e UsuarioId | working-tree |
| `src/backend/application/ports.py` | primary | source-code | production | Python | Definição de portas de repositório | working-tree |
| `src/backend/api/factory.py` | supporting | source-code | production | Python | Configuração da fábrica FastAPI | working-tree |
| `src/backend/infrastructure/persistence/sqlalchemy/metadata.py` | supporting | source-code | production | Python | Base ORM SQLAlchemy | working-tree |

### Limites da evidência dos artefatos

Os arquivos do repositório foram inspecionados em sua versão mais recente na branch `dev`. A entidade `Documento` e o identificador `DocumentoId` já se encontram no domínio, enquanto as camadas de orquestração de aplicação, persistência e interface HTTP ainda não possuíam o caso de uso de exclusão implementado.

## Problema enriquecido

### Resultado desejado

Disponibilizar endpoint autenticado `DELETE /documentos/{documento_id}` que permita a remoção segura de um documento complementar pelo seu proprietário, persistindo a exclusão (soft-delete através do preenchimento de `deleted_at`, conforme modelagem do DER) e retornando `204 No Content` sem corpo de resposta. Proteger contra vulnerabilidades de enumeração/IDOR disparando `404 Not Found` caso o documento não exista ou pertença a outro estudante.

### Atores e interesses

- **Estudante autenticado:** Deseja gerenciar seu perfil e remover documentos que não considera mais necessários ou pertinentes.
- **Sistema de Segurança:** Exige que a operação ocorra exclusivamente sob a identidade comprovada da sessão e não permita enumeração de recursos alheios.
- **Camada de Aplicação:** Deseja isolamento completo de persistência e HTTP através de portas (`RepositorioDocumento`) e contratos desacoplados.

### Evidências e fatos observados

- O DER em `docs/modelagem_der.md` define a tabela `DOCUMENTO` com colunas `id`, `usuario_id`, `nome_arquivo`, `tipo_arquivo`, `url_armazenamento`, `created_at` e `deleted_at`.
- As entidades `Documento` e `DocumentoId` já estão presentes no domínio em `src/backend/domain/itens_perfil.py` e `src/backend/domain/value_objects.py`.
- O padrão arquitetural adotado no repositório (ex.: `exclusao_formacao_academica.py`, `exclusao_versao_curriculo.py`) utiliza soft delete ou exclusão controlada com resposta `204 No Content` e erro uniforme `404 Not Found` para documento inexistente ou alheio.

### Hipóteses

- O preenchimento da coluna `deleted_at` com o timestamp UTC corrente é suficiente para invalidar consultas subsequentes no repositório relacional.
- Na fatia vertical de documentos complementares, a exclusão do registro em `documentos` é independente de eventuais associações futuras com versões de currículo.

### Perguntas em aberto

Nenhuma identificada.

### Escopo

- Adição de invariantes e validações em `Documento.__post_init__` em `src/backend/domain/itens_perfil.py`.
- Criação da exceção `DocumentoNaoEncontrado` e DTO `ExcluirDocumentoEntrada`.
- Definição da porta abstrata `RepositorioDocumento` em `src/backend/application/ports.py`.
- Implementação do caso de uso `ExcluirDocumento` em `src/backend/application/exclusao_documento.py`.
- Criação do modelo ORM `DocumentoRegistro` e repositório `RepositorioDocumentoSqlAlchemy`.
- Criação da migração Alembic para a tabela `documentos`.
- Criação da rota `DELETE /documentos/{documento_id}` em `src/backend/api/documento.py` e integração na fábrica `create_app` em `src/backend/api/factory.py`.
- Implementação de testes unitários em 100% das camadas (domínio, aplicação, infraestrutura e API).

### Fora do escopo

- Upload físico de arquivos e provedores remotos de storage em nuvem (S3/GCS).
- Seleção e desvinculação de documentos em currículos (`CURRICULO_DOCUMENTO`).
- Telas ou componentes frontend.

### Critérios de sucesso

- Testes unitários com doubles cobrindo cenários de sucesso (204), documento inexistente (404), documento de outro usuário (404), usuário não autenticado (401) e indisponibilidade (503).
- 100% de conformidade com os linters (`ruff check` e `ruff format`).
- Aprovação dos 4 jobs de integração contínua do GitHub Actions.

## Restrições aplicáveis

- **Clean Architecture:** Camada de domínio e aplicação sem dependências externas de frameworks ou ORM.
- **Docstrings Triplas:** Toda função, método, classe e DTO deve conter docstrings explicando o que faz, como faz e qual finalidade atende.
- **Rastreabilidade:** Tags `# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001` em todos os trechos novos.
- **Ambientes Nix:** Nix obrigatório para backend e quality; Git e gh fora do Nix.

## Classificação comentada

- **sphere: backend**: A demanda envolve exclusivamente componentes do backend.
- **concerns: [business-rules, api, persistence]**: Cobre a regra de propriedade e validações (business-rules), o endpoint HTTP (api) e a tabela relacional com soft delete (persistence).
- **decision_kind: feature-decomposition**: Organização da funcionalidade em camadas da Clean Architecture.

## Decisão de roteamento

- **root:** prompts
- **selected_directory:** prompts/backend
- **considered_directories:** [prompts/backend]
- **confidence:** high
- **rationale:** Trata-se de implementação de casos de uso, entidades e adapters no backend.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| Segurança e IDOR | Alta | Uniformidade 404 para inexistente ou alheio | Impede vazamento da existência de documentos de outros usuários |
| Desacoplamento Arquitetural | Alta | Portas tipadas em Application e doubles para testes | Permite isolamento determinístico e evolução independente de adapters |
| Consistência de Schema | Média | Soft-delete via `deleted_at` compatível com o DER | Garante integridade do modelo relacional estabelecido |

## Alternativas consideradas

### Alternativa A: Exclusão lógica (Soft Delete) via coluna `deleted_at` com proteção IDOR (Recomendada)
- O caso de uso busca o documento pelo `documento_id`. Se não encontrar ou o `usuario_id` for divergente, lança `DocumentoNaoEncontrado` (404).
- O repositório marca `deleted_at = agora` e atualiza a sessão, omitindo documentos deletados em consultas futuras.

### Alternativa B: Exclusão física (Hard Delete) via SQL `DELETE`
- Remove a linha fisicamente da tabela.
- Desvantagem: Perde histórico de auditoria e diverge do campo `deleted_at` planejado no DER.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Confiança | Base |
|---|---:|---:|---:|---|---|
| Conformidade com o DER | Alta | Total | Parcial (ignora deleted_at) | Alta | docs/modelagem_der.md |
| Segurança contra IDOR | Alta | Total | Total | Alta | Práticas do sistema |
| Rastreabilidade / Auditoria | Média | Total | Nenhuma | Alta | Requisitos de segurança |

## Histórico e decisão atual

### Decisão da versão anterior
N/A (versão inicial).

### Decisão recomendada nesta versão
Adotar a **Alternativa A**: Exclusão lógica com preenchimento de `deleted_at` na persistência relacional, orquestrada por caso de uso desacoplado que valida o proprietário e responde com `204 No Content` na API HTTP.

### Impacto da revisão
N/A.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Segurança | Maximizada | Eliminação de vazamento de existência de recursos alheios | Disparo indistinguível de DocumentoNaoEncontrado |
| Isolamento | Maximizada | Testabilidade completa sem banco de dados real | Uso de mocks/doubles na camada de aplicação e API |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Desempenho | Latência mínima em queries | Índices em `id` e `usuario_id` e filtro simples em `deleted_at IS NULL` |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Segurança | Exposição de metadados privados por enumeração | Alta | Estudantes da plataforma |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Segurança | Ausência de diferenciação entre inexistente e não autorizado no 404 | Detalhamento do erro ao cliente | Plenamente aceitável e recomendável |

## Riscos e efeitos de segunda ordem

- *Risco:* Sobrecarga futura de registros deletados na tabela `documentos`.
- *Mitigação:* Índices parciais ou políticas de purga assíncrona podem ser introduzidos se necessário.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Exclusão segura e isolada | 100% de sucesso nos testes unitários | Execução via Nix backend | Falha em testes de concorrência ou segurança |

## Handoffs e atividades posteriores

- Implementação do núcleo de domínio e caso de uso através de `backend-domain-orchestration-v2`.
- Implementação dos adaptadores de infraestrutura e rotas HTTP através de `backend-adapters-drivers-v2`.
- Verificação automatizada nos gates Nix e abertura do Pull Request.

## Síntese

A análise aprova o desenho técnico para a exclusão de documentos complementares, estabelecendo o contrato de rota `DELETE /documentos/{documento_id}`, o caso de uso `ExcluirDocumento` e a persistência relacional em conformidade com o DER e Clean Architecture.

Arquivo criado em prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md. Avalie se o local escolhido é de fato o mais adequado.
