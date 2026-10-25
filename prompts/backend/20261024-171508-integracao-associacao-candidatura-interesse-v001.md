---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: v001
status: proposed
created_at: "2026-10-24T17:15:08-03:00"
lineage:
  mode: initial
  root: null
  supersedes: null
  change_type: initial
  secondary_change_types: []
  decision_impact: initial
subjects:
  kind: repository
  files:
    - &evidence
      path: src/backend/domain/associacao_curriculo_vaga.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: d1df2ab6f86fb899e1f4c59c9db11f9fc42f27ba
      availability: available
    - <<: *evidence
      path: src/backend/application/associacao_curriculo_vaga.py
    - <<: *evidence
      path: src/backend/application/consulta_associacao_curriculo_vaga.py
    - <<: *evidence
      path: src/backend/infrastructure/persistence/sqlalchemy/associacao_curriculo_vaga.py
    - <<: *evidence
      path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_associacao_curriculo_vaga.py
    - <<: *evidence
      path: src/backend/api/factory.py
    - <<: *evidence
      path: src/backend/main.py
    - <<: *evidence
      path: src/backend/tests/fixtures/credenciais_sessao.py
      function: test
      analysis_scope: selected-section
      locator: imports; verificar_revisoes_unicas; BancoCredenciaisSessao até preparar
    - <<: *evidence
      path: src/backend/tests/fixtures/curriculos_autenticados_integracao.py
      function: test
    - <<: *evidence
      path: src/backend/tests/integracao_repositorio_associacao_curriculo_vaga.py
      function: test
    - <<: *evidence
      path: src/backend/tests/test_persistencia_associacao_curriculo_vaga_integracao.py
      function: test
    - <<: *evidence
      path: docs/requisitos_funcionais.md
      representation: prose
      function: schema-contract
      format: Markdown
      analysis_scope: selected-section
      locator: RF12; RN01–RN07; pendências
    - <<: *evidence
      path: docs/matriz_testes.md
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: propósito; RF12; CT-RF12-01–15 e C01–C07
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/ambientes, prompts/revisao]
  confidence: high
  rationale: "Especificação de integração de componentes backend; precedentes de testes e associação na mesma pasta."
classification:
  sphere: engineering
  concerns: [integration, domain, security]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: medium
---

# Análise de decisão — integração de associação com candidatura e interesse implícito

## Solicitação original

Transcrição literal da demanda recebida, sem converter suas instruções em critérios de produto:

> $decision-analysis-v4 Implementar "Criar cenário de integração para associação com candidatura e interesse implícito.". O resultado esperado é um teste de integração executável, com **cenários positivos e negativos**. Antes de decidir o que ele contém, descubra o que o projeto define e implementa sobre associação (entre currículo e vaga, ou outra), candidatura e interesse, o que significa "interesse implícito" neste projeto e quais componentes o teste pode usar. Esta é uma análise nova, iniciada do zero.
>
> ## Regra principal: não presumir
>
> Todo fato deve vir de um artefato lido (histórico Git, código, testes, migrations, documentação de segurança, requisitos, matrizes de teste, configuração de ambiente), com o caminho indicado. O que nenhum artefato definir deve ser registrado como lacuna, nunca como fato.
>
> - Separe em seções distintas: **(a) fatos encontrados**, com caminho e trecho; **(b) lacunas**, ou seja, o que nenhum artefato define; **(c) recomendações**, que são suas, com justificativa.
> - Para cada lacuna, apresente as opções viáveis, recomende uma e marque se depende de decisão de produto ou se pode ser tomada tecnicamente com base no que existe.
> - Quando artefatos divergirem (código, documentação, requisitos, testes), aponte a divergência, diga qual fonte parece mais confiável e por quê, sem escolher em silêncio.
> - Não transponha para este tema regras de outros recursos (perfil, formação, projeto, currículo, documentos) sem que um artefato sobre associação, candidatura ou interesse as sustente.
>
> ## Ponto de partida
>
> Parta exclusivamente do estado atual desta branch, criada a partir da `dev`. Não presuma a existência de nenhuma associação, candidatura, noção de interesse, teste, fixture, cenário ou análise sobre o tema. Descubra por inspeção o que existe: o que existir entra como fato (e deve ter a cobertura avaliada), o que não existir entra como lacuna. **Inventarie as fixtures e os harnesses de teste de integração que de fato existem na base** e não presuma o nome nem a existência de nenhum.
>
> ## Texto do card
>
> Somente o título foi fornecido: "Criar cenário de integração para associação com candidatura e interesse implícito.". Não há descrição nem critérios de aceite. **Não invente critérios.** Derive o que for possível do título e dos artefatos, marque a origem de cada critério como "inferido" e liste exatamente o que precisa ser fornecido para fechar cada lacuna. O título e o pedido do usuário exigem **cenários positivos e negativos**: isso é requisito da entrega.
>
> ## Fontes a analisar
>
> 1. **Histórico Git local.** A CLI do GitHub e a rede podem não estar disponíveis; **não dependa delas**. Localize por inspeção (merges "Merge pull request #N", squashes com sufixo "(#N)", mensagens, nomes de branch e histórico dos arquivos) os trabalhos ligados a associação, candidatura, interesse e vaga. Número de card não é número de PR: não infira a ligação apenas pela coincidência de números, e registre como identificou cada trabalho.
> 2. **Documentação pertinente**, localizada por busca (não presumida): requisitos funcionais e não funcionais, requisitos de segurança e privacidade, o DER, matrizes de rastreabilidade e de teste em `docs/`, e análises anteriores em `prompts/`. Busque por termos como associação, candidatura, candidatar, interesse, implícito, vaga e currículo, e registre os termos usados e o que cada busca retornou, inclusive resultados vazios.
> 3. **Código atual relacionado**: entidades, value objects, casos de uso, portas, repositórios, rotas e handlers, DTOs, migrations (inclusive constraints, chaves estrangeiras e unicidade), middleware de autenticação, composição da aplicação (`main.py` e `factory.py`) e testes existentes, unitários e integrados, que toquem esses temas.
>
> ## O que levantar
>
> - **Os conceitos e como se relacionam.** Defina, **somente com base nos artefatos**, o que são "associação", "candidatura" e "interesse" neste projeto: se são entidades, estados, campos ou eventos; o que os liga (por exemplo vaga, currículo e pessoa); se candidatura e associação são o mesmo conceito ou conceitos distintos; e onde cada um é definido (documento) e onde é apenas implementado (código). Se algum dos três conceitos não existir, registre como lacuna.
> - **O que "interesse implícito" significa.** Descubra se há qualquer artefato que defina interesse implícito (derivado de uma ação, como a associação ou a candidatura, em vez de declarado explicitamente), se ele é **persistido** ou **calculado na leitura**, qual ação o gera, se aparece em alguma resposta da API, se há regra de privacidade ou consentimento sobre ele, e se há leitores dele. Se o termo não estiver definido, trate como **lacuna de produto** com as interpretações viáveis e uma recomendação, e diga qual parte do cenário depende da resposta.
> - **A vaga.** Descubra de onde vêm as vagas no backend (tabela própria, fonte externa ou nenhuma) e como uma associação referencia uma vaga (chave estrangeira, identificador solto, cópia de dados). Isso decide o que um teste de banco consegue exercitar.
> - **O contrato por operação.** Para cada operação que cria, consulta, altera ou remove associação, candidatura ou interesse: método, caminho, de onde vem o identificador da pessoa (caminho, corpo, sessão), caso de uso, repositório, formato de entrada e de saída, status de sucesso, **e o status de cada falha tratada** (sem sessão, sessão inválida, recurso inexistente, recurso de outra pessoa, entrada inválida, duplicidade, conta excluída). Registre a **precedência dos erros entre camadas** (middleware, validação do framework, handler e caso de uso), para o teste não misturar oráculos de composições diferentes. Separe o que está **definido em documento** do que está **só implementado**.
> - **Regras de integridade e invariantes.** Unicidade, chaves estrangeiras, o que acontece com a associação quando a vaga, o currículo ou a conta são excluídos, e qualquer limite definido. Registre apenas o que estiver definido ou implementado; o restante é lacuna, sem inventar o comportamento esperado.
> - **A composição real.** Como a aplicação que sobe (`main.py`, `factory.py`) instala a autenticação e os casos de uso desse tema, e se estão realmente ligados na composição de produção. **Não presuma o estado**: leia o código atual e registre o que a composição faz, e o que isso implica para o que o cenário consegue provar. Recomende como o teste deve compor a aplicação e qual limite declarar sobre a composição de produção.
> - **Cobertura existente:** o que os testes atuais já cobrem sobre o tema, em que nível (unitário com doubles ou integração com banco real), e o que falta, para o cenário novo não repetir cobertura sem necessidade.
> - **O que "cenário de integração" significa no projeto.** Procure em `docs/` e `prompts/` a definição, as convenções e os precedentes, e o formato esperado (fluxo encadeado ou casos independentes). Dado o requisito de cenários positivos e negativos, avalie a estrutura mais adequada (por exemplo um fluxo positivo encadeado e uma matriz de negativas independentes, cada uma com controle positivo) e justifique.
> - **O ambiente de testes integrados:** o que `nix develop .#tests` oferece hoje, como os testes integrados existentes são organizados e executados, como o banco é preparado (SQLite e, se houver, PostgreSQL) e como a autenticação é montada nos testes existentes.
> - **Bloqueios de execução preexistentes:** verifique por inspeção e registre, **sem tratá-los como escopo e sem corrigi-los**, o estado da cadeia de migrations do Alembic (revisões duplicadas ou múltiplas heads), das dependências do ambiente `.#tests` e de qualquer rota do tema que não esteja implementada ou composta. Execute apenas comandos de leitura e um **baseline informativo** da suíte do backend, registrando comando, ambiente, resultado e contagens, sem alterar nada.
>
> ## Escopo
>
> Definir o **cenário de integração executável** sobre associação com candidatura e interesse implícito, com componentes reais e banco migrado, cobrindo **cenários positivos e negativos**: etapas, dados, verificações, resultados esperados, fixtures, forma de execução e limites do que prova.
>
> Fora do escopo: alterar rotas, casos de uso, persistência, middleware, contrato ou composição; corrigir defeitos de back-end encontrados (registre-os como achados); definir ou criar a política de interesse; ativar autenticação na composição de produção; front-end; novas regras de negócio ou de segurança; alterações permanentes de ambiente.
>
> ## Instruções
>
> - Para cada decisão que os artefatos não resolverem, recomende uma opção com justificativa e marque se depende de produto.
> - **Cobertura positiva e negativa obrigatória.** Derive os cenários dos documentos e do código. Cada cenário deve ter objetivo, pré-condições, passos, resultado esperado, a fonte que o sustenta, a origem do critério (definido ou inferido) e a camada (HTTP, caso de uso, banco). Considere **apenas se algum artefato os definir ou implementar**:
>   - **Positivos:** criar a associação válida com sessão válida; registrar a candidatura; o interesse implícito tal como definido (e o que o gera); consulta ou listagem refletindo o estado persistido, relido em outra sessão de banco; repetição ou idempotência, se definida; remoção ou desassociação, se existir; efeito sobre o interesse quando a associação ou a candidatura muda.
>   - **Negativos:** sem sessão; sessão inválida, expirada ou revogada; currículo ou vaga inexistente; currículo de outra pessoa; associação de outra pessoa; entrada inválida (tipo, formato, identificador malformado); duplicidade; candidatura sem associação ou interesse sem candidatura, se o contrato definir pré-condição; conta excluída; método não permitido; e qualquer outra recusa que o código implemente.
>   - Todo cenário negativo deve ter um **controle positivo** no mesmo recurso, para provar que a recusa vem da regra e não de uma rota que sempre falha, e deve verificar que o **estado persistido não mudou** (por leitura em outra sessão de banco) e que o caso de uso não foi chamado quando a recusa ocorre antes dele. O que não estiver definido entra como lacuna, e a análise deve dizer se o cenário registra o comportamento atual como caracterização (rotulada como tal) ou aguarda decisão. Não force status que o código não produz.
> - Defina a estrutura: nomes e localização dos arquivos conforme a convenção, reaproveitamento das fixtures **que de fato existem na base** (verifique, não presuma), preparação do banco (migrations aplicadas até o head, nunca `create_all`), isolamento entre testes, dependências do ambiente e como os testes que dependem de recurso ausente são ignorados com motivo explícito, sem gerar erro quando o ambiente não os suporta. Diferencie claramente, no contrato dos testes, fluxo positivo e matriz negativa, e diga se devem ser métodos separados.
> - **Honestidade da prova.** Um teste ignorado não é prova. Diga como o resultado distingue "executado e aprovado" de "ignorado por ambiente", e o que o cenário não prova (por exemplo a composição de produção, concorrência e corridas de unicidade, o comportamento sob falha de banco, PostgreSQL, e qualquer política de interesse que não esteja definida).
> - Registre achados de back-end (divergências entre código, documentação e contrato, comportamentos não definidos, riscos de segurança ou de privacidade, inclusive o tratamento de dados de interesse) em seção própria, sem corrigi-los.
> - Indique a divisão de trabalho. **Leia o contrato de escopo e o teste de adequação da skill `integration-system-testing-v1` e confirme, com evidência, se esta fatia é elegível**; se não for, registre como lacuna de processo e indique o executor adequado. Especifique nomes de arquivos, ambientes e comandos, para o executor não precisar inventá-los. Diga também se o resultado precisa de um registro em documento ou se basta o texto do PR, e recomende o mínimo, de acordo com os precedentes do projeto.
> - **Alterações temporárias de ambiente.** Registre que, para executar o cenário, o executor poderá aplicar alterações temporárias em `nix/tests.nix` (somente se o ambiente não oferecer Python do backend e o driver SQLite assíncrono) e, se a cadeia do Alembic estiver com revisões duplicadas ou múltiplas heads, uma **linearização temporária** das migrations. Proponha o plano concreto, arquivo por arquivo (somente identificadores e arestas, sem alterar DDL), com verificação de ausência de ciclo e de uma única head sem warnings. Ambas devem ser revertidas com `git restore` por caminhos explícitos (nunca `git restore .`) ao final, com os diffs completos copiados para o resumo e `git status --short` sem nenhum arquivo em `nix/`, `flake.nix`, `flake.lock` ou `alembic/versions/`. Se já houver mudanças do usuário nesses caminhos, a execução não deve restaurá-las: deve parar e informar. Recomende executar primeiro no estado original, para registrar skips e bloqueios, e depois sob o experimento temporário, deixando claro que o segundo prova os componentes sob o grafo temporário e não a cadeia original.
> - Defina o roteamento do artefato de análise (pasta em `prompts/`) conforme a organização existente.
> - Registre na validação: a execução do cenário em `nix develop .#tests`; a execução informativa da suíte completa em `nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src`, que não pode gerar erros novos em relação ao baseline observado (registre o baseline real); e o gate de lint do CI ao final de cada execução: `nix develop .#quality --command ruff check src/backend` (se falhar por I001, corrigir com `nix develop .#quality --command ruff check --select I --fix <arquivos-apontados>` e repetir o gate completo).
> - Não implemente nada.

