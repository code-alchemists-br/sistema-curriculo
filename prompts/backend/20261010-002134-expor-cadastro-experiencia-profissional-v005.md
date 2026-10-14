---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v005"
status: proposed
created_at: "2026-10-10T00:21:34-03:00"
lineage:
  mode: revision
  root: prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md
  supersedes: prompts/backend/20261009-233338-expor-cadastro-experiencia-profissional-v004.md
  change_type: reassessment
  secondary_change_types: [correction, enrichment]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20261009-233338-expor-cadastro-experiencia-profissional-v004.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked; revisão da linhagem"
      availability: available
    - path: prompts/backend/20261009-231827-expor-cadastro-experiencia-profissional-v003.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked; antecedente da v004"
      availability: available
    - path: src/backend/api/experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked"
      availability: available
    - path: src/backend/api/cadastro_acesso.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "cadastro, login, sessão e logout"
      content_state: working-tree
      revision: "modificado"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "modificado"
      availability: available
    - path: src/backend/api/runtime.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked"
      availability: available
    - path: src/backend/infrastructure/composicao.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/sessao_autenticada.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked"
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261009_0003_criar_experiencias_e_sessoes.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked"
      availability: available
    - path: src/backend/infrastructure/security/sessoes.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked"
      availability: available
    - path: src/backend/tests/test_api_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked"
      availability: available
    - path: src/backend/tests/test_infrastructure_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked"
      availability: available
    - path: src/backend/tests/test_infrastructure_sessoes.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF01, RF02, RF03 e RF13, conforme v004"
      content_state: commit
      revision: "388fa9e; recorte registrado na v004"
      availability: available
    - path: docs/requisitos-seguranca.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "sessão e identidade, conforme v004"
      content_state: commit
      revision: "388fa9e; recorte registrado na v004"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "instruções fornecidas e arquivo lido"
      availability: available
---

# Análise de decisão — cadastro de experiência profissional já exposto

## Solicitação original

v001: “$decision-analysis-v4 Implementar cadastro de experiências profissionais com relação às camadas de casos de uso e domain. Use doubles de teste apropriados para testes unitários.”

v002: “$decision-analysis-v4 Fa;a uma analise para o card Expor cadastro de experiência profissional no backend. Inclua os testes unitarios adequados”

v003: “$decision-analysis-v4 Revise prompts/backend/20261009-231117-expor-cadastro-experiencia-profissional-v002.md”

v004: “revise essas decisoes”

Solicitação desta revisão, preservada literalmente: “revise esse prompt”

## Informações complementares

