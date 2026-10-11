---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v002"
status: proposed
created_at: "2026-10-11T02:35:11-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261011-001011-associacao-curriculo-vaga-v001.md
  supersedes: prompts/backend/20261011-001011-associacao-curriculo-vaga-v001.md
  change_type: scope-change
  secondary_change_types: [enrichment, correction]
  decision_impact: strengthened
subjects:
  kind: mixed
  files:
    - path: "code-alchemists-br/sistema-curriculo#130"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: whole-file
      locator: "título e corpo atuais consultados em 2026-10-11"
      content_state: external
      revision: null
      availability: available
    - path: "code-alchemists-br/sistema-curriculo#131"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: whole-file
      locator: "título e corpo atuais consultados em 2026-10-11"
      content_state: external
      revision: null
      availability: available
    - path: "code-alchemists-br/sistema-curriculo#132"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: whole-file
      locator: "título e corpo atuais consultados em 2026-10-11"
      content_state: external
      revision: null
      availability: available
    - path: "Solicitação complementar do usuário — execução exclusiva da #131 (2026-10-11)"
      relationship: primary
      representation: prose
      function: documentation
      format: mensagem de usuário
      analysis_scope: whole-file
      locator: "instruções complementares e resposta de autorização para revisar"
      content_state: external
      revision: null
      availability: available
    - path: prompts/backend/20261011-001011-associacao-curriculo-vaga-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: "análise decisória anterior, versão v001"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF12, RN01-RN04, tabela de combinações e detalhamentos pendentes"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/matriz_testes.md
      relationship: primary
      representation: prose
      function: test
      format: markdown
      analysis_scope: selected-section
      locator: "CT-RF12-01 a CT-RF12-09 e CT-RF12-C01 a CT-RF12-C07"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: documentation
      format: Mermaid ER diagram in Markdown
      analysis_scope: whole-file
      locator: "diagrama ER completo; não contém associação currículo-vaga"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/Arquitetura/ADR-001-arquitetura-do-sistema.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "seções 2.1-2.4, 2.12-2.14"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "aggregate root, estado privado, visão imutável e invariantes locais"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "identificadores tipados CurriculoId e outros IDs"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/itens_perfil.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "entidades do domínio com identidade tipada e proprietário"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/exceptions.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "RegraDeDominioViolada"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/__init__.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "exports públicos do domínio"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "contratos de repositório e identificadores; sem porta existente para vaga/associação"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_domain_curriculo.py
      relationship: supporting
      representation: test-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: "testes unitários do aggregate root e das invariantes locais"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_domain_entities.py
      relationship: supporting
      representation: test-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "construção de entidades e IDs tipados em memória"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/doubles/api_vagas_grupo2.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "VagaExternaDto.id é str"
      content_state: working-tree
      revision: null
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: "escopo, Nix e documentação obrigatória"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: "fronteiras Clean Architecture/DDD e testes"
      content_state: working-tree
      revision: null
      availability: available
    - path: prompts/README.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: "organização e convenções de prompts"
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories:
    - prompts/backend
    - prompts/requisitos
    - prompts/revisao
    - prompts/ambientes
  confidence: high
  rationale: "A análise define um modelo e regras de domínio do backend; backend é a categoria semanticamente mais específica entre as pastas existentes."
classification:
  sphere: engineering
  concerns: [domain, architecture, data]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: low
  reversibility: moderate
  risk: medium
---

# Análise de decisão — Modelo e regra da associação currículo-vaga

> **Escopo desta aprovação:** somente a fatia de Domain e testes unitários da #131. A proposta não aprova #130, #132, remoção de classificações ou persistência. As perguntas abertas abaixo continuam sem decisão e não autorizam comportamentos correspondentes.

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

## Informações complementares

- As três issues estão abertas e atribuídas ao mesmo responsável. Cada corpo consultado contém a instrução genérica: “Tarefa da fatia vertical atribuída a @Andre-LSL. Inclua os testes unitários pertinentes.” Os corpos não detalham o comportamento além dos títulos.
- A consulta `gh issue view` foi feita ao repositório `code-alchemists-br/sistema-curriculo` em 2026-10-11.
- A issue #131 foi consultada novamente durante esta revisão e continua aberta, sem comentários ou detalhes adicionais no corpo além da instrução genérica já registrada.
- A análise v001 não encontrou artefato anterior dedicado às issues #130, #131 ou #132; esta revisão continua essa linhagem.
- O diagrama ER atual não modela associação currículo-vaga.
- Após a v001, o usuário solicitou implementação exclusiva da #131, exigiu a manutenção das quatro pendências fora desse escopo e autorizou a revisão antes de prosseguir: “Sim, revisar a análise primeiro”.

