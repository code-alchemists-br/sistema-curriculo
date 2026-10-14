---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v003"
status: pending
created_at: "2026-10-12T23:22:54-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261012-230050-expor-consulta-dados-pessoais-estudante-v001.md
  supersedes: prompts/backend/20261012-230726-expor-consulta-dados-pessoais-estudante-v002.md
  change_type: enrichment
  secondary_change_types: []
  decision_impact: unchanged
subjects:
  kind: mixed
  files:
    - path: "Solicitação do usuário: card Expor consulta de dados pessoais do estudante"
      relationship: primary
      representation: prose
      function: documentation
      format: text
      analysis_scope: whole-file
      locator: null
      content_state: external
      revision: null
      availability: available
    - path: prompts/backend/20261012-230726-expor-consulta-dados-pessoais-estudante-v002.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 530e8f6"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF02 e RF13"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: docs/matriz_testes.md
      relationship: supporting
      representation: prose
      function: test
      format: Markdown
      analysis_scope: selected-section
      locator: "CT-RF02-01 e CT-RF13-01/02"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: docs/mapeamento_jornadas.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "seção 6.3, Dados pessoais e contato"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RNF04 e definições pendentes de autenticação/autorização"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: docs/requisitos-seguranca.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "método/sessão, autorização do usuário comum, propriedade, RF-AUTZ-03/06/07/10 e RF-DADOS-05"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/api/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/api/dados_contato.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/api/cadastro_acesso.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "rotas de cadastro e login"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "injeção e registro dos routers de perfil/dados de contato"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/main.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/application/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/application/dados_contato.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: Python
      analysis_scope: selected-section
      locator: "porta RepositorioUsuario"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/domain/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "campos do agregado Usuario e dados_contato"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/tests/test_api_perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/tests/test_api_dados_contato.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/tests/test_application_perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/tests/test_application_dados_contato.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: src/backend/infrastructure/security/sessoes.py
      relationship: context
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "GerenciadorSessoesSqlAlchemy.obter_usuario"
      content_state: commit
      revision: "0f896f4, branch origin/task94; fora da referência local origin/dev"
      availability: available
    - path: prompts/backend/20261011-102943-rejeicao-requisicoes-sem-credenciais-validas-v004.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "inventário de rotas GET e limitação de autenticação; revalidado no código de 530e8f6"
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
    - path: "Histórico Git: HEAD task88 e origin/main"
      relationship: context
      representation: structured-data
      function: unknown
      format: Git commit metadata
      analysis_scope: selected-section
      locator: "HEAD 530e8f65; origin/main aff3b76; teste de ancestralidade main → HEAD"
      content_state: commit
      revision: "530e8f65fe3f29864d147f95bfc0ee14964ffc74 / aff3b76e8880dc4cd2068d56232ada02a28b6399"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "530e8f6"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "O card trata de expor leitura por API no backend; requisitos de privacidade e segurança são evidências de apoio."
classification:
  sphere: engineering
  concerns: [security, privacy, implementation]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: high
  reversibility: moderate
  risk: high
---

# Análise de decisão — consulta de dados pessoais do estudante

## Solicitação original

`$decision-analysis-v4 Faça uma analise para o card Expor consulta de dados pessoais do estudante. Inclua testes unitarios adequados`

## Informações complementares

Nenhum critério ou identificador do card, contrato HTTP aprovado, lista fechada de campos, responsável por autenticação ou dependência de sessão foi fornecido além da solicitação original.

Solicitação desta revisão, preservada literalmente: `$decision-analysis-v4 Revise prompts/backend/20261012-230050-expor-consulta-dados-pessoais-estudante-v001.md`

Informação posterior, preservada literalmente: `faça um pull da main para trazer as ultimas alterações para essa branch`

