---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-26T08:12:30-03:00"
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
    - path: src/frontend/features/visualizar-curriculo/ui/ModeloClassico.tsx
      relationship: primary
      representation: source-code
      function: component-implementation
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/frontend/features/visualizar-curriculo/ui/ModeloClassico.css
      relationship: primary
      representation: source-code
      function: style-sheet
      format: css
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/frontend/features/visualizar-curriculo/ui/ModeloCompacto.tsx
      relationship: primary
      representation: source-code
      function: component-implementation
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/frontend/features/visualizar-curriculo/ui/ModeloCompacto.css
      relationship: primary
      representation: source-code
      function: style-sheet
      format: css
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/compatibilidade-responsividade.md
      relationship: supporting
      representation: specification
      function: architectural-standard
      format: markdown
      analysis_scope: selected-section
      locator: "seções de telas largas e resoluções F1.1"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/testes/evidencias/f11-11-responsividade-previa.md
      relationship: supporting
      representation: test-evidence
      function: validation-report
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/frontend/features/visualizar-curriculo/ui/PreviaCurriculo.responsividade.test.tsx
      relationship: context
      representation: automated-test
      function: test-suite
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/frontend
  considered_directories:
    - prompts/frontend
    - prompts/revisao
    - prompts/templates
  confidence: high
  rationale: "Trata da legibilidade visual, regras tipográficas e suíte de testes de componentes dos modelos de currículo na camada de frontend."
classification:
  sphere: engineering
  concerns:
    - user-experience
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

# Análise de decisão — Teste Visual/Manual de Legibilidade em Tela Larga para Modelos de Currículo (Issue #220 [F5.12])

## Solicitação original

Execução da Issue #220 [F5.12]: "Criar teste visual/manual de legibilidade em tela larga para cada modelo."
Planejamento: WBS 1.4.1._, 1.4.2._. Início: 2026-10-26. Entrega: 2026-11-01. Responsável único: @minoruhaga. Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.

## Informações complementares

- O projeto definiu em F1.1 (`docs/compatibilidade-responsividade.md`) que telas largas abrangem `Desktop Padrão (1024px)` e `Desktop Amplo (1280px+)`, estendendo-se a telas Full HD (1920px) e monitores ultrawide.
- A tarefa complementar simétrica é a Issue #219 [F5.11] (atribuída a @xavier-dan), com foco específico em telas estreitas (< 768px).
- A legibilidade tipográfica em telas largas impõe restrições ergonômicas críticas:
  1. Limitação de medida de linha (`line-length` / `max-width`): evitar que parágrafos se estendam descontroladamente em larguras excessivas (o que força o leitor a movimentos oculares excessivos e perda de rastreamento de linha).
  2. Alinhamento de cabeçalhos bi-coluna (`justify-content: space-between`): títulos de cargo/curso à esquerda e períodos à direita na mesma linha basal.
  3. Distribuição de competências e idiomas em multi-colunas (`repeat(auto-fill, minmax(14rem, 1fr))`) para aproveitamento equilibrado do espaço horizontal.
  4. Contraste e hierarquia de fontes proporcionais sem quebras indesejadas em 1024px e 1280px+.
- De acordo com o fluxo obrigatório de governança e skills, a implementação deve usar `$frontend-implementation-v3` para os testes de componentes unitários de frontend e estruturar o roteiro e registro de evidências em `docs/testes/evidencias/f5-12-legibilidade-tela-larga.md`.

## Mudanças desde a versão anterior

Nenhum — análise inicial (`mode: initial`).

## Artefatos analisados

| Caminho                                                                                 | Relação    | Representação  | Função                   | Formato          | Recorte          | Estado/revisão |
| --------------------------------------------------------------------------------------- | ---------- | -------------- | ------------------------ | ---------------- | ---------------- | -------------- |
| `src/frontend/features/visualizar-curriculo/ui/ModeloClassico.tsx`                      | primary    | source-code    | component-implementation | typescript-react | whole-file       | working-tree   |
| `src/frontend/features/visualizar-curriculo/ui/ModeloClassico.css`                      | primary    | source-code    | style-sheet              | css              | whole-file       | working-tree   |
| `src/frontend/features/visualizar-curriculo/ui/ModeloCompacto.tsx`                      | primary    | source-code    | component-implementation | typescript-react | whole-file       | working-tree   |
| `src/frontend/features/visualizar-curriculo/ui/ModeloCompacto.css`                      | primary    | source-code    | style-sheet              | css              | whole-file       | working-tree   |
| `docs/compatibilidade-responsividade.md`                                                | supporting | specification  | architectural-standard   | markdown         | selected-section | working-tree   |
| `docs/testes/evidencias/f11-11-responsividade-previa.md`                                | supporting | test-evidence  | validation-report        | markdown         | whole-file       | working-tree   |
| `src/frontend/features/visualizar-curriculo/ui/PreviaCurriculo.responsividade.test.tsx` | context    | automated-test | test-suite               | typescript-react | whole-file       | working-tree   |

