---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: v001
status: proposed
created_at: "2026-10-24T18:13:03-03:00"
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
    - path: src/backend/api/vagas.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: d1df2ab6f86fb899e1f4c59c9db11f9fc42f27ba
      availability: available
    - path: src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.tsx
      relationship: primary
      representation: source-code
      function: production
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: d1df2ab6f86fb899e1f4c59c9db11f9fc42f27ba
      availability: available
    - path: src/frontend/features/listar-vagas/api/cliente-vagas-grupo2.ts
      relationship: primary
      representation: source-code
      function: schema-contract
      format: typescript
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: d1df2ab6f86fb899e1f4c59c9db11f9fc42f27ba
      availability: available
routing:
  root: prompts
  selected_directory: prompts/frontend
  considered_directories: [prompts/frontend, prompts/backend, prompts/requisitos, prompts/ambientes, prompts/revisao, prompts/templates]
  confidence: medium
  rationale: "A decisão é sobre a prova da jornada e de seus estados visíveis. Frontend tem precedente de análise de jornada; backend é candidato forte, mas não representa sozinho o resultado para o usuário. Não existe pasta de testes entre as subpastas observadas."
classification:
  sphere: engineering
  concerns: [integration, reliability, user-experience]
  decision_kind: selection
  scope: system
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: low
---

# Análise de decisão — Busca de vagas com resultado, vazio e indisponibilidade

## Solicitação original

Insumo literal preservado no apêndice A. Título fornecido: **"Criar cenário E2E para busca de vagas com resultado, vazio e indisponibilidade."** Não foi fornecida descrição do card nem critérios de aceite. A instrução final foi **"Não implemente nada."** Esta entrega especifica testes futuros; não contém teste implementado nem afirma aprovação dos cenários propostos.

## Informações complementares

O usuário forneceu a skill `decision-analysis-v4` e as instruções gerais do repositório. Os arquivos locais correspondentes foram lidos. Esta é uma análise nova, sem herdar decisão de análises anteriores de vagas. Elas são fontes históricas a confrontar com a branch atual, não critérios novos nem aprovação desta proposta.

## Mudanças desde a versão anterior

Nenhum identificado — modo `initial`, v001. Não há versão anterior desta linhagem. Foram encontradas análises de contrato, adapter, API, acessibilidade e CSS de vagas, com objetos diferentes.

## Artefatos analisados

Estado comum a todos os caminhos relativos abaixo: working tree inicialmente limpo, baseado em `d1df2ab6f86fb899e1f4c59c9db11f9fc42f27ba`, branch `test-e2e-busca-vagas`. Consulta: `git branch --show-current`, `git rev-parse HEAD`, `git status --short`. Não houve consulta ao GitHub nem serviço externo. A origem na `dev` é declaração do usuário; não foi reconstruída por consulta remota.

O frontmatter identifica os três objetos principais. A tabela completa o registro dos demais arquivos efetivamente usados; cada linha declara representação, função, formato e recorte. Listagens e buscas não equivalem a leitura integral.

| Caminho | Relação | Representação / função / formato | Recorte examinado |
|---|---|---|---|
| `AGENTS.md` | context | prose / prompt-instruction / Markdown | integral |
| `src/backend/AGENTS.md` | context | prose / prompt-instruction / Markdown | integral |
| `src/frontend/AGENTS.md` | context | prose / prompt-instruction / Markdown | integral |
| `.agents/skills/decision-analysis-v4/SKILL.md` | context | prose / prompt-instruction / Markdown | integral |
| `.agents/skills/decision-analysis-v4/references/classification-taxonomy.md` | context | prose / prompt-instruction / Markdown | integral |
| `.agents/skills/decision-analysis-v4/references/output-schema.md` | context | prose / prompt-instruction / Markdown | integral |
| `.agents/skills/decision-analysis-v4/references/output-routing.md` | context | prose / prompt-instruction / Markdown | integral |
| `.agents/skills/decision-analysis-v4/references/artifact-classification.md` | context | prose / prompt-instruction / Markdown | integral |
| `docs/configuracao-ambiente.md` | supporting | prose / documentation / Markdown | integral; ambientes e execução local |
| `docs/requisitos_funcionais.md` | supporting | prose / documentation / Markdown | RF10–RF12 e pendências; busca por vagas |
| `docs/requisitos_nao_funcionais.md` | supporting | prose / documentation / Markdown | integral |
| `docs/contrato-busca-vagas.md` | supporting | prose / schema-contract / Markdown | integral |
| `docs/contratos_integracao_grupo2.md` | supporting | prose / schema-contract / Markdown | integral |
| `docs/matriz_rastreabilidade.md` | supporting | prose / documentation / Markdown | linhas de RF10, RF11 e referências a vagas |
| `docs/matriz_testes.md` | supporting | prose / documentation / Markdown | CT-RF10-01–04 e CT-RF11-01–04 |
| `docs/casos-de-uso-v2.md` | context | prose / documentation / Markdown | atores, UC09 e módulo Grupo 2 |
| `docs/mapeamento_jornadas.md` | context | prose / documentation / Markdown | seções 1–4: exclusão do Grupo 2 do recorte dos wireframes |
| `docs/wireframes/README.md` | context | prose / documentation / Markdown | busca por vagas e exclusão do Grupo 2 |
| `docs/dossie-aceite.md` | supporting | prose / documentation / Markdown | linhas de API de vagas e jornada simulada |
| `docs/testes/evidencias/f11-vagas-responsividade-movel.md` | context | prose / documentation / Markdown | recortes devolvidos por busca: natureza estática, baseline, limites e comandos |
| `prompts/README.md` | context | prose / prompt-instruction / Markdown | integral |
| `prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md` | supporting | prose / documentation / Markdown | escopo, fatos, hipóteses e limitações do double |
| `prompts/backend/20261009-110249-contrato-adaptador-busca-vagas-v002.md` | supporting | prose / documentation / Markdown | baseline temporária, semântica dos filtros e decisão |
| `prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md` | supporting | prose / documentation / Markdown | problema, fatos e escopo, aproximadamente linhas 145–195 |
| `prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md` | supporting | prose / documentation / Markdown | problema, fatos, escopo e critérios, linhas 145–190 |
| `prompts/frontend/20261019-073800-vagas-leitor-tela-teclado-v001.md` | context | prose / documentation / Markdown | hipóteses, escopo e afirmações sobre ARIA/userEvent |
| `prompts/frontend/20261021-205543-validacao-vagas-largura-movel-f11-v002.md` | context | prose / documentation / Markdown | ocorrências de vagas, vazio, timeout e fallback; não adotada como especificação funcional |
| `prompts/frontend/20261007-081300-cenario-e2e-preenchimento-curriculo-v001.md` | context | prose / documentation / Markdown | ocorrências de E2E e proposta de harness; somente classificação histórica |
| `src/backend/api/vagas.py` | primary | source-code / production / Python | integral |
| `src/backend/application/consulta_vagas.py` | primary | source-code / production / Python | integral |
| `src/backend/application/ports.py` | supporting | source-code / schema-contract / Python | `VagaExternaDto` e `BuscadorVagas`, linhas 827–868 |
| `src/backend/infrastructure/integrations/cliente_vagas_grupo2.py` | primary | source-code / production / Python | integral, incluindo ordem dos `except` |
| `src/backend/api/factory.py` | supporting | source-code / production / Python | imports de vagas, assinatura de `create_app`, middleware e registro do router |
| `src/backend/main.py` | supporting | source-code / production / Python | integral |
| `src/backend/api/middleware_autenticacao.py` | supporting | source-code / production / Python | integral |
| `src/backend/infrastructure/security/autenticador_sessao_indisponivel.py` | supporting | source-code / production / Python | integral |
| `src/backend/tests/test_api_vagas.py` | supporting | source-code / test / Python | integral |
| `src/backend/tests/test_consulta_vagas_use_case.py` | supporting | source-code / test / Python | integral |
| `src/backend/tests/test_cliente_vagas_grupo2_http.py` | supporting | source-code / test / Python | métodos inventariados, timeout, schema e resposta malformada |
| `src/backend/tests/test_application_vagas_port.py` | supporting | source-code / test / Python | inventário dos três métodos e contrato observado |
| `src/backend/tests/test_double_api_vagas_grupo2.py` | supporting | source-code / test / Python | inventário dos nove métodos |
| `src/backend/tests/doubles/api_vagas_grupo2.py` | supporting | source-code / data-fixture / Python | integral |
| `src/backend/tests/fixtures/credenciais_sessao.py` | supporting | source-code / test / Python | imports, disponibilidade, banco, revisões, `RespostaCredenciais`, `solicitar_asgi` |
| `src/backend/tests/fixtures/curriculos_autenticados_integracao.py` | context | source-code / test / Python | imports, disponibilidade, revisões, inventário de classes e `requisitar` |
| `src/backend/tests/fixtures/perfis_integracao.py` | context | source-code / data-fixture / Python | nomes de classes e funções; não adotadas suas regras |
| `src/backend/tests/fixtures/massa_teste_curriculos.py` | context | source-code / data-fixture / Python | nomes de classes e funções |
| `src/backend/tests/fixtures/curriculo_exportacao.py` | context | source-code / data-fixture / Python | nomes de classe e fábrica |
| `src/backend/tests/test_integracao_rejeicao_requisicoes_sem_credenciais_validas.py` | context | source-code / test / Python | ASGI e skips; nenhuma regra de currículo transferida a vagas |
| `src/backend/tests/test_integracao_composicao_credenciais_sessao.py` | context | source-code / test / Python | motivo do skip C02 |
| `src/backend/infrastructure/persistence/alembic/versions/*.py` | context | source-code / schema-contract / Python | somente atribuições `revision`/`down_revision` retornadas por busca, não DDL |
| `src/frontend/app/App.tsx` | supporting | source-code / production / TSX | integral |
| `src/frontend/pages/vagas/ui/PaginaVagasGrupo2.tsx` | primary | source-code / production / TSX | integral |
| `src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.tsx` | primary | source-code / production / TSX | integral |
| `src/frontend/features/listar-vagas/api/cliente-vagas-grupo2.ts` | primary | source-code / schema-contract / TypeScript | integral |
| `src/frontend/features/listar-vagas/model/mensagem-erro-vagas.ts` | supporting | source-code / production / TypeScript | integral |
| `src/frontend/features/listar-vagas/index.ts` | supporting | source-code / production / TypeScript | integral, API pública |
| `src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.test.tsx` | supporting | source-code / test / TSX | fixture, resultados, vazio, erro e recuperação |
| `src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.a11y.test.tsx` | supporting | source-code / test / TSX | nomes dos sete testes; loading/vazio; não prova leitor de tela real |
| `src/frontend/features/listar-vagas/api/cliente-vagas-grupo2.test.ts` | supporting | source-code / test / TypeScript | integral |
| `src/frontend/features/listar-vagas/model/mensagem-erro-vagas.test.ts` | supporting | source-code / test / TypeScript | nomes dos cinco testes e mensagens |
| `src/frontend/app/test/vagas-responsividade-css.test.ts` | context | source-code / test / TypeScript | início: CSSOM, leitura estática, fixture e alvos; inventário/baseline |
| `src/frontend/app/test/setup.ts` | supporting | source-code / configuration / TypeScript | integral, import de jest-dom |
| `src/frontend/app/jornada-curriculo.e2e.test.tsx` | context | source-code / test / TSX | imports, harness e nomes/linhas dos quatro testes |
| `src/frontend/app/jornada-selecao-previa-exportacao.e2e.test.tsx` | context | source-code / test / TSX | imports, harness, doubles e nomes/linhas dos dois testes |
| `src/frontend/features/acesso-estudante/api/cliente-acesso-estudante.ts` | context | source-code / production / TypeScript | fábrica, URL e `fetch`; não reutilizado como cliente de vagas |
| `src/frontend/package.json` | supporting | structured-data / build / JSON | integral |
| `src/frontend/package-lock.json` | supporting | structured-data / build / JSON | busca por browser e recorte dos peers opcionais do Vitest |
| `src/frontend/vite.config.ts` | supporting | source-code / configuration / TypeScript | integral |
| `src/frontend/tsconfig.app.json` | supporting | structured-data / configuration / JSONC | integral |
| `src/frontend/tsconfig.node.json` | supporting | structured-data / configuration / JSONC | integral |
| `src/frontend/eslint.config.js` | supporting | source-code / configuration / JavaScript | integral |
| `src/frontend/.gitignore` | context | prose / configuration / gitignore | integral |
| `flake.nix` | supporting | source-code / build / Nix | integral |
| `flake.lock` | supporting | structured-data / build / JSON | integral |
| `nix/backend-python-packages.nix` | supporting | source-code / build / Nix | integral |
| `nix/backend.nix` | supporting | source-code / build / Nix | integral |
| `nix/frontend.nix` | supporting | source-code / build / Nix | integral |
| `nix/tests.nix` | supporting | source-code / build / Nix | integral |
| `nix/quality.nix` | supporting | source-code / build / Nix | integral |
| `.github/workflows/ci.yml` | supporting | structured-data / configuration / YAML | integral |