Solicitação desta nova revisão, preservada literalmente: `$decision-analysis-v4 Revise novamente prompts/backend/20261012-230050-expor-consulta-dados-pessoais-estudante-v001.md`

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Evidências do repositório | Base `task88` em `530e8f6`; documentos e código usados como apoio | Reconfirmados em `530e8f6`, que coincide com a referência local `origin/dev`; sem diferenças nos arquivos que sustentam a decisão | Reavaliação da linhagem e dos fatos críticos no estado atual | Nenhuma mudança de evidência ou de decisão |
| Dependência de sessão | Implementação identificada em `origin/task94`, commit `0f896f4`, fora da referência local `origin/dev` | Relação de ancestralidade e implementação de resolução de sessão reconfirmadas; ainda não integrada à referência local `origin/dev` | Verificar se a lacuna que bloqueia a consulta foi resolvida | `pending` permanece |
| Decisão e testes | Leitura própria autenticada; testes unitários previstos nas camadas Application, API e persistência | Direção mantida; escopo dos testes esclarecido como unitário com doubles, deixando sessão/HTTP/banco reais para integração | O pedido de revisão não trouxe critérios novos do card | Impacto `unchanged`; sem execução de testes, pois nenhum código foi alterado |
| Histórico de `main` | Não incluído na v002 | `origin/main` em `aff3b76` é ancestral do HEAD `530e8f6` de `task88`; merge fast-forward informou `Already up to date` | Verificar se a atualização solicitada trazia evidência ou código novo para esta análise | Nenhuma alteração de base; incertezas do card permanecem |
| Demais seções decisórias | Problema, restrições, alternativas, perfil de pagamento, perdas, riscos, validação e handoffs descritos na v002 | Reexaminados e mantidos | A verificação de `main` não trouxe novos artefatos de código ou requisitos | Sem mudança de recomendação |
| Classificação e roteamento | `engineering`, com segurança, privacidade e implementação; `prompts/backend` | Mantidos após a reavaliação | A natureza da demanda continua sendo uma consulta de API backend | Nenhuma mudança |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| Solicitação do usuário: card Expor consulta de dados pessoais do estudante | Principal | Prosa | Documentação | Texto | Solicitação integral | Externa, recebida nesta conversa |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Requisitos | Markdown | RF02, RF13 | Commit `530e8f6` |
| `docs/matriz_testes.md` | Apoio | Prosa | Teste | Markdown | CT-RF02-01 e CT-RF13-01/02 | Commit `530e8f6` |
| `docs/mapeamento_jornadas.md` | Apoio | Prosa | Documentação | Markdown | Seção 6.3 | Commit `530e8f6` |
| `docs/requisitos_nao_funcionais.md` | Apoio | Prosa | Requisitos | Markdown | RNF04 e definições pendentes | Commit `530e8f6` |
| `docs/requisitos-seguranca.md` | Apoio | Prosa | Requisitos | Markdown | Sessão, propriedade e autorização | Commit `530e8f6` |
| `src/backend/api/perfil_estudante.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/api/dados_contato.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/api/cadastro_acesso.py` | Apoio | Código-fonte | Produção | Python | Cadastro/login | Commit `530e8f6` |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Injeção e registro de routers | Commit `530e8f6` |
| `src/backend/main.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/application/perfil_estudante.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/application/dados_contato.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/application/ports.py` | Apoio | Código-fonte | Contrato | Python | `RepositorioUsuario` | Commit `530e8f6` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/infrastructure/persistence/sqlalchemy/usuario.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/domain/usuario.py` | Apoio | Código-fonte | Produção | Python | Campos do agregado e contato | Commit `530e8f6` |
| `src/backend/tests/test_api_perfil_estudante.py` | Apoio | Código-fonte | Teste | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/tests/test_api_dados_contato.py` | Apoio | Código-fonte | Teste | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/tests/test_application_perfil_estudante.py` | Apoio | Código-fonte | Teste | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/tests/test_application_dados_contato.py` | Apoio | Código-fonte | Teste | Python | Arquivo completo | Commit `530e8f6` |
| `src/backend/infrastructure/security/sessoes.py` | Contexto | Código-fonte | Produção | Python | Resolução de sessão | Commit `0f896f4` em `origin/task94`, fora da referência local `origin/dev` |
| `prompts/backend/20261011-102943-rejeicao-requisicoes-sem-credenciais-validas-v004.md` | Contexto | Prosa | Documentação | Markdown | Inventário e lacuna de leitura/autenticação | Commit `530e8f6`; conclusões cotejadas com código atual |
| `AGENTS.md` e `src/backend/AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Arquivos completos | Commit `530e8f6` |
| `prompts/backend/20261012-230726-expor-consulta-dados-pessoais-estudante-v002.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree baseado em `530e8f6` |
| Histórico Git: `task88` / `origin/main` | Contexto | Dados estruturados | Metadados Git | Git | Ancestralidade entre `aff3b76` e `530e8f6` | Referências remotas consultadas nesta revisão |

