---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-09-21T16:27:49-03:00"
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
    - path: src/backend/domain/itens_perfil.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ExperienciaProfissional"
      content_state: commit
      revision: "e12c3e8"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ExperienciaProfissionalId e Periodo"
      content_state: commit
      revision: "e12c3e8"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e12c3e8"
      availability: available
    - path: docs/mapeamento_jornadas.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "UC04 e seção 6.5"
      content_state: commit
      revision: "e12c3e8"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: markdown/mermaid
      analysis_scope: selected-section
      locator: "EXPERIENCIA_PROFISSIONAL"
      content_state: commit
      revision: "e12c3e8"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e12c3e8"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e12c3e8"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/frontend]
  confidence: high
  rationale: "A decisão cria comportamento de Domain, caso de uso e portas do backend; requisitos apenas sustentam UC04."
classification:
  sphere: engineering
  concerns: [domain, architecture, implementation]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — cadastro de experiências profissionais

## Solicitação original

$decision-analysis-v4 Implementar cadastro de experiências profissionais com relação às camadas de casos de uso e domain. Use doubles de teste apropriados para testes unitários.

## Informações complementares

- UC04 prevê cadastrar experiência profissional.
- A entidade ExperienciaProfissional já existe no domínio, com id, usuario_id, empresa, cargo, descricao e periodo.
- Periodo já representa início obrigatório e fim opcional com validação cronológica.
- Não há caso de uso, porta, repositório, API, adapter ou teste específico de experiências.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem de cadastro de experiências | Nenhum identificado | v001 inicial | Não existe análise anterior específica de UC04 | Nenhum histórico a preservar |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| src/backend/domain/itens_perfil.py | Principal | Código-fonte | Produção | Python | ExperienciaProfissional | Commit e12c3e8 |
| src/backend/domain/value_objects.py | Principal | Código-fonte | Produção | Python | ID e Periodo | Commit e12c3e8 |
| src/backend/application/ports.py | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit e12c3e8 |
| docs/mapeamento_jornadas.md | Apoio | Prosa | Documentação | Markdown | UC04 e seção 6.5 | Commit e12c3e8 |
| docs/modelagem_der.md | Apoio | Diagrama | Contrato de schema | Mermaid | EXPERIENCIA_PROFISSIONAL | Commit e12c3e8 |
| AGENTS.md e src/backend/AGENTS.md | Contexto | Prosa | Instrução | Markdown | Arquivos completos | Commit e12c3e8 |

### Limites da evidência dos artefatos

Não há limites de texto, política para experiência atual, contrato HTTP,
persistência de experiências, autenticação ou definição de edição/exclusão
além da referência de jornada. A análise não cria API nem decide políticas de
autorização ou banco.

## Problema enriquecido

### Resultado desejado

Permitir que o estudante registre uma experiência profissional reutilizável,
com empresa, cargo, descrição e período válido, por um caso de uso independente
de infraestrutura e verificável com doubles.

### Atores e interesses

- O estudante precisa cadastrar experiências para compor currículos.
- O domínio precisa manter proprietário, identidade e período válido.
- A Application precisa orquestrar geração de ID e persistência sem ORM.
- A equipe precisa evoluir UC04 sem misturar experiência a uma versão de currículo.

### Evidências e fatos observados

- UC04 e a jornada preveem lista e formulário para adicionar ou editar experiências.
- O DER e a entidade convergem nos campos empresa, cargo, descricao, data_inicio e data_fim.
- ExperienciaProfissional já é item reutilizável do perfil com usuario_id.
- Periodo já protege a relação cronológica; não há adapter ou porta de experiência.
- O projeto exige doubles em testes unitários e dependências apontadas para dentro.

### Hipóteses

- O cadastro inicial cria somente uma experiência, sem editar, excluir ou associar currículo.
- UsuarioId vem de fronteira confiável futura; não se decide API ou autorização agora.
- Empresa, cargo e descrição devem ser textos não vazios; período é criado pelo value object existente.
- Experiência em andamento é representada por fim ausente, sem campo booleano adicional.

### Perguntas em aberto

- Quais limites e vocabulários de empresa, cargo e descrição serão aplicados?
- Como a interface indicará experiência atual?
- Quais regras de edição, exclusão e uso em currículos serão priorizadas depois?
- Como API e autorização fornecerão UsuarioId sem confiar em ID arbitrário?

### Escopo

- Criar uma fábrica ou transição explícita de domínio para construir ExperienciaProfissional válida.
- Criar CadastrarExperienciaProfissional, sua entrada e falha de aplicação quando necessária.
- Criar portas mínimas de repositório e geração de ExperienciaProfissionalId.
- Criar testes unitários de domínio e Application com doubles determinísticos.
- Reutilizar Periodo, UsuarioId e a entidade existente, sem converter DTOs em domínio.

### Fora do escopo

- API, DTO HTTP, autenticação, autorização, ORM, migration, banco ou adapter.
- Edição, exclusão, lista, associação ao currículo, importação ou IA.
- Validações de comprimento, vocabulários corporativos e políticas trabalhistas não definidas.
- Testes de integração, sistema ou E2E.

### Critérios de sucesso

- A experiência criada conserva ID tipado e UsuarioId, e contém textos não vazios e Periodo válido.
- O caso de uso gera ID por porta, constrói o item e solicita salvar por porta assíncrona.
- Nenhuma regra de negócio depende de ORM, API, banco ou relógio.
- Tests cobrem sucesso, texto vazio, período inválido e ausência de salvar quando a construção falha.
- Doubles não usam rede, banco ou aleatoriedade real.

