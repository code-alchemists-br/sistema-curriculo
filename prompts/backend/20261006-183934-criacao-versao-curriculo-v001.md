---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-06T18:39:34-03:00"
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
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: markdown-with-mermaid
      analysis_scope: selected-section
      locator: "trechos que mencionam CURRICULO (linhas 11-35 e 104-169)"
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: partial
    - path: docs/casos-de-uso-v2.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "linhas 105-118 (caso de uso Gerenciar versões)"
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: partial
    - path: prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 130-170 (portas de geração de identidade) e 240-275 (RepositorioCurriculo); demais portas apenas por listagem de declarações"
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: partial
    - path: src/backend/application/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: available
    - path: src/backend/application/cadastro_projeto_academico.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "método executar do caso de uso (precedente de criação sem verificação do proprietário)"
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: partial
    - path: src/backend/application/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "classe CadastrarFormacaoAcademica (precedente de criação com verificação do proprietário)"
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: partial
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "declarações da classe e dos métodos assíncronos (por listagem)"
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: partial
    - path: src/backend/api/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: available
    - path: src/backend/api/projeto_academico.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "função criar_router (precedente de rota de criação com 201)"
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: partial
    - path: .github/workflows/ci.yml
      relationship: context
      representation: structured-data
      function: build
      format: yaml
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e1c4598bc92e9e0f5fccb356104fe22a3c"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "O propósito é decidir a construção de uma fatia de backend (caso de uso, persistência e API) sobre o agregado Curriculo; a análise relacionada de edição de versão está em prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, security, architecture]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: medium
---

# Análise de decisão — criação de versão de currículo (fatia vertical)

## Solicitação original

Texto literal fornecido pelo usuário:

```text
Implementar criação de versão de currículo
#109
Tarefa da fatia vertical atribuída a @regazzio. Inclua os testes unitários pertinentes.
```

O identificador `#109` foi informado na solicitação; a branch de trabalho criada a partir da `dev` chama-se `task-109`.

## Informações complementares

Insumos literais registrados na conversa que originou esta análise (a grafia original foi preservada):

- Mensagem do gestor do projeto, reproduzida pelo usuário em conversa anterior: "No começo as coisas não estavam muito bem definidas, mas agora as funcionalidades já são claras. Os time serão reorganizados para lidar com slices verticais agora ao invés de horizontais. Isso só afeta backend. Frontend fica do mesmo jeito"
- Comentário do usuário sobre a tarefa anterior, tomado como sinal de preferência por entregas menores: "descricao menor, dá? to achando muito grande esse PR"
- Análise relacionada, já aprovada e mergeada com a edição de versão: `prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md`. Esta análise é independente e não a revisa.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/domain/curriculo.py` | primary | source-code | production | python | arquivo inteiro | commit `388fa9e` |
| `docs/requisitos_funcionais.md` | primary | prose | documentation | markdown | arquivo inteiro | commit `388fa9e` |
| `docs/modelagem_der.md` | supporting | diagram-model | schema-contract | markdown-with-mermaid | trechos com CURRICULO (linhas 11-35 e 104-169) | commit `388fa9e` |
| `docs/casos-de-uso-v2.md` | supporting | prose | documentation | markdown | linhas 105-118 | commit `388fa9e` |
| `prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `388fa9e` |
| `src/backend/application/ports.py` | supporting | source-code | production | python | linhas 130-170 e 240-275, mais listagem de declarações | commit `388fa9e` |
| `src/backend/application/versao_curriculo.py` | supporting | source-code | production | python | arquivo inteiro | commit `388fa9e` |
| `src/backend/application/cadastro_projeto_academico.py` | supporting | source-code | production | python | método `executar` | commit `388fa9e` |
| `src/backend/application/perfil_estudante.py` | supporting | source-code | production | python | classe `CadastrarFormacaoAcademica` | commit `388fa9e` |
| `src/backend/infrastructure/persistence/sqlalchemy/curriculo.py` | supporting | source-code | production | python | arquivo inteiro | commit `388fa9e` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py` | supporting | source-code | production | python | arquivo inteiro | commit `388fa9e` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py` | supporting | source-code | production | python | declarações de métodos (listagem) | commit `388fa9e` |
| `src/backend/api/versao_curriculo.py` | supporting | source-code | production | python | arquivo inteiro | commit `388fa9e` |
| `src/backend/api/projeto_academico.py` | supporting | source-code | production | python | função `criar_router` | commit `388fa9e` |
| `.github/workflows/ci.yml` | context | structured-data | build | yaml | arquivo inteiro | commit `388fa9e` |
| `AGENTS.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `388fa9e` |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `388fa9e` |

`subjects.kind` é `mixed` porque a demanda é curta e a decisão depende, em peso equivalente, do código existente e dos requisitos.

### Limites da evidência dos artefatos

- A evidência corresponde ao estado do commit `388fa9e1c4598bc92e9e0f5fccb356104fe22a3c` (cabeça da `dev` na consulta), com a árvore de trabalho da branch `task-109` limpa.
- Arquivos com recorte parcial sustentam somente os fatos citados dos trechos indicados. Em `repositorio_usuario.py`, o recorte é a listagem de declarações; o corpo dos métodos não foi relido nesta consulta e o conteúdo de `usuario.py` (mapeamento) foi examinado em consulta anterior da mesma sessão, sem alteração do arquivo desde então (último commit em 2026-09-20).
- A inexistência de adapter de geração de identidade baseia-se em busca textual por `uuid4` e `Gerador` nos arquivos de produção fora de `application` e `domain`; não resultou da leitura de todos os arquivos.
- A afirmação de que métodos não implementados de um adapter que herda explicitamente de um `Protocol` retornam `None` é **inferência** sobre o comportamento da linguagem, não verificada por execução neste ambiente.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md` e suas referências; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário e os documentos de análise existentes.

