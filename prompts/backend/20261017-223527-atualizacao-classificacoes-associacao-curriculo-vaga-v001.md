---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-17T22:35:27-03:00"
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
    - path: "code-alchemists-br/sistema-curriculo#132"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: whole-file
      locator: "título e corpo consultados via gh issue view"
      content_state: external
      revision: null
      availability: available
    - path: "Solicitação do usuário — análise exclusiva da issue #132"
      relationship: primary
      representation: prose
      function: documentation
      format: mensagem de usuário
      analysis_scope: whole-file
      locator: "objetivo, contexto, questões, escopo e saída requeridos"
      content_state: external
      revision: null
      availability: available
    - path: "code-alchemists-br/sistema-curriculo#130"
      relationship: supporting
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: whole-file
      locator: "título e corpo consultados via gh issue view"
      content_state: external
      revision: null
      availability: available
    - path: "code-alchemists-br/sistema-curriculo#131"
      relationship: supporting
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: whole-file
      locator: "título e corpo consultados via gh issue view"
      content_state: external
      revision: null
      availability: available
    - path: "code-alchemists-br/sistema-curriculo#541"
      relationship: supporting
      representation: prose
      function: documentation
      format: GitHub pull request
      analysis_scope: whole-file
      locator: "descrição, implementação, decisões, handoff e status consultados via gh pr view"
      content_state: external
      revision: null
      availability: available
    - path: prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "solicitação original das issues, identidade composta, limites de #130 e handoff explícito para #132"
      content_state: working-tree
      revision: "v004; checkout baseado em ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "decisão da #131, invariantes implementadas, semânticas de remoção deliberadamente pendentes e handoff para #132"
      content_state: working-tree
      revision: "v002; checkout baseado em ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: selected-section
      locator: "escopo, Nix, documentação e limites de atividade"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: prompts/README.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: "organização e propósito das subpastas de prompts"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF12, RN01-RN04, combinações válidas e detalhamentos pendentes sobre alterações"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: docs/matriz_testes.md
      relationship: primary
      representation: prose
      function: test
      format: Markdown
      analysis_scope: selected-section
      locator: "CT-RF12-01..09 e CT-RF12-C01..C07"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RNF04/RNF05, critérios de verificação e pendências de autorização"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/domain/associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "enum, agregado, construção, propriedade imutável e adição de classificação"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/domain/exceptions.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "RegraDeDominioViolada"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/application/associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "caso de uso e erros da criação da associação"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioCurriculo e RepositorioAssociacaoCurriculoVaga"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/application/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "CurriculoNaoEncontrado e verificação de ownership na edição"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "consulta pela chave composta, salvamento, flush e tradução de colisão"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "mapeamento da chave composta, linhas de classificação e conversões de/para Domain"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/api/itens_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "traduções 404/422 e indisponibilidade 503 em handlers existentes"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/api/cadastro_acesso.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "padrão 409 para conflito de negócio"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "composição dos routers; não há router de associação"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/tests/test_domain_associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: "invariantes de construção e adição; não há testes de remoção"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/tests/test_application_associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "ownership, ausência, duplicidade e persistência do caso de criação"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/tests/test_infrastructure_repositorio_associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "adapter, mapeadores, flush e transação sem commit no repository"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
    - path: src/backend/tests/test_persistencia_associacao_curriculo_vaga_integracao.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "round-trip, chave composta e rollback atômico em SQLite"
      content_state: working-tree
      revision: "ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories:
    - prompts/backend
    - prompts/requisitos
    - prompts/revisao
    - prompts/ambientes
    - prompts/frontend
    - prompts/templates
  confidence: high
  rationale: "A decisão é sobre Domain, Application, ports e persistência do backend; a análise anterior da #130 está em prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, architecture, security]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — Atualização de classificações da associação currículo-vaga (#132)

## Solicitação original

