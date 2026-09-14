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
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1688619b8cad70805a28397dd30c9b2968a3b1fc"
      availability: available
    - path: nix/backend.nix
      relationship: supporting
      representation: source-code
      function: configuration
      format: nix
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 1688619b8cad70805a28397dd30c9b2968a3b1fc"
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
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/ambientes]
  confidence: high
  rationale: "A decisão produz a base de interface HTTP do backend; o ambiente Nix é somente evidência de disponibilidade do framework."
classification:
  sphere: engineering
  concerns: [architecture, implementation, integration]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: low
  reversibility: easy
  risk: low
---

# Análise de decisão — fundamentos mínimos do FastAPI

## Solicitação original

`$decision-analysis-v4 Agora com base no documento 'docs\fundamentos-backend.md', faça uma análise para implementação de um base mínina FastApi. Não quero domain, use case, nem rota. Quero apenas o fundamento inicial FastApi onde depois serão adicionados de forma composável os outros componentes.`

## Informações complementares

- O documento principal estabelece FastAPI como interface HTTP e determina
  Clean Architecture, DDD e composição de dependências na camada mais externa.
- `src/backend` contém somente suas instruções arquiteturais; não há aplicação,
  pacote Python, endpoint, entidade, caso de uso ou repositório existente.
- O dev shell de backend, no working tree, já declara FastAPI e Uvicorn sob
  Nix, mas essa análise não autoriza nova alteração de ambiente.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem | Nenhum identificado | v001 inicial | Não há análise anterior para o alicerce FastAPI | Nenhum histórico a preservar |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `docs/fundamentos-backend.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree baseado em `1688619` |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução para agentes | Markdown | Arquivo completo | Commit `1688619` |
| `nix/backend.nix` | Apoio | Código-fonte | Configuração | Nix | Arquivo completo | Working tree baseado em `1688619` |
| `prompts/README.md` | Contexto | Prosa | Documentação | Markdown | Arquivo completo | Commit `1688619` |
| `AGENTS.md` | Contexto | Prosa | Instrução para agentes | Markdown | Arquivo completo | Commit `1688619` |

### Limites da evidência dos artefatos

O documento principal e o dev shell Nix estão no working tree e ainda não foram
versionados nesta branch. A estrutura de `src/backend` foi examinada somente
como baseline: ela contém `AGENTS.md`, sem código de aplicação ou convenções de
pacotes e testes. Não há requisitos de negócio que justifiquem criar domínio,
caso de uso, rota ou contrato HTTP nesta etapa.

## Problema enriquecido

### Resultado desejado

Criar uma base mínima, importável e executável de FastAPI em `src/backend`, com
uma fábrica de aplicação e um ponto de entrada ASGI. A base deve permitir que
routers, injeção de dependências e componentes de domínio sejam compostos no
futuro, sem antecipar suas implementações agora.

### Atores e interesses

- Desenvolvedores de backend precisam de um ponto estável para iniciar a API e
  adicionar adapters de transporte posteriormente.
- A equipe de arquitetura precisa manter FastAPI na borda, sem dependência do
  domínio ou da aplicação em relação ao framework.
- A equipe de testes precisa de uma fábrica que permita obter uma aplicação em
  isolamento, sem iniciar servidor ou recursos externos.

### Evidências e fatos observados

- O documento define FastAPI como interface HTTP e Uvicorn como servidor ASGI.
- As regras de backend exigem que composição e injeção ocorram na camada mais
  externa e proíbem regra de negócio em controllers ou adaptadores.
- Não há código em `src/backend` além das regras locais.
- O ambiente Nix atual já disponibiliza FastAPI e Uvicorn para o backend.

### Hipóteses

- Um módulo de fábrica de aplicação é suficiente para estabelecer a composição
  inicial sem registrar endpoint, middleware ou dependência de negócio.
- Um módulo de entrada que exponha uma instância criada pela fábrica permite
  execução futura por Uvicorn sem determinar ainda uma estratégia de deploy.

### Perguntas em aberto

- Nome público, versão, documentação OpenAPI, prefixos de rota e configurações
  de CORS ainda não foram decididos; não devem ser inventados nesta etapa.
- A convenção exata de descoberta de testes Python ainda não existe. O teste
  unitário deve seguir uma estrutura mínima compatível com a linguagem e o
  ambiente existente, sem introduzir runner ou dependência nova.

### Escopo

- Criar um pacote Python de interface/API sob `src/backend`.
- Criar uma função de fábrica `create_app` que devolva uma instância de
  `FastAPI` sem efeitos externos.
- Criar um módulo de entrada ASGI que exponha a aplicação criada pela fábrica.
- Incluir somente metadados neutros e necessários da aplicação, sem representar
  requisito de negócio ou contrato funcional.
- Criar e executar um teste unitário isolado para a fábrica, no ambiente
  `nix develop .#backend`.
