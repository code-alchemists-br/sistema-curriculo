---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v002"
status: proposed
created_at: "2026-10-31T13:22:42-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261031-124820-regressao-pdf-corte-sobreposicao-v001.md
  supersedes: prompts/backend/20261031-124820-regressao-pdf-corte-sobreposicao-v001.md
  change_type: scope-change
  secondary_change_types: [enrichment, correction]
  decision_impact: revised
subjects:
  kind: file-set
  files:
    - path: prompts/backend/20261031-124820-regressao-pdf-corte-sobreposicao-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked; SHA-256 c8f963dc731d22cad2d1f0e96712ce19b620fe05cc8f7ca56e0932e56fa16128"
      availability: available
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
    - path: src/backend/tests/fixtures/curriculo_exportacao.py
      relationship: primary
      representation: source-code
      function: data-fixture
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
    - path: src/backend/domain/modelo_curriculo.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: available
    - path: .github/workflows/ci.yml
      relationship: supporting
      representation: structured-data
      function: configuration
      format: YAML
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/revisao, prompts/requisitos, prompts/frontend, prompts/ambientes, prompts/templates]
  confidence: high
  rationale: "Continuidade da linhagem e finalidade de teste do gerador Python; frontend e ambiente permanecem fora da entrega."
classification:
  sphere: engineering
  concerns: [reliability, implementation, delivery]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: medium
---

# Análise de decisão — Proteção preventiva do layout nominal do PDF

## Solicitação original

A primeira solicitação da linhagem está preservada literalmente no Apêndice A. A entrada desta revisão, com D1–D12 e as onze atividades solicitadas, está preservada literalmente no Apêndice B. As decisões novas substituem os pontos incompatíveis da solicitação inicial, especialmente a interpretação de introduções de formato como correções históricas. Não alteram retrospectivamente a v001.

## Informações complementares

Origem normativa desta revisão: decisão do usuário, D1–D12. Os limiares são heurística de engenharia, ajustável por design, aprovada pelo usuário para esta fatia; não são critérios originais do card descobertos em documentação.

O objeto permanece o teste executável futuro. Esta atividade só entrega análise e calibração temporária, sem testes novos ou alteração de produção. A calibração autorizada gerou PDFs em memória e usou patch de escopo exclusivamente no processo Python. Não houve instalação, rede, checkout, switch, stash, reset, worktree ou cópia histórica.

Estado revisto: HEAD d45115dc5d9fd75f336cc86281b687f49e3e0ffc, igual à v001. A v001 já era arquivo não rastreado no início desta revisão; isso foi preservado. Nenhum arquivo de código/configuração estava modificado. Seu SHA-256 antes da escrita da v002 é c8f963dc731d22cad2d1f0e96712ce19b620fe05cc8f7ca56e0932e56fa16128.

## Mudanças desde a versão anterior

| Elemento | v001 | v002 | Motivo/origem | Impacto |
|---|---|---|---|---|
| enquadramento | pending à espera de identificar correções | proteção preventiva da geração PDF de 84e3a5b; DOCX excluído | D1 e Git reconsultado | remove necessidade de reprodução histórica e cenários R01/R02 |
| limites | propostas sem aprovação | D3 aprovado; mesmos números, escritos literalmente | decisão do usuário | fecha área e critério nominal de colisão |
| cadeia | direto ou rota; composição como lacuna | DTO → renderizador real → leitor real | D2 | exclui HTTP/banco/frontend/E2E |
| dados | volumes propostos | volumes finitos e catálogo aprovados | D4–D6 | cenários determinados sem inventar máximos de produto |
| detector | viabilidade ainda não medida | subconjunto identificado em PDFs reais e controles de coordenadas | D7 + calibração | fecha L06 para implementação restrita, não para PDF genérico |
| sensibilidade | sintéticos e possível cópia histórica | N01–N05 obrigatórios; N06 viável e recomendado | D8 + patches medidos | acrescenta mutações reais de margem/leading |
| descoberta/CI | módulo sem test_, só manual e handoff CI | test_integracao_regressao_pdf_layout.py, descoberto pelo job atual | D9, desvio deliberado | CI contínuo pelo discover; execução formal adicional em tests |
| ambiente | experimento opcional com PyMuPDF | zero alterações de ambiente; ferramentas novas rejeitadas | D7/D10 | remove plano de alteração/restauração Nix |
| registro | PR mínimo ou evidência docs se exigida | PR basta; sem docs ou binários | D11 | fecha L11 |
| baseline | 1.126 / 84; hashes conhecidos | 1.126 / 84 novamente; mesmos IDs e skips | execução desta revisão | nenhuma diferença por identidade |
| frontend | baseline de 336 casos na v001 | não reexecutado | não afetado e instrução explícita | não apresentar resultado antigo como execução nova |
| status/handoff | pending / ambiguous | proposed / valid para integração | decisões + evidência atual | implementável sem autorização de mudar produto |
| artefatos | ampla inspeção documental | releitura dos essenciais; novo recorte de operadores, codificação e callbacks | calibração autorizada | nenhuma mudança de produção encontrada; evidência nova de Tw e agrupamento textual |

## Artefatos analisados

Os arquivos do projeto abaixo estão em working-tree, baseados no HEAD acima e sem delta de conteúdo rastreado. Revisões Git têm content_state commit. A v001 é working-tree não rastreado, não se afirma que pertence ao HEAD. Arquivos temporários são external e são removidos ao fim; os trechos e resultados necessários estão preservados nesta análise.

| Caminho | Relação | Representação / função / formato | Recorte e estado |
|---|---|---|---|
| prompts/backend/20261031-124820-regressao-pdf-corte-sobreposicao-v001.md | primary | prose / documentation / Markdown | integral, incluindo frontmatter e solicitação; working-tree não rastreado |
| src/backend/infrastructure/exportacao/renderizador_pdf.py | primary | source-code / production / Python | integral atual e git show 84e3a5b; ausência no pai; histórico e diff até HEAD |
| src/backend/application/documento_renderizado.py | primary | source-code / production / Python | DTOs e montagem atuais; leitura integral na revalidação e diff de 4ad3416 |
| src/backend/tests/fixtures/curriculo_exportacao.py | primary | source-code / data-fixture / Python | integral; dados, IDs, datas e legado padrao_fatec |
| src/backend/tests/test_integracao_validacao_pdf_legibilidade.py | primary | source-code / test / Python | integral por recortes complementares, cinco métodos e suporte |
| src/backend/tests/test_infrastructure_renderizador_pdf.py | supporting | source-code / test / Python | inventário/cobertura da v001 e teste sem seções relido; suíte executada |
| src/backend/domain/modelo_curriculo.py | supporting | source-code / schema-contract / Python | integral; sete identificadores |
| src/backend/main.py | supporting | source-code / production / Python | integral; composição sem exportador |
| src/backend/api/factory.py | supporting | source-code / production / Python | parâmetros exportar_curriculo_* e registro do router |
| nix/backend-python-packages.nix, nix/backend.nix, nix/tests.nix, nix/quality.nix | supporting | source-code / build / Nix | integral de cada arquivo |
| flake.nix, flake.lock | supporting | source-code e structured-data / build / Nix e JSON | integral; pinagem e shells |
| .github/workflows/ci.yml | supporting | structured-data / configuration / YAML | integral, comandos reais |
| ruff.toml, .gitignore | supporting | structured-data e prose / configuration / TOML e texto | integral |
| AGENTS.md, src/backend/AGENTS.md, src/frontend/AGENTS.md | context | prose / prompt-instruction / Markdown | integral; especializações e ambientes |
| docs/configuracao-ambiente.md | context | prose / documentation / Markdown | seção de uso do ambiente Nix e gates, relida |
| prompts/README.md | context | prose / documentation / Markdown | integral; roteamento |
| docs/requisitos_funcionais.md, docs/requisitos_nao_funcionais.md, docs/matriz_testes.md | supporting | prose / documentation / Markdown | RF09, RNF07, CT-RF09 e buscas específicas |
| docs/exportacao-pdf-docx.md | context | prose / documentation / Markdown | integral |
| docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md | context | prose / documentation / Markdown | margens e alegações de legibilidade/zero falhas |
| docs/Arquitetura/ADR-005-catalogo-inicial-modelos-curriculo.md | context | prose / documentation / Markdown | título e status |
| prompts/backend/20261026-082930-validacao-pdf-paginacao-v001.md | context | prose / documentation / Markdown | alegações “nunca” e “qualquer leitor”, relidas por busca |
| src/frontend/app/jornada-selecao-previa-exportacao.e2e.test.tsx, src/frontend/app/jornada-curriculo.e2e.test.tsx | context | source-code / test / TSX | nomes dos harnesses, Blob simulado e comentário sobre gerador |
| src/frontend/features/visualizar-curriculo/ui/ModeloClassico.css | context | stylesheet / production / CSS | @media print |
| .agents/skills/decision-analysis-v4/SKILL.md | context | prose / prompt-instruction / Markdown | integral, mais referências obrigatórias |
| .agents/skills/decision-analysis-v4/references/classification-taxonomy.md, output-schema.md, output-routing.md, artifact-classification.md, revision-protocol.md | context | prose / prompt-instruction / Markdown | integral; cada nome sob o diretório references indicado |
| .agents/skills/integration-system-testing-v1/SKILL.md | context | prose / prompt-instruction / Markdown | integral |
| .agents/skills/integration-system-testing-v1/references/test-scope-boundary.md, test-fit-check.md, analysis-input-contract.md | context | prose / prompt-instruction / Markdown | integral; cada nome sob references indicado |
| outros SKILL.md e contratos/fit-checks inventariados na v001 | context histórico | prose / prompt-instruction / Markdown | conclusões anteriores mantidas somente como contexto, sem fingir nova leitura integral de todos |
| Git 84e3a5b, 4ad3416 e histórico do caminho PDF | supporting | source-code e structured-data / production e documentation / Git | show, diff-tree, ancestralidade, pais, log por caminho |
| /tmp/pdf-v002.Oi7cbJ/calibrar.py | supporting | executable-script / test / Python | integral executado; diagnóstico temporário, não suíte entregue |
| /tmp/pdf-v002.Oi7cbJ/complemento.py | supporting | executable-script / test / Python | integral executado; limiares e IDs |
| /tmp/pdf-v002.Oi7cbJ/calibracao.jsonl, calibracao.stderr, complemento.jsonl, complemento.stderr | supporting | generated / generated-output / JSONL e texto | resultados das gerações e medições; trechos preservados abaixo |
| /tmp/pdf-v002.Oi7cbJ/backend-baseline.log, pdf-baseline-tests.log | supporting | generated / generated-output / texto | contagens, identidades, motivos e resultados |
| pacotes ReportLab 5.0.1 e pypdf 6.18.1 do shell tests | supporting | source-code / production / Python | APIs efetivamente usadas na calibração: PdfReader, ContentStream, visitors, Canvas e pdfmetrics |

### Limites da evidência dos artefatos

Não se tomou a v001 como fonte suficiente dos fatos-chave: os essenciais acima foram relidos e o histórico reconsultado. A comparação não encontrou mudança de HEAD nem de código rastreado; o recorte novo é a saída efetiva do gerador e o comportamento do leitor. O inventário amplo de fixtures/skills não foi confundido com nova auditoria integral de todos os módulos não usados nesta entrega.

