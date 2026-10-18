---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v004"
status: pending
created_at: "2026-10-09T23:33:38-03:00"
lineage:
  mode: revision
  root: prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md
  supersedes: prompts/backend/20261009-231827-expor-cadastro-experiencia-profissional-v003.md
  change_type: reassessment
  secondary_change_types: [correction, enrichment]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20261009-231827-expor-cadastro-experiencia-profissional-v003.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree; untracked"
      availability: available
    - path: prompts/backend/20261009-231117-expor-cadastro-experiencia-profissional-v002.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree; untracked"
      availability: available
    - path: prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e (conforme v003)"
      availability: available
    - path: src/backend/api/projeto_academico.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e (conforme v003)"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e (conforme v003)"
      availability: available
    - path: src/backend/application/cadastro_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e (conforme v003)"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioExperienciaProfissional e GeradorExperienciaProfissionalId"
      content_state: commit
      revision: "388fa9e (conforme v003)"
      availability: available
    - path: src/backend/api/cadastro_acesso.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "rota POST /acessos"
      content_state: commit
      revision: "388fa9e (conforme v003)"
      availability: available
    - path: src/backend/application/acesso_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e (conforme v003)"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF01, RF02, RF03 e RF13"
      content_state: commit
      revision: "388fa9e (conforme v003)"
      availability: available
    - path: docs/requisitos-seguranca.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "sessão autenticada, método de autenticação e autorização por usuário"
      content_state: commit
      revision: "388fa9e (conforme v003)"
      availability: available
    - path: docs/mapeamento_jornadas.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "UC04 e formulário de experiências"
      content_state: commit
      revision: "388fa9e (conforme v003)"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: markdown/mermaid
      analysis_scope: selected-section
      locator: "EXPERIENCIA_PROFISSIONAL e vínculo com USUARIO"
      content_state: commit
      revision: "388fa9e (conforme v003)"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "working tree; conteúdo lido nesta revisão"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/frontend]
  confidence: high
  rationale: "A revisão decide dependências e ordem de entrega para expor um caso de uso do backend; requisitos e segurança fornecem evidências."
classification:
  sphere: engineering
  concerns: [integration, security, delivery]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: high
  reversibility: moderate
  risk: high
---

# Análise de decisão — exposição segura do cadastro de experiência profissional

## Solicitação original

Versão v001: “$decision-analysis-v4 Implementar cadastro de experiências profissionais com relação às camadas de casos de uso e domain. Use doubles de teste apropriados para testes unitários.”

Versão v002: “$decision-analysis-v4 Fa;a uma analise para o card Expor cadastro de experiência profissional no backend. Inclua os testes unitarios adequados”

Versão v003: “$decision-analysis-v4 Revise prompts/backend/20261009-231117-expor-cadastro-experiencia-profissional-v002.md”

Nova solicitação, preservada literalmente: “revise essas decisoes”

## Informações complementares

