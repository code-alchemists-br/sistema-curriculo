---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-18T13:18:22-03:00"
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
    - {path: docs/contrato-credenciais-sessao.md, relationship: primary, representation: prose, function: schema-contract, format: markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/api/middleware_autenticacao.py, relationship: primary, representation: source-code, function: production, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/api/cadastro_acesso.py, relationship: primary, representation: source-code, function: production, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/api/sessoes.py, relationship: primary, representation: source-code, function: production, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/api/factory.py, relationship: primary, representation: source-code, function: production, format: python, analysis_scope: selected-section, locator: "create_app: assinatura, registro de middleware e routers", content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/main.py, relationship: primary, representation: source-code, function: production, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/application/sessoes.py, relationship: primary, representation: source-code, function: production, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/application/autenticacao_sessao.py, relationship: primary, representation: source-code, function: production, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/application/acesso_estudante.py, relationship: supporting, representation: source-code, function: production, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/infrastructure/security/tokens_sessao.py, relationship: primary, representation: source-code, function: production, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/infrastructure/security/autenticador_sessao.py, relationship: primary, representation: source-code, function: production, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/infrastructure/security/autenticador_sessao_indisponivel.py, relationship: primary, representation: source-code, function: production, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/infrastructure/persistence/sqlalchemy/sessao.py, relationship: primary, representation: source-code, function: schema-contract, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_sessao.py, relationship: primary, representation: source-code, function: production, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: src/backend/infrastructure/persistence/alembic/versions/20261012_0004_criar_sessoes.py, relationship: primary, representation: source-code, function: schema-contract, format: python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: nix/tests.nix, relationship: supporting, representation: source-code, function: configuration, format: nix, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: nix/backend.nix, relationship: supporting, representation: source-code, function: configuration, format: nix, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: nix/backend-python-packages.nix, relationship: supporting, representation: source-code, function: configuration, format: nix, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
    - {path: flake.nix, relationship: supporting, representation: source-code, function: configuration, format: nix, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: 46a7a75, availability: available}
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/ambientes, prompts/revisao, prompts/requisitos, prompts/frontend, prompts/templates]
  confidence: high
  rationale: "O resultado especifica integração do contrato HTTP e persistência do backend; ambiente é suporte, não objeto central."
classification:
  sphere: engineering
  concerns: [integration, security, data]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: high
  reversibility: easy
  risk: high
---

# Análise de decisão — Validação do contrato de credenciais e registro contra #80–#82

## Solicitação original

Transcrição literal da demanda; as skills fornecidas na conversa são instruções de execução, registradas em Informações complementares.

```text
$decision-analysis-v4 Implementar "Criar roteiro de validação do contrato de credenciais e registrar o resultado contra os cards #80–#82". Antes de decidir o que o roteiro deve conter, descubra o que foi feito nesses três cards, analise o contrato de credenciais de sessão e o código que o implementa, e a documentação pertinente. Esta é uma análise nova, iniciada do zero.

## Regra principal: não presumir

Todo fato deve vir de um artefato lido (histórico Git, código, testes, migrations, documentação de segurança, requisitos, configuração de ambiente), com o caminho indicado. O que nenhum artefato definir deve ser registrado como lacuna, nunca como fato.

- Separe em seções distintas: **(a) fatos encontrados**, com caminho e trecho; **(b) lacunas**, ou seja, o que nenhum artefato define; **(c) recomendações**, que são suas, com justificativa.
- Para cada lacuna, apresente as opções viáveis, recomende uma e marque se depende de decisão de produto ou se pode ser tomada tecnicamente com base no que existe.
- Quando artefatos divergirem (código, documentação, requisitos, testes, texto dos cards), aponte a divergência, diga qual fonte parece mais confiável e por quê, sem escolher em silêncio.
- Não transponha regras de outros recursos (formação, projeto, currículo) para o contrato de credenciais sem que um artefato de credenciais as sustente.

## Ponto de partida

Parta exclusivamente do estado atual desta branch, criada a partir da `dev`. Não presuma a existência de nenhum teste, roteiro, análise ou registro de validação sobre credenciais. Descubra por inspeção o que já existe na base: o que existir entra como fato (e deve ser avaliado quanto à cobertura), o que não existir entra como lacuna.

## Fontes a analisar

1. **Os cards #80, #81 e #82 e o trabalho feito neles.**
   - A CLI do GitHub e a rede podem não estar disponíveis; **não dependa delas**. Localize o trabalho por inspeção do histórico Git local (`git log --all`, mensagens de commit, mensagens de merge "Merge pull request #N", nomes de branch, histórico dos arquivos relacionados) e por menções nos documentos e análises presentes na base.
   - **Número de card não é número de PR.** Os números podem aparecer como `#N` em mensagens de commit, em nomes de branch (por exemplo `feature/N-...`, `issue-N`, `task-N`) ou em referências em documentos; PRs têm numeração própria. Registre como identificou a ligação entre cada card e cada PR ou commit, e **não infira a ligação apenas pela coincidência de números**. Se um card não puder ser resolvido, registre como lacuna.
   - Para cada card, levante: título e objetivo; critérios de aceite, **se estiverem disponíveis localmente**; PRs, commits e arquivos relacionados; decisões registradas; testes adicionados; e o que ficou explicitamente fora.
   - **Texto dos cards (preencher se disponível; caso contrário, será tratado como lacuna):**
     - Card #80: [colar título e critérios de aceite]
     - Card #81: [colar título e critérios de aceite]
     - Card #82: [colar título e critérios de aceite]
     Se o texto não estiver disponível, **não invente critérios de aceite**: derive o que for possível do trabalho feito, marque a origem de cada critério como "inferido" e liste exatamente o que precisa ser fornecido para fechar a lacuna.
2. **Documentação pertinente**, localizada por busca (não presumida): requisitos de segurança, requisitos funcionais ligados a autenticação e sessão, o contrato de credenciais, DER, configuração de ambiente e testes, e qualquer análise anterior sobre credenciais ou sessão que exista na base.
3. **Código atual relacionado**: o middleware de autenticação, a entidade e as portas de sessão, o criador, o autenticador e o revogador de sessão, o repositório e a migration de sessão, as rotas de acesso e de sessão, a composição da aplicação (`main.py` e `factory.py`) e os testes existentes, unitários e integrados, que tocam sessão, credenciais ou 401.

## O que levantar

- **O contrato de credenciais:** o que são as credenciais de sessão; como são emitidas, transportadas (cabeçalho, cookie ou outro), validadas, expiradas e revogadas; formatos, prazos e regras de segurança; e quais respostas HTTP o contrato prevê em cada falha (ausente, malformada, desconhecida, expirada, revogada, de conta excluída ou inexistente). Registre separadamente o que está **definido** e o que está **só implementado sem definição**.
- **A persistência da sessão:** modelo, constraints, índices, o que é armazenado (e se a credencial é guardada em claro ou derivada), expiração, revogação e o comportamento do repositório.
- **A composição real:** como a autenticação é instalada na aplicação que sobe (`main.py`, `factory.py`), em que condição o middleware é registrado e com qual autenticador. **Não presuma o estado**: leia o código atual e registre o que a composição de produção realmente faz, e o que isso implica para o que um roteiro de validação consegue provar.
- **Cobertura existente:** o que os testes atuais já cobrem sobre o contrato (e com que nível: unitário com doubles, ou integração com banco real), e o que está sem cobertura, para o roteiro não repetir cobertura sem necessidade.
- **O significado de "roteiro de validação" e de "registrar o resultado contra os cards":**
  - procure precedentes no projeto (roteiros, planos ou registros de validação em `docs/`, `prompts/` ou outro lugar) e o formato esperado;
  - determine onde e como um resultado é registrado contra um card neste projeto (documento no repositório, descrição de PR, comentário no card). Se o registro exigir uma ação no GitHub e ela não estiver disponível, a entrega deve ser um texto pronto para colar por card, e isso deve ser registrado como limite;
  - o roteiro deve ser **executável** (testes integrados), conforme decisão do usuário. Verifique se os cards ou a documentação definem outro formato e, se definirem, aponte a divergência.
- **O ambiente de testes integrados:** o que `nix develop .#tests` oferece hoje (Python, dependências do backend, banco), como os testes integrados existentes são organizados e executados, e como obter SQLite e, se aplicável, PostgreSQL.
- **Bloqueios de execução preexistentes:** verifique por inspeção e registre, **sem tratá-los como escopo e sem corrigi-los**, o estado da cadeia de migrations do Alembic (revisões duplicadas ou múltiplas heads), das dependências do ambiente `.#tests` e de qualquer rota prevista pelo contrato que não esteja implementada.

## Escopo

Definir (1) o **roteiro de validação executável** do contrato de credenciais de sessão e de sua persistência, derivado do contrato e dos cards #80–#82, e (2) o **registro de resultado por card**, com veredito para cada um, a ser preenchido a partir de uma execução real. A análise deve definir cenários, ordem, dados, resultados esperados, fixtures, forma de execução e o modelo do registro.

Fora do escopo: alterar o contrato, o middleware, a persistência ou a composição; corrigir defeitos de back-end encontrados (registre-os como achados); front-end; novas regras de segurança; e alterações permanentes de ambiente.

## Instruções