## Problema enriquecido

### Resultado desejado

Um estudante consegue criar uma nova versão de currículo informando título, layout e visibilidade, e a versão fica persistida e vinculada a ele. Dados inválidos são recusados sem efeito. A entrega atravessa Application, Infrastructure e Interface, com testes unitários.

### Atores e interesses

- **Estudante:** manter versões distintas de currículo para objetivos diferentes (caso de uso "Gerenciar versões").
- **Equipe de backend:** receber uma fatia vertical coerente com a Clean Architecture e, de preferência, pequena para revisão.
- **Equipe da área de perfil:** não ter o adapter de usuário alterado em paralelo por outra fatia.
- **Líder técnico e QA arquitetural:** verificar fronteiras entre camadas e o registro da decisão.

### Evidências e fatos observados

1. `Curriculo` valida na construção título não vazio e visibilidade booleana, tem `layout` como texto livre e já possui `editar_versao`. Criar uma versão equivale a construir o agregado com uma nova identidade (`src/backend/domain/curriculo.py`).
2. RF14 prevê que o estudante "crie, consulte, edite e exclua múltiplos currículos vinculados à sua conta"; o caso de uso "Gerenciar versões" descreve versões distintas para objetivos diferentes (`docs/requisitos_funcionais.md`, `docs/casos-de-uso-v2.md`). O DER define `CURRICULO` com `usuario_id` (FK), `titulo_versao`, `layout`, `is_public` e timestamps (`docs/modelagem_der.md`).
3. A porta `RepositorioCurriculo` declara somente `obter_por_id` e `atualizar`; não há `salvar` nem porta de geração de identidade de currículo (`src/backend/application/ports.py`).
4. A tabela `curriculos` já possui todas as colunas necessárias e a chave estrangeira para `usuarios`. O adapter implementa `obter_por_id` e `atualizar`, e o módulo de mapeamento converte registro em agregado, mas não agregado em registro (`.../sqlalchemy/curriculo.py`, `.../repositorio_curriculo.py`).
5. Nenhum `Gerador*Id` possui adapter em produção: a busca por `uuid4` e `Gerador` fora de `application` e `domain` não encontrou nada.
6. O time tem dois precedentes de criação: **projeto acadêmico** gera a identidade por porta, constrói a entidade e salva, sem consultar o proprietário; **formação acadêmica** consulta o proprietário por `RepositorioUsuario.obter_por_id` e rejeita ausência ou exclusão (`cadastro_projeto_academico.py`, `perfil_estudante.py`).
7. `RepositorioUsuarioSqlAlchemy` declara `existe_por_email`, `salvar` e `obter_por_email`, mas herda explicitamente de `RepositorioUsuario`, cuja porta também declara `obter_por_id` e `atualizar`. A tabela `usuarios` não possui `deleted_at`, e o mapeamento de usuário não reconstrói exclusão lógica (examinado em consulta anterior da sessão; arquivo sem alteração desde 2026-09-20).
8. A rota de criação de projeto acadêmico responde 201 com DTO próprio, 422 para violação de domínio e 503 sem executor (`api/projeto_academico.py`). A rota de edição de versão já define `VersaoCurriculoResposta` e o contrato de executor, e `criar_router` recebe um único executor (`api/versao_curriculo.py`).
9. Não há autenticação nem sessão: as rotas recebem `usuario_id` no caminho, e `main.py` executa `create_app()` sem executores, de modo que as rotas respondem 503 na aplicação real (análise relacionada, fatos 7 e 8).
10. O CI executa `python -m unittest discover` do backend em todo pull request (`.github/workflows/ci.yml`).
11. `AGENTS.md` e `src/backend/AGENTS.md` exigem dependências voltadas ao domínio, invariantes no domínio, ORM Code First com migrations, DTOs na fronteira, testes unitários com doubles no ambiente `backend` e docstring com "o que faz, como faz e qual finalidade".

