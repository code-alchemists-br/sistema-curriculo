---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-16T07:48:03-03:00"
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
    - path: "github:code-alchemists-br/sistema-curriculo#106"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: selected-section
      locator: "título, descrição e requisitos da funcionalidade de armazenamento de documentos complementares"
      content_state: external
      revision: "consultada em 2026-10-16; sem identificador imutável"
      availability: partial
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: a08488c
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: a08488c
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "tabela DOCUMENTO (linhas 100 a 109)"
      content_state: commit
      revision: a08488c
      availability: available
    - path: src/backend/domain/itens_perfil.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "entidade Documento (linhas 378 a 392)"
      content_state: commit
      revision: a08488c
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "value object DocumentoId (linhas 218 a 237)"
      content_state: commit
      revision: a08488c
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: a08488c
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/
      relationship: supporting
      representation: source-code
      function: configuration
      format: Python
      analysis_scope: selected-section
      locator: "heads de migração existentes em dev"
      content_state: commit
      revision: a08488c
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A decisão abrange o domínio, portas de aplicação, armazenamento e persistência de documentos complementares no backend."
classification:
  sphere: engineering
  concerns: [architecture, data, security]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: low
  reversibility: moderate
  risk: low
---

# Análise de decisão — Armazenamento de Documento Complementar (Issue #106)

## Solicitação original

Issue #106 — “Implementar armazenamento de documento complementar”.
Objetivo: disponibilizar endpoint autenticado `POST /documentos` para que estudantes cadastrem e armazenem documentos complementares (comprovantes, certificados em PDF ou imagem) no perfil. A solução deve desacoplar o armazenamento físico dos metadados através de uma porta abstrata (`ArmazenadorDocumentos`), validar tipos e tamanhos de arquivo permitidos, persistir os metadados Code First no SQLAlchemy e cobrir o fluxo com testes unitários no ambiente Nix.

## Informações complementares

Refinamentos técnicos acordados no plano de execução (`plano_execucao_issue_106.md`):
1. **Contrato de Transporte HTTP (Compatibilidade com Nix):** O endpoint receberá JSON com metadados e conteúdo em Base64 (`nome_arquivo`, `tipo_arquivo`, `conteudo_base64`). Essa abordagem utiliza 100% da biblioteca padrão do Python (`base64`), sem exigir dependências externas como `python-multipart` que não constam em `nix/backend-python-packages.nix`.
2. **Segurança e Validação no Domínio:**
   - Tipos de arquivo permitidos: `application/pdf`, `image/png`, `image/jpeg`.
   - Limite de tamanho: 10 MB (10.485.760 bytes).
   - Sanitização de nome de arquivo: rejeição ou limpeza de caracteres de controle, caminhos relativos (`..`) e espaços excessivos para prevenção de Path Traversal.
3. **Desacoplamento Clean Architecture:**
   - Porta `ArmazenadorDocumentos(Protocol)` na Application: `async def armazenar(conteudo: bytes, nome_arquivo: str, tipo_arquivo: str) -> str`.
   - Porta `RepositorioDocumento(Protocol)` na Application: métodos `salvar` e `obter_por_id`.
   - Porta `GeradorDocumentoId(Protocol)` na Application: `def gerar() -> DocumentoId`.
4. **Constante HTTP 422:** Usar `status.HTTP_422_UNPROCESSABLE_CONTENT` da biblioteca `fastapi.status` / `starlette.status`.
5. **Linearidade do Alembic:** Criar migração Alembic para a tabela `documentos` unificando os heads atuais de `dev` se necessário, ou derivando de forma linear do head ativo.

## Mudanças desde a versão anterior

