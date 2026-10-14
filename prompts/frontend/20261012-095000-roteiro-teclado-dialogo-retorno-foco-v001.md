---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-12T09:50:00-03:00"
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
    - path: src/frontend/shared/ui/ModalConfirmacao.tsx
      relationship: primary
      representation: source-code
      function: production
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/frontend/AGENTS.md
      relationship: primary
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: selected-section
      locator: "linhas 141-166 (CRITICAL — Acessibilidade e responsividade) e 214-220 (Testes de acessibilidade)"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RNF02 (Acessibilidade - navegação por teclado e sem armadilhas de foco)"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: README.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Testes/Controle de qualidade: avaliação da UI e conformidade"
      content_state: commit
      revision: "530e8f6"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/frontend
  considered_directories: [prompts/frontend, prompts/revisao, prompts/templates]
  confidence: high
  rationale: "A decisão e os artefatos tratam da avaliação de acessibilidade por teclado (a11y/WCAG) e da garantia de contenção e retorno de foco no componente de diálogo modal compartilhado do frontend."
classification:
  sphere: engineering
  concerns: [accessibility, testability, quality]
  decision_kind: design
  scope: subsystem
  lifecycle: development
  urgency: normal
  uncertainty: low
  reversibility: high
  risk: low
---

# Análise de decisão — Roteiro de teclado no diálogo modal e registro do retorno de foco

## Solicitação original

```text
Issue #396: [F11.5] Executar roteiro de teclado no diálogo ou componente equivalente e registrar o retorno de foco.
Planejamento: WBS 1.7.1.*, 1.7.2.*, 1.8.1.* | Início: 2026-10-12 | Entrega: 2026-10-18
Pessoas: Responsável único: @minoruhaga; Apoios: Responsável da fatia validada, Kelly Daiane Miranda Mendes
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Papel de Gustavo Minoru Haga (`@minoruhaga`): Testes / Controle de qualidade (QA), responsável pela verificação da acessibilidade da UI, roteiros de teclado e automações de testes pertinentes.
- O WBS `1.7.1.*`, `1.7.2.*` e `1.8.1.*` prevê testes integrados e E2E de acessibilidade em componentes críticos da jornada.
- Diretrizes mandatórias de `src/frontend/AGENTS.md`:
  - `[CRITICAL]` Toda interface DEVE ser utilizável por teclado, possuir semântica adequada e apresentar foco previsível.
  - `[REQUIRED]` Componentes modais DEVEM conter o foco enquanto abertos (focus trap) e restaurar o foco ao elemento que disparou sua abertura no fechamento (WCAG 2.1.2 e 2.4.3).
  - `[REQUIRED]` O fechamento por `Escape` DEVE ser garantido.
  - `[REQUIRED]` Testes de acessibilidade e teclado DEVEM ser executados no ambiente `nix develop .#frontend`.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Início da linhagem | N/A | v001 | Criação inicial da análise de decisão para a Issue #396 | Define o roteiro de teclado, os achados no diálogo modal e a suíte automatizada de retorno de foco |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/frontend/shared/ui/ModalConfirmacao.tsx` | Primária | Código-fonte | Produção | TSX | Componente de diálogo modal de confirmação existente em `dev` | Commit 530e8f6 |
