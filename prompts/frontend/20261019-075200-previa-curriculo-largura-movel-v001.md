---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-19T07:52:00-03:00"
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
      locator: "linhas 158-160 (CRITICAL — Responsividade móvel) e 214-220 (Testes de responsividade)"
      content_state: commit
      revision: "5266771db464515c43e8b0687a223acd0712b2fd"
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RNF03 (Compatibilidade e adaptação da interface móvel)"
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
  rationale: "Trata-se de validação de responsividade de componentes visuais do frontend na largura móvel F1.1."
classification:
  sphere: engineering
  concerns:
    - user-experience
    - implementation
    - compliance
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: low
  reversibility: easy
  risk: low
---

# Análise de decisão — Validação da prévia de currículo na largura móvel F1.1 (#366)

## Solicitação original

Issue #366 ([F8.10]): "Validar a prévia de currículo na largura móvel definida em F1.1."

Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.

## Informações complementares

- Pessoas envolvidas: Responsável único @minoruhaga; Apoios: Daniel Lacerda Xavier; Gustavo Minoru Haga.
- WBS: 1.2.1.3–1.2.1.4, 1.4.2.4, 1.5.2.4.
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

Os componentes e arquivos CSS foram inspecionados em sua totalidade no commit `5266771`.

## Problema enriquecido

### Resultado desejado
Validar que a apresentação da prévia de currículo em ambos os layouts disponíveis (`ModeloClassico` e `ModeloCompacto`) adapta-se com precisão às larguras de tela móveis especificadas em F1.1 (360px, 480px / `30rem` e 640px / `40rem`), garantindo que não ocorra overflow horizontal, que o empilhamento de seções e linhas de cabeçalho funcione de maneira previsível e que todos os dados essenciais do estudante permaneçam legíveis e acessíveis.

### Atores e interesses
- **Estudante acessando por smartphone (viewport móvel 360px a 480px)**: Necessita visualizar a prévia completa do currículo de forma confortável, sem rolagem lateral horizontal involuntária e com quebra de linhas limpa em nomes, contatos e seções.
- **Recrutador/Avaliador em dispositivo móvel**: Precisa de visualização clara e hierárquica das informações acadêmicas e profissionais em telas pequenas.
- **Equipe de desenvolvimento e QA**: Precisa de suíte automatizada de testes (`PreviaCurriculo.mobile.test.tsx`) que simule a largura móvel e valide classes, regras de media query e integridade do DOM de maneira determinística.

### Evidências e fatos observados
1. Em `ModeloClassico.css`:
   - Possui `@media (max-width: 40rem)` (640px):
     * Reduz o padding do container para `1.25rem` e o gap para `1.25rem`.
     * Transforma `.modelo-classico__linha-cabecalho` em `flex-direction: column` e `align-items: flex-start`, garantindo que curso/cargo e período não colidam lateralmente.
     * Transforma `.modelo-classico__contato` em `flex-direction: column` com `align-items: center` e remove os separadores inline (`content: "•"` via `display: none`).
   - O título principal (`.modelo-classico__nome`) usa `clamp(1.75rem, 3.5vw, 2.25rem)` para escalonar fluidamente em larguras menores.
2. Em `ModeloCompacto.css`:
   - Possui `@media (max-width: 30rem)` (480px):
     * Reduz o padding do container para `1rem`.
     * Transforma `.modelo-compacto__contato` e `.modelo-compacto__itens-inline` em `display: grid` com `gap: 0.25rem`.
     * Oculta separadores inline com `display: none`.
   - O título principal (`.modelo-compacto__cabecalho h1`) usa `clamp(1.5rem, 4vw, 2rem)`.
3. Ambos os componentes preservam a semântica de `<article>`, `<header>`, `<section>`, `<h1>`, `<h2>`, `<ul>` e `<li>`.
4. Os testes unitários existentes (`ModeloClassico.test.tsx` e `ModeloCompacto.test.tsx`) verificam apenas a presença textual e omissão de seções vazias em renderização padrão de desktop, sem verificar o comportamento em viewport móvel nem a integridade de layout para telas compactas.

### Hipóteses
- Uma suíte de testes dedicada `PreviaCurriculo.mobile.test.tsx` pode instanciar os modelos sob contêineres dimensionados para 360px, 480px e 640px e aferir:
  1. A integridade estrutural e ausência de elementos que forcem overflow.
  2. O comportamento das regras CSS de responsividade móvel aplicadas aos dois modelos.
  3. A correta apresentação de todos os blocos do currículo (dados pessoais, contato com links externos, formação, experiência, projetos, competências, idiomas e documentos).

### Perguntas em aberto
Nenhuma. As especificações de F1.1 e os breakpoints de CSS estão consolidados no código.

### Escopo
- Criar a suíte de testes unitários `src/frontend/features/visualizar-curriculo/ui/PreviaCurriculo.mobile.test.tsx` cobrindo:
  1. Renderização do `ModeloClassico` na largura móvel (360px, 480px e 640px).
  2. Renderização do `ModeloCompacto` na largura móvel (360px e 480px).
  3. Validação de ausência de quebras estruturais e preservação de todos os blocos de dados do currículo.
  4. Validação de classes e seletores responsáveis pelo empilhamento responsivo.
