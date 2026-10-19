---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-19T08:08:00-03:00"
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
    - path: src/frontend/features/visualizar-curriculo/ui/ModeloClassico.tsx
      relationship: primary
      representation: source-code
      function: production
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771db464515c43e8b0687a223acd0712b2fd"
      availability: available
    - path: src/frontend/features/visualizar-curriculo/ui/ModeloClassico.css
      relationship: primary
      representation: source-code
      function: production
      format: css
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771db464515c43e8b0687a223acd0712b2fd"
      availability: available
    - path: src/frontend/features/visualizar-curriculo/ui/ModeloCompacto.tsx
      relationship: primary
      representation: source-code
      function: production
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771db464515c43e8b0687a223acd0712b2fd"
      availability: available
    - path: src/frontend/features/visualizar-curriculo/ui/ModeloCompacto.css
      relationship: primary
      representation: source-code
      function: production
      format: css
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771db464515c43e8b0687a223acd0712b2fd"
      availability: available
    - path: src/frontend/AGENTS.md
      relationship: supporting
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: selected-section
      locator: "linhas 158-160 (CRITICAL — Responsividade multi-dispositivo) e 214-220 (Testes de responsividade)"
      content_state: commit
      revision: "5266771db464515c43e8b0687a223acd0712b2fd"
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RNF03 (Compatibilidade e adaptação da interface)"
      content_state: commit
      revision: "5266771db464515c43e8b0687a223acd0712b2fd"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/frontend
  considered_directories:
    - prompts/frontend
    - prompts/revisao
  confidence: high
  rationale: "Trata-se de validação de responsividade multi-tamanhos da prévia de currículo e catalogação de evidências no frontend."
classification:
  sphere: engineering
  concerns:
    - user-experience
    - compliance
    - implementation
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: low
  reversibility: easy
  risk: low
---

# Análise de decisão — Validação da responsividade da prévia nos tamanhos F1.1 e registro de evidência (#409)

## Solicitação original

Issue #409 ([F11.11]): "Validar responsividade da prévia de currículo nos tamanhos definidos em F1.1 e registrar evidência."

Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.

## Informações complementares

- Pessoas envolvidas: Responsável único @minoruhaga; Apoios: Responsável da fatia validada; Kelly Daiane Miranda Mendes.
- WBS: 1.7.1.*, 1.7.2.*, 1.8.1.*.
- Período: 2026-10-19 a 2026-10-25.

## Mudanças desde a versão anterior

