---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: pending
created_at: "2026-10-31T12:48:20-03:00"
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
    - path: src/backend/infrastructure/exportacao/renderizador_pdf.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: available
    - path: src/backend/application/documento_renderizado.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: available
    - path: src/backend/application/exportacao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: available
    - path: src/backend/api/exportacao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "rotas, handler e composição"
      content_state: working-tree
      revision: "working-tree based on d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: available
    - path: src/backend/tests/test_infrastructure_renderizador_pdf.py
      relationship: primary
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: available
    - path: src/backend/tests/test_integracao_validacao_pdf_legibilidade.py
      relationship: primary
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/frontend, prompts/requisitos, prompts/revisao, prompts/ambientes, prompts/templates]
  confidence: high
  rationale: "O gerador e a fronteira real de teste estão no backend; frontend e ambiente delimitam a prova e são contexto ou handoffs."
classification:
  sphere: engineering
  concerns: [reliability, implementation, delivery]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: high
  reversibility: easy
  risk: medium
---

# Análise de decisão — Regressão de corte e sobreposição no PDF

## Solicitação original

A solicitação integral está preservada no Apêndice A. O título fornecido é “Criar teste de regressão para ausência de corte ou sobreposição em PDF”. A última instrução é “Não implemente nada”; o resultado desta atividade é exclusivamente esta análise, e o teste executável é o resultado da atividade futura.

## Informações complementares

Análise nova, mode initial, conforme solicitação expressa. A análise de 26/10 encontrada no repositório é evidência de outro trabalho, não uma versão anterior desta linhagem. A repetição da solicitação após interrupção não mudou seu conteúdo nem constitui revisão. Nenhuma descrição ou critério de aceite do card foi fornecido. Não houve acesso ao GitHub nem consulta externa; os comandos Nix desta análise usaram --offline.

## Mudanças desde a versão anterior

Nenhum identificado — análise inicial. A investigação foi retomada após interrupção sem reiniciar os baselines já concluídos.

## Artefatos analisados

Todos os caminhos relativos nesta seção são da árvore de trabalho inicialmente limpa, baseada em HEAD d45115dc5d9fd75f336cc86281b687f49e3e0ffc, branch test-regressao-sobreposicao-pdf. A inspeção final anterior à escrita confirmou o mesmo HEAD e git status --short vazio. “Recortes de busca” significa apenas linhas retornadas e seu contexto; não significa leitura integral.

