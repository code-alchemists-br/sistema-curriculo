---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v007"
status: proposed
created_at: "2026-10-13T00:48:54-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261012-230050-expor-consulta-dados-pessoais-estudante-v001.md
  supersedes: prompts/backend/20261013-003734-expor-consulta-dados-pessoais-estudante-v006.md
  change_type: scope-change
  secondary_change_types: [reassessment]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: "Solicitação original: card Expor consulta de dados pessoais do estudante"
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
      revision: "registrado em v005; depois dispensada integração com task94"
      availability: available
    - path: "Complemento do usuário: ID na rota e sessão própria"
      relationship: primary
      representation: prose
      function: documentation
      format: text
      analysis_scope: whole-file
      locator: null
      content_state: external
      revision: "mensagens desta revisão"
      availability: available
    - path: prompts/backend/20261013-003734-expor-consulta-dados-pessoais-estudante-v006.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "artefato v006 no workspace, não rastreado no Git"
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
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RNF04 e seu critério de verificação"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: docs/requisitos-seguranca.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "modelo USER/ADMIN, propriedade e RF-AUTZ-01/03/06/07/08/09/10"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: docs/matriz_testes.md
      relationship: supporting
      representation: prose
      function: test
      format: Markdown
      analysis_scope: selected-section
      locator: "CT-RF13-01/02/03"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/api/cadastro_acesso.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
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
    - path: src/backend/api/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "DTO e handlers atuais de PUT/DELETE; sem GET ou principal autenticado"
      content_state: working-tree
      revision: "working-tree based on 530e8f6"
      availability: available
    - path: src/backend/application/acesso_estudante.py
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
      locator: "ConsultarPerfilEstudante"
      content_state: working-tree
      revision: "working-tree based on 530e8f6"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 530e8f6"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 530e8f6"
      availability: available
    - path: prompts/backend/20261011-102943-rejeicao-requisicoes-sem-credenciais-validas-v004.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "ausência de sessão/autorização na API de task88"
      content_state: commit
      revision: "v004, baseado em 530e8f6"
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
    - path: "Estado Git local"
      relationship: context
      representation: structured-data
      function: unknown
      format: Git metadata
      analysis_scope: selected-section
      locator: "branch task88, HEAD 530e8f6, alterações locais"
      content_state: commit
      revision: "530e8f6"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A nova decisão acrescenta autenticação de backend ao contrato de consulta já roteado para backend; requisitos de segurança permanecem evidência de apoio."
classification:
  sphere: engineering
  concerns: [security, privacy, integration]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: high
---

# Análise de decisão — consulta pessoal com sessão própria

## Solicitação original

`$decision-analysis-v4 Faça uma analise para o card Expor consulta de dados pessoais do estudante. Inclua testes unitarios adequados`

## Informações complementares

O usuário definiu os campos da consulta como nome, e-mail, telefones, cidade e contatos profissionais. Inicialmente indicou usar a sessão de `task94`; depois dispensou aquela integração e escolheu ID na rota.

Instrução adicional, preservada literalmente: `Criar sessão própria`.

A solicitação atual continua o pedido para concluir a consulta pessoal do estudante, agora incluindo o mecanismo de identidade necessário à autorização da rota por ID.

## Mudanças desde a versão anterior