Nenhuma — versão inicial (`v001`).

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| Issue #106 | primary | prose | documentation | GitHub issue | título, descrição e requisitos de documentos | externa, consultada em 2026-10-16 |
| `AGENTS.md` | context | prose | prompt-instruction | Markdown | arquivo completo | commit `a08488c` |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | Markdown | arquivo completo | commit `a08488c` |
| `docs/modelagem_der.md` | supporting | prose | documentation | Markdown | tabela `DOCUMENTO` (linhas 100–109) | commit `a08488c` |
| `src/backend/domain/itens_perfil.py` | supporting | source-code | production | Python | entidade `Documento` existente (linhas 378–392) | commit `a08488c` |
| `src/backend/domain/value_objects.py` | supporting | source-code | production | Python | value object `DocumentoId` (linhas 218–237) | commit `a08488c` |
| `src/backend/application/ports.py` | supporting | source-code | production | Python | arquivo completo | commit `a08488c` |

### Limites da evidência dos artefatos

A entidade `Documento` e o value object `DocumentoId` já existem no domínio, concebidos na modelagem inicial do perfil e na prévia de versão de currículo. O DER detalha a tabela `DOCUMENTO` com campos `id`, `usuario_id`, `nome_arquivo`, `tipo_arquivo`, `url_armazenamento`, `created_at`, `updated_at`, `deleted_at`. As migrações do Alembic em `dev` possuem múltiplos ramos convergentes (`20261015_0012`).

## Problema enriquecido

### Resultado desejado

Permitir que um estudante autenticado realize upload/armazenamento de um documento complementar via `POST /documentos`, garantindo que:
- O conteúdo seja validado quanto a tipo MIME seguro e tamanho máximo;
- O conteúdo seja persistido no serviço/mecanismo de armazenamento através de porta assíncrona;
- Os metadados sejam persistidos no banco de dados relacional via SQLAlchemy;
- A resposta retorne status `201 Created` com os metadados do documento e a URL de acesso;
- O fluxo seja totalmente testado com doubles em memória no ambiente Nix.

### Atores e interesses

- **Estudante:** Armazenar certificados e comprovantes para anexar ao currículo.
- **Application (Clean Architecture):** Não depender de provedores de storage ou de bibliotecas de transporte multipart.
- **Segurança:** Bloquear envio de executáveis ou arquivos maliciosos e prevenir Path Traversal no nome do arquivo.
- **Persistência:** Registrar os metadados de forma consistente com a tabela `DOCUMENTO` do DER.

### Evidências e fatos observados

- `Documento` e `DocumentoId` já existem no domínio, mas `Documento` não possui validação no construtor.
- O ambiente Nix não possui `python-multipart`, tornando o transporte via payload JSON com Base64 a opção mais limpa, robusta e compatível.
- O DER prevê a tabela `DOCUMENTO` vinculada a `USUARIO(id)` via chave estrangeira `usuario_id`.

### Hipóteses

- O armazenamento de documentos em ambiente de desenvolvimento/teste pode salvar em diretório local ou URI de storage simulada, garantindo determinismo sem infraestrutura em nuvem.
- Em testes unitários, `ArmazenadorDocumentosDouble` operando em memória valida todo o caso de uso e a borda HTTP sem tocar no disco.

### Escopo

1. Regras de domínio em `src/backend/domain/itens_perfil.py`:
   - Constantes de tipos MIME permitidos (`PDF`, `PNG`, `JPEG`) e tamanho máximo (10 MB).
   - Sanitização de nome de arquivo e validação de invariantes.
2. Portas de aplicação em `src/backend/application/ports.py`:
   - `ArmazenadorDocumentos(Protocol)`.
   - `RepositorioDocumento(Protocol)` (métodos `salvar`, `obter_por_id`).
   - `GeradorDocumentoId(Protocol)`.
3. Caso de uso `ArmazenarDocumento` e DTOs em `src/backend/application/cadastro_documento.py`.
4. Implementações de infraestrutura:
   - Gerador UUID4 em `src/backend/infrastructure/identificadores/geradores.py`.
   - Mapeamento ORM `DocumentoRegistro` em `src/backend/infrastructure/persistence/sqlalchemy/documento.py`.
   - `RepositorioDocumentoSqlAlchemy` em `src/backend/infrastructure/persistence/sqlalchemy/repositorio_documento.py`.
   - `ArmazenadorDocumentosLocal` em `src/backend/infrastructure/storage/armazenador_documentos_local.py`.
   - Migração Alembic criando a tabela `documentos`.