A sessão, a rota e os adapters de persistência que as versões v003/v004 listavam como ausentes existem agora no working tree. A v003 foi escrita antes dessas mudanças e a v004 manteve conclusões antigas sem incorporá-las. A implementação inclui também cadastro/login/logout, composição de runtime e migration, portanto seu escopo ficou maior do que somente expor o caso de uso de experiência.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Situação da sessão | Dependência não implementada; mecanismo não definido | Adapter de sessão server-side, token aleatório com hash armazenado, expiração e cookie HTTP-only existem no working tree | Inspeção dos adapters e das rotas atuais | A dependência técnica deixou de estar ausente; a escolha precisa ser avaliada como implementação existente |
| Persistência de experiência | Sem adapter ou migration identificados | Modelo SQLAlchemy, repository adapter e migration Alembic existem no working tree | Inspeção dos arquivos atuais | O bloqueio anterior de persistência foi superado no código |
| Rota e composição | Rota ainda dependente de decisões futuras | Router, runtime e composição por sessão estão implementados e registrados | Inspeção da API, factory e composição | A funcionalidade não é mais apenas proposta; precisa de validação operacional |
| Estado da evidência | v004 tratava o código base como commit antigo | Arquivos novos/modificados estão no working tree, vários ainda não rastreados | `git status --short` | Não se pode atribuir a implementação ao commit base nem tratá-la como entregue/implantada |
| Decisão | `pending`, aguardando donos e contratos das dependências | Recomendar manter a abordagem implementada e fechar validação/aceite antes de considerar entregue | Evidência concreta reduziu a incerteza técnica | Impacto `revised`; a pendência deixa de ser “quem implementará” e passa a ser integração operacional e aceite do produto |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261009-233338-expor-cadastro-experiencia-profissional-v004.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree, não rastreado |
| `prompts/backend/20261009-231827-expor-cadastro-experiencia-profissional-v003.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree, não rastreado |
| `src/backend/api/experiencia_profissional.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree, não rastreado |
| `src/backend/api/cadastro_acesso.py` | Apoio | Código-fonte | Produção | Python | Cadastro/login/sessão/logout | Working tree, modificado |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree, modificado |
| `src/backend/api/runtime.py` | Apoio | Código-fonte | Contrato | Python | Arquivo completo | Working tree, não rastreado |
| `src/backend/infrastructure/composicao.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree, não rastreado |
| `src/backend/infrastructure/persistence/sqlalchemy/experiencia_profissional.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree, não rastreado |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_experiencia_profissional.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree, não rastreado |
| `src/backend/infrastructure/persistence/sqlalchemy/sessao_autenticada.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree, não rastreado |
| `src/backend/infrastructure/persistence/alembic/versions/20261009_0003_criar_experiencias_e_sessoes.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree, não rastreado |
| `src/backend/infrastructure/security/sessoes.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree, não rastreado |
| `src/backend/tests/test_api_experiencia_profissional.py` | Apoio | Código-fonte | Teste | Python | Arquivo completo | Working tree, não rastreado |
| `src/backend/tests/test_infrastructure_experiencia_profissional.py` | Apoio | Código-fonte | Teste | Python | Arquivo completo | Working tree, não rastreado |
| `src/backend/tests/test_infrastructure_sessoes.py` | Apoio | Código-fonte | Teste | Python | Arquivo completo | Working tree, não rastreado |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF01, RF02, RF03 e RF13, conforme v004 | Commit `388fa9e`, recorte herdado da v004 |
| `docs/requisitos-seguranca.md` | Apoio | Prosa | Requisitos | Markdown | Sessão e identidade, conforme v004 | Commit `388fa9e`, recorte herdado da v004 |
| `AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Arquivo completo | Instrução do workspace e arquivo local lido |

### Limites da evidência dos artefatos

Os arquivos de implementação examinados estão no working tree e ainda não representam uma entrega rastreada. A existência de uma migration e de testes não comprova que a migration tenha sido aplicada a um banco real nem que o fluxo integrado esteja operacional. As referências aos requisitos funcionais e de segurança foram herdadas dos recortes registrados pela v004, não relidas integralmente nesta revisão. A análise do código não confirma aceite do card, limites de texto, deploy ou compatibilidade com ambiente de produção.

## Problema enriquecido

### Resultado desejado

Disponibilizar cadastro durável de experiência profissional para o usuário autenticado, reaproveitando o caso de uso e atribuindo o registro à identidade obtida da sessão.

### Atores e interesses

- Estudante: registrar experiência e receber resposta coerente com o que foi persistido.
- API: converter a requisição em entrada do caso de uso sem aceitar identidade do cliente.
- Persistência: armazenar experiência e sessão na mesma unidade transacional da requisição.
- Equipe: validar migração, configuração e contrato funcional antes de tratar o trabalho como concluído.

### Evidências e fatos observados

- A API contém rota `POST /experiencias-profissionais` e obtém o usuário pelo runtime da requisição, em vez de receber `usuario_id` no corpo.
- O runtime compõe o caso de uso existente com repository adapter SQLAlchemy.
- O modelo relacional associa experiência a usuário; há migration Alembic para experiências e sessões.
- A implementação de sessão gera token opaco, persiste seu hash e expiração, e valida o token recebido por cookie.
- A rota traduz dados para `Periodo`, chama o caso de uso e mapeia o resultado para DTO de resposta.
- Os adapters e testes citados estão em arquivos novos/modificados no working tree.

### Hipóteses

- O escopo funcional continua sendo somente criar experiência profissional.
- O contrato de cookie de sessão é aceitável para os clientes da aplicação.
- O banco usado pelo ambiente alvo suporta os tipos e constraints declarados na migration.
- O cadastro deve falhar como não autenticado sem sessão válida e não deve aceitar identidade arbitrária do cliente.

