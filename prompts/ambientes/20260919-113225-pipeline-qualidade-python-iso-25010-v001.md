---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-09-19T11:32:25-03:00"
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
    - path: flake.nix
      relationship: primary
      representation: structured-data
      function: build
      format: nix
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 9cef180"
      availability: available
    - path: nix/backend.nix
      relationship: primary
      representation: executable-script
      function: build
      format: nix
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 9cef180"
      availability: available
    - path: nix/tests.nix
      relationship: supporting
      representation: executable-script
      function: build
      format: nix
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 9cef180"
      availability: available
    - path: .github/CODEOWNERS
      relationship: context
      representation: prose
      function: configuration
      format: CODEOWNERS
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 9cef180"
      availability: available
    - path: README.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "papéis da equipe e responsabilidades de testes/CI&CD"
      content_state: working-tree
      revision: "working-tree based on 9cef180"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 9cef180"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/ambientes
  considered_directories: [prompts/ambientes, prompts/revisao, prompts/backend]
  confidence: high
  rationale: "A decisão define automação, execução Nix e controles transversais de CI; não altera uma funcionalidade ou camada específica do backend."
classification:
  sphere: engineering
  concerns: [delivery, reliability, security]
  decision_kind: design
  scope: system
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — pipeline de qualidade Python alinhado à ISO/IEC 25010

## Solicitação original

```text
Faça uma análise para incluir no pipeline do GitHub por meio de Git Actions análises com o Randon python. Eu pensei nessas análises:

ISO/IEC 25010
│
├── Maintainability
│   ├── Analysability
│   │    ├── Cyclomatic Complexity ── Radon
│   │    ├── Halstead ─────────────── Radon
│   │    └── Code Smells ──────────── Pylint/Ruff
│   │
│   ├── Modifiability
│   │    ├── Maintainability Index ── Radon
│   │    ├── Duplication ──────────── jscpd
│   │    └── Coupling ─────────────── análise arquitetural
│   │
│   ├── Testability
│   │    ├── Cyclomatic Complexity
│   │    └── Test Coverage ────────── coverage.py
│   │
│   └── Modularity
│        ├── Coupling
│        ├── Dependency cycles
│        └── Dependency structure
│
├── Reliability
│   ├── pytest
│   └── mutation testing
│
└── Security
    ├── Bandit
    └── pip-audit
```

## Informações complementares

