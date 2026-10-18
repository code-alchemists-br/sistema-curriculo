---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-15T21:22:05-03:00"
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
    - path: src/backend/domain/itens_perfil.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ProjetoAcademico e vocabulários/limites relacionados"
      content_state: commit
      revision: "5532f45"
      availability: available
    - path: src/backend/application/cadastro_projeto_academico.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5532f45"
      availability: available
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioProjetoAcademico e GeradorProjetoAcademicoId"
      content_state: commit
      revision: "5532f45"
      availability: available
    - path: src/backend/api/projeto_academico.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5532f45"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "parâmetro, import e inclusão do router de projeto"
      content_state: commit
      revision: "5532f45"
      availability: available
    - path: src/backend/api/middleware_autenticacao.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5532f45"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/metadata.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5532f45"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "CurriculoItemRegistro e mapeamento ProjetoAcademicoId"
      content_state: commit
      revision: "5532f45"
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261015_0011_criar_cursos.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python/Alembic
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5532f45"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: Markdown/Mermaid
      analysis_scope: selected-section
      locator: "PROJETO_ACADEMICO, CURRICULO_PROJETO e CURRICULO_FORMACAO"
      content_state: commit
      revision: "5532f45"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF04 e Detalhamentos ainda necessários"
      content_state: commit
      revision: "5532f45"
      availability: available
    - path: docs/configuracao-ambiente.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "Utilizando um ambiente Nix do projeto"
      content_state: commit
      revision: "5532f45"
      availability: available
    - path: prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "checkout; não rastreado no estado observado"
      availability: available
    - path: prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "checkout; não rastreado no estado observado"
      availability: available
    - path: prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: unknown
      revision: null
      availability: unavailable
    - path: prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "decisões originais de Domain/Application para projeto acadêmico"
      content_state: working-tree
      revision: "checkout; não rastreado no estado observado"
classification:
  sphere: engineering
  concerns: [domain, architecture, data]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — expor cadastro de projeto acadêmico

## Solicitação original

`$decision-analysis-v4 Implementar "Expor cadastro de projeto acadêmico". Task para o back-end. "Expor" significa disponibilizar a funcionalidade por endpoint HTTP, como nos cards de formação acadêmica. Identifique as necessidades e siga de acordo com as documentações, os requisitos e o que já está implementado.`

O usuário estabeleceu ainda como contexto fixo o padrão de cadastro, edição e exclusão de formação acadêmica e declarou que esta demanda é uma linhagem nova. Foram fornecidos como apoio `prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md`, `prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md` e `prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md`. O terceiro caminho não foi encontrado no checkout e não foi usado como evidência.

## Informações complementares