Nenhum — análise inicial.

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/frontend/features/visualizar-curriculo/ui/ModeloClassico.tsx` | primary | source-code | production | typescript-react | whole-file | commit `5266771` |
| `src/frontend/features/visualizar-curriculo/ui/ModeloClassico.css` | primary | source-code | production | css | whole-file | commit `5266771` |
| `src/frontend/features/visualizar-curriculo/ui/ModeloCompacto.tsx` | primary | source-code | production | typescript-react | whole-file | commit `5266771` |
| `src/frontend/features/visualizar-curriculo/ui/ModeloCompacto.css` | primary | source-code | production | css | whole-file | commit `5266771` |
| `src/frontend/AGENTS.md` | supporting | prose | prompt-instruction | markdown | L158-L160, L214-L220 | commit `5266771` |
| `docs/requisitos_nao_funcionais.md` | supporting | prose | documentation | markdown | RNF03 | commit `5266771` |

### Limites da evidência dos artefatos

Os arquivos foram inspecionados em seu conteúdo completo no commit `5266771`.

## Problema enriquecido

### Resultado desejado
Validar a responsividade e a integridade de apresentação da prévia de currículo em todas as faixas dimensionais especificadas pelo projeto (F1.1 e RNF03) — compreendendo Mobile Compacto (360px e 480px), Mobile Clássico (640px), Tablet (768px), Desktop Padrão (1024px) e Desktop Expandido (1280px+) — e registrar formalmente as evidências técnicas e catalogação de achados em relatório rastreável.

### Atores e interesses
- **Estudante e Recrutador em diversos dispositivos (Smartphones, Tablets e Desktops)**: Devem ter uma experiência fluida, sem barras de rolagem horizontal espúrias, com adaptação natural de colunas, espaçamentos confortáveis e legibilidade mantida em qualquer resolução.
- **Equipe de QA e Engenharia**: Precisa de um catálogo de evidências auditável e de testes automatizados unitários no Vitest cobrindo a matriz dimensional F1.1.

### Evidências e fatos observados (Catálogo de Achados F1.1)

1. **Faixa 1 — Mobile Compacto (360px a 480px / `30rem`)**:
   - `ModeloCompacto`: O breakpoint `@media (max-width: 30rem)` entra em ação, transformando contatos e itens inline de flexbox com separadores (`•`) para grid vertical (`display: grid; gap: 0.25rem`), ocultando os marcadores pontuais e reduzindo o padding do contêiner para `1rem`.
   - `ModeloClassico`: Opera com padding de `1.25rem`, contatos empilhados verticalmente e centralizados, sem separadores inline. Título escala via `clamp(1.75rem, 3.5vw, 2.25rem)`.
   - Ausência de overflow: blindado com `overflow-wrap: break-word` e `word-break: break-word`.

2. **Faixa 2 — Mobile Clássico (481px a 640px / `40rem`)**:
   - `ModeloClassico`: O breakpoint `@media (max-width: 40rem)` assegura que `.modelo-classico__linha-cabecalho` permaneça empilhado verticalmente (`flex-direction: column`, `align-items: flex-start`), evitando que curso/cargo colidam com o período.
   - `ModeloCompacto`: Retoma a apresentação flex com marcadores inline discretos quando a largura supera `30rem` (480px).

3. **Faixa 3 — Tablet (641px a 768px)**:
   - Ambos os modelos: a largura do viewport permite que as linhas de cabeçalho (`.modelo-classico__linha-cabecalho`) apresentem curso/cargo à esquerda e período à direita com `justify-content: space-between`.
   - `ModeloClassico`: O grid de competências e idiomas (`repeat(auto-fill, minmax(14rem, 1fr))`) distribui os itens em 2 colunas equilibradas.
   - Padding do `ModeloClassico` expande para `2.5rem`, oferecendo visual de folha A4 arejada.

4. **Faixa 4 — Desktop Padrão e Expandido (1024px e 1280px+)**:
   - `ModeloClassico`: Delimitado por `max-width: 52rem` (832px) com `margin: 0 auto`, assegurando que o currículo não se torne excessivamente largo e mantenha comprimento de linha ergonômico para leitura humana.
   - `ModeloCompacto`: Delimitado por `max-width: 56rem` (896px) com `margin: 0 auto`.
   - Em ambas as variantes, sombras suaves (`box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08)`) e tipografia hierárquica garantem apresentação sóbria para visualização e impressão (`@media print`).

### Hipóteses
- Uma suíte dedicada `PreviaCurriculo.responsividade.test.tsx` pode parametrizar a matriz F1.1 (360px, 480px, 640px, 768px, 1024px, 1280px) e verificar a conformidade de ambas as variantes em cada faixa dimensional.
- A criação do artefato de evidências `docs/testes/evidencias/f11-11-responsividade-previa.md` atende integralmente ao requisito de registro formal da issue #409.

### Perguntas em aberto
Nenhuma. Todos os breakpoints e critérios foram validados nas análises e no código.

### Escopo
1. Criar a suíte `src/frontend/features/visualizar-curriculo/ui/PreviaCurriculo.responsividade.test.tsx` cobrindo a matriz F1.1 completa (360px, 480px, 640px, 768px, 1024px, 1280px).
2. Criar o documento de evidências formais em `docs/testes/evidencias/f11-11-responsividade-previa.md` detalhando os testes executados, a matriz de conformidade e o comportamento em cada viewport.
3. Garantir 100% de testes passando, 0 erros no `npm run check` e formatação limpa no `npm run format:check`.

### Fora do escopo
- Alterações em endpoints ou serviços de backend.
- Modificações em outros componentes do frontend que não pertençam à prévia de currículo.

### Critérios de sucesso
- 100% dos testes da suíte `PreviaCurriculo.responsividade.test.tsx` passando no ambiente Nix `.#frontend`.
- Documento `docs/testes/evidencias/f11-11-responsividade-previa.md` criado e estruturado.
- `npm run check` sem erros de tipagem.
- Prettier e ESLint aprovados em `.#quality`.

