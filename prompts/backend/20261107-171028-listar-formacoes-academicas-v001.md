---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-11-07T17:10:28-03:00"
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
    - path: "AGENTS.md"
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/AGENTS.md"
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "prompts/README.md"
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/api/formacao_academica.py"
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/api/factory.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "contratos e registro do router de formação"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/main.py"
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "app = create_app e executores de formação"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/api/middleware_autenticacao.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/application/ports.py"
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioFormacaoAcademica, linhas 124–193"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/infrastructure/persistence/sqlalchemy/repositorio_formacao_academica.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/domain/itens_perfil.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "_chave_ordenacao_formacao e ordenar_formacoes, linhas 235–281"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/api/listagem_versoes_curriculo.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "docs/wireframes/04-formacao.md"
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "prompts/backend/20261016-100000-expor-ordenacao-formacoes-consulta-v001.md"
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md"
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "frontmatter, linhas 1–120; convenção de classificação e roteamento"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "Novo contrato HTTP, caso de uso e composição de persistência do backend; não é revisão geral nem levantamento de requisitos."
classification:
  sphere: engineering
  concerns: [architecture, security, integration]
  decision_kind: design
  scope: component
  lifecycle: evolution
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — listar formações acadêmicas do estudante autenticado

## Solicitação original

> $decision-analysis-v4 Precisamos de um endpoint GET para formacoes-academicas. Ele deve fazer sentido com os endpoints já existentes.

## Informações complementares

Contexto anterior do usuário, preservado literalmente:

> estou testando o backend fazendo requisições manualmente pelo swagger. mas, não estou conseguindo mandar um post/formacao-academica. Esta dando 503. O que faço?

> O código deve ser alterado para que os endpoints de formacoes-academicas funcionem no uvicorn.

A segunda mensagem foi repetida na sessão. As alterações anteriores de composição estão no working tree; não constituem implementação do GET. Esta atividade escreve somente esta análise.

## Mudanças desde a versão anterior

