---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: 2026-09-13
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
    - path: docs/fundamentos-backend.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 1688619b8cad70805a28397dd30c9b2968a3b1fc"
      availability: available
    - path: nix/backend.nix
      relationship: supporting
      representation: source-code
      function: configuration
      format: nix
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1688619b8cad70805a28397dd30c9b2968a3b1fc"
      availability: available
    - path: flake.nix
      relationship: supporting
      representation: source-code
      function: configuration
      format: nix
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1688619b8cad70805a28397dd30c9b2968a3b1fc"
      availability: available
    - path: prompts/README.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1688619b8cad70805a28397dd30c9b2968a3b1fc"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1688619b8cad70805a28397dd30c9b2968a3b1fc"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/ambientes
  considered_directories: [prompts/ambientes, prompts/backend]
  confidence: high
  rationale: "A decisão modifica exclusivamente o dev shell Nix que disponibiliza ferramentas ao desenvolvimento do backend."
classification:
  sphere: engineering
  concerns: [architecture, implementation, delivery]
  decision_kind: selection
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: low
  reversibility: easy
  risk: medium
---

# Análise de decisão — ambiente Nix para os fundamentos do backend

## Solicitação original

`$decision-analysis-v4 analise o documento 'docs\fundamentos-backend.md'. Crie uma análise para ser usada com skill 'nix-environment-implementation-v1'. Essa análise deve observar as decisões técnicas do documento e adicionar as libs e/ou frameworks adequados sob o controle do nix a serem usadas com o ambiente de backend.`

## Informações complementares

- O documento principal recomenda uma API REST com FastAPI, SQLAlchemy 2.x,
  Alembic, PostgreSQL, `psycopg` e `pydantic-settings`.
- O documento determina Code First, migrations Alembic e a separação entre
  domínio, aplicação, infraestrutura e API; SQLModel não deve ser o modelo
  central.
- O dev shell `backend` atual contém somente `pkgs.git` e `pkgs.python3`.
- `flake.nix` expõe o shell como `.#backend` e importa `nix/backend.nix`.
- A raiz exige que ferramentas de desenvolvimento sejam usadas nos ambientes
  Nix do projeto.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem | Nenhum identificado | v001 inicial | Não há análise anterior identificada | Nenhum histórico a preservar |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `docs/fundamentos-backend.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree baseado em `1688619` |
| `nix/backend.nix` | Apoio | Código-fonte | Configuração | Nix | Arquivo completo | Commit `1688619` |
| `flake.nix` | Apoio | Código-fonte | Configuração | Nix | Arquivo completo | Commit `1688619` |
| `prompts/README.md` | Contexto | Prosa | Documentação | Markdown | Arquivo completo | Commit `1688619` |
| `AGENTS.md` | Contexto | Prosa | Instrução para agentes | Markdown | Arquivo completo | Commit `1688619` |

### Limites da evidência dos artefatos

`docs/fundamentos-backend.md` ainda não está versionado; a análise registra o
conteúdo presente no working tree. Não foram avaliadas versões nem atributos
exatos do Nixpkgs por execução de Nix. A implementação deve confirmar que cada
atributo selecionado existe no conjunto `python3Packages` fornecido pelo input
fixado do projeto antes de gravar a configuração.

## Problema enriquecido

### Resultado desejado

Disponibilizar no dev shell `.#backend` um único interpretador Python com as
bibliotecas necessárias para iniciar uma API REST síncrona baseada em FastAPI,
SQLAlchemy e Alembic, sem instalar dependências globalmente ou usar scripts SQL
manuais como mecanismo de schema.

### Atores e interesses

- Desenvolvedores de backend precisam executar, testar e evoluir a API com
  dependências reproduzíveis.
- A equipe de arquitetura precisa preservar DDD, Clean Architecture, Code First
  e migrations versionadas.
- A equipe de ambientes precisa manter a mudança limitada ao Nix e sem ativar
  serviços externos.

### Evidências e fatos observados

- `nix/backend.nix` cria o shell `backend` e declara `pkgs.python3` sem módulos
  Python adicionais.
- `docs/fundamentos-backend.md` lista `fastapi`, `uvicorn`, `sqlalchemy`,
  `alembic`, `psycopg` e `pydantic-settings` como dependências iniciais.
- O documento separa DTOs de API, entidades de domínio e mapeamentos de
  persistência, e exclui SQLModel como modelo central.

### Hipóteses

- Os seis pacotes estão disponíveis no conjunto de pacotes Python compatível
  com o `python3` do Nixpkgs fixado pelo projeto.
- Um ambiente construído com `python3.withPackages` disponibiliza os módulos
  para o mesmo interpretador invocado como `python` ou `python3` no shell.

### Perguntas em aberto

- Quais são os atributos exatos de `psycopg` e `pydantic-settings` no Nixpkgs
  fixado; essa confirmação é uma verificação de implementação, não uma mudança
  de decisão.