| Elemento | Versão anterior (v006) | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Mecanismo de identidade | A v006 dispensava task94, mas deixava a fonte de principal como handoff e excluía criar mecanismo novo | O usuário escolheu sessão própria; recomenda-se sessão opaca persistida, criada após login e validada no servidor | Resolver o bloqueio de não haver principal autenticado na branch | Amplia escopo de segurança e composição |
| Sessão | Sem contrato local | Token aleatório opaco, somente hash persistido, cookie HttpOnly/Secure/SameSite=Lax, expiração absoluta recomendada de 8 horas e logout revogável | Tornar verificável o ciclo emissão/validação/revogação sem reaproveitar task94 | Nova recomendação proposta, sujeita a aprovação |
| Rota e autorização | GET por ID condicionado a outra fonte autenticada | GET por ID comparado ao principal obtido da sessão própria; USER apenas próprio perfil; ADMIN sem acesso cruzado implícito | Ligar a rota ao mecanismo agora solicitado | Segurança depende de enforcement no servidor |
| Decisão | v006 recomendava rota por ID, mas bloqueava sua implementação segura | v007 propõe sessão própria e especifica ciclo básico para permitir implementação | Instrução do usuário remove a lacuna de escolha de mecanismo | `decision_impact: revised` |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| Solicitação original do card | Principal | Prosa | Documentação | Texto | Solicitação integral | Externa, nesta linhagem |
| Complementos sobre campos, task94, ID na rota e sessão própria | Principal | Prosa | Documentação | Texto | Mensagens integrais registradas na linhagem | Externa, desta conversa |
| `prompts/backend/20261013-003734-expor-consulta-dados-pessoais-estudante-v006.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree, v006 |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF02 e RF13 | Commit `530e8f6` |
| `docs/requisitos_nao_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RNF04 e critério de acesso | Commit `530e8f6` |
| `docs/requisitos-seguranca.md` | Apoio | Prosa | Documentação | Markdown | RBAC, propriedade, autenticação e RF-AUTZ-01/03/06/07/08/09/10 | Commit `530e8f6` |
| `docs/matriz_testes.md` | Apoio | Teste | Documentação | Markdown | CT-RF13-01/02/03 | Commit `530e8f6` |
| `src/backend/api/cadastro_acesso.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Composição de routers e executores | Commit `530e8f6` |
| `src/backend/main.py` | Apoio | Código-fonte | Produção | Python | Inicialização da aplicação | Commit `530e8f6` |
| `src/backend/api/perfil_estudante.py` | Apoio | Código-fonte | Produção | Python | DTO, PUT/DELETE e ausência de GET | Working tree baseado em `530e8f6` |
| `src/backend/application/acesso_estudante.py` | Apoio | Código-fonte | Produção | Python | Validação de credenciais sem sessão | Commit `530e8f6` |
| `src/backend/application/perfil_estudante.py` | Apoio | Código-fonte | Produção | Python | Caso de uso de consulta | Working tree baseado em `530e8f6` |
| `src/backend/infrastructure/persistence/sqlalchemy/usuario.py` | Apoio | Código-fonte | Produção | Python | Mapeamento atual de usuário | Working tree baseado em `530e8f6` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py` | Apoio | Código-fonte | Produção | Python | Query por ID | Working tree baseado em `530e8f6` |
| `prompts/backend/20261011-102943-rejeicao-requisicoes-sem-credenciais-validas-v004.md` | Contexto | Prosa | Documentação | Markdown | Lacuna de autenticação na API | v004, baseado em `530e8f6` |
| `AGENTS.md` e `src/backend/AGENTS.md` | Contexto | Prosa | Instrução de agente | Markdown | Arquivos completos | Commit `530e8f6` |
| Estado Git local | Contexto | Dados estruturados | Metadados | Git | Branch, HEAD e alterações | `task88`, HEAD `530e8f6` |

### Limites da evidência dos artefatos

A inspeção usa o estado local de `task88` em `530e8f6` e alterações presentes no working tree; não atualiza o remoto. A API atual valida login, mas a Application declara que não cria sessão, token ou política de autorização. A fábrica recebe executores de cadastro/acesso sem um gerenciador de sessão, e a aplicação padrão não injeta principal autenticado. O caso de uso de consulta, DTO, mapping de dados e query por ID já estão no working tree, mas não há endpoint GET nem fonte de principal conectado à API.

Não foram consultados provedores externos nem secretos de ambiente. Esta análise não define implantação, rotação de segredo ou configuração live.

## Problema enriquecido

### Resultado desejado

Permitir que estudante consulte os campos pessoais acordados em `GET /estudantes/{usuario_id}` sem permitir que o ID fornecido pelo cliente autorize leitura de contas alheias. A autenticação deve usar sessão própria do sistema, sem dependência da branch `task94`.

### Atores e interesses