A solicitação atual pede reavaliar a decisão pendente da linhagem. Não acrescenta aceite do card, mecanismo escolhido de autenticação, responsável por identidade/sessão ou confirmação de armazenamento fornecido por outra atividade.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Problema de identidade | Dependência descrita como mecanismo de autenticação a esclarecer | Separadas autenticação, identidade do principal e autorização de propriedade; requisito de segurança descreve sessão, mas não fixa mecanismo | Releitura do requisito de segurança e do fluxo de acesso | Evita tratar autenticação como mera validação de credencial ou escolher tecnologia sem evidência |
| Decisão de escopo | Aguardar aceite sobre endpoint e persistência | Recomendar dois entregáveis ordenados: capacidade autenticada e persistência operacional antes de habilitar o endpoint; exposição HTTP fica delimitada depois desses pré-requisitos | Separação das responsabilidades já demonstradas nos contratos e no código | O card pode ser planejado sem inventar mecanismo, mas sua implementação segue bloqueada até dependências terem responsáveis e contratos |
| Persistência | Ausência de adapter/migration observada | Mantida: existe porta interna de salvar, mas a busca de arquivos do backend não encontrou adapter nem migration de experiência | Inspeção da árvore atual | Mantém a necessidade de adapter Code First/Alembic ou dependência externa identificada |
| API | Convenção de projeto acadêmico como exemplo | Confirmado que router e factory aceitam executor opcional, mas a rota de projeto usa `usuario_id` no path e não resolve identidade autenticada | Releitura integral dos módulos | A convenção serve para injeção e DTO, não para identidade ou segurança |
| Status | `pending` | `pending` | Critérios do card e donos das dependências seguem ausentes | A recomendação fica mais precisa; não há autorização para liberar rota sem identidade e armazenamento |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261009-231827-expor-cadastro-experiencia-profissional-v003.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree, não rastreado |
| `prompts/backend/20261009-231117-expor-cadastro-experiencia-profissional-v002.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree, não rastreado |
| `prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Commit `388fa9e`, conforme a linhagem anterior |
| `src/backend/api/projeto_academico.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `388fa9e`, conforme a linhagem anterior |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `388fa9e`, conforme a linhagem anterior |
| `src/backend/application/cadastro_experiencia_profissional.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `388fa9e`, conforme a linhagem anterior |
| `src/backend/application/ports.py` | Apoio | Código-fonte | Produção | Python | Portas de experiência | Commit `388fa9e`, conforme a linhagem anterior |
| `src/backend/api/cadastro_acesso.py` | Apoio | Código-fonte | Produção | Python | Endpoint de acesso | Commit `388fa9e`, conforme a linhagem anterior |
| `src/backend/application/acesso_estudante.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `388fa9e`, conforme a linhagem anterior |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF01, RF02, RF03, RF13 | Commit `388fa9e`, conforme a linhagem anterior |
| `docs/requisitos-seguranca.md` | Apoio | Prosa | Requisitos | Markdown | Sessão, autenticação, autorização por proprietário | Commit `388fa9e`, conforme a linhagem anterior |
| `docs/mapeamento_jornadas.md` | Apoio | Prosa | Documentação | Markdown | UC04 e cadastro/edição de experiências | Commit `388fa9e`, conforme a linhagem anterior |
| `docs/modelagem_der.md` | Apoio | Diagrama/modelo | Contrato de schema | Markdown/Mermaid | Experiência e vínculo com usuário | Commit `388fa9e`, conforme a linhagem anterior |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Arquivo completo | Conteúdo atual lido nesta revisão |

### Limites da evidência dos artefatos

Os códigos da análise anterior são identificados como commit `388fa9e`; a revisão leu o conteúdo disponível no workspace e não encontrou mudanças de código no estado do Git reportado, somente as análises v002 e v003 não rastreadas. A ausência de adapter/migration foi verificada pela listagem dos arquivos do backend e pela análise precedente; não prova ausência de serviço externo. Os requisitos definem que deve haver sessão autenticada, mas não definem implementação, protocolo, duração, armazenamento ou responsável técnico.

## Problema enriquecido

### Resultado desejado

Permitir que um estudante cadastre experiência profissional durável, vinculada à sua própria identidade autenticada, usando o caso de uso existente e sem aceitar identidade arbitrária fornecida pelo cliente.

### Atores e interesses

- Estudante: cadastrar experiência e recuperá-la em usos posteriores.
- API: converter transporte para o caso de uso e devolver resposta pública.
- Segurança: garantir que a identidade venha de sessão confiável e que a operação respeite propriedade.
- Persistência: armazenar a experiência associada ao usuário.
- Equipe: entregar etapas com contratos e responsáveis explícitos.

### Evidências e fatos observados

- RF13 exige autenticação para informações pessoais e currículos. O documento de segurança também descreve sessão autenticada e autorização considerando o usuário autenticado.
- O caso de uso `CadastrarExperienciaProfissional` e sua entrada existem; a execução gera ID, constrói a entidade e chama `RepositorioExperienciaProfissional.salvar`.
- A porta de persistência de experiência existe no núcleo, mas não foi localizada implementação concreta nem migration de experiência na árvore do backend.
- A API de projetos acadêmicos demonstra DTO, router com executor injetado e composição pela factory. Seu identificador de usuário vem do path e não é evidência de principal autenticado.
- O endpoint de acesso chama `AcessarEstudante`, que busca/verifica credenciais e retorna sucesso sem criar sessão ou token.
- O requisito de segurança contempla sessão e autorização, mas deixa aberto o método/protocolo concreto.

### Hipóteses

- O card de exposição cobre somente criar uma experiência; consulta, edição e exclusão permanecem em entregas próprias.
- Os campos são os já suportados pelo caso de uso e domínio: empresa, cargo, descrição, data de início e data final opcional.
- Não se deve introduzir mecanismo de sessão, token ou provedor por inferência nesta decisão de API.
- A rota não será habilitada em produção até os executores autenticado e persistente estarem compostos.

### Perguntas em aberto

- Qual atividade e responsável entregarão o mecanismo de sessão e a forma de obter o principal autenticado na API?
- Qual atividade e responsável entregarão o repositório de experiência, modelo Code First, migration e composição?
- O card atual inclui essas dependências, ou pode depender formalmente de cards concluídos antes de habilitar a rota?
- Quais limites de texto são aprovados? A decisão não bloqueia o uso das regras atuais do domínio, mas não autoriza inventar novos limites.

### Escopo

Decisão de decomposição e ordem para a futura entrega:

1. Identificar/entregar mecanismo autenticado compatível com o requisito de segurança e fornecer principal confiável à API.
2. Implementar adapter de persistência conforme Code First/Alembic e compô-lo com o caso de uso, ou identificar dependência externa equivalente já entregue.
3. Depois, implementar DTO, router e binding local que usem principal autenticado e executor existente, com testes unitários de cada adapter isolado.
4. Validar protocolo HTTP e persistência operacional em atividade de testes de integração separada.

### Fora do escopo

- Escolher JWT, cookie, sessão server-side ou provedor externo sem decisão arquitetural própria.
- Implementar autenticação, autorização ou política transversal dentro do router de experiências.
- Aceitar `usuario_id` do path/body como prova de identidade.
- Acrescentar regra de negócio ao controller ou duplicar o caso de uso.
- Implementar listagem, edição ou exclusão de experiências.
- Teste HTTP real, teste de banco, migration integrada ou E2E nesta análise de adapters.

### Critérios de sucesso

- Existe uma fonte confiável e documentada para principal autenticado, com responsável e contrato definidos.
- Existe adapter persistente compatível com a porta já definida ou uma dependência concluída que o forneça.
- O endpoint recebe proprietário somente do principal confiável, converte datas em `Periodo`, invoca o caso de uso e não serializa entidade diretamente.
- A ausência de principal ou de composição não resulta em operação aberta nem em sucesso simulado.
- Testes unitários substituem executor, principal provider e demais dependências externas; testes HTTP e persistência real são separados como integração.

## Restrições aplicáveis

- Clean Architecture e DDD: domínio/application não dependem de FastAPI, ORM ou infraestrutura.
- Autenticação estabelece identidade; autorização restringe a operação ao usuário autenticado.
- Repositórios concretos, ORM e migrations ficam na camada externa; schema relacional usa Code First e Alembic.
- API não expõe entidade de domínio e não contém regra de negócio.
- Funções, classes e DTOs devem ter documentação completa conforme `AGENTS.md`.
- Testes unitários do backend usam `nix develop .#backend`; testes de integração usam `nix develop .#tests`.