### Limites da evidência dos artefatos

O CSS dos modelos já possui regras de contenção (`max-width: 52rem` no clássico e `max-width: 56rem` no compacto) e classes dedicadas de layout (`.modelo-classico__linha-cabecalho`, `.modelo-classico__grid-duas-colunas`, `.modelo-compacto__itens-inline`). O que falta para cumprir integralmente o card #220 é o teste focado especificamente na aferição e comprovação das propriedades de legibilidade em tela larga (ambos automatizado via Vitest/Testing Library e o procedimento visual/manual estruturado em evidência formal).

## Problema enriquecido

### Resultado desejado

Disponibilizar uma suíte automatizada de testes unitários de componente (`PreviaCurriculo.legibilidade-larga.test.tsx`) e um documento formal de roteiro e evidência de teste visual/manual (`docs/testes/evidencias/f5-12-legibilidade-tela-larga.md`) que comprovem a preservação absoluta da legibilidade para os dois modelos suportados (`ModeloClassico` e `ModeloCompacto`) nas resoluções de tela larga (1024px e 1280px+).

### Atores e interesses

- **Estudante / Candidato:** Deseja ter certeza de que seu currículo impresso na tela ou exportado para visualização em navegadores desktop apresentará estética profissional e leitura fluida e confortável para os recrutadores.
- **Recrutador / Avaliador:** Necessita ler o currículo em monitor de escritório ou notebook sem cansaço visual, com linhas de comprimento ergonômico, cabeçalhos alinhados e clara distinção entre empresas, cargos e datas.
- **Engenharia de Software:** Necessita de garantias automatizadas no CI para impedir regressões tipográficas e de layout que permitam estiramento de linha ou sobreposição em telas grandes.

### Evidências e fatos observados

- `ModeloClassico.css` limita a largura máxima a `52rem` (832px) com centralização `margin: 0 auto` e espaçamento `padding: 2.5rem`, assegurando densidade ótima de caracteres por linha em viewports ≥ 1024px.
- `ModeloClassico.css` implementa cabeçalhos de itens com `.modelo-classico__linha-cabecalho { display: flex; justify-content: space-between; align-items: baseline; }` fora do breakpoint móvel.
- `ModeloCompacto.css` limita a largura máxima a `56rem` (896px) com `margin: 0 auto`, `padding: 1.5rem` e distribuição horizontal de itens com `gap: 0.25rem 0.75rem`.
- Os testes existentes em `PreviaCurriculo.responsividade.test.tsx` cobrem integridade dos dados e renderização genérica, mas não possuem asserções dedicadas às regras de legibilidade tipográfica, contenção de largura e alinhamentos de tela larga em cada modelo.

### Hipóteses

- A validação automatizada de nós DOM, seletores CSS específicos de layout largo (`.modelo-classico__linha-cabecalho`, `.modelo-classico__grid-duas-colunas`) e medição de contenção de largura em contêineres simulados de 1024px, 1280px, 1440px e 1920px confere cobertura determinística contra regressões.
- A elaboração de roteiro e registro de evidência visual/manual consolida os critérios do teste de usabilidade para revisão humana rápida (< 10 minutos).

### Perguntas em aberto

- Nenhuma pendência impeditiva. O comportamento dos componentes já está estável na branch `dev`.

### Escopo

- Implementação do teste automatizado unitário `src/frontend/features/visualizar-curriculo/ui/PreviaCurriculo.legibilidade-larga.test.tsx`.
- Elaboração do roteiro de teste visual/manual e registro de evidências em `docs/testes/evidencias/f5-12-legibilidade-tela-larga.md`.
- Verificação de rastreabilidade, docstrings tripartites e validação no ambiente Nix `frontend` e `quality`.

### Fora do escopo