Não houve implementação nem execução da futura suíte de 11/12 métodos. A calibração demonstra a viabilidade do instrumento no subconjunto medido, não aprovação dos futuros cenários completos ou ausência universal de defeitos. Os logs temporários são removidos; os dados quantitativos e o procedimento relevante ficam registrados neste documento. Não se depende de rede ou GitHub para nenhuma conclusão.

## Problema enriquecido

### Resultado desejado

Entregar posteriormente uma suíte preventiva executável, na fronteira ReportLab/pypdf, que verifique conteúdo sintético completo e caixas nominais do PDF gerado, com sensibilidade demonstrada por PDFs defeituosos e mutações em memória. A aprovação desta análise não autoriza mudar produção.

### Atores e interesses

Engenharia precisa de teste sensível e reproduzível; estudante se beneficia da preservação de conteúdo; revisor precisa distinguir a medição nominal de fidelidade visual. Design pode revisar as heurísticas em nova decisão, sem alargar silenciosamente as tolerâncias.

### (a) Fatos encontrados — revalidados e com trechos

#### Histórico e código

- git merge-base --is-ancestor retornou 0 para ambos os hashes. git show -s --format=fuller confirmou: 84e3a5b041f318934f8249182dcd30dd25b3830d, mmagc, 23/10/2026 22:29:55 -03:00, “feat(backend): renderização PDF do currículo a partir do DTO #230”; 4ad34167cfec4a4e08da298879213382cbf3163b, mmagc, 22/10/2026 22:08:40 -03:00, “feat(backend): renderização DOCX do currículo a partir do DTO #231”.
- git diff-tree --name-status marca como A renderizador_pdf.py e test_infrastructure_renderizador_pdf.py no primeiro; no segundo, renderizador_docx.py, seu teste e __init__.py de exportação. git show dos renderizadores nos respectivos pais falha explicitamente porque os caminhos não existem. O PDF introduz ReportLab/pypdf e agrupamento/paginação; o DOCX introduz python-docx e a porta comum. São introduções, não correções.
- Arquivos de 84e3a5b: nix/backend-python-packages.nix, src/backend/infrastructure/exportacao/__init__.py, renderizador_pdf.py e src/backend/tests/test_infrastructure_renderizador_pdf.py. Arquivos de 4ad3416: nix/backend-python-packages.nix, src/backend/application/__init__.py, documento_renderizado.py, src/backend/infrastructure/exportacao/__init__.py, renderizador_docx.py e src/backend/tests/test_infrastructure_renderizador_docx.py. Os nomes curtos pertencem aos diretórios explicitados.
- git log -- src/backend/infrastructure/exportacao/renderizador_pdf.py continua retornando somente 84e3a5b. git log --all --ancestry-path 84e3a5b..HEAD -- esse caminho não retorna mudança; git diff 84e3a5b HEAD -- esse caminho está vazio. Nenhum commit corretivo real de layout PDF apareceu para acionar o bloqueio de D1.
- renderizador_pdf.py: ESTILO_CLASSICO = EstiloModelo(tamanho_fonte=10.5, espaco_bloco=6, margem_cm=2.0); ESTILO_COMPACTO = (...9, 3, 1.5); ESTILOS_POR_MODELO = {"compacto": ESTILO_COMPACTO}; seleção por .get(documento.modelo, ESTILO_CLASSICO). _estilos gera corpo leading=base*1.3. A4 e margens simétricas entram em SimpleDocTemplate; não há entrada de outro papel/orientação.
- Mesmo arquivo: KeepTogether([Paragraph(título da seção), *primeiro]) e KeepTogether para blocos seguintes. A docstring diz “quando possível”. O arquivo usa Helvetica/Bold/Oblique, BytesIO, author/creator vazios, lang="pt-BR" e invariant=1 somente quando solicitado.
- _texto: encode("cp1252", "replace").decode(...) e escape. O texto fora do conjunto vira “?”, conforme comportamento atual; isso não se rotula como corte geométrico.
- documento_renderizado.py define DTOs frozen com cabeçalho, blocos e seções; montar_documento_renderizado usa a ordem de seções da prévia, omite seções sem itens e formata textos/datas. O nome do modelo vem de previa.curriculo.layout.
- curriculo_exportacao.py fornece obter_curriculo_exportacao_fixture, IDs UUID estáveis, datas 2023/2024/2025 e layout="padrao_fatec". Não é necessário copiar constantes de helpers privados de outros testes.
- modelo_curriculo.py contém classico, compacto, ats-simples, criativo, moderno, academico e primeiro-emprego. O renderizador só possui a chave compacto em seu mapa; o fallback atual foi confirmado pela leitura, não importado de convenção frontend.
- test_integracao_validacao_pdf_legibilidade.py tem cinco métodos: geometria A4/abertura; conteúdo da primeira página; fixture extensa em duas páginas/Idiomas na segunda; texto clássico versus compacto; metadados/caminho privado. Comparar ESTILO_*.margem_cm à constante não mede a margem no PDF. Nenhum desses cinco calcula interseção de caixas.
- docs/requisitos_nao_funcionais.md RNF07 continua dizendo “preservar o conteúdo, a organização e a legibilidade ... sem cortes ou sobreposições”; os limiares não vêm dessa frase. CT-RF09-01/03/05 em docs/matriz_testes.md continuam em nível de conteúdo/layout, consistência e falha controlada.
- nix/backend-python-packages.nix lista reportlab e pypdf; backend.nix e tests.nix reutilizam essa lista; tests acrescenta aiosqlite. .github/workflows/ci.yml continua com discover -s src/backend/tests -t src em backend e Ruff em quality. Nenhuma nova configuração de CI foi encontrada.
- main.py continua sem injetar exportador PDF; a factory recebe exportar_curriculo_pdf=None. Isso é achado de composição, não dependência do novo teste direto.

Referências #230/#231 são textos das mensagens. Os vínculos a PRs #576/#574 da v001 foram obtidos pelos merges locais e não se confundem com esses números de card; a revisão não depende de acesso ao PR. O escopo PDF de D1 exclui o DOCX, preservando sua menção apenas como contexto histórico.

#### Calibração realmente executada

Comando-base, a partir da raiz:

    nix develop .#tests --offline --no-write-lock-file --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src TZ=UTC LC_ALL=C.UTF-8 python /tmp/pdf-v002.Oi7cbJ/calibrar.py

A execução efetiva redirecionou stdout/stderr para arquivos no mesmo diretório em /tmp. complemento.py foi executado com o mesmo prefixo. O sandbox inicialmente impediu abrir /nix/var/nix/db/big-lock (“Read-only file system”); a repetição autorizada fora do sandbox concluiu offline. Não foi falta de biblioteca nem motivo de skip de teste.

Versões observadas: ReportLab 5.0.1 e pypdf 6.18.1. Cada PDF foi produzido em BytesIO com invariante=True; a fixture foi convertida em prévia/DTO e o cabeçalho substituído por Pessoa Sintética, pessoa@example.invalid e https://example.invalid/perfil, sem gravar PDF em disco. Gerações reais: normal e um bloco de 120 detalhes para cada estilo; oito combinações token 512/2048 × detalhe/contato × estilo; mais controles de matrizes e mutações em memória. Não houve erro de geração nessas combinações; isso não é uma auditoria completa de todos os defeitos.

| Caso diagnóstico | Páginas | Tj / visitor_text não vazio | Observação |
|---|---:|---:|---|
| fixture sintética clássica | 1 | 28 / 28 | Tw=-0.120445 seguido de Tw=0 |
| fixture sintética compacta | 1 | 28 / 28 | sem Tw explícito |
| bloco com 120 detalhes, clássico | 4 | 126 / 126 | bloco se divide; não impor indivisibilidade |
| bloco com 120 detalhes, compacto | 4 | 126 / 126 | idem |
| token 512 em detalhe, clássico/compacto | 1 / 1 | 12 / 11 Tj | token repartido por largura |
| token 2048 em detalhe, clássico/compacto | 1 / 1 | 35 / 29 Tj | idem |
| token 512 em contato, clássico/compacto | 1 / 1 | 13 / 11 Tj | inclui URL e contatos precedentes |
| token 2048 em contato, clássico/compacto | 1 / 1 | 36 / 30 Tj | não há perda na concatenação dos runs medida |
| leading=1, clássico | 1 | 18 / 5 | visitor_text agrega linhas; não pode fornecer uma caixa única |

Esses totais de página são observações do diagnóstico sem a marcação final dos cenários. Não são novos critérios de aceite. A marcação final pode mudar quebra/volume.

Inventário efetivo de operadores nos PDFs de produção medidos: cm, q, Q, BT, ET, Tf, TL, Tm, Tj, T*, rg e Tw. Por exemplo, normal clássico: cm=34, q=59, Q=59, BT=27, ET=27, Tf=27, TL=27, Tm=26, Tj=28, T*=28, rg=26, Tw=2.

| Operação/recurso pedido | Resultado observado |
|---|---|
| cm e q/Q | presentes, pilha balanceada; traduções no gerador; escala adicional calibrada em controle |
| Tm e T* | presentes |
| Td, TD, TJ | ausentes em todos os casos medidos |
| Tc, Tz, Ts | ausentes; estados padrão 0, 100 e 0, respectivamente |
| Tw | presente no normal clássico, inclusive valor negativo -0.120445 e restauração 0 |
| rotação de página | /Rotate=0 |
| UserUnit | efetivo 1, sem unidade alternativa |
| caixas | MediaBox=[0,0,595.2756,841.8898]; CropBox efetiva igual nesse diagnóstico |
| fontes | /Helvetica, /Helvetica-Bold, /Helvetica-Oblique; /Subtype=/Type1; /Encoding=/WinAnsiEncoding |
| incorporação | recursos de fonte examinados sem /FontDescriptor e sem referência a FontFile nesses recursos; não prometer aparência em qualquer leitor |
| clipping, imagem, máscara | não apareceram no subconjunto medido; devem ser recusados caso apareçam |

O texto dos Tj foi obtido dos bytes originais da string PDF, decodificados por WinAnsi/cp1252, não por str(objeto) presumindo PDFDocEncoding. Espaços têm avanço afetado por Tw. Para o subconjunto atual, cada Tj corresponde a uma linha/run desenhado; visitor_operand_before fornece CTM e matriz de texto antes desse Tj. visitor_text serve de conferência textual, não de fonte única de caixas.

Comparação com posições conhecidas, usando Canvas.saveState, translate(100,200), scale(1.25,0.75), drawString(10,20,"Ação CONTROLE") e restoreState:
- CTM recebida: [1.25,0,0,0.75,100,200]; Tm: [1,0,0,1,10,20].
- Origem esperada pela composição: (112.5,215.0); origem medida antes do Tj e no visitor_text: (112.5,215.0).
- Helvetica-Bold 12: caixa nominal medida [112.5,213.137,237.51,221.462].
- Depois de Q, drawString(50,100,"ITÁLICO") devolveu origem (50,100) com CTM identidade, Helvetica-Oblique 12 e caixa [50,97.516,96.68,108.616].
- A fixture normal entregou, para Pessoa Sintética, CTM [1,0,0,1,62.69291,753.9969], Tm [1,0,0,1,0,4.2], origem (62.69291,758.1969), fonte Bold 21. Os callbacks coincidiram nesse exemplo.
- Com leading=1, as três primeiras baselines de detalhe foram y=679.8469, 678.8469 e 677.8469; visitor_text não separou todas essas linhas. A medida por Tj preservou-as.

