---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-31T21:20:54-03:00"
lineage:
  mode: initial
  root: null
  supersedes: null
  change_type: initial
  secondary_change_types: []
  decision_impact: initial
subjects:
  kind: repository
  files:
    - path: "AGENTS.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "src/backend/AGENTS.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "src/frontend/AGENTS.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: ".agents/skills/decision-analysis-v4/SKILL.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/decision-analysis-v4/references/classification-taxonomy.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/decision-analysis-v4/references/output-schema.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/decision-analysis-v4/references/output-routing.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/decision-analysis-v4/references/artifact-classification.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/requisitos_funcionais.md"
      relationship: "primary"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/requisitos_nao_funcionais.md"
      relationship: "primary"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/mapeamento_jornadas.md"
      relationship: "primary"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/casos-de-uso-v2.md"
      relationship: "primary"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/manual-estudante.md"
      relationship: "primary"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/dossie-aceite.md"
      relationship: "primary"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/registro-aceite-licoes.md"
      relationship: "primary"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/checklist-demonstracao.md"
      relationship: "primary"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/exportacao-pdf-docx.md"
      relationship: "primary"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/acessibilidade.md"
      relationship: "primary"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/compatibilidade-responsividade.md"
      relationship: "primary"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/matriz_rastreabilidade.md"
      relationship: "primary"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/matriz_testes.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Cenários RF01–RF15 e tabela de cobertura"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/wireframes/README.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/wireframes/01-acesso.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/wireframes/02-painel-inicial.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/wireframes/03-dados-pessoais.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/wireframes/04-formacao.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/wireframes/05-experiencias.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/wireframes/06-informacoes-complementares.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/wireframes/07-revisao.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/wireframes/08-visualizacao-curriculo.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/wireframes/09-exportacao.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/testes/roteiro-teste-responsividade-f1-1.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/requisitos-seguranca.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/contrato-campos-obrigatorios-grupo2.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/Arquitetura/ADR-004-integracao-grupo2-busca-vagas.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções recuperadas por cat/rg: campos, ações, navegação, estados e limites"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "prompts/README.md"
      relationship: "context"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "docs/configuracao-ambiente.md"
      relationship: "context"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "prompts/frontend/20261026-080500-roteiro-teste-responsividade-f1-1-v001.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Cabeçalho, escopo, decisão, validação ou ocorrências dos termos de busca; não baseline atual"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "prompts/frontend/20261007-080500-teste-acessibilidade-formulario-curriculo-v001.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Cabeçalho, escopo, decisão, validação ou ocorrências dos termos de busca; não baseline atual"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "prompts/frontend/20261007-081300-cenario-e2e-preenchimento-curriculo-v001.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Cabeçalho, escopo, decisão, validação ou ocorrências dos termos de busca; não baseline atual"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "prompts/backend/20261025-193758-integracao-selecao-ordenacao-curriculo-v001.md"
      relationship: "supporting"
      representation: "prose"
      function: "documentation"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Cabeçalho, escopo, decisão, validação ou ocorrências dos termos de busca; não baseline atual"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/main.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "src/backend/api/factory.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/infrastructure/security/autenticador_sessao_indisponivel.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "src/backend/api/cadastro_acesso.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Assinaturas dos routers, métodos, caminhos e tratamento de executores ausentes"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/api/perfil_estudante.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Assinaturas dos routers, métodos, caminhos e tratamento de executores ausentes"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/api/formacao_academica.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Assinaturas dos routers, métodos, caminhos e tratamento de executores ausentes"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/api/experiencia_profissional.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Assinaturas dos routers, métodos, caminhos e tratamento de executores ausentes"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/api/exportacao_curriculo.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Assinaturas dos routers, métodos, caminhos e tratamento de executores ausentes"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/api/vagas.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Assinaturas dos routers, métodos, caminhos e tratamento de executores ausentes"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/api/documento.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Assinaturas dos routers, métodos, caminhos e tratamento de executores ausentes"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/api/versao_curriculo.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Assinaturas dos routers, métodos, caminhos e tratamento de executores ausentes"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/app/App.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "src/frontend/app/main.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "src/frontend/pages/acesso-estudante/ui/PaginaAcessoEstudante.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/pages/personal-data/ui/PaginaDadosPessoais.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/pages/formacao-academica/ui/PaginaFormacaoAcademica.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/pages/experiencias-profissionais/ui/PaginaExperienciasProfissionais.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/pages/cursos-idiomas/ui/PaginaCursosIdiomas.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/pages/competencias/ui/PaginaCompetencias.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/pages/projetos-academicos/ui/PaginaCadastroProjetosAcademicos.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/pages/selecionar-modelo-curriculo/ui/PaginaSelecaoModeloCurriculo.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/pages/validacao-curriculo/ui/PaginaValidacaoCurriculo.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Seções de objetivo, fluxo, critérios, fontes, limites e/ou composição recuperadas por cat/sed/rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/features/acesso-estudante/api/cliente-acesso-estudante.ts"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Clientes, callbacks onSalvar, transporte e navegação retornados por busca"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/features/edit-personal-data/ui/FormularioDadosPessoais.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Clientes, callbacks onSalvar, transporte e navegação retornados por busca"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/features/cadastrar-formacao-academica/ui/FormularioFormacaoAcademica.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Clientes, callbacks onSalvar, transporte e navegação retornados por busca"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/features/edit-professional-experience/ui/FormularioExperiencias.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Clientes, callbacks onSalvar, transporte e navegação retornados por busca"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/features/edit-courses/ui/FormularioCursos.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Clientes, callbacks onSalvar, transporte e navegação retornados por busca"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/features/edit-languages/ui/FormularioIdiomas.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Clientes, callbacks onSalvar, transporte e navegação retornados por busca"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/features/edit-skills/ui/FormularioCompetencias.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Clientes, callbacks onSalvar, transporte e navegação retornados por busca"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/features/cadastro-certificacoes/ui/FormularioCertificacao.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Clientes, callbacks onSalvar, transporte e navegação retornados por busca"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/app/jornada-curriculo.e2e.test.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Harnesses, doubles, render e cenários; não execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/app/jornada-selecao-previa-exportacao.e2e.test.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Harnesses, doubles, render e cenários; não execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/app/busca-vagas.integracao.test.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Harnesses, doubles, render e cenários; não execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/pages/cursos-idiomas/ui/PaginaCursosIdiomas.test.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Harnesses, doubles, render e cenários; não execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/pages/selecionar-modelo-curriculo/ui/PaginaSelecaoModeloCurriculo.test.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Harnesses, doubles, render e cenários; não execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/frontend/features/edit-personal-data/ui/FormularioDadosPessoais.a11y.test.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "TypeScript/TSX"
      analysis_scope: "selected-section"
      locator: "Harnesses, doubles, render e cenários; não execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/tests/test_integracao_ciclo_vida_perfil_autorizado.py"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Docstrings, imports, preparação, nomes de cenários e limites; sem execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/tests/test_integracao_crud_formacao_academica.py"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Docstrings, imports, preparação, nomes de cenários e limites; sem execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/tests/test_integracao_crud_informacoes_complementares.py"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Docstrings, imports, preparação, nomes de cenários e limites; sem execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/tests/test_integracao_selecao_ordenacao_curriculo.py"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Docstrings, imports, preparação, nomes de cenários e limites; sem execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/tests/test_integracao_associacao_candidatura_interesse.py"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Docstrings, imports, preparação, nomes de cenários e limites; sem execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/tests/test_integracao_exportacao_docx.py"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Docstrings, imports, preparação, nomes de cenários e limites; sem execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/tests/test_integracao_validacao_pdf_legibilidade.py"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Docstrings, imports, preparação, nomes de cenários e limites; sem execução"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/tests/fixtures/massa_teste_curriculos.py"
      relationship: "supporting"
      representation: "source-code"
      function: "data-fixture"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Conversão da massa e guardas de driver/grafo"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/tests/fixtures/selecao_ordenacao_curriculo.py"
      relationship: "supporting"
      representation: "source-code"
      function: "data-fixture"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Conversão da massa e guardas de driver/grafo"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/tests/fixtures/ciclo_vida_perfil_autorizado.py"
      relationship: "supporting"
      representation: "source-code"
      function: "data-fixture"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Conversão da massa e guardas de driver/grafo"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "docs/massa_teste_curriculos.json"
      relationship: "supporting"
      representation: "structured-data"
      function: "data-fixture"
      format: "JSON"
      analysis_scope: "selected-section"
      locator: "Perfis de Ana, Bruno e Carolina, conteúdo curricular"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".github/workflows/ci.yml"
      relationship: "context"
      representation: "structured-data"
      function: "configuration"
      format: "YAML/JSON"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "src/frontend/package.json"
      relationship: "context"
      representation: "structured-data"
      function: "configuration"
      format: "YAML/JSON"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "flake.nix"
      relationship: "context"
      representation: "source-code"
      function: "configuration"
      format: "Nix/TypeScript"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "nix/tests.nix"
      relationship: "context"
      representation: "source-code"
      function: "configuration"
      format: "Nix/TypeScript"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "nix/quality.nix"
      relationship: "context"
      representation: "source-code"
      function: "configuration"
      format: "Nix/TypeScript"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "src/frontend/vite.config.ts"
      relationship: "context"
      representation: "source-code"
      function: "configuration"
      format: "Nix/TypeScript"
      analysis_scope: "whole-file"
      locator: null
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "available"
    - path: "src/backend/infrastructure/persistence/alembic/versions/20261015_0011_criar_cursos.py"
      relationship: "supporting"
      representation: "source-code"
      function: "schema-contract"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Somente atribuições revision e down_revision"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/infrastructure/persistence/alembic/versions/20261015_0011_exclusao_logica_formacoes_academicas.py"
      relationship: "supporting"
      representation: "source-code"
      function: "schema-contract"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Somente atribuições revision e down_revision"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_links_profissionais.py"
      relationship: "supporting"
      representation: "source-code"
      function: "schema-contract"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Somente atribuições revision e down_revision"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/infrastructure/persistence/alembic/versions/20261015_0012_criar_projetos_academicos.py"
      relationship: "supporting"
      representation: "source-code"
      function: "schema-contract"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Somente atribuições revision e down_revision"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/backend-domain-orchestration-v2/SKILL.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/backend-domain-orchestration-v2/references/clean-boundary.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/backend-domain-orchestration-v2/references/backend-fit-check.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/backend-adapters-drivers-v2/SKILL.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/backend-adapters-drivers-v2/references/outer-boundary.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/backend-adapters-drivers-v2/references/backend-fit-check.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/frontend-implementation-v3/SKILL.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/frontend-implementation-v3/references/scope-boundary.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/frontend-implementation-v3/references/frontend-fit-check.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/cross-cutting-implementation-v1/SKILL.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/cross-cutting-implementation-v1/references/scope-boundary.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/cross-cutting-implementation-v1/references/cross-cutting-fit-check.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/integration-system-testing-v1/SKILL.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/integration-system-testing-v1/references/test-scope-boundary.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/integration-system-testing-v1/references/test-fit-check.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/nix-environment-implementation-v1/SKILL.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/nix-environment-implementation-v1/references/nix-scope-boundary.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: ".agents/skills/nix-environment-implementation-v1/references/nix-fit-check.md"
      relationship: "context"
      representation: "prose"
      function: "prompt-instruction"
      format: "Markdown"
      analysis_scope: "selected-section"
      locator: "Contrato, escopo, fronteiras e teste de adequação ou esquema/roteamento"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc (base; árvore inicialmente limpa)"
      availability: "partial"
    - path: "src/backend/application/exportacao_curriculo.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Docstrings e fluxo do caso de uso no início do arquivo"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: "partial"
    - path: "src/backend/application/versao_curriculo.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Docstrings e fluxo do caso de uso no início do arquivo"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: "partial"
    - path: "src/backend/application/revisao_versao_curriculo.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Docstrings e fluxo do caso de uso no início do arquivo"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: "partial"
    - path: "src/backend/application/perfil_completo.py"
      relationship: "supporting"
      representation: "source-code"
      function: "production"
      format: "Python"
      analysis_scope: "selected-section"
      locator: "Docstrings e fluxo do caso de uso no início do arquivo"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: "partial"
    - path: "src/frontend/features/edit-professional-experience/ui/FormularioExperiencias.test.tsx"
      relationship: "supporting"
      representation: "source-code"
      function: "test"
      format: "TSX"
      analysis_scope: "selected-section"
      locator: "Ocorrências de onSalvar/assertions retornadas por rg"
      content_state: "working-tree"
      revision: "d45115dc5d9fd75f336cc86281b687f49e3e0ffc"
      availability: "partial"