## Informações complementares

O usuário forneceu a skill `decision-analysis-v4` com caminho `.agents/skills/decision-analysis-v4/SKILL.md`, cujo conteúdo foi lido junto das referências obrigatórias. Forneceu também as regras gerais `AGENTS.md` e o contexto de execução. Nenhuma decisão posterior de produto foi recebida. A declaração de que a branch foi criada de `dev` é do usuário; a inspeção confirma branch `test-integracao-candidatura-interesse`, HEAD `d1df2ab6f86fb899e1f4c59c9db11f9fc42f27ba` e árvore inicialmente limpa. Esta é uma linhagem nova para o cenário, não revisão das análises dos recursos.

## Mudanças desde a versão anterior

Nenhum identificado — modo `initial`.

## Artefatos analisados

O frontmatter identifica os principais; o inventário abaixo também registra os apoios efetivamente consultados. Salvo indicação explícita, todos são conteúdo `working-tree`, disponível, baseado no HEAD acima, sem modificações locais; não foi feita consulta remota. Para linhas de tabela com vários caminhos, cada caminho recebe individualmente a classificação e o recorte informados.

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `AGENTS.md`; `src/backend/AGENTS.md` | context | prose | prompt-instruction | Markdown | integral | working-tree/HEAD |
| `.agents/skills/decision-analysis-v4/SKILL.md`; `references/classification-taxonomy.md`; `references/output-schema.md`; `references/output-routing.md`; `references/artifact-classification.md` (relativos à skill) | context | prose | prompt-instruction | Markdown | integral | working-tree |
| `.agents/skills/integration-system-testing-v1/SKILL.md`; `references/analysis-input-contract.md`; `references/test-scope-boundary.md`; `references/test-fit-check.md` (relativos à skill) | context | prose | prompt-instruction | Markdown | integral | working-tree |
| `docs/configuracao-ambiente.md`; `prompts/README.md` | supporting | prose | documentation | Markdown | integral | working-tree/HEAD |
| `docs/requisitos_funcionais.md`; `docs/requisitos_nao_funcionais.md`; `docs/matriz_testes.md`; `docs/matriz_rastreabilidade.md` | supporting | prose | schema-contract | Markdown | resultados de busca, RF12/RF15, RN01–07, RNF04/05 e CT-RF12 | working-tree/HEAD |
| `docs/requisitos-seguranca.md` | supporting | prose | documentation | Markdown | busca; §§4.1, 4.2, 4.10; pendências | working-tree/HEAD |
| `docs/Arquitetura/ADR-002-autenticacao-autorizacao-propriedade.md` | supporting | prose | documentation | Markdown | integral | working-tree/HEAD |
| `docs/contrato-credenciais-sessao.md` | supporting | prose | schema-contract | Markdown | busca; persistência, cookie e identidade | working-tree/HEAD |
| `docs/modelagem_der.md` | supporting | diagram-model | schema-contract | Mermaid/Markdown | relações e blocos de associação e classificações | working-tree/HEAD |
| `docs/contratos_integracao_grupo2.md`; `docs/contrato-busca-vagas.md` | supporting | prose | schema-contract | Markdown | resultados de busca: sugestões, IDs e ausência de candidatura externa | working-tree/HEAD |
| `prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md` | supporting | prose | documentation | Markdown | fatos, escopo, critérios, decisão e integração | working-tree/HEAD |
| `prompts/backend/20261018-210535-atualizacao-classificacoes-associacao-curriculo-vaga-v002.md` | supporting | prose | documentation | Markdown | dimensões, alternativas e decisão; linhas 700–760 | working-tree/HEAD |
| `prompts/backend/20261019-191822-consulta-paginada-associacoes-estudante-v002.md` | supporting | prose | documentation | Markdown | busca: teste SQLite, ambiente, decisão e limites | working-tree/HEAD |
| `src/backend/domain/associacao_curriculo_vaga.py` | primary | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/domain/value_objects.py` | supporting | source-code | production | Python | `CurriculoId`, `VagaId` | working-tree/HEAD |
| `src/backend/application/associacao_curriculo_vaga.py`; `src/backend/application/consulta_associacao_curriculo_vaga.py` | primary | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/application/ports.py` | supporting | source-code | schema-contract | Python | localização dos ports e DTOs; contratos confirmados pelos consumidores/adapters | working-tree/HEAD |
| `src/backend/application/consulta_vagas.py` | supporting | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/api/factory.py`; `src/backend/main.py`; `src/backend/api/middleware_autenticacao.py`; `src/backend/api/vagas.py` | primary | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/infrastructure/security/autenticador_sessao.py`; `src/backend/infrastructure/persistence/sqlalchemy/repositorio_sessao.py` | supporting | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/infrastructure/persistence/sqlalchemy/associacao_curriculo_vaga.py`; `src/backend/infrastructure/persistence/sqlalchemy/repositorio_associacao_curriculo_vaga.py`; `src/backend/infrastructure/persistence/sqlalchemy/metadata.py` | primary | source-code | production | Python | integral | working-tree/HEAD |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py`; `src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py` | supporting | source-code | production | Python | exclusão física de versão; atribuição de deleted_at de conta | working-tree/HEAD |
| `alembic.ini`; `src/backend/infrastructure/persistence/alembic/env.py` | supporting | source-code | configuration | INI/Python | integral | working-tree/HEAD |
| `src/backend/infrastructure/persistence/alembic/versions/*.py` | supporting | source-code | schema-contract | Python | identificadores/arestas de todos os 20 arquivos; DDL integral da associação, usuários, currículos, contato e consulta de estudante | working-tree/HEAD; arquivos discriminados na tabela do grafo |
| `src/backend/tests/fixtures/curriculos_autenticados_integracao.py` | supporting | source-code | test | Python | integral | working-tree/HEAD |
| `src/backend/tests/fixtures/credenciais_sessao.py` | supporting | source-code | test | Python | imports, constantes, preflight, BancoCredenciaisSessao até preparar, assinaturas restantes | working-tree/HEAD |
| `src/backend/tests/fixtures/perfis_integracao.py`; `src/backend/tests/fixtures/massa_teste_curriculos.py`; `src/backend/tests/fixtures/curriculo_exportacao.py` | supporting | source-code | data-fixture | Python | docstrings, imports, classes e entrada de seed/leitura | working-tree/HEAD |
| `src/backend/tests/fixtures/__init__.py` | context | source-code | test | Python | metadata-only: existência | working-tree/HEAD |
| `src/backend/tests/test_domain_associacao_curriculo_vaga.py`; `src/backend/tests/test_application_associacao_curriculo_vaga.py`; `src/backend/tests/test_application_consulta_associacao_curriculo_vaga.py`; `src/backend/tests/test_infrastructure_repositorio_associacao_curriculo_vaga.py` | supporting | source-code | test | Python | nomes dos testes, doubles/imports e docstring do adapter | working-tree/HEAD |
| `src/backend/tests/test_persistencia_associacao_curriculo_vaga_integracao.py`; `src/backend/tests/integracao_repositorio_associacao_curriculo_vaga.py` | primary | source-code | test | Python | integral | working-tree/HEAD |
| `src/backend/tests/test_integracao*.py` | supporting | source-code | test | Python | inventário de classes, helpers, skips, preparação; não leitura integral de todos | working-tree/HEAD |
| `nix/tests.nix`; `nix/backend.nix`; `nix/backend-python-packages.nix`; `flake.nix`; `.github/workflows/ci.yml` | supporting | source-code | configuration | Nix/YAML | integral dos Nix; jobs de lint/backend/integração do CI | working-tree/HEAD |
| histórico Git local de `HEAD` | supporting | structured-data | documentation | commits/diffs de metadados | mensagens, merges, stat dos trabalhos e histórico dos arquivos | commit/HEAD |

