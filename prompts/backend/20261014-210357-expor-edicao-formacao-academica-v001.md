---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-14T21:03:57-03:00"
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
    - path: prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "Contexto de cadastro já implementado e regras vigentes referidas nesta demanda"
      content_state: working-tree
      revision: "v003; artefato de apoio, fora da linhagem desta análise"
      availability: partial
    - path: src/backend/domain/itens_perfil.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "FormacaoAcademica, NivelFormacaoAcademica e StatusFormacaoAcademica"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioFormacaoAcademica e contratos de repositórios de perfil/currículo"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "EditarVersaoCurriculo, entrada e CurriculoNaoEncontrado"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "handler PUT, DTO de edição e mapeamento HTTP"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/middleware_autenticacao.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "identidade validada em request.state.usuario_id e regra para recursos por usuário"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/formacao_academica.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "DTOs, rota de cadastro, obtenção do proprietário pela sessão e resposta"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_formacao_academica.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/formacao_academica.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "modelo, constraints e conversões entre registro e entidade"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261014_0007_criar_formacoes_academicas.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python/Alembic
      analysis_scope: selected-section
      locator: "colunas e CHECKs da tabela formacoes_academicas"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_api_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "testes do handler PUT de edição"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_application_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "testes do caso de uso de edição"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: Markdown/DER
      analysis_scope: selected-section
      locator: "entidade FORMACAO_ACADEMICA"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF02 e detalhamentos ainda necessários"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/contrato-credenciais-sessao.md
      relationship: context
      representation: prose
      function: schema-contract
      format: Markdown
      analysis_scope: selected-section
      locator: "identidade do proprietário da sessão e acesso a recursos autenticados"
      content_state: working-tree
      revision: null
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "O objeto central é a edição de um recurso do backend; prompts/backend contém a análise de cadastro usada como apoio, mas esta é uma linhagem nova."
classification:
  sphere: engineering
  concerns: [domain, architecture, security]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — expor edição de formação acadêmica

## Solicitação original

`$decision-analysis-v4 Implementar "Expor edição de formação acadêmica". Task para o back-end. Identifique as necessidades e siga de acordo com as documentações, os requisitos e o que já está implementado.

## Contexto (já implementado, não reabrir)

O cadastro de formação acadêmica está implementado e descrito em prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md (usar como artefato de apoio, sem revisá-lo; esta é uma nova linhagem). Isso inclui:
- Domain: enums NivelFormacaoAcademica e StatusFormacaoAcademica, constantes públicas de tamanho, `FormacaoAcademica` com invariantes (strip, 1 a 200, sem controle, coerência entre status e data_fim).
- Application: `CadastrarFormacaoAcademica` e sua entrada tipada.
- API: `POST /formacoes-academicas`, DTOs explícitos, 201, proprietário só pela sessão, 422 com mensagem segura.
- Persistência: modelo SQLAlchemy, repositório concreto, migration 20261014_0007 com CHECKs.

Regras de negócio vigentes que a edição deve respeitar sem mudança: enums, limites de texto, e a coerência de `data_fim` (em_andamento e interrompido com fim opcional, concluido com fim obrigatório, fim nunca anterior ao início, datas futuras permitidas).

## O que investigar

- Se já existe algum caso de uso, porta ou rota de edição/atualização para outros itens do perfil (experiência profissional, competência) e qual o padrão adotado (PUT ou PATCH, resposta, tratamento de não encontrado e de propriedade). Siga esse padrão, a menos que contrarie o contrato de sessão.
- O que falta no Domain/Application para editar: método de alteração na entidade preservando as invariantes, caso de uso de edição, e métodos novos no `RepositorioFormacaoAcademica` (obter por id, atualizar). Avalie o impacto no repositório concreto e nos testes existentes.
- Como identificar o registro e garantir a propriedade: a formação a editar deve pertencer ao usuário da sessão. Recomende o comportamento para registro inexistente e para registro de outro usuário (por exemplo, o mesmo 404 nos dois casos para não revelar a existência), com justificativa.
- Semântica da edição: PUT (substituição completa) versus PATCH (parcial). Recomende uma, considerando que `status` e `data_fim` se validam em conjunto (uma edição parcial pode gerar combinação inválida com o valor já persistido).
- Campos editáveis e imutáveis: id e usuario_id não podem mudar; confirme o restante.
- Se a mudança exige migration ou alteração de CHECKs (esperado: não).
- Concorrência: avalie se a edição simultânea exige controle (versão ou timestamp) ou se last-write-wins é aceitável no contexto atual, sem ampliar o escopo sem necessidade.
- Atualização de docs/modelagem_der.md e docs/requisitos_funcionais.md (RF02), se necessária.

## Escopo

Somente a edição de formação acadêmica pelo próprio estudante autenticado. Fora do escopo: consulta, exclusão, front-end, alteração das regras de negócio vigentes e qualquer mudança nos limites do agregado.

## Instruções

- Recomende, quando possível, as decisões técnicas (PUT ou PATCH, códigos de resposta, tratamento de propriedade) e separe com clareza o que depende de decisão de produto, para eu decidir antes da implementação.
- Indique como a implementação deve ser dividida entre Domain/Application (`$backend-domain-orchestration-v2`) e API/persistência (`$backend-adapters-drivers-v2`), e quais pontos ficam fora das duas skills (documentação, testes de integração).
- Não implemente nada.`

