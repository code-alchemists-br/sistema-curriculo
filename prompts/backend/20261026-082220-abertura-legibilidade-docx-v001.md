---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-26T08:22:20-03:00"
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
    - path: src/backend/infrastructure/exportacao/renderizador_docx.py
      relationship: primary
      representation: source-code
      function: adapter-implementation
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/exportacao_curriculo.py
      relationship: primary
      representation: source-code
      function: api-route
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/exportacao_curriculo.py
      relationship: supporting
      representation: source-code
      function: use-case
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/fixtures/curriculo_exportacao.py
      relationship: supporting
      representation: test-fixture
      function: test-support
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_infrastructure_renderizador_docx.py
      relationship: context
      representation: automated-test
      function: unit-test-suite
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories:
    - prompts/backend
    - prompts/revisao
    - prompts/templates
  confidence: high
  rationale: "Trata da especificação de teste de integração de backend para abertura, legibilidade e conformidade OpenXML da exportação DOCX."
classification:
  sphere: engineering
  concerns:
    - reliability
    - architecture
    - implementation
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: low
  reversibility: easy
  risk: low
---

# Análise de decisão — Teste de Integração de Abertura e Legibilidade do DOCX (Issue #234 [F6.14])

## Solicitação original

Execução da Issue #234 [F6.14]: "Criar teste de abertura e legibilidade do DOCX no aplicativo definido em F1.5."
Planejamento: WBS 1.4.3._, 1.4.4._. Início: 2026-10-26. Entrega: 2026-11-01. Responsável único: @minoruhaga. Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.

## Informações complementares