routing:
  root: prompts
  selected_directory: prompts/requisitos
  considered_directories:
    [prompts/requisitos, prompts/frontend, prompts/revisao, prompts/backend]
  confidence: high
  rationale: "Refinamento do contrato de aceitação do processo completo; propósito sistêmico, sem implementação ou linhagem anterior."
classification:
  sphere: product
  concerns: [user-experience, delivery, privacy]
  decision_kind: clarification
  scope: system
  lifecycle: delivery
  urgency: normal
  uncertainty: high
  reversibility: easy
  risk: medium
---

# Análise de decisão — roteiro de aceitação com estudante representativo

## Solicitação original

Título literal: "Criar roteiro de aceitação com estudante representativo para a jornada completa."

O usuário esclareceu que "jornada completa" significa o processo completo do sistema, de ponta a ponta, e não sabe se o entregável é teste ou documento. Não forneceu descrição, número do card ou critérios oficiais. Esta análise começa do zero; a única escrita autorizada é um novo artefato de análise. A solicitação detalhada encontra-se preservada no apêndice de insumos.

## Informações complementares

Skill explicitamente invocada: decision-analysis-v4. Inspeção local, sem GitHub CLI/rede, execução de aplicação, testes, migrations, instalação ou mudança de ambiente. Precedentes encontrados são contexto, não linhagem desta análise.

## Mudanças desde a versão anterior

Nenhum identificado — initial/v001; não substitui análises anteriores.

## Artefatos analisados

O inventário individual em subjects.files registra caminho, relação, representação, função, formato, recorte, disponibilidade, estado e revisão. As citações abaixo registram trechos decisivos. Não confundir arquivo descoberto com arquivo de conteúdo examinado.

| Conjunto                                               | Relação/função                     | Representação/formato | Recorte                                                         |
| ------------------------------------------------------ | ---------------------------------- | --------------------- | --------------------------------------------------------------- |
| Requisitos, jornadas, casos de uso, matrizes e manuais | Principal: necessidades e processo | Prosa/Markdown        | Conteúdo ou seções declarados no inventário                     |
| Composição, páginas e routers                          | Apoio: estado atual                | Código Python/TSX     | Composição, defaults, callbacks, guardas de dependências        |
| Testes e fixtures                                      | Apoio: cobertura e limites         | Código/JSON           | Docstrings, harnesses, imports, cenários, guardas; sem executar |
| AGENTS, skills e referências                           | Contexto: restrições/elegibilidade | Prosa/Markdown        | Contratos e testes de adequação                                 |
| CI, manifestos e Nix                                   | Contexto: gates/ambientes          | YAML/JSON/Nix         | Comandos e composição declarados                                |
| Histórico local                                        | Apoio: evolução                    | Metadados Git         | log, show --stat, branch, HEAD, merge-base e status             |

### Limites da evidência dos artefatos

Nenhuma evidência empírica nova de funcionamento, navegador, desempenho ou aceite humano. Existência de teste não prova aprovação. Resultados históricos não são baseline desta branch. Ausências significam não localizado nas buscas/recortes declarados.

Saídas extensas sofreram truncamento; não se reivindica auditoria integral de todos os arquivos retornados. Recortes decisivos foram recuperados com consultas menores. O inventário usa selected-section de forma conservadora para leituras extensas. Artefatos apenas listados têm conteúdo não avaliado.

## Problema enriquecido

### Resultado desejado

Especificar um roteiro humano completo e rastreável, com formulário vazio e limites reais de execução, para que outro executor possa escrevê-lo sem inventar critérios oficiais ou resultados.

### Atores e interesses

Estudante é ator definido em requisitos/casos de uso. Autor técnico/QA, facilitador/observador e responsável de produto são papéis recomendados, ainda não atribuídos. A equipe decide aceite conforme docs/registro-aceite-licoes.md; nenhum signatário individual foi definido.

### (a) Fatos encontrados, caminhos e trechos

#### F01 — Base local e histórico Git

git branch --show-current retornou test-roteiro-jornada-completa. HEAD = d45115dc5d9fd75f336cc86281b687f49e3e0ffc. A referência local dev e git merge-base HEAD dev apontam ao mesmo commit. git status --short inicial vazio. Confirma igualdade com dev local, não atualização remota.