## Informações complementares

O usuário declarou que o cadastro, seus enums, limites, invariantes, API, persistência e migration 20261014_0007 estão implementados e não devem ser reabertos. Esses itens são pré-condições da análise. Também declarou que toda a semântica atual de status e datas deve permanecer: `em_andamento` e `interrompido` aceitam fim opcional, `concluido` exige fim, a data final nunca antecede o início e datas futuras são permitidas.

## Mudanças desde a versão anterior

Nenhuma — análise inicial de uma nova linhagem. A análise do cadastro v003 é somente evidência de apoio e não é revisada nem substituída.

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md` | Apoio | Prosa | Documentação | Markdown | Partes sobre contrato implementado e regras vigentes | Working tree, v003; consultado como apoio, não revisado |
| `src/backend/domain/itens_perfil.py` | Principal | Código-fonte | Produção | Python | Enumerações e entidade `FormacaoAcademica` | Working tree, sem referência de commit registrada |
| `src/backend/application/ports.py` | Principal | Código-fonte | Produção | Python | Porta de formação, portas de experiência, competência e currículo | Working tree, sem referência de commit registrada |
| `src/backend/application/versao_curriculo.py` | Apoio | Código-fonte | Produção | Python | Caso de uso `EditarVersaoCurriculo`, entrada e ausência/propriedade | Working tree, sem referência de commit registrada |
| `src/backend/api/versao_curriculo.py` | Apoio | Código-fonte | Produção | Python | Rota PUT, DTO e mapeamento de resposta/erros | Working tree, sem referência de commit registrada |
| `src/backend/api/middleware_autenticacao.py` | Apoio | Código-fonte | Produção | Python | Sessão validada e identidade em `request.state` | Working tree, sem referência de commit registrada |
| `src/backend/api/formacao_academica.py` | Apoio | Código-fonte | Produção | Python | DTOs, POST, identidade pela sessão e resposta | Working tree, sem referência de commit registrada |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_formacao_academica.py` | Principal | Código-fonte | Produção | Python | Implementação concreta atual | Working tree, arquivo completo consultado |
| `src/backend/infrastructure/persistence/sqlalchemy/formacao_academica.py` | Apoio | Código-fonte | Produção | Python | Modelo, CHECKs e mapeamentos | Working tree, sem referência de commit registrada |
| `src/backend/infrastructure/persistence/alembic/versions/20261014_0007_criar_formacoes_academicas.py` | Apoio | Código-fonte | Produção | Python/Alembic | Definição da tabela e constraints | Working tree, sem referência de commit registrada |
| `src/backend/tests/test_api_versao_curriculo.py` | Apoio | Código-fonte | Teste | Python | Testes de handler PUT | Working tree, seção identificada por busca |
| `src/backend/tests/test_application_versao_curriculo.py` | Apoio | Código-fonte | Teste | Python | Testes do caso de uso de edição | Working tree, seção identificada por busca |
| `docs/modelagem_der.md` | Apoio | Modelo/diagrama | Contrato de schema | Markdown/DER | Campos da formação acadêmica | Working tree, seção consultada |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF02 e detalhamentos | Working tree, seções consultadas |
| `docs/contrato-credenciais-sessao.md` | Contexto | Prosa | Contrato | Markdown | Propriedade e identidade autenticada | Working tree, seção consultada |
| `AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Regras gerais | Workspace |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Arquitetura e regras do backend | Working tree |

### Limites da evidência dos artefatos

O artefato de cadastro foi consultado apenas para validar o contexto declarado pelo usuário, sem revisão nem reabertura de decisões. Os testes de API de experiência e competência não demonstraram rotas de edição; a busca de rotas e contratos disponíveis encontrou cadastro para esses itens. O padrão comparável de edição foi verificado em versões de currículo. As evidências representam o working tree atual, sem fixação de commit. A inspeção das suítes de formação limitou-se aos caminhos existentes e buscas de referências, não a uma revisão integral dos testes.

## Problema enriquecido

### Resultado desejado

Permitir que o estudante autenticado substitua os dados mutáveis de uma formação própria, preservando sua identidade e proprietário e mantendo as invariantes atuais em todas as camadas.

### Atores e interesses

- Estudante autenticado: corrigir ou atualizar instituição, curso, nível, período e situação da própria formação.
- API: receber substituição completa, obter proprietário exclusivamente da sessão e responder sem expor entidades internas nem existência de registros alheios.
- Application e Domain: localizar a formação, proteger o escopo de proprietário e garantir que o novo estado completo continue válido.
- Persistência: buscar, reconstruir, atualizar e devolver a entidade sem assumir regras de domínio nem encerrar a transação por conta própria.
- Mantenedores: manter documentação, testes e contrato coerentes com a regra de status e fim validada em conjunto.

### Evidências e fatos observados

- A entidade `FormacaoAcademica` é `frozen` e suas invariantes são aplicadas na construção: enum válido, textos normalizados e limitados, e `concluido` requer data de fim. `Periodo` carrega o par início/fim.
- `RepositorioFormacaoAcademica` atualmente expõe somente `salvar`; o adapter SQLAlchemy acrescenta o registro e chama `flush`, sem consulta nem atualização.
- A API de formação já obtém o `UsuarioId` de `request.state.usuario_id`; a identidade de proprietário não é aceita do corpo no cadastro.
- Não há rota de edição observada para experiência profissional ou competência. A edição de currículo usa `PUT`, recebe todos os campos editáveis, devolve DTO do recurso e mapeia `CurriculoNaoEncontrado` para 404.
- O caso de uso de currículo consulta por ID e retorna a mesma falha quando ausente ou pertencente a outro usuário, impedindo inferência sobre existência. Seu handler atual recebe proprietário em rota, mas a demanda de formação determina sessão e prevalece sobre esse detalhe.
- A tabela e os CHECKs da formação já armazenam os campos necessários e permitem todas as combinações temporais que a regra atual aceita.
- RF02 já declara que o sistema deve permitir consultar, editar e excluir as informações cadastradas. O DER descreve estrutura e não precisa mudar se não houver alteração de dados ou relações.

### Hipóteses

- A rota de edição usa identificador da formação no caminho, sem identificador do estudante; a sessão é a única fonte de proprietário.
- O retorno representa a formação atualizada, mantendo o padrão do handler PUT de currículo.
- Como a entidade é imutável, um método de domínio pode retornar um novo estado ou alterar os campos de forma controlada; em ambos os casos deve manter `id` e `usuario_id` idênticos e construir/validar o novo conjunto completo.
- Não há necessidade atual de auditoria por campo, histórico de versões ou detecção de edição perdida que justifique versionamento otimista.

### Perguntas em aberto

Nenhuma decisão de produto é necessária para preservar o escopo dado. A recomendação técnica é `PUT` de substituição completa; a revisão/aceitação desta análise deve preceder a implementação. Se o produto desejar edição parcial, histórico ou conflito otimista, isso altera materialmente o contrato e exige revisão desta análise.

### Escopo

- Método de alteração em `FormacaoAcademica` que preserve invariantes.
- Caso de uso e entrada tipada para edição, além de consulta por ID e atualização na porta.
- Handler/DTO/rota autenticados, extraindo proprietário da sessão.
- Implementação concreta SQLAlchemy de busca e atualização.
- Testes unitários de Domain, Application e adapters conforme os limites das skills.
- Testes superiores da composição/API e eventual validação relacional, em atividade separada.
- Revisão textual de RF02 para explicitar a edição autenticada da formação, sem mudar seu requisito geral.

### Fora do escopo

Consulta como funcionalidade pública, exclusão, front-end, mudança de regras de negócio ou limites do agregado, mudança de CHECKs/migration, edição de experiência/competência, autenticação nova, histórico de alterações e controle otimista de concorrência.

### Critérios de sucesso

- Apenas sessão válida pode invocar a rota; a identidade de proprietário é sempre derivada da sessão.
- Registro inexistente e registro alheio produzem o mesmo 404 e mensagem pública indiferenciada.
- Requisição substitui todos os campos mutáveis; cliente não pode definir nem alterar `id` e `usuario_id`.
- A edição aplica enums, `strip`, tamanho 1–200, rejeição de controles e coerência de `status`/`data_fim` como já definido; violação mantém padrão 422 seguro.
- Sucesso devolve 200 com DTO da formação atualizada; não há criação de outro recurso nem migração.
- Concorrência segue last-write-wins nesta entrega.
- Testes unitários cobrem alteração válida, revalidação conjunta, imutabilidade das identidades, ausência/propriedade alheia, mapeamento HTTP e chamadas dos métodos do adapter.
- Testes integrados cobrem composição com sessão real/de dupla apropriada, rota, persistência e isolamento de proprietário conforme skill de teste superior.

## Restrições aplicáveis

- Regras atuais declaradas pelo usuário são fixas: enums e limites existentes; texto normalizado com 1 a 200 caracteres e sem controle; `em_andamento` e `interrompido` com fim opcional; `concluido` com fim obrigatório; fim não anterior ao início; futuro permitido.
- `id` e `usuario_id` não podem ser alterados. Os outros campos da formação são editáveis em conjunto.
- A sessão autenticada é fonte exclusiva de `usuario_id`; contrato antigo com `{usuario_id}` no caminho não pode ser copiado.
- Clean Architecture: regra de estado no Domain, orquestração e portas no núcleo, tradução HTTP na API e SQLAlchemy/mapeamento na infraestrutura.
- Toda alteração comportamental deve receber testes unitários executados no Nix `backend`; integração e níveis acima usam `nix develop .#tests`. A análise não executa esses testes.
- A documentação de função/classe nova deve descrever o que faz, como faz e finalidade.
- Esta análise não autoriza código; status `proposed` exige avaliação da decisão antes de implementação.

