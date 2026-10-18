---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v003"
status: pending
created_at: "2026-10-12T16:25:50-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261011-001011-associacao-curriculo-vaga-v001.md
  supersedes: prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md
  change_type: scope-change
  secondary_change_types: [enrichment, reassessment]
  decision_impact: reopened
subjects:
  kind: mixed
  files:
    - path: "code-alchemists-br/sistema-curriculo#130"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: whole-file
      locator: "título e corpo consultados via gh issue view em 2026-10-12"
      content_state: external
      revision: null
      availability: available
    - path: "Solicitação do usuário — análise exclusiva da #130 (2026-10-12)"
      relationship: primary
      representation: prose
      function: documentation
      format: mensagem de usuário
      analysis_scope: whole-file
      locator: "escopo, questões, evidências indicadas e resultado esperado; reproduzida abaixo"
      content_state: external
      revision: null
      availability: available
    - path: prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "frontmatter, solicitação original, responsabilidades #130/#131/#132, decisão e handoffs"
      content_state: working-tree
      revision: v002
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: selected-section
      locator: "fronteiras Clean Architecture/DDD, Code First, Nix, documentação e testes"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF12, RF15, RN01-RN04 e detalhamentos pendentes"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/matriz_testes.md
      relationship: primary
      representation: prose
      function: test
      format: Markdown
      analysis_scope: selected-section
      locator: "CT-RF12-01..09, CT-RF12-C01..C07, CT-RF15-02/03/04 e nota RNF04"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RNF04, RNF05, critérios de verificação e pendências de autorização"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/Arquitetura/ADR-001-arquitetura-do-sistema.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "seções 2.1-2.4 e 2.8-2.10"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: documentation
      format: Mermaid ER em Markdown
      analysis_scope: whole-file
      locator: "diagrama completo; não contém associação currículo-vaga"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/contrato-credenciais-sessao.md
      relationship: supporting
      representation: prose
      function: schema-contract
      format: Markdown
      analysis_scope: selected-section
      locator: "identidade confiável UsuarioAutenticado e autenticação/autorização de rotas protegidas"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/contratos_integracao_grupo2.md
      relationship: supporting
      representation: prose
      function: schema-contract
      format: Markdown
      analysis_scope: selected-section
      locator: "objetivo e responsabilidades: vagas externas são sugestões, não associações automáticas"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "agregado, construção não vazia, classificação e normalização candidatura => interesse"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "CurriculoId e VagaId"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioCurriculo e contratos de persistência; ausência de port de associação"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "CriarVersaoCurriculo, EditarVersaoCurriculo e erro de currículo ausente/alheio"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/acesso_estudante.py
      relationship: context
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "padrão de caso de uso e portas"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "DTOs, tradução de erros e identidade de usuário recebida na rota"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "injeção de executores e composição de routers"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "registro ORM e mapeamento externo ao domínio"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "adapter assíncrono; flush sem commit, transação sob composição externa"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/metadata.py
      relationship: supporting
      representation: source-code
      function: configuration
      format: Python
      analysis_scope: whole-file
      locator: "registro de modelos ORM na metadata consumida pelo Alembic"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261005_0002_criar_curriculos.py
      relationship: supporting
      representation: source-code
      function: build
      format: Python/Alembic
      analysis_scope: whole-file
      locator: "padrão de migration Code First"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_application_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "testes unitários do caso de uso, propriedade e ausência sem persistência"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_infrastructure_curriculo_mapping.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: "metadata e migration verificados em memória"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_infrastructure_repositorio_curriculo.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "contrato de adapter e ausência de commit próprio"
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "Continuidade da linhagem e propósito de implementação do backend; requisitos/revisao não são o objeto principal."
classification:
  sphere: engineering
  concerns: [domain, architecture, data]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: high
  reversibility: moderate
  risk: medium
---

# Análise de decisão — Criação manual de associação currículo-vaga (#130)

## Solicitação original

> Analise em conjunto as issues:
>
> #130 "Implementar criação de associação currículo-vaga"
> #131 "Implementar regra de candidatura implica interesse"
> #132 "Implementar atualização de classificações da associação"
>
> Objetivo principal desta análise:
>
> Definir o modelo mínimo e as regras necessárias para que essas três issues compartilhem uma implementação coerente, com foco em permitir que a primeira implementação seja a issue #131.
>
> Não implemente código nesta etapa.
>
> IMPORTANTE
>
> 1. Leia todos os AGENTS.md aplicáveis antes da análise.
> 2. Consulte o conteúdo atual das issues #130, #131 e #132 no GitHub, se possível usando `gh issue view`.
> 3. Leia somente os arquivos necessários.
> 4. Não faça revisão geral do repositório.
> 5. Não altere arquitetura existente.
> 6. Não implemente API, banco, migration ou adapter nesta etapa.
> 7. Não invente classificações, estados ou regras que não estejam sustentados pelos requisitos ou testes existentes.
> 8. Se alguma decisão realmente não puder ser tomada com a evidência disponível, registre-a como pendente.
>
> CONTEXTO
>
> As três issues tratam da mesma associação entre currículo e vaga:
>
> #130 cria a associação.
>
> #131 estabelece a regra "candidatura implica interesse".
>
> #132 atualiza as classificações da associação.
>
> A análise deve determinar como essas responsabilidades se relacionam e garantir que a #130 e a #132 reutilizem a mesma regra de domínio definida para a #131.
>
> Há indícios na documentação e na matriz de testes de que as classificações atualmente previstas são:
>
> interesse
> compatibilidade
> candidatura
>
> Não introduza classificações adicionais sem evidência.
>
> QUESTÕES QUE A ANÁLISE DEVE RESPONDER
>
> 1. Qual deve ser o modelo mínimo da associação currículo-vaga?
> 2. Quais dados ela precisa possuir para suportar #130, #131 e #132?
> 3. Como currículo e vaga devem ser identificados?
> 4. As classificações devem ser representadas como conjunto, enum, flags ou outra estrutura já compatível com os padrões do projeto?
> 5. Qual é exatamente a regra da #131?
> 6. Quando `candidatura` for adicionada, `interesse` deve ser adicionado automaticamente?
> 7. O que deve acontecer se alguém tentar remover `interesse` enquanto `candidatura` continua presente?
>
> Não invente a resposta. Determine-a a partir dos requisitos, matriz de testes e padrões existentes. Caso não haja evidência suficiente, registre a decisão como pendente.
>
> 8. Remover `candidatura` deve remover `interesse`?
>
> Verifique se existe evidência. Não infira automaticamente.
>
> 9. A regra "candidatura implica interesse" deve ficar no Domain?
> 10. A #131 pode ser implementada antes da persistência da #130?
> 11. Qual parte mínima do modelo precisa existir para implementar #131 isoladamente?
> 12. Quais responsabilidades pertencem à:
>
> Domain
> Application
> Infrastructure
> API
>
> 13. O que a #130 deve reutilizar da #131?
> 14. O que a #132 deve reutilizar da #130 e da #131?
> 15. Quais decisões precisam ser tomadas agora e quais podem esperar a implementação de persistência?
> 16. Quais testes unitários são pertinentes especificamente para #131?
> 17. Quais testes pertencem depois à #130 ou #132 e não devem entrar na implementação da #131?
>
> ARQUIVOS PRIORITÁRIOS
>
> Leia somente quando necessário:
>
> AGENTS.md
>
> src/backend/AGENTS.md
>
> docs/Arquitetura/ADR-001-arquitetura-do-sistema.md
>
> docs/requisitos_funcionais.md
>
> docs/matriz_testes.md
>
> docs/modelagem_der.md
>
> src/backend/domain/
>
> src/backend/domain/curriculo.py
>
> src/backend/domain/value_objects.py
>
> src/backend/application/ports.py
>
> exemplos existentes de entidades e invariantes de domínio
>
> qualquer análise em prompts/ diretamente relacionada a currículo-vaga ou às issues #130, #131 e #132
>
> Procure por `RegraDeDominioViolada` e por padrões existentes de validação de invariantes somente se forem relevantes.
>
> ESCOPO DA PRIMEIRA IMPLEMENTAÇÃO
>
> Embora a análise cubra #130, #131 e #132, a primeira implementação será somente a #131.
>
> Portanto, ao final, indique explicitamente:
>
> 1. quais arquivos a #131 provavelmente precisará criar ou alterar;
> 2. qual comportamento exato deve ser implementado;
> 3. quais testes unitários devem acompanhar a #131;
> 4. o que deve permanecer fora dessa implementação para #130 e #132.
>
> RESULTADO ESPERADO
>
> Quero uma decisão técnica pequena e implementável que permita executar #131 primeiro sem criar um modelo incompatível com #130 e #132.
>
> Não implemente código.
>
> Gere o artefato de análise no diretório apropriado de `prompts/`, seguindo as regras da skill e mantendo a rastreabilidade exigida pelo projeto.

