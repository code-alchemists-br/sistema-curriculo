---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-09-21T23:51:40-03:00"
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
      locator: "ProjetoAcademico"
      content_state: working-tree
      revision: "working-tree based on 6759a53"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ProjetoAcademicoId"
      content_state: working-tree
      revision: "working-tree based on 6759a53"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "Portas de experiência profissional"
      content_state: working-tree
      revision: "working-tree based on 6759a53"
      availability: available
    - path: src/backend/application/cadastro_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 6759a53"
      availability: available
    - path: src/backend/tests/test_application_cadastro_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 6759a53"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF02, RF04, RF13 e detalhamentos"
      content_state: working-tree
      revision: "working-tree based on 6759a53"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: markdown/mermaid
      analysis_scope: selected-section
      locator: "PROJETO_ACADEMICO e CURRICULO_PROJETO"
      content_state: working-tree
      revision: "working-tree based on 6759a53"
      availability: available
    - path: prompts/frontend/20260921-120136-tela-cadastro-projetos-academicos-v001.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Decisão e lacunas de integração"
      content_state: working-tree
      revision: "working-tree based on 6759a53"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 6759a53"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 6759a53"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/frontend, prompts/requisitos]
  confidence: high
  rationale: "Decide Domain, Application, portas e testes de backend; tela e requisitos são evidência."
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

# Análise de decisão — cadastro de projetos acadêmicos

## Solicitação original

$decision-analysis-v4 Implementar cadastro de projetos acadêmicos com relação às camadas de casos de uso e domain. Use doubles de teste apropriados para testes unitários.

## Informações complementares

`ProjetoAcademico` e `ProjetoAcademicoId` existem, com `usuario_id`, `titulo`, `descricao` e `tecnologias`; RF04 requer registrar projetos. Não há caso de uso, porta, adapter, API, persistência ou teste de projetos. O cadastro de experiências profissionais fornece precedente local de entrada tipada, portas, spy e stub.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem backend de projetos | Nenhum identificado | v001 inicial | Não há análise anterior | Nenhum histórico |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `itens_perfil.py` | Principal | Código-fonte | Produção | Python | `ProjetoAcademico` | Working tree baseado em 6759a53 |
| `value_objects.py` | Principal | Código-fonte | Produção | Python | `ProjetoAcademicoId` | Working tree baseado em 6759a53 |
| `ports.py` e cadastro de experiência | Apoio | Código-fonte | Produção | Python | Portas e caso análogo | Working tree baseado em 6759a53 |
| Requisitos e DER | Apoio | Prosa/diagrama | Documentação/contrato | Markdown/Mermaid | RF04 e projeto | Working tree baseado em 6759a53 |
| Instruções raiz e backend | Contexto | Prosa | Instrução | Markdown | Arquivos completos | Working tree baseado em 6759a53 |

### Limites da evidência dos artefatos

Não há política de obrigatoriedade, limites ou formato de tecnologias; também faltam contrato HTTP, sessão, adapter e migration. A decisão cobre somente o núcleo testável.

## Problema enriquecido

### Resultado desejado

Cadastrar projeto reutilizável com identidade e proprietário explícitos por caso de uso independente de ORM, API e banco, testável com doubles.

### Atores e interesses

Estudante registra projetos; domínio protege conteúdo apresentável; Application orquestra sem infraestrutura; futura API deriva `UsuarioId` da sessão.

### Evidências e fatos observados

DER, entidade e RF04 convergem nos três textos e proprietário. A entidade não valida textos. As instruções exigem invariantes no Domain, portas internas e testes sem I/O.

### Hipóteses

Título, descrição e tecnologias são textos obrigatórios não vazios; tecnologias permanece `str`; persistência segue contrato assíncrono local.

### Perguntas em aberto

Quais limites, normalizações e formato de tecnologias? Como a UI orientará a descrição? Como a borda autenticada deriva o proprietário?

### Escopo

Validar `ProjetoAcademico`; criar entrada, caso de uso, repositório e gerador de ID; exportar API pública aplicável; testar com spy e stub.

### Fora do escopo

ORM, migration, banco, API, autenticação, lista, edição, exclusão, associação ao currículo, IA e testes de integração são Nenhum identificado nesta fatia.

### Critérios de sucesso

Entidade recusa textos inválidos; caso de uso salva uma única entidade válida e não salva após falha; testes não usam banco, rede, ORM ou UUID aleatório.

## Restrições aplicáveis

Domain não depende de Application, API ou infraestrutura; Application usa apenas portas. Invariantes ficam na entidade. Novas classes, funções e DTOs têm docstrings completas. Testes unitários rodam no Nix `backend`.

## Classificação comentada