Token do diagnóstico: "ZZINICIO" + "X"*(N-13) + "ZZFIM", N=512/2048. Em detalhe clássico de 512: segmentos de 68, seis de 67 e um de 42 caracteres; compacto: 84, cinco de 82 e 18. O stream contém Tj/T* por linha; a concatenação controlada recuperou o token integral nos oito casos. Em contato pode haver prefixo do cabeçalho na primeira linha ou fragmento de sentinela na última, portanto não filtrar linhas só por substring da sentinela. Os testes finais usam sentinelas distintas, especificadas adiante.

#### Calibração dos limiares e das mutações

complemento.py desenhou dois “M” em Helvetica 12. Largura medida 9.996 pt, ascendente 8.616, descendente -2.484, altura nominal 11.1. Segundo run: x=100+9.996−dx, y=200+11.1−dy. Resultado:
| dx pretendido | dy pretendido | dx/dy medidos, arredondados | Colisão por D3 |
|---:|---:|---|---|
| 0.49 | 0.49 | 0.49 / 0.49 | não |
| 0.49 | 0.51 | 0.49 / 0.51 | não |
| 0.51 | 0.49 | 0.51 / 0.49 | não |
| 0.51 | 0.51 | 0.51 / 0.51 | sim |

A aritmética crua foi, por exemplo, 0.5099999999999909, sem arredondar antes da decisão. Na área clássica, invasões de 0.49 e 0.51 pt foram colocadas separadamente em cada um dos quatro lados. Todas as de 0.49 ficaram dentro da folga e todas as de 0.51 foram classificadas fora_area. Exemplo esquerdo: xmin=56.20291 / 56.18291. Exemplo inferior: ymin=56.20291 / 56.18291. Não se aumentou a tolerância.

N05 foi medido nos dois estilos com:
    patch.dict(modulo.ESTILOS_POR_MODELO, {modelo: replace(estilo_original, margem_cm=0.5)})

A .get do código de produção passa a selecionar essa chave inclusive para classico; não se altera a área esperada. Menor x dos runs=20.17323, versus margens aprovadas 56.69291339 e 42.51968504, portanto fora_area nos dois estilos. O mapa foi restaurado ao sair do contexto. Patchar só a variável ESTILO_COMPACTO não seria suficiente, pois o mapa já contém a instância anterior: a forma medida evita esse falso controle.

N06 é viável: guardar original=_estilos; patch.object sobre esse nome, side_effect que chama original, substitui somente estilos["corpo"] por seu clone com leading=1 e retorna o dict. Um detalhe longo do renderizador real passa a ter baselines distantes 1 pt e altura nominal de 9.7125 pt no clássico, produzindo profundidade vertical 8.7125 pt em linhas com sobreposição horizontal. O contexto restaurou a função; estilos de produção no arquivo não foram tocados. A revisão recomenda incluir esse opcional, totalizando 12 métodos. Não se executou aqui a futura asserção de auditoria; demonstrou-se a mutação e a medida que a asserção usará.

### Hipóteses

A implementação futura seguirá o subconjunto calibrado e recusará explicitamente seu alargamento. Os controles futuros precisam validar o próprio extrator entregue; as medições desta análise não substituem executar esses controles no código definitivo.

### (b) Lacunas da v001 e fechamento por origem

| Lacuna | Fechamento | Origem | Consequência |
|---|---|---|---|
| L01 — correções históricas | fechada | decisão do usuário D1; histórico revalidado | proteção preventiva; DOCX, R01/R02 e cópia histórica excluídos |
| L02 — corte/área útil | fechada | D3/D7, heurística de engenharia ajustável por design | área e folga literais |
| L03 — sobreposição | fechada | D3, mesma classificação de heurística; calibração 0.49/0.51 | duas profundidades estritamente >0.5 |
| L04 — limites/volume | fechada para esta fatia | D5 | volumes finitos de caracterização, sem máximos de produto |
| L05 — sete modelos/fallback | fechada | D6 + enum/mapa revalidados | testar oito identificadores, dois estilos |
| L06 — instrumento | fechada para o subconjunto | D7 + calibração de operadores, matrizes, codificação, Tw e leading | implementar leitura restrita por Tj; fora do subconjunto falha |
| L07 — CI | fechada | D9 e comando discover lido | prefixo test_; não precisa novo job |
| L08 — composição/nível | fechada | D2 | renderizador/leitor diretos; composição produtiva não é pré-condição |
| L09 — outras certificações | fechada por exclusão | D12 | nenhuma alegação visual/ATS/acessibilidade/leitores/impressão |
| L10 — dependência/experimento | fechada | D7/D10 | sem leitor novo nem alteração temporária de ambiente |
| L11 — evidência | fechada | D11 | PR basta, sem docs/binários |
| L12 — processo | fechada para análise | decisões atuais + contrato da skill relido | proposed e handoff valid; implementação exige invocação própria da versão exata |

Lacunas gerais fora da fatia permanecem como limites, não bloqueios escondidos:
| Limite | Opções | Recomendação / responsável | Insumo para outra decisão |
|---|---|---|---|
| visibilidade real da tinta, leitores, impressão, ATS e acessibilidade | campanha específica ou excluir alegações | excluir nesta entrega, conforme D12; produto/design | leitores/versões, corpus, requisitos e oráculos próprios |
| outros operadores/fontes/layouts futuros | ampliar subconjunto validado ou falhar explicitamente | falhar e pedir nova revisão; engenharia | PDF reproduzível, operadores novos, controles de coordenadas/estado e limiares aplicáveis |
| máximos de produto | definir limites ou continuar caracterização finita | não inventar máximos; produto | volumes contratuais e política para entradas além deles |

### Perguntas em aberto

Nenhuma decisão adicional é necessária para implementar a fatia definida. O resultado dos futuros testes continua desconhecido. Caso a implementação revele defeito atual ou um operador não coberto, deve produzir achado e interromper a alegação de proteção, sem corrigir produção ou instalar ferramenta. proposed não significa “testes já aprovados”.

### Escopo

Dois arquivos de testes, 11 métodos obrigatórios e N06 opcional agora considerado viável/recomendado; leitura de PDF real, conteúdo, geometria nominal, controles de sensibilidade; execução sem banco, HTTP, frontend ou serviços externos.

### Fora do escopo

Produção, DOCX, estilos/templates de aplicação, HTTP, autenticação/MIME/OpenAPI, cópia histórica, banco/migrations, frontend/E2E, CI/Nix/manifestos de dependência, .gitignore, docs de evidências, rasterização/goldens e novas bibliotecas. Nesta atividade, também é proibido escrever os dois arquivos de teste: só o novo Markdown e temporários de calibração.

### Critérios de sucesso

Decisão do usuário: D1–D12, implementação futura com P01–P06/N01–N05 e, se adotado, N06; zero diferenças textuais não autorizadas; zero marcadores ausentes/duplicados; caixas dentro da área com folga e sem interseção acima de D3; negativos reprovados pela categoria correta; zero skips novos no ambiente fornecido. Inferência de engenharia: validar o instrumento antes de confiar no resultado agregado e comparar baselines por identidade/status, não só contagem. Nenhum critério é apresentado como descrição original do card.

## Restrições aplicáveis

AGENTS raiz/backend continuam exigindo Nix e execução formal de integração em tests, Git fora de Nix, preservação de Clean Architecture e documentação do que/como/finalidade. A nova solicitação autoriza expressamente os diagnósticos temporários em /tmp; é especialização da regra de só escrever análise da skill. Não autoriza testes/produção nesta atividade.

D9 é desvio deliberado da recomendação sem prefixo da v001: o usuário escolheu a descoberta automática no job backend, apesar de ser integração. A execução formal local obrigatória continua em tests. Não se esconde essa divergência de ambiente nem se altera AGENTS/CI para eliminá-la. Como reportlab/pypdf são declarados nos dois shells e nenhum SQLite é necessário, não há dependência ausente que justifique skip novo no CI.

## Classificação comentada

engineering; concerns reliability, implementation e delivery; componente backend; design de teste; risco medium pela possibilidade de falso verde; reversibilidade easy. Incerteza reduzida de high para medium: contrato e viabilidade foram fechados, mas o teste definitivo ainda não foi implementado/executado. Não há mudança material de código que exija reabrir D1.

## Decisão de roteamento

Reinventário das subpastas imediatas: backend, ambientes, frontend, templates, revisao e requisitos. Permanece prompts/backend por continuidade da linhagem e propósito do teste servidor, conforme prompts/README.md. frontend e ambientes são apenas contexto/exclusões; revisao descreve o ato, não o assunto. Nenhum AGENTS.md/AGENTS.override.md adicional foi encontrado sob prompts/backend. Confiança high; não cria pasta nova.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar/direção | Justificativa |
|---|---|---|---|
| correctness | alta | conteúdo completo, limites D3 e sensibilidade real | não confundir assinatura PDF com qualidade de layout |
| reliability | alta | sem rede/banco; controles executados; resultado explícito | evitar falso verde/skip |
| simplicity | média | ferramentas já disponíveis, subconjunto finito | evitar renderer genérico e setup novo |
| delivery-speed | média | dois arquivos, sem mudança de produto | reduzir dependências de outras entregas |
| interoperability | excluída como certificação | somente arquivo/modelos/versões medidos | respeitar D12 |

## Alternativas consideradas

A — Manter só os testes atuais. Executável, porém não atende D3/D8: presença de texto e A4 não detectam coordenadas inválidas ou colisões.

B — Conteúdo integral e caixas nominais por Tj/palavra, pypdf e métricas ReportLab, com sintéticos e patches em memória. Selecionada por D7 e sustentada pela calibração.

C — Rasterização, golden, PyMuPDF ou Poppler. Fora das restrições de D7/D10; não é alternativa viável nesta entrega, mesmo que pudesse ser avaliada em outro trabalho. Não propor instalação se surgir vermelho.

D — Apenas conteúdo completo sem geometria. Viável tecnicamente no ambiente atual, menor custo, mas não atende os critérios de área/sobreposição escolhidos. Não é alternativa suficiente para fechar o card.

Há uma única alternativa que satisfaz simultaneamente as decisões atuais: B. A/D ficam como comparadores do custo e alcance da escolha; C não recebe preferência numérica fictícia por ser incompatível com o escopo.

## Perfil de pagamento comparativo

Escala ordinal, sem somar pontuações. A comparação técnica não substitui as decisões do usuário.

| Dimensão | Prioridade | A | B | D | Confiança | Evidência |
|---|---|---|---|---|---|---|
| correctness | alta | -1 | +2 | 0 | média/alta | B mede posições e tem controles; A/D não |
| reliability | alta | 0 | +1 | +1 | média | B requer qualificar leitura e registrar unsupported |
| simplicity | média | +2 | 0 | +1 | alta | B tem extrator restrito; não requer pacote novo |
| delivery-speed | média | +2 | 0 | +1 | média | custo de implementar instrumentação permanece |
| interoperability | fora da fatia | 0 | 0 | 0 | alta | nenhuma alternativa aqui certifica leitores |