### Perguntas em aberto

- A migration já foi aplicada em algum ambiente alvo e o fluxo foi verificado com banco configurado?
- O card aceita o fluxo de sessão introduzido junto à exposição do cadastro ou essa implementação precisa ser registrada como trabalho separado?
- Os limites de texto e mensagens de erro correspondem aos critérios aprovados pelo produto?

### Escopo

- Revisar a decisão de expor o cadastro à luz dos adapters e da composição já presentes.
- Preservar a identidade do estudante como dado derivado da sessão.
- Validar em ambiente apropriado a migration, o fluxo de cadastro/login, cadastro da experiência e logout.
- Manter testes unitários de API e adapters no ambiente backend.

### Fora do escopo

- Alterar o backend como parte desta análise.
- Acrescentar consulta, edição ou exclusão de experiências.
- Declarar a migration aplicada ou a implantação concluída sem evidência.
- Alterar requisitos funcionais, segurança ou contrato do frontend.

### Critérios de sucesso

- O endpoint só cadastra para um usuário resolvido por sessão válida.
- A experiência é persistida por adapter real e associada ao usuário autenticado.
- Migration aplica e reverte/avança corretamente no banco do ambiente de teste.
- Testes unitários cobrem casos autenticado, não autenticado, dados inválidos e persistência do adapter.
- A equipe confirma escopo do card e contrato de campos/respostas.

## Restrições aplicáveis

- Manter domínio e aplicação sem dependência de FastAPI ou SQLAlchemy.
- Não usar ID enviado pelo cliente como prova de identidade.
- Testes unitários backend usam `nix develop .#backend`; testes de integração usam `nix develop .#tests`.
- Funções, classes e DTOs devem documentar responsabilidade, abordagem e finalidade.
- Esta revisão só altera o artefato de análise; código de produção requer atividade própria.

## Classificação comentada

Esfera `engineering`, pois a decisão avalia a integração técnica de API, autenticação e persistência. As preocupações são `security`, `integration` e `delivery`. O risco é alto: associação incorreta de usuário pode gravar dados pessoais no perfil errado. A incerteza é média, concentrada na validação operacional e no aceite funcional.

## Decisão de roteamento

Manter `prompts/backend`, destino das análises anteriores e correspondente ao objeto atual. Foram consideradas `prompts/requisitos` e `prompts/revisao`; backend segue mais específico porque o objeto é a composição e operação técnica da API.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Security | Muito alta | Identidade apenas da sessão validada | Evita cadastro em nome de outra conta |
| Correctness | Alta | Persistência confirmada por migration e banco | Código presente não garante schema aplicado |
| Interoperability | Alta | API, sessão e repository operam juntos | A composição é necessária para entrega utilizável |
| Delivery-speed | Média | Reaproveitar o que já foi criado e fechar validação | Evita refazer trabalho já disponível |

## Alternativas consideradas

### A — Adotar a implementação existente após validação operacional

Manter o endpoint, sessão server-side, repository adapter e migration atuais; validar migração e fluxo integrado, obter aceite do card e corrigir incompatibilidades encontradas. É a alternativa recomendada: aproveita implementação concreta e preserva identidade autenticada.

### B — Reverter os componentes transversais e dividir em entregas

Separar sessão, persistência e API em atividades diferentes. Reduz mistura de escopo, mas descarta ou retrabalha código já criado e adia a funcionalidade. É adequada apenas se a equipe confirmar que a sessão não pertence ao escopo ou rejeitar o contrato implementado.

### C — Manter endpoint sem validar migração/fluxo integrado

Conclui a atividade com base apenas em presença de arquivos e testes unitários. É inviável como declaração de entrega, pois não comprova schema aplicado nem interação real com banco.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | A | B | C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Security | Muito alta | +2 | +1 | -2 | Alta | A e B preservam sessão; C não fecha validação operacional |
| Correctness | Alta | +2 | +1 | -1 | Média | A valida código e banco; B entrega em etapas |
| Delivery-speed | Média | +2 | -1 | +2 | Média | A reaproveita o working tree; C parece rápida mas deixa risco não verificado |
| Simplicity | Média | 0 | +1 | +1 | Média | B separa responsabilidades; A mantém composição existente |