- O proprietário deve vir somente de `request.state.usuario_id`; POST deve responder 201 com DTO explícito; dados inválidos e violações de domínio devem receber 422 com mensagem segura; 401 é do middleware e 503 segue o padrão dos handlers.
- Enums e limites usados pelo DTO devem vir do Domain. Invariantes ficam no Domain, sem validação de negócio duplicada em Application.
- Persistência deve usar ORM Code First, repositório concreto e migration Alembic aditiva com CHECKs compatíveis com PostgreSQL e SQLite.
- A tarefa cobre somente cadastro HTTP do próprio estudante. Consulta, edição, exclusão, front-end e mudanças em formação estão fora.
- Foram pedidos contratos e assinaturas explícitos para as skills de Domain/Application, adapters/drivers e testes de integração, além de documentar comandos de validação e o gate Ruff.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem de exposição do cadastro de projeto | Nenhum identificado | v001 inicial | Demanda nova; análises de formação e de núcleo de projetos são apoio, não ancestralidade | Nenhum histórico alterado |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/domain/itens_perfil.py` | Principal | Código-fonte | Produção | Python | Entidade `ProjetoAcademico` e padrões de texto/formação | Commit `5532f45` |
| `src/backend/application/cadastro_projeto_academico.py` | Principal | Código-fonte | Produção | Python | Arquivo completo | Commit `5532f45` |
| `src/backend/application/ports.py` | Principal | Código-fonte | Produção | Python | Porta do projeto e gerador de ID | Commit `5532f45` |
| `src/backend/api/projeto_academico.py` | Principal | Código-fonte | Produção | Python | Arquivo completo | Commit `5532f45` |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Injeção e registro do router | Commit `5532f45` |
| `src/backend/api/middleware_autenticacao.py` | Apoio | Código-fonte | Produção | Python | Middleware completo e extração de usuário da rota | Commit `5532f45` |
| `src/backend/infrastructure/persistence/sqlalchemy/metadata.py` | Principal | Código-fonte | Produção | Python | Imports de modelos registrados no Alembic | Commit `5532f45` |
| `src/backend/infrastructure/persistence/sqlalchemy/curriculo.py` | Apoio | Código-fonte | Produção | Python | Tabela polimórfica e mapeamento de tipos de item | Commit `5532f45` |
| `src/backend/infrastructure/persistence/alembic/versions/20261015_0011_criar_cursos.py` | Apoio | Código-fonte | Produção | Python/Alembic | Revisão e encadeamento | Commit `5532f45` |
| `docs/modelagem_der.md` | Apoio | Modelo/diagrama | Contrato de schema | Markdown/Mermaid | Projeto e relações polimórficas desenhadas como tabelas de associação | Commit `5532f45` |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF04 e detalhamentos pendentes | Commit `5532f45` |
| `docs/configuracao-ambiente.md` | Contexto | Prosa | Documentação | Markdown | Ambiente backend, quality e testes | Commit `5532f45` |
| `prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md` | Apoio | Prosa | Documentação | Markdown | Decisões de contrato e padrão HTTP | Checkout; conteúdo integral lido |
| `prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md` | Apoio | Prosa | Documentação | Markdown | Padrão de propriedade e edição | Checkout; conteúdo integral fornecido/lido no conjunto de apoio |
| `prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md` | Apoio | Prosa | Documentação | Markdown | Referência indicada pelo usuário | Indisponível: arquivo não existe no checkout |
| `prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md` | Apoio | Prosa | Documentação | Markdown | Decisão original do núcleo e lacunas explicitadas | Checkout; conteúdo usado como histórico de contexto |

### Limites da evidência dos artefatos

O estado Git observado estava limpo no commit `5532f45`; os prompts usados como apoio não estavam no índice do repositório. O terceiro artefato de formação fornecido não existe no diretório. A confirmação operacional de Alembic, feita com `nix develop .#backend --command alembic -c alembic.ini heads`, retornou `20261015_0011 (head)`. Não foram executados testes nem comandos de implementação. Não foi inspecionada uma configuração de banco implantado.

## Problema enriquecido

### Resultado desejado

Disponibilizar por HTTP o caso de uso existente para o estudante autenticado criar projeto acadêmico próprio, com persistência relacional e contrato compatível com os padrões de formação, sem introduzir campos ou operações fora do cadastro.

### Atores e interesses

- Estudante autenticado: cadastrar título, descrição e tecnologias do próprio projeto.
- API: obter proprietário da sessão, validar o contrato de transporte e não serializar a entidade.
- Domain/Application: preservar invariantes e orquestrar a entidade já existente pelo repositório e gerador de identidade existentes.
- Persistência: armazenar e reconstruir o item por SQLAlchemy, com migration versionada.
- Mantenedores: manter o DER e RF04 coerentes com o schema e a rota real.

### Evidências e fatos observados