Nenhum identificado: análise inicial de uma nova capacidade. A análise de ordenação de 16/10 trata da prévia de currículo e explicitamente exclui uma rota dedicada de listagem; é antecedente de apoio, não versão anterior desta linhagem.

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `AGENTS.md` | context | prose | prompt-instruction | Markdown | whole-file: arquivo completo | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | Markdown | whole-file: arquivo completo | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `prompts/README.md` | context | prose | documentation | Markdown | whole-file: arquivo completo | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `src/backend/api/formacao_academica.py` | primary | source-code | production | Python | whole-file: arquivo completo | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `src/backend/api/factory.py` | supporting | source-code | production | Python | selected-section: contratos e registro do router de formação | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `src/backend/main.py` | primary | source-code | production | Python | selected-section: app = create_app e executores de formação | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `src/backend/api/middleware_autenticacao.py` | supporting | source-code | production | Python | whole-file: arquivo completo | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `src/backend/application/ports.py` | supporting | source-code | schema-contract | Python | selected-section: RepositorioFormacaoAcademica, linhas 124–193 | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_formacao_academica.py` | supporting | source-code | production | Python | whole-file: arquivo completo | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `src/backend/domain/itens_perfil.py` | supporting | source-code | production | Python | selected-section: _chave_ordenacao_formacao e ordenar_formacoes, linhas 235–281 | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `src/backend/api/listagem_versoes_curriculo.py` | supporting | source-code | production | Python | whole-file: arquivo completo | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `docs/wireframes/04-formacao.md` | supporting | prose | documentation | Markdown | whole-file: arquivo completo | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `prompts/backend/20261016-100000-expor-ordenacao-formacoes-consulta-v001.md` | supporting | prose | documentation | Markdown | whole-file: arquivo completo | working-tree baseado em `66af300`; não equivale necessariamente ao commit |
| `prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md` | context | prose | documentation | Markdown | selected-section: frontmatter, linhas 1–120; convenção de classificação e roteamento | working-tree baseado em `66af300`; não equivale necessariamente ao commit |

### Limites da evidência dos artefatos

A leitura representa o working tree, incluindo mudanças anteriores ainda não commitadas em `main.py`. Nenhum teste foi executado nesta análise e nenhum comportamento novo foi certificado. Buscas em outros prompts serviram para localizar antecedentes; seu conteúdo não foi tratado como requisito aprovado. O módulo de listagem de associações procurado por nome não existia nesse caminho e não foi usado como evidência. Não foram consultados serviços externos nem métricas de volume. Instruções da skill e suas quatro referências foram lidas como método, não como evidência de produto.

## Problema enriquecido

### Resultado desejado

Permitir ao estudante recuperar suas formações após cadastro ou edição, inclusive em nova sessão do Swagger, e identificar os IDs necessários a PUT e DELETE sem depender da resposta transitória do POST.

### Atores e interesses

- Estudante: consultar seus itens e localizar o que deseja editar ou remover.
- Consumidor da API: contrato previsível e reutilização dos campos já conhecidos.
- Equipe do backend: implementação nas fronteiras existentes e funcionamento no Uvicorn.

### Evidências e fatos observados

- A API de formação publica POST na coleção e PUT/DELETE no item; não há GET nesse router.
- `FormacaoAcademicaResposta` contém `id`, `usuario_id`, `instituicao`, `curso`, `nivel`, `data_inicio`, `data_fim` e `status`.
- Proprietário de formação vem de `request.state.usuario_id`; o middleware autentica cookie e não declara formação como rota pública.
- A porta e o adapter existentes consultam por ID e proprietário, mas não oferecem listagem por proprietário. A consulta ativa filtra `deleted_at IS NULL`; exclusão possui consulta específica que inclui excluídas.
- `ordenar_formacoes` já define situação, datas e desempate por ID. O antecedente da prévia orienta reutilizar essa regra em futura listagem.
- O wireframe prevê lista com ações Adicionar, Editar e Remover.
- `main.app` agora injeta executores de escrita quando há fábrica de sessões; o GET precisará de ligação equivalente.
- A listagem de versões de currículo usa um objeto contendo uma coleção. Seu proprietário no caminho é um contrato legado e não deve substituir a identidade autenticada usada em formação.

### Hipóteses

H1: “GET para formacoes-academicas” significa listar a coleção do próprio estudante. O wireframe e a necessidade de recuperar IDs sustentam essa interpretação; GET de item não a substitui.

H2: a coleção por estudante é pequena o bastante para leitura integral. Não há medição que confirme esse limite; a opção sem paginação é uma simplificação proposta, não uma capacidade comprovada.

H3: a apresentação deve seguir a ordenação do domínio já usada na prévia. A regra é explícita no código e no antecedente consultado.

### Perguntas em aberto

Qual é a distribuição real da quantidade de formações por estudante? Medir antes de introduzir paginação por necessidade de capacidade. Nenhuma pergunta bloqueia a proposta de contrato; a ambiguidade entre coleção e item está explicitada em H1 para revisão humana.

### Escopo

Um GET de coleção autenticado, DTO de listagem, caso de uso, porta de listagem, adapter SQLAlchemy, executor de leitura com sessão curta, injeção na factory e no `main.app`, documentação OpenAPI e testes.

### Fora do escopo

GET por ID, consultas de outros estudantes, filtros, pesquisa, paginação nesta primeira versão, restauração ou listagem de excluídas, mudanças em POST/PUT/DELETE, prévia/exportação e implementação de frontend. Não alterar retenção histórica nem migrations sem necessidade demonstrada.

### Critérios de sucesso

1. Após autenticação, GET permite observar cadastro e edição confirmados pelas rotas existentes.
2. Lista vazia é sucesso com coleção vazia, nunca 404.
3. Coleção contém somente formações ativas do usuário autenticado e mantém os oito campos do DTO existente por item.
4. Após DELETE confirmado, o item desaparece da coleção; registros de outro dono nunca aparecem.
5. A ordem segue `ordenar_formacoes` e não a ordem incidental do banco.
6. Funciona pelo objeto `backend.main:app` usado no Uvicorn com PostgreSQL migrado, sem overrides de dependência.
7. Consulta não realiza escrita e falhas não expõem SQL, credenciais ou dados de outros usuários.

## Restrições aplicáveis

- Clean Architecture e DDD: domínio independente; regras e ordenação não pertencem ao controller ou ao ORM.
- Identidade exclusivamente da sessão; nenhum parâmetro de proprietário pode alterar o escopo da consulta.
- Repositório deve aplicar proprietário e exclusão na consulta ao banco, antes de devolver dados à Application.
- Schema relacional continua Code First. A capacidade usa colunas existentes e não demanda migration por si só.
- API expõe DTOs, nunca entidades ou registros ORM diretamente.
- Documentar funções/classes com responsabilidade, abordagem e finalidade.
- Toda mudança de comportamento futura precisa de testes unitários no Nix backend; integração e níveis superiores no Nix tests. Git permanece fora do Nix.
- Nesta atividade, a skill permite somente um novo Markdown de análise; implementação fica como handoff.

## Classificação comentada

`engineering` domina porque a decisão desenha contrato HTTP e integração com persistência existente. `architecture`, `security` e `integration` distinguem fronteiras, isolamento por proprietário e ligação no Uvicorn. O objeto é `mixed`: a demanda define a capacidade e os arquivos delimitam o contrato. Incerteza média pela ausência de volumetria; risco médio pelo impacto de vazamento entre estudantes. Alterar um contrato consumido tem reversibilidade moderada.

## Decisão de roteamento

Inventário observado de subpastas imediatas: `ambientes`, `backend`, `frontend`, `requisitos`, `revisao`, `templates`. Selecionada `prompts/backend`, com confiança alta, por tratar da API e da composição do servidor. `requisitos` é menos específica e `revisao` não corresponde ao propósito principal. Não foram encontrados AGENTS locais adicionais ou overrides nas candidatas; aplicam-se as instruções da raiz. O README de prompts confirma essa organização.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| user-value | Alta | Permitir recuperar a coleção e IDs | Viabiliza a lista e as ações existentes |
| correctness | Alta | Mesmos campos, exclusão e ordem do domínio | Evita contradição entre operações |
| security | Obrigatória | Consulta somente do dono autenticado | Impede divulgação entre contas |
| simplicity | Média | Menor contrato que atende à coleção | Evita novos recursos sem demanda |
| scalability | Média | Não impor capacidade sem evidência | Paginação pode ser necessária com volume |

## Alternativas consideradas

- A — Estado atual: manter apenas escrita. É a referência comparativa e não satisfaz a solicitação.
- B — GET de coleção própria sem paginação, em envelope `formacoes`, ordenado pelo domínio. Viável e recomendado.
- C — GET de coleção própria paginada desde a primeira versão. Viável, mas exige decidir paginação e aplicar ordem global coerente antes do recorte.
- D — Somente GET de item por ID. É tecnicamente viável, mas não resolve descoberta da coleção e dos IDs; pode ser complemento futuro.

Listar globalmente ou aceitar um proprietário arbitrário sem autorização é inviável pela restrição de isolamento; não entra como alternativa de pagamento.

## Perfil de pagamento comparativo

Escala ordinal relativa a A: +2 melhora forte, +1 moderada, 0 neutro ou desconhecido, -1 piora moderada, -2 forte. Sem soma; confiança descreve a sustentação de cada comparação.

| Dimensão | Prioridade | A | B | C | Confiança | Base |
|---|---|---|---|---|---|---|
| user-value | Alta | 0 | +2 | +2 | Alta | Coleção permite recuperar IDs; paginação requer navegação adicional |
| correctness | Alta | 0 | +1 | +1 | Alta | DTO explícito e regra existente; C exige ordenação global antes da página |
| security | Obrigatória | 0 | 0 | 0 | Alta | B/C só são viáveis com o mesmo isolamento; leitura aumenta superfície a testar |
| simplicity | Média | 0 | -1 | -2 | Alta | B adiciona fluxo de leitura; C adiciona também protocolo de páginas |
| scalability | Média | 0 | 0 | +1 | Baixa | Volume desconhecido; C limita respostas, B não tem capacidade comprovada |

D melhora leitura de um item (+1 em user-value), mas continua sem descoberta da coleção; perde para B no resultado principal e não é priorizada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado nesta linhagem. A decisão de ordenação da prévia continua independente; sua exclusão de listagem era limite daquela entrega, não proibição permanente.

### Decisão recomendada nesta versão

Adotar B como proposta para aprovação humana:

- `GET /formacoes-academicas`, sem corpo, sem filtro de proprietário e sem parâmetro de paginação nesta versão.
- HTTP 200 com `{"formacoes": [...]}`; ausência de registros devolve `{"formacoes": []}`.
- Cada item usa o contrato `FormacaoAcademicaResposta`: os oito campos já retornados por POST/PUT, sem `deleted_at` nem campos internos novos. Preservar enums e semântica de `data_fim`.
- Identidade vem exclusivamente de `request.state.usuario_id`. Nunca tratar `usuario_id` de query/corpo como autorização. Não declarar a rota pública nem adicionar CORS especial.
- Repositório lista com `usuario_id` autenticado e `deleted_at IS NULL`. Application chama `ordenar_formacoes` sobre o resultado; handler preserva a sequência e converte em DTOs.
- Ordem: em andamento pelo início decrescente; concluídas pelo fim decrescente; interrompidas pelo fim ou início decrescente. Empates seguem início decrescente e ID textual conforme a função existente. Não copiar a regra para SQL ou controller nesta versão.
- Criar entrada de Application com `UsuarioId`, caso de uso de listagem e capacidade de repositório por proprietário, seguindo as fronteiras já usadas. Nenhuma escrita ou commit de mutação é necessário no GET.
- Injetar executor de leitura com sessão assíncrona curta pela factory e pelo `main.app`; reutilizar a fábrica de sessões e o ciclo de vida da engine, sem sessões globais.
- Cookie ausente/inválido: HTTP 401 uniforme pelo middleware (`Sessão ausente ou inválida.`). Executor ausente com chamada autenticada: HTTP 503 (`Listagem indisponível.`). A autenticação continua precedendo o handler. Sem banco e sem autenticação válida, não prometer 503 em vez de 401.
- Nenhum 404 para coleção vazia, nenhum 422 de regra de escrita e nenhum sucesso vazio artificial quando o banco falhar. Falhas de infraestrutura devem manter a política geral de erros seguros; 503 por executor ausente não deve ser apresentado como tratamento já existente para toda falha de banco.
- OpenAPI descreve coleção, campos, autenticação por cookie, ordem e respostas aplicáveis. Documentar a capacidade nova sem alterar respostas das operações existentes.

### Impacto da revisão

Nenhum identificado: modo inicial. A decisão propõe a leitura dedicada que o antecedente da prévia deixou para outra atividade.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| user-value | prioritized | Recuperação da coleção e IDs após nova sessão | Wireframe e H1 |
| correctness | prioritized | Mesmos campos e regra de ordem, excluídas ocultas | Router, repositório e domínio |
| simplicity | prioritized | Uma única rota de leitura e nenhum protocolo de páginas | Comparação B/C/D |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| security | Nenhum registro de outro proprietário | Identidade da sessão e filtro obrigatório no banco |
| scalability | Coleção pequena validada antes de uso amplo | H2 permanece aberta; envelope permite futura evolução planejada |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| user-value | Dependência de IDs guardados do POST | Alta | Estudante e consumidor |
| correctness | Ordem divergente ou reaparecimento de excluídas | Alta | Estudante |
| simplicity | Mais parâmetros e navegação sem evidência de necessidade | Média | Consumidor e equipe |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| user-value | Novo fluxo vertical de leitura e testes | delivery-speed | Necessário para completar o uso da coleção |
| correctness | Ordenação em memória e leitura de toda a coleção | scalability | Aceito provisoriamente sob H2 |
| simplicity | Adiar paginação e GET individual | optionality | Revisar se volume ou consumidor exigirem |

## Riscos e efeitos de segunda ordem

- Consulta sem filtro de dono vaza dados: testes com duas contas devem impedir regressão.
- Uso da consulta que inclui excluídas expõe tombstones: listagem deve usar somente ativos e não alterar a leitura histórica de currículos.
- Paginar futuramente sem ordem global muda o significado da listagem: exige decisão explícita e estratégia compatível com o domínio.
- Testar apenas router/factory pode ocultar executor ausente no Uvicorn: integração deve usar `backend.main:app`.
- Reaproveitar DTO de escrita exige atualizar sua documentação para refletir também leitura; não modificar os campos por conveniência.
- Respostas pessoais podem ser armazenadas por intermediários: avaliar política privada de cache na implementação, sem transformar a coleção em recurso público.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| H1: coleção é o recurso necessário | Consumidor consegue listar e escolher item para PUT/DELETE | Revisão do contrato e cenário Swagger | Necessidade explícita de carregar item isolado |
| H2: leitura integral é adequada | Distribuição de itens e custo da consulta | Medição local com dados sintéticos representativos | Respostas ou consumo acima dos limites definidos pela equipe |
| H3: mesma ordem em consulta e prévia | Casos com todos os status, datas empatadas e IDs distintos | Unitários reutilizando a regra de domínio | Necessidade de ordem diferente para a tela |
| Isolamento e exclusão | Duas contas, registros ativos/excluídos e lista vazia | Unitários e integração SQLAlchemy/PostgreSQL | Qualquer registro alheio ou excluído retornado |
| Composição real | POST → GET → PUT → GET → DELETE → GET com cookie real | PostgreSQL efêmero e `main.app`, sem overrides | 503 com banco/executor configurados ou escrita não observável |
| Ausência de mutação | Estado bruto idêntico antes/depois do GET | Consulta independente em integração | Alteração em dados ou tombstones |
| Contrato HTTP e erros | DTO, ordem, 200/401/503 e schema documentados | Testes de API/OpenAPI e dependência ausente isolada | Esquema divergente ou detalhes internos expostos |

## Handoffs e atividades posteriores

1. Revisar e aprovar esta proposta; `status: proposed` não representa decisão já aprovada.
2. Em atividade de implementação, criar a fatia vertical de leitura e ligá-la ao Uvicorn, mantendo POST/PUT/DELETE e arquivos de trabalho anteriores.
3. Adicionar/executar unitários no Nix backend e integração no Nix tests, com PostgreSQL temporário; registrar falhas e skips sem tratá-los como sucesso.
4. Validar manualmente no Swagger com login e banco local migrado. Para HTTP local, preservar a configuração deliberada de cookie existente.
5. Medir volumetria para reavaliar H2. Integração de frontend, GET individual e paginação ficam como demandas posteriores, se necessárias.

## Síntese

Proposta: GET autenticado da coleção própria, envelope `formacoes`, mesmos campos públicos de POST/PUT, somente itens ativos e ordenação do domínio. O aceite inclui a composição real no Uvicorn. A principal incerteza é o volume da coleção; nesta análise nenhuma implementação foi realizada.