### Entrada posterior do usuário — solicitação de implementação (literal)

> $backend-domain-orchestration-v2
>
> Implemente SOMENTE a issue #131:
> "Implementar regra de candidatura implica interesse".
>
> Use como decisão técnica a análise:
>
> prompts/backend/20261011-001011-associacao-curriculo-vaga-v001.md
>
> IMPORTANTE
>
> A análise foi feita conjuntamente para #130, #131 e #132, mas nesta execução o escopo é EXCLUSIVAMENTE a #131.
>
> Não implemente #130.
> Não implemente #132.
> Não implemente persistência.
> Não implemente repository.
> Não implemente API.
> Não implemente adapter.
> Não implemente integração com Grupo 2.
> Não implemente migration.
>
> OBJETIVO
>
> Implementar no Domain a regra:
>
> candidatura implica interesse.
>
> Quando uma associação possuir ou receber a classificação `candidatura`, ela também deve possuir `interesse`.
>
> As classificações reconhecidas pelos requisitos atuais são:
>
> - interesse
> - compatibilidade
> - candidatura
>
> Use os padrões já existentes no Domain e siga os AGENTS.md aplicáveis.
>
> ESCOPO MÍNIMO
>
> Se ainda não existir uma estrutura de domínio adequada para representar a associação currículo-vaga, crie somente a estrutura mínima necessária para suportar a regra da #131.
>
> Não transforme essa estrutura na implementação completa da criação/persistência da associação prevista na #130.
>
> Não tome decisões que pertencem às issues posteriores.
>
> PENDÊNCIAS QUE NÃO DEVEM SER RESOLVIDAS NESTA ISSUE
>
> A análise identificou que ainda não há evidência suficiente para definir:
>
> 1. o comportamento ao tentar remover `interesse` enquanto `candidatura` permanece ativa;
>
> 2. o comportamento ao tentar remover a última classificação;
>
> 3. a estratégia de unicidade da associação currículo-vaga;
>
> 4. se a associação persistida terá ID próprio ou chave composta.
>
> Não invente essas regras.
>
> Se implementar uma API genérica de remoção obrigar a decidir algum desses pontos, não implemente essa operação nesta issue.
>
> TESTES DA #131
>
> Adicione testes unitários pertinentes à regra, incluindo no mínimo:
>
> 1. associação/classificação apenas com `interesse` permanece com `interesse`;
>
> 2. adicionar/criar com `candidatura` resulta em:
>    `candidatura + interesse`;
>
> 3. adicionar `candidatura` quando `interesse` já existe não duplica classificação;
>
> 4. adicionar `candidatura` preserva outras classificações existentes, como `compatibilidade`;
>
> 5. o domínio não permite que um estado produzido pela operação da #131 tenha `candidatura` sem `interesse`.
>
> Não adicione testes de persistência, API ou infraestrutura.
>
> VALIDAÇÃO
>
> Execute somente os testes necessários no ambiente Nix indicado pelo projeto.
>
> Execute lint/format apenas nos arquivos alterados, respeitando os AGENTS.md.
>
> Não faça commit.
> Não faça push.
>
> Ao final informe:
>
> - arquivos criados/alterados;
> - comportamento implementado;
> - testes executados;
> - qualquer decisão que tenha permanecido pendente.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Escopo aprovado | Questões conjuntas de #130, #131 e #132; status `pending` por decisões não especificadas de remoção e persistência | Execução delimitada à regra e aos testes unitários da #131; questões remanescentes continuam pendentes fora da fatia | Instrução posterior explícita do usuário e confirmação “Sim, revisar a análise primeiro” | A decisão da fatia #131 fica `proposed`; as pendências não são resolvidas nem bloqueiam essa fatia |
| Critérios de teste da #131 | Recomendações de teste para a regra compartilhada | Cinco critérios mínimos especificados pelo usuário, incluindo preservação de outras classificações e nenhum estado produzido com candidatura sem interesse | Tornar o resultado testável e separar testes das issues posteriores | Reforça os critérios sem alterar a semântica das operações de remoção |
| Evidência da issue #131 | Consulta registrada na v001 | Issue consultada novamente; permanece aberta e sem novos detalhes | Confirmar atualidade da demanda focal | Nenhuma alteração material de requisito |
| Classificação dos artefatos | Alguns descritores de função não eram valores controlados da taxonomia | Funções normalizadas conforme a taxonomia v4 | Correção de rastreabilidade, sem alteração da decisão de domínio | Metadados passam a usar vocabulário controlado |
| Rastreabilidade | v001 | v002, supersede v001 | Revisão de escopo e enriquecimento | v001 preservada sem alteração |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `code-alchemists-br/sistema-curriculo#130` | Primário | Prosa | Requisito da issue | GitHub issue | Título e corpo atuais | Externo; consultado em 2026-10-11 |
| `code-alchemists-br/sistema-curriculo#131` | Primário | Prosa | Requisito da issue | GitHub issue | Título e corpo atuais | Externo; consultado em 2026-10-11 |
| `code-alchemists-br/sistema-curriculo#132` | Primário | Prosa | Requisito da issue | GitHub issue | Título e corpo atuais | Externo; consultado em 2026-10-11 |
| Solicitação complementar do usuário — execução exclusiva da #131 | Primário | Prosa | Documentação de requisito | Mensagem de usuário | Instruções de escopo, comportamento, pendências, testes e validação; preservadas acima | Externo; recebida em 2026-10-11 |
| `prompts/backend/20261011-001011-associacao-curriculo-vaga-v001.md` | Apoio | Prosa | Documentação decisória | Markdown | Artefato v001 lido integralmente | Working tree; não versionado |
| `docs/requisitos_funcionais.md` | Primário | Prosa | Requisitos | Markdown | RF12, RN01-RN04, combinações e pendências ligadas a associações | Working tree |
| `docs/matriz_testes.md` | Primário | Prosa | Critérios de teste | Markdown | CT-RF12-01..09 e CT-RF12-C01..C07 | Working tree |
| `docs/modelagem_der.md` | Apoio | Diagrama | Modelo de dados | Mermaid/Markdown | Diagrama ER completo; não inclui associação currículo-vaga | Working tree |
| `docs/Arquitetura/ADR-001-arquitetura-do-sistema.md` | Apoio | Prosa | Arquitetura | Markdown | Separação de camadas, domínio, persistência e testes | Working tree |
| `src/backend/domain/curriculo.py` | Apoio | Código-fonte | Padrão de agregado | Python | Entidade, mutações locais, coleção privada e leitura imutável | Working tree |
| `src/backend/domain/value_objects.py` | Apoio | Código-fonte | Padrão de identidades | Python | Definição de `CurriculoId` e demais IDs | Working tree |
| `src/backend/domain/itens_perfil.py` | Apoio | Código-fonte | Padrão de entidades | Python | Identidade tipada e propriedade | Working tree |
| `src/backend/domain/exceptions.py` | Apoio | Código-fonte | Erro de domínio | Python | `RegraDeDominioViolada` | Working tree |
| `src/backend/domain/__init__.py` | Apoio | Código-fonte | API pública do domínio | Python | Exports | Working tree |
| `src/backend/application/ports.py` | Apoio | Código-fonte | Portas existentes | Python | Contratos de repositório e geração de IDs pertinentes | Working tree |
| `src/backend/tests/test_domain_curriculo.py` | Apoio | Testes | Testes unitários | Python | Invariantes do agregado e preparação em memória | Working tree |
| `src/backend/tests/test_domain_entities.py` | Apoio | Testes | Testes unitários | Python | Entidades e IDs tipados | Working tree |
| `src/backend/tests/doubles/api_vagas_grupo2.py` | Apoio | Código de teste | Contrato de vaga externa | Python | Campo `VagaExternaDto.id: str` | Working tree |
| `AGENTS.md`, `src/backend/AGENTS.md` | Contexto | Instruções | Restrições aplicáveis | Markdown | Escopo, camadas, DDD, testes e documentação | Working tree |
| `prompts/README.md` | Contexto | Prosa | Organização de prompts | Markdown | Categorias e convenções | Working tree |

