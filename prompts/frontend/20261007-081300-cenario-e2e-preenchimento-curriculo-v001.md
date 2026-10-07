---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-07T08:13:00-03:00"
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
    - path: docs/mapeamento_jornadas.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Seções 5 e 6 (Jornada única: preencher, revisar e gerar currículo)"
      content_state: commit
      revision: "e403b36"
      availability: available
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
    - path: src/frontend/features/validate-curriculum/ui/TelaValidacaoCurriculo.tsx
      relationship: primary
      representation: source-code
      function: production
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e403b36"
      availability: available
    - path: src/frontend/features/validate-curriculum/model/validacao-curriculo.ts
      relationship: primary
      representation: source-code
      function: production
      format: typescript
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e403b36"
      availability: available
    - path: src/frontend/pages/personal-data/ui/PaginaDadosPessoais.tsx
      relationship: supporting
      representation: source-code
      function: production
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e403b36"
      availability: available
    - path: src/frontend/pages/validacao-curriculo/ui/PaginaValidacaoCurriculo.tsx
      relationship: supporting
      representation: source-code
      function: production
      format: typescript-react
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e403b36"
      availability: available
    - path: src/frontend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: selected-section
      locator: "Qualidade e testes (E2E e jornada)"
      content_state: commit
      revision: "e403b36"
      availability: available
    - path: README.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Papéis da equipe: Testes/Controle de qualidade e testes E2E"
      content_state: commit
      revision: "e403b36"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/frontend
  considered_directories: [prompts/frontend, prompts/revisao, prompts/templates]
  confidence: high
  rationale: "A decisão e os testes automatizam o fluxo integrado de ponta a ponta (E2E) da jornada do currículo no frontend, desde a coleta de dados pessoais até a revisão final e exportação."
classification:
  sphere: engineering
  concerns: [reliability, testability, quality]
  decision_kind: design
  scope: subsystem
  lifecycle: development
  urgency: normal
  uncertainty: low
  reversibility: high
  risk: low
---

# Análise de decisão — Preparar cenário E2E de preenchimento do currículo

## Solicitação original

```text
Issue #153: Preparar cenário E2E de preenchimento do currículo
Monte o fluxo automatizado inicial de dados pessoais até a revisão, usando doubles quando necessário.
```

## Informações complementares

- Atribuição de Gustavo Minoru Haga (Testes/Controle de qualidade): *"Responsáveis pelos testes integrados e E2E. Avaliação do design de UX bem como os testes da UI. Criação de doubles de testes para si mesmos e para outros membros da equipe conforme necessidade."*
- Conforme o documento `docs/mapeamento_jornadas.md`, a jornada principal do estudante inicia em **Dados pessoais e contato** (Seção 6.3), avança pelas seções curriculares e culmina em **Revisar e editar / Validação** (Seções 6.7 e 6.8), liberando as ações de confirmação e exportação (PDF/DOCX).
- A automação deve utilizar doubles injetados para simular persistência assíncrona, respostas da API e ações finais sem acoplamento a rede ou backend físico.
- Regras de qualidade de `src/frontend/AGENTS.md`:
  - `[REQUIRED]` Fluxos críticos da jornada de currículo devem possuir cobertura de testes automatizados.
  - `[REQUIRED]` Testes devem validar comportamento observável e contratos públicos.
  - `[REQUIRED]` Documentação completa com o que faz, como faz e qual finalidade atende.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Início da linhagem | N/A | v001 | Criação inicial da análise de decisão para a Issue #153 | Define arquitetura do teste E2E da jornada do currículo |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `docs/mapeamento_jornadas.md` | Primária | Prosa | Documentação | Markdown | Seções 5 e 6 (Fluxo e etapas da jornada) | Commit e403b36 |