A decisão é de engenharia de componente com preocupações de domínio, arquitetura e implementação: o modelo existe sem invariante e a intenção não possui orquestração.

## Decisão de roteamento

`prompts/backend` é mais específico para Domain, Application, portas e testes. `prompts/frontend` e `prompts/requisitos` são evidência e handoff.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Correctness | Alta | Satisfazer | Item incompleto não compõe currículo. |
| Modifiability | Alta | Priorizar | Portas isolam adapter e API futuros. |
| Simplicity | Alta | Priorizar | Evita antecipar requisitos ausentes. |
| Reliability | Média | Satisfazer | Falha não pode salvar. |
| Delivery-speed | Média | Priorizar | Doubles evitam infraestrutura. |

## Alternativas consideradas

### A — Caso de uso específico, invariante no domínio e portas estreitas

Validar os textos na entidade; criar entrada, gerador, repositório e orquestração; testar com stub e spy. Recomendada.

### B — Validar somente no caso de uso

Permite entidade inválida por outros caminhos e desloca regra de negócio do domínio; inviável pelas restrições DDD.

### C — Vertical completa com ORM, API e tela

Exige schema, adapter, contrato e autenticação ainda sem evidência, ampliando indevidamente a demanda; inviável nesta fatia.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Correctness | Alta | +2 | -2 | +2 | Alta | Invariantes pertencem à entidade. |
| Modifiability | Alta | +2 | +1 | +1 | Alta | Portas isolam infraestrutura. |
| Simplicity | Alta | +2 | +1 | -2 | Alta | C amplia a fatia. |
| Reliability | Média | +2 | -1 | +2 | Alta | A constrói antes de salvar. |
| Delivery-speed | Média | +2 | +1 | -2 | Alta | A usa testes locais. |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### Decisão recomendada nesta versão

Adotar A: `CadastrarProjetoAcademico` recebe `UsuarioId` e três textos, gera `ProjetoAcademicoId` por `GeradorProjetoAcademicoId`, cria a entidade e chama `RepositorioProjetoAcademico.salvar` só após validação. A entidade lança `RegraDeDominioViolada` para campo não textual, vazio ou apenas espaços, sem impor limites, normalização, taxonomia ou coleção de tecnologias. Usar `GeradorProjetoAcademicoIdStub` e `RepositorioProjetoAcademicoSpy` assíncrono; cobrir sucesso e ausência de salvamento na falha.

### Impacto da revisão

Nenhum — análise inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Modifiability | prioritized | Adapter e API conectáveis sem dependência reversa. | Clean Architecture. |
| Simplicity | prioritized | Fatia limitada ao núcleo. | Escopo explícito. |
| Delivery-speed | prioritized | Testes determinísticos. | Spy e stub locais. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Correctness | Nenhum item sem textos essenciais. | Entidade valida campos. |
| Reliability | Falha não persiste. | Construção precede `salvar`. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Correctness | Projeto inútil em currículo. | Alta | Estudante e recrutador. |
| Modifiability | Infraestrutura contamina caso de uso. | Média | Equipe. |
| Reliability | Entidade inválida é enviada ao armazenamento. | Média | Estudante. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Correctness | Regras e testes extras. | Delivery-speed | Aceitável. |
| Modifiability | Duas abstrações antes do adapter. | Simplicity | Aceitável; dependências reais. |
| Simplicity | Sem endpoint nesta fatia. | User-value imediato | Aceitável; fora do escopo. |

## Riscos e efeitos de segunda ordem

Tecnologias em texto obrigatório pode divergir de tags futuras; revisar quando houver decisão de produto. A API não deve aceitar `UsuarioId` livre do cliente. O precedente não justifica abstração genérica, pois invariantes diferem.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Entidade protege textos | Exceção por campo inválido | Testes Domain | Campo opcional ou estruturado. |
| Caso de uso é independente | Imports apenas Domain e Protocols | Revisão e Nix backend | Transação ou consulta real. |
| Falha não persiste | Spy vazio após exceção | Teste assíncrono | Idempotência aprovada. |
| DTO espelha modelo | Proprietário e três campos | Revisão | DER/RF04 mudar. |

## Handoffs e atividades posteriores

Implementar adapter ORM Code First, migration e integração quando autorizados. Definir API autenticada, limites, normalização, formato de tecnologias e orientação de RF04; revisar a decisão então. Integrar a tela apenas após contrato HTTP.

## Síntese

Modo `initial`; classificação `engineering` com domínio, arquitetura e implementação; objeto misto de demanda e artefatos backend. Recomenda-se caso de uso específico com invariantes mínimas, duas portas e doubles locais. Sem revisão anterior. Incerteza principal: obrigatoriedade, limites e representação de tecnologias.