### Limites da evidência dos artefatos

- A v001 é um artefato novo não versionado no Git no momento da revisão; foi preservada sem alteração e lida integralmente como base desta linhagem.
- Os arquivos de requisitos, matriz, arquitetura e domínio registrados na v001 não apresentam alterações no status do Git desta revisão; não foram relidos integralmente. A decisão se baseia nos recortes já registrados na v001 e na nova delimitação do usuário.
- As issues não descrevem contratos, cenários de borda ou modelo; para regras, prevalecem RF12, RN03 e a matriz de testes.
- A ausência da associação no DER e no código é evidência de que ainda não há modelo local a reutilizar; não autoriza inferir schema, identidade própria, unicidade, timestamps ou exclusão.
- O double da API do Grupo 2 representa o identificador da vaga como texto. Não há `VagaId` no domínio consultado nem requisito que determine UUID para vagas.
- A busca localizada no domínio não encontrou enums existentes; a escolha de enum para o vocabulário fechado abaixo é recomendação de design, não padrão preexistente.
- A leitura de `ports.py` foi limitada a contratos de repositório/ID relevantes. Não foi feita revisão geral do backend.

## Problema enriquecido

### Resultado desejado

Definir um único modelo de domínio para a associação currículo-vaga, de forma que a regra “candidatura implica interesse” seja implementável primeiro na #131 e usada sem duplicação pela criação (#130) e atualização (#132).