5. Rota HTTP `POST /documentos` em `src/backend/api/documento.py` integrada na fábrica de aplicação `factory.py`.
6. Testes unitários puros com `unittest` para domínio, aplicação, repositório e rota.

### Fora do escopo

- Associação de documentos com versões de currículo (`CURRICULO_DOCUMENTO` - escopo futuro).
- Exclusão de documentos (Issue #108).
- Telas de frontend.

### Critérios de sucesso

- `POST /documentos` funcionando com autenticação de sessão e retornando 201 com o DTO esperado.
- Rejeição de tipos não autorizados ou arquivos > 10 MB com `422 Unprocessable Content`.
- Suíte completa de testes unitários passando em `nix develop .#backend --command python -m unittest ...`.
- Linters `ruff check` e `ruff format` 100% limpos em `nix develop .#quality`.

## Restrições aplicáveis

- **Clean Architecture:** Camada de aplicação e domínio 100% livres de dependências externas.
- **Nix Obrigatório:** Testes e linters executados via Nix; Git fora do Nix.
- **Docstrings Triplas:** Obrigatórias em todas as classes, funções e DTOs.
- **Tags de Proveniência:** Presentes em todos os códigos novos e alterados.

## Decisão de roteamento

- Subpasta: `prompts/backend`.
- Justificativa: Modificações restritas ao backend da aplicação (domínio, aplicação, infraestrutura e API).

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| Compatibilidade de ambiente | Alta | Zero dependências adicionais no Nix | Evita necessidade de alterar a infraestrutura do projeto |
| Segurança de arquivos | Alta | Whitelist estrita de MIME types e validação de tamanho | Impede upload de artefatos perigosos |
| Desacoplamento de Storage | Alta | Porta abstrata ArmazenadorDocumentos | Permite plugar S3, GCS, sistema local ou doubles de teste |

## Alternativas consideradas

### Alternativa 1: Upload via JSON com conteúdo em Base64
- Payload JSON contendo metadados e string codificada em Base64.
- Totalmente compatível com FastAPI/Pydantic sem `python-multipart`.
- Perfeita adequação à biblioteca padrão do Python (`base64`).

### Alternativa 2: Upload via multipart/form-data
- Exige instalação de `python-multipart` no Nix.
- Adiciona complexidade na manipulação de `UploadFile` assíncrono.

## Histórico e decisão atual

### Decisão recomendada nesta versão
Adotar a **Alternativa 1**:
1. Implementar o endpoint `POST /documentos` aceitando JSON com `nome_arquivo: str`, `tipo_arquivo: str` e `conteudo_base64: str`.
2. Decodificar e validar o tamanho e tipo no caso de uso/domínio.
3. Persistir os bytes via `ArmazenadorDocumentos` e os metadados via `RepositorioDocumento`.
4. Retornar status 201 com `DocumentoResposta`.
5. Criar a tabela `documentos` e a migração Alembic correspondente.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Validação de MIME types | Testes unitários rejeitando arquivos `.exe` ou tipos não permitidos | `python -m unittest` | Arquivo não autorizado aceito |
| Validação de tamanho | Testes unitários rejeitando payloads > 10 MB | `python -m unittest` | Payload gigante aceito |
| Persistência e Storage | Metadados salvos no repositório e URL devolvida | Teste unitário de use case e API | Falha na geração da resposta |

## Handoffs e atividades posteriores

1. Handoff para `$backend-domain-orchestration-v2`: Regras de domínio e caso de uso `ArmazenarDocumento`.
2. Handoff para `$backend-adapters-drivers-v2`: Implementação do repositório, storage local, migração Alembic e router HTTP.

## Síntese

Decisão tomada para implementar o armazenamento de documentos complementares da Issue #106 desacoplando o storage através de porta assíncrona, utilizando transporte JSON Base64 para total compatibilidade com o ambiente Nix e protegendo a integridade e segurança no domínio com testes unitários determinísticos.
