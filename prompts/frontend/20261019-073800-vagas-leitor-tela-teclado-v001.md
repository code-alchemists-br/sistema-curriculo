---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-19T07:38:00-03:00"
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
    - path: src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.tsx
      relationship: primary
      representation: source-code
      function: production
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771db464515c43e8b0687a223acd0712b2fd"
      availability: available
    - path: src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.css
      relationship: supporting
      representation: source-code
      function: production
      format: css
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5266771db464515c43e8b0687a223acd0712b2fd"
      availability: available
    - path: src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.test.tsx
      relationship: supporting
      representation: test
      function: verification
      format: typescript-react
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
      locator: "linhas 141-166 (CRITICAL — Acessibilidade e responsividade) e 214-220 (Testes de acessibilidade)"
      content_state: commit
      revision: "5266771db464515c43e8b0687a223acd0712b2fd"
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RNF02 e RNF03"
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
  rationale: "Trata-se de análise de acessibilidade e navegação por teclado em componente e testes de interface no frontend."
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

# Análise de decisão — Validação de leitor de tela e navegação por teclado na página de vagas (#407)

## Solicitação original

Issue #407 ([F11.9]): "Validar leitor de tela e navegação por teclado na página de vagas, incluindo vazio e erro."

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
| `src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.tsx` | primary | source-code | production | typescript-react | whole-file | commit `5266771` |
| `src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.css` | supporting | source-code | production | css | whole-file | commit `5266771` |
| `src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.test.tsx` | supporting | test | verification | typescript-react | whole-file | commit `5266771` |
| `src/frontend/AGENTS.md` | supporting | prose | prompt-instruction | markdown | L141-L166, L214-L220 | commit `5266771` |
| `docs/requisitos_nao_funcionais.md` | supporting | prose | documentation | markdown | RNF02, RNF03 | commit `5266771` |

### Limites da evidência dos artefatos

Os arquivos foram inspecionados em seu conteúdo completo no commit `5266771`.

## Problema enriquecido

### Resultado desejado
Garantir que a tela `TelaVagasGrupo2` atenda plenamente aos critérios de acessibilidade WCAG 2.1 AA e às diretrizes de `src/frontend/AGENTS.md`, permitindo navegação completa via teclado (`Tab`, `Shift+Tab`, `Enter`, `Space`) e anúncios em tempo hábil para leitores de tela em todos os seus quatro estados fundamentais: carregamento, listagem com resultados, estado vazio e estado de erro recuperável.

### Atores e interesses
- **Pessoa usuária que depende de leitor de tela (NVDA/JAWS/VoiceOver)**: Precisa ser comunicada de forma não intrusiva sobre o carregamento (`role="status"`), anúncios de ausência de vagas (`role="status"`) e alertas assertivos de falha de conexão/serviço (`role="alert"`).
- **Pessoa usuária de navegação exclusiva por teclado**: Precisa de ordem de foco sequencial lógica, indicadores visuais de foco visíveis (`:focus-visible`) e capacidade de submeter buscas e acionar decisões ou recuperação de erros sem uso do mouse.
- **Equipe de desenvolvimento e QA**: Precisa de suíte automatizada de testes dedicada (`TelaVagasGrupo2.a11y.test.tsx`) rápida, determinística e executável no ambiente Nix (`.#frontend`).

### Evidências e fatos observados
1. O formulário de busca (`<form className="vagas-grupo2__pesquisa">`) possui rótulo acessível associado via `htmlFor="termo-pesquisa-vagas"`, campo de input do tipo `search` e botão de submissão.
2. O estado de carregamento possui `<p role="status">Carregando vagas sugeridas...</p>`.
3. O estado de erro possui `role="alert"` no container da seção (`<section ... role="alert">`) e botão de recuperação ("Tentar novamente") acessível.
4. O estado vazio atual (`linhas 178-193 de TelaVagasGrupo2.tsx`):
   ```tsx
   <section
     aria-labelledby="titulo-vagas-vazias"
     className="vagas-grupo2__estado"
   >
     <h2 id="titulo-vagas-vazias">Nenhuma vaga encontrada</h2>
     ...
   </section>
   ```
   **Achado**: O estado vazio não possui `role="status"` nem atributo de live region. Para leitores de tela, a transição entre o carregamento e a ausência de vagas não é automaticamente anunciada como uma atualização de status, exigindo navegação manual pelo DOM. Adicionar `role="status"` no elemento de estado vazio resolve a comunicabilidade.