## Histórico e decisão atual

### Decisão da versão anterior

B era recomendada condicionalmente; pending por L01–L03/L06 e handoff ambiguous. Recomendava módulo sem test_ e possível experimento de leitor novo. Essas opções são substituídas por D1–D12.

### (c) Decisão recomendada nesta versão

Status proposed. Implementar B nos dois arquivos definidos por D9, sem alterar ambiente ou produção. Manter o escopo preventivo e as alegações de D12. Incluir N06, cuja viabilidade foi demonstrada, resultando em 12 métodos; os 11 obrigatórios continuam identificados separadamente.

O instrumento deve usar operadores e estado observados, com leitura antes de cada Tj e avanços por fonte/Tw. Não construir caixas a partir do último visitor_text de um parágrafo. Não expandir silenciosamente o subconjunto para aceitar PDFs que o teste não sabe medir.

### Impacto da revisão

decision_impact revised: fecha decisões, muda descoberta/CI e escopo histórico, e acrescenta evidência empírica. A v001 é preservada com seus achados e status original. Nenhum resultado futuro foi promovido a fato observado.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho | Sustentação |
|---|---|---|---|
| correctness | prioritized | detectar posição/colisão/perda na massa definida | D3/D4/D8 + calibração |
| reliability | prioritized | sensibilidade e repetibilidade controladas | mesmos shells/pacotes, invariância e patches com contexto |
| simplicity | prioritized | nenhuma dependência/configuração nova | D7/D10 |
| interoperability | sacrificed nesta fatia | custo de não certificar leitores aceito | D12 |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Atendimento |
|---|---|---|
| correctness | D3, nominal e finito | valores literais e controles limítrofes |
| reliability | zero skips novos; negativos sensíveis | resultados por ID e categoria |
| delivery-speed | dois arquivos, sem serviços/ambiente novo | DTO e bytes em memória |

### Estrutura final e contratos dos helpers

Arquivos futuros, não criados nesta revisão:
1. src/backend/tests/test_integracao_regressao_pdf_layout.py — unittest.TestCase, classe RegressaoPdfLayoutIntegracaoTestCase, 11 métodos obrigatórios e N06 recomendado. Usar subTest para variações, sem multiplicar métodos nem marcar expectedFailure.
2. src/backend/tests/fixtures/pdf_layout.py — dados e instrumento exclusivos da suíte; quatro funções públicas abaixo, tipos de resultado e auxiliares privados estritamente necessários. Nenhum desses artefatos é importado por produção.

Assinaturas propostas como contrato de implementação (definição de engenharia desta revisão):

    criar_documento_pdf_layout(cenario: str, *, modelo: str = "classico", comprimento_token: int | None = None, campo_token: str | None = None, subcaso: str | None = None) -> CasoPdfLayout
    extrair_geometria_pdf(conteudo: bytes) -> GeometriaPdf
    auditar_pdf_layout(conteudo: bytes, *, esperado: tuple[CampoEsperado, ...], modelo: str) -> RelatorioPdfLayout
    criar_pdf_controle_defeituoso(tipo: str, *, variante: str = "padrao", dx: float | None = None, dy: float | None = None) -> ControlePdfLayout

Discriminantes finitos: cenario aceita P01 a P06 e N06; campo_token em P03 é D ou C e comprimento_token é 512 ou 2048; subcaso em P05 é opcionais, sem_secoes ou caracteres. O criador de controles aceita tipo fora_area, sobreposicao, conteudo_ausente ou instrumento; variante identifica valido, padrao (defeituoso), mediabox, ctm, duplicado, diferenca_textual, limiar, fonte, rotacao ou clipping conforme o cenário. Parâmetro fora dessa tabela é erro do teste, não skip nem geração genérica.

Responsabilidades:
- criar_documento_pdf_layout entrega documento e manifesto textual independentes. Para normal usa a fábrica pública → PreviaVersaoCurriculo → montar_documento_renderizado; sanitiza/marca o DTO antes da geração. Nos demais, constrói diretamente os DTOs imutáveis. Não lê constantes de geometria do renderizador para produzir o esperado.
- extrair_geometria_pdf abre os bytes, valida subconjunto/fontes/caixas/estado, extrai runs em ordem de emissão com CTM/Tm, calcula quatro cantos e guarda caixas por página. Não decide sozinho se o currículo está aprovado.
- auditar_pdf_layout chama o extrator, compara conteúdo e multiplicidade com manifesto, aplica área e interseção e retorna todos os problemas mensuráveis. Só ausência de dependência gera skip na suíte; incompatibilidade do oráculo levanta erro explícito.
- criar_pdf_controle_defeituoso produz bytes sintéticos ReportLab e manifesto completo que deveria ser visível, além da categoria/pares esperados; preserva o par positivo correspondente. Também serve aos subcasos numéricos de N04, sem duplicar algoritmo de auditoria. Não chama renderizador para simular defeito geométrico sintético; N05/N06 usam explicitamente o renderizador real no módulo de teste.

Tipos e relatório:
- CasoPdfLayout: documento, esperado, identificação de cenário/modelo; esperado é tuple de CampoEsperado.
- CampoEsperado: id de campo, marcador_inicio, marcador_fim, texto literal integral e token_sem_quebra opcional. O esperado não é obtido lendo o PDF nem importando _texto.
- GeometriaPdf: páginas (número a partir de 1, MediaBox/CropBox efetivas, Rotate, UserUnit), runs ordenados (ordem de emissão, texto, fonte, tamanho, CTM, Tm, quatro cantos e caixa).
- RelatorioPdfLayout: estado “aprovado”/“reprovado”, páginas analisadas e tuple de problemas. Tipo de problema: fora_area, sobreposicao ou conteudo_ausente. Duplicação ou divergência textual usa conteudo_ausente com motivo discriminado “duplicado”/“diferenca_textual”; não significa literalmente que duplicata esteja ausente.
- Problema: tipo, motivo, pagina (ou None se não localizável para conteúdo ausente), marcadores/ids de campos, caixa_a, caixa_b quando houver par, fonte/tamanho de cada run, profundidade_x/profundidade_y no par e invasões por lado em fora_area. Incluir texto curto do run e posição de emissão para identificar fragmentos cujo marcador está em outra linha.
- OraculoPdfNaoSuportado: exceção de asserção com prefixo literal “oráculo não suporta ...”, página, operador/recurso, operandos relevantes e contexto. Não converter em relatório aprovado nem em skip. Fonte, rotação, clipping, imagem, máscara ou operador fora do whitelist entram aqui.
- A suíte mantém estado de execução separado do relatório de PDF: “executado e aprovado”, “executado e reprovado”, “não executado por ambiente”. Um negativo pode ter PDF reprovado e teste aprovado, com esse resultado registrado claramente.

Todas as funções/classes, inclusive tipos de teste, terão docstring explicando o que fazem, como e para quê, além de comentário de proveniência com caminho e v002 exatos. Não refatorar produção ou outros testes para facilitar imports.

### Subconjunto validado e algoritmo restrito

1. Ler ContentStream e recursos antes de disparar extração. Whitelist inicial: cm, q, Q, BT, ET, Tf, TL, Tm, Tj, T*, rg, Tw. Validar operandos, números finitos, pilha balanceada, texto dentro de BT/ET e fontes resolvidas. Não aceitar silenciosamente operador apenas porque parece inofensivo.
2. Página A4 retrato, MediaBox com origem zero e medidas aprovadas, Rotate=0, UserUnit efetivo 1. Resolver herança de caixas pela página, obter CropBox efetiva e sua interseção com MediaBox. Área auditável é a interseção da área aprovada com as caixas visíveis efetivas; não basta comparar largura da folha.
3. Fontes permitidas: Type1 Helvetica/Helvetica-Bold/Helvetica-Oblique, WinAnsiEncoding sem redefinição/Differences. Strings dos Tj pelos bytes originais cp1252. Recusar fonte sem mapeamento ou encoding diferente. Nada de consultar fontes do sistema.
4. Manter fonte, tamanho e Tw (inclusive negativo) com salvamento/restauração q/Q. Estados Tc=0, Tz=100, Ts=0 e renderização de texto padrão; como não foram emitidos operadores de mudança desses estados, a presença de Tc/Tz/Ts/Tr é unsupported até nova calibração. TJ, Td/TD, aspas de texto, path/clipping e Do/BI/gs também ficam fora; não implementar leitor genérico para justificá-los.
5. CTM suportada: identidade, translação e escala positiva sem rotação/shear; Tm observada com parte linear identidade e origem local variável. Qualquer componente de rotação/reflexão/shear fora disso é unsupported. Aplicar Tm e CTM aos quatro cantos mesmo no caso simples; não usar só origem nem somar offsets presumindo matriz identidade.
6. Em visitor_operand_before de cada Tj, fotografar CTM/Tm e estado ativo; pypdf resolve Tm/T*/cm no subconjunto. Não tomar o tm de visitor_text agregado como origem de todas as linhas. Validar que cada Tj do conteúdo foi representado uma vez. Sequência de vários Tj sem posicionamento/avanço validado não pode reutilizar origem silenciosamente: rejeitar estrutura fora do padrão medido ou validá-la em revisão.
7. Avanços por caractere = largura de métrica da fonte escalada pelo tamanho, mais Tw para cada espaço de código 0x20. Largura total soma os avanços. Ascendente/descendente vêm de pdfmetrics.getAscentDescent. Para reduzir caixas vazias, dividir run em palavras por espaços reais; o avanço dos espaços reposiciona a próxima palavra, mas espaço sozinho não vira objeto de colisão. Nunca dar uma caixa a um parágrafo multilinha.
8. Calcular retângulo nominal local de cada palavra/run, transformar quatro cantos e tomar envelope em coordenadas da página. Comparar palavras/runs distintos na mesma página, inclusive mesma seção; não excluir pares por compartilharem título/parágrafo, nem deduplicar por coordenada. Duas cópias desenhadas no mesmo lugar devem ser detectáveis.
9. Guardar ordem de emissão para conteúdo. Extrair texto também com pypdf para conferir a correspondência de caracteres; a reconstrução controlada dos campos não depende de ordem inferida por ordenação visual. Detectar qualquer diferença de texto/contagem. Alteração do leitor que mude esse comportamento exige investigação, não atualização cega de esperado.
10. Recursos inesperados que possam pintar/ocultar conteúdo (XObject, imagens inline, máscara, ExtGState não validado) devem falhar antes da aprovação, inclusive se não forem percebidos por um callback textual. Não é prova de tinta: é um domínio de medição explicitamente restrito.

### Limiares aprovados e normalização

Origem de todos os números de aceite desta seção: decisão do usuário D3, classificados como heurística de engenharia, ajustável por design. Os valores coincidem com parte da implementação atual, mas sua adoção como oráculo foi decisão, não descoberta de requisito de produto.

