---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v006"
status: proposed
created_at: "2026-10-13T00:37:34-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261012-230050-expor-consulta-dados-pessoais-estudante-v001.md
  supersedes: prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md
  change_type: scope-change
  secondary_change_types: [reassessment]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: "Solicitação do usuário: card Expor consulta de dados pessoais do estudante"
      relationship: primary
      representation: prose
      function: documentation
      format: text
      analysis_scope: whole-file
      locator: null
      content_state: external
      revision: null
      availability: available
    - path: "Complemento do usuário: campos e identidade pela sessão de task94"
      relationship: primary
      representation: prose
      function: documentation
      format: text
      analysis_scope: whole-file
      locator: null
      content_state: external
      revision: "registrado em v005; revisto por informação posterior"
      availability: available
    - path: "Complemento do usuário: não precisa integrar task94"
      relationship: primary
      representation: prose
      function: documentation
      format: text
      analysis_scope: whole-file
      locator: null
      content_state: external
      revision: "mensagem desta revisão"
      availability: available
    - path: "Complemento do usuário: id na rota"
      relationship: primary
      representation: prose
      function: documentation
      format: text
      analysis_scope: whole-file
      locator: null
      content_state: external
      revision: "mensagem desta revisão"
      availability: available
    - path: prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "artefato v005 no workspace, não rastreado no Git"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF02 e RF13"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: docs/matriz_testes.md
      relationship: supporting
      representation: prose
      function: test
      format: Markdown
      analysis_scope: selected-section
      locator: "CT-RF02-01 e CT-RF13-01/02/03"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RNF04 e verificação de acesso sem autenticação/autorização"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: docs/requisitos-seguranca.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "seções 3.2, 3.3, 3.5, 3.6 e requisitos RF-AUTZ-01/03/06/07/08/09/10"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/api/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 530e8f6"
      availability: available
    - path: src/backend/api/cadastro_acesso.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "rotas de cadastro e login; ausência de emissão/resolução de sessão"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "injeção de executores e registro de routers"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/main.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/application/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ConsultarPerfilEstudante e entrada por UsuarioId"
      content_state: working-tree
      revision: "working-tree based on 530e8f6"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "obter_por_id"
      content_state: working-tree
      revision: "working-tree based on 530e8f6"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "campos pessoais e mapping ORM"
      content_state: working-tree
      revision: "working-tree based on 530e8f6"
      availability: available
    - path: prompts/backend/20261011-102943-rejeicao-requisicoes-sem-credenciais-validas-v004.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "inventário de rotas GET e ausência de autenticação na branch"
      content_state: commit
      revision: "v004, baseado em 530e8f6"
      availability: available
    - path: "Estado Git local"
      relationship: context
      representation: structured-data
      function: unknown
      format: Git metadata
      analysis_scope: selected-section
      locator: "branch task88, HEAD 530e8f6, status do working tree"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A decisão mantém o foco na rota e no contrato de consulta do backend; requisitos funcionais e de segurança sustentam as regras de acesso."
classification:
  sphere: engineering
  concerns: [security, privacy, data]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: high
---

# Análise de decisão — consulta de dados pessoais do estudante por ID

## Solicitação original

`$decision-analysis-v4 Faça uma analise para o card Expor consulta de dados pessoais do estudante. Inclua testes unitarios adequados`

## Informações complementares

O usuário definiu anteriormente os campos da consulta e pediu que a identidade viesse da sessão de `task94`: `consultar nome, e-mail, telefone, cidade e contatos profissionais identifique o estudante com a sessão encontrada na task 94`.

Informação posterior do usuário, preservada literalmente: `não preciso da integração com a task94`.

Escolha de localização do recurso, preservada literalmente: `id na rota`.

Solicitação desta revisão, preservada literalmente: `$decision-analysis-v4 revise se é possivel registrar a rota por ID e suas regras de acesso;`.

## Mudanças desde a versão anterior