O inventário de skills e seus recortes individuais está em “Divisão de trabalho”. Esses arquivos também são artefatos `context`, `prose / prompt-instruction / Markdown`, working tree no mesmo HEAD. O histórico Git é evidência `commit`, examinada por mensagem, pais, stat e histórico de caminhos, conforme tabela própria. A biblioteca padrão consultada está em `/nix/store/ji63yqcldc0z05zywlw1l6p8xgm2hhvh-python3-3.14.7-env/lib/python3.14/urllib/error.py`: introspecção de caminho e MRO, não leitura integral; relação supporting, source-code / production / Python, conteúdo externo ao repositório.

### Limites da evidência dos artefatos

`find . -name AGENTS.md -o -name AGENTS.override.md` encontrou somente raiz, backend e frontend. Nenhuma instrução local em `docs`, `nix`, `.agents` ou `prompts` foi encontrada. `rg --files` não encontrou pasta raiz `tests` (erro explícito “No such file or directory”). Não se pressupôs fixture central frontend: as massas estão locais nos testes consultados. Não se inspecionou servidor real do Grupo 2. Não foram abertos links externos contidos nos documentos. Ausência de ferramenta declarada não prova ausência global na máquina; ferramentas globais são proibidas pelo projeto de qualquer forma.

## Problema enriquecido

### Resultado desejado

Especificar uma entrega executável e determinística que cubra **resultado, vazio e indisponibilidade**, com fluxo positivo, negativos, controles positivos e sensibilidade dos oráculos. Distinguir a prova possível hoje da jornada frontend–backend que ainda exige produto composto. Ator principal: estudante que pesquisa/refina/reexecuta a busca. QA precisa detectar regressão sem depender do parceiro; engenharia precisa de oráculos que não escondam falhas de composição.

### (a) Fatos encontrados — com caminho e trecho

#### F1. Histórico local e identificação dos trabalhos

Comandos: `git log --all --oneline --regexp-ignore-case --grep='vagas\|busca.*vaga\|grupo.*2'`; histórico dos caminhos de `api/vagas.py`, adapter, feature e página; `git show --stat 531c77e`, `git show --stat 737fef5`; metadados dos merges. Nenhuma ligação é inferida só pelo número entre parênteses.

| Evidência Git | Trabalho identificado | Como a ligação foi estabelecida |
|---|---|---|
| `a86fc37`, “docs: adiciona requisitos de busca de vagas” | requisitos | mensagem; não se deduziu PR/card |
| `e711a98`, “Merge pull request #163 … task-151”; filho `d43e933`, “preparar double … (#151)” | double | merge, branch e arquivo no histórico; PR 163, referência de trabalho 151 |
| `e995f8f`, “Merge pull request #450 … feature/tela-vagas-grupo2”; `6bcfded` e correções até `6a38f80` | tela/cliente/página | nome da branch, mensagem e histórico dos arquivos |
| `4d082ea` / `0a3d570`, “docs/contratos-integracao-grupo2” | proposta de contrato entre equipes | mensagem do merge e do commit, sem equiparar a produção |
| `0ade208`, “Merge pull request #452 … feature/124-contrato-busca-vagas”; `b0e6971` | porta interna | merge relaciona branch 124 a PR 452; histórico de vagas |
| `f627617`, “Merge pull request #483 … feature/126-consulta-vagas-api-externa”; filho `737fef5` | caso de uso e adapter HTTP | pais do merge, branch e stat do filho |
| `5bfdac8`, PR 489, `feat/issues-281-236-vagas-acessiveis`; `081e5f4` | estados acessíveis | branch e histórico da feature |
| `39dd620`, PR 501, `feat/issue-288-erro-recuperavel-vagas`; `0472c1b` | erro recuperável | merge e histórico do arquivo |
| `324989d`, PR 546, `feature/128-expor-busca-vagas`; filho `531c77e` | endpoint de busca | merge e stat; sufixo `(#128)` é referência do trabalho, não prova de PR 128 |
| `2fb44e7`, PR 557, `feat/issue-407-vagas-leitor-tela-teclado`; `8e198e5` | testes semânticos/teclado | mensagem e histórico |
| `97062b5`, PR 571, `test/validacao-largura-mobile`; `38180f5` | caracterização CSS móvel | mensagem, arquivo e evidência versionada |

`git log --all --grep='374'` não retornou resultados. `docs/matriz_rastreabilidade.md:53` menciona “#374 – cenário E2E”; isso não comprova descrição de card, PR ou teste implementado. Nenhum cenário atual específico de vagas com nome E2E foi localizado no inventário.

#### F2. Registro das buscas documentais

Busca exploratória: `rg -n -i 'vaga|RNF0|disponibilidade|tempo de resposta|usabilidade|ponta.a.ponta|e2e' docs`; busca em `prompts/backend/*vagas*` e `prompts/frontend/*vagas*` por `vaga|busca|indisponibilidade|timeout|vazio|fallback|estado de erro`. Os retornos relevantes foram os contratos, RF/RNF, matrizes, dossiê, análises de double/porta/adapter/API, ARIA e CSS identificados acima. A saída ampla foi parcialmente truncada; por isso não se afirma exaustividade linha a linha. Foi feita uma busca controlada e completa no conjunto abaixo para registrar inclusive vazios.

Conjunto D: `docs/contrato-busca-vagas.md`, `docs/contratos_integracao_grupo2.md`, `docs/requisitos_funcionais.md`, `docs/requisitos_nao_funcionais.md`, `docs/matriz_testes.md`, `docs/matriz_rastreabilidade.md`. Comando por termo: `rg -l -i "$termo" <os seis caminhos D>`.

| Termo literal | Arquivos D retornados |
|---|---|
| `vaga` | todos os seis |
| `busca` | todos os seis |
| `indisponibilidade` | matriz de testes, RNF, contrato de busca |
| `timeout` | proposta de contratos Grupo 2; os demais usam outros termos ou não contêm essa grafia |
| `vazio` | matrizes de rastreabilidade e de testes; singular literal não cobre “vazia” |
| `fallback` | **nenhum** |
| `estado de erro` | matriz de rastreabilidade |

Busca ampla de `fallback` em docs/prompts encontrou referência ao fallback de CSSOM e análises de outros recursos; **não encontrou política de fallback funcional de busca de vagas**. Não se transpôs comportamento desses outros recursos. `rg -n 'E2E|ponta a ponta|aceite' .agents/skills/decision-analysis-v4/references/*.md` não retornou definição de nível de teste. A definição veio da skill de testes. Busca de interface em `docs/wireframes/README.md` retornou: “Não fazem parte deste recorte … integração com o Grupo 2”; `docs/mapeamento_jornadas.md`, seção 4: “UC09 … não integra a jornada guiada do aluno”. Não foi localizado wireframe de vagas no inventário `docs/wireframes/*`.

#### F3. O que E2E significa e o que os nomes atuais realmente testam

`.agents/skills/integration-system-testing-v1/references/test-scope-boundary.md`, `system-acceptance-e2e`: **“Exercita um componente implantável completo, uma API pela interface real, uma jornada de usuário ou um critério de aceitação através das camadas relevantes.”** A mesma fonte distingue: **“Exercitar jornada pelo navegador é E2E; testar isoladamente um componente visual é unitário”**. É uma categoria ampla que admite sistema pela API, mas não torna teste DOM sinônimo de navegador.

`src/frontend/vite.config.ts`: `environment: "jsdom"`, `setupFiles: "./app/test/setup.ts"`; não há modo browser configurado. O setup importa `@testing-library/jest-dom/vitest`. Nos dois arquivos `app/*.e2e.test.tsx`, `render`, `userEvent` e `vi` trabalham sobre React realmente renderizado em DOM simulado. `JornadaCurriculoHarness` encadeia páginas localmente; `JornadaCompletaHarness` simula seleção, prévia e exportador `Blob`. Não há API backend real, navegador real nem navegação produtiva completa. O comentário “no navegador” no primeiro harness exagera a prova; a configuração e imports executados são mais confiáveis para classificar o nível. `docs/dossie-aceite.md` chama a jornada de **“harness local”** e exclui a jornada integrada real.

`src/frontend/package.json` declara React 19.3.0, React DOM, Zod 4.1.5; dev: Testing Library, jsdom 30.1.0, Vite 8.3.0, Vitest 5.0.1, TypeScript 7.0.2, ESLint e Prettier. Não declara Playwright/Cypress/browser runner. O lock **contém** os nomes `@vitest/browser-playwright`, `browser-preview` e `browser-webdriverio`, mas no bloco `peerDependencies` com `optional: true` do Vitest (linhas 6357 em diante). A busca por entradas `node_modules/(@playwright|playwright|cypress|@vitest/browser)` não retornou pacote instalado no lock. Não confundir referência de peer com dependência resolvida. Nix não declara navegador em nenhum dos quatro ambientes.

#### F4. Resultado: contratos e cadeia de dados

`docs/requisitos_funcionais.md`, RF10: **“consultar uma ferramenta de busca de vagas por meio de API e processar a lista … em JSON”**; RF11: apresentar em página web. São requisitos, não prova de ligação existente.

`src/backend/api/vagas.py`: `GET /vagas`, resposta 200 `ResultadoBuscaVagasResposta(termo, filtros, total=len(...), vagas=...)`. Query: `termo: str = ""`, `localizacao: str | None = None`, `modalidade: str | None = None`. Não há enum, tamanho mínimo/máximo, paginação ou proibição de termo vazio; “REMOTO/HIBRIDO/PRESENCIAL” aparece como exemplo, não enum validado. Filtros são incluídos se não forem `None`; string vazia é encaminhada. Não há regra implementada que justifique um negativo “modalidade inválida” ou “termo numérico”: query HTTP é textual. Parâmetros desconhecidos não são lidos pelo handler. Não foi encontrado exemplo alcançável de 422 por esses três parâmetros textuais.

`ConsultarVagas.executar`, em `application/consulta_vagas.py`: `return await self._buscador_vagas.buscar_vagas(termo=entrada.termo, filtros=entrada.filtros if entrada.filtros else None)`. Não normaliza termo apesar da docstring genérica falar em normalização. `application/ports.py` define DTO imutável de oito campos, com opcionais anotados como `str`. A API permite `None` em localização/modalidade/URL; isso é uma diferença de representação, e o adapter converte ausentes/nulos para `""`.

`ClienteApiVagasGrupo2Http`: transporte padrão `urllib.request.urlopen`, via `asyncio.to_thread`; URL default **exemplificativa** `https://grupo2.exemplo.com/api/vagas`, timeout default `5.0`. O construtor aceita `executor_http(url, timeout) -> bytes`. Ao montar URL, faz `termo.strip()` e `urllib.parse.urlencode`; filtros não nulos são convertidos em texto. Aceita lista raiz, `{vagas: [...]}` ou `{associacoes: [...]}`; item pode estar sob `vaga`. Exige id/título/empresa não vazios e descrição string (inclusive vazia); requisitos ausentes/nulos ou de tipo não lista viram tupla vazia, itens não nulos viram strings. Não valida sintaxe da URL de candidatura. Esses comportamentos são implementados, não confirmação do fornecedor.

No frontend, `cliente-vagas-grupo2.ts` recebe **função injetável**, não URL nem `Response` HTTP. Schema: `{associacoes: [{curriculo_id, vaga}]}`, strings essenciais com `.trim().min(1)`, requisitos lista obrigatória, localização/modalidade nullable e URL válida ou null. `CriteriosPesquisaVagas` tem só `termo`. Não existe conversão implementada de `{vagas,total}` do backend para esse contrato nem classificação por status HTTP 401/502/503/504. A busca global por `fetch(` e `VITE_API_URL` encontrou o cliente de acesso em `features/acesso-estudante/api/cliente-acesso-estudante.ts`; **não** um cliente HTTP compartilhado/de vagas. O caminho presumível `shared/api/cliente-http.ts` foi verificado e não existe. O cliente de acesso não sustenta regras para vagas.

`TelaVagasGrupo2.tsx`: mount faz `pesquisar({termo: ""})`; submit usa `{termo: termo.trim()}`; renderiza cards com título, empresa, descrição, requisitos e, se não nulos, metadados/link. URL abre outra aba. Não seguir esse link nos testes. A fonte de sugestões da tela é o cliente injetado; ainda não a rota `/vagas` da API.

#### F5. Vazio: sucesso válido, inclusive na pesquisa inicial

`docs/contrato-busca-vagas.md`: **“Uma busca sem resultados também retorna 200, com total: 0 e vagas: [], preservando termo e filtros”**. API implementa isso. `docs/contratos_integracao_grupo2.md`, seção 4: `associacoes` pode estar vazia, mas o documento inteiro tem status **“proposta para validação entre as equipes”**.

UI: retorno `sugestoes.length === 0` produz estado `vazio`; `<section role="status" aria-labelledby="titulo-vagas-vazias">`, heading **“Nenhuma vaga encontrada”**, texto **“Não encontramos vagas sugeridas”**, complemento `para “<termo>”`, orientação para ajustar palavra-chave. O input permanece. Não há estado ocioso vazio antes de buscar: o inicial é `carregando`, seguido de busca automática com termo vazio. Um vazio após mount é resposta dessa busca, não “ainda não pesquisou”.