## Restrições aplicáveis

- Domain permanece independente de Application e infraestrutura.
- Application depende de portas internas e não executa I/O diretamente.
- Invariantes ficam no domínio; entradas da Application usam value objects.
- Toda função, classe e DTO requer documentação completa.
- Testes unitários futuros rodam em nix develop .#backend.

## Classificação comentada

A decisão é engineering, com foco em domain por construir item válido,
architecture por introduzir portas e implementation por entregar UC04. O risco
é médio: a entidade já delimita dados e período, mas propriedade e persistência
reais dependem de atividades posteriores.

## Decisão de roteamento

prompts/backend é o destino mais específico porque os artefatos alvo são
Domain, Application e portas. prompts/requisitos sustenta campos e jornada;
prompts/frontend trata a futura tela, fora da atividade atual.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Correctness | Alta | Priorizar | Período e propriedade precisam permanecer válidos |
| Modifiability | Alta | Priorizar | Caso de uso não deve depender de banco ou API |
| Simplicity | Média | Satisfazer | Reutilizar entidade e Periodo existentes |
| Delivery-speed | Média | Priorizar | Doubles permitem testes antes de adapters |

## Alternativas consideradas

### A — Item de perfil reutilizável com caso de uso e portas mínimas

Criar pela própria entidade e persistir por RepositorioExperienciaProfissional,
com GeradorExperienciaProfissionalId substituível. É recomendada: preserva
limites existentes e permite associação futura a currículos.

### B — Inserir experiência diretamente dentro de Curriculo

Acopla uma experiência a uma única versão e contradiz o DER, que indica item
do usuário reutilizável por mais de um currículo. É rejeitada.

### C — Criar diretamente no controller ou adapter

Mistura regra, construção e I/O, viola Clean Architecture e impede testes
isolados. É rejeitada.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Correctness | Alta | +2 | -1 | -1 | Alta | DER e entidade existente |
| Modifiability | Alta | +2 | -2 | -2 | Alta | Portas isolam infraestrutura |
| Simplicity | Média | +1 | 0 | +1 | Alta | Reuso evita novo agregado |
| Delivery-speed | Média | +1 | 0 | +1 | Média | Doubles removem dependência de adapter |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### Decisão recomendada nesta versão

Adotar a alternativa A. Manter ExperienciaProfissional como entidade reutilizável
de perfil e introduzir uma construção de domínio que recuse empresa, cargo ou
descrição vazios, delegando cronologia a Periodo. Criar CadastrarExperienciaProfissional
para gerar ExperienciaProfissionalId, receber UsuarioId e valores tipados,
construir a entidade e salvar por porta.

Os testes devem usar gerador e repositório doubles, controlando ID e lista de
itens salvos. Não devem criar API, banco, ORM ou fonte de identidade
autenticada. A persistência real, endpoints e autorização são handoffs.

### Impacto da revisão

Nenhum; v001 inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Correctness | prioritized | Impede texto vazio e período cronologicamente inválido | Entidade e Periodo |
| Modifiability | prioritized | Troca adapter sem reescrever o caso de uso | Portas explícitas |
| Delivery-speed | prioritized | Testa criação sem infraestrutura | Doubles controlados |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Simplicity | Não criar agregado adicional | Reutiliza item de perfil existente |
| Reliability | Falha não solicita persistência | Construção antecede salvar |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Correctness | Experiências sem dados ou período coerente | Média | Estudantes |
| Modifiability | Caso de uso acoplado ao banco | Média | Equipe |
| Delivery-speed | UC04 bloqueada por infraestrutura | Média | Produto |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Correctness | Fábrica e portas adicionais | Simplicity | Aceitável para proteger invariantes |
| Modifiability | Persistência real fica posterior | Time-to-value fim a fim | Aceitável sem adapter existente |
| Simplicity | Não modelar edição nesta entrega | Optionality | Aceitável por limitar o card |

## Riscos e efeitos de segunda ordem

- Sem autorização, UsuarioId deve ser recebido somente de fronteira confiável futura.
- Sem migration e adapter, o caso de uso não produz cadastro persistente fim a fim.
- Limites de texto e experiências atuais podem exigir revisão quando o produto os definir.
- Associação a currículo deve preservar o item independente, não duplicar dados.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Entidade representa UC04 | DER e jornada atuais | Revisão de código e requisitos | Campos adicionais obrigatórios |
| Período é válido | Testes com fim anterior ao início | Unitário de domínio | Período inválido aceito |
| Caso não depende de I/O concreto | Doubles de repositório e gerador | Unitário Application | ORM ou rede importados |
| Reuso em currículos permanece possível | Nenhuma referência a Curriculo na criação | Revisão de arquitetura | Cadastro exigir currículo específico |

## Handoffs e atividades posteriores

- Infraestrutura: implementar adapter, mapeamento Code First e migration.
- API/autorização: expor contrato e derivar UsuarioId de identidade autenticada.
- Produto: definir limites, experiência atual, edição, exclusão e lista.
- Integration/system testing: validar persistência e fluxos HTTP após os handoffs.

## Síntese

UC04 possui entidade e value objects, mas não caso de uso nem porta. A decisão
cria uma fatia limpa de Domain/Application para cadastrar experiência válida e
testável por doubles, preservando sua reutilização em currículos e deixando
infraestrutura e autorização para atividades posteriores.