## Classificação comentada

`engineering` domina porque a decisão trata de decomposição técnica para entregar UC04. `security`, `integration` e `delivery` distinguem o risco de identidade, a composição com persistência e a ordem entre atividades. O risco é alto porque uma rota insegura expõe dados de estudante; a incerteza é alta porque não foram fornecidos critérios do card nem responsáveis pelas dependências.

## Decisão de roteamento

Destino: `prompts/backend`, continuidade da linhagem e foco em API, composição e dependências do backend. `prompts/requisitos` e `prompts/frontend` são candidatas secundárias, pois requisitos sustentam os critérios e frontend não é o objeto da decisão.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Security | Muito alta | Obrigatório derivar identidade de principal autenticado | Impede gravar experiência para conta de terceiros |
| Correctness | Alta | Reutilizar caso de uso e persistir por porta implementada | Evita sucesso sem armazenamento durável |
| Interoperability | Alta | Compor rota, principal, executor e repositório | Um router isolado não constitui funcionalidade operacional |
| Delivery-speed | Média | Entregar em dependências ordenadas | Permite paralelizar sem expor rota insegura |
| Simplicity | Média | Não escolher mecanismo transversal nesta decisão | Mantém decisão no escopo do card e evita acoplamento prematuro |

## Alternativas consideradas