### Limites da evidência dos artefatos

Não houve uso de GitHub, consulta de cards, PostgreSQL, execução do novo cenário ou experimento temporário. Os testes citados por nomes evidenciam intenção/cobertura declarada, não garantem aprovação individual nesta análise. O baseline global aprovado não executou os 33 testes ignorados. A busca inicial no histórico `--all` encontrou `231eaf6` e `docs/politica_exclusao.md`, mas esse arquivo **não existe na árvore atual** e o commit não apareceu no histórico restrito a HEAD: excluído como fonte normativa desta branch. Tentativas de caminhos presumidos `docs/politica-exclusao-recursos.md`, `docs/politica_exclusao_recursos.md` e `src/backend/api/associacoes_curriculo_vaga.py` retornaram ausentes; nenhuma conclusão foi baseada em seu suposto conteúdo.

A análise de atualização foi consultada por glob `prompts/backend/*atualizacao-classificacoes*v002.md` e seu caminho completo foi confirmado pela listagem. A evidência usada é o recorte que declara «Não criar endpoint nem definir método, rota, request, response ou status de sucesso nesta análise», não um contrato HTTP.

## Problema enriquecido

### Resultado desejado

Especificar testes executáveis que integrem Application, Domain, adapters SQLAlchemy e SQLite migrado, provando que candidatura inclui interesse durável e que recusas existentes preservam o estado. Cobertura positiva e negativa é **definida pelo pedido**; a seleção abaixo é **inferida dos artefatos**, não critério de aceite atribuído ao card.

### Atores e interesses

Estudante proprietário e outro estudante: RN07 e RNF04 exigem isolamento. Executor: precisa de contratos verificáveis e banco descartável. Revisão de produto: precisa decidir somente lacunas de política, sem reinterpretar a RN03 já definida.

### (a) Fatos encontrados — caminhos e trechos

| ID | Fonte e trecho observado | Consequência verificável |
|---|---|---|
| F01 | `docs/requisitos_funcionais.md`, RF12: «crie manualmente associações entre seus currículos e vagas» e «armazenar essas associações e suas classificações em banco de dados» | Associação é relação currículo–vaga persistente, por ação do estudante. |
| F02 | Mesmo documento, RN02/RN03: «mais de uma classificação simultaneamente»; «Candidatura implica interesse»; «preservada em qualquer alteração» | Candidatura/interesse são classificações da mesma associação, não entidades independentes nem envio externo. |
| F03 | Mesmo documento: «A inclusão de interesse como consequência de uma candidatura manual atende à RN03» e «não constitui criação automática de uma associação» | Há definição semântica suficiente para interesse derivado de candidatura; o rótulo “implícito” não cria outra política. |
| F04 | Mesmo documento, RN05–07: adição/remoção idempotentes; «Remover candidatura preserva interesse»; identidade «da sessão autenticada» | Transições e ownership têm regra documental explícita sobre associação. |
| F05 | `domain/associacao_curriculo_vaga.py`: enum `INTERESSE`, `COMPATIBILIDADE`, `CANDIDATURA`; construtor e `adicionar_classificacao` acrescentam interesse | Implementação é agregado com conjunto não vazio; classificação livre é recusada, duplicatas de classificação são eliminadas. |
| F06 | Mesmo arquivo, `remover_classificacao`: «Não é possível remover interesse enquanto houver candidatura»; última classificação também recusada | Há negativos de domínio exercitáveis através da Application real. |
| F07 | `application/associacao_curriculo_vaga.py`: currículo ausente/alheio gera `CurriculoNaoEncontrado`; par existente gera `AssociacaoCurriculoVagaJaExiste` antes da construção | Ordem de validação de criação é ownership → duplicidade → agregado → salvar. |
| F08 | Mesmo arquivo, `_obter_associacao_do_proprietario`: ownership antes de `obter_para_atualizacao`; ausência gera `AssociacaoCurriculoVagaNaoEncontrada` | Atualização não cria associação e não lê associação alheia antes da guarda. |
| F09 | `infrastructure/persistence/sqlalchemy/associacao_curriculo_vaga.py`: PK `(curriculo_id, vaga_id)`; `vaga_id: Text`; FK somente para currículo; classes em tabela dependente | Não há tabela de vaga nem validação de existência externa nessa persistência. O teste usa referência textual sintética. |
| F10 | Mesmo mapping e migration `20261017_0004_criar_associacoes_curriculo_vaga.py`: PK de classificação inclui valor; FK composta `ondelete="CASCADE"`; nenhum CHECK de enum/dependência/vazio | Banco garante PK/FK, mas não sozinho candidatura ⇒ interesse ou conjunto não vazio. |
| F11 | `repositorio_associacao_curriculo_vaga.py`: salva com `flush`; atualização faz delete/inserts sob transação externa; leitura usa `para_associacao` | Interesse é persistido como linha normalizada, **e** reconstrução também normaliza; só ler agregado pode esconder linha ausente. É obrigatório conferir SQL bruto. |
| F12 | Mesmo adapter, `listar_por_usuario`: join currículo, filtro `usuario_id`, ordenação pelo par, offset/limit; `obter_para_atualizacao` usa `with_for_update()` | Há leitores internos do interesse; não há leitor HTTP deste tema. SQLite não prova lock PostgreSQL. |
| F13 | `domain/value_objects.py`, `VagaId`: «sem impor formato»; valida somente `isinstance(..., str)` | Vaga inexistente/ID vazio não tem recusa de existência/formato; tipo não textual é recusado. `CurriculoId` requer UUID já construído. |
| F14 | `api/factory.py`: instala middleware somente quando `autenticador_sessao is not None`; inclui vagas, não associação | Nenhum executor/DTO/handler de associação é composto. Busca `associacao|classificac` em `api/` e `main.py` retornou vazia. |
| F15 | `main.py`: `create_app(autenticador_sessao=AutenticadorSessaoIndisponivel(), ...)` | Produção **instala** autenticação, porém indisponível; não se deve dizer que não há middleware. Não compõe repositórios/casos de associação. Engine serve readiness. |
| F16 | `api/middleware_autenticacao.py`: cookie ausente ou autenticador retorna None → `401`; comparação de usuário em caminhos reconhecidos → `403` | Ordem é middleware antes de routing/validação; não define status de uma operação de associação inexistente. |
| F17 | `repositorio_sessao.py`: expiração maior que instante, revogação nula, usuário `deleted_at is None` | Conta logicamente excluída invalida sessão; essa guarda não existe nos casos de associação chamados diretamente. |
| F18 | `application/consulta_vagas.py`: delega a `BuscadorVagas`; `docs/contratos_integracao_grupo2.md`: «sugestões de vagas» | Busca externa é separada da associação manual; não é necessário consultar rede para testar a relação. |
| F19 | `docs/requisitos_funcionais.md`: candidatura «não define, por si só» envio externo; CT-RF12-08 veda envio | Construção do cenário não inclui submissão a provedor. Ports do caso de criação são só currículo/associação. |
| F20 | `docs/requisitos_nao_funcionais.md`, RNF04/05: proteção de associações, referências válidas, candidatura com interesse | Segurança/integridade são específicas do tema; não se importam políticas de documentos/formações. |

Nos caminhos abreviados F05–F18, os prefixos completos constam no inventário; Domain/Application/API são sob `src/backend/`.

#### Registro de busca e descoberta