| Elemento | Versão anterior (v005) | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Fonte da identidade | Sessão de `task94`; ID do estudante não viria do cliente | O ID pode aparecer no path, mas será somente seletor do recurso e deverá ser comparado no servidor com a identidade autenticada | O usuário dispensou a integração com `task94` e escolheu `id na rota` | Muda o contrato HTTP; não elimina RF13 nem a checagem de propriedade |
| Acesso entre contas | A consulta era exclusivamente do próprio perfil derivado da sessão | Usuário comum só consulta se o ID do path corresponder à sua própria identidade autenticada; usuário sem autenticação recebe negação; administrador não ganha acesso amplo automaticamente | Compatibilizar a rota solicitada com RF13, RNF04 e RF-AUTZ | Define regra de autorização para a consulta |
| Status para ID alheio/ausente/excluído | `404` era recomendado para perfil inexistente/excluído | Recomenda-se a mesma resposta genérica `404` para recurso ausente, excluído ou não pertencente ao principal, evitando revelar existência | Reduzir enumeração e divulgação lateral de contas | Recomendação de contrato HTTP a validar |
| Evidência técnica | A v005 avaliou contrato e estado de task88/task94 | Revalidados código e requisitos na branch local `task88`; não há autenticador conectado à API nesta branch | A nova regra exige saber se a identidade autenticada já está disponível | A rota é viável como contrato, mas exige uma fonte de principal autenticado antes de ser segura em produção |
| Decisão | `GET /estudantes/me` baseado em `task94` | Recomenda-se `GET /estudantes/{usuario_id}` com autorização de proprietário no servidor; não confiar no ID isoladamente | Atender ao novo formato solicitado sem contradizer os requisitos de acesso | `decision_impact: revised` |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| Solicitação original do card | Principal | Prosa | Documentação | Texto | Solicitação integral | Externa, desta linhagem |
| Complemento sobre campos e sessão de `task94` | Principal | Prosa | Documentação | Texto | Mensagem integral | Externa, registrada em v005 e reavaliada |
| Complemento “não preciso da integração com a task94” | Principal | Prosa | Documentação | Texto | Mensagem integral | Externa, desta revisão |
| Complemento “id na rota” | Principal | Prosa | Documentação | Texto | Mensagem integral | Externa, desta revisão |
| `prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree, v005 |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF02 e RF13 | Commit `530e8f6` |
| `docs/matriz_testes.md` | Apoio | Prosa | Teste | Markdown | CT-RF02-01 e CT-RF13-01/02/03 | Commit `530e8f6` |
| `docs/requisitos_nao_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RNF04 e verificação de acesso | Commit `530e8f6` |
| `docs/requisitos-seguranca.md` | Apoio | Prosa | Documentação | Markdown | RBAC, usuário comum, propriedade e RF-AUTZ-01/03/06/07/08/09/10 | Commit `530e8f6` |
| `src/backend/api/perfil_estudante.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree baseado em `530e8f6` |
| `src/backend/api/cadastro_acesso.py` | Apoio | Código-fonte | Produção | Python | Rotas de cadastro/login | Commit `530e8f6` |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Injeção de executores e registro de routers | Commit `530e8f6` |
| `src/backend/main.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/application/perfil_estudante.py` | Apoio | Código-fonte | Produção | Python | Caso `ConsultarPerfilEstudante` | Working tree baseado em `530e8f6` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py` | Apoio | Código-fonte | Produção | Python | Query `obter_por_id` | Working tree baseado em `530e8f6` |
| `src/backend/infrastructure/persistence/sqlalchemy/usuario.py` | Apoio | Código-fonte | Produção | Python | Mapping dos campos da consulta | Working tree baseado em `530e8f6` |
| `prompts/backend/20261011-102943-rejeicao-requisicoes-sem-credenciais-validas-v004.md` | Contexto | Prosa | Documentação | Markdown | Inventário da API e lacuna de autenticação | v004, baseado em `530e8f6` |
| Estado Git local | Contexto | Dados estruturados | Metadados | Git | Branch e working tree | `task88`, HEAD `530e8f6` |
| `AGENTS.md` e `src/backend/AGENTS.md` | Contexto | Prosa | Instrução de agente | Markdown | Arquivos completos | Commit `530e8f6` |

### Limites da evidência dos artefatos

