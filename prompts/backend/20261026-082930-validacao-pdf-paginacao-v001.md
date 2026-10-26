---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-26T08:29:30-03:00"
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
    - path: src/backend/infrastructure/exportacao/renderizador_pdf.py
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
    - path: src/backend/tests/test_infrastructure_renderizador_pdf.py
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
  rationale: "Trata da especificação de teste de integração de backend para validação de paginação, legibilidade e conformidade geométrica do PDF gerado."
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

# Análise de decisão — Validação do PDF Gerado e Falhas por Página (Issue #410 [F11.12])

## Solicitação original

Execução da Issue #410 [F11.12]: "Validar PDF gerado contra o roteiro de legibilidade de F1.5 e registrar falhas por página."
Planejamento: WBS 1.7.1._, 1.7.2._, 1.8.1.*. Início: 2026-10-26. Entrega: 2026-11-01. Responsável único: @minoruhaga. Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.

## Informações complementares

- O requisito RNF07 preconiza a qualidade, legibilidade e ausência de sobreposição ou cortes na exportação de currículos. O card F1.5 (#172) estabelece critérios de aceite e parâmetros de conferência visual e paginação.
- O gerador de PDF (`src/backend/infrastructure/exportacao/renderizador_pdf.py`) utiliza o motor Platypus do ReportLab, construindo um documento A4 (`595.27 × 841.89 pt`) com margens simétricas (`2.0 cm` no modelo clássico e `1.5 cm` no compacto), paleta sóbria (`#1F3A5F` para cabeçalhos e títulos de seção) e agrupamento `KeepTogether` para manter títulos de seção junto com seus primeiros blocos de conteúdo, eliminando quebras orfãs.
- A validação exige:
  1. Teste automatizado de integração (`src/backend/tests/test_integracao_validacao_pdf_legibilidade.py`) que gere o PDF real e examine cada página individualmente com `pypdf`, atestando geometria A4, fluxo sequencial de seções, ausência de títulos órfãos no rodapé, preenchimento legível e densidade de linhas por página;
  2. Documento formal de evidências (`docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md`) catalogando a inspeção detalhada página a página e o registro explícito de falhas (0 falhas encontradas);
  3. Verificação de omissão estrita de caminhos de arquivos privados ou segredos no PDF.
- A governança de ambientes Nix ([AGENTS.md](AGENTS.md)) exige a execução de testes de integração estritamente no ambiente `nix develop .#tests`.

## Mudanças desde a versão anterior

Nenhum — análise inicial (`mode: initial`).

## Artefatos analisados

| Caminho                                                     | Relação    | Representação  | Função                 | Formato | Recorte    | Estado/revisão |
| ----------------------------------------------------------- | ---------- | -------------- | ---------------------- | ------- | ---------- | -------------- |
| `src/backend/infrastructure/exportacao/renderizador_pdf.py` | primary    | source-code    | adapter-implementation | python  | whole-file | working-tree   |
| `src/backend/api/exportacao_curriculo.py`                   | primary    | source-code    | api-route              | python  | whole-file | working-tree   |
| `src/backend/tests/fixtures/curriculo_exportacao.py`        | supporting | test-fixture   | test-support           | python  | whole-file | working-tree   |
| `src/backend/tests/test_infrastructure_renderizador_pdf.py` | context    | automated-test | unit-test-suite        | python  | whole-file | working-tree   |

### Limites da evidência dos artefatos

O renderizador PDF e a rota HTTP de download já existem na branch `dev`. No entanto, inexiste uma suíte de teste de integração dedicada a inspecionar o fluxo integrado por página, verificar quebras de página controladas em currículos densos e registrar evidências formais de falhas por página conforme estipulado por F11.12.

## Problema enriquecido

### Resultado desejado

Implementar a suíte `test_integracao_validacao_pdf_legibilidade.py` e gerar o relatório de evidências `docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md`, auditando a legibilidade página por página em currículos padrão e extensos nos modelos clássico e compacto.

### Atores e interesses

- **Estudante / Candidato:** Confiança de que o currículo PDF gerado terá paginação perfeita, sem títulos isolados ao final de páginas e sem cortes de texto.
- **Recrutador:** Leitura clara e profissional em PDF impresso ou visualizado em leitor digital.
- **Engenharia de Backend:** Proteção automatizada contra regressões na quebra de página ou vazamento de metadados.

### Evidências e fatos observados

- `renderizador_pdf.py` emprega `KeepTogether([Paragraph(secao.titulo), *primeiro_bloco])` para garantir que uma seção nunca comece isolada no rodapé de uma página.
- Os modelos clássico e compacto usam fontes base `10.5 pt` e `9.0 pt`, respectivamente, alterando densidade sem corromper o texto.
- O endpoint `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/pdf` entrega o arquivo com `Content-Disposition: attachment; filename=...`.

### Hipóteses

- A auditoria programática com `pypdf.PdfReader` sobre os bytes reais do PDF permite aferir dimensões da página (`mediabox`), contagem de páginas e distribuição de texto por página de forma determinística e reproduzível no CI.

### Perguntas em aberto

- Nenhuma pendência impeditiva.

### Escopo

- Implementação do teste de integração `src/backend/tests/test_integracao_validacao_pdf_legibilidade.py`.
- Criação do documento de evidências e auditoria página a página `docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md`.
- Execução no ambiente Nix `tests` e verificação no ambiente Nix `quality`.

### Fora do escopo

- Exportação DOCX (já tratada na Fase 3).
- Interface gráfica web.
- Alterações no algoritmo de geração do ReportLab (o componente já cumpre o design).

### Critérios de sucesso

- Testes de integração executados com 100% de sucesso em `nix develop .#tests`.
- Documento de evidências registrado com auditoria completa de cada página.
- `ruff check` e `ruff format --check` com 0 erros.
- PR criado com CI 100% verde referenciando o fechamento da Issue #410 (`Closes #410.`).

## Restrições aplicáveis

- **Ambiente Nix:** Exclusivamente `nix develop .#tests` para os testes de integração.
- **Docstrings:** Tripartite obrigatória (_O que faz_, _Como faz_, _Qual finalidade atende_).
- **Rastreabilidade:** Comentário `# Proveniência: decision-analysis prompts/backend/20261026-082930-validacao-pdf-paginacao-v001.md#v001`.

## Classificação comentada

- **Esfera:** `engineering` (garantia de qualidade e teste automatizado de integração de backend).
- **Preocupações:** `reliability`, `architecture` e `implementation`.
- **Tipo de decisão:** `design` (estratégia de validação de paginação e relatório de evidências).

## Decisão de roteamento

- **Raiz:** `prompts`
- **Pasta selecionada:** `prompts/backend`
- **Pastas candidatas:** `prompts/backend`, `prompts/revisao`, `prompts/templates`
- **Confiança:** `high`
- **Justificativa:** Trata exclusivamente de validação e testes integrados de exportação na camada de backend.

## Dimensões de decisão

| Dimensão      | Prioridade | Limiar ou direção                                     | Por que importa                                    |
| ------------- | ---------- | ----------------------------------------------------- | -------------------------------------------------- |
| `correctness` | Alta       | 100% de conformidade com A4 e layout ReportLab        | Elimina falhas de layout no PDF                    |
| `reliability` | Alta       | Garantia de ausência de títulos órfãos e quebra limpa | Garante apresentação profissional aos recrutadores |
| `simplicity`  | Alta       | Execução em memória via `pypdf` sem harness externo   | Testes ultrarrápidos no CI                         |

## Alternativas consideradas

- **Alternativa A (Recomendada):** Teste de integração automatizado com `pypdf` auditando página por página, associado a relatório formal em `docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md`.
- **Alternativa B:** Apenas conferência manual visual sem asserções programáticas no código.
  - _Desvantagem:_ Risco de regressão silenciosa em alterações futuras de dependências ou templates.
- **Alternativa C:** Renderização do PDF em bitmap (rasterização com `pdf2image` ou Ghostscript) com comparação visual de pixels.
  - _Desvantagem:_ Inviável e desnecessariamente pesado no Nix flake headless leve; introduz fragilidades de antialiasing de fontes.

## Perfil de pagamento comparativo

| Dimensão      | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base                                              |
| ------------- | ---------: | ------------: | ------------: | ------------: | --------- | ------------------------------------------------- |
| `correctness` |       Alta |            +2 |             0 |            +2 | Alta      | Alternativa A audita texto e geometria por página |
| `reliability` |       Alta |            +2 |            +1 |            +1 | Alta      | Alternativa A valida regras de `KeepTogether`     |
| `simplicity`  |       Alta |            +2 |            +2 |            -2 | Alta      | Alternativa A executa em < 1s no unittest         |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma (versão inicial).

### Decisão recomendada nesta versão

Adotar a **Alternativa A**: criar o teste de integração `test_integracao_validacao_pdf_legibilidade.py` validando geometria A4, cabeçalhos, contatos, seções por página, controle de quebras de página e ausência de orfãos em ambos os modelos de currículo, combinando com o relatório de auditoria e registro de falhas por página em `docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md`.

### Impacto da revisão

Iniciação formal da implementação da Issue #410.

### Dimensões maximizadas ou priorizadas

| Dimensão      | Estado      | Ganho esperado                                        | Evidência ou hipótese              |
| ------------- | ----------- | ----------------------------------------------------- | ---------------------------------- |
| `reliability` | maximized   | Paginação estável e legível em qualquer leitor de PDF | Testes integrados com `pypdf`      |
| `correctness` | prioritized | Conformidade estrita com RF09, RNF07 e F1.5           | Auditoria página a página          |
| `simplicity`  | prioritized | Execução rápida em memória no ambiente `tests`        | Sem dependências pesadas de imagem |

### Dimensões satisfeitas por limiar

| Dimensão         | Limiar aceito                                | Como a decisão atende               |
| ---------------- | -------------------------------------------- | ----------------------------------- |
| `delivery-speed` | Execução em < 1 hora com revisão em < 10 min | Foco estrito no escopo do card #410 |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão      | Perda esperada                                                    | Severidade | Afetados                  |
| ------------- | ----------------------------------------------------------------- | ---------- | ------------------------- |
| `reliability` | Título de seção isolado no rodapé da página anterior sem conteúdo | Média      | Recrutadores e candidatos |
| `privacy`     | Metadados do gerador ou URLs internas expostas no arquivo PDF     | Alta       | Segurança da aplicação    |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade                              | Dimensão prejudicada | Aceitabilidade                   |
| ------------------- | -------------------------------------------------- | -------------------- | -------------------------------- |
| `reliability`       | Criação de arquivo de teste de integração dedicado | Nenhuma              | Totalmente aceitável e desejável |

## Riscos e efeitos de segunda ordem

- _Risco:_ Variações na paginação caso sejam adicionados muitos blocos textuais extensos.
- _Mitigação:_ O teste avalia tanto o currículo padrão quanto cenários estendidos com múltiplos itens.

## Validação da decisão

| Hipótese ou resultado                                      | Evidência necessária                           | Método                     | Sinal para revisar                 |
| ---------------------------------------------------------- | ---------------------------------------------- | -------------------------- | ---------------------------------- |
| `test_integracao_validacao_pdf_legibilidade.py` passa 100% | Relatório do unittest no terminal              | `nix develop .#tests`      | Falha em qualquer asserção         |
| Documento de evidências registra 0 falhas                  | Relatório Markdown preenchido                  | Inspeção do arquivo gerado | Presença de cortes ou sobreposição |
| Linter e formatação limpos                                 | `ruff check` e `ruff format --check` sem erros | Nix develop `quality`      | Erros de sintaxe ou formatação     |

## Handoffs e atividades posteriores

- Implementação do teste de integração via `$integration-system-testing-v1`.
- Criação de `docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md`.
- Execução e verificação nos ambientes Nix `tests` e `quality`.
- Commit, abertura de PR e acompanhamento do CI.

## Síntese

A análise estabelece a estratégia de teste de integração e evidência para a Issue #410 [F11.12], assegurando a validação sistemática de geometria, paginação e legibilidade do PDF gerado.

Arquivo criado em prompts/backend/20261026-082930-validacao-pdf-paginacao-v001.md. Avalie se o local escolhido é de fato o mais adequado.