Foi usada busca `rg -n -i 'associa|candidat|interesse|implícit|implicit' docs prompts`, seguida por recortes, busca ampla `associa|candidat|candidatar|interesse|implícit|implicit|vaga|currículo` e buscas em código. A busca ampla localizou 120 arquivos em docs/prompts; não se alega leitura integral desses 120. Resultados pertinentes:

| Termo/família | Retorno utilizado |
|---|---|
| associação / `associa` | RF12, RN01–07, DER, matrizes e análises de criação/atualização/consulta; também associações de outros recursos, descartadas como regra deste tema |
| candidatura / `candidat` / candidatar | RN03, CT-RF12 e URL de candidatura do contrato Grupo 2; não apareceu operação separada “candidatar” no backend examinado |
| interesse | enum, regra RN03, preservação RN06 e classificações persistidas; nenhum serviço de interesses independente encontrado |
| implícito / `implícit` / `implicit` | Rastreabilidade RF12 menciona card #408; `implicit` também casa palavras como “simplicity”, ruído descartado |
| frase exata `interesse implícito|interesse implicito|implicit interest` | Somente `docs/matriz_rastreabilidade.md:55`, rótulo de #408; não retornou política adicional nem definição técnica separada |
| vaga | contratos Grupo 2/busca e Application/rota de busca; VagaId textual no agregado; nenhuma tabela `vagas` no conjunto de migrations/mapping de associação examinado |
| currículo / `currículo` | RF12/RF15, matriz, DER e fixtures; descartadas regras sem relação comprovada com associação |
| `associacao|classificac` em `src/backend/api src/backend/main.py` | Vazio: nenhuma rota/DTO do tema |
| integração / cenário em `docs/matriz_testes.md`, `docs/fundamentos-backend.md` e prompts de associação | Matriz define cenários de aceitação, não impõe fluxo único; prompts de consulta decidem SQLite; harnesses mostram métodos independentes com fluxos internos |

Não foi localizada definição universal de “cenário de integração” em docs que obrigue cadeia única; o contrato da skill de testes fornece definição operacional explícita: colaboração real de ao menos duas unidades/fronteira técnica.

#### Histórico local identificado, sem equiparar card e PR

Fonte: `git log HEAD --oneline --regexp-ignore-case --grep='associa\|candidat\|interesse\|vaga'`, `git show --stat` dos commits e histórico dos arquivos.

| Trabalho | Identificação comprovada | Conteúdo observado |
|---|---|---|
| Regra #131 | merge `a501f7c`: **PR #454**, branch `feature/131-candidatura-implica-interesse`; commit `f7d68a0` com sufixo #131 e stat do domínio | agregado, VO, unitários e análises v001/v002 |
| Criação #130 | merge `26dc294`: **PR #541**, branch `feature/130-criacao-associacao-curriculo-vaga`; `85a5878` | Application, port, mapping, migration, DER e testes; stat não contém API |
| Atualização #132 | merge `5266771`: **PR #553**, branch `feature/132-atualizacao-classificacoes-associacao`; `d7b3545` | RN05–07, mutadores, casos e adapter; sem API |
| Consulta #243 | merge `4a4a36b`: **PR #565**, branch `feature/243-consulta-paginada-associacoes`; `e75b51f` | caso, adapter e teste SQLite; `6e78e3e` separa módulo integrado e job de CI |
| Busca #124/#126/#128 | merges `0ade208` PR #452, `f627617` PR #483, `324989d` PR #546; nomes de branch contêm respectivos cards; mensagens `b0e6971`, `737fef5`, `531c77e` | contrato, cliente externo e rota GET /vagas |
| Double #151 | `e711a98` PR #163, branch `task-151`; `d43e933` menciona double Grupo 2 | precedente de provedor simulado, não associação persistida |

A associação do título a #408 é somente a declaração de `docs/matriz_rastreabilidade.md:55`; não foi inferido PR #408. Histórico frontend apareceu na busca, mas não foi usado como regra backend. Não foi identificado cenário já implementado especificamente para o título.

#### Contrato atual por operação

“N/A HTTP” significa **nenhum método, caminho, DTO, serialização ou status implementado**, não uma proposta de endpoint.

| Operação | Documento | Entrada/identidade e saída implementadas | Caso/port/adapter | Falhas e ordem implementadas | HTTP |
|---|---|---|---|---|---|
| criar associação, inclusive com candidatura | RF12/RN01–03; análise criação v004 propõe HTTP 409 | `CriarAssociacaoCurriculoVagaEntrada(usuario_id: UsuarioId, curriculo_id: CurriculoId, vaga_id: VagaId, classificacoes: tuple[ClassificacaoAssociacao,...])`; retorna agregado | `CriarAssociacaoCurriculoVaga`; RepositorioCurriculo e RepositorioAssociacaoCurriculoVaga; adapters SqlAlchemy reais | CurriculoNaoEncontrado ausente/alheio → AssociacaoCurriculoVagaJaExiste → RegraDeDominioViolada vazio/enum → erro de persistência | N/A HTTP; 409 documental/proposto não implementado |
| adicionar candidatura/interesse/compatibilidade | RN03/RN05/RN07 | `AlterarClassificacaoAssociacaoCurriculoVagaEntrada(usuario_id, curriculo_id, vaga_id, classificacao)`; retorna agregado, inclusive no-op | `AdicionarClassificacaoAssociacaoCurriculoVaga`; mesmos ports | CurriculoNaoEncontrado → AssociacaoCurriculoVagaNaoEncontrada → RegraDeDominioViolada → persistência se mudou | N/A HTTP |
| remover classificação | RN05/RN06/RN07 | mesma entrada, retorna agregado | `RemoverClassificacaoAssociacaoCurriculoVaga`; mesmos ports | ownership → ausência do par → tipo/classificação → interesse com candidatura / última classe; no-op ausente | N/A HTTP |
| consultar/listar | RF12 persistência; análise consulta v002 | `ListarAssociacoesCurriculoVagaEntrada(usuario_id, offset, limit)`; tuple de agregados; dono é parâmetro interno, não sessão automaticamente | `ListarAssociacoesCurriculoVaga`; port listar_por_usuario; adapter filtra e pagina | entrada exige int estrito, offset ≥ 0, limit > 0, senão ValueError; vazio retorna () | N/A HTTP |
| excluir associação inteira | RF12 não fecha fluxo; requisitos lista como pendência | nenhum caso/port de remoção integral encontrado | nenhum | sem contrato | N/A HTTP |
| interesse separado / candidatura separada | RN03 os define como classificações | não há recurso/evento separado; usa adicionar/remover/criar acima | idem | “interesse sem candidatura” é permitido; adicionar candidatura sem par é recusado na alteração, mas criar com candidatura é permitido | N/A HTTP |

Para **cada uma** das quatro operações implementadas: sem sessão, sessão inválida/expirada/revogada e conta excluída **não têm status nem validação de sessão no caso direto**. É obrigatório fornecer `UsuarioId` confiável; não alegar que passar A certifica autenticação. Recurso alheio/inexistente são exceções acima, não 403/404 automáticos. Vaga inexistente não é consultada, logo não há 404 de vaga. Duplicidade só na criação; adição repetida é sucesso idempotente. Entrada malformada pertence aos VOs/enum/DTO interno, sem conversão HTTP. Não há status 405 específico do tema demonstrável por rota existente.

Como contexto, **GET `/vagas` existe**, mas consulta oportunidades externas, não associações: query termo/localizacao/modalidade, resposta `ResultadoBuscaVagasResposta(termo,filtros,total,vagas)`, 200; executor ausente → 503, identidade request.state não UUID → 401, timeout → 504, erro de integração → 502 (`api/vagas.py`). Não usar esses status como contrato de associação.

Precedência na composição real: `main` passa autenticador indisponível; middleware ativo pode devolver 401 antes de routing, DTO e handler. `factory` sem autenticador não instala middleware. Em composição de teste autenticada, cookie inválido → 401 antes do framework; com sessão válida, a guarda de caminho reconhecido pode produzir 403 antes da validação. Somente depois há routing/validação e handler. Nas operações diretas não há nenhuma dessas camadas: VOs/entrada são construídos antes da chamada; no caso de uso valem as ordens da tabela. Um 401 sobre URL inexistente não prova proteção de associação; falta controle positivo sobre a rota. Não criar handler artificial para fabricar esse controle.

#### Integridade, exclusão e limites

PK do par e PK do trio impedem duplicidade relacional. FK currículo é sem CASCADE; FK classes → associação é CASCADE. A migration de currículo referencia usuários sem CASCADE. Assim, **com FKs ativas**, tentativa de apagar fisicamente currículo referenciado é bloqueada; `repositorio_curriculo.excluir` remove seleções e currículo, não associações. Isso é consequência técnica da FK, não política de produto aprovada. Conta tem deleted_at, e autenticação exclui contas marcadas; os casos diretos de associação não consultam conta. Associação/classificações não têm deleted_at e não se apagam por marcar a conta. Remoção física de conta com currículo dependente também encontra FK. Não há vaga local para excluir; indisponibilidade externa não tem ação implementada aqui. Não há teto de associações, de paginação ou de comprimento em VagaId definido nos trechos lidos. Não inferir limite para texto a partir de outro recurso.

#### Interesse implícito: prova exata e limites

O sentido suportado é **interesse incluído por candidatura manual**, conforme F02/F03/F05. Não é calculado por visualização, clique, busca ou pontuação de compatibilidade. A persistência contém linha `interesse`, sem coluna que distinga explícito/implícito nem evento de origem. `para_associacao` normaliza na leitura também, portanto a prova exige linhas brutas antes de reconstrução. Os leitores identificados são obter_para_atualizacao e listar_por_usuario; não foi encontrado retorno da classificação por API. RN06 preserva interesse após retirar candidatura, logo não se trata de projeção descartável que desaparece quando a candidatura sai.

`docs/requisitos-seguranca.md` exige proteção no ciclo de vida e critérios de retenção em geral; RNF04 e ADR-002 incluem expressamente associações. Não foi encontrada política **específica** de consentimento, retenção ou exploração de interesse derivado. Não confundir armazenamento da classificação com consentimento para marketing, compartilhamento ou perfilamento.