Valores são ordinais e não são somados.

## Histórico e decisão atual

### Decisão da versão anterior

v004 recomendou dividir a implementação e manter `pending` até identificar donos e contratos de sessão/principal e persistência. Essa decisão partia do estado de código anterior, no qual esses componentes não estavam presentes.

### Decisão recomendada nesta versão

Adotar a alternativa A: a abordagem implementada é tecnicamente coerente com a necessidade identificada e já cobre API, principal derivado da sessão, persistência e migration. Tratar como proposta pronta para validação, não como entrega concluída. O próximo gate é aplicar a migration em ambiente apropriado, executar a validação integrada e obter aceite do escopo e dos contratos.

### Impacto da revisão

`revised`: a recomendação muda de decompor dependências ainda inexistentes para validar e aceitar a solução que já está no working tree. A v003 e a v004 permanecem históricas e não devem ser reescritas.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Security | prioritized | Principal deriva de sessão opaca validada | Implementação de sessão e handler atuais |
| Correctness | prioritized | Caso de uso existente persiste via repository adapter | Composição atual e migration presente |
| Delivery-speed | prioritized | Aproveitar trabalho já realizado | Arquivos no working tree |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Simplicity | Evitar refatoração ampla sem evidência de falha | Preservar composição atual e revisar somente problemas encontrados na validação |
| Reversibility | Manter mudança reversível até aceite | Working tree e migration permitem revisão antes de release |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Security | Conta errada ou sessão inválida associada ao cadastro | Alta | Estudante e operação |
| Correctness | Endpoint responde sem banco compatível ou persistência real | Alta | Estudante e produto |
| Delivery-speed | Retrabalho ao descobrir tarde divergência de contrato | Média | Equipe |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Security e correctness | Rodar validação de integração e revisão do contrato antes do aceite | Velocidade imediata | Necessário, dada a associação de dados pessoais |
| Simplicity | Manter sessão e experiência na mesma composição de runtime | Separação estrita de escopo | Aceitável se o dono do produto aceitar o escopo ampliado |

## Riscos e efeitos de segunda ordem

- Migration criada mas não aplicada pode deixar a aplicação falhar ao consultar tabela inexistente.
- A composição introduz sessão em cadastro/login além do endpoint de experiência; o escopo do card pode não cobrir essa mudança transversal.
- Configuração de banco, flags de cookie e política de implantação precisam corresponder aos ambientes de execução.
- Limites e mensagens do contrato ainda não foram confirmados com critérios do card.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Migration é aplicável | Banco de teste configurado e revision Alembic aplicada | Teste de integração no ambiente `tests` | Erro de schema, constraint ou engine |
| Usuário é derivado da sessão | Testes de request autenticado e sem cookie; inspeção do handler | Unitário e integração | Aceita cadastro sem sessão ou usa ID do cliente |
| Cadastro persiste associado | Ler registro após request e conferir `usuario_id` | Integração com banco | Resposta sem registro ou proprietário incorreto |
| Escopo e contrato são aceitos | Critérios do card e aceite de produto/segurança | Revisão do card | Rejeição do cookie, campos ou inclusão da sessão |

## Handoffs e atividades posteriores

- Backend: executar testes unitários pertinentes no ambiente Nix `backend` e validar a migration/fluxo integrado no ambiente `tests`.
- Produto/gestão: confirmar aceite do endpoint, sessão, campos e respostas no card.
- Segurança/operação: revisar configurações de cookie e sessão para ambientes de execução.
- Corrigir somente falhas concretas apontadas pelas validações; não ampliar operações de experiência sem novo requisito.

## Síntese

A recomendação anterior ficou desatualizada: sessão autenticada, rota de cadastro, repository adapter, composição e migration já existem no working tree. A decisão atual é preservar essa abordagem e fechar validação integrada, configuração e aceite funcional. A análise passa a `proposed`, pois há evidência técnica suficiente para recomendar a solução; ainda não afirma que a migration foi aplicada ou que o card está concluído.