| Propriedade | Valor literal no teste | Regra |
|---|---|---|
| página | W=595.27559055, H=841.88976378 pt | erro absoluto por dimensão ≤0.05 |
| margem clássica | 56.69291339 pt | área [m,m,W−m,H−m] |
| margem compacta | 42.51968504 pt | mesma expressão |
| folga externa | 0.5 pt em cada lado | caixa não pode ultrapassar a área efetiva além disso |
| sobreposição | dx>0.5 E dy>0.5 | dx=min(xmax)-max(xmin), dy=min(ymax)-max(ymin), par da mesma página |
| conteúdo | zero ausente/duplicado/diferença não autorizada | comparar todo o manifesto, além de marcadores |
| controles de limiar | 0.49 e 0.51 por eixo e por lado | não arredondar antes de classificar |

Valores não são lidos de ESTILO_*/A4 do renderizador em cada execução. Não acrescentar padding de Frame. Não aumentar .5 nem .05 para fazer um caso passar. Arredondamento é só para diagnóstico impresso, nunca para a decisão.

Normalização explícita:
- O conjunto normal usa espaços ASCII, quebras CR/LF e rótulos literais; transformar CRLF/CR em LF, tratar quebras entre palavras e sequências de espaços ASCII de apresentação como um único espaço; aparar bordas do campo. Preservar todo acento e pontuação.
- Percorrer campos pelos marcadores únicos, preservando ordem e exigindo cada início/fim exatamente uma vez. Comparar todo o conteúdo entre marcadores e todo o stream esperado, incluindo separadores de contato “ | ” e seções/campos na ordem. Texto extra fora do manifesto também é divergência.
- Para token longo explicitamente cadastrado no manifesto, recompor somente segmentos consecutivos do mesmo token separados por quebra de linha/página introduzida pela geração, entre suas sentinelas. Não remover todos os espaços do PDF e não aplicar recomposição a qualquer palavra. Usar a concatenação de runs e seus limites conhecidos para o caso em que o leitor não insere newline; não perder fragmento curto de sentinela.
- P05 tem esperado literal “Nota ? ok” para entrada “Nota ✓ ok”. Não chamar _texto para calculá-lo e não normalizar qualquer “?” como se fosse equivalência universal.

### Dados sintéticos exatos e marcação

Convenção comum de engenharia para tornar D4 executável: em cada caso, atribuir IDs em ordem de emissão, F000, F001, ...; valor não vazio vira “FnnnI <valor literal> FnnnZ”. Subtítulo/período None não têm marcador nem texto. O manifesto é construído dos valores de entrada conhecidos, com esperado de conversão especial escrito separadamente; nunca da saída do renderizador. Recomeçar numeração por PDF é permitido, pois auditorias não misturam documentos.

Cabeçalho-base de DTO: nome Pessoa Sintética; email pessoa@example.invalid; telefones=(); endereco=None; cidade=None; linkedin=https://example.invalid/perfil; curriculo_lattes=None. titulo_versao="Regressão PDF sintética"; nome_arquivo_base="curriculo-sintetico". Esses metadados não viram texto esperado se não são desenhados. Marcação aplica-se aos textos desenhados, incluindo títulos de seção, títulos de bloco e cada detalhe.

P01 usa a fábrica pública e monta a prévia com uma formação, uma experiência, um projeto, as competências/idiomas e documentos=(). Após montar o DTO, substitui cabeçalho e metadados pelos valores acima e aplica marcação. Textos das seções/blocos preservados da fixture devem ser listados literalmente no manifesto, incluindo:
- Formação acadêmica; Tecnologia em Análise e Desenvolvimento de Sistemas; Faculdade de Tecnologia de São Paulo (FATEC-SP) - Tecnólogo; 02/2023 - previsão 12/2025; Situação: Em andamento.
- Experiência profissional; Estagiária de Desenvolvimento de Software; Empresa de Soluções Tecnológicas Ltda; 01/2024 - atual; descrição literal “Atuação no desenvolvimento de APIs RESTful utilizando Python e FastAPI, modelagem de banco de dados relacional e criação de suítes de testes automatizados para controle de qualidade de software.”
- Projetos acadêmicos; Sistema de Apoio Curricular Profissional; descrição literal “Plataforma completa para centralização de perfil estudantil, assistência na redação de trajetórias acadêmicas e exportação automatizada de currículos.”; “Tecnologias: Python, FastAPI, TypeScript, React, PostgreSQL, Nix”.
- Competências; Python e Clean Architecture / Técnica - Avançado; FastAPI e APIs RESTful / Técnica - Intermediário.
- Idiomas; Inglês / Avançado; Espanhol / Intermediário.

P02: uma seção EXPERIENCIAS_PROFISSIONAIS, título “Experiência profissional”; i=0..39, BlocoDocumento(titulo="Bloco {i:02d}", subtitulo="Subtítulo {i:02d}", periodo="01/2024 - 12/2024", detalhes=(" ".join("V{i:02d}_{j:02d}" para j=0..29),)). Aplicar a marcação comum por campo. Esses tokens são únicos por bloco/detalhe.

P03: N em {512,2048}, campo em {D,C}. Prefixo="I"+campo+N em quatro dígitos, sufixo="F"+campo+N em quatro dígitos; token=prefixo+"X"*(N−len(prefixo)−len(sufixo))+sufixo. Assim, IDs de sentinela são ID0512/FD0512, IC0512/FC0512, ID2048/FD2048 e IC2048/FC2048. N é comprimento do token, sem a URL. Detalhe recebe token puro; contato linkedin recebe "https://example.invalid/"+token. Uma seção PROJETOS_ACADEMICOS “Projetos acadêmicos”, bloco “Bloco token”; nos casos de contato, detalhe literal “Detalhe curto”. Aplicar marcas comuns fora do token; cadastrar exatamente qual token pode ser recomposto.

P04: uma seção PROJETOS_ACADEMICOS, um bloco título “Bloco extenso”, subtitulo="Subtítulo sintético", periodo="01/2024 - 12/2024"; detalhes j=0..119, cada um “D{j:03d} Ação sintética FIM{j:03d}”, com marcação única por detalhe.

P05: subcasos em um único método: (a) cabeçalho com opcionais None e telefones=(), bloco “Opcional” com subtitulo/periodo None e detalhes=(); (b) cabeçalho apenas com seções=(); (c) título “Ação <REST> & ç” e detalhe “Nota ✓ ok”, esperado “Nota ? ok”. Não tornar nome/email obrigatórios vazios nem inventar regra de validação de formulário.

P06: valores literais classico, compacto, ats-simples, criativo, moderno, academico, primeiro-emprego, padrao_fatec, confrontados com a enumeração para sinalizar expansão do catálogo. Mesmo documento sintético curto nos oito, uma seção PROJETOS_ACADEMICOS, bloco “Modelo sintético” com subtítulo e detalhe “Conteúdo de modelo”. Valores literais de corpo 10.5/9 e nome 21/18 podem caracterizar estilo; todos os não compactos devem ter a mesma geometria/conteúdo que classico quando só modelo varia. Isso não estabelece oito layouts PDF.

Os parâmetros dos controles negativos estão definidos nos cenários abaixo. Dados vêm de fixtures sintéticas, sem consulta/serviço externo. Não usar dados pessoais reais de usuário.

### Cenários finais

Pré-condição comum: dependências existentes, ambiente tests, dados novos por caso, bytes em memória, invariante=True, D3 literal e manifesto independente. Passos positivos comuns: criar caso → renderizar → auditar → exigir relatório aprovado/sem problemas → verificar condições adicionais. Passos negativos: gerar par controle válido/defeituoso → aplicar o mesmo auditar_pdf_layout/esperado/área → exigir válido aprovado e defeituoso reprovado com categoria e evidência corretas. Nenhum expectedFailure.

Todos são integration na fronteira produtor real/leitor real; atributo medido é conteúdo/geometria nominal. Nos sintéticos, o produtor real é Canvas ReportLab. As variações são subTest, mantendo o número de métodos.

| ID / método | Objetivo, dados e passos específicos | Oráculo e resultado esperado | Fonte / origem do critério |
|---|---|---|---|
| P01 test_pdf_normal_respeita_area_e_preserva_conteudo | positivo em classico/compacto com a cadeia da fixture e os dados/marcas acima | conteúdo completo, caixas aprovadas nos dois estilos; não exigir uma página | fixture + DTO + gerador revalidados; decisão do usuário D2/D3/D4 |
| P02 test_quarenta_blocos_preservam_todos_os_detalhes | P02 exato acima, dois estilos; auditar todos os campos, não apenas títulos | >1 página; nenhuma perda/duplicação/colisão/invasão; não exigir exatamente duas | teste atual de 40 itens e Paragraph; D3/D4/D5; marcação é definição de engenharia |
| P03 test_texto_longo_e_url_sao_preservados | 2 comprimentos × 2 campos × 2 estilos; tokens/sentinelas exatos acima | recuperar integralmente cada token pela recomposição restrita e aprovar todas as linhas/caixas | calibração de tokens + D4/D5; caracterização finita |
| P04 test_bloco_maior_que_pagina_preserva_linhas | 120 detalhes, dois estilos | >1 página; todos os detalhes na ordem e caixas aprovadas; não exigir bloco indivisível | KeepTogether “quando possível”, calibração 4 páginas; D5 |
| P05 test_campos_opcionais_e_acentos_sao_caracterizados | três subcasos acima, dois estilos | não desenhar None; conteúdo literal representável intacto; ✓ → ? explicitamente; geometria aprovada | _cabecalho/_bloco/_texto, D4 e escopo de opcionais implementado; caracterização |
| P06 test_catalogo_pdf_caracteriza_fallback | oito identificadores e documento curto comum | sete não compactos equivalem ao clássico; compacto tem geometria/estilo próprio; todos passam auditoria | enum/mapa revalidados; D6, sem fidelidade visual |
| N01 test_detector_rejeita_texto_fora_da_area | Helvetica 12, A4, dois campos “ALFA” e “OMEGA” marcados; controle em (100,200)/(100,160); variante desloca ALFA para xmin=margem−10; outra para x=-10; tudo ainda extraível | relatório reprovado, tipo fora_area com página/caixa/marker. Controle válido aprovado | Canvas/pypdf calibrados; D3/D8; posições definidas tecnicamente |
| N02 test_detector_rejeita_sobreposicao | Helvetica 12; dois textos únicos marcados; controle em y=200/180, x=100; defeituoso ambos em (100,200); subcaso com tradução de CTM | sobreposicao, identifica dois runs/ids e dx/dy>0.5; conteúdo não é omitido/deduplicado. Controle separado aprovado | D3/D8 + calibração de matrizes |
| N03 test_detector_rejeita_texto_ausente | manifesto contém “F000I ALFA F000Z” e “F001I OMEGA F001Z”; PDF defeituoso omite apenas o segundo campo; posições válidas | conteudo_ausente motivo ausente; controle completo aprovado. Subcasos adicionais duplicam campo ou trocam pontuação e devem apontar duplicado/diferenca_textual | D4/D8; controle semântico definido por engenharia |
| N04 test_detector_valida_transformacoes_e_limites | controle traduzido/escalado e restaurado com “Ação CONTROLE” Bold 12 em (10,20) sob CTM (1.25,0,0,0.75,100,200), “ITÁLICO” Oblique em (50,100); pares de textos marcados “F000I M F000Z” e “F001I N F001Z”, primeiro em (100,200), segundo em (100+stringWidth(primeiro, Helvetica,12)−dx,200+11.1−dy), dx/dy de .49/.51; oito invasões externas dos quatro lados; formas fora do subconjunto | origens 112.5/215 e 50/100, quatro cantos coerentes; somente .51/.51 colide; .49 externo passa e .51 reprova. Fonte Times-Roman, rotação por cm, clipping e operador fora do whitelist devem levantar “oráculo não suporta ...”, não skip. Comparação de coordenadas de calibração pode usar precisão diagnóstica 1e-4 pt, sem alterar limiares D3 | medição efetiva desta revisão; D3/D7/D8. Precisão diagnóstica é escolha técnica, não folga de aprovação |
| N05 test_detector_rejeita_regressao_real_de_margem | documento normal; controle real sem patch; em cada modelo, patch.dict no mapa com replace(estilo, margem_cm=0.5), gerar e auditar com margem original literal | válido passa; mutante acusa fora_area; depois do contexto mapa/resultado controle restaurados. Confirmar alteração real dos bytes/coordenadas, não só do objeto de estilo | .get do gerador e calibração xmin=20.17323; D8 |
| N06 test_detector_rejeita_leading_reduzido_em_memoria | opcional viável e recomendado; detalhe único “L000 L001 ... L119” com marcas próprias, dois estilos; patch da função _estilos, chamando original e clonando corpo com leading=1 | controle original passa; mutante gera colisões entre linhas e acusa sobreposicao; restauração em contexto/finally; não duplicar markers para fabricar colisão | função atual + mutação calibrada; decisão do usuário D8 e recomendação de engenharia |