#### Cobertura existente e inventário de fixtures/harnesses

| Artefato real | Nível e preparo | O que já cobre / reuso decidido |
|---|---|---|
| `test_domain_associacao_curriculo_vaga.py` | unitário, entidades em memória | normalização, enum, classificação vazia, conjuntos, idempotência, remoção e invariantes; não repetir como nova suíte isolada |
| `test_application_associacao_curriculo_vaga.py` | unitário, RepositorioCurriculoStub/RepositorioAssociacaoSpy | ownership, ausência, duplicidade, persistência solicitada, no-op e falhas; não prova SQL/transação |
| `test_application_consulta_associacao_curriculo_vaga.py` | unitário, port double | página e validações, tuple vazio |
| `test_infrastructure_repositorio_associacao_curriculo_vaga.py` | unitário, AsyncMock/MagicMock de AsyncSession | conversões, lock compilado, flushes, PK e tradução de IntegrityError; não prova execução do SQL |
| `test_persistencia_associacao_curriculo_vaga_integracao.py` | SQLite síncrono real, **metadata.create_all** | round-trip, PK, rollback e atualização com mapeadores; não executa Application+adapter async nem migrations |
| `integracao_repositorio_associacao_curriculo_vaga.py` | SQLite async real, arquivo temporário, **metadata.create_all** | filtro antes da paginação, ordem, vazio; job explícito no CI, fora de discover `test*.py` |
| `fixtures/credenciais_sessao.py` | BancoCredenciaisSessao, SQLite migrado, subprocesso Alembic upgrade head, sessão nova e autenticação persistida | **reusar BancoCredenciaisSessao** para ambiente/banco/contas; não mudar a fixture. Falha conhecida de grafo deve ser detectada antes de preparar. Seedar currículos próprios depois de preparar. |
| `fixtures/curriculos_autenticados_integracao.py` | BancoCurriculosAutenticadosIntegracao, SQLite migrado via thread, upgrade **heads**, auth persistida, ASGI e spies wraps | precedente útil para snapshot/controle/cleanup; não reusar app cheio nem doubles de itens; grafo múltiplo aceito por upgrade heads não atende este contrato de head única |
| `fixtures/perfis_integracao.py` | popular_perfis_fake/ler_perfis_fake: usuário/currículo SQL síncrono, formação/experiência em memória | existe, mas mistura entidades desnecessárias; não usar para semear este teste async |
| `fixtures/massa_teste_curriculos.py` | lê `docs/massa_teste_curriculos.json`, cria entidades/prévia | massa ampla em memória, não harness de associação; não usar |
| `fixtures/curriculo_exportacao.py` | CurriculoExportacaoFixture/obter_curriculo_exportacao_fixture | determinística em memória, exportação; não usar |
| `fixtures/__init__.py` | pacote descoberto | não é fonte de massa adicional |
| `test_integracao_persistencia_sessao.py`; `test_integracao_contrato_credenciais_sessao.py`; `test_integracao_composicao_credenciais_sessao.py` | usam harness de credenciais; composição é tratada separadamente, com skip explícito da produção não composta | precedentes para migração/estado de sessão e honestidade de composição |
| `test_integracao_recusa_curriculo_alheio.py` | harness autenticado e SQLite migrado, guards/controles/snapshot | precedente técnico de negativas; suas regras de currículo não viram regra de associação |
| `test_integracao_isolamento_dados_estudantes.py`; `test_integracao_isolamento_experiencias.py`; `test_integracao_recusa_perfil_alheio.py`; `test_integracao_rejeicao_referencia_curriculo.py`; `test_integracao_crud_informacoes_complementares.py` | ASGI e doubles em memória segundo classes/imports/preparo localizados | precedentes de integração de camadas, não prova de persistência deste tema |
| `test_integracao_persistencia_dados_pessoais.py` | SQLite real com create_all | precedente relacional sem migrations |
| `test_integracao_storage_204.py` | teste de storage local | não é harness de associação |
| `test_integracao_rejeicao_requisicoes_sem_credenciais_validas.py` | ASGI, com skips explícitos para composição persistida ausente | negativa sem controle de associação não atende ao pedido |

Na tabela, `fixtures/` e nomes de testes são relativos a `src/backend/tests/`. Foram inventariadas as cinco fixtures de conteúdo mais o inicializador existentes, não presumidas novas fixtures. Não se identificou harness PostgreSQL de associação nos arquivos examinados. A definição de servidor PostgreSQL de desenvolvimento no guia não equivale a infraestrutura de teste preparada.

### (b) Lacunas

| ID | O que não está definido/disponível | Opções viáveis | Recomendação e justificativa | Decisão necessária / informação exata para fechar |
|---|---|---|---|---|
| L01 | descrição e aceite do card | aceitar recorte de componentes; exigir jornada HTTP completa | recorte de componentes agora, sem afirmar entrega HTTP; título não determina transporte | produto/aceite: confirmar se fluxo Application+SQLite satisfaz o card ou fornecer contrato HTTP completo e dependências |
| L02 | contrato HTTP/composição de associação | aguardar endpoints; testar contratos internos atuais | testar interno; não fabricar rota, status 201/404/409/422/405 | técnica para recorte; produto/API para fechar HTTP: método, path, DTOs, identidade, success/failures e precedência |
| L03 | semântica adicional do rótulo “implícito” além de RN03 | só consequência candidatura; interesse por navegação/compatibilidade | usar RN03 existente; outras interpretações ampliam produto | técnica para RN03; produto se título significar outra derivação: ação geradora, duração, origem e leitores; cenários de novas fontes aguardam |
| L04 | consentimento, retenção e uso secundário específico de interesse | manter somente classificação privada; criar origem/prova de consentimento/expurgo | testar só privado/persistido no estado atual, não criar política | produto/privacidade: finalidade, base de tratamento/consentimento aplicável, prazo, acesso e destino; não bloqueia teste RN03 |
| L05 | exclusão integral e efeito de vaga indisponível/conta/currículo | preservar, cascata, bloquear, expurgo | registrar FK atual e manter fora do cenário funcional central | produto: política por recurso e operações/status; backend deverá implementar separadamente |
| L06 | validade externa/namespace/limites de VagaId | referência textual opaca; validação online/catálogo | referência opaca conforme VO/adapter; negativo “vaga não existe” não tem oráculo | produto: formato, fonte, existência, namespace e limite, se exigidos |
| L07 | formato obrigatório de cenário integrado | cadeia única; métodos independentes; híbrido | híbrido: fluxo positivo e negativas independentes, por diagnóstico/isolamento | técnica, apoiada nos harnesses e contrato da skill |
| L08 | cadeia Alembic executável única | esperar correção; experimento temporário só de arestas | primeiro registrar skip original, depois experimento temporário permitido pelo usuário | técnica; handoff de correção permanente fora deste escopo |
| L09 | dependências disponíveis em runtime do shell tests | validar shell sem mudanças; fallback temporário | configuração já oferece backend Python + aiosqlite; não alterar preventivamente | técnica; executor registra versões/imports no ambiente, não assumir ausência por prompt antigo |
| L10 | prova HTTP positiva para negativas de autenticação deste recurso | esperar rota; handler fake; teste separado da auth | aguardar rota para negativas HTTP; reutilizar testes de sessão como contexto, sem vendê-los como prova da associação | técnica para exclusão; produto/API fecha L02 antes da extensão |
| L11 | banco sozinho protege RN03/enum/não vazio | caracterizar limitação; criar constraints | leitura SQL bruta evita falso positivo; não mudar DDL | técnica para prova; engenharia de backend decide reforço em atividade separada |

Não faltam as regras candidatura ⇒ interesse ou remoção de candidatura: estão definidas. Não registrar essas regras como abertas só porque o termo exato “implícito” tem uma única ocorrência descritiva.

### Hipóteses

H1 (técnica, validação pendente): com grafo linearizado sem mudança de DDL, as migrations executam em SQLite e a fixture de credenciais prepara as contas. H2: chamar os casos reais em sessões ORM curtas permite provar transições sem nova API. H3: snapshots SQL completos impedem normalização de leitura de mascarar corrupção. Nenhuma hipótese é tratada como resultado já executado.

### Perguntas em aberto

L01/L02 exigem resposta somente para declarar conclusão HTTP/do card mais amplo; L04/L05/L06 exigem especificações de produto se forem incorporadas depois. O recorte proposto não depende de criar política nova. Aprovar esta versão pela invocação explícita da skill de testes confirma somente o recorte técnico descrito.

### Escopo

Testes/harness exclusivamente de teste, SQLite descartável migrado, casos/adapters reais, ownership, classificação, duplicidade, consultas e transições persistidas. Experimento temporário de grafo permitido no handoff, sem executar nesta análise.

### Fora do escopo

Qualquer mudança de produto, política de interesse, frontend, API nova, middleware, composição produtiva, migrations permanentes, CI ou ambiente permanente; concorrência, banco indisponível, PostgreSQL e provedores reais. Nenhuma implementação realizada nesta atividade.

### Critérios de sucesso

Critério definido pela demanda: positivos **e** negativos executáveis. Critérios inferidos desta análise: P01–P03 e N01–N08 abaixo têm componentes reais, controle positivo, estado SQL relido em outra sessão e diagnóstico de skip. O comando `.#tests` deve descobrir explicitamente o módulo. Aprovação com zero testes executados não satisfaz entrega executada. Não atribuir critérios novos ao texto do card.

## Restrições aplicáveis

AGENTS raiz/backend: Nix correto, migrations Code First, Clean Architecture/DDD e documentação de toda função/classe (o que/como/finalidade). A skill de análise permite apenas este novo Markdown. Contrato de testes proíbe mudanças no produto para fazer verde. Usuário autoriza propor experimento descartável, mas nesta análise só baseline informativo e inspeção; não foi modificado ambiente, migrations ou testes.

## Classificação comentada

Engineering domina: desenho de prova entre Application, Domain e persistência. Integração, domínio e segurança distinguem o recorte. Risco médio pela possibilidade de falso positivo de normalização ou comprovação de rota inexistente; reversibilidade fácil do código de teste. Incerteza média se limita à execução migrada e aceite do transporte.