5. Em `TelaVagasGrupo2.css`, há regra explícita `:focus-visible` com contorno de `3px solid #93c5fd` e `outline-offset: 2px` para todos os controles interativos (input, botão pesquisar, botões de decisão, botão recuperar e link de ação).
6. Os testes existentes em `TelaVagasGrupo2.test.tsx` cobrem o comportamento funcional e alguns nomes acessíveis, mas não cobrem formalmente o ciclo de navegação por teclado (`userEvent.tab()`), a presença de live regions nos estados vazio e de erro, nem a acessibilidade completa da suíte.

### Hipóteses
- A inclusão de `role="status"` no container do estado vazio (`<section aria-labelledby="titulo-vagas-vazias" className="vagas-grupo2__estado" role="status">`) é suficiente para suprir a comunicação com leitores de tela sem causar ruído excessivo ou conflito semântico.
- Uma suíte de testes unitários dedicada em `src/frontend/features/listar-vagas/ui/__tests__/TelaVagasGrupo2.a11y.test.tsx` com `userEvent` é capaz de simular fielmente a navegação sequencial por teclado e verificar as propriedades de acessibilidade WCAG.

### Perguntas em aberto
Nenhuma. O escopo é delimitado e os artefatos estão disponíveis.

### Escopo
- Adicionar `role="status"` na renderização do estado vazio em `TelaVagasGrupo2.tsx`.
- Criar a suíte de testes `src/frontend/features/listar-vagas/ui/__tests__/TelaVagasGrupo2.a11y.test.tsx` validando:
  1. Navegação por teclado completa nos estados: formulário, listagem de cards, estado vazio e estado de erro com foco no botão de tentativa.
  2. Comunicação para leitor de tela via `role="status"` e `role="alert"`.
  3. Verificação de nomes acessíveis e atributos ARIA nos botões de decisão e links externos.
- Preservar 100% de aprovação nos testes existentes e na verificação estática de tipos (`npm run check`) e formatação (`npm run format:check`).

### Fora do escopo
- Alterações em APIs de backend ou mocks remotos.
- Redesenho visual ou alteração de regras de negócio de filtragem de vagas.
- Testes E2E via browser real (que pertencem a níveis superiores de teste).

### Critérios de sucesso
- `npm run check` com 0 erros de tipagem.
- `npx vitest run src/frontend/features/listar-vagas/ui/__tests__/TelaVagasGrupo2.a11y.test.tsx` com 100% dos testes passando.
- `npx vitest run src/frontend/features/listar-vagas` sem regressão nos testes existentes.
- Formatação aprovada em `nix develop .#quality --command bash -c "npm run format:check"`.

## Restrições aplicáveis

- **AGENTS.md (raiz e frontend)**: Execução obrigatória via Nix (`.#frontend` e `.#quality`); testes unitários não devem tocar rede real; documentação tripartite para quaisquer novas funções criadas.
- **WCAG 2.1 AA**: Semântica HTML nativa prioritária sobre ARIA; live regions controladas para evitar redundância.

## Classificação comentada

- **Esfera**: `engineering` — implementação técnica de testes e ajuste pontual de semântica acessível.
- **Preocupações**: `user-experience`, `compliance`, `implementation`.
- **Risco**: `low` — alteração cirúrgica com impacto estritamente localizado no componente visual e adição de testes.

## Decisão de roteamento