> Faça uma análise decisória exclusivamente para a issue #132:
>
> "Implementar atualização de classificações da associação currículo-vaga"
>
> NÃO implemente código.
> NÃO altere código existente.
> NÃO faça commit.
> NÃO faça push.
> NÃO redesenhe a arquitetura.
>
> CONTEXTO
>
> A issue #131 já definiu e implementou o Domain de associação currículo-vaga:
>
> - `AssociacaoCurriculoVaga`
> - `ClassificacaoAssociacao`
> - `VagaId`
> - regra `CANDIDATURA => INTERESSE`
> - classificações sem duplicação
> - associação exige pelo menos uma classificação
>
> A issue #130 está implementada no PR #541 e definiu:
>
> - uma única associação por `(curriculo_id, vaga_id)`;
> - chave composta `(curriculo_id, vaga_id)`;
> - criação duplicada rejeitada;
> - alterações posteriores das classificações pertencem à #132;
> - port/repository de associação já existe na implementação da #130.
>
> Use como contexto autoritativo da #130:
>
> `prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md`
>
> OBJETIVO
>
> Determinar exatamente o comportamento da atualização das classificações de uma associação já existente.
>
> Primeiro investigue no repositório:
>
> - requisitos funcionais;
> - matriz de testes;
> - prompts anteriores;
> - documentação;
> - Domain atual;
> - Application existente;
> - issue #132;
> - referências cruzadas às issues #130, #131 e #132.
>
> Consulte também:
>
> `gh issue view 132 --repo code-alchemists-br/sistema-curriculo`
>
> QUESTÕES QUE A ANÁLISE DEVE RESPONDER
>
> 1. Qual deve ser o comando/caso de uso de atualização?
>
> 2. A atualização opera:
>    - substituindo o conjunto completo de classificações;
>    - adicionando/removendo individualmente;
>    - ou existem comandos separados?
>
> 3. O que acontece ao adicionar uma classificação que já existe?
>
> 4. O que acontece ao remover uma classificação que não existe?
>
> 5. O que acontece ao tentar remover `INTERESSE` quando a associação contém `CANDIDATURA`?
>
> 6. A operação deve rejeitar qualquer estado final em que exista:
>    `CANDIDATURA` sem `INTERESSE`?
>
> 7. O que acontece ao tentar remover a última classificação da associação?
>
> 8. A associação pode permanecer sem classificações?
>    Confronte isso com o Domain da #131.
>
> 9. Como identificar a associação?
>    Considere a decisão da #130 de chave composta:
>    `(curriculo_id, vaga_id)`.
>
> 10. Como validar ownership?
>     O estudante deve poder alterar somente associações pertencentes aos
>     seus próprios currículos.
>
> 11. Qual comportamento para:
>     - currículo inexistente;
>     - currículo de outro usuário;
>     - associação inexistente?
>
> 12. Quais erros pertencem ao Domain e quais pertencem à Application?
>
> 13. Quais traduções HTTP são coerentes com os padrões existentes do projeto?
>
> 14. Quais mudanças são necessárias no port/repository criado pela #130?
>
> 15. É necessário carregar e reconstruir `AssociacaoCurriculoVaga` para
>     executar a alteração, evitando reproduzir regras de Domain na Application?
>
> 16. Como garantir persistência atômica das classificações?
>
> 17. Existe algum risco de concorrência relevante?
>
> IMPORTANTE
>
> Não invente requisitos silenciosamente.
>
> Para cada decisão:
>
> - diferencie evidência explícita;
> - inferência arquitetural;
> - decisão ainda ausente.
>
> Se alguma regra não estiver documentada, proponha a alternativa mais coerente
> com o Domain e a divisão das issues, mas marque claramente como decisão proposta.
>
> PREFERÊNCIAS DE MODELAGEM A SEREM AVALIADAS, NÃO ASSUMIDAS
>
> Considere especialmente se é mais coerente:
>
> - rejeitar remoção de `INTERESSE` enquanto houver `CANDIDATURA`;
> - rejeitar remoção da última classificação;
> - tratar adição de classificação já existente como idempotente;
> - tratar remoção de classificação inexistente como idempotente ou erro.
>
> Não aceite essas opções automaticamente. Confronte-as com os requisitos e padrões do projeto.
>
> ESCOPO
>
> A #132 NÃO deve:
>
> - criar novas associações;
> - alterar a unicidade definida na #130;
> - implementar busca de vagas;
> - integrar Grupo 2;
> - alterar autenticação;
> - implementar histórico das issues futuras;
> - remover a regra `CANDIDATURA => INTERESSE`.
>
> SAÍDA
>
> Gere uma nova análise versionada em `prompts/backend/`.
>
> A análise deve terminar com:
>
> - decisão recomendada;
> - regras de negócio consolidadas;
> - fluxo de Application;
> - mudanças necessárias em ports/repository;
> - erros esperados;
> - traduções HTTP;
> - testes necessários;
> - pendências reais, se existirem;
> - handoff claro para implementação.
>
> Não implemente código nesta etapa.

## Informações complementares