| Trabalho                             | Evidência local                                                                                                                                                | Identificação e limite                                                      |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Mapeamento                           | 4247f61 “adiciona mapeamento de jornadas”; 9cef180 “redefine guided curriculum journey”; histórico por docs/mapeamento_jornadas.md                             | Ligação por caminho/mensagem                                                |
| Manual, checklist, dossiê e registro | 7576bd0 “document remaining student and API workflows”; histórico de docs/dossie-aceite.md                                                                     | Histórico do artefato, não aceite de entrega                                |
| Jornada simulada                     | 5907ade adiciona src/frontend/app/jornada-selecao-previa-exportacao.e2e.test.tsx, mensagem #373; merge 24fde90 PR #441 de feat/issue-373-cenario-e2e-curriculo | Caminho, mensagem e branch ligam card #373 a PR #441; números distintos     |
| Roteiro manual                       | 0d49541 adiciona docs/testes/roteiro-teste-responsividade-f1-1.md e análise; a9f60a8 merge PR #598 de docs/issue-375-roteiro-teste-responsividade-f1-1         | Card #375 e PR #598 ligados por branch/conteúdo, não coincidência           |
| Renderizadores                       | Histórico de infrastructure/exportacao: 84e3a5b PDF (#230), 4ad3416 DOCX (#231); merges 9c45efd PR #576/task230 e d60da82 PR #574/task231                      | Arquivos e mensagens                                                        |
| Rota PDF                             | 05d992f “expor download da exportação de currículo em PDF”                                                                                                     | Sem atribuir card não fornecido                                             |
| Perfil/associação                    | 4bf0484 ciclo de vida perfil / merge 991ef98 PR #582; 2e145d2 candidatura/interesse / merge 4ddf89c PR #595                                                    | Semântica corroborada pelos módulos atuais                                  |
| Redesign atual                       | 3fffddb telas; ec1284f acesso; e5dda2a callback em App; merges PR #612/#610                                                                                    | Histórico de App.tsx e código atual divergem da fotografia antiga do manual |

Busca git log --all --oneline -i --grep='roteiro de aceitação\|estudante representativo' não retornou commits. Não foi identificado vínculo inequívoco deste título a card/PR. Não houve dependência de GitHub ou rede.

#### F02 — Inventário e buscas

find localizou somente AGENTS.md, src/backend/AGENTS.md e src/frontend/AGENTS.md; os três foram lidos antes da avaliação dessas áreas. Nenhum AGENTS adicional localizado em docs/prompts/skills.

Busca: rg -l -i "$termo" docs prompts, antes desta escrita. Contagens são de arquivos com ocorrência, não de artefatos pertinentes ou aprovados.

| Termo literal      | Arquivos | Retornos pertinentes/limites                                                                   |
| ------------------ | -------: | ---------------------------------------------------------------------------------------------- |
| jornada            |       41 | mapeamento, manual, wireframes, dossiê, análises E2E                                           |
| fluxo              |       76 | RF/RNF, matrizes, acessibilidade, compatibilidade                                              |
| persona            |       12 | Ocorrências em personalização e caminhos personal-data; nenhuma persona de pesquisa localizada |
| estudante          |      127 | requisitos, massa, contratos, manuais e análises                                               |
| perfil de usuário  |        0 | Vazio                                                                                          |
| público-alvo       |        1 | docs/contrato-campos-obrigatorios-grupo2.md:45, “público-alvo: FATEC-SP”                       |
| representativo     |        4 | RNF01, roteiro F1.1 e duas análises; massa não é participante                                  |
| aceitação          |       20 | matriz, RNF01, guia de skills, roteiro                                                         |
| aceite             |       67 | dossiê/registro/checklist, wireframes e precedentes                                            |
| homologação        |        2 | roteiro F1.1 e sua análise                                                                     |
| usabilidade        |        8 | RNF01 e análises/evidências específicas                                                        |
| roteiro            |       13 | checklist, roteiro F1.1 e análises de teclado/responsividade                                   |
| teste com usuários |        0 | Vazio                                                                                          |
| evidência          |      115 | matrizes, dossiê, docs/testes e análises                                                       |

Buscas adicionais: “plano de aceitação”, “caso de aceitação” e “estudante representativo” = vazias; “jornada completa” = duas análises frontend de 07/10; “consentimento” retornou docs/requisitos-seguranca.md, docs/adequacao_semantica_ia.md e três análises backend de associações. Não se localizou protocolo de consentimento de pesquisa humana. Consentimento de outra funcionalidade não é consentimento para sessão.

Inventário descobriu docs de requisitos, matrizes, jornadas, casos de uso, manuais, contratos, arquitetura/ADRs, nove wireframes Markdown e evidências. Nem todo contrato descoberto foi auditado. Buscas iniciais por nomes hipotéticos de testes e alembic/versions na raiz falharam; os caminhos reais foram localizados por rg --files. Aqueles nomes não são evidência.

#### F03 — Natureza e precedentes de aceitação

- docs/requisitos_nao_funcionais.md, RNF01: “simples e compreensível para estudantes sem experiência na elaboração de currículos”; situação: “critério de aceitação a validar”.
- Mesmo arquivo, verificação proposta: “Observar estudantes representativos realizando cadastro de informações e exportação de um currículo sem auxílio externo; taxa de sucesso e tempo esperado a definir.” Método proposto não é meta aprovada.
- docs/checklist-demonstracao.md: “A lista é um roteiro, não um registro de execução ou aceite”; pede commit, ambiente, dados sintéticos e não apresentar mock como integração.
- docs/dossie-aceite.md: “Não é uma decisão de entrega; faltam execução demonstrável e aprovação da equipe.”
- docs/registro-aceite-licoes.md: “Não registra aceite, não aceite nem lições como fatos”; campos pendentes.
- docs/testes/roteiro-teste-responsividade-f1-1.md, §§1,7,8: procedimento humano para desenvolvedores/homologadores/revisores, com laudo em docs/testes/evidencias. Precedente limitado à responsividade. Seu template contém “Aprovado”: não copiar preenchimento para novo modelo.
- docs/matriz_testes.md especifica pré-condições, ação e esperado. docs/matriz_rastreabilidade.md: cenário “não significa ... que o teste já foi executado com sucesso”.
- .agents/skills/integration-system-testing-v1/references/test-scope-boundary.md define system-acceptance-e2e por exercício das camadas relevantes; relatórios/screenshots são outputs. A skill implementa testes, não presume que todo documento com “aceitação” seja teste.

#### F04 — Processo e público

docs/requisitos_funcionais.md, objetivo: estudantes FATEC-SP e outros cursos da instituição, buscando estágio e próximos à conclusão. RF01–15 incluem dados, projetos/orientação, seções/modelos, prévia/revisão, PDF/DOCX, vagas/associações, autenticação, versões e escolha do currículo.

docs/casos-de-uso-v2.md: “Aluno (FATEC-SP / em busca de estágio)”; recuperar acesso por e-mail, documentos complementares e versões para objetivos distintos; recrutador opcional. Não define participante, quantidade ou amostragem.

docs/mapeamento_jornadas.md, §§2,5–7: “único fluxo progressivo”; acesso → painel → dados → formação → experiências → complementares → revisão → prévia → geração PDF/DOCX → download. Versões/documentos/Grupo 2 ficam fora do recorte dos wireframes, não do sistema.

docs/wireframes/README.md: nove arquivos representam essa trilha, excluindo integração Grupo 2 do pacote. docs/wireframes/09-exportacao.md: tentar novamente mantém dados/prévia; sucesso permite baixar novamente/voltar ao painel.

#### F05 — Composição atual e integração

- docs/configuracao-ambiente.md inicia uvicorn backend.main:app.
- src/backend/main.py chama create_app somente com AutenticadorSessaoIndisponivel, verificador de persistência e lifespan; não injeta executores de negócio.
- src/backend/infrastructure/security/autenticador_sessao_indisponivel.py: “sempre considera o token inválido”; retorna None. DATABASE_URL pode viabilizar readiness, não compõe o negócio.
- src/backend/api/factory.py recebe executores None e registra routers; ausências viram indisponibilidade. Assistente determinístico é exceção explícita. Não registra router de associação.
- Routers cadastro/perfil/formação/experiência/documento/versão/vagas/exportação têm guardas None→503; rotas privadas também dependem de sessão. Não afirmar 503 universal antes da autenticação.
- src/frontend/app/main.tsx monta App. App.tsx monta landing pública, acesso e oito etapas por estado/parâmetro etapa; CTA criar abre dados diretamente. Não monta painel autenticado, recuperação, vagas ou prévia/download integrado.
- pages/acesso-estudante/ui/PaginaAcessoEstudante.tsx usa cliente HTTP e alterna login/cadastro, “sem criar navegação autenticada”. Cliente em features/acesso-estudante/api/cliente-acesso-estudante.ts chama POST /estudantes e /acessos; fetch não declara credentials: include. Cookie/CORS entre origens requer ensaio, não comprovado.
- Páginas de dados/formação/projetos usam clientes Indisponivel sem injeção em App. Experiências/cursos/idiomas/competências/certificações têm onSalvar opcional, não conectado a backend nessa composição.
- pages/selecionar-modelo-curriculo/ui/PaginaSelecaoModeloCurriculo.tsx: “Mantém somente a seleção visual local”. App apenas muda etapa e não persiste modelo.
- pages/validacao-curriculo/ui/PaginaValidacaoCurriculo.tsx recebe DADOS_VALIDACAO_PADRAO; App não fornece dados das etapas nem callbacks de prévia/PDF/confirmação. Esses defaults não provam dados salvos pelo estudante. Sua procedência sintética não foi comprovada: não copiar para evidência.
- src/frontend/vite.config.ts define jsdom; nome e2e não equivale a navegador real.

#### F06 — Privacidade e massa

docs/requisitos-seguranca.md, §§4.6–4.8/4.12–4.16: propriedade, currículo privado, minimização, não registrar credenciais, evitar dados pessoais desnecessários. Prazo de logs operacionais/segurança = 30 dias no coletor; não é prazo de evidência de pesquisa. Consentimentos avançados/retenção detalhada seguem em análise.

docs/manual-estudante.md: “Use somente dados fictícios da massa de teste”; não copiar nomes/documentos/tokens/currículos reais para screenshots/logs/issues.

docs/massa_teste_curriculos.json contém Ana (estágio web, graduação em andamento, experiência/projeto), Bruno (financeiro/pós-graduação) e Carolina (design/freelance). Não define facilidade de uso, dispositivo ou necessidade assistiva. Ana é da Unicamp na massa, não FATEC: representatividade parcial. Telefones/LinkedIn plausíveis não devem ser contatados/abertos.

src/backend/tests/fixtures/massa_teste_curriculos.py converte JSON em entidades/prévia; hash de fixture não é senha operacional. Massa não provisiona conta na composição atual. docs/contrato-campos-obrigatorios-grupo2.md §2 proíbe transmitir identificadores diretos ao Grupo 2.

#### F07 — Casos de uso e níveis de teste

src/backend/application/exportacao_curriculo.py: “encadeia a prévia ... montagem do documento renderizado e ... gerador”; ExportarCurriculo devolve bytes/nome/MIME e converte falha ou conteúdo vazio em FalhaGeracaoArquivoCurriculo. É capacidade implementada sem ligação em main.

src/backend/application/versao_curriculo.py: criação/edição usam agregado/porta e verificação de propriedade. src/backend/application/revisao_versao_curriculo.py: obtém prévia e relógio e aplica regra do domínio sem alterar estado. src/backend/application/perfil_completo.py: valida propriedade/unicidade/estado e solicita única persistência. Esses mecanismos não demonstram, sem composição, conclusão por navegador.

Taxonomia lida nas referências de fronteira das skills:

- Unitário: unidade isolada, portas/dependências substituídas; domínio sem banco/rede/framework, componente isolado pode usar DOM simulado.
- Integração: colaboração real entre unidades/fronteiras; inclui ASGI, caso real e SQLite mesmo com dependência externa substituída.
- Contrato: compatibilidade de consumidor/provedor/schema/protocolo entre partes independentes.
- Sistema/aceitação/E2E: componente implantável ou jornada através das camadas relevantes. Nome e2e em teste com harness/jsdom não prova implantação ou browser real.
- Não funcional: atributo do sistema integrado, com método/oráculo; inspeção humana específica complementa automação sem certificar tudo.

Nomes test_*.py sem prefixo na tabela abaixo referem-se a src/backend/tests/. Nomes *.test.tsx de jornada/busca referem-se a src/frontend/app/. Teste de componente citado pelo nome refere-se ao slice e caminho identificados no inventário. Resultados esperados documentais da tabela são **definidos nos artefatos citados**; associação J→RF/CT, ordem de ramos, protocolo e políticas da sessão são **inferidos nesta análise**. Um cenário de matriz definido não é critério oficial fornecido para este card.

### Jornada completa e cobertura existente

Recomendação inferida, a confirmar: trilha guiada mais ramos RF01–15/casos de uso; não inventar sequência única para módulos desconectados. A ordem obrigatória entre exportação, vagas e gestão de versões não é definida. Não exigir candidatura para simplesmente gerar PDF.

Legenda: E = executável na aplicação que sobe na extensão declarada; T = cenário parcial apenas na composição de teste; B = finalidade funcional bloqueada na aplicação atual. T não é ambiente humano de homologação. Cobertura é código/contrato encontrado, não resultado de execução.

| Etapa/fontes                                                               | Pré-condição e resultado definido                                                 | Tela/composição frontend                                                    | Backend/integração                                                                     | Classe e limite atual                                                    | Requisitos/CT e testes                                                                                                                                                                       |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| J00 Primeiro acesso; wireframes/README/01                                  | App disponível; entrada para conta/criação                                        | Landing e ações locais em App                                               | Independente de executor para apresentação                                             | E só apresentação; usabilidade/renderização não ensaiadas                | UC01/02; sem CT específico de landing; testes App só inventariados                                                                                                                           |
| J01 Cadastro/login; UC01/02, mapeamento 6.1                                | Dados válidos/conta; autenticar e chegar ao painel                                | Página/cliente HTTP, sem transição autenticada                              | Routers existem; main sem executores/sessão operacional                                | B/T: não verifica persistência, cookie/browser ou continuidade           | RF13; CT-RF13-01–03; test_integracao_ciclo_vida_perfil_autorizado.py: ASGI/SQLite, não main/browser                                                                                          |
| J02 Recuperar senha; UC02, wireframe 01                                    | Conta/e-mail; enviar link e voltar ao login                                       | pages/recuperar-senha descoberto, conteúdo não auditado, não montado em App | Sem recuperação composta na factory                                                    | B: não verifica envio, recebimento, troca/acesso                         | UC02; matriz RF13 sem CT dedicado                                                                                                                                                            |
| J03 Painel/iniciar/retomar; mapeamento 6.2/7, wireframe 02                 | Conta; vazio/rascunho/concluído define próxima ação                               | Landing não equivale a painel por estado do currículo                       | Sem composição de rascunho/retomada localizada                                         | B: sem retomada persistida ou continuidade após interromper              | RF03/14 relacionados; CT-RF03-01/02 e RF14 não especificam retomada                                                                                                                          |
| J04 Dados pessoais; mapeamento 6.3, wireframe 03                           | Conta; nome/e-mail/telefone/cidade obrigatórios no wireframe; salvar/corrigir     | Página montada com cliente indisponível                                     | Perfil/contato previstos, não ligados em main                                          | B/T: validação local não prova salvamento/releitura                      | RF01/02/13; CT-RF01-01/05, RF02-01/05/06; ciclo perfil; jornada-curriculo.e2e.test.tsx com double; a11y local                                                                                |
| J05 Formação; mapeamento 6.4/wireframe 04                                  | Conta; curso/instituição/período/situação; adicionar/editar/remover               | Montada com cliente indisponível                                            | POST/PUT/DELETE previstos; main sem executores; teste declara ausência de GET/listagem | B/T: sem CRUD humano completo                                            | RF01/02; CT-RF01-02/05, RF02-01; test_integracao_crud_formacao_academica.py: ASGI/SQLite, leitura por porta interna                                                                          |
| J06 Experiência; mapeamento 6.5/wireframe 05                               | Conta; organização/cargo/período/descrição, editar/remover/ordenar                | Estado/callback opcional, sem persistência em App                           | Casos/routers de cadastro/edição/exclusão previstos, não compostos                     | B: estado local não prova persistência/ordenação final                   | RF01/02; CT-RF01-03, RF02-02/04; FormularioExperiencias.test.tsx localizado, não execução                                                                                                    |
| J07 Complementares/projetos/orientação; mapeamento 6.6, RF04               | Conta; habilidades/idiomas/cursos/projetos/links; orientar sem IA                 | Páginas montadas parcialmente; callbacks locais/clientes ausentes           | Cadastros previstos, não compostos; assistente determinístico tem default              | B/T para salvar; assistente isolado não prova etapa integrada            | RF01/02/04; CT-RF01-04/05 e RF04-01–03; test_integracao_crud_informacoes_complementares.py cobre só curso/documentos com memória                                                             |
| J08 Documentos; casos de uso                                               | Conta; guardar certificados/portfólio protegido                                   | Não conectado em App                                                        | Router armazenar/baixar/excluir previsto, não composto                                 | B/T: não verifica armazenamento/download por pessoa                      | Capacidade UC sem CT específico próprio; teste complementar cobre armazenamento/exclusão, não todo ciclo                                                                                     |
| J09 Versões; RF03/14 e UC                                                  | Conta/dados; versões por objetivos, consultar/editar/excluir isoladamente         | Sem lista/painel composto                                                   | Routers criar/editar/listar/excluir na factory, não main                               | B/T: não prova segunda versão ou navegação real                          | CT-RF03-01–03 e RF14-01–05; testes de seleção usam versões prontas, não CRUD humano                                                                                                          |
| J10 Itens/seções/modelo; RF03/05/06/15                                     | Versão própria/itens; reaproveitar e organizar, associar modelo                   | Modelo local; App só avança; itens não integrados                           | Seleção/desseleção/ordem/edição previstos, não main                                    | B/T; E só escolha visual; sem persistência/ordem final                   | CT-RF03-01–03, RF05-01/02, RF06-01–03, RF15-01/03/04; test_integracao_selecao_ordenacao_curriculo.py usa consultas de itens doubles e limites de ordem explícitos                            |
| J11 Revisar/editar; mapeamento 6.7/RF08                                    | Conteúdo; resumo, pendências, editar e voltar                                     | Validação com defaults, sem dados/callbacks reais                           | Revisão/decisões na factory, sem executor em main                                      | B/T: não revisa o que o estudante cadastrou                              | RF02/08; CT-RF07-03, RF08-01–03; jornada-curriculo.e2e.test.tsx fornece seções/doubles                                                                                                       |
| J12 Prévia/troca de modelo; mapeamento 6.8/RF07                            | Conteúdo confirmado/modelo; refletir dados e mudanças                             | Componentes/harness existem, sem prévia integrada no App                    | Router previsto, executor ausente em main                                              | B/T: sem fidelidade cadastro→prévia real                                 | CT-RF06-03, RF07-01–03; jornada-selecao-previa-exportacao.e2e.test.tsx simula seleção/prévia                                                                                                 |
| J13 PDF/DOCX/download; mapeamento 6.9/wireframe 09                         | Currículo próprio escolhido; gerar, baixar, tentar sem perder dados               | Callbacks ausentes, sem caminho integrado                                   | Router e renderizadores reais, exportadores não injetados em main                      | B/T: sem download browser, fidelidade ao digitado ou abertura por pessoa | RF09/15; CT-RF09-01–05, RF15-01/03/04; test_integracao_exportacao_docx.py e test_integracao_validacao_pdf_legibilidade.py usam exportador real, prévia/autenticador stubs; frontend usa Blob |
| J14 Vagas; RF10/11                                                         | Conta, serviço disponível ou falha controlada; resultados/vazio/erro              | PaginaVagasGrupo2 existe, não montada em App                                | GET /vagas na factory; consultar_vagas ausente em main                                 | B/T: não prova Grupo 2 ativo/front↔back                                  | CT-RF10-01–04 e RF11-01/03/04; busca-vagas.integracao.test.tsx cruza página/cliente com remoto simulado                                                                                      |
| J15 Selecionar currículo/associar/classificar/consultar; RF12/15 e RN01–07 | Conta, versão e vaga; associação manual/persistida; candidatura implica interesse | Sem fluxo em App                                                            | Casos/repos importados nos testes; sem router/DTO/handler de associação                | B/T: não prova ação humana, HTTP ou existência de vaga                   | CT-RF11-02, RF12-01–15/C01–C07, RF15-02–04; test_integracao_associacao_candidatura_interesse.py é componentes/SQLite, não HTTP/E2E                                                           |

O processo possui resultados definidos diferentes: arquivo gerado/baixado e associação manual persistida. Não há ordem total obrigatória entre ramos. RF12 explicita: classificação candidatura não implica envio externo. Recrutador é opcional; JSON aparece como exemplo em UC, mas RF09 confirma PDF/DOCX; IA e importação não são etapas obrigatórias.

#### Alternativos e falhas sustentados

| Fonte                          | Comportamento esperado                                                      | Limite atual                                                   |
| ------------------------------ | --------------------------------------------------------------------------- | -------------------------------------------------------------- |
| mapeamento §7/wireframes 03/07 | Campo inválido: erro contextual, preservar valores, corrigir                | Validação local não prova persistência                         |
| mapeamento §7/wireframe 02     | Salvar rascunho e continuar                                                 | Composição não localizada                                      |
| mapeamento §7                  | Voltar da revisão/prévia à seção e conferir edição                          | App desconectado; harness não substitui                        |
| mapeamento §7                  | Sem formação/experiência: avançar quando produto permitir                   | Regra condicional, não tornar obrigatório por causa de harness |
| CT-RF01-05/RF02-04             | Falha de gravação sem parcial; item removido informa ausência/atualiza      | Requer cenário técnico controlado                              |
| CT-RF09-04/05/wireframe 09     | Negar sem sessão; falha sem arquivo inválido, nova tentativa preserva dados | Callback/Blob não provam exportação                            |
| CT-RF10-02–04/RF11-03/04       | Vazio, JSON inválido, indisponibilidade/demora controlados                  | Preparação técnica; não provocar falha externa com estudante   |
| CT-RF12/RF15                   | Escolha manual e recusas inválidas/alheias/sem seleção                      | Integração de componentes não é sessão humana                  |

#### Divergências: não decidir silenciosamente

| Divergência                                       | Fontes                                                                                                                           | Fonte mais confiável para a pergunta/tratamento                                                                                                 |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Jornada guiada versus sistema inteiro             | mapeamento §2 exclui versões/Grupo 2 do recorte; RF10–15 e UC os incluem                                                         | RF + esclarecimento do usuário para escopo sistêmico; mapeamento/wireframes para trilha. Produto confirma ramos                                 |
| Revisão sem análise automática versus orientações | mapeamento §§2/6.7; RF08; factory                                                                                                | Distinguir conferência/regras determinísticas de IA; produto/design confirmam linguagem. Sem scoring inventado                                  |
| Manual antigo versus código                       | manual/checklist/dossiê declaram fotografia ab2b8bc de 19/10; App/renderizadores mudaram                                         | Composição atual governa executabilidade; textos antigos são precedentes. “Não há gerador” amplo demais; “não integrado em main/App” sustentado |
| Integração antiga versus atual                    | UC/contrato-campos descrevem sincronização/matching POST /api/v1/vagas/match; ADR-004 aceito 25/10 descreve GET /vagas→adapter   | ADR atual/factory para implementado; não incluir submissão ao matcher como capacidade comprovada                                                |
| Experiência obrigatória no harness                | harness bloqueia sem experiência; mapeamento admite ausência condicional                                                         | Harness prova cenário local, não regra global; produto deve definir, sem experiência fictícia                                                   |
| Resumos de matriz                                 | RF02 detalha 05/06 mas resumo para em 04; rastreabilidade RF12 para em 09, matriz de testes vai a 15                             | Cenários detalhados para planejar, sem presumir execução; não corrigir matrizes neste escopo                                                    |
| Suporte visual/navegadores                        | compatibilidade define Edge/Firefox desktop; roteiro F1.1 amplia plataformas e acrescenta DPR/14px/44px                          | RNF03/compatibilidade governam suporte; regras específicas de outro roteiro não viram aceite geral                                              |
| Laudo PDF “APROVADO” e alcance                    | docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md declara atendimento integral; teste usa stubs e leitura automatizada | Código delimita ensaio; laudo histórico não aprova esta sessão/todos os modelos/abertura visual                                                 |

#### Achados próprios, sem correção

Frontend: clientes indisponíveis/callbacks locais; modelo não persistido; validação com defaults; ausência de prévia/download/vagas/associação conectados. Aparência pessoal dos defaults é risco, não comprovação de dados reais.

Backend: main sem negócios compostos; autenticação rejeita tokens; associação sem HTTP; formação sem consulta GET/listagem, conforme docstring de test_integracao_crud_formacao_academica.py. Readiness não garante jornada.

Persistência: src/backend/infrastructure/persistence/alembic/versions/20261015_0011_criar_cursos.py e 20261015_0011_exclusao_logica_formacoes_academicas.py repetem revision "20261015_0011"; 20261015_0012_criar_links_profissionais.py e 20261015_0012_criar_projetos_academicos.py repetem "20261015_0012". Duplicidade observada por leitura é bloqueio preexistente à preparação confiável do banco. Alembic não foi executado; não afirmar heads atuais pela lista histórica da fixture.

Ambiente/testes: fixtures de seleção/perfil possuem guardas de driver/grafo com skips. nix/tests.nix inclui Python backend e aiosqlite, não Node explícito; ensaio frontend no ambiente tests não foi demonstrado. Não mudar ambiente por esta entrega.

Documentação: fotografias antigas; RF02/RF12 inconsistentes; sem CT dedicado de recuperação/rascunho/documentos equivalente ao processo completo; sem metas humanas RNF01. Privacidade: sem protocolo/retentor de evidência de pesquisa e sem responsável por consentimento.

### (b) Lacunas, opções e decisões condicionais

“Nenhum artefato define” refere-se ao corpus examinado, não a fonte externa desconhecida.

| ID/lacuna                    | Opções viáveis                                               | Recomendação justificada                                                                                        | Tipo e exatamente o que fornecer                                                                                  |
| ---------------------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| L01 Natureza/aceite oficial  | Roteiro; automação; híbrido                                  | Documento humano, padrão recomendado, a confirmar: título e RNF01 sustentam observação                          | Produto: confirmar finalidade e se card exige só criação ou também execução; fornecer descrição/aceite se existir |
| L02 Processo/ordem           | Só trilha; trilha+ramos; sequência única                     | Trilha+ramos, padrão recomendado, a confirmar: RF10–15 e esclarecimento sem inventar ordem                      | Produto/design: confirmar ramos opcionais/obrigatórios e entradas/retornos                                        |
| L03 Participante/número      | Persona; pessoa real; grupos segmentados                     | Uma pessoa real elegível + dados sintéticos, padrão recomendado, a confirmar; ensaio qualitativo inicial        | Produto: critérios/quantidade/responsável pelo recrutamento; design: inclusão e necessidades                      |
| L04 Experiência/dispositivo  | Iniciante; experiente; perfis contrastantes                  | Pouca experiência em fazer currículo, buscando estágio, pelo RNF01; registrar dispositivo habitual              | Produto/design: perfil, experiência, necessidade assistiva e configurações da amostra                             |
| L05 Seções/rascunho          | Admitir ausência de experiência; exigir; variar por objetivo | Não exigir item fictício; ramo sem experiência condicional                                                      | Produto: política de obrigatoriedade/quantidades/avanço/retomada; design: mensagens                               |
| L06 Usabilidade/encerramento | Qualitativo; metas quantitativas; comparar grupos            | Observação qualitativa sem corte de tempo/taxa inventado, padrão recomendado, a confirmar                       | Produto/design: tarefas obrigatórias, ajuda, tentativas, metas e regra de encerramento                            |
| L07 Estados/gravidade        | Política local; importar responsividade; política geral      | Política local inferida abaixo; não importar outra funcionalidade                                               | Produto/QA: confirmar estados/severidade/tolerância a defeitos/risco                                              |
| L08 Consentimento/evidência  | Notas mínimas; capturas; gravação                            | Sem gravação por padrão; pseudônimo/dados sintéticos, a confirmar antes de sessão                               | Produto/governança: finalidade, informação/consentimento, acesso, retenção/descarte, retirada e responsável       |
| L09 Massa operacional        | Ana; adaptação FATEC; nova massa                             | Reusar conteúdo sintético de Ana com limitação explícita; variante sem experiência condicional, sem editar JSON | Produto aprova adequação; engenharia fornece conta/reset e credenciais fora do Git                                |
| L10 Instância integrada      | dev bloqueado; homologação; harness declarado                | Escrever agora com bloqueios; sessão só após preflight real; harness é apoio técnico                            | Engenharia: URL/commit/entrypoint, dependências, estado inicial, exportação/vagas/associação e reset              |
| L11 Cobertura faltante       | Referenciar CT; ampliar CT; mapa local                       | Mapa local J→RF/CT/RNF e limites sem editar matriz oficial                                                      | Engenharia/QA: casos ausentes, nível por fronteira e evidência por identidade futura                              |
| L12 Autoria documental       | Skill de testes; autor QA; criar skill                       | Autor técnico/QA fora de skill implementadora; resultado não é teste                                            | Organização/engenharia: autorizar criação dos dois Markdown desta análise; skill documental é outra demanda       |
| L13 Assinatura/aceite        | Facilitador; produto; colegiado                              | Equipe/produto decide, facilitador registra; papéis sem nomes                                                   | Produto: signatários/autoridade sobre risco e distinção aprovação documental versus aceite                        |
| L14 Contratos divergentes    | Texto antigo; código; reconciliar                            | Requisitos para necessidades e composição atual para executabilidade; conflitos explícitos                      | Produto/design/engenharia: decisão por domínio sobre revisão, integração e suporte                                |
| L15 RNF e aplicativos reais  | Um aplicativo; matriz inteira; automático                    | Registrar configuração real sem generalizar; sem metas quantitativas inventadas                                 | Produto/design/QA: leitores DOCX/PDF, dispositivos/navegadores e limiares se necessários                          |

Nenhuma lacuna impede escrever o documento com condicionais. L03/L08/L10/L13 impedem selecionar/convocar/executar ou conceder aceite sem contexto, não a autoria. Status proposed, sujeito a revisão humana.

### Hipóteses

H1: roteiro humano atende melhor ao título que automação sem participante. H2: equipe aceita preparar roteiro antes da integração. H3: uma sessão inicial produz observação qualitativa útil sem representatividade estatística. São inferências, não fatos.

### Perguntas em aberto

L01–L15. Confirmação mínima de produto: natureza e recorte (L01/L02). Demais podem permanecer condicionais no documento.

### Escopo

Natureza, estrutura, caminhos, rastreabilidade, critérios definidos/inferidos, protocolo, registro vazio, gates, limites e handoffs.

### Fora do escopo

Executar aceitação, recrutar/escolher pessoa, preencher resultados, corrigir código/testes/docs/migrations, integrar sistema, alterar Nix/CI, criar skill ou teste. Nenhuma alteração temporária de ambiente necessária.

### Critérios de sucesso

Do card: nenhum critério oficial fornecido além do título. Da análise: requisitos explícitos do usuário, evidências/lacunas/opções, contrato implementável e uma única escrita. Do futuro documento: cobertura J00–15/trilha+ramos, campos vazios, fontes, condicionais e limites são critérios inferidos desta recomendação, não critérios oficiais do card.

## Restrições aplicáveis

AGENTS exige Nix para desenvolvimento; git fora do ambiente. Backend: Clean Architecture/DDD; frontend: FSD, acessibilidade e fluxo sem IA. Sem mudança funcional/testes unitários a acrescentar. Skill autoriza somente novo Markdown de análise em pasta existente. Dados reais/segredos fora do Git. Referências legais são as do projeto; não se emite parecer jurídico.

## Classificação comentada

product: definir observação e aceite do processo do estudante. Preocupações user-experience, delivery e privacy. clarification/system/delivery, incerteza alta, reversibilidade fácil; risco médio de falso aceite/identificação se limites forem ignorados.

## Decisão de roteamento

Subpastas imediatas realmente inventariadas: backend, ambientes, frontend, templates, revisao e requisitos. prompts/README.md define requisitos para levantamento/análise/refinamento. Escolha prompts/requisitos: contrato de aceitação do sistema inteiro, não só UI ou backend. Frontend tem precedente de roteiro visual, revisao cabe inspeção documental, backend tem testes; propósito principal favorece requisitos. Não há linhagem prévia nem AGENTS local; confiança alta.

## Dimensões de decisão

| Dimensão      | Prioridade | Direção/limiar                                    | Base                               |
| ------------- | ---------- | ------------------------------------------------- | ---------------------------------- |
| user-value    | 1          | Observar compreensão humana                       | RNF01/título                       |
| correctness   | 1          | Não declarar execução/integração/aceite sem prova | main/App/dossiê                    |
| privacy       | 1          | Minimização e evidência autorizada                | segurança/manual                   |
| simplicity    | 2          | Sem infraestrutura nova                           | Precedente Markdown                |
| time-to-value | 2          | Contrato redigível agora                          | Bloqueios não impedem planejamento |

## Alternativas consideradas

| Opção                             | Prova quando executada/usada                                                  | Não prova                                                                            | Exige/quem executa/cabe hoje                                                                  | Título                                                                        |
| --------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Estado atual: checklist/matrizes  | Especificações e evidências parciais                                          | Sessão representativa/processo completo                                              | Já disponível, mas insuficiente                                                               | Atendimento não demonstrado                                                   |
| A Documento humano + modelo vazio | Após sessão: ações, compreensão, ajuda, obstáculos na configuração registrada | Documento sozinho nada executa; pessoa única não prova população/WCAG/matriz inteira | Autor QA; estudante real/facilitador depois. Escrever cabe agora; execução completa bloqueada | Sim para criar roteiro, condicionado a produto; não fecha execução/aceite     |
| B Automação de jornada            | Fluxo e contratos das fronteiras realmente exercitadas                        | Compreensão ou representatividade humana                                             | Engenheiro de testes/oráculos/harness/ambiente tests. Só recorte parcial viável hoje          | Sozinha insuficiente para leitura recomendada                                 |
| C Híbrido com nova automação      | Observação humana + regressão funcional delimitada                            | Não remove ausência de integração                                                    | Autor/QA/engenharia + baseline por identidade; maior escopo                                   | Pode satisfazer, mas código novo não é exigido pelo título/critério fornecido |

A e C são viáveis para planejamento; B viável como teste parcial, não prova de sistema ausente. Não criar mocks/“E2E completo” para mascarar bloqueio. Referenciar automação existente em A não transforma a entrega em híbrido com código.

## Perfil de pagamento comparativo

Escala ordinal relativa ao estado atual, sem soma.

| Dimensão      | Prioridade |   A | B parcial |   C | Confiança | Base                       |
| ------------- | ---------: | --: | --------: | --: | --------- | -------------------------- |
| user-value    |          1 |  +2 |         0 |  +2 | Alta      | RNF01/observação           |
| correctness   |          1 |  +1 |        +1 |  +1 | Média     | Limites explícitos         |
| privacy       |          1 |  +1 |         0 |  +1 | Média     | Minimização proposta       |
| simplicity    |          2 |  +2 |        -1 |  -2 | Alta      | Só Markdown em A           |
| time-to-value |          2 |  +2 |        -1 |  -1 | Alta      | A redigível sem integração |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### (c) Recomendações e decisão desta versão

Adotar A: documento operacional de roteiro de aceitação para execução humana e modelo vazio de registro. **O documento não é um teste.** Ele especifica a sessão; a atividade humana futura avalia o sistema. Descrever entrega como “documentar protocolo de aceitação e registro de execução”, nunca “implementar teste E2E” ou “aceitar a jornada”.

Atende à interpretação recomendada de “Criar roteiro”; confirmar natureza oficial L01. Não converter RNF01 proposto em meta aprovada.

### Impacto da revisão

Nenhum identificado — inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão    | Estado      | Ganho                        | Base              |
| ----------- | ----------- | ---------------------------- | ----------------- |
| user-value  | prioritized | Preserva observação humana   | RNF01/H1          |
| correctness | prioritized | Distingue plano/mocks/aceite | dossiê/composição |
| simplicity  | prioritized | Só Markdown                  | Precedentes       |

### Dimensões satisfeitas por limiar

| Dimensão      | Limiar                             | Atendimento                      |
| ------------- | ---------------------------------- | -------------------------------- |
| privacy       | Nenhum dado real/segredo no modelo | Sintéticos e referência restrita |
| time-to-value | Escrever sem corrigir produto      | Bloqueios/condicionais           |

## Especificação implementável

### Arquivos a criar em tarefa posterior

1. docs/testes/roteiro-aceitacao-jornada-completa-estudante.md — protocolo e rastreabilidade.
2. docs/testes/evidencias/modelo-registro-aceitacao-jornada-completa-estudante.md — formulário reutilizável vazio, não laudo.

Pastas já existentes; nomes minúsculos/hífens seguem roteiro/evidências descobertos. Não criar relatório executado, editar matrizes/dossiê/registro antigos ou preencher data/participante/veredito.

### Estrutura seção a seção do roteiro

| Seção                      | Conteúdo obrigatório                                                                                                                                |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 Natureza/objetivo/status | Documento operacional, não teste; card só com título; não executado; separar documento e aceite                                                     |
| 2 Escopo/resultados        | J00–15, trilha/ramos, opcionais, fontes, conflitos; sem envio externo presumido                                                                     |
| 3 Origem dos critérios     | ID local, definido/inferido, caminho/seção/trecho, RF/CT/RNF, decisão condicional                                                                   |
| 4 Ambiente/pré-condições   | Commit/branch, URL/entrypoint, dependências reais, conta/sessão, estado/reset, browser/SO/viewport, leitores PDF/DOCX; valores de sessão vazios     |
| 5 Perfil/recrutamento      | Público documentado e L03/L04; pessoa real observa, persona/massa fornece conteúdo; sem nomear participante                                         |
| 6 Privacidade              | Finalidade/voluntariedade/interrupção, consentimento antes de sessão, sem gravação padrão, pseudônimo, retenção/acesso a confirmar                  |
| 7 Massa/preparação         | Ana como referência parcial, campos sintéticos a usar, variantes condicionais, credenciais fora do Git, nenhum contato externo                      |
| 8 Preflight                | Engenharia confirma salvar/reler/sessão/versões/itens/modelo/revisão/prévia/download/vagas/associação; bloqueia dependentes sem fingir continuidade |
| 9 Protocolo facilitador    | Objetivo neutro, sem ensinar solução; observar compreensão/ajuda/tempo/tentativas; registrar intervenção                                            |
| 10 Passos                  | Expandir J00–15 com ação, esperado, critério/origem, evidência, RF/CT/RNF, dependência e limitação                                                  |
| 11 Regras                  | Estados e gravidade propostos; critérios sem limiar; fim da sessão distinto de aceite                                                               |
| 12 Registro/revisão        | Link para modelo vazio; preenchimento só após executar, sanitização, assinatura por papéis                                                          |
| 13 Cobertura/limites       | Automação existente e fronteiras; lacunas; não repetir matriz combinatória como tarefa humana                                                       |

Cada passo deve ter: ID/ramo; objetivo para estudante; ação de referência para facilitador; pré-condição; dados; esperado; critério rotulado definido/inferido e fonte; evidência mínima; requisito/caso real ou “sem CT dedicado”; E/T/B de planejamento separado do resultado vazio; dependência/alternativa/limite.

Conteúdo mínimo: acesso e recuperação como ramo; painel vazio/rascunho/concluído; preencher/corrigir; adicionar/editar/remover e orientação de projeto; documentos; criar/escolher versões; selecionar itens/seções/modelo; revisar/retornar; prévia/troca; PDF e DOCX/download/conferência; vagas resultado/vazio/erro; associação manual/consulta/classificações.

Não escrever cliques para telas não compostas. Documentar intenção e pré-condição ausente. Negativos de autorização/integridade ficam como referências técnicas; estudante não deve atacar conta alheia ou provocar falha externa. Não repetir todas combinações RF12: pessoa observa compreensão de escolha manual, automação trata invariantes. Ausência de experiência tem esperado condicional a L05; não herda bloqueio de harness.

### Perfil/protocolo recomendado, a confirmar

Uma pessoa real estudante FATEC, buscando estágio ou próxima à conclusão, com pouca/nenhuma experiência em elaborar currículo. Não confundir experiência profissional com habilidade de criar currículo. Levantar familiaridade com web, dispositivo habitual e necessidade assistiva só no grau necessário; não coletar diagnóstico. Produto/design definem recrutamento inclusivo.

Um participante serve ao ensaio qualitativo inicial proposto, não estima taxa populacional nem representa toda a instituição. Mais perfis/dispositivos exigem outras sessões e plano explícito, sem número “estatístico” inventado.

Facilitador/observador podem ser a mesma pessoa, com registro fiel. Estudante usa dados sintéticos; pensar em voz alta é opcional. Briefing informa finalidade, forma/acesso ao registro e possibilidade de parar. Sem protocolo/consentimento aprovado não iniciar. Sem gravação por padrão, falas identificáveis ou assinatura pessoal em Git.

Registrar configuração efetivamente usada. Não exigir todos navegadores/seis larguras de cada participante nem declarar RNF02/RNF03 integralmente validados. Auditoria de acessibilidade e matriz de compatibilidade são complementos específicos.

### Regras de resultado e gravidade propostas — inferidas, L06/L07/L13

| Estado                | Condição após executar                                                                 | Alegação permitida                                   |
| --------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| Não executado         | Ação não realizada                                                                     | Sem evidência; registrar motivo                      |
| Bloqueado             | Pré-condição/implementação/composição ausente impede tentativa válida                  | Bloqueio, sem aprovação nem reprovação automática    |
| Executado e aprovado  | Tentativa real, esperado rastreado observado, evidência e condição de ajuda declaradas | Só passo/participante/versão/configuração observados |
| Executado e reprovado | Tentativa válida contradiz esperado definido ou inferido confirmado                    | Achado com fonte e evidência                         |
| Inconclusivo          | Falta regra/oráculo/evidência apesar de tentativa                                      | Encaminhar decisão, sem conformidade                 |

Distinguir “sem ajuda” e “concluído com ajuda”; ajuda não satisfaz silenciosamente método RNF01 sem auxílio. Sem meta aprovada, tempo/taxa apenas descritivos. Cenário de falha controlada pode passar sem aprovar a operação de sucesso.

Gravidade local proposta, não importada de responsividade: crítica = exposição indevida/credencial ou perda/corrupção grave; interromper sessão e registrar mínimo. Alta = resultado principal impossível sem alternativa segura. Média = contorno/ajuda relevante. Baixa = não impeditivo. Prioridade de correção é outra decisão.

Encerrar sessão contabilizando todas tarefas, inclusive bloqueadas/não executadas/inconclusivas. Declarar jornada aceita apenas após execução/aprovação de todos passos obrigatórios confirmados por produto, sem bloqueio/inconclusivo obrigatório e com decisão expressa de signatário. Tolerância a defeitos/risco depende de confirmação; não inventar “zero defeitos” global.

### Modelo de registro inteiramente vazio

Instruções/legenda separadas do formulário. Nenhum estado, data, participante, resultado ou veredito preselecionado, inclusive “não executado”. IDs de planejamento podem ser cabeçalhos, não resultados.

```markdown
# Modelo de registro de execução — aceitação da jornada completa

## Identificação

- Referência/versão do roteiro:
- Commit/branch:
- Ambiente/URL/composição:
- Data/duração:
- Código do participante:
- Perfil pertinente sem identificação:
- Facilitador/observador:
- Referência restrita de autorização de participação:
- SO/navegador/versão/dispositivo/viewport/tecnologia assistiva:
- Massa/estado inicial/reset:
- Leitores PDF/DOCX e versões:

## Passos

| Passo/critério/origem | Ação observada | Esperado rastreado | Resultado observado | Ajuda/tempo/tentativas | Estado | Evidência sanitizada | Defeito/gravidade | Bloqueio/dependência | Responsável/retorno |
| --------------------- | -------------- | ------------------ | ------------------- | ---------------------- | ------ | -------------------- | ----------------- | -------------------- | ------------------- |
|                       |                |                    |                     |                        |        |                      |                   |                      |                     |

## Percepção do participante

| Tarefa | Compreensão em paráfrase sem identificação | Dificuldade | Sugestão espontânea | Limite |
| ------ | ------------------------------------------ | ----------- | ------------------- | ------ |
|        |                                            |             |                     |        |

## Consolidação

- Passos executados:
- Não executados/motivos:
- Bloqueados/dependências:
- Inconclusivos:
- Evidências/revisão de sanitização:
- Limites/alegações permitidas:
- Pendências/responsáveis/prazos:
- Decisão/justificativa:
- Responsável autorizado pela decisão:
- Assinatura/registro de aprovação:
```

Após execução autorizada, cópia textual recomendada em docs/testes/evidencias/aceitacao-jornada-completa-estudante-<identificador-da-sessao>.md, sem nome pessoal no identificador. Não criar cópia agora. Quem valida relato e quem decide aceite são papéis distintos. Registrar papel/referência restrita do aprovador quando necessário, sem assinatura digitalizada.

Capturas sanitizadas têm precedente, mas não são obrigatórias. Não versionar nesta entrega imagens/vídeos/PDF/DOCX/logs brutos/traces/cookies/consentimento assinado ou dados reais. Futuras capturas dependem de finalidade/autorização/revisão/acesso/retenção definidos. Não inventar provedor ou prazo.

### Honestidade: alegações permitidas e proibidas

Permitido: roteiro proposto; observação limitada à configuração; cenário técnico com fronteira simulada; bloqueio por composição.

Proibido: jornada aceita sem execução/decisão; generalizar de uma pessoa para estudantes; RNF01 atendido sem política; E2E real por jsdom; download por callback/Blob; WCAG AA por checklist; toda matriz por um browser; candidatura enviada por classificação; Grupo 2 ativo por fixture; copiar aprovação de laudo antigo.

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão    | Perda                                       | Severidade | Afetados         |
| ----------- | ------------------------------------------- | ---------- | ---------------- |
| correctness | Aceite aparente de fluxo desconectado       | Alta       | Equipe/estudante |
| user-value  | Automação não revela compreensão            | Alta       | Design/estudante |
| privacy     | Evidência identifica pessoa/expõe currículo | Alta       | Participante     |

### Custos aceitos para priorizá-las

| Favorecida  | Custo                           | Prejudicada   | Aceitabilidade                                           |
| ----------- | ------------------------------- | ------------- | -------------------------------------------------------- |
| user-value  | Sessão/moderação futura         | time-to-value | Justificado por RNF01, não executado agora               |
| correctness | Bloqueios/condicionais extensos | simplicity    | Necessários                                              |
| simplicity  | Sem nova regressão automatizada | reliability   | Testes existentes referenciados; outro card para ampliar |

## Riscos e efeitos de segunda ordem

Confundir roteiro/laudo/teste; trocar aplicação por harness; transformar recomendação em política oficial; divulgar defaults pessoais; impedir autoria pela falta de integração; inferir cobertura total de fixture. Mitigações: natureza explícita, preflight, origem dos critérios, revisão de dados, separar autoria/sessão e mapa de fronteiras.

## Ambiente e gates

Sem impacto em código, comportamento ou testes. **Não há baseline de suíte para entrega A e nenhum foi executado.** Não copiar contagens históricas. Se incluir executável, revisar análise antes, com baseline real por identidade no ambiente correto e autorização/controle das alterações temporárias. Esta versão não autoriza linearização Alembic, edição Nix, restore ou limpeza.

Fontes: docs/configuracao-ambiente.md, .github/workflows/ci.yml, src/frontend/package.json, flake.nix e nix/*.nix examinados. CI executa lint/testes backend, integração de associações, frontend lint/format/check/build e Gitleaks. Não há gate explícito de Markdown docs/prompts. npm --prefix src/frontend run format:check usa prettier --check . no frontend; não comprova formatação de docs. A análise histórica do roteiro F1.1 atribui alcance documental excessivo a esse comando.

Comandos reais de consulta/gate existentes:

```bash
git status --short
git diff --check
git diff --stat
git diff --name-only
nix develop .#quality --command gitleaks git --redact --no-banner --exit-code 1
```

Formatação específica proposta para os dois documentos, usando a dependência Prettier do manifesto, se já instalada:

```bash
nix develop .#quality --command src/frontend/node_modules/.bin/prettier --check docs/testes/roteiro-aceitacao-jornada-completa-estudante.md docs/testes/evidencias/modelo-registro-aceitacao-jornada-completa-estudante.md
```

É comando proposto para autoria posterior, não gate já executado. Não instalar dependências por conveniência nesta análise. Gitleaks git varre histórico, não garante arquivo untracked; git diff --check tampouco cobre untracked. Ler documentos novos e revisar segredos/dados explicitamente; modo de scan do working tree precisa de help verificado antes de especificar comando adicional. Não declarar gates aprovados sem executar.

Nenhuma alteração de ambiente necessária. Regras de diffs temporários/restauração não se aplicam a A. Estado final da análise deve ser só um novo Markdown; da futura autoria, só dois documentos. Não exigir árvore artificialmente limpa removendo entregáveis ou mudanças alheias.

## Validação da decisão

| Hipótese/resultado     | Evidência necessária             | Método                                     | Revisar se                                     |
| ---------------------- | -------------------------------- | ------------------------------------------ | ---------------------------------------------- |
| A atende card          | Confirmação L01                  | Produto                                    | Descrição oficial exigir código/execução       |
| Processo coberto       | J00–15/ramos confirmados         | Produto/design confrontam RF/UC/wireframes | Recorte mudar                                  |
| Autor não inventa      | Estrutura/fontes/condicionais    | Revisão QA                                 | Passo essencial sem oráculo sequer condicional |
| Sessão pode ocorrer    | Conta/preflight/composição reais | Engenharia, tarefa futura                  | Só harness ou main incompleto                  |
| Registro honesto       | Campos sem resultado             | Leitura/diff                               | Data/participante/aprovação preenchidos        |
| Privacidade suficiente | Protocolo/responsável/retenção   | Produto/governança                         | Evidência identificável desnecessária          |

## Handoffs e atividades posteriores

### Skills inventariadas e adequação

Exatamente sete SKILL.md em .agents/skills. Foram lidos contrato de escopo e teste de adequação de cada skill, não invocadas skills implementadoras.

| Skill                             | Referências lidas e critério                                                                                      | Veredito para documento                                                                                     |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| decision-analysis-v4              | SKILL e classification-taxonomy/output-schema/output-routing/artifact-classification: só novo Markdown de análise | Valid para esta análise; não para escrever roteiro como implementação                                       |
| backend-domain-orchestration-v2   | SKILL, clean-boundary.md, backend-fit-check.md: backend/domínio/orquestração/unidade interna                      | Mismatch: não é domínio/use case                                                                            |
| backend-adapters-drivers-v2       | SKILL, outer-boundary.md, backend-fit-check.md: contrato interno/adapter/driver/unidade externa                   | Mismatch: não altera API/ORM                                                                                |
| frontend-implementation-v3        | SKILL, scope-boundary.md, frontend-fit-check.md: tela funcional/unidade cliente                                   | Mismatch: não constrói tela/teste unitário                                                                  |
| cross-cutting-implementation-v1   | SKILL, scope-boundary.md, cross-cutting-fit-check.md: mecanismo transversal e política                            | Mismatch: privacidade é restrição documental, não mecanismo                                                 |
| integration-system-testing-v1     | SKILL, test-scope-boundary.md, test-fit-check.md: quatro confirmações, primeira “resultado é um teste”            | Mismatch para A. Palavra aceitação não basta. Elegível à fatia executável de B/C com outra análise/oráculos |
| nix-environment-implementation-v1 | SKILL, nix-scope-boundary.md, nix-fit-check.md: só artefatos Nix, documentação é non-nix                          | Mismatch: ambiente de validação não define natureza                                                         |

Lacuna de processo: não há skill local de autoria de roteiro humano. Autor técnico/QA deve receber tarefa documental explícita citando esta versão: **criar apenas os dois Markdown propostos, sem executar sessão, preencher resultados ou alterar produto**. Isso é o que o usuário precisaria autorizar depois; não invocar skill de testes inadequada nem criar skill automaticamente.

Produto confirma natureza/escopo/perfil/políticas; design revisa tarefas neutras/inclusão; QA escreve documentos e rastreia; engenharia atesta preflight em demanda distinta; equipe seleciona estudante/signatário e autoriza sessão futura. Não foram usados subagentes.

## Síntese

Status proposed: contrato suficiente para escrever com recomendações condicionais. Documento operacional não é teste nem aceite executado. Jornada completa integrada não está disponível na composição atual. Confirmações L01–15 não são fatos nem resultados e não bloqueiam a autoria documental.

### Verificações realizadas nesta análise

- git status --short: somente este novo artefato; git diff --exit-code e git diff --cached --exit-code sem diferenças em arquivos rastreados.
- Nix no sandbox falhou ao abrir /nix/var/nix/db/big-lock (filesystem somente leitura); verificações repetidas fora do sandbox mediante autorização.
- Gitleaks via nix develop .#quality: 356 commits, aproximadamente 8,85 MB, código 0, nenhum segredo encontrado no histórico. Não cobre o novo arquivo untracked.
- Prettier --check inicialmente apontou formatação neste arquivo; a formatação foi ajustada somente nele, preservando literalmente o insumo original abaixo.
- Nenhum teste, aplicação, migration ou sessão de aceitação foi executado.

## Apêndice — insumo original integral do usuário

O bloco abaixo preserva a solicitação recebida; não é resultado de investigação.

> Início do insumo

```text
$decision-analysis-v4 Implementar "Criar roteiro de aceitação com estudante representativo para a jornada completa.". Antes de decidir o que entregar, descubra **que tipo de entregável o card pede** (roteiro/documento de aceitação para execução humana, teste automatizado, ou combinação), qual é a jornada completa do sistema segundo os artefatos do projeto, o que significa "estudante representativo" aqui, e o que da jornada pode de fato ser percorrido hoje. Esta é uma análise nova, iniciada do zero.

## Regra principal: não presumir

Todo fato deve vir de um artefato lido (histórico Git, código, testes, documentação, requisitos, matrizes, wireframes, definições de ambiente, workflows de CI), com o caminho indicado. O que nenhum artefato definir deve ser registrado como lacuna, nunca como fato.

- Separe em seções distintas: **(a) fatos encontrados**, com caminho e trecho; **(b) lacunas**, ou seja, o que nenhum artefato define; **(c) recomendações**, que são suas, com justificativa.
- Para cada lacuna, apresente as opções viáveis, recomende uma e marque se depende de decisão de produto, de design ou de engenharia. **Quando a decisão for de produto e houver um padrão técnico razoável, adote-o como recomendação condicional ("padrão recomendado, a confirmar") e prossiga**, reservando o bloqueio apenas para o que impeça de fato escrever o entregável.
- Quando artefatos divergirem (documentos entre si, ou documentos e código), aponte a divergência, diga qual fonte parece mais confiável e por quê, sem escolher em silêncio.
- Não transponha para a aceitação regras ou resultados de testes de outros recursos sem que um artefato sobre a jornada as sustente.

## Ponto de partida

Parta exclusivamente do estado atual desta branch, criada a partir da `dev` atualizada. Não presuma a existência de nenhum roteiro, plano de aceitação, persona, tela, rota, teste ou análise. O que existir entra como fato (com a cobertura avaliada), o que não existir entra como lacuna. Inventarie o que de fato existe na base e não presuma nomes.

## Texto do card

Somente o título foi fornecido: "Criar roteiro de aceitação com estudante representativo para a jornada completa.". Não há descrição nem critérios de aceite. **Não invente critérios.** Derive o que for possível do título e dos artefatos, marque a origem de cada critério como "definido" ou "inferido" e liste exatamente o que precisa ser fornecido para fechar cada lacuna. Esclarecimento do usuário: "jornada completa" refere-se ao **processo completo do sistema**, de ponta a ponta, e o usuário **não tem certeza se o entregável é um teste ou um roteiro/documento de aceitação**: resolver isso é parte da análise.

## Fontes a analisar

1. **Histórico Git local.** A CLI do GitHub e a rede podem não estar disponíveis; **não dependa delas**. Localize por inspeção (merges, squashes, mensagens, nomes de branch, histórico dos arquivos) os trabalhos ligados às etapas da jornada e a qualquer roteiro, plano ou evidência de aceitação. Número de card não é número de PR: não infira a ligação apenas pela coincidência de números, e registre como identificou cada trabalho.
2. **Documentação pertinente**, localizada por busca (não presumida): requisitos funcionais e não funcionais (inclusive usabilidade, compatibilidade e acessibilidade), mapeamento de jornadas e fluxos, wireframes e documentos de interface, matrizes de rastreabilidade e de testes, casos de teste e evidências em `docs/`, manual e guias, e análises anteriores em `prompts/`. Registre os termos buscados (por exemplo jornada, fluxo, persona, estudante, perfil de usuário, público-alvo, representativo, aceitação, aceite, homologação, usabilidade, roteiro, teste com usuários, evidência) e o que cada busca retornou, **inclusive resultados vazios**.
3. **Código atual relacionado**, no front-end e no backend: telas e navegação, rotas e handlers, casos de uso, composição da aplicação que sobe (`main.py`, `factory.py` e a composição do front-end), massas e fixtures de teste, e os testes existentes (unitários, integrados e de jornada).
4. **Ferramental e instruções:** `AGENTS.md` (raiz, backend e front-end), a classificação de níveis de teste usada pelas referências das skills, workflows de CI, definições de ambiente e as skills disponíveis em `.agents/skills` (inventarie quais existem, sem presumir nomes).

## O que levantar

- **A natureza do entregável (a pergunta central).** Procure no projeto como "roteiro", "plano", "caso de aceitação" e "evidência" são tratados: formato, localização, conteúdo, quem executa, como o resultado é registrado e se existem precedentes de documento manual versus teste automatizado. Verifique o que `AGENTS.md`, `docs/` e as referências de teste dizem sobre aceitação e sobre testes de sistema ponta a ponta. Compare as alternativas: (a) **documento de roteiro de aceitação para execução humana**, com modelo de registro; (b) **teste automatizado** da jornada; (c) **híbrido**. Para cada uma, diga o que prova e o que **não** prova (por exemplo, compreensão e usabilidade por uma pessoa real contra fluxo funcional automatizado), o que exige, quem executa e se ela cabe no que o repositório oferece hoje. Recomende uma, com justificativa, e diga se o título do card é satisfeito por ela. **Se a conclusão for documento, diga explicitamente que ele não é um teste e como deve ser descrito.**
- **A jornada completa.** Reconstrua, **somente a partir dos artefatos**, as etapas do processo do sistema do início ao fim (do primeiro acesso até o resultado final do uso), com a fonte de cada etapa, as pré-condições e os resultados esperados que os documentos definem. Inclua os caminhos alternativos e de falha que os documentos definem. Registre divergências entre documentos sobre a jornada. Não adicione etapas que nenhum artefato sustente.
- **O que é "estudante representativo".** Descubra se algum artefato define persona, perfil de usuário, público-alvo ou critérios de representatividade; se existe massa de dados de teste e se ela serve; se o ator é uma pessoa real, uma persona ou ambos; quantos participantes, que características (por exemplo experiência, dispositivo, necessidades de acessibilidade) e que dados ele usa. Se nada definir, trate como lacuna de produto e proponha um perfil e critérios mínimos com justificativa. **Trate privacidade**: participação de pessoa real, consentimento, dados pessoais em evidência e o que a documentação de segurança e de privacidade exige; prefira dados sintéticos.
- **O estado de implementação por etapa.** Para cada etapa da jornada, registre com evidência: se a tela existe, se a rota ou o caso de uso de backend existe, se a etapa está composta na aplicação que sobe e se há integração real entre front-end e backend, ou se só existe em ambiente de teste ou com simulação. **Não presuma que a jornada completa é executável hoje.** Classifique cada etapa como executável na aplicação que sobe, executável só com composição de teste, ou bloqueada, e diga o que isso implica para o roteiro (por exemplo aceitação em etapas, em ambiente de homologação ou com a composição de teste explicitamente declarada).
- **Critérios de aceite e regras de decisão.** O que os requisitos e as matrizes de teste definem como critério (por requisito e caso de teste), o que significa uma etapa "aprovada", "reprovada" ou "bloqueada", a gravidade de um defeito e o que encerra a aceitação. Registre o que depende de produto.
- **Rastreabilidade e cobertura existente.** Para cada etapa, quais requisitos e casos de teste a cobrem e quais testes automatizados já a exercitam e em que nível. O roteiro não deve repetir o que a automação já prova, mas também não pode alegar o que a automação não prova. Aponte lacunas da matriz.
- **Evidência e registro.** Onde e em que formato o resultado da execução deve ser registrado, os precedentes de evidência no repositório, e o que não pode entrar (dados pessoais, capturas, binários). Diga quem assina ou aprova.
- **Ambiente e gates.** Se o entregável for documento: que gates se aplicam a arquivos de documentação (formatação, varredura de segredos) e confirme que não há impacto sobre testes. Se houver qualquer parte executável ou alteração de testes: baseline informativo (comando, ambiente, resultado, contagens, comparado por identidade), usando os comandos reais descobertos por inspeção. Execute apenas comandos de leitura.
- **Bloqueios preexistentes:** registre, sem tratá-los como escopo e sem corrigi-los, tudo que impeça percorrer a jornada ou executar o roteiro.

## Escopo

Definir o **entregável do card** (de modo que um executor possa produzi-lo sem inventar nada): sua natureza, estrutura, conteúdo, modelo de registro de resultados, regras de aceitação, rastreabilidade e protocolo de execução com o estudante representativo, com a jornada completa e o estado real de cada etapa.

Fora do escopo: **executar a aceitação ou fabricar resultados**; alterar código, testes ou documentos existentes além do que a análise recomendar como entregável; implementar funcionalidade ou integração que não exista; corrigir defeitos encontrados (registre-os como achados); decidir pela equipe quem será o estudante real; alterações de ambiente ou de CI.

## Instruções

- Para cada decisão que os artefatos não resolverem, recomende uma opção com justificativa e marque se depende de produto, de design ou de engenharia.
- **Especificação implementável.** Defina o(s) arquivo(s) a criar (caminho e nome conforme as convenções de `docs/`), a estrutura seção a seção, o conteúdo obrigatório (objetivo e escopo; ambiente e pré-condições; perfil do estudante e massa de dados; passos com ação, resultado esperado, critério de aceite, evidência e requisito rastreado; regras de aprovação, reprovação e bloqueio; gravidade; modelo de registro vazio para a execução; limites e alegações permitidas e proibidas), e diga o que o executor pode escrever sem decisão de produto e o que precisa de confirmação. O modelo de registro deve ficar **em branco**: nenhum resultado, data, participante ou veredito pode ser preenchido pela implementação.
- **Honestidade da aceitação.** Diga como o roteiro distingue "executado e aprovado" de "não executado" e de "bloqueado por ausência de implementação ou de composição", e que alegações são proibidas (por exemplo declarar a jornada aceita sem execução, ou generalizar a partir de um participante). Aponte, etapa por etapa, o que o roteiro **não** consegue verificar hoje.
- Registre achados de front-end, backend e documentação (divergências, etapas sem implementação, requisitos sem caso de teste, riscos de privacidade) em seção própria, sem corrigi-los.
- Indique a divisão de trabalho. **Leia o contrato de escopo e o teste de adequação de cada skill inventariada em `.agents/skills` e confirme, com evidência, se o entregável recomendado é elegível a alguma delas**; se nenhuma cobrir (por exemplo por ser documento de aceitação, e não teste ou código), registre como lacuna de processo e indique quem deve produzi-lo e o que o usuário precisaria autorizar. Especifique nomes de arquivos e comandos de validação, para o executor não precisar inventá-los.
- Se a recomendação incluir qualquer parte executável, registre as regras de alteração temporária de ambiente (diffs completos no resumo, `git restore` por caminhos explícitos, `git status` limpo ao final). Se for só documento, declare que nenhuma alteração de ambiente é necessária.
- Defina o roteamento do artefato de análise (pasta em `prompts/`) conforme a organização existente, e justifique.
- Se, com as recomendações condicionais, o contrato do entregável ficar suficientemente definido, mude o status para `proposed` e explique o que ainda precisa de confirmação; se algo bloquear a escrita do entregável, mantenha `pending` e liste exatamente o que falta e quem deve fornecer.
- Não implemente nada. A única escrita é o novo artefato de análise.

```

> Fim do insumo

A mensagem de invocação subsequente forneceu a skill decision-analysis-v4 e seu caminho .agents/skills/decision-analysis-v4/SKILL.md; o conteúdo normativo foi lido nesse arquivo e suas quatro referências, conforme inventário.
