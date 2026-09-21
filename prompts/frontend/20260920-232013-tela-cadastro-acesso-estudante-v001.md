---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-09-20T23:20:13-03:00"
lineage:
  mode: initial
  root: null
  supersedes: null
  change_type: initial
  secondary_change_types: []
  decision_impact: initial
subjects:
  kind: file-set
  files:
    - path: src/frontend
      relationship: primary
      representation: source-code
      function: production
      format: "diretório sem aplicação implementada"
      analysis_scope: metadata-only
      locator: null
      content_state: commit
      revision: "3bdfee0"
      availability: available
    - path: src/frontend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "3bdfee0"
      availability: available
    - path: nix/frontend.nix
      relationship: supporting
      representation: executable-script
      function: build
      format: nix
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "3bdfee0"
      availability: available
    - path: src/backend/api/cadastro_acesso.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "3bdfee0"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "3bdfee0"
      availability: available
    - path: docs/casos-de-uso-v2.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: "selected-section"
      locator: "Visão geral, Casos de uso identificados e Módulo do aluno"
      content_state: commit
      revision: "3bdfee0"
      availability: available
    - path: docs/mapeamento_jornadas.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: "selected-section"
      locator: "Seções 3, 4, 5 e 6.1"
      content_state: commit
      revision: "3bdfee0"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: "selected-section"
      locator: "Objetivo e escopo, Autenticação e Definições pendentes"
      content_state: commit
      revision: "3bdfee0"
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: "selected-section"
      locator: "Requisitos consolidados e Definições pendentes"
      content_state: commit
      revision: "3bdfee0"
      availability: available
    - path: docs/Arquitetura/ADR-001-arquitetura-do-sistema.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: "selected-section"
      locator: "Seções 2.5, 2.6, 2.7 e 2.9"
      content_state: commit
      revision: "3bdfee0"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/frontend
  considered_directories: [prompts/frontend, prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "O objetivo principal é uma tela React/TypeScript e seu fluxo de interação; backend e requisitos são evidências e handoffs."
classification:
  sphere: engineering
  concerns: [implementation, integration, user-experience]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — tela de cadastro e acesso do estudante

## Solicitação original

`$decision-analysis-v4 Faça uma análise para implementar a tela de cadastro e acesso do estudante em TypeScript e React.`

## Informações complementares

- O usuário definiu TypeScript e React como tecnologias da interface.
- O diretório `src/frontend` não contém aplicação, componentes, arquivos de
  configuração TypeScript, dependências Node, testes ou estilos; contém apenas
  `AGENTS.md`.
- O backend expõe `POST /estudantes` e `POST /acessos`, mas a fábrica ASGI é
  criada sem os executores e o derivador de senha. No estado atual, ambas as
  rotas retornam `503` em vez de executar o fluxo.
- O acesso atual somente confirma credenciais e devolve `204`; não cria sessão,
  cookie, token ou identidade utilizável em navegação posterior.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem desta tela | Nenhum identificado | v001 inicial | Não há análise anterior identificada para uma interface React de cadastro e acesso | Nenhum histórico a preservar |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/frontend` | Principal | Código-fonte | Produção | Diretório | Metadados | Commit `3bdfee0`; sem aplicação |
| `src/frontend/AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Arquivo completo | Commit `3bdfee0` |
| `nix/frontend.nix` | Apoio | Script executável | Build | Nix | Arquivo completo | Commit `3bdfee0`; contém somente Git |
| `src/backend/api/cadastro_acesso.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `3bdfee0` |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `3bdfee0` |
| Documentos de casos de uso, jornada, requisitos e ADR listados no front matter | Apoio/contexto | Prosa | Documentação | Markdown | Seções indicadas | Commit `3bdfee0` |

### Limites da evidência dos artefatos

Não há wireframe, identidade visual, biblioteca de componentes, navegador
suportado, gerenciador de pacotes, runtime Node, ferramenta de build nem runner
de testes já adotados. Não foi presumido um contrato de autenticação: os
requisitos o demandam, mas a API atual somente verifica credenciais. A análise
propõe uma primeira tela de conta; ela não autoriza inventar sessão persistente
ou acesso a recursos protegidos.

## Problema enriquecido

### Resultado desejado

Oferecer ao estudante uma página React em TypeScript, responsiva e utilizável
por teclado, na qual ele possa alternar entre criar sua conta e informar suas
credenciais. A tela deve isolar o cliente HTTP, validar apenas a experiência de
formulário, traduzir respostas conhecidas em mensagens claras e preservar os
dados preenchidos após falhas.

### Atores e interesses

- O estudante precisa iniciar a jornada criando conta ou confirmando suas
  credenciais sem lidar com detalhes de API.
- A equipe de frontend precisa de uma base React/TypeScript mínima que respeite
  Feature-Sliced Design (FSD) e permita testar o fluxo isoladamente.
- A equipe de backend precisa de um contrato consumível e de composição real
  das dependências para que a tela não fique permanentemente indisponível.
- A equipe de produto precisa evitar comunicar “login realizado” quando ainda
  não há sessão nem navegação autenticada.

### Evidências e fatos observados

- UC01 e UC02 preveem criar conta e realizar login; a jornada começa em
  cadastro/login antes do painel inicial.
- `POST /estudantes` recebe `nome`, `email` e `senha`; em sucesso devolve
  `201` com `id`, `nome` e `email`. A API mapeia e-mail já cadastrado para
  `409`, entrada inválida para `422` e indisponibilidade para `503`.
- `POST /acessos` recebe `email` e `senha`; em sucesso devolve `204`; falhas
  de credencial são `401` e indisponibilidade é `503`.
- O frontend precisa manter DTOs externos separados de modelos de UI, chamadas
  HTTP fora de componentes e estado local por fluxo, conforme `AGENTS.md`.
- RNF01, RNF02 e RNF03 demandam clareza, campos identificáveis, erros
  compreensíveis, teclado e funcionamento em dispositivos móveis.

### Hipóteses

- Uma página única com abas ou seletor explícito entre “Entrar” e “Criar conta”
  reduz a primeira navegação, pois os dois fluxos são a mesma porta de entrada.
- Após `201`, trocar para a aba de entrada e preencher o e-mail recém-criado é
  útil; a senha não deve ser preservada nem preenchida automaticamente.
- Após `204`, a tela deve informar somente que as credenciais foram confirmadas
  e aguardar uma futura decisão de sessão e rota protegida.
- Vite é uma base adequada para a primeira aplicação React/TypeScript, desde
  que a atividade de ambiente escolha e declare Node, gerenciador de pacotes,
  dependências e runner de testes no Nix do projeto.

### Perguntas em aberto

- Qual URL por ambiente o cliente deve usar para a API e qual origem será
  permitida por CORS durante desenvolvimento e produção?
- Qual será o mecanismo de autenticação persistente e para qual rota o aluno
  deverá ser enviado após credenciais válidas?
- Há identidade visual, textos institucionais, política de privacidade ou
  requisitos específicos para e-mail institucional que devam aparecer na tela?
- Qual gerenciador de pacotes e qual política de versões Node a equipe adotará?

### Escopo

- Preparar uma aplicação React/TypeScript mínima, com build e testes unitários
  declarados no ambiente frontend, como pré-requisito técnico separado.
- Criar uma página de acesso na camada `pages` que componha uma feature local
  ou `features/acesso-estudante`, conforme a reutilização efetivamente
  necessária.
- Criar dois formulários: cadastro (`nome`, `email`, `senha`, confirmação de
  senha) e acesso (`email`, `senha`), com alternância explícita.
- Criar funções tipadas de cliente para `POST /estudantes` e `POST /acessos`,
  com validação/normalização do JSON de resposta na fronteira e URL de API por
  configuração de ambiente.
- Tratar estados de envio, sucesso e erros `401`, `409`, `422`, `503`, rede e
  resposta inválida, mantendo os valores não sensíveis preenchidos.
- Aplicar HTML semântico, labels, associação de erros, foco previsível,
  anúncio de estado e layout responsivo.
- Criar testes unitários de modelo de formulário, tradutor de falhas e
  componentes/formulários com cliente substituído.

### Fora do escopo

- Criar ou decidir cookies, tokens, sessão, refresh, autorização, rota
  protegida, recuperação de senha ou política de credenciais.
- Alterar o domínio, casos de uso, portas, regras de cadastro ou contrato HTTP
  existente do backend.
- Implementar a composição de dependências, conexão de banco ou CORS no
  backend; são pré-requisitos externos.
- Criar painel inicial, currículo, perfil, recuperação de senha, design system
  amplo, internacionalização ou uma iniciativa geral de theming.
- Executar testes de API, integração, E2E, navegador real ou acessibilidade de
  ponta a ponta nesta fatia.

### Critérios de sucesso

- O frontend compila em TypeScript e organiza dependências conforme FSD, sem
  importação ascendente ou chamada HTTP direta por componente visual.
- O estudante consegue navegar por teclado entre os dois fluxos, identificar
  cada campo e receber erros associados e compreensíveis.
- Cadastro envia exatamente o contrato da API e trata `201`, `409`, `422`,
  `503` e falhas de rede sem apagar o formulário indevidamente.
- Acesso envia exatamente o contrato da API e trata `204`, `401`, `503` e
  falhas de rede sem afirmar que uma sessão foi criada.
- O layout permanece funcional em largura móvel e desktop, e os testes
  unitários não usam backend, rede real ou navegador E2E.

## Restrições aplicáveis

- TypeScript e React são obrigatórios por solicitação explícita.
- FSD é obrigatório: `app → pages → widgets → features → entities → shared`;
  slices expõem API pública e não há imports entre slices pares.
- Componentes visuais não fazem HTTP; a fronteira API usa contratos explícitos
  e tipos distintos do estado de UI quando necessário.
- O frontend não substitui a validação ou segurança do backend e não simula
  autenticação persistente inexistente.
- Novas telas precisam de semântica, teclado, feedback de estados e adaptação a
  móvel; testes unitários rodam no ambiente Nix de frontend.

## Classificação comentada

Esta é uma decisão de engenharia de entrega de componente frontend. A maior
preocupação é implementação da tela; integração importa porque há dois
contratos HTTP e o backend ainda não está operacional; experiência do usuário
importa porque cadastro e acesso iniciam toda a jornada do aluno. A incerteza é
média devido à ausência de fundação frontend e autenticação persistente.

## Decisão de roteamento

As subpastas existentes são `ambientes`, `backend`, `frontend`, `requisitos`,
`revisao` e `templates`. `prompts/frontend` é o destino mais específico porque
a decisão orienta tela React, FSD, estado de formulário e cliente da interface.
`prompts/backend` foi considerada pelos contratos e handoffs, mas eles são
evidência; `prompts/requisitos` contém origem do fluxo, mas não é o alvo da
implementação.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| User-value | Alta | Priorizar | A conta é a entrada para a jornada de currículo |
| Correctness | Alta | Satisfazer | A UI precisa representar fielmente status e contrato da API |
| Simplicity | Alta | Priorizar | A primeira interface não deve antecipar sessão ou design system amplo |
| Modifiability | Média | Priorizar | FSD e cliente isolado permitem evoluir login quando houver sessão |
| Delivery-speed | Média | Priorizar | A tela deve avançar em paralelo ao backend, com bloqueios explícitos |
| Reliability | Média | Satisfazer | Erros e indisponibilidade devem preservar dados e orientar o usuário |

## Alternativas consideradas

### A — Adiar toda a tela até o backend fornecer sessão persistente

Evita interface temporária, mas bloqueia a porta de entrada da jornada e não
aproveita os contratos de cadastro e verificação já definidos. É inadequada:
o cadastro é útil independentemente de uma rota autenticada posterior.

### B — Criar somente mockups estáticos

É rápida para discutir estética, mas não entrega o card, não valida contratos,
estados de erro ou acessibilidade observável e duplica trabalho quando React
for iniciado. É rejeitada.

### C — Estabelecer fundação React/TypeScript e implementar uma página de acesso integrada aos contratos existentes

Cria a tela funcional até a fronteira HTTP, deixa claro que `204` confirma
credenciais sem criar sessão e separa a composição real do backend como
handoff. Exige trabalho inicial de ambiente e coordenação de CORS, mas atende
o valor atual sem inventar política de autenticação. É recomendada.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | A — Adiar | B — Mockup | C — Fundação e tela | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| User-value | Alta | -2 | +1 | +2 | Alta | Jornada inicia em cadastro/login |
| Correctness | Alta | +1 | -1 | +2 | Alta | Contratos HTTP observados |
| Simplicity | Alta | +1 | +2 | +1 | Média | C aceita fundação mínima, sem sessão |
| Modifiability | Média | 0 | -1 | +2 | Alta | FSD obrigatório |
| Delivery-speed | Média | -2 | +1 | +1 | Média | Fundação é custo inicial, mas evita reescrita |
| Reliability | Média | 0 | -1 | +1 | Média | Estados controlados e cliente isolado |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### Decisão recomendada nesta versão

Adotar a alternativa C em duas fatias coordenadas. Primeiro, uma atividade de
ambiente estabelece React, TypeScript, Vite, Node, gerenciador de pacotes e
runner de testes no Nix, com a estrutura FSD mínima. Depois, implementar uma
única página de acesso com dois formulários e um cliente HTTP tipado. A página
não navega a conteúdo protegido: após sucesso de acesso, mostra confirmação
neutra até a decisão de autenticação persistente.

O cliente deve usar uma URL configurável de API e oferecer uma transformação
explícita dos status HTTP para estados de UI. Cadastro bem-sucedido oferece
entrada posterior com o e-mail preenchido; a senha jamais é retida após
sucesso ou troca de formulário.

### Impacto da revisão

Nenhum; v001 inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| User-value | prioritized | O aluno inicia UC01/UC02 pela web | Jornada documentada |
| Correctness | prioritized | Contratos e mensagens refletem respostas reais | API FastAPI analisada |
| Modifiability | prioritized | Sessão futura substitui somente fluxo posterior | FSD e cliente isolado |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Simplicity | Sem sessão, router global ou design system antes da necessidade | Uma página e estado local por formulário |
| Reliability | Falha compreensível sem perda não solicitada de dados | Estado de erro e reenvio controlados |
| Acessibilidade | Teclado, labels, erros associados e status anunciado | Elementos nativos e feedback semântico |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| User-value | Aluno não inicia a jornada pela plataforma | Alta | Estudantes e produto |
| Correctness | Tela pode prometer login quando só houve verificação | Alta | Estudantes e segurança |
| Reliability | Erro técnico apaga dados ou não orienta reenvio | Média | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Correctness | Mostrar confirmação limitada após `204`, sem redirecionar ao painel | Experiência de conclusão imediata | Aceitável até autenticação ser decidida |
| Modifiability | Criar estrutura FSD e cliente tipado antes do componente final | Delivery-speed inicial | Aceitável para evitar acoplamento precoce |
| Reliability | Implementar estados e testes além do formulário visual | Simplicity de implementação | Aceitável por ser fluxo crítico |

## Riscos e efeitos de segunda ordem

- Sem composição real no backend, a tela corretamente mostrará indisponibilidade
  (`503`), mas não poderá ser aceita como fluxo fim a fim.
- Sem CORS ou proxy de desenvolvimento definido, o navegador pode bloquear as
  chamadas mesmo que o backend esteja operacional.
- Tratar `204` como autenticação completa induziria uma falsa sensação de acesso
  e exigiria retrabalho quando token ou cookie forem definidos.
- Adicionar dependências Node fora do ambiente Nix violaria as regras do
  repositório e reduziria reprodutibilidade.
- A ausência de identidade visual torna a estética reversível; não deve atrasar
  semântica, responsividade e estados de formulário.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| A tela envia contratos corretos | Corpos e status observados pelo cliente mockado | Testes unitários de API/modelo | Divergência em contrato backend versionado |
| Estudante entende falhas | Erros por campo e mensagem geral compreensíveis | Revisão de UI e teste unitário de estados | Usuários não distinguem credencial inválida de indisponibilidade |
| FSD mantém fronteiras | Imports pela API pública e ausência de ciclos | Build/lint configurados na fundação | Necessidade de import ascendente ou entre slices pares |
| Cadastro e acesso funcionam fim a fim | Backend composto, CORS definido e ambiente integrado | Handoff de teste de integração | `503`, bloqueio CORS ou resposta incompatível |
| Próxima etapa pós-login é honesta | Requisito de sessão aprovado | Revisão de produto/segurança | Definição de token, cookie ou rota protegida |

## Handoffs e atividades posteriores

- **Ambientes/frontend:** declarar Node, gerenciador de pacotes, React,
  TypeScript, Vite e ferramentas de teste no ambiente Nix; criar o bootstrap
  mínimo. Esta preparação não deve ser escondida na implementação da tela.
- **Backend adapters/drivers:** compor `CadastrarEstudante`,
  `AcessarEstudante`, repositório, gerador de ID, derivador/verificador de senha
  e ciclo de sessão; definir CORS ou mecanismo equivalente para a origem do
  frontend.
- **Segurança/autenticação:** decidir mecanismo persistente de sessão,
  expiração, armazenamento e rota pós-login antes de proteger recursos ou
  redirecionar após `204`.
- **Integration/system testing:** após os handoffs, validar cadastro e acesso
  entre navegador/cliente e API real, incluindo contrato e CORS.
- **Produto/UI/UX:** fornecer identidade visual, política de privacidade e
  eventual requisito de e-mail institucional, se forem necessários ao aceite.

## Síntese

A tela é tecnicamente viável, mas não é uma simples adição de componente: o
repositório ainda não possui projeto React/TypeScript nem backend operacional
para as rotas. A decisão propõe fundação mínima seguida de uma página FSD com
cadastro e confirmação de credenciais, sem fingir sessão autenticada. Essa
separação permite entregar valor de interface agora e preservar uma evolução
segura quando autenticação e composição forem definidas.