- Estudante: login, consultar a própria conta, manter sessão controlada e poder encerrá-la.
- API: emitir e validar sessões, identificar o principal autenticado e aplicar autorização por propriedade antes da resposta.
- Administrador: não recebe acesso a dados pessoais de terceiros sem permissão específica posteriormente aprovada.
- Operação: não armazenar token em claro nem exigir provedor externo.

### Evidências e fatos observados

- RF13 exige autenticação para acesso a dados pessoais.
- RNF04 exige que usuários sem autenticação/autorização não consultem dados protegidos.
- RF-AUTZ-03/06/07 limitam usuário comum à própria conta, exigem autorização no servidor e proíbem confiar somente no ID do cliente.
- RF-AUTZ-08/09/10 determinam permissões administrativas explícitas, menor privilégio e negação por padrão.
- O fluxo atual de acesso confirma credenciais, mas não emite sessão ou token.
- A decisão v006 escolheu path ID como localizador e exige principal independente para compará-lo.
- O usuário pediu uma sessão própria, removendo a necessidade de integrar `task94`.

### Hipóteses

- O provedor local de identidade é o próprio backend: credenciais verificadas pelo caso de uso atual dão origem à sessão.
- Uma sessão server-side com token opaco é preferível neste contexto a token auto-contido sem estado, pois permite revogação imediata no logout.
- Recomenda-se duração absoluta de 8 horas, sem renovação deslizante; esse valor é uma proposta inicial, não requisito pré-existente.
- O cookie será `HttpOnly`, `Secure`, `SameSite=Lax`, restrito a `Path=/`; em desenvolvimento HTTP, qualquer exceção de `Secure` deve ficar restrita a configuração local não versionada e nunca ser o padrão de produção.
- A base de dados de sessões já é a persistência disponível; não será introduzido serviço externo.

### Perguntas em aberto

Nenhuma decisão necessária para uma implementação inicial, caso o usuário aprove esta proposta. A duração absoluta recomendada de 8 horas e o comportamento administrativo devem permanecer explícitos nos critérios e podem ser revistos por produto/segurança.

### Escopo

- Após validação de credenciais bem-sucedida, criar sessão aleatória de alta entropia; não criar sessão em falha de login.
- Enviar token somente em cookie HttpOnly/Secure/SameSite=Lax e nunca no JSON de resposta.
- Persistir somente hash criptográfico do token, `usuario_id`, criação, expiração e estado de revogação; comparar hash do token recebido e rejeitar sessões expiradas ou revogadas.
- Recomendar expiração absoluta após 8 horas, sem renovação deslizante.
- Disponibilizar encerramento da sessão corrente, revogando o registro e removendo o cookie do cliente.
- Derivar o principal exclusivamente da sessão validada no servidor.
- Em `GET /estudantes/{usuario_id}`, USER acessa somente quando o ID do path corresponde ao principal. ADMIN também fica negado para leitura cruzada até permissão específica.
- Responder `401` sem sessão válida e `404` genérico para perfil inexistente, excluído ou pertencente a outro usuário.
- Retornar exatamente nome, e-mail, telefones, cidade, LinkedIn e currículo Lattes.
- Manter casos de uso e domínio sem dependência de FastAPI, cookie, token ou ORM; implementar emissão/validação na fronteira transversal e ligação na composição externa.

### Fora do escopo

- Integrar `task94` ou provedor externo de identidade.
- JWT, OAuth/OIDC ou federação de identidade.
- MFA, recuperação de conta, rotação de senha, gestão de dispositivos ou sessões múltiplas pela interface.
- Acesso administrativo amplo sem grant explícito.
- Expor dados pessoais a partir de endpoint sem sessão.
- Alterar semântica dos casos de uso de perfil já definidos.
- Operar migration ou alterar ambiente compartilhado/produção nesta atividade.

### Critérios de sucesso

