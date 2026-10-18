---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-18T13:31:00-03:00"
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
    - path: src/backend/application/assistente_descricao_projeto.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: planned
      revision: "issue #198"
      availability: available
    - path: src/backend/application/__init__.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "exportações públicas da camada Application"
      content_state: working-tree
      revision: "dev"
      availability: available
    - path: src/backend/tests/test_application_assistente_descricao_projeto.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: planned
      revision: "issue #198"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend]
  confidence: high
  rationale: "A decisão define um contrato da camada Application para o assistente de descrição de projetos."
classification:
  sphere: engineering
  concerns: [application, architecture, testing]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: medium
  uncertainty: low
  reversibility: moderate
  risk: low
---

# Análise de decisão — Contrato do assistente de descrição de projeto

## Solicitação original

> Issue #198: [F4.8] Definir contrato do assistente de descrição de projeto:
> entrada, saída, erro e implementação ausente.

## Contexto

O RF04 prevê o cadastro de projetos acadêmicos e uma orientação para que o
estudante consiga descrever seus projetos de forma clara e objetiva.

Os requisitos de modularidade também determinam que o assistente não dependa
obrigatoriamente de inteligência artificial e possa receber diferentes
implementações no futuro.

A issue #198 não solicita a estratégia concreta de geração da descrição. Essa
implementação pertence às issues posteriores da mesma fatia.

## Problema

É necessário definir um contrato interno que permita aos consumidores da
camada Application solicitar uma sugestão de descrição sem depender de API,
infraestrutura, inteligência artificial ou de uma implementação concreta.

O contrato deve tornar explícitos:

- os dados de entrada;
- os dados de saída;
- a falha controlada de indisponibilidade;
- a interface esperada das implementações;
- o comportamento quando nenhuma implementação estiver configurada.

## Alternativas consideradas

### Alternativa 1 — Contrato tipado e implementação ausente explícita

Definir DTOs imutáveis de entrada e saída, uma exceção específica, um
`Protocol` assíncrono e uma implementação ausente que sempre produza a falha
controlada.

Vantagens:

- mantém a camada Application desacoplada;
- permite implementação determinística ou externa no futuro;
- torna o cenário sem implementação explicitamente testável;
- evita dependência de IA ou provedor específico.

Desvantagem:

- adiciona tipos específicos mesmo antes da estratégia concreta existir.

### Alternativa 2 — Função concreta sem contrato

Criar diretamente uma função que produza a descrição.

Rejeitada porque anteciparia a estratégia de geração e dificultaria a troca de
implementação.

### Alternativa 3 — Dependência direta de API ou serviço de IA

Rejeitada porque criaria dependência de infraestrutura na camada Application e
contrariaria a modularidade prevista para o assistente.

## Decisão

Adotar a Alternativa 1.

A entrada será representada por `AssistenteDescricaoProjetoEntrada`, contendo
`título` e `tecnologias`.

A saída será representada por `AssistenteDescricaoProjetoSaida`, contendo a
descrição sugerida.

`AssistenteDescricaoProjeto` será um `Protocol` com operação assíncrona
`sugerir_descricao`.

`AssistenteDescricaoProjetoIndisponivel` representará a falha controlada.

`AssistenteDescricaoProjetoAusente` representará explicitamente o cenário em
que nenhuma estratégia estiver configurada.

O contrato será exportado publicamente pelo pacote
`backend.application`, seguindo o padrão atual da camada.

## Escopo

Incluído:

- contrato de entrada;
- contrato de saída;
- interface do assistente;
- erro de indisponibilidade;
- implementação ausente;
- exportação pelo pacote Application;
- testes unitários do contrato.

Fora do escopo:

- geração determinística da descrição;
- integração com IA;
- integração com API externa;
- exposição HTTP da sugestão;
- alterações de frontend.

## Critérios de sucesso

1. Entrada e saída possuem campos e tipos verificáveis.
2. Entrada e saída são imutáveis.
3. A interface possui assinatura assíncrona estável.
4. A implementação ausente produz erro controlado.
5. Todos os símbolos do contrato são exportados pelo pacote Application.
6. O teste unitário é executável junto do arquivo de produção na mesma branch.