| `src/frontend/AGENTS.md` | Primária | Prosa | Instrução | Markdown | Regras de arquitetura FSD, acessibilidade e testes | Commit 530e8f6 |
| `docs/requisitos_nao_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RNF02 (Acessibilidade e teclado) | Commit 530e8f6 |

---

## Roteiro de Operação por Teclado e Achados no Diálogo Modal

O roteiro inspecionou o ciclo de vida de teclado do componente [`ModalConfirmacao.tsx`](file:///home/minoru/projetos/sistema-curriculo/src/frontend/shared/ui/ModalConfirmacao.tsx) conforme o padrão WAI-ARIA Modal Dialog Pattern e WCAG 2.1:

1. **Passo 1 (Disparo)**: Usuário foca no botão disparador e pressiona `Enter` ou `Space`.
2. **Passo 2 (Foco Inicial)**: O diálogo é renderizado e o foco é imediatamente transferido para dentro dele (botão Cancelar).
3. **Passo 3 (Navegação Interna e Contenção de Foco - Focus Trap)**: Navegação via `Tab` e `Shift+Tab`.
4. **Passo 4 (Fechamento via Escape)**: Tecla `Escape` fecha o diálogo.
5. **Passo 5 (Fechamento via Botão / Ação)**: Acionamento de Cancelar ou Confirmar fecha o diálogo.
6. **Passo 6 (Retorno de Foco ao Disparador Original)**: Ao fechar, o foco é restaurado ao elemento disparador ativo no momento da abertura.

### Matriz de Rastreabilidade do Roteiro de Teclado

| ID | Item do Roteiro | Critério WCAG | Comportamento Observado no Componente Original | Status | Ação / Correção |
|---|---|---|---|---|---|
| **ROT-01** | Captura de foco inicial na abertura | WCAG 2.4.3 (A) | `useEffect` foca em `refBotaoCancelar.current` quando `aberto === true`. | **Conforme** | Manter e cobrir em teste automatizado. |
| **ROT-02** | Fechamento via tecla Escape | WAI-ARIA Dialog Pattern | Event listener captura tecla `Escape` e chama `onCancelar()`. | **Conforme** | Manter e cobrir em teste automatizado. |
| **ROT-03** | Contenção de foco (*focus trap* com Tab e Shift+Tab) | WCAG 2.1.2 (A) | **FALHA IDENTIFICADA**: Ao navegar com `Tab` a partir do botão Confirmar, o foco escapa para o restante da página (não cicla de volta para Cancelar). Ao navegar com `Shift+Tab` a partir de Cancelar, o foco também escapa. | **Não Conforme (Corrigir)** | Interceptar tecla `Tab` no evento de teclado e manter o foco ciclando exclusivamente entre os botões internos do modal. |
| **ROT-04** | Retorno estrito de foco ao elemento disparador | WCAG 2.4.3 (A) | **FALHA IDENTIFICADA**: Ao fechar o modal (seja por `Escape`, Cancelar ou Confirmar), o componente retornava `null` sem restaurar o foco. O foco do documento era abandonado no `document.body`. | **Não Conforme (Corrigir)** | Capturar o elemento ativo (`document.activeElement` ou `elementoDisparador`) na abertura através de `refDisparador` e restaurar `refDisparador.current.focus()` no fechamento e desmontagem. |

---

## Problema enriquecido

### Resultado desejado

1. **Ajuste de Acessibilidade em `ModalConfirmacao.tsx`**:
   - Salvar a referência do elemento ativo disparador na abertura (`refDisparador.current`).
   - Restaurar o foco no disparador quando `aberto` passar para `false` ou no cleanup/unmount.
   - Adicionar suporte a `elementoDisparador?: HTMLElement | null` nas props como opção explícita.
   - Implementar contenção de foco com `Tab` e `Shift+Tab` mantendo o foco restrito aos botões do modal.
   - Manter 100% de retrocompatibilidade com consumidores existentes.
2. **Nova Suíte de Testes Automatizados `ModalConfirmacao.keyboard.test.tsx`**:
   - Validar a abertura e foco inicial no botão de cancelamento.
   - Validar a contenção de foco com `Tab` e `Shift+Tab` (*focus trap*).
   - Validar o fechamento via `Escape` e o **retorno estrito de foco ao botão disparador**.
   - Validar o fechamento por clique nos botões e restauração de foco ao disparador.

### Critérios de sucesso

- 100% dos testes unitários e de acessibilidade passando no ambiente Nix.
- 0 erros de tipagem no TypeScript.
- Alteração atômica e revisável em menos de 10 minutos.

## Restrições aplicáveis

- `[CRITICAL]` Uso obrigatório do ambiente Nix (`nix develop .#frontend`).
- `[REQUIRED]` Nenhuma alteração pode quebrar testes existentes.
- `[REQUIRED]` A alteração deve ser isolada na branch `feat/issue-396-roteiro-teclado-retorno-foco-dialogo`.

## Decisão recomendada

Implementar os ajustes de contenção e retorno de foco em `ModalConfirmacao.tsx` e criar a suíte de testes `ModalConfirmacao.keyboard.test.tsx`.
Arquivo criado em `prompts/frontend/20261012-095000-roteiro-teclado-dialogo-retorno-foco-v001.md`. Avalie se o local escolhido é de fato o mais adequado.