| `src/frontend/features/edit-personal-data/ui/FormularioDadosPessoais.tsx` | Primária | Código-fonte | Produção | TSX | Etapa inicial de dados pessoais | Commit e403b36 |
| `src/frontend/features/validate-curriculum/ui/TelaValidacaoCurriculo.tsx` | Primária | Código-fonte | Produção | TSX | Etapa final de revisão e validação | Commit e403b36 |
| `src/frontend/features/validate-curriculum/model/validacao-curriculo.ts` | Primária | Código-fonte | Produção | TS | Contrato de validação e regras de bloqueio | Commit e403b36 |
| `src/frontend/pages/personal-data/ui/PaginaDadosPessoais.tsx` | Apoio | Código-fonte | Produção | TSX | Composição da página de dados pessoais | Commit e403b36 |
| `src/frontend/pages/validacao-curriculo/ui/PaginaValidacaoCurriculo.tsx` | Apoio | Código-fonte | Produção | TSX | Composição da página de validação final | Commit e403b36 |
| `src/frontend/AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Padrões de teste e arquitetura FSD | Commit e403b36 |
| `README.md` | Contexto | Prosa | Documentação | Markdown | Papéis de QA | Commit e403b36 |

### Limites da evidência dos artefatos

O frontend possui as páginas e componentes de cada etapa desacoplados; a navegação global por roteador ainda não está unificada em um único componente App. Portanto, para testar a jornada de ponta a ponta (E2E) de forma coesa, o teste deve exercitar o fluxo através de um orquestrador de jornada de teste (`JornadaPreenchimentoCurriculoHarness` ou fluxo progressivo) que integra a coleta de dados pessoais, o preenchimento de seções e a transição para a revisão final com validação de ações de exportação.

## Problema enriquecido

### Resultado desejado

Implementar uma suíte de testes E2E/integração que automatize a jornada completa do estudante:
1. **Início da jornada:** o estudante acessa a etapa de dados pessoais e contato, informa dados válidos e submete o formulário com dublê assíncrono.
2. **Progressão curricular:** os dados do estudante são propagados para o modelo de validação do currículo juntamente com as seções preenchidas (formação acadêmica, experiências profissionais, competências e projetos).
3. **Revisão e Validação:** o fluxo avança para a tela de revisão final (`TelaValidacaoCurriculo`), confirmando que:
   - Todas as seções obrigatórias aparecem como válidas (`status: valida`).
   - O indicador de feedback exibe `Todas as seções obrigatórias estão válidas` com `role="status"`.
   - As ações de "Visualizar prévia", "Confirmar currículo" e "Exportar PDF" são desbloqueadas.
   - O acionamento dessas ações dispara os respectivos dublês de sucesso.
4. **Cenário de bloqueio por pendência:** quando o fluxo possui uma etapa obrigatória pulada ou inconsistente, a revisão exibe alerta com `role="alert"`, lista a pendência e mantém bloqueadas as ações de exportação e confirmação.

### Atores e interesses

- **Equipe de QA (Gustavo Minoru Haga):** Garantir a cobertura da jornada ponta a ponta conforme especificado na matriz de requisitos e na Issue #153.
- **Desenvolvedores Frontend:** Assegurar que os dados fluem corretamente entre a etapa inicial de dados pessoais e a tela final de validação.
- **Usuários:** Ter a certeza de que a experiência do Wizard funciona de ponta a ponta sem falhas de integração visual.

### Evidências e fatos observados

- O contrato `validarCurriculo` de `validate-curriculum` valida de forma estrita o objeto `CurriculoParaValidacao`.
- `FormularioDadosPessoais` converte inputs para `Student` e salva via `ClienteDadosPessoais.salvar()`.
- O dublê permite capturar o payload enviado e propagá-lo para a etapa de revisão.

### Hipóteses

- Montar um fluxo E2E utilizando `userEvent` para simular cliques reais e digitação do usuário produz uma verificação robusta e de alta fidelidade da experiência do aluno.
- Testar o caminho feliz (todas as seções completas) e o caminho de pendência (seção pulada bloqueando ações) assegura a cobertura de ambos os lados da regra de negócio.

### Escopo

- Implementar `src/frontend/app/jornada-curriculo.e2e.test.tsx` com suíte E2E automatizada da jornada.
- Integrar dublês de dados pessoais e de ações de revisão (prévia, confirmação, exportação).
- Cobrir o fluxo completo desde o formulário de dados pessoais até os botões da revisão final.
- Cobrir cenário alternativo com pendências bloqueando exportação.
- Validar via Nix (`nix develop .#frontend`).