- Diretório selecionado: `prompts/frontend/`
- Justificativa: A demanda trata exclusivamente da acessibilidade do componente de interface `TelaVagasGrupo2` e de sua suíte de testes de frontend.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `compliance` | Alta | WCAG 2.1 AA e `AGENTS.md` | O projeto exige conformidade com leitores de tela e navegação por teclado. |
| `correctness` | Alta | 100% de asserções determinísticas | Testes de a11y não devem ser frágeis ou sujeitos a condições de corrida. |
| `simplicity` | Média | Alteração mínima em produção | Adicionar apenas o atributo `role="status"` necessário sem criar complexidade estrutural. |

## Alternativas consideradas

- **Alternativa A (Recomendada)**: Ajustar `role="status"` no container de estado vazio de `TelaVagasGrupo2.tsx` e criar a suíte `TelaVagasGrupo2.a11y.test.tsx` com `@testing-library/user-event` simulando a navegação sequencial por teclado (`Tab`, `Enter`) e inspecionando os papéis acessíveis de cada estado.
- **Alternativa B**: Apenas criar testes de acessibilidade no arquivo existente `TelaVagasGrupo2.test.tsx` sem corrigir o estado vazio. (Inviável: deixaria o leitor de tela sem notificação no estado vazio, violando o requisito de [F11.9]).
- **Alternativa C**: Introduzir uma biblioteca externa de anúncios (`aria-live-announcer`). (Inviável: violaria a restrição de não adicionar dependências desnecessárias quando `role="status"` nativo resolve).

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `compliance` | Alta | +2 | -1 | +2 | Alta | Testes e WCAG |
| `correctness` | Alta | +2 | 0 | +1 | Alta | Semântica nativa |
| `simplicity` | Média | +2 | +1 | -2 | Alta | Sem novas libs |

## Histórico e decisão atual

### Decisão da versão anterior
Nenhum — análise inicial.

### Decisão recomendada nesta versão
Adotar a **Alternativa A**:
1. Adicionar `role="status"` à seção de estado vazio em `TelaVagasGrupo2.tsx`.
2. Implementar `src/frontend/features/listar-vagas/ui/__tests__/TelaVagasGrupo2.a11y.test.tsx` cobrindo:
   - Navegação por teclado (`Tab`, `Shift+Tab`) e foco visível em todos os controles.
   - Anúncios acessíveis nos estados de carregamento (`role="status"`), vazio (`role="status"`) e erro (`role="alert"`).
   - Acionamento de busca e botões de decisão via teclado (`Enter`/`Space`).
   - Retentativa via botão acessível no estado de erro.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `compliance` | maximized | Conformidade integral WCAG 2.1 AA na página de vagas | Estados de carregamento, vazio e erro devidamente comunicados a ATs |
| `correctness` | prioritized | Verificação automatizada contínua no CI | Suíte de testes isolada e determinística |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | Mínima intervenção em código de produção | Apenas adição de `role="status"` na tag existente |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `compliance` | Falha no leitor de tela ao esvaziar resultados | Moderada | Usuários de leitores de tela |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `correctness` | Tempo de escrita e execução da suíte a11y | Velocidade imediata | Totalmente aceitável (ganho de robustez) |

## Riscos e efeitos de segunda ordem

- Risco: Flakiness em testes assíncronos de `userEvent`.
  Mitigação: Usar `findBy*` e `await user.tab()` conforme padrão do Testing Library.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Estado vazio anunciado | Presença de `role="status"` no elemento vazio | Asserção Vitest | Falha na asserção `getByRole("status")` |
| Navegação por teclado fluida | Foco transita ordenadamente nos elementos interativos | Teste com `userEvent.tab()` | Elemento focado diverge da ordem visual |

## Handoffs e atividades posteriores

- Executar `$frontend-implementation-v3` informando o caminho desta análise: `prompts/frontend/20261019-073800-vagas-leitor-tela-teclado-v001.md`.

## Síntese

Arquivo criado em `prompts/frontend/20261019-073800-vagas-leitor-tela-teclado-v001.md`. Avalie se o local escolhido é de fato o mais adequado.