| Caminho | Relação | Representação / função / formato | Recorte | Estado/revisão |
|---|---|---|---|---|
| src/backend/infrastructure/exportacao/renderizador_pdf.py | primary | source-code / production / Python | integral; diff de criação e ausência no pai | working-tree; commit 84e3a5b e pai |
| src/backend/infrastructure/exportacao/renderizador_docx.py | supporting | source-code / production / Python | integral; criação e ausência no pai | working-tree; commit 4ad3416 e pai |
| src/backend/infrastructure/exportacao/__init__.py | supporting | source-code / production / Python | antes/depois dos dois commits | commit |
| src/backend/application/documento_renderizado.py | primary | source-code / production / Python | integral atual; pai de 4ad3416; diff da porta | working-tree; commit |
| src/backend/application/__init__.py | supporting | source-code / production / Python | imports e __all__ alterados em 4ad3416 | commit, diff |
| src/backend/application/exportacao_curriculo.py | primary | source-code / production / Python | integral | working-tree |
| src/backend/api/exportacao_curriculo.py | primary | source-code / production / Python | rotas, handler e registro | working-tree |
| src/backend/api/factory.py | supporting | source-code / production / Python | parâmetros 244–246 e registro 412–415 | working-tree |
| src/backend/main.py | supporting | source-code / production / Python | integral | working-tree |
| src/backend/domain/modelo_curriculo.py | supporting | source-code / schema-contract / Python | integral | working-tree |
| src/backend/tests/test_infrastructure_renderizador_pdf.py | primary | source-code / test / Python | integral atual e commit; ausência no pai | working-tree; 84e3a5b |
| src/backend/tests/test_infrastructure_renderizador_docx.py | supporting | source-code / test / Python | integral por recortes complementares; ausência no pai | working-tree; 4ad3416 |
| src/backend/tests/test_integracao_validacao_pdf_legibilidade.py | primary | source-code / test / Python | integral | working-tree |
| src/backend/tests/test_api_exportacao_curriculo_pdf.py | supporting | source-code / test / Python | integral | working-tree |
| src/backend/tests/test_api_exportacao_curriculo.py | supporting | source-code / test / Python | stubs, harness ASGI e declarações dos testes | working-tree |
| src/backend/tests/test_application_exportacao_curriculo.py | supporting | source-code / test / Python | declarações de doubles e testes | working-tree |
| src/backend/tests/test_application_documento_renderizado.py | supporting | source-code / test / Python | declarações de cenários | working-tree |
| src/backend/tests/test_fixture_exportacao_curriculo.py | supporting | source-code / test / Python | declarações de cenários | working-tree |
| src/backend/tests/fixtures/curriculo_exportacao.py | supporting | source-code / data-fixture / Python | integral | working-tree |
| src/backend/tests/fixtures/massa_teste_curriculos.py | context | source-code / data-fixture / Python | cabeçalho, origem JSON e declarações | working-tree |
| src/backend/tests/fixtures/associacoes_candidatura_integracao.py | context | source-code / test / Python | import opcional e verificação do grafo | working-tree |
| demais oito módulos de fixtures discriminados no inventário abaixo, incluindo __init__.py | context | source-code / data-fixture / Python | nomes; classes e funções quando presentes; não implementação integral | working-tree, selected-section ou metadata-only |
| src/frontend/app/App.tsx | supporting | source-code / production / TSX | integral | working-tree |
| src/frontend/app/jornada-selecao-previa-exportacao.e2e.test.tsx | supporting | source-code / test / TSX | integral | working-tree |
| src/frontend/app/jornada-curriculo.e2e.test.tsx | context | source-code / test / TSX | declarações de harness e seus usos | working-tree |
| src/frontend/app/busca-vagas.integracao.test.tsx | context | source-code / test / TSX | imports e declarações de verificadores | working-tree |
| src/frontend/app/test/fixtures/busca-vagas.ts | context | source-code / data-fixture / TS | declarações de fábricas | working-tree |
| src/frontend/app/test/setup.ts | supporting | source-code / configuration / TS | integral | working-tree |
| src/frontend/pages/validacao-curriculo/ui/PaginaValidacaoCurriculo.tsx | supporting | source-code / production / TSX | props e repasse do callback PDF | working-tree |
| src/frontend/pages/visualizar-curriculo/ui/PaginaVisualizacaoCurriculo.tsx | context | source-code / production / TSX | declarações encontradas por busca | working-tree |
| src/frontend/pages/visualizar-curriculo/ui/PaginaVisualizacaoCurriculo.css | supporting | stylesheet / production / CSS | media print | working-tree |
| src/frontend/features/visualizar-curriculo/ui/ModeloClassico.css | supporting | stylesheet / production / CSS | media print | working-tree |
| src/frontend/features/visualizar-curriculo/ui/ModeloCompacto.css | supporting | stylesheet / production / CSS | integral | working-tree |
| src/frontend/features/visualizar-curriculo/ui/ModeloAcademico.css, ModeloAtsSimples.css, ModeloCriativo.css, ModeloModerno.css, ModeloPrimeiroEmprego.css | context | stylesheet / production / CSS | linhas de break-inside e media print, descobertas por busca; cada nome relativo ao mesmo diretório | working-tree |
| src/frontend/package.json | supporting | structured-data / build / JSON | integral | working-tree |
| src/frontend/package-lock.json | supporting | structured-data / build / JSON | busca de leitores PDF e browser; peers opcionais Vitest | working-tree |
| src/frontend/vite.config.ts | supporting | source-code / configuration / TS | integral | working-tree |
| src/frontend/tsconfig.json, tsconfig.app.json, tsconfig.node.json | supporting | structured-data / configuration / JSONC | integral, cada nome sob src/frontend | working-tree |
| src/frontend/eslint.config.js | supporting | source-code / configuration / JS | integral | working-tree |
| flake.nix, flake.lock | supporting | source-code e structured-data / build / Nix e JSON | integral | working-tree |
| nix/backend-python-packages.nix | supporting | source-code / build / Nix | integral atual e pais/diffs dos commits | working-tree; commit |
| nix/backend.nix, nix/frontend.nix, nix/tests.nix, nix/quality.nix | supporting | source-code / build / Nix | integral | working-tree |
| .github/workflows/ci.yml | supporting | structured-data / configuration / YAML | integral | working-tree |
| ruff.toml, .gitignore, src/frontend/.gitignore | context | structured-data ou prose / configuration / TOML e texto | integral | working-tree |
| AGENTS.md, src/backend/AGENTS.md, src/frontend/AGENTS.md | context | prose / prompt-instruction / Markdown | integral | working-tree |
| docs/configuracao-ambiente.md | context | prose / documentation / Markdown | integral | working-tree |
| docs/exportacao-pdf-docx.md, docs/modelos_curriculo.md, docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md | supporting | prose / documentation / Markdown | integral | working-tree |
| docs/requisitos_funcionais.md, docs/requisitos_nao_funcionais.md, docs/matriz_testes.md, docs/matriz_rastreabilidade.md | supporting | prose / documentation / Markdown | RF09, RNF07, CT-RF09 e resultados de busca | working-tree |
| docs/manual-estudante.md, docs/mapeamento_jornadas.md, docs/compatibilidade-responsividade.md | context | prose / documentation / Markdown | resultados de busca PDF/exportação e sobreposição | working-tree |
| docs/acessibilidade.md, docs/previa-curriculo.md | context | prose / documentation / Markdown | resultados de busca; definição do limite da prévia | working-tree |
| docs/wireframes/09-exportacao.md, docs/Arquitetura/ADR-005-catalogo-inicial-modelos-curriculo.md | supporting | prose / documentation / Markdown | integral | working-tree |
| docs/testes/evidencias/f5-12-legibilidade-tela-larga.md, docs/testes/evidencias/f11-11-responsividade-previa.md | context | prose / documentation / Markdown | recortes devolvidos pela busca; nenhuma regra transferida para PDF | working-tree |
| prompts/README.md | context | prose / documentation / Markdown | integral | working-tree |
| prompts/backend/20261026-082930-validacao-pdf-paginacao-v001.md | supporting | prose / documentation / Markdown | linhas 1–150 e resultados de busca de oráculos/alegações | working-tree |
| prompts/frontend/20261024-181303-cenario-busca-vagas-tres-desfechos-v001.md e demais prompts encontrados por busca | context | prose / documentation / Markdown | apenas linhas retornadas; inventário de resultados abaixo, não revalidação das análises | working-tree |
| .agents/skills/*/SKILL.md e referências discriminadas na divisão de trabalho | context | prose / prompt-instruction / Markdown | contratos de escopo e fit-check; referências v4 requeridas | working-tree |
| histórico Git dos caminhos discriminados abaixo | supporting | structured-data e source-code / documentation e production / Git | metadados, diffs, pais, merges e histórico por caminho | commit |
| /tmp/pdf-baseline-frontend-tests.log, /tmp/pdf-baseline-frontend-lint.log, /tmp/pdf-baseline-frontend-check.log, /tmp/pdf-baseline-frontend-format:check.log, /tmp/pdf-baseline-ruff.log | supporting | generated / generated-output / texto | resultados dos comandos desta atividade | external, execução local |
| /nix/store/5zhcznw11g5hdccykibviivms4wcqpqs-python3-3.14.7-env/lib/python3.14/site-packages/pypdf/_page.py | supporting | source-code / production / Python | assinatura e docstring de extract_text, linhas 2170–2250 | external, pypdf 6.18.1 |
| mesmo prefixo site-packages/reportlab/pdfbase/_fontdata.py e pdfmetrics.py | supporting | source-code / production / Python | métricas Helvetica e getAscentDescent por introspecção | external, ReportLab 5.0.1 |
| mesmo prefixo site-packages/reportlab/platypus/frames.py | supporting | source-code / production / Python | assinatura Frame por introspecção: padding padrão 6 pt | external, ReportLab 5.0.1 |

### Limites da evidência dos artefatos

As buscas amplas tiveram saídas extensas; não se alega leitura integral de todos os resultados. As conclusões dependem dos recortes específicos identificados. Não se leu o texto remoto de cards ou PRs. Não se abriu leitor visual nem se fez experimento geométrico novo. Os PDFs foram gerados somente pelas suítes existentes. Versões observadas são as deste Nix store, não uma promessa sobre versões futuras. Não se avaliou o grafo inteiro de migrations: a recomendação não depende de banco.

## Problema enriquecido

### Resultado desejado

Definir uma suíte executável que gere o PDF real, confronte conteúdo esperado e posições por página, e demonstre que o mesmo detector aprova um controle válido e rejeita defeitos deliberados. Vincular a regressão às duas correções somente quando forem identificadas correções reais de PDF. O título e RNF07 não bastam para inventar dois defeitos históricos.

### Atores e interesses

Estudante: preservar conteúdo do currículo; engenharia: impedir regressões detectáveis; produto/design: definir o que é corte e sobreposição aceitável; executor/revisor: distinguir prova automatizada, caracterização e alegação visual.

### (a) Fatos encontrados — caminhos e trechos

#### Estado e história local

As consultas git show --format=fuller --stat, git show <hash> --, git show <hash>:<caminho>, git show <hash>^:<caminho> e git merge-base --is-ancestor foram realizadas sem mudar branch. Os dois testes de ancestralidade retornaram 0. Nenhum hash foi ausente ou ambíguo.

| Commit | Metadados e mensagem | Arquivos e antes/depois | Natureza demonstrada |
|---|---|---|---|
| 84e3a5b041f318934f8249182dcd30dd25b3830d | Autor e committer mmagc; 2026-10-23 22:29:55 -03:00; “feat(backend): renderização PDF do currículo a partir do DTO #230” | nix/backend-python-packages.nix: acrescenta reportlab e pypdf; infrastructure/exportacao/__init__.py: remove “futuramente”; cria renderizador_pdf.py (197 linhas) e test_infrastructure_renderizador_pdf.py (292 linhas). Os dois arquivos novos não existem no pai, confirmado pelo erro explícito de git show. | Introduz geração PDF onde não havia este renderizador. Cria Paragraph, margens, KeepTogether, quebra automática e modo invariante; não há código PDF anterior com corte/sobreposição sendo corrigido. Não demonstra um defeito histórico de corte nem um de sobreposição. |
| 4ad34167cfec4a4e08da298879213382cbf3163b | Autor e committer mmagc; 2026-10-22 22:08:40 -03:00; “feat(backend): renderização DOCX do currículo a partir do DTO #231” | nix/backend-python-packages.nix: acrescenta python-docx; application/__init__.py: reexporta a porta; application/documento_renderizado.py: importa Protocol e acrescenta RenderizadorDocumentoCurriculo; cria infrastructure/exportacao/__init__.py, renderizador_docx.py (145 linhas) e test_infrastructure_renderizador_docx.py (231 linhas). Arquivos novos ausentes no pai. | Introduz DOCX e porta comum DTO → bytes. keep_with_next=True é regra DOCX para o título do bloco e seus destaques. Não modifica geração PDF e não constitui correção de corte/sobreposição em PDF. |

Diff relevante de 84e3a5b: SimpleDocTemplate(... pagesize=A4, leftMargin=margem, ... invariant=1 if self._invariante else 0); história recebe KeepTogether([Paragraph(título da seção), *primeiro]) e KeepTogether(bloco) para os demais. _texto usa encode("cp1252", "replace") e escape. Isso fundamenta casos de caracterização de quebra e conteúdo; não fundamenta a existência de um bug anterior.

Diff relevante de 4ad3416: declara class RenderizadorDocumentoCurriculo(Protocol), renderizar(documento) -> bytes; DOCX configura Calibri e margens, e escreve parágrafos com keep_with_next. A causa de uma falha PDF anterior é indeterminável porque esse diff não contém tal falha. Portanto, não é correto classificá-los como duas correções do mesmo defeito nem de defeitos distintos de PDF: são duas capacidades distintas, uma delas de outro formato.

Referências de issue são o texto #230 e #231 das mensagens, sem comprovação remota do vínculo ao card atual. PRs foram identificados por merges locais e seus pais: 9c45efdbdc89012709a7938fd1ba62b43a78d4bb, “Merge pull request #576 ... task230”, tem 84e3a5b como segundo pai; d60da824b9bab9cdaa17a042af826ea85318216a, “Merge pull request #574 ... task231”, tem 4ad3416 como segundo pai. Não se equiparou card a PR.

git log -- src/backend/infrastructure/exportacao e pelo arquivo renderizador_pdf.py mostra sua introdução; git log --all --ancestry-path 84e3a5b..HEAD -- <renderizador_pdf.py> não retornou alteração posterior. git diff 84e3a5b HEAD -- <renderizador_pdf.py> <test_infrastructure_renderizador_pdf.py> está vazio. O mesmo vale para renderizador_docx.py e seu teste em relação a 4ad3416.

Trabalhos posteriores encontrados por caminho/mensagem, sem supor correções: 55b7263 adiciona download DOCX; 05d992f adiciona download PDF; 4cb315424dd32891cf8335c10f3fc6eff97c5603, autor Gustavo Minoru Haga, 2026-10-26 08:33:26 -03:00, “test(backend): validar pdf gerado contra roteiro de legibilidade e paginacao (#410)”, acrescenta a suíte de auditoria; merge 50440bf menciona PR #601. Há também 9f9118e, “Create guia-exportacao-pdf-docx.md”, encontrado na busca por mensagem, cujo conteúdo não foi usado como prova. No catálogo, 37e5daf e merge fef3fdf/#610 ampliam os modelos; no frontend, e7c6d86 trata tela larga, ffe0c65 e 8788827 tratam responsividade. Esses históricos não tornam seus critérios regras de PDF.

#### Pipeline, formato e determinismo

1. application/documento_renderizado.py: “montar_documento_renderizado” percorre previa.curriculo.ordem_secoes, omite seções sem itens, converte os itens em BlocoDocumento e transporta titulo_versao, modelo=previa.curriculo.layout, cabeçalho e seções. Datas usam formatação explícita MM/AAAA; dados ausentes de contato retornam campos opcionais vazios. O DTO não recebe tamanho de página nem orientação.
2. application/exportacao_curriculo.py: ExportarCurriculo.executar chama o gerador de prévia, monta o DTO, chama a porta renderizar e devolve bytes, nome e MIME; exceções do renderizador e resultado vazio viram FalhaGeracaoArquivoCurriculo. A montagem do DTO fica antes do try do renderizador: não se presume que todo erro possível desse pipeline seja traduzido pela mesma exceção.
3. infrastructure/exportacao/renderizador_pdf.py: produção no servidor Python, ReportLab/Platypus, BytesIO, SimpleDocTemplate e Paragraph. Não converte HTML/CSS nem invoca navegador. A4 é fixo, retrato pelas dimensões de A4, sem seleção de outro papel/orientação nesse renderizador.
4. Mesmo arquivo: ESTILO_CLASSICO=(10.5 pt, espaço 6 pt, margem 2 cm); ESTILO_COMPACTO=(9 pt, espaço 3 pt, margem 1,5 cm). ESTILOS_POR_MODELO={"compacto": ...}; get(documento.modelo, ESTILO_CLASSICO) faz todo outro identificador cair no clássico. Corpo leading=base*1.3; nome=base*2, leading=base*2.4; seção=base*1.35, leading=base*1.7. Usa Helvetica, Helvetica-Bold e Helvetica-Oblique; não há carregamento de fonte de sistema ou registro de TTF nesse código. Não se comprovou incorporação de fontes inspecionando os objetos dos PDFs; fontes padrão não garantem aparência idêntica em todos os leitores.
5. Cabeçalho junta contatos preenchidos por “ | ”. Título, subtítulo, período e cada detalhe são Paragraph separados, com Spacer no final; agrupamento mantém o bloco inteiro “quando possível”, conforme docstring. Não há regra no código de que um bloco maior que uma página deva ser mantido indivisível. A paginação é delegada ao Platypus.
6. _texto substitui caracteres fora de cp1252 por “?” e escapa <, > e &. Isso é transformação atual de conteúdo, não corte geométrico. O teste de conteúdo deve distinguir essa transformação documentada de perda de texto.
7. Metadados: title=titulo_versao; author, subject, creator e keywords vazios; lang="pt-BR"; invariant desligado por padrão. O construtor diz “fixa datas e identificadores internos” quando invariante=True, e test_modo_invariante_gera_bytes_identicos compara duas gerações. Isso demonstra repetibilidade nessa condição, não invariância byte a byte entre versões de bibliotecas.
8. api/exportacao_curriculo.py: GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/pdf; resposta application/pdf, Content-Disposition e cabeçalhos privados. Sem executor, handler retorna 503; sem principal UUID, 401; versão ausente/alheia, 404; FalhaGeracaoArquivoCurriculo, 500 genérico. O middleware pode recusar antes do handler.
9. api/factory.py recebe exportar_curriculo_pdf=None e registra a rota. main.py chama create_app apenas com autenticador indisponível, readiness e lifespan: não injeta gerador/exportador. A aplicação que sobe não oferece uma exportação real autenticada pela composição atual. Em teste, pode-se compor explicitamente o executor real sem banco.
10. frontend/app/App.tsx tem navegação local para início, acesso e etapas de cadastro/validação; não fornece cliente PDF real. PaginaValidacaoCurriculo aceita onExportarPdf opcional e o repassa. A busca por exportacao/pdf, jsPDF, html2pdf, window.print e pdfjs em src/frontend não encontrou integração de geração/download; o único Blob PDF da jornada é um double com oito bytes “%PDF-1.4”.
11. Há CSS de impressão: ModeloClassico.css tem @media print e break-inside: avoid; PaginaVisualizacaoCurriculo.css oculta seu cabeçalho ao imprimir; outros modelos têm regras próprias. Nada no renderizador ReportLab lê essas folhas. Testar essas regras ou o DOM não prova o PDF deste pipeline.

#### Busca documental e resultados negativos

Consulta realizada: rg -i -l -- <termo> docs prompts, antes da criação desta análise. Contagens são arquivos com ocorrência, sem distinguir relevância; “corte” também encontra a palavra “recorte”. A busca ampla não é prova de que todos os documentos encontrados definem contratos.

| Termo literal | Arquivos retornados | Evidência pertinente examinada |
|---|---:|---|
| PDF | 31 | exportacao-pdf-docx; requisitos; evidência F11.12; prompts backend de PDF |
| exportar | 27 | RF09, CT-RF09, mapeamento_jornadas |
| exportação | 49 | matrizes, manual, wireframe 09 |
| impressão | 3 | resultados documentais sem limiar geométrico novo de PDF |
| margem | 3 | evidência F11.12 e análises de layout |
| página | 27 | evidência F11.12, análises e documentos de interface |
| corte | 108 | RNF07; muitos resultados apenas de “recorte” |
| sobreposição | 12 | RNF07, evidências de PDF e de tela, sem tolerância operacional validada |
| overflow | 7 | sobretudo prévia e responsividade; não transferido para PDF |
| quebra de página | 2 | análise PDF e evidência F11.12 |

Busca conjunta CropBox|TrimBox|tolerância.*pdf|pdf.*tolerância|interseção.*pdf em docs e prompts: nenhum resultado. Nenhuma definição formal de interseção de caixas ou tolerância de corte foi localizada nesses recortes.

A busca PDF em prompts encontrou os seguintes arquivos, além dos recortes de outros temas retornados pela busca ampla:
- backend/20261007-190814-selecao-itens-versao-curriculo-v001.md;
- frontend/20261007-081300-cenario-e2e-preenchimento-curriculo-v001.md;
- frontend/20261024-181303-cenario-busca-vagas-tres-desfechos-v001.md;
- backend/20261019-082400-integracao-crud-informacoes-complementares-v001.md;
- backend/20261008-183601-previa-versao-curriculo-v001.md;
- backend/20261025-100000-rota-exportacao-pdf-v001.md;
- backend/20261006-215500-fixture-teste-exportacao-curriculo-v001.md;
- backend/20261026-082930-validacao-pdf-paginacao-v001.md;
- backend/20261019-110000-download-documento-complementar-v001.md;
- backend/20261025-193758-integracao-selecao-ordenacao-curriculo-v001.md;
- backend/20261016-074803-armazenamento-documento-complementar-v001.md;
- backend/20261016-102843-exclusao-documento-complementar-v001.md;
- backend/20261026-082220-abertura-legibilidade-docx-v001.md.

São resultados de localização; somente os recortes declarados na tabela de artefatos foram usados como evidência de conteúdo. Não se adotaram premissas das análises existentes.

docs/requisitos_nao_funcionais.md, RNF07: “preservar o conteúdo, a organização e a legibilidade ... sem cortes ou sobreposições”. Isso define a intenção, não algoritmo, área útil ou tolerâncias. docs/matriz_testes.md, CT-RF09-01: arquivo com conteúdo e layout; CT-RF09-03: consistência com visualização; CT-RF09-05: falha controlada. Nenhum deles especifica limiar de interseção.

#### Inventário real de harnesses e fixtures

Backend: unittest.TestCase e IsolatedAsyncioTestCase; descoberta atual contém 1.126 identidades. A listagem src/backend/tests tem 172 arquivos, incluindo fixtures e suporte, não 172 suítes. A existência dos seguintes módulos foi confirmada, e suas declarações inventariadas:

| Arquivo sob src/backend/tests/fixtures | Harness/fábrica encontrado | Uso recomendado nesta fatia |
|---|---|---|
| __init__.py | inicializador | nenhum novo comportamento |
| curriculo_exportacao.py | CurriculoExportacaoFixture; obter_curriculo_exportacao_fixture | reutilizar IDs, entidades e datas estáveis, com adaptação sintética de campos |
| massa_teste_curriculos.py | CurriculoMassaTeste; obter_curriculos_massa_teste | alternativa existente; lê docs/massa_teste_curriculos.json; dispensável para a geometria específica |
| perfis_integracao.py | PerfilIntegracaoFake; popular_perfis_fake; ler_perfis_fake | não exigir banco para o teste PDF |
| curriculos_autenticados_integracao.py | BancoCurriculosAutenticadosIntegracao; ConsultasItensDouble; GeradorCurriculoDeterministico; RotaCurriculo | não reutilizar cadeia de migrations sem necessidade |
| credenciais_sessao.py | BancoCredenciaisSessao; ObservadorPerfil; RespostaCredenciais; token_sintetico | autenticação persistida fora do objetivo |
| ciclo_vida_perfil_autorizado.py | BancoCicloVidaPerfilAutorizado; GeradorUsuarioIdUUID4; RelogioUTC; ObservadorCasoPerfil | dispensável |
| formacoes_academicas_integracao.py | BancoFormacoesAcademicasIntegracao; GeradorFormacaoSequencial; RelogioExclusaoFixo | dispensável |
| selecao_ordenacao_curriculo.py | PreparadorBanco; BancoSelecaoOrdenacao; ConsultasTipadasDouble; construir_item | dispensável |
| associacoes_candidatura_integracao.py | BancoAssociacoes; OperacaoObservada; verificar_grafo | dispensável |
| busca_vagas_integracao.py | TransporteVagasRegistrado; AutenticadorVagasFake; PortaVagasCanonicaFake; criar_app_busca_vagas | outro recurso; não copiar regras para PDF |

Harnesses PDF/HTTP concretamente encontrados: _documento_renderizado e _texto_do_pdf nos testes de renderizador; AutenticadorSessaoStub, GeradorPreviaStub, _baixar e _app nos testes de rota; AutenticadorSessaoIntegracaoPdfStub, GeradorPreviaPdfIntegracaoStub, _criar_aplicacao_teste_pdf e _executar_requisicao_get_pdf em test_integracao_validacao_pdf_legibilidade.py. São suporte local de módulos existentes, vários nomes privados, não uma API pública geral de fixtures. Reaproveitar a fábrica pública de dados; não importar helper privado de outra suíte sem explicitar a dependência. Não refatorar os testes existentes só para compartilhá-los.

Frontend: 59 arquivos .test.ts/.test.tsx, confirmados pelo inventário e baseline; Vitest/jsdom com setup jest-dom, Testing Library e userEvent. Há JornadaCurriculoHarness em app/jornada-curriculo.e2e.test.tsx e JornadaCompletaHarness em app/jornada-selecao-previa-exportacao.e2e.test.tsx. Ambos são composições locais em DOM simulado, não navegador real integrado ao backend. A fixture central localizada é app/test/fixtures/busca-vagas.ts (respostaResultado, criarPendente); a jornada de exportação tem FORMACOES, EXPERIENCIAS e COMPETENCIAS inline e um ExportadorPdf simulado. Não foi localizada fixture binária PDF nem biblioteca de leitura PDF declarada no frontend. O peer opcional @vitest/browser-playwright do lock não prova instalação de Playwright ou browser configurado; vite.config.ts configura environment: "jsdom".

#### Cobertura existente e oráculos

| Artefato | O que as asserções verificam | Limite |
|---|---|---|
| test_infrastructure_renderizador_pdf.py, 11 métodos | validade, cabeçalho, ordem de títulos, textos mínimos, títulos do DOCX no PDF, igualdade textual clássico/compacto, metadados, escaping/cp1252, 40 blocos em várias páginas, bytes invariantes e documento sem seções | extrai texto e procura títulos; o caso longo não compara integralmente detalhes nem coordenadas |
| test_integracao_validacao_pdf_legibilidade.py, 5 métodos | rota ASGI com executor real e prévia/sessão stub; MediaBox A4; texto da primeira página; fixture extensa com exatamente duas páginas e Idiomas na segunda; igualdade textual dos modelos; privacidade | não calcula caixas de texto, corte ou interseções. Comparar ESTILO_CLASSICO.margem_cm à constante 2.0 não mede a margem no PDF |
| test_api_exportacao_curriculo_pdf.py | MIME, nome, bytes legíveis, sessão/propriedade, erros, independência DOCX/PDF e OpenAPI | não mede layout; rota criada em teste não prova main.py |
| test_application_exportacao_curriculo.py | nome/MIME e coordenação com doubles; recusa e falha controlada | sem renderização real |
| test_application_documento_renderizado.py | conteúdo, formatação, ordem/omissões, imutabilidade e determinismo do DTO | sem PDF |
| test_fixture_exportacao_curriculo.py | completude, referências, repetibilidade e serialização | valida massa, não layout |
| test_infrastructure_renderizador_docx.py | estrutura e conteúdo DOCX | não é oráculo geométrico de PDF |
| jornada-selecao-previa-exportacao.e2e.test.tsx | chamada do exportador double e mensagem de download | Blob de oito bytes não é PDF completo; não verifica arquivo/layout |
| testes de prévia móvel/tela larga | DOM/CSS dos modelos | renderização de navegador diferente do ReportLab |

Identidades dos cinco testes PDF integrados existentes:
- backend.tests.test_integracao_validacao_pdf_legibilidade.TesteIntegracaoValidacaoPdfLegibilidade.test_geometria_a4_e_abertura_do_pdf_com_leitor_externo;
- ...test_auditoria_de_legibilidade_por_pagina_modelo_classico;
- ...test_auditoria_de_paginacao_em_curriculo_extenso_sem_titulos_orfaos;
- ...test_modelo_compacto_mantem_mesmo_texto_com_alta_densidade_e_margens_menores;
- ...test_higienizacao_de_metadados_e_omissao_de_caminhos_privados.

#### Ferramental e ambientes observados

flake.lock fixa nixpkgs b1b875982b17dabde9b4a37f3e229e74913e6db3, x86_64-linux em flake.nix.

| Shell | Pacotes declarados | Observação |
|---|---|---|
| backend | Git e Python com FastAPI, uvicorn, SQLAlchemy, Alembic, psycopg, pydantic-settings, python-docx, reportlab e pypdf | Python observado 3.14.7; reportlab 5.0.1, pypdf 6.18.1, python-docx 1.2.0; aiosqlite ausente |
| frontend | Git, nodejs | Node do Nix 24.20.0; dependências node_modules existentes; Vitest 5.0.1, TypeScript 7.0.2, Vite 8.3.0, React 19.3.0, jsdom 30.1.0 |
| tests | mesmo Python do backend mais aiosqlite | leitores/geradores já disponíveis; apropriado para fronteira de renderização e API |
| quality | Git, Gitleaks, nodejs, Ruff; Python do backend mais Bandit, coverage, Radon | gate Ruff seleciona F e I em ruff.toml; não há gate de tipos Python declarado no workflow |

No shell tests, find_spec: fitz=False, pdfminer=False, pypdfium2=False, PIL=True. which: pdftotext, pdftoppm, mutool e gs ausentes. node apareceu herdado de /home/daniel/.nvm/... no PATH desse shell, não como pacote declarado: é proibido usá-lo para desenvolvimento deste projeto. Ruff também não está declarado em tests, e não foi usado ali. No frontend não há dependência declarada de leitor PDF; uma ocorrência “PDF” dentro de integrity do lock é apenas substring, não pacote.

docs/configuracao-ambiente.md prescreve npm ci e Nix. O CI instala dependências frontend com npm ci no shell quality. Nesta análise não houve instalação, atualização de lock, build ou acesso externo: Nix foi executado com --offline --no-write-lock-file, usando o store disponível. Offline não elimina necessidade de acesso local ao banco de locks do Nix: a primeira tentativa no sandbox falhou com “Read-only file system” em /nix/var/nix/db/big-lock; a repetição autorizada fora do sandbox concluiu. Não se deve contornar essa permissão com ferramentas globais.

### (b) Lacunas — opções, decisão necessária e insumo exato

| ID | O que os artefatos não fecham | Opções viáveis | Recomendação e responsável | Insumo para fechar |
|---|---|---|---|---|
| L01 | Quais são as duas correções históricas de corte/sobreposição em PDF | fornecer hashes corretos e reproduções; ou confirmar que o card é proteção preventiva do gerador introduzido | esclarecer vínculo antes de prometer proteção dos “dois comportamentos”; produto/engenharia | hashes completos ou patches, pré-condição, entrada que falhava e saída esperada para cada defeito; se os hashes atuais forem intencionais, autorização para reformular como caracterização/prevenção de PDF |
| L02 | Definição operacional de corte, área útil e elementos incluídos | só integridade textual; ou integridade + caixas dentro das margens; ou análise visual independente | adotar conteúdo + caixas nominais de texto nas margens implementadas, condicionado à aprovação de design/produto | aprovar margens 2/1,5 cm, inclusão de acentos/contatos/títulos e tratamento de clipping e ornamentos |
| L03 | Definição de sobreposição e tolerância visual | interseção de caixas de linhas; de palavras/glifos; imagem renderizada | palavras/runs com métricas e relatório de pares; evitar caixas de parágrafos multilinha; design aprova contrato, engenharia calibra cálculo | aprovar tolerância proposta de 0,5 pt por eixo; fornecer exemplos limítrofes aceitos/rejeitados; decidir se tocar caixas sem cobrir tinta é falha |
| L04 | Limites de comprimento/volume do PDF e comportamento para blocos maiores que uma página | caracterizar comprimentos finitos; ou produto fixar limites; ou rejeição explícita | caracterizar finitamente sem inventar máximo de produto; engenharia, produto para limites/rejeição | entradas reais mínimas das regressões; política para parágrafo/bloco maior que página, título vazio e documento totalmente vazio |
| L05 | Relação entre sete modelos atuais e apenas dois estilos PDF | testar fallback como caracterização; ou exigir aparência de cada modelo | caracterizar fallback existente, sem aceitar fidelidade visual silenciosamente; produto/design | decidir quais modelos têm contrato visual próprio no PDF e correspondência com prévia; não importar a ordem/layout do HTML |
| L06 | Coordenadas/cobertura do detector no PDF concreto | pypdf + métricas existentes; leitor independente adicional | começar com ferramentas existentes e controle de sensibilidade; engenharia | inspeção dos operadores realmente emitidos, validação das transformações e medições nos controles; aprovar escopo limitado de geometria nominal |
| L07 | Execução obrigatória desta nova suíte em CI no shell tests | comando manual dedicado; novo step/job; descoberta integrada em tests | comando explícito agora; handoff CI separado para proteção contínua; engenharia | autorização para alterar ci.yml em outra fatia, política de falha quando houver skips e responsável pelo gate |
| L08 | Composição funcional da exportação na aplicação que sobe | teste direto do renderizador/DTO; app criado em teste; E2E produtivo | chamada direta para geometria e aproveitar testes de rota existentes; engenharia | nenhuma mudança de produção para este teste; para alegar E2E, composição de sessão, prévia e exportador e cliente UI reais |
| L09 | Certificação visual, leitores, impressão, ATS e acessibilidade PDF | excluir alegações; ou campanha visual/manual específica | excluir da prova automática proposta; produto/design para campanha separada | leitores/versões/ambientes, requisitos de impressão/acessibilidade/ATS, fontes e critérios de aceite próprios |
| L10 | Experimento com dependência adicional se a geometria atual for insuficiente | não adicionar; PyMuPDF temporário; Poppler temporário | não adicionar no caminho principal; experimento opcional isolado; engenharia | aprovar objetivo adicional e limiares; confirmar pacote no nixpkgs fixado e store offline, sem instalar por conveniência |
| L11 | Registro documental mínimo desta nova regressão | PR com comandos e limites; evidência Markdown adicional | PR basta para esta fatia, incluindo sensibilidade; há precedente de evidência formal F11.12, mas não obrigação geral encontrada | produto/revisor confirmar se o card exige evidência formal; nesse caso autorizar um Markdown manual em docs/testes/evidencias/regressao-pdf-corte-sobreposicao.md, sem outputs binários |
| L12 | Procedimento de implementação com análise pending | revisão para proposed depois das decisões; autorização explícita delimitada fora da skill | revisar esta análise após L01–L03/L06; processo/engenharia | confirmação das decisões e invocação explícita da skill adequada com caminho/versão; não tratar esta análise pending como autorização de implementação |

Não se escolhe silenciosamente um critério de aceite na ausência desses insumos. As propostas seguintes são recomendações técnicas condicionais e critérios inferidos de proteção, não critérios originais do card.

### Hipóteses

A geometria nominal de texto do subconjunto ReportLab emitido pode ser medida com pypdf e métricas ReportLab. Precisa ser validada por controles que detectem transformações locais, não apenas pela presença de callbacks. A ausência de erro em extração textual não indica ausência de corte visual.

### Perguntas em aberto

L01–L03 e L06 impedem afirmar que a decisão fecha integralmente o card. L05 e L09 delimitam alegações; L07 determina proteção contínua. As perguntas e insumos exatos estão na tabela; não é necessário interromper a análise para responder às opções técnicas independentes.

### Escopo

Especificação de uma suíte de regressão do arquivo PDF gerado, dados sintéticos, oráculos, sensibilidade, execução e limitações. Resultado final desta atividade: um Markdown novo.

### Fora do escopo

Alterar produção, templates, estilos, bibliotecas, commits, CI, dependências permanentes, migrations ou outros recursos; instalar ferramentas; executar versões adulteradas ou criar cópia histórica nesta análise.

### Critérios de sucesso

Definidos pela solicitação: análise baseada em artefatos, sem implementação, com plano executável e lacunas explícitas. Inferidos de RNF07 e do renderizador: preservar todos os textos esperados representáveis; manter suas caixas nominais dentro da área contratada; não apresentar interseções indevidas de texto; aprovar controle positivo e rejeitar controles negativos independentes. Dependem de L01–L03/L06 para se tornarem aceite do teste.

## Restrições aplicáveis

AGENTS raiz: Nix obrigatório para ferramentas; Git fora de Nix; integração em tests; documentação de funções/classes explica o que, como e finalidade. Backend preserva Clean Architecture/DDD; frontend preserva FSD. A inspeção de arquivos AGENTS.md/AGENTS.override.md nas árvores relevantes encontrou somente raiz e os dois de src; nenhuma instrução local adicional em prompts/backend foi localizada. Skill decision-analysis-v4: somente novo Markdown. Não se usaram checkout, switch, stash, reset ou worktree. Os comandos de restore abaixo são exclusivamente plano futuro, não foram executados.

## Classificação comentada

engineering domina: desenho de teste e confiabilidade da saída, concerns reliability, implementation e delivery. scope component: gerador backend com contexto da composição e frontend. Risco medium: falso verde pode induzir confiança indevida; reversibilidade easy para o futuro código de teste. Incerteza high pela divergência dos hashes e ausência de oráculo aprovado.

## Decisão de roteamento

Subpastas imediatas realmente encontradas em prompts: backend, ambientes, frontend, templates, revisao e requisitos. prompts/README.md descreve backend para desenvolvimento/revisão do servidor; ambientes existe embora não esteja na lista desse README. Escolha prompts/backend, confiança alta: o PDF é produzido no servidor e os testes propostos exercitam o adaptador Python; a inspeção frontend delimita a prova e não torna a entrega um teste cliente. requisitos é candidata para L02/L03, revisao para auditoria, frontend para DOM, ambientes para experimento; nenhuma supera o propósito principal. Não cria categoria nova nem usa pasta templates por ser prompt.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | alta | conteúdo completo + controles negativos realmente rejeitados | evitar falso verde de mera geração |
| reliability | alta | execução repetível e diagnóstico por página/elemento | resultado estável e investigável |
| simplicity | média | usar ReportLab/pypdf existentes | não depender de instalação/binários |
| delivery-speed | média | compor gerador sem banco/servidor | evitar bloqueios alheios ao defeito |
| interoperability | baixa nesta fatia | alegações limitadas ao arquivo inspecionado | não certificar leitores sem medi-los |

## Alternativas consideradas

A — Estado atual: manter asserções de texto mínimo, MediaBox e paginação da fixture. Executável hoje, mas insuficiente para detectar texto desenhado fora da página ou dois textos no mesmo lugar.

B — Recomendada condicional: integridade textual completa + leitura por página e geometria nominal dos textos usando pypdf/ReportLab existentes, com controles sintéticos. Sem golden binário, sem banco e sem mudança de ambiente. Não se reduz a conferir coordenada de origem de um parágrafo.

C — Leitor independente/rasterização: PyMuPDF ou Poppler em experimento temporário; caixas de palavras ou imagens renderizadas. Reduz acoplamento às métricas do gerador, mas exige recurso ausente e não resolve sozinho definição de aceitação nem comprova regressões históricas não identificadas.

### O que cada técnica pode provar

| Técnica | O que comprova quando bem implementada | O que não comprova | Determinismo / requisitos / viabilidade |
|---|---|---|---|
| Texto esperado versus extraído | presença, multiplicidade e ordem contratada do conteúdo dos dados sintéticos; perda/duplicação textual | visibilidade, clipping, tinta ou posição; texto fora da página ainda pode ser extraído | pypdf existente; normalizar somente quebras/espaços controlados; marcadores únicos e comparação integral evitando só assertIn de títulos |
| Coordenadas por página + métricas | posições e limites nominais dos runs/glifos suportados; interseções dessas caixas | contornos reais da tinta, oclusão por objetos posteriores, legibilidade ou toda semântica PDF | pypdf visitor_* em modo plain e métricas existentes; exige validação das matrizes/estado; viável como engenharia futura, não demonstrado nesta análise |
| MediaBox/CropBox/conteúdo | papel, orientação, área visível e objetos/textos fora dos limites conforme o analisador | MediaBox A4 isolado não informa onde está o texto | pypdf existente; verificar herança de caixas, /Rotate, /UserUnit e interseção das caixas; não confundir margem de estilo com margem medida |
| Rasterizar e analisar pixels | tinta efetivamente produzida por um motor; pode denunciar conteúdo nas bordas e clipping visível | sem referência/oráculo de objeto, pixels não identificam texto perdido nem toda sobreposição; páginas “limpas” podem estar vazias | PIL sozinho não é rasterizador PDF comprovado; gs/pdftoppm/mutool/pypdfium2/fitz não disponíveis no shell tests; antialiasing/fontes/DPI/motor precisam fixação |
| Imagem de referência | igualdade/diferença visual com baseline aprovado no mesmo motor | baseline pode incorporar defeito; não prova conteúdo/semântica nem todos os leitores | motor ausente; precisa golden, DPI, versão, revisão visual e limiar; mais manutenção e ruído entre ambientes; não recomendado aqui |
| PyMuPDF para texto/caixas | posições fornecidas por motor independente, útil para confrontar o analisador de B | caixas não equivalem automaticamente a ausência de corte/oclusão; não certifica fidelidade visual | fitz ausente; pré-requisito separado em L10; alternativa sem ele é B com limite de métricas compartilhadas |

A API local pypdf/_page.py, extract_text, informa que visitor_text recebe texto, matriz de transformação, matriz de texto, fonte e tamanho. Em extraction_mode="layout" os visitors são ignorados. A docstring adverte: “Do not rely on the order of text coming out ...”. Logo, não usar layout+visitor nem presumir ordem/caixas exatas por fragmento. A geometria exige tratar transformações e linhas, não x=tm[4], y=tm[5] isolados.

## Perfil de pagamento comparativo

Escala ordinal, sem soma; melhora relativa ao problema, não uma medida cardinal.

| Dimensão | Prioridade | A | B | C | Confiança | Base |
|---|---|---|---|---|---|---|
| correctness | alta | -1 | +1 | +1 | média | A não mede geometria; B e C dependem do contrato e da sensibilidade |
| reliability | alta | 0 | +1 | 0 | média | B pinado e sem raster; C depende de novo motor |
| simplicity | média | +2 | +1 | -1 | alta | dependências já declaradas versus nova instalação |
| delivery-speed | média | +2 | +1 | -1 | média | volume finito de implementação; não houve benchmark do detector |
| interoperability | baixa | 0 | 0 | +1 | baixa | C adiciona apenas um motor, não todos os leitores |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado nesta linhagem.

### (c) Recomendações — decisão desta versão

Status pending. Recomenda-se B para a fatia de caracterização/prevenção do gerador atual, condicionada às decisões L01–L03 e à calibração L06. Não se recomenda declarar implementável a proteção de “duas correções” a partir dos hashes fornecidos. A menor investigação faltante é obter os dois casos/patches corretos e aprovar os limites nominais abaixo; não é instalar outra biblioteca por padrão.

### Impacto da revisão

Nenhum identificado — initial. A descoberta da suíte F11.12 e dos sete identificadores atuais altera o plano em relação a uma suposição de projeto vazio, não em relação a uma versão anterior desta análise.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | detectar perdas e interseções que A não mede | controles negativos propostos; validação ainda necessária |
| reliability | prioritized | resultado local, inspecionável e repetível | invariante e dependências existentes |
| simplicity | prioritized | não introduzir leitor/binário no caminho principal | Nix já declara reportlab/pypdf |
| interoperability | unresolved | nenhuma certificação entre leitores | L09 |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito proposto | Como a decisão atende |
|---|---|---|
| delivery-speed | sem servidor, banco, rede ou golden binário | DTO → renderizador real → leitor real em memória |
| correctness | todos os cenários obrigatórios executados; zero skip para alegar proteção | relatório distingue execução, ambiente e produto |

### Especificação executável proposta, após aprovação

Nível: integração na fronteira entre renderizador real ReportLab e leitor PDF real, atributo não funcional de integridade/diagramação. Sem E2E de aplicação. Gerar documento diretamente a partir de DocumentoCurriculoRenderizado construído de dados sintéticos e, para controle de conteúdo normal, de obter_curriculo_exportacao_fixture → PreviaVersaoCurriculo → montar_documento_renderizado. Os testes HTTP atuais já demonstram transporte com composição artificial; não repetir autenticação, MIME e OpenAPI no teste novo de geometria.

Estrutura futura:
- src/backend/tests/integracao_regressao_pdf_layout.py: unittest.TestCase, classe RegressaoPdfLayoutIntegracaoTestCase; cenários reais e controles sintéticos; nome sem prefixo test_ segue o precedente integracao_repositorio_associacao_curriculo_vaga.py para execução explícita no shell tests.
- src/backend/tests/fixtures/pdf_layout.py: fábricas de DTO sintético, conteúdo esperado independente do renderizador e analisador restrito do PDF. Nomes propostos: criar_documento_pdf_layout, extrair_geometria_pdf, auditar_pdf_layout e criar_pdf_controle_defeituoso. Não importar _texto de produção para construir o esperado: explicitar os casos de cp1252 e seu resultado.
- Nenhuma mudança frontend, produção, runner, manifesto ou Nix no plano B.
- Não criar arquivo binário de referência. Helpers/classes novos terão docstrings de responsabilidade, abordagem e finalidade e comentário de proveniência deste artefato/versão.

O módulo deliberadamente não entra na descoberta test*.py do job backend atual. Consequência: não roda automaticamente no CI hoje. A alternativa de nomeá-lo test_integracao_* o faria entrar no job backend, mas executaria integração fora do shell tests exigido. Recomenda-se comando dedicado e handoff posterior para CI, sem chamar de proteção contínua enquanto isso não existir. Não modificar a descoberta ou o workflow nesta fatia.

### Oráculos e tratamento geométrico

Proposta técnica de B, ainda não aceite definido:
1. Ler bytes com PdfReader(BytesIO(...)); todas as páginas com dimensões e orientação esperadas; avaliar MediaBox e CropBox efetiva. Não se contentar com página válida.
2. Obter texto completo com marcadores únicos por campo/bloco/detalhe, incluindo início e fim de textos longos. Comparar sequência normalizada e multiplicidades esperadas por cenário; para token sem espaço dividido em linhas, recompor somente as quebras conhecidas do token. Não remover pontuação/acentos nem transformar texto arbitrariamente para fazer o teste passar.
3. Recuperar posições de texto no modo plain com visitors de operandos/texto e, se necessário, ContentStream, identificando linha, fonte, tamanho, matriz de texto e CTM. Separar fragmentos multilinha; nunca atribuir uma única caixa a um parágrafo inteiro.
4. Para o subconjunto emitido, calcular avanços de texto com larguras de fonte e estado Tc/Tw/Tz/Ts, Tj/TJ, deslocamentos e leading; aplicar CTM e matriz de texto aos quatro cantos das caixas. Manter estado q/Q e cm e movimentos BT/ET/Tm/Td/TD/T*. Interpretar Encoding de fontes. Métricas getAscentDescent e stringWidth já pertencem ao ReportLab disponível. O subconjunto efetivamente necessário precisa ser confirmado em L06, antes de prometer um parser genérico.
5. Fontes, operadores, rotações, clipping, formas ou objetos inesperados que afetem a conclusão não devem ser silenciosamente descartados. Falhar com “oráculo não suporta ...” e encaminhar investigação; só ausência de dependência permite skip. Não presumir que bbox nominal representa a tinta real. Não construir um renderizador PDF completo no teste por improvisação.
6. Comparar caixas de palavras/runs não vazios da mesma página, preservando identidades e ordem de emissão; excluir espaços não pintados, não excluir pares apenas por pertencerem à mesma seção. Interseções detectadas reportam página, marcadores, caixas, fonte e profundidades por eixo. Usar caixas de linha apenas como filtro rápido; uma caixa de parágrafo é larga demais e gera falsos positivos.
7. Documentar a condição “sem clipping/oclusão inesperados no subconjunto validado”. Texto invisível, sobreposição por retângulos, imagem ou máscaras não é certificado apenas por métricas. Se esses objetos aparecerem, reabrir L06 em vez de aprovar o PDF.

### Área útil e limiares propostos

Unidade: pt, 72 pt por polegada, 1 cm = 72/2,54 pt conforme uso de cm do ReportLab. Valores abaixo são inferidos do código ou heurísticas propostas, não tolerâncias fornecidas pelo card.

| Medida | Valor proposto | Origem e justificativa | Risco e decisão |
|---|---|---|---|
| página | A4 = 595,27559055 × 841,88976378 pt; erro por dimensão ≤0,05 pt | A4 do código; erro técnico proposto para serialização decimal, alinhado à ordem de grandeza do teste existente places=1 | tolerância de engenharia; não permitir outro papel silenciosamente |
| área útil clássica | [56,69291339; 56,69291339; W−56,69291339; H−56,69291339] | margem 2 cm implementada | adoção como contrato depende de design; não inferir só da caixa da página |
| área útil compacta | [42,51968504; 42,51968504; W−42,51968504; H−42,51968504] | margem 1,5 cm implementada | idem |
| folga externa de caixa nominal | 0,5 pt em cada lado | heurística de arredondamento/métrica; não é uma nova margem de produção | design deve aprovar; pode deixar passar invasão ≤0,5 pt; testar 0,49/0,51 e casos grosseiros |
| sobreposição | reprovar quando profundidade em x >0,5 pt E profundidade em y >0,5 pt, entre caixas nominais não vazias | heurística evita contato/ruído minúsculo; sem percentual de área arbitrário | pode perder colisão pequena ou sinalizar caixas sem tinta sobreposta; precisa design e controles |
| integridade de conteúdo | zero marcadores ausentes/duplicados e zero diferença textual fora da normalização especificada | RNF07 e DTO; tolerância semântica zero para dados representáveis | engenharia; não converter ✓ em ausência aceitável: esperado explícito “?” na caracterização atual |
| paginação longa | >1 página, sem total fixo para massa gerada de 40 blocos | teste existente usa 40 blocos | engenharia; exatamente duas páginas é apenas caracterização da fixture F11.12, não regra universal |

Frame tem padding interno padrão de 6 pt por introspecção local, enquanto SimpleDocTemplate recebe margens. Não somar/subtrair 6 pt como requisito do produto: isso não é margem mínima documentada. Não derivar o esperado das próprias constantes lidas do renderizador a cada execução, pois o teste deixaria passar uma regressão de margem. Os valores aprovados devem ser explícitos no teste e comparados à saída. A tolerância deve ser calibrada nos controles com matrizes e acentos, não ampliada depois de um vermelho sem investigação.

### Cenários propostos

Todos exigem ambiente tests com ReportLab/pypdf, entradas em memória, gerador invariante, sem rede/banco. Passos comuns: construir DTO e manifesto esperado independente → gerar bytes com renderizador real → abrir e auditar páginas/conteúdo/caixas → asserções e diagnóstico. Para controles negativos, os bytes são sintéticos e o mesmo auditar_pdf_layout deve retornar a categoria de defeito esperada; o teste usa assertRaises/assertions específicas e termina aprovado quando o detector reprova. Não usar expectedFailure para ocultar defeito.

| ID / método futuro | Objetivo e pré-condição específica | Entradas | Passos / esperado | Fonte e origem | Camada / nível |
|---|---|---|---|---|---|
| P01 test_pdf_normal_respeita_area_e_preserva_conteudo | controle positivo; limites aprovados | fixture de exportação, nome/contatos substituídos por “Pessoa Sintética”, pessoa@example.invalid e URLs example.invalid; clássico e compacto | passos comuns; todo conteúdo e caixas aprovados; não exige uma página | fixture e renderizador; critério inferido de RNF07 | gerador + leitor / integration |
| P02 test_quarenta_blocos_preservam_todos_os_detalhes | estender cobertura de títulos para cada campo | 40 blocos, título B00...B39 e 30 tokens únicos por detalhe; dois estilos | >1 página; todos os tokens na ordem prevista e sem colisão/invasão | test_muitos_itens_quebram_em_varias_paginas_sem_perder_texto; conteúdo ampliado inferido | gerador + leitor / integration |
| P03 test_texto_longo_e_url_sao_preservados | caracterização da quebra de Paragraph; não é reprodução histórica comprovada | campo de detalhe e contato com token ASCII sem espaços de 512 e 2048 caracteres, com sentinelas distintas | passos comuns; recompor token dividido; auditar todas as linhas. Se houver falha atual, registrar achado; não corrigir nem rotular automaticamente defeito corrigido | Paragraph e _cabecalho implementados; comprimentos são escolha técnica inferida, L04 | gerador + leitor / integration |
| P04 test_bloco_maior_que_pagina_preserva_linhas | caracterização de KeepTogether quando não cabe | um bloco com 120 detalhes curtos e marcadores únicos; ambos estilos | passos comuns; >1 página e todos os detalhes; não exigir bloco indivisível | docstring “quando possível” e uso KeepTogether; volume inferido | gerador + leitor / integration |
| P05 test_campos_opcionais_e_acentos_sao_caracterizados | não transpor validação de formulário | contato opcional None, telefones=(), subtítulo/período None, seções=(); subcaso “Ação <REST> & ç” e “Nota ✓ ok” | campos ausentes não geram “None”; conteúdo representável integral; ✓ resulta em “?” no subcaso explícito; cabeçalho obrigatório sintético mantido | _cabecalho/_bloco/_texto e testes existentes; caracterização inferida | gerador + leitor / integration |
| P06 test_catalogo_pdf_caracteriza_fallback | cobrir entradas implementadas sem inventar sete layouts PDF | sete identificadores de ModeloCurriculo e legado padrao_fatec da fixture | medir estilo compacto somente no compacto; demais saída equivalente ao clássico em conteúdo/geometria; marcar fallback como caracterização, não fidelidade de modelo | enum atual e ESTILOS_POR_MODELO.get; inferido, L05 | gerador + leitor / integration |
| N01 test_detector_rejeita_texto_fora_da_area | sensibilidade para corte geométrico | PDF sintético A4 com dois textos distintos; um movido 10 pt além da margem aprovada e outro fora da MediaBox | conteúdo ainda extraível; auditor deve emitir fora_area com página/caixa. Par normal idêntico, exceto posição, deve passar | controle solicitado pelo usuário; valores técnicos inferidos | produtor sintético + leitor/detector / integration |
| N02 test_detector_rejeita_sobreposicao | sensibilidade para colisão | dois textos únicos desenhados na mesma posição; controles com separação vertical 20 pt; subcaso CTM traduzida/local | mesma auditoria acusa sobreposicao e identifica o par; controle separado passa; não deduplicar textos por coordenada | controle solicitado; sintético inferido | produtor sintético + leitor/detector / integration |
| N03 test_detector_rejeita_texto_ausente | sensibilidade semântica | documento esperado com “FIM-B03”, PDF sintético que omite só esse marcador | acusa conteudo_ausente mesmo com página válida e caixas boas; controle completo passa | RNF07 + controle solicitado; inferido | produtor sintético + leitor/detector / integration |
| N04 test_detector_valida_transformacoes_e_limites | validar o próprio instrumento | pares com q/Q e cm; negrito/itálico/acentos; casos 0,49/0,51 pt em cada eixo | classificações explícitas conforme limiares aprovados; operadores não suportados dão falha de oráculo, nunca verde | APIs locais pypdf/ReportLab; L03/L06, inferido | produtor sintético + leitor/detector / integration |
| R01 / R02 sem método definitivo | reproduzir cada correção histórica | indisponíveis nos artefatos fornecidos | aguardar L01; não inventar teste que alegue falhar nos pais dos hashes atuais | associação declarada pelo usuário diverge do Git | pendente |

P03/P04 não estabelecem limites máximos de produto. P05 não autoriza nome/e-mail ausentes em entidades; cobre somente campos opcionais realmente implementados. Não há cenário Letter, paisagem ou “todas as dimensões” porque o renderizador só implementa A4 fixo. Todos os critérios de resultado derivados para esta nova suíte são inferidos; os números atuais de estilo são fatos de implementação e não critérios originais do card.

### Controle de sensibilidade: opções e procedimento futuro

| Forma | Viabilidade local | O que demonstra / risco | Recomendação |
|---|---|---|---|
| pais de 84e3a5b e 4ad3416 | os renderizadores novos não existem nos respectivos pais | import falhar ou biblioteca ausente não demonstra regressão de layout | não usar como controle positivo de sensibilidade; documentar ausência |
| cópia histórica de correções reais ainda a identificar | viável com git archive, sem trocar árvore; depende L01 e compatibilidade do DTO | mesma entrada deve passar depois e reprovar antes na mesma categoria de corte/colisão; dependências atuais podem mascarar mudança de biblioteca | melhor evidência histórica depois de obter correções/fixtures |
| PDFs sintéticos deliberadamente defeituosos | ReportLab já disponível; sem instalação; não executado nesta análise | valida detector para defeito conhecido; não prova que um bug histórico existiu ou foi corrigido | obrigatório em B |
| adulterar geração em memória | unittest.mock.patch com escopo ou módulo carregado em processo descartável | retirar KeepTogether testa órfãos, não necessariamente corte/colisão; reduzir leading ou deslocar um draw pode provocar colisão | opcional, somente mutação que corresponda a defeito definido; restaurar por contexto, não monkeypatch global |
| alterar arquivo de produção no working tree | fora da restrição desta análise e desnecessário | risco de contaminar código e resultado | rejeitada |

Plano futuro para cópia histórica, sem executar agora: usar TemporaryDirectory(prefix="pdf-regressao-", dir="/tmp"); obter cada revisão correta com git archive --format=tar <hash> e extrair por subprocess/stdlib dentro do diretório temporário, sem checkout/switch/worktree. Validar caminhos do tar antes da extração. No shell Nix tests do projeto atual e com mesmo conjunto de dependências, executar subprocess com cwd e PYTHONPATH apontando somente para a cópia, para não importar módulos atuais por acidente. Importar módulo por caminho absoluto na cópia; registrar revisão e __file__ usado. Gerar PDF histórico com a mesma entrada ou adaptador de fixture explicitamente documentado; auditar com o detector atual, em processo distinto. Repetir no estado corrigido. ImportError, erro de DTO, LayoutError sem PDF ou falta de dependência são bloqueio de reprodução, não sucesso de sensibilidade de corte/colisão. TemporaryDirectory remove a cópia e PDFs em finally. Tempo não medido: orçar uma execução por par cenário/revisão e comparar com baseline PDF de 0,939 s para seis testes existentes, sem transformar isso em SLA.

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | teste verde com texto perdido ou encavalado | alta | estudante e engenharia |
| reliability | detector não sensível ao defeito real | alta | manutenção |
| simplicity | ambiente novo torna execução indisponível | média | CI e desenvolvimento |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | desenvolver/calibrar leitura geométrica restrita | delivery-speed | condicionado a controle de sensibilidade; se virar parser genérico, reavaliar C |
| simplicity | usar métricas também fornecidas pelo gerador | independência da prova | só com limitação explícita e controles independentes |
| reliability | adiar alegação de regressões históricas até L01 | fechamento imediato do card | necessário para não inventar prova |
| conformidade ao ambiente | módulo dedicado fora de discovery backend | execução automática em CI | custo visível até handoff L07 |

## Riscos e efeitos de segunda ordem

Pypdf pode extrair texto que não está visível. Caixas métricas de fontes não são contornos de glifos; negrito/itálico/acentos e overhang podem produzir falsa colisão ou falso negativo. Se os controles mostrarem isso, rever a representação geométrica ou experimentar leitor independente, não só aumentar tolerância. Compartilhar métricas com ReportLab cria possível erro comum. Novos objetos, fontes ou operadores devem tornar o oráculo inconclusivo/falho. Reutilizar um resultado “zero falhas” de docs como baseline visual perpetuaria alegações não demonstradas.

### Achados de backend, frontend e documentação, sem correções

| Área | Divergência/achado | Fonte mais confiável para a questão | Consequência |
|---|---|---|---|
| histórico | usuário chama hashes de duas correções; são introdução PDF e introdução DOCX | diff e pais locais, que mostram arquivos novos | L01 bloqueia alegação histórica |
| backend | geração existe, mas main.py não a compõe | main.py e parâmetros da factory | teste direto não certifica exportação disponível no produto que sobe |
| backend | catálogo tem sete identificadores; PDF só distingue compacto e fallback | enum e get do renderizador | não alegar layouts PDF específicos para os outros cinco |
| backend | proteção de KeepTogether “quando possível” não é prova de nunca haver órfão | código e docstring do renderizador | caso de bloco maior requer caracterização, não promessa universal |
| frontend | comentário da jornada diz que gerador real não existe; gerador agora existe no backend | renderizador atual versus comentário histórico | comentário está desatualizado quanto à existência, mas a simulação do teste continua real |
| frontend | há CSS de impressão e testes DOM | imports/config e pipeline ReportLab | sem elo de execução, não demonstram PDF |
| documentação | docs/exportacao-pdf-docx e manual dizem que não há gerador real integrado | código distingue existência do gerador de ausência de composição | parte “não existe gerador” envelheceu; ausência de integração ainda tem suporte |
| documentação | evidência F11.12 afirma “atende integralmente ... legibilidade” e “0 falhas” | asserções da suíte para a cobertura automatizada | não há medição de colisões, corte ou prova de auditoria visual reproduzível no recorte |
| documentação | análise de 26/10 afirma “nunca” e “qualquer leitor” e inexistência de pendência | implementação/tests atuais | exagero de alcance; não herdado nesta nova análise |
| documentação | ADR-005 tem título interno “ADR-004” e status Proposto | conteúdo literal do arquivo | ambiguidade documental, sem corrigi-la |
| CI | job chamado unitário descobre também módulos de integração test_integracao_* | comando discover e nomes atuais | não copiar esse desencontro para nova suíte; usar tests explícito |
| ambiente | suites integradas dependentes de aiosqlite ignoradas em backend | skip identities e probe do shell | zero falhas não significa toda integração executada |
| ambiente | shell tests herda Node global | which e nix/tests.nix | não usar binário global como solução para testes frontend |

Nenhum desses achados foi corrigido ou convertido em escopo adicional.

## Validação da decisão

### Baseline executado no estado original

Todos os comandos partiram da raiz. Flags comuns efetivamente usadas: nix develop .#<shell> --offline --no-write-lock-file --command. PYTHONDONTWRITEBYTECODE=1 foi usado no Python desta análise. Saídas frontend/Ruff foram registradas temporariamente em /tmp; a execução backend verbose foi capturada pela ferramenta, e o loader foi inventariado separadamente por identidade. Não houve comparação com outro HEAD nem código modificado: a comparação desta análise é contra a mesma árvore original; não se inventa resultado “depois da implementação”.

| Comando após --command | Shell | Resultado observado |
|---|---|---|
| env PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -v -s src/backend/tests -t src | backend | exit 0; 1.126 testes, 108,290 s; 84 skips; 0 failures/errors |
| npm --prefix src/frontend test -- --reporter=verbose | frontend | exit 0; 59 arquivos e 336 testes aprovados, 78,41 s; zero falhas/skips reportados |
| ruff check --output-format=concise src/backend | quality | exit 0; “All checks passed!”; zero diagnósticos |
| npm --prefix src/frontend run lint | frontend | exit 0; zero diagnósticos |
| npm --prefix src/frontend run check | frontend | exit 0; zero diagnósticos |
| npm --prefix src/frontend run format:check | frontend | exit 0; todos os arquivos encontrados formatados |
| env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest -v backend.tests.test_integracao_validacao_pdf_legibilidade backend.tests.integracao_repositorio_associacao_curriculo_vaga | tests | exit 0; seis testes aprovados, zero skips; 0,939 s |

A descoberta backend segue exatamente o comando do CI, com -v adicional. Ela é uma suíte mista, apesar do nome do job: executou também integrações existentes e ignorou algumas. A regra correta para testes integrados futuros permanece shell tests. A suíte frontend também contém harnesses integrados no mesmo npm test; o baseline global pedido foi executado no shell frontend conforme o componente, sem reclasificar esses harnesses como unitários. Não se tomou isso como precedente para executar nova integração fora de tests.

Identidades de diagnóstico: conjunto de erros de Ruff, ESLint, TypeScript e Prettier vazio. O baseline backend emitiu StarletteDeprecationWarning para HTTP_422_UNPROCESSABLE_ENTITY em test_api_cadastros_regressao.py:151 e :180 e avisos de duração de tasks asyncio; não são gates novos nem defeitos PDF corrigidos nesta atividade.

Comparação por identidade para execução futura: registrar conjunto ordenado de TestCase.id(), status e motivo de skip no backend e caminho + cadeia describe/it no frontend. Não aceitar só igualdade de contagens. Nesta árvore, SHA-256 de "\n".join(sorted(ids))+"\n":
- backend loader, 1.126 IDs: cf356054397768a2facaae1b98cb32bfbf176328abfeea6abfff23021cc1c2be;
- 84 IDs de skip estático, confirmados pelo resultado da suíte: 945e56ba4008718246f4771676c17b7fd198214570ee93d551b481b640971786;
- frontend, 336 linhas de caso aprovado (sem duração final), formato “arquivo > describe > it” extraído do reporter verbose: 533771e7aa52ebe424481f2aeb39e2dbd650135835b44f1df148be7409dc4535.

O hash verifica identidade do conjunto, não substitui o diff de IDs se houver mudança. Os logs em /tmp não são artefatos versionados nem persistência garantida. Na implementação futura, conservar o manifesto de baseline em diretório temporário e comparar identidade a identidade; para cada teste novo exigir status executado. Como somente este Markdown é entregue, não há alteração de identidade de teste nesta atividade.

Skips do backend por módulo, todos sob backend.tests, com quantidade e motivo observado:
| Módulo | Quantidade | Motivo |
|---|---:|---|
| test_integracao_associacao_candidatura_interesse | 12 | aiosqlite ausente |
| test_integracao_ciclo_vida_perfil_autorizado | 2 | aiosqlite ausente |
| test_integracao_contrato_credenciais_sessao | 13 | aiosqlite ausente |
| test_integracao_crud_formacao_academica | 19 | aiosqlite ausente |
| test_integracao_persistencia_sessao | 6 | aiosqlite ausente |
| test_integracao_recusa_curriculo_alheio | 11 | aiosqlite ausente |
| test_integracao_selecao_ordenacao_curriculo | 18 | aiosqlite ausente |
| test_integracao_composicao_credenciais_sessao.ComposicaoCredenciaisSessaoIntegracaoTestCase.test_C02_fluxo_autenticado_ignorado_por_produto | 1 | “produção não compõe login, criador, revogador nem autenticador persistido” |
| test_integracao_rejeicao_requisicoes_sem_credenciais_validas: test_sessao_expirada e test_sessao_revogada | 2 | “a aplicação ainda não compõe persistência de sessões” |

Os cinco IDs PDF integrados, discriminados na cobertura, executaram e passaram também no shell tests; não estão nesses skips. O sexto ID da execução explícita é backend.tests.integracao_repositorio_associacao_curriculo_vaga.ConsultaPaginadaAssociacaoIntegracaoTestCase.test_pagina_filtra_proprietario_antes_de_paginar_e_ordenar.

### Gates reais do CI e consequências

.github/workflows/ci.yml:
- backend-lint: nix develop .#quality --command ruff check --output-format=github src/backend. Executado com formato concise para diagnóstico local, mesmas regras/alvos; zero diagnósticos.
- backend-tests: nix develop .#backend --command python -m unittest discover -s src/backend/tests -t src. Baseline acima, mesmo alvo, -v adicional.
- backend-integration-tests: nix develop .#tests --command env PYTHONPATH=src python -m unittest backend.tests.integracao_repositorio_associacao_curriculo_vaga. Identidade executada acima no mesmo ambiente, junto da suíte PDF.
- frontend-quality: npm ci, lint, format:check, check, build, todos via shell quality. Baselines lint/tipos/formatação foram executados via frontend, que disponibiliza o mesmo pacote pkgs.nodejs; não se alega execução do job remoto inteiro. npm ci não foi executado por proibição de instalar; build não foi executado por limitar a atividade a leitura e baselines de testes/gates estáticos. Comando futuro real: nix develop .#quality --command npm --prefix src/frontend run build; gera dist e exige controle de artefatos.
- secrets-scan: nix develop .#quality --command gitleaks git --redact --no-banner --exit-code 1. Não executado: varredura global do histórico não é baseline de PDF nem gate de lint/tipos; continua gate do PR.
- Não há npm test no workflow atual. As 336 aprovações locais não são proteção automática frontend nesse workflow.
- A suíte F11.12 é descoberta pelo job backend atual, mas o relatório recomenda tests e ela foi executada nesse shell nesta atividade. Nova suíte dedicada não estará no CI sem handoff L07.

### Comandos futuros da fatia

    nix develop .#tests --offline --no-write-lock-file --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src TZ=UTC LC_ALL=C.UTF-8 python -m unittest -v backend.tests.integracao_regressao_pdf_layout
    nix develop .#quality --offline --no-write-lock-file --command ruff check src/backend/tests/integracao_regressao_pdf_layout.py src/backend/tests/fixtures/pdf_layout.py
    nix develop .#quality --offline --no-write-lock-file --command ruff format --check src/backend/tests/integracao_regressao_pdf_layout.py src/backend/tests/fixtures/pdf_layout.py

Ruff format --check é recomendação restrita aos arquivos novos, não gate atual global de formatação Python. Se a locale C.UTF-8 não estiver disponível, registrar e fixar outra locale disponível antes de medir; não depender silenciosamente da locale do host. Não foi necessário executar esse comando futuro para produzir esta análise.

Repetir os comandos de baseline aplicáveis após a implementação e comparar IDs/diagnósticos. Frontend não muda; se seu baseline for repetido, usar shell frontend; harnesses integrados futuros exigem ambiente tests apropriado, sem recorrer a Node global.

### Determinismo, isolamento e skips

Gerar bytes em BytesIO e renderizador invariante=True; dados, datas e UUID fixos; sem datetime.now/random/ordem de set; DTOs novos por teste. TZ=UTC e locale explícita no processo, rótulos pt-BR literais. Fontes padrão e métricas declaradas, sem buscar fontes do host/rede. Testar conteúdo/caixas, não hash binário entre máquinas. Comparação de bytes somente para a propriedade invariante já testada, no mesmo ambiente.

Quando precisar guardar PDFs/relatórios para diagnóstico ou cópia histórica: TemporaryDirectory em /tmp, limpeza em finally/context manager mesmo após falha; nenhuma saída sob src/docs. Não versionar imagens, PDFs, traces, caches ou dependências.

Import opcional de pypdf/reportlab deve ser protegido somente para ModuleNotFoundError cujo name corresponda exatamente à dependência ausente; unittest.SkipTest com motivo “ambiente: pypdf/reportlab ausente; executar nix develop .#tests ...”. Não capturar Exception ou erro de parsing como skip. Capability ausente de leitor opcional só ignora cenário opcional explicitamente nomeado. Se a suíte principal toda for ignorada, resultado é “não executado”, nunca “regressão protegida”. Falha de geometria, erro de leitura do PDF, fonte inesperada ou oráculo incompatível é falha/inconclusão a investigar, não indisponibilidade genérica do ambiente.

Alegações permitidas após B aprovado e controles executados: presença/multiplicidade dos textos sintéticos e ausência de invasão/interseção nas caixas nominais suportadas, para modelos/volumes/casos e versões medidos. Alegações proibidas: “sem qualquer corte ou sobreposição em todo PDF”, fidelidade visual à prévia HTML, legibilidade humana, acessibilidade PDF, semântica de tagging, leitores específicos, ATS, impressão, todos os dados possíveis ou proteção das duas correções não identificadas.

### Matriz de validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| dois defeitos históricos identificados | patches e reproduções L01 | pais versus corrigidos, mesma entrada/oráculo | hashes continuam só introduções de formato |
| detector não reprova tudo | P01 e controles válidos de N01/N02 | gerar e auditar | controle válido reprovado |
| detector vê perda | N03 rejeitado com categoria correta | omissão deliberada de marcador | passa apesar da omissão |
| detector vê posição/colisão | N01/N02/N04 rejeitados, CTM correta | PDF sintético conhecido | só origem medida; texto com matriz passa incorretamente |
| ambiente permanente suporta suíte | execução tests original sem skips | comando dedicado | passa só com dependência temporária |
| nenhum teste antigo regrediu | diff de IDs/status e diagnósticos | baselines antes/depois | novo erro, skip ou desaparecimento de ID |
| proteção contínua | job CI tests dedicado executa novos IDs | handoff separado e execução remota futura | suíte só manual ou todos os testes ignorados |

## Handoffs e atividades posteriores

### Divisão de trabalho e adequação das skills locais

Inventário .agents/skills: decision-analysis-v4, frontend-implementation-v3, integration-system-testing-v1, nix-environment-implementation-v1, backend-adapters-drivers-v2, backend-domain-orchestration-v2 e cross-cutting-implementation-v1. Nenhuma skill adicional foi presumida.

Foram lidos os SKILL.md e os contratos/fit-check abaixo; as classificações são desta análise, não invocações para implementar:

| Skill | Contrato e teste de adequação lidos (sob references/) | Evidência e veredito |
|---|---|---|
| decision-analysis-v4 | classification-taxonomy.md, output-schema.md, output-routing.md, artifact-classification.md | elegível para esta análise; somente Markdown. initial por pedido expresso; não implementar |
| integration-system-testing-v1 | test-scope-boundary.md, test-fit-check.md | teste real cruza renderizador/leitor, atributos de arquivo, alvo em memória: fatia elegível em natureza. Veredito atual ambiguous porque oráculo/limiares e regressões históricas não fechados. O fit exige “oráculo verificável e evidência suficiente”; SKILL exige valores/condições aprovados para limiares quantitativos. Após L01–L03/L06, candidata correta para B |
| backend-adapters-drivers-v2 | outer-boundary.md, backend-fit-check.md | mismatch para esta entrega integrada: exige isolar uma unidade externa; a biblioteca de geração e o leitor são reais. Ser Python/infrastructure não torna o teste unitário |
| backend-domain-orchestration-v2 | clean-boundary.md, backend-fit-check.md | mismatch: não há regra interna/orquestração nova; uso real do adaptador sai da unidade do núcleo |
| frontend-implementation-v3 | scope-boundary.md, frontend-fit-check.md | mismatch: não é tela nem teste unitário cliente; DOM não produz este PDF |
| cross-cutting-implementation-v1 | scope-boundary.md, cross-cutting-fit-check.md | mismatch: resultado é teste de layout/conteúdo, não mecanismo de observabilidade, resiliência, segurança ou identidade |
| nix-environment-implementation-v1 | nix-scope-boundary.md, nix-fit-check.md | mismatch para suíte Python; elegível apenas como handoff separado de experimento Nix se L10 aprovado, sem modificar testes ou manifestos de linguagem |

Não há lacuna de processo por inexistência de skill de integração; há gate de evidência/decisão ainda não satisfeito. Para prosseguir, fornecer insumos da tabela e produzir revisão para proposed; depois invocar explicitamente $integration-system-testing-v1 com caminho e versão exatos. Não é preciso autorizar modificação de produção nem alargar escopo. Se o executor optar por unidade pura do detector separada, reclassificar a fatia e o perfil, sem fingir que teste unitário substitui PDF real.

Trabalho sequencial recomendado: produto/design resolvem L01–L03/L05; engenharia valida L06 por controles e revisa a análise; executor implementa somente os dois arquivos de teste; revisor confirma sensibilidade, identidades e alegações; CI é handoff próprio. Não se delegou a subagentes nesta atividade.

### Plano concreto de ambiente temporário — somente execução futura

Plano principal B: zero linhas a alterar em nix/backend-python-packages.nix, nix/backend.nix, nix/frontend.nix, nix/tests.nix, nix/quality.nix, flake.nix, flake.lock, src/frontend/package.json e src/frontend/package-lock.json. O inventário de manifestos/locks não encontrou manifesto Python separado de dependências que deva ser inventado: a lista central está em nix/backend-python-packages.nix. Pypdf/ReportLab já existem; não há justificativa para adicionar pacote antes de medir o bloqueio.

A solicitação permite ao executor futuro alterar temporariamente definições Nix e manifestos/locks quando necessário; não autoriza fazê-lo nesta análise nem torna toda alteração necessária. Experimento C opcional e separado, se B for insuficiente:
1. Antes de qualquer escrita, executar git status --short -- nix flake.nix flake.lock src/frontend/package.json src/frontend/package-lock.json; git diff e git diff --cached desses caminhos. Se houver mudança do usuário em qualquer alvo necessário, parar e informar; não restaurar nem mesclar por conta própria.
2. Único alvo proposto: nix/tests.nix, na expressão atual “ps: backendPythonPackages ps ++ [ ps.aiosqlite ]”, trocar exatamente por “ps: backendPythonPackages ps ++ [ ps.aiosqlite ps.pymupdf ]”. Incluir comentário de proveniência se a skill Nix for usada. Nenhuma alteração em flake.nix/flake.lock ou frontend; manter mesmo nixpkgs. Confirmar primeiro a existência/versão do pacote nesse nixpkgs por leitura/avaliação offline; se indisponível no store, registrar bloqueio, sem instalar nesta análise. Na execução futura, qualquer fetch/instalação exige contexto e autorização próprios para não contrariar o isolamento sem rede.
3. Não mudar nix/backend-python-packages.nix: leitor experimental deve ficar só em tests. Não adicionar Poppler simultaneamente. Se a alternativa escolhida for rasterização, nova decisão deve especificar o binário e substitui este experimento, não se acumula por conveniência.
4. Diff proposto sem comentário, para revisão: linha removida “ps: backendPythonPackages ps ++ [ ps.aiosqlite ]”; linha adicionada “ps: backendPythonPackages ps ++ [ ps.aiosqlite ps.pymupdf ]”. O diff completo real, incluindo eventual comentário e contexto, deve ser copiado literalmente para o resumo antes de restaurar. Não se forja aqui um diff executado.
5. Executar primeiro a suíte no estado original, preservando IDs/status/bloqueios. Só depois executar experimento e registrar versões; comparar também instrumentos sobre os mesmos PDFs. O segundo resultado prova execução sob ambiente temporário, não suporte pelo ambiente permanente. Não deixar import obrigatório de fitz no teste que será entregue sem dependência permanente.
6. Ao final, fora de Nix, após confirmar que só há alterações próprias no alvo e que nenhum usuário o modificou durante o experimento: git restore --source=HEAD --worktree -- nix/tests.nix. Não fazer stage do experimento. Se houver alteração inesperada no index, parar; se for comprovadamente somente do experimento e houver autorização, restaurar explicitamente esse único caminho também no index. Nunca git restore . e nunca restaurar caminhos alheios.
7. Verificar git status --short -- nix/tests.nix; git diff --exit-code -- nix/tests.nix; git diff --cached --exit-code -- nix/tests.nix. Também verificar todos os caminhos inicialmente auditados; precisam permanecer sem delta. Incluir git status --short global no resumo, com somente entregas autorizadas. Diffs completos de qualquer outro alvo temporário passam pelo mesmo procedimento com nomes explícitos, antes de reverter.
8. Remover somente diretório temporário criado pela execução, por limpeza do contexto TemporaryDirectory; não remover store/perfis/dependências do usuário. PDFs/imagens/relatórios/caches não entram no commit.

.gitignore raiz ignora node_modules, dist, build e *.log de forma geral; frontend ignora *.tsbuildinfo. Não há padrão geral encontrado para *.pdf, imagens de execução, __pycache__, *.pyc, coverage ou relatórios de teste. Não alterar .gitignore nesta análise: preferir /tmp e PYTHONDONTWRITEBYTECODE=1. Algumas suítes existentes podem criar caches em execução; git status final deve expor qualquer novo arquivo antes de entrega. Não adicionar ignore amplo de PDF que oculte futuras fixtures intencionais.

### Evidência mínima e aprovação futura

Recomenda-se PR com versão/revisão da análise, comando real, versões, IDs executados/skips, saída dos controles de sensibilidade, limites e diff de baseline, sem PDF/imagens anexados ao repositório. O precedente docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md justifica documento manual se o card o exigir, mas não sustenta inventar exigência de “zero falhas visuais”. A skill de integração exclui relatórios gerados salvo convenção/finalidade de baseline aprovada. Não alterar evidência anterior nem esta análise na implementação.

## Síntese

É possível desenhar uma regressão do gerador PDF atual com ReportLab e pypdf já disponíveis, sem banco, rede ou dependências novas. Falta comprovar quais são as duas correções históricas e aprovar o significado medido de corte/sobreposição. A decisão permanece pending; os cenários propostos são especificação condicional e caracterização explícita. Nenhum teste novo, configuração ou produção foi implementado.

## Apêndice A — Solicitação literal do usuário

O bloco abaixo preserva a solicitação, sem converter declarações nela contidas em fatos do repositório. As instruções da skill foram fornecidas separadamente pelo usuário e conferidas no arquivo .agents/skills/decision-analysis-v4/SKILL.md; sua versão lida está identificada no inventário de artefatos.

<solicitacao-original>

$decision-analysis-v4 Implementar "Criar teste de regressão para ausência de corte ou sobreposição em PDF". O resultado esperado é um teste de regressão executável. Antes de decidir o que ele contém, descubra como o PDF é gerado neste projeto, o que as duas correções de produção associadas ao card mudaram, o que "corte" e "sobreposição" significam objetivamente aqui, e o que o ferramental disponível consegue provar. Esta é uma análise nova, iniciada do zero: a branch foi criada a partir da `dev` atualizada, e você deve identificar por inspeção o que existe e o que há de novo.

## Regra principal: não presumir

Todo fato deve vir de um artefato lido (histórico Git, código, testes, configuração, documentação, requisitos, definições de ambiente, workflows de CI), com o caminho indicado. O que nenhum artefato definir deve ser registrado como lacuna, nunca como fato.

- Separe em seções distintas: **(a) fatos encontrados**, com caminho e trecho; **(b) lacunas**, ou seja, o que nenhum artefato define; **(c) recomendações**, que são suas, com justificativa.
- Para cada lacuna, apresente as opções viáveis, recomende uma e marque se depende de decisão de produto ou de design, ou se pode ser tomada tecnicamente com base no que existe.
- Quando artefatos divergirem (documentação, código, commits, testes), aponte a divergência, diga qual fonte parece mais confiável e por quê, sem escolher em silêncio.
- Não transponha para o PDF regras, convenções ou resultados de outros recursos sem que um artefato sobre o PDF as sustente.

## Ponto de partida

Parta exclusivamente do estado atual desta branch. Não presuma a existência de nenhuma exportação de PDF, biblioteca, teste, fixture, cenário ou análise sobre o tema. O que existir entra como fato (com a cobertura avaliada), o que não existir entra como lacuna. **Inventarie os harnesses e fixtures de teste que de fato existem na base** (backend e front-end) e não presuma nomes.

## Texto do card

Somente o título foi fornecido: "Criar teste de regressão para ausência de corte ou sobreposição em PDF". Não há descrição nem critérios de aceite. **Não invente critérios.** Derive o que for possível do título, dos commits e dos artefatos, marque a origem de cada critério como "inferido" e liste exatamente o que precisa ser fornecido para fechar cada lacuna.

## Commits de produção associados ao card

O card está associado aos commits de produção **84e3a5b** e **4ad3416**. Trate-os como o ponto de partida do levantamento, sem presumir o que fizeram:

- Verifique, por Git local, se cada hash existe e se é ancestral do HEAD atual. A CLI do GitHub e a rede podem não estar disponíveis; **não dependa delas**. Se um hash não existir ou for ambíguo (por exemplo por squash ou rebase), registre isso e localize o trabalho por mensagem, arquivos e histórico, sem inventar conteúdo.
- Para cada commit, levante: mensagem, autor e data, arquivos alterados, o diff relevante, testes adicionados ou alterados, referências a PR ou issue, e **qual defeito de PDF cada um corrige ou qual comportamento muda**. Derive a natureza do defeito **do diff e da mensagem**, não do título do card.
- Número de card não é número de PR: não infira a ligação apenas pela coincidência de números, e registre como identificou cada trabalho.
- Leia o código dos arquivos alterados **antes e depois** de cada commit (por `git show <rev>:<caminho>` e `git show <rev>^:<caminho>`, somente leitura), para entender o comportamento anterior e o corrigido. **Não use `git checkout`, `git switch`, `git stash`, `git reset` nem `git worktree` durante esta análise.**
- Verifique se existe outro commit posterior que altere o mesmo código de geração de PDF (`git log -- <caminhos>`), e se algum teste existente já tenta proteger o comportamento corrigido.

## Fontes a analisar

1. **Histórico Git local:** além dos dois commits, o histórico dos arquivos de exportação e de geração de PDF, dos modelos ou templates de currículo, do cliente de exportação e dos testes relacionados.
2. **Documentação pertinente**, localizada por busca (não presumida): requisitos funcionais e não funcionais sobre exportação, impressão, formatos de saída, paginação, margens, tamanhos de página, compatibilidade e acessibilidade; documentos de interface e de design; matrizes de rastreabilidade e de teste; evidências de testes anteriores em `docs/`; e análises anteriores em `prompts/`. Registre os termos buscados (por exemplo PDF, exportar, exportação, impressão, margem, página, corte, sobreposição, overflow, quebra de página) e o que cada busca retornou, **inclusive resultados vazios**.
3. **Código atual relacionado**, no backend e no front-end: onde o PDF é gerado (servidor, cliente, navegador ou ferramenta externa), bibliotecas usadas e suas versões, modelos ou variantes de layout, folhas de estilo de impressão, rotas e clientes de exportação, tratamento de erros, composição da aplicação e os testes existentes (unitários, de componente, de integração e de ponta a ponta).
4. **Ferramental e instruções:** `AGENTS.md` (raiz, backend e front-end), manifestos de dependências e lockfiles, configurações de bundler, linguagem, lint e testes, definições de ambiente Nix, workflows de CI e as skills disponíveis em `.agents/skills` (inventarie quais existem, sem presumir nomes).

## O que levantar

- **O pipeline de geração do PDF.** Descubra, com evidência: onde e como o PDF é produzido; a biblioteca ou o motor de renderização; os dados de entrada; as variantes (modelos de currículo, tamanhos de página, orientação) e como cada uma é selecionada; como paginação, margens, quebras de página e fontes são tratadas; e se a saída é determinística (fontes embutidas, metadados com data ou identificador aleatório, dependência de locale ou de fuso).
- **O defeito que os dois commits corrigem.** Descreva, para cada commit, o comportamento defeituoso anterior, a causa no código e a correção, **somente com base no diff**. Diga se os dois tratam do mesmo defeito ou de defeitos distintos, e se eles cobrem corte (conteúdo perdido ou fora da área útil), sobreposição (elementos que se cobrem) ou outro problema.
- **O que "corte" e "sobreposição" significam objetivamente neste projeto.** Procure se algum artefato define o critério (margens mínimas, área útil, tolerâncias). Se nenhum o definir, trate como **lacuna de produto ou de design** e proponha definições operacionais verificáveis (por exemplo conteúdo fora da área útil da página, texto esperado ausente do PDF, caixas de texto que se interceptam além de uma tolerância), com os valores e a justificativa, marcando o que depende de decisão e o que é heurística.
- **Como inspecionar um PDF em teste, e o que isso prova.** Avalie, com base no que o projeto já tem e no que o ambiente pode oferecer, as alternativas de verificação, por exemplo: (a) extração de texto com coordenadas por página e checagem geométrica; (b) comparação do texto esperado (dados sintéticos de entrada) com o texto extraído, para detectar perda de conteúdo; (c) análise das caixas de página e do conteúdo; (d) rasterização da página e análise de pixels; (e) comparação com imagens de referência. Para cada alternativa, diga o que prova, o que **não** prova, se é determinística entre ambientes, o que exige de dependências e de binários, e se pode ser executada com o que existe. Registre quais bibliotecas ou ferramentas de leitura de PDF já estão instaladas ou declaradas (backend, front-end e Nix) e **não instale nada**.
- **Como provar que o teste detectaria a regressão.** Um teste de regressão só vale se falhar quando o defeito volta. Defina como demonstrar isso (o chamado controle de sensibilidade) e avalie a viabilidade de cada forma: executar a mesma verificação contra a versão anterior à correção (os pais dos commits associados), em uma cópia isolada fora do repositório, ou contra PDFs sintéticos deliberadamente defeituosos, ou contra uma variante do código adulterada em memória. Descreva o procedimento, o que ele exige (dependências, ambiente, tempo) e os riscos. **Não execute nada que altere o repositório ou o working tree.** Se o procedimento exigir criar uma cópia do código, descreva-o para a execução futura.
- **Dados de teste.** Quais entradas sintéticas exercitam o defeito (por exemplo textos longos sem pontos de quebra, listas extensas que atravessam a quebra de página, campos vazios ou ausentes, caracteres acentuados e especiais, todas as variantes de modelo e de tamanho de página). Nenhum dado pessoal, e nenhum serviço externo ou rede.
- **A cadeia exercitável e a composição.** Descubra se a exportação está ligada na aplicação que sobe, se depende de componentes que podem não existir em teste e como o teste deve compor a geração (chamada direta da função de geração, rota, ou página). Registre o que a composição de produção faz hoje e o que isso implica para o que o teste consegue provar.
- **Cobertura existente:** o que os testes atuais já cobrem sobre exportação e PDF, em que nível e com quais oráculos (por exemplo se só conferem que o PDF "foi gerado"), e o que falta, para o teste novo não repetir cobertura sem necessidade.
- **O ambiente:** o que cada ambiente Nix (backend, front-end, tests, quality) oferece hoje; como as dependências são instaladas; se há rede durante a execução; e os comandos reais de testes, lint, tipos e formatação, descobertos por manifestos, workflows e documentação. Execute apenas comandos de leitura e um **baseline informativo** das suítes do backend e do front-end e dos gates de lint e de tipos aplicáveis, registrando comando, ambiente, resultado e contagens, comparando por identidade de teste e não só por total. Se alguma dependência instalada faltar, registre o bloqueio e **não instale nada**.
- **Bloqueios preexistentes:** registre, sem tratá-los como escopo e sem corrigi-los, tudo que impediria executar o teste (ferramenta de leitura de PDF ausente, dependências não instaladas, exportação sem composição, binário de renderização indisponível, grafo de migrations inválido se o teste exigir banco).

## Escopo

Definir o **teste de regressão executável** que protege os dois comportamentos corrigidos nos commits associados, verificando ausência de corte e de sobreposição no PDF gerado: o nível do teste, as entradas, as verificações, os oráculos, os controles de sensibilidade, as fixtures, a forma de execução, a estrutura de arquivos e os limites do que prova.

Fora do escopo: alterar a geração do PDF, os modelos, os estilos, as bibliotecas ou os commits de produção; corrigir defeitos de layout encontrados (registre-os como achados); alterações permanentes de ambiente ou de dependências; chamar serviços externos; alterações em outros recursos.

## Instruções

- Para cada decisão que os artefatos não resolverem, recomende uma opção com justificativa e marque se depende de produto, de design ou de engenharia.
- **Priorize o ferramental que o projeto já tem.** Se a recomendação exigir dependência nova, binário ou configuração que não existe, registre como **pré-requisito separado**, com a justificativa, e indique a alternativa sem ele e o que ela deixaria de provar.
- **Cenários.** Cada cenário deve ter objetivo, pré-condições, entradas, passos, resultado esperado, a fonte que o sustenta, a origem do critério (definido ou inferido), a camada exercitada e o nível do teste. Considere, **apenas se algum artefato os definir ou implementar**: PDF com conteúdo normal (controle positivo, para provar que o detector não reprova tudo); o conteúdo que reproduz cada defeito corrigido nos dois commits; variações de volume e de comprimento que atravessem a quebra de página; as variantes de modelo e de tamanho de página; campos ausentes; e **controles de sensibilidade**, em que a mesma verificação aplicada a um PDF defeituoso (sintético ou da versão anterior à correção) **deve reprovar**. O que não estiver definido entra como lacuna, e a análise deve dizer se o teste o registra como caracterização (rotulada como tal) ou aguarda decisão.
- **Tolerâncias e limiares.** Se a verificação usar limiares (margens, áreas de interseção, tolerâncias numéricas), explicite cada valor, a justificativa, o que ele protege contra falso positivo e falso negativo, e a decisão de produto envolvida.
- **Determinismo e isolamento.** Defina como evitar dependência de data, de fuso, de locale, de fontes do sistema, de rede e de ordem de execução, e como os artefatos temporários (PDFs, imagens) são criados e removidos fora do repositório. Diga se algum arquivo binário de referência é necessário e, se for, justifique tamanho, origem e manutenção; **prefira dados e geometria a imagens de referência**.
- **Honestidade da prova.** Um teste ignorado não é prova. Diga como o resultado distingue "executado e aprovado" de "ignorado por ambiente", e **quais alegações são permitidas e proibidas** (por exemplo, não afirmar fidelidade visual, legibilidade, acessibilidade, comportamento em leitores de PDF específicos, compatibilidade com sistemas de triagem de currículos ou aparência em impressão, se o nível do teste não os prova). Diga também o que o teste não prova.
- Defina a estrutura: nomes e localização dos arquivos conforme a convenção de cada camada, reaproveitamento dos harnesses e fixtures **que de fato existem na base**, configuração necessária, como os testes são executados e como os que dependem de recurso ausente são ignorados com motivo explícito, sem gerar erro quando o ambiente não os suporta. Diga se o teste roda no CI hoje, e a consequência para a proteção real da regressão.
- Registre achados de backend, de front-end e de documentação (divergências entre commits, código, documentação e testes; estados não tratados; riscos) em seção própria, sem corrigi-los.
- Indique a divisão de trabalho. **Leia o contrato de escopo e o teste de adequação de cada skill inventariada em `.agents/skills` e confirme, com evidência, se esta fatia é elegível a alguma delas**; se nenhuma cobrir, registre como lacuna de processo, recomende como prosseguir e indique o que o usuário precisaria autorizar explicitamente. Especifique nomes de arquivos, ambientes e comandos, para o executor não precisar inventá-los. Diga também se o resultado precisa de um registro em documento (por exemplo em `docs/testes/evidencias/`) ou se basta o texto do PR, e recomende o mínimo, de acordo com os precedentes do projeto.
- **Alterações temporárias de ambiente.** Registre que, para executar o teste, o executor poderá aplicar alterações temporárias em definições Nix (`nix/*`, `flake.nix`, `flake.lock`) e nos manifestos de dependências (manifesto e lockfile do front-end, ou de dependências do backend), por exemplo para disponibilizar uma biblioteca ou binário de leitura de PDF. Proponha o plano concreto, arquivo por arquivo e linha por linha. Todas devem ser revertidas por `git restore` com caminhos explícitos (nunca `git restore .`) ao final, com os diffs completos copiados para o resumo, e `git status --short` e `git diff --exit-code` (inclusive `--cached`) sem nenhum desses caminhos. Se já houver mudanças do usuário neles, a execução não deve restaurá-las: deve parar e informar. Se o teste exigir também **uma cópia do código anterior às correções** para o controle de sensibilidade, indique como obtê-la sem alterar o working tree (por exemplo em um diretório temporário fora do repositório) e como removê-la. Artefatos gerados pela execução (PDFs, imagens, relatórios, caches, dependências instaladas) não devem entrar no commit: verifique o `.gitignore` e registre o que faltar. Recomende executar primeiro no estado original, para registrar bloqueios, e depois sob o experimento temporário, deixando claro que o segundo prova o teste sob o ambiente temporário e não sob o ambiente permanente.
- Defina o roteamento do artefato de análise (pasta em `prompts/`) conforme a organização existente, e justifique, caso o tema cruze backend e front-end.
- Registre na validação os comandos **reais** de cada camada, descobertos por inspeção e executados no ambiente Nix correspondente: testes, lint, tipos e formatação do front-end; testes e lint do backend; e os gates do `.github/workflows/ci.yml` aplicáveis, com o baseline observado, para a execução futura não gerar regressão nem erro novo (comparação por identidade de teste e de diagnóstico, não só por total).
- Não implemente nada.

</solicitacao-original>