## Classificação comentada

`engineering` domina porque a decisão define mudanças coordenadas no domínio, aplicação, API e persistência. `domain` e `architecture` refletem preservação de invariantes e limites de camadas; `security` representa o requisito de ocultar existência de registros alheios e derivar o proprietário da sessão. O escopo é um componente do backend, no ciclo de entrega. A incerteza é média por causa do contrato HTTP ainda recomendado, embora regras de produto e propriedade estejam definidas. O risco é médio: erro de propriedade poderia expor ou alterar dados privados, mas a operação é localizada e reversível.

## Decisão de roteamento

Criar em `prompts/backend`, por tratar diretamente de operação de backend e manter a proximidade semântica com a análise de cadastro usada como apoio. `prompts/requisitos` foi considerada por haver referência a RF02, mas documentação de requisito é handoff secundário; `prompts/revisao` foi descartada porque esta é uma nova linhagem, não revisão. Não foram encontradas instruções específicas em subpastas de `prompts`.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | Alta | Estado completo sempre válido | `status` e `data_fim` dependem um do outro |
| security | Alta | Não permitir mudança nem descoberta de dados alheios | Formação é dado privado do estudante |
| simplicity | Média | Reusar forma de edição já conhecida e evitar camada protocolar nova | Mantém custo e superfície de mudança limitados |
| user-value | Média | Permitir correção dos dados já cadastrados | Atende edição prevista em RF02 |
| modifiability | Média | Portas e adapters explícitos | Habilita evolução sem acoplar domínio ao ORM |