`docs/matriz_testes.md` chama CT-RF10-02 e CT-RF11-03 de **Negativo**, mas exige processar sem erro e informar ausência. É classificação do caso, não status de erro. O cenário novo deve manter ambos: desfecho de sucesso e contraste negativo contra resultado/erro, sem inventar 404 ou 204.

#### F6. Indisponibilidade: documentação versus implementação

| Origem da falha | Documento | Implementação / sinal observado por inspeção | UI atual |
|---|---|---|---|
| `TimeoutIntegracaoVagas` | contrato de busca: 504 | handler captura primeiro e lança 504 com detalhe controlado | sem ligação de status; cliente reconhece código tipado ou regex na mensagem de erro |
| `RespostaInvalidaVagas` / `ErroIntegracaoVagas` | contrato: 502 | handler lança 502; JSON/schema inválido no adapter gera a primeira | `FalhaVagasGrupo2("resposta-invalida")` tem mensagem própria, mas não nasce de leitura automática desse HTTP |
| executor ausente | contrato: 503 | handler verifica `consultar_vagas is None` antes de identidade e lança 503, “Consulta de vagas indisponível.” | cliente padrão já falha com `indisponivel`; não é interpretação de 503 |
| falha de rede `URLError` sem timeout | análise histórica da API fala em rede→502; adapter fala em conexão→timeout | adapter captura `URLError` e lança `TimeoutIntegracaoVagas` também sem timeout; cadeia resulta em **504** | função remota rejeitando `Error` genérico vira `indisponivel` |
| HTTP 4xx/5xx externo via `urllib.error.HTTPError` | docstring/análise histórica do adapter sugere 5xx→resposta inválida→502 | MRO lida no Python Nix: `HTTPError, URLError, OSError...`; entra no primeiro `except`, portanto **504**, caracterização a validar no novo teste | não há mapeamento de status HTTP externo implementado na tela |
| exceção inesperada do executor HTTP | sem taxonomia externa confirmada | `except Exception` converte para `RespostaInvalidaVagas`→502 | rejeição genérica de função do cliente vira `indisponivel` |
| payload backend entregue diretamente ao cliente UI | contrato de busca explicita que não são intercambiáveis | Zod recusa ausência de `associacoes` | “Recebemos uma resposta inesperada ao consultar as vagas. Tente novamente mais tarde.” |

Detalhes backend: timeout **“Tempo limite esgotado ao consultar vagas externas. Tente novamente mais tarde.”**; 502 **“Não foi possível obter dados válidos do serviço de vagas no momento.”**. Não forçar 503 para toda falha do parceiro.

`obterMensagemErroVagas`: indisponível **“O serviço de vagas está temporariamente indisponível. Tente novamente mais tarde.”**; timeout **“O serviço de vagas demorou para responder. Verifique sua conexão e tente novamente.”**; erro desconhecido **“Não foi possível carregar as vagas no momento. Tente novamente mais tarde.”**. UI usa `<section role="alert">`, heading **“Não foi possível carregar as vagas”** e botão **“Tentar novamente”**. `termo` do formulário não é apagado. Retry usa `estado.criterios`, que podem diferir do input se a pessoa editar o campo após a falha e clicar retry; comportamento implementado, sem critério de produto encontrado para esse caso. Submit usa texto atual. Não se afirma cancelamento, timeout real no frontend ou prevenção de corrida: não há AbortController/timer no cliente lido; as buscas podem se sobrepor e `.then(setEstado)` pode aplicar resposta antiga.

`docs/requisitos_nao_funcionais.md`: RNF06 é **proposta derivada**, pede tratamento controlado e preservar informações dos currículos; RNF08 tem **metas mensuráveis a definir**. Disponibilidade, período de medição, dispositivos e metas de usabilidade também estão pendentes. Cinco segundos do adapter é configuração técnica, não SLA de jornada. Preservar input está implementado e é obrigação geral do AGENTS frontend (“preservando dados locais sempre que possível”); não comprova preservação de todo currículo persistido.

#### F7. Composição e precedência

`factory.py` aceita `consultar_vagas: ConsultaVagasExecutor | None = None` e inclui router. Instala middleware de sessão apenas se `autenticador_sessao` for fornecido. `main.py` cria app com `AutenticadorSessaoIndisponivel()` e readiness; não fornece `consultar_vagas`. O autenticador concreto indisponível sempre retorna `None`. Logo o `main.app` recusa busca privada em **401** antes de chegar ao handler 503. Não há caminho positivo de busca na composição produtiva examinada.

Com middleware ativo: cookie ausente→401, cookie não reconhecido→401 **“Sessão ausente ou inválida.”**, antes de validação/handler/provedor. Para sessão aceita, FastAPI resolve parâmetros, então handler verifica executor (503), depois UUID em `request.state.usuario_id` (401 **“Autenticação necessária.”**), constrói entrada, chama use case/adapter. Timeout é capturado antes da base `ErroIntegracaoVagas`. Sem middleware e executor ausente, 503 vence ausência de identidade; com executor e identidade ausente/não UUID, 401 vence provedor. São configurações distintas, que devem ter testes e oráculos separados. Não injetar UUID direto no teste principal que pretende provar middleware.

`App.tsx` tem `type RotaAtiva = "inicio" | "acesso"`; não importa página de vagas. `PaginaVagasGrupo2` existe e permite injetar cliente, mas seu default é `criarClienteVagasGrupo2Indisponivel()`. É possível montá-la diretamente em teste sem mudar App; isso não prova acesso por URL/menu da aplicação. Mesmo com browser novo, o App e o main atuais não viabilizam o caminho feliz integrado. Um adapter escrito só no teste para converter contratos esconderia uma ligação ausente do produto.

#### F8. Harnesses, fixtures e cobertura existentes

| Base real | O que existe / o que cobre | Reuso recomendado e limite |
|---|---|---|
| `backend/tests/fixtures/credenciais_sessao.py` | `BancoCredenciaisSessao`, `ObservadorPerfil`, `RespostaCredenciais`, `solicitar_asgi`, tokens e relógio fixos, checagem de revisões; ASGI sem sockets | reutilizar `solicitar_asgi`/resposta, sem criar banco; aceita app/método/path/query/token, coleta status/corpo completo com limite 10s |
| `backend/tests/fixtures/curriculos_autenticados_integracao.py` | `BancoCurriculosAutenticadosIntegracao`, `ConsultasItensDouble`, `GeradorCurriculoDeterministico`, `RotaCurriculo`, `rotas_curriculo`, `requisitar`; SQLite migrado | não usar banco/rotas de currículo para vagas; harness de requisição exige banco/rota, menos apropriado |
| `backend/tests/fixtures/perfis_integracao.py` | `PerfilIntegracaoFake`, `popular_perfis_fake`, `ler_perfis_fake` e fábricas sintéticas | inventariado, não necessário à busca |
| `backend/tests/fixtures/massa_teste_curriculos.py` | `CurriculoMassaTeste`, `obter_curriculos_massa_teste` e builders | não necessário à busca |
| `backend/tests/fixtures/curriculo_exportacao.py` | `CurriculoExportacaoFixture`, `obter_curriculo_exportacao_fixture` | não necessário à busca |
| `backend/tests/doubles/api_vagas_grupo2.py` | 4 modos, `configurar_modo`, `definir_vagas`, `obter_chamadas`, `limpar_chamadas`, JSON; 3 vagas padrão | sucesso/vazio e spy reutilizáveis; filtros só registrados, não aplicados; não comprova filtragem do parceiro |
| `backend/tests/test_api_vagas.py` | 8 testes: resultado/vazio, 504/502/base, 503, 401 e OpenAPI; chama `rota.endpoint` diretamente, stub de executor | não prova status no transporte/validação FastAPI/middleware/use case/adapter integrados; novo teste deve atravessá-los |
| `test_consulta_vagas_use_case.py` | 5 testes, double e exceções; retorno/vazio/preservação/propagação | unidade, não HTTP |
| `test_cliente_vagas_grupo2_http.py` | 10 testes: 5 mapper, 5 assíncronos; formatos, timeout, JSON/schema | adapter com executor fake, sem API/UI; não há teste inventariado de HTTPError 500 |
| `test_application_vagas_port.py` | 3 testes DTO/imutabilidade/assinatura | contrato interno estrutural |
| `test_double_api_vagas_grupo2.py` | 9 testes dos modos, alternância, spy, JSON e massa customizada | prova do double, não da cadeia produtiva |
| `TelaVagasGrupo2.test.tsx` | 7 testes, fixture local `sugestao` e `criarCliente`; UI com `listarSugestoes` mockado, resultado/vazio/falha/retry e decisões | novo teste deve usar cliente real com schema para acrescentar integração; não repetir decisões de associação |
| `TelaVagasGrupo2.a11y.test.tsx` | 7 testes, mock local, Tab, nomes, status, alert e decisões | sem navegador/leitor real; usar labels como seletores, sem declarar conformidade completa |
| `cliente-vagas-grupo2.test.ts` | 5 testes, `respostaValida` local e `vi.fn`: adaptação, rejeição, termo, rede e timeout | não testa página junto com adaptação |
| `mensagem-erro-vagas.test.ts` | 5 testes das mensagens | função pura |
| `app/test/vagas-responsividade-css.test.ts` | fixture CSS e controles CSSOM estáticos | não harness funcional nem layout real; não reutilizar breakpoint como regra de busca |
| `app/*.e2e.test.tsx` | dois harnesses locais de currículo, seis testes | inventariados para classificar ferramenta; não importar seus fluxos/dados/regras em vagas |

O double antigo define **outro** `VagaExternaDto` e exceções `ApiVagasIndisponivel`/`RespostaInvalidaApiVagas` que **não** herdam das exceções de `application/consulta_vagas.py`. Injetá-lo em modo de falha não aciona automaticamente 504/502 no router. Para cadeia completa, preferir o adapter real com executor HTTP fake; não “corrigir” o double compartilhado fora do escopo. Para uso apenas de sucesso do double, não alegar teste do mapper real.

### (b) Lacunas — opções, recomendação e decisão necessária

| Lacuna (nenhum artefato fecha o ponto) | Opções viáveis | Recomendação e responsável | Informação exata para fechar |
|---|---|---|---|
| Aceite do card: só título | API; UI; conjunto separado; jornada browser | conjunto separado agora, engenharia; **produto** precisa aceitar limite do card | confirmar se aceite exige navegador e ligação produtiva, ou aceita prova de sistema API + integração UI explicitamente separadas |
| Contrato externo confirmado | manter proposta; homologar com parceiro | manter sintético; produto/integração entre equipes | endpoint/método, auth, schema definitivo, parâmetros, códigos, timeout, paginação, ordenação e versão aprovados |
| Ponte frontend–backend inexistente | adapter produtivo futuro; simulação apenas de cada fronteira | não inventar ponte no teste; engenharia/produto | contrato consumidor aprovado, composição e navegação de vagas implementadas em tarefa separada |
| Estado vazio anterior a buscar | inicial ocioso; loading + busca automática atual | caracterizar atual; alteração depende de **design/produto** | aprovar se busca automática continua e qual texto/ação inicial desejado |
| 422 anunciado sem entrada textual inválida conhecida | inventar restrição; testar aceitações atuais; aguardar regra | não criar negativo artificial; engenharia caracteriza termo vazio e modalidade livre | produto deve definir restrições (enum/tamanho/obrigatoriedade), depois API implementá-las; até lá sem cenário 422 exigível |
| 5xx/rede→504 diverge da intenção documental | caracterizar; aguardar correção | caracterizar **504 atual**, rotulado como achado, engenharia; sem corrigir | decidir contrato desejado, abrir correção separada e atualizar expectativa quando implementada |
| Retry após editar input durante erro / concorrência | retry dos critérios falhos; retry do input atual; bloquear/cancelar | testar recuperação com critérios sem edição intermediária; **design** para novos casos | semântica aprovada para edição/retry e busca concorrente; não transformá-la em critério nesta entrega |
| SLA, disponibilidade, usabilidade e matriz browser | testes funcionais; exploração sem limiar; aceite quantitativo futuro | funcional apenas, engenharia; limiares de produto/operação e matriz de design | p95/p99, carga/volume, meta/período de disponibilidade, dispositivos, browsers, padrão de acessibilidade e método de usabilidade |
| Navegador e runtime frontend em `tests` | shell composto existente; mudança temporária; ambiente permanente posterior | compor shells para DOM; browser como pré-requisito separado | se browser for obrigatório: pacote/versão de runner, browser e bibliotecas Nix, comando e bloqueio de egress aprovados |
| Permissão de portas locais/rede no executor futuro | ASGI sem sockets; loopback com preflight/skip | zero sockets agora; engenharia | runner de browser só poderá comprovar rede local se porta e navegador realmente iniciarem; não houve probe de sockets nesta análise |
| Nomenclatura E2E ampla da skill versus expectativa comum | chamar tudo E2E; nomear nível exato | `sistema-api` e `integracao` sem sufixo e2e; engenharia | aprovação do enquadramento do card ou ampliação futura para browser integrado |
| Cobertura persistente completa de sessão | auth fake; banco migrado | auth fake no teste de busca, engenharia | se exigir login/sessão reais: composição própria e migrations íntegras; não é condição da busca com porta de identidade substituída |
| Processo para experimento temporário multitecnologia | skill de testes com limites; tarefa direta delimitada; handoffs Nix separados | testes pela skill elegível; experimento por tarefa direta com exceções explícitas já descritas pelo usuário | na execução: invocar versão exata; confirmar apenas o que exceder a autorização persistente, sem pedir novamente autorização já dada |