## Decisão de roteamento

Inventário real das pastas imediatas: `backend`, `ambientes`, `frontend`, `templates`, `revisao`, `requisitos`. `prompts/README.md` atribui backend ao desenvolvimento/revisão servidor; análises de associação e SQLite já estão ali. Escolha `prompts/backend`, confiança alta. `ambientes` trataria provisão como assunto central; `requisitos` seria política de interesse; `revisao` seria auditoria, não desenho desta entrega. Não há AGENTS/override em prompts nem em suas subpastas no inventário de instruções; só raiz se aplica à escrita. A existência de análises anteriores dos componentes não muda esta linhagem inicial.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | alta | provar linhas brutas e transições reais | reconstrução pode esconder interesse não gravado |
| security | alta | negativas com controle e nenhuma consulta alheia antecipada | RN07/RNF04 |
| reliability | alta | migração real, isolamento e zero falha mascarada | create_all não testa schema versionado |
| simplicity | média | reusar banco/contas, nenhum transporte novo | recorte autorizado |

## Alternativas consideradas

A: manter testes atuais de unidade/create_all; viável como estado atual, insuficiente para a entrega migrada. B: integrar casos reais + adapters async + SQLite migrado, fluxo e negativas; recomendada. C: aguardar API produtiva e executar jornada HTTP depois; viável como sequência futura, mas bloqueia valor atual e depende de trabalho fora do escopo. Criar rota de teste que simule API é inviável para provar o contrato público inexistente.

## Perfil de pagamento comparativo

Escala ordinal; não somar.

| Dimensão | Prioridade | A | B | C | Confiança | Base |
|---|---|---|---|---|---|---|
| correctness | alta | 0 | +2 | +2 | alta/média | B cobre fronteiras existentes; C cobre transporte só depois de existir |
| security | alta | 0 | +1 | +2 | média | B prova ownership interno, C poderia provar sessão end-to-end |
| reliability | alta | 0 | +1 | 0 | média | B exige grafo temporário; C ainda sem alvo |
| simplicity | média | +2 | +1 | -1 | alta | B reusa harness e não altera produto |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado nesta linhagem.

### (c) Recomendações — decisão nesta versão

Escolher B e rotular o nível **integração de componentes**. Compor diretamente casos/repositórios reais por sessão SQLAlchemy; não chamar `main.app`, não acrescentar router e não ligar executores fictícios na factory. A fixture `BancoCredenciaisSessao` prepara SQLite migrado e duas contas. Emitir sessão com `CriadorSessaoSeguro`, confirmar e autenticar por `AutenticadorSessaoPersistida(RepositorioSessaoSqlAlchemy(...))`; usar a identidade retornada na entrada do caso. Isso demonstra validação persistida seguida do caso interno, **não** encaminhamento por middleware/handler. Não chamar essa sequência de integração HTTP autenticada.

Arquivos novos propostos (não criados agora):

- `src/backend/tests/fixtures/associacoes_candidatura_integracao.py`: suporte específico com BancoCredenciaisSessao, currículos, sessões curtas, snapshots SQL e spies `wraps`; documentação de todas as classes/funções.
- `src/backend/tests/integracao_associacao_candidatura_interesse.py`: `IsolatedAsyncioTestCase`, módulo explícito conforme precedente de `6e78e3e`, com métodos positivos e negativos separados. Não entra por acidente na suíte unitária sem aiosqlite.

Incluir comentário `Proveniência: decision-analysis prompts/backend/20261024-171508-integracao-associacao-candidatura-interesse-v001.md#v001` em cada arquivo. Não alterar fixtures existentes nem `.github/workflows/ci.yml`.

#### Dados e protocolo comum

Usar A/B e contas do `BancoCredenciaisSessao`; currículos A1 `UUID(int=201)`, A2 `UUID(int=203)` e B1 `UUID(int=202)`, UUID inexistente `299`. Semear `CurriculoRegistro` com título sintético, layout `simples`, is_public False; commit depois de usuários já preparados. Vagas `vaga-integracao-01`, `vaga-integracao-02` são IDs textuais sintéticos, sem catálogo externo. Cada método/subcaso tem arquivo SQLite/diretório próprios e cleanup garantido mesmo após SkipTest/falha.

Para **toda** operação positiva: commit externo, fechar sessão, abrir outra sessão para comparar tabelas `associacoes_curriculo_vaga` e `classificacoes_associacao_curriculo_vaga`; depois ler pelo caso/listagem em outra sessão. Comparar conjuntos, não ordem de classificações. Para toda negativa: preparar controle positivo equivalente, tirar snapshot SQL bruto ordenado de raízes/classes/currículos, executar recusa, verificar nenhuma escrita pendente (new/dirty/deleted e spies), encerrar transação, reler por sessão distinta e comparar igualdade. Não usar rollback cego como única prova de “nenhuma alteração”: nos erros anteriores à persistência fazer commit externo após confirmar ausência de mutações, de modo a detectar escrita indevida. Em IntegrityError de banco, rollback obrigatório antes da releitura; relatar que prova atomicidade do boundary do teste.

Spies envolvem métodos reais, não substituem retornos. Negativa pré-caso (N07) exige `executar.assert_not_awaited`; ownership interno exige caso chamado, mas `existe_por_par`/`obter_para_atualizacao` e escrita não chamados. Zerar contadores após o controle para não misturar chamadas. Não afirmar “caso não chamado” quando a recusa é dele.

#### Fluxo positivo encadeado: métodos separados da matriz negativa

Todos os critérios de cenário são **inferidos** para esta entrega; a coluna de fonte distingue regra documental definida de comportamento apenas implementado. Camada de todos: caso de uso + banco; autenticação no preparo é adapter + banco, sem HTTP.

| ID / objetivo | Pré-condições | Passos | Resultado esperado e verificações | Fonte/regra |
|---|---|---|---|---|
| P01 `test_criacao_com_candidatura_persiste_interesse_e_isola_curriculo` | banco migrado, A com A1/A2, B/B1; token válido de A | autenticar token real; criar A1/vaga01 com **só candidatura**; commit; reler SQL e listar A/B em novas sessões; fechar sessão de autenticação, emitir novo token e repetir consulta interna | uma raiz A1/vaga01; duas linhas exatas candidatura/interesse; nenhuma raiz A2/B1; listagem A contém par/classes, B não; segunda autenticação válida e estado idêntico | RF12/RN03, CT-RF12-02/05/C03; criação/adapter atuais |
| P02 `test_adicao_remocao_e_repeticao_preservam_interesse` | A1/vaga01 criado inicialmente com compatibilidade | adicionar candidatura; commit/reler; repetir adição; remover candidatura; repetir remoção; adicionar interesse repetido; remover compatibilidade; reler a cada transição | compatibilidade+candidatura+interesse; repetição não escreve; após remover candidatura ficam compatibilidade+interesse; repetição mantém; final interesse, mesma raiz | RN03/05/06, CT-RF12-03/04/10/11/12, mutadores e Application |
| P03 `test_interesse_isolado_e_candidatura_com_compativel_sao_permitidos` | A1/A2 próprios e pares novos | criar só interesse num par; criar candidatura+compatibilidade no outro; commit e reler bruto/listagem | primeiro só interesse, segundo três classes; nenhum efeito cruzado | CT-RF12-C01/C06; enum/construtor |

P01 prova “registrar candidatura” como classificar a associação, não envio de candidatura a serviço externo. P02 prova efeito sobre interesse quando candidatura muda; não implementa desassociação integral inexistente. Evitar repetir toda a matriz combinatória unitária: estes três métodos exercitam os pontos em que persistência/normalização/transação colaboram.

#### Matriz negativa independente

Cada linha deve ser método separado; variantes podem usar subTest **com banco novo por variante**. P = controle positivo no mesmo recurso/operação; todos seguem o protocolo de snapshot em sessão nova. Não existe status HTTP nestes casos.

| ID / objetivo | Pré-condições e controle positivo | Passos da negativa | Resultado esperado / chamada interrompida | Fonte e origem |
|---|---|---|---|---|
| N01 `test_criacao_duplicada_nao_muda_classificacoes` | criar A1/vaga01 com interesse com sucesso (P) | tentar criar mesmo par com candidatura | AssociacaoCurriculoVagaJaExiste; salvar não chamado; interesse continua único | inferido; implementado em Criar e PK; rejeição também descrita na análise criação v004 |
| N02 `test_curriculo_alheio_nao_consulta_associacao` | B cria B1/vaga01 e altera com sucesso; emitir token A válido (P sobre **B1**) | A tenta criar outro par B1/vaga02 e adicionar/remover em B1/vaga01, variantes isoladas | CurriculoNaoEncontrado; caso chamado, consultas/escritas da associação não chamadas; snapshot global igual | inferido de RN07/CT-RF12-15 e `_obter_associacao_do_proprietario`/Criar |
| N03 `test_curriculo_inexistente_recusa_antes_da_associacao` | usar UUID299 inexistente; no controle equivalente criar currículo com **esse UUID** em banco independente e concluir operação | banco negativo mantém UUID299 ausente; criar/adicionar/remover com demais dados iguais | CurriculoNaoEncontrado; não consulta associação nem escreve | inferido do código; ausência não é “currículo de outra pessoa” |
| N04 `test_alteracao_sem_associacao_nao_cria_par` | controle com A1/vaga01 existente permite adição/remoção; negativo mesmo par em banco novo sem raiz | adicionar candidatura ou remover classificação sem criar par | AssociacaoCurriculoVagaNaoEncontrada; sem escrita/criação; snapshot idêntico | inferido de código e intenção de alteração de associação existente |
| N05 `test_remover_interesse_com_candidatura_preserva_todas_linhas` | A1/vaga01 com candidatura/interesse; controle: remover candidatura e então interesse **com compatibilidade restante** no mesmo par em banco independente | remover interesse enquanto candidatura ativa | RegraDeDominioViolada; atualizar_classificacoes não chamado; par/classes intactos | inferido de RN06/CT-RF12-13, regra documental definida |
| N06 `test_remover_ultima_classificacao_preserva_raiz` | mesmo par com interesse+compatibilidade no controle permite remover interesse; negativo só interesse (variante só compatibilidade) | remover última classe | RegraDeDominioViolada; sem atualização; raiz e classe preservadas | inferido de RN06/CT-RF12-14, definido |
| N07 `test_entrada_invalida_antes_do_caso_nao_chama_executor` | controle com mesmo A1/vaga01, UUID e VagaId válidos cria normalmente | construir CurriculoId com valor não UUID; VagaId não textual; enum com valor desconhecido; entrada de listagem offset -1, limit 0 ou bool; depois não chamar caso se construção falhar | RegraDeDominioViolada nos VOs, ValueError no enum/entrada de paginação; spy executar não chamado; banco idêntico | inferido/ **caracterização interna**, VO/enum e ListarEntrada; não é validação HTTP/422 |
| N08 `test_classificacao_vazia_ou_invalida_na_criacao_nao_persiste` | controle A1/vaga01 com candidatura válida em banco equivalente | chamar Criar com tuple vazia; variante string não enum passada na tuple | RegraDeDominioViolada após ownership/duplicidade; caso chamado, salvar não chamado; banco intacto | inferido de CT-RF12-06 e construtor; string é caracterização da guarda de domínio para chamada interna |