## Alternativas consideradas

- **A — PUT com substituição completa (recomendada):** corpo contém instituição, curso, nível, início, fim e status; a ausência de campo obrigatório rejeita o payload. O domínio valida o conjunto novo inteiro.
- **B — PATCH parcial:** omissões preservam valores atuais e null pode remover `data_fim`. O caso de uso teria de mesclar estado persistido e entrada antes de validar status/período; semântica de campos ausentes e null fica mais complexa.
- **C — PUT parcial com valores default ou reconstruídos na API:** parece reduzir campos do cliente, mas mistura estado atual e entrada no adapter e pode introduzir combinações inválidas fora do domínio. É tecnicamente inferior e não é recomendada.

Para propriedade, consideraram-se devolver 403 para registro alheio e o mesmo 404 para alheio ou ausente. Recomenda-se 404 uniforme porque a distinção não é necessária ao estudante e revelaria a existência de dados privados.

Para concorrência, consideraram-se last-write-wins e versão/timestamp com conflito. Recomenda-se last-write-wins, dado o escopo pequeno, ausência de mecanismo de versão atual e custo adicional de contratos, persistência e UI sem requisito de edição colaborativa.

## Perfil de pagamento comparativo

Valores ordinais: `+2` melhora forte, `+1` melhora moderada, `0` neutro/desconhecido, `-1` piora moderada, `-2` piora forte.