- O requisito RNF07 estabelece: "A exportação em PDF e DOCX deve preservar o conteúdo, a organização e a legibilidade do currículo, sem cortes ou sobreposições. Exportar currículos em PDF e DOCX e conferir conteúdo, legibilidade e organização nos modelos suportados; aplicativos usados para validar DOCX a definir."
- O card associado F1.5 (#172) estabelece os critérios de aceite da exportação, enquanto o card #412 [F11.13] (atribuído a @xavier-dan) realiza a validação operacional manual. O card #234 [F6.14] exige a automação formal do teste de integração que atesta que o arquivo gerado pelo backend abre sem erros em leitores OpenXML conformes e preserva a organização e legibilidade.
- Na arquitetura do backend:
  - O endpoint `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/docx` orquestra autenticação via cookie de sessão, caso de uso `ExportarCurriculo`, montagem do DTO `DocumentoCurriculoRenderizado` e execução do adaptador `RenderizadorDocumentoCurriculoDocx`.
  - A suíte de testes de integração deve validar a cadeia de ponta a ponta: requisição HTTP autenticada contra a rota da API ou execução do caso de uso com o adaptador real, inspecionando o arquivo de saída via pacote ZIP / OpenXML (`python-docx`), garantindo:
    1. Estrutura ZIP / OpenXML válida e íntegra (`[Content_Types].xml`, `word/document.xml`, `word/styles.xml`, `docProps/core.xml`);
    2. Abertura desimpedida sem aviso de corrupção ou erro de schema por leitores externos;
    3. Conformidade tipográfica e estrutural de legibilidade: títulos com hierarquia navegável ("Heading 1"), regras de paragrafo `keep_with_next` para prevenir linhas órfãs em quebras de página, estilos negrito/itálico em períodos e empresas, e margens definidas por modelo (2.0 cm no clássico, 1.5 cm no compacto);
    4. Omissão absoluta de dados sensíveis e URLs de armazenamento privado (`url_armazenamento`), protegendo a privacidade e segurança do estudante;
    5. Metadados e idioma do documento (`pt-BR`) devidamente marcados.
- De acordo com a governança do repositório ([AGENTS.md](AGENTS.md)):
  - Testes de integração do backend DEVEM ser executados obrigatoriamente no ambiente Nix `tests` (`nix develop .#tests`).
  - Todas as funções, métodos de teste e classes auxiliares DEVEM conter docstrings tripartites completas (_O que faz_, _Como faz_, _Qual finalidade atende_).
  - Rastreabilidade de proveniência formal deve ser inserida no cabeçalho do arquivo de teste.

## Mudanças desde a versão anterior

Nenhum — análise inicial (`mode: initial`).

## Artefatos analisados

| Caminho                                                      | Relação    | Representação  | Função                 | Formato | Recorte    | Estado/revisão |
| ------------------------------------------------------------ | ---------- | -------------- | ---------------------- | ------- | ---------- | -------------- |
| `src/backend/infrastructure/exportacao/renderizador_docx.py` | primary    | source-code    | adapter-implementation | python  | whole-file | working-tree   |
| `src/backend/api/exportacao_curriculo.py`                    | primary    | source-code    | api-route              | python  | whole-file | working-tree   |
| `src/backend/application/exportacao_curriculo.py`            | supporting | source-code    | use-case               | python  | whole-file | working-tree   |
| `src/backend/tests/fixtures/curriculo_exportacao.py`         | supporting | test-fixture   | test-support           | python  | whole-file | working-tree   |
| `src/backend/tests/test_infrastructure_renderizador_docx.py` | context    | automated-test | unit-test-suite        | python  | whole-file | working-tree   |

### Limites da evidência dos artefatos

O renderizador DOCX já está implementado e possui testes unitários de infraestrutura em `test_infrastructure_renderizador_docx.py`. No entanto, inexiste um teste de integração dedicado (`test_integracao_exportacao_docx.py`) que exerça o fluxo integrado através da API/aplicação e audite formalmente os critérios de legibilidade OpenXML, regras de quebra de página (`keep_with_next`), propriedades estruturais e integridade do pacote conforme exigido por F6.14.

## Problema enriquecido

### Resultado desejado

Implementar uma suíte de teste de integração `src/backend/tests/test_integracao_exportacao_docx.py` que gere o arquivo DOCX através da cadeia integrada de exportação e comprove que o pacote é 100% legível, atende ao padrão Office Open XML (ISO/IEC 29500), não possui falhas de abertura e respeita os critérios de legibilidade e privacidade em ambos os modelos (`classico` e `compacto`).

### Atores e interesses

- **Estudante / Usuário:** Deseja baixar seu currículo em formato DOCX e abri-lo perfeitamente no Word ou LibreOffice sem quebras de layout, perdas de formatação ou avisos de arquivo corrompido.
- **Recrutador / Avaliador:** Precisa receber um documento com hierarquia textual clara, títulos destacados, datas organizadas e texto fluido em português.
- **Engenharia de Backend:** Necessita de um teste integrado rápido e automatizado executável no ambiente Nix `tests`, que proteja a exportação DOCX de regressões estruturais.

### Evidências e fatos observados

- O renderizador utiliza `python-docx` e empacota o arquivo no padrão OpenXML (`PK` zip com `word/document.xml`).
- A rota `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/docx` devolve `200 OK` com os bytes do arquivo e o tipo MIME `application/vnd.openxmlformats-officedocument.wordprocessingml.document`.
- As margens configuradas são `2.0 cm` (clássico) e `1.5 cm` (compacto), com tamanho de fonte `11 pt` (clássico) e `9.5 pt` (compacto).
- O cabeçalho usa estilo `Title` para o nome do estudante e `Heading 1` para as seções, com `keep_with_next = True` nos títulos e subtítulos de cada bloco para evitar linhas viúvas/órfãs.

### Hipóteses

- A validação do arquivo DOCX gerado através da leitura com leitor externo (`docx.Document`) e inspeção de XML de baixo nível (`zipfile` e namespace OpenXML) fornece prova determinística de abertura e legibilidade sem necessidade de rodar o Microsoft Word interativamente na esteira de CI.

### Perguntas em aberto

- Nenhuma pendência impeditiva. As fixtures de teste e contratos estão prontos na branch `dev`.

### Escopo

- Criação de `src/backend/tests/test_integracao_exportacao_docx.py`.
- Cobertura integrada da rota da API com cliente de teste FastAPI e caso de uso real de exportação.
- Asserções de abertura, legibilidade tipográfica, conformidade OpenXML e isolamento de dados sensíveis.
- Execução e validação no ambiente Nix `tests`.

### Fora do escopo

- Exportação PDF (coberta pela Fase 4 - Issue #410 [F11.12]).
- Interface web ou componentes React (camada frontend).
- Alterações no código de produção do renderizador ou da rota (apenas adição do teste de integração).

### Critérios de sucesso

- Testes executados com sucesso em `nix develop .#tests --command bash -c "PYTHONPATH=src python3 -m unittest src/backend/tests/test_integracao_exportacao_docx.py"`.
- Linter e formatação Python (`ruff check` e `ruff format --check`) com 0 erros.
- PR criado com CI 100% verde referenciando o fechamento da Issue #234 (`Closes #234.`).

## Restrições aplicáveis

- **Ambiente Nix:** Exclusivamente `nix develop .#tests` para os testes de integração.
- **Docstrings:** Tripartite obrigatória em todas as classes e métodos.
- **Rastreabilidade:** Comentário `# Proveniência: decision-analysis prompts/backend/20261026-082220-abertura-legibilidade-docx-v001.md#v001`.
- **Clean Architecture:** Preservação das fronteiras entre API, Application, Domain e Infrastructure.

## Classificação comentada

- **Esfera:** `engineering` (garantia de qualidade e teste automatizado de integração de backend).
- **Preocupações:** `reliability` (resiliência e conformidade do formato gerado), `architecture` (integração entre camadas) e `implementation` (testes em unittest).
- **Tipo de decisão:** `design` (estratégia de oráculo e validação do artefato de exportação DOCX).

## Decisão de roteamento

- **Raiz:** `prompts`
- **Pasta selecionada:** `prompts/backend`
- **Pastas candidatas:** `prompts/backend`, `prompts/revisao`, `prompts/templates`
- **Confiança:** `high`
- **Justificativa:** Trata da implementação de testes de integração para funcionalidades do backend.

## Dimensões de decisão

| Dimensão      | Prioridade | Limiar ou direção                               | Por que importa                                          |
| ------------- | ---------- | ----------------------------------------------- | -------------------------------------------------------- |
| `correctness` | Alta       | 100% dos testes passando sem falhas             | Previne entregas de arquivos DOCX corrompidos            |
| `reliability` | Alta       | Validação estrita do schema OpenXML e metadados | Garante compatibilidade universal com Word e LibreOffice |
| `simplicity`  | Alta       | Execução em memória sem persistência em disco   | Testes rápidos e determinísticos                         |

## Alternativas consideradas

- **Alternativa A (Recomendada):** Implementar `test_integracao_exportacao_docx.py` utilizando o client de teste da API FastAPI e o motor de leitura OpenXML (`python-docx` + `zipfile`), testando a integridade do pacote gerado de ponta a ponta.
- **Alternativa B:** Depender apenas do teste unitário de infraestrutura existente (`test_infrastructure_renderizador_docx.py`).
  - _Desvantagem:_ Não cobre o fluxo integrado através do endpoint HTTP da API e não testa cenários integrados com os múltiplos modelos e critérios de legibilidade de F1.5.
- **Alternativa C:** Tentar instalar o Microsoft Word ou LibreOffice via CLI no container de CI para executar macros de abertura.
  - _Desvantagem:_ Extremamente pesado, frágil e incompatível com o flake headless leve do projeto; viola as regras de simplicidade e rapidez dos testes.

## Perfil de pagamento comparativo

| Dimensão         | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base                                              |
| ---------------- | ---------: | ------------: | ------------: | ------------: | --------- | ------------------------------------------------- |
| `correctness`    |       Alta |            +2 |             0 |            +2 | Alta      | Alternativa A valida a especificação real         |
| `reliability`    |       Alta |            +2 |            +1 |            +1 | Alta      | Alternativa A audita o OpenXML gerado             |
| `simplicity`     |       Alta |            +2 |            +2 |            -2 | Alta      | Alternativa A roda em < 2s sem ferramentas extras |
| `delivery-speed` |      Média |            +2 |            +2 |            -2 | Alta      | Alternativa A pronta para execução imediata       |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma (versão inicial).

### Decisão recomendada nesta versão

Adotar a **Alternativa A**: criar o teste de integração `test_integracao_exportacao_docx.py` para exercitar a rota integrada de exportação DOCX, confirmando a abertura por leitor externo, a conformidade de cabeçalhos RFC 6266, a hierarquia tipográfica de seções, o controle de quebras de página (`keep_with_next`), as margens dos modelos clássico e compacto e a blindagem contra vazamento de caminhos internos de armazenamento.

### Impacto da revisão

Iniciação formal da implementação da Issue #234.

### Dimensões maximizadas ou priorizadas

| Dimensão      | Estado      | Ganho esperado                                                  | Evidência ou hipótese                      |
| ------------- | ----------- | --------------------------------------------------------------- | ------------------------------------------ |
| `reliability` | maximized   | Garantia de abertura e legibilidade do DOCX em qualquer leitor  | Validação profunda dos fluxos OpenXML      |
| `correctness` | prioritized | Conformidade estrita com RF09, RNF07 e UC08                     | Testes de integração de ponta a ponta      |
| `simplicity`  | prioritized | Testes em memória com execução ultrarrápida no ambiente `tests` | Zero dependências externas não gerenciadas |

### Dimensões satisfeitas por limiar

| Dimensão         | Limiar aceito                                | Como a decisão atende                                     |
| ---------------- | -------------------------------------------- | --------------------------------------------------------- |
| `delivery-speed` | Execução em < 1 hora com revisão em < 10 min | Escopo enxuto, direto e perfeitamente focado no card #234 |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão      | Perda esperada                                                       | Severidade | Afetados                            |
| ------------- | -------------------------------------------------------------------- | ---------- | ----------------------------------- |
| `reliability` | Estudantes baixando DOCX inválidos que não abrem em seus aplicativos | Alta       | Estudantes e recrutadores           |
| `privacy`     | URLs internas de storage vazadas no XML do arquivo DOCX              | Crítica    | Sistema e dados pessoais dos alunos |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade                                  | Dimensão prejudicada | Aceitabilidade                    |
| ------------------- | ------------------------------------------------------ | -------------------- | --------------------------------- |
| `reliability`       | Criação de suíte de testes de integração de exportação | Nenhuma material     | Totalmente aceitável e necessária |

## Riscos e efeitos de segunda ordem

- _Risco:_ Variações na biblioteca `python-docx` causarem diferenças sutis de atributos XML.
- _Mitigação:_ As asserções inspecionam o modelo de objetos de alto nível e partes fundamentais do padrão OpenXML, sem depender de detalhes transientes.

## Validação da decisão

| Hipótese ou resultado                           | Evidência necessária                           | Método                   | Sinal para revisar         |
| ----------------------------------------------- | ---------------------------------------------- | ------------------------ | -------------------------- |
| `test_integracao_exportacao_docx.py` passa 100% | Relatório do unittest no terminal              | `nix develop .#tests`    | Falha em qualquer asserção |
| Rota da API responde 200 com MIME correto       | Asserção do status code e Content-Type         | Cliente de teste FastAPI | Status diferente de 200    |
| Padrões de código e docstrings cumpridos        | `ruff check` e `ruff format --check` sem erros | Nix develop `quality`    | Avisos ou erros de lint    |

## Handoffs e atividades posteriores

- Implementação do teste de integração via `$integration-system-testing-v1`.
- Execução dos testes no ambiente Nix `tests`.
- Verificação de qualidade no ambiente Nix `quality`.
- Commit, abertura de PR e acompanhamento do CI.

## Síntese

A análise estabelece a estratégia de teste de integração para a Issue #234 [F6.14], garantindo a abertura, legibilidade e conformidade do DOCX gerado pelo backend através da rota integrada da aplicação.

Arquivo criado em prompts/backend/20261026-082220-abertura-legibilidade-docx-v001.md. Avalie se o local escolhido é de fato o mais adequado.