- Login válido cria uma sessão persistida e cookie seguro; login inválido não emite cookie nem sessão.
- Banco contém hash do token, não o token bruto.
- Cookie não inclui token em corpo JSON; atributos `HttpOnly`, `Secure`, `SameSite=Lax`, `Path=/` e expiração são verificáveis.
- Ausência, valor inválido, expiração ou revogação resultam em `401`, sem conteúdo pessoal.
- Logout revoga a sessão corrente e remove cookie; sessão revogada deixa de autenticar imediatamente.
- USER autenticado consulta seu próprio ID com sucesso; tentar outro ID recebe `404` sem dados.
- ADMIN não consulta perfil alheio sem autorização específica explícita.
- Perfil inexistente, excluído e alheio produzem `404` genérico equivalente.
- Resposta contém somente os campos acordados, sem hash/token/endereço completo.
- Testes unitários isolam gerador de token, hash/armazenamento e policy; testes integrados cobrem login, cookie, consulta e logout em banco descartável.

## Restrições aplicáveis

- RF13, RNF04 e RF-AUTZ-01/03/06/07/08/09/10 são restrições duras.
- Não confiar no ID do path para autorização; validar no servidor contra principal de sessão.
- Não armazenar nem registrar token em claro; não expor credenciais ou dados internos.
- Restringir mudanças à sessão/identidade, composição necessária, rota aprovada e persistência/migration correspondente.
- Persistência segue Code First/Alembic e exige migration versionada.
- Sessão não pode ser criada após falha de autenticação.
- Operações reais de produção, deploy, configuração de segredos ou execução de migration em ambiente compartilhado precisam de autorização operacional separada.
- Testes unitários de backend usam `nix develop .#backend`; integração usa `nix develop .#tests`.

## Classificação comentada

`engineering` domina. `security` e `privacy` são centrais porque a mudança estabelece a fonte confiável de identidade e o controle de acesso para dados pessoais. `integration` representa a persistência da sessão e a ligação com HTTP. A incerteza é média: o mecanismo escolhido é tecnicamente delimitado, mas o prazo de 8 horas é uma recomendação inicial e não há infraestrutura de auth no código atual. Risco alto decorre do impacto de acesso horizontal ou reutilização de token caso a implementação falhe.

## Decisão de roteamento

Destino `prompts/backend`, continuidade semântica da linhagem de consulta pessoal. `prompts/requisitos` e `prompts/revisao` foram consideradas, mas a finalidade principal é especificar mecanismo e composição do backend.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Security | Muito alta | Token imprevisível, não armazenado em claro, revogável e validado no servidor | Impede falsificação e reutilização após logout |
| Privacy | Muito alta | Sessão autoriza somente dados próprios; payload mínimo | Evita exposição horizontal ou de credenciais |
| Correctness | Muito alta | Login, validação, expiração, revogação e rota compartilham o mesmo ciclo | Evita sessões órfãs ou autorização divergente |
| Simplicity | Média | Sessão local persistida sem IdP externo | Reduz dependência operacional e permite revogação |
| Operability | Média | Expiração absoluta e logout observáveis por comportamento | Limita duração de credencial comprometida |

## Alternativas consideradas

### A — Sessão própria server-side com token opaco

Gerar token aleatório de alta entropia após login válido, enviar em cookie HttpOnly/Secure/SameSite=Lax, persistir somente hash e metadados, expirar em 8 horas e revogar em logout. Cada requisição resolve o principal pela sessão ativa. O ID do path continua sendo apenas alvo; a comparação de propriedade autoriza USER.

### B — Token assinado stateless

Emitir JWT após login e validar assinatura/expiração em cada requisição. Evita consulta de sessão por requisição, mas introduz segredo/chaves de assinatura e dificulta revogação imediata sem armazenamento adicional ou denylist. O repositório não possui configuração de chave nem essa infraestrutura.

### C — Integrar `task94` ou provedor de identidade

Reutilizar sessão de outro ramo ou integrar IdP. O usuário dispensou task94 e nenhum provedor externo foi indicado. Essa alternativa amplia acoplamento ou dependência e não atende à instrução atual sem autorização adicional.

### D — Não autenticar e confiar no ID