| Dimensão | Prioridade | Alternativa A: PUT completo | Alternativa B: PATCH parcial | Alternativa C: PUT mesclado fora do núcleo | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| correctness | Alta | +2 | 0 | -2 | Alta | PUT valida status e datas como conjunto; PATCH exige mescla precisa; C desloca invariantes para fora do domínio |
| simplicity | Média | +2 | -1 | -2 | Alta | A mantém um contrato explícito e próximo ao PUT de currículo |
| user-value | Média | +1 | +2 | 0 | Média | PATCH pode ser mais cômodo para pequenas alterações; não há requisito de edição parcial |
| security | Alta | +1 | +1 | -1 | Média | Qualquer alternativa pode preservar ownership, mas A reduz semântica de merge sensível na borda |
| modifiability | Média | +1 | 0 | -1 | Média | A expõe campos mutáveis claramente; PATCH requer política de null/omissão mais detalhada |
| reliability | Média | +1 | 0 | -1 | Média | C aumenta risco de descompasso entre dados persistidos, API e domínio |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma. Esta é a primeira versão de uma linhagem nova.

### Decisão recomendada nesta versão

Usar `PUT /formacoes-academicas/{formacao_id}` com substituição completa dos campos editáveis. O handler obtém `usuario_id` de `request.state.usuario_id` e nunca do caminho ou corpo. O caso de uso recebe identidade do usuário e da formação, consulta a formação, trata ausência e propriedade alheia com a mesma falha de não encontrado, chama a operação de edição da entidade e solicita atualização pela porta. Responder 200 com DTO atualizado, 404 idêntico para ausente/alheio, 422 para violação dos dados e 401 conforme middleware para sessão inválida. Reutilizar resposta 503 se a dependência estiver indisponível, conforme o padrão local.