### Hipóteses

H1: compor shells `tests` + `frontend` fornece Node/npm declarados e mantém ambiente obrigatório para integração DOM, sem instalação. Não foi executado esse comando composto nesta análise; validar antes de alegar execução da nova suíte. H2: `solicitar_asgi` pode ser reutilizado sem instanciar seu banco; assinatura e imports sustentam isso, mas integração nova ainda não foi escrita. H3: controles de sensibilidade reduzirão falsos positivos; são requisito do usuário, não resultado demonstrado aqui.

### Perguntas em aberto

As entradas mínimas são a última coluna das lacunas. Nenhuma impede especificar a caracterização proposta. A aprovação de conclusão do card como E2E integrado **continua em aberto**. Não se fabrica critério de aceite para fechá-la.

### Escopo / Fora do escopo

Somente especificação de arquivos de teste, fixtures, oráculos, execução, limites e evidência futura. Esta análise escreveu apenas este Markdown. Fora: produto, contratos, composição, CI, correções dos achados, serviço real, dependências/ambientes permanentes e outros recursos. Baselines foram informativos. Nenhuma migration ou definição de ambiente foi editada, nem pacote/browser instalado.

### Critérios de sucesso e origem

Definido pelo **usuário**: três desfechos e positivos/negativos, controles positivos, sensibilidade, spy, isolamento, honestidade e ausência de implementação agora. Os critérios específicos de execução abaixo são **inferidos** para satisfazer o título a partir dos artefatos; não são critérios de aceite inventados do card. Em cada cenário, `D` significa comportamento definido documentalmente, `I` inferência de critério de teste, `C` caracterização de implementação atual. Uma mesma linha pode ter suporte D e construção I.

## Restrições aplicáveis

Nix obrigatório (raiz); Git fora do Nix; componentes unitários nos próprios shells, integração e superiores em `tests`; documentação de toda função/classe com responsabilidade, abordagem e finalidade. Backend preserva Clean Architecture/DDD; frontend preserva FSD e APIs públicas. Nenhuma skill de implementação foi invocada agora. `decision-analysis-v4` permite somente um novo Markdown. Artefatos de execução ignorados não entram no commit.

## Classificação comentada

`engineering`, escolha do nível de teste e método de prova; `integration`, `reliability`, `user-experience`. Escopo de sistema por cruzar contratos e estados, sem exigir mudança funcional. Risco baixo e reversível por ser especificação/testes locais. Incerteza média: o comportamento atual é legível, mas aceite de E2E e contrato externo ainda não foram confirmados.

## Decisão de roteamento

`find prompts -maxdepth 1 -type d` encontrou `backend`, `ambientes`, `frontend`, `templates`, `revisao`, `requisitos`. `prompts/README.md` organiza por tema; não há pasta de testes. Escolhida `frontend` por foco em jornada/estados e precedente da análise de jornada. `backend` seria defensável pela prova API; confiança média porque a demanda cruza ambos. `requisitos` não prevalece porque esta é seleção técnica baseada no comportamento existente; `ambientes` não é objetivo; `revisao` não corresponde ao modo inicial; `templates` não é template. Nenhuma pasta foi criada.

## Dimensões de decisão

| Dimensão | Prioridade | Direção / limiar | Motivo |
|---|---|---|---|
| correctness | alta | não esconder fronteiras ausentes | evitar falsa prova E2E |
| reliability | alta | três desfechos determinísticos sem egress | isolar indisponibilidade real do parceiro |
| user-value | alta | verificar estados e recuperação observáveis | API sozinha não prova mensagem da tela |
| simplicity | média | ferramentas existentes, sem produto novo | reduzir pré-requisitos e duplicação |
| optionality | média | ampliar para browser quando houver composição | preservar caminho futuro |

## Alternativas consideradas

| Alternativa | Prova | Não prova | Ambiente e viabilidade |
|---|---|---|---|
| Estado atual: só suítes existentes | unidades de API/use case/adapter e UI mockada | colaboração de todas as camadas, sensibilidade conjunta | executável com skips/falhas preexistentes; insuficiente como novo cenário |
| A — sistema pela API com provedor simulado | middleware, routing/serialização FastAPI, use case, adapter e parâmetros até executor fake | página, navegador, parceiro ou main produtivo | `tests`, Python stdlib; sem banco nem porta; viável |
| B — página + cliente real com função remota simulada | React/DOM, formulário, validação Zod, mensagens, transições/retry | backend, cookies/CORS/rede HTTP, layout e browser | Vitest/jsdom, shells `tests` + `frontend`; viável com composição de shells a validar |
| C — navegador real contra backend de teste | se montado: DOM/browser e comunicação HTTP local até adapter fake | ainda não garante App/main produtivos se substituídos | falta runner/browser; contratos/composição não conectados; não executável com base atual sem pré-requisitos |
| D — A + B (recomendada) | soma explícita das duas provas em seus contratos atuais e contraste da incompatibilidade | **não** une magicamente os dois contratos | sem nova dependência; maior cobertura atual sem inventar comportamento |

Navegador com interceptação de API seria variante de B, não C: prova browser/UI, mas não backend. Harness browser com página diretamente montada pode ser exclusivamente de teste, porém deve ser chamado de página em browser, sem afirmar navegação do App. Converter `{vagas}` em `{associacoes}` em adapter exclusivo do teste não é alternativa legítima para provar integração produtiva; criaria a funcionalidade faltante.

## Perfil de pagamento comparativo

Escala ordinal, sem somatório. Confiança alta nas fronteiras lidas; média no ambiente composto ainda não executado.

| Dimensão | Prioridade | A API | B página | C browser + backend | D combinação | Confiança / base |
|---|---|---|---|---|---|---|
| correctness | alta | +1 | +1 | 0 enquanto ligação ausente | +2 pela declaração de limites | alta, contratos/código |
| reliability | alta | +2 | +2 | +1 com mais processos | +2 | alta, injeção existente |
| user-value | alta | 0 | +2 | +2 se viabilizada | +2 | alta, estados UI |
| simplicity | média | +2 | +1 | -2 | +1 | alta, Nix/manifests |
| optionality | média | +1 | +1 | +1 | +2 | média, futura composição |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### (c) Recomendações — decisão desta versão

**D: implementar futuramente testes de sistema pela API e integração de página/cliente, separados, cobrindo os três desfechos e suas contraprovas.** O backend deve usar adapter real e executor HTTP fake com registro de URL/timeout; a página deve usar `criarClienteVagasGrupo2` real, função remota fake e schema real. Não usar stub de use case no caminho feliz API nem stub de `listarSugestoes` no caminho principal da página, pois já existem esses testes isolados.

O rótulo **“E2E da busca de vagas integrada” seria exagero** nesta entrega. A categoria ampla `system-acceptance-e2e` da skill admite a prova API, mas o nome recomendado é **“Busca de vagas — sistema pela API e integração da página com transporte simulado”**. No PR/card, dizer que o E2E integrado continua bloqueado por rota/composição/contratos e browser; não declarar o card integralmente atendido sem aceite explícito dessa redução de alcance.

### Impacto da revisão

Inicial. Nenhuma análise antiga foi modificada. Esta recomendação não ratifica afirmações históricas de contrato externo confirmado ou de leitor de tela real.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho | Base |
|---|---|---|---|
| correctness | prioritized | oráculos sobre comportamento atual, sem ponte falsa | F4–F8 |
| reliability | prioritized | falhas reproduzíveis sem rede/espera | executor injetável e promises controladas |
| user-value | prioritized | mensagens e preservação de termo verificadas | UI real + cliente real |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar | Atendimento |
|---|---|---|
| simplicity | nenhuma nova dependência para A+B | stdlib e ferramentas declaradas |
| optionality | fixture de falha isolada, sem corrigir produto | browser posterior pode reusar massas sintéticas, após decisão |

## Especificação executável proposta — ainda não implementada

### Arquivos, montagem e isolamento

Criar **somente** estes arquivos de teste na execução futura:

1. `src/backend/tests/fixtures/busca_vagas_integracao.py`: `TransporteVagasRegistrado`, `AutenticadorVagasFake`, fábrica `criar_app_busca_vagas`. Reusar `solicitar_asgi` e `RespostaCredenciais` de `fixtures/credenciais_sessao.py`, sem instanciar `BancoCredenciaisSessao`. Fake de identidade implementa `AutenticadorSessao`, devolvendo `UsuarioId(UUID(int=101))` só para token sintético explicitamente aceito, registrando consultas; token desconhecido retorna `None`. A identidade da jornada principal deve entrar pelo middleware real via cookie, não por state manual. Compor `create_app(autenticador_sessao=fake, consultar_vagas=ConsultarVagas(ClienteApiVagasGrupo2Http(url_base="https://provedor.invalid/vagas", executor_http=transporte)))`.
2. `src/backend/tests/integracao_busca_vagas.py`: fluxo positivo/refinamento e matriz negativa em **métodos separados**, usando `subTest` para modalidades equivalentes de falha. Nome sem prefixo `test_` segue o precedente `integracao_repositorio_associacao_curriculo_vaga.py`, para não introduzir teste superior no discover da CI chamado de unitário. Executar explicitamente no shell `tests`.
3. `src/frontend/app/test/fixtures/busca-vagas.ts`: massas JSON sintéticas, transporte `vi.fn` com fila de promises/retornos e logs de critérios; não nova rota/adapter HTTP. Usar API pública de `features/listar-vagas`, respeitando FSD de `app` para baixo.
4. `src/frontend/app/busca-vagas.integracao.test.tsx`: montar `PaginaVagasGrupo2` com cliente real, imports públicos de `pages/vagas` e `features/listar-vagas`; `afterEach(cleanup)` e restauração dos mocks. Positivos e matriz negativa em `describe`/métodos separados no mesmo arquivo, compartilhando só fixture/oráculos. Não criar sufixo `.e2e` para DOM simulado.

Dados propostos (critério **inferido**, não massa já existente): duas vagas `vaga-e2e-001` e `vaga-e2e-002`, títulos `Estágio Python Sintético` e `QA Sintético`, empresa `Empresa Sintética`, descrição `Atividades sintéticas de teste.`, requisitos `['Python','Git']`/`[]`, localização `Cidade Sintética`, modalidade `REMOTO`, URL `https://vagas.invalid/001`/`null`. UI envolve cada vaga em `associacoes` com `curriculo_id: "curriculo-sintetico-001"`; API usa lista direta de vagas em bytes JSON. Termos `Python`, `sem-correspondencia-sintetica` e `QA`, sem pessoa real. URL é somente dado, nunca destino acessado.

Transporte fake registra cópia imutável de URL, timeout e sequência; comparar query com `urllib.parse.parse_qs`, não ordem textual do urlencode. Modos: bytes de resultado, `b"[]"`, JSON inválido `b"{"`, schema `[{"id":"incompleta"}]`, `TimeoutError`, `URLError("conexao-sintetica")`, `HTTPError` 500, exceção genérica. Nunca `sleep` para simular timeout. A cadeia real converte esses sinais. Falha canônica genérica `ErroIntegracaoVagas` exige cenário separado com porta fake canônica, explicitamente sem provar o adapter HTTP nesse caso.

Proibir egress durante a suíte com mocks de `urllib.request.urlopen` e conexões socket de saída que falhem se usados; não aplicar a política a transporte local inexistente. Frontend deve falhar se `fetch` for usado: a única chamada admitida é a função remota injetada. Relógio e aleatoriedade não participam da busca; UUID/token fixos no fake, não comparar correlation ID aleatório. Resetar app/filas/logs/DOM entre testes; aguardar cada transição para evitar corrida. Promises deferred comprovam loading sem atraso de relógio. Não criar banco, rodar migrations ou importar `main.app` no caminho positivo; teste de composição atual é independente e não precisa de banco. Não herdar `DATABASE_URL` para servidores futuros.

### Convenções da matriz

Todos os cenários são especificações **I**. Fonte de comportamento D/C aparece por linha. API: nível `system-acceptance-e2e` pela taxonomia local, descrito ao usuário como **sistema pela API/ASGI**. UI: nível **integration**, página→feature→cliente→schema, DOM jsdom; API remota simulada. Controles positivos integram o **mesmo método** negativo, com nova fase e reset de logs: mesma rota/cliente/dados aceitos, mudando somente a condição causal. Se controle falhar, cenário não comprova recusa correta. Não usar `/health` ou outro recurso como controle de vagas.

### Cenários de API