- `ProjetoAcademico` já existe com `id`, `usuario_id`, `titulo`, `descricao` e `tecnologias`. O construtor rejeita tipo diferente de texto e valores vazios/só com espaços, mas não normaliza nem define limites máximos.
- `CadastrarProjetoAcademico` já constrói a entidade, obtém ID por `GeradorProjetoAcademicoId.gerar()`, chama `RepositorioProjetoAcademico.salvar(projeto)` e retorna a entidade. As duas portas já existem; não é necessário criar porta nova para o fluxo básico.
- O handler/API já existe com DTOs de request e response, 201, 503 quando executor ausente e tradução de `RegraDeDominioViolada` para 422. O request declara limites 1–200 para título, 1–2000 para descrição e 1–300 para tecnologias. A rota atual é `/estudantes/{usuario_id}/projetos-academicos` e usa proprietário fornecido no caminho; esse comportamento não atende à instrução atual.
- `api/factory.py` já recebe `cadastrar_projeto_academico` e registra o router. O middleware autentica por padrão toda rota não pública, grava o usuário validado em `request.state.usuario_id`, mas compara o usuário da URL quando o caminho está em `/estudantes/{uuid}/...`.
- Não há modelo SQLAlchemy de projeto, inclusão do modelo em `metadata.py`, repositório SQLAlchemy concreto ou migration de projetos. Há gerador concreto de IDs reutilizável no backend.
- Seleções de currículo já reconhecem `ProjetoAcademicoId` como tipo `projeto_academico` em API e infraestrutura. `curriculo_itens` é polimórfica e sua migration tem apenas FK para currículo e PK composta; não há FK para o item nem CHECK/enum de `tipo`. O cadastro de projeto não requer nova seleção nem mudança de política dessa tabela.
- O DER descreve `PROJETO_ACADEMICO` com título, descrição e tecnologias, além de `CURRICULO_PROJETO`; o schema real usa a tabela polimórfica `curriculo_itens`. A mesma divergência conceitual aparece em `CURRICULO_FORMACAO` e outras associações, portanto não é uma ausência específica de suporte ao tipo projeto.
- O Alembic reporta um único head atual, `20261015_0011`. Datas não fazem parte do agregado de projeto; não há questão de timezone para este cadastro.
- RF04 pede registrar projetos e orientar descrição. RF02 é amplo e não precisa ser alterado para habilitar um POST; especificar cadastro autenticado de projeto como detalhe de RF04 é mais preciso.

### Hipóteses

- A referência de formação define a linha de resposta pretendida: rota sem `usuario_id` no caminho, sessão como única origem do proprietário e validação no Domain.
- Os limites que já constam no DTO de API existente são uma intenção contratual aproveitável e devem ser promovidos a constantes do Domain; isso corrige a fronteira sem inventar novos valores.
- `tecnologias` permanece string simples, como entidade, DER e prévia atuais indicam; não se presume tags, lista normalizada ou catálogo.
- O repositório deve persistir um registro novo e fazer `flush`, seguindo os adapters síncronos com sessão SQLAlchemy já usados no backend.

### Perguntas em aberto

Nenhuma decisão de produto é necessária para o escopo de cadastro definido. As recomendações de limites e texto livre abaixo derivam do contrato existente e do esquema atual. Só mudança de produto que inclua outros atributos, catálogo de tecnologia ou duplicidade proibida exige revisão.

### Escopo

- Evoluir invariantes de `ProjetoAcademico` e constantes de tamanho para corresponder ao contrato existente.
- Manter caso de uso, entrada, porta de repositório e gerador de ID; não criar nova porta.
- Corrigir o handler para `POST /projetos-academicos`, usando `Request` e `request.state.usuario_id` exclusivamente.
- Manter DTOs explícitos, resposta 201, erros seguros 422/503 e 401 do middleware.
- Criar modelo ORM, repositório concreto, registro de metadata, binding na composição externa e migration aditiva a partir do head confirmado.
- Atualizar documentação nos trechos indicados e acrescentar testes unitários e integrados pelas skills correspondentes.

### Fora do escopo