A inspeção considera a referência local da branch `task88`, HEAD `530e8f6`, e alterações presentes no working tree; não atualiza nem consulta o remoto. O código atual contém o caso de uso de consulta, query por ID, campos ORM e DTO, mas `perfil_estudante.py` ainda registra somente PUT e DELETE. A API não recebe um principal autenticado: cadastro/login validam credenciais, mas não criam sessão ou token; `main.py` chama `create_app()` sem runtime de autenticação. A implementação de `task94` não foi reavaliada, pois o usuário dispensou sua integração.

## Problema enriquecido

### Resultado desejado

Expor nome, e-mail, telefones, cidade, LinkedIn e currículo Lattes de um estudante em uma rota que receba `usuario_id` no caminho, preservando autenticação, autorização por propriedade e resposta mínima.

### Atores e interesses

- Estudante: consultar somente os dados da própria conta.
- Cliente HTTP: selecionar o recurso por ID, sem determinar por isso a autorização.
- Backend: validar a identidade autenticada e a permissão no servidor antes de devolver dados.
- Administrador: só deve consultar contas alheias quando uma permissão administrativa explícita existir; o papel, por si só, não concede acesso irrestrito.

### Evidências e fatos observados

- O usuário alterou a escolha anterior e dispensou a integração com `task94`, escolhendo ID na rota.
- RF13 exige autenticação para consultar dados pessoais.
- RNF04 exige negar acesso a usuários sem autenticação ou autorização.
- RF-AUTZ-03 limita USER à própria conta; RF-AUTZ-06 exige validação da autorização no servidor; RF-AUTZ-07 proíbe confiar exclusivamente em identificadores do cliente; RF-AUTZ-09/10 estabelecem menor privilégio e negação por padrão.
- A documentação de segurança afirma que ADMIN não deve ser interpretado automaticamente como irrestrito e que as permissões administrativas dependem de necessidade/política.
- A API atual já usa `usuario_id` em PUT/DELETE de perfil, mas essas rotas não demonstram autenticação ou autorização. Reutilizar somente o padrão de path não satisfaz RF13/RNF04.
- A aplicação desta branch não possui um principal autenticado conectado à rota; logo, uma rota pública baseada somente no ID seria tecnicamente simples, mas incompatível com os requisitos.
- O DTO existente limita a resposta a nome, e-mail, telefones, cidade, LinkedIn e Lattes.

### Hipóteses

- A finalidade continua sendo consulta dos próprios dados do estudante, não consulta pública ou diretório de usuários.
- `usuario_id` no path identifica o recurso solicitado; uma identidade autenticada separada determina quem está fazendo a requisição.
- Até que uma permissão administrativa de leitura de dados pessoais seja especificada, a regra será deny-by-default para administradores que tentem ler contas alheias.
- Para reduzir enumeração, usuário alheio, perfil inexistente e perfil excluído podem receber a mesma resposta `404`; esta escolha de status deve ser confirmada no contrato HTTP.

### Perguntas em aberto

- Qual mecanismo disponível na branch fornecerá ao handler o principal autenticado, já que `task94` foi dispensada e o código atual não fornece outro mecanismo?
- A política administrativa continuará negando consulta de dados pessoais de terceiros por padrão, ou existe uma permissão administrativa específica a aprovar?

### Escopo

- Recomendar `GET /estudantes/{usuario_id}` como rota de recurso.
- Exigir autenticação; sem principal autenticado, negar a requisição (`401` recomendado).
- Para papel USER, comparar no servidor o ID do path ao ID do principal autenticado; permitir somente quando forem iguais.
- Nunca tratar o ID do path como prova de identidade ou permissão.
- Negar acesso a IDs de terceiros; até existir permissão administrativa explícita, aplicar deny-by-default também a ADMIN para esse recurso.
- Devolver somente nome, e-mail, telefones, cidade, LinkedIn e currículo Lattes; não expor hash, token, endereço completo ou modelo ORM.
- Responder `404` genérico a perfil inexistente, excluído ou não pertencente ao principal, sujeito à validação do contrato.

### Fora do escopo

- Integrar a implementação de sessão da branch `task94`.
- Criar acesso público por conhecimento de ID ou confiar somente no ID fornecido pelo cliente.
- Conceder acesso global ao papel ADMIN sem permissão específica.
- Consultar formação, experiências, competências, projetos ou currículos.
- Decidir ou implementar um novo mecanismo transversal de autenticação nesta análise.
- Implementar código, infraestrutura ou testes nesta atividade de análise.