| ID / objetivo / origem | Pré-condições e passos | Oráculo específico, spy e controle | Fonte / camada / nível |
|---|---|---|---|
| A01 positivo resultado e filtros (D+I) | app completo de teste, token aceito, bytes de duas vagas; GET `/vagas?termo=Python&localizacao=Cidade+Sintetica&modalidade=REMOTO` | status real 200, `total=2`, igualdade de todos os campos/ordem devolvidos, eco termo/filtros; transporte 1 chamada, query exata e timeout 5.0; não alegar que o fake filtrou | contrato de busca, API/use case/adapter; sistema API |
| A02 positivo refinamento e vazio; contraste negativo de “há resultado” (D+I) | A01 aprovado no mesmo método; configurar `[]`; repetir com termo `sem-correspondencia-sintetica`, mesmos filtros; depois resultado para `QA` | 200, `total=0`, `vagas=[]`, eco exato; mais uma chamada com termo novo; oráculo de resultado A01 deve rejeitar o vazio; retorno posterior contém só massa da nova resposta, sem resíduo | CT-RF10-02, F5; sistema API |
| A03 negativo timeout e recuperação positiva (D+I) | primeiro A01; reset log; executor lança `TimeoutError`; GET com token e mesmos critérios; trocar para bytes válidos e repetir | 504 e detalhe literal F6, sem mensagem técnica/URL interna; fake chamado 1x com query; recuperação 200 prova rota funcional e novo registro; oráculos 200/vazio recusam falha | contrato, adapter e handler; sistema API |
| A04 negativo conexão e HTTP externo (C+I) | controle A01; variantes `URLError` sem timeout e `HTTPError(...,500,...)`; GET autenticado; restaurar sucesso | **504 atual**, mesmo detalhe de timeout, nenhuma URL/500 interno no corpo; chamada registrada por variante; recuperação 200. Rotular caracterização de divergência, nunca 502 por intenção documental | ordem dos except + MRO lida; sistema API |
| A05 negativo JSON/schema/erro inesperado (D/C+I) | controle A01; variantes `b"{"`, bytes de schema incompleto, `RuntimeError("interno-sintetico")`; GET; recuperar | 502 e detalhe literal F6, sem dado corrompido nem segredo técnico; spy 1x em cada falha; recuperar 200 com mesma query; oráculo vazio recusa esse corpo | CT-RF10-03, adapter/handler; sistema API |
| A06 negativo erro canônico base (C+I) | controle com mesma porta fake retornando DTO canônico; alternar para `ErroIntegracaoVagas`; GET | 502 controlado, porta chamada e parâmetros preservados; recuperar 200. Não afirmar teste do mapeamento HTTP externo nesta linha | `api/vagas.py`, teste unitário existente; integração API/use case/porta fake |
| A07 negativo executor ausente (D+I) | app com middleware/fake de identidade aceitando token e `consultar_vagas=None`; GET; controle app idêntico com cadeia A01 conectada | 503 literal, zero consultas de provedor; 200 e 1 consulta no controle; não misturar ausência de sessão | contrato, factory e handler; sistema API |
| A08 negativo sem cookie e cookie desconhecido (D+I) | app A01; controle autenticado 200; reset; retirar cookie ou enviar token não reconhecido | 401 “Sessão ausente ou inválida.”; provedor 0x; sem cookie autenticador 0x; desconhecido autenticador 1x. Token aceito novamente→200 e chamada; não afirmar expiração real com fake | middleware e contrato; sistema API |
| A09 negativo identidade de state ausente/inválida e precedência (C+I) | app sem middleware de sessão; middleware **exclusivo do teste**, quando necessário, injeta state ausente/string; executor conectado; controle injeta UUID válido | 401 “Autenticação necessária.” e provedor 0x; UUID→200 com chamada. Separar caso executor None e state ausente→503. Não afirmar autenticador persistido nesta montagem | `api/vagas.py` e assinatura factory; integração de fronteira |
| A10 caracterização sem restrições artificiais (C+I) | token aceito; GET com termo vazio, modalidade `QUALQUER-TEXTO`, filtro vazio e parâmetro extra; bytes válidos | 200; campo textual livre chega à query; termo whitespace omitido pelo adapter; extra desconhecido não chega ao provedor. Sem suposto negativo 422. Echo da API mantém termo bruto, query do adapter usa trim | código atual, doc 422 genérico; sistema API |

Não adicionar expiração/revogação de sessão persistida, CRUD de currículo ou associação: pertencem a outras suítes e exigiriam banco sem necessidade desta busca. Um caso de `main.app`→401, se adicionado, deve ter nome `caracteriza_composicao_atual_sem_caminho_positivo` e não contar como controle do recurso nem prova de busca: só comprova fechamento atual. Não usar skip para ocultar falha de oráculo alcançável.

### Cenários de página e cliente

| ID / objetivo / origem | Pré-condições e passos | Resultado esperado, spy e controle | Fonte / camada / nível |
|---|---|---|---|
| U01 positivo loading→resultado e pesquisa refinada (D/C+I) | render página com cliente real e função remota deferred; resolver JSON válido; digitar `  Python  `, submeter; resolver novo resultado para Python | antes: status com texto **“Carregando vagas sugeridas...”**; depois lista nomeada **“Vagas sugeridas”**, heading/título, empresa, descrição, requisitos e href da massa; ausência de vazio/alert; log `[{termo:""},{termo:"Python"}]`; input mantém espaços digitados enquanto critérios são trim; sem clique em link externo | RF11, tela e cliente reais; integration/jsdom |
| U02 positivo vazio válido e negativo sem cards residuais (D+I) | controle U01; submeter termo sem correspondência; resposta `{associacoes:[]}`; depois refinar para QA e devolver resultado | section status com heading **“Nenhuma vaga encontrada”**, texto de termo exato e orientação; input preservado; lista anterior e títulos das vagas ausentes, sem alert; query registrada; refinar restaura lista, remove vazio. Não chamar isso de erro HTTP | CT-RF10-02/CT-RF11-03, schema/UI; integration |
| U03 negativo transporte indisponível e recuperação positiva (C+I) | controle U01; submit Python; função remota rejeita `Error("falha-sintetica https://interno.invalid")`; retry com resposta válida | alert heading específico + mensagem de **serviço temporariamente indisponível**; botão retry habilitado; input preservado; sem cards/vazio; spy com Python na falha e retry; depois resultado e alert ausente; não expor URL/erro técnico | cliente→FalhaVagasGrupo2 e mensagens/UI; integration |
| U04 negativo timeout e recuperação positiva (C+I) | controle U01; função rejeita `Error("Request timed out")`; retry com mesmos critérios | mensagem exata de demora F6, não mensagem genérica; mesmas garantias de estado e spy U03; recuperação aprovada; não mede duração nem timeout de navegador | regex cliente + mensagem; integration |
| U05 negativo payload malformado e recuperação positiva (D/C+I) | controle U01; função resolve `{associacoes:[{vaga:{}}]}`; retry resolve JSON válido | alert e mensagem exata de resposta inesperada; zero cards corrompidos; termo/critério preservados; registros reais da função remota; recuperar sucesso | CT-RF10-03, Zod e UI; integration |
| U06 negativo de compatibilidade entre contratos (C+I) | controle com JSON aceito pela UI; entregar `{termo:"Python",filtros:{},total:1,vagas:[...]}` no lugar do payload; depois payload UI válido | resposta-inválida e mensagem correspondente; não transformar silenciosamente em resultado/vazio; recuperação com formato aceito prova causa. **Não chama backend** e não alega teste de contrato do parceiro confirmado | contrato de busca + schema UI; caracterização integration |
| U07 caracterização inicial e default (C+I) | método 1: deferred na chamada inicial `{termo:""}`, resolver associações vazias; método 2: página com cliente default; controle método 2 com cliente real/retorno válido | método 1: loading antes, vazio depois, 1 chamada vazia; não estado “antes de buscar”. Método 2: indisponível sem requisição HTTP e sem resultados; controle produz cards. Não conta como indisponibilidade do backend | mount da tela e default da página; integração de composição local |

Erro UI desconhecido direto possui mensagem neutra e testes unitários existentes. Não duplicar como se fosse nova modalidade de falha do cliente real: o cliente real já converte rejeições para códigos conhecidos. Se testar a mensagem neutra, rotular unidade/characterização da tela com cliente stub, não aumentar alegação da integração.

### Oráculos e controles de sensibilidade obrigatórios

Criar helpers exclusivos da suíte: `verificarResultado`, `verificarVazio`, `verificarIndisponibilidade`, `verificarCarregando`. Cada um verifica **conjunção** de sinal exclusivo e exclusão dos demais: lista nomeada + conteúdo esperado; status + heading vazio + termo; alert + heading/mensagem literal + retry; status + texto loading. `role=status` sozinho é insuficiente porque loading e vazio compartilham role. Cada helper recebe explicitamente o DOM/recorte atual; não engolir erro de `findBy`.

Após estabelecer cada estado correto, executar o **mesmo verificador** contra cada um dos outros estados incompatíveis e exigir falha (`expect(() => ...).toThrow()` para oráculo síncrono já estabilizado). Não construir DOM falso para “provar” comportamento do produto; usar estados renderizados pela página e limpeza entre montagens. Para mensagem de timeout versus indisponibilidade versus resposta inválida, aplicar a verificação literal a cada variante errada, exigindo rejeição. Na API, aplicar helpers de status+schema+conteúdo a respostas de outro estado e exigir `AssertionError`; isso detecta oráculo que aceita qualquer 200 ou qualquer corpo truthy. Os erros esperados das contraprovas são capturados e rotulados como **controle aprovado**, não falhas reais omitidas. Não capturar falhas do cenário principal.

Cobertura positiva e negativa **nos três desfechos**: resultado positivo U01/A01 e recusa do oráculo de resultado sobre vazio/falha; vazio válido A02/U02 e recusa sobre loading/resultado/erro, sem lista velha; indisponibilidade A03–A09/U03–U06 e controles positivos antes/depois que recuperam resultado, além de rejeitar falso alert nos estados saudáveis. A inexistência de vagas é “negativo” na matriz de casos e sucesso no protocolo; ambas as leituras ficam explícitas.

### Execução futura, ausência de recursos e honestidade

Comandos propostos, a partir da raiz, sem instalar nada:

```bash
nix develop .#tests --command env PYTHONPATH=src python -B -m unittest -v backend.tests.integracao_busca_vagas
nix develop .#tests --command nix develop .#frontend --command npm --prefix src/frontend test -- app/busca-vagas.integracao.test.tsx --reporter=verbose
```

O segundo compõe Node/npm do shell frontend com a entrada em tests obrigatória ao nível. Não é comando que já passou: H1 exige preflight. Se esse encadeamento não disponibilizar ferramentas corretamente, registrar bloqueio e usar o experimento temporário autorizado abaixo, sem cair em Node global. Para novos unitários que eventualmente sejam autorizados separadamente: `backend`/`frontend`, não `tests` só por conveniência.

Recurso opcional ausente deve ser verificado antes de import que causaria crash: browser spec futuro pode usar `it.skip` com motivo explícito ou suite separada opt-in; Python pode usar `unittest.SkipTest` para dependência opcional conhecida. Não capturar `Exception` de teste para converter em skip. Suíte atual A+B não exige banco/browser: ausência de composição de produção não justifica ignorá-la, pois sua composição de teste é deliberada. Se npm/Vitest/Python base não existir, a falha acontece antes do runner; registrar **bloqueado, zero testes executados**, sem fabricar “skip aprovado”. Um launcher futuro só deve retornar resultado de indisponibilidade com motivo e contagens claras; CI precisa diferenciar esse estado de aceitação concluída.

Registrar separadamente: planejados, descobertos, executados/aprovados, falhos, ignorados e motivo, por ID. **Skip não é prova.** Se só API executou, só API foi comprovada. Permitido: “rota ASGI com dependências de teste produziu 200/502/503/504/401”, “página/cliente em jsdom apresentaram estados para respostas simuladas”. Proibido: navegador real, layout, responsividade visual, leitor de tela, conformidade acessível integral, desempenho/SLA, provedor real, filtros realmente aplicados pelo parceiro, persistência/login reais ou composição de produção validada por A+B. Não usar latência de unittest/Vitest como RNF08. Não inferir que indisponibilidade de parceiro foi medida.

## Ambiente e baseline informativo observado

### Oferta declarada e instalação

`flake.nix`: `x86_64-linux`, nixpkgs `nixos-unstable`; lock fixa `b1b875982b17dabde9b4a37f3e229e74913e6db3`. `backend-python-packages.nix`: fastapi, uvicorn, sqlalchemy, alembic, psycopg, pydantic-settings. `backend`: Python com esses pacotes + Git; `tests`: mesmos + aiosqlite; `frontend`: Node + Git (npm disponível na execução); `quality`: Node, Git, Ruff, Gitleaks e Python base + Bandit, coverage, Radon. Nenhum browser declarado; `tests` não declara Node. Não há manifesto Python necessário ao comando de teste além do Nix encontrado na inspeção direcionada; não se presume pytest/httpx.