Consulta, edição, exclusão, front-end, mudanças em cartões de formação, links, status, datas, associação direta a formação, competências associadas, participantes, autoria/papel do estudante, estrutura de lista para tecnologias, deduplicação, autenticação nova e alterações ao schema de `curriculo_itens`.

### Critérios de sucesso

- `POST /projetos-academicos` exige sessão válida por padrão e nunca aceita `usuario_id` em path, query, header ou body como proprietário.
- Sem sessão, o middleware responde 401. Com sessão válida, o dono recebido pelo caso de uso é o UUID de `request.state.usuario_id`.
- Corpo aceita somente `titulo`, `descricao` e `tecnologias`; cada texto é string, `strip` aplicado uma vez e tamanho normalizado de 1 a 200, 1 a 2000 e 1 a 300 respectivamente; controles Unicode da categoria Cc são rejeitados. Erros de formato/domínio são 422 sem ecoar conteúdo fornecido.
- Sucesso cria e salva projeto e responde 201 com DTO de `id`, `usuario_id`, `titulo`, `descricao` e `tecnologias`, sem serializar entidade.
- Modelo e migration possuem FK para usuário, campos não nulos e limites coerentes. CHECKs para não vazio e tamanho usam expressões compatíveis com PostgreSQL e SQLite. A migration é filha do head atual (ou do head mais recente confirmado no início da implementação), sem editar migrations existentes.
- Não existe restrição única de título por usuário; dois projetos com o mesmo nome são permitidos.
- Testes unitários pertinentes e testes integrados de banco/API cobrem os critérios sem introduzir mudanças de produto alheias.

## Restrições aplicáveis

- Proprietário exclusivamente da sessão autenticada, em `request.state.usuario_id`.
- Não serializar a entidade Domain; request/response DTOs explícitos.
- Domain mantém invariantes; Application não duplica sua validação.
- Enums/limites do Domain são importados pelos DTOs quando aplicáveis. O projeto atual não tem campos enum, portanto não criar vocabulário artificial.
- Migration Alembic aditiva e constraints com sintaxe compatível com PostgreSQL alvo e SQLite de testes.
- Clean Architecture, ORM Code First, testes Nix por camada e docstrings completas conforme `AGENTS.md`.
- Esta análise `proposed` não executa nem implementa a decisão.

## Classificação comentada

`engineering` é a esfera dominante: a decisão conecta núcleo já existente à API e ao armazenamento. `domain` cobre tamanhos e invariantes, `architecture` define fronteiras entre núcleo e drivers, e `data` cobre ORM/migration. É um componente em entrega. Incerteza média reflete que a API antiga já contém limites, mas ainda não há adapter/migration. Risco médio porque erro de identidade pode gravar informação privada sob proprietário errado; a operação de criação e seu schema são reversíveis com cuidado.

## Decisão de roteamento

Criar em `prompts/backend`. As candidatas imediatas existentes foram `prompts/backend`, `prompts/ambientes`, `prompts/frontend`, `prompts/templates`, `prompts/revisao` e `prompts/requisitos`. Backend é a escolha semântica pela alteração principal em API, persistência e contrato do núcleo; requisitos e DER são handoffs documentais. É uma linhagem nova, logo não herda o caminho dos prompts de formação. Nenhum `AGENTS.md` de subpasta de `prompts` foi encontrado.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| security | Alta | Sessão é a única origem do dono; 401 padrão | Protege propriedade e evita IDOR |
| correctness | Alta | Entidade persistida representa todos os campos e invariantes | Evita divergência API/Domain/schema |
| simplicity | Alta | Reusar caso de uso, portas, ID e router existentes | Minimiza mudança e contratos duplicados |
| interoperability | Média | CHECK e tipos funcionam em PostgreSQL e SQLite | Mantém produção e testes alinhados |
| user-value | Média | Estudante consegue registrar projeto pelo endpoint | Materializa RF04 |

## Alternativas consideradas