- Para cada decisão que os artefatos não resolverem, recomende uma opção com justificativa e marque se depende de produto.
- **Rastreabilidade:** para cada card, monte a ligação entre critérios de aceite, cenários do roteiro, resultado esperado, evidência exigida e o status possível (atendido, parcialmente atendido, não atendido, não verificável). A análise define o **modelo** desse registro; os resultados em si só podem ser preenchidos após execução real.
- **Honestidade do registro:** um card só pode ser marcado como atendido com evidência de execução real (comando, ambiente, resultado). Teste ignorado (skip) não conta como prova, e a análise deve dizer como o registro distingue "executado e aprovado" de "ignorado por ambiente". Critério sem fonte local deve aparecer como "não verificável".
- Derive os cenários do contrato e da persistência. Cada cenário deve ter objetivo, pré-condições, passos, resultado esperado, nível (rota via aplicação, repositório com banco real ou migration) e a fonte que o sustenta, incluindo a ligação com o card. Considere, **apenas se o contrato ou os cards os definirem**, cenários como: emissão, uso válido, ausência, malformação, expiração, revogação, repetição de revogação, conta excluída ou inexistente e isolamento entre usuários. O que não estiver definido entra como lacuna, sem inventar o comportamento esperado; para esses casos, indique se o roteiro registra o comportamento atual como caracterização ou aguarda decisão.
- Indique o que o roteiro consegue validar com a composição montada dentro do teste e o que só seria validado com a composição de produção.
- Defina a estrutura da suíte: nomes e localização dos arquivos, fixtures, preparação do banco (migrations aplicadas até o head), isolamento entre testes, dependências do ambiente e como os testes que dependem de recurso ausente são ignorados com motivo explícito, sem gerar erro quando o ambiente não os suporta.
- Registre achados de back-end (divergências entre cards, contrato e código, comportamentos não definidos, riscos de segurança) em seção própria, sem corrigi-los.
- Indique a divisão de trabalho: o que fica com `$integration-system-testing-v1` (a suíte, em `nix develop .#tests`) e o que fica fora (o registro por card, documentação, correções de back-end, trabalho no GitHub). Especifique nomes de arquivos, ambientes e comandos, para a skill não precisar inventá-los.
- **Alterações temporárias de ambiente.** Registre que, para executar a suíte, a skill poderá aplicar alterações temporárias em `nix/tests.nix` (Python do backend e o driver SQLite assíncrono necessário) e, se a cadeia do Alembic estiver com revisões duplicadas, uma linearização temporária das migrations. Ambas devem ser revertidas com `git restore` ao final, com os diffs completos copiados para o resumo, e `git status --short` não pode listar nenhum arquivo em `nix/`, `flake.nix`, `flake.lock` ou `alembic/versions/`. Se já houver mudanças do usuário nesses caminhos, a skill não deve restaurá-las: deve parar e informar.
- Defina o roteamento do artefato de análise (pasta em `prompts/`) conforme a organização existente.
- Registre na validação: a execução da suíte em `nix develop .#tests`; a execução informativa da suíte completa em `nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src`, que não pode gerar erros novos em relação ao baseline observado; e o gate de lint do CI ao final de cada execução: `nix develop .#quality --command ruff check src/backend` (se falhar por I001, corrigir com `nix develop .#quality --command ruff check --select I --fix <arquivos-apontados>` e repetir o gate completo).
- Não implemente nada.
```

## Informações complementares

- O usuário forneceu as skills `.agents/skills/decision-analysis-v4/SKILL.md` e `.agents/skills/integration-system-testing-v1/SKILL.md`. A primeira rege esta análise. A segunda é destinatária do handoff; não foi invocada para implementar testes, pois não há referência de análise aprovada e o usuário proíbe implementação neste turno.
- A autorização de alterações temporárias pertence à execução futura. Nenhuma foi aplicada nesta análise.
- Esta é uma linhagem nova por determinação explícita do usuário. A análise histórica de rejeição de credenciais encontrada na base é contexto, não antecessora. Não se leu código de suíte de outras branches para transplantá-lo.

## Mudanças desde a versão anterior

Nenhum identificado — modo `initial`.

## Artefatos analisados

Os arquivos em `subjects.files` foram lidos nos recortes declarados. Para evitar omitir contexto efetivamente usado, a tabela completa abaixo complementa o frontmatter. Abreviações de caminho: **P** = `src/backend/infrastructure/persistence`; **T** = `src/backend/tests`; **S** = `.agents/skills`. Todos os caminhos abreviados são expansões literais, não globs de evidência. Estado WT = working tree limpo, baseado no HEAD `46a7a75d03ac9c9fec0eb2b109ba76f52d507a14`; conteúdo histórico tem revisão própria.

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| Todos os 19 arquivos de `subjects.files` | Conforme frontmatter | Conforme frontmatter | Conforme frontmatter | Conforme frontmatter | Conforme frontmatter | WT |
| `AGENTS.md`; `src/backend/AGENTS.md` | Contexto | prose | prompt-instruction | Markdown | Inteiros | WT |
| `S/decision-analysis-v4/SKILL.md`; `references/classification-taxonomy.md`, `output-schema.md`, `output-routing.md`, `artifact-classification.md` sob a mesma skill | Contexto | prose | prompt-instruction | Markdown | Inteiros | WT |
| `S/integration-system-testing-v1/SKILL.md` | Contexto | prose | prompt-instruction | Markdown | Texto fornecido pelo usuário | External, fornecido na conversa |
| `S/integration-system-testing-v1/references/analysis-input-contract.md`, `test-scope-boundary.md`, `test-fit-check.md`, `implementation-protocol.md` | Contexto | prose | prompt-instruction | Markdown | Inteiros; saída parcial do trecho de fit-check, usada somente para delimitação | WT |
| `docs/configuracao-ambiente.md` | Apoio | prose | documentation | Markdown | Ambientes Nix, variáveis, execução local e logs | WT |
| `docs/requisitos-seguranca.md` | Apoio | prose | schema-contract | Markdown | §§2.5–2.8, 2.11–2.12, 9; busca de referências a credenciais | WT |
| `docs/requisitos_funcionais.md` | Apoio | prose | schema-contract | Markdown | RF13 e questão aberta sobre método | WT |
| `docs/requisitos_nao_funcionais.md` | Apoio | prose | documentation | Markdown | RNF04, verificação proposta e questões abertas | WT |
| `docs/modelagem_der.md` | Apoio | diagram-model | schema-contract | Mermaid/Markdown | Inteiro | WT |
| `docs/matriz_testes.md` | Apoio | prose | test | Markdown | Objetivo, convenções e CT-RF13-01/02/03 | WT |
| `docs/interfaces-cadastro-31-32.md` | Contexto | prose | documentation | Markdown | Inteiro; precedente de registro, sem importar regras dos cadastros | WT |
| `docs/manual-git.md` | Contexto | prose | documentation | Markdown | Fluxo Git e PR para dev | WT |
| `prompts/README.md` | Contexto | prose | prompt-instruction | Markdown | Inteiro | WT |
| `prompts/backend/20261011-102943-rejeicao-requisicoes-sem-credenciais-validas-v004.md` | Contexto | prose | documentation | Markdown | Frontmatter, solicitação, evidência, escopo, limitações e handoff de contrato | WT; análise histórica v004 |
| `src/backend/api/perfil_estudante.py` | Apoio | source-code | production | Python | Principal, DTO de edição e handlers GET, PUT e DELETE | WT |
| `src/backend/application/perfil_estudante.py` | Apoio | source-code | production | Python | ExcluirPerfil, ConsultarPerfilEstudante e entradas/portas relacionadas | WT |
| `P/sqlalchemy/repositorio_usuario.py`; `P/sqlalchemy/usuario.py`; `P/sqlalchemy/metadata.py` | Apoio | source-code | production | Python | Inteiros | WT |
| `src/backend/infrastructure/security/senhas.py` | Apoio | source-code | production | Python | Inteiro | WT |
| `P/alembic/env.py`; `alembic.ini` | Apoio | source-code / structured-data | configuration | Python/INI | Inteiros | WT |
| `P/alembic/versions/*` | Apoio | source-code | schema-contract | Python | Somente linhas revision/down_revision de todos os arquivos, incluindo anotações de tipo; não conteúdo integral | WT; nomes completos na saída de busca descrita em F08 |
| `P/alembic/versions/20261015_0011_exclusao_logica_formacoes_academicas.py`; `20261015_0011_criar_cursos.py`; `20261015_0012_criar_links_profissionais.py`; `20261015_0012_criar_projetos_academicos.py`; `20261013_0004_adicionar_dados_consulta_estudante.py` no mesmo diretório | Apoio | source-code | schema-contract | Python | Inteiros | WT |
| `T/test_infrastructure_tokens_sessao.py`; `T/test_infrastructure_autenticador_sessao.py`; `T/test_api_acesso_estudante.py`; `T/test_api_sessoes.py` | Principal | source-code | test | Python | Inteiros | WT |
| `T/test_api_middleware_autenticacao.py` | Principal | source-code | test | Python | Lista de cenários, estrutura com stub/dispatch e testes de composição finais | WT |
| `T/test_integracao_rejeicao_requisicoes_sem_credenciais_validas.py`; `T/test_integracao_persistencia_dados_pessoais.py` | Principal / apoio | source-code | test | Python | Inteiros | WT |
| `T/test_main.py` | Apoio | source-code | test | Python | Classes, métodos e configuração de engine/lifespan | WT |
| `T/test_integracao_recusa_perfil_alheio.py`; `T/test_integracao_isolamento_dados_estudantes.py`; `T/test_integracao_isolamento_experiencias.py`; `T/test_integracao_rejeicao_referencia_curriculo.py` | Apoio | source-code | test | Python | Declarações de doubles, harness ASGI e nomes/objetivos dos testes por busca, sem leitura integral | WT |
| `.github/workflows/` (workflow encontrado pela busca `ruff check\|unittest`) | Contexto | structured-data | configuration | YAML | Linhas dos gates Ruff/unittest, não workflow integral | WT |
| Histórico Git local: commits discriminados em F02 | Principal | structured-data | documentation | Git | Mensagens de merge/commit, estatísticas e diff de contrato em f30d034 | Commit |

### Limites da evidência dos artefatos

A listagem de nomes não é leitura de conteúdo. Não se auditou cada teste de API que incidentalmente pode produzir 401. A avaliação cobre diretamente os módulos centrais acima e inventaria os testes integrados relacionados. O baseline executou a descoberta completa, mas execução não substitui leitura de cada teste. As evidências históricas não tornam verdadeiro hoje o estado descrito por uma análise antiga.

Não houve consulta ao GitHub, fetch ou leitura de texto remoto dos cards. Foram pesquisados `git log --all` (mensagens curtas e corpos nos arquivos de sessão), branches locais/remotas armazenadas, histórico dos arquivos e referências textuais em `docs/` e `prompts/`. A busca mais ampla por `#80`, `#81`, `#82` e variantes de card na árvore não encontrou texto desses cards. Isso demonstra ausência no recorte pesquisado, não inexistência no GitHub.

## Problema enriquecido

### Resultado desejado

Especificar uma suíte integrada executável, complementar aos unitários existentes, e um modelo auditável de resultado por card. A análise não certifica cards, não publica comentários e não implementa a suíte.

### Atores e interesses

Responsável pela suíte precisa de alvos e oráculos concretos; responsáveis pelos cards precisam distinguir atendimento do contrato de aceite histórico; backend precisa receber achados sem correção implícita; estudantes dependem da rejeição de sessões inválidas e de persistência sem segredo reutilizável.

### Evidências e fatos observados — (a) fatos encontrados

#### F01 — Base, instruções e descoberta

`git rev-parse HEAD` retornou `46a7a75d03ac9c9fec0eb2b109ba76f52d507a14`; `git log --all --oneline --decorate` mostra HEAD na branch `test-validacao-contrato-credenciai`, coincidente com `dev` e `origin/dev` locais. `git status --short` estava vazio antes da análise. Não se afirma atualidade com o servidor remoto.

`AGENTS.md`: “Toda ferramenta de desenvolvimento DEVE ser executada pelo ambiente Nix”; testes integrados usam `tests`, unitários usam o componente; Git opera fora do Nix. `src/backend/AGENTS.md`: testes respeitam camadas e domínio independente. A busca por `AGENTS.md` e `AGENTS.override.md` encontrou somente raiz, backend e frontend; nenhuma regra adicional em `docs`, `nix`, `prompts` ou na pasta candidata.

`prompts/README.md`: “backend/ — prompts relacionados ao desenvolvimento e à revisão do backend”. As subpastas imediatas encontradas foram `backend`, `ambientes`, `frontend`, `templates`, `revisao`, `requisitos`.

#### F02 — Cards, PRs e commits: o que é demonstrável localmente

| Card | Título/objetivo e origem | Aceite literal | Ligação demonstrada | Decisões, arquivos e testes | Exclusões explícitas |
|---|---|---|---|---|---|
| #80 | Não localizado; não atribuir título | Não localizado | Nenhum commit/PR inequivocamente vinculado | Nenhum trabalho atribuível com segurança a #80 | Não localizadas |
| #81 | Não localizado; não atribuir título | Não localizado | Nenhum commit/PR inequivocamente vinculado | Nenhum trabalho atribuível com segurança a #81 | Não localizadas |
| #82 | **Inferido**, “persistir revogação de sessão”, da mensagem a50905c e nome de branch; título oficial indisponível | Não localizado | Merge `8a6880a`: “Merge pull request #467 from code-alchemists-br/feature/82-sessao-revogavel”; segundo pai `a50905c` | Revogação por hash, data UTC, flush, atualização condicionada para não reescrever primeira revogação; router de logout e composição; `api/{factory,sessoes}.py`, `application/sessoes.py`, `P/sqlalchemy/repositorio_sessao.py`, `infrastructure/security/tokens_sessao.py`, `T/test_api_sessoes.py`, `T/test_infrastructure_tokens_sessao.py` | Nenhuma exclusão atribuível literalmente ao card; limites do contrato são separados |

A ligação #82→PR #467 usa o número **na branch de origem**, não a numeração da PR. `git show --stat a50905c` indica sete arquivos, 315 inserções e quatro remoções; os dois módulos de teste usam doubles, não banco real.

Trabalho relacionado, integrado à história do HEAD, **sem atribuição silenciosa a #80/#81**:

| Artefato Git | Trecho identificador | Trabalho e arquivos relacionados |
|---|---|---|
| `575006e`; merge `647a2b0` / PR #458 / `feature/contrato-credenciais-sessao` | “docs: define contrato de credenciais de sessão” | Contrato e referência em `docs/requisitos-seguranca.md`; `1627442` integra interface protegida; `d049892` consolida guias. Não há número #80 no vínculo lido |
| `13979d8`; merge `d98e3a7` / PR #461 / `feature/emissao-token-acesso` | “feat: emite token de sessão no login” | Login, retorno de UsuarioId, portas, criador, modelo, repositório, metadata e migration; `test_api_acesso_estudante.py`, `test_application_acesso_estudante.py`, `test_infrastructure_tokens_sessao.py`. A estatística não equivale à leitura integral do teste de Application |
| `746fd35`; merge `dc71962` / PR #463 / `feature/sessao-revogavel` | “feat: permite revogar sessão do estudante” | Logout e revogação; sete arquivos. Há também merge `8f86c32` / PR #470 da branch sem número. Não deduzir outros cards dessas sobreposições |
| `4b2f89a`; merge `b39ea23` / PR #464 / `feature/autenticacao-sessao` | “feat: protege rotas com sessão persistida” | Middleware, autenticador, consulta, testes de middleware, sessão e infraestrutura. Merge `fea8f24` / PR #468 menciona `feature/83-middleware-autenticacao`, evidência de trabalho adjacente #83, não de #80/#81 |
| `d6ba138`; merge `2748d21` / PR #515 / `fix/autenticacao` | “proteger app sem autenticador de sessão” | Fallback fechado e evolução do teste integrado de rejeição, cujo histórico também contém #149 (`38e3fc1`, `c39d9a8`) |
| `f30d034`; merge `11e9389` / PR #545 / `docs/card-418-contrato-credenciais-sessao` | “align credential session contract with implementation” | Atualização normativa/descritiva atual; não atribuir ao card #80 nem tratá-la como aceite retroativo |

`git log --all` também revelou `eca8708` em outra branch e branches com nomes de suíte/validação de credenciais. Esses nomes são descoberta de histórico, não evidência de testes na base; seu conteúdo não foi importado. Na árvore atual não foi localizado roteiro específico nem registro preenchido para #80–#82.

#### F03 — Contrato definido hoje

Fonte primária de interface: `docs/contrato-credenciais-sessao.md`; `docs/requisitos-seguranca.md` §9 diz “Esse contrato é a fonte detalhada da interface HTTP”.

| Assunto | Trecho do contrato | Implementação lida que o materializa |
|---|---|---|
| Natureza | “opaca e mantida no servidor”; “32 bytes”; “Base64 URL-safe sem padding” | `tokens_sessao.py`: `secrets.token_bytes(32)`, codificação URL-safe e remoção de `=`; representação emitida tem 43 caracteres |
| Armazenamento | “somente seu resumo SHA-256, com índice único, nunca o token em claro” | `sessao.py`: `String(64), nullable=False, unique=True`; criador calcula hexdigest |
| Transporte | “exclusivamente por cookie”; não aceitar Authorization, query ou corpo | `middleware_autenticacao.py`: `request.cookies.get(COOKIE_SESSAO)`; `api/sessoes.py`: alias `__Host-sessao` |
| Cookie | `Path=/; Max-Age=28800; Secure; HttpOnly; SameSite=Lax`; sem Domain | `cadastro_acesso.py` usa esses atributos, sem exceção local HTTP |
| Prazo | “no máximo 8 horas”; “Não há renovação automática” | Criador `_DURACAO=timedelta(hours=8)`; consulta exige `expira_em > instante`, sem update por atividade |
| Login | `204 No Content`; em falha de conta inexistente/excluída/senha incorreta: `401` uniforme e sem cookie | `AcessarEstudante.executar` rejeita conta ausente/excluída/senha incompatível; handler responde “E-mail ou senha não conferem.” |
| Formato do login | Campos ausentes/limites do DTO: `422`; e-mail estruturalmente inválido aceito pelo tamanho: `401` | DTO senha 8–1024, email 3–320; handler captura `RegraDeDominioViolada` e `CredenciaisInvalidas` |
| Indisponibilidade | Acesso/criador não configurados: `503`, sem cookie | Guardas do handler em `cadastro_acesso.py` |
| Validade | Registro existe, revogação nula, expiração posterior, conta existe e `deleted_at` nulo | `repositorio_sessao.py`: SELECT com JOIN usuários e os filtros; autenticador calcula SHA-256 UTF-8 em cada chamada |
| Falhas em rota protegida | “401 antes de chamar o handler” se falhar condição | Middleware retorna `{"detail":"Sessão ausente ou inválida."}`; ausência e desconhecimento são uniformes |
| Principal | “UUID autenticado em request.state.usuario_id” | Middleware grava `usuario_id.valor`, não token/hash nem identidade declarada no cliente |
| Logout | `DELETE /sessao/atual`, `204` para ausente/desconhecida/expirada/já revogada, remove cookie; com cookie e sem revogador: `503` | `api/sessoes.py`: só chama revogador se token presente; sem token limpa cookie mesmo sem serviço |
| Escopo de logout | “revoga somente o registro associado ao token apresentado”; mais de uma sessão ativa | UPDATE por hash e `revogada_em IS NULL`; preserva primeira data, não toca outros hashes |
| Conta excluída | “invalida todas as sessões”; validação rejeita imediatamente conta excluída | JOIN com `usuarios.deleted_at IS NULL`; não há revogação física de todas as linhas nesse fluxo |
| Públicos | Cadastro, login, logout, documentação, health/readiness e OPTIONS | `ROTAS_PUBLICAS` contém os pares exatos; OPTIONS liberado independentemente de caminho |
| Limites | “não implementa validação de Origin, token CSRF nem limitação de tentativas” | Não há essas etapas no middleware/login lidos; não certificá-las |

As credenciais da conta são email/senha no JSON; a credencial de sessão é o token opaco, não a senha nem o UUID. O contrato documenta scrypt N=16384, r=8, p=1, salt 16 bytes e saída 64 bytes; `infrastructure/security/senhas.py` serializa parâmetros, deriva com `hashlib.scrypt` e compara com `hmac.compare_digest`. A suíte proposta exercita login real com esse adapter, sem refazer seus testes unitários criptográficos.

`docs/requisitos_funcionais.md` RF13: “exigir autenticação para acesso às informações pessoais e aos currículos”. `docs/requisitos_nao_funcionais.md` RNF04 exige usuários autorizados, mas declara regras a detalhar. `docs/matriz_testes.md` CT-RF13-01/02/03 cobre acesso autenticado e negativa sem sessão; não define como fechar cards nem equivale a teste executado.

#### F04 — Persistência definida e detalhes apenas implementados

`P/sqlalchemy/sessao.py`, `SessaoRegistro`: tabela `sessoes`, PK UUID `id`; FK não nula `usuario_id → usuarios.id`; hash único não nulo `String(64)`; `criada_em`/`expira_em` não nulos `DateTime(timezone=True)`; `revogada_em` anulável. `20261012_0004_criar_sessoes.py` declara `down_revision="20261007_0003"`, cria os seis campos, FK `fk_sessoes_usuario_id_usuarios`, unicidade `uq_sessoes_token_hash` e PK. O índice único mencionado no contrato é representado por constraint UNIQUE; não há `create_index` separado nessa migration. Não afirmar formato físico de índice sem inspecionar o banco.

Não há CHECK de comprimento/hexadecimal do hash, de duração de oito horas, de ordem de datas ou de data de revogação; o tamanho SQL String(64) não equivale a validação hexadecimal. Não há índice explícito de usuario_id ou expira_em nem cascade de exclusão no trecho lido. Esses controles não serão inventados no teste.

`repositorio_sessao.py`: `salvar` usa `uuid4()`, adiciona linha e faz `flush`; `revogar_por_hash` faz UPDATE condicionado ao hash e revogação nula, seguido de flush; não faz commit/rollback. A responsabilidade transacional externa é documentação do adapter, **não política HTTP definida pelo contrato**. O SELECT retorna `UsuarioId` ou `None`, sem materializar token. Uma sessão expirada não precisa ter revogada_em preenchida para ser rejeitada; logout pode preencher revogação de linha expirada, pois seu UPDATE não filtra expiração.

Não foi localizada entidade de domínio de sessão na busca `sess` em `src/backend/domain`; o artefato concreto é o registro ORM e as portas em `application/sessoes.py` e `application/autenticacao_sessao.py`. Não introduzir entidade nova.

#### F05 — Composição real e alcance de prova

`api/factory.py`, `create_app`: `if autenticador_sessao is not None: app.add_middleware(...)`. Sem autenticador a fábrica não instala o middleware, comportamento explicitamente testado em `test_api_middleware_autenticacao.py`.

`main.py`: `app = create_app(autenticador_sessao=AutenticadorSessaoIndisponivel(), verificador_persistencia=..., lifespan=...)`. O adapter `autenticador_sessao_indisponivel.py` faz `return None` para qualquer token. A engine criada quando há DATABASE_URL é usada para readiness; não é convertida em repositório de sessões, criador, login ou revogador. Esses argumentos permanecem ausentes.

Implicações derivadas das guardas lidas: a app exportada protege rotas privadas com 401 inclusive com token válido de outro banco; login com DTO válido encontra acesso não configurado e responde 503; logout sem cookie responde 204, mas com cookie encontra revogador ausente e responde 503. O baseline atual prova apenas o que seus testes exercitam, não uma jornada de login→banco→sessão na app exportada.

`api/sessoes.py` registra somente DELETE. O contrato atual diz “Não existe atualmente uma rota GET /sessao/atual”. Portanto sua ausência não é violação desse contrato atual, mas é divergência em relação à versão inicial, descrita em F09. Não criar endpoint ou usar GET inexistente como controle positivo de autenticação.

#### F06 — Cobertura já existente, por nível

| Fonte em T/ | Evidência/trecho | Nível e limite | Complemento necessário |
|---|---|---|---|
| `test_api_acesso_estudante.py` | `AcessoExecutorStub`, `CriadorSessaoStub`, chamada direta de `handler` | Unitário de borda: atributos do cookie, identidade encaminhada e falha/log sem segredo; não atravessa HTTP real/DB | Login ASGI com Application, scrypt e repositórios reais |
| `test_api_sessoes.py` | `_handler(...)(resposta, token)` e `RevogadorSessaoStub` | Unitário: limpeza do cookie, ausência de token, 503 sem revogador, registro no OpenAPI | Idempotência e escopo reais em banco, reuso negado |
| `test_infrastructure_tokens_sessao.py` | `RepositorioSessaoStub`, `AsyncSessionDouble`, `patch.object(migration,"op")` | Unitário: token 43 caracteres/hash/8h, UTC, Unicode no revogador, flush e SQL condicionado, metadata e DDL simulado | Constraints e dados após commit/reabertura; DDL Alembic aplicado |
| `test_infrastructure_autenticador_sessao.py` | `ConsultaSessaoStub`, `AsyncSessionConsultaDouble`, `comando.compile()` | Unitário: hash UTC, None, fallback; filtros SELECT/JOIN/deleted_at como texto SQL | Execução dos filtros com linhas reais e igualdade no limite de expiração |
| `test_api_middleware_autenticacao.py` | `AutenticadorSessaoStub`, dispatch direto e inspeção `user_middleware` | Unitário: ausência/inválido/válido, state, públicos, várias propriedades, correlação, composição opcional e fallback | Integração autenticador persistido→middleware→router |
| `test_integracao_rejeicao_requisicoes_sem_credenciais_validas.py` | importa `backend.main.app`; `@unittest.skip("a aplicação ainda não compõe persistência de sessões")` | Integração ASGI real sem banco: ausência e inválido; expirada/revogada ignorados | Não usar os dois skips como evidência de validade/revogação |
| `test_integracao_persistencia_dados_pessoais.py` | `sqlite+pysqlite://`, `Base.metadata.create_all`, nova Session | Banco real síncrono para campos pessoais; não testa repositório assíncrono de sessão nem migrations até head | Banco assíncrono migrado de sessão |
| `test_integracao_recusa_perfil_alheio.py` e integrados de isolamento | `AutenticadorDeterministico` / `AutenticadorEstudanteA`, repositórios em memória | ASGI com identidades dadas por doubles; não valida token persistido | Isolamento de sessões/identidade com repositório real; não importar 404 de outros recursos |
| `test_main.py` | patch de `create_async_engine`, testes de ausência/URL/lifespan | Unitário da composição de readiness | Separar certificação da composição de autenticação de produção |

Não se encontrou na árvore atual um módulo dedicado a executar o contrato de sessão com banco real migrado. O novo roteiro não repetirá testes isolados de parâmetros de scrypt, geração aleatória, compilação de SQL ou listas exaustivas de handlers já cobertas por unitários. Repetir alguns status é necessário para provar as fronteiras integradas, não para aumentar contagem.

#### F07 — Precedentes e significado do registro

`docs/interfaces-cadastro-31-32.md` é precedente explícito: “Resultados reais no Nix”, comandos, contagens, skips, limites e PR referenciando issues. Diz “Os handlers são chamados diretamente: esses testes não provam trânsito HTTP real, autenticação completa, banco”. Isso sustenta o formato de evidência, não regras de credenciais.

`docs/manual-git.md` diferencia push de PR, com revisão e destino dev. Não foi localizada regra geral exigindo comentário no card nem local padronizado de resultado por card. A análise histórica de rejeição em `prompts/backend/...v004.md` é especificação de lacuna, não registro atual de atendimento. Não há evidência de que os cards #80–#82 tenham sido validados só por haver documentação.

#### F08 — Ambiente e bloqueios preexistentes

`nix/tests.nix`: `packages = [ pkgs.git ];`. Não declara Python, dependências backend, driver SQLite assíncrono, PostgreSQL ou SQLite CLI. `nix/backend.nix` usa `pkgs.python3.withPackages backendPythonPackages`; `nix/backend-python-packages.nix` declara fastapi, uvicorn, sqlalchemy, alembic, psycopg e pydantic-settings, sem aiosqlite e sem httpx. `flake.nix` oferece backend/frontend/tests/quality; não oferece serviço de banco.

`alembic.ini` aponta `script_location = src/backend/infrastructure/persistence/alembic` e `prepend_sys_path = src`; `P/alembic/env.py` exige DATABASE_URL e usa engine assíncrona, sem iniciar a API. Não há banco provisionado por essas configurações.

Revisões duplicadas, verificadas por busca em **todas** as declarações `revision`/`down_revision`, inclusive anotadas:

| Revisão | Arquivos em P/alembic/versions | Relação atual |
|---|---|---|
| `20261015_0011` | `20261015_0011_criar_cursos.py`; `20261015_0011_exclusao_logica_formacoes_academicas.py` | Ambos descendem de `20261015_0010` |
| `20261015_0012` | `20261015_0012_criar_links_profissionais.py`; `20261015_0012_criar_projetos_academicos.py` | Ambos descendem do identificador ambíguo `20261015_0011` |

A revisão de documentos `20261016_0013` depende de `20261015_0012`, depois experiências `20261017_0014` e ordem de seções `20261017_0015`. Há merges declarados de ramos anteriores (`20261014_0009` e `20261015_0010`); múltiplos pais por si só não significam defeito.

Inspeção real `nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 alembic heads`, exit 0, emitiu warnings “Revision 20261015_0011 is present more than once” e idem `0012`, imprimindo `20261015_0011`, `20261015_0012`, `20261017_0015 (head)`. Não interpretar isso como grafo válido de head única: identificadores duplicados tornam a resolução ambígua. Não se aplicou upgrade e não se afirma erro específico de upgrade não observado.

#### F09 — Divergências e fonte preferível, sem resolução silenciosa

| Divergência | Fontes/trechos | Fonte mais confiável para qual pergunta e encaminhamento |
|---|---|---|
| Contrato inicial previa `GET /sessao/atual` 200 com usuario_id; atual diz não existir | `git show 575006e:docs/contrato-credenciais-sessao.md`, seção Consultar sessão; diff `f30d034` remove a operação; `api/sessoes.py` só DELETE | Para comportamento atual: código e contrato atualizado convergem. Para aceite histórico: texto original é evidência de escopo proposto, mas não prova que era aceite de #80/#81. Expor a retirada no registro; não inventar teste de 200 nem chamar ausência de implementação de sucesso histórico |
| CSRF/Origin obrigatórios no contrato inicial; atual admite ausência | `575006e`: “operações que alteram estado DEVEM validar ... Origin ... e aplicar proteção CSRF”; `f30d034` e seção Limites atual | Para garantia de segurança, não considerar edição documental como implementação. Código lido confirma ausência no fluxo. Não criar oráculos de CSRF; remeter a produto/segurança a aceitação do risco e escopo histórico |
| Segurança exige proteção contra excesso; contrato diz que cards não a configuram | `docs/requisitos-seguranca.md` RF-AUT-08 versus contrato §Criar sessão/limites | Requisito geral continua evidência de necessidade, contrato atual descreve ausência. Não afirmar cumprimento de RF-AUT-08; não inventar 429, limiar ou tarefa de correção |
| Generalização de 403 no contrato versus GET perfil alheio com 404 | Contrato: “Nas verificações de propriedade implementadas ... 403”; `api/perfil_estudante.py`, consultar: `if principal_id != usuario_id: ...404` | Código é evidência direta do comportamento da rota; contrato é oráculo normativo, portanto existe divergência. Usar PUT perfil, explicitamente listado no contrato, para 403 de isolamento; não generalizar resultado para GET nem transpor 404 de formação/currículo |
| Análise histórica diz que não existe validador e propõe xfail/503; código atual tem middleware e fallback | `prompts/backend/...rejeicao...v004.md`, limites; `main.py`, `autenticador_sessao_indisponivel.py` e teste integrado atual | Código e testes atuais prevalecem para estado atual. Preservar análise histórica; não copiar xfail de estado superado |
| Contrato manda testes de regras por doubles; usuário quer roteiro integrado com banco | Contrato §§Testes de rotas protegidas/Testes de contrato: “não devem usar banco ou relógio real para validar regras”; demanda atual exige integração/persistência | Pedido atual autoriza complemento integrado; manter unitários determinísticos existentes e controlar relógio no novo teste. Banco real verifica colaboração/DDL, sem trocar política nem reescrever contrato |
| DER omite token_hash de SESSAO | `docs/modelagem_der.md`, SESSAO tem id, usuario_id e datas; contrato e `sessao.py` têm token_hash | Para schema atual: ORM Code First e migration conforme AGENTS backend; DER é visão incompleta. Registrar achado documental, não remover hash nem inventar coluna em teste |
| Iniciar app com banco não compõe autenticação | Guia de ambiente mostra DATABASE_URL e readiness; `main.py` usa engine apenas no verificador | Código de composição é evidência direta; guia não promete runtime autenticado. Não afirmar que configurar URL resolve sessões |

#### F10 — Execuções reais desta análise, não resultados de cards

| Execução | Ambiente/resultado observado | Alcance |
|---|---|---|
| `nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src` | Primeira tentativa bloqueada pelo sandbox: lock `/nix/var/nix/db/big-lock` somente leitura. Repetida com execução autorizada fora do sandbox: exit 0, **781 testes em 9,708s, OK (skipped=2)**, Python Nix 3.14.7 identificado no traceback de warnings | Baseline informativo solicitado. Zero failures/errors/expected failures no resumo; avisos de depreciação 422 e asyncio existentes. Dois skips são expirada/revogada do teste integrado de fallback |
| `nix develop .#quality --command ruff check src/backend` | Exit 0, “All checks passed!” | Gate de lint após baseline; sem I001 a corrigir |
| `nix develop .#tests --command sh -c 'command -v python3 \|\| true; command -v postgres \|\| true; command -v sqlite3 \|\| true'` | Exit 0; somente `/usr/bin/python3` foi encontrado | Evidência de PATH herdado, não Python Nix disponível. Nenhum Python global foi executado. Ausência de executáveis de banco nessa inspeção não prova ausência de serviço externo; não houve conexão externa |
| Inspeção `alembic heads` de F08 | Backend Nix, exit 0 com warnings de duplicação | Inspeção de metadados, não teste de migration aplicada |

A suíte nova não existe nem foi executada neste turno. As contagens acima não são veredito de #80, #81 ou #82. Nenhum resultado futuro foi preenchido. A informação do baseline completo em backend é exceção explicitamente solicitada pelo usuário; os novos integrados executam formalmente em `tests`.

### Hipóteses

H1: SQLite assíncrono com migrations temporariamente desambiguadas permitirá testar a colaboração sem banco externo; ainda não executado, logo não é fato. H2: pode-se atribuir parte dos trabalhos sem número aos cards #80/#81 após obter seus textos e vínculos; não assumir qual parte. H3: a mudança documental f30d034 não encerra automaticamente compromissos históricos; precisa de confirmação de escopo.

### Perguntas em aberto — (b) lacunas

Cada linha registra ausência de definição no recorte lido, opções viáveis, recomendação e responsável. Bloqueios definidos por artefatos não são lacunas de definição; ficam em F08 e nos achados.

| ID | Lacuna | Opções viáveis | Recomendação e justificativa | Depende de produto? |
|---|---|---|---|---|
| L01 | Texto oficial e aceite dos três cards; vínculo #80/#81→trabalho | Fornecer export/texto local com links de PR/commits; ou manter rastreio inconclusivo e validar contrato atual | Prosseguir com suíte do contrato; solicitar título, descrição, critérios, exclusões, decisões e referência inequívoca de PR/commit de cada card. Critérios oficiais ficam não verificáveis até lá | Sim, dono dos cards confirma escopo; descoberta dos vínculos é técnica |
| L02 | Título oficial #82 e aceite; só branch/mensagem disponíveis | Tratar mensagem como título; ou rotular inferência e obter texto | Rotular inferido e preservar vínculo #82→467; evita confundir implementação com aceite | Sim para confirmar aceite |
| L03 | Semântica detalhada de credencial malformada: gramática de entrada, limites, cookies duplicados, escapes | Exigir sintaxe rígida mediante decisão; ou caracterizar valores aceitos pelo parser como desconhecidos | Caracterizar `__Host-sessao=nao-base64!` e valor vazio sem registro, com 401 derivado da inexistência, não da gramática. Casos duplicados/limites/bytes ilegais aguardam decisão; não inventar 400/422 ou tamanho máximo | Sim para novo contrato; caracterização simples é técnica |
| L04 | Tratamento HTTP de falha de banco/flush/commit durante emissão/validação/revogação | Definir status/atomicidade via produto/arquitetura; ou observar sem impor aceitação | Fora da matriz de aceite; se ocorrer na execução, registrar erro como achado, sem converter para 503 inventado. Exercitar rollback do repositório apenas como caracterização da responsabilidade externa | Sim para resposta pública; técnica para transação do harness |
| L05 | Forma e destino obrigatório de “resultado contra card” | Documento no repo + texto para PR/card; só descrição de PR; só comentários no card | Documento futuro `docs/validacao-contrato-credenciais-cards-80-82.md` e três blocos prontos para colar. Segue precedente docs/interfaces..., sem depender de GitHub | Não para modelo local; publicação/fechamento requer ação explicitamente autorizada |
| L06 | Não há receita de banco assíncrono no shell tests nem URL de teste dedicada | SQLite descartável; PostgreSQL local já disponível; ambos | SQLite como base obrigatória quando dependências presentes; PostgreSQL opcional para fidelidade de dialeto, sem provisionamento permanente. Criar variável exclusiva de teste, nunca reutilizar DATABASE_URL herdada | Técnica |
| L07 | Nenhum artefato define cenário de órfão de sessão permitido com FK ativa | Desabilitar FK para forjar corrupção; ou testar FK e recusar cenário impossível no schema válido | Testar FK com usuário inexistente e login de conta inexistente. JOIN observado é evidência estática da rejeição de órfãos; não alegar prova dinâmica desse estado nem enfraquecer FK | Técnica; produto só se desejar contrato de recuperação de corrupção |
| L08 | Retenção exata e rotina de limpeza de sessões não definidas | Definir política e job; ou excluir teste de limpeza | Excluir; contrato apenas permite limpeza e não fornece prazo nem executor | Sim, produto/segurança |
| L09 | Critérios de aceitação histórica após retirada de GET sessão e CSRF | Adotar contrato atual para todos os cards; ou separar versão atual de compromisso histórico | Separar: suite valida contrato atual, registro explicita alteração e não encerra card sem aceite original/decisão | Sim |
| L10 | Matriz exaustiva de rotas a validar integrada, além dos unitários, não está especificada | Repetir todas as rotas com banco; ou integração representativa e inventário dos unitários | Selecionar login/logout, GET próprio e PUT alheio. Declarar que não prova “cada rota” do contrato; cobertura exaustiva é handoff separado | Técnica para suíte mínima; produto se “todas as rotas” for aceite de card |
| L11 | Contrato de indisponibilidade da composição de produção e prazo para completá-la não definidos | Criar runtime no teste como se fosse produção; ou separar e mostrar limitação | Separar composições; não modificar main. Handoff de backend para wiring real, sem assumir que pertence a #80–#82 | Técnica para honestidade da prova; produto para prioridade |

### Escopo

Definir suíte ASGI+Application+segurança+SQLAlchemy+banco migrado, cenários de repositório/DDL, protocolo temporário de execução e modelo de registro. As decisões técnicas propostas podem ser avaliadas sem conhecer o texto dos cards; o fechamento histórico dos cards permanece não verificável. `status: proposed` aprova uma proposta de teste do contrato atual, não o aceite dos cards sem fonte.

### Fora do escopo

Correções de produto, contrato, middleware, ORM, migrações permanentes, composição, frontend, CSRF/rate limiting novos, redefinição de senha, limpeza, CI/deploy, chamadas externas, publicação no GitHub e fechamento de cards. A exceção temporária de ambiente/migrations é exclusivamente para execução futura e não constitui correção entregue.

### Critérios de sucesso

Suíte com cenários/fontes/oráculos abaixo, sem mocks de persistência no fluxo integrado; execução em tests identificando Python Nix e dialeto; migrations até head sem create_all como substituto; resultado distingue pass/fail/skip/bloqueio; regressão completa sem erros novos comparada ao baseline; lint completo aprovado; nenhuma alteração permanente nas áreas protegidas; registro por card explicita critérios inferidos e critérios não verificáveis.

## Restrições aplicáveis

Uma única escrita nesta atividade: este Markdown. Não implementar decisões nem executar alterações temporárias agora. Skills e AGENTS se aplicam aos caminhos reais, inclusive migrations dentro do backend. Toda classe/função futura, inclusive fixtures/helpers, precisa documentação de o que/como/finalidade. Comentários de proveniência devem indicar exatamente este arquivo e `#v001` nos novos testes.

Credenciais sintéticas não devem aparecer em logs/relatórios: registrar IDs de cenário, códigos HTTP e comparações booleanas/hash mascarado; redigir Cookie/Set-Cookie nas evidências. Não usar banco de produção/compartilhado nem DATABASE_URL herdada como autorização.

## Classificação comentada

`engineering` domina: escolha de desenho da integração. `integration`, `security` e `data` cobrem fronteiras, credenciais e persistência. Incerteza alta é documental/histórica e de ambiente, não ausência de contrato atual. Risco alto é atribuir garantia indevida de autenticação ou fechamento de cards; análise e testes são reversíveis.

## Decisão de roteamento

Selecionar `prompts/backend`, diretamente, conforme inventário F01 e `prompts/README.md`. `ambientes` é candidata de apoio, `requisitos` trataria mudança do contrato, `revisao` privilegiaria auditoria; o objetivo central é um handoff de testes de backend. `frontend` e `templates` não correspondem ao objeto. Confiança alta; nenhuma pasta nova criada.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | Muito alta | Oráculos com fonte e resultado de execução | Impede confundir descrição, skip e prova |
| security | Muito alta | Token só no cookie, hash no banco, invalidação e isolamento | Risco concreto de credencial reutilizável |
| interoperability | Alta | SQLite e PostgreSQL distinguidos | Dialetos não provam as mesmas propriedades |
| simplicity | Média | Poucos fluxos integrados sem refazer unitários | Reduz manutenção |
| operability | Alta | Execução reproduzível e cleanup explícito | Ambiente atual é insuficiente |

## Alternativas consideradas

**Estado atual:** unitários/doubles e integração de fallback; sem prova de repositório de sessão com banco migrado. Não atende ao roteiro integrado solicitado.

**A — SQLite obrigatório quando suportado + PostgreSQL opcional, ASGI montada com componentes reais e verificação separada da app exportada.** Testes complementares e portáveis, dependências temporárias mínimas; risco de cobertura menor do dialeto de produção explicitado.

**B — PostgreSQL local exclusivo como único banco da suíte.** Viável quando o serviço dedicado existe; maior fidelidade de timezone/constraints, mas todos os cenários com persistência ficam ignorados sem esse serviço e o Nix não o provisiona hoje.

**C — Aguardar saneamento permanente de ambiente e wiring para testar somente backend.main.app.** Viável como ordenação de entregas, preserva pureza da composição de produção, mas adia a prova dos componentes já implementados; não pode chamar alterações de produto de parte desta suíte.

Roteiro apenas manual/doubles não é alternativa admissível para a entrega executável solicitada. Alterar backend para passar testes viola escopo. Nenhuma alternativa autoriza fechar #80/#81 por proximidade temática.

## Perfil de pagamento comparativo

Escala ordinal relativa ao estado atual; não somar. Valores não são probabilidade nem medida cardinal.

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| correctness | 1 | +2 | +2 | +1 | Média | A/B exercitam componentes reais; C adia; F05/F06 |
| security | 1 | +1 | +1 | 0 | Média | Prova limitada às fronteiras executadas, sem implementar controles ausentes |
| interoperability | 2 | +1 | +2 | 0 | Média | PostgreSQL é alvo operacional do guia; SQLite é precedente local |
| simplicity | 3 | +1 | 0 | +1 | Média | A requer driver/harness; B serviço; C dependências de outras entregas |
| operability | 2 | +2 | -1 | -1 | Alta | Shell tests só tem Git; A reduz dependência de serviço externo |

## Histórico e decisão atual — (c) recomendações

### Decisão da versão anterior

Nenhum identificado.

### Decisão recomendada nesta versão

Adotar A, com cenários integrados derivados do contrato atual e persistência, sem prometer fluxo de produção. Autorizar futuramente somente suporte temporário descrito abaixo, com reversão e evidência integral. Usar registro local e blocos para cards; manter #80/#81 e aceite oficial de #82 não verificáveis até disponibilização de fonte. Esta escolha é técnica; L01/L02/L09 exigem confirmação dos donos dos cards para veredito global.

### Impacto da revisão

Nenhum identificado — primeira versão, análise nova. A descoberta de documentação histórica não cria linhagem de revisão.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | Separação entre oráculo, caracterização e estado de execução | F06 e modelo por card |
| security | prioritized | Prova de não armazenar segredo e de revogação persistida | F03/F04; execução ainda futura |
| operability | prioritized | Base local independente de servidor | H1, dependente de execução |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| simplicity | Sem novas regras/abstrações de produto | Fixtures e transações só em testes |
| interoperability | SQLite obrigatório se disponível; PostgreSQL explicitamente opcional | Não extrapolar prova SQLite para timezone/produção |

## Roteiro executável proposto

### Estrutura e composição, sem implementação neste arquivo

Arquivos novos propostos, respeitando convenção de `unittest` em T/:

| Arquivo | Responsabilidade e nível |
|---|---|
| `src/backend/tests/test_integracao_contrato_credenciais_sessao.py` | Rotas ASGI reais de login/logout/perfil, middleware e serviços reais com banco; `integration`/contrato HTTP e segurança funcional |
| `src/backend/tests/test_integracao_persistencia_sessao.py` | Repositório real, commit/reabertura, filtros, constraints e migration aplicada; `integration` |
| `src/backend/tests/test_integracao_composicao_credenciais_sessao.py` | Caracterização separada de backend.main.app, sem overrides de auth; `system-acceptance-e2e` no nível API ASGI, sem navegador |
| `src/backend/tests/fixtures/credenciais_sessao.py` | Banco temporário, massa, clock controlado, montagem da aplicação e helper HTTP ASGI, exclusivamente suporte integrado |

Usar `unittest.IsolatedAsyncioTestCase`; imports opcionais somente após detecção de recursos, para evitar ModuleNotFoundError na descoberta. Se sqlalchemy/fastapi não existirem, não importar módulos produtivos que dependam deles antes do gate. Faltar Python Nix é bloqueio do comando, não skip de unittest possível; corrigir apenas pelo suporte temporário autorizado, nunca usar `/usr/bin/python3`.

Reutilizar abordagem de ASGI manual com coleção de eventos de `T/test_integracao_recusa_perfil_alheio.py`: entregar `http.request` uma vez, aguardar finalização antes de `http.disconnect`, com timeout explícito para detectar resposta incompleta. Não copiar o helper que desconecta imediatamente sem avaliar corpo. Usar `scheme=https`, host `testserver`, corpo JSON real e inspeção de status/headers/body; não exige httpx. Isso não prova TLS real nem comportamento de cookie em navegador. Nunca acrescentar endpoint fictício de sessão nem ignorar o middleware no controle positivo.

No harness, `create_app` recebe `AcessarEstudante(RepositorioUsuarioSqlAlchemy, DerivadorSenhaScrypt)`, `CriadorSessaoSeguro`, `RevogadorSessaoSeguro`, `AutenticadorSessaoPersistida(RepositorioSessaoSqlAlchemy)` e casos reais `ConsultarPerfilEstudante`/`EditarPerfil` quando usados. Os adapters compartilham AsyncSession do contexto do teste; não usar double para autenticação ou repositório. Um proxy de observação pode contar chamadas ao caso real de perfil, delegando integralmente; ele não fabrica identidade nem resultados. Isso permite provar “handler/caso de uso não alcançado” com contador zero mais snapshot de banco.

Commit é responsabilidade **do harness**, depois de cada operação concluída, antes de desmontar a app e abrir outra AsyncSession/app para ler o estado. Em erro, rollback. A prova será de persistência sob transação controlada pelo teste; não afirmar que produção faz commit antes de devolver Set-Cookie. Esse limite permanece explícito no relatório. Não tentar corrigir a ausência de Unit of Work produtivo.

Na caracterização de produção, importar `backend.main.app` sem overrides de autenticação, com DATABASE_URL deliberadamente removida antes do import e restaurada no cleanup do processo de teste; não conectar a URL herdada. Se módulo já estiver carregado com engine externa, usar processo separado pelo mesmo Python Nix com ambiente filtrado. Não editar/recarregar main para injetar serviços. Não repetir as duas negativas ASGI já existentes sem propósito: novos casos caracterizam login 503/logout e ausência de fluxo válido; manter os testes existentes como evidência do fallback.

### Banco e fixtures

1. Cada teste com banco usa `TemporaryDirectory` exclusivo, SQLite em arquivo `sessao.sqlite3`, URL `sqlite+aiosqlite:///...`, engine descartada em teardown, sem dependência da ordem dos casos. Arquivo, em vez de memória isolada por conexão, permite aplicar migrations em processo separado e reabrir sessões.
2. Aplicar **todas** as migrations até `head` via Alembic, na raiz, com DATABASE_URL exclusivamente do banco temporário. Não `create_all`, não `stamp head`, não aplicar só a revisão de sessões. Setup verifica head/ausência de duplicação na árvore temporária, depois colunas de usuários necessárias ao login/deleted_at.
3. Ativar `PRAGMA foreign_keys=ON` em **cada** conexão SQLite de fixture e consultar o valor antes dos testes de FK. Não chamar rejeição de órfão de “pass” com FK desativada.
4. Massa: usuários A/B com UUIDs `10000000-0000-4000-8000-000000000001` e `...0002`, nomes “Pessoa A”/“Pessoa B”, emails `a@example.test`/`b@example.test`, senha sintética `Senha-Teste-123` derivada pelo adapter real; terceiro email não cadastrado `ausente@example.test`. Nenhum dado pessoal real.
5. Duas sessões A1/A2 e uma B1. Para estados artificiais, gerar tokens sintéticos determinísticos URL-safe de 43 caracteres, persistir **seus hashes**, com timestamps fixos. O cenário de emissão usa gerador real; não provar entropia por amostra estatística. Não imprimir tokens.
6. Fixar tempo `T=2026-10-18T12:00:00+00:00` em patch restrito dos módulos `tokens_sessao` e `autenticador_sessao`, sem alterar código produtivo. Sessão válida com criada T e expira T+8h; vencida com expira T−1s; limítrofe com expira T. Avançar clock controlado, sem sleep. Repositório recebe T explicitamente nos testes diretos. Data UTC lida de SQLite pode vir sem tzinfo: normalizar como UTC no assert somente se isso refletir a codificação conhecida da fixture; PostgreSQL testa retorno timezone-aware separadamente. Não modificar filtros produtivos.
7. Fotografar estado antes/depois por SELECT em sessão nova: contagem e campos de sessoes e usuarios; comparar hashes como booleanos, datas e propriedade sem expor segredo nos logs. Para negativos de mutação, enviar PUT válido com nome/email sintéticos, esperando estado intacto e contador do executor zero.
8. PostgreSQL opcional: `CREDENCIAIS_TEST_POSTGRES_URL` deve apontar deliberadamente para base local **descartável e exclusiva da suíte**, driver `postgresql+psycopg`, nunca usar fallback de DATABASE_URL. Instância/usuário/base são fornecidos externamente, não pelo shell tests. Rodar cada teste em schema exclusivo aleatório com search_path controlado, inclusive nas conexões da migration, ou em base exclusiva por caso se houver permissão. Escolha recomendada: schema por caso; a fixture deve confirmar propriedade e limpar apenas o schema criado. Não aplicar migrations nem cleanup antes de confirmar o alvo local dedicado. Sem URL, skip explícito. Não obter PostgreSQL por instalação global; eventual servidor descartável precisaria de harness Nix adicional aprovado, não está autorizado como dependência permanente aqui.

### Ordem, cenários e oráculos

Ordem recomendada para diagnóstico: preflight → migration/schema → persistência → emissão → uso/negativas → revogação/isolamento → composição exportada → regressão/lint → registro. Os testes são independentes; nenhum depende de token criado por outro teste.

Vínculos: **C82-I** = critério inferido de `a50905c`/PR #467; **K** = contrato atual sem atribuição resolvida a #80/#81. Toda célula K permanece candidata a rastrear aos cards após L01; não é aceite oficial.

| ID / objetivo | Pré-condições e dados | Passos | Resultado esperado e evidência exigida | Nível / fonte / card |
|---|---|---|---|---|
| M01 — schema migrado | Banco vazio exclusivo, dependências presentes, grafo desambiguado temporariamente se necessário | `alembic upgrade head`; inspeção SQLAlchemy e alembic_version; nova conexão | Sem warnings de duplicação no grafo usado; head final, tabela sessoes com seis campos, PK/FK/UNIQUE e nullability conforme F04. Guardar comando, dialeto, versões e diff temporário | Migration / revisão 0004, ORM, env Alembic / K |
| M02 — unicidade e obrigatoriedade | M01, usuário A | Inserir uma sessão; tentar mesmo hash com outro id; tentar NULL nos campos não anuláveis em transações independentes | IntegrityError no banco, rollback da tentativa, primeira linha preservada; inspecionar constraint real, não somente metadata | Migration/banco / revisão 0004 / K |
| M03 — FK de conta | M01, FK SQLite confirmada ON | Tentar salvar sessão com usuario_id inexistente, rollback, contar linhas | Rejeição por FK e nenhuma sessão órfã. Não inventar resposta HTTP para inserção interna inválida | Migration/repositório / FK da revisão 0004 / K |
| P01 — persistência durável do hash | M01, A | Criador real cria token; harness commit; abrir nova sessão e consultar linha e autenticador | Hash igual SHA-256(token), diferente de token; somente seis colunas; datas com diferença 8h, revogada nula, id UUID e usuario A; autenticação encontra A | Repositório/banco / contrato Credencial e armazenamento, Criador/Repo / K |
| P02 — fronteira de expiração sem renovação | Linhas com expira T−1s, T, T+1s | Consultar `obter_usuario_ativo(hash,T)`; autenticar com clock T; consultar campos novamente | Expira <=T retorna None; T+1s retorna A; nenhuma data/campo alterado pela consulta. Evidência de SELECT e snapshot, não SQL compilado | Repositório/banco / contrato Validação e prazo; SELECT `>` / K |
| P03 — rollback externo, caracterização | M01, usuário A | Salvar/flush sem commit, rollback externo; abrir nova sessão | Linha não persiste; documentar semântica do adapter e não prometer atomicidade HTTP | Repositório/banco / docstring do repositório / K, não aceite normativo |
| H01 — emissão real | A ativo, senha válida, serviços reais e relógio T | POST `/acessos` com `{"email":"a@example.test","senha":"Senha-Teste-123"}`; commit do harness; nova sessão | 204, corpo vazio, só cookie __Host-sessao; atributos F03, sem Domain; token decodifica 32 bytes, 43 caracteres sem padding; persistência P01. Resumo de headers redigido | Rota via app + banco / contrato Criar sessão / K |
| H02 — login recusado uniforme | A/B persistidos; A excluído em variante; email inexistente em variante | POST senha errada; POST email ausente; POST conta excluída, cada caso em fixture limpa | Mesmo 401 e detail, sem Set-Cookie, sem sessão nova; comparar snapshots. Não exige tempo de resposta igual | Rota via app + banco / contrato Credenciais da conta e Criar sessão, AcessarEstudante / K |
| H03 — formatos HTTP de login | Serviços reais, banco limpo | POST sem senha; senha com 7/1025 caracteres; email `abc` com senha válida | 422 para DTO; 401 para email estrutural inválido `abc`; nenhum cookie/sessão. Não converter casos ausentes em 401 | Rota via app + banco / contrato Criar sessão, DTO e catch / K |
| H04 — uso e identidade própria | H01 reproduzido dentro do próprio teste; nova app/sessão DB | GET `/estudantes/{A}` com cookie de A, repetir após T+1h; snapshot datas | 200, identidade A no DTO, sem hash/token; sessão não prolongada. Executor real recebe A. Não usar GET /sessao/atual | Rota via app + banco / contrato Validação/principal e código GET perfil / K |
| H05 — ausência/transporte não aceito | Sessão A válida no banco, sem Cookie | PUT `/estudantes/{A}` JSON válido com Authorization Bearer do token; variantes query `token` e corpo com campo token, sem cookie; variante totalmente ausente | 401 uniforme antes de executar caso de uso, estado intacto. Token fora do cookie não autentica | Rota via app + banco / contrato transporte/rotas protegidas / K |
| H06 — desconhecida e malformada caracterizada | Nenhuma linha para hashes das entradas | PUT válido com cookie desconhecido URL-safe; variantes vazio e `nao-base64!` que parser aceite | 401 por ausência de registro; contador zero/estado intacto. Casos vazio e não-base64 são caracterização, não validação de gramática inexistente; não garantir parser de todo cliente | Rota via app + banco / contrato registro existe; L03 / K |
| H07 — expirada/revogada | Registro real para token com expira T−1s ou revogada_em=T−1s, A ativo | PUT válido com cookie, clock T, snapshot antes/depois | 401 uniforme, executor zero, estado intacto; prova filtros reais e não fallback que rejeita tudo | Rota via app + banco / contrato Validação / K; revogação também C82-I |
| H08 — conta excluída invalida todas | A1/A2 válidas, B1 válida | UPDATE de fixture em usuarios.deleted_at para A e commit; novas apps/sessões; tentar A1/A2, depois B1 | A1/A2 401 e B1 funciona em GET próprio; sem exigir revogada_em em A. Snapshot prova invalidação por JOIN, não revogação em lote | Rota via app + banco / contrato Revogação e limpeza, JOIN / K |
| H09 — isolamento de identidade | A/B ativos, cookie A | PUT `/estudantes/{B}` com JSON válido de edição e identidade forjada em corpo/query; depois GET próprio A | PUT 403, B intacto, executor edição zero; controle A 200. Não usar GET B como se devesse responder 403; ver divergência F09 | Rota via app + banco / tabela de operações do contrato, middleware / K |
| R01 — logout com persistência | A1/A2 e B1 válidas | DELETE `/sessao/atual` com A1; commit; nova conexão; tentar reusar A1, A2 e B1 | 204 e cookie removido com Max-Age=0 e atributos; A1 revogada e 401 no reuso, A2/B1 válidas; apenas uma linha alterada | Rota via app + banco / contrato Encerrar e logout só sessão atual / C82-I |
| R02 — repetir logout preserva primeira data | R01 preparado no próprio teste | DELETE A1 em T, nova sessão/clock T+1min, DELETE A1 novamente | Ambos 204 e cookie removido; mesmo revogada_em inicial, A2/B1 intactas | Rota e repositório/banco / contrato idempotência + UPDATE condicionado / C82-I |
| R03 — logout sem sessão ativa | Variantes sem cookie, token desconhecido, token expirado, revogado | DELETE com serviço real em cada variante, commit e reler | Sempre 204/cookie removido; desconhecido não cria linha; outras sessões intactas. Preencher data em expirado é caracterização do UPDATE, não exigência contratual | Rota via app + banco / contrato Encerrar / C82-I |
| H10 — dependências ausentes | Aplicação de teste criada com autenticador real, omitindo executor de login ou criador ou revogador, banco isolado | POST login DTO válido em duas variantes; DELETE com cookie sem revogador; DELETE sem cookie | Login 503/sem cookie/sem linha; logout com cookie 503/sem remoção; sem cookie 204/remove. Não simular erro de DB como indisponibilidade não definida | Rota via aplicação / contrato Operações HTTP / K e C82-I para logout |
| C01 — composição exportada caracterizada | backend.main.app original, sem DATABASE_URL externa | POST login válido; DELETE com/sem cookie sintético; verificar middleware da app | Atual: 503 login, 503 logout com cookie, 204 logout sem cookie, fallback presente. Rotular comportamento atual e impossibilidade de provar autenticação positiva; não tratar 503 como cumprimento de login | Rota na composição de produção / main, factory, guards / K; limite de C82-I |
| C02 — fluxo autenticado na composição de produção | Requer wiring persistido real que hoje não existe | Cenário reservado, não fabricar token aceito pelo fallback | Skip “produção não compõe login/criador/revogador/autenticador persistido”; sem prova de jornada. Não adicionar endpoint/override para fazer passar | Composição de produção / F05 / K |

M02 não exige que SQLite aplique comprimento de VARCHAR; não há regra de hexadecimal SQL a testar. P02 testa corte `>` por fonte explícita, não regra transplantada. H08 usa exclusão de fixture para isolar contrato de sessão; não certifica endpoint de exclusão. Conta inexistente é coberta por H02/M03; sessão órfã persistida com FK desativada não será gerada (L07). Repetição de revogação vem do contrato e UPDATE, não de idempotência de outros recursos.

Opcional PostgreSQL: repetir M01–M03, P01/P02 e R01/R02 com mesmo oráculo, verificando adicionalmente timezone-aware em UTC no roundtrip. Não exige usar navegador, provar alta entropia estatística, scan de segurança, carga ou thresholds inexistentes.

### Recursos ausentes, skips e falhas

- Sem aiosqlite: `SkipTest("SQLite integrado indisponível: aiosqlite não fornecido pelo Python Nix de tests")` na classe SQLite após gate de import, mantendo descoberta executável. Sem sqlalchemy/fastapi/alembic, motivo identifica precisamente a dependência e ambiente; não realizar instalação pip/global. No caminho autorizado, preferir habilitar suporte temporário e executar de fato a suíte.
- Sem `CREDENCIAIS_TEST_POSTGRES_URL`, psycopg ou serviço local acessível: skip da classe PostgreSQL com motivo distinto para cada causa. Verificar endereço/localidade e confirmação de alvo dedicado antes de abrir conexão. Erro de configuração perigosa é bloqueio, não tentativa de conexão.
- Grafo preexistente duplicado: M01 registra bloqueio do baseline original; usar autorização temporária abaixo e repetir. Se suporte temporário não puder ser aplicado, ignorar dependentes com motivo “migrations preexistentes ambíguas”, relatando bloqueio externo. Não capturar qualquer erro de upgrade como “ambiente indisponível”: erro novo não reconhecido, bug de fixture ou falha do produto deve falhar e ser investigado.
- Controles positivos precisam executar: se banco inteiro foi ignorado, saída “OK (skipped=N)” **não atende** contrato. Nenhum xfail novo para esconder defeito. Erro legítimo permanece FAIL/ERROR e handoff.
- C02 fica explicitamente ignorado por produto/composição, não por ambiente. Falta de rota GET sessão não ganha skip de requisito vigente inexistente: permanece achado histórico/documental.

### Suporte temporário autorizado para execução futura

Antes de qualquer alteração, fora do Nix: `git status --short --untracked-files=all` e diff de `nix/`, `flake.nix`, `flake.lock`, `src/backend/infrastructure/persistence/alembic/versions/` (inclusive staged). Se houver mudança do usuário nesses caminhos, **parar e informar**, sem restaurar nem reaproveitar trabalho alheio. A árvore estava limpa nesta análise, mas a skill deve reverificá-la na execução.

Somente temporariamente em `nix/tests.nix`, disponibilizar Python via `pkgs.python3.withPackages`, reutilizando `import ./backend-python-packages.nix { inherit pkgs; }` e acrescentando `ps.aiosqlite` no conjunto de pacotes Python. Não editar backend-python-packages.nix, flake ou lock para isso. Usar SQLite da biblioteca Python/driver, sem precisar de sqlite3 CLI; PostgreSQL não é instalado/provisionado por essa mudança.

Para desambiguar as duas revisões duplicadas, proposta temporária mínima, apenas `revision`/`down_revision` (e documentação do identificador para consistência), sem alterar DDL:

| Arquivo em P/alembic/versions | revision temporária | down_revision temporária |
|---|---|---|
| `20261015_0011_criar_cursos.py` | manter `20261015_0011` | manter `20261015_0010` |
| `20261015_0011_exclusao_logica_formacoes_academicas.py` | `20261015_0011b` | `20261015_0011` |
| `20261015_0012_criar_links_profissionais.py` | manter `20261015_0012` | `20261015_0011b` |
| `20261015_0012_criar_projetos_academicos.py` | `20261015_0012b` | `20261015_0012` |
| `20261016_0013_criar_documentos.py` | manter `20261016_0013` | `20261015_0012b` |

Preservar merges anteriores e sequência após documentos. Isso lineariza somente o trecho ambíguo, sem corrigir permanentemente a história. Inspecionar o grafo e aplicar até head no banco vazio. Se aparecer outro problema, registrar e não expandir correção de produto. A execução resultante prova DDL/collaboração sob grafo temporário; **não prova que o baseline original migra corretamente**.

Antes do cleanup, copiar **diffs completos**, sem truncamento, de nix/tests.nix e de cada migration temporariamente alterada para o resumo da execução; incluir comando, ambiente, motivo, novos IDs e distinção entre baseline e grafo temporário. Pode guardar diff transitório em `/tmp`, mas o resumo precisa conter o conteúdo, não apenas o nome do arquivo.

Reverter ao final, inclusive após falha/interrupção, com `git restore -- nix/tests.nix` e `git restore -- <lista-exata-das-migrations-alteradas>`, fora do Nix. Não restaurar diretórios amplos nem staged do usuário. Depois: `git diff --check`, `git status --short --untracked-files=all`; este último **não pode listar nenhum caminho em nix/, flake.nix, flake.lock ou src/backend/infrastructure/persistence/alembic/versions/**. Se uma mudança concorrente surgir, interromper restauração do arquivo afetado e informar; não apagar trabalho do usuário. Suíte/fixtures novas são as únicas alterações de código esperadas ao encerrar a futura skill.

### Comandos futuros e gates

Executar da raiz após suporte temporário, sem usar Python global. O preflight deve registrar `sys.executable`, `sys.version`, versões de SQLAlchemy/Alembic/driver e dialetos. Confirmar caminho em `/nix/store/`.

```sh
nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest backend.tests.test_integracao_persistencia_sessao backend.tests.test_integracao_contrato_credenciais_sessao backend.tests.test_integracao_composicao_credenciais_sessao -v
nix develop .#quality --command ruff check src/backend
```

A fixture deve executar a migration por subprocesso do **mesmo interpretador Nix** (`sys.executable -m alembic upgrade head`), com `DATABASE_URL` do alvo temporário, `PYTHONPATH=src`, cwd raiz e ambiente filtrado. Para inspeção manual, no mesmo shell tests: `alembic heads`; migration manual somente com URL local exclusiva já configurada. Não copiar uma URL fictícia como alvo operacional.

Após execução da suíte, rodar também o comando informativo completo exatamente solicitado:

```sh
nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src
nix develop .#quality --command ruff check src/backend
```

Baseline desta análise: 781 testes, zero failures/errors, dois skips. Novos testes SQLite podem ficar ignorados no shell backend por ausência de aiosqlite; isso é aceitável somente na verificação informativa, com motivo explícito e prova anterior no shell tests. Comparar também os nomes dos testes antigos: nenhum erro/falha novo, nenhum teste antigo escondido/removido. Se ambiente/HEAD mudou, capturar novo baseline anterior à implementação e explicar a diferença, sem apagar o registro atual.

Ao final **de cada execução de testes**, executar o gate completo Ruff. Se ocorrer I001 nos arquivos apontados, aplicar somente ordenação de imports autorizada: `nix develop .#quality --command ruff check --select I --fix <arquivos-apontados>` e repetir `nix develop .#quality --command ruff check src/backend`. Não corrigir defeitos funcionais nem lint alheio silenciosamente; registrar se arquivo produtivo preexistente bloquear o gate. Nesta análise não houve I001. Não rodar testes novos no backend como substituto da execução formal em tests.

## Modelo de rastreabilidade e registro por card

### Matriz antes da execução

Esta tabela define campos e candidatos; não é resultado preenchido. “Não verificável” na coluna oficial decorre da fonte ausente, independentemente de futuros testes verdes.

| Card / critério | Origem e grau de certeza | Cenários candidatos | Esperado | Evidência exigida | Status possível após execução |
|---|---|---|---|---|---|
| #80 — título/aceites não fornecidos | Sem fonte local | K: M01–M03, P01–P03, H01–H10, C01/C02 **a associar após confirmação**, não atribuição | Contrato atual conforme matriz, sem afirmar critério de #80 | Texto do card + vínculo de PR/commit + execução relevante | Critério oficial: **não verificável** até L01; depois avaliar quatro estados |
| #81 — título/aceites não fornecidos | Sem fonte local | Mesmos candidatos K, sem distribuir arbitrariamente por card | Idem | Idem, específico de #81 | Critério oficial: **não verificável** até L01 |
| #82-I1 — revogar só sessão apresentada | **Inferido** do trabalho a50905c, PR #467; contrato Encerrar/Revogação | R01, H07 | 204, hash marcado, reuso 401, demais válidas | Test IDs executados, comando/ambiente/dialeto, nova conexão/snapshot antes/depois e HTTP redigido | Atendido/parcial/não atendido/não verificável para o **critério inferido**, não para aceite oficial |
| #82-I2 — repetição não muda primeira revogação | **Inferido** do UPDATE condicionado e docs da porta | R02 | 204 em ambas, mesmo timestamp inicial | Linhas relidas em nova sessão após duas chamadas, clocks distintos | Quatro estados conforme execução; skip nunca atendido |
| #82-I3 — limpar cookie e responder sem sessão ativa | **Inferido** do router/testes adicionados e contrato atual | R03, H10 | Atributos de remoção; idempotência; 503 sem revogador com cookie | Headers redigidos, estado de sessões, comando Nix | Quatro estados; composição de produção registrada separadamente |
| #82 — aceite oficial completo | Texto ausente apesar do vínculo ao trabalho | Somente após obter aceite | Não definir aceite por leitura do diff | Texto/decisões de escopo + evidência de todos os critérios | **Não verificável** até L02; não promover inferências a aceite |

### Estados de execução e regra de agregação

Guardar dois eixos independentes:

1. **Execução por cenário:** `executado-aprovado`, `executado-reprovado`, `erro-de-execução`, `ignorado-ambiente`, `ignorado-produto/composição`, `não-executado`. Capturar quantidade pass/fail/error/skip por cenário/dialeto, motivo de skip, comando, exit code, Python Nix, timestamp, HEAD e diffs temporários. `OK (skipped=N)` no resumo não converte cenários ignorados em aprovados.
2. **Atendimento por critério/card:** `atendido` somente com fonte identificada e todos os cenários necessários realmente aprovados; `parcialmente atendido` quando parte definida tem prova positiva e parte permanece sem prova/defeituosa, discriminando-a; `não atendido` quando execução demonstra violação de critério definido (um obrigatório refutado impede aprovação global); `não verificável` quando falta fonte/identidade do critério, alvo ou execução essencial. Critério sem fonte local permanece não verificável mesmo com cenário de contrato verde.

Não somar testes nem porcentagens para decidir atendimento. O veredito global do card exige escopo confirmado e critérios oficiais; destacar separadamente atendimento técnico do contrato. Uma futura decisão explícita dos donos pode adotar os critérios inferidos, mas deve ser registrada como nova fonte, não reescrever a origem histórica. Nenhum card recebe “atendido” nesta análise.

### Documento futuro e textos prontos por card

Fora da skill de implementação da suíte, responsável pelo registro criará `docs/validacao-contrato-credenciais-cards-80-82.md` após execução real, contendo base, comandos, versões, tabela de resultados, cobertura/limites, matriz por card, achados, diffs temporários completos e status final. Essa criação é recomendação para atividade posterior; não é uma segunda escrita autorizada nesta análise.

Os três blocos abaixo são modelos prontos para preencher e colar, **não comentários enviados**. Não preencher placeholders com aprovação por default. Ausência de GitHub não bloqueia entrega local: fornecer os blocos preenchidos após execução; publicação só em atividade explicitamente autorizada.

```text
Card #80 — Validação do contrato de credenciais
Título e critérios oficiais: não localizados na base 46a7a75; fornecer texto e vínculo de PR/commit.
Análise: prompts/backend/20261018-131822-validacao-contrato-credenciais-cards-80-82-v001.md#v001.
Execução real: <data, HEAD, comando em nix develop .#tests, Python/dialeto, exit code e IDs>.
Contrato atual: <cenários executados-aprovados / reprovados / erros / skips com motivos>.
Critérios oficiais do card: não verificáveis enquanto faltar a fonte; não atribuir automaticamente os cenários K a este card.
Veredito após execução: <não verificável; outro estado somente após fornecer fonte e aplicar matriz>.
Limites: composição montada em teste não certifica login de produção; migrations <originais ou temporárias, com diff>; <demais achados>.
Regressão/lint: <comandos e resultados>; registro local: <caminho/commit>.
```

```text
Card #81 — Validação do contrato de credenciais
Título e critérios oficiais: não localizados na base 46a7a75; fornecer texto e vínculo de PR/commit.
Análise: prompts/backend/20261018-131822-validacao-contrato-credenciais-cards-80-82-v001.md#v001.
Execução real: <data, HEAD, comando em nix develop .#tests, Python/dialeto, exit code e IDs>.
Contrato atual: <cenários executados-aprovados / reprovados / erros / skips com motivos>.
Critérios oficiais do card: não verificáveis enquanto faltar a fonte; trabalho de emissão é conhecido, mas vínculo com #81 não foi demonstrado.
Veredito após execução: <não verificável; outro estado somente após fornecer fonte e aplicar matriz>.
Limites: <composição produtiva, grafo temporário, dialeto e achados>.
Regressão/lint: <comandos e resultados>; registro local: <caminho/commit>.
```

```text
Card #82 — Validação da revogação de sessão
Vínculo local: merge 8a6880a da PR #467, branch feature/82-sessao-revogavel, commit a50905c.
Título/aceites oficiais: indisponíveis; objetivo e critérios abaixo são inferidos do trabalho, não transcrição do card.
Análise: prompts/backend/20261018-131822-validacao-contrato-credenciais-cards-80-82-v001.md#v001.
Execução real: <data, HEAD, comando em nix develop .#tests, Python/dialeto, exit code>.
#82-I1/R01/H07: <status, códigos HTTP, persistência e isolamento, evidência redigida>.
#82-I2/R02: <status, preservação da primeira data, evidência>.
#82-I3/R03/H10: <status, limpeza de cookie e variantes, evidência>.
Skips/erros: <IDs e motivos; não são prova de atendimento>.
Veredito técnico dos critérios inferidos: <preencher após execução>.
Veredito do aceite oficial: não verificável até obter texto/escopo do card.
Limites: produção não compõe revogador; <dialeto/grafo temporário e demais achados>.
Regressão/lint e cleanup: <comandos, resultados, status e diff completo>; registro: <caminho/commit>.
```

## Achados de backend e documentação — sem correções

| ID | Achado e evidência | Implicação / handoff |
|---|---|---|
| A01 | `main.py` injeta fallback que sempre retorna None, sem login/criador/revogador; F05 | Fluxo autenticado de produção não é operacional nessa composição. Backend deve decidir wiring/transações em atividade própria |
| A02 | Duplicação 0011/0012, F08 e comando real heads | Não certificar cadeia original; saneamento permanente fora do escopo, suporte temporário apenas como autorização do usuário |
| A03 | tests.nix só Git; falta driver assíncrono; F08/F10 | Sem habilitação temporária, suite de persistência fica bloqueada/ignorada; PATH global não é solução |
| A04 | GET sessão previsto em 575006e, removido em f30d034 e ausente no router | Expor mudança de escopo histórico; contrato atual não exige criá-lo |
| A05 | CSRF/Origin e limitação ausentes versus contrato antigo/RF-AUT-08; F09 | Risco de segurança registrado; SameSite não é prova desses controles. Sem novo requisito/tarefa implementada aqui |
| A06 | Generalização 403 versus GET perfil alheio 404; F09 | Alinhar documentação/decisão do endpoint em handoff próprio; não importar comportamento de outros recursos |
| A07 | DER SESSAO sem token_hash; F09 | Documentação de modelo incompleta frente a ORM/migration; não inferir armazenamento em claro |
| A08 | Política HTTP de commit/erro de banco não definida; repositório só flush | Harness prova integração sob commit externo; não promete entrega atômica produtiva nem status em falhas não definidas |
| A09 | Regras de hash/datas garantidas por emissor/consulta, não CHECK SQL; F04 | Não chamar ausência de CHECK de violação de requisito inexistente; não afirmar que DB impede toda sessão semanticamente inválida |
| A10 | Cookie Secure inclusive local versus guia com uvicorn HTTP; contrato e guia | Harness usa HTTPS sintético; não prova que navegador enviará cookie no setup HTTP do guia. Não retirar Secure como workaround |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | Cards fechados por inferência/skip/contagem | Alta | Revisores e donos dos cards |
| security | Fallback 401 confundido com validação de expiração/revogação | Alta | Usuários e backend |
| operability | Dependência de ambiente global e resultado irreproduzível | Alta | Responsável por executar |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | Registro detalhado de fontes, skips, diffs e duas composições | simplicity | Aceito para não superestimar prova |
| operability | Patch e reversão temporários; SQLite não equivale a PostgreSQL | interoperability | Aceito com dialeto explícito e repetição opcional |
| security | Cards podem continuar não verificáveis mesmo com testes verdes | time-to-value | Aceito; falta de aceite não é resolvida por execução |

## Riscos e efeitos de segunda ordem

Suporte temporário pode esconder defeito permanente de migrations: publicar diff completo e manter A02. Caracterização de 503 pode virar falsa garantia de autenticação: separar C01 de aceitação do contrato. Skips podem fazer CI parecer suficiente: registrar quantidades por cenário e exigir positivo real. Dados/headers de credenciais podem vazar por falhas de assert: redigir mensagens e logs da suíte. Mudanças concorrentes podem ser perdidas por restore: preflight e lista exata, parar se houver trabalho alheio. Confundir critério inferido com aceite oficial é risco de governança da entrega: manter origem e veredito separados.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| H1: suíte executável sem serviço externo | M01–R03 reais em tests, aiosqlite/Python Nix, controles positivos executados | Implementação futura pela skill após referência explícita a esta versão | SQLite não suporta DDL necessário; pedir revisão sem contornar com create_all |
| Sem regressão | Descoberta completa backend comparada a 781/0 erros/2 skips de baseline | Comando exato e nomes/contagens, após suíte | Erro novo ou teste antigo ocultado |
| Gate de qualidade | “All checks passed!” após cada execução | Ruff completo, tratamento I001 conforme comando prescrito | Lint persistente fora de escopo |
| Cleanup honesto | Diffs completos temporários no resumo e status final sem áreas protegidas | Git fora do Nix, restore somente mudanças próprias | Alteração do usuário/concorrrente ou diff residual |
| Rastreabilidade dos cards | Títulos/aceites/PRs ou commits fornecidos localmente | Resolver L01/L02 e atualizar matriz antes de veredito oficial | Nova fonte muda cenários/oráculos ou revela compromisso histórico diferente |
| Produção certificável | Runtime real com serviços, banco e transação operacionais | Atividade posterior fora desta suíte; repetir cenários de app exportada | Wiring muda: revisar análise, não adotar silenciosamente |

## Handoffs e atividades posteriores

| Responsável / classificação | Entrega | Caminhos/ambiente | Limites |
|---|---|---|---|
| `$integration-system-testing-v1` — integration/contract/system-acceptance-e2e | Suíte e fixtures propostas, gate de atualidade da análise, proveniência e execução | Quatro arquivos T/ acima; `nix develop .#tests`; regressão informativa backend e Ruff quality | Somente após invocação com caminho exato desta análise v001; não escrever registro docs nem corrigir produto |
| Mesma skill, exceção temporária expressa do usuário | Habilitar Python backend+aiosqlite e desambiguar revisões somente durante execução; restaurar | `nix/tests.nix` e cinco migrations indicadas; desenvolvimento sob ambiente correspondente; Git fora Nix | Exceção à fronteira normal de produto/Nix somente para experimento descartável; não entregar correção permanente |
| Responsável por registro/documentação | Preencher documento e três blocos após execução, com vereditos e fontes | `docs/validacao-contrato-credenciais-cards-80-82.md` | Fora da implementação da skill; não transformar relatório em código-fonte de teste |
| Donos dos cards/produto | Fornecer texto dos cards, aceite e vínculo #80/#81; confirmar escopo histórico | Artefato local/export autorizado | Sem fonte, critérios oficiais não verificáveis |
| Backend — product-change | Avaliar A01/A02/A05/A06/A08 e decisões próprias | main/factory/persistência/segurança | Não corrigir durante a suíte |
| GitHub — external-test-operations | Eventual comentário/PR com textos e links | Fora do Nix para gh; somente mediante autorização explícita | Não executado nesta análise nem delegado implicitamente à skill; sem fechar cards |
| Unitários — unit | Manutenção de testes isolados se outro trabalho alterar regras | `nix develop .#backend` | Não adicionar unitários nesta skill de integração |

## Síntese

Proposta inicial de suíte integrada do contrato atual, com base SQLite migrada, repetição PostgreSQL opcional e composição produtiva avaliada separadamente. O registro por card terá prova de execução e origem de critérios; o vínculo #82 é demonstrável, #80/#81 e o aceite oficial dos três permanecem lacunas. Não houve implementação de teste, correção de backend, modificação de ambiente ou publicação. O baseline real e o lint são informativos; não aprovam os cards.
