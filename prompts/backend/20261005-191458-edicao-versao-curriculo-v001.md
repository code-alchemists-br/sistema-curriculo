---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-05T19:14:58-03:00"
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
    - path: src/backend/domain/curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255 (conteúdo lido antes das alterações locais propostas por esta análise)"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
    - path: docs/requisitos-seguranca.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "linhas 300-312, 370-392 e 436-446 (propriedade do recurso, verificação de propriedade e negação por padrão)"
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: partial
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "linhas 18 e 33 (RNF04)"
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: partial
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: markdown-with-mermaid
      analysis_scope: selected-section
      locator: "trechos que mencionam CURRICULO (linhas 11-35 e 104-169)"
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: partial
    - path: docs/casos-de-uso-v2.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "linhas 105-118 (caso de uso Gerenciar versões)"
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: partial
    - path: docs/GUIA-DE-USO-DAS-SKILLS-v001.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 1-32 e 205-242 (importações e portas de projeto acadêmico, usadas como precedente)"
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255 (conteúdo lido antes das alterações locais propostas por esta análise)"
      availability: partial
    - path: src/backend/application/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/metadata.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/env.py
      relationship: supporting
      representation: source-code
      function: configuration
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20260916_0001_criar_usuarios.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: python
      analysis_scope: selected-section
      locator: "linhas 1-14 (identificadores da revisão)"
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: partial
    - path: src/backend/tests/test_infrastructure_usuario_mapping.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
    - path: src/backend/tests/test_infrastructure_repositorio_usuario.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: selected-section
      locator: "linhas 1-120 (convenção de testes do adapter com doubles)"
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: partial
    - path: src/backend/api/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
    - path: src/backend/api/cadastro_acesso.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 134-149 (rota /acessos, resposta 204 sem sessão ou token)"
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: partial
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
    - path: src/backend/main.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "f3979c41f2272deaa54aad8b160c9d27ff6e6255"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "O propósito é decidir a construção de uma fatia de backend (domínio, casos de uso, persistência e API); os artefatos principais são código de domínio e requisitos já consumidos por análises existentes em prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, security, data]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — edição de versão de currículo (fatia vertical)

## Solicitação original

Texto literal fornecido pelo usuário:

```text
Implementar edição de versão de currículo
Tarefa da fatia vertical Inclua os testes unitários pertinentes.
```

O número da tarefa não consta na solicitação. A branch de trabalho criada pelo usuário chama-se `task-113` (observado no repositório em 2026-10-05); esse nome é apenas um dado observado e não é tratado como identificador oficial da tarefa.

## Informações complementares

Insumos literais registrados na conversa que originou esta análise (a grafia original foi preservada):

- Mensagem do gestor do projeto, reproduzida pelo usuário em conversa anterior: "No começo as coisas não estavam muito bem definidas, mas agora as funcionalidades já são claras. Os time serão reorganizados para lidar com slices verticais agora ao invés de horizontais. Isso só afeta backend. Frontend fica do mesmo jeito"
- Pedido do usuário sobre a rastreabilidade do código: "consegue colocar esse # provneiencia? pra seguir o padrao do pessoal?"
- Pedido do usuário para a produção deste documento: "gere esse documento. CUIDADO com as coisas."