### Atores e interesses

- Estudante: inicia manualmente a associação e escolhe classificações.
- Domain: mantém as classificações da associação em estado válido.
- Application: orquestra criação e atualização e verifica contexto/propriedade por portas.
- Infrastructure: persiste associações e estado de classificação.
- API: valida formato externo e traduz comandos/resultados, sem conter regra de negócio.

### Evidências e fatos observados

- A instrução posterior restringe esta primeira fatia à #131 e exige explicitamente que remoção genérica de classificação não seja implementada caso implique escolher qualquer uma das regras ainda pendentes.
- Para a #131, a instrução posterior torna obrigatórios testes de interesse isolado, criação/adicionamento de candidatura com interesse, não duplicação de interesse preexistente, preservação de compatibilidade e ausência de estado de domínio candidatura-sem-interesse produzido pela operação pública.
- RF12 permite criar manualmente associação de um currículo com uma vaga e armazenar uma ou mais classificações dentre `interesse`, `compatibilidade` e `candidatura`.
- RN01 exige iniciativa manual do estudante; visualizar/buscar/exportar não cria associação automaticamente.
- RN02 permite várias das três classificações simultaneamente.
- RN03 estabelece que candidatura implica interesse e exige preservar essa condição em qualquer alteração.
- RN04 diz que compatibilidade é manual e não exige cálculo automático.
- CT-RF12-02 e a combinação C03 esperam que uma entrada classificada somente como candidatura resulte em candidatura e interesse na associação escolhida, sem criar outra associação.
- CT-RF12-03 determina que remover candidatura mantém interesse.
- CT-RF12-04 determina que adicionar compatibilidade preserva candidatura e interesse.
- CT-RF12-06 exige pelo menos uma classificação para criar a associação.
- CT-RF12-08 exclui envio de currículo ou candidatura a serviço externo.
- CT-RF12-09 exige que falha de persistência não deixe associação parcial nem candidatura sem interesse.
- RF12 lista exatamente três classificações; não há evidência para estado, score ou classificação adicional.
- `CurriculoId` é um value object baseado em UUID. O DTO externo atual representa `VagaExternaDto.id` como `str`.
- O padrão do domínio usa agregados com estado protegido, métodos explícitos, coleções internas e vistas imutáveis; violações locais usam `RegraDeDominioViolada`.
- A arquitetura e as instruções de backend colocam invariantes no Domain, orquestração em Application, ORM/migrations em Infrastructure e validação de formato/transporte na API.

### Hipóteses

- A associação é um agregado pequeno: a relação e suas classificações formam uma unidade local de consistência, e sua regra pertence naturalmente a essa unidade.
- Um `VagaId` pode preservar o identificador externo opaco como texto, sem impor UUID ou normalização sem requisito.
- Não é necessário duplicar `usuario_id` na associação para proteger a regra de classificação; propriedade e autorização devem ser verificadas no fluxo da Application usando o currículo e os contratos disponíveis.
- O modelo de domínio pode existir e ser testado em memória antes de qualquer persistência.

### Perguntas em aberto

- **Pendente, fora da #131:** ao remover `interesse` enquanto `candidatura` está presente, a operação deve ser rejeitada, deixar o estado inalterado/restaurar interesse ou também remover candidatura? O requisito exige preservar RN03, mas a matriz não define o resultado específico; os requisitos registram o comportamento de interface como detalhamento ainda necessário. Nenhum método de remoção de classificações será implementado na #131.
- **Pendente para #132:** ao remover a única classificação restante, deve-se rejeitar a atualização ou excluir a associação? RF12 requer uma ou mais classificações, mas não define essa transição; a exclusão de associações também aparece como fluxo ainda a detalhar. A #131 não oferece remoção de classificação.
- **Pendente para #130/persistência:** uma associação currículo-vaga pode ser repetida? Ela terá ID próprio ou chave composta? Os documentos analisados não especificam unicidade nem chave técnica.
- **Pendente para fronteiras externas e fora da #131:** qual mensagem/resposta a API apresenta se uma alteração de interesse for incompatível com candidatura? Depende da decisão de produto/domínio e não há API nesta fatia.
- **Pendente apenas se houver múltiplas fontes de vaga:** se IDs de fontes distintas colidirem, será necessário escopo de provedor no identificador; o contexto atual só evidencia o DTO do Grupo 2.

### Escopo