### Fora do escopo

- Implementar geração de arquivos binários reais (PDF/DOCX) no navegador (escopo de exportação).
- Integração com backend real PostgreSQL.

### Critérios de sucesso

- Testes E2E executando e passando 100% no ambiente Nix.
- Jornada de ponta a ponta verificada com asserções observáveis do DOM.
- Total conformidade com o `src/frontend/AGENTS.md`.

## Restrições aplicáveis

- `[CRITICAL]` Testes executados no ambiente `nix develop .#frontend`.
- `[REQUIRED]` Uso de Feature-Sliced Design e isolamento de dependências.
- `[REQUIRED]` Docstrings e documentação explicando o que faz, como faz e qual finalidade atende.

## Classificação comentada

- **Esfera:** Engenharia.
- **Preocupações:** Confiabilidade (`reliability`), testabilidade (`testability`) e qualidade (`quality`).
- **Nível de decisão:** Design de testes E2E e integração de fluxo da jornada.

## Decisão de roteamento

Alocado em `prompts/frontend` por se tratar da jornada do usuário e dos componentes da interface frontend.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `e2e_fidelity` | 1 | Interação real com userEvent do início ao fim | Garante teste de alta fidelidade sem atalhos |
| `isolation` | 2 | Doubles determinísticos para clientes externos | Impede oscilação e dependência de rede |
| `completeness` | 3 | Validação de sucesso e de bloqueio por pendência | Garante a integridade das regras da jornada |

## Alternativas consideradas

- **Alternativa A (Recomendada):** Teste de integração E2E em `src/frontend/app/jornada-curriculo.e2e.test.tsx` com componente orquestrador de jornada reproduzindo a progressão real do Wizard.
- **Alternativa B:** Testar cada tela isoladamente sem conectá-las. (Não atende ao requisito de teste E2E da jornada).
- **Alternativa C:** Teste com Cypress/Playwright abrindo navegador externo. (Pesado e não configurado no flake atual do repositório; o `vitest` + `jsdom` já atende com alta velocidade e compatibilidade).

## Histórico e decisão atual

### Decisão recomendada nesta versão

Criar o arquivo `src/frontend/app/jornada-curriculo.e2e.test.tsx` montando a jornada interativa de preenchimento de dados pessoais até a revisão final e exportação, usando doubles controlados.

## Riscos e efeitos de segunda ordem

- Nenhum risco para o código de produção, pois trata-se exclusivamente da adição de testes E2E.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Fluxo feliz chega à revisão e libera exportação | Botão "Exportar PDF" habilitado e acionado | Vitest via Nix | Botão desabilitado ou erro |
| Pendência bloqueia exportação | Botão "Exportar PDF" disabled | Vitest via Nix | Botão liberado indevidamente |

## Handoffs e atividades posteriores

- Conclusão do pacote de 4 issues de QA (#151, #152, #153 e #154) atribuídas a Gustavo Minoru Haga.
- Handoff para integração contínua e validação pelo PM.

## Síntese

O teste E2E automatiza a jornada do estudante desde o preenchimento de dados pessoais até a validação e liberação de exportação do currículo, consolidando a qualidade do fluxo principal.

Arquivo criado em prompts/frontend/20261007-081300-cenario-e2e-preenchimento-curriculo-v001.md. Avalie se o local escolhido é de fato o mais adequado.