- **A — Expor o núcleo existente e completar a persistência (recomendada):** substituir a rota antiga pela rota de coleção sem usuário no caminho; derivar dono da sessão; preservar Application/portas e criar somente modelo, adapter e migration ausentes; promover ao Domain os limites já presentes no DTO.
- **B — Criar uma segunda rota para coexistir com a antiga:** acrescenta superfície que aceita proprietário no caminho e preserva ambiguidade de autorização. É inviável diante da restrição de proprietário exclusivo da sessão.
- **C — Reescrever Domain/Application junto com a exposição e adicionar campos planejados (datas, categoria, links, participantes):** duplica comportamento existente e inventa contrato sem base em RF/DER. É inviável pelo escopo e pela simplicidade.
- **D — Expor a rota antiga sem tocar em persistência:** não há adapter/modelo para salvar e a rota permite fonte de proprietário proibida. Não satisfaz os critérios.

## Perfil de pagamento comparativo

Escala ordinal: `+2` melhora forte, `+1` melhora moderada, `0` neutro/desconhecido, `-1` piora moderada e `-2` piora forte.

| Dimensão | Prioridade | A: completar vertical | B: manter segunda rota | C: reescrever/ampliar | D: só endpoint antigo | Confiança | Base |
|---|---:|---:|---:|---:|---|---|---|
| security | Alta | +2 | -2 | 0 | -2 | Alta | A usa estado de sessão; B/D preservam proprietário em URL |
| correctness | Alta | +2 | -1 | -1 | -2 | Alta | A fecha ausência de persistência e respeita agregado |
| simplicity | Alta | +2 | -2 | -2 | +1 | Alta | A reutiliza caso de uso e portas existentes |
| interoperability | Média | +2 | 0 | +1 | -2 | Alta | A inclui migration e constraints compatíveis |
| user-value | Média | +2 | +1 | +1 | -1 | Alta | A disponibiliza gravação utilizável |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma nesta linhagem. O prompt anterior de Domain/Application de projeto acadêmico é evidência de contexto, não versão anterior desta análise.

### Decisão recomendada nesta versão

Adotar A com o seguinte contrato:

