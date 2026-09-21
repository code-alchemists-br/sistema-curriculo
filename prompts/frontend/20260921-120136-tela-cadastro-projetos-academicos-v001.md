---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-09-21T12:01:36-03:00"
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
    - path: src/frontend/app/App.tsx
      relationship: primary
      representation: source-code
      function: production
      format: TypeScript/React
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "383122b"
      availability: available
    - path: src/frontend/pages/acesso-estudante/ui/PaginaAcessoEstudante.tsx
      relationship: supporting
      representation: source-code
      function: production
      format: TypeScript/React
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "383122b"
      availability: available
    - path: src/frontend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "383122b"
      availability: available
    - path: src/backend/domain/itens_perfil.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ProjetoAcademico"
      content_state: commit
      revision: "383122b"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: documentation
      format: markdown/mermaid
      analysis_scope: selected-section
      locator: "PROJETO_ACADEMICO e CURRICULO_PROJETO"
      content_state: commit
      revision: "383122b"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF02, RF04, RF13 e detalhamentos necessários"
      content_state: commit
      revision: "383122b"
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RNF01 a RNF04 e RNF09 a RNF10"
      content_state: commit
      revision: "383122b"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/frontend
  considered_directories: [prompts/frontend, prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "O objetivo primário é uma tela React; domínio e requisitos sustentam campos e handoffs."
classification:
  sphere: engineering
  concerns: [implementation, integration, user-experience]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: high
  reversibility: moderate
  risk: medium
---

# Análise de decisão — tela de cadastro de projetos acadêmicos

## Solicitação original

$decision-analysis-v4 Faça uma análise para o card "Implementar tela para cadastro de projetos acadêmicos." APIs e outras necessidades de backend inexistentes serão cobertas por doubles de testes apropriados.

## Informações complementares

- O frontend existente usa React, TypeScript, Vite, Vitest e Feature-Sliced Design.
- A aplicação compõe somente a página de cadastro e acesso; não há router, sessão persistente nem identidade de estudante no cliente.
- O domínio contém ProjetoAcademico, mas não há caso de uso, porta de repositório, persistência ou rota HTTP para projetos.
- O DER descreve titulo, descricao e tecnologias; não especifica obrigatoriedade, limites ou formato de tecnologias.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem da tela de projetos acadêmicos | Nenhum identificado | v001 inicial | Não há análise anterior específica para esse card | Nenhum histórico a preservar |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| src/frontend/app/App.tsx | Principal | Código-fonte | Produção | TypeScript/React | Arquivo completo | Commit 383122b |
| src/frontend/pages/acesso-estudante/ui/PaginaAcessoEstudante.tsx | Apoio | Código-fonte | Produção | TypeScript/React | Arquivo completo | Commit 383122b |
| src/frontend/AGENTS.md | Contexto | Prosa | Instrução | Markdown | Arquivo completo | Commit 383122b |
| src/backend/domain/itens_perfil.py | Apoio | Código-fonte | Produção | Python | ProjetoAcademico | Commit 383122b |
| docs/modelagem_der.md | Apoio | Modelo de diagrama | Documentação | Mermaid | Projeto acadêmico e sua associação | Commit 383122b |
| docs/requisitos_funcionais.md | Apoio | Prosa | Documentação | Markdown | RF02, RF04, RF13 e pendências | Commit 383122b |
| docs/requisitos_nao_funcionais.md | Contexto | Prosa | Documentação | Markdown | RNF01–RNF04 e RNF09–RNF10 | Commit 383122b |

### Limites da evidência dos artefatos

Não há wireframe, rota de navegação, contrato HTTP, identidade autenticada,
limites de campos nem vocabulário para tecnologias. A ausência de referências
de projeto na API confirma que não há endpoint disponível, mas não autoriza a
tela a criar contrato de produção ou persistir dados localmente.

## Problema enriquecido

### Resultado desejado

Oferecer uma unidade React para informar título, descrição e tecnologias de um
projeto acadêmico, com orientação breve, validação de experiência, estados
claros de envio e falha e testes unitários determinísticos com doubles.

### Atores e interesses

- O estudante precisa registrar um projeto para selecioná-lo futuramente em versões do currículo.
- O frontend precisa de uma página FSD sem HTTP em componentes nem dados de autenticação inexistentes.
- O backend precisa definir caso de uso, propriedade, persistência e contrato antes da integração real.
- O produto precisa decidir campos obrigatórios, limites e o ponto da jornada da tela.

### Evidências e fatos observados

- RF04 exige registrar projetos acadêmicos e orientar descrições claras e objetivas.
- RF02 prevê consulta, edição e exclusão em geral, mas este card restringe-se ao cadastro.
- DER e domínio convergem em titulo, descricao e tecnologias, com proprietário usuario_id e UUID.
- O frontend exige labels, erros associados, teclado, responsividade, APIs públicas de slices e separação de DTOs.
- Não há endpoint nem identidade cliente que associe um projeto ao estudante com segurança.

### Hipóteses

- Formulário de uma página com três campos de texto livre atende ao modelo sem inventar taxonomia ou IA.
- A orientação será estática, indicando objetivo, contribuição e tecnologias, sem gerar conteúdo.
- Um cliente injetável permite testar sucesso, indisponibilidade e resposta inválida sem tornar double uma dependência de produção.

### Perguntas em aberto

- Quais campos são obrigatórios, seus limites e o formato de tecnologias: texto, lista ou tags?
- Em qual rota ou etapa a página aparecerá depois que houver sessão?
- Como a identidade autenticada preencherá usuario_id sem expor esse campo à tela?
- A lista, edição e exclusão serão card posterior ou parte do mesmo fluxo?

### Escopo

- Criar página ou slice FSD de cadastro com titulo, descricao e tecnologias.
- Manter valores, erros, envio, sucesso e falha como estado local.
- Criar contrato de cliente explícito, DTO separado do estado de UI e fronteira substituível por HTTP futuro.
- Validar somente experiência local; regras definitivas continuam no backend.
- Criar testes unitários de modelo e formulário com doubles para sucesso, indisponibilidade e resposta inválida.

### Fora do escopo

- Caso de uso, rota, banco, migração, autorização ou outro código backend.
- Sessão, identidade, rota protegida, CORS ou navegação global.
- Persistência local, dados simulados em produção, lista, edição e exclusão de projetos.
- IA, design system, internacionalização e testes de integração, contrato, sistema ou E2E.

### Critérios de sucesso

- Página e feature preservam FSD, API pública, ausência de ciclos e de HTTP em UI.
- Campos têm labels, erros associados, foco previsível, status semântico e layout móvel/desktop funcional.
- Envio entrega somente titulo, descricao e tecnologias ao contrato do cliente e preserva valores após falha.
- Sucesso não afirma persistência quando não houver cliente real configurado; doubles existem somente nos testes.
- Testes não acessam rede e cobrem validação, tradução de falhas e interação com cliente substituído.

## Restrições aplicáveis

- React, TypeScript, FSD, API pública por slice e separação de transporte, domínio e UI são obrigatórios.
- Shared não pode conhecer projetos; componentes visuais não podem fazer HTTP.
- Autenticação, autorização e persistência não podem ser simuladas como comportamento de produção.
- Mudança de comportamento exige testes unitários no ambiente Nix frontend.
- O fluxo não pode depender de IA.

## Classificação comentada

É decisão de engenharia para uma tela de negócio. Implementação e experiência
do usuário são centrais; integração importa porque o domínio existe, mas a
fronteira HTTP não. A incerteza é alta pela ausência de contrato, identidade e
posição na navegação, embora os três campos delimitem a unidade.

## Decisão de roteamento

prompts/frontend é o destino mais específico: o produto imediato é uma tela
React e testes unitários. prompts/backend foi considerada pela ausência de
contrato, mas é handoff; prompts/requisitos é fonte dos campos, não o alvo.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| User-value | Alta | Priorizar | Projetos são informação reutilizável do currículo conforme RF04 |
| Correctness | Alta | Satisfazer | A tela não deve inventar propriedade, API ou persistência |
| Simplicity | Alta | Priorizar | Três campos evitam antecipar lista, tags ou IA |
| Modifiability | Média | Priorizar | Cliente injetável permite conectar o backend depois |
| Delivery-speed | Média | Priorizar | Doubles unitários permitem avançar sem API |
| Reliability | Média | Satisfazer | Falhas devem orientar e manter valores |

## Alternativas consideradas

### A — Página FSD com contrato de cliente injetável e doubles apenas nos testes

Implementa formulário, modelo de UI e mensagens; a composição futura fornece o
cliente real. É a recomendada porque entrega a unidade sem criar infraestrutura
ou fonte de verdade paralela.

### B — Persistir projetos em memória ou localStorage enquanto não há backend

Demonstra um fluxo aparentemente completo, mas cria dados sem proprietário
autenticado, retenção ou sincronização. É rejeitada: double de teste não deve
ser persistência de produto.

### C — Implementar primeiro a vertical completa no backend e integrar a tela

Resolveria o contrato real, mas amplia o card para domínio, aplicação,
persistência, API e autenticação. É inviável nesta fatia e deve virar atividade
backend própria.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| User-value | Alta | +1 | +1 | +2 | Média | C também persiste |
| Correctness | Alta | +2 | -2 | +2 | Alta | Não há API, identidade ou armazenamento |
| Simplicity | Alta | +2 | +1 | -2 | Alta | A limita-se à tela |
| Modifiability | Média | +2 | -1 | +1 | Alta | Interface separa UI e transporte |
| Delivery-speed | Média | +2 | +1 | -2 | Alta | Backend completo excede o card |
| Reliability | Média | +1 | -1 | +2 | Média | B perde dados e cria expectativa incorreta |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### Decisão recomendada nesta versão

Adotar a alternativa A. Criar pages/projetos-academicos e uma feature local ou
features/cadastro-projeto-academico conforme a reutilização concreta. A página
deve ser composável por API pública e não substituir a página de acesso atual
enquanto sessão e navegação não forem definidas.

O formulário delega a ClienteProjetosAcademicos. A composição de produção deve
apresentar indisponibilidade até existir contrato real; testes recebem double
tipado para simular sucesso, indisponibilidade e resposta incompatível. Nenhum
double deve afirmar que um projeto foi persistido fora do teste.

### Impacto da revisão

Nenhum; v001 inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Correctness | prioritized | Não prometer persistência ou autorização inexistentes | Não há endpoint nem sessão |
| Simplicity | prioritized | Manter três campos e uma intenção de cadastro | DER e RF04 |
| Modifiability | prioritized | Substituir double por HTTP sem reescrever UI | Cliente explícito |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| User-value | Estudante preenche a informação solicitada | Formulário orientado e feedback observável |
| Reliability | Falha não apaga dados | Estado local e tradução de erro |
| Acessibilidade | Teclado, labels e erros compreensíveis | HTML nativo e status semântico |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| User-value | Projetos não podem ser preparados para o currículo | Média | Estudantes e produto |
| Correctness | UI pode mascarar ausência de persistência e proprietário | Alta | Estudantes e equipe |
| Modifiability | Integração futura exige reescrever componentes | Média | Frontend |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Correctness | Não demonstrar lista persistente sem backend | Conclusão imediata | Aceitável até contrato existir |
| Simplicity | Tecnologias ficam como texto livre | Estruturação avançada | Aceitável sem vocabulário aprovado |
| Modifiability | Interface de cliente e doubles unitários | Velocidade inicial | Aceitável para evitar API hipotética |

## Riscos e efeitos de segunda ordem

- Integrar diretamente ao App pode remover a porta de acesso ou expor fluxo sem estudante autenticado.
- Tornar campos obrigatórios ou definir limites agora pode divergir de produto e backend.
- Usar o double como fallback de produção pode fazer o estudante acreditar que seus dados foram salvos.
- Uma futura lista de tecnologias exigirá adaptação de DTO e modelo, mas não precisa reescrever a UI inteira.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Campos representam o domínio atual | Entidade e contrato backend aprovados | Revisão antes da integração | Contrato exigir formato diferente |
| Formulário orienta sem rede | Estados observáveis com double | Testes unitários de modelo e UI | Usuário não consegue corrigir entrada |
| UI fica desacoplada | API pública e cliente injetado | Typecheck e revisão de imports | UI precisar conhecer HTTP ou usuário |
| Persistência real funciona | Caso de uso, API, sessão e CORS definidos | Handoff de integração | Endpoint ou identidade divergente |

## Handoffs e atividades posteriores

- Backend: definir comandos, caso de uso, repositório, persistência, propriedade e contrato HTTP.
- Produto/requisitos: decidir obrigatoriedade, limites, formato de tecnologias e ponto de navegação.
- Autenticação/autorização: fornecer identidade de estudante e rota protegida.
- Integration/system testing: após os handoffs, validar tela, API, CORS, persistência e propriedade com $integration-system-testing-v1.

## Síntese

O card é viável como unidade de frontend porque o domínio e DER delimitam três
campos. Não é viável como cadastro persistente fim a fim: faltam contrato,
caso de uso, identidade e rota. A decisão entrega uma página composável,
validação local e doubles exclusivos de testes, mantendo o backend como fonte
de verdade quando ele existir.