Campos editáveis: `instituicao`, `curso`, `nivel`, `data_inicio`, `data_fim` e `status`. Campos imutáveis: `id` e `usuario_id`. A operação do domínio recebe os seis novos valores e valida a combinação inteira, não altera a identidade nem proprietário.

Não criar migration ou modificar CHECKs: edição usa as mesmas colunas e combinações já representadas. Não adicionar controle de versão; last-write-wins é aceitável nesta entrega. Atualizar RF02 com uma nota de detalhamento que descreva a edição autenticada da formação própria e os campos imutáveis. Não alterar o DER porque estrutura e cardinalidade permanecem iguais.

### Impacto da revisão

Não aplicável; análise inicial. O artefato de cadastro é apoio, sem supersessão ou mudança de sua linhagem.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | Revalidar a relação entre status e fim usando o conjunto completo enviado | Regras explícitas do usuário e invariantes atuais |
| security | prioritized | Ocultar a existência de formação alheia e usar a sessão como identidade | Contrato de sessão e padrão de falha de edição de currículo |
| simplicity | prioritized | Reusar PUT e evitar semântica de merge e controle de concorrência novo | Edição existente de currículo e escopo limitado |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| user-value | Estudante consegue editar todos os dados de conteúdo permitidos | PUT inclui cada campo mutável |
| modifiability | Camadas internas não importam HTTP ou SQLAlchemy | Entrada, porta e adapter concretos separados |
| reliability | Atualização termina no ciclo transacional existente | Repositório faz flush; composição mantém a transação |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | Mistura involuntária entre situação e período ou entrada parcial aplicada incorretamente | Alta | Estudante e consumidores da formação |
| security | Recurso alheio pode ser alterado ou sua existência inferida | Alta | Estudantes |
| simplicity | Semântica de PATCH/controle otimista sem necessidade torna a API e os testes mais difíceis | Média | Mantenedores e clientes da API |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness e simplicity | Cliente precisa enviar todos os campos editáveis mesmo quando muda apenas um | user-value/conveniência | Aceitável enquanto não houver cliente parcial ou requisito de PATCH |
| security | Resposta 404 não distingue “não existe” de “não pertence a você” | clareza operacional para o cliente | Aceitável; evita divulgação desnecessária |
| simplicity | Edições simultâneas podem sobrescrever a gravação anterior | reliability em cenários concorrentes | Aceitável no contexto atual; rever se houver edição simultânea observada ou requisito de histórico |

## Riscos e efeitos de segunda ordem

