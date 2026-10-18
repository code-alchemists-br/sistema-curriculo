---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-18T12:37:41-03:00"
lineage:
  mode: initial
  root: null
  supersedes: null
  change_type: initial
  secondary_change_types: []
  decision_impact: initial
subjects:
  kind: file-set
  files:
    - {path: AGENTS.md, relationship: context, representation: prose, function: prompt-instruction, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/AGENTS.md, relationship: context, representation: prose, function: prompt-instruction, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: .agents/skills/decision-analysis-v4/SKILL.md, relationship: context, representation: prose, function: prompt-instruction, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: .agents/skills/integration-system-testing-v1/references/analysis-input-contract.md, relationship: context, representation: prose, function: prompt-instruction, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: .agents/skills/integration-system-testing-v1/references/test-scope-boundary.md, relationship: context, representation: prose, function: prompt-instruction, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/middleware_autenticacao.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/factory.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "create_app, imports e registro de routers", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/main.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/versao_curriculo.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "DTOs, criar_router e handlers", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/listagem_versoes_curriculo.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "criar_router/listar", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/exclusao_versao_curriculo.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "criar_router e exclusão", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/previa_versao_curriculo.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "rota, conversão da entrada e tratamento de falhas", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/itens_versao_curriculo.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "DTO e criar_router", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/revisao_versao_curriculo.py, relationship: supporting, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: "arquivo vazio", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/sessoes.py, relationship: supporting, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/versao_curriculo.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "exceção, entradas e executar dos três casos de uso", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/listagem_versoes_curriculo.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/exclusao_versao_curriculo.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "executar e guarda de proprietário", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/previa_versao_curriculo.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "construtor e executar, linhas 110–180", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/selecao_itens_versao_curriculo.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "entradas, construtores e executar", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/revisao_versao_curriculo.py, relationship: supporting, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "entrada e delegação à prévia", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/sessoes.py, relationship: supporting, representation: source-code, function: schema-contract, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/infrastructure/security/autenticador_sessao.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/infrastructure/security/autenticador_sessao_indisponivel.py, relationship: supporting, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/infrastructure/security/tokens_sessao.py, relationship: supporting, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_sessao.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "obter_por_id, atualizar, salvar, listar_por_usuario e excluir", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py, relationship: supporting, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "CurriculoRegistro e conversões de ordem e versão", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/infrastructure/persistence/sqlalchemy/metadata.py, relationship: supporting, representation: source-code, function: configuration, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/infrastructure/persistence/alembic/env.py, relationship: supporting, representation: source-code, function: configuration, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: alembic.ini, relationship: supporting, representation: structured-data, function: configuration, format: INI, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_integracao_isolamento_dados_estudantes.py, relationship: primary, representation: source-code, function: test, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_integracao_rejeicao_referencia_curriculo.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_integracao_recusa_perfil_alheio.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_api_middleware_autenticacao.py, relationship: primary, representation: source-code, function: test, format: Python, analysis_scope: selected-section, locator: "stub, dispatch e testes de currículo/fábrica/main", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_application_versao_curriculo.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: selected-section, locator: "linhas 90–135; nomes dos demais testes", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_application_previa_versao_curriculo.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: selected-section, locator: "linhas 561–590; nomes dos demais testes", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_application_selecao_itens_versao_curriculo.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: selected-section, locator: "linhas 172–245; nomes dos demais testes", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_application_listagem_versoes_curriculo.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: selected-section, locator: "linhas 140–175; nomes dos demais testes", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_application_exclusao_versao_curriculo.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: selected-section, locator: "linhas 110–145; nomes dos demais testes", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_infrastructure_autenticador_sessao.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: metadata-only, locator: "nomes de testes de hash, expiração, revogação e conta excluída", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_infrastructure_repositorio_curriculo.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: metadata-only, locator: "nomes de testes e buscas de configuração", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/test_integracao_persistencia_dados_pessoais.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: selected-section, locator: "setUp, tearDown e roundtrip", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/fixtures/perfis_integracao.py, relationship: supporting, representation: source-code, function: data-fixture, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/tests/fixtures/sessoes_integracao.py, relationship: supporting, representation: source-code, function: data-fixture, format: Python, analysis_scope: whole-file, locator: null, content_state: commit, revision: eca8708, availability: available}
    - {path: src/backend/tests/test_integracao_contrato_credenciais_sessao.py, relationship: supporting, representation: source-code, function: test, format: Python, analysis_scope: selected-section, locator: "setup, sessão, helper HTTP e testes de validade", content_state: commit, revision: eca8708, availability: available}
    - {path: docs/contrato-credenciais-sessao.md, relationship: primary, representation: prose, function: schema-contract, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: docs/requisitos-seguranca.md, relationship: primary, representation: prose, function: documentation, format: Markdown, analysis_scope: selected-section, locator: "§2–3, §4.6–4.7 e §9, buscas de autorização", content_state: working-tree, revision: null, availability: available}
    - {path: docs/requisitos_funcionais.md, relationship: supporting, representation: prose, function: documentation, format: Markdown, analysis_scope: selected-section, locator: "RF07, RF13–15 e pontos em aberto", content_state: working-tree, revision: null, availability: available}
    - {path: docs/requisitos_nao_funcionais.md, relationship: supporting, representation: prose, function: documentation, format: Markdown, analysis_scope: selected-section, locator: "RNF04 e sua verificação", content_state: working-tree, revision: null, availability: available}
    - {path: docs/configuracao-ambiente.md, relationship: context, representation: prose, function: documentation, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: nix/tests.nix, relationship: supporting, representation: source-code, function: configuration, format: Nix, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: nix/backend.nix, relationship: supporting, representation: source-code, function: configuration, format: Nix, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: nix/backend-python-packages.nix, relationship: supporting, representation: source-code, function: configuration, format: Nix, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: flake.nix, relationship: supporting, representation: source-code, function: configuration, format: Nix, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: prompts/backend/20261016-221632-recusa-perfil-alheio-middleware-ativo-v001.md, relationship: context, representation: prose, function: documentation, format: Markdown, analysis_scope: selected-section, locator: "solicitação, fatos, alternativas, decisão e validação", content_state: working-tree, revision: null, availability: available}
    - {path: prompts/backend/20261010-183257-isolamento-dados-estudantes-integracao-v004.md, relationship: context, representation: prose, function: documentation, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/ambientes, prompts/revisao]
  confidence: high
  rationale: "Especificação de teste integrado de autorização da API backend; precedentes de isolamento e perfil nessa pasta. Ambiente e requisitos são insumos, não o resultado."
classification:
  sphere: engineering
  concerns: [security, integration, data]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: high
---

# Análise de decisão — Recusa de currículo alheio com middleware ativo

## Solicitação original

Texto da demanda preservado literalmente abaixo; os blocos de skills fornecidos depois são instruções complementares, não autorização para implementar.