`docs/configuracao-ambiente.md`: dependências frontend por `npm ci` no Nix, baseadas no package-lock; backend pelo shell Nix. **Não foi executado npm ci nem qualquer instalação**. As dependências existentes permitiram os comandos abaixo. Nix não declara rede desligada nem política de loopback; ambiente desta sessão tem rede restrita e sandbox não permite escrever no store. Tentativas iniciais dos comandos backend/test frontend/Ruff falharam antes da execução com `error: opening lock file "/nix/var/nix/db/big-lock": Read-only file system`. Foram repetidas com escalonamento de sandbox aprovado. Não se atribui esse bloqueio ao código. Nenhum serviço externo foi chamado pela análise; não foi verificado egress de toda a suíte legada por monitoramento de rede.

### Comandos reais e resultados

| Comando executado | Ambiente / resultado observado | Contagens / ressalva |
|---|---|---|
| `nix develop .#backend --command python -B -m unittest discover -s src/backend/tests -t src` | baseline do comando CI com `-B`; resumo confirmado em repetição com `2>&1 \| tail -90` | **955**, OK, **33 skips**, portanto 922 sem skip, 0 falhas/erros; pipe da repetição tem status de tail, conclusão vem do resumo unittest |
| `nix develop .#tests --command python -B -c 'import unittest,sys; sys.path.insert(0,"src"); suite=unittest.defaultTestLoader.discover("src/backend/tests",top_level_dir="src"); result=unittest.TextTestRunner(verbosity=0).run(suite); print("BASELINE_IDENTITIES"); [print("SKIP",test.id(),reason) for test,reason in result.skipped]; [print("FAIL",test.id(),detail) for test,detail in result.failures+result.errors]; print("TOTAL",result.testsRun,"SKIP",len(result.skipped),"FAIL",len(result.failures),"ERROR",len(result.errors)); sys.exit(not result.wasSuccessful())'` | mesma suíte também em tests, captura final via `2>&1 \| tail -50` | **955, 33 skips, 0 falhas, 0 erros**; confirma bloqueios de grafo mesmo com aiosqlite |
| `nix develop .#tests --command env PYTHONPATH=src python -B -m unittest backend.tests.test_api_vagas backend.tests.test_consulta_vagas_use_case backend.tests.test_cliente_vagas_grupo2_http backend.tests.test_application_vagas_port backend.tests.test_double_api_vagas_grupo2` | amostra existente de vagas | **35 aprovados**, 0 skips |
| `nix develop .#tests --command env PYTHONPATH=src python -B -m unittest backend.tests.integracao_repositorio_associacao_curriculo_vaga` | gate integrado da CI | **1 aprovado**; banco dessa suíte não comprova grafo Alembic válido nem busca de vagas |
| `nix develop .#frontend --command npm --prefix src/frontend test -- --reporter=verbose` | suíte completa Vitest existente | **55 arquivos: 53 aprovados/2 falhos; 286 testes: 280 aprovados/6 falhos; 0 skips reportados**; seis timeouts de 5000ms, nomes abaixo |
| `nix develop .#quality --command ruff check --output-format=concise src/backend` | Ruff, mesmo gate CI com saída concise em vez de github | **0 diagnósticos**, “All checks passed!” |
| `nix develop .#frontend --command npm --prefix src/frontend run lint` | ESLint | saída 0, nenhum diagnóstico |
| `nix develop .#frontend --command npm --prefix src/frontend run check` | `tsc -b --pretty false` | saída 0, nenhum diagnóstico no grafo configurado |
| `nix develop .#frontend --command npm --prefix src/frontend run format:check` | Prettier check | saída 0, “All matched files use Prettier code style!” |
| `nix develop .#quality --command npm --prefix src/frontend run build` | `tsc -b && vite build` | saída 0, 36 módulos; output em `src/frontend/dist` ignorado |
| `nix develop .#quality --command gitleaks git --redact --no-banner --exit-code 1` | gate local de histórico | saída 0, **311 commits**, “no leaks found”; não é auditoria universal de segurança |

CI `.github/workflows/ci.yml`: Ruff em quality, discover em backend, integração nomeada em tests; frontend quality faz **npm ci**, lint, format:check, check e build em quality; secrets-scan com histórico completo. Não há passo frontend `npm test` no workflow lido. Lint/tipos/formatação frontend foram executados em `frontend`, que oferece Node, conforme atividade de componente; CI usa quality (também Node), build foi exercitado ali. Não se repetiram todos em quality sem necessidade. `npm ci` **não executado** por proibição de instalar. Não há gate backend de tipos/formatação no workflow lido; não inventar mypy/pyright ou comando de script inexistente.

O discover chamado de unitário pela CI contém testes integrados: nome do job não muda nível. A execução adicional em `tests` informa esse contraste; não é autorização para acrescentar novo integrado ao discover em backend. O script frontend também inclui os dois arquivos chamados e2e, embora a execução baseline tenha seguido o script/ambiente frontend existente. Novos testes superiores terão comando `tests` explícito.

`tsconfig.app.json` inclui `app` e `vite-env.d.ts`, seguindo imports; `tsconfig.node.json` inclui `vite.config.ts`. “Tipos passaram” refere-se a esse grafo, não à garantia de que todo teste em `features` foi verificado. ESLint usa Babel parser, regras JSX a11y, React hooks, boundaries FSD e imports sem ciclo; não é type checker. Teste novo em app entra no include de tipos.

### Identidade das seis falhas frontend (não corrigidas)

Todas: `Error: Test timed out in 5000ms.` Não foi alterado timeout nem atribuída causa; execução de baselines em paralelo pode afetar duração, mas isso é hipótese, não diagnóstico confirmado.

| Arquivo / linha | Nome literal |
|---|---|
| `app/jornada-curriculo.e2e.test.tsx:194` | conclui a jornada com sucesso desde o preenchimento de dados pessoais até a liberação e disparo das ações de exportação |
| `app/jornada-curriculo.e2e.test.tsx:305` | bloqueia as ações de confirmação e exportação de PDF quando uma seção obrigatória está pendente |
| `app/jornada-curriculo.e2e.test.tsx:389` | preserva os dados preenchidos e impede o avanço quando o double indica indisponibilidade |
| `app/jornada-curriculo.e2e.test.tsx:439` | permite retornar da revisão para editar os dados pessoais e avançar novamente |
| `app/jornada-selecao-previa-exportacao.e2e.test.tsx:258` | conclui criação, edição, seleção, prévia e exportação com download simulado |
| `app/jornada-selecao-previa-exportacao.e2e.test.tsx:347` | bloqueia prévia e exportação quando nenhuma experiência foi selecionada |

Nenhuma dessas falhas é teste de vagas. Os testes de vagas existentes estavam entre os aprovados; API+unidades de backend foram também executados separadamente (35).

### Identidade dos 33 skips backend

Capturados por `test.id()` e motivo, não só total. Prefixo comum `backend.tests.`. Para comparação futura usar cada módulo/classe/método abaixo, não aceitar que outro teste falhe/ignore só porque o total continuou 33.

| Módulo.Classe | Métodos ignorados | Motivo |
|---|---|---|
| `test_integracao_composicao_credenciais_sessao.ComposicaoCredenciaisSessaoIntegracaoTestCase` | `test_C02_fluxo_autenticado_ignorado_por_produto` | produção não compõe login, criador, revogador nem autenticador persistido |
| `test_integracao_contrato_credenciais_sessao.ContratoCredenciaisSessaoIntegracaoTestCase` | `test_H01_emissao_cookie_e_persistencia_duravel`; `test_H02_login_recusado_uniforme`; `test_H03_formatos_de_login`; `test_H04_uso_proprio_sem_prolongar_sessao`; `test_H05_somente_cookie_autentica`; `test_H06_cookie_desconhecido_e_malformado_caracterizado`; `test_H07_sessao_expirada_ou_revogada`; `test_H08_conta_excluida_invalida_todas_sessoes`; `test_H09_isolamento_de_identidade`; `test_H10_dependencias_ausentes`; `test_R01_logout_revoga_somente_sessao_atual`; `test_R02_repeticao_preserva_primeira_revogacao`; `test_R03_logout_sem_sessao_ativa` | revisões Alembic duplicadas |
| `test_integracao_persistencia_sessao.PersistenciaSessaoIntegracaoTestCase` | `test_M01_schema_migrado_ate_head`; `test_M02_unicidade_e_campos_obrigatorios`; `test_M03_fk_rejeita_usuario_inexistente`; `test_P01_criador_persiste_hash_duravel_e_autentica`; `test_P02_fronteira_de_expiracao_sem_mutacao`; `test_P03_rollback_externo_descarta_flush` | revisões Alembic duplicadas |
| `test_integracao_recusa_curriculo_alheio.RecusaCurriculoAlheioIntegracaoTestCase` | `test_s10_cookie_desconhecido_recusa_todas_as_rotas`; `test_s1_controle_positivo_em_cada_rota`; `test_s2_dono_b_no_caminho_recusado_antes_dos_executores`; `test_s3_curriculo_b_sob_dono_a_recusado_no_caso_de_uso`; `test_s4_curriculo_alheio_e_inexistente_tem_mesma_resposta`; `test_s5_item_alheio_e_inexistente_nao_entram_no_curriculo_a`; `test_s6_caracteriza_extra_proibido_na_ordem_sem_efeitos`; `test_s6_caracteriza_extras_ignorados_sem_trocar_proprietario`; `test_s7_sem_cookie_recusa_todas_as_rotas`; `test_s8_sessao_revogada_recusa_todas_as_rotas`; `test_s9_sessao_expirada_recusa_todas_as_rotas` | cadeia Alembic com revisões duplicadas |
| `test_integracao_rejeicao_requisicoes_sem_credenciais_validas.RejeicaoSemCredenciaisValidasTestCase` | `test_sessao_expirada`; `test_sessao_revogada` | a aplicação ainda não compõe persistência de sessões |

Duplicatas indicadas literalmente pelos guards e confirmadas pelas atribuições lidas: revisão `20261015_0011` em `20261015_0011_criar_cursos.py` e `20261015_0011_exclusao_logica_formacoes_academicas.py`; `20261015_0012` em `20261015_0012_criar_links_profissionais.py` e `20261015_0012_criar_projetos_academicos.py`, sob `src/backend/infrastructure/persistence/alembic/versions/`. Não foi executada migração nova nem verificação completa de head/ciclo; duplicidade já basta para o bloqueio dos harnesses. Os cenários propostos A+B não exigem banco, portanto não dependem dessa correção.

Warnings observados no baseline: `StarletteDeprecationWarning` de `HTTP_422_UNPROCESSABLE_ENTITY` nos testes de cadastros regressão, criar versão, dados de contato, idiomas, itens, perfil e versão; warnings asyncio de tarefas lentas e aviso de política IA inválida com manutenção da última versão. Não houve diagnóstico de lint/tipos. Não tratar warning com identificador aleatório de tarefa como regressão por texto bruto; comparar classe, local e mensagem estável. Não se coletou lista exaustiva de todos os warnings nas saídas truncadas.

## Achados de backend, frontend e documentação — sem correção

| Área | Achado / divergência | Fonte mais confiável para o teste atual e razão |
|---|---|---|
| Backend | main sem executor de vagas e auth fechado; 401 encobre 503 | `main.py`, autenticador e middleware atuais, porque definem a aplicação executada; não intenção da análise antiga |
| Backend | 5xx e conexão podem virar 504, contrário a “5xx→RespostaInvalida” | ordem dos `except` no adapter e MRO do Python Nix; caracterizar e reportar, sem exigir 502 inexistente |
| Backend | double de falha usa classes diferentes das exceções capturadas | arquivos atuais dos dois módulos; não reutilizar modo de falha presumindo equivalência nominal |
| Backend | docstring de use case fala normalizar, mas delega cru; DTO string versus API nullable | instruções executadas/tipos de resposta e conversão do adapter; assertions por fronteira |
| Frontend | página não roteada, default sempre indisponível, sem HTTP de vagas | App/página/cliente atuais; RF11 é obrigação, não prova de completude |
| Frontend | formato de associações incompatível com API de busca; critérios só termo | schemas atuais; não transpor filtros API para UI |
| Frontend | corridas possíveis em buscas sobrepostas; retry conserva critérios da falha, não necessariamente texto editado depois | UI atual; novo comportamento aguarda design, fora da matriz obrigatória proposta |
| Documentação | análise de 15/10 chama contrato “alinhado entre equipes”; contrato atual diz “proposta” | status explícito de `docs/contratos_integracao_grupo2.md`, corroborado pelo contrato de busca; análise histórica não confirma acordo externo |
| Documentação | contrato cita 422, mas três queries são textuais sem restrições | assinatura executável da rota para oráculo; documento serve como intenção genérica, lacuna para exemplo inválido |
| Documentação/testes | E2E “no navegador”, ARIA dito como leitor real | runner jsdom e imports; nomes não ampliam prova, dossiê atual já limita jornada simulada |
| Documentação | vazio classificado negativo, mas processamento é sucesso | matriz para categoria do cenário; contrato/código para status; não há conflito no oráculo quando dimensões separadas |
| Ambiente | migrations duplicadas, browser ausente, tests sem Node, timeouts de currículo | atribuições Nix/migration e execução local; não corrigidos nem incorporados como feature desta entrega |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda | Severidade | Afetados |
|---|---|---|---|
| correctness | teste verde por ponte inventada ou rota sempre falha | alta para confiança | QA/revisão |
| reliability | rede externa torna resultado não determinístico | alta | CI/equipe |
| user-value | API verde sem verificar mensagem de vazio/erro | média | estudante |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | manter duas cadeias explicitamente separadas | simplicidade | aceitável enquanto contratos não conectados |
| reliability | transporte e identidade simulados | fidelidade de produção | aceitável com limites expressos e sem alegar auth real |
| simplicidade | adiar browser e navegação integrada | abrangência da jornada | só aceitável se produto aceitar alcance; caso contrário card permanece incompleto |