O usuário ainda não respondeu às duas perguntas abertas feitas antes desta análise (inclusão de `created_at`, `updated_at` e `deleted_at` na persistência; ver "Perguntas em aberto").

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/domain/curriculo.py` | primary | source-code | production | python | arquivo inteiro | commit `f3979c4` |
| `docs/requisitos_funcionais.md` | primary | prose | documentation | markdown | arquivo inteiro | commit `f3979c4` |
| `docs/requisitos-seguranca.md` | supporting | prose | documentation | markdown | linhas 300-312, 370-392 e 436-446 | commit `f3979c4` |
| `docs/requisitos_nao_funcionais.md` | supporting | prose | documentation | markdown | linhas 18 e 33 (RNF04) | commit `f3979c4` |
| `docs/modelagem_der.md` | supporting | diagram-model | schema-contract | markdown-with-mermaid | trechos com CURRICULO (linhas 11-35 e 104-169) | commit `f3979c4` |
| `docs/casos-de-uso-v2.md` | supporting | prose | documentation | markdown | linhas 105-118 | commit `f3979c4` |
| `docs/GUIA-DE-USO-DAS-SKILLS-v001.md` | context | prose | documentation | markdown | arquivo inteiro | commit `f3979c4` |
| `AGENTS.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `f3979c4` |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `f3979c4` |
| `src/backend/application/ports.py` | supporting | source-code | production | python | linhas 1-32 e 205-242 | commit `f3979c4` |
| `src/backend/application/perfil_estudante.py` | supporting | source-code | production | python | arquivo inteiro | commit `f3979c4` |
| `src/backend/infrastructure/persistence/sqlalchemy/usuario.py` | supporting | source-code | production | python | arquivo inteiro | commit `f3979c4` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py` | supporting | source-code | production | python | arquivo inteiro | commit `f3979c4` |
| `src/backend/infrastructure/persistence/sqlalchemy/metadata.py` | supporting | source-code | production | python | arquivo inteiro | commit `f3979c4` |
| `src/backend/infrastructure/persistence/alembic/env.py` | supporting | source-code | configuration | python | arquivo inteiro | commit `f3979c4` |
| `src/backend/infrastructure/persistence/alembic/versions/20260916_0001_criar_usuarios.py` | supporting | source-code | schema-contract | python | linhas 1-14 | commit `f3979c4` |
| `src/backend/tests/test_infrastructure_usuario_mapping.py` | supporting | source-code | test | python | arquivo inteiro | commit `f3979c4` |
| `src/backend/tests/test_infrastructure_repositorio_usuario.py` | supporting | source-code | test | python | linhas 1-120 | commit `f3979c4` |
| `src/backend/api/perfil_estudante.py` | supporting | source-code | production | python | arquivo inteiro | commit `f3979c4` |
| `src/backend/api/cadastro_acesso.py` | supporting | source-code | production | python | linhas 134-149 | commit `f3979c4` |
| `src/backend/api/factory.py` | supporting | source-code | production | python | arquivo inteiro | commit `f3979c4` |
| `src/backend/main.py` | supporting | source-code | production | python | arquivo inteiro | commit `f3979c4` |

`subjects.kind` é `mixed` porque a demanda é curta e a decisão depende, em peso equivalente, do código de domínio existente e dos documentos de requisitos, segurança e modelagem.

### Limites da evidência dos artefatos

- A evidência corresponde ao estado do commit `f3979c41f2272deaa54aad8b160c9d27ff6e6255` (cabeça da `dev` na consulta). No momento da redação, o working tree da branch `task-113` já continha alterações locais não commitadas em `src/backend/domain/curriculo.py`, `src/backend/application/ports.py`, `src/backend/application/__init__.py` e um novo `src/backend/application/versao_curriculo.py`. Essas alterações implementam uma versão preliminar desta própria decisão, foram lidas por quem as propôs antes de serem aplicadas e **não** são tratadas como evidência.
- `curriculo.py` e `ports.py` foram lidos antes dessas alterações; os demais arquivos não aparecem modificados no working tree.
- Arquivos com recorte parcial (`requisitos-seguranca.md`, `requisitos_nao_funcionais.md`, `modelagem_der.md`, `casos-de-uso-v2.md`, `ports.py`, a migration `20260916_0001`, `test_infrastructure_repositorio_usuario.py` e `cadastro_acesso.py`) sustentam somente os fatos citados dos trechos indicados.
- A afirmação de que não existe porta, caso de uso, modelo ORM, migration ou rota de currículo além do domínio baseia-se na listagem de nomes dos arquivos Python de `src/backend` (somente nomes) e em busca textual por "curriculo" no código de produção; não resultou da leitura de todos os arquivos.
- A inexistência de criação de engine ou sessão da aplicação refere-se apenas aos arquivos examinados (`main.py`, `factory.py`, `env.py`). O `env.py` cria um engine exclusivamente para execução de migrations.
- Este documento foi redigido manualmente por um assistente seguindo as instruções de `.agents/skills/decision-analysis-v4/SKILL.md` e suas referências; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário e os documentos de análise existentes; o contexto da conversa não informou fuso explicitamente.

## Problema enriquecido

### Resultado desejado

Um estudante consegue alterar o título da versão, o layout e a visibilidade (`is_public`) de uma versão de currículo que lhe pertence. Edições inválidas e tentativas sobre versões de outro usuário são recusadas sem qualquer efeito. A entrega atravessa domínio, orquestração, persistência e interface HTTP, com testes unitários.

### Atores e interesses

- **Estudante dono da versão:** manter versões distintas de currículo para objetivos diferentes (caso de uso "Gerenciar versões").
- **Outro estudante:** não pode consultar nem alterar versão alheia (RNF04).
- **Equipe de backend:** receber uma fatia vertical coerente com a Clean Architecture, DDD e Code First exigidos.
- **Líder técnico e QA arquitetural:** verificar fronteiras entre camadas e registro da decisão.

### Evidências e fatos observados

1. `Curriculo` é um aggregate root **mutável** (`@dataclass(slots=True)`, sem `frozen`) com `id`, `usuario_id`, `titulo_versao`, `layout`, `is_public` e uma coleção interna de referências. `__post_init__` exige título não vazio e `is_public` booleano. `layout` é texto sem validação, pois "seus valores ainda não foram definidos". `incluir_referencia` e `remover_referencia` alteram o próprio agregado. O agregado não possui `deleted_at` (`src/backend/domain/curriculo.py`).
2. Não há porta de repositório, caso de uso, modelo ORM, migration nem rota para currículo (ver limites da evidência).
3. O DER define `CURRICULO` com `id`, `usuario_id` (FK), `titulo_versao`, `layout`, `is_public`, `created_at`, `updated_at` e `deleted_at`; `USUARIO` cria `CURRICULO`; seis tabelas de associação ligam currículos aos itens do perfil (`docs/modelagem_der.md`).
4. RF14 prevê que o estudante "crie, consulte, edite e exclua múltiplos currículos vinculados à sua conta"; RF13 exige autenticação; RNF04 exige proteção para que a alteração ocorra "somente por usuários autorizados" (`docs/requisitos_funcionais.md`, `docs/requisitos_nao_funcionais.md`). O caso de uso "Gerenciar versões" descreve versões distintas para objetivos diferentes (`docs/casos-de-uso-v2.md`).
5. O documento de segurança determina negar o acesso a recursos de outro usuário, verificar a propriedade sempre que um recurso for acessado, considerar tanto o identificador do currículo quanto o usuário autenticado e adotar negação por padrão (`docs/requisitos-seguranca.md`, seções 3.6 e 3.9).
6. A persistência existente cobre somente `usuarios` (colunas `id`, `nome`, `email`, `hash_senha`). `metadata.py` importa apenas `Base` do módulo de usuário; existe uma única migration (`20260916_0001`, `down_revision = None`); o teste de mapeamento verifica exatamente essas colunas; `RepositorioUsuarioSqlAlchemy` expõe `existe_por_email`, `salvar` e `obter_por_email`.
7. Não existe sessão nem token: a rota `/acessos` responde 204 sem criar sessão (`src/backend/api/cadastro_acesso.py`). As rotas atuais recebem o `usuario_id` no caminho, com a limitação já documentada no prompt de decisão do perfil.
8. `main.py` executa `create_app()` sem argumentos; `create_app` recebe os executores como parâmetros opcionais e os routers respondem 503 quando ausentes. Nos arquivos examinados não há criação de engine ou sessão da aplicação.
9. Precedentes de Application e Interface: `EditarPerfil` (busca, rejeita ausência ou exclusão, delega ao domínio, persiste) e a rota `PUT /estudantes/{usuario_id}` com mapeamento 200, 404, 409, 422 e 503.
10. O guia das skills recomenda decompor demandas em partes menores e não pedir a uma única skill que implemente áreas misturadas; domínio e orquestração pertencem a `$backend-domain-orchestration-v2`, e persistência e endpoints a `$backend-adapters-drivers-v2`.
11. `AGENTS.md` e `src/backend/AGENTS.md` exigem: dependências voltadas ao domínio; invariantes no domínio e alterações pela raiz do agregado; ORM Code First na camada de infraestrutura com migrations Alembic versionadas; DTOs na fronteira sem expor entidades; testes unitários com doubles no ambiente `backend`; execução de ferramentas via Nix; docstring com "o que faz, como faz e qual finalidade" em toda função e classe.

### Hipóteses

- **H1.** "Editar versão" significa alterar `titulo_versao`, `layout` e `is_public`. A composição da versão (referências aos itens do perfil) não faz parte desta edição.
- **H2.** A verificação de propriedade ocorre no caso de uso, e a negação é indistinguível de "não encontrado".
- **H3.** O `usuario_id` continua vindo do caminho da rota, como nas demais rotas, até que exista autenticação.
- **H4.** A persistência mapeia somente o que o domínio modela hoje (`id`, `usuario_id`, `titulo_versao`, `layout`, `is_public`), sem `created_at`, `updated_at` e `deleted_at`, seguindo o recorte adotado para `usuarios`.
- **H5.** O adapter reconstrói o agregado sem referências, porque as tabelas de associação não são persistidas nesta fatia, e `atualizar` altera somente as colunas escalares, sem tocar associações.
- **H6.** A criação de versões de currículo será outra fatia; esta fatia depende de existir a tabela `curriculos`, que ela mesma introduz.
- **H7.** Testes unitários com doubles bastam para esta entrega; a verificação contra banco real exigiria o ambiente `tests` e está fora do escopo.

### Perguntas em aberto

1. A persistência deve incluir `created_at`, `updated_at` e `deleted_at` agora (o DER os prevê) ou somente o que o domínio usa (H4)?
2. A negação por propriedade deve responder 404 (H2) ou 403? O documento de segurança diz "negar" sem definir o código.
3. Quais valores de `layout` são válidos? Hoje é texto livre (RF06 menciona "modelos de currículo com layouts profissionais").
4. Um currículo excluído logicamente (`deleted_at`) deve ser inalterável? O domínio ainda não modela essa condição.
5. A edição deve ser bloqueada quando o dono do currículo tem o perfil excluído? Hoje isso não é verificado em outros fluxos de recursos do perfil de forma consistente.
6. Haverá controle de concorrência (edições simultâneas) ou prevalece a última gravação?
7. Quem comporá engine, sessão e transação reais na raiz de composição, já que nenhuma fatia faz isso hoje?

### Escopo

- Método de edição no agregado `Curriculo` com validação antes da alteração.
- Porta `RepositorioCurriculo` com `obter_por_id` e `atualizar`.
- Caso de uso de edição com verificação de propriedade e exceção para ausência ou propriedade alheia.
- Modelo ORM, mapeador, adapter SQLAlchemy, registro na metadata e migration Alembic da tabela `curriculos`.
- Rota HTTP de edição, DTOs e registro em `factory.py`.
- Testes unitários de cada camada com doubles apropriados.

### Fora do escopo

- Criar, consultar, listar e excluir versões de currículo.
- Incluir ou remover itens (referências) da versão.
- Autenticação, sessão, derivação da identidade a partir de credencial e autorização geral.
- Composição de engine, sessão e transação reais na aplicação.
- Testes de integração com banco real e testes de sistema.
- Vocabulário de `layout`, geração, exportação e associação com vagas.
- Persistência das seis tabelas de associação e dos campos `created_at`, `updated_at` e `deleted_at` (sujeito à pergunta 1).
- Controle de concorrência otimista.

### Critérios de sucesso

- Editar título, layout e visibilidade de uma versão própria persiste o novo estado e preserva identidade, dono e referências.
- Título em branco ou visibilidade não booleana é recusado e não deixa o agregado parcialmente alterado.
- Versão inexistente e versão de outro usuário produzem a mesma falha e nenhuma atualização.
- A migration cria e remove somente `curriculos`, encadeada à revisão `20260916_0001`, e o modelo ORM coincide com a migration.
- Nenhuma camada interna depende de camada externa e nenhuma entidade é exposta pela API.
- A suíte unitária do ambiente `backend` passa sem acesso a banco, rede ou relógio reais.

## Restrições aplicáveis

- Domain não depende de Application, Infrastructure, API, frameworks ou ORM; Application não depende de Infrastructure nem da API (`src/backend/AGENTS.md`).
- Invariantes de negócio protegidas pelo domínio, com alterações pela raiz do agregado; formato e campos obrigatórios validados na fronteira (`src/backend/AGENTS.md`).
- Persistência relacional com ORM Code First; mapeamentos na infraestrutura; schema versionado por migrations Alembic; scripts SQL manuais não definem o schema (`src/backend/AGENTS.md`).
- DTOs não substituem entidades e entidades não são expostas pela API (`src/backend/AGENTS.md`).
- Toda mudança de comportamento inclui testes unitários; testes do domínio não dependem de banco, rede ou relógio (`src/backend/AGENTS.md`).
- Ferramentas de desenvolvimento executam pelo ambiente Nix correspondente; testes unitários rodam no ambiente `backend` (`AGENTS.md`).
- Toda função e classe tem docstring com o que faz, como faz e qual finalidade (`AGENTS.md`).
- Propriedade do recurso deve ser verificada e acesso a recurso de outro usuário deve ser negado (`docs/requisitos-seguranca.md`, `docs/requisitos_nao_funcionais.md`).
- Domínio e orquestração, de um lado, e adapters, de outro, são implementados por skills distintas; a análise não deve induzir uma única skill a implementar áreas misturadas (`docs/GUIA-DE-USO-DAS-SKILLS-v001.md`).

## Classificação comentada

- `sphere: engineering`: construção técnica de uma funcionalidade já definida pelos requisitos RF14 e RF02.
- `concerns: domain, security, data`: invariantes e transição do agregado; verificação de propriedade (RNF04); nova tabela e migration.
- `decision_kind: design`: decide-se como distribuir responsabilidades entre as camadas, e não se a funcionalidade existirá.
- `scope: component`: afeta o backend de currículos, com uma nova tabela.
- `lifecycle: delivery`, `urgency: normal`.
- `uncertainty: medium`: há perguntas abertas sobre campos persistidos, código de negação e concorrência.
- `reversibility: moderate`: a migration pode ser revertida enquanto a tabela não tiver dados, e passa a exigir migrations corretivas depois disso.
- `risk: medium`: uma falha de propriedade expõe a edição de currículos alheios; a gravidade é reduzida porque a identidade ainda não é autenticada (ver riscos).

## Decisão de roteamento

A análise foi roteada para `prompts/backend`. Candidatas consideradas: `prompts/backend` e `prompts/requisitos`. O propósito é decidir a construção de uma fatia de backend (domínio, casos de uso, persistência e API), e os artefatos principais são código de domínio e requisitos que análises anteriores sobre perfil, projetos e dados de contato já tratam em `prompts/backend`. `prompts/requisitos` foi descartada porque a análise não levanta nem refina requisitos. A confiança é alta. Não foram encontrados `AGENTS.md` ou `AGENTS.override.md` específicos em `prompts/backend` entre os arquivos de instrução localizados na raiz e em `src`.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | 1 | Maximizar a proteção das invariantes e da atomicidade da edição | Um estado inválido ou parcial persistido contamina currículos exportados |
| `security` | 1 | Garantir que somente o dono altere a versão | RNF04 e o princípio de negação por padrão |
| `simplicity` | 2 | Reutilizar padrões existentes, sem novas bibliotecas ou abstrações | O `AGENTS.md` proíbe abstrações hipotéticas |
| `modifiability` | 2 | Não impedir a adição posterior de timestamps, exclusão lógica e referências | A fatia de criação e as de itens evoluirão o mesmo agregado e a mesma tabela |
| `time-to-value` | 3 | Entregar em etapas testáveis na mesma branch | A reorganização em fatias verticais pede entregas completas e revisáveis |

## Alternativas consideradas

**Estado atual.** Existe apenas o agregado `Curriculo`. Não há como alterar uma versão por nenhuma interface.

**Alternativa A — Fatia vertical em quatro camadas com persistência mínima (recomendada).**

- *Domain:* `Curriculo.editar_versao(titulo_versao, layout, is_public)` valida os dados antes de alterar o agregado; a validação é compartilhada com `__post_init__`.
- *Application:* porta `RepositorioCurriculo` (`obter_por_id`, `atualizar`); caso de uso `EditarVersaoCurriculo`; exceção `CurriculoNaoEncontrado` para ausência e para propriedade de outro usuário.
- *Infrastructure:* modelo `CurriculoRegistro` (tabela `curriculos`: `id`, `usuario_id` com chave estrangeira para `usuarios.id`, `titulo_versao`, `layout`, `is_public`), mapeador, `RepositorioCurriculoSqlAlchemy`, registro na metadata e migration encadeada a `20260916_0001`.
- *Interface:* `PUT /estudantes/{usuario_id}/curriculos/{curriculo_id}` com DTOs próprios e mapeamento 200, 404, 422 e 503; registro em `factory.py`.
- *Testes:* unitários de domínio, caso de uso (spy do repositório), adapter (sessão simulada), mapeamento e migration (em memória) e rota (caso de uso real com doubles apenas nas portas).

Decisões internas e alternativas rejeitadas:

- *Como editar no domínio.* Escolhida a mutação do agregado após validação, coerente com `Curriculo` já mutável. Rejeitada a refatoração para agregado imutável com `replace`, como `Usuario`, por alterar métodos existentes sem necessidade. Rejeitada a atribuição direta de campos no caso de uso, por violar "alterações pela raiz do agregado".
- *Onde verificar propriedade.* Escolhida a verificação no caso de uso, testável com doubles. Rejeitado o filtro no repositório (`obter_por_id_e_usuario`), por colocar política de acesso no adapter, embora o documento de segurança sugira considerar id e usuário juntos; permanece como defesa em profundidade possível. Rejeitada a resposta 403, por revelar a existência do recurso.
- *O que persistir.* Escolhidas as colunas escalares do domínio (H4 e H5).

**Alternativa B — Fatia vertical com persistência completa do DER.** Além de A, incluir `created_at`, `updated_at`, `deleted_at`, as seis tabelas de associação e hidratação completa das referências.

**Alternativa C — Entregar Domain, Application e Interface sem persistência real.** Seguir o recorte das últimas tarefas (doubles apenas), sem modelo ORM nem migration. Não viola restrição dura, mas deixa de entregar a fatia vertical que a reorganização descrita pelo gestor pede.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | 1 | +1 | +1 | -1 | média | A e B verificam regra, atomicidade e contrato de persistência por testes unitários; C deixa o contrato de persistência sem verificação |
| `security` | 1 | +1 | +1 | 0 | baixa | A e B tornam `usuario_id` obrigatório com chave estrangeira; a propriedade é verificada no caso de uso nas três; a proteção real depende de autenticação, fora do escopo |
| `simplicity` | 2 | +1 | -2 | +2 | média | B soma seis tabelas, timestamps e hidratação completa; C não adiciona camada |
| `modifiability` | 2 | 0 | +1 | -1 | baixa | A exigirá migration e ajuste do adapter para timestamps e referências; B antecipa parte; C exigirá construir a persistência depois |
| `time-to-value` | 3 | +1 | -1 | 0 | média | A entrega uma fatia utilizável em etapas; B alonga a entrega; C entrega rápido, mas sem uso real fora dos testes |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**, entregue em etapas na mesma branch e no mesmo pull request: (1) Domain e Application com testes; (2) Infrastructure com testes; (3) Interface com testes. A edição altera título, layout e visibilidade; a propriedade é verificada no caso de uso e a negação equivale a "não encontrado" (H2); o `usuario_id` segue vindo da rota (H3); a persistência mapeia somente os campos escalares do domínio (H4 e H5). O status é `proposed`: a decisão exige aprovação humana, em especial sobre as perguntas 1 e 2.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | prioritized | Edição atômica e invariantes preservadas; contrato de persistência verificado | Teste de domínio que prova que nada muda quando a edição é recusada; testes de mapeamento e migration |
| `security` | prioritized | Versão de outro usuário não é alterada nem revelada | Teste do caso de uso com solicitante diferente do dono; limitação H3 mantém o ganho parcial até existir autenticação |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | Somente padrões já presentes no repositório, sem novas bibliotecas | Reutiliza o desenho de `EditarPerfil`, da rota de perfil, do mapeamento de `usuarios` e dos testes com doubles |
| `modifiability` | Não bloquear timestamps, exclusão lógica e referências futuros | Colunas adicionais entram por migration incremental; o adapter atualiza só escalares |
| `time-to-value` | Cada etapa testável isoladamente | Etapas por camada com suíte própria, todas na mesma branch |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `security` | Um estudante poderia alterar a versão de outro | Alta | Estudantes donos dos currículos |
| `correctness` | Título vazio ou estado parcial persistido; versões exportadas ou públicas com dados inválidos | Média | Estudantes e quem visualizar a versão pública |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `security` | Ausência e propriedade alheia usam a mesma falha; o cliente não distingue "não existe" de "não é seu" | Diagnóstico por quem consome a API | Aceitável pelo princípio de negação por padrão |
| `correctness` | O adapter hidrata `Curriculo` sem referências e atualiza só escalares | `modifiability` | Aceitável somente se documentado e se a fatia de referências estender o adapter |
| `simplicity` | Não persistir `created_at`, `updated_at` e `deleted_at` agora | `modifiability` | Aceitável sujeito à pergunta 1; exige migration posterior |

## Riscos e efeitos de segunda ordem

- **A verificação de propriedade é nominal enquanto a identidade vier do cliente.** O `usuario_id` e o `curriculo_id` chegam pela URL; quem conhecer ambos os identificadores consegue editar a versão. A verificação só impede erros e acessos cruzados acidentais. A proteção efetiva depende de autenticação e autorização (RF13, RNF04), previstas em handoff.
- **Agregado hidratado sem referências.** Uma fatia futura que reutilize `atualizar` depois de `incluir_referencia` perderia silenciosamente as referências, pois o adapter não as persiste. Mitigação: documentar na docstring do adapter e tratar na fatia de referências.
- **Múltiplas cabeças no Alembic.** Se outra fatia criar migration com o mesmo `down_revision` (`20260916_0001`), surgirão duas cabeças. Mitigação: integrar a `dev` antes de abrir o PR e coordenar a numeração das revisões.
- **Modelo ORM sem verificação contra banco real.** Testes unitários não detectam diferenças de dialeto ou da chave estrangeira. Mitigação: handoff para testes de integração no ambiente `tests`.
- **Nenhuma fatia compõe engine e sessão reais.** A rota continua respondendo 503 até que a composição exista, embora a fatia esteja completa nas quatro camadas.
- **Última gravação prevalece.** Sem controle de concorrência, duas edições simultâneas sobrescrevem uma à outra.
- **Referência de proveniência.** Os comentários `# Proveniência` do código apontam para o nome definitivo deste arquivo, incluindo o horário, e precisam ser conferidos após a gravação.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| A edição é atômica e preserva identidade, dono e referências | Estado do agregado após edição válida e inválida | Teste unitário de domínio | Falha de qualquer asserção de preservação |
| Propriedade alheia é negada sem efeito | Caso de uso lança a mesma exceção da ausência e não chama `atualizar` | Teste unitário do caso de uso com spy | Qualquer atualização observada para solicitante diferente do dono |
| O modelo ORM coincide com a migration | Colunas, tipos, nulabilidade e chave estrangeira iguais | Teste de metadata e migration em memória, no padrão do teste de `usuarios` | Divergência entre `CurriculoRegistro` e `upgrade()` |
| O adapter converte e atualiza somente escalares | Atributos alterados e `flush` aguardado em sessão simulada | Teste unitário com `MagicMock(spec=AsyncSession)` | Atributo extra alterado ou falha de propagação |
| A rota traduz falhas para status seguros | 200, 404, 422 e 503 | Teste unitário da rota com caso de uso real e doubles nas portas | Status diferente do contrato |
| Persistência funciona em banco real (H7) | Migration aplicada e consulta efetiva | Teste de integração no ambiente `tests` | Falha de DDL ou de chave estrangeira |
| Contrato de negação (404) é aceitável | Parecer do líder técnico e da equipe de segurança | Revisão humana | Decisão por 403 ou por filtro no repositório |