- Ajustar pontualmente propriedades de estilo em `ModeloClassico.css` ou `ModeloCompacto.css` se identificado qualquer risco de overflow horizontal (por exemplo, quebra de links longos como URLs Lattes ou LinkedIn via `word-break: break-word` ou `overflow-wrap: anywhere`).

### Fora do escopo
- Breakpoints de tablet (768px) e desktop (1024px+), que pertencem à Issue #409 ([F11.11]).
- Registro formal do documento de evidências, que também pertence à Issue #409 ([F11.11]).
- Alterações nos contratos DTO da entidade `curriculo`.

### Critérios de sucesso
- `npm run check` com 0 erros de tipagem.
- 100% de aprovação na nova suíte `PreviaCurriculo.mobile.test.tsx`.
- Nenhuma regressão nos testes existentes de `visualizar-curriculo`.
- Formatação aprovada em `nix develop .#quality --command bash -c "npm run format:check"`.

## Restrições aplicáveis

- **AGENTS.md**: Execução obrigatória em ambientes Nix (`.#frontend` e `.#quality`); testes rápidos, determinísticos e isolados; comentários de proveniência e documentação tripartite.
- **F1.1 (RNF03)**: Suporte obrigatório a larguras móveis (360px a 640px).

## Classificação comentada

- **Esfera**: `engineering` — validação técnica de responsividade de interface e garantia de ausência de overflow móvel.
- **Preocupações**: `user-experience`, `compliance`, `implementation`.
- **Risco**: `low` — foco em testes e eventuais ajustes de CSS preventivos contra overflow.

## Decisão de roteamento

- Diretório selecionado: `prompts/frontend/`
- Justificativa: Tarefa ligada aos componentes visuais da feature `visualizar-curriculo`.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `compliance` | Alta | RNF03 e F1.1 | O currículo deve ser perfeitamente utilizável em smartphones. |
| `correctness` | Alta | Testes cobrindo 360px, 480px e 640px | Garante que ambas as variantes suportem telas compactas. |
| `simplicity` | Média | Aproveitar o layout CSS já existente | Focar na validação e blindagem contra overflow. |

## Alternativas consideradas

- **Alternativa A (Recomendada)**: Criar a suíte `PreviaCurriculo.mobile.test.tsx` com cenários dedicados para `ModeloClassico` e `ModeloCompacto`, blindando links com `overflow-wrap: break-word` no CSS se necessário.
- **Alternativa B**: Misturar os testes de viewport móvel dentro de `ModeloClassico.test.tsx` e `ModeloCompacto.test.tsx`. (Rejeitada: dificulta a rastreabilidade da entrega da issue #366 e mistura testes de conteúdo básico com responsividade).

## Histórico e decisão atual

### Decisão da versão anterior
Nenhum — análise inicial.

### Decisão recomendada nesta versão
Adotar a **Alternativa A**:
1. Blindar contêineres de contato contra quebra horizontal de URLs longas em `ModeloClassico.css` e `ModeloCompacto.css` com `overflow-wrap: break-word`.
2. Implementar `src/frontend/features/visualizar-curriculo/ui/PreviaCurriculo.mobile.test.tsx` validando o comportamento móvel nos breakpoints 360px, 480px e 640px.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `compliance` | maximized | Aderência completa a F1.1 na faixa móvel | Testes automatizados nas dimensões 360px, 480px e 640px |
| `user-experience` | prioritized | Prévia fluida e sem corte de texto em telas pequenas | Envoltórios flexíveis e `word-break` seguro |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | Zero dependências externas de viewport | Testes utilizando mock de dimensões e asserção de estrutura/classes |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `user-experience` | Usuário móvel enfrentando barra de rolagem horizontal indevida | Moderada a Alta | Usuários de smartphones |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `user-experience` | Adição de regra CSS de `overflow-wrap` | Nenhuma | Totalmente aceitável |

## Riscos e efeitos de segunda ordem

- Risco: JSDOM não simula o motor de layout de browser real com cálculos reais de quebra de texto.
  Mitigação: Testar a presença das classes de empilhamento responsivo, atributos de contêiner e aplicar wrappers de viewport com largura fixa nos testes.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Ambas as variantes renderizam dados completos em mobile | Todos os nós de dados presentes no DOM em container móvel | Teste Vitest | Falha na localização de seções |
| Links longos não provocam overflow | Propriedade `overflow-wrap` presente no CSS | Inspeção de classes | Texto ultrapassando contêiner |

## Handoffs e atividades posteriores

- Executar `$frontend-implementation-v3` informando o caminho desta análise: `prompts/frontend/20261019-075200-previa-curriculo-largura-movel-v001.md`.
- Handoff para Fase 3 (Issue #409): reaproveitar os fixtures desta suíte para estender aos tamanhos de tablet (768px) e desktop (1024px+).

## Síntese

Arquivo criado em `prompts/frontend/20261019-075200-previa-curriculo-largura-movel-v001.md`. Avalie se o local escolhido é de fato o mais adequado.
