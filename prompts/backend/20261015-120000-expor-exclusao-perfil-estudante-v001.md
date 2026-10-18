---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-15T12:00:00-03:00"
lineage:
  mode: initial
  root: null
  supersedes: null
  change_type: initial
  secondary_change_types: []
  decision_impact: new
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "8d18c5b646b60f295d04587bf048f3ea3842a62f"
      availability: available
    - path: src/backend/api/perfil_estudante.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "8d18c5b646b60f295d04587bf048f3ea3842a62f"
      availability: available
    - path: src/backend/api/middleware_autenticacao.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "8d18c5b646b60f295d04587bf048f3ea3842a62f"
      availability: available
    - path: src/backend/application/acesso_estudante.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "8d18c5b646b60f295d04587bf048f3ea3842a62f"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_sessao.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "8d18c5b646b60f295d04587bf048f3ea3842a62f"
      availability: available
    - path: docs/requisitos-seguranca.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "4.9 a 4.16"
      content_state: commit
      revision: "8d18c5b646b60f295d04587bf048f3ea3842a62f"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "8d18c5b646b60f295d04587bf048f3ea3842a62f"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "8d18c5b646b60f295d04587bf048f3ea3842a62f"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/revisao]
  confidence: high
  rationale: "A decisão define a rota HTTP, o fluxo de acesso e a consulta de sessões do backend."
classification:
  sphere: engineering
  concerns: [security, privacy, architecture]
  decision_kind: design
  scope: component
  lifecycle: evolution
  urgency: normal
  uncertainty: low
  reversibility: moderate
  risk: high
---

# Análise de decisão — expor exclusão de perfil do estudante

## Solicitação original

Issue GitHub nº 90: `Expor exclusão de perfil do estudante`. Tarefa da fatia
vertical, com testes unitários pertinentes. Decisão de produto informada pelo
responsável: não usar identificador na URL e realizar a exclusão lógica (soft
delete) somente do usuário autenticado.

## Artefatos analisados

- Decisão anterior `20260920-202606-edicao-exclusao-perfil-estudante-v001`,
  que definiu exclusão lógica por `deleted_at`, idempotência e identidade vinda
  de contexto autenticado.
- `DELETE /estudantes/{usuario_id}` já existente, que usava o UUID da URL e
  dependia somente do middleware para comparar proprietário.
- `AcessarEstudante`, que não verificava exclusão lógica.
- `RepositorioSessaoSqlAlchemy.obter_usuario_ativo`, que validava sessão sem
  considerar o estado do usuário.

## Problema enriquecido

### Resultado desejado

O estudante autenticado exclui logicamente o próprio perfil e, a partir desse
instante, o perfil fica indisponível aos fluxos de acesso: novas tentativas de
login falham e as sessões já emitidas deixam de autenticar.

### Evidências e fatos observados

- A decisão anterior exige que a identidade venha de contexto autenticado e
  que a exclusão torne o perfil indisponível aos fluxos de acesso.
- O login aceitava conta com `deleted_at` preenchido.
- A consulta de sessão ativa não fazia junção com `usuarios`; um cookie emitido
  antes da exclusão continuava válido.
- Já existe a convenção `DELETE /sessao/atual` para operar sobre o recurso da
  sessão corrente sem identificador.

### Escopo

- Substituir `DELETE /estudantes/{usuario_id}` por `DELETE /estudantes/atual`,
  usando apenas o principal instalado pelo middleware.
- Remover o cookie de sessão na resposta bem-sucedida.
- Rejeitar login de perfil excluído com a mesma falha de credenciais inválidas.
- Descartar sessões de usuários com `deleted_at` na consulta de sessão ativa.
- Cobrir os comportamentos com testes unitários.

### Fora do escopo

- Purga física, cascatas sobre currículos e itens, retenção e anonimização.
- Reutilização do e-mail de perfil excluído.
- Reautenticação por senha antes da exclusão.

## Alternativas consideradas

### Alternativa A — `DELETE /estudantes/atual` com principal da sessão

Sem UUID na URL, não há identificador fornecido pelo cliente a comparar ou a
forjar. Segue a convenção de `/sessao/atual`.

### Alternativa B — manter `DELETE /estudantes/{usuario_id}` com comparação

Mantém simetria com `PUT` e `GET`, mas continua aceitando identificador do
cliente e duplica a checagem entre middleware e handler.

### Alternativa C — revogar somente a sessão corrente

Exige nova porta de revogação no caso de uso e deixa ativas as demais sessões
do estudante; a filtragem por `deleted_at` cobre todas sem nova escrita.

## Decisão recomendada nesta versão

Adotar a Alternativa A, complementada pela filtragem de sessões por perfil
ativo na consulta persistida e pelo bloqueio no caso de uso de acesso. O
middleware deixa de tratar `DELETE` de perfil como rota com UUID; a rota nova
continua privada por padrão e recebe o principal em `request.state`.

## Riscos e efeitos de segunda ordem

- Clientes que chamavam `DELETE /estudantes/{uuid}` passam a receber 405; não
  há uso no frontend atual.
- A junção adiciona uma leitura de `usuarios` por requisição autenticada,
  feita por chave primária.

## Validação da decisão

- Handler exclui o perfil do principal, devolve 204 e expira o cookie.
- Ausência de principal resulta em 401; perfil ausente em 404 genérico.
- OpenAPI expõe `DELETE /estudantes/atual` e não expõe DELETE por UUID.
- Middleware exige sessão e encaminha a exclusão sem comparação de UUID.
- Login de perfil excluído falha sem conferir senha.
- Consulta de sessão contém junção com `usuarios` e `deleted_at IS NULL`.

## Síntese

A exclusão do perfil passa a operar exclusivamente sobre o estudante
autenticado, sem identificador na URL, e torna o perfil imediatamente
indisponível para login e para sessões existentes, sem purga física.