## Handoffs e atividades posteriores

- **`$backend-domain-orchestration-v2`:** `Curriculo.editar_versao`, porta `RepositorioCurriculo`, caso de uso `EditarVersaoCurriculo`, entrada, exceção `CurriculoNaoEncontrado` e testes unitários de domínio e Application.
- **`$backend-adapters-drivers-v2`:** modelo `CurriculoRegistro`, mapeador, `RepositorioCurriculoSqlAlchemy`, registro na metadata, migration encadeada a `20260916_0001`, rota `PUT /estudantes/{usuario_id}/curriculos/{curriculo_id}`, DTOs, registro em `factory.py` e testes unitários dessas unidades.
- **`$cross-cutting-implementation-v1`:** autenticação e autorização que forneçam a identidade a partir da sessão (RF13, RNF04), remoção do `usuario_id` do caminho e telemetria; reavaliar o código de resposta de negação.
- **`$integration-system-testing-v1`:** testes de integração do adapter e da migration contra banco real e testes de API da rota.
- **Composição:** definir quem implementa engine, sessão e transação da aplicação na raiz de composição, necessários para que qualquer fatia deixe de responder 503.
- **Próximas fatias:** criar, consultar, listar e excluir versões; incluir e remover itens da versão; tratar `created_at`, `updated_at` e `deleted_at` conforme a pergunta 1.
- **Decomposição:** se o time preferir, dividir esta análise em duas menores (domínio e orquestração; adapters e interface), conforme o guia das skills.
- **Rastreabilidade:** conferir se os comentários `# Proveniência` do código usam o nome definitivo deste arquivo.

## Síntese

A edição de versão de currículo é uma fatia vertical pequena e bem delimitada: o agregado `Curriculo` já existe e é mutável, mas nenhum outro elemento (porta, caso de uso, tabela, migration ou rota) existe. A decisão recomendada entrega as quatro camadas com persistência mínima, valida os dados no próprio agregado antes de alterá-lo e verifica a propriedade no caso de uso, negando versões alheias como "não encontradas". A principal limitação é que a identidade ainda vem da rota: enquanto não houver autenticação, a verificação de propriedade protege contra erros, mas não contra um cliente que conheça os dois identificadores. As perguntas sobre timestamps persistidos e sobre o código de negação (404 ou 403) devem ser respondidas antes da aprovação.
