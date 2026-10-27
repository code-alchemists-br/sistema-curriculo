---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-26T08:05:00-03:00"
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
    - path: "github:code-alchemists-br/sistema-curriculo#375"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: whole-file
      locator: "título, descrição, planejamento WBS 1.7.1.*, 1.7.2.*, 1.8.1.* e critérios de aceite"
      content_state: external
      revision: "consultada em 2026-10-26; sem identificador imutável"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d023070"
      availability: available
    - path: src/frontend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d023070"
      availability: available
    - path: docs/compatibilidade-responsividade.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: "linhas 1-140 (definição formal de F1.1 e RNF03)"
      content_state: commit
      revision: "d023070"
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "linhas 16 e 32 (RNF03 — Compatibilidade e adaptação da interface)"
      content_state: commit
      revision: "d023070"
      availability: available
    - path: docs/testes/evidencias/f11-11-responsividade-previa.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: "matriz dimensional, breakpoints e catálogo de comportamentos da prévia"
      content_state: commit
      revision: "d023070"
      availability: available
    - path: docs/testes/evidencias/f11-vagas-responsividade-movel.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "linhas 30-120 (critérios de calibração dimensional e ensaio estático)"
      content_state: commit
      revision: "d023070"
      availability: available
    - path: src/frontend/features/visualizar-curriculo/ui/PreviaCurriculo.responsividade.test.tsx
      relationship: supporting
      representation: source-code
      function: test
      format: TypeScript / TSX
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d023070"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/frontend
  considered_directories: [prompts/frontend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A decisão formaliza o roteiro operacional de teste de responsividade das interfaces frontend do sistema conforme a matriz de dispositivos e larguras de tela de F1.1."
classification:
  sphere: engineering
  concerns: [testing, quality, usability]
  decision_kind: guideline
  scope: system
  lifecycle: verification
  urgency: normal
  uncertainty: low
  reversibility: high
  risk: low
---

# Análise de decisão — Roteiro de Teste de Responsividade com Dispositivos F1.1 (Issue #375)

## Solicitação original

GitHub Issue #375: `[F9.6] Criar roteiro de teste de responsividade com dispositivos definidos em F1.1.`
Planejamento: WBS 1.7.1.*, 1.7.2.*, 1.8.1.*.
Início: 2026-10-26. Entrega: 2026-11-01.
Pessoas: Responsável único: `@minoruhaga`. Apoios: Kelly Daiane Miranda Mendes; Rodolpho P. M. Ferreira; Thiago Jose Miranda Matias; Marcelo Aparecido da Rosa.
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.

## Informações complementares

1. Especificação de Base F1.1 (`docs/compatibilidade-responsividade.md`): Define a matriz mandatória de 6 larguras de referência (360px, 480px, 640px, 768px, 1024px e 1280px+), 4 famílias de navegadores modernos (Chrome, Edge, Firefox, Safari) e 10 critérios objetivos de aceitação de responsividade (RNF03).
2. Propósito do Roteiro (F9.6): Transformar a especificação estática de F1.1 em um procedimento operacional passo a passo de teste manual e emulado, orientando tanto a engenharia quanto os papéis de homologação e qualidade na validação contínua de novas telas e fluxos.
3. Relação com Colegas: Este roteiro atua como base habilitadora para os testes de homologação (`@kellyDMmendes` em #378 e #379) e roteiros de aceitação de jornada (`@xavier-dan` em #376).

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Estado | Inexistente | v001 inicial | Elaboração de análise de decisão para a issue #375 | Define a estrutura e critérios do roteiro de teste de responsividade |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `github:code-alchemists-br/sistema-curriculo#375` | primary | prose | documentation | GitHub issue | whole-file | external / 2026-10-26 |
| `AGENTS.md` | context | prose | prompt-instruction | Markdown | whole-file | commit `d023070` |
| `src/frontend/AGENTS.md` | context | prose | prompt-instruction | Markdown | whole-file | commit `d023070` |
| `docs/compatibilidade-responsividade.md` | primary | prose | documentation | Markdown | linhas 1-140 | commit `d023070` |
| `docs/requisitos_nao_funcionais.md` | supporting | prose | documentation | Markdown | linhas 16 e 32 | commit `d023070` |
| `docs/testes/evidencias/f11-11-responsividade-previa.md` | supporting | prose | documentation | Markdown | whole-file | commit `d023070` |
| `docs/testes/evidencias/f11-vagas-responsividade-movel.md` | supporting | prose | documentation | Markdown | linhas 30-120 | commit `d023070` |
| `src/frontend/features/visualizar-curriculo/ui/PreviaCurriculo.responsividade.test.tsx` | supporting | source-code | test | TypeScript / TSX | whole-file | commit `d023070` |

### Limites da evidência dos artefatos

Os documentos e testes do projeto estão consolidados no commit `d023070` da branch `dev`. A especificação F1.1 já é fonte da verdade estável no repositório desde a conclusão do card #168.

## Problema enriquecido

### Resultado desejado

Criar o documento `docs/testes/roteiro-teste-responsividade-f1-1.md` contendo o roteiro formal, sistemático e reprodutível de teste de responsividade, detalhando:
1. Mapeamento dos dispositivos e emuladores recomendados para cada largura de F1.1 (360px, 480px, 640px, 768px, 1024px e 1280px+).
2. Protocolo de configuração de ambiente de inspeção (Chrome/Firefox/Safari DevTools com DPI/DPR calibrados e orientação vertical/horizontal).
3. Matriz de execução por fluxo prioritário do produto (Autenticação, Edição de Perfil/Formação/Experiência, Prévia de Currículo, Busca de Vagas e Exportação).
4. Checklist objetivo de aceitação e oráculos de não conformidade (scroll horizontal indevido, sobreposições de texto, quebra de linha de títulos/datas, elementos de toque < 44x44px, controles ocultos).
5. Modelo estruturado de relatório de evidências para testes manuais e automatizados.

### Atores e interesses

- **Engenharia de Frontend:** Necessita de critérios objetivos e passos claros para testar suas telas antes de abrir PRs.
- **Time de Qualidade / Homologação (`@kellyDMmendes`, `@xavier-dan`):** Precisa de um roteiro padronizado para executar testes de aceitação e registrar laudos com reprodutibilidade.
- **Estudantes e Usuários Finais:** Beneficiam-se de uma experiência consistente, legível e utilizável em qualquer smartphone, tablet ou computador.

### Evidências e fatos observados

- O documento `docs/compatibilidade-responsividade.md` (F1.1) define que a menor largura formalmente suportada é 360px e que rolagens horizontais causadas pelo layout são proibições estritas.
- As evidências de `f11-11-responsividade-previa.md` e `f11-vagas-responsividade-movel.md` demonstraram que os seletores de mídia CSS operam primariamente nos limiares de `30rem` (480px) e `40rem` (640px), exigindo atenção especial aos pontos de transição.
- Dispositivos populares modernos de referência:
  - 360px: Moto G, Samsung Galaxy menores.
  - 480px: Linha iPhone Pro Max em modo retrato, smartphones intermediários.
  - 640px: Smartphones dobráveis desdobrados ou celulares amplos em modo paisagem.
  - 768px: iPad Mini / Tablets compactos em retrato.
  - 1024px: iPad Pro / Desktop compacto.
  - 1280px+: Monitores padrão Full HD e ultrawide.

### Hipóteses

- A formalização deste roteiro padronizado permitirá que futuros testes (incluindo as issues #220, #219, #376 e #379) utilizem a mesma tabela de evidências, reduzindo retrabalho e eliminando inconsistências na coleta de laudos visuais.

### Perguntas em aberto

Nenhuma. Os contratos de design, larguras e navegadores suportados já foram homologados no RNF03 e F1.1.

### Escopo

1. Criação do arquivo de roteiro de teste `docs/testes/roteiro-teste-responsividade-f1-1.md`.
2. Especificação detalhada de procedimentos passo a passo para verificação manual em navegadores desktop (modo responsivo de DevTools) e em dispositivos físicos.
3. Definição do checklist de 10 pontos de aceitação de responsividade com critérios de passa/falha.
4. Rastreabilidade com as issues #168 (F1.1), #375 (F9.6) e com a matriz de rastreabilidade do projeto.

### Fora do escopo

- Implementação de código de telas no frontend ou backend.
- Execução dos testes das telas individuais (que pertencem às respectivas issues de validação como #220 e #219).
- Automação de ferramentas de visual regression testing pagas ou de terceiros.

### Critérios de sucesso

- O roteiro documentado cobre integralmente todas as 6 faixas de resolução de F1.1 e os fluxos críticos de uso.
- Formatação em Markdown limpa e aprovada pelo Prettier do projeto (`npm run format:check`).
- Rastreabilidade bidirecional estabelecida com `docs/compatibilidade-responsividade.md`.

## Restrições aplicáveis

- **Governança de Documentação:** Seguir o padrão de redação técnica e terminologia ubíqua do projeto estabelecido nos `AGENTS.md`.
- **Higiene e Qualidade:** Validação pré-commit com `nix develop .#quality --command bash -c "cd src/frontend && npm run format:check"`.

## Classificação comentada

- **Esfera:** `engineering` — Engenharia de qualidade e procedimentos de teste de software.
- **Preocupações:** `[testing, quality, usability]` — Padronização de testes de aceitação de usabilidade responsiva.
- **Tipo de decisão:** `guideline` — Guia e roteiro de procedimento operacional padrão.
- **Escopo:** `system` — Abrange todas as interfaces de usuário do sistema.
- **Ciclo de vida:** `verification` — Verificação e homologação.
- **Urgência:** `normal` — Planejada na sprint semanal (F9.6).
- **Incerteza:** `low` — Matriz F1.1 já ratificada e estável.
- **Reversibilidade:** `high` — Artefato de documentação técnica.
- **Risco:** `low` — Sem impacto em tempo de execução ou banco de dados.

## Decisão de roteamento

O artefato foi alocado em `prompts/frontend/` pois rege diretamente a estratégia de testes e homologação das interfaces e componentes visuais do frontend.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| Reprodutibilidade operacional | 1 (Alta) | Procedimento replicável por qualquer integrante do time | Permite que qualquer desenvolvedor execute a checagem sem ambiguidades |
| Cobertura dimensional | 2 (Alta) | 100% de aderência aos 6 tamanhos da matriz F1.1 | Garante conformidade contratual com o RNF03 |
| Clareza de oráculos | 3 (Média) | Critérios objetivos de aprovação/reprovação | Evita avaliações puramente subjetivas sobre "beleza" em vez de usabilidade |

## Alternativas consideradas

- **Alternativa A (Recomendada): Roteiro Operacional Estruturado com Checklist e Modelo de Laudo:** Cria um roteiro completo em `docs/testes/roteiro-teste-responsividade-f1-1.md` contendo tabela de dispositivos, passos de emulação no DevTools, checklist de inspeção de 10 itens e template para registro de evidências.
- **Alternativa B: Apenas referenciar a tabela estática de `docs/compatibilidade-responsividade.md`:** Deixa a execução sem guia prático passo a passo, gerando inconsistências entre as evidências coletadas pelos desenvolvedores.
- **Alternativa C: Criação de script automatizado em Playwright/Puppeteer para captura de screenshots:** Não viável no escopo desta issue documental (F9.6) e exigiria dependências externas não configuradas no ambiente Nix atual.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A (Recomendada) | Alternativa B (Apenas link) | Alternativa C (Script externo) | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Reprodutibilidade | 1 | Excelente (passo a passo claro) | Fraca (apenas limites) | Média (complexidade de setup) | Alta | Padrão dos roteiros de F11 |
| Cobertura F1.1 | 2 | Completa (6 faixas mapeadas) | Parcial | Parcial | Alta | Tabela de `compatibilidade-responsividade.md` |
| Custo de manutenção | 3 | Baixo (Markdown versionado) | Baixo | Alto | Alta | Diretrizes do repositório |

## Histórico e decisão atual

### Decisão da versão anterior
Nenhuma (versão inicial).

### Decisão recomendada nesta versão
Adotar a **Alternativa A**, criando o documento formal `docs/testes/roteiro-teste-responsividade-f1-1.md`, consolidando o protocolo passo a passo de ensaio de responsividade para apoiar as validações de toda a equipe.

### Impacto da revisão
Entrega a Issue #375 [F9.6] com alto valor para a governança de testes de homologação do projeto.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Padronização de qualidade | Priorizada | Laudos homogêneos em todas as issues de responsividade | Experiência bem-sucedida em #409 e #366 |
| Fidelidade aos requisitos | Priorizada | Total alinhamento com RNF03 e F1.1 | Documento F1.1 aprovado em dev |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Tempo de revisão | <= 10 minutos | Documento conciso, objetivo e bem diagramado |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Qualidade | Regressões visuais não detectadas em larguras intermediárias | Média | Estudantes em dispositivos móveis |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Roteiro manual | Exige tempo de teste humano nos fluxos de homologação | Automação 100% mecânica | Alta (validações visuais requerem inspeção humana) |

## Riscos e efeitos de segunda ordem

- Risco de atualização de novos breakpoints no CSS sem refletir no roteiro: Mitigado pela menção explícita aos breakpoints vigentes `30rem` e `40rem` e pelo vínculo com a matriz de larguras de F1.1.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Roteiro é compreensível e aplicável | Validação na execução da Issue #220 | Aplicação prática do roteiro | Dúvidas de procedimento durante o teste |
| Formatação impecável | `npm run format:check` sem erros no Prettier | Execução no ambiente quality | Falha de formatação |

## Handoffs e atividades posteriores

- Criação e commit do documento `docs/testes/roteiro-teste-responsividade-f1-1.md`.
- Pull Request associado à Issue #375 contra `dev`.
- Utilização do roteiro nas tarefas subsequentes (#220, #219, #376 e #379).

## Síntese

A análise confirma que a Issue #375 [F9.6] deve formalizar o roteiro operacional de teste de responsividade baseado na matriz F1.1 (`docs/compatibilidade-responsividade.md`), estruturando procedimentos passo a passo, checklist de 10 oráculos de aceitação e modelo de registro de evidências para o Sistema Currículo.
