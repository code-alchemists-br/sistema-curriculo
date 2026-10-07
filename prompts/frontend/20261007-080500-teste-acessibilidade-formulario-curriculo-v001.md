---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-07T08:05:00-03:00
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
    - path: src/frontend/features/edit-personal-data/ui/FormularioDadosPessoais.tsx
      relationship: primary
      representation: source-code
      function: production
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e403b36"
      availability: available
    - path: src/frontend/AGENTS.md
      relationship: primary
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: selected-section
      locator: "linhas 141-166 (CRITICAL — Acessibilidade e responsividade) e 214-220 (Testes de acessibilidade)"
      content_state: commit
      revision: "e403b36"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF01 a RF03 (Cadastro de dados pessoais e contato)"
      content_state: commit
      revision: "e403b36"
      availability: available
    - path: README.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Testes/Controle de qualidade: avaliação da UI e conformidade"
      content_state: commit
      revision: "e403b36"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/frontend
  considered_directories: [prompts/frontend, prompts/revisao, prompts/templates]
  confidence: high
  rationale: "A decisão e a automação de testes tratam diretamente da camada de apresentação (UI) e conformidade de acessibilidade (WCAG/a11y) do formulário de dados pessoais da jornada de currículo no frontend."
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

# Análise de decisão — Criar teste de acessibilidade do formulário de currículo

## Solicitação original

```text
Issue #152: Criar teste de acessibilidade do formulário de currículo
Automatize a verificação inicial de rótulos, foco e associação de erros em um formulário da jornada.
```

## Informações complementares

- Papel de Gustavo Minoru Haga (Testes/Controle de qualidade): avaliação e automação de testes de UI e qualidade observável.
- Diretrizes mandatórias de `src/frontend/AGENTS.md`:
  - `[CRITICAL]` Toda interface DEVE ser utilizável por teclado, possuir semântica adequada e apresentar campos, estados e erros de forma compreensível.
  - `[REQUIRED]` Elementos HTML semânticos DEVEM ser preferidos. Campos DEVEM possuir identificação acessível; mensagens de erro DEVEM estar associadas aos respectivos campos (`aria-describedby` e `aria-invalid`).
  - `[REQUIRED]` A navegação por foco DEVE permanecer previsível via teclado (`Tab`).
  - `[REQUIRED]` Testes de acessibilidade DEVEM ser executados no ambiente `nix develop .#frontend`.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Início da linhagem | N/A | v001 | Criação inicial da análise de decisão para a Issue #152 | Delimita escopo dos testes de acessibilidade no formulário da jornada |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/frontend/features/edit-personal-data/ui/FormularioDadosPessoais.tsx` | Primária | Código-fonte | Produção | TSX | Componente do formulário de dados pessoais | Commit e403b36 |
| `src/frontend/AGENTS.md` | Primária | Prosa | Instrução | Markdown | Seções de acessibilidade e testes | Commit e403b36 |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF01 a RF03 | Commit e403b36 |
| `README.md` | Contexto | Prosa | Documentação | Markdown | Papéis de QA | Commit e403b36 |

### Limites da evidência dos artefatos

O formulário de dados pessoais (`FormularioDadosPessoais`) já implementa semântica inicial com `label`, `aria-describedby` e `aria-invalid`, mas sua suíte de testes existente (`FormularioDadosPessoais.test.tsx`) cobria apenas o fluxo de envio com mock e preservação de dados em indisponibilidade, sem testar a11y, foco por teclado e associação de erros.

## Problema enriquecido

### Resultado desejado

Implementar uma suíte automatizada de testes dedicada à acessibilidade (`a11y`) para o formulário de dados pessoais e de contato da jornada do currículo, garantindo verificações estritas de:
1. **Rótulos acessíveis:** todos os inputs do formulário devidamente associados a `<label>` com nomes acessíveis legíveis por tecnologias assistivas.
2. **Navegação por foco:** ordem de tabulação sequencial, lógica e previsível entre todos os campos e botões (`userEvent.tab()`).
3. **Associação de erros:** após tentativa de envio inválida, os campos devem possuir `aria-invalid="true"`, estar vinculados às mensagens de erro via `aria-describedby` apontando para IDs existentes no DOM, e limpar esses atributos acessíveis ao serem corrigidos.
4. **Comunicação de status global:** mensagens de feedback devem utilizar `role="status"` ou `role="alert"` para anúncio imediato por leitores de tela.

### Atores e interesses

- **Equipe de QA (Gustavo Minoru Haga):** Automatizar validações de qualidade e acessibilidade para evitar regressões nas regras de WCAG/a11y exigidas no `AGENTS.md`.
- **Estudantes e Usuários com Tecnologias Assistivas:** Garantir que o preenchimento do currículo seja 100% navegável por teclado e compreensível via leitores de tela.
- **Desenvolvedores Frontend:** Possuir suíte rápida que aponte quebras de acessibilidade em refatorações futuras.