### Critérios de sucesso

- O ID da rota seleciona o alvo, mas nunca basta para autorizar a consulta.
- Requisição sem principal autenticado é negada.
- USER só lê o perfil cujo ID corresponde à sua identidade autenticada; tentativa com outro ID é negada sem revelar se a conta existe.
- ADMIN não lê dados de terceiros sem permissão explicitamente concedida.
- Perfil inexistente, excluído e alheio têm resposta indistinguível se for confirmado o status `404` genérico.
- Resposta contém exatamente os seis campos definidos e não inclui hash/token/endereço completo.
- A implementação só é considerada segura quando o ponto de composição da API puder fornecer um principal autenticado verificável, ainda que obtido por mecanismo diferente de `task94`.

## Restrições aplicáveis

- RF13: autenticação necessária para acesso a informações pessoais.
- RNF04: consulta somente por usuários autorizados.
- RF-AUTZ-03/06/07: USER acessa somente seus próprios dados; autorização validada no servidor; identificador do cliente não determina autorização isoladamente.
- RF-AUTZ-08/09/10: permissões administrativas explícitas, menor privilégio e negação por padrão.
- A resposta usa DTO explícito; entidades e modelo ORM não são respostas HTTP.
- Dados consultados devem vir de armazenamento durável e perfis excluídos não devem ser servidos.
- `AGENTS.md` exige testes unitários pertinentes para comportamento novo, executados no ambiente Nix `backend`; testes de integração pertencem ao ambiente Nix `tests`.

## Classificação comentada

`engineering` domina. `security`, `privacy` e `data` são as preocupações centrais: o path contém um identificador controlado pelo cliente, o payload contém dados pessoais e os valores devem vir de armazenamento durável. A incerteza é média porque a regra de propriedade pode ser especificada com evidência forte, mas a fonte de principal autenticado e a permissão administrativa para esse recurso não estão implementadas/definidas na branch atual. O risco permanece alto se o endpoint aceitar IDs sem validação de propriedade.

## Decisão de roteamento

Destino `prompts/backend`, mantendo a linhagem. O objeto continua sendo o contrato e a implementação de leitura HTTP no backend. `prompts/requisitos` foi considerada porque os requisitos de acesso fundamentam a política; contudo, a decisão principal é como a rota deve funcionar. `prompts/revisao` não foi escolhida apenas por se tratar de revisão.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Security | Muito alta | Nenhuma autorização baseada só no ID do path; verificar principal e proprietário no servidor | Evita IDOR e acesso horizontal |
| Privacy | Muito alta | Resposta mínima; não confirmar existência de perfil alheio | Reduz exposição de dados pessoais e enumeração |
| Correctness | Muito alta | ID seleciona o perfil pedido e o acesso corresponde à política | Separa seleção de recurso de autorização |
| Simplicity | Média | Uma rota GET com path de recurso e uma checagem de propriedade | Mantém contrato simples sem dispensar controles |

## Alternativas consideradas

### A — GET por ID com autenticação independente e verificação de propriedade

Criar `GET /estudantes/{usuario_id}`. O middleware/runtime de autenticação fornece o principal; a autorização compara `usuario_id` com o ID do principal para USER. ID alheio, inexistente ou excluído recebe `404` genérico recomendado. ADMIN também é negado por padrão para dados alheios, até existir permissão específica. A opção atende ao pedido do usuário e aos requisitos quando a identidade independente estiver disponível.

### B — GET do próprio perfil sem ID no path

Usar `GET /estudantes/me`, resolvendo o perfil pelo principal autenticado. O contrato reduz risco de seleção divergente e expressa diretamente “meu perfil”, mas não segue a escolha atual do usuário de colocar o ID na rota. Continua dependendo de algum mecanismo de autenticação, que não precisa necessariamente ser `task94`.

### C — GET público por ID sem autenticação ou checagem de propriedade

Devolver dados sempre que o ID existir. É simples de consumir e fácil de implementar com o handler atual, mas viola RF13, RNF04 e RF-AUTZ-03/06/07/09/10. É inviável para dados pessoais.

### D — GET por ID permitindo leitura cruzada por qualquer ADMIN