- `POST /projetos-academicos`; não criar rota paralela sob `/estudantes/{usuario_id}`.
- O handler recebe `request: Request`, constrói `UsuarioId(request.state.usuario_id)` e preenche `CadastrarProjetoAcademicoEntrada(usuario_id, titulo, descricao, tecnologias)`. O DTO não possui dono.
- Request: `{ "titulo": string, "descricao": string, "tecnologias": string }`. Response 201: `{ "id": UUID, "usuario_id": UUID, "titulo": string, "descricao": string, "tecnologias": string }`.
- Manter o caso de uso e contratos atuais: `async CadastrarProjetoAcademico.executar(entrada: CadastrarProjetoAcademicoEntrada) -> ProjetoAcademico`; `RepositorioProjetoAcademico.salvar(projeto: ProjetoAcademico) -> None`; `GeradorProjetoAcademicoId.gerar() -> ProjetoAcademicoId`. **Nenhuma porta nova é necessária.**
- Promover os limites declarados no DTO já existente a constantes de Domain: `TAMANHO_MINIMO_TEXTO_PROJETO = 1`, `TAMANHO_MAXIMO_TITULO_PROJETO = 200`, `TAMANHO_MAXIMO_DESCRICAO_PROJETO = 2000`, `TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO = 300`. A entidade normaliza com `strip`, rejeita Cc, exige mínimo 1 e aplica o máximo por campo. O DTO importa os limites do Domain e faz somente validação de forma/tipo/comprimento; a entidade continua sendo autoridade da regra.
- Campos todos obrigatórios e sem mínimo adicional além de um caractere não branco. Manter tecnologias como texto livre obrigatório, sem enum/tags/lista, porque esse é o formato existente. Não criar tipos controlados para projeto/status.
- Sem datas ou status: nenhum campo temporal existe no Domain ou DER do projeto, então coerência de período e datas futuras não se aplicam. Sem links: nenhum campo correspondente está no modelo; não inventar validação URL agora. Se futuramente forem incluídos links, exigir `http`/`https`, rejeitar demais esquemas, limitar comprimento e escapar/validar destino na apresentação; isso é revisão futura, não parte deste cadastro.
- Sem unicidade de título/nome por estudante. A entidade, requisitos e schema não definem identidade lógica do projeto pelo título, e projetos homônimos podem ser distintos. A PK UUID é a identidade.
- Criar `ProjetoAcademicoRegistro` em `projeto_academico.py`, espelhando os cinco campos persistidos, UUID para IDs, FK nomeada para `usuarios.id`, `String(200)` para título e `String(300)` para tecnologias, descrição textual com limite lógico 2000; incluir CHECKs de trim/length com nomes estáveis. Registrar em metadata.
- Criar `RepositorioProjetoAcademicoSQLAlchemy` em `repositorio_projeto_academico.py` recebendo a sessão conforme convenção concreta local; `salvar` converte entidade para registro, adiciona e faz `flush`, sem commit e sem regra de domínio. O modelo oferece conversões `para_registro(projeto)` e `para_projeto_academico(registro)`.
- Gerar migration aditiva com tabela `projetos_academicos`, FK para usuário, PK, NOT NULL e CHECKs equivalentes. Confirmar de novo o head quando a implementação for iniciada; no instante desta análise o head observado é `20261015_0011`.
- Reusar o parâmetro e a inclusão do router já existentes em `api/factory.py`; a composição mais externa deve injetar adapter e `GeradorProjetoAcademicoId` no caso de uso e passar executor à factory. A factory do router, isoladamente, já está registrada.
- Manter mensagens 422 que não ecoem valores do usuário. Manter 503 para executor/dependência indisponível. Middleware global dá 401 antes do handler; não alterar política transversal.

O CHECK de tamanho e não vazio usa `length(trim(campo)) BETWEEN ...`, disponível nos dois bancos considerados. Não tentar CHECK portável para todos os caracteres Unicode de controle: rejeição de Cc fica no Domain e na validação do DTO, e a migration não duplica regra com SQL específico de um banco.

### Impacto da revisão

Não aplicável; versão inicial de uma linhagem de exposição. A descoberta altera a hipótese implícita de que a API estivesse ausente: o router e o contrato já existem, porém a rota não respeita a sessão e não existe persistência concreta.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| security | prioritized | Criar apenas sob a identidade autenticada | Middleware já grava `request.state.usuario_id`; rota atual lê path |
| correctness | prioritized | Contrato de request, domínio e banco usa os mesmos limites | Limites existentes no DTO e invariantes no Domain |
| simplicity | prioritized | Preservar Application, portas, ID e registro do router já feitos | Código existente observado |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| interoperability | PostgreSQL e SQLite aceitam tipos/checks da migration | Tipos UUID, VARCHAR/TEXT, FK e `length(trim())` portáveis |
| user-value | Estudante consegue registrar três informações de projeto | Request usa os três campos que o caso de uso já recebe |
| data integrity | Projeto sempre pertence a usuário existente | FK para `usuarios.id`; validação de texto no Domain e CHECK no banco |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| security | Projeto pode ser gravado em nome de usuário indicado pelo cliente | Alta | Estudantes |
| correctness | API aceita limite que o Domain/schema não aplicam, ou endpoint anuncia sucesso sem salvar | Alta | Estudante e currículo |
| simplicity | Reescrever o caso de uso duplica fluxos já testados e aumenta divergência | Média | Mantenedores |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | Adicionar modelo, adapter, migration e checks à mudança | delivery-speed | Aceitável; persistência é necessária para cumprir cadastro HTTP |
| security | Rota deixa de aceitar URLs com ID do usuário | conveniência de clientes antigos | Aceitável; rota antiga não cumpre o requisito de sessão exclusiva |
| data integrity | Limites e normalização tornam-se invariantes do Domain | flexibilidade de textos longos | Aceitável porque os limites já estão expostos no DTO atual |
| simplicity | Tecnologias continuam texto único sem estrutura | interoperabilidade com filtros por tecnologia | Aceitável sem requisito de pesquisa/tag; revisar se surgir esse uso |