A resposta posterior “Sim, revisar a análise primeiro” e o pedido de implementação exclusiva da #131 estão documentados na entrada complementar da [v002](./20261011-023511-associacao-curriculo-vaga-v002.md#informações-complementares), sem alterar retrospectivamente esse primeiro pedido.

## Informações complementares

### Entrada posterior — solicitação atual (literal)

> Analise exclusivamente a issue #130:
>
> "Implementar criação de associação currículo-vaga"
>
> Não implemente código nesta etapa.
>
> CONTEXTO
>
> A issue #131, "Implementar regra de candidatura implica interesse", já foi implementada e mergeada em `dev`.
>
> A implementação da #131 introduziu no Domain:
>
> - `AssociacaoCurriculoVaga`
> - `ClassificacaoAssociacao`
> - `VagaId`
>
> e definiu a regra:
>
> - `candidatura` implica `interesse`;
> - ao construir ou adicionar `candidatura`, `interesse` é incluído automaticamente;
> - classificações existentes são preservadas;
> - não há duplicação de classificações;
> - não existem operações de remoção ainda.
>
> Use como decisão anterior relevante:
>
> prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md
>
> A #130 deve REUTILIZAR esse domínio e não duplicar a regra da #131.
>
> OBJETIVO
>
> Definir exatamente o escopo necessário para implementar a criação manual de uma associação currículo-vaga, respeitando a arquitetura existente e preparando a implementação sem antecipar a #132.
>
> IMPORTANTE
>
> 1. Leia todos os `AGENTS.md` aplicáveis.
> 2. Consulte a issue #130 no GitHub com `gh issue view`, se possível.
> 3. Leia somente os arquivos necessários.
> 4. Não faça revisão geral do repositório.
> 5. Não redesenhe a arquitetura.
> 6. Não implemente código nesta etapa.
> 7. Não implemente funcionalidades da #132.
> 8. Não invente regras de negócio sem evidência nos requisitos, matriz de testes ou arquitetura existente.
> 9. Considere a implementação mergeada da #131 como estado atual do domínio.
> 10. Se alguma decisão não puder ser tomada com as evidências existentes, registre explicitamente como pendente.
>
> QUESTÕES QUE A ANÁLISE DEVE RESPONDER
>
> 1. Qual é exatamente a responsabilidade da #130?
>
> 2. A #130 deve ser implementada principalmente na camada Application?
>
> 3. Qual deve ser o caso de uso/comando responsável pela criação da associação?
>
> 4. Quais dados mínimos a entrada da criação precisa receber?
>
> Verifique especialmente:
>
> - `curriculo_id`
> - `vaga_id`
> - classificações iniciais
>
> Não acrescente campos sem evidência.
>
> 5. Como deve ser validado que existe pelo menos uma classificação inicial?
>
> Determine se essa validação já pertence ao Domain existente ou se precisa existir também na fronteira da Application/API.
>
> 6. Como a #130 deve reutilizar `AssociacaoCurriculoVaga` e a regra da #131?
>
> 7. A Application deve criar diretamente o agregado ou utilizar alguma fábrica/padrão já existente no projeto?
>
> 8. Como deve ser verificado que o currículo pertence ao estudante autenticado?
>
> Procure contratos, ports e casos de uso existentes que demonstrem o padrão do projeto.
>
> 9. É necessário validar a existência da vaga antes de criar a associação?
>
> Se sim:
>
> - qual fonte deve ser consultada;
> - se a validação depende do Grupo 2;
> - se isso bloquearia a #130.
>
> Não invente dependência externa se os requisitos não exigirem.
>
> 10. Como a associação deve ser persistida?
>
> Determine qual porta mínima de repositório é necessária na Application.
>
> 11. Existe algum repositório/port atual que possa ser reutilizado?
>
> Não crie abstração nova sem verificar primeiro.
>
> 12. Como tratar tentativa de criar novamente uma associação para o mesmo par currículo-vaga?
>
> Verifique se requisitos ou matriz de testes definem:
>
> - rejeição;
> - idempotência;
> - atualização da associação existente;
> - múltiplas associações permitidas.
>
> Se não houver evidência suficiente, registre como pendente.
>
> 13. A associação precisa de ID próprio nesta issue?
>
> Ou `curriculo_id + vaga_id` é suficiente como identidade lógica?
>
> Não escolha arbitrariamente. Verifique requisitos, padrões de persistência e testes.
>
> 14. A #130 exige migration/ORM agora ou existe separação entre caso de uso e persistência concreta em outra issue?
>
> Determine o mínimo necessário para considerar a #130 concluída.
>
> 15. Qual atomicidade é necessária?
>
> Especialmente diante da regra:
>
> `candidatura => interesse`
>
> A criação não pode persistir estado parcial.
>
> 16. Quais erros de Application fazem sentido nesta criação?
>
> Use padrões existentes do projeto e não invente uma taxonomia nova sem necessidade.
>
> 17. Quais responsabilidades pertencem a:
>
> - Domain
> - Application
> - Infrastructure
> - API
>
> para a #130?
>
> 18. O que deve permanecer explicitamente fora da #130 para a #132?
>
> Especialmente:
>
> - adicionar classificação depois da criação;
> - remover classificação;
> - remover `candidatura`;
> - remover `interesse`;
> - tentativa de remover a última classificação.
>
> 19. Quais testes unitários pertencem especificamente à #130?
>
> 20. Quais testes de integração/persistência seriam necessários, se houver, e em qual camada?
>
> ARQUIVOS PRIORITÁRIOS
>
> Leia somente se forem necessários:
>
> - `AGENTS.md`
> - `src/backend/AGENTS.md`
> - `docs/requisitos_funcionais.md`
> - `docs/matriz_testes.md`
> - `docs/Arquitetura/ADR-001-arquitetura-do-sistema.md`
> - `docs/modelagem_der.md`
> - `prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md`
> - `src/backend/domain/associacao_curriculo_vaga.py`
> - `src/backend/domain/value_objects.py`
> - `src/backend/application/ports.py`
> - casos de uso existentes na Application
> - ports/repositories existentes
> - testes existentes que mostrem o padrão de criação e persistência
>
> ESCOPO ESPERADO
>
> A análise deve tentar produzir uma decisão implementável para #130 sem resolver antecipadamente #132.
>
> A criação deve reutilizar o agregado existente da #131 e não reimplementar:
>
> `candidatura implica interesse`
>
> Não implemente operação de remoção de classificação.
>
> Não implemente atualização de classificações.
>
> Não implemente integração com Grupo 2, salvo se houver evidência explícita de que a criação da associação exige essa comunicação.
>
> RESULTADO ESPERADO
>
> Ao final, informe claramente:
>
> 1. quais arquivos provavelmente serão criados ou alterados na #130;
>
> 2. qual será o fluxo exato da criação;
>
> 3. quais ports/repositories serão necessários;
>
> 4. quais regras já estão resolvidas pela #131;
>
> 5. quais decisões permanecem pendentes;
>
> 6. quais testes pertencem à #130;
>
> 7. o que fica explicitamente para #132.
>
> Gere o artefato de análise no diretório apropriado de `prompts/`, preservando a rastreabilidade exigida pela skill.