### Hipóteses

- **H1.** "Criar versão" cria uma versão **sem referências** aos itens do perfil; incluir itens é outra fatia.
- **H2.** `titulo_versao` e `layout` são obrigatórios e `is_public` é opcional, com padrão `False` (privada por padrão).
- **H3.** Não há limite de versões por estudante nem exigência de títulos únicos, pois os requisitos não os definem.
- **H4.** A identidade é gerada no servidor por uma porta (`GeradorCurriculoId`) com adapter UUID4; o cliente não escolhe o id.
- **H5.** A criação não exige nova migration: a tabela existente cobre os campos do domínio.
- **H6.** O proprietário é o `usuario_id` do caminho da rota, como nas demais rotas, até existir autenticação.
- **H7.** A criação não consulta o proprietário no caso de uso; a chave estrangeira é a barreira de integridade (Alternativa A).
- **H8.** A resposta de criação reutiliza o mesmo DTO público da edição e usa o status 201.

### Perguntas em aberto

1. O caso de uso deve verificar existência e exclusão do proprietário (Alternativa B) ou confiar na chave estrangeira (Alternativa A)?
2. Deve existir limite de versões por estudante ou unicidade de título?
3. A visibilidade padrão `False` é aceita?
4. Quais valores de `layout` são válidos (RF06 menciona "modelos de currículo com layouts profissionais")? Hoje é texto livre.
5. Quem implementa `obter_por_id`, `atualizar` e `deleted_at` no adapter de usuário, e quando? A fatia de criação só poderá adotar a Alternativa B depois disso.
6. A rota aninhada `POST /estudantes/{usuario_id}/curriculos` é aceitável, ou o time prefere outro caminho?

### Escopo

- Porta `GeradorCurriculoId` e método `salvar` na porta `RepositorioCurriculo`.
- Caso de uso de criação com entrada própria.
- Conversão de agregado para registro, `salvar` no adapter SQLAlchemy e adapter UUID4 de geração de identidade.
- Rota `POST` de criação, DTO de requisição, registro no `factory.py`.
- Testes unitários de cada camada com doubles apropriados.

### Fora do escopo

- Consultar, listar e excluir versões; incluir ou remover itens da versão; duplicar uma versão existente.
- Verificação de existência e exclusão do proprietário (ver pergunta 1).
- Autenticação, sessão e autorização; composição de engine, sessão e transação reais.
- Nova migration, timestamps e persistência das associações com itens do perfil.
- Limite de versões, unicidade de título e vocabulário de `layout`.
- Testes de integração com banco real.

### Critérios de sucesso

- Criar uma versão válida gera uma identidade nova, constrói o agregado, solicita o salvamento uma única vez e devolve a versão criada.
- Título em branco ou visibilidade inválida é recusado pelo domínio antes de qualquer salvamento.
- O adapter insere a linha com todas as colunas e envia a alteração à sessão sem commit; o mapeamento reproduz as colunas do modelo.
- O adapter de identidade devolve um `CurriculoId` com UUID válido e distinto a cada chamada.
- A rota responde 201 com dados públicos, 422 para dado inválido e 503 sem executor.
- A suíte unitária do ambiente `backend` passa, inclusive no CI, sem banco, rede ou relógio reais.