## Riscos e efeitos de segunda ordem

Caracterizar 504 pode cristalizar defeito: nomear cenário como caracterização e vincular achado para revisão quando a correção for autorizada. Skips podem produzir falsa aprovação: separar contagens e alegações. Duplicação entre novas integrações e unidades pode aumentar manutenção: testar colaboração e parâmetros reais, não repetir detalhes internos já verificados. Habilitar browser sem composição pode criar harness enganoso: exigir declaração de quais módulos são produtivos e quais são exclusivos do teste. Generalizar prova de currículo para vagas é proibido: os harnesses anteriores só justificam descoberta do ferramental/convenção.

## Validação da decisão

| Hipótese / resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| três desfechos executados | IDs A/U com status e contagens | comandos explícitos, logs de spy e oráculos sensíveis | skip/falha ou ausência de estado exclusivo |
| requests atravessam cadeia | query/timeout registrados e retorno serializado | adapter real até função fake; cliente UI real até função fake | stub antes da camada que se afirma provar |
| negativo causal | controle positivo no mesmo método e mesmo recurso | alterar apenas condição de falha | controle falha ou provedor chamado em recusa anterior |
| ambiente composto suficiente | Node/npm de Nix e Vitest disponível em tests+frontend | preflight do comando proposto | executável global ou dependência faltante |
| sem regressão | identidades de teste/diagnóstico baseline e final | comparar listas e mensagens estáveis, não apenas totais | nova falha/skip/diagnóstico mesmo com contagem igual |
| E2E integrado passa a ser possível | rota App, cliente compatível, main ligado e browser declarados | nova inspeção e nova versão da análise | mudanças nesses artefatos ou aceite exige browser |

Executar na implementação os testes novos e os comandos reais de baseline acima, preservando Nix adequado por nível. Não repetir instalações. Gate backend de lint permanece quality; frontend lint/check/format no frontend, CI quality equivalente documentado. Se houver testes integrados no discover, registrar a mistura existente e usar tests para eles; não ampliar erro de classificação. Baseline final deve comparar as seis identidades de timeout e 33 skips, não “permitir qualquer seis falhas”. Uma falha nova de vagas nunca é absorvida pelo baseline legado. Capturar causa se houver variação de timeout; não prometer causa conhecida.

## Handoffs e atividades posteriores

### Divisão de trabalho e adequação das skills inventariadas

Inventário real `.agents/skills`: **sete** diretórios de skills. Foram lidos os sete `SKILL.md`, os contratos de escopo e testes de adequação abaixo. São instruções de processo consultadas como contexto; não invocação de implementação nesta análise.

| Skill / arquivos lidos (relativos a `.agents/skills/`) | Trecho decisivo / adequação desta fatia |
|---|---|
| `decision-analysis-v4/SKILL.md` e quatro referências obrigatórias já registradas | “A única escrita permitida é um novo artefato Markdown de análise.” **Elegível para esta entrega**, não executor de teste. Não possui fit-check separado; adequação: demanda exige decisão antes de implementar, artefatos e roteamento |
| `integration-system-testing-v1/SKILL.md`, `references/test-scope-boundary.md`, `references/test-fit-check.md` | permite “API, sistema, aceitação, E2E”; fit exige resultado teste, nível superior, oráculo e alvo seguro. **Elegível para A+B**, condicionada à validação formal na futura invocação. Sinais independentes: chamada ASGI atravessa middleware/use case/adapter; página atravessa cliente/schema real; dados locais isolados; nenhum produto novo |
| `frontend-implementation-v3/SKILL.md`, `references/scope-boundary.md`, `references/frontend-fit-check.md` | “não … composição de múltiplas camadas”; “demanda composta apenas por teste integrado/sistêmico”→mismatch. **Não elegível para A+B**; elegível só para eventual unidade cliente isolada separadamente autorizada, não substitui esta entrega |
| `backend-domain-orchestration-v2/SKILL.md`, `references/clean-boundary.md`, `references/backend-fit-check.md` | qualquer teste deve “isolar uma unidade interna”; níveis superiores encaminhados. **Mismatch** para sistema API |
| `backend-adapters-drivers-v2/SKILL.md`, `references/outer-boundary.md`, `references/backend-fit-check.md` | proíbe “testes de integração, contrato, API … E2E”; exige unidade externa isolada. **Mismatch** para A+B; não autoriza corrigir adapter neste card |
| `cross-cutting-implementation-v1/SKILL.md`, `references/scope-boundary.md`, `references/cross-cutting-fit-check.md` | fit exige resultado mecanismo transversal e teste unitário; “teste solicitado atravessa uma fronteira real” é sinal negativo. **Mismatch**, mesmo que testemos indisponibilidade/autenticação já existentes |
| `nix-environment-implementation-v1/SKILL.md`, `references/nix-scope-boundary.md`, `references/nix-fit-check.md` | resultado deve ser ambiente Nix e só Nix; manifesto npm é `non-nix`. **Mismatch para teste**; elegível apenas para handoff separado de Nix se aprovado, nunca para toda a entrega multitecnologia |

Não há lacuna de processo para os testes A+B: a skill integrada existe. Para executar depois, invocar explicitamente `$integration-system-testing-v1` com **este caminho e v001**, aprovando a fatia proposta (regra da própria skill). Não há autorização nesta análise para implementar agora. Para browser/experimento de ambiente multitecnologia, a skill integrada proíbe Nix operacional e a skill Nix proíbe npm; usar tarefa direta delimitada ou handoffs separados, com exceções do usuário explicitadas. O pedido atual já autoriza **registrar** o protocolo temporário, não executá-lo durante análise. Não exigir aprovação repetida para ações já autorizadas na futura execução; respeitar bloqueios reais de sandbox.

### Pré-requisitos separados para navegador real

Somente se produto exigir: escolher runner/browser/versionamento, declarar dependências exclusivamente dev/test, disponibilizar Node + Python + browser e bibliotecas no ambiente tests, configurar fixture web e backend locais com provedor fake, bloquear egress externo, garantir rota e contrato produtivos ou declarar harness de página separado. Nomes propostos futuros, ainda não aprovados nem existentes: `src/frontend/playwright.config.ts`, `src/frontend/e2e/busca-vagas.spec.ts`, `src/backend/tests/fixtures/servidor_busca_vagas.py`. Não fornecer comando `npx playwright` como se já existisse: pacote/versão/comando precisam ser aprovados e declarados antes. A alternativa sem isso é A+B, com os limites anteriores.

### Alterações temporárias de ambiente — protocolo solicitado, não executado

Primeiro executar no estado original e registrar bloqueios. Somente depois, na atividade futura autorizada, pode haver experimento com `nix/*`, `flake.nix`, `flake.lock`, `src/frontend/package.json` e `src/frontend/package-lock.json`. **Nenhuma alteração permanente** desses caminhos faz parte desta entrega. Antes: `git status --short -- nix flake.nix flake.lock src/frontend/package.json src/frontend/package-lock.json src/backend/infrastructure/persistence/alembic/versions` e `git diff -- <mesmos caminhos>`; verificar também staged/untracked. Se houver mudança do usuário em qualquer alvo, **parar e informar**, sem restaurá-la.

Para A+B, não se recomenda banco nem linearização. Se cenário futuro aprovado exigir banco migrado e o grafo tiver duplicatas/múltiplas heads, experimento pode mudar **somente identificadores e arestas** `revision/down_revision`, nunca DDL. Registrar mapa antes/depois, analisar grafo por AST no shell tests (unicidade, referências existentes, ausência de ciclos e exatamente uma head), e executar `nix develop .#tests --command alembic heads` sem warnings de duplicidade; depois upgrade no SQLite temporário deliberadamente configurado. Não aplicar contra URL herdada ou banco compartilhado. Só uma head sem warnings **e** sem ciclo é condição do experimento; não basta ignorar warning. O algoritmo/check exclusivo de teste deve ser escrito somente na tarefa de execução aprovada, sem inventar script existente aqui.

Guardar **diff completo**, inclusive lockfiles, no resumo da execução antes de restaurar. Ao final, fora de Nix, restaurar apenas alvos efetivamente alterados e originalmente limpos, com caminhos explícitos. Exemplos para o conjunto atualmente existente (não executar se não foi alterado):

```bash
git restore -- flake.nix flake.lock nix/backend.nix nix/backend-python-packages.nix nix/frontend.nix nix/tests.nix nix/quality.nix src/frontend/package.json src/frontend/package-lock.json
git restore -- src/backend/infrastructure/persistence/alembic/versions/20261015_0011_criar_cursos.py src/backend/infrastructure/persistence/alembic/versions/20261015_0011_exclusao_logica_formacoes_academicas.py src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_links_profissionais.py src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_projetos_academicos.py
git status --short -- nix flake.nix flake.lock src/frontend/package.json src/frontend/package-lock.json src/backend/infrastructure/persistence/alembic/versions
```

Se outras arestas precisarem mudar, adicionar os nomes reais ao restore e ao resumo; nunca usar `git restore .`, wildcard como substituto de inventário, nem apagar mudanças do usuário. Arquivo temporário novo não rastreado não é removido por restore: listar e tratar individualmente na autorização de limpeza, sem `git clean` amplo. O status final **não pode listar nenhum caminho do experimento**. A execução sob ambiente temporário prova componentes **nesse ambiente**, não a definição Nix/manifests permanentes. Registrar ambos os resultados lado a lado, com skip/bloqueio original e aprovações experimentais.

Nesta análise, diff de ambiente/migrations: **vazio**, nada a restaurar. `git status --short` estava vazio após baselines/build, antes deste Markdown. Build gerou somente dist ignorado. Não foi feito experimento temporário.

### Artefatos e evidência mínima

`git ls-files '*gitignore*'` retorna somente `src/frontend/.gitignore`: `node_modules/`, `dist/`, `*.tsbuildinfo`. Não há `.gitignore` raiz. Faltam regras versionadas para relatórios browser, `test-results/`, `playwright-report/`, traces, vídeos, capturas e caches Python; não criá-los dentro do Git nesta análise. Recomendar outputs em `/tmp/busca-vagas-<execucao>/` e cache/browser fora de fonte, sem download nesta tarefa. Não comitar dependências, browsers, cache, dist nem relatórios brutos; verificar `git status --short --untracked-files=all` ao final da implementação. Não remover caches preexistentes do usuário.

Precedente `docs/testes/evidencias/f11-vagas-responsividade-movel.md` registra método, limites, comandos e controles, além de baseline por identidade. Recomenda-se **um registro manual mínimo** `docs/testes/evidencias/busca-vagas-tres-desfechos.md` na futura implementação: commit, ambiente original/temporário, IDs/contagens, controles, falhas/skips, limites e diffs completos temporários, sem dados pessoais nem outputs brutos. PR deve resumir e apontar esse registro; só texto do PR é opção mais leve, mas perde evidência versionada de limites/experimento. Não há regra encontrada que torne screenshots obrigatórios para A+B. Este documento de análise já registra o baseline de hoje; não criar segundo arquivo agora.

## Síntese

A branch tem contratos e unidades suficientes para especificar sistema pela API com transporte externo fake e integração página/cliente com respostas fake. Ela não tem ligação produtiva entre as duas pontas nem ferramental de browser declarado. Recomendação D proposta para aprovação da fatia, com três desfechos e positivos/negativos/controladores explicitados; E2E integrado permanece sem prova. Principal incerteza: qual alcance o responsável pelo card aceitará para o termo E2E. Nenhum teste/produto/ambiente foi implementado ou corrigido nesta análise.

## Apêndice A — Entrada literal da demanda