### Fatos complementares constatados

- `gh issue view 130 --repo code-alchemists-br/sistema-curriculo` retornou a issue aberta com o título indicado e corpo genérico: “Tarefa da fatia vertical atribuída a @Andre-LSL. Inclua os testes unitários pertinentes.” A issue não define mais regras.
- O usuário informa que #131 foi mergeada em `dev`; o arquivo de domínio atual foi lido e contém os conceitos e o comportamento declarados. O estado do branch/commit não foi verificado por Git nesta análise.
- A implementação atual do domínio exige classificação não vazia e normaliza candidatura acrescentando interesse; a coleção é set, classificações anteriores permanecem e não há operação de remoção.
- Há contrato de sessão que determina identidade confiável `UsuarioAutenticado(usuario_id)` e exige que rotas protegidas usem a identidade contextual, nunca identidade declarada pelo cliente. Os arquivos de backend examinados não contêm os símbolos `UsuarioAutenticado` ou `usuario_autenticado`; a rota atual de currículo recebe `usuario_id` pelo caminho. A disponibilidade concreta da dependência de sessão para a nova rota precisa ser confirmada/integrada.
- RF12 exige criação manual e persistência em banco; CT-RF12-05 e CT-RF12-09 exigem round-trip e ausência de estado parcial em falha. Não foi encontrada decisão ou teste para repetição do mesmo par currículo-vaga, nem modelo da associação no DER.

## Mudanças desde a versão anterior

