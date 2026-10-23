---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-19T18:29:07-03:00"
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
    - path: "code-alchemists-br/sistema-curriculo#243"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: whole-file
      locator: "título, descrição e critério de aceite da issue #243"
      content_state: external
      revision: null
      availability: available
    - path: "code-alchemists-br/sistema-curriculo#130"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: selected-section
      locator: "linhagem e decisão das issues #130/#131/#132 registrada em v004"
      content_state: external
      revision: null
      availability: available
    - path: prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md
      relationship: primary
      representation: prose
      function: decision-record
      format: Markdown
      analysis_scope: selected-section
      locator: "decisões de domínio, contrato do repositório e documentos de revisão da associação currículo-vaga"
      content_state: working-tree
      revision: v004
      availability: available
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: application-contract
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioCurriculo, RepositorioAssociacaoCurriculoVaga e contrato mínimo de persistência"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/associacao_curriculo_vaga.py
      relationship: primary
      representation: source-code
      function: use-case
      format: Python
      analysis_scope: selected-section
      locator: "criação e atualização de classificações com verificação de ownership"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/listagem_versoes_curriculo.py
      relationship: primary
      representation: source-code
      function: use-case
      format: Python
      analysis_scope: whole-file
      locator: "padrão da Application para listar entidades próprias de um estudante"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/associacao_curriculo_vaga.py
      relationship: primary
      representation: source-code
      function: domain-model
      format: Python
      analysis_scope: whole-file
      locator: "agregado, regras de domínio e classificações"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_application_associacao_curriculo_vaga.py
      relationship: supporting
      representation: test
      function: unit-test
      format: Python
      analysis_scope: selected-section
      locator: "stubs de ownership, duplicidade e persistência para a associação"
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "A demanda é de backend/application e a evidência está concentrada em casos de uso, ports e domínio da associação currículo-vaga."
classification:
  sphere: engineering
  concerns: [domain, architecture, implementation]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: medium
---

# Análise de decisão — Consulta paginada das associações de um estudante (#243)

## Solicitação original

> Modelar consulta paginada das associações de um estudante.
>
> Objetivo: determinar a implementação mínima, verificável isoladamente e compatível com a arquitetura atual.
>
> Restrições da análise:
>
> - não implementar código;
> - não alterar arquivos existentes;
> - não fazer commits, push ou PR;
> - não ampliar o escopo para endpoints HTTP da #244;
> - não redesenhar a arquitetura;
> - evitar leituras fora da fatia vertical;
> - basear a decisão em contratos, casos de uso, modelos e testes existentes das associações currículo-vaga, incluindo as integrações das issues #130, #131 e #132.

## Informações complementares

A issue #243 é a consulta, não a entrega HTTP. O usuário exige separar claramente a responsabilidade da #243 da da #244 e manter a análise restrita ao caso de uso e à camada de aplicação, sem introduzir contratos que não existem no projeto.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem | Nenhuma | Inicial | Nova análise focada na issue #243 | Inicial |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| code-alchemists-br/sistema-curriculo#243 | primary | prose | issue | GitHub issue | título, descrição e critério de aceite | external |
| prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md | primary | prose | decision-record | Markdown | decisões de criação, duplicidade e port de persistência | working-tree / v004 |
| src/backend/application/ports.py | primary | source-code | application-contract | Python | RepositorioCurriculo e RepositorioAssociacaoCurriculoVaga | working-tree |
| src/backend/application/associacao_curriculo_vaga.py | primary | source-code | use-case | Python | verificação de ownership e persistência | working-tree |
| src/backend/application/listagem_versoes_curriculo.py | primary | source-code | use-case | Python | padrão de listagem do estudante e ordenação determinística | working-tree |
| src/backend/domain/associacao_curriculo_vaga.py | primary | source-code | domain-model | Python | agregado e invariantes de associação | working-tree |
| src/backend/tests/test_application_associacao_curriculo_vaga.py | supporting | test | unit-test | Python | stubs para propriedade, duplicidade e persistência | working-tree |

### Limites da evidência dos artefatos

A evidência mostra a base estrutural que a #243 precisa reutilizar; não há no repositório um contrato compartilhado de paginação para query por associação ou um endpoint HTTP dedicado à issue #244. O que existe de fato é: modelo de domínio, port de persistência da associação, caso de uso de criação/alteração e padrão de listagem do estudante em Application.

## Problema enriquecido

### Resultado desejado

Modelar uma consulta de leitura paginada das associações de um estudante, mantendo a regra arquitetural da Clean Architecture, sem duplicar lógica de autorização no adapter e sem expandir o escopo para transporte HTTP.

### Atores e interesses

- Estudante autenticado: deseja consultar apenas suas próprias associações entre currículos e vagas.
- Application: centraliza autorização, consulta e ordenação determinística.
- Infraestrutura: resolve a consulta e a paginação em SQLAlchemy ou outra tecnologia, sem decidir o comportamento de negócio.
- Projeto: deseja manutenção mínima, baixo acoplamento e compatibilidade com a arquitetura existente.