- Nesta análise, “Randon” foi interpretado como **Radon**, a ferramenta Python de métricas de complexidade ciclomática, Halstead e Maintainability Index. A documentação do Radon confirma esses quatro comandos (`cc`, `hal`, `mi` e `raw`) e as faixas A–F da complexidade ciclomática ([Radon](https://radon.readthedocs.io/en/latest/commandline.html)).
- O repositório usa Nix obrigatoriamente para ferramentas de desenvolvimento. O shell `backend` hoje fornece FastAPI, SQLAlchemy, Alembic, psycopg e configurações Pydantic; não fornece explicitamente pytest, coverage, Radon, Ruff, Bandit ou pip-audit.
- Não há workflow em `.github/workflows` no estado examinado. Há testes Python em `src/backend/tests`, escritos com `unittest`, e não há manifesto/lock de dependências Python para `pip` examinado nesta análise.
- Ruff pode produzir anotações próprias para GitHub Actions; Bandit e pip-audit possuem integração documentada para Actions ([Ruff](https://docs.astral.sh/ruff/integrations/), [Bandit](https://bandit.readthedocs.io/en/latest/ci-cd/github-actions.html), [pip-audit](https://github.com/pypa/pip-audit/blob/main/README.md)).

## Mudanças desde a versão anterior

Nenhum identificado — análise inicial.

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `flake.nix` | Principal | Dados estruturados | Build | Nix | Arquivo completo | working tree baseado em `9cef180` |
| `nix/backend.nix` | Principal | Script executável | Build | Nix | Arquivo completo | working tree baseado em `9cef180` |
| `nix/tests.nix` | Apoio | Script executável | Build | Nix | Arquivo completo | working tree baseado em `9cef180` |
| `.github/CODEOWNERS` | Contexto | Prosa | Configuração | CODEOWNERS | Arquivo completo | working tree baseado em `9cef180` |
| `README.md` | Contexto | Prosa | Documentação | Markdown | papéis de testes e CI/CD | working tree baseado em `9cef180` |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução de agentes | Markdown | Arquivo completo | working tree baseado em `9cef180` |

### Limites da evidência dos artefatos

Não foram executados Radon, cobertura, linters ou testes: as ferramentas ainda não estão declaradas no ambiente Nix analisado, e esta é uma decisão pré-implementação. A ausência de `.github/workflows` foi constatada por inventário da pasta `.github`; nenhum workflow inexistente foi analisado. Não foram examinados arquivos do frontend, portanto `jscpd` e seus impactos nesse componente não podem receber um gate definitivo nesta versão.

## Problema enriquecido

### Resultado desejado

Criar um workflow de GitHub Actions reprodutível pelo Nix que avalie o backend Python em pull requests e na branch principal, tornando visíveis e, quando maduros, bloqueantes indicadores de manutenibilidade, confiabilidade e segurança da árvore proposta.

### Atores e interesses

- Equipe de backend: feedback rápido sobre testes, defeitos estáticos, complexidade e fronteiras arquiteturais.
- Responsáveis por testes/qualidade: evidência versionada, comparável e sem falsos bloqueios iniciais.
- Responsáveis por CI/CD: execução determinística pelo mesmo ambiente Nix exigido localmente.
- Revisores e mantenedores: gates compreensíveis, com exceções explícitas e evolução gradual de limiares.

### Evidências e fatos observados

- O backend é Python e possui testes unitários; os testes existentes usam `unittest`, não pytest.
- O flake expõe shells `backend`, `frontend` e `tests`; o shell `tests` contém apenas Git.
- O shell `backend` não declara ferramentas de análise ou teste solicitadas.
- Não há workflow GitHub Actions nem arquivo de configuração central para essas ferramentas no recorte examinado.
- As regras do repositório exigem Nix para comandos de desenvolvimento e definem arquitetura limpa para o backend.

### Hipóteses

- O workflow será executado em runners hospedados pelo GitHub e poderá instalar/usar Nix de forma fixa e auditável.
- A primeira implementação pode estender o shell `backend` (ou criar shell específico de qualidade) sem mudar o comportamento de produção.
- O objetivo imediato é o código Python em `src/backend`; controles do frontend serão objeto de decisão própria.

### Perguntas em aberto

- Quais branches devem ser protegidas e quais checks serão exigidos para merge?
- Qual é a linha de base real de cobertura, complexidade e achados após as ferramentas serem instaladas?
- Qual será a fonte de dependências Python distribuídas: Nix, manifesto pip bloqueado, ou ambas? Sem isso, `pip-audit` não possui inventário reprodutível para um gate.
- Quais exceções de segurança têm prazo, responsável e justificativa aceitáveis?

### Escopo

Decidir a estratégia e a ordem de adoção de análises automatizadas para o backend Python e os requisitos de reprodutibilidade do workflow.

### Fora do escopo

- Criar workflow, alterar Nix ou instalar dependências.
- Definir política de proteção de branches no GitHub.
- Avaliar código do frontend ou configurar `jscpd` para toda a base.
- Escolher/configurar definitivamente ferramenta e limiar para mutation testing, coupling e ciclos.

### Critérios de sucesso

- Toda execução usa uma definição Nix versionada e versões fixadas, sem `pip install` ad hoc no workflow.
- O primeiro conjunto de checks produz resultados acionáveis para Python e não bloqueia merge por dívida histórica desconhecida.
- A evolução para gates de cobertura e Radon usa uma linha de base registrada e limiares explicitamente aprovados.
- Segurança estática e vulnerabilidades têm tratamento distinguível entre achado novo, risco conhecido e falha operacional.

## Restrições aplicáveis

1. Ferramentas de desenvolvimento, testes, lint e verificações devem ser executados por `nix develop .#<ambiente> --command ...`; uma Action que instale ferramentas diretamente com `pip` violaria a regra do repositório.
2. Mudanças no backend devem preservar Clean Architecture; métrica de acoplamento não substitui contratos arquiteturais explícitos.
3. Cada check bloqueante deve ser determinístico, ter escopo definido (`src/backend`) e usar versões configuradas no repositório.
4. Não se deve escolher limiares de cobertura ou complexidade antes da primeira linha de base.

## Classificação comentada

É uma decisão de design de engenharia e entrega: define controles automáticos transversais, afetando confiabilidade e segurança além da qualidade interna. O risco é médio porque gates mal calibrados interrompem entregas, enquanto ausência de análises retarda a detecção de regressões.

## Decisão de roteamento

Foi escolhida `prompts/ambientes` porque o objeto principal é o ambiente e a automação de CI, com Nix como restrição central. `prompts/backend` seria adequado a uma decisão de código da camada backend; `prompts/revisao` descreve atividade de revisão, mas não a infraestrutura contínua que a executa.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Reprodutibilidade | Alta | Limiar: Nix e versões configuradas | Evita divergência entre máquina e CI. |
| Confiabilidade do gate | Alta | Limiar: falsos positivos e instabilidade controlados | Um check instável perde legitimidade. |
| Segurança | Alta | Priorizar achados exploráveis e dependências auditáveis | Previne introdução silenciosa de riscos conhecidos. |
| Manutenibilidade | Alta | Priorizar tendência e regressão, não número isolado | Radon e lint orientam revisão sem fingir medir todo o design. |
| Tempo de feedback | Média | Priorizar execução de PR curta | Mantém adesão ao pipeline. |
| Carga cognitiva | Média | Minimizar ferramentas e regras sobrepostas | Facilita correção pelo autor da mudança. |

## Alternativas consideradas

### Alternativa A — todos os controles como gates imediatos

Criar um workflow único e bloqueante com Radon, Ruff/Pylint, jscpd, cobertura, mutation testing, Bandit, pip-audit e análise arquitetural desde o primeiro PR.

É inviável no estado atual: faltam ferramentas e configurações Nix, baseline e inventário pip; `jscpd` também cruza um frontend não examinado. Produziria falhas sem contrato de qualidade calibrado.

### Alternativa B — adoção faseada, Python primeiro, com baseline antes de novos gates

Criar um workflow orientado a paths do backend, acionado em `pull_request` e `push`, que entra via shell Nix de qualidade. Na fase inicial, testes unitários, Ruff e Bandit são bloqueantes após corrigir a linha de base; Radon (`cc`, `mi`, `hal`) e cobertura publicam relatórios/baseline. Pip-audit, mutation, duplicação e arquitetura têm entrada em fases posteriores, com pré-requisitos explícitos.

### Alternativa C — somente relatórios sem gates permanentes

Executar as ferramentas sem falhar o workflow. É seguro para descobrir dados, porém não impede regressão após a linha de base e transforma controles críticos em avisos facilmente ignorados.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Reprodutibilidade | Alta | +1 | +2 | +2 | Alta | Regra Nix e shells atuais |
| Confiabilidade do gate | Alta | -2 | +2 | +1 | Alta | Ausência de baseline/configuração |
| Segurança | Alta | +2 | +2 | 0 | Média | Ferramentas propostas e inventário incompleto |
| Manutenibilidade | Alta | +1 | +2 | +1 | Média | Radon/Ruff cobrem partes, não todo o atributo ISO |
| Tempo de feedback | Média | -2 | +1 | +1 | Média | Mutation e análise ampla são mais custosos |
| Carga cognitiva | Média | -2 | +1 | +2 | Alta | Número de ferramentas e limiares |

Os valores são ordinais; não devem ser somados.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada.

### Decisão recomendada nesta versão

Adotar a **Alternativa B** e implementar em três etapas deliberadas:

1. **Fundação bloqueante:** criar o workflow Nix e um ambiente de qualidade Python versionado. Executar os testes atuais por `python -m unittest discover` ou migrá-los deliberadamente para pytest antes de usar `pytest` como nome do check. Adicionar Ruff e Bandit com configuração versionada e escopo `src/backend`.
2. **Medição e calibração:** publicar como artefatos/sumário do job `radon cc`, `radon mi`, `radon hal` e `coverage.py`; registrar baseline. Depois de revisão humana, bloquear somente regressões (por exemplo, novas unidades acima do rank acordado e cobertura abaixo do baseline por mudança), não uma meta universal inventada.
3. **Controles especializados:** tornar `pip-audit` bloqueante apenas após definir e bloquear o inventário de dependências Python. Avaliar mutation testing em execução agendada/manual; introduzir teste de arquitetura declarativo para dependências, acoplamento e ciclos; decidir `jscpd` em análise que inclua frontend e a ferramenta Node/Nix correspondente.

Radon deve ser nomeado corretamente no workflow. Sua complexidade ciclomática reporta ranks A–F; inicialmente, usar B como faixa de atenção e C ou pior como candidato à revisão humana é uma hipótese de calibração, não uma regra de merge nesta análise.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Reprodutibilidade | maximized | Mesmos comandos e versões localmente e na Action | Regra obrigatória de Nix e flake existente |
| Confiabilidade do gate | prioritized | Falhas representam regressões úteis | Baseline precede limiares |
| Segurança | prioritized | Detecção inicial de padrões inseguros | Bandit é aplicável diretamente ao código Python |
| Manutenibilidade | prioritized | Tendência visível de complexidade e qualidade estática | Radon e Ruff têm cobertura parcial do atributo ISO |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Tempo de feedback | PR não deve depender de mutation testing nem análise de todo o frontend | Controles caros ficam agendados/adiados |
| Carga cognitiva | Cada gate deve ter escopo, configuração e forma de correção documentados | Adoção em etapas e ferramentas separadas por objetivo |
| Segurança de dependências | Inventário bloqueado e auditável antes de bloquear PR | `pip-audit` é condicionado a esse pré-requisito |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Reprodutibilidade | CI e desenvolvimento local podem divergir | Alta | Equipe e revisores |
| Segurança | Padrões inseguros ou CVEs conhecidos chegam mais tarde à revisão | Alta | Usuários e mantenedores |
| Manutenibilidade | Crescimento de complexidade fica invisível até custar mais para mudar | Média | Backend e testes |
| Confiabilidade | Testes podem deixar de ser executados continuamente | Média | Produto e equipe de qualidade |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Reprodutibilidade | Preparar e manter shell Nix de qualidade | Tempo inicial de entrega | Aceitável; é requisito do repositório |
| Confiabilidade do gate | Não bloquear métricas históricas na primeira execução | Segurança/rigor imediato | Aceitável temporariamente, com prazo de baseline |
| Tempo de feedback | Mutation testing não roda em todo PR | Profundidade de detecção | Aceitável em execução agendada/manual |
| Foco no Python | Adiar `jscpd` e frontend | Cobertura de modularidade multilinguagem | Aceitável até análise de escopo frontend |

## Riscos e efeitos de segunda ordem

- Configurar Ruff como substituto automático de Pylint sem escolher regras pode reduzir cobertura de alguns smells; a decisão recomenda Ruff como primeiro linter por simplicidade, não equivalência total.
- Maintainability Index e Halstead são indicadores, não prova de design limpo. Usá-los como bloqueio absoluto incentiva refatorações cosméticas.
- Cobertura alta não prova qualidade dos testes; mutation testing pode elevar a confiança, mas deve ter orçamento de tempo e exclusões justificadas.
- `pip-audit` sem manifesto/lock pode auditar um ambiente diferente daquele efetivamente distribuído ou produzir resultado não reproduzível.
- Uma Action que use `setup-python` e `pip install` parece mais simples, porém contradiz a política Nix e cria duas fontes de verdade para dependências.
- Métricas de acoplamento exigem contratos de camadas explícitos; sem eles, a ferramenta mede importações, não conformidade arquitetural relevante.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Shell de qualidade é reproduzível | Avaliação e execução local/CI com versões fixadas | Rodar todos os checks via `nix develop` no PR piloto | Dependência baixada fora do Nix ou divergência local/CI |
| Testes unitários podem ser gate | Suite atual passa de modo determinístico | Executar discovery no shell backend e registrar duração | Falhas intermitentes ou dependência de banco/rede |
| Radon é útil sem gerar ruído | Relatório de `cc`, `mi` e `hal` revisado por mantenedores | Comparar achados com dificuldade real de manutenção | Muitos falsos positivos ou ausência de ações úteis |
| Cobertura admite limiar | Baseline por arquivo/módulo e tendências em PRs | Gerar relatório coverage antes de definir `fail-under` | Meta global mascara módulos críticos ou bloqueia dívida prévia |
| pip-audit pode ser gate | Manifesto e lock de dependências de produção definidos | Auditar o inventário bloqueado em execução repetida | Resultado varia sem mudança de dependência |
| Análise arquitetural protege as camadas | Contratos de importação/ciclos acordados | Prova de conceito em módulos `domain`, `application`, `infrastructure`, `api` | Contratos conflitam com composição externa legítima |

## Handoffs e atividades posteriores

1. Uma atividade de implementação de ambientes/CI deve criar o workflow, sem instalar ferramentas fora do Nix, e declarar suas versões no flake/shell apropriado.
2. A equipe deve decidir se mantém `unittest` como executor oficial ou migra para pytest; `coverage.py` funciona nos dois cenários, mas o check deve refletir o executor escolhido.
3. Após a primeira execução, abrir revisão desta análise com baseline real, regras Ruff/Bandit, exclusões e limiares aprovados.
4. Abrir análise separada para a estrutura de dependências: contratos de importação, ciclos e medição de acoplamento do backend.
5. Abrir análise que examine o frontend antes de adotar `jscpd` ou controles JavaScript/TypeScript.
6. Definir estratégia de dependências Python bloqueadas antes de habilitar `pip-audit` como gate.

## Síntese

Recomenda-se um pipeline GitHub Actions para o backend Python, executado exclusivamente em Nix e introduzido por fases. Radon deve gerar a linha de base para complexidade, Halstead e Maintainability Index antes de impor limites; testes, Ruff e Bandit são os primeiros candidatos a gates depois da calibração. Cobertura, pip-audit, mutation testing, duplicação e arquitetura têm valor, mas dependem respectivamente de baseline, inventário bloqueado, orçamento de execução, escopo frontend e contratos arquiteturais explícitos.