> $decision-analysis-v4 Implementar "Criar teste de integração que recusa acesso a currículo alheio após o middleware estar ativo". O resultado é um **teste de integração executável**. Antes de decidir o que ele deve conter, analise como o middleware de autenticação, as rotas de currículo e a verificação de propriedade funcionam hoje, e a documentação pertinente.
>
> ## Regra principal: não presumir
>
> Todo fato deve vir de um artefato lido (histórico Git, código, testes, migrations, documentação de segurança, requisitos, configuração de ambiente), com o caminho indicado. O que nenhum artefato definir deve ser registrado como lacuna, nunca como fato.
>
> - Separe em seções distintas: **(a) fatos encontrados**, com caminho e trecho; **(b) lacunas**, ou seja, o que nenhum artefato define; **(c) recomendações**, que são suas, com justificativa.
> - Para cada lacuna, apresente as opções viáveis, recomende uma e marque se depende de decisão de produto ou se pode ser tomada tecnicamente com base no que existe.
> - Quando artefatos divergirem (código, documentação, requisitos, testes), aponte a divergência, diga qual fonte parece mais confiável e por quê, sem escolher em silêncio.
> - Não transponha regras de outros cards (formação, projeto, credenciais) para currículo sem que um artefato de currículo ou de segurança as sustente.
>
> ## Fontes a analisar
>
> 1. **Histórico Git local.** A CLI do GitHub e a rede podem não estar disponíveis; **não dependa delas**. Localize por inspeção do histórico (merges "Merge pull request #N", squashes com sufixo "(#N)", mensagens e histórico dos arquivos) os trabalhos que:
>    - criaram ou alteraram `src/backend/api/middleware_autenticacao.py` e a sua instalação em `factory.py` e `main.py`;
>    - definiram o contrato de credenciais de sessão (#458) e persistiram a sessão revogável (#463);
>    - criaram as rotas de currículo (listagem, versões, prévia, seleção de itens) e os casos de uso de currículo;
>    - criaram o teste existente de isolamento de dados de estudantes (`test_integracao_isolamento_dados_estudantes.py`).
>    Registre como identificou cada trabalho. Se algo não puder ser resolvido, registre como lacuna, sem inventar conteúdo.
> 2. **Documentação pertinente**, localizada por busca: `docs/requisitos-seguranca.md`, requisitos funcionais ligados a currículo, acesso e autorização, `docs/contrato-credenciais-sessao.md`, `docs/configuracao-ambiente.md` e análises anteriores em `prompts/` sobre middleware, isolamento e currículo.
> 3. **Código atual**: o middleware, a fábrica da aplicação, `main.py`, os routers e casos de uso de currículo (incluindo onde e como a propriedade é verificada), os repositórios, os testes unitários e integrados existentes e as fixtures de teste.
>
> ## O que levantar
>
> - **O que significa "currículo alheio".** Faça o inventário de **todas** as rotas que leem, alteram ou excluem currículos e recursos aninhados (versões, prévia, seleção de itens). Para cada uma: método, caminho, de onde vem o identificador do dono (caminho, corpo, sessão), qual mecanismo recusa o acesso alheio (middleware, caso de uso ou ambos) e o status HTTP efetivo. Separe dois vetores: (i) `usuario_id` de outra pessoa no caminho com sessão própria; (ii) identificador de recurso de outra pessoa com o `usuario_id` próprio no caminho.
> - **O que o contrato exige.** O que os documentos de segurança e o contrato definem para acesso a recurso alheio: status esperado (por exemplo 401, 403 ou 404), uniformidade da resposta para evitar revelar a existência do recurso, e se a mensagem pública pode diferir entre "inexistente" e "alheio". Registre separadamente o que está **definido** e o que está **só implementado sem definição**.
> - **O estado de "middleware ativo".** Onde o middleware é instalado, em que condição, e se a composição que sobe (`main.py`) o ativa. Uma análise anterior reportou que `main.py` chama `create_app()` sem autenticador, e que a fábrica só instala o middleware quando recebe um; **verifique se isso continua verdadeiro** na base atual. Descubra se existe PR, card ou documento pendente para ativar o middleware na composição raiz. Recomende como o teste deve tratar isso (por exemplo, montar a aplicação no teste com autenticador e repositório reais) e qual limite declarar sobre a composição de produção.
> - **Cobertura existente:** o que `test_integracao_isolamento_dados_estudantes.py`, os testes do middleware e os testes dos casos de uso de currículo já cobrem, para o novo teste não repetir cobertura sem necessidade, e quais lacunas restam.
> - **O harness disponível:** como os testes integrados existentes montam a aplicação e o banco. Verifique se `src/backend/tests/test_integracao_contrato_credenciais_sessao.py` e `src/backend/tests/fixtures/sessoes_integracao.py` existem na base atual (podem estar em PR aberto e ainda não mergeado). Decida, com justificativa, entre reutilizá-los (e registrar a dependência de ordem de merge) ou usar o harness existente na base. Registre também como a sessão é emitida nos testes e como a expiração e a revogação são simuladas.
> - **O ambiente de testes:** o que `nix develop .#tests` oferece hoje, como o banco é preparado (SQLite, e PostgreSQL se houver) e como as migrations são aplicadas.
> - **Pré-existentes conhecidos.** Registre como bloqueios de execução, **sem tratá-los como escopo e sem corrigi-los**: (1) a cadeia do Alembic pode ter revisões duplicadas na `dev` (`20261015_0011` e `20261015_0012`), o que impede `upgrade heads`; (2) o ambiente `.#tests` pode estar sem Python e sem `aiosqlite`; (3) `GET /sessao/atual` pode estar sem handler. Confirme cada um por inspeção.
>
> ## Escopo
>
> Definir o **teste de integração** que prova que, com o middleware de autenticação ativo, uma pessoa autenticada **não consegue acessar currículo de outra**: cenários, dados, fixtures, resultados esperados e forma de execução, derivados do contrato, das rotas e dos mecanismos de propriedade analisados.
>
> Fora do escopo: alterar o middleware, as rotas, os casos de uso, a persistência ou a composição; ativar o middleware em `main.py`; corrigir migrations; alterar o ambiente Nix de forma definitiva; CSRF, `Origin` e limitação de taxa; front-end. Achados de back-end vão para seção própria, sem correção.
>
> ## Instruções
>
> - Para cada decisão que os artefatos não resolverem, recomende uma opção com justificativa e marque se depende de produto.
> - Derive os cenários do contrato e do inventário de rotas. Cada cenário deve ter objetivo, pré-condições, passos, resultado esperado, nível (rota via aplicação, repositório com banco real) e a fonte que o sustenta. Considere, apenas se o contrato ou os mecanismos existentes os sustentarem: pessoa A com sessão própria tentando ler, alterar, excluir e pré-visualizar currículo de B; `usuario_id` de B no caminho; identificador de recurso de B com o `usuario_id` de A; `usuario_id` de B no corpo ou na query sem efeito sobre o proprietário; resposta idêntica à de recurso inexistente, se isso estiver definido; ausência de alteração no banco após tentativa de escrita (verificada por leitura direta); executor não chamado quando a recusa ocorre no middleware; sem sessão, sessão revogada e sessão expirada. Inclua um **controle positivo**: A acessa o próprio currículo com sucesso, para provar que a recusa vem da propriedade e não de a rota estar sempre falhando. O que não estiver definido entra como lacuna, e a análise deve dizer se o teste registra o comportamento atual como caracterização ou aguarda decisão.
> - Defina a estrutura do teste: nome e localização dos arquivos, reaproveitamento de fixtures, preparação do banco (dois usuários sintéticos com currículos e itens), isolamento entre testes, dependências do ambiente e como os testes dependentes de recurso ausente são ignorados com motivo explícito, sem gerar erro quando o ambiente não os suporta.
> - Indique o que o teste valida com a composição montada no teste e o que só seria validado se a composição de produção ativasse o middleware. O teste não deve afirmar que `main.app` está sem autenticador.
> - Indique a divisão de trabalho: o que fica com `$integration-system-testing-v1` e o que fica fora. Especifique nomes de arquivos, ambientes e comandos, para a skill não precisar inventá-los. Registre que, para executar a suíte, a skill poderá aplicar **alterações temporárias** em `nix/tests.nix` (Python do backend e `aiosqlite`) e, se a cadeia do Alembic estiver com revisões duplicadas, uma **linearização temporária** das migrations; ambas devem ser revertidas por `git restore` ao final, com os diffs copiados para o resumo e `git status --short` sem nenhum arquivo em `nix/`, `flake.nix`, `flake.lock` ou `alembic/versions/`.
> - Registre achados de back-end (divergências, comportamentos não definidos, riscos de segurança) em seção própria, sem corrigi-los.
> - Defina o roteamento do artefato de análise (pasta em `prompts/`) conforme a organização existente.
> - Registre na validação: a execução do teste em `nix develop .#tests`; a execução informativa da suíte completa em `nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src` (que não pode gerar erros novos); e o gate de lint do CI ao final de cada execução: `nix develop .#quality --command ruff check src/backend` (se falhar por I001, corrigir com `nix develop .#quality --command ruff check --select I --fix <arquivos-apontados>` e repetir o gate completo).
> - Não implemente nada.

## Informações complementares

Foram fornecidos os textos de `decision-analysis-v4` e `integration-system-testing-v1`. Aplicação nesta atividade: somente análise; a segunda skill descreve o destinatário futuro. Sua exigência de caminho exato de uma análise será satisfeita apenas numa futura invocação explícita com este arquivo. Não se iniciou implementação, nem se alterou ambiente ou migration.

## Mudanças desde a versão anterior

Nenhum identificado — `initial`. As análises de isolamento #150 e de perfil são contexto de outros trabalhos, não uma versão anterior desta demanda. A busca em `prompts/` não identificou linhagem de recusa de currículo com middleware ativo.

## Artefatos analisados

O inventário individual de caminhos, relação, representação, função, formato, recorte e estado está em `subjects.files`. Os seguintes insumos adicionais também foram examinados:

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `.agents/skills/decision-analysis-v4/references/classification-taxonomy.md` | context | prose | prompt-instruction | Markdown | completo | working-tree; revision null |
| `.agents/skills/decision-analysis-v4/references/output-schema.md` | context | prose | prompt-instruction | Markdown | completo | working-tree; revision null |
| `.agents/skills/decision-analysis-v4/references/output-routing.md` | context | prose | prompt-instruction | Markdown | completo | working-tree; revision null |
| `.agents/skills/decision-analysis-v4/references/artifact-classification.md` | context | prose | prompt-instruction | Markdown | completo | working-tree; revision null |
| `.agents/skills/decision-analysis-v4/references/revision-protocol.md` | context | prose | prompt-instruction | Markdown | completo, para verificar seleção de modo | working-tree; revision null |
| `prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md` | context | prose | documentation | Markdown | buscas de propriedade e metadados | working-tree; revision null |
| `prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md` | supporting | prose | documentation | Markdown | propriedade, erros, decisão e handoffs | working-tree; revision null |
| `prompts/backend/20261008-183601-previa-versao-curriculo-v001.md` | supporting | prose | documentation | Markdown | fatos 1–11, H1–H10, perguntas e validação | working-tree; revision null |
| `prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md` | supporting | prose | documentation | Markdown | buscas de filtro, ausência, propriedade e autenticação | working-tree; revision null |
| `prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md` | context | prose | documentation | Markdown | buscas de ausência, propriedade e erros | working-tree; revision null |
| `src/backend/infrastructure/persistence/alembic/versions/*.py` | supporting | source-code | configuration | Python | todas as declarações revision/down_revision; não todos os corpos | working-tree; revision null |
| `src/backend/infrastructure/persistence/alembic/versions/20261015_0011_criar_cursos.py` | supporting | source-code | configuration | Python | completo | working-tree; revision null |
| `src/backend/infrastructure/persistence/alembic/versions/20261015_0011_exclusao_logica_formacoes_academicas.py` | supporting | source-code | configuration | Python | completo | working-tree; revision null |
| `src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_links_profissionais.py` | supporting | source-code | configuration | Python | completo | working-tree; revision null |
| `src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_projetos_academicos.py` | supporting | source-code | configuration | Python | completo | working-tree; revision null |
| `src/backend/infrastructure/persistence/alembic/versions/20261017_0015_adicionar_ordem_secoes_curriculos.py` | supporting | source-code | configuration | Python | completo | working-tree; revision null |
| `.git` — histórico local | supporting | structured-data | documentation | Git | log por mensagens/caminhos, stats e contrato em #458; hashes abaixo | commit; disponível localmente |

### Limites da evidência dos artefatos

HEAD observado: `46a7a75` (`Merge pull request #543 ... task-212`); working tree inicialmente limpo. Usou-se `git log --all`, portanto um merge encontrado não implica ancestralidade do HEAD. Não houve consulta GitHub nem consulta de rede para investigar cards. Só se pode afirmar disponibilidade em referências locais; não o estado remoto de PRs abertos. Conteúdo atual é working-tree, com `revision: null`; não atribuir silenciosamente esse conteúdo a versões antigas.

Os testes unitários de aplicação tiveram asserções de propriedade lidas nos recortes indicados; os demais cenários foram identificados por nomes. Os de infraestrutura foram identificados por nomes, sem auditoria integral das asserções. A execução global informa resultado, não prova individual de qualidade de cada asserção. Migrations foram inspecionadas, não aplicadas nesta análise. Ausência de arquivo no checkout foi distinguida de disponibilidade via `git show` em outra branch.

## Problema enriquecido

### Resultado desejado

Especificar uma entrega futura de testes executáveis que integre cookie, sessão persistida, middleware ativo, routers e casos de uso reais de currículo, verificando os dois vetores de acesso cruzado e a preservação do banco. Este Markdown é a entrega desta atividade; não é o teste implementado.

### Atores e interesses

Estudantes A e B: privacidade dos currículos e integridade de versões/seleções. Mantenedores: prova reproduzível sem depender de produção ou de PR não incorporado. Implementador: cenários e oráculos explícitos, diagnóstico de ambiente e limites de atuação.

### (a) Fatos encontrados — caminhos e trechos

#### F1 — Segurança e contrato, sem importar regras de outros recursos

| Fonte | Trecho | Consequência observada |
|---|---|---|
| `docs/requisitos-seguranca.md`, §3.3 | “O acesso a recursos pertencentes a outro usuário deverá ser negado.” | Currículos privados de B não podem ser acessados por A |
| mesmo arquivo, §3.6 | “tanto o identificador do currículo quanto o usuário autenticado” | Comparar somente UUID do dono no caminho é insuficiente para o vetor de ID de currículo trocado |
| mesmo arquivo, §3.7 | “A alteração de um identificador na URL, no corpo da requisição ou em parâmetros não deverá permitir acesso indevido.” | Sustenta controles de corpo/query sem inventar campo de proprietário |
| mesmo arquivo, RF-AUTZ-04/05 e §4.7 | “próprios currículos”; “privados por padrão” | Escopo de currículo tem suporte próprio |
| `docs/requisitos_funcionais.md`, RF13/RF14 | “exigir autenticação”; “múltiplos currículos vinculados à sua conta” | Controle próprio deve funcionar, sem acesso cruzado |
| `docs/requisitos_nao_funcionais.md`, RNF04 | “consulta e alteração somente por usuários autorizados” | Atributo de segurança testável pela integração |
| `docs/contrato-credenciais-sessao.md`, validação | “Se alguma condição falhar, o middleware responde `401` antes de chamar o handler.” | Ausente, desconhecida, expirada, revogada ou conta excluída não executam handler |
| mesmo contrato, comportamento HTTP | “uma sessão válida que tenta acessar o recurso de outro estudante responde `403 Forbidden`”; “O middleware atual não mascara esses recursos com `404`.” | Status de recusa do middleware atual explicitamente documentado |
| mesmo contrato, tabela de rotas | “Rotas sob `/estudantes/{usuario_id}/curriculos`”; UUID da rota deve corresponder à identidade autenticada | Vetor (i) é 403, inclusive criação e listagem |

**Definido:** credencial exclusiva no cookie `__Host-sessao`; sessão opaca, SHA-256 persistido, 8 horas, conta ativa, ausência de revogação; 401 antes do handler para falha de autenticação; 403 nas verificações de propriedade do middleware. O contrato exige controles sem sessão por rota e casos de sessão válida/inválida/expirada/revogada. Sua recomendação de doubles refere-se a testes unitários de API; distingue integração com persistência no ambiente `tests`.

**Política específica de currículo documentada em artefatos técnicos:** `application/versao_curriculo.py:CurriculoNaoEncontrado` explica “ausência e propriedade de outro usuário sob a mesma resposta”; a prévia H5 e seleção em `prompts/backend/20261008-183601-previa-versao-curriculo-v001.md` e `20261007-190814-selecao-itens-versao-curriculo-v001.md` registram a mesma ocultação. `test_integracao_rejeicao_referencia_curriculo.py:test_curriculo_de_outro_usuario_e_indistinguivel_do_inexistente` compara status e corpo de edição. Isso sustenta 404 uniforme para o vetor (ii), sem projetar a regra para recusas de middleware.

**Só implementado, sem contrato público detalhado encontrado:** textos exatos das três mensagens abaixo; política por campo extra de cada DTO; coexistência geral 403/404 para todos os subrecursos num único documento normativo. A segurança exige negar, mas não fixa uma mensagem global igual para todos os erros. Não há fundamento para exigir que 401, 403 e 404 sejam idênticos entre si, nem igualdade de cabeçalhos dinâmicos de correlação.

#### F2 — Middleware e composição atual

`src/backend/api/middleware_autenticacao.py:dispatch` lê `request.cookies.get(COOKIE_SESSAO)`, chama `autenticar`, instala `request.state.usuario_id = usuario_id.valor`. `_usuario_id_recurso_estudante` reconhece **qualquer método** sob `/estudantes/{uuid}/curriculos`. Se UUID diverge, responde antes de `call_next`:

```python
status_code=403,
content={"detail": "A sessão não pode acessar este recurso."}
```

Sem cookie ou sem identidade validada: `401`, `{"detail":"Sessão ausente ou inválida."}`. A comparação não consulta currículo nem prova existência do dono indicado.

`src/backend/api/factory.py:256–259`: `if autenticador_sessao is not None: app.add_middleware(...)`. Isso continua condicional. **A informação antiga sobre `main.py` deixou de ser verdadeira:** `src/backend/main.py` hoje chama `create_app(autenticador_sessao=AutenticadorSessaoIndisponivel(), ...)`. Esse adapter, em `src/backend/infrastructure/security/autenticador_sessao_indisponivel.py`, retorna sempre `None`. Portanto `main.app` instala middleware, com fallback fechado; não tem autenticação persistida funcional nem os executores de currículo injetados por esse módulo.

`src/backend/tests/test_api_middleware_autenticacao.py:test_app_exportada_instala_autenticador_fechado` verifica esse fallback. O novo teste não deve importar `main.app` nem afirmar ausência de autenticador.

#### F3 — Inventário completo das rotas registradas de currículo

Abreviações: `U=/estudantes/{usuario_id}/curriculos`, `C=U/{curriculo_id}`. Todos os donos passados aos casos de uso abaixo vêm do **caminho**, convertidos em `UsuarioId`; o middleware valida a igualdade desse valor com a **sessão**. Corpo não fornece dono efetivo. Status abaixo são derivados do fluxo do código atual com executores configurados, sessão A válida e payload válido; não são resultados de nova execução nesta análise. Sem executor configurado, o handler alcançado responde 503; por isso não usar dependência ausente para provar isolamento.

| Método/caminho | Dono e outros IDs | Vetor (i): sessão A, dono B no caminho | Vetor (ii): dono A, recurso B | Controle próprio | Fonte |
|---|---|---|---|---|---|
| GET U | dono no caminho | middleware 403; listagem não executada | Não há ID de recurso; listar A filtra dono no caso e repositório, 200 sem B | 200 | `api/listagem_versoes_curriculo.py:85–110`; `application/listagem_versoes_curriculo.py:executar` |
| POST U | dono no caminho; dados da versão no corpo | middleware 403; criação não executada | Não há ID de currículo fornecido; criar sob A produz dono A | 201 | `api/versao_curriculo.py:242–265`; `application/versao_curriculo.py:CriarVersaoCurriculo` |
| PUT C | dono e currículo no caminho | middleware 403, caso não executado | caso de uso obtém por ID e compara dono; 404 | 200 | `api/versao_curriculo.py:204–233`; `application/versao_curriculo.py:EditarVersaoCurriculo.executar` |
| PUT C/ordem-secoes | dono/currículo no caminho; ordem no corpo | middleware 403 | caso confere dono, 404 | 204 | `api/versao_curriculo.py:175–202`; `application/versao_curriculo.py:AtualizarOrdemSecoesCurriculo.executar` |
| DELETE C | dono/currículo no caminho | middleware 403 | caso confere dono antes de excluir, 404 | 204 | `api/exclusao_versao_curriculo.py:55–76`; `application/exclusao_versao_curriculo.py:executar` |
| GET C/previa | dono/currículo no caminho | middleware 403 | caso confere dono antes de ler usuário/itens, 404 | 200 | `api/previa_versao_curriculo.py:282–309`; `application/previa_versao_curriculo.py:143–159` |
| POST C/itens | dono/currículo no caminho; tipo/item_id no corpo | middleware 403 | currículo B: caso recusa com 404 antes de consultar item. Currículo A + item B: `ItemNaoEncontrado`, 404 | 201 | `api/itens_versao_curriculo.py:185–214`; `application/selecao_itens_versao_curriculo.py:99–111` |
| DELETE C/itens/{tipo}/{item_id} | todos os IDs no caminho | middleware 403 | currículo B: caso recusa com 404. Currículo A + item B não selecionado: regra de remoção, 422; não há consulta de dono do item | 204 com referência selecionada | `api/itens_versao_curriculo.py:217–246`; `application/selecao_itens_versao_curriculo.py:DesselecionarItemVersaoCurriculo.executar` |

Para as oito rotas: sem sessão ou com sessão inválida, expirada ou revogada, o middleware recusa com **401**, antes da propriedade e dos executores. Nos seis endpoints com `curriculo_id`, a guarda do caso de uso é `curriculo is None or curriculo.usuario_id != entrada.usuario_id`, lançando `CurriculoNaoEncontrado("Versão de currículo não encontrada.")`, traduzido em `404` com `detail`. Portanto ambos os mecanismos protegem esses endpoints, em etapas diferentes.

Não foi encontrada rota GET C isolada, exportação ou rota de revisão registrada no checkout: busca de `/curriculos` em todos os módulos de API e registro em `factory.py`; `api/revisao_versao_curriculo.py` tem **0 bytes**. Há caso de uso de revisão que delega à prévia (`application/revisao_versao_curriculo.py`), mas isso não torna uma rota executável. Não inventar endpoint nem incluí-lo como se já existisse.

#### F4 — Propriedade, persistência e itens

`src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py:obter_por_id` faz `self._session.get(CurriculoRegistro, curriculo_id.valor)`: não filtra dono. A guarda de objeto está nos casos de uso, não nesse método do repositório. `listar_por_usuario` filtra `CurriculoRegistro.usuario_id == usuario_id.valor`; o caso ainda descarta retornos alheios. `salvar`, `atualizar` e `excluir` fazem flush; commit pertence à composição. Exclusão apaga seleções antes da versão.

`application/selecao_itens_versao_curriculo.py:SelecionarItemVersaoCurriculo` usa a porta `ConsultaProprietarioItem`, com mesma falha para item inexistente ou alheio. `application/previa_versao_curriculo.py:executar` usa `ConsultaItemPerfil` e omite item ausente, alheio ou inconsistente. A busca no diretório de infraestrutura por consultas/proprietário não localizou adapter concreto dessas duas portas; a análise de seleção registra o adapter como handoff. Isso não autoriza implementá-lo como produção dentro do teste.

`fixtures/perfis_integracao.py:popular_perfis_fake` persiste usuários/currículos por sessão **síncrona**; itens são reconstruídos em memória por `ler_perfis_fake`. Seu hash é `hash-fake-nao-utilizavel-em-autenticacao`. Não é fixture de login nem comprova persistência real dos itens. O texto “itens ainda não possuem mapping” é histórico: a metadata atual importa tabelas de formação, experiência e outros itens (`infrastructure/persistence/sqlalchemy/metadata.py`). Não reutilizar esse texto como fato atual.

#### F5 — Sessão real e harness disponível

`infrastructure/security/tokens_sessao.py:CriadorSessaoSeguro.criar` gera 32 bytes, codifica Base64 URL-safe sem padding, persiste SHA-256, criada_em UTC e expiração +8h; `RevogadorSessaoSeguro.revogar` atualiza por hash. `AutenticadorSessaoPersistida.autenticar` usa SHA-256 e `datetime.now(timezone.utc)`. `RepositorioSessaoSqlAlchemy.obter_usuario_ativo` faz join com usuários e filtra expiração `> instante`, revogação nula e `deleted_at` nulo. Não há relógio injetável nesses adapters.

**Checkout:** os dois caminhos `test_integracao_contrato_credenciais_sessao.py` e `fixtures/sessoes_integracao.py` não existem. **Histórico local:** `git log --all -- <dois caminhos>` encontra `eca8708 test: contrato credenciais sessao #391`; `git branch -a --contains eca8708` indica `test-validacao-contrato-credenciais`; `git merge-base --is-ancestor eca8708 HEAD` retorna 1. Seus conteúdos foram lidos via `git show`, não tratados como arquivos da base.

Nesse commit, `BancoSessoesIntegracao` usa arquivo SQLite temporário com aiosqlite ou schema PostgreSQL aleatório, aplica `command.upgrade(..., "heads")` em thread, restaura `DATABASE_URL`, oferece sessões assíncronas e cleanup. A suíte emite com `CriadorSessaoSeguro`, altera timestamps no banco para expiração/revogação e também configura login real. Há diferenças internas: docstring diz que não há `alembic.ini`, mas ele existe na base atual; helper HTTP desconecta cedo e usa HTTP. Reuso futuro exige nova inspeção, não cópia cega.

**Harness da base:** `test_integracao_isolamento_dados_estudantes.py` e `test_integracao_recusa_perfil_alheio.py` chamam a aplicação por ASGI com portas em memória; o segundo mantém `receive` aberto até o último fragmento, usa HTTPS e timeout. `test_integracao_persistencia_dados_pessoais.py:setUp` usa SQLite síncrono com `StaticPool` e `Base.metadata.create_all`; esse teste não aplica migrations. Esses são os precedentes disponíveis, não um harness assíncrono de sessão já mergeado.

#### F6 — Histórico local: identificação e limites

Método: `git log --all --oneline --grep=... -i`, histórico por caminho (`git log --format='%h %s' -- <arquivos>`) e `git show --stat` dos merges relevantes. Números de PR abaixo vêm das mensagens locais de merge, não de suposição pelo número do card.

| Trabalho identificado | Evidência local e identificação | Artefato relacionado |
|---|---|---|
| Contrato #458 | merge `647a2b0`, mensagem `Merge pull request #458`; commits `575006e`, `1627442`, `d212f3d` | `docs/contrato-credenciais-sessao.md`, segurança e ambiente; contrato daquele commit lido |
| Emissão/persistência inicial | merge #461 `d98e3a7`, commit `13979d8`; stats incluem migration `20261012_0004_criar_sessoes.py` | token, repositório, sessão, login |
| Sessão revogável #463 | merge `dc71962`, commit `746fd35`, stats de logout, tokens e repositório | #463 acrescenta revogação; não atribuir a ele sozinho toda a persistência inicial |
| Middleware e instalação na fábrica | merge #464 `b39ea23`, commit `4b2f89a`; também merge #468 `fea8f24`, commit `3c0e97e`, com arquivos equivalentes no histórico | `api/middleware_autenticacao.py`, `api/factory.py`, autenticador/repositório |
| Fallback em main e atualização do isolamento | merge #515 `2748d21`, commit `d6ba138`; diff/stat explícito | `main.py`, adapter indisponível, testes de middleware e isolamento |
| Auditoria/correlação posteriores | histórico por caminho: `d84bb05`, `c34231f`, `6599238`, `8310298` | middleware/logging; não inferido número de PR |
| Edição de versão | `440d120` domínio/aplicação, `910a0fc` persistência, `d877b79` rota; merge #158 `388fa9e` localizado por mensagem | `application/versao_curriculo.py`, `api/versao_curriculo.py` |
| Criação de versão | `9a8328f` aplicação, `26c66f8` persistência, `a68aaa7` rota; merge #159 `5d5b185` localizado | mesmos módulos |
| Seleção de itens | `a2c6be0` aplicação, `69a1623` persistência, `c18340f` rotas; merge #166 `118974f` | seleção e `api/itens_versao_curriculo.py` |
| Listagem | `df67ee7`, `6e2d56f`, `18565b8`; merge #447 `9531b6b` encontrado | listagem aplicação, repositório e rota |
| Prévia | `cbd5729` aplicação, `8d2a8cb` rota; merge #445 `1abd0e1` encontrado | prévia; `0c208c4`, `78313ac`, `d0571d8` evoluem ordenação/projeção |
| Exclusão | `787ad57`, `b7af265`, `01968c5`; merge #469 `fc613d5` | exclusão aplicação, persistência e rota |
| Ordem/modelo/propriedade atual | `7f30fc9`, `888efd8`, `de40f96` no histórico dos arquivos; `e5bfa01` persistência da ordem | versão, seleção e mapeamento |
| Isolamento #150 | `072cb8a` cria teste e análise v004; merge #451 `ffbd0a2`; `d6ba138` o atualiza | `test_integracao_isolamento_dados_estudantes.py` |
| Revisão anunciada | `73f02d0`, `f561fd0` têm mensagens de rota/revisão; arquivo atual vazio e sem registro na fábrica | divergência, não evidência de endpoint atual |
| Harness ainda fora do HEAD | `eca8708` / branch local citada | dois arquivos do contrato; estado de PR remoto desconhecido |
| Atualização documental posterior | `11e9389`, mensagem merge #545, localizado por `--all` | contrato atual se autodescreve em termos de implementação; não presumir merge remoto ou no HEAD pela listagem |

Não foi encontrado, nas buscas locais por composição/ativar/autenticador e nos handoffs lidos, um identificador inequívoco de card **pendente** para ligar o autenticador persistido em `main.py`. Existe o trabalho já realizado #515 e o fallback explicitamente transitório. Não declarar que não há card remoto; isso permanece lacuna.

#### F7 — Cobertura existente e incremento necessário

| Fonte | Cobertura observada | O que não prova |
|---|---|---|
| `test_integracao_isolamento_dados_estudantes.py`, arquivo completo | ASGI + middleware e casos reais de listagem/edição; cookie A determinístico, controle próprio; leitura/escrita cruzada; sem cookie e token inválido; comparação de estado em memória | usa `status >= 400`, não exige 403/401 exatos; não usa banco/sessão real; não cobre vetor (ii), exclusão, prévia, itens ou ordem |
| `test_api_middleware_autenticacao.py`, seções lidas | dispatch direto com stub; 401/403 de listagem, criação, edição e itens; state; configuração da fábrica; fallback main | banco e cadeia HTTP completa com validação persistida; a matriz lida não inclui exclusão da versão, prévia ou ordem |
| `test_integracao_rejeicao_referencia_curriculo.py`, completo | edição ASGI, caso real, repositório em memória; 404 igual em alheio/ausente, sem escrita; 422 e positivo | compõe sem autenticador; não prova encadeamento com middleware |
| `test_integracao_recusa_perfil_alheio.py`, completo | harness ASGI robusto e spies envolvendo casos reais, matriz de perfil/contato | são outros recursos; não usar seu 404 de perfil para definir currículo |
| `test_application_versao_curriculo.py:90–135` | `assertRaises(CurriculoNaoEncontrado)`, título original e `curriculos_atualizados == []` para versão alheia; mesma exceção para ausente | unitário não é teste integrado; outros cenários só inventariados por nome |
| `test_application_previa_versao_curriculo.py:561–590` | mesmo teste percorre versão inexistente e alheia; exige exceção e `repositorio_usuario.consultas == []`, `consulta.consultas == []` | não prova adapter de itens real nem sessão persistida |
| `test_application_selecao_itens_versao_curriculo.py:172–245` | versão alheia/ausente: exceção e nenhuma consulta de dono/escrita; item alheio/ausente: `ItemNaoEncontrado`, referências vazias e nenhuma atualização | não prova estado SQL após HTTP; remoção própria só inventariada por nome |
| `test_application_listagem_versoes_curriculo.py:140–175` / `test_application_exclusao_versao_curriculo.py:110–145` | listagem exige só a versão própria mesmo com double devolvendo alheia; exclusão compara `str(alheia.exception) == str(ausente.exception)` e `excluidos == []` | sem prova da sessão persistida |
| `test_infrastructure_autenticador_sessao.py` | nomes de testes de hash, tempo UTC, revogação e conta excluída | recorte não comprova execução de consulta contra banco real |

Incremento recomendado: não refazer testes isolados das regras; fechar a fronteira ASGI → middleware → autenticador/repositório de sessão → casos de currículo → banco e expandir a matriz de rotas com status exato e leitura SQL independente.

#### F8 — Ambiente e bloqueios pré-existentes

1. `nix/tests.nix`: `packages = [ pkgs.git ];`. Não declara Python nem aiosqlite, servidor PostgreSQL ou provisionamento de banco. `nix/backend-python-packages.nix` lista FastAPI, Uvicorn, SQLAlchemy, Alembic, Psycopg e pydantic-settings; não aiosqlite. `flake.nix` aponta `tests` para esse arquivo. A inspeção executável de PATH no shell mostrou `/usr/bin/python3` e um shim Windows para `python`; são herdados, não Python fornecido pelo projeto e não podem ser usados como substitutos.
2. Grafo Alembic: os dois arquivos `20261015_0011_criar_cursos.py` e `20261015_0011_exclusao_logica_formacoes_academicas.py` declaram `revision = "20261015_0011"`; os dois `20261015_0012_criar_links_profissionais.py` e `20261015_0012_criar_projetos_academicos.py` declaram `revision = "20261015_0012"`. Ambos os pares compartilham respectivos predecessores. Isso confirma colisões de identidade no grafo; `upgrade heads` não é caminho confiável para aplicar todas as migrations. O erro concreto de upgrade não foi reproduzido nesta análise e não deve ser inventado.
3. `api/sessoes.py` registra apenas `DELETE /sessao/atual`; `docs/contrato-credenciais-sessao.md` diz “Não existe atualmente uma rota `GET /sessao/atual`”. Ausência confirmada; bloqueia cenários que dependam desse GET, não o teste proposto, que usa GET da listagem/prévia como alvo privado.
4. `alembic.ini`: `script_location = src/backend/infrastructure/persistence/alembic`; `env.py` exige `DATABASE_URL`, importa metadata e cria engine assíncrona. A documentação de ambiente usa PostgreSQL local e `alembic upgrade head`; o harness em branch usa `heads`. Não há evidência de PostgreSQL disponível nesta sessão. SQLite descartável com driver assíncrono é recomendação, não serviço já instalado pelo shell.

### Divergências e precedência explícita

| Divergência | Fonte mais confiável para esta análise | Justificativa e tratamento |
|---|---|---|
| análise de perfil diz main sem autenticador; código atual injeta fallback | `main.py` + teste atual + commit `d6ba138` | Evidência executável e mudança posterior; não reproduzir diagnóstico antigo |
| análise #150 v004 exige expectedFailure; teste atual não tem as quatro marcações e já usa cookie/middleware | teste atual + histórico #515 | Não transportar instrução histórica de falha esperada para teste novo |
| contrato #458 permitia 403 ou 404 segundo política; contrato atual descreve 403 no middleware; casos retornam 404 por recurso | contrato atual para middleware, código/docstring/teste de currículo para objeto | São camadas e vetores diferentes; falta consolidação normativa, não licença para uniformizar tudo |
| contrato diz identidade autenticada; handlers de currículo ainda montam DTO com UUID do caminho | código atual para mecânica, contrato para obrigação | Igualdade validada pelo middleware protege composição com auth; teste deve demonstrar isso, não alegar leitura direta de state pelo handler |
| fixture antiga fala em ausência de mappings de itens; metadata atual importa modelos | metadata atual | Fixture continua híbrida; não atribuir a ela persistência que não realiza |
| histórico anuncia rota de revisão; arquivo atual vazio | checkout + factory atual | História não prova presença atual; endpoint fica fora e vira achado |
| harness da branch diz ausência de alembic.ini | `alembic.ini` atual | Não reutilizar sua configuração/documentação sem reavaliação |

### (b) Lacunas — opções e natureza da decisão

| ID | O que nenhum artefato examinado resolve | Opções viáveis | Recomendação e justificativa | Produto? |
|---|---|---|---|---|
| L1 | Política normativa única que reconcilie 403 de caminho e 404 de objeto em todo currículo | manter distinção; adotar 404 global; adotar 403 global | caracterizar distinção atual no teste, com fontes por camada; mudança global deve ter nova decisão | Sim para alterar política; não para caracterizar |
| L2 | Texto público obrigatório de cada erro e política global de mensagem alheio/inexistente | exigir mensagem atual; validar só negação/estrutura; definir texto novo | fixar mensagens atuais como caracterização; comparar igualdade alheio/ausente apenas dentro do vetor (ii) | Não para caracterização; sim para novo contrato público |
| L3 | Política expressa para `usuario_id` extra no corpo/query por DTO | rejeitar extra; ignorar extra; padronizar futuramente | testar ausência de efeito na propriedade; caracterizar ignorado onde DTO não proíbe e 422 em ordem-secoes; não mudar DTOs | Não para teste; produto/API para padronização |
| L4 | Estado remoto e ordem de merge do harness #391 | esperar merge e reutilizar; usar base e fixture dedicada | usar base, sem dependência de merge; branch não é arquivo disponível ao implementador | Não, decisão técnica |
| L5 | Harness assíncrono completo já incorporado para esse cenário | adaptar precedentes da base; condicionar ao harness de outra branch | criar fixture exclusiva do teste, com migração e AsyncSession; reutilizar padrão ASGI robusto e constantes de perfis onde útil | Não |
| L6 | Card pendente inequívoco para composição persistida na raiz | buscar responsável/card posteriormente; abrir novo trabalho após triagem | encaminhar sem inventar número nem bloquear teste da fábrica | Não para teste; planejamento posterior |
| L7 | Implementação concreta das portas de item encontrada na infraestrutura | doubles determinísticos; fixture de teste que consulta ORM; aguardar adapter de produto | doubles das duas portas, explicitamente limitados; currículo, seleções e sessões permanecem SQL reais | Não; adapter de produto é handoff |
| L8 | Garantia de SQLite migrado e PostgreSQL disponível no ambiente tests atual | provisionar PostgreSQL; SQLite temporário; aguardar correção do ambiente | SQLite temporário como alvo obrigatório de validação; PostgreSQL fica handoff opcional, sem URL herdada | Não |
| L9 | Conteúdo remoto completo de cards e causa de arquivo de revisão vazio | inferir pelo histórico; investigar depois | registrar indisponibilidade e não inferir contrato de endpoint | Não para excluir rota inexistente; produto para restabelecê-la |

### Hipóteses

H1: após ajustes temporários autorizados de ambiente/grafo, SQLite aceita a cadeia completa; precisa ser validado, não foi provado aqui. H2: o helper ASGI do teste de perfil é adaptável à matriz de currículos e respostas 204; validar coleta de corpo vazio. H3: fixtures dedicadas conseguem manter transações externas e consulta independente sem alterações de produção. Falha dessas hipóteses pede revisão de harness, não correção de produto nesta skill.

### Perguntas em aberto

L1–L9 acima. Nenhuma exige resposta de produto para implementar a fatia proposta como caracterização explícita das interfaces existentes. Mudança de status, texto normativo ou restauração de endpoint exige decisão separada.

### Escopo

Novo teste integrado de segurança de currículo, fixture dedicada, dados sintéticos, aplicação montada pela fábrica com auth persistida e casos reais; SQL real para usuários/sessões/currículos/seleções; portas de conteúdo/propriedade de itens controladas em memória; execução isolada, skips restritos a recursos ausentes.

### Fora do escopo

Middleware, routers, regras, ORM/adapters produtivos, composição raiz, correções permanentes de migrations/Nix, CSRF/Origin/rate limiting, frontend, CI, exportação inexistente, GET de sessão inexistente e criação de adapter produtivo de itens. Nenhum desses achados será corrigido nesta análise ou automaticamente pela futura skill.

### Critérios de sucesso

O teste novo deve ser descoberto por unittest, executar positivamente com ambiente preparado, exigir 401/403/404 exatos conforme vetor, não vazar marcadores privados, provar controle próprio por endpoint, observar executores e comparar banco antes/depois em sessões distintas. Não usar `expectedFailure` em proteção já implementada. Skip não conta como prova de segurança. Uma execução real da matriz em `.#tests` é necessária antes de declarar a entrega validada.

## Restrições aplicáveis

`AGENTS.md` raiz e backend lidos; busca não encontrou AGENTS adicionais em tests/fixtures/prompts nem override de destino. Nix obrigatório; integração em `tests`; Git fora do Nix. Toda classe/função nova deverá documentar o que faz, como e finalidade. Proveniência em todo código novo: `Proveniência: decision-analysis prompts/backend/20261018-123741-recusa-curriculo-alheio-middleware-ativo-v001.md#v001`.

Só este Markdown pode ser escrito nesta atividade. As exceções temporárias descritas para a futura execução decorrem da instrução explícita do usuário, não de permissão inferida para corrigir ambiente ou banco.

## Classificação comentada

`engineering`, com `security`, `integration`, `data`: o resultado é prova executável das fronteiras existentes. Risco alto pelo potencial de vazamento/alteração de dados; reversibilidade fácil porque a decisão adiciona testes. Incerteza média pelo harness e pelo grafo de migrations, sem incerteza sobre a necessidade de negar acesso alheio.

## Decisão de roteamento

Inventário imediato observado: `prompts/ambientes`, `backend`, `frontend`, `requisitos`, `revisao`, `templates`. Escolha `prompts/backend`, onde estão as análises de isolamento #150, recusa de perfil e rotas de currículo. `requisitos` seria adequada para definir política nova, `ambientes` para consertar Nix; não são a entrega. `revisao` e `templates` não descrevem o propósito desta análise inicial.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| security | Alta | provar os dois vetores com sessão válida | 401 isolado não prova propriedade |
| correctness | Alta | controle próprio e estado SQL preservado | recusa pode ocultar rota quebrada ou escrita indevida |
| reliability | Alta | isolamento, corpo completo, skips explícitos | evita falso positivo e erro de ambiente na descoberta |
| simplicity | Média | sem dependência de merge externo | entrega reproduzível no checkout |
| modifiability | Média | fixture dedicada e matriz por operação | reduz duplicação sem alterar testes existentes |

## Alternativas consideradas

**Estado atual:** integração A/B com repositório e auth em memória só para listagem/edição; não atende a sessão/banco reais e à matriz completa.

**A — Expandir apenas integração em memória.** Viável e barata; mantém precedentes da base, cobre todos os caminhos via ASGI, mas deixa sem prova consulta persistida, expiração/revogação reais e leitura direta do banco.

**B — Integração com banco isolado e fixture dedicada na base (recomendada).** Reaproveita o padrão ASGI robusto já incorporado, compõe adapters de sessão/currículo reais e acrescenta harness só de teste. Cobre fronteiras faltantes sem esperar outra branch. Aceita preparação temporária de ambiente/grafo para validar, com restauração obrigatória.

**C — Reutilizar `fixtures/sessoes_integracao.py` de #391 após merge.** Viável com dependência explícita: incorporar primeiro o trabalho que contém `eca8708`, revisar atualidade e só depois implementar este teste. Evita repetir infraestrutura, mas introduz ordem de merge e exige resolver as divergências do helper e configuração. Não usar import condicional que silencie ausência de arquivo interno como se fosse recurso externo opcional.

## Perfil de pagamento comparativo

Escala ordinal; não somar. Base: F2–F8. Confiança alta para diferenças de cobertura observadas, média para custo futuro do harness.

| Dimensão | Prioridade | A | B | C | Confiança | Base |
|---|---|---|---|---|---|---|
| security | Alta | +1 | +2 | +2 | Alta | B/C integram consulta persistida |
| correctness | Alta | +1 | +2 | +2 | Alta | B/C permitem leitura SQL independente |
| reliability | Alta | +1 | +1 | 0 | Média | B exige validar harness; C depende de merge |
| simplicity | Média | +2 | -1 | +1 | Média | custo de fixture nova versus reuso |
| modifiability | Média | +1 | +1 | +2 | Média | C compartilha harness de sessão |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado nesta linhagem. Decisões de perfil e #150 não são substituídas.

### (c) Decisão recomendada nesta versão

Adotar B: criar futuramente `src/backend/tests/test_integracao_recusa_curriculo_alheio.py` e `src/backend/tests/fixtures/curriculos_autenticados_integracao.py`. Não modificar teste antigo de isolamento nem copiar seus cenários integralmente. Usar `unittest.IsolatedAsyncioTestCase`; dados e app novos em cada caso/subcaso independente. Não importar fixtures de branch não incorporada. Se #391 for incorporado antes da implementação, a mudança de estratégia de harness deve ser reavaliada explicitamente; não assumir reuso silencioso.

#### Estrutura concreta do harness recomendado

1. Fixture `BancoCurriculosAutenticadosIntegracao`: `TemporaryDirectory` + arquivo SQLite, URL `sqlite+aiosqlite`, migrations via `Config` apontando ao `alembic.ini` real, `command.upgrade(...,"heads")` em `asyncio.to_thread` fora do loop assíncrono do teste. Restaurar `DATABASE_URL` em `finally`, serializar a preparação; não paralelizar mutação de variável de ambiente. Registrar engine, fábrica `async_sessionmaker(expire_on_commit=False)` e cleanup assíncrono imediato. Não usar `create_all` como substituto silencioso de migrations.
2. Seed com dois usuários A/B, currículos privados CA/CB, títulos e itens com marcadores distintos. IDs fixos por banco novo; e-mails `a@example.test`/`b@example.test`; hash de senha sintético, sem fazer login. Emitir sessão A com `CriadorSessaoSeguro(RepositorioSessaoSqlAlchemy(...)).criar(A)` e commit antes da requisição. Manter token só na memória e enviá-lo como Cookie em escopo HTTPS. B pode ter sessão própria para controles, mas nenhuma chamada de ataque usa token B.
3. Persistir currículos e seleções com `RepositorioCurriculoSqlAlchemy.salvar`; commit do seed. Selecionar referência de um item sintético de cada dono; os objetos de item e suas duas consultas ficam no double dedicado, documentado como tal. Não alegar persistência da entidade de item: o que é real é a linha de seleção `curriculo_itens`, o currículo, usuário e sessão. Não há necessidade de transpor regras específicas de formação/projeto para compor esses dados.
4. Compor `create_app` com `AutenticadorSessaoPersistida` + `RepositorioSessaoSqlAlchemy`, `RepositorioCurriculoSqlAlchemy`, casos `CriarVersaoCurriculo`, `EditarVersaoCurriculo`, `AtualizarOrdemSecoesCurriculo`, `ListarVersoesCurriculo`, `ExcluirVersaoCurriculo`, `SelecionarItemVersaoCurriculo`, `DesselecionarItemVersaoCurriculo`, `GerarPreviaVersaoCurriculo`. Para prévia, usar repositório de usuário real e double da porta de itens. Para criação, gerador determinístico só de teste. Não injetar manualmente `request.state`.
5. Envolver `executar` dos casos reais em spies com `AsyncMock(wraps=...)`, como o precedente de perfil. Não substituir o comportamento real. Para recusa no middleware, zero chamadas/awaits em todos os executores. Para vetor (ii), executor correspondente chamado uma vez, recebendo `usuario_id=A`; não exigir zero chamadas porque a guarda está dentro dele. Usar deltas de contadores ou zerar por cenário.
6. Sessão ORM do fluxo sob controle externo; após chamada, flush/commit pela fixture, inclusive para tornar detectável uma escrita indevida ocorrida apesar da resposta de erro. Ler snapshots em **outra sessão ORM**, sem identity map compartilhado. Comparar todas as colunas de currículos A/B e conjunto ordenado de seleções, inclusive dono, título, modelo, visibilidade, ordem e existência; comparar contagem de versões para tentativa de criação. Não fazer rollback antes do snapshot que esconderia uma escrita indevida. Após assertivas, cleanup elimina o banco inteiro.
7. Adaptar a mecânica ASGI de `test_integracao_recusa_perfil_alheio.py` na nova fixture, sem import de helper privado desse teste: HTTPS, path/query separados, timeout 5s e `receive` aguardando fim do corpo. Coletar status, headers e JSON, tratando 204 como corpo vazio. Uma extração compartilhada com alteração do teste antigo não é necessária nesta entrega.

#### Matriz de cenários implementável

Precondição comum P: banco isolado migrado, usuários ativos A/B, CA/CB, referências IA/IB distinguíveis e sessão A emitida/persistida. Escritas usam JSON válido: título `"Atualizado A"`, layout `"compacto"`, `is_public=false`; criação equivalente; seleção `tipo` válido + UUID IA; ordem completa com os sete valores de `SecaoCurriculo`, permutada validamente. Para remoção própria, IA deve estar selecionado; para seleção própria, usar outro item de A ainda não selecionado. Seed novo evita conflito entre controles.

Nível R: rota via aplicação real, com middleware/casos/adapters e banco real. Nível D: verificação complementar por leitura direta do banco real, nunca teste unitário isolado. Cada linha abaixo se expande em métodos/subtests com diagnóstico da operação e identidade.

| ID / objetivo | Pré-condições e passos | Resultado esperado | Nível | Fonte/oráculo |
|---|---|---|---|---|
| S1 — provar rotas funcionais próprias | P; chamar cada uma das oito rotas no alvo A/CA, com seed apropriado à operação | GET lista/prévia 200 com marcador A e sem B; edição 200 e dados persistidos; criação 201, dono A e contagem +1; seleção 201 com item A persistido; ordem, remoção e exclusão 204 com efeito correspondente. B intacto | R+D | inventário F3, casos e repositório F4 |
| S2 — bloquear dono B no caminho | P; para cada uma das oito rotas, sessão A + U de B, CB quando aplicável, payload válido | 403 e detail atual; nenhum executor chamado/aguardado; nenhum marcador privado B; snapshots A/B e seleções idênticos, inclusive criação sem linha nova | R+D | contrato, `_usuario_id_recurso_estudante` e `dispatch` F1/F2 |
| S3 — bloquear currículo B sob caminho A | P; seis rotas com curriculo_id: edição, ordem, exclusão, prévia, seleção, desseleção; substituir CA por CB mantendo A | 404 `{"detail":"Versão de currículo não encontrada."}`; executor correspondente chamado uma vez com A; banco intacto. Prévia não lê itens, seleção não consulta proprietário de item após falha de currículo | R+D | guardas dos casos F3/F4 |
| S4 — ocultar existência no vetor de objeto | repetir S3 com UUID inexistente válido em banco novo equivalente; comparar status+JSON por operação | alheio e inexistente produzem o mesmo 404/detail. Não comparar X-Correlation-ID nem exigir igualdade com o 403 de S2 | R+D | exceção documentada e teste de referência de currículo F1/F7; caracterização estendida das guardas idênticas |
| S5 — impedir seleção de item B em currículo A | P; POST CA/itens com IB e depois com item inexistente | ambos 404 `{"detail":"Item do perfil não encontrado."}`; seleção CA/CB intacta por SQL; controle positivo com item A 201 | R+D | `SelecionarItemVersaoCurriculo.executar`, documentação específica de seleção |
| S6 — parâmetros do cliente não trocam dono | P; GET listagem e GET prévia sob A com query `usuario_id=B`; POST criação/PUT edição/POST itens sob A com campo extra `usuario_id=B` | respostas próprias normais no comportamento atual; DTO interno com A, criação pertence a A, B intacto. Separadamente PUT ordem com extra B retorna 422, sem executor/efeitos; comentário caracteriza extra=forbid local | R+D | §3.7 segurança; DTOs/handlers F3; L3 |
| S7 — ausência de sessão | P sem Cookie; todas as oito rotas com caminhos/payloads válidos | 401/detail uniforme, nenhum executor, snapshots intactos; Bearer ou query/corpo não substituem cookie | R+D | contrato de rotas protegidas e `dispatch` |
| S8 — sessão revogada | P; revogar token A por `RevogadorSessaoSeguro`, commit; reapresentar cookie antigo nas oito rotas | 401/detail igual a S7; nenhum executor, snapshots de currículo/seleções intactos | R+D | contrato, adapter/repositório de sessão F5 |
| S9 — sessão expirada | P; atualizar apenas `expira_em` da sessão para UTC no passado com margem (ex.: agora -1 dia), commit, nova consulta de auth; chamar oito rotas | 401/detail igual a S7; nenhum executor, currículos/seleções intactos | R+D | filtro `expira_em > instante`, contrato F5 |
| S10 — token desconhecido | P; cookie sintético não emitido, ao menos GET listagem e uma escrita válida | 401 uniforme e nenhuma escrita/executor | R+D | contrato e consulta por hash; complementa o double antigo com banco |

S8 verifica revogação persistida, sem exigir ciclo de logout HTTP/login completo; isso já pertence à suíte de contrato #391. S9 não usa sleep, não testa limite exato de expiração, não substitui o relógio global de produção. O teste de currículo só usa estado deliberadamente passado, conforme filtro existente. Conta excluída pode continuar na suíte de credenciais: não é necessária para provar propriedade de currículo.

Não adicionar GET C, GET `/sessao/atual` ou revisão fictícia para ampliar matriz. Não exigir que IB não selecionado em DELETE CA/itens produza 404; o fluxo atual pode produzir 422 e isso não é o mesmo que propriedade do currículo. Caso adicional de caracterização dessa remoção é dispensável para este aceite; não impor política nova.

#### Skips e recursos ausentes

- Detectar aiosqlite por import guardado; ignorar a classe SQLite com motivo `aiosqlite ausente; execute no ambiente Nix tests preparado` antes de criar engine. Não importar aiosqlite incondicionalmente no topo. Não capturar erro de asserção como skip.
- Python ausente não pode ser resolvido por decorator: é bloqueio do comando, a registrar no resumo. Não executar Python global para produzir um falso verde.
- Preflight das identidades de migration pode gerar `SkipTest("cadeia Alembic com revisões duplicadas; bloqueio preexistente ...")`, com pares específicos. Isso evita erros em ambiente não preparado, mas não valida migrations nem o teste de isolamento; a execução de aceite deverá usar o grafo temporariamente linearizado ou já corrigido por trabalho próprio. Demais falhas de migration não devem ser engolidas genericamente.
- Não é necessário skip por ausência de GET sessão: o cenário usa currículos. Não há classe PostgreSQL obrigatória nesta entrega, nem dependência implícita de `DATABASE_URL` herdada. Se futuramente adicionada, exigir URL de teste deliberada e schema descartável; sem isso, skip explícito. Nenhuma execução em banco compartilhado.
- FastAPI/SQLAlchemy/Alembic são pré-requisitos do Python de backend reutilizado no shell temporário. Não transformar falha do produto, 500, corpo truncado ou controle positivo falhando em skip/expectedFailure.

### Impacto da revisão

Inicial. Corrige, na interpretação desta demanda, dois contextos históricos obsoletos (main sem middleware e isolamento com expectedFailure), sem reescrever análises anteriores.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| security | prioritized | prova dos dois vetores e sessões persistidas | F1–F5; S2–S10 |
| correctness | prioritized | recusa com preservação real de dados e positivo funcional | S1 e leitura SQL independente |
| reliability | prioritized | resultado distinguível de dependência ausente e rota indisponível | skips restritos e controles positivos |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| simplicity | sem dependência de merge remoto | B usa checkout e fixture dedicada |
| modifiability | não repetir regras unitárias | matriz por fronteira/rota e doubles limitados às portas de item |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| security | sessão negada por fallback confundida com autorização real | Alta | estudantes e mantenedores |
| correctness | resposta de erro encobre escrita persistida ou rota sempre quebrada | Alta | titulares dos dados |
| reliability | corpo truncado ou skip genérico produz falso verde | Alta | equipe |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| security/correctness | banco migrado e fixture assíncrona nova | simplicity | aceito para acrescentar evidência ausente |
| independência de merge | pequena sobreposição futura de harness com #391 | modifiability | aceito; consolidar depois em trabalho próprio |
| limite de escopo | portas de itens em memória | amplitude de integração | aceito e declarado; não se afirma adapter real de conteúdo |
| execução local | diffs temporários e restauração de Nix/grafo | delivery-speed | aceito por autorização explícita, sem mudança definitiva |

## Riscos e efeitos de segunda ordem

- Caracterizações de status/texto podem congelar dívida; comentários devem apontar L1/L2 e não rotulá-las como norma global de segurança.
- Snapshot na mesma sessão pode ler cache; snapshot após rollback pode esconder escrita. Usar commit controlado e sessão nova, somente no banco descartável.
- O middleware reconhece prefixo de caminho, inclusive endpoints inexistentes. Um 403 isolado não prova registro da rota; S1 deve passar para todas as operações da matriz.
- Corrigir IDs do Alembic temporariamente torna aquela execução condicionada ao grafo transitório. Publicar o diff e declarar isso; não afirmar que a base original migrou com sucesso.
- Passar com doubles de itens não prova consulta de conteúdo contra banco nem todos os tipos de item. Essa limitação é intencional e deve constar no relatório de implementação.

### Achados de back-end — sem correção

1. Main está protegido por fallback fechado, mas não autentica sessão persistida nem compõe casos de currículo; teste da fábrica não certifica login ou operação de produção.
2. Identidade dos DTOs de currículo ainda vem do caminho. Na composição com middleware ela é validada por igualdade; compor a fábrica sem autenticador continua possível e é coberto por teste de compatibilidade existente. Não alterar essa API nesta tarefa.
3. Contrato de sessão e política de ocultação de currículo não estão consolidados por vetor. Não converter 404 em 403 ou o inverso sem nova decisão.
4. Revisão tem histórico de rota, mas arquivo vazio no checkout e sem registro: investigar em tarefa própria, sem adicionar endpoint no teste.
5. Colisões Alembic e ausência de Python/aiosqlite em tests são bloqueios de execução preexistentes; não são defeitos introduzidos pela suíte proposta.
6. GET de sessão não existe; não usar como probe de autenticação.
7. Consultas reais das portas de item não foram encontradas; documentação antiga de fixtures/mappings está desatualizada. Não corrigir documentação ou adapters nesta atividade.

## Validação da decisão

### Execuções realizadas nesta análise

Os primeiros comandos Nix falharam no sandbox por `/nix/var/nix/db/big-lock: Read-only file system`; foram repetidos com escalonamento pelo mecanismo de aprovação de ferramenta. Não houve contorno por ferramentas globais.

| Comando | Resultado observado | Limite |
|---|---|---|
| `nix develop .#tests --command sh -c 'command -v python3; command -v python; command -v alembic'` | shell iniciou; encontrou `/usr/bin/python3` e shim externo; saída 1 por alembic ausente | inspeção de PATH, não execução de testes com Python do projeto |
| `nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src` | **781 testes, OK, skipped=2**, 9,434s; saída 0 | execução informativa solicitada; integrações formais continuam exigindo tests; não houve teste novo |
| `nix develop .#quality --command ruff check src/backend` | **All checks passed!**, saída 0 | nenhum I001 encontrado; nenhuma correção aplicada |

O novo teste não foi executado, pois ainda não foi implementado e a atividade proíbe implementação. Migrations não foram corrigidas nem executadas. A suíte informativa já cobre testes que chamam integrações, mas não substitui o aceite formal em tests. Saídas de ferramentas são evidência de execução desta sessão, não arquivos fonte do produto.

### Protocolo futuro de execução e restauração

Antes de qualquer alteração temporária, registrar `git status --short` e diffs, confirmar que os caminhos a restaurar estão limpos. Se já houver mudanças do usuário nesses caminhos, não usar `git restore` sobre elas: executar em checkout/worktree isolado ou solicitar direção. Git/restore fora do Nix.

Para executar a suíte, a skill poderá temporariamente acrescentar a `nix/tests.nix` o Python do backend e aiosqlite: reutilizar `import ./backend-python-packages.nix { inherit pkgs; }` numa função de `python3.withPackages` e acrescentar `ps.aiosqlite`. Não alterar definitivamente Nix, flake ou lock. Registrar diff completo antes de restaurar; comandos mutáveis de desenvolvimento no ambiente apropriado.

Se as colisões ainda existirem, linearização **somente temporária**, preservando os corpos de upgrade/downgrade: manter cursos como `20261015_0011`, dar identidade única à exclusão lógica de formações (por exemplo `20261015_0011f`, predecessor cursos); ligar links como `20261015_0012` após essa exclusão; dar identidade única a projetos (`20261015_0012p`, predecessor links); apontar documentos `20261016_0013` para projetos. Os demais elos permanecem. Essa sugestão técnica deve ser validada pelo Alembic, não aplicada nesta análise. Nenhuma alteração em schema produtivo, banco compartilhado ou histórico remoto. Se aparecer outro conflito, reportar e reavaliar, sem ampliar a correção temporária indiscriminadamente.

Após preparar ambiente e grafo, executar:

```bash
nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest backend.tests.test_integracao_recusa_curriculo_alheio -v
nix develop .#quality --command ruff check src/backend

nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s src/backend/tests -t src
nix develop .#quality --command ruff check src/backend
```

Cada caso deve preparar SQLite e aplicar migrations automaticamente; não depender de banco iniciado manualmente. Se necessário diagnosticar o grafo, usar `nix develop .#tests --command env PYTHONPATH=src alembic heads`; para aplicação manual apenas em SQLite descartável, `DATABASE_URL=sqlite+aiosqlite:////tmp/<banco-exclusivo>.sqlite3` e `alembic upgrade heads`, sempre por `.#tests`. O ambiente temporário não fornece PostgreSQL servidor; não inventar execução PostgreSQL bem-sucedida.

No final de **cada execução** de teste, executar o gate completo Ruff. Se houver I001, seguir instrução do usuário:

```bash
nix develop .#quality --command ruff check --select I --fix <arquivos-apontados>
nix develop .#quality --command ruff check src/backend
```

Fix em produção que ultrapasse imports ou altere comportamento continua fora do escopo; reportar em vez de corrigir. O comando informativo não pode introduzir erros novos em relação ao baseline registrado. Quantidade total crescerá pelos testes novos; comparar falhas/erros, não exigir 781 como total final.

Antes do cleanup, copiar **os diffs completos** de Nix e migrations para o resumo da implementação. Depois usar `git restore -- nix/tests.nix` e `git restore -- <cada caminho de migration temporariamente alterado>`, inclusive documentos; restaurar só o que foi alterado pela atividade. Isso deve ocorrer em `finally` operacional, inclusive se testes falharem. Verificar `git status --short` sem nenhum arquivo em `nix/`, `flake.nix`, `flake.lock` ou `src/backend/infrastructure/persistence/alembic/versions/`. Só os arquivos de teste aprovados devem permanecer modificados. Repetir gate Ruff final após eventuais correções. Relatar separadamente: teste executado com grafo transitório, skips no grafo original e ausência de prova da composição raiz.

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| H1 — SQLite migrado funciona | banco até heads e seed válido | execução em tests com ajustes temporários identificados | novo erro de dialeto/grafo não previsto |
| H2 — ASGI coleta resposta inteira | status final, corpo completo e 204 vazio | controles positivos por rota | timeout, corpo truncado ou 503 |
| H3 — persistência observável | efeito positivo em sessão nova; negativos idênticos ao snapshot | SQL direto independente | escrita oculta por cache/rollback |
| Auth persistida está ativa no teste | token emitido real permite S1; revogação/expiração causam 401 | S1/S8/S9 | 401 em tudo ou executor fake |
| Propriedade funciona | S2 403 sem executor; S3 404 dentro do executor | spies e respostas exatas | apenas status genérico >=400 |
| Limpeza respeita escopo | status sem Nix/migrations alterados | diff copiado e git restore | qualquer resíduo em caminhos proibidos |

## Handoffs e atividades posteriores

| Responsabilidade | Classificação | Destino |
|---|---|---|
| teste ASGI + sessão/currículo SQL, matriz S1–S10 | integration / non-functional (security) | `$integration-system-testing-v1`, futura invocação com este caminho exato e v001 |
| fixture dedicada, spies e doubles de portas de itens | integration | mesma skill; somente dois arquivos propostos |
| preparação efêmera para executar, com restauração e diff no resumo | suporte descartável autorizado pelo usuário | mesma execução futura, sem mudança permanente |
| novos unitários de casos/middleware | unit | fora; não duplicar cobertura nesta entrega |
| composição de main, adapter produtivo de itens, rota de revisão ou GET sessão | product-change | backend responsável; sem alteração pela skill |
| correção definitiva Alembic e dependências de Nix | product-change / external-test-operations | trabalhos próprios, sem promover diffs temporários |
| CI, deploy, banco compartilhado, PostgreSQL externo | external-test-operations | fora desta entrega |
| status global de ocultação, textos normativos e campos extras | policy / product-change | decisão de produto/API se houver mudança; teste caracteriza atual |

A futura skill deve ler suas referências de gate restantes e todos os AGENTS aplicáveis antes de escrever, validar atualidade desta versão e comunicar aderência, alvo seguro e exclusões. Não executá-la agora: o usuário pediu somente análise. Não há necessidade de delegação a agentes para este trabalho.

## Síntese

Propor teste integrado com SQLite descartável, autenticação persistida e casos reais montados na fábrica, cobrindo oito rotas e distinguindo dono alheio no caminho (403) de currículo alheio sob dono próprio (404). A composição raiz atual tem middleware com autenticador fechado; esta suíte não certifica sua operação com persistência real. O principal risco de execução é a combinação de shell tests incompleto e grafo Alembic com identidades duplicadas. Ambos ficam fora da correção definitiva e exigem diagnóstico, preparação temporária autorizada, restauração e relato explícito.
