---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-12T09:40:00-03:00"
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
    - path: src/frontend/features/acesso-estudante/ui/FormularioCadastro.tsx
      relationship: primary
      representation: source-code
      function: production
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/frontend/features/acesso-estudante/ui/FormularioAcesso.tsx
      relationship: supporting
      representation: source-code
      function: production
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/frontend/pages/acesso-estudante/ui/PaginaAcessoEstudante.tsx
      relationship: supporting
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
      locator: "RNF02 (Acessibilidade - navegação por teclado, identificação de campos e erros)"
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
  rationale: "A decisão e os artefatos tratam diretamente da auditoria de acessibilidade (a11y/WCAG) e da garantia automatizada de rótulos, foco e retorno de erros no formulário de cadastro do frontend."
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

# Análise de decisão — Varredura manual de rótulos e foco no formulário de cadastro e registro de achados rastreáveis

## Solicitação original

```text
Issue #395: [F11.4] Executar varredura manual de rótulos e foco no formulário de cadastro e registrar achados rastreáveis.
Planejamento: WBS 1.7.1.*, 1.7.2.*, 1.8.1.* | Início: 2026-10-12 | Entrega: 2026-10-18
Pessoas: Responsável único: @minoruhaga; Apoios: Responsável da fatia validada, Kelly Daiane Miranda Mendes
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Papel de Gustavo Minoru Haga (`@minoruhaga`): Testes / Controle de qualidade (QA), responsável pela avaliação de conformidade observável da UI, acessibilidade e automação de testes correspondentes.
- O WBS `1.7.1.*` e `1.8.1.*` estabelece os testes de qualidade observável e acessibilidade para formulários da aplicação.
- Diretrizes mandatórias de `src/frontend/AGENTS.md`:
  - `[CRITICAL]` Toda interface DEVE ser utilizável por teclado, possuir semântica adequada e apresentar campos, estados e erros de forma compreensível.
  - `[REQUIRED]` Elementos HTML semânticos DEVEM ser preferidos. Campos DEVEM possuir identificação acessível; mensagens de erro DEVEM estar associadas aos respectivos campos (`aria-describedby` e `aria-invalid`).
  - `[REQUIRED]` A navegação por foco DEVE permanecer previsível via teclado (`Tab`).
  - `[REQUIRED]` Mensagens de alerta e erro DEVEM usar `role="alert"` (anúncio assertivo imediato), e confirmações DEVEM usar `role="status"`.
  - `[REQUIRED]` Testes de acessibilidade DEVEM ser executados no ambiente `nix develop .#frontend`.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Início da linhagem | N/A | v001 | Criação inicial da análise de decisão para a Issue #395 | Registra os achados rastreáveis da varredura de acessibilidade e a especificação da suíte automatizada |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/frontend/features/acesso-estudante/ui/FormularioCadastro.tsx` | Primária | Código-fonte | Produção | TSX | Componente do formulário de cadastro de conta do estudante | Commit 530e8f6 |
| `src/frontend/features/acesso-estudante/ui/FormularioAcesso.tsx` | Apoio | Código-fonte | Produção | TSX | Componente do formulário de acesso de credenciais | Commit 530e8f6 |
| `src/frontend/pages/acesso-estudante/ui/PaginaAcessoEstudante.tsx` | Apoio | Código-fonte | Produção | TSX | Porta de entrada que compõe o formulário de cadastro | Commit 530e8f6 |
| `src/frontend/AGENTS.md` | Primária | Prosa | Instrução | Markdown | Regras de acessibilidade, FSD e qualidade | Commit 530e8f6 |
| `docs/requisitos_nao_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RNF02 (Acessibilidade) | Commit 530e8f6 |

---

## Matriz de Varredura e Achados Rastreáveis (WCAG 2.1 AA)

A varredura manual e técnica inspecionou os seguintes elementos do `FormularioCadastro.tsx`:
1. Campo **Nome** (`#nome`)
2. Campo **E-mail** (`#email-cadastro`)
3. Campo **Senha** (`#senha-cadastro`)
4. Campo **Confirme a senha** (`#confirmacao-senha`)
5. Botão **Criar conta** (`button[type="submit"]`)
6. Região de mensagens e feedback global (`.form-message`)

### Tabela de Rastreabilidade de Achados