## Riscos e efeitos de segunda ordem

- Alterar o path pode afetar cliente que ainda chame a rota antiga; não preservar a rota antiga, pois ela conflita com a regra explícita de proprietário. Confirmar consumidores e atualizar contrato de integração se houver cliente ativo.
- A rota sem UUID não aciona a comparação de proprietário por path do middleware, mas continua protegida pelo middleware default; a identidade deve ser lida do `request.state` no handler. Não alterar middleware.
- O limite de descrição em 2000 é derivado do DTO existente, não de limite textual explícito no RF. Caso produto prefira outro valor, isso exige revisar este artefato antes da implementação.
- O DER apresenta associações conceituais separadas (`CURRICULO_PROJETO`, `CURRICULO_FORMACAO`), enquanto o schema real consolida os itens em `curriculo_itens`. Corrigir apenas o tratamento documental necessário para não sugerir que o cadastro de projeto exige uma nova tabela de junção; uma revisão ampla do DER das demais categorias excede esta task.
- Sem unicidade lógica, duplicatas exatas podem ocorrer intencionalmente. Se o produto passar a definir que título identifica projeto por estudante, revisar requisitos, Domain, porta, índice único e tratamento de concorrência.
- Dados de tecnologia e descrição podem conter texto destinado a currículo; consumidores devem renderizar como texto e não como HTML confiável. Não há URL ou HTML rico no contrato recomendado.
- O head Alembic muda com cards concorrentes; a migration deve derivar do head confirmado imediatamente antes de sua criação, sem reescrever a migration `0011`.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Sessão é o único proprietário | Caso de uso recebe UUID de `request.state`; request não tem dono | Teste de rota/middleware, incluindo 401 e usuário autenticado | Cliente exigir delegação ou criação administrativa |
| Limites 200/2000/300 são os pretendidos | DTO atual, constantes Domain e schema coincidem | Revisão dos contratos e testes unitários de limites | RF ou decisão de produto definir tamanho diferente |
| Entity/Application podem ser reutilizadas | Mesmo contrato de entrada/porta, sem regra nova de fluxo | Testes unitários backend e composição da factory | Necessidade de transação/efeito de negócio adicional |
| Migration é portável | Tabela, constraints e FK aplicadas nos dois dialetos | Testes integrados com PostgreSQL real e SQLite | Diferença semântica entre constraints nos bancos |
| Projeto já pode ser selecionado no currículo | Tipo `projeto_academico` reconhecido no contrato de seleção e armazenamento | Teste de regressão da seleção; nenhuma nova mudança de tipo necessária | Alteração no vocabulário de tipos ou política FK polimórfica |
| DER e RF explicam o cadastro entregue | Trechos ajustados sem contradizer schema real | Revisão documental | Alteração de campos/relacionamentos aprovada |

## Handoffs e atividades posteriores