## Restrições aplicáveis

- Domain não depende de Application, Infrastructure, API, frameworks ou ORM; Application não depende de Infrastructure nem da API (`src/backend/AGENTS.md`).
- Invariantes de negócio ficam no domínio; formato e campos obrigatórios são validados na fronteira; entidades não são expostas pela API (`src/backend/AGENTS.md`).
- Persistência com ORM Code First, mapeamentos na infraestrutura e schema por migrations Alembic (`src/backend/AGENTS.md`).
- Toda mudança de comportamento inclui testes unitários executados no ambiente Nix `backend`; ferramentas de desenvolvimento rodam via Nix (`AGENTS.md`).
- Toda função e classe tem docstring com o que faz, como faz e qual finalidade (`AGENTS.md`).
- Não introduzir abstrações apenas para necessidade hipotética (`src/backend/AGENTS.md`); a única abstração nova é a porta de geração de identidade, exigida pelo padrão de testes determinísticos já adotado.

## Classificação comentada

- `sphere: engineering`: construção técnica de funcionalidade definida por RF14.
- `concerns: domain, security, architecture`: construção do agregado; propriedade nominal do recurso; primeira implementação de um adapter de identidade e dependência entre fatias.
- `decision_kind: design`, `scope: component`, `lifecycle: delivery`, `urgency: normal`.
- `uncertainty: medium`: há perguntas abertas sobre verificação do proprietário, limites e visibilidade padrão.
- `reversibility: easy`: não há mudança de schema e a verificação do proprietário pode ser acrescentada depois sem quebrar a API.
- `risk: medium`: sem autenticação, qualquer cliente cria versões em nome de qualquer `usuario_id`; o impacto fica limitado a criar registros próprios do estudante informado.

## Decisão de roteamento

Roteada para `prompts/backend`, a mesma pasta da análise relacionada de edição de versão. Candidatas: `prompts/backend` e `prompts/requisitos`; esta última foi descartada porque a análise não levanta nem refina requisitos. Confiança alta. Não foram encontrados `AGENTS.md` ou `AGENTS.override.md` específicos em `prompts/` (busca por nome de arquivo na árvore de trabalho, feita nesta consulta).

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | 1 | Nenhuma versão órfã e nenhum estado inválido persistido | A versão criada é a base de currículos exportados |
| `security` | 1 | Não ser pior que a edição; propriedade ao menos nominal | RNF04 e negação por padrão |
| `simplicity` | 2 | Reutilizar padrões existentes e manter o PR pequeno | O usuário sinalizou que o PR anterior foi considerado grande |
| `team-autonomy` | 2 | Não alterar o adapter de usuário, de outra fatia | Evita conflitos e retrabalho com a área de perfil |
| `time-to-value` | 3 | Entregar em etapas testáveis na mesma branch | A reorganização em fatias verticais pede entregas revisáveis |

## Alternativas consideradas

**Estado atual.** Existe o agregado e a tabela, mas não há como criar uma versão por nenhuma interface, e nenhuma identidade de currículo é gerada.

**Alternativa A — Fatia vertical enxuta, sem verificar o proprietário no caso de uso (recomendada).**

- *Application:* porta `GeradorCurriculoId`; método `salvar` em `RepositorioCurriculo`; `CriarVersaoCurriculoEntrada` e `CriarVersaoCurriculo`, que geram a identidade, constroem o `Curriculo` (o domínio valida) e só então salvam.
- *Infrastructure:* `para_registro` e `salvar` (`add` e `flush`, sem commit) no adapter de currículo; `GeradorCurriculoIdUuid4`, primeiro adapter de identidade do projeto.
- *Interface:* `POST /estudantes/{usuario_id}/curriculos` no router de versões, com 201, 422 e 503; `criar_router` passa a receber também o executor de criação, com valor padrão `None`, e `create_app` ganha o parâmetro correspondente.
- Sem migration e sem mudança no adapter de usuário.