Tratar o papel ADMIN como autorização universal. A documentação não concede acesso irrestrito automaticamente e deixa permissões administrativas sujeitas a necessidade/política; portanto, acesso cruzado amplo não está aprovado. Só seria alternativa viável após uma permissão administrativa específica.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | A | B | C | D | Confiança | Base |
|---|---:|---:|---:|---:|---:|---|---|
| Security | Muito alta | +2 | +2 | -2 | -1 | Alta | A/B validam principal; C confia em ID; D amplia privilégio sem regra aprovada |
| Privacy | Muito alta | +2 | +2 | -2 | -1 | Alta | A/B podem ocultar existência de perfil alheio; C/D ampliam leitura |
| User-value | Alta | +2 | +1 | +1 | +1 | Média | A respeita escolha de ID na rota mantendo consulta do proprietário |
| Correctness | Muito alta | +2 | +2 | -2 | -1 | Alta | A/B separam identidade e alvo; C/D não asseguram proprietário |
| Simplicity | Média | +1 | +2 | +2 | +1 | Média | B é mais direto; A acrescenta comparação; controles de C são simples, porém inválidos |
| Delivery-speed | Média | 0 | 0 | +2 | 0 | Média | A/B dependem de autenticação; C parece rápido mas não cumpre requisito |

Os valores são ordinais e não são somados. C é descartada por violar restrições duras; D exige permissão administrativa ainda não definida. A e B são seguras quando ligadas a identidade autenticada independente. A é recomendada porque acomoda a escolha de path ID sem tratar esse ID como autoridade.

## Histórico e decisão atual

### Decisão da versão anterior

A v005 recomendou `GET /estudantes/me`, obtendo a identidade do cookie/runtime de `task94` e sem receber ID de proprietário do cliente. Essa recomendação correspondia ao complemento então registrado.

### Decisão recomendada nesta versão

É possível registrar a rota por ID e manter acesso seguro se a API tratar o path apenas como identificador do recurso. Recomendo `GET /estudantes/{usuario_id}` com autenticação obrigatória e verificação server-side: para USER, o ID da rota deve ser igual ao ID do principal autenticado. O usuário não precisa integrar especificamente `task94`, mas ainda é necessário que algum mecanismo autenticado confiável forneça esse principal; o código atual da branch não o faz.

Para reduzir enumeração, recomendo `404` genérico para perfil inexistente, excluído ou pertencente a outro estudante. Requisições sem principal autenticado devem ser negadas, com `401` recomendado. ADMIN não deve obter acesso a contas alheias automaticamente; o acesso exige permissão específica aprovada. O payload continua limitado a nome, e-mail, telefones, cidade, LinkedIn e Lattes.

O contrato é recomendado e fica `proposed`. A implementação segura permanece bloqueada até a API receber identidade autenticada de um mecanismo que não precisa ser `task94`; esta lacuna técnica não autoriza remover RF13 ou confiar no path.

### Impacto da revisão

`revised`: a preferência do usuário por ID na rota substitui o caminho `/me` da v005. A regra de segurança foi mantida e tornada explícita: path ID seleciona o recurso, enquanto identidade autenticada e autorização decidem acesso. A v005 permanece preservada.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Security | prioritized | Impedir leitura de terceiros mesmo com ID conhecido | RF-AUTZ-03/06/07 e RNF04 |
| Privacy | prioritized | Impedir enumeração e serialização de dados internos | Minimização do DTO e resposta genérica recomendada |
| User-value | prioritized | Usar a rota por ID escolhida pelo usuário | Complemento desta revisão |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Simplicity | Um GET para os campos aprovados | Rota por recurso com payload único |
| Least privilege | USER acessa somente seu perfil e ADMIN sem acesso cruzado implícito | Comparação de proprietário e deny-by-default |
| Interoperability | ID explícito seleciona o recurso | UUID no path com resposta DTO estável |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Security | ID conhecido ou enumerado permite acessar conta de terceiro | Alta | Estudantes e operação |
| Privacy | Respostas diferentes revelam que uma conta existe | Alta | Estudantes |
| User-value | Rota não aceita o identificador de recurso esperado pelo cliente | Média | Cliente e frontend |
| Correctness | Consulta retorna perfil diferente do principal autorizado | Alta | Estudantes e produto |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Security | Integrar uma fonte confiável de principal e checar propriedade em cada leitura | Delivery-speed | Necessário por RF13/RNF04; não exige especificamente `task94` |
| Privacy | Usar resposta genérica para IDs alheios, inexistentes e excluídos | Diagnóstico explícito pelo cliente | Aceitável para não revelar existência de perfis |
| Least privilege | Negar leitura administrativa cruzada até aprovação de permissão específica | Flexibilidade operacional | Aceitável conforme deny-by-default da documentação |