## Restrições aplicáveis

- **AGENTS.md**: Ambientes Nix obrigatórios (`.#frontend`, `.#quality`); documentação tripartite; comentário de proveniência em código e testes.
- **F1.1 (RNF03)**: Matriz de responsividade multi-dispositivo (Mobile, Tablet, Desktop).

## Classificação comentada

- **Esfera**: `engineering` — testes de responsividade e registro de evidências técnicas.
- **Preocupações**: `user-experience`, `compliance`, `implementation`.
- **Risco**: `low` — escopo seguro, concentrado em testes e documentação.

## Decisão de roteamento

- Diretório selecionado: `prompts/frontend/`
- Justificativa: A demanda trata de validação de responsividade dos componentes de prévia de currículo do frontend.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `compliance` | Alta | F1.1 e RNF03 | O currículo deve ser responsivo em toda a matriz de dispositivos. |
| `correctness` | Alta | Cobertura de 360px a 1280px | Testes paramétricos garantem ausência de regressões em qualquer tamanho. |
| `observability` | Média | Evidências registradas em markdown | Fornece rastreabilidade para auditoria de QA e revisores da issue. |

## Alternativas consideradas

- **Alternativa A (Recomendada)**: Implementar a suíte `PreviaCurriculo.responsividade.test.tsx` com cenários para Mobile, Tablet e Desktop e registrar formalmente o relatório em `docs/testes/evidencias/f11-11-responsividade-previa.md`.
- **Alternativa B**: Apenas adicionar mais casos ao arquivo de teste móvel criado na Fase 2 sem criar o documento de evidências. (Rejeitada: descumpriria a exigência explícita da issue #409: "... e registrar evidência").

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Confiança | Base |
|---|---:|---:|---:|---|---|
| `compliance` | Alta | +2 | -1 | Alta | Atende ao critério da issue |
| `correctness` | Alta | +2 | +1 | Alta | Matriz completa |
| `observability`| Média | +2 | -2 | Alta | Documento dedicado |

## Histórico e decisão atual

### Decisão da versão anterior
Nenhum — análise inicial.

### Decisão recomendada nesta versão
Adotar a **Alternativa A**:
1. Criar `PreviaCurriculo.responsividade.test.tsx` cobrindo todas as resoluções da matriz F1.1.
2. Criar `docs/testes/evidencias/f11-11-responsividade-previa.md` registrando detalhadamente as evidências de conformidade.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `compliance` | maximized | Atendimento estrito a F1.1 em todas as faixas dimensionais | Cobertura automatizada de testes |
| `observability` | prioritized | Rastreabilidade e comprovação auditável de QA | Documento formal de evidências |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | Uso de mocks em DOM sem dependências de browser pesado | Execução rápida de testes no CI |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `compliance` | Rejeição da entrega por ausência de registro formal de evidências | Moderada | Processo de QA e entrega |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `observability` | Tempo de redação do documento de evidências | Velocidade imediata | Totalmente aceitável |

## Riscos e efeitos de segunda ordem

- Risco: Documento de evidências ficar desatualizado se os layouts mudarem.
  Mitigação: Manter a suíte automatizada sincronizada com o documento.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Ambos os modelos adaptam-se de 360px a 1280px | Testes passando em todas as larguras da matriz | Vitest | Falha em qualquer viewport |
| Evidência formal registrada | Arquivo `.md` presente em `docs/testes/evidencias/` | Verificação Git | Arquivo ausente |

## Handoffs e atividades posteriores

- Handoff para Fase 4 (Issue #398): Iniciar os testes de integração do backend no ambiente `nix develop .#tests`.

## Síntese

Arquivo criado em `prompts/frontend/20261019-080800-previa-responsividade-evidencias-v001.md`. Avalie se o local escolhido é de fato o mais adequado.