Permitir leitura se o UUID existir. É incompatível com RF13/RNF04 e regras de propriedade/negação padrão; descartada.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | A | B | C | D | Confiança | Base |
|---|---:|---:|---:|---:|---:|---|---|
| Security | Muito alta | +2 | +1 | +2 | -2 | Alta | A permite revogação; B exige chave e revogação extra; C pode ser seguro mas foi dispensada; D viola requisitos |
| Privacy | Muito alta | +2 | +1 | +2 | -2 | Alta | A/C permitem controle de sessão; B depende da gestão de claims e chaves; D expõe perfis |
| Correctness | Muito alta | +2 | +1 | +1 | -2 | Média | A tem estado explícito para expiração/revogação; B/C têm acoplamento não disponível |
| Simplicity | Média | +1 | 0 | -1 | +2 | Média | A evita IdP/chaves JWT, mas requer tabela; D é simples e inadequada |
| Operability | Média | +1 | 0 | -1 | -2 | Média | A revoga no servidor; B requer mecanismo adicional para invalidação |
| Delivery-speed | Média | 0 | 0 | -1 | +2 | Média | A exige migration e composição; D é rápida mas inaceitável |

Os valores são ordinais e não são somados. D é inviável por requisitos. C foi dispensada pelo usuário. A é recomendada sobre B pela revogação imediata e ausência de infraestrutura de assinatura já estabelecida; o custo é consulta ao armazenamento de sessão em cada requisição.

## Histórico e decisão atual

### Decisão da versão anterior

A v006 recomendou `GET /estudantes/{usuario_id}` com checagem de propriedade, mas bloqueou a entrega segura porque não existia principal autenticado e excluiu criar mecanismo novo.

### Decisão recomendada nesta versão

Criar sessão própria server-side baseada em token opaco. Após login válido, gerar token imprevisível, armazenar somente seu hash com vínculo ao usuário e datas/estado, e devolvê-lo apenas em cookie HttpOnly, Secure, SameSite=Lax. Recomenda-se expiração absoluta após 8 horas e endpoint de logout que revoga a sessão e limpa o cookie. A requisição resolve o principal consultando o token hash e rejeita ausência, expiração ou revogação.

Implementar `GET /estudantes/{usuario_id}` usando esse principal: USER só acessa o próprio ID. ADMIN fica negado para leitura cruzada enquanto não houver permissão específica. Responder 401 sem sessão válida e 404 genérico para ID alheio/inexistente/excluído. Manter o DTO com os seis campos pessoais definidos.

`status: proposed`: a solicitação explícita autoriza avaliar e implementar uma sessão própria, e esta revisão explicita um mecanismo e parâmetros recomendados para aprovação. A integração específica de `task94` não é necessária.

### Impacto da revisão

`revised`: o usuário selecionou sessão própria, retirando o bloqueio de mecanismo da v006. A revisão amplia o escopo para autenticação/sessão, define política inicial de emissão, armazenamento, expiração e revogação, e mantém ID na rota com comparação server-side.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Security | prioritized | Principal confiável e revogação de sessão | RF13/RNF04 e escolha explícita por sessão própria |
| Privacy | prioritized | Acesso por propriedade e token fora do payload | RF-AUTZ-03/07 e campos definidos |
| Correctness | prioritized | Ciclo coerente de login, consulta e logout | Inexistência atual de sessão no fluxo de acesso |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Interoperability | Cookie padrão com atributos documentados | Cliente envia cookie automaticamente; token não vai no JSON |
| Revocability | Sessão deixa de valer após logout | Estado revogado persistido e validado em cada request |
| Operational independence | Sem provedor externo | Backend gera e valida as próprias sessões |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Security | Sessão forjada, expirada aceita ou logout ineficaz | Alta | Estudantes e operação |
| Privacy | ID alheio permite leitura, ou token aparece em resposta/log | Alta | Estudantes |
| Correctness | Login parece bem-sucedido sem criar identidade que a rota consiga resolver | Alta | Usuário e frontend |
| Operability | Token comprometido não pode ser revogado | Alta | Estudantes e operação |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Revogação imediata | Consulta e armazenamento de sessão por request | Latência e simplicidade de persistência | Aceitável para sessões pessoais, a medir depois |
| Security | Criar migration/tabela e ciclo de logout | Delivery-speed | Necessário para mecanismo revogável |
| Privacy | Resposta uniforme 404 e negar acesso cruzado | Diagnóstico pelo cliente | Aceitável para evitar enumeração |
| Security | Expiração absoluta de 8 horas sem renovação deslizante | Conveniência de sessões longas | Recomendação inicial, revisável após validação de produto |