**Alternativa B — Alternativa A mais verificação do proprietário (como `CadastrarFormacaoAcademica`).** O caso de uso consulta `RepositorioUsuario.obter_por_id` e rejeita ausência ou exclusão com as exceções de perfil existentes. Exige implementar `obter_por_id` no adapter de usuário, hoje ausente, e depende de `deleted_at` para a regra de exclusão ter efeito real.

**Alternativa C — Entregar só Application e Interface com doubles, sem persistência.** Segue o recorte das últimas fatias, mas não entrega a fatia vertical pedida e deixa o contrato de persistência sem verificação.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | 1 | 0 | +1 | -1 | média | A e B impedem versão órfã (FK) e estado inválido (domínio); B transforma proprietário inexistente em falha de negócio em vez de erro de infraestrutura; C não verifica persistência |
| `security` | 1 | 0 | 0 | 0 | baixa | O ganho extra de B (rejeitar proprietário excluído) não é realizável hoje porque `deleted_at` não é persistido; a propriedade segue nominal nas três |
| `simplicity` | 2 | +1 | -1 | +2 | média | B acrescenta dependência de repositório de usuário, método novo no adapter de usuário e mais testes; C não adiciona camada |
| `team-autonomy` | 2 | +1 | -1 | +1 | média | B altera `repositorio_usuario.py`, área de outra fatia, com risco de conflito |
| `time-to-value` | 3 | +1 | -1 | 0 | média | A entrega uma fatia completa e pequena; C entrega rápido, mas sem uso real fora dos testes |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**, entregue em etapas na mesma branch e no mesmo pull request: (1) Application com testes; (2) Infrastructure com testes; (3) Interface com testes. A criação gera a identidade por porta, constrói o agregado (o domínio valida) e salva; a visibilidade padrão é `False` (H2); o proprietário vem do caminho da rota (H6) e a integridade é garantida pela chave estrangeira (H7). A verificação do proprietário (Alternativa B) fica como evolução aditiva, a ser feita quando o adapter de usuário implementar `obter_por_id` e persistir `deleted_at`. O status é `proposed`: a decisão exige aprovação humana, em especial sobre a pergunta 1.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `simplicity` | prioritized | PR pequeno, sem migration e sem alterar arquivos de outra fatia | A entrega toca somente arquivos de currículo e os pontos de composição já existentes |
| `team-autonomy` | prioritized | Nenhuma alteração no adapter de usuário | Alternativa B exigiria `obter_por_id` em `repositorio_usuario.py` |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `correctness` | Nenhuma versão órfã e nenhum estado inválido persistido | O domínio valida antes de `salvar`; a chave estrangeira impede proprietário inexistente no banco |
| `security` | Não ser pior que a edição | A propriedade segue nominal, como na edição; nenhum dado de outro estudante é lido ou alterado pela criação |
| `time-to-value` | Cada etapa testável isoladamente | Etapas por camada com suíte própria, na mesma branch |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | Versões sem dono válido ou com título vazio persistidas | Alta | Estudantes e quem visualizar a versão |
| `simplicity` | PR extenso e difícil de revisar | Média | Revisores e o autor |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` e `team-autonomy` | Proprietário inexistente vira erro de integridade do banco, e não uma falha de negócio traduzida | `correctness` | Aceitável enquanto a composição real não existir e até a fatia de perfil entregar `obter_por_id`; deve ser tratada nessa evolução |
| `simplicity` e `team-autonomy` | Proprietário excluído logicamente ainda pode criar versões | `security` | Aceitável porque `deleted_at` não é persistido hoje; depende da fatia de perfil |
| `simplicity` | Sem limite de versões nem unicidade de título | `correctness` | Aceitável pelas hipóteses H3; sujeito à pergunta 2 |

## Riscos e efeitos de segunda ordem

- **Proprietário inexistente.** Hoje a criação em nome de um `usuario_id` desconhecido falharia no banco, e essa falha chegaria ao cliente como erro genérico quando houver composição real. Mitigação: evolução para a Alternativa B.
- **Criação em nome de qualquer usuário.** Como a identidade vem da URL, qualquer cliente pode criar versões em nome de um `usuario_id` conhecido. Mitigação: autenticação e autorização (handoff).
- **Adapter de usuário possivelmente incompleto (inferência).** Como `RepositorioUsuarioSqlAlchemy` herda explicitamente do `Protocol`, os métodos não sobrescritos (`obter_por_id`, `atualizar`) seriam os do `Protocol`, que não têm corpo e devolveriam `None`. Se confirmado, qualquer caso de uso de perfil composto com esse adapter trataria todo usuário como inexistente. Não afeta esta fatia, mas deve ser verificado pela equipe de perfil.
- **Primeiro adapter de identidade.** Define o local e o nome de um padrão que outras fatias provavelmente reutilizarão. Mitigação: nome e local específicos de currículo, sem generalização antecipada.
- **Gravação sem commit.** `salvar` envia a inserção à sessão sem commit; sem composição real ninguém confirma a transação. Mitigação: mesma política do adapter de edição, documentada na docstring.
- **Sinais de PR grande.** Se o PR ultrapassar o tamanho desejado, o corte natural é por etapa (um commit por camada).

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| A criação valida antes de salvar | O repositório não recebe chamada de `salvar` quando o domínio recusa os dados | Teste unitário do caso de uso com spy do repositório | Qualquer `salvar` com dado inválido |
| A identidade é gerada por porta e usada no agregado | O agregado devolvido usa o id do stub | Teste unitário do caso de uso com stub de identidade | Id divergente do stub |
| O adapter insere a linha e envia à sessão sem commit | `add` com os valores corretos e `flush` aguardado | Teste unitário com `MagicMock(spec=AsyncSession)` | Colunas ausentes, falta de `flush` ou uso de commit |
| O adapter de identidade é válido e distinto | UUID versão 4 e valores diferentes entre chamadas | Teste unitário do adapter | Repetição de valores ou tipo diferente de `CurriculoId` |
| A rota traduz falhas para status seguros | 201, 422 e 503 | Teste unitário da rota com caso de uso real e doubles nas portas | Status diferente do contrato |
| Proprietário inexistente é aceitável nesta fatia (H7) | Parecer do líder técnico e da equipe de perfil | Revisão humana | Decisão pela Alternativa B antes do merge |
| Persistência funciona em banco real | Inserção efetiva e violação de chave estrangeira observada | Teste de integração no ambiente `tests` | Falha de inserção ou comportamento diferente do esperado |

## Handoffs e atividades posteriores

- **`$backend-domain-orchestration-v2`:** porta `GeradorCurriculoId`, método `salvar` em `RepositorioCurriculo`, `CriarVersaoCurriculoEntrada`, `CriarVersaoCurriculo` e testes unitários.
- **`$backend-adapters-drivers-v2`:** `para_registro`, `salvar` no adapter, `GeradorCurriculoIdUuid4`, rota `POST`, DTO de requisição, registro em `factory.py` e testes unitários dessas unidades.
- **Equipe de perfil:** implementar `obter_por_id`, `atualizar` e `deleted_at` no adapter de usuário e verificar a inferência sobre os métodos herdados do `Protocol`. Depois disso, acrescentar a verificação do proprietário na criação (Alternativa B).
- **`$cross-cutting-implementation-v1`:** autenticação e autorização que forneçam a identidade a partir da sessão e removam o `usuario_id` do caminho.
- **`$integration-system-testing-v1`:** testes de integração do adapter contra banco real, incluindo a violação de chave estrangeira.
- **Composição:** definir quem compõe engine, sessão e transação reais, já que nenhuma fatia faz isso hoje.
- **Próximas fatias:** consultar, listar e excluir versões; incluir e remover itens da versão; limite de versões e unicidade de título, conforme a pergunta 2.
- **Rastreabilidade:** conferir se os comentários `# Proveniência` do código usam o nome definitivo deste arquivo.

## Síntese

A criação de versão de currículo é uma fatia pequena: o agregado, a tabela e a rota de edição já existem, e faltam a geração de identidade, o salvamento e a rota de criação. A decisão recomendada entrega Application, Infrastructure e Interface sem migration e sem tocar o adapter de usuário, deixando a verificação do proprietário como evolução aditiva, porque o ganho de segurança dela (rejeitar proprietário excluído) ainda não é realizável sem `deleted_at` persistido. A principal limitação é que um proprietário inexistente falharia no banco em vez de virar uma falha de negócio, e que a identidade ainda vem da rota. A pergunta sobre verificar o proprietário agora ou depois deve ser respondida antes da aprovação.