N03 usa controle em banco equivalente pois o recurso inexistente não pode permanecer ausente e simultaneamente permitir operação positiva. Registrar explicitamente a única diferença de preparo. N02 cobre associação alheia pelo ownership do currículo, não inventa ID de associação independente.

Negativas **não programar como se já houvesse contrato**: sem cookie, inválido/expirado/revogado, conta excluída via HTTP e método não permitido (L02/L10); vaga inexistente (L06); interesse sem candidatura como recusa (é permitido, P03); criação de candidatura sem associação como recusa genérica (criação é válida, P01; somente mutação sem par é N04). Não simular status esperados nem aceitar um 401/404 de rota ausente como aprovação. Se mantidos placeholders HTTP, usar skip explícito “rota de associação e controle positivo HTTP ausentes nesta branch”, sem falso corpo executável; recomendação mínima é listá-los no PR como handoff, sem testes vazios.

Não adicionar teste de falha de banco/concorrência só por CT-RF12-09: esta fatia declara o limite e mantém a cobertura de rollback existente como contexto, sem alegar que a nova suíte prova indisponibilidade ou corrida.

#### Ambiente, migração e skips

`nix/tests.nix` **já** importa `backend-python-packages.nix` e inclui `ps.aiosqlite`; lista comum contém FastAPI, uvicorn, SQLAlchemy, Alembic, psycopg e pydantic-settings. Não há cliente/servidor PostgreSQL dedicado declarado nesse shell. `nix/backend.nix` usa a lista comum sem aiosqlite. Nenhuma dependência de httpx é necessária: não há HTTP nesta fatia.

Harness proposto usa `BancoCredenciaisSessao`, que exige head única e aplica `upgrade head`; nunca `create_all` nem `stamp` para pular DDL. Novo preflight específico, antes de instanciar/preparar o banco, deve inspecionar atribuições AST incluindo AnnAssign, detectar IDs repetidos, referência ausente, ciclo e heads. Revisões duplicadas/múltiplas heads **conhecidas** no estado original → SkipTest com nomes/IDs. Erro de parsing, migration inesperadamente quebrada, erro SQL ou asserção → falha/erro, nunca skip genérico. Driver opcional: capturar somente ModuleNotFoundError de aiosqlite e aplicar skip antes de abrir engine; não esconder falta de dependência obrigatória ou erro de import de produto. Imports do harness existentes não dependem diretamente de importar aiosqlite com sucesso, há guarda explícita.

Relatar separadamente `testsRun`, failures/errors, skips por motivo e quantidade efetivamente exercitada; subTest não é teste adicional na contagem unittest. Exigir P01–P03/N01–N08 executados para declarar a fatia provada. Um `OK (skipped=...)` sozinho não comprova negócio. Se todo cenário novo for ignorado por grafo, entrega de código é executável condicionalmente, mas a validação funcional permanece não demonstrada no estado original.

### Impacto da revisão

Nenhum identificado — decisão inicial; não altera análises anteriores.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | não confundir normalização na leitura com persistência | F11 |
| security | prioritized | controles equivalentes e interrupção observável | RN07/guards atuais |
| reliability | prioritized | validar schema migrado e isolamento | fixture existente/H1 |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| simplicity | dois arquivos de teste, sem produto | reutiliza banco existente e limita dados |
| observabilidade da prova | aprovado/ignorado/falhou distintos | verbose + contagens + razão do skip |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | agregado relido encobre linha interesse ausente | alta | estudante/revisores |
| security | negativa sempre falha por rota inexistente | alta | equipe e dados privados |
| reliability | schema create_all passa apesar de migrations inválidas | alta | executor/entrega |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | snapshots SQL e sessões novas | simplicity | necessário para prova independente |
| reliability | experimento temporário e restauração detalhada | delivery-speed | permitido, sem fingir cadeia original íntegra |
| scope | API fica como handoff | user-value | transparente; não há autorização para implementar transporte |

## Achados de backend e divergências — sem correções

1. **D01 API planejada ≠ entregue:** análise criação v004 inclui API e 409; código do commit `85a5878` e factory atuais não a implementam. Código atual é mais confiável para capacidade/status executável; documento é evidência de intenção, não de rota disponível. Atualização v002 explicitamente deixa HTTP fora; não estender essa decisão para dizer que criação nunca pretendeu API.
2. **D02 shell antigo ≠ atual:** análise consulta v002 diz que faltava aiosqlite; `nix/tests.nix` atual o inclui. Configuração atual prevalece para composição declarada, confirmação runtime fica ao executor. Backend sem driver explica skips possíveis; os 33 motivos individuais não foram todos coletados no baseline não verbose e não são atribuídos em bloco ao grafo.
3. **D03 integridade de RNF05 ≠ constraints completas:** não há FK de vaga nem CHECK que force candidatura/interesse; Domain normaliza na escrita e leitura. Não afirmar banco inválido por aceitar ID opaco quando o contrato deliberadamente usa referência externa. A garantia de RN03 é do caminho dos agregados, não de qualquer SQL arbitrário.
4. **D04 exclusão:** requisitos ainda listam tratamento de associação na exclusão como pendente. FK atual tende a bloquear exclusão física de currículo associado; caso de exclusão de currículo não limpa associação. Registrar consequência/risco; não criar cascata, retenção ou status neste trabalho.
5. **D05 conta excluída:** autenticação persistida filtra deleted_at; casos diretos de associação e listagem não verificam conta ativa. Invocação interna com UsuarioId de conta excluída pode contornar guarda se caller não autenticar. Não tratar como 401 do caso, nem acrescentar regra sem tarefa própria.
6. **D06 composição produtiva:** há middleware com autenticador indisponível e nenhuma associação. O teste interno não certifica produção segura/funcional. Não “ativar auth”: ela já está instalada, falta dependência operacional.
7. **D07 privacidade:** classificações não guardam origem explícita/derivada, finalidade secundária ou consentimento. Sem política específica encontrada, não inferir autorização para leitores externos/marketing. Testes usam somente dados sintéticos e não imprimem tokens/hash/conteúdo privado.
8. **D08 matriz:** introdução de `docs/matriz_testes.md` menciona RN01–04, mas tabela atual contém RN05–07; rastreabilidade RF12 enumera 01–09/C01–07 sem 10–15. Regras funcionais e linhas atuais são mais específicas para mutações; registrar desatualização documental, não corrigi-la.
9. **D09 grafo:** duplicações 0011/0012 e ramos finais impedem certificar `upgrade head` original. Testes create_all existentes não detectam esse bloqueio. Plano abaixo é experimento, não reparo.

## Riscos e efeitos de segunda ordem

Sucesso no grafo temporário pode ser confundido com cadeia Alembic saudável; anexar ambos os resultados. Testes que só reconstruam agregados podem passar com linhas corrompidas; conferir SQL antes do mapper. Assumir que A veio da sessão pode esconder ausência do handler; declarar integração direta. Spies de método real e leitura global capturam efeitos cruzados, mas não certificam ausência de qualquer chamada de rede futura se um componente novo for introduzido; revisar ao alterar dependências. SQLite não valida semântica PostgreSQL de locks/corridas.

## Validação da decisão

### Baseline informativo real desta análise

Comando solicitado, a partir da raiz:

```sh
nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src
```

Primeira tentativa dentro do sandbox: erro Nix `opening lock file "/nix/var/nix/db/big-lock": Read-only file system`, sem testes. Reexecução com permissão de acesso ao Nix: exit 0; **Ran 955 tests in 14.864s; OK (skipped=33)**. Zero failures, zero errors; 922 testes não ignorados pelo resumo. Houve warnings Starlette de status 422 depreciado e avisos de duração asyncio; não corrigidos. O módulo explícito `integracao_repositorio_associacao_curriculo_vaga` não é incluído pelo padrão de discover. Não se atribuem motivos individuais aos 33 skips sem relatório verbose.

Gate executado depois do baseline:

```sh
nix develop .#quality --command ruff check src/backend
```

Exit 0, `All checks passed!`. Nenhuma correção aplicada. Não foram executados o cenário novo (não existe), migrations, import probes em tests nem experimento temporário. Estado inicial e inspeção posterior: `git status --short` vazio antes deste Markdown.

### Comandos do executor e comparação

```sh
nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest -v backend.tests.integracao_associacao_candidatura_interesse
nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src
nix develop .#quality --command ruff check src/backend
```