| Atividade | Responsabilidade | Encaminhamento |
|---|---|---|
| Promover limites/normalização/rejeição de controles à entidade `ProjetoAcademico`; testes unitários do Domain | Domain | `$backend-domain-orchestration-v2`, análise `prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001` |
| Preservar `CadastrarProjetoAcademico`, entrada e portas atuais; confirmar apenas que nenhuma mudança de Application é necessária e executar seus testes unitários pertinentes | Application | `$backend-domain-orchestration-v2`; nenhuma porta nova; assinatura existente é `executar(entrada: CadastrarProjetoAcademicoEntrada) -> ProjetoAcademico` |
| Trocar rota para `/projetos-academicos`, extrair sessão, manter DTOs/respostas; criar modelo, mapeadores, repositório concreto, metadata e migration; testes unitários isolados dessas unidades | API/persistência | `$backend-adapters-drivers-v2`; porta existente `RepositorioProjetoAcademico.salvar(projeto: ProjetoAcademico) -> None`; gerador existente `GeradorProjetoAcademicoId.gerar() -> ProjetoAcademicoId`; sem assinatura de porta nova |
| Integração real de migrations em PostgreSQL e SQLite, chamada da rota via aplicação/middleware, 401 sem sessão e 422 para payload inválido/violação; confirmar 201 e ownership com sessão | Testes integrados | `$integration-system-testing-v1`, usando `nix develop .#tests`; testes de nível superior não pertencem às duas skills de implementação |
| Atualizar DER e RF04 nos trechos explicitados abaixo | Documentação | Fora das duas skills de código; atividade documental separada |
| Avaliar alteração transversal no middleware, links, campos extras ou tipos de seleção | Segurança/produto/arquitetura | Fora desta decisão; nova análise se necessário. O middleware atual não precisa ser alterado |

### Plano de validação e gates

- Testes unitários de Domain, Application e adapters no ambiente de backend: `nix develop .#backend --command python -m unittest ...`, selecionando os módulos pertinentes conforme os arquivos alterados.
- Testes integrados com migration aplicada em PostgreSQL real isolado e SQLite, rota exercitada pela aplicação com middleware, 401 e 422 (além de 201/ownership): atividade `$integration-system-testing-v1`, no ambiente `nix develop .#tests`.
- Ao fim de **cada execução de implementação/validação de cada skill**, executar o gate de lint do CI: `nix develop .#quality --command ruff check src/backend`. Se falhar por I001, corrigir somente os arquivos apontados com `nix develop .#quality --command ruff check --select I --fix <arquivos-apontados>` e repetir o gate completo.
- Esta análise não executa testes nem lint.

### Trechos exatos de documentação a atualizar

- `docs/modelagem_der.md`: bloco Mermaid `PROJETO_ACADEMICO` (atualmente linhas 72–79 aproximadamente), registrar comprimentos recomendados dos três textos e a FK de proprietário sem introduzir datas/status/links. Na relação de currículo, explicar que `CURRICULO_PROJETO` é a relação conceitual e é materializada pelo tipo `projeto_academico` em `curriculo_itens`. Registrar que essa tabela é polimórfica, possui FK para currículo e não possui FK do `item_id` para a tabela específica. A mesma divergência alcança `CURRICULO_FORMACAO`; apontá-la sem redesenhar todas as associações neste card.
- `docs/requisitos_funcionais.md`: manter a linha de alto nível RF04; no bloco **Detalhamentos ainda necessários**, trocar o item genérico de campos por um detalhamento do cadastro autenticado do projeto próprio com título, descrição e tecnologias, limites e endpoint `POST /projetos-academicos`, resposta criada e propriedade proveniente da sessão. Não alterar RF02, pois esta tarefa não implementa consulta, edição ou exclusão.

## Síntese

O núcleo de cadastro e o router já existem, mas o endpoint atual confia em `usuario_id` do caminho e não há tabela, adapter SQLAlchemy ou migration. Recomenda-se expor `POST /projetos-academicos` com proprietário obtido exclusivamente de `request.state.usuario_id`, preservar o caso de uso/portas atuais e completar somente API, persistência, migration e os limites de texto derivados do DTO atual. Os três textos permanecem obrigatórios, livres e limitados; tecnologias não vira lista, não há enum de status, datas, links ou unicidade por título. O tipo de projeto já é reconhecido pelas seleções de currículo e não exige novo CHECK em `curriculo_itens`. A principal incerteza real é se os limites do DTO existente, especialmente descrição 2000, representam a intenção final do produto; a evidência atual permite recomendá-los sem bloquear a implementação.