- Documentar a função criada conforme as regras de docstring aplicáveis.

### Fora do escopo

- Entidades, value objects, agregados, regras de domínio, casos de uso, portas,
  repositórios, ORM, banco de dados, migrations e configurações de Psycopg.
- Routers, endpoints, decorators de operação, rotas de saúde, DTOs HTTP,
  autenticação, autorização, CORS, middleware, logging, métricas ou tracing.
- Dependências externas, configurações de ambiente, Pydantic Settings, arquivos
  `.env`, Docker, CI/CD, Nix, manifests de Python ou execução de Uvicorn.
- Testes de integração, API, contrato, sistema ou E2E.

### Critérios de sucesso

- O módulo de fábrica pode ser importado no ambiente de backend e retorna uma
  instância de `FastAPI`.
- O módulo de entrada ASGI expõe a instância criada pela fábrica.
- A aplicação criada não registra rotas, não abre conexões e não inicializa
  recursos externos.
- A função possui docstring que explica o que faz, como cria a base e por que
  existe.
- O diff fica restrito à fundação de interface FastAPI e ao teste unitário
  correspondente, sem modificar ambiente ou componentes de domínio.

## Restrições aplicáveis

- FastAPI deve permanecer na camada Interface/API; domínio e aplicação não
  podem depender do framework.
- A composição deve ocorrer na camada mais externa, mas não pode antecipar
  dependências que ainda não existem.
- Toda função criada deve ter documentação que cubra responsabilidade, abordagem
  e finalidade.
- Testes unitários do backend devem usar o ambiente `backend` e não devem
  iniciar servidor, rede, banco, filesystem, container ou framework externo.
- A alteração deve incluir a proveniência da análise em comentário compatível
  com Python, conforme a skill de implementação aplicável.

## Classificação comentada

Trata-se de uma decisão de engenharia sobre a base de composição da interface
HTTP do backend. As preocupações são arquitetura, implementação e integração:
o framework deve ser isolado na borda, a fundação precisa ser pequena e a
entrada ASGI deve integrar-se ao servidor posteriormente. O risco é baixo e a
alteração é facilmente reversível porque não cria contrato HTTP nem estado
persistente.

## Decisão de roteamento

`prompts/backend` é a pasta mais específica para um alicerce de código servidor
e interface API. `prompts/ambientes` foi considerada porque FastAPI está
disponível pelo dev shell, mas a análise não altera Nix nem outra configuração
de ambiente.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Simplicidade | Alta | Maximizar | A fundação deve conter apenas composição e entrada ASGI. |
| Modificabilidade | Alta | Maximizar | Novos routers e dependências devem poder ser conectados sem reestruturar a base. |
| Separação arquitetural | Alta | Satisfazer | FastAPI deve ficar limitado à interface externa. |
| Testabilidade | Média | Satisfazer | A fábrica deve poder ser validada sem executar servidor. |
| Time-to-value | Média | Priorizar | A aplicação deve se tornar importável com o menor conjunto de arquivos. |

## Alternativas consideradas

### Alternativa A — Instância global única em um arquivo `main.py`

Criar diretamente `app = FastAPI()` em um único módulo. É a menor quantidade de
código, mas dificulta variar ou compor a construção da aplicação para testes,
routers e dependências futuras sem alterar o ponto de entrada.

### Alternativa B — Fábrica de aplicação e entrada ASGI separada

Criar uma função `create_app` em módulo de interface e um módulo de entrada que
exponha `app = create_app()`. Mantém a inicialização sem efeitos externos,
permite composição posterior no ponto mais externo e permanece pequeno. É a
alternativa recomendada.

### Alternativa C — Fundação com endpoint de saúde e configuração inicial

Criar fábrica, entrada, rota de health check, configurações e middleware para provar a
aplicação em execução. Viola a restrição explícita de não criar rota e antecipa
contratos, políticas e componentes ainda não decididos.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Simplicidade | Alta | +2 | +1 | -1 | Alta | Escopo explícito do usuário |
| Modificabilidade | Alta | 0 | +2 | +1 | Alta | Fábrica separa construção e entrada |
| Separação arquitetural | Alta | +1 | +2 | -1 | Alta | Regras de Clean Architecture |
| Testabilidade | Média | +1 | +2 | 0 | Média | Fábrica pode ser exercitada sem servidor |
| Time-to-value | Média | +2 | +1 | 0 | Média | Menos arquivos versus base extensível |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### Decisão recomendada nesta versão

Usar a Alternativa B. A implementação deve criar a menor estrutura de pacote
necessária em `src/backend` para:

1. definir `create_app`, uma fábrica sem argumentos e sem efeitos externos que
   instancia e retorna `FastAPI`;
2. expor `app = create_app()` em um módulo de entrada ASGI apropriado para uso
   futuro por Uvicorn;
3. testar unitariamente a fábrica, sem iniciar Uvicorn ou acessar rede;
4. inserir o comentário de proveniência com
   `prompts/backend/20260913-fundamentos-fastapi-v001.md#v001` nos arquivos de
   código criados.

Os metadados da instância devem permanecer neutros. Não criar `include_router`,
`@app.get`, `@app.post`, `lifespan`, middleware, configuração, modelos, portas
ou injeção de dependência até que exista uma análise que os justifique.

### Impacto da revisão

Análise inicial; nenhum impacto de revisão.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Simplicidade | maximized | Apenas fábrica, entrada e teste unitário são adicionados | Escopo explicitamente limitado |
| Modificabilidade | maximized | Routers e dependências podem ser compostos no futuro na fábrica | Separação entre construção e ASGI |
| Time-to-value | prioritized | Há um objeto ASGI importável sem implementar funcionalidade | FastAPI disponível no dev shell |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Separação arquitetural | Nenhuma regra de domínio ou infraestrutura no FastAPI | Escopo proíbe componentes internos e persistência |
| Testabilidade | Fábrica validável sem servidor ou recursos externos | Teste unitário chama somente `create_app` |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Modificabilidade | A entrada global torna a composição futura mais acoplada | Média | Desenvolvedores de backend |
| Separação arquitetural | Regras ou contratos entram na camada HTTP antes de existirem componentes internos | Alta | Manutenibilidade do backend |
| Testabilidade | A inicialização passa a exigir servidor ou recursos externos | Média | Equipe de testes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Modificabilidade | Um módulo adicional para a fábrica | Simplicidade | Aceitável, pois evita reestruturação posterior |
| Separação arquitetural | Não expor endpoint que demonstre a aplicação por HTTP | Time-to-value | Aceitável, pois rotas estão explicitamente fora do escopo |
| Testabilidade | Não testar servidor ASGI nesta etapa | Cobertura de integração | Aceitável até haver contrato HTTP aprovado |

## Riscos e efeitos de segunda ordem

- Adicionar metadados de produto, CORS, middleware ou configuração por
  conveniência criaria decisões e políticas não aprovadas.
- Uma rota de health check aparentemente inofensiva ainda cria contrato HTTP e deve
  aguardar análise própria.
- A falta de convenção de testes pode induzir inclusão de dependência ou runner;
  a implementação deve usar a menor opção já disponível e registrar bloqueio se
  não for possível testar sem ampliar o ambiente.
- A aplicação importável não prova disponibilidade de rede, banco, rotas ou
  deploy; esses aspectos permanecem fora desta análise.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Fábrica retorna aplicação FastAPI | Asserção de tipo ou identidade em teste unitário | Executar teste no ambiente `.#backend` | Importação ou construção falha |
| Entrada expõe a instância composta | Importação do módulo de entrada e comparação com instância FastAPI | Teste unitário sem Uvicorn | Entrada inicia efeito externo ou não expõe `app` |
| Não há contrato HTTP antecipado | Ausência de operações de rota e routers no diff | Revisão de diff | Decorator de rota, router ou middleware aparece |
| Mudança preserva fronteiras | Arquivos somente na interface e teste unitário | Revisão de diff e instruções aplicáveis | Domínio, aplicação, persistência ou configuração externa muda |

## Handoffs e atividades posteriores

- `$backend-adapters-drivers-v2`: implementar a fábrica, a entrada ASGI e seu
  teste unitário, desde que o gate confirme que a fundação sem contratos
  internos é uma responsabilidade externa elegível.
- `$backend-domain-orchestration-v2`: introduzir domínio, casos de uso e portas
  somente a partir de uma análise de comportamento de negócio.
- `$backend-adapters-drivers-v2`: adicionar routers, DTOs de transporte,
  repositórios concretos, SQLAlchemy e migrations somente quando os contratos
  internos necessários existirem.
- `$cross-cutting-implementation-v1`: tratar CORS, logging, telemetria,
  autenticação, autorização e resiliência após decisão específica.
- `$integration-system-testing-v1`: criar testes de API ou integração após a
  definição de rotas e contratos observáveis.

## Síntese

O backend não contém código de aplicação, mas o ambiente Nix já disponibiliza
FastAPI e Uvicorn. A base mínima recomendada é uma fábrica `create_app` e um
ponto de entrada ASGI que expõe a instância criada, acompanhados de teste
unitário. Essa escolha permite composição futura na borda e não antecipa
domínio, caso de uso, rota, persistência, configuração ou preocupação
transversal.