### Limites da evidência dos artefatos

O código examinado pertence à base de `task88`, commit `530e8f6`, igual à referência local `origin/dev`. `origin/main`, commit `aff3b76`, é ancestral desse HEAD, então a solicitação de atualizar `task88` a partir de `main` não trouxe commits novos; os artefatos de código e requisitos continuam no mesmo estado. A referência remota de `dev` não foi atualizada nesta revisão, portanto essa igualdade descreve apenas a referência local. O working tree contém v001 e v002 como arquivos de análise não rastreados. A implementação de sessão examinada está em `origin/task94`, commit `0f896f4`, e não é ancestral da referência local `origin/dev`; portanto ela é uma alternativa de dependência, não capacidade disponível nesta base. Nenhum identificador ou texto integral do card foi fornecido.

## Problema enriquecido

### Resultado desejado

Permitir que um estudante consulte, por API, seus próprios dados pessoais persistidos, com resposta limitada aos campos definidos para o card e sem expor credenciais ou dados de outra conta.

### Atores e interesses

- Estudante: recuperar os dados previamente cadastrados para conferência e continuidade do preenchimento.
- API: traduzir a requisição autenticada para uma consulta e devolver DTO explícito.
- Segurança: permitir leitura somente do proprietário autenticado e negar por padrão.
- Backend/persistência: consultar e reconstruir os dados duráveis sem vazar modelo ORM ou hash de senha.
- Produto/gestão: definir quais campos o card chama de dados pessoais e como se relaciona às seções de contato e às demais informações.

### Evidências e fatos observados

- RF02 requer consulta, edição e exclusão de informações cadastradas; CT-RF02-01 espera exibir informações cadastradas, mas agrega dados pessoais, formação, experiência e competência.
- A jornada da seção 6.3 agrupa nome, e-mail, telefone, cidade e meios profissionais de contato sob “dados pessoais e contato”.
- RF13 exige autenticação para acesso a dados pessoais e currículos. O RNF04 e os requisitos de autorização restringem o acesso aos recursos próprios e proíbem confiar somente no identificador enviado pelo cliente.
- `perfil_estudante.py` expõe PUT e DELETE, sem GET. `dados_contato.py` expõe PUT, sem GET. A única rota GET observada no backend é a listagem de versões de currículo.
- Não existe caso de uso de consulta de perfil/dados pessoais em `application/perfil_estudante.py`; há casos de uso de edição, exclusão e atualização de contato.
- A porta `RepositorioUsuario` declara `obter_por_id`, mas `RepositorioUsuarioSqlAlchemy` não implementa esse método. O modelo SQLAlchemy de usuário guarda id, nome, e-mail e hash; não mapeia os campos de contato presentes no agregado.
- O login da base `task88` valida credenciais sem estabelecer sessão. A fábrica registra executores opcionais e a aplicação padrão não compõe um principal autenticado para leitura.
- Uma implementação de sessão existe em `origin/task94`, mas essa referência não integra a referência local `origin/dev` examinada.
- `origin/main` no commit `aff3b76` é ancestral de `task88` no commit `530e8f6`; a atualização solicitada não acrescenta commits à branch nem altera as evidências de código e requisitos desta análise.
- Os testes existentes cobrem edição e contato com doubles; não há teste unitário de consulta desses dados.

### Hipóteses

- A consulta é somente leitura e não deve alterar o agregado nem registrar uma nova versão dos dados.
- “Dados pessoais” inclui ao menos nome e e-mail; pode também incluir endereço/cidade, telefones e links profissionais, conforme a jornada 6.3.
- Formação, experiência, competências e currículos continuam em consultas próprias, fora desta fatia.
- O usuário comum consulta somente os dados da própria conta; não há requisito fornecido para busca por terceiros ou acesso administrativo.
- O endpoint deve derivar o proprietário da identidade autenticada, mesmo que a convenção HTTP atual use `usuario_id` no caminho para operações de escrita.

### Perguntas em aberto