```text
$decision-analysis-v4 Implementar "Criar cenário E2E para busca de vagas com resultado, vazio e indisponibilidade.". O resultado esperado é um teste executável, com **cenários positivos e negativos**. Antes de decidir o que ele contém, descubra o que o projeto define e implementa para a busca de vagas, o que "E2E" significa e o que o ferramental disponível consegue provar, o que cada um dos três desfechos do título (resultado, vazio e indisponibilidade) significa neste projeto e como cada um se manifesta para quem usa a busca. Esta é uma análise nova, iniciada do zero.

## Regra principal: não presumir

Todo fato deve vir de um artefato lido (histórico Git, código, testes, configuração, documentação, requisitos, contratos de integração, workflows de CI, definições de ambiente), com o caminho indicado. O que nenhum artefato definir deve ser registrado como lacuna, nunca como fato.

- Separe em seções distintas: **(a) fatos encontrados**, com caminho e trecho; **(b) lacunas**, ou seja, o que nenhum artefato define; **(c) recomendações**, que são suas, com justificativa.
- Para cada lacuna, apresente as opções viáveis, recomende uma e marque se depende de decisão de produto ou de design, ou se pode ser tomada tecnicamente com base no que existe.
- Quando artefatos divergirem (documentação, código, contrato de integração, testes), aponte a divergência, diga qual fonte parece mais confiável e por quê, sem escolher em silêncio.
- Não transponha para a busca de vagas regras, convenções ou resultados de testes de outros recursos sem que um artefato sobre vagas as sustente.

## Ponto de partida

Parta exclusivamente do estado atual desta branch, criada a partir da `dev`. Não presuma a existência de nenhuma página, rota, cliente, provedor, teste, fixture, cenário ou análise sobre busca de vagas. Descubra por inspeção o que existe: o que existir entra como fato (com a cobertura avaliada), o que não existir entra como lacuna. **Inventarie os harnesses e fixtures de teste que de fato existem na base** (backend e front-end) e não presuma nomes.

## Texto do card

Somente o título foi fornecido: "Criar cenário E2E para busca de vagas com resultado, vazio e indisponibilidade.". Não há descrição nem critérios de aceite. **Não invente critérios.** Derive o que for possível do título e dos artefatos, marque a origem de cada critério como "inferido" e liste exatamente o que precisa ser fornecido para fechar cada lacuna. O título e o pedido do usuário exigem **os três desfechos (resultado, vazio e indisponibilidade) e cenários positivos e negativos**: isso é requisito da entrega.

## Fontes a analisar

1. **Histórico Git local.** A CLI do GitHub e a rede podem não estar disponíveis; **não dependa delas**. Localize por inspeção (merges "Merge pull request #N", squashes com sufixo "(#N)", mensagens, nomes de branch e histórico dos arquivos) os trabalhos ligados à busca de vagas no backend e no front-end. Número de card não é número de PR: não infira a ligação apenas pela coincidência de números, e registre como identificou cada trabalho.
2. **Documentação pertinente**, localizada por busca (não presumida): requisitos funcionais e não funcionais (inclusive disponibilidade, tempo de resposta e usabilidade), contratos de integração com a fonte externa de vagas, a matriz de rastreabilidade e a de testes, documentos de interface e análises anteriores em `prompts/`. Registre os termos buscados (por exemplo vaga, busca, indisponibilidade, timeout, vazio, fallback, estado de erro) e o que cada busca retornou, **inclusive resultados vazios**.
3. **Código atual relacionado**, no backend e no front-end: rotas e handlers, DTOs, casos de uso, portas, clientes do provedor externo, doubles de provedor, traduções de erro para status, composição da aplicação (`main.py` e `factory.py`), a página e as features do front-end, o cliente HTTP do front-end, os estados da interface e os testes existentes (unitários, de componente, integrados e de ponta a ponta).
4. **Ferramental e instruções:** `AGENTS.md` (raiz, backend e front-end), manifestos de dependências e lockfile, configurações de bundler, linguagem, lint e testes, definições de ambiente Nix, workflows de CI e as skills disponíveis em `.agents/skills` (inventarie quais existem, sem presumir nomes).

## O que levantar

- **O que é "E2E" neste projeto.** Procure a definição em `AGENTS.md`, nas referências das skills de teste (classificação de níveis, inclusive "aceite de sistema ponta a ponta"), em `docs/` e em `prompts/`. Verifique, **com evidência**, o que os arquivos de teste hoje chamados de "e2e" ou "ponta a ponta" de fato exercitam: em qual runner e ambiente rodam, se há navegador real, se a interface é renderizada de verdade, se a API é a real ou simulada. Descubra se existe ferramental de navegador (por exemplo Playwright, Cypress ou modo navegador do runner), se está declarado nas dependências e se o ambiente Nix o provê (Node, gerenciador de pacotes, navegador). Se nada definir "E2E", trate como lacuna.
- **Os desfechos do título, um a um, e como se manifestam:**
  - **Resultado:** a operação que busca, os parâmetros aceitos (e suas regras), o formato da resposta, quem fornece as vagas e como o resultado chega à interface.
  - **Vazio:** quando a busca devolve zero vagas é sucesso (e com qual status), e se existe também um estado vazio **antes** de buscar; como a interface o apresenta. Registre se "vazio" é desfecho válido ou erro no contrato.
  - **Indisponibilidade:** o que o projeto entende por indisponível (provedor externo fora do ar, timeout, erro de integração, executor não composto, falha de rede no cliente); **o status ou sinal de cada falha no backend**, como o cliente do front-end a interpreta e o que a interface mostra (mensagem, possibilidade de repetir a busca, preservação do que o usuário digitou). Registre separadamente o que está **definido em documento** e o que está **só implementado**. Não force um status que o código não produz.
- **A fonte externa de vagas e como isolá-la.** Descubra como o provedor é acessado, se existe contrato documentado, se há double ou simulador reutilizável e como produzir de forma **determinística** cada desfecho (resultado, vazio, falha, timeout) **sem chamar serviço real nem usar rede**. Registre o que o ambiente de teste permite (portas locais, rede desligada).
- **O contrato de cada camada e a precedência dos erros.** Autenticação, validação de parâmetros, executor ausente, erro do provedor, timeout. Registre em que ordem essas condições são avaliadas e qual camada responde, para o cenário não misturar oráculos.
- **A cadeia realmente exercitável.** Descubra se a interface de vagas está acessível na aplicação (rota, composição) e se a aplicação do backend que sobe tem os executores de vagas ligados; registre o que a composição de produção faz hoje e o que isso implica para o que um cenário consegue provar. Se não houver ligação real entre front-end e backend, diga o que é possível montar dentro do teste e qual limite declarar.
- **Cobertura existente:** o que já é coberto sobre busca de vagas, em que nível e com que oráculos, para o cenário novo não repetir cobertura sem necessidade.
- **O que cada nível de teste consegue provar sobre a jornada.** Avalie, com base no que o projeto tem, alternativas como: (a) teste de sistema pela API, com o provedor simulado; (b) teste de componente ou de página no front-end com a API simulada; (c) jornada em navegador real contra um backend de teste; (d) combinação. Para cada uma, diga o que prova e o que **não** prova, o que exige de ambiente e se pode ser executada com o que existe. **Se a recomendação não envolver navegador real, diga explicitamente se o rótulo "E2E" do card pode ser usado sem exagero e qual nome e qual descrição refletem o nível real do teste.**
- **O ambiente de execução:** o que cada ambiente Nix (backend, front-end, tests, quality) oferece hoje, como as dependências são instaladas, se há rede durante a execução, e quais comandos de testes, lint e tipos existem (em manifestos, workflows e documentação). Execute apenas comandos de leitura e um **baseline informativo** das suítes do backend e do front-end e dos gates de lint e de tipos, registrando comando, ambiente, resultado e contagens, sem alterar nada. Se alguma dependência instalada faltar, registre o bloqueio e **não instale nada**.
- **Bloqueios preexistentes:** registre, sem tratá-los como escopo e sem corrigi-los, tudo que impediria executar o cenário (ferramental de navegador ausente, dependências não instaladas, interface sem rota, backend sem composição de vagas, banco ou migrations inválidos se o cenário os exigir, ambiente sem rede).

## Escopo

Definir o **cenário executável** da busca de vagas, cobrindo os três desfechos (resultado, vazio e indisponibilidade) com **cenários positivos e negativos**: etapas, dados, verificações, resultados esperados, fixtures, forma de execução, nível real do teste e limites do que prova.

Fora do escopo: alterar a página, a API, o cliente, o provedor, os contratos ou a composição; implementar funcionalidade de vagas que não exista; corrigir defeitos encontrados (registre-os como achados); chamar o provedor real ou qualquer serviço externo; alterações permanentes de ambiente ou de dependências; alterações em outros recursos.

## Instruções

- Para cada decisão que os artefatos não resolverem, recomende uma opção com justificativa e marque se depende de produto, de design ou de engenharia.
- **Cobertura positiva e negativa obrigatória, nos três desfechos.** Cada cenário deve ter objetivo, pré-condições, passos, resultado esperado, a fonte que o sustenta, a origem do critério (definido ou inferido), a camada exercitada e o nível do teste. Considere, **apenas se algum artefato os definir ou implementar**:
  - **Positivos:** busca com resultado e a apresentação das vagas devolvidas; parâmetros e filtros chegando ao provedor; busca repetida ou refinada; o desfecho vazio como resultado válido; recuperação depois de uma indisponibilidade.
  - **Negativos:** indisponibilidade do provedor (cada modalidade de falha que o código distingue, por exemplo timeout e erro de integração); executor não composto; parâmetro inválido; ausência de sessão ou identidade inválida, se a rota exigir; resposta malformada do provedor, se o código a trata; e qualquer outra recusa implementada.
  - **Controles:** todo cenário negativo deve ter um **controle positivo** no mesmo recurso, para provar que a recusa vem da regra e não de uma rota ou tela que sempre falha; cada estado da interface deve ser verificado por uma asserção **específica daquele estado** e deve existir um **controle de sensibilidade** (a mesma verificação aplicada ao estado errado deve falhar), de modo que um teste não passe por coincidência. Verifique, por spies ou registros do provedor simulado, que a requisição **realmente atravessou** a cadeia (parâmetros recebidos) e que, nas recusas anteriores ao provedor, ele **não** foi chamado.
  - O que não estiver definido entra como lacuna, e a análise deve dizer se o cenário registra o comportamento atual como caracterização (rotulada como tal) ou aguarda decisão.
- Defina a estrutura: nomes e localização dos arquivos conforme a convenção de cada camada, reaproveitamento dos harnesses e fixtures **que de fato existem na base**, configuração necessária, isolamento (rede, relógio, aleatoriedade, estado), dados sintéticos (nenhum dado pessoal), como os testes são executados e como os que dependem de recurso ausente são ignorados com motivo explícito, sem gerar erro quando o ambiente não os suporta. Diga se fluxos positivos e matriz negativa devem ser métodos ou arquivos separados.
- **Honestidade da prova.** Um teste ignorado não é prova. Diga como o resultado distingue "executado e aprovado" de "ignorado por ambiente" e **quais alegações são permitidas e proibidas** (por exemplo, não afirmar validação em navegador real, de layout, de acessibilidade ou de desempenho se o nível do teste não os prova). Diga também o que o cenário não prova (por exemplo, o provedor real, a composição de produção e a latência).
- **Prioridade ao ferramental existente.** Se a recomendação exigir dependência nova, navegador ou configuração que não existe, registre como **pré-requisito separado**, com a justificativa, e indique a alternativa sem ele e o que ela deixaria de provar.
- Registre achados de backend, de front-end e de documentação (divergências entre contrato, código, interface e testes; estados não tratados; riscos) em seção própria, sem corrigi-los.
- Indique a divisão de trabalho. **Leia o contrato de escopo e o teste de adequação de cada skill inventariada em `.agents/skills` e confirme, com evidência, se esta fatia é elegível a alguma delas**; se nenhuma cobrir (por exemplo por ser teste de ponta a ponta, não funcional ou que cruza front-end e backend), registre como lacuna de processo, recomende como prosseguir e indique o que o usuário precisaria autorizar explicitamente. Especifique nomes de arquivos, ambientes e comandos, para o executor não precisar inventá-los. Diga também se o resultado precisa de um registro em documento (por exemplo em `docs/testes/evidencias/`) ou se basta o texto do PR, e recomende o mínimo, de acordo com os precedentes do projeto.
- **Alterações temporárias de ambiente.** Registre que, para executar o cenário, o executor poderá aplicar alterações temporárias em definições Nix (`nix/*`, `flake.nix`, `flake.lock`) e nos manifestos de dependências do front-end (manifesto e lockfile) e, se o cenário exigir banco migrado e o grafo do Alembic estiver com revisões duplicadas ou múltiplas heads, uma linearização temporária das migrations (somente identificadores e arestas, sem alterar DDL, com verificação de ausência de ciclo e de uma única head sem warnings). Todas devem ser revertidas por `git restore` com caminhos explícitos (nunca `git restore .`) ao final, com os diffs completos copiados para o resumo, e `git status --short` não pode listar nenhum desses caminhos. Se já houver mudanças do usuário neles, a execução não deve restaurá-las: deve parar e informar. Artefatos gerados pela execução (relatórios, capturas, vídeos, caches, dependências instaladas, navegadores baixados) não devem entrar no commit: verifique o `.gitignore` e registre o que faltar. Recomende executar primeiro no estado original, para registrar bloqueios, e depois sob o experimento temporário, deixando claro que o segundo prova os componentes sob o ambiente temporário e não o ambiente permanente.
- Defina o roteamento do artefato de análise (pasta em `prompts/`) conforme a organização existente, e justifique, pois o tema cruza backend e front-end.
- Registre na validação os comandos **reais** de cada camada, descobertos por inspeção e executados no ambiente Nix correspondente: testes, lint, tipos e formatação do front-end; testes e lint do backend; e os gates do `.github/workflows/ci.yml` aplicáveis, com o baseline observado, para a execução futura não gerar regressão nem erro novo (comparação por identidade de teste e de diagnóstico, não só por total).
- Não implemente nada.
```
