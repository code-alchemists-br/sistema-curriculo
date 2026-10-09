---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-09T15:30:00-03:00"
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
    - path: src/frontend/features/edit-professional-experience/ui/FormularioExperiencias.tsx
      relationship: primary
      representation: source-code
      function: production
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5b8836c"
      availability: available
    - path: src/frontend/features/edit-professional-experience/ui/FormularioExperiencias.test.tsx
      relationship: supporting
      representation: source-code
      function: test
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5b8836c"
      availability: available
    - path: src/frontend/AGENTS.md
      relationship: primary
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: selected-section
      locator: "linhas 141-166 (CRITICAL — Acessibilidade e responsividade) e 214-220 (Testes de acessibilidade)"
      content_state: commit
      revision: "5b8836c"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF01 a RF03 (Cadastro de dados do estudante e experiências)"
      content_state: commit
      revision: "5b8836c"
      availability: available
    - path: README.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Testes/Controle de qualidade: avaliação da UI e conformidade"
      content_state: commit
      revision: "5b8836c"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/frontend
  considered_directories: [prompts/frontend, prompts/revisao, prompts/templates]
  confidence: high
  rationale: "A decisão trata da correção de acessibilidade (a11y/WCAG) e da criação da suíte de testes de acessibilidade no componente de formulário de experiências profissionais da jornada de currículo."
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

# Análise de decisão — Corrigir falha de acessibilidade no formulário de experiências profissionais

## Solicitação original

```text
Issue #368: [F8.12] Corrigir uma falha de acessibilidade por card, com teste automatizado ou roteiro manual rastreável.
WBS: 1.2.1.3–1.2.1.4, 1.4.2.4, 1.5.2.4
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Papel de Gustavo Minoru Haga (`@minoruhaga`): Testes/Controle de qualidade (QA), responsável pela garantia de acessibilidade da UI e testes automatizados.
- O WBS 1.4.2.4 mapeia a etapa de experiências profissionais do estudante no frontend.
- Regras mandatórias de `src/frontend/AGENTS.md`:
  - `[CRITICAL]` Toda interface nova ou alterada DEVE ser utilizável por teclado, possuir semântica adequada e apresentar campos, estados e erros de forma compreensível.
  - `[REQUIRED]` Elementos HTML semânticos DEVEM ser preferidos. Campos DEVEM possuir identificação acessível; mensagens de erro DEVEM estar associadas aos respectivos campos (`aria-describedby` e `aria-invalid`).
  - `[REQUIRED]` A navegação por foco DEVE permanecer previsível via teclado (`Tab`).
  - `[REQUIRED]` Mudanças relevantes de estado e erros DEVEM ser comunicados de forma acessível (`role="alert"` para erros, `role="status"` para confirmações).
  - `[REQUIRED]` Testes de acessibilidade DEVEM ser executados no ambiente `nix develop .#frontend`.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Início da linhagem | N/A | v001 | Criação inicial da análise de decisão para a Issue #368 | Define as correções de acessibilidade em `FormularioExperiencias.tsx` e a nova suíte de testes |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/frontend/features/edit-professional-experience/ui/FormularioExperiencias.tsx` | Primária | Código-fonte | Produção | TSX | Componente do formulário de experiências profissionais | Commit 5b8836c |
| `src/frontend/features/edit-professional-experience/ui/FormularioExperiencias.test.tsx` | Apoio | Código-fonte | Teste | TSX | Testes existentes de negócio da feature | Commit 5b8836c |
| `src/frontend/AGENTS.md` | Primária | Prosa | Instrução | Markdown | Regras de arquitetura FSD, acessibilidade e testes | Commit 5b8836c |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF01 a RF03 | Commit 5b8836c |
| `README.md` | Contexto | Prosa | Documentação | Markdown | Papéis de QA | Commit 5b8836c |

### Limites da evidência dos artefatos

O componente `FormularioExperiencias` já possuía `aria-describedby` e `aria-invalid` nos campos de texto básicos, mas apresentava três falhas críticas de acessibilidade:
1. O checkbox "Emprego atual" não possuía atributo `id` nem vínculo programático explícito com `<label htmlFor={id}>`, ao contrário de todos os outros inputs do formulário.
2. Ao submeter com campos obrigatórios vazios ou inválidos, os erros locais eram calculados, mas nenhuma mensagem global de alerta acessível era gerada (`setMensagem` não era chamado em falha de validação). Usuários de leitores de tela ficavam sem qualquer anúncio sonoro de que a tentativa de salvar havia falhado.
3. A tag de feedback global `<p className="form-message" role="status">` usava estaticamente `role="status"` (apropriado apenas para mensagens informativas de cortesia), violando as diretrizes WCAG 4.1.3 e 3.3.1 que exigem `role="alert"` (assertivo) para comunicação de erros e pendências críticas.

## Problema enriquecido

### Resultado desejado