R01/R02 foram removidos do conjunto de cenários. Não se gera nem baixa cópia de versões históricas. Não há cenário Letter/paisagem não implementado.

### Sensibilidade, falhas atuais e honestidade

N01–N05 são obrigatórios. N06 foi demonstrado viável; implementar os 12 é a recomendação desta versão, sem skip condicional que o transforme em teste contado e não executado. Se o executor entregar somente os 11 obrigatórios, registrar explicitamente a opção no PR; não contar método inexistente nem exigir 12 por total sem IDs.

Negativo aprovado significa: controle positivo passa e o detector reprova o PDF defeituoso com a categoria esperada e a evidência que localiza o defeito. Exigir apenas “qualquer AssertionError” não basta. N04 deve capturar especificamente OraculoPdfNaoSuportado nos subcasos fora do instrumento. Nos demais negativos, unsupported é falha do teste, não sensibilidade demonstrada.

Falha atual encontrada em P02/P03/P04 ou outro positivo é achado. Preservar o teste que a evidencia e reportar revisão/handoff, sem corrigir PDF, alargar tolerância, expectedFailure ou skip por layout. Um parser que não suporta a saída medida bloqueia a alegação até investigação; não justifica instalar PyMuPDF/Poppler nesta entrega.

### Determinismo, isolamento e skips

Usar invariante=True, BytesIO, datas/UUID fixos da fixture e DTOs recém-construídos. Não usar data/hora, aleatoriedade ou ordem não especificada para os dados. TZ=UTC e LC_ALL=C.UTF-8 efetivamente funcionaram na calibração; não depender de locale implícita. Fontes e métricas padrão já declaradas, sem rede/fonte do host.

PDFs/imagens não são gravados no repositório nem entram no commit. Se diagnóstico exigir disco, somente TemporaryDirectory(prefix="pdf-layout-", dir="/tmp") com cleanup em finally/context manager. A revisão usou um diretório temporário exclusivo para scripts/logs, removido ao final; o código final não precisa guardar PDFs. Patches sempre com contexto, sem alteração global persistente entre métodos.

Imports opcionais protegidos somente por ModuleNotFoundError cujo name seja exatamente reportlab ou pypdf. No caso de um subpacote/erro interno inesperado, relançar, não mascarar. A classe de teste deve continuar importável sem executar helper que já exija a biblioteca; marcar todos os métodos com motivo explícito “ambiente: reportlab/pypdf ausente; executar nix develop .#tests ...” nesse único caso. Não levantar SkipTest durante import que faça o módulo virar um único skip e esconda as identidades dos métodos.

Erro de PDF, fonte/operador inesperado, compatibilidade do oráculo, ausência de marcador, mutação ineficaz ou falha atual não viram skip. Esperado nos shells fornecidos: zero skips novos, pois as duas bibliotecas existem. Resultado todo ignorado é “não executado”, nunca “protegido”. O PR deve listar os IDs e status, separando resultado do teste e resultado do PDF negativo.

Alegações permitidas após controles aprovados: presença/multiplicidade do texto sintético e ausência de invasão/interseção das caixas nominais no subconjunto validado, nos modelos, volumes e versões medidos. Proibidas: ausência universal de corte/sobreposição, fidelidade à prévia HTML, legibilidade humana, acessibilidade, leitores específicos, ATS, impressão, todos os dados possíveis ou proteção de correções históricas. Origem: decisão do usuário D12.

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda | Severidade | Afetados |
|---|---|---|---|
| correctness | texto extraível em posição inválida passa sem geometria | alta | estudante/engenharia |
| reliability | negativo não detectado dá falsa confiança | alta | manutenção |
| simplicity | dependência externa bloqueia execução e CI | média | equipe |

### Custos aceitos para priorizá-las

| Prioridade favorecida | Custo aceito | Dimensão prejudicada | Justificativa |
|---|---|---|---|
| correctness | manter extrator restrito e controles | delivery-speed | calibração torna implementação delimitada |
| simplicity | métricas compartilhadas com gerador | independência da prova | risco exposto e limitado por controles geométricos conhecidos |
| delivery contínuo | suíte integrada também descoberta no job chamado unitário | clareza de nomenclatura/ambiente | D9 deliberado; execução formal em tests preservada |
| confiabilidade da alegação | não certificar tinta/leitores | alcance | D12 define limite aceitável |

## Riscos e efeitos de segunda ordem

Caixa nominal não representa exatamente contorno de tinta; acentos/itálico podem ter overhang e métricas compartilhadas podem conter erro comum. Não há rasterizador independente nesta entrega. O fallback de modelos não garante aparência específica. Um teste que aceite operador/recurso não medido pode dar falso verde; por isso o whitelist é parte do contrato, e mudança de biblioteca/gerador exige revalidação.

### Achados mantidos e novos, sem correções

| Achado | Evidência atual ou proveniência | Tratamento |
|---|---|---|
| interpretação histórica inicial incorreta | Git relido + D1 | resolvida no enquadramento, sem mudar os commits |
| aplicação produtiva sem exportação composta | main.py / factory relidos | mantido fora do escopo direto |
| sete modelos e só dois estilos PDF | enum/mapa relidos | fallback caracterizado por D6 |
| KeepTogether não promete indivisibilidade de bloco grande | código e 120 detalhes em quatro páginas no diagnóstico | não impor promessa universal |
| comentário frontend diz que gerador não existe | jornada .e2e relida versus renderizador existente | comentário desatualizado quanto à existência; simulação permanece |
| CSS print/DOM não prova saída ReportLab | @media print relido e pipeline sem HTML | nenhuma regra transposta |
| guia/manual sobre disponibilidade envelheceram | guia relido; manual é achado histórico da v001, não reauditoria integral | distinguir gerador existente e composição ausente |
| evidência F11.12 afirma conformidade visual/zero falhas ampla | trechos relidos versus cinco métodos relidos | asserções não sustentam toda a alegação |
| análise anterior diz “nunca”/“qualquer leitor” | prompts/backend/20261026... linhas 129/222 relidas | não herdado como garantia |
| ADR-005 intitula-se ADR-004 e é Proposto | cabeçalho relido | não corrigido |
| job “unitários” descobre integrações | ci.yml relido e baseline | D9 aceita descoberta; não reclassificar a suíte |
| skips de SQLite/composição no backend | baseline atual, mesmas 84 identidades | não chamar toda integração de executada |
| Node global herdado no shell tests | achado histórico da v001, não reprobe nesta revisão | irrelevante à fatia Python; não usar nem alegar nova medição |
| Tw negativo em PDF normal | calibração: -0.120445 | novo: largura não pode ignorar espaçamento de palavra |
| visitor_text agrega várias linhas sob leading pequeno | N06: 18 Tj / cinco visitors | novo: medir cada Tj com matrizes antes da operação |
| token pode partir a própria sentinela | oito casos de token | novo: não selecionar fragmentos por sentinela inteira; recompor só o campo conhecido |
| fonte padrão sem embedding examinado | fontes Type1/WinAnsi sem descriptor nos casos | novo: não certificar aparência entre leitores |
| redução só da variável compacta pode ser mutação ineficaz | mapa guarda instância de estilo | novo: patch.dict no mapa, conforme calibração |
| blocos maiores que página geram mais de duas páginas | diagnóstico de 120 detalhes | novo: quatro páginas observadas, sem fixar esse total no teste |
| primeiro diagnóstico ignorava Tw na estimativa de largura | roteiro temporário corrigido após inventário | a decisão usa a medição final com Tw; não se amplia limiar para encobrir instrumento incompleto |

Nenhum achado de layout da saída completa é afirmado como corrigido. Não foi implementado auditor completo nesta atividade para declarar “zero colisões” em toda a massa.

## Validação da decisão

### Baseline reexecutado e comparação por identidade

Ambiente original, sem mudanças Nix/manifestos. Os comandos usaram --offline --no-write-lock-file, env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src TZ=UTC LC_ALL=C.UTF-8. Backend completo:

    nix develop .#backend --offline --no-write-lock-file --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src TZ=UTC LC_ALL=C.UTF-8 python -m unittest discover -v -s src/backend/tests -t src

Resultado observado: exit 0, 1.126 testes, 67.988 s, 84 ignorados, zero falhas e erros; 1.042 executados/aprovados. Mesmos IDs da v001, sem desaparecimento/adição/duplicação de ID. SHA-256 de "\n".join(sorted(ids))+"\n":
- todos os 1.126 IDs: cf356054397768a2facaae1b98cb32bfbf176328abfeea6abfff23021cc1c2be — igual à v001;
- os 84 IDs efetivamente ignorados no log desta execução: 945e56ba4008718246f4771676c17b7fd198214570ee93d551b481b640971786 — igual à v001.

Assim, a comparação é por identidade, não só por total. O conjunto de failures/errors permanece vazio. Motivos atuais: aiosqlite ausente em 81 casos (12/51/18 com três formulações de motivo); composição de login/autenticador não pronta em um; sessões expirada/revogada não compostas em dois. São preexistentes, não permitem skip nos novos casos PDF.

Execução formal das suítes PDF existentes:

    nix develop .#tests --offline --no-write-lock-file --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src TZ=UTC LC_ALL=C.UTF-8 python -m unittest -v backend.tests.test_infrastructure_renderizador_pdf backend.tests.test_integracao_validacao_pdf_legibilidade