## Riscos e efeitos de segunda ordem

- Se o token bruto for persistido ou registrado, vazamento do banco/log passa a permitir tomada de sessão; armazenar somente hash e nunca logar cookie.
- Cookie `Secure` não trafega por HTTP local; exceção local deve ser isolada e não alterar padrão de produção.
- Sessão em cookie é enviada automaticamente pelo navegador; SameSite=Lax é recomendação mínima para esse fluxo, e outros endpoints mutáveis ainda devem avaliar CSRF segundo sua própria análise.
- Revogar sessão exige uma consulta server-side em cada request; cache não deve atrasar logout nesta primeira versão.
- Limpeza física de sessões expiradas pode ser tarefa operacional posterior; autenticação deve rejeitá-las mesmo sem limpeza.
- Caminho por ID sem comparação com principal permite IDOR; UUID não substitui autorização.
- Implementar autenticação local cria responsabilidade por segurança, expiração e suporte; não é equivalente a integrar `task94`.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Login cria sessão somente com credencial válida | Sessão/cookie após sucesso; nenhum após falha | Testes unitários de orquestração e integração de API | Login inválido cria sessão |
| Token é protegido | Banco contém hash, cookie contém token e JSON/log não contém token | Teste unitário de hasher/serializer e integração com armazenamento descartável | Token em claro persistido ou serializado |
| Sessões inválidas falham | Token ausente/desconhecido/expirado/revogado responde 401 | Teste integrado HTTP e repository descartável | Requisição inválida recebe dados |
| Logout revoga | Cookie de sessão deixa de funcionar após logout | Teste integrado em banco descartável | Token revogado continua válido |
| Path ID não autoriza terceiro | USER A com sessão válida e ID B recebe 404 genérico | Teste de API com dois usuários sintéticos | Dados de B são devolvidos a A |
| Duração proposta atende uso | 8 horas absolutas são aceitas pelo produto e relógio controla expiração | Aprovação de requisito e teste determinístico de expiração | Usuários precisam sessões maiores/menores ou renovação |
| Política admin é suficiente | ADMIN sem permission grant é negado | Testes de autorização e confirmação de produto | Necessidade de acesso administrativo explícito |

## Handoffs e atividades posteriores

- `$cross-cutting-implementation-v1`: implementar sessão local (emissão, armazenamento de hash, validação, expiração, revogação e principal) conforme a política proposta, sem integrar `task94`.
- `$backend-adapters-drivers-v2`: criar `GET /estudantes/{usuario_id}`, DTO e ligação HTTP ao use case, verificando principal de sessão versus ID do path; manter separada a implementação funcional do endpoint.
- `$backend-domain-orchestration-v2`: reutilizar o caso de uso de consulta e seu tratamento de perfil ausente/excluído; não inserir autenticação no domínio/Application.
- Persistência: adicionar modelo e migration para sessões, token hash, usuário, datas e revogação; não armazenar token em claro.
- `$integration-system-testing-v1`: cobrir login, cookie, consulta por proprietário/terceiro, expiração, revogação/logout e dados persistidos contra ambiente descartável.
- Produto/gestão: validar duração inicial de 8 horas, logout e eventual permissão administrativa de leitura de terceiros.
- Frontend: enviar cookie automaticamente, consumir rota por ID e tratar 401/404.

## Síntese

O usuário escolheu criar sessão própria, portanto não é necessário integrar `task94`. Recomendo sessão server-side com token opaco aleatório, somente hash persistido, cookie HttpOnly/Secure/SameSite=Lax, expiração absoluta inicial de 8 horas e logout revogável. A identidade virá da sessão validada, nunca do ID sozinho. `GET /estudantes/{usuario_id}` permitirá USER somente quando o ID da rota for o do principal; ADMIN não terá acesso cruzado sem permissão explícita. Sem sessão válida, recomendar 401; para perfil alheio, inexistente ou excluído, 404 genérico. Esta proposta amplia materialmente a v006 e requer implementação transversal de sessão, adapter HTTP, migration e testes unitários/integrados em atividades próprias.