| Elemento | v002 | v003 | Motivo | Impacto |
|---|---|---|---|---|
| Foco da análise | Decisão exclusiva da regra de domínio da #131; #130 era handoff | Decisão exclusiva da criação manual #130 | Solicitação atual muda o foco, sem alterar a linhagem | Reabre as decisões necessárias à #130; não modifica a decisão do domínio |
| Estado da #131 | A v002 registrava a #131 aberta e propunha sua implementação | Usuário informa que #131 foi mergeada; domínio atual confirma o modelo/regras | Contexto posterior e inspeção do código atual | A criação passa a reutilizar implementação existente |
| Artefatos de entrada | Requisitos, matriz, DER, ADR, domínio anterior a #131 e ports | Inclusão do domínio atual, use case, API/factory, ORM/repository/migration, contrato de sessão, RNF e contrato do Grupo 2 | Necessidade de decidir fluxo completo e fronteiras | Evidência mais concreta para Application/API/persistência |
| Persistência | Migration/atomicidade entregues como handoff para #130/#132, sem decisão da #130 | RF12 e CT-RF12-05/09 demandam persistência e integridade na fatia de criação; padrão do backend exige Code First | Delimitar o mínimo de conclusão da #130 | Recomenda incluir adapter e migration, sob a chave ainda pendente |
| Identidade e duplicidade | Pendentes para criação futura | Continuam sem evidência; nenhuma regra apareceu na matriz ou nos ports | Consultas atuais não acrescentam política de domínio | Mantém `status: pending`; bloqueia a escolha final de PK/constraint e resposta de repetição |
| Autenticação | Handoff geral de API | Contrato de sessão agora especifica identidade contextual; backend consultado não tem os símbolos da dependência | Pergunta explícita sobre estudante autenticado | Define a fonte correta da identidade; integração concreta da dependência precisa ser confirmada |
| Grupo 2 | Integração reservada para outro fluxo | Contrato consultado confirma que vagas são sugestões e associação continua manual | Pergunta explícita sobre validar vaga | Não há base para consultar Grupo 2 na criação |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `code-alchemists-br/sistema-curriculo#130` | Primário | Prose | Documentation | GitHub issue | Título e corpo | Externo; consulta atual via `gh`; corpo genérico |
| Solicitação atual do usuário | Primário | Prose | Documentation | Mensagem | Escopo, contexto, vinte questões e resultado; literal acima | Externo; 2026-10-12 |
| `prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md` | Apoio | Prose | Documentation | Markdown | Metadados, solicitação original, decisão, pendências e handoffs | Working tree; versão v002 |
| `AGENTS.md` | Contexto | Prose | Prompt-instruction | Markdown | Regras de arquitetura, Nix, testes e documentação | Working tree |
| `src/backend/AGENTS.md` | Contexto | Prose | Prompt-instruction | Markdown | Arquitetura, DDD, fronteiras, persistência e testes | Working tree |
| `docs/requisitos_funcionais.md` | Primário | Prose | Documentation | Markdown | RF12/RF15, RN01-RN04 e pendências | Working tree |
| `docs/matriz_testes.md` | Primário | Prose | Test | Markdown | CT-RF12-01..09/C01..C07 e CT-RF15/nota RNF04 | Working tree |
| `docs/requisitos_nao_funcionais.md` | Apoio | Prose | Documentation | Markdown | RNF04/RNF05, verificação e pendências | Working tree |
| `docs/Arquitetura/ADR-001-arquitetura-do-sistema.md` | Apoio | Prose | Documentation | Markdown | Arquitetura, aplicação, persistência, Grupo 2 e acesso | Working tree |
| `docs/modelagem_der.md` | Apoio | Diagram-model | Documentation | Mermaid/Markdown | Diagrama completo; associação ausente | Working tree |
| `docs/contrato-credenciais-sessao.md` | Apoio | Prose | Schema-contract | Markdown | `UsuarioAutenticado` e regras de rota protegida | Working tree |
| `docs/contratos_integracao_grupo2.md` | Apoio | Prose | Schema-contract | Markdown | Propósito e semântica de sugestões externas | Working tree |
| `src/backend/domain/associacao_curriculo_vaga.py` | Apoio | Source-code | Production | Python | Arquivo completo | Working tree; commit não verificado |
| `src/backend/domain/value_objects.py` | Apoio | Source-code | Production | Python | `CurriculoId` e `VagaId` | Working tree; commit não verificado |
| `src/backend/application/ports.py` | Apoio | Source-code | Production | Python | `RepositorioCurriculo` e portas próximas; sem port de associação | Working tree; commit não verificado |
| `src/backend/application/versao_curriculo.py` | Apoio | Source-code | Production | Python | Criação/edição, ownership check e erro de ausência/alheio | Working tree; commit não verificado |
| `src/backend/application/acesso_estudante.py` | Contexto | Source-code | Production | Python | Padrão de orquestração injetada | Working tree; commit não verificado |
| `src/backend/api/versao_curriculo.py` | Apoio | Source-code | Production | Python | DTOs, rota, identidade recebida e tradução de erros | Working tree; commit não verificado |
| `src/backend/api/factory.py` | Apoio | Source-code | Production | Python | Injeção de executores e registro de routers | Working tree; commit não verificado |
| `src/backend/infrastructure/persistence/sqlalchemy/curriculo.py` | Apoio | Source-code | Production | Python | Modelo e conversões ORM/domínio | Working tree; commit não verificado |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py` | Apoio | Source-code | Production | Python | Consulta/salvamento e fronteira de transação | Working tree; commit não verificado |
| `src/backend/infrastructure/persistence/sqlalchemy/metadata.py` | Apoio | Source-code | Configuration | Python | Registro explícito de modelos para Alembic | Working tree; commit não verificado |
| `src/backend/infrastructure/persistence/alembic/versions/20261005_0002_criar_curriculos.py` | Apoio | Source-code | Build | Python/Alembic | Padrão de migration | Working tree; commit não verificado |
| `src/backend/tests/test_application_versao_curriculo.py` | Apoio | Source-code | Test | Python | Teste unitário de propriedade e criação/edição | Working tree; commit não verificado |
| `src/backend/tests/test_infrastructure_curriculo_mapping.py` | Apoio | Source-code | Test | Python | Metadata e migration em memória | Working tree; commit não verificado |
| `src/backend/tests/test_infrastructure_repositorio_curriculo.py` | Apoio | Source-code | Test | Python | Flush, propagação de falha e sem commit no adapter | Working tree; commit não verificado |

### Limites da evidência dos artefatos

- A issue #130 não contém critérios específicos além de “fatia vertical” e testes unitários.
- O DER completo não representa a associação.
- O contrato de sessão é evidência normativa para a identidade confiável; não foi localizado o símbolo/adapter de dependência no backend inspecionado. A existência de outro ponto de composição de autenticação não foi afirmada.
- O padrão do repositório SQLAlchemy define flush sem commit e transação externa, mas a composição concreta de sessão/commit/rollback da nova rota não foi examinada nem presumida.
- Não foi consultado o histórico Git nem verificado o merge da #131; sua situação mergeada é informação complementar do usuário. O domínio presente na árvore foi lido diretamente.
- A consulta à issue não informa uma regra de idempotência, unicidade, atualização em repetição ou identidade técnica da associação.
- A análise não executou build ou testes; não houve alteração de código.

## Problema enriquecido

### Resultado desejado

Entregar a fatia vertical de criação iniciada explicitamente pelo estudante: converter a intenção em um agregado válido, garantir que o currículo pertence à identidade autenticada, persistir uma associação e suas classificações com integridade, sem reimplementar a regra de #131.

### Atores e interesses

- Estudante autenticado: escolhe currículo, vaga e uma ou mais classificações, e espera que a criação seja persistida.
- Application: orquestra ownership, construção do agregado e solicitação de salvamento.
- Domain: protege as invariantes internas, inclusive estado não vazio e `candidatura => interesse`.
- API: recebe intenção autenticada, valida transporte e converte erros/saída sem expor o agregado diretamente.
- Infrastructure: mapeia e grava a associação e suas classificações sob a transação da operação.

### Evidências e fatos observados

1. RF12 exige associação manual entre currículo e vaga, uma ou mais classificações de interesse, compatibilidade e/ou candidatura, com persistência em banco.
2. RN01 proíbe criação automática; a seleção de uma vaga pode iniciar um fluxo manual, mas não conclui a associação por si só.
3. RN02 admite múltiplas classificações simultâneas; RN03 exige interesse sempre que há candidatura; RN04 não exige cálculo automático de compatibilidade.
4. CT-RF12-06 requer negar criação sem classificação; CT-RF12-05 exige sobrevivência a sessão/reautenticação; CT-RF12-09 exige ausência de associação parcial em falha de gravação.
5. O agregado da #131 já valida classificação inicial não vazia e normaliza candidatura para acrescentar interesse usando o mesmo conjunto fechado e sem duplicatas.
6. `RepositorioCurriculo` já permite obter um currículo pelo identificador tipado, e `EditarVersaoCurriculo` confere `curriculo.usuario_id == entrada.usuario_id`, tratando ausência e propriedade alheia igualmente.
7. `RepositorioCurriculo` não persiste o agregado `AssociacaoCurriculoVaga`; não existe port de repositório de associação nos contratos lidos.
8. `VagaId` é textual e opaco; o domínio não modela detalhes ou cliente externo de vaga.
9. O contrato de sessão define a identidade confiável como `UsuarioAutenticado(usuario_id)`; identidade declarada no caminho/corpo não é fonte confiável.
10. A integração Grupo 2 apresenta vagas como sugestões; RF12/RN01 exigem ação manual para associá-las.
11. O backend exige ORM Code First e migrations versionadas, mantém mapeamentos na Infrastructure, e os adapters conhecidos não fazem commit da sessão.
12. Nenhum requisito, cenário de teste, ERD ou port consultado define duplicidade, política de repetição ou chave persistida da associação.

### Hipóteses

- A API de criação pode receber o identificador opaco de uma vaga exibida em resultado de busca; não há requisito para revalidá-lo consultando Grupo 2.
- A operação unitária de persistência pode receber o agregado completo e gravar sua representação sob uma única transação, seguindo o adapter de currículo.
- A nova rota poderá usar a dependência de identidade descrita no contrato de sessão. A disponibilidade concreta dessa dependência deve ser confirmada antes de implementar a fronteira.

### Perguntas em aberto

1. Repetir criação para o mesmo par deve ser rejeitado, idempotente, atualizar o registro, ou permitir múltiplas associações? A evidência atual não escolhe.
2. A persistência usará chave composta `(curriculo_id, vaga_id)` ou ID técnico próprio? A política de repetição e a identidade persistida precisam ser decididas em conjunto.
3. A dependência comum de autenticação/sessão já está implementada e pode ser injetada na nova rota? Os arquivos de backend pesquisados não mostram seu símbolo.
4. Qual a resposta pública quando o par já existe? Não definir antes da política de repetição.

### Escopo

- Comando/caso de uso de criação manual, primariamente na Application.
- Entrada mínima: identidade do estudante autenticado, `CurriculoId`, `VagaId` e classificações iniciais.
- Conferência do proprietário do currículo pela Application.
- Construção direta do agregado existente da #131 e persistência por port próprio de associação.
- API protegida e integração com a composição da aplicação, validando transporte e traduzindo resultados.
- Mapping Code First e migration necessários para cumprir RF12; adapter que persiste uma criação completa atomicamente.
- Testes unitários das decisões Application/API/adapter e testes de persistência que demonstrem round-trip e rollback.
- Resolver duplicidade/chave antes de fechar schema, constraint e comportamento HTTP quando já há associação.

### Fora do escopo

- Integração com Grupo 2 ou consulta de vaga para validar existência.
- Criação automática de associação a partir de busca, recomendação, visualização ou seleção de currículo sem comando explícito.
- Reimplementar `candidatura => interesse` em Application, API, ORM ou migration; a fonte é o Domain da #131.
- Cálculo de compatibilidade ou candidatura a um serviço externo.
- Alteração das classificações depois da criação ou operações de remoção reservadas à #132.
- Escolher silenciosamente política de repetição ou ID de persistência.

### Critérios de sucesso

1. Uma solicitação manual com identidade autenticada, currículo próprio, `VagaId` e classificação inicial válida cria e persiste uma única associação no fluxo autorizado.
2. Entrada `candidatura` é normalizada pelo agregado da #131; interesse e outras classificações informadas chegam ao armazenamento sem perda ou duplicação.
3. Entrada vazia não persiste; o agregado continua a ser a proteção de domínio mesmo que API também restrinja o tamanho da coleção.
4. Currículo inexistente ou pertencente a outra identidade não produz associação nem revela sua existência indevidamente.
5. Falha em qualquer etapa da gravação deixa a transação sem associação/classificação parcial.
6. A decisão sobre chamadas repetidas e chave técnica fica aprovada e testada antes de concluir migration/constraint.
7. Nenhuma chamada a Grupo 2 ocorre para criar a associação.

## Restrições aplicáveis

- Clean Architecture/DDD: API valida formato/autenticação; Application orquestra; Domain protege invariantes; Infrastructure implementa portas e ORM.
- Entradas externas são convertidas em comando/DTO; entidades de domínio não são expostas diretamente pela API.
- Mapeamento relacional Code First e migrations Alembic versionadas; ORM permanece em Infrastructure.
- Identidade autenticada é proveniente do contexto de sessão, nunca de um ID arbitrário enviado pelo cliente.
- A operação de criação deve proteger a consistência da agregação e da regra candidatura/interesse numa transação.
- Não incluir operação, regras ou testes da #132.
- Não inventar regra para vaga inexistente, repetição ou ID persistido.
- Nenhum código foi implementado nesta análise.

## Classificação comentada

- `sphere: engineering`: a decisão principal define uma fatia técnica de backend.
- `concerns: [domain, architecture, data]`: reutilização de agregado, fronteiras de casos de uso e gravação relacional são as questões que alteram a solução.
- `decision_kind: design`: delimita responsabilidades e contratos para implementar criação.
- `scope: component`: afeta a fatia de associação no backend, incluindo suas interfaces externas.
- `lifecycle: delivery`: prepara a entrega funcional da issue.
- `urgency: normal`: não há prazo informado.
- `uncertainty: high`: repetição/chave persistida não têm evidência e a dependência de autenticação não foi localizada no código inspecionado.
- `reversibility: moderate`: API e caso de uso são reversíveis; chave primária e unicidade persistidas podem ser caras de migrar depois de haver dados.
- `risk: medium`: erro de autorização ou persistência afeta dados do estudante; as incertezas de integridade elevam risco da decisão de schema.

## Decisão de roteamento

Destino escolhido: `prompts/backend`.

Subpastas imediatas inventariadas: `prompts/ambientes`, `prompts/backend`, `prompts/frontend`, `prompts/requisitos`, `prompts/revisao` e `prompts/templates`. Candidatas semânticas consideradas: `backend`, `requisitos` e `revisao`. A continuidade v002→v003 e o objeto principal — implementação de uma fatia de backend — favorecem `backend`; `requisitos` faria sentido para redefinir RF12, o que não é o objetivo, e `revisao` não é preferida apenas por ser uma revisão de análise.

Confiança: alta. Não foi encontrado `AGENTS.md` adicional em `prompts/` ou `prompts/backend/`; aplica-se o `AGENTS.md` da raiz.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | Alta | Toda associação criada já respeita as invariantes | A entrada pode incluir candidatura e classes variáveis |
| security | Alta | O ator vem da sessão e só pode associar currículo próprio | O recurso contém dados privados e RNF04 se aplica |
| reliability | Alta | Gravação integral ou nenhuma gravação | CT-RF12-09 explicitamente exige ausência de parcialidade |
| simplicity | Alta | Reusar agregado, porta de currículo e padrões existentes | Evita duplicar #131 e criar abstração especulativa |
| modifiability | Média | Chave e política de repetição devem ser explicitadas antes de fixar schema | Mudança posterior pode requerer migração com dados |
| delivery-speed | Média | Não introduzir dependência externa sem requisito | Criação manual não deve depender de Grupo 2 |

## Alternativas consideradas

### Alternativa A — Application e port sem persistência concreta nesta issue

Criar o caso de uso com o agregado existente e um novo port, adiando ORM/migration para uma futura issue. É simples e testável em unitário, mas não satisfaz RF12 nem CT-RF12-05/09 e não completa a fatia vertical. Só seria aceitável se houvesse issue/decisão que separasse formalmente persistência; não foi encontrada evidência dessa separação.

### Alternativa B — Fatia vertical completa, com as decisões de identidade/repetição em aberto

Application valida propriedade, cria o agregado existente e solicita salvamento pelo novo port; API protegida entrega a identidade autenticada; Infrastructure implementa mapping, repositório e migration Code First; transaction boundary envolve toda a inserção. Esta é a única alternativa que atende os requisitos completos sem deslocar regras de negócio às bordas. O schema final e a semântica de repetição não podem ser congelados até resolver as perguntas pendentes.

### Alternativa C — API/controlador persistindo diretamente ou replicando normalização

Inviável: viola as fronteiras atuais da Clean Architecture, duplica a regra já protegida no Domain e facilita gravar estado divergente. Não é alternativa elegível.

### Decisão técnica atual

Adotar a Alternativa B como escopo de conclusão da #130, mas manter a decisão de negócio e persistência `pending` enquanto repetição/identidade técnica não forem decididas. A implementação do caminho feliz e os contratos não devem transformar um conflito não especificado em comportamento público acidental.

## Perfil de pagamento comparativo

Escala ordinal: `+2` melhora fortemente; `+1` melhora moderadamente; `0` neutro/desconhecido; `-1` piora moderadamente; `-2` piora fortemente. Alternativas A e C não completam a demanda ou violam restrições, logo não são opções de entrega equivalentes.

| Dimensão | Prioridade | A: adiar persistência | B: fatia vertical | C: API direta/duplicação | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| correctness | Alta | -1 | +2 | -2 | Alta | RN03 é do agregado; RF12 exige armazenamento |
| security | Alta | 0 | +1 | -2 | Alta | B aplica contexto confiável e checagem do dono; C não respeita a fronteira |
| reliability | Alta | -2 | +2 | -2 | Alta | CT-RF12-09 e transação necessária |
| simplicity | Alta | +2 | +1 | -1 | Média | A entrega menos código porém incompleta; B segue padrão existente; C acopla camadas |
| modifiability | Média | 0 | +1 | -2 | Média | B separa port/adapter e mapeamento; C mistura políticas e persistência |
| delivery-speed | Média | +1 | 0 | +1 | Média | A e C podem aparentar menor esforço, mas não atendem conclusão segura |

## Histórico e decisão atual

### Decisão da versão anterior

A v002 delimitou a #131 ao agregado de domínio e seus testes. Indicou a #130 como responsável por criação manual, propriedade do currículo, consulta de vaga, política de duplicidade, port, endpoint e persistência/migration, sem decidir estes detalhes. O agregado recomendado foi então implementado conforme informa o usuário e conforme observado na árvore atual.

### Decisão recomendada nesta versão

1. Implementar na Application um caso de uso de intenção única, por exemplo `CriarAssociacaoCurriculoVaga`, com entrada contendo apenas:
   - `usuario_id: UsuarioId`, obtido do principal autenticado;
   - `curriculo_id: CurriculoId`;
   - `vaga_id: VagaId`;
   - classificações iniciais (`ClassificacaoAssociacao`).
2. A API converte os IDs de transporte em value objects e obtém `usuario_id` do contexto de sessão, jamais de um campo de corpo/caminho controlado pelo cliente.
3. O caso de uso consulta `RepositorioCurriculo.obter_por_id(curriculo_id)`. Ausência ou `curriculo.usuario_id != usuario_id` encerra sem persistir; seguir o comportamento já existente que trata ambos como currículo não encontrado.
4. Construir diretamente `AssociacaoCurriculoVaga(curriculo_id, vaga_id, classificacoes)`. O construtor Domain rejeita coleção vazia, valida o vocabulário e acrescenta interesse automaticamente quando há candidatura.
5. Solicitar uma única operação de salvamento no port novo `RepositorioAssociacaoCurriculoVaga.salvar(associacao)`. Não usar `RepositorioCurriculo.salvar`, pois seu contrato aceita o agregado `Curriculo`, não uma associação.
6. Retornar um resultado/DTO de criação sem serializar o agregado diretamente. Erros de domínio seguem o padrão de tradução existente; erros de I/O permanecem explícitos e não são convertidos em sucesso.
7. O adapter persiste a associação e todas as classificações na mesma transação. O adapter faz flush, não commit, conforme padrão atual; a composição externa deve commit/rollback a operação inteira.
8. Não chamar Grupo 2. O identificador de vaga é referência opaca recebida do resultado apresentado; não há evidência de fonte local ou contrato exigindo reconsulta para validar existência.
9. Não congelar a chave/constraint nem o comportamento da repetição até decisão sobre unicidade e identidade técnica.

### Respostas diretas às questões da análise

| Questão | Decisão |
|---|---|
| Responsabilidade exata da #130 | Criar manualmente e persistir uma associação válida, vinculada a currículo próprio do estudante autenticado, sem efeitos externos |
| Camada principal | Application para o caso de uso/orquestração; é uma fatia vertical, não apenas Application |
| Caso de uso/comando | `CriarAssociacaoCurriculoVaga` e entrada dedicada; nome proposto, alinhado à linguagem existente |
| Entrada mínima | Usuário autenticado, `curriculo_id`, `vaga_id`, classificações iniciais; sem ID de associação, timestamp, descrição de vaga ou outro campo sem evidência |
| Não vazia | Domain já protege a invariante; continua autoritativo. API pode rejeitar coleção vazia na validação do DTO para resposta imediata, mas não substitui Domain; o caso de uso não precisa duplicar a regra |
| Reuso da #131 | Instanciar o mesmo `AssociacaoCurriculoVaga`; não criar normalizador/validador paralelo |
| Fábrica | Não há fábrica Domain existente para esse agregado; construção direta no caso de uso segue `CriarVersaoCurriculo` e aciona a validação do construtor |
| Propriedade do currículo | Obter currículo pela porta existente e comparar `usuario_id`; identidade do ator vem da sessão/`UsuarioAutenticado`; ausência e propriedade alheia recebem tratamento indistinguível conforme o padrão de edição |
| Existência da vaga | Não reconsultar nesta issue: RF10 e contrato Grupo 2 tratam busca/sugestões; RF12 é ação manual, e o contrato proíbe tratar sugestão como associação automática |
| Port de persistência | Port próprio mínimo de associação com `salvar(AssociacaoCurriculoVaga)`; reutilizar `RepositorioCurriculo` somente para leitura/ownership |
| Repositório atual reutilizável | Não para salvar associação; `RepositorioCurriculo` tem contrato e tipo de agregado diferentes |
| Repetir o mesmo par | Pendente: não há critério de rejeição, idempotência, atualização ou multiplicidade |
| ID próprio | O agregado atual já é referenciado pelos IDs de currículo e vaga; nenhum ID técnico é exigido para o fluxo de domínio. Chave primária persistida composta versus surrogate permanece pendente, acoplada à regra de duplicidade |
| ORM/migration | Sim para a #130 concluída: RF12 exige banco e o backend exige Code First/migrations. Não há evidência de issue separando a persistência; issue #130 é descrita como fatia vertical |
| Atomicidade | Inserir cabeçalho e classificações numa única transação; rollback total em erro, sem commit no adapter. A classificação persistida é a saída normalizada do agregado |
| Erros Application | Reusar o padrão de currículo não encontrado para inexistente/alheio e `RegraDeDominioViolada` do agregado para entrada de domínio inválida. Não criar taxonomia nova para I/O; propagar falha de repositório. Erro de associação duplicada aguarda política |
| Pendência adicional | Confirmar/integrar a dependência concreta de autenticação da API; contrato define o principal, mas o símbolo não foi encontrado no backend inspecionado |

### Responsabilidades por camada

| Camada | Responsabilidades da #130 | Não deve fazer |
|---|---|---|
| Domain | Preservar o agregado e invariantes já entregues na #131 | Consultar proprietário, vaga, API ou persistência; adicionar remoção/atualização |
| Application | Caso de uso; obter currículo; comparar proprietário com identidade confiável; construir agregado; chamar port de salvar uma vez | Acessar ORM/HTTP; repetir regra candidatura/interesse; inventar política de duplicidade |
| Infrastructure | Port de associação, mapping ORM, metadata, migration Code First; persistir as classes junto ao agregado dentro da transação | Regras de classificação, autenticação, política não aprovada ou commit escondido no adapter |
| API | Exigir contexto de sessão, validar campos/formato e lista não vazia, converter IDs/classificações, invocar caso de uso e traduzir erros/DTO | Aceitar usuário arbitrário do cliente, expor entidade Domain ou normalizar candidatura por conta própria |

### Arquivos prováveis para a #130

**Criar:**

- `src/backend/application/associacao_curriculo_vaga.py` — entrada e caso de uso, seguindo o padrão de casos existentes.
- `src/backend/api/associacao_curriculo_vaga.py` — DTO, rota autenticada, execução do caso de uso e resposta.
- `src/backend/infrastructure/persistence/sqlalchemy/associacao_curriculo_vaga.py` — registros ORM e conversões para o agregado, uma vez decidida a chave.
- `src/backend/infrastructure/persistence/sqlalchemy/repositorio_associacao_curriculo_vaga.py` — implementação do novo port.
- Nova migration Alembic Code First após decisão da chave/duplicidade.
- Testes unitários de Application/API, mapping e repositório, mais teste de persistência/integridade.

**Alterar provavelmente:**

- `src/backend/application/ports.py` — declarar port mínimo de salvamento.
- `src/backend/application/__init__.py` — exportar caso/entrada, se mantido o padrão público atual.
- `src/backend/infrastructure/persistence/sqlalchemy/metadata.py` — registrar o mapping para descoberta Alembic.
- `src/backend/api/factory.py` — injetar executor e registrar router.
- `docs/modelagem_der.md` — representar associação/classificações após a identidade/key escolhida.

**Não alterar para duplicar #131:** `src/backend/domain/associacao_curriculo_vaga.py` e `src/backend/domain/value_objects.py`, salvo ajuste estritamente necessário detectado por incompatibilidade real; a análise atual não identifica necessidade.

Localização exata da rota, forma final do DTO de resposta, estratégia ORM detalhada e nomes finais de tabelas dependem das convenções de composição descobertas durante implementação e da decisão de chave. Não adicionar campo público sem requisito.

### Decisões necessárias antes de fechar implementação persistida

1. Escolher semântica de repetição: rejeitar, idempotência, atualizar estado, ou permitir múltiplas associações. A escolha deve considerar se a chamada cria outra instância ou recupera/atualiza uma existente; não inferir “create” como regra de domínio de unicidade.
2. Escolher identidade de persistência compatível com a semântica: par composto se o par for único; ID técnico próprio se houver múltiplas instâncias ou se padrão persistente exigir. Não há evidência para escolher hoje.
3. Confirmar se a dependência comum de sessão prevista no contrato já está disponível no composition root. Se não estiver, bloquear rota pública sem autenticação ou integrar a dependência aprovada; não aceitar `usuario_id` cliente como substituto.
4. Identificar o boundary externo que controla commit/rollback da nova request. O adapter existente explicitamente não realiza transação.

### Decisões já resolvidas pela #131

- Vocabulário fechado: interesse, compatibilidade e candidatura.
- Estado interno como conjunto, sem duplicatas.
- A construção com candidatura acrescenta interesse.
- Inclusão de candidatura acrescenta interesse, sem descartar classificações existentes.
- Domain impede uma construção vazia.
- Nenhum método de remoção está presente.
- A #130 chama o agregado existente; não reimplementa a normalização.

### Impacto da revisão

A v002 deixou a #130 para trabalho futuro porque sua análise focal era a #131. Esta revisão reabre deliberadamente a criação à luz da #131 mergeada e dos requisitos de persistência. A responsabilidade central e a composição por camadas ficam especificadas, mas a recomendação de schema permanece bloqueada pela ausência de regra de repetição/identidade e a viabilidade da rota requer confirmar o contexto de sessão implementado. Portanto, `status: pending` não significa falta de evidência para o caminho feliz; significa que as decisões pendentes impedem uma especificação segura da persistência e do contrato de repetição.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | Nenhuma classificação persiste sem normalização do agregado | Código atual da #131, RN03 e tabela CT-RF12 |
| security | prioritized | Currículo é associado somente pelo principal autenticado e proprietário verificado | Contrato de sessão, RNF04 e padrão de `EditarVersaoCurriculo` |
| reliability | prioritized | Uma única transação impede estado parcial em falha | CT-RF12-09 e adapter existente sem commit local |
| simplicity | prioritized | Reutiliza Domain, port de currículo e padrão direto de construção | Implementações atuais na Application |
| modifiability | unresolved | Schema não é congelado sem política de repetição | Ausência de unicidade e identidade no RF, matriz e DER |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| user-value | A ação explícita do estudante cria associação persistida | RF12, RN01 e CT-RF12-05 |
| interoperability | Vaga representada por `VagaId` textual opaco | Identificador externo existente; nenhum formato adicional exigido |
| simplicidade de integração | Sem chamada ao Grupo 2 na criação | A associação é manual; resultado externo é sugestão |
| segurança | Nenhum identificador de usuário declarado pelo cliente torna-se ator confiável | Contrato de sessão; middleware/dependência ainda precisa ser confirmado no código |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | Reimplementar a regra ou persistir classes antes da normalização pode armazenar candidatura sem interesse | Alta | Estudante, produto e dados |
| security | Confiar no usuário_id do corpo/rota permite associação com currículo alheio | Alta | Estudantes e responsáveis pelos dados |
| reliability | Commits separados podem deixar cabeçalho sem classes ou classes incompletas | Alta | Estudantes e suporte |
| user-value | Sem adapter/migration, a associação desaparece e RF12/CT-RF12-05 não são atendidos | Alta | Estudante |
| modifiability | Definir chave sem política de repetição pode exigir migração/reconciliação | Média/alta | Operação e manutenção |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | Um caso de uso, port e mapping a mais que um handler simples | Simplicity | Aceitável; necessário para as fronteiras e persistência existentes |
| security | A rota depende de sessão comum e faz consulta de propriedade antes de gravar | Delivery-speed | Aceitável; identidade é requisito e dado é protegido |
| reliability | Transação externa controla a operação inteira e requer rollback de teste | Simplicity | Aceitável; CT-RF12-09 exige isso |
| modifiability | Adiar a migration/constraint até resolver identidade e repetição | Delivery-speed | Aceitável até produto/arquitetura definir; não aceitável como entrega final RF12 |

## Riscos e efeitos de segunda ordem

- Inserção em múltiplas chamadas/transactions pode persistir candidatura isolada em falha; normalização precisa ocorrer antes do único pedido de persistência, e linhas precisam compartilhar rollback.
- Usar `usuario_id` do path atual sem contexto autenticado reproduziria limitação documentada nas rotas de currículo e não satisfaria o contrato de sessão.
- Converter falha de database em “não encontrado” ou sucesso esconderia erro; deixar falha de persistência explícita para o tratamento de infraestrutura/API já estabelecido.
- Não verificar vaga externamente significa que uma referência desatualizada pode ser persistida; nenhuma política de validade/expiração foi especificada, então esta perda é aceita e não justifica introduzir chamada ao Grupo 2.
- Sem decisão para duplicidade, deixar constraint padrão do banco produzir erro bruto também não define comportamento aceitável; resolver a política antes da publicação do endpoint e da migration.
- Um ID próprio afeta ORM, migration, relacionamento das classificações e retorno da API; chave composta afeta referências futuras. Essa decisão deve considerar #132, sem implementar atualização agora.
- A criação de uma associação manual não deve criar associação de qualquer outro currículo nem considerar a inclusão automática de interesse uma segunda associação.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Reuso do agregado mantém normalização | Código #131 atual e testes Domain já existentes | Revisar/rodar regressão unitária da associação e testar o caso de uso recebendo candidatura | Application/API alteram classificações separadamente ou o resultado salvo difere do agregado |
| Classificação inicial vazia não salva | Construtor Domain exige pelo menos uma classificação e CT-RF12-06 | Teste de Application: exceção antes de chamar repository; API unitária para erro de validação de corpo | Port é chamado ou API aceita vazio |
| Currículo deve pertencer ao usuário autenticado | Contrato de sessão, caso de uso de edição e RNF04 | Testar titular, currículo ausente e currículo de outro ator; teste API garante ator derivado da sessão | Qualquer caminho aceita usuário controlado pelo cliente ou salva de outro dono |
| Vaga não requer consulta ao Grupo 2 | RF12/RN01 e contrato que classifica retorno como sugestão | Teste de Application com `VagaId` recebido, sem cliente externo | RF ou contrato aprovado passar a exigir revalidação |
| Port dedicado é necessário | `RepositorioCurriculo` só trabalha com `Curriculo` e busca; nenhum port de associação foi encontrado | Verificar assinatura da nova porta e doubles unitários | Repositório genérico existente aceitar explicitamente aggregates distintos sem violar coesão |
| Adapter Code First persiste todo estado | RNF05, CT-RF12-05 e padrão metadata/Alembic | Mapping test, repository adapter tests, round-trip com banco/migration | Association ou classes não são reconstruídas ou falha parcial fica commitada |
| Uma transação cobre a escrita integral | CT-RF12-09 e adapter corrente delega transaction ao chamador | Teste de integração: falha na persistência de classe, rollback e banco sem linhas parciais | Commit por etapa ou dados sobrevivem após falha |
| Repetição e chave persistida estão decididas | Decisão de produto/owner, ajuste de requisito ou teste de aceitação | Registrar política; testar duplicata e constraint em caso de uso/repository/DB | Evidência nova contradiz unicidade ou idempotência selecionada |
| Rota usa principal comum | Implementação concreta de autenticação/contexto e contrato de sessão | Inspecionar ponto de composição; teste API sem sessão (401), sessão válida e usuário conflitante no request | Dependência não existe, não é confiável, ou identidade enviada pelo cliente prevalece |

## Handoffs e atividades posteriores

### Implementação #130

- Incluir unitários Application para currículo próprio/ausente/alheio, não persistir sem classificação, construir uma vez com o agregado #131 e encaminhar o estado normalizado a `salvar`, sem chamada a Grupo 2, e propagar falha.
- Incluir unitários API para autorização/contexto, validação sintática, DTO/erro e não execução sem autenticação; cobrir que ator vem do principal da sessão, não do request.
- Adicionar port de associação e adapter SQLAlchemy, com testes unitários de conversão, flush e falhas.
- Adicionar mapping/metadata/migration Code First. Atualizar DER quando a identidade e schema estiverem definidos.
- Adicionar integração de persistência para round-trip (CT-RF12-05) e rollback completo (CT-RF12-09), usando ambiente `tests` do projeto. Unitários backend ficam no ambiente `backend`.
- Resolver, antes da conclusão, política de repetição e chave/ID técnico em uma fonte aprovada. Se não houver essa decisão, manter as duas pendências abertas e não escolher constraint silenciosamente.
- Confirmar a dependência comum de sessão no composition root; se indisponível, abrir/encaminhar a dependência para a atividade de autenticação correspondente, sem expor a rota protegida sem autenticação.

### Explicitamente fora da #130 — #132

- Adicionar classificações após a criação.
- Remover qualquer classificação, inclusive `candidatura` ou `interesse`.
- Decidir o efeito de remover `interesse` enquanto há candidatura.
- Decidir ou implementar remoção da última classificação.
- Atualizar classificações existentes; qualquer operação futura deve carregar associação válida e chamar operações do mesmo agregado.
- Não acrescentar API de edição, métodos Domain de remoção ou testes que especulem esses comportamentos.

### Fora desta decisão

- Não analisar nem implementar outras issues, integração Grupo 2, fluxo de busca ou comunicação externa.
- Não executar testes/build nesta etapa de análise.

## Síntese

A #130 é a criação manual e persistente de uma associação, com Application como orquestradora principal e uma implementação vertical pelas camadas: a API deriva o estudante do contexto autenticado; o caso de uso consulta `RepositorioCurriculo`, verifica propriedade, instancia diretamente `AssociacaoCurriculoVaga` da #131 e chama um port novo de associação; Infrastructure implementa mapping, adapter e migration Code First sob uma transação única. Não é necessário consultar Grupo 2 nem inventar identidade adicional na entrada.

A regra `candidatura => interesse`, a classificação não vazia, a não duplicação e a preservação de classificações já foram resolvidas pela #131 e devem ser exercidas pelo agregado, sem lógica paralela. Para completar RF12, migration/persistência fazem parte da #130: não há evidência de uma issue que as separe.

Permanece pendente a política para criar de novo o mesmo par e a escolha entre chave composta e ID persistido próprio. Além disso, a API deve integrar a dependência de autenticação descrita no contrato, cuja implementação concreta não foi encontrada no backend inspecionado. Nenhuma dessas incertezas autoriza antecipar a #132.