Resultado observado: exit 0, 16 testes, 1.170 s, zero skips/falhas/erros. Inclui os 11 métodos do renderizador e os cinco integrados da evidência existente. Não é execução da nova suíte, que ainda não existe. Não foi executado discover completo em tests nesta revisão: seus casos SQLite dependem de outras condições; não se extrapolam as 84 contagens de backend para esse shell.

Ruff efetivamente executado:

    nix develop .#quality --offline --no-write-lock-file --command ruff check --output-format=github src/backend

Resultado: exit 0, zero diagnósticos de gate. ruff.toml permanece select=["F","I"]. Avisos StarletteDeprecationWarning e duração de tarefas asyncio nos testes antigos não são novos diagnósticos de Ruff. Não houve baseline frontend novo: D2 não muda frontend, e D10 proíbe seus manifestos/configuração; resultados da v001 permanecem históricos, sem alegar reexecução.

### Comandos obrigatórios para o executor futuro

Execução formal:

    nix develop .#tests --offline --no-write-lock-file --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src TZ=UTC LC_ALL=C.UTF-8 python -m unittest -v backend.tests.test_integracao_regressao_pdf_layout

Mesmo módulo no shell do CI, para confirmar ausência de skip novo:

    nix develop .#backend --offline --no-write-lock-file --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src TZ=UTC LC_ALL=C.UTF-8 python -m unittest -v backend.tests.test_integracao_regressao_pdf_layout

Descoberta completa no backend:

    nix develop .#backend --offline --no-write-lock-file --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src TZ=UTC LC_ALL=C.UTF-8 python -m unittest discover -v -s src/backend/tests -t src

Gate real de lint e recomendação de formatação só nos arquivos novos:

    nix develop .#quality --offline --no-write-lock-file --command ruff check --output-format=github src/backend
    nix develop .#quality --offline --no-write-lock-file --command ruff format --check src/backend/tests/test_integracao_regressao_pdf_layout.py src/backend/tests/fixtures/pdf_layout.py

ruff format --check não é gate atual global do backend; é recomendação da revisão restrita aos arquivos novos. Não executar format com escrita em arquivos existentes por conveniência.

### Resultado futuro esperado, ainda não observado

| Entrega escolhida | módulo em tests | módulo em backend | discover backend |
|---|---|---|---|
| 11 obrigatórios | 11 aprovados, zero skips | mesmos 11 aprovados, zero skips | 1.137 total, mesmos 84 skips, zero failures/errors |
| 12 com N06 recomendado | 12 aprovados, zero skips | mesmos 12 aprovados, zero skips | 1.138 total, mesmos 84 skips, zero failures/errors |

Aumentos são de métodos, não de subTest. Comparar conjunto antigo de IDs/status intacto, acrescido exatamente dos IDs listados em Cenários finais sob backend.tests.test_integracao_regressao_pdf_layout.RegressaoPdfLayoutIntegracaoTestCase. Qualquer ID novo ignorado, ID antigo removido ou diagnóstico novo deve ser explicado; não aceitar só “1.138”. Os hashes de todos os testes mudarão com os IDs novos e precisam ser recalculados, não copiados da v001. O conjunto dos skips antigos deve continuar com o mesmo hash, se não houver mudança externa.

### CI contínuo e gates não executados

ci.yml já chama discover no backend; nome test_integracao_regressao_pdf_layout.py entra no padrão test*.py e usa bibliotecas presentes. Proteção contínua futura vem dessa descoberta, sem novo job e sem alteração do workflow. Ainda não há proteção da nova suíte hoje porque seus arquivos não existem; não confundir configuração suficiente com execução já observada.

O job de integração dedicado existente continua executando somente backend.tests.integracao_repositorio_associacao_curriculo_vaga em tests. Um job específico para a nova suíte em tests seria melhoria opcional separada, não pré-requisito de D9 e fora desta entrega. Gates frontend e secrets-scan permanecem no workflow; não foram reexecutados aqui por não serem afetados. Não instalar dependências/npm ci nem fazer build para uma revisão de análise sem delta cliente.

### Matriz de validação da decisão

| Resultado | Evidência atual | Validação futura | Sinal para revisar |
|---|---|---|---|
| enquadramento preventivo correto | histórico e D1 | confirmar mesmo caminho antes de implementar | commit corretivo real ou delta material |
| instrumento viável | operadores/fontes/matrizes/Tw e limiares medidos | extrator definitivo passa N04 | saída medida vira unsupported ou caixas erradas |
| sensibilidade de área | N05 em memória xmin=20.17323 | auditor definitivo acusa fora_area | patch ineficaz ou tolerância derivada do mutante |
| sensibilidade de leading | baselines de 1 pt e bbox de 9.7125 | N06 acusa sobreposicao | visitor agregado encobre linhas |
| conteúdo completo | tokens recompostos nos oito diagnósticos | P01–P06/N03 com manifesto integral | missing, duplicata, pontuação/acentos alterados |
| isolamento | estado de patches restaurado; PDFs só memória | contextos/cleanup mesmo com falha | mutação contamina caso seguinte |
| sem regressão antiga | hashes atuais iguais à v001 | diff de IDs/status/diagnósticos após testes novos | qualquer mudança inexplicada |

## Handoffs e atividades posteriores

### Elegibilidade e executor

A skill .agents/skills/integration-system-testing-v1/SKILL.md e seus test-scope-boundary.md, test-fit-check.md e analysis-input-contract.md foram relidos. Veredito da fatia passou de ambiguous a valid:
1. Resultado é exclusivamente teste, não produto.
2. Fronteira real entre ReportLab e pypdf e atributo de saída, com tipos/cenários identificados.
3. Há limiares aprovados (D3), dados (D4–D6), método (D7) e sensibilidade (D8), acrescidos da calibração.
4. Alvo seguro local, em memória; sem produção/serviço externo ou dependência nova.

O contrato exige cenário/alvo/método/oráculo e valores aprovados para testes não funcionais; D3 e esta revisão atendem essa exigência. A calibração foi feita pela skill de análise conforme autorização específica do usuário, não como execução antecipada do gate de implementação da skill de testes.

Executor recomendado: $integration-system-testing-v1, invocado explicitamente com o caminho exato desta v002 proposed. Essa invocação aprova somente a versão referenciada e a fatia elegível; o pedido atual proíbe implementar e não deve ser tratado como essa invocação. Não precisa nova autorização para Nix, dependência, CI, produção, docs ou serviço: todas essas mudanças estão excluídas.

Alvos do executor: src/backend/tests/test_integracao_regressao_pdf_layout.py e src/backend/tests/fixtures/pdf_layout.py, com comandos e IDs definidos acima. Comentários de proveniência apontam para esta v002. Demais perfis inventariados na v001 continuam sem fatia de implementação aqui: frontend, domínio/orquestração e adapters isolados não substituem teste integrado; cross-cutting não é o objetivo; Nix não será alterado. Nenhuma delegação a subagentes foi realizada.

### Registro mínimo e limites operacionais

Por decisão do usuário D11, o PR deve conter: referência/versão da análise, comandos, versões, IDs/status, resultados dos controles positivos/negativos, limiares e limites de prova. Sem documento em docs/testes/evidencias e sem PDFs/imagens. Não atualizar a evidência antiga para alegar cobertura que ela não tem.