### A — Implementar somente endpoint agora

Reutiliza caso de uso e padrão de API, mas não dispõe de principal autenticado nem adapter de persistência. Recusar uma identidade do cliente deixa a rota sem proprietário confiável; aceitá-la viola RF13. Não atende requisito de segurança nem cadastro durável. Inviável no estado atual.

### B — Incluir autenticação, persistência e API no mesmo card

Pode produzir o fluxo completo, mas exige decisão e desenho de mecanismo de autenticação, além de adapter/migration, composição e API. A análise não tem autoridade nem evidência para escolher protocolo ou ampliar o aceite do card. Só é viável após revisão arquitetural e confirmação explícita do produto.

### C — Separar dependências e habilitar API após pré-requisitos

Tratar identidade/sessão e persistência como entregas com dono/contrato próprios; implementar a API de cadastro quando ambas estiverem disponíveis. Mantém segurança e limites de camada, e permite paralelizar as atividades. Recomendada como plano; a execução da API continua pendente até os pré-requisitos serem identificados.

### D — Expor rota com `usuario_id` do cliente e persistência simulada

É rápida, porém não autentica o usuário e não garante armazenamento. Rejeitada por contrariar RF13 e o objetivo de cadastro persistente.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | A | B | C | D | Confiança | Base |
|---|---:|---:|---:|---:|---:|---|---|
| Security | Muito alta | -2 | +2* | +2 | -2 | Alta | RF13 e requisito de sessão; *B depende de decisão de mecanismo |
| Correctness | Alta | -1 | +2 | +2 | -2 | Alta | Caso de uso e porta existem; adapter concreto não foi encontrado |
| Interoperability | Alta | 0 | +2 | +2 | -1 | Média | Factory injeta executores opcionais; composição completa ainda não existe |
| Delivery-speed | Média | +2 | -2 | +1 | +2 | Média | C permite preparar entregas em paralelo; D é rápida porém inválida |
| Simplicity | Média | +1 | -2 | +1 | +2 | Média | Separar mecanismo transversal mantém escopo claro |

Valores são ordinais e não foram somados. D é mostrada para tornar explícita uma prática rejeitada, não como alternativa viável.

## Histórico e decisão atual

### Decisão da versão anterior

v003 manteve `pending` até obter aceite do card e identificar quem forneceria identidade autenticada e persistência. A evidência de login sem sessão e ausência de adapter/migration foi considerada insuficiente para liberar a API.

### Decisão recomendada nesta versão

Adotar C como plano de decomposição: identificar donos e contratos para sessão/principal autenticado e repositório persistente; depois habilitar o endpoint como adapter fino que reutiliza caso de uso e porta existentes. Não aceitar identidade declarada pelo cliente e não inventar mecanismo de autenticação. A análise continua `pending` para implementação porque não há confirmação de que os pré-requisitos estejam entregues ou atribuídos, nem aceite que permita incluí-los no card.

### Impacto da revisão