- Telas estreitas (< 768px), que são de responsabilidade da Issue #219 [F5.11] atribuída a @xavier-dan.
- Alterações estruturais ou reestilização dos modelos clássico e compacto (os componentes já cumprem o design aprovado).
- Testes E2E com Cypress/Playwright ou dependências de navegadores reais pesados no CI.
- Backend, banco de dados ou rotas de exportação.

### Critérios de sucesso

- Teste automatizado executado com sucesso via `nix develop .#frontend --command bash -c "cd src/frontend && npx vitest run features/visualizar-curriculo/ui/PreviaCurriculo.legibilidade-larga.test.tsx"`.
- Documento de evidências visual/manual preenchido e auditado segundo o padrão do projeto.
- `npm run check` e `npm run format:check` passando com 0 erros.
- PR criado com CI 100% verde e fechamento referenciado (`Closes #220.`).

## Restrições aplicáveis

- **AGENTS.md raiz e src/frontend:** Uso estrito do ambiente Nix `frontend` para execução dos testes unitários e `quality` para lint/formatação. Git/gh fora do Nix.
- **Docstrings tripartites obrigatórias:** Em todas as funções e métodos de teste criados.
- **Rastreabilidade de código:** Inclusão de `// Proveniência: decision-analysis prompts/frontend/20261026-081230-legibilidade-modelos-tela-larga-v001.md#v001`.
- **FSD (Feature-Sliced Design):** Manutenção dos arquivos na camada `features/visualizar-curriculo/ui`.

## Classificação comentada

- **Esfera:** `engineering` (construção de suíte de testes de componente e documentação técnica de garantia de qualidade).
- **Preocupações:** `user-experience` (ergonomia de leitura em telas desktop), `architecture` (preservação do FSD e isolamento de componentes) e `implementation` (testes em Vitest com Testing Library).
- **Tipo de decisão:** `design` (definição de critérios de verificação e oráculos para legibilidade ampla).

## Decisão de roteamento

- **Raiz:** `prompts`
- **Pasta selecionada:** `prompts/frontend`
- **Pastas candidatas:** `prompts/frontend`, `prompts/revisao`, `prompts/templates`
- **Confiança:** `high`
- **Justificativa:** Trata exclusivamente de comportamento, ergonomia visual e testes dos componentes React de visualização de currículo na camada de frontend.

## Dimensões de decisão

| Dimensão        | Prioridade | Limiar ou direção                                     | Por que importa                                          |
| --------------- | ---------- | ----------------------------------------------------- | -------------------------------------------------------- |
| `correctness`   | Alta       | 100% dos testes passando sem flakes                   | Garante estabilidade contínua no CI                      |
| `user-value`    | Alta       | Máxima clareza de legibilidade em 1024px e 1280px+    | Permite leitura confortável por recrutadores             |
| `simplicity`    | Alta       | Teste determinístico de componente sem harness pesado | Mantém tempo de execução em frações de segundo           |
| `modifiability` | Média      | Isolamento e modularidade das asserções por modelo    | Facilita extensão futura para novos modelos de currículo |

## Alternativas consideradas

- **Alternativa A (Recomendada):** Teste unitário de componente com Vitest/React Testing Library focado na árvore de elementos, classes de layout largo e restrições de estilo de tela ampla, combinado com roteiro formal de teste visual/manual em `docs/testes/evidencias/f5-12-legibilidade-tela-larga.md`.
- **Alternativa B:** Apenas teste visual manual sem cobertura automatizada no código.
  - _Desvantagem:_ Risco imediato de regressão não detectada em alterações futuras de CSS; violação do critério de inclusão de testes pertinentes.
- **Alternativa C:** Introdução de framework pesado de teste visual E2E com screenshot diff (ex: Playwright ou Cypress com snapshot).
  - _Desvantagem:_ Inviável no ambiente headless CI atual do projeto sem dependências de browsers em nix flake; viola a regra de manter testes unitários rápidos e isolados.

## Perfil de pagamento comparativo

| Dimensão         | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base                                           |
| ---------------- | ---------: | ------------: | ------------: | ------------: | --------- | ---------------------------------------------- |
| `correctness`    |       Alta |            +2 |             0 |            +2 | Alta      | Teste automatizado garante não-regressão       |
| `user-value`     |       Alta |            +2 |            +1 |            +2 | Alta      | Ambos os modelos verificados em alta resolução |
| `simplicity`     |       Alta |            +2 |            +1 |            -2 | Alta      | Alternativa A roda em < 1s no Vitest           |
| `delivery-speed` |      Média |            +2 |            +2 |            -2 | Alta      | Alternativa A entrega imediatamente            |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma (versão inicial).