- Somente o mínimo de modelo Domain necessário à regra da #131: associação com identificadores tipados, enum das classificações permitidas e coleção protegida.
- A regra de inclusão automática de `interesse` ao construir/adicionar `candidatura`, preservando quaisquer classificações anteriores.
- Somente testes unitários de domínio que comprovem os critérios explicitados para a #131.
- Os limites do que pertence às #130 e #132 e as pendências que permanecem fora desta fatia.

### Fora do escopo

- A implementação de código não é parte deste artefato de análise; o handoff elegível posterior é exclusivamente a #131.
- API, persistência, migrations, ORM, adapters ou contratos concretos de repositório.
- Fluxo de busca, cálculo de compatibilidade, candidatura em serviço externo, estados adicionais, histórico ou timestamps.
- Decidir unicidade do par, ID persistente independente ou exclusão quando currículo/vaga deixa de existir.
- Definir a experiência de interface para remoção de interesse com candidatura ativa.
- Qualquer operação genérica de remoção de classificação ou regra para remoção da última classificação.

### Critérios de sucesso

- A #131 pode ser implementada e testada sem banco ou API.
- A entidade compartilhada não permite que candidatura seja produzida sem interesse quando recebe/adiciona candidatura.
- A #131 não contém API genérica de remoção nem decide semânticas de exclusão/remoção.
- #130 e #132 encaminham criações/alterações ao mesmo comportamento do Domain, sem reimplementar a regra.
- Somente as três classificações sustentadas aparecem no modelo.
- As decisões não sustentadas permanecem explícitas como pendências.

## Restrições aplicáveis

- Respeitar Clean Architecture e DDD: regra local protegida pelo agregado no Domain; Application não depende de Infrastructure; API e repositórios não contêm regras.
- Não alterar a arquitetura existente nem adiantar API ou infraestrutura na #131.
- Identificadores de currículo e vaga devem preservar os tipos/origens comprovados; não tratar a vaga como UUID sem evidência.
- Persistência relacional futura usa ORM Code First e migrations na Infrastructure, mas isso não faz parte da #131.
- A #131 deve incluir testes unitários do backend, independentes de banco, rede, relógio e framework, executados no ambiente Nix `backend`.
- Classes e funções adicionadas devem documentar o que fazem, como fazem e a finalidade.
- O arquivo deste artefato é a única escrita autorizada nesta análise.

## Classificação comentada

- **Esfera `engineering`:** o problema é decidir a estrutura técnica do modelo e sua implementação entre camadas.
- **Preocupações `domain`, `architecture`, `data`:** há invariante de negócio, fronteiras de camadas e futura representação de associação/classificações.
- **Tipo `design`:** a análise seleciona modelo e distribuição de responsabilidades.
- **Escopo `component`:** restringe-se ao componente backend, sem mudança entre sistemas.
- A incerteza da decisão isolada da #131 é baixa: a regra e os casos mínimos têm respaldo direto em RN03, CT-RF12-02/C03 e na instrução posterior. Permanecem incertezas médias nas operações futuras de remoção e persistência, explicitamente fora desta aprovação.

## Decisão de roteamento

Destino: `prompts/backend`. As subpastas existentes foram inventariadas; `backend` é mais específica para uma análise sobre entidades, invariantes e camadas do backend. `requisitos` seria adequada a elicitação funcional geral, mas o resultado principal solicitado é a decisão do modelo de domínio. `revisao` e `ambientes` não correspondem ao propósito. Não foi encontrado `AGENTS.md` adicional em `prompts/`.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | Máxima | Nenhum estado final pode violar RN03 | É a regra comum das três issues |
| simplicity | Alta | Modelo mínimo, sem campos não requisitados | Permite iniciar pela #131 sem arquitetura especulativa |
| modifiability | Alta | Um único ponto de aplicação da regra | #130 e #132 não podem divergir |
| interoperability | Média | Preservar o ID externo de vaga sem supor UUID | A vaga vem de API e hoje tem ID textual |
| cognitive-load | Média | Tipos explícitos e conjunto pequeno | Facilita entender e testar combinações |

## Alternativas consideradas

1. **Agregado `AssociacaoCurriculoVaga` com enum de classificação e conjunto. Recomendado.** Guarda `CurriculoId`, um `VagaId` opaco e classificações; expõe alterações que normalizam candidatura para incluir interesse. Encapsula a invariável local junto ao estado e atende a criação e atualização.
2. **Value object separado `ClassificacoesAssociacao` dentro do agregado.** Pode concentrar a normalização e produzir coleção imutável; é válido, mas adiciona uma abstração sem necessidade atual demonstrada, dado que há uma única regra e um único proprietário natural do estado.
3. **Três flags booleanas ou bit flags.** Codificam as combinações possíveis, mas tornam a adição de valores/serialização menos explícita e podem permitir combinações inválidas; não oferecem benefício sobre enum + conjunto para exatamente três rótulos simultâneos.
4. **Regra em Application ou Infrastructure.** Inviável: viola as fronteiras arquiteturais e permite que outros caminhos criem estado inválido. A duplicação em #130 e #132 também contraria a exigência de regra compartilhada.