1. **Correção no componente `FormularioExperiencias.tsx`:**
   - Adicionar identificador explícito `${prefixo}-emprego-atual` ao input checkbox e associá-lo ao respectivo `<label htmlFor={`${prefixo}-emprego-atual`}>`.
   - Na falha de validação da submissão, emitir mensagem global de pendência (`"Há campos obrigatórios não preenchidos."`).
   - Ajustar o papel da mensagem global para usar dinamicamente `role={mensagem.includes("sucesso") ? "status" : "alert"}`.
   - Limpar a mensagem global assim que o usuário corrigir campos ou tentar nova interação.
2. **Nova suíte de testes de acessibilidade `FormularioExperiencias.a11y.test.tsx`:**
   - Testar que todos os campos (empresa, cargo, início, fim, emprego atual, descrição e botões) possuem identificação e rótulos acessíveis.
   - Testar a ordem de foco e tabulação sequencial via teclado (`Tab` e `Shift+Tab`).
   - Testar a vinculação de erros aos campos via `aria-invalid="true"` e `aria-describedby` apontando para o elemento de erro no DOM.
   - Testar que o envio inválido anuncia mensagem com `role="alert"`, enquanto o envio com sucesso anuncia com `role="status"`.
   - Testar a desabilitação e reabilitação acessível do campo de data final ao alternar "Emprego atual".

### Atores e interesses

- **Equipe de QA (Gustavo Minoru Haga):** Cumprir o critério de aceite da Issue #368 ([F8.12]), entregando uma correção de acessibilidade acompanhada de suíte de testes automatizada, isolada e verificável em menos de 10 minutos.
- **Pessoas com Deficiência e Usuários de Tecnologias Assistivas:** Conseguir preencher e corrigir suas experiências profissionais com leitores de tela e navegação por teclado sem bloqueios.
- **Desenvolvedores Frontend:** Garantir que futuras alterações não regridam a conformidade WCAG do formulário.

### Evidências e fatos observados

- `npm test` do frontend executa testes em ambiente `jsdom` via Vitest e Testing Library.
- Os 8 testes existentes em `FormularioExperiencias.test.tsx` continuam passando sem regressões.

### Hipóteses

- Corrigir a identificação do checkbox e o anúncio de mensagens de erro globais resolve de forma definitiva o problema de acessibilidade apontado no card.
- Isolar os testes de acessibilidade em `FormularioExperiencias.a11y.test.tsx` preserva o foco dos testes unitários funcionais já existentes em `FormularioExperiencias.test.tsx`.

### Escopo

- Modificar `src/frontend/features/edit-professional-experience/ui/FormularioExperiencias.tsx`.
- Criar `src/frontend/features/edit-professional-experience/ui/FormularioExperiencias.a11y.test.tsx`.
- Validar via `npm run check` e `npm test` no ambiente Nix (`nix develop .#frontend`).

### Fora do escopo

- Alteração das regras de negócio do modelo `experiencias.ts` (já estável e validado).
- Mudanças em outros formulários da aplicação.

### Critérios de sucesso

- 100% dos testes unitários e de acessibilidade passando no ambiente Nix.
- 0 erros de tipagem no TypeScript.
- Alteração atômica e verificável em menos de 10 minutos.

## Restrições aplicáveis

- `[CRITICAL]` Uso obrigatório do ambiente Nix (`nix develop .#frontend`).
- `[REQUIRED]` Nenhuma quebra de testes pré-existentes.
- `[REQUIRED]` Documentação completa com docstrings explicando o que faz, como faz e qual finalidade atende.

## Classificação comentada

- **Esfera:** Engenharia.
- **Preocupações:** Acessibilidade (`accessibility`), testabilidade (`testability`), qualidade (`quality`).
- **Nível de decisão:** Correção de interface e automação de testes de acessibilidade.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `accessibility` | 1 | Conformidade estrita com WCAG 2.1 e ARIA | Garante usabilidade para tecnologias assistivas |
| `backward_compatibility` | 2 | Preservar 100% dos testes funcionais existentes | Impede quebras em contratos já estabelecidos |
| `isolation` | 3 | Arquivo dedicado de testes de a11y | Facilita manutenção e clareza de escopo |

## Alternativas consideradas

- **Alternativa A (Recomendada):** Corrigir a associação do checkbox e adicionar anúncio assertivo de erro com `role="alert"` em `FormularioExperiencias.tsx`, criando suíte dedicada `FormularioExperiencias.a11y.test.tsx`.
- **Alternativa B:** Apenas adicionar os testes em `FormularioExperiencias.test.tsx` sem corrigir a ausência do alerta global e sem rótulo explícito no checkbox (incompleto e não corrige a falha).

## Histórico e decisão atual

### Decisão recomendada nesta versão

Implementar a Alternativa A na branch `feat/issue-368-corrigir-falha-acessibilidade`.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Checkbox possui identificação acessível explícita | Input com ID e associado ao Label | Teste Vitest | Falha na busca por acessible name ou ID |
| Erro de submissão anunciado assertivamente | Elemento no DOM com `role="alert"` | Teste Vitest | Elemento com `role="status"` ou ausente |
| Testes existentes continuam passando | 8/8 testes verdes em `FormularioExperiencias.test.tsx` | Vitest via Nix | Quebra de qualquer teste existente |