### Decisão recomendada nesta versão

Adotar a **Alternativa A**: implementar a suíte `PreviaCurriculo.legibilidade-larga.test.tsx` com cenários dedicados para `ModeloClassico` e `ModeloCompacto` em 1024px e 1280px+, validando a contenção de largura máxima (`52rem` e `56rem`), a centralização horizontal, o cabeçalho de metadados em linha bi-coluna e a distribuição em grid de competências; e formalizar o relatório de inspeção visual humana no arquivo `docs/testes/evidencias/f5-12-legibilidade-tela-larga.md`.

### Impacto da revisão

Iniciação formal da implementação da Issue #220.

### Dimensões maximizadas ou priorizadas

| Dimensão      | Estado      | Ganho esperado                                              | Evidência ou hipótese                       |
| ------------- | ----------- | ----------------------------------------------------------- | ------------------------------------------- |
| `correctness` | maximized   | Validação contínua no CI contra regressões de layout        | Testes automatizados executados a cada PR   |
| `user-value`  | prioritized | Conforto visual e ergonomia comprovados para recrutadores   | Medida de linha e alinhamento inspecionados |
| `simplicity`  | prioritized | Execução rápida e determinística no ambiente Nix `frontend` | Zero overhead de emuladores pesados         |

### Dimensões satisfeitas por limiar

| Dimensão         | Limiar aceito                                | Como a decisão atende                                     |
| ---------------- | -------------------------------------------- | --------------------------------------------------------- |
| `delivery-speed` | Execução em < 1 hora com revisão em < 10 min | Escopo enxuto, direto e perfeitamente focado no card #220 |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão      | Perda esperada                                                | Severidade | Afetados                       |
| ------------- | ------------------------------------------------------------- | ---------- | ------------------------------ |
| `user-value`  | Textos esticados por toda a largura de monitores 4K/ultrawide | Alta       | Usuários finais e recrutadores |
| `correctness` | Falhas visuais não percebidas em merges subsequentes          | Média      | Time de desenvolvimento        |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade                                       | Dimensão prejudicada | Aceitabilidade                   |
| ------------------- | ----------------------------------------------------------- | -------------------- | -------------------------------- |
| `correctness`       | Criação e manutenção de arquivo adicional de teste unitário | Nenhuma material     | Totalmente aceitável e desejável |

## Riscos e efeitos de segunda ordem

- _Risco:_ O arquivo de evidências ficar desatualizado se o CSS mudar no futuro.
- _Mitigação:_ O teste automatizado no CI falhará se houver alterações de classes ou quebras estruturais.

## Validação da decisão

| Hipótese ou resultado                                    | Evidência necessária               | Método                                   | Sinal para revisar                       |
| -------------------------------------------------------- | ---------------------------------- | ---------------------------------------- | ---------------------------------------- |
| `PreviaCurriculo.legibilidade-larga.test.tsx` passa 100% | Relatório do Vitest no terminal    | `npm run test` no nix develop `frontend` | Falha em qualquer asserção de componente |
| Relatório de evidência documenta fielmente o resultado   | Documento Markdown preenchido      | Inspeção manual e revisão do PR          | Omite dados ou screenshots/critérios     |
| Padrões de código e tipos respeitados                    | `check` e `format:check` sem erros | Nix develop `frontend` e `quality`       | Erros de linter ou formatação            |

## Handoffs e atividades posteriores

- Implementação do código de teste via `$frontend-implementation-v3`.
- Criação do documento `docs/testes/evidencias/f5-12-legibilidade-tela-larga.md`.
- Execução dos testes e validação da suíte no ambiente Nix.
- Commit padronizado, abertura de PR e acompanhamento do CI.

## Síntese

A análise estabelece a estratégia completa para a Issue #220 [F5.12], articulando cobertura de testes automatizados unitários no Vitest para ambos os modelos (`ModeloClassico` e `ModeloCompacto`) em telas de 1024px e 1280px+ com relatório de evidências de teste visual e manual.

Arquivo criado em prompts/frontend/20261026-081230-legibilidade-modelos-tela-larga-v001.md. Avalie se o local escolhido é de fato o mais adequado.