- Esquecer um campo no DTO PUT pode apagá-lo ou impedir uma edição válida; cobertura unitária deve verificar que todos os campos mutáveis chegam à entidade.
- Recriar a entidade mantendo `id` e `usuario_id` é uma forma compatível com `frozen`; método de domínio deve deixar explícito que identidade e proprietário não se alteram.
- O middleware atual seleciona recursos de estudante por rotas com `{usuario_id}` para fazer comparação preventiva. A nova rota centrada em `{formacao_id}` não deve incorporar proprietário na URL; o handler usa identidade autenticada e o caso de uso verifica propriedade depois da busca. Não relaxar nem ampliar globalmente a política do middleware para acomodar a rota.
- Repositório deve reconstruir a entidade do registro consultado para preservar fronteira ORM/domínio e atualizar a representação mapeada na mesma sessão; não duplicar validações nos CHECKs.
- Sem controle otimista, duas requisições válidas concorrentes podem resultar na última gravação prevalecer. O comportamento é deliberado e reversível.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| PUT cobre todas as necessidades de edição | Fluxo consumidor envia os campos completos | Revisão do contrato e teste do DTO | Cliente real necessita alterar campos isolados |
| 404 uniforme protege a privacidade sem prejudicar UX | Respostas de ausência e de proprietário divergente equivalentes | Teste de caso de uso e integração API | Produto exigir feedback distinto e aceitar divulgação explícita |
| Identidade da sessão atravessa o novo handler | Sessão válida define o usuário da entrada e corpo/path não podem substituí-lo | Testes do adapter e integração com middleware | Rota exigir mecanismo diferente de composição |
| CHECKs atuais cobrem os estados permitidos | Comparar expressões do modelo/migration com regras já fixadas | Revisão do schema e testes de persistência existentes | Nova regra ou constraint surgir; nesse caso revisar schema e migration |
| Last-write-wins é suficiente | Ausência de requisito e de evidência de colisões simultâneas relevantes | Acompanhar uso/relatos operacionais | Perda de edição observada ou requisito de histórico/conflito |

## Handoffs e atividades posteriores

| Atividade | Responsabilidade | Encaminhamento |
|---|---|---|
| Método de edição na entidade e testes unitários de suas invariantes | Domain | `$backend-domain-orchestration-v2` |
| Caso de uso, entrada tipada e evolução da porta de formação (consulta por ID e atualização), com testes unitários do caso de uso | Application | `$backend-domain-orchestration-v2`; a implementação deve declarar a checagem de ownership como fronteira transversal e não alterar política de autenticação |
| DTO/rota PUT, resposta HTTP, binding de identidade da sessão e testes unitários isolados do handler | API | `$backend-adapters-drivers-v2`, reutilizando o contrato de sessão existente |
| Implementação SQLAlchemy de obter por ID e atualizar; testes unitários com sessão/ORM substituídos | Persistência | `$backend-adapters-drivers-v2`; não criar migration |
| Autorização transversal e integração do novo caminho com middleware/sessão | Segurança e composição | Handoff explícito fora das duas skills; reaproveitar o middleware atual e encaminhar mudanças de política a `$cross-cutting-implementation-v1` se forem necessárias |
| Testes de rota por aplicação ASGI, sessão real/de teste, persistência, isolamento e migration integrada (se o verificador de schema exigir) | Testes superiores | `$integration-system-testing-v1`; skill de adapters não os cria |
| Atualizar detalhamento do RF02 e avaliar confirmação de que o DER não muda | Documentação de requisitos/modelagem | Fora das duas skills; atualizar RF02, deixar DER sem alteração justificada |
| Avaliar versionamento otimista, auditoria ou histórico se aparecer requisito | Produto/arquitetura futura | Nova análise antes de ampliar escopo |

Os testes unitários de Domain, Application e adapters pertencem às respectivas skills e ao ambiente Nix `backend`; os testes integrados pertencem à skill de testes superiores e ao ambiente `tests`. A obrigação de testar comportamento vale na futura implementação, não nesta análise.

## Síntese

Recomenda-se `PUT /formacoes-academicas/{formacao_id}` como substituição completa, com 200 e DTO atualizado, 422 para entrada inválida e 404 indistinguível para formação ausente ou alheia. O proprietário vem somente da sessão; `id` e `usuario_id` permanecem imutáveis e os seis demais campos podem ser editados. Domain/Application acrescentam edição e contratos; API/persistência traduzem e executam a operação sem migration. Last-write-wins é suficiente no escopo atual. RF02 merece detalhamento específico; o DER permanece válido. A principal incerteza é a conveniência de PUT completo para futuros clientes; se houver necessidade parcial, produto deve pedir revisão antes da implementação.