- O card cobre somente nome/e-mail, ou também os campos de contato (endereço/cidade, telefones, LinkedIn e Lattes)?
- O card inclui a persistência dos campos de contato, que hoje não estão no modelo SQLAlchemy, ou depende de outra entrega?
- O card depende da sessão disponível em outra branch/atividade ou inclui a integração da identidade autenticada? Qual é o contrato de principal já aceito para a base `dev`?
- A consulta deve usar identidade implícita do usuário (`/estudantes/me`) ou manter um identificador explícito e verificar propriedade no servidor?
- Qual resposta HTTP é esperada para perfil inexistente ou excluído, e o comportamento deve evitar revelar a existência de contas?

### Escopo

- Definir consulta somente leitura do perfil pessoal autenticado.
- Delimitar o conjunto de campos da resposta, sem credenciais, hash, dados de sessão ou informações de outros estudantes.
- Reutilizar contratos internos existentes quando suficientes; identificar a necessidade de caso de uso ou adapter faltante sem implementá-los nesta análise.
- Especificar testes unitários pertinentes para Application, interface HTTP e repository adapter, cada qual isolado por doubles.

### Fora do escopo

- Consultar ou consolidar currículos, formação acadêmica, experiências, competências ou projetos.
- Editar ou excluir dados pessoais.
- Criar política administrativa, mecanismo de autenticação ou armazenamento de sessão dentro do card sem aceite explícito.
- Testes com servidor ASGI e banco reais, que pertencem à atividade de integração.
- Inventar códigos HTTP ou contratos de campos enquanto o card não os confirmar.

### Critérios de sucesso

- A resposta representa exatamente o conjunto de campos aceito para o card e não inclui hash de senha, segredo de sessão ou modelo ORM.
- A identidade da consulta vem do principal autenticado; um usuário não consegue selecionar outra conta pelo path, query ou corpo.
- Perfil inexistente/excluído segue o comportamento HTTP e de privacidade definido pelo contrato.
- A leitura é sem efeito colateral e consulta os valores persistidos atuais.
- Testes unitários cobrem caminho encontrado, ausência/estado excluído conforme decisão, mapeamento do DTO, delegação ao caso de uso e consulta do adapter com ORM substituído.
- Testes integrados validam sessão, HTTP e banco em atividade separada; não são substituídos por testes unitários.

## Restrições aplicáveis

- RF13 exige autenticação; RNF04 e requisitos de autorização limitam leitura aos dados autorizados e do próprio estudante.
- Não confiar somente em ID fornecido pelo cliente; a verificação ocorre no backend e adota negação por padrão.
- Domínio/Application não dependem de FastAPI, SQLAlchemy ou transporte. Entidades não são respostas HTTP.
- Persistência relacional segue Code First/Alembic; dados que não estejam persistidos não podem ser apresentados como consulta durável.
- Novas funções, classes e DTOs devem documentar responsabilidade, abordagem e finalidade.
- Testes unitários backend usam `nix develop .#backend`; integração usa `nix develop .#tests`.

## Classificação comentada

`engineering` domina: trata-se da entrega de leitura por API e das dependências de consulta. `security`, `privacy` e `implementation` são as preocupações principais porque a rota exporia dados pessoais e hoje não há sessão composta nesta base. A incerteza é alta por falta de lista de campos e dependência de autenticação; o risco é alto porque erro de propriedade divulga informações privadas.

## Decisão de roteamento

Destino `prompts/backend`: a finalidade principal é especificar um card de API/backend. `prompts/requisitos` foi considerada pela dúvida sobre os campos e `prompts/revisao` por existir uma análise relacionada à lacuna de leitura, mas nenhuma altera que esta é uma decisão de entrega técnica nova.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Security | Muito alta | Consultar apenas a conta vinculada ao principal autenticado | Evita IDOR e divulgação entre estudantes |
| Privacy | Muito alta | Resposta mínima e sem credenciais/atributos internos | Dados pessoais não devem vazar por serialização ampla |
| Correctness | Alta | Ler estado persistido e representar somente campos acordados | Evita consulta incompleta ou dados não duráveis |
| Simplicity | Média | Evitar um endpoint agregador de todo o currículo nesta task | Mantém a rota e os testes focados |

## Alternativas consideradas

### A — Consulta autenticada do perfil básico (nome e e-mail)

Criar consulta somente leitura para o principal autenticado e retornar nome/e-mail. Contato permanece fora desta resposta até existir armazenamento e aceite. É a menor fatia implementável com a tabela atual, mas pode não satisfazer a expectativa da jornada 6.3.

### B — Consulta autenticada de dados pessoais e contato