- O projeto ainda não definiu uma necessidade que justifique driver assíncrono,
  servidor PostgreSQL local, ferramenta de testes ou linter no shell.

### Escopo

- Alterar somente `nix/backend.nix`.
- Substituir o Python isolado por um ambiente derivado de
  `pkgs.python3.withPackages`.
- Incluir FastAPI, Uvicorn, SQLAlchemy, Alembic, Psycopg e Pydantic Settings.
- Preservar `pkgs.git` e o `shellHook` existentes.
- Validar a avaliação do shell e os imports dos módulos incluídos, no ambiente
  Nix de backend.

### Fora do escopo

- Código da API, routers, DTOs, domínio, repositórios, modelos ou migrations.
- Alterações em `flake.nix`, `flake.lock`, manifests Python, Docker, CI/CD ou
  arquivos de testes.
- Instalação de PostgreSQL, criação de banco, ativação de serviço ou conexão a
  banco externo.
- SQLModel, drivers assíncronos, bibliotecas de teste, linters e ferramentas de
  qualidade não listadas no documento principal.
- Instalação global, `pip install`, virtualenv ou gerenciador de dependências
  paralelo ao Nix.

### Critérios de sucesso

- `nix develop .#backend` disponibiliza um interpretador Python com os módulos
  `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`, `psycopg` e
  `pydantic_settings` importáveis.
- O comando `uvicorn` fica disponível no mesmo shell.
- A avaliação do shell Nix passa sem criar ou alterar artefatos não Nix.
- A alteração fica restrita ao ambiente de backend e mantém as escolhas de
  Code First e separação arquitetural descritas no documento principal.

## Restrições aplicáveis

- Ferramentas de desenvolvimento devem usar `nix develop .#backend` para
  atividades de backend.
- A implementação é exclusiva de artefatos Nix e não pode alterar código da
  aplicação, manifests de linguagem ou estado global da máquina.
- A configuração deve usar Nix como fonte de dependências; não deve recorrer a
  instalação imperativa por `pip`, `venv` ou equivalente.
- A alteração não autoriza iniciar ou configurar PostgreSQL, nem gerar ou
  executar migrations.

## Classificação comentada

A esfera é `engineering`, pois a decisão trata da composição reproduzível do
ambiente de desenvolvimento. As preocupações são arquitetura, implementação e
delivery: a seleção deve refletir as fronteiras do backend, tornar as
dependências disponíveis e manter o shell reproduzível. O escopo é de um
componente, o dev shell de backend, e a alteração é facilmente reversível, mas
tem risco médio porque uma dependência ausente ou incompatível bloqueia todo o
fluxo de desenvolvimento.

## Decisão de roteamento

`prompts/ambientes` foi escolhido por ser a subpasta existente mais específica
para uma alteração de ambiente Nix. `prompts/backend` foi considerada porque os
pacotes atendem ao backend, mas descreve com menor precisão o artefato que a
próxima skill pode modificar.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Reprodutibilidade | Alta | Maximizar | O ambiente deve ser declarado e não depender de instalação global. |
| Separação arquitetural | Alta | Satisfazer | A configuração não pode introduzir SQLModel ou misturar código de aplicação e ambiente. |
| Simplicidade | Alta | Priorizar | O primeiro shell deve conter somente as dependências explicitamente decididas. |
| Operabilidade | Média | Satisfazer | Imports e o servidor ASGI devem estar disponíveis no shell. |
| Evolutividade | Média | Priorizar | Novas dependências podem ser adicionadas de forma explícita quando houver decisão posterior. |

## Alternativas consideradas

### Alternativa A — Manter somente `pkgs.python3`

Preserva o shell atual e delega bibliotecas a instalação posterior fora do Nix.
É incompatível com a exigência de controlar dependências pelo Nix e não permite
executar a base técnica documentada.

### Alternativa B — Declarar os módulos Python como pacotes isolados em `mkShell`

Adiciona cada derivação Python diretamente à lista de `packages`. Pode expor
executáveis, mas não garante que o `python3` selecionado no shell seja o mesmo
interpretador com todos os módulos no `PYTHONPATH`. Aumenta a ambiguidade do
ambiente.

### Alternativa C — Usar `pkgs.python3.withPackages` no shell de backend

Cria um único interpretador com FastAPI, Uvicorn, SQLAlchemy, Alembic, Psycopg
e Pydantic Settings. Preserva `git`, limita a alteração ao Nix e torna os
imports esperados verificáveis. É a alternativa recomendada.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Reprodutibilidade | Alta | -2 | +1 | +2 | Alta | Regra raiz e composição declarativa do Nix |
| Separação arquitetural | Alta | -1 | +1 | +2 | Alta | Escopo Nix e documento principal |
| Simplicidade | Alta | +1 | 0 | +2 | Média | Um único interpretador elimina ambiguidade de módulos |
| Operabilidade | Média | -2 | 0 | +2 | Média | Imports e CLI disponíveis no ambiente composto |
| Evolutividade | Média | -1 | +1 | +2 | Média | Lista explícita e revisável de dependências |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### Decisão recomendada nesta versão