## Riscos e efeitos de segunda ordem

- Um ID de UUID pode ser difícil de adivinhar, mas isso não é controle de autorização; vazamento, logs, URLs ou enumeração tornam o ID acessível.
- Reutilizar o padrão de PUT/DELETE atual sem uma dependência de principal repetiria uma lacuna existente, não uma política segura.
- A API não tem atualmente fonte autenticada para comparar com o path. Implementar apenas a rota deixaria a segurança incompleta.
- Conceder acesso amplo a ADMIN pode expor dados além da necessidade; a documentação exige permissão explícita e menor privilégio.
- `404` para mismatch, inexistente e excluído reduz enumeração, mas pode dificultar suporte; qualquer resposta mais específica deve ser avaliada contra privacidade.
- Autorização deve ocorrer no servidor e antes de serializar qualquer dado pessoal.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Path ID não concede autorização | Sem principal recebe `401`; principal A tentando ID B não recebe dados | Teste de API com autenticação válida/inválida e dois estudantes sintéticos | ID B obtém resposta de sucesso sem ser de A |
| Proprietário pode consultar seu perfil | Principal A requisita ID A e recebe os seis campos permitidos | Teste de aceitação/integrado e inspeção do DTO | Campo faltante ou extra |
| Conta alheia não é enumerável | Mismatch, perfil inexistente e excluído têm mesma resposta genérica | Comparar status e corpo em testes de API | Resposta distingue existência/estado de terceiros |
| ADMIN não recebe privilégio implícito | Sem permissão específica, leitura cruzada é negada | Teste de autorização por papel/permissão | ADMIN lê perfil de USER sem grant explícito |
| Um mecanismo diferente de task94 pode fornecer o principal | Composição da API injeta principal autenticado validado | Revisão de arquitetura e integração do mecanismo escolhido | Handler depende somente do path ou de identidade enviada no corpo/query |

## Handoffs e atividades posteriores

- `$backend-adapters-drivers-v2`: implementar GET `/estudantes/{usuario_id}`, DTO e tradução HTTP somente após existir principal autenticado fornecido pela composição.
- `$backend-domain-orchestration-v2`: manter o caso de uso de consulta com perfil ausente/excluído tratado como não encontrado; a autorização do principal deve permanecer na borda/transversal definida.
- Autenticação/segurança: escolher ou integrar uma fonte confiável de principal autenticado diferente de `task94`, caso a dispensa de `task94` permaneça; não aceitar ID do cliente como identidade.
- Produto/gestão: confirmar a resposta genérica 404 e se haverá alguma permissão administrativa específica para leitura de dados pessoais.
- Testes unitários: handler/DTO deve provar que principal e path são comparados e que payload não contém hash/token; testes de API devem cobrir sem sessão, próprio ID, ID alheio, inexistente, excluído e ADMIN sem permissão.
- `$integration-system-testing-v1`: validar a rota com autenticação real implementada e banco descartável; não substituir a autorização por doubles em teste de aceitação.
- Frontend: consumir o endpoint e lidar com 401/404 após o contrato ser aprovado.

## Síntese

Sim, a rota pode ser registrada por ID: `GET /estudantes/{usuario_id}`. O ID no path deve apenas selecionar o perfil; a autorização precisa usar um principal autenticado independente. USER só acessa o próprio perfil, o servidor compara IDs, e ADMIN não ganha acesso a terceiros sem permissão específica. Recomendo 401 sem identidade e 404 genérico para perfil alheio, inexistente ou excluído. Essa abordagem atende à escolha do usuário e preserva RF13, RNF04 e RF-AUTZ. Não é seguro implementar a rota confiando somente no ID: a branch atual não conecta principal autenticado à API. A integração de `task94` não é obrigatória, mas outro mecanismo autenticado precisa existir antes da entrega.