Retornar nome, e-mail e campos de contato definidos pela jornada 6.3; exigir que eles estejam mapeados e persistidos antes de declarar a leitura completa. É a alternativa que melhor corresponde ao título e à jornada, mas a persistência atual de contato está incompleta e o card não confirma a lista de campos.

### C — GET por `usuario_id` explícito com autorização de propriedade

Manter o estilo de caminho existente, mas validar no servidor que o usuário autenticado pode ler aquele ID. É viável se clientes precisarem consultar contas específicas; para o estudante consultar os próprios dados, expõe identificador sem necessidade e aumenta a superfície de autorização.

### D — Agregar todos os dados do estudante em uma única resposta

Incluir contato, formação, experiência, competências e currículos no mesmo GET. Não é recomendada para este card: o CT-RF02-01 é amplo, porém o título não aprova um agregador, e isso mistura recursos e contratos distintos.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | A | B | C | D | Confiança | Base |
|---|---:|---:|---:|---:|---:|---|---|
| Security | Muito alta | +2 | +2 | +1 | +1 | Alta | A/B usam principal; C depende de checagem de propriedade; todas exigem auth |
| Privacy | Muito alta | +2 | +1 | +1 | -2 | Média | A minimiza campos; B amplia conteúdo; D aumenta exposição |
| User-value | Alta | +1 | +2 | +1 | +2 | Média | Jornada 6.3 agrupa dados pessoais e contato; D excede o card |
| Correctness | Alta | +2 | +1 | +1 | -1 | Média | A usa campos hoje persistidos; B requer persistência de contato ainda ausente |
| Simplicity | Média | +2 | +1 | -1 | -2 | Alta | Consulta própria sem ID é mais simples que autorizar recursos arbitrários |

Os valores são ordinais e não são somados. A e B são alternativas viáveis somente com autenticação; B requer completar antes a disponibilidade durável dos campos de contato.

## Histórico e decisão atual

### Decisão da versão anterior

A v002 manteve a recomendação de consulta explícita e somente leitura do perfil do próprio estudante, associada ao principal autenticado, sem aceitar identidade arbitrária e sem agregar formação, experiência, competências ou currículos. Manteve `pending` até haver definição dos campos e da dependência de autenticação disponível na base de integração.

### Decisão recomendada nesta versão

Direção recomendada: consulta de perfil próprio, sem `usuario_id` escolhido pelo cliente, baseada em principal autenticado; não criar leitura sem autenticação. Preferir cobrir nome, e-mail e contato se o card confirmar a lista e a persistência for disponibilizada. Caso o card restrinja a fatia aos campos atualmente persistidos, a alternativa A é a entrega mínima. Não incluir formação, experiência, competências ou currículos.

A decisão permanece `pending`: a lista de campos altera o modelo de leitura e os requisitos do adapter, e a sessão disponível em outra branch ainda não integra a referência local `origin/dev`. O desbloqueio mínimo é obter os critérios de aceite do card com a lista de campos e identificar qual dependência autenticada será integrada à base de entrega. Até isso ocorrer, as alternativas A e B são recortes condicionais, não contrato aprovado.

### Impacto da revisão

`unchanged`: os requisitos e códigos relevantes continuam no commit `530e8f6`; a referência atual de `main` (`aff3b76`) já é ancestral dele e, portanto, não trouxe mudanças para reavaliar. O usuário não acrescentou critérios de aceite nem removeu as incertezas que impedem fechar o contrato; a recomendação e o status `pending` não mudam. Esta revisão não altera a análise contextual sobre rejeição de credenciais, que permanece fora desta linhagem.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Security | prioritized | Leitura sempre limitada ao principal autenticado | RF13, RNF04 e propriedade da conta descrita nos requisitos de segurança |
| Privacy | prioritized | DTO explícito e mínimo, sem hash/token | Tabela de usuário inclui hash e não deve ser serializada |
| Correctness | prioritized | Resposta baseada no armazenamento realmente disponível | Código ORM atual persiste nome/e-mail, mas não contato |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Simplicity | Não agregar todos os dados do currículo nesta rota | Manter formação, experiência, competência e currículo fora da consulta pessoal |
| Reversibility | Não fixar rota ou payload antes do contrato mínimo | Escolher `/me` ou caminho específico na implementação após aceite do card |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Security | Usuário lê dados de outra conta ou acesso anônimo obtém perfil | Alta | Estudantes e operação |
| Privacy | Hash, sessão ou campos fora do propósito aparecem no payload | Alta | Estudantes |
| User-value | Consulta omite contato que a tela de dados pessoais espera | Média | Estudantes e frontend |
| Correctness | API apresenta contato não persistido ou desatualizado como fonte canônica | Alta | Estudantes e produto |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Security | Esperar a sessão/principal estar integrado e testar propriedade | Delivery-speed | Necessário por RF13 e RNF04 |
| Privacy | Definir lista de campos e DTO explícito | Flexibilidade imediata do payload | Aceitável para evitar serialização ampla |
| Correctness | Completar persistência de contato se incluída | Simplicity e velocidade | Aceitável somente se o card incluir esses campos |