Por D10, não alterar temporária nem permanentemente nix/*, flake.nix, flake.lock, manifestos/locks frontend, ci.yml ou .gitignore. O plano de experimento PyMuPDF/restauração da v001 está retirado. Não há linhas de ambiente a modificar ou restaurar; se faltar recurso, reportar evidência e bloquear a alegação, sem instalar.

Verificar no fim git status --short, git diff --exit-code e git diff --cached --exit-code nos caminhos de ambiente/produção protegidos. Não usar git restore para “limpar” mudanças do usuário; nenhuma restauração foi necessária nesta revisão. A v001, já não rastreada no início, permanece intocada.

O .gitignore lido não ignora genericamente PDF ou pycache; a revisão não o altera. Usar PYTHONDONTWRITEBYTECODE=1 e /tmp; conferir que somente a nova análise é delta desta atividade. A criação de TemporaryDirectory é autorizada para diagnóstico e o cleanup é obrigatório; não remover caches/dependências/arquivos alheios.

### Proveniência da calibração e reprodução mínima

Scripts temporários executados:
- calibrar.py SHA-256 16a4109c747dcba6e9027a88fa633753efa5c08ddd4a54eb5996b6aae231f4eb, versão final incluindo Tw e recuperação do token integral;
- complemento.py SHA-256 af583ff12f194173e9e88cbd028189a93606968999cec49c267fc961608d3d97, versão final com os quatro lados da área e a matriz de interseções. A v001 foi novamente conferida antes da escrita: SHA-256 c8f963dc731d22cad2d1f0e96712ce19b620fe05cc8f7ca56e0932e56fa16128, idêntico ao início.

O procedimento preservado permite reproduzir o diagnóstico sem assumir um detector já implementado: construir os DTOs/controles indicados em Calibração, percorrer ContentStream, registrar recursos/operações, fotografar cm/tm antes de cada Tj e medir pdfmetrics.stringWidth + Tw*n_espaços e getAscentDescent; transformar cada canto local primeiro por Tm, depois por CTM; comparar às coordenadas conhecidas e às profundidades .49/.51. O diagnóstico não usa rasterização nem cria um interpretador genérico. A checagem de token concatena exatamente os runs do campo conhecido, e não uma seleção incompleta por sentinela.

As mensagens/logs/resultados quantitativos necessários estão nesta análise. Scripts e logs de /tmp são removidos ao final, sem anexar binários ou criar teste de produção. Os dois “M” iguais usados no diagnóstico numérico não são o manifesto do teste final: N04 usa os textos marcados distintos da tabela de cenários, com largura recalculada para o primeiro run; a regra de interseção e as profundidades são as mesmas.

## Síntese

A v002 recomenda B com status proposed: contrato preventivo fechado por D1–D12, instrumento restrito calibrado, 11 métodos obrigatórios e N06 viável/recomendado, dois arquivos futuros e descoberta automática pelo CI existente. Permanecem limites declarados de caixas nominais e versões/casos finitos, não bloqueios de produto disfarçados. A implementação dos testes é handoff futuro, autorizado somente pela invocação explícita da skill apropriada com esta versão. Nenhuma produção ou suíte nova foi implementada nesta revisão.

## Apêndice A — Primeira solicitação da linhagem, literal

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

## Apêndice B — Entrada literal desta revisão

<entrada-v002>

$decision-analysis-v4 Revisar prompts/backend/20261031-124820-regressao-pdf-corte-sobreposicao-v001.md e gerar a v002, incorporando as decisões e informações abaixo, para que a análise passe de pending a proposed e seja implementável. Atualize linhagem, "Mudanças desde a versão anterior", lacunas, decisão recomendada, cenários, validação e handoffs. Preserve a v001. Não implemente produção nem testes: as únicas escritas permitidas são o novo artefato de análise e arquivos temporários em /tmp (calibração abaixo).

## Regra principal: não presumir
Valem as regras da v001: fatos com caminho e trecho, lacunas separadas de recomendações, divergências apontadas sem escolha silenciosa. Decisão fornecida pelo usuário entra com origem "decisão do usuário" e os limiares como "heurística de engenharia, ajustável por design", e não como fato de artefato. **Não confie na v001: reverifique por leitura os fatos-chave** e registre qualquer diferença.

## Decisões do usuário (tratar como requisito)

D1. **Enquadramento (fecha L01).** Os commits 84e3a5b (renderizador PDF, #230) e 4ad3416 (renderizador DOCX, #231) são introduções de formato, não correções, e não existe commit posterior que altere `renderizador_pdf.py`. O card é tratado como **proteção preventiva do gerador PDF introduzido em 84e3a5b**. O 4ad3416 fica fora do escopo do PDF. Remova R01 e R02 e **não alegue proteção de "duas correções históricas"**. Se, na releitura, aparecer commit corretivo real de layout PDF, reporte-o, mantenha `pending` e liste o insumo exato.

D2. **Nível (fecha L08).** Integração na fronteira entre o renderizador real (ReportLab) e o leitor real (pypdf), chamando o renderizador diretamente a partir de `DocumentoCurriculoRenderizado` construído com dados sintéticos e, para o controle de conteúdo normal, de `obter_curriculo_exportacao_fixture` → prévia → `montar_documento_renderizado`. Sem HTTP, banco, rede, front-end nem E2E. Não repita autenticação, MIME nem OpenAPI, já cobertos.

D3. **Limiares (fecha L02 e L03), em pt, heurísticas de engenharia.** Página A4 = 595,27559055 × 841,88976378, erro por dimensão ≤ 0,05. Área útil clássica com margem 2 cm (56,69291339 pt) e compacta com 1,5 cm (42,51968504 pt), **escritas literalmente no teste** (nunca lidas do renderizador a cada execução; não somar o padding de 6 pt do Frame). Folga externa de 0,5 pt por lado para caixas nominais de texto. Sobreposição: reprovar quando a profundidade em x > 0,5 pt **e** em y > 0,5 pt entre caixas nominais de runs/palavras não vazios da mesma página. Integridade de conteúdo: zero marcador ausente ou duplicado e zero diferença textual fora da normalização especificada. Calibre nos controles (0,49 e 0,51 pt por eixo) e não amplie a tolerância depois de um vermelho sem investigar.

D4. **Conteúdo.** Marcadores únicos por campo, bloco e detalhe, com início e fim dos textos longos; comparação integral da sequência normalizada (só quebras e espaços controlados); não remover acentos nem pontuação. A transformação cp1252 (caractere fora do conjunto vira `?`) é **caracterização explícita**, com esperado escrito no teste, sem importar `_texto` de produção.

D5. **Volumes (fecha L04), como caracterização finita sem máximos de produto.** 40 blocos (mais de uma página; não exija exatamente duas), token ASCII sem espaços de 512 e de 2048 caracteres em detalhe e em contato (com sentinelas distintas, recompondo só a quebra conhecida), e um bloco com 120 detalhes curtos que não cabe numa página (não exija bloco indivisível). Falha atual encontrada nesses casos vira achado, nunca correção nem rótulo de defeito "corrigido".

D6. **Modelos (fecha L05).** Os sete identificadores de `ModeloCurriculo` e o legado `padrao_fatec` da fixture. Só o compacto tem estilo próprio; os demais caem no clássico: caracterização do fallback, sem alegar fidelidade visual nem layouts PDF específicos.

D7. **Detector (fecha L06).** Alternativa B: `pypdf` mais métricas do ReportLab já instalados, caixas nominais de texto por linha ou run (nunca uma caixa por parágrafo), CTM e matriz de texto aplicadas aos quatro cantos, MediaBox e CropBox efetivas. Sem rasterização, sem imagem de referência, **sem dependência nova** (PyMuPDF e Poppler rejeitados nesta entrega). Operador, fonte, rotação, clipping, imagem ou máscara fora do subconjunto validado deve falhar com "oráculo não suporta ..." e nunca ser ignorado; só ausência de dependência permite skip. Não construa um renderizador PDF genérico.

D8. **Sensibilidade.** (a) PDFs sintéticos defeituosos gerados com ReportLab: texto fora da área (N01), sobreposição (N02), conteúdo ausente (N03) e validação do próprio instrumento com `q/Q`, `cm`, negrito, itálico, acentos e 0,49/0,51 pt (N04); (b) **N05, regressão real de margem**: gerar com o renderizador real depois de reduzir a margem do estilo por patch de escopo em memória (por exemplo `mock.patch.dict` com `dataclasses.replace`, confirmando a forma no código), auditar com a área aprovada de D3 e exigir `fora_area`; (c) N06 **opcional**, só se existir mutação em memória que reduza o leading sem tocar produção; senão, reporte que não é viável. A cópia histórica foi descartada (não há correção a reproduzir). Os pais de 84e3a5b e 4ad3416 não servem de controle (os arquivos não existem lá).

D9. **Arquivos e descoberta (fecha L07), com desvio da v001.** `src/backend/tests/test_integracao_regressao_pdf_layout.py` e `src/backend/tests/fixtures/pdf_layout.py` (nomes de helper: `criar_documento_pdf_layout`, `extrair_geometria_pdf`, `auditar_pdf_layout`, `criar_pdf_controle_defeituoso`). O módulo **tem prefixo `test_`**: precisa só de reportlab e pypdf, presentes nos shells `backend` e `tests`, então é descoberto pelo `discover` do job backend e roda no CI **sem skip e sem novo job**. Registre isso como desvio deliberado da recomendação sem prefixo, ainda com execução formal obrigatória em `.#tests`. Conteúdo: 11 métodos obrigatórios (P01 a P06 e N01 a N05) mais o N06 opcional.

D10. **Ambiente (fecha L10).** Nenhuma alteração temporária nem permanente em nix/, flake.nix, flake.lock, manifestos do front-end, CI ou `.gitignore`. Se a calibração mostrar que isso é insuficiente, registre o bloqueio com a evidência, sem propor instalação.

D11. **Registro (fecha L11).** O texto do PR basta (revisão da análise, comandos, versões, identidades, resultado dos controles, limiares e limites); sem documento em `docs/` e sem anexar PDFs ou imagens.

D12. **Alegações permitidas e proibidas.** Permitido, após os controles aprovados: presença e multiplicidade dos textos sintéticos e ausência de invasão da área e de interseção das caixas nominais no subconjunto validado, para os modelos, volumes e versões medidos. Proibido: "sem qualquer corte ou sobreposição em todo PDF", fidelidade à prévia HTML, legibilidade humana, acessibilidade, leitores específicos, ATS, impressão, todos os dados possíveis e proteção de correções históricas.

## O que a revisão deve fazer

1. **Reverificar por leitura** (sem checkout, switch, stash, reset nem worktree): os dois hashes (ancestralidade, arquivos novos, ausência no pai), a ausência de alteração posterior em `renderizador_pdf.py`, o renderizador atual (estilos, margens, KeepTogether, `_texto`, invariante, fontes), o DTO, a fixture de exportação e a suíte existente de validação PDF (5 métodos).
2. **Calibração somente leitura (insumo de L06).** No shell tests (`nix develop .#tests --offline --no-write-lock-file --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src TZ=UTC LC_ALL=C.UTF-8 python ...`), execute um script **gravado em /tmp** que gere, em memória, PDFs com o renderizador real (clássico e compacto, com a fixture e com um bloco longo) e inventarie: operadores do content stream realmente emitidos, fontes e codificações, uso de `cm`, `q/Q`, `Tm`, `Td`, `T*`, `Tj`, `TJ`, `Tc`, `Tw`, `Tz`, `Ts`, rotação, UserUnit, e o que `visitor_text` do pypdf entrega (texto, matriz, fonte, tamanho) comparado com as posições reais. Registre também se um token longo sem espaços é dividido em linhas e como. **Nada pode ser escrito no repositório**; limpe /tmp ao final. Se a calibração mostrar que o subconjunto necessário é viável, descreva-o; se mostrar bloqueio, mantenha `pending` e justifique.
3. **Fechar L01 a L12** conforme as decisões, registrando a origem de cada uma.
4. **Especificação executável final**, cenário a cenário: ID, método, objetivo, pré-condições, entradas sintéticas exatas (sem dado pessoal; `Pessoa Sintética`, `pessoa@example.invalid`, URLs `example.invalid`), passos, oráculo, resultado esperado, fonte, origem do critério (definido, inferido ou decisão do usuário) e nível. Inclua P01 (controle positivo, dois estilos), P02 (40 blocos), P03 (tokens longos), P04 (bloco maior que a página), P05 (opcionais, acentos e cp1252), P06 (catálogo e fallback), N01 a N05 e o N06 condicional. Especifique as assinaturas e responsabilidades dos quatro helpers, os tipos de defeito (`fora_area`, `sobreposicao`, `conteudo_ausente`, oráculo não suportado), o formato do relatório (página, marcadores, caixas, fonte, profundidades por eixo) e como cada controle negativo termina aprovado quando o detector reprova (sem `expectedFailure`).
5. **Determinismo e isolamento:** renderizador com `invariante=True`, BytesIO, datas e identificadores fixos, `TZ=UTC` e locale explícita, nada de data ou aleatoriedade, nenhum PDF no repositório e temporários só em `TemporaryDirectory` sob /tmp com limpeza em `finally`.
6. **Skips e honestidade:** import protegido só para `ModuleNotFoundError` do `reportlab` ou `pypdf` (motivo explícito); nenhuma captura genérica de erro de leitura, fonte inesperada ou oráculo incompatível (falha ou inconclusão a investigar); resultado todo ignorado é "não executado", nunca "protegido". Diga como o relatório distingue executado e aprovado de ignorado.
7. **Validação:** comandos reais do backend e do CI, descobertos por inspeção: execução formal em `.#tests` (`env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src TZ=UTC LC_ALL=C.UTF-8 python -m unittest -v backend.tests.test_integracao_regressao_pdf_layout`), `discover` completo em `.#backend`, `ruff check` em `.#quality` e, só para os arquivos novos, `ruff format --check` (recomendação, não gate atual). **Remeça o baseline** (referência: 1126 testes, 84 ignorados, 0 falhas e erros, comparados por identidade; hashes SHA-256 da v001) e declare o esperado: 11 testes novos a mais (12 se o N06 existir), **zero ignorados novos**, nos dois shells. O front-end não muda: registre isso sem rodá-lo, a menos que algo o afete.
8. **Handoff:** releia o contrato de escopo e o fit-check de `integration-system-testing-v1` com os limiares agora aprovados e diga se o veredito deixou de ser ambiguous. Se a invocação exigir alguma autorização explícita do usuário, liste. Indique o executor, os dois arquivos e os comandos. Registre que CI contínuo vem do prefixo `test_` e não exige novo job, e que um job dedicado em `.#tests` é melhoria opcional separada.
9. **Achados:** mantenha os da v001 e acrescente os novos (inclusive o que a calibração revelar), sem corrigir nada.
10. **Status:** se o contrato ficar suficientemente definido (limiares, cenários, oráculos, sensibilidade, alegações, calibração do detector e destinatário do handoff), mude para `proposed` e explique o que mudou. Se algo ainda bloquear (por exemplo a calibração do detector), mantenha `pending` e liste exatamente o que falta e quem deve fornecer.
11. Não implemente nada além do novo artefato de análise.

</entrada-v002>