### Evidências e fatos observados

1. O agregado de associação já existe em `src/backend/domain/associacao_curriculo_vaga.py` e usa esquema de identidade composta `curriculo_id + vaga_id`.
2. A regra de domínio já definiu que `candidatura` implica `interesse` e que a associação exige pelo menos uma classificação válida.
3. O port `RepositorioAssociacaoCurriculoVaga` já existe em `src/backend/application/ports.py` com operações de `existe_por_par`, `obter_para_atualizacao`, `atualizar_classificacoes` e `salvar`.
4. O caso de uso `CriarAssociacaoCurriculoVaga` já valida ownership ao consultar `RepositorioCurriculo.obter_por_id` e compara `curriculo.usuario_id` com `entrada.usuario_id`.
5. O padrão de listagem do estudante em `src/backend/application/listagem_versoes_curriculo.py` confirma que a Application deve filtrar pelo proprietário e ordenar de modo determinístico, sem confiar em entrada externa.
6. O projeto ainda não apresenta um contrato de paginação universal para consultas assíncronas de leitura; a composição de paginação é ausente na estrutura atual e deve ser mantenha mínima para esta issue.

### Hipóteses

- A consulta deve ser tratada como caso de uso da application, não como endpoint HTTP.
- A forma mínima e segura de garantir o isolamento do estudante é queryar o repositório por `usuario_id`, ou por um conjunto de currículos do dono, filtrado na própria consulta.
- A implementação pode ser pequena e verificável isoladamente sem definir um DTO ou retorno de API completo.

### Perguntas em aberto

- Qual é a convenção de paginação definitiva do projeto? Não há evidence suficiente para inventar um padrão global.
- Qual critério de ordenação deve prevalecer para associções? O projeto tem ordenação determinística para versões de currículo, mas não para associações.
- Qual é o tamanho padrão e o limite máximo da página? Essas decisões ainda não foram estabilizadas.

### Escopo

- Definir o contrato mínimo do caso de uso de consulta paginada de associações de um estudante.
- Reutilizar o modelo de domínio e o port já existentes.
- Garantir que o estudante só veja associações dos seus currículos.
- Manter interpretação em Application, sem alterar a camada HTTP da #244.

### Fora do escopo

- Implementar endpoint REST da #244.
- Definir resposta JSON final da API.
- Criar uma página global ou contrato de paginação compartilhado para todo o sistema.
- Redescrever a arquitetura do módulo de currículo-vaga.

### Critérios de sucesso

- A consulta usa a Application como ponto de autorização e de orquestração.
- O retorno contém somente associações pertencentes ao estudante autenticado.
- O método é verificável em testes unitários isolados.
- O comportamento não exige transportar dados de HTTP.

## Restrições aplicáveis

- Clean Architecture e DDD já estabelecidos em `src/backend/AGENTS.md`.
- Domain livre de infraestrutura e API.
- Application depende apenas de ports abstratos; não pode conhecer ORM.
- O caso de uso deve receber identidade do usuário e não confiar em identificadores arbitrários de currículo vindos da requisição.
- Não inventar regras de negócio além das já defendidas por #130/#131/#132.

## Classificação comentada

A issue #243 é principalmente uma decisão de design em engenharia, com foco em arquitetura e aplicação. O problema não é de produto nem de API; é de como o sistema consulta e protege o domínio de acesso do estudante, preservando as regras existentes e mantendo compatibilidade com a implementação já em desenvolvimento.

## Decisão de roteamento

- Local mais coerente: `prompts/backend`.
- Motivo: a questão é de aplicação/backend, com port, use-case e modelo de domínio, não de documentação, frontend ou endpoint HTTP.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | alta | somente associações do estudante autenticado | evita vazamento de dados e mantém o contrato de segurança do projeto |
| modifiability | alta | usar ports e caso de uso sem conhecer instância HTTP | preserva Clean Architecture e facilita testes |
| simplicity | alta | contrato mínimo e verificável isoladamente | reduz risco de escopo e evita inovação desnecessária |
| time-to-value | média | entregar consulta capaz de ser validada em poucos testes | atende critério de aceite e reduz PR | 
| reliability | média | ordenar e paginar de maneira determinística | evita reordenação instável e resultados inconsistentes |

## Alternativas consideradas

1. Alternativa A: adicionar a consulta diretamente no adaptador/endpoint, sem Application.
   - Viável parcialmente, mas quebra o padrão observado e não protege a regra no núcleo da aplicação.
2. Alternativa B: criar um caso de uso em Application sem port dedicado, usando `RepositorioAssociacaoCurriculoVaga` e `RepositorioCurriculo` existentes.
   - Viável e coerente com o projeto; é a menor mudança sem redesenho.