Rodar os três primeiro no estado original e depois no experimento, reportando os resultados separadamente. Baseline não pode ganhar failures/errors: comparação por identificação e erro, não apenas total (955/33 é referência desta branch, testes novos explícitos não devem alterar contagem do discover). Se lint der I001 **nos arquivos do executor**, usar `nix develop .#quality --command ruff check --select I --fix <arquivos-apontados>` e repetir o gate completo. Se apontar arquivos de produto não alterados, registrar bloqueio/handoff sem ampliar escopo. Não há autorização nesta análise para corrigir produto por lint.

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| RN03 dura no banco | duas linhas brutas após commit | P01/P02 em sessão nova | leitura normaliza mas SQL não contém interesse |
| ownership antes da associação | exceção + spies + snapshot | N02/N03 | leitura de par alheio antes da guarda |
| negativos são seletivos | controle equivalente aprovado | todos N | controle falha também |
| ambiente original bloqueado | skip com revisões/heads | execução original | erro inesperado escondido em skip |
| experimento permite prova | migrations executadas e todos P/N exercitados | execução temporária | DDL incompatível, warnings ou skip residual |

## Handoffs e atividades posteriores

### Elegibilidade da skill de testes

Foram lidos o contrato de entrada, fronteira de escopo e teste de adequação em `.agents/skills/integration-system-testing-v1/references/`. Fatia B é **valid** para implementação após invocação explícita desta análise `proposed`: (1) entrega é teste; (2) cruza Application/adapter/SQLite real; (3) oráculos P/N acima existem em RN03/RN05/RN06/RN07 e código; (4) alvo é arquivo SQLite descartável, só arquivos de teste. Dois sinais independentes: fronteira real com banco e harness migrado já existente. Não é teste unitário de agregado, nem exige API nova.

Classificação de responsabilidades: P/N e fixture → `integration`; caracterização do transporte inexistente não vira `contract` fabricado; API/composição/constraints/política → `product-change`, excluídos; alteração permanente de Nix/CI → `external-test-operations`, excluída. Negativas HTTP agora são `ambiguous` por falta de oráculo/controle positivo, não fatia validada. Se o executor concluir que API é indispensável, parar e pedir revisão/decomposição L01/L02. Não implementar contra esta análise como se aprovasse toda uma jornada HTTP.

O experimento de migrations altera temporariamente arquivos produtivos de schema, portanto **não é responsabilidade de escrita da skill de testes**, que proíbe corrigir migrations. Divisão recomendada: executor de testes cria a fatia elegível; operador técnico autorizado pelo pedido executa experimento temporário separado e restaura caminhos. Caso se trate de uma única sessão de agente com a skill, não estender o alcance dela por inferência: preservar teste e encaminhar operação fora da skill. Correção permanente cabe a backend/persistência; ambiente permanente à atividade Nix; decisão de L04/L05 a produto/privacidade. Não delegação automática a subagentes.

### Plano concreto do experimento temporário — não aplicado nesta análise

Antes de qualquer mudança, executar fora do Nix `git status --short` e `git diff -- nix flake.nix flake.lock src/backend/infrastructure/persistence/alembic/versions`; conferir também staged e arquivos untracked. **Se houver mudanças do usuário nesses caminhos, parar e informar; não restaurar nem sobrescrever.** Não é suficiente só verificar unstaged. Salvar texto completo dos diffs temporários no resumo da execução antes de restaurar. Não versionar esse experimento.

`nix/tests.nix` só pode mudar se confirmação no próprio `.#tests` mostrar ausência de Python/backend ou aiosqlite; a configuração lida já satisfaz ambos. Se necessário, manter import da lista comum e Python withPackages com `backendPythonPackages ps ++ [ ps.aiosqlite ]`; não mexer em flake.nix/lock. Se a configuração atual satisfizer, nenhuma alteração Nix.

Identificadores e arestas de todos os arquivos do grafo, relativos a `src/backend/infrastructure/persistence/alembic/versions/`. `—` conserva exatamente os valores atuais. IDs temporários novos terminam em letra para não colidir; nenhuma função upgrade/downgrade, DDL ou nome de arquivo muda:

| Arquivo | revision atual → temporária | down_revision atual → temporária |
|---|---|---|
| `20260916_0001_criar_usuarios.py` | 20260916_0001 — | None — |
| `20261005_0002_criar_curriculos.py` | 20261005_0002 — | 20260916_0001 — |
| `20261007_0003_criar_curriculo_itens.py` | 20261007_0003 — | 20261005_0002 — |
| `20261012_0004_criar_sessoes.py` | 20261012_0004 — | 20261007_0003 — |
| `20261012_0005_criar_experiencias_profissionais.py` | 20261012_0005 — | 20261012_0004 — |
| `20261014_0006_criar_competencias.py` | 20261014_0006 — | 20261012_0005 — |
| `20261014_0007_adicionar_dados_contato_usuario.py` | 20261014_0007 — | 20261014_0006 — |
| `20261013_0004_adicionar_dados_consulta_estudante.py` | 20261013_0004 — | 20261014_0007 — |
| `20261014_0007_criar_formacoes_academicas.py` | 20261014_0008 — | 20261014_0007 → 20261013_0004 |
| `20261014_0007_unificar_ramos_schema.py` | 20261014_0009 — | (20261013_0004, 20261014_0008) → 20261014_0008 |
| `20261015_0009_criar_idiomas.py` | 20261015_0009 — | 20261014_0008 → 20261014_0009 |
| `20261015_0010_criar_certificacoes.py` | 20261015_0010 — | (20261014_0009, 20261015_0009) → 20261015_0009 |
| `20261015_0011_criar_cursos.py` | 20261015_0011 — | 20261015_0010 — |
| `20261015_0011_exclusao_logica_formacoes_academicas.py` | 20261015_0011 → 20261015_0011b | 20261015_0010 → 20261015_0011 |
| `20261015_0012_criar_links_profissionais.py` | 20261015_0012 — | 20261015_0011 → 20261015_0011b |
| `20261015_0012_criar_projetos_academicos.py` | 20261015_0012 → 20261015_0012b | 20261015_0011 → 20261015_0012 |
| `20261016_0013_criar_documentos.py` | 20261016_0013 — | 20261015_0012 → 20261015_0012b |
| `20261017_0014_exclusao_logica_experiencias_profissionais.py` | 20261017_0014 — | 20261016_0013 — |
| `20261017_0015_adicionar_ordem_secoes_curriculos.py` | 20261017_0015 — | 20261017_0014 — |
| `20261017_0004_criar_associacoes_curriculo_vaga.py` | 20261017_0004 — | 20261007_0003 → 20261017_0015 |

Original: duplicados `20261015_0011` (cursos/exclusão formação), `20261015_0012` (links/projetos); terminais por inspeção de arestas `20261017_0015` e `20261017_0004`. Com duplicação não alegar que o resolvedor Alembic tem grafo válido de duas heads: são candidatos terminais da declaração dos arquivos.

Proposta é uma cadeia de 20 nós na ordem da tabela, uma raiz None e head `20261017_0004`. Justificativa de ausência de ciclo: cada predecessor aponta para a linha imediatamente anterior; validar isso por AST no executor, incluindo unicidade, predecessor existente e visita topológica que percorra os 20 nós. Não basta contar heads. A associação fica no final para reunir os ramos sem criar migration de merge. Os dois pontos de merge existentes passam a aresta simples; somente metadados mudam. Atualizar eventual cabeçalho descritivo de revision/revises somente para refletir os IDs, sem tocar DDL. Não renomear arquivos.

Conferir com `nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m alembic heads` e `... python3 -m alembic history`; capturar stdout/stderr, exigir **uma head e nenhum warning**. Depois o harness aplica `upgrade head` em SQLite novo, confirma `alembic_version` igual à head e roda P/N. Configuração/metadata importadas são reais. Se qualquer DDL falhar, parar: o plano não autoriza mudá-la. O experimento prova componentes **sob esse grafo temporário**, não a cadeia original nem migração de banco existente com dados.

Antes da restauração, copiar o **diff completo**, sem abreviação, dos seguintes caminhos ao resumo. Restaurar em finally por caminhos explícitos (somente os que o operador efetivamente alterou, após guarda de árvore limpa):

```sh
git restore -- nix/tests.nix
git restore -- src/backend/infrastructure/persistence/alembic/versions/20261014_0007_criar_formacoes_academicas.py src/backend/infrastructure/persistence/alembic/versions/20261014_0007_unificar_ramos_schema.py src/backend/infrastructure/persistence/alembic/versions/20261015_0009_criar_idiomas.py src/backend/infrastructure/persistence/alembic/versions/20261015_0010_criar_certificacoes.py src/backend/infrastructure/persistence/alembic/versions/20261015_0011_exclusao_logica_formacoes_academicas.py src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_links_profissionais.py src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_projetos_academicos.py src/backend/infrastructure/persistence/alembic/versions/20261016_0013_criar_documentos.py src/backend/infrastructure/persistence/alembic/versions/20261017_0004_criar_associacoes_curriculo_vaga.py
git status --short
```

Não executar a primeira linha se Nix não mudou. Nunca `git restore .`. Estado final não pode conter mudanças em `nix/`, `flake.nix`, `flake.lock` ou `src/backend/infrastructure/persistence/alembic/versions/`; somente os testes e este artefato podem ser entregues. Se houve modificação concorrente nesses caminhos, parar e preservar conteúdo em vez de restaurar cegamente. Após restauração repetir execução original e gate para confirmar retorno ao diagnóstico original. Registro deve distinguir original inicial, temporário e original restaurado.

### Registro mínimo e responsáveis

Esta análise é o registro decisório durável. Para execução, basta texto do PR com arquivos, proveniência, P/N cobertos, contagens, skips, comandos, achados e **diffs completos do experimento**. Precedentes `prompts/backend/*consulta-paginada*` documentam decisão; `docs/testes/evidencias/` contém evidências de frontend, não demonstra obrigação de criar documento backend para este cenário. Não criar segundo relatório versionado por analogia. Se o PR não permitir preservar os diffs completos, anexar como evidência de execução fora do código; não omitir. Correções do backend e novas políticas devem virar atividades independentes, com nova análise quando alterarem oráculos.

## Síntese

Recomenda-se implementar somente a integração direta de casos reais com SQLite migrado: fluxo positivo da candidatura/interesse, transições idempotentes e matriz negativa com controles e snapshots independentes. RN03/RN06 resolvem a semântica central; ausência de API e grafo Alembic inválido limitam a prova. Resultado desta atividade é exclusivamente esta análise `initial`, não implementação nem execução do novo teste.