`revised`: a recomendação passa de “aguardar esclarecimento” para uma sequência concreta de dependências, com divisão entre segurança, persistência, API e testes. O bloqueio de implementação permanece e fica associado a evidências objetivas.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Security | prioritized | Identidade da experiência deriva de sessão validada | RF13 e requisito de sessão autenticada |
| Correctness | prioritized | Caso de uso grava por adapter real | Porta existente; ausência de adapter na árvore |
| Interoperability | prioritized | Componentes só são habilitados quando compostos | Padrão atual de executor opcional pode resultar em 503 |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Simplicity | Não selecionar autenticação nesta decisão de API | Encaminha mecanismo transversal ao dono arquitetural |
| Delivery-speed | Permitir trabalho paralelo e entrega incremental | API pode avançar após contratos das duas dependências estarem definidos |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Security | Cadastro em nome de terceiro ou exposição de dados profissionais | Alta | Estudantes e operação |
| Correctness | Resposta de sucesso sem armazenamento durável | Alta | Estudantes e produto |
| Interoperability | Rota não composta ou permanentemente indisponível | Média | Clientes da API e equipe |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Security | Aguardar entrega/contrato de sessão e principal | Delivery-speed | Necessário por RF13 |
| Correctness | Implementar modelo, migration e repository adapter ou aguardar dependência | Simplicity e velocidade | Necessário para cadastro durável |
| Interoperability | Coordenar composição e critérios entre cards | Autonomia de entrega | Aceitável para evitar rota inoperante |

## Riscos e efeitos de segunda ordem

- Sessão sem autorização de propriedade ainda pode permitir acesso cruzado; o principal deve ser a única origem do `UsuarioId` no cadastro.
- A API pode responder 503 se o executor continuar opcional; configuração de produção precisa falhar de modo explícito ou não registrar rota não operacional.
- Uma migration integrada requer testes de nível superior, fora dos testes unitários de adapter.
- Criar o endpoint antes de definir quem entrega as dependências pode cristalizar contrato HTTP incompleto.
- Limites de texto devem continuar os requisitos aprovados; não copiar limites de projeto acadêmico por conveniência.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Identidade autenticada estará disponível | Contrato do principal e card responsável por sessão | Revisão arquitetural/composição | Nenhum dono ou mecanismo definido mantém API bloqueada |
| Persistência estará disponível | Adapter, migration e composição ou referência de entrega concluída | Inspeção de implementação | Porta sem adapter mantém fluxo não operacional |
| API atribui a experiência ao principal | Teste unitário do handler com principal controlado; ignora IDs do cliente | Unitário direto com doubles | Identidade do corpo/path influencia proprietário |
| API traduz os dados sem duplicar regra | DTO converte datas para `Periodo` e invoca caso de uso existente | Revisão e teste unitário | Regra de domínio reaparece no handler |
| Fluxo HTTP e persistência funcionam juntos | Cliente ASGI e banco/migration em ambiente de teste apropriado | Testes de integração separados | Resposta ou gravação diverge do contrato |

## Handoffs e atividades posteriores

- Arquitetura/segurança: escolher e documentar mecanismo de sessão, fornecimento de principal e autorização de propriedade.
- Gestão do card: informar aceite e atribuir responsáveis/pré-requisitos; confirmar se a entrega do endpoint pode depender desses cards.
- Backend/persistência: implementar adapter Code First/Alembic da porta de experiência e registrá-lo na composição, se não houver entrega externa.
- Backend/API: depois dos pré-requisitos, criar DTO/router/factory e testes unitários isolados.
- `$integration-system-testing-v1`: validar rota HTTP e persistência real em teste de integração quando a composição estiver pronta.
- Produto: definir limites de texto e confirmar se operações de consulta, edição e exclusão são cards separados.

## Síntese

A decisão agora recomenda decompor e ordenar a entrega: primeiro garantir identidade autenticada e persistência operacional, depois expor o caso de uso existente por API. A evidência sustenta essa ordem, mas não identifica responsáveis nem contratos concluídos. Portanto a análise permanece `pending` e nenhuma rota deve ser implementada ou habilitada ainda. O desbloqueio mínimo é apontar os cards/donos e contratos dessas duas dependências, ou confirmar formalmente que o card será ampliado e encaminhar a escolha de autenticação para decisão arquitetural própria.