- A consulta atual à issue #132 retornou apenas o título “Implementar atualização de classificações da associação” e o texto genérico de fatia vertical/testes unitários. Não há critérios próprios para adição, remoção ou HTTP.
- A consulta atual à #130 e à #131 confirmou os títulos e o texto genérico de fatia vertical; a #131 está fechada e a #130 permanece aberta na consulta. O PR #541 está aberto no momento da consulta; sua descrição declara a chave composta, a rejeição de criação duplicada, a reutilização do Domain e o handoff de alterações posteriores para a #132. Portanto, não afirmo que #130/#541 estejam mergeadas.
- O checkout inspecionado estava no commit `ab08c2f7dd63c7ce7eccbb81f072cfc0248a11c0`, branch `feature/130-criacao-associacao-curriculo-vaga`. O código relevante lido corresponde à decisão da #130 registrada em v004. Arquivos `__pycache__` não rastreados foram observados e preservados; nenhum conteúdo de código foi alterado nesta análise.
- A análise trata uma issue nova da linhagem de decisões, não revisa nem substitui a decisão v004 da #130. A v004 é contexto autoritativo para a identidade e as fronteiras de #130; a v002 registra que as semânticas de remoção foram intencionalmente deixadas para #132.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem desta demanda | Não havia análise dedicada à #132 | Nova análise inicial v001 | A #132 recebeu escopo decisório próprio | Define proposta para atualização sem alterar as decisões da #130/#131 |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `code-alchemists-br/sistema-curriculo#132` | Primário | Prose | Documentation | GitHub issue | Título e corpo consultados via `gh issue view` | Externo; atual na consulta |
| Solicitação do usuário — análise exclusiva da #132 | Primário | Prose | Documentation | Mensagem | Contexto, questões e escopo completos, reproduzidos acima | Externo; atual |
| `code-alchemists-br/sistema-curriculo#130` | Apoio | Prose | Documentation | GitHub issue | Título e corpo | Externo; atual na consulta |
| `code-alchemists-br/sistema-curriculo#131` | Apoio | Prose | Documentation | GitHub issue | Título e corpo | Externo; atual na consulta |
| `code-alchemists-br/sistema-curriculo#541` | Apoio | Prose | Documentation | GitHub pull request | Descrição, decisões, handoff e estado | Externo; atual na consulta; aberto |
| `prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md` | Apoio | Prose | Documentation | Markdown | Solicitação, identidade composta, escopo negativo da #130 e handoff #132 | Working tree baseado em `ab08c2f`; v004 |
| `prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md` | Apoio | Prose | Documentation | Markdown | Decisão #131 e pendências/handoff sobre remoções | Working tree baseado em `ab08c2f`; v002 |
| `AGENTS.md` | Contexto | Prose | Prompt-instruction | Markdown | Restrições gerais de Nix, escopo e documentação | Working tree em `ab08c2f` |
| `src/backend/AGENTS.md` | Contexto | Prose | Prompt-instruction | Markdown | Clean Architecture, DDD, ports/repositories e testes | Working tree em `ab08c2f` |
| `prompts/README.md` | Contexto | Prose | Documentation | Markdown | Organização e finalidade dos prompts | Working tree em `ab08c2f` |
| `docs/requisitos_funcionais.md` | Primário | Prose | Documentation | Markdown | RF12, RN01–RN04, combinações e detalhamento pendente | Working tree em `ab08c2f` |
| `docs/matriz_testes.md` | Primário | Prose | Test | Markdown | CT-RF12-01..09 e CT-RF12-C01..C07 | Working tree em `ab08c2f` |
| `docs/requisitos_nao_funcionais.md` | Apoio | Prose | Documentation | Markdown | RNF04/RNF05 e pendências de autorização | Working tree em `ab08c2f` |
| `src/backend/domain/associacao_curriculo_vaga.py` | Apoio | Source-code | Production | Python | Arquivo completo | Working tree em `ab08c2f` |
| `src/backend/domain/exceptions.py` | Apoio | Source-code | Production | Python | `RegraDeDominioViolada` | Working tree em `ab08c2f` |
| `src/backend/application/associacao_curriculo_vaga.py` | Apoio | Source-code | Production | Python | Arquivo completo | Working tree em `ab08c2f` |
| `src/backend/application/ports.py` | Apoio | Source-code | Schema-contract | Python | `RepositorioCurriculo` e `RepositorioAssociacaoCurriculoVaga` | Working tree em `ab08c2f` |
| `src/backend/application/versao_curriculo.py` | Apoio | Source-code | Production | Python | Erro de currículo ausente/alheio e ownership na edição | Working tree em `ab08c2f` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_associacao_curriculo_vaga.py` | Apoio | Source-code | Production | Python | Arquivo completo | Working tree em `ab08c2f` |
| `src/backend/infrastructure/persistence/sqlalchemy/associacao_curriculo_vaga.py` | Apoio | Source-code | Production | Python | Mapping e conversões do agregado | Working tree em `ab08c2f` |
| `src/backend/api/itens_versao_curriculo.py` | Apoio | Source-code | Production | Python | Tradução de ausência, violação de domínio e executor indisponível | Working tree em `ab08c2f` |
| `src/backend/api/cadastro_acesso.py` | Apoio | Source-code | Production | Python | Tradução de conflito de negócio | Working tree em `ab08c2f` |
| `src/backend/api/factory.py` | Apoio | Source-code | Production | Python | Registro de routers; não há router de associação | Working tree em `ab08c2f` |
| `src/backend/tests/test_domain_associacao_curriculo_vaga.py` | Apoio | Source-code | Test | Python | Arquivo completo | Working tree em `ab08c2f` |
| `src/backend/tests/test_application_associacao_curriculo_vaga.py` | Apoio | Source-code | Test | Python | Ownership, ausência, criação e delegação de Domain | Working tree em `ab08c2f` |
| `src/backend/tests/test_infrastructure_repositorio_associacao_curriculo_vaga.py` | Apoio | Source-code | Test | Python | Contratos de consulta, salvamento, mapeamento e transação | Working tree em `ab08c2f` |
| `src/backend/tests/test_persistencia_associacao_curriculo_vaga_integracao.py` | Apoio | Source-code | Test | Python | Round-trip, unicidade e rollback usando SQLite | Working tree em `ab08c2f` |

### Limites da evidência dos artefatos

- A issue #132 não determina semântica de operação, idempotência, rota ou códigos HTTP.
- A matriz documenta dois efeitos de atualização: retirar somente candidatura mantendo interesse (CT-RF12-03) e adicionar compatibilidade sem perder candidatura/interesse (CT-RF12-04). Não especifica duplicidade de adição, remoção de item ausente, remoção de interesse com candidatura, remoção da última classificação nem atualização concorrente.
- A regra de autorização do RNF04 é geral; o método de autenticação e as regras específicas continuam pendentes nos requisitos. A descrição do PR #541 registra que a dependência comum de identidade autenticada ainda não estava disponível para expor a criação por HTTP.
- O mapping/repository de #130 foi lido, mas a composição de produção que inicia, confirma ou reverte uma `AsyncSession` não foi encontrada entre os arquivos inspecionados. O adapter de #130 faz `flush` e deixa commit/rollback ao boundary externo.
- Os testes de persistência inspecionados usam SQLite em memória. Não foi identificada evidência suficiente para afirmar qual banco é o alvo de produção nem se o locking pessimista é suportado/ativado nele.
- A observação de que o PR #541 está aberto é o estado no momento da consulta, não altera a instrução do usuário para tratar sua decisão técnica como autoridade de #130.

## Problema enriquecido

### Resultado desejado

Permitir que o proprietário do currículo modifique classificações de uma associação já existente pelo par natural `(curriculo_id, vaga_id)`, mantendo todas as invariantes do agregado #131, sem criar associação, duplicar regra na Application ou alterar a identidade/unicidade aprovada na #130.

### Atores e interesses

- Estudante autenticado: altera somente associações dos próprios currículos e espera que uma classificação repetida não provoque duplicidade.
- Application: verifica ownership, carrega a associação pelo par completo, solicita a transição ao agregado e persiste apenas uma mudança válida.
- Domain: protege conjunto fechado, unicidade, mínimo de uma classificação e `CANDIDATURA => INTERESSE`.
- Repository/adapter: reconstrói e persiste o agregado sem decidir regra de negócio e sem tomar posse de commit/rollback.
- API futura: deve derivar o ator de identidade confiável, traduzir falhas conhecidas e não expor entidades de Domain.

### Evidências e fatos observados

1. **Explícito — requisitos:** RF12 permite uma ou mais classificações entre interesse, compatibilidade e candidatura. RN02 aceita múltiplas simultâneas; RN03 exige interesse sempre que há candidatura e manda preservar essa condição em qualquer alteração.
2. **Explícito — matriz:** CT-RF12-03 exige remover candidatura e manter interesse. CT-RF12-04 exige adicionar compatibilidade preservando candidatura e interesse. CT-RF12-C01..C07 e RF12-06 mantêm o conjunto previsto e a proibição de associação vazia na criação.
3. **Explícito — pendência documental:** `requisitos_funcionais.md` ainda lista o comportamento da interface ao tentar retirar interesse com candidatura e o fluxo de alteração das associações como detalhamentos necessários. A v002 registra que remoção de interesse com candidatura e remoção da última classificação foram deliberadamente deixadas para #132.
4. **Explícito — #131 implementada:** `AssociacaoCurriculoVaga` aceita conjunto não vazio, enum fechado, evita duplicatas por conjunto, normaliza candidatura para incluir interesse e expõe a leitura como `frozenset`. Possui `adicionar_classificacao`, mas não possui operação de remoção.
5. **Explícito — #130:** v004 e descrição do PR definem uma associação por par e chave primária composta `(curriculo_id, vaga_id)`. A criação duplicada é conflito, não atualização. O agregado existente e seu port/repository devem ser reutilizados.
6. **Explícito — Application existente:** o caso de criação carrega currículo e mascara ausência/propriedade alheia como `CurriculoNaoEncontrado`; só então verifica o par. Essa sequência é um precedente para não revelar currículos de terceiros.
7. **Explícito — repository existente:** há `existe_por_par` e `salvar`; o adapter lê pela chave composta e persiste raiz/classificações num flush, sem commit. Mapping já contém `para_associacao` e conversões das linhas de classificação para o agregado.
8. **Explícito — transporte atual:** não existe router de associação registrado em `api/factory.py`. Handlers existentes traduzem recurso ausente para 404, `RegraDeDominioViolada` para 422, dependência indisponível para 503 e alguns conflitos de negócio para 409.
9. **Explícito — integridade/autorização:** RNF04 limita alteração a usuários autorizados; RNF05 exige estado candidatura-com-interesse. O método concreto de autenticação permanece pendente.
10. **Explícito — transação:** os testes atuais provam rollback atômico de raiz/classificações e o adapter não faz commit; ainda não provam o fluxo de atualização nem o limite transacional de produção.

### Hipóteses

- **Proposta:** uma ação unitária sobre uma classificação (adicionar ou remover uma) é suficiente para #132. Nenhum requisito pede um formulário de substituição em lote ou atomicidade entre várias ações distintas.
- **Proposta:** adicionar item já presente e remover item ausente são comandos idempotentes sem persistência se o estado não mudar. A estrutura de conjunto e o comportamento de adição do Domain já favorecem essa semântica; não há registro de eventos/histórico nesta issue.
- **Proposta:** remover interesse com candidatura ativa é rejeitado, em vez de remover candidatura implicitamente ou ignorar o pedido. Isso preserva escolha explícita e exige uma ordem clara: retirar candidatura primeiro.
- **Proposta:** a ausência do currículo e o currículo de outro ator continuam indistinguíveis externamente, como no caso existente.
- **Hipótese a validar:** o boundary externo pode manter um único transaction scope aberto desde a leitura com lock até a persistência, sem mudar a arquitetura ou atribuir transação ao repository.

### Perguntas em aberto

- **Decidido como proposta nesta análise:** adição/remoção individual, dois comandos explícitos, no-ops idempotentes, remoção inválida rejeitada e associação não vazia.
- **Pendente técnico real:** qual banco e nível de isolamento serão usados em produção e, portanto, qual mecanismo implementará serialização por associação. O repositório não revela o alvo de produção; SQLite não valida `SELECT FOR UPDATE`.
- **Pendente de produto/transporte, fora da entrega da #132 sem identidade autenticada:** método HTTP, formato da requisição/resposta e status de sucesso.
- Nenhuma outra decisão de domínio impede a implementação após aprovação desta proposta.

### Escopo

- Alterar apenas classificações de associação previamente persistida.
- Identificar cada associação pelo par `(curriculo_id, vaga_id)`.
- Verificar ownership pelo currículo antes de consultar a associação.
- Implementar invariantes no agregado Domain e orquestração por Application.
- Expandir a porta/repository existente da #130 para leitura e alteração do agregado existente.
- Preservar atomicidade e explicitar o risco de concorrência por chave.
- Testes unitários de Domain, Application e adapter; teste de persistência pertinente se a mudança no adapter o exigir.

### Fora do escopo

- Criar ou remover associações, mudar unicidade/chave composta, introduzir ID técnico ou converter criação duplicada em upsert.
- Acrescentar classificações, mudar `CANDIDATURA => INTERESSE`, integrar Grupo 2 ou buscar/validar vagas externas.
- Alterar autenticação, autorização compartilhada, credenciais, ou aceitar identidade de usuário confiada ao cliente HTTP.
- Adicionar endpoint HTTP antes de haver fonte confiável para a identidade solicitante; não adicionar histórico, eventos ou funcionalidades de issues futuras.
- Alterar arquitetura, ownership de transações, migration ou DER sem necessidade demonstrada por esta decisão.

### Critérios de sucesso

- Os casos CT-RF12-03 e CT-RF12-04 são atendidos usando o agregado existente e persistindo o resultado.
- Nenhuma mutação pode deixar candidatura sem interesse ou associação sem classificação.
- Currículo ausente/alheio não leva à consulta nem à alteração da associação; associação ausente é explícita.
- Identidade de consulta e escrita usa sempre os dois IDs da chave composta, sem criar outro par.
- No-op idempotente não produz escrita; erro de domínio não produz persistência.
- Uma falha de persistência não deixa subconjunto novo de classificações confirmado.
- Atualizações concorrentes da mesma associação não perdem silenciosamente uma mutação nem confirmam estado inválido.

## Restrições aplicáveis

- Clean Architecture/DDD: invariantes são protegidas por Domain; Application coordena ownership e repository; adapters não decidem regra; API não contém negócio.
- O agregado da #131 é a única autoridade para classificar e para validar a não-vacuidade; a Application não deve copiar essas condições.
- A identidade aprovada pela #130 é o par composto. O repository de criação permanece não-upsert.
- RN03 e RNF05 são restrições de estado final, não apenas regras de entrada.
- A autenticação e a identidade confiável não podem ser alteradas nesta issue. Sem principal confiável no backend, não se deve expor endpoint que confie em `usuario_id` enviado pelo cliente.
- O repository segue o padrão existente: sessão injetada, `flush`, sem commit/rollback próprio; transação precisa abranger a operação completa.
- Apenas os três valores existentes de `ClassificacaoAssociacao` são válidos.

## Classificação comentada

- `sphere: engineering`: a decisão define semântica e limites de implementação da fatia backend.
- `concerns: domain, architecture, security`: invariantes de classificação, responsabilidades Domain/Application/Repository e isolamento por ownership são as distinções principais.
- `decision_kind: design`, `scope: component`, `lifecycle: delivery`: é uma decisão local da associação no backend, destinada a uma entrega específica.
- Incerteza média: as invariantes e a chave estão bem sustentadas; idempotência, remoção conflitante e mecanismo de concorrência não foram definidos por produto.
- Risco médio: violar RN03 ou ownership afeta integridade/isolamento; o conjunto pequeno e o domínio existente tornam a recuperação simples se os testes cobrem os limites.

## Decisão de roteamento

Escolhido `prompts/backend`: o objeto é uma decisão de negócio implementada em Domain, Application e repository backend, e a análise autoritativa da #130 já está nessa pasta. `prompts/requisitos` é alternativa plausível para decisões de regra de produto, mas o pedido é uma decisão de contrato entre camadas; `revisao` não foi escolhido porque não é revisão de código. `ambientes`, `frontend` e `templates` não correspondem ao propósito. Não há `AGENTS.md` específico em `prompts/`; aplica-se o da raiz.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | Maximizada | Nunca persistir estado incompatível com RN03 ou sem classificações | É regra confirmada e invariante do agregado #131 |
| security | Priorizada | Não permitir mutação de associação de currículo alheio; não introduzir identidade HTTP não confiável | RNF04 e precedente de ocultar recurso alheio |
| reliability | Priorizada | Cada transição deve ser atômica e a concorrência não deve sobrescrever estado silenciosamente | A associação armazena classificações em linhas filhas |
| simplicity | Satisfeita | Alterar somente uma classificação por comando; sem batch, histórico ou abstração nova | Escopo da issue e cenários unitários atuais |
| modifiability | Satisfeita | Reutilizar port, repository, mapping e agregado existentes | A #132 é continuação da #130/#131, não novo modelo |
| user-value | Satisfeita | Resultado de cada ação é explícito e previsível | Evita que uma remoção apague outra escolha do estudante |

## Alternativas consideradas

### A — Substituir o conjunto completo

Um caso de uso recebe todas as classificações finais e persiste a substituição do conjunto. A operação seria transacional, mas a API precisa definir o que significa omitir uma classificação; o chamador teria de conhecer e enviar o estado completo. A matriz descreve ações pontuais, não substituição integral, e a reconstrução pelo construtor normaliza candidatura sem interesse em vez de distinguir uma remoção conflitante. Viável tecnicamente, sem evidência suficiente para preferi-la.

### B — Comandos separados de adição e remoção unitárias (recomendada)

`AdicionarClassificacaoAssociacaoCurriculoVaga` e `RemoverClassificacaoAssociacaoCurriculoVaga`, cada qual recebendo ator, `CurriculoId`, `VagaId` e uma classificação. Cada caso carrega o agregado atual, delega a mutação ao Domain e solicita a atualização pelo port. Corresponde às ações específicas já testadas e permite que o Domain rejeite uma remoção que viole dependência ou mínimo. Não se propõe batch.

### C — Um comando genérico com ação

Um único caso de uso recebe o par, classificação e ação (`adicionar`/`remover`). Pode compartilhar ownership/leitura/escrita sem duplicar o fluxo, mas adiciona uma operação genérica ao contrato e combina dois resultados de domínio num único comando. É viável se o time preferir um único executor; não é exigido pelos requisitos.

## Perfil de pagamento comparativo

Escala ordinal: `+2` melhora forte, `+1` melhora moderada, `0` neutro/desconhecido, `-1` piora moderada e `-2` piora forte. Os valores não são somados.

| Dimensão | Prioridade | A: substituir conjunto | B: comandos separados | C: comando genérico | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| correctness | Maximizada | +1 | +2 | +2 | Alta | B/C expressam a única mutação e permitem validar intenção no Domain; A exige interpretar conjunto omitido |
| user-value | Satisfeita | 0 | +2 | +1 | Média | CT-RF12-03/04 descrevem atos isolados e resultado específico |
| simplicity | Satisfeita | +1 | 0 | +1 | Média | A tem uma chamada, B tem duas intenções nomeadas, C compartilha orquestração mas inclui ação genérica |
| reliability | Priorizada | +1 | +1 | +1 | Média | Todas podem ser atômicas; nenhuma elimina sozinha o problema de concorrência |
| modifiability | Satisfeita | 0 | +1 | 0 | Média | B separa evolução de semântica de adição e remoção, ambas com invariantes distintas |
| security | Priorizada | 0 | 0 | 0 | Alta | Em todas, ownership e principal confiável são os mesmos requisitos |

## Histórico e decisão atual

### Decisão da versão anterior

Não havia análise dedicada da #132. A v002 limitou-se à #131 e deixou remoções fora do escopo: registrou que remover candidatura deve preservar interesse por CT-RF12-03, mas deixou pendentes remover interesse com candidatura e remover a última classificação. A v004 da #130 consolidou o par composto, manteve atualização posterior fora da criação e encaminhou explicitamente essas alterações para #132. Nenhuma dessas análises decidiu idempotência ou forma do comando.

### Decisão recomendada nesta versão

Adotar dois comandos de Application, um para adicionar e outro para remover uma classificação por chamada. Ambos recebem os dois identificadores do par e o ator; carregam o currículo, verificam ownership e só então carregam o agregado. O Domain mantém a mutação. Adicionar duplicata e remover ausente são no-ops idempotentes. Remover interesse com candidatura ativa ou remover a última classificação é rejeitado pelo Domain. Toda transição mantém `CANDIDATURA => INTERESSE`.

Esta recomendação é **proposta**, não fato já aprovado em requisito. A forma unitária é preferida por refletir CT-RF12-03/04 e manter a decisão de cada remoção no agregado sem adicionar API/batch não solicitados.

### Impacto da revisão

Inicial: não substitui nem reabre decisão anterior. Converte em proposta as semânticas de remoção que estavam pendentes, sem alterar o contrato de identidade da #130 nem a regra aprovada/implementada pela #131.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | maximized | Invariantes são validadas uma vez no agregado antes de persistir | RN03/RNF05 e Domain #131 |
| security | prioritized | Associação de terceiro não é consultada após currículo alheio/ausente | Padrão `CurriculoNaoEncontrado` na Application |
| reliability | prioritized | No-ops não escrevem; mudança válida é gravada como unidade transacional | Proposta compatível com conjunto, adapter e padrão de flush |
| user-value | prioritized | Uma remoção nunca elimina candidatura silenciosamente para permitir apagar interesse | Decisão proposta; evita efeito colateral além da ação solicitada |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| simplicity | No máximo uma classificação é alterada por comando; sem abstração nova de batch | Dois casos de uso explícitos e mutadores no agregado existente |
| modifiability | Nenhuma nova identidade ou categoria | Par composto e tipos atuais permanecem |
| interoperability | Sem alteração do contrato HTTP agora | A issue não muda autenticação nem adiciona rota |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | Candidatura sem interesse ou associação vazia pode ser confirmada | Alta | Estudante, consistência de dados e features que consumam associação |
| security | Usuário pode inferir ou alterar associação de currículo de outra pessoa | Alta | Proprietários de currículos |
| reliability | Escrita parcial ou atualização concorrente pode perder classificações | Média/alta | Estudante e consultas futuras |
| user-value | Remoção de interesse pode apagar candidatura sem consentimento explícito | Média | Estudante |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | Uma remoção solicitada pode ser recusada e exigir que o estudante retire candidatura primeiro | Rapidez/conveniência da ação | Aceitável: evita modificar escolha adicional de forma implícita |
| reliability | Leitura e escrita ocorrem numa transação e podem serializar alterações da mesma associação | Throughput para o mesmo par | Aceitável; cada agregado é independente |
| simplicity | A interface que selecionar várias mudanças pode fazer várias chamadas | Simplicidade da interação em lote | Aceitável até que exista requisito de atualização em lote |
| security | Endpoint não é exposto sem principal autenticado confiável | Disponibilidade imediata da feature por HTTP | Aceitável conforme handoff da #130 e restrição de não alterar autenticação |

## Riscos e efeitos de segunda ordem

- **Regra proposta pode ser rejeitada por produto:** RN03 exige preservar a dependência, mas não determina se apagar interesse deve recusar ou cascatar a remoção da candidatura. Rejeitar é a alternativa que não apaga silenciosamente outra decisão do estudante. Se produto aprovar cascata, atualizar requisitos e matriz antes de implementá-la.
- **No-op pode ocultar erro de interação:** idempotência evita falhas em repetição/retry e segue conjunto; se a interface precisar distinguir “já estava assim”, isso deve ser feedback de produto, não uma regra que crie duplicata.
- **Delete/reinsert de linhas sem uma única transação perde dados:** a atomicidade depende de o mesmo transaction scope abranger leitura, mutação, delete/insert/flush e commit externo.
- **Concorrência:** duas leituras do mesmo conjunto seguidas de substituições podem causar lost update; leitura seguida de gravação sem serialização também pode aceitar uma transição incompatível com uma concorrente. Recomenda-se lock da linha raiz identificada pela chave composta durante leitura, decisão e persistência, mantendo a transação aberta até o commit. Se o banco de produção não suportar lock de linha, a implementação deve usar controle otimista/conflict detection ou outra serialização equivalente; não aceitar last-write-wins silencioso. O mecanismo exato depende de banco/isolamento ainda não identificado.
- **Não confundir atualização e criação:** não usar `salvar` como upsert. Ausência de raiz no fluxo de atualização é erro; apenas o caso de criação pode inserir a associação.
- **Não acoplar transporte sem identidade confiável:** a rota existente não tem principal comum de sessão; usar `usuario_id` controlado pelo cliente contrariaria a autorização da RNF04.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Alterações unitárias bastam | Confirmação de que não há requisito de envio em lote | Validar escopo da issue/produto antes de API | Necessidade documentada de substituir todo o conjunto atomicamente |
| Remoção de interesse com candidatura é rejeitada | Aprovação de regra e atualização da matriz/documentação | Confirmar com responsável de produto antes de liberar comportamento | Decisão explícita de cascata ou de normalização silenciosa |
| Adição duplicada e remoção ausente são no-op | Testes demonstram idempotência e ausência de gravação | Testes unitários de Domain/Application | Necessidade de feedback/erro distinto explicitamente aprovada |
| Associação e classificações são atômicas | Falha em qualquer escrita deixa estado persistido anterior intacto | Teste de persistência com rollback, incluindo substituição das classificações | Commit parcial ou transaction boundary não cobre a operação inteira |
| Atualizações concorrentes não perdem estado | Banco, isolamento e comportamento de lock conhecidos | Teste concorrente no banco representativo e teste de conflito | Alvo não suporta lock ou há atualização silenciosa descartada |
| Não há rota HTTP nesta entrega | Existência de identidade confiável e autorização comum | Verificar contrato de sessão antes de futura exposição | Autenticação comum torna-se disponível sem alteração de política |

## Handoffs e atividades posteriores

### Implementação da #132 — após aprovação desta proposta

1. Acrescentar ao agregado métodos de remoção e testes de invariantes: no-op de ausência; proibir associação vazia e interesse ausente enquanto candidatura permanecer; preservar candidatura e compatibilidade em alterações não relacionadas.
2. Implementar dois comandos/casos de uso de Application (`Adicionar...` e `Remover...`) com ator, `CurriculoId`, `VagaId` e uma classificação. Reutilizar `RepositorioCurriculo.obter_por_id` e `CurriculoNaoEncontrado`; verificar ownership antes da busca da associação.
3. Adicionar erro Application específico para associação não encontrada; consultar por `(curriculo_id, vaga_id)`. Não distinguir externamente currículo inexistente de currículo alheio.
4. Estender `RepositorioAssociacaoCurriculoVaga` com leitura do agregado por par e atualização somente de classificações. Manter `existe_por_par` e `salvar` para criação; não alterar a semântica de duplicidade.
5. No adapter, usar o mapping existente para reconstruir `AssociacaoCurriculoVaga`, deixar o Domain aplicar regras, e persistir a alteração sem inserir/alterar a raiz nem confirmar a transação.
6. Definir com a composição externa um transaction scope que cubra leitura/mutação/escrita e rollback de falhas. Escolher serialização por chave depois de confirmar banco/isolamento; não aceitar lost updates.
7. Implementar e executar testes unitários de Domain, Application e adapter. Acrescentar teste de persistência da atualização e rollback integral. Atualizar a matriz de testes com as decisões aprovadas e cobrir ownership, associação ausente e os limites de remoção.
8. Manter a #132 sem rota HTTP enquanto identidade confiável não estiver disponível; não alterar autenticação nem encaminhar usuário controlado pelo cliente.

### Traduções HTTP coerentes se/ quando houver API autenticada

- Currículo ausente ou alheio: HTTP 404, usando a mensagem uniforme de `CurriculoNaoEncontrado`, como nas rotas de currículo existentes.
- Associação ausente para currículo próprio e par solicitado: HTTP 404, usando o novo erro Application específico; não traduzir em criação automática.
- Remoção que viola RN03 ou tenta retirar a última classificação: HTTP 422 para `RegraDeDominioViolada`, conforme handlers existentes.
- Classificação repetida/ausente idempotente: sucesso sem alteração; não 409 nem 404.
- Principal/executor indisponível: 503 apenas conforme padrão da rota; falhas reais de persistência devem continuar explícitas e não receber resposta de sucesso.
- HTTP 409 é coerente somente se um conflito concorrente for detectado e exposto deliberadamente. Não mapear erro de domínio ou item ausente para 409 sem novo contrato.
- Método, rota, corpo e status de sucesso permanecem fora desta decisão; só devem ser definidos quando houver identidade autenticada confiável.

### Pendências reais

- Aprovar com produto a proposta de rejeitar remoção de interesse sob candidatura, rejeitar última classificação e tratar adição/remoção repetida como no-op.
- Identificar banco de produção, nível de isolamento e composição transacional para escolher e validar o mecanismo de serialização concorrente. Isso não altera a recomendação de nunca perder mutações silenciosamente.
- API e sucesso HTTP permanecem pendentes da disponibilidade de identidade autenticada comum; não bloqueiam testes de Domain/Application/adapter desta issue.

## Síntese

### Decisão recomendada

Implementar alterações unitárias com comandos separados de adicionar/remover classificação, operando exclusivamente sobre associação existente identificada por `(curriculo_id, vaga_id)`. Adição de existente e remoção de ausente são no-ops idempotentes. Remover `INTERESSE` enquanto houver `CANDIDATURA` e remover a última classificação são rejeitados pelo Domain. Nenhum estado final inválido é persistido. Esta é uma proposta informada pela matriz e pelo Domain atual, não um requisito explícito; aprová-la e refletir as novas regras na matriz antes da implementação.

### Regras de negócio consolidadas

| Regra | Base |
|---|---|
| Alterar somente associação existente, identificada pelo par composto completo | #130/v004; decisão explícita |
| Uma classificação adicionada deve pertencer ao enum existente; a inclusão de candidatura acrescenta interesse pelo Domain | #131; comportamento existente |
| Adicionar classificação presente é idempotente e não duplica nem persiste novamente | Proposta baseada em conjunto/idempotência; ausente de requisito |
| Remover classificação ausente é idempotente e não persiste novamente | Proposta; ausente de requisito |
| Remover candidatura deixa interesse e as demais classificações intactas | CT-RF12-03; decisão explícita |
| Remover interesse enquanto candidatura existe é rejeitado; remover candidatura implicitamente não é permitido | Proposta para satisfazer RN03 sem efeito colateral não autorizado |
| Remover última classificação é rejeitado; associação vazia não é válida | Domínio #131 exige uma classificação; a transição de remoção é proposta |
| Não pode existir estado final com candidatura sem interesse | RN03/RNF05; regra explícita |
| Apenas proprietário do currículo pode atualizar; currículo inexistente/alheio é ocultado com o mesmo erro | RNF04 e padrão existente; aplicação arquitetural |
| Alteração e persistência das classificações são atômicas | RNF05, padrão transacional #130 e teste atual de rollback |

### Fluxo de Application

1. Receber `usuario_id` de fonte interna confiável, `curriculo_id`, `vaga_id` e classificação.
2. Obter o currículo pelo `RepositorioCurriculo`; se ausente ou alheio, lançar `CurriculoNaoEncontrado` antes de consultar associações.
3. Consultar `RepositorioAssociacaoCurriculoVaga` por `(curriculo_id, vaga_id)`; ausência lança `AssociacaoCurriculoVagaNaoEncontrada`.
4. Invocar no agregado a operação correspondente à intenção (adicionar/remover). Domain valida o valor e todas as invariantes.
5. Se o conjunto não mudou por operação idempotente, devolver o resultado sem chamada de persistência.
6. Caso tenha mudado, chamar a operação de atualização do port e aguardar seu flush. Propagar falhas; o boundary transacional externo deve confirmar a transação antes de apresentar a operação como sucesso ao chamador.

### Mudanças necessárias em ports/repository

- Manter a porta e o adapter da #130. Acrescentar consulta por chave composta que devolve `AssociacaoCurriculoVaga | None`, usando o conversor `para_associacao` existente.
- Acrescentar operação explícita para atualizar classificações de associação existente. Ela altera apenas as linhas dependentes; não cria raiz, não altera os IDs, não faz upsert e não executa commit/rollback.
- Reutilizar `(curriculo_id, vaga_id)` em todas as consultas, locks e escritas; manter constraint composta de classificação para evitar duplicatas.
- Garantir que leitura para mutação, transição de domínio e escrita pertençam à mesma transação; atualizar doubles e testes do contrato.
- Serializar transições concorrentes pela linha raiz/chave composta se o banco de produção suportar. Caso contrário, implementar controle de versão/conflict detection ou mecanismo equivalente após confirmar a tecnologia; não assumir que SQLite prova lock de produção.

### Erros esperados

| Camada | Erro | Ocorrência | Efeito |
|---|---|---|---|
| Domain | `RegraDeDominioViolada` | Classificação inválida; remoção da última; remoção de interesse enquanto candidatura continua | Rejeitar antes da persistência; não alterar estado persistido |
| Application | `CurriculoNaoEncontrado` existente | Currículo ausente ou não pertencente ao ator | Encerrar antes de consultar associação |
| Application | Novo `AssociacaoCurriculoVagaNaoEncontrada` | Par não existe após validar ownership | Não criar associação implicitamente |
| Application | Falha de port/persistência | Erro de I/O/flush/commit | Propagar; rollback pertence ao boundary transacional |
| No erro | No-op idempotente | Adição já existente ou remoção ausente | Sem duplicação e sem escrita |

### Testes necessários

- **Domain:** remoção de candidatura preserva interesse; remover interesse com candidatura falha sem mutar o agregado; remover a última falha sem mutar; remoção de item ausente e adição existente são idempotentes; adição de candidatura acrescenta interesse; mutações não descartam compatibilidade; nenhuma operação pública gera associação vazia ou candidatura sem interesse.
- **Application:** ator proprietário conclui e solicita update; currículo ausente/alheio falha sem consultar associação; associação ausente é específica; consulta usa ambos IDs; erro de Domain não solicita update; no-op não chama update; falha de port propaga.
- **Repository/adapter:** consulta compõe agregado com todas as linhas; atualização mantém raiz/chave; classificações sem duplicação; atualização não confirma transação; falha no flush é explícita; serialização/conflict behavior conforme banco escolhido.
- **Persistência:** classificações mudam como unidade e rollback restaura conjunto anterior em falha; constraints mantêm unicidade/FK. Executar integração no ambiente `tests` somente se esse teste for de integração; testes unitários de backend no ambiente `backend`.
- **Documentação:** ampliar `docs/matriz_testes.md` com casos não cobertos (repetições, ownership, associação ausente, remoções inválidas e atomicidade) depois de aprovação das propostas.

### Pendências reais

1. Aprovação de produto para as semânticas propostas de remoção e idempotência, hoje não definidas por requisitos/issue/matriz.
2. Identificação do banco/isolamento e do boundary transacional de produção para fechar como serializar operações concorrentes e testar essa garantia.
3. API e status de sucesso ficam para etapa com identidade autenticada comum; não se deve resolver isso por uma alteração de autenticação na #132.

### Handoff claro para implementação

Após aprovação das propostas de domínio, implementar somente Domain, Application, port/repository e testes pertinentes da #132. Reutilizar agregado e infraestrutura criados para #130; não criar associação, não alterar unicidade, não fazer integração externa e não expor endpoint sem principal confiável. Implementar remoção e erros no Domain/Application; carregar e reconstruir o agregado por chave composta; atualizar as linhas de classificação numa transação única; adicionar cobertura unitária e de persistência; confirmar o mecanismo de concorrência conforme banco real; documentar as novas decisões na matriz. Não alterar autenticação, histórico ou escopo das issues futuras.