3. Alternativa C: definir um contrato completo de paginação e DTO de página compartilhado para todo sistema.
   - Inviável como implementação mínima desta issue, porque a evidência não sustenta tal padrão global.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| correctness | 5 | -2 | +2 | +1 | alta | uso já existente de ownership em `CriarAssociacaoCurriculoVaga` |
| modifiability | 4 | -1 | +2 | -1 | alta | ports e use-case já são o padrão do projeto |
| simplicity | 4 | -2 | +2 | -2 | alta | escala mínima de solução |
| reliability | 3 | -1 | +1 | +1 | média | ordenação determinística e controle por usuário |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado. A análise inicial da issue #243 não existe ainda.

### Decisão recomendada nesta versão

A implementação mínima recomendada para #243 é:

1. Criar um caso de uso em `src/backend/application` para listar as associações do estudante, seguindo o mesmo padrão de `ListarVersoesCurriculo`.
2. Receber `usuario_id` como entrada do caso de uso; não receber curriculo_id arbitrário vindo da camada externa.
3. Necessitar de um port de consulta em `RepositorioAssociacaoCurriculoVaga` para listar associações pelo proprietário, com paginação mínima (`offset`/`limit` ou equivalente simples) e ordenação determinística.
4. Reusar o contrato existente `RepositorioCurriculo.listar_por_usuario` para apoio de ownership se o adapter do repositório de associação não filtrar por proprietário diretamente.
5. Retornar uma tupla de `AssociacaoCurriculoVaga` em vez de definir um payload HTTP ou página global do sistema.
6. Manter a decisão de contrato detalhado de paginação para uma etapa posterior se a equipe quiser compartilhar a convenção em outras consultas.

### Impacto da revisão

A decisão recomendada preserva a arquitetura existente e evita inventar um endpoint, um DTO de API ou uma regra global de paginação que não está sustentada pelo código atual.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | maximized | consulta segura para apenas associações do estudante | `CriarAssociacaoCurriculoVaga` já valida ownership por `usuario_id` |
| modifiability | prioritized | port e use-case independentes de infraestrutura | `src/backend/application/ports.py` e `listagem_versoes_curriculo.py` seguem esse padrão |
| simplicity | prioritized | desenho mínimo, testável em poucos casos | a issue exige “verificável isoladamente” |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| reliability | ordenação determinística e paginação mínima | use-case controla a chamada do repositório e o retorno em uma tupla estável |
| time-to-value | implementação em poucos arquivos | a issue não exige endpoint nem API |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | vazamento de associações de outros usuários | alta | estudantes autenticados |
| modifiability | acoplamento a adaptadores e HTTP | alta | equipe de backend |
| simplicity | aumento de complexidade desnecessária | média | prazo e manutenção |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | poucas regras extras no Application | time-to-value | aceitável |
| modifiability | manter um port mínimo extra | velocidade de entrega inicial | aceitável |

## Riscos e efeitos de segunda ordem

- Se a #243 tentar definir resposta de API, ela se sobrepõe à #244 e cria acoplamento indevido.
- Se a paginação for especificada sem padrão do projeto, a solução poderá ficar incompatível com futuras consultas.
- Se o filtro de ownership for deixado apenas no adapter, a camada de Application perderá capacidade de validar segurança.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| A consulta deve ficar em Application | um caso de uso de leitura com `usuario_id` e port de repositório | testes unitários do caso de uso | qualquer acoplamento a HTTP ou ORM |
| O estudante só vê associações próprias | duas associações: uma do usuário e outra de outro usuário | teste de unitário em Application | resultado inclui associação alheia |
| A paginação mínima pode ser simples | `limit` e `offset` ou `pagina`/`tamanho` | teste de limites e slice | contrato com semântica ambígua ou dependente de API |
| A ordenação deve ser determinística | mesma entrada leva ao mesmo retorno | teste de ordenação | ordem muda entre execuções |

## Handoffs e atividades posteriores

- Definir o contrato final de paginação junto à #244, se a equipe decidir padronizar o comportamento em outras consultas.
- Registrar e validar eventual padrão de metadata da página em uma issue separada, evitando inventar esse contrato na #243.
- Implementar a camada de infraestrutura apenas após a assinatura mínima da Application e os testes unitários forem aprovados.

## Síntese

A issue #243 é válida e deve ser tratada como consulta de leitura em Application, com as regras já estabelecidas pelas issues #130, #131 e #132. O ponto central não é endpoint HTTP, e sim: garantir propriedade e paginação mínima sem inventar um padrão global que o projeto ainda não definiu. A melhor implementação é uma use-case de leitura com `usuario_id`, port de consulta no `RepositorioAssociacaoCurriculoVaga`, retorno em tupla ordenada e filtra por dono do currículo. O que continua indefinido e deve permanecer fora da issue é a convenção final de `offset`/`limit`, ordenação global, metadata de página e contrato de resposta de API; essas decisões devem ser deixadas para a #244 ou para uma análise de padronização posterior.