### Evidências e fatos observados

- O ecossistema de testes do frontend utiliza `vitest`, `@testing-library/react` e `@testing-library/user-event`.
- `userEvent.setup()` suporta simulação fiel de teclado com `.tab()`.
- `@testing-library/jest-dom` fornece matchers declarativos como `toHaveFocus()`, `toHaveAccessibleName()`, `toBeInvalid()` e `toHaveAttribute("aria-describedby", ...)`.

### Hipóteses

- Criar um arquivo de teste dedicado `FormularioDadosPessoais.a11y.test.tsx` isola a responsabilidade de acessibilidade, mantendo os testes funcionais de negócio em `FormularioDadosPessoais.test.tsx`.

### Escopo

- Implementar `src/frontend/features/edit-personal-data/ui/FormularioDadosPessoais.a11y.test.tsx`.
- Validar rótulos acessíveis em todos os campos.
- Validar fluxo de foco por teclado (`Tab` e `Shift+Tab`).
- Validar vinculação de erros (`aria-invalid`, `aria-describedby` e visibilidade da mensagem de erro).
- Validar anúncios de mensagens de retorno (`role="status"` e `role="alert"`).
- Executar os testes via Nix (`nix develop .#frontend --command npm test`).

### Fora do escopo

- Alterar a lógica de negócio do formulário ou criar novos campos (escopo de feature).
- Testes visuais de contraste de cores (exigem navegador headless com renderização gráfica completa).

### Critérios de sucesso

- 100% dos testes de acessibilidade propostos passando sem falhas no ambiente Nix.
- Verificação de rótulos, foco e associação de erros coberta explicitamente.
- Cumprimento de todas as diretrizes do `src/frontend/AGENTS.md`.

## Restrições aplicáveis

- `[CRITICAL]` Testes executados no ambiente `frontend` do Nix.
- `[REQUIRED]` Código organizado no slice `features/edit-personal-data/ui/`.
- `[REQUIRED]` Docstrings e documentação de testes explicando o que faz, como faz e qual finalidade atende.

## Classificação comentada

- **Esfera:** Engenharia.
- **Preocupações:** Acessibilidade (`accessibility`), testabilidade (`testability`) e qualidade (`quality`).
- **Nível de decisão:** Design de testes de acessibilidade e validação de interface.

## Decisão de roteamento

Alocado em `prompts/frontend` por se tratar de testes de componente e conformidade a11y da interface do usuário.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `accessibility_coverage` | 1 | Cobertura integral de rótulos, foco e erros | Atende diretamente ao enunciado da Issue #152 |
| `determinism` | 2 | Execução isolada com jsdom e vitest | Evita intermitência nos testes de frontend |
| `maintainability` | 3 | Testes declarativos e legíveis | Facilita a expansão para outros formulários da jornada |

## Alternativas consideradas

- **Alternativa A (Recomendada):** Módulo de teste dedicado `FormularioDadosPessoais.a11y.test.tsx` exercitando cenários com `@testing-library/react` e `@testing-library/user-event`.
- **Alternativa B:** Adicionar asserções misturadas dentro de `FormularioDadosPessoais.test.tsx`. (Prejudica a clareza e separação de preocupações entre testes funcionais e testes de acessibilidade).
- **Alternativa C:** Teste pontual manual no navegador. (Inviável para CI e não automatiza a verificação contínua).

## Histórico e decisão atual

### Decisão recomendada nesta versão

Criar o arquivo `src/frontend/features/edit-personal-data/ui/FormularioDadosPessoais.a11y.test.tsx` com suíte completa focada em conformidade de acessibilidade para o formulário da jornada.

## Riscos e efeitos de segunda ordem

- Nenhum risco para o código de produção, pois trata-se exclusivamente de adição de suíte de testes.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Todos os campos têm rótulos acessíveis | `toHaveAccessibleName` em todos os inputs | Teste unitário Vitest | Falha de acessibilidade |
| Navegação por foco é sequencial | Asserções com `user.tab()` e `toHaveFocus()` | Teste unitário Vitest | Foco pulando campos |
| Erros vinculados via aria-describedby | `aria-invalid` e `aria-describedby` conferidos | Teste unitário Vitest | Erros soltos no DOM |

## Handoffs e atividades posteriores

- Reutilização dos padrões de teste de acessibilidade para os demais formulários da jornada (projetos acadêmicos, competências, etc.).
- Base para o teste da jornada completa na Issue #153.

## Síntese

A suíte de testes de acessibilidade automatiza a verificação de rótulos, foco e mensagens de erro do formulário da jornada, garantindo conformidade com o RNF de acessibilidade e WCAG.

Arquivo criado em prompts/frontend/20261007-080500-teste-acessibilidade-formulario-curriculo-v001.md. Avalie se o local escolhido é de fato o mais adequado.