| ID do Achado | Critério WCAG | Item Verificado | Comportamento Observado | Status de Conformidade | Ação / Recomendação |
|---|---|---|---|---|---|
| **ACH-01** | WCAG 1.3.1 (A), 4.1.2 (A) | Rótulos acessíveis dos 4 campos de entrada | Todos os campos utilizam `<label htmlFor={id}>` explicitamente vinculado ao `id` do `<input>`. Leitores de tela anunciam corretamente os nomes acessíveis "Nome", "E-mail", "Senha" e "Confirme a senha". | **Conforme** | Manter estrutura existente. |
| **ACH-02** | WCAG 2.1.1 (A), 2.4.3 (A) | Ordem de foco e tabulação sequencial | A navegação via `Tab` e `Shift+Tab` segue a sequência natural: Nome → E-mail → Senha → Confirme a senha → Criar conta, sem armadilhas de teclado. | **Conforme** | Manter e cobrir em teste automatizado via `userEvent.tab()`. |
| **ACH-03** | WCAG 2.4.7 (AA) | Indicadores visíveis de foco | Inputs e botões recebem indicador nativo de foco do navegador quando navegados por teclado. | **Conforme** | Manter conformidade. |
| **ACH-04** | WCAG 1.3.1 (A), 3.3.1 (A) | Associação programática de erros individuais aos campos | Quando um campo apresenta erro de validação (ex: e-mail inválido ou senhas divergentes), o elemento recebe `aria-invalid="true"` e `aria-describedby={`${id}-erro`}` apontando para o `<p id={`${id}-erro`}>`. | **Conforme** | Cobrir em teste automatizado. |
| **ACH-05** | WCAG 3.3.1 (A), 4.1.3 (AA) | Feedback global ao submeter com campos inválidos | **FALHA IDENTIFICADA**: Ao clicar em "Criar conta" com pendências de preenchimento, `enviarCadastro` executa `setErros(novosErros)`, mas **não define mensagem global** (`setMensagem` permanece `null`). A submissão falha de forma silenciosa para quem usa leitores de tela na live region. | **Não Conforme (Corrigir)** | Em caso de erro de validação local no submit, emitir mensagem assertiva na live region (`role="alert"`): `"Há pendências que precisam ser corrigidas antes de criar a conta."`. |
| **ACH-06** | WCAG 4.1.3 (AA) | Live region em erro de API | Quando a chamada remota da API falha (ex.: e-mail em uso ou indisponibilidade), a mensagem é apresentada com `role="alert"`. | **Conforme** | Manter e cobrir em teste automatizado. |

---

## Problema enriquecido

### Resultado desejado

1. **Correção de Acessibilidade em `FormularioCadastro.tsx`**:
   - Atualizar `enviarCadastro` para que, ao constatar erros de validação local, defina a mensagem global de alerta: `"Há pendências que precisam ser corrigidas antes de criar a conta."`.
   - Limpar a mensagem global no método `atualizarCampo` quando o estudante reiniciar a digitação para corrigir o campo.
   - Preservar tipagens estritas e padrão de documentação de código do projeto.
2. **Nova Suíte de Testes de Acessibilidade `FormularioCadastro.a11y.test.tsx`**:
   - Automatizar a validação dos achados ACH-01 a ACH-06 com `@testing-library/react` e `@testing-library/user-event`.
   - Garantir que a suíte seja executável de forma rápida, determinística e verificável em menos de 10 minutos no ambiente `nix develop .#frontend`.

### Atores e interesses

- **Equipe de QA (Gustavo Minoru Haga):** Cumprir o compromisso da Issue #395 ([F11.4]), entregando catálogo de achados rastreáveis e testes automatizados de garantia de acessibilidade.
- **Estudantes com deficiência visual ou motora:** Navegar com autonomia pelo formulário de criação de conta usando leitores de tela e teclado.

## Restrições aplicáveis

- `[CRITICAL]` Uso obrigatório do ambiente Nix (`nix develop .#frontend`).
- `[REQUIRED]` Nenhuma alteração pode quebrar testes existentes.
- `[REQUIRED]` A alteração deve ser isolada na branch `feat/issue-395-varredura-rotulos-foco-cadastro`.

## Alternativas consideradas

- **Alternativa A (Recomendada):** Registrar o catálogo de achados, sanar o ACH-05 com mensagem assertiva global no formulário e criar a suíte automatizada `FormularioCadastro.a11y.test.tsx`.
- **Alternativa B:** Apenas documentar os achados sem criar a suíte automatizada ou sem corrigir a falha silenciosa de submit (incompleta, violando o critério de aceite de testes pertinentes e verificabilidade).

## Decisão recomendada

Adotar a **Alternativa A**.
Arquivo criado em `prompts/frontend/20261012-094000-varredura-rotulos-foco-cadastro-v001.md`. Avalie se o local escolhido é de fato o mais adequado.