Usar a Alternativa C. A skill `$nix-environment-implementation-v1` deve
modificar exclusivamente `nix/backend.nix` para manter `pkgs.git` e substituir
`pkgs.python3` por um ambiente `pkgs.python3.withPackages` que inclua:

- `fastapi`;
- `uvicorn`;
- `sqlalchemy`;
- `alembic`;
- `psycopg`;
- `pydantic-settings`.

Antes da escrita, a skill deve confirmar no Nixpkgs do projeto os atributos
exatos e compatíveis desses pacotes. Se algum não existir ou não puder ser
composto com o interpretador selecionado, ela deve parar e registrar a
evidência, sem substituir silenciosamente por SQLModel, `pip`, virtualenv ou
outro pacote.

### Impacto da revisão

Análise inicial; nenhum impacto de revisão.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Reprodutibilidade | maximized | Dependências entram pelo Nix e acompanham o dev shell | Regra raiz e `withPackages` |
| Simplicidade | prioritized | Um único interpretador Python contém módulos e executáveis necessários | Hipótese a validar por imports e `uvicorn` |
| Evolutividade | prioritized | A lista de pacotes pode evoluir por decisão explícita | Estrutura atual de `nix/backend.nix` |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Separação arquitetural | Somente configuração Nix muda | O alvo é exclusivamente `nix/backend.nix` |
| Operabilidade | Módulos e `uvicorn` importáveis/executável disponível | A validação exigirá imports e descoberta do comando no shell |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Reprodutibilidade | Cada desenvolvedor instala bibliotecas de forma diferente ou global | Alta | Equipe de backend e CI futura |
| Operabilidade | Não é possível iniciar nem validar a base da API no shell oficial | Alta | Desenvolvedores de backend |
| Separação arquitetural | Uma solução simplificada mistura modelos de API, domínio e persistência | Média | Manutenibilidade do backend |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Reprodutibilidade | Avaliação inicial do Nix pode baixar ou construir dependências | Time-to-value | Aceitável para um ambiente declarativo e repetível |
| Simplicidade | Não incluir ainda drivers assíncronos, PostgreSQL local ou ferramentas extras | Optionality | Aceitável até haver necessidade aprovada |
| Separação arquitetural | Não adotar SQLModel para reduzir boilerplate inicial | Delivery-speed | Aceitável para preservar DDD e Clean Architecture |

## Riscos e efeitos de segunda ordem

- Atributos de pacotes podem diferir entre revisões do Nixpkgs; confirmar antes
  de editar reduz o risco de um shell não avaliável.
- `psycopg` pode exigir consideração adicional de bibliotecas nativas conforme
  a variante fornecida pelo Nixpkgs; não adicionar bibliotecas do sistema sem
  evidência de falha ou requisito.
- A presença de bibliotecas no shell não autoriza criar a API, iniciar banco ou
  executar migrations; essas atividades exigem análises e skills apropriadas.
- Um servidor PostgreSQL local pode ser necessário no futuro, mas adicioná-lo
  agora ampliaria escopo e não é requisito do documento analisado.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Pacotes existem no Nixpkgs do projeto | Avaliação dos atributos no flake atual | Inspeção/eval Nix antes da escrita | Algum atributo ausente ou incompatível |
| Interpretador contém os módulos | Imports dos seis módulos no `nix develop .#backend` | Comando Python pontual no shell | `ModuleNotFoundError` ou interpretador divergente |
| Uvicorn está disponível | Localização e execução de versão do CLI no shell | `uvicorn --version` | Comando ausente ou dependência quebrada |
| Mudança permanece Nix-only | Diff restrito a `nix/backend.nix` | Revisão de diff | Qualquer arquivo não Nix alterado |

## Handoffs e atividades posteriores

- `$nix-environment-implementation-v1`: implementar exclusivamente a alteração
  do dev shell definida nesta análise.
- `$backend-domain-orchestration-v2`: criar domínio, casos de uso e portas após
  uma análise específica de comportamento de negócio.
- `$backend-adapters-drivers-v2`: implementar API FastAPI, persistência
  SQLAlchemy, repositórios concretos e migrations após análise específica.
- `$integration-system-testing-v1`: definir testes de integração de API,
  PostgreSQL e migrations quando houver cenários e oráculos aprovados.

## Síntese

O shell de backend atual contém apenas Python e Git, enquanto o documento
principal define uma base REST síncrona com FastAPI, SQLAlchemy, Alembic,
Psycopg e Pydantic Settings. A alternativa recomendada é compor um único
interpretador `python3.withPackages` em `nix/backend.nix`, preservando Git e
mantendo toda a mudança sob Nix. A análise não autoriza implementação de API,
schema, banco ou migrations; ela autoriza somente a próxima skill Nix a validar
os atributos e alterar o dev shell.