## Riscos e efeitos de segunda ordem

- Um GET que aceite `usuario_id` sem verificação de propriedade cria risco de acesso horizontal entre contas.
- A sessão no commit `0f896f4` está em branch separada; depender dela sem integração/contrato aceito deixa a rota sem identidade autenticada na base de `task88`.
- O modelo ORM atual contém hash de senha; devolver o agregado inteiro em `response_model` ou serialização implícita pode expor credencial derivada.
- O agregado possui `dados_contato`, mas o mapper/modelo SQLAlchemy não persiste esses campos; uma leitura pode aparentar funcionar em memória e falhar após novo carregamento.
- CT-RF02-01 inclui também formação, experiência e competência; usar esse critério como exigência do card pode expandir a task indevidamente.
- A resposta após exclusão lógica e o código HTTP para ausência ainda não foram definidos para esta consulta.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Campos da consulta estão definidos | Critério de aceite/campos do card confirmados | Revisão de produto e comparação com jornada 6.3 | Produto espera contato ou seções que não estejam no DTO proposto |
| Principal autenticado está disponível na base | Contrato de sessão integrado e composição em `dev` | Inspeção da dependência e teste unitário do handler | Handler recebe ID arbitrário ou sessão ainda não integrada |
| Consulta lê somente perfil próprio | Teste de identidade/propriedade e resposta de conta alheia negada | Teste unitário para mapeamento; integração para autorização real | Um usuário obtém dados de outro ID |
| Dados retornados são duráveis | Mapeamento e query do repository cobrem os campos aceitos | Testes unitários do adapter e integração com banco | Campo existe apenas no agregado em memória |
| Contrato atende RF02 sem ampliar o card | Critérios do card relacionam a rota à fatia de dados pessoais | Revisão de produto/gestão | Esperança de resposta completa de formação, experiência ou competência |

## Handoffs e atividades posteriores

- Produto/gestão: confirmar se o escopo é nome/e-mail ou nome/e-mail mais dados de contato e validar o vínculo com RF02/CT-RF02-01.
- Arquitetura/segurança: apontar contrato de principal autenticado disponível na base `dev`; a análise não escolhe nem implementa política transversal.
- `$backend-domain-orchestration-v2`: caso de uso de consulta somente leitura e eventuais contratos internos faltantes, sem regra duplicada no handler.
- `$backend-adapters-drivers-v2`: DTO/GET, implementação de `obter_por_id` no repository SQLAlchemy e testes unitários isolados dos adapters, após a decisão e contratos.
- Persistência: completar o mapeamento Code First de contato se os campos forem aprovados como parte da consulta.
- `$integration-system-testing-v1`: teste HTTP com sessão real e banco descartável para propriedade, ausência de sessão e dados persistidos.
- Frontend: consumir o payload aprovado e tratar ausência de sessão/perfil conforme contrato, em atividade própria.

## Síntese

O card pertence ao backend e corresponde à consulta de dados pessoais do estudante, mas a consulta deve ser autenticada e restrita à própria conta. A base `task88` não recebeu commits ao comparar com `main`, pois `origin/main` já é ancestral do HEAD atual. Permanecem ausentes GET de perfil/contato, caso de uso de consulta, implementação SQLAlchemy de `obter_por_id` e sessão autenticada integrada; além disso, o modelo não persiste os campos de contato do agregado. A recomendação é uma leitura explícita do próprio perfil, sem aceitar identidade arbitrária e sem agregar outras seções do currículo. A análise permanece `pending` até produto confirmar os campos e a equipe indicar a dependência de sessão que estará disponível na base de integração.