### Responsabilidades por camada

| Camada | Responsabilidade nesta funcionalidade |
|---|---|
| Domain | Definir `AssociacaoCurriculoVaga`, os identificadores de domínio e as três classificações; proteger o estado válido e implementar candidatura ⇒ interesse sem conhecer persistência ou transporte. |
| Application | Orquestrar intenção manual de criação (#130) e atualização (#132), obter/persistir o agregado por portas e verificar que o estudante atua sobre currículo próprio. A #131 isolada não precisa de caso de uso ou porta. |
| Infrastructure | Implementar armazenamento e mapeamento Code First, migrations, transação/atomicidade e conversão entre persistência e agregado, quando as issues de persistência forem executadas. |
| API | Validar forma dos dados de entrada, autenticação/autorização de fronteira e traduzir comandos/respostas/erros; não duplicar a regra de classificação nem expor entidade de domínio. |

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa 1: agregado + enum/set | Alternativa 2: VO de classificações | Alternativa 3: flags | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| correctness | Alta | +2 | +2 | 0 | Alta | Todas podem encapsular regra, mas agregado é o dono natural; flags dependem de validação explícita |
| simplicity | Alta | +2 | 0 | +1 | Média | Um agregado e uma coleção requerem menos peças do que agregado mais VO |
| modifiability | Alta | +1 | +2 | -1 | Média | VO pode crescer com múltiplas regras; flags escalam pior ao acrescentar rótulos |
| interoperability | Média | +1 | +1 | 0 | Média | Enum/set e VO são mapeáveis sem antecipar schema; flags criam representação de bit |
| cognitive-load | Média | +2 | 0 | -1 | Média | Enum e conjunto tornam multiplicidade e vocabulário visíveis |

## Histórico e decisão atual

### Decisão da versão anterior

v001 recomendou o agregado de domínio com conjunto de classificações e marcou a análise conjunta como `pending`, pois não havia evidência sobre remoções e detalhes de persistência.

### Decisão recomendada nesta versão

Para a fatia da #131, usar o agregado de domínio mínimo `AssociacaoCurriculoVaga` como dono de `curriculo_id`, `vaga_id` e de um conjunto de classificações. O vocabulário será um enum `ClassificacaoAssociacao` restrito a `INTERESSE`, `COMPATIBILIDADE` e `CANDIDATURA`; a coleção interna será um `set` e a leitura pública, uma visão imutável (`frozenset`), seguindo o padrão já usado pelo agregado `Curriculo`.

Ao construir o agregado com candidatura, ou ao adicioná-la, o comportamento deve garantir interesse automaticamente. Assim, entrada `CANDIDATURA` resulta no conjunto `{CANDIDATURA, INTERESSE}`; `{COMPATIBILIDADE, CANDIDATURA}` resulta nas três classificações. Adicionar candidatura quando interesse já existe não cria duplicata; classificações não relacionadas são preservadas. A regra é domínio e deve ser invocada pelo mesmo modelo por #130 e #132.

Reutilizar `CurriculoId` para identificar currículo. Criar `VagaId` tipado que preserve como texto opaco o `id` externo atualmente textual; não exigir UUID, gerar identificador local ou incorporar dados descritivos da vaga. Não acrescentar ID próprio à associação, proprietário duplicado, timestamp ou estado sem requisito. A política de unicidade/chave de persistência fica pendente para a #130.

O modelo não oferecerá operação de remoção de classificação nesta fatia. Isso evita escolher o que ocorre ao remover interesse com candidatura ativa ou ao tentar retirar a última classificação. Essas questões permanecem pendentes para #132; também permanecem pendentes unicidade e chave/ID persistidos da associação para #130.

### Decisões necessárias agora e decisões adiáveis

- **Decidir agora para #131:** vocabulário fechado das três classificações; IDs de currículo e vaga tipados sem impor UUID à vaga; modelo de domínio com estado não vazio; normalização explícita de candidatura para incluir interesse; propriedade da regra no agregado.
- **Pode esperar pela #130/#132 e persistência:** ID técnico da associação, chave/constraint de unicidade, schema, representação relacional de classificações, migration, estratégia transacional e API.
- **Precisa de esclarecimento antes do respectivo fluxo de remoção em #132:** remover interesse com candidatura ativa e remover a última classificação. A #131 não inclui esses fluxos.

### Impacto da revisão

O escopo da decisão aprovada foi reduzido de um modelo comum ainda pendente em v001 para o incremento independente e comprovável da #131. A decisão técnica central foi fortalecida pela especificação explícita do usuário para comportamento e testes. As pendências de remoção, unicidade e identidade persistida não foram resolvidas; foram isoladas dos critérios e do código desta fatia.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | Candidatura não existe sem interesse em estado construído ou produzido pela inclusão suportada | RN03, CT-RF12-02/C03 e critérios complementares |
| simplicity | prioritized | #131 pode existir sem dependências externas | Regra local e padrões de teste do domínio |
| modifiability | prioritized | #130 e #132 usam a mesma operação/invariante | Requisito do usuário e propriedade do agregado |
| interoperability | satisficed | Vaga mantém identidade textual da fonte externa | `VagaExternaDto.id: str` |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Interoperabilidade com persistência futura | Não vincular domínio a ORM/tabela | IDs e enum pertencem ao domínio; mapping será externo |
| Escopo da primeira entrega | Somente regra de domínio e testes unitários | Sem portas, casos de uso, API, banco, adapter ou métodos de remoção na #131 |
| Vocabulário | Somente classificações documentadas | Enum limitado às três entradas do RF12 |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | Estado candidatura sem interesse contradiz RN03 e os resultados da matriz | Alta | Estudante, sistema e dados persistidos |
| modifiability | Regras duplicadas podem divergir entre criação e atualização | Média | Desenvolvedores e manutenção futura |
| simplicity | Implementar persistência/API junto da #131 amplia seu escopo e impede teste isolado rápido | Média | Entrega da #131 |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | Criação e inclusão de candidatura precisam passar por operação/fábrica do agregado | Simplicity | Aceitável; é a menor proteção que mantém a regra centralizada |
| modifiability | Introduzir enum de classificação e `VagaId` além do módulo de agregado | Simplicity | Aceitável; reduz mistura de IDs e classificações livres |
| início antecipado da #131 | Não definir semântica de remoção de classificações | Completude da #132 | Aceitável porque a #131 não implementa essas operações e não as testa |

## Riscos e efeitos de segunda ordem

- Se qualquer caminho gravar classificações fora do agregado, a persistência pode aceitar estado inválido. #130 e #132 devem construir/alterar o objeto de domínio e armazenar seu estado resultante.
- A matriz exige que a falha de persistência não deixe associação parcial; atomicidade pertence à implementação da persistência/uso futuro, não ao modelo unitário da #131.
- Uma decisão precipitada de cascata ao remover interesse pode apagar candidatura que o estudante pretendia manter; uma rejeição pode demandar resposta de erro na interface. Ambas são consequências distintas e não resolvidas pelos testes atuais. Remover a última classificação também precisa de decisão para não produzir uma associação sem classificações.
- A escolha de `VagaId` como texto preserva o contrato atual; a eventual integração de novas fontes pode exigir namespace, mas isso não deve ser antecipado agora.
- A ausência de política sobre associação duplicada pode deixar comportamento divergente de criação até #130 definir e testar essa regra.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Associação somente com interesse preserva apenas interesse | Critério complementar 1 do usuário | Teste unitário de construção no agregado da #131 | Construção acrescentar candidatura ou compatibilidade |
| Criação/adição de candidatura resulta em interesse e candidatura | RN03, CT-RF12-02/C03 e critério complementar 2 | Testes unitários de construção e adição da #131 | Qualquer operação pública de criação/adição deixar candidatura sem interesse |
| Adicionar candidatura não duplica interesse preexistente | Critério complementar 3 e semântica de conjunto | Teste unitário da adição no agregado da #131 | Coleção expor duplicatas |
| Adicionar candidatura preserva compatibilidade existente | RN02 e critério complementar 4 | Teste unitário de combinação na #131 | A operação descartar uma classificação anterior |
| Nenhum estado produzido pela operação pública #131 contém candidatura isolada | RN03 e critério complementar 5 | Inspecionar a visão pública após construção e inclusão | Obter `CANDIDATURA` sem `INTERESSE` |
| Compatibilidade é independente | Testes de interesse isolado, compatibilidade isolada e combinações válidas | Testes unitários com as combinações RF12 | Regra nova atribuir compatibilidade automaticamente |
| Remover candidatura preserva interesse | CT-RF12-03 e teste unitário da operação de atualização quando implementada | Testes da #132; handoff, não parte desta proposta | Requisito/teste alterado para remover também interesse |
| Semântica de remover interesse ou a última classificação | Decisão de produto/domínio e atualização da matriz | Refinar antes de criar o fluxo de remoção em #132 | Nova evidência que determine o comportamento |
| Identidade e duplicidade persistidas | Regras de criação e desenho Code First aprovados | Especificação e testes da #130; handoff | Necessidade de múltiplas associações do mesmo par ou nova fonte de vagas |

## Handoffs e atividades posteriores

### Implementação da #131 — primeira entrega

Arquivos prováveis:

- Criar `src/backend/domain/associacao_curriculo_vaga.py` para `AssociacaoCurriculoVaga`, `ClassificacaoAssociacao` e as operações de construção/inclusão que mantêm a invariante.
- Alterar `src/backend/domain/value_objects.py` para adicionar `VagaId` como identidade opaca textual, sem impor formato não especificado.
- Alterar `src/backend/domain/__init__.py` para exportar os conceitos públicos, conforme o padrão do pacote.
- Criar `src/backend/tests/test_domain_associacao_curriculo_vaga.py` para testes unitários de domínio.

Comportamento a implementar:

1. A associação guarda `CurriculoId`, `VagaId` e uma ou mais classificações; o modelo não inventa campos nem classificações.
2. Na construção/normalização e na inclusão de `CANDIDATURA`, acrescenta `INTERESSE` automaticamente; preserva classificações já presentes. O agregado válido contém ao menos uma classificação.
3. `INTERESSE` sozinho e `COMPATIBILIDADE` sozinha permanecem permitidos; compatibilidade não calcula aderência.
4. A regra é pura, local e livre de persistência, rede, API ou efeitos colaterais.
5. A leitura das classificações não permite mutação externa que contorne o agregado.

Testes unitários pertinentes à #131:

- Criar associação com somente `CANDIDATURA` e verificar que o estado contém `CANDIDATURA` e `INTERESSE`.
- Criar associação com somente `INTERESSE` e verificar que permanece somente `INTERESSE`.
- Adicionar `CANDIDATURA` a associação com `INTERESSE` e verificar que interesse continua presente.
- Verificar que o conjunto não contém uma segunda ocorrência de `INTERESSE` depois da inclusão de `CANDIDATURA`.
- Adicionar `CANDIDATURA` a associação com `COMPATIBILIDADE` e verificar as três classificações, sem perda de estado anterior.
- Verificar que incluir somente `INTERESSE` ou somente `COMPATIBILIDADE` não introduz outra classificação.
- Verificar que somente as três classificações do requisito são representáveis e que a visão pública não permite produzir/observar estado com `CANDIDATURA` sem `INTERESSE`.
- Testar preservação dos IDs tipados `CurriculoId` e `VagaId` no modelo.

Não implementar nem testar operação genérica de remoção de classificações na #131. Permanecem pendentes o resultado de remover `INTERESSE` com `CANDIDATURA` ativa e a tentativa de remover a última classificação. Remover `CANDIDATURA` mantendo `INTERESSE` tem resultado documentado, mas a operação e seu teste pertencem à #132.

### Fora da #131

- **#130:** caso de uso de criação manual, validação de pelo menos uma classificação na entrada, verificação de currículo/proprietário e vaga, política de duplicidade, porta de repositório, endpoint e comportamento sem interação manual. A criação deve chamar o mesmo agregado/fábrica da #131; se receber candidatura, não duplicar a regra.
- **#132:** carregar associação persistida e atualizar classificações via operações do mesmo agregado; garantir que adicionar compatibilidade preserve candidatura/interesse e que remover candidatura deixe interesse. Decidir primeiro a remoção de interesse com candidatura presente e a tentativa de remover a última classificação.
- **Infrastructure/#130/#132:** mapping Code First, migration, atomicidade, round-trip e falha sem persistência parcial.
- **API/#130/#132:** DTOs, validação sintática, autorização/autenticação e tradução de erros; sem regra `candidatura ⇒ interesse` em controller.
- Testes de persistência, contrato, API ou integração pertencem às fatias futuras apropriadas, não à unidade da #131.

## Síntese

A evidência é suficiente para propor a #131 isoladamente: criar o mínimo modelo Domain da associação com `CurriculoId`, `VagaId` textual tipado e conjunto fechado das três classificações; construir ou adicionar candidatura sempre acrescenta interesse, sem duplicá-lo e sem descartar compatibilidade. Não se implementa remoção, aplicação, API ou persistência. A #130 e a #132 devem reutilizar esse mesmo núcleo em entregas futuras. Remoções, unicidade e identidade persistida continuam pendentes e fora da decisão atual. O status `proposed` solicita aprovação desta fatia; não é aprovação das issues #130 ou #132.
