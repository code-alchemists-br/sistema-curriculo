---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-07T19:08:14-03:00"
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
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "alias IdItemPerfil e classe ReferenciaCurriculo"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: src/backend/domain/itens_perfil.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "declarações das seis entidades de item e de seus campos (por listagem)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: src/backend/domain/__init__.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "nomes exportados relativos a currículo e referência (por listagem)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: docs/modelagem_der.md
      relationship: primary
      representation: diagram-model
      function: schema-contract
      format: markdown-with-mermaid
      analysis_scope: selected-section
      locator: "linhas 17-34 (relacionamentos de associação) e 117-146 (tabelas de associação)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: docs/mapeamento_jornadas.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "linhas 40-60 (casos de uso relacionados à jornada) e menções a seleção por busca textual"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: docs/wireframes/07-revisao.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: docs/wireframes/02-painel-inicial.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "linhas 1-40"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: prompts/backend/20260914-camada-dominio-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "linhas 164-168, 188-195, 238-244 e 405-418 (associações, propriedade transagregados, ordenação, remoção de itens)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "declarações de portas de repositório e de geração (por listagem) e classes RepositorioCurriculo e GeradorCurriculoId"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: src/backend/application/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261005_0002_criar_curriculos.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: python
      analysis_scope: metadata-only
      locator: "nome e existência no diretório de revisões; conteúdo não relido nesta consulta"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: src/backend/api/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: src/backend/tests/fixtures/curriculo_exportacao.py
      relationship: context
      representation: source-code
      function: data-fixture
      format: python
      analysis_scope: selected-section
      locator: "linhas 1-45 e trechos que constroem Curriculo e chamam incluir_referencia (por listagem)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: README.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "linhas da tabela de responsabilidades da equipe relativas a perfil, itens e versões"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: .agents/skills/backend-domain-orchestration-v2/SKILL.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: .agents/skills/backend-adapters-drivers-v2/SKILL.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "O propósito é decidir a construção de uma fatia de backend (portas, casos de uso, persistência e API) sobre o agregado Curriculo; as análises relacionadas de criação e edição de versão estão em prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, security, data]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: high
---

# Análise de decisão — seleção de itens da versão de currículo

## Solicitação original

Texto literal fornecido pelo usuário:

```text
Implementar seleção de itens da versão de currículo, Inclua os testes unitários pertinentes.
```

O número da tarefa e a indicação de "fatia vertical" não constam na solicitação desta vez (as tarefas anteriores traziam "Tarefa da fatia vertical"). O identificador informado depois pelo usuário, na conversa, foi 117 (branch `task-117`), junto com a orientação de implementar uma etapa por vez.

## Informações complementares

Insumos literais registrados na conversa que originou esta análise (a grafia original foi preservada):

- Respostas do usuário às duas perguntas de escopo feitas antes desta análise: persistência por "Tabela única curriculo_itens (Recomendada)" e operações "Selecionar e desselecionar (Recomendada)".
- Comentário do usuário sobre uma tarefa anterior, tomado como sinal de preferência por entregas menores: "descricao menor, dá? to achando muito grande esse PR"
- Mensagem do gestor do projeto, reproduzida pelo usuário em conversa anterior: "No começo as coisas não estavam muito bem definidas, mas agora as funcionalidades já são claras. Os time serão reorganizados para lidar com slices verticais agora ao invés de horizontais. Isso só afeta backend. Frontend fica do mesmo jeito"
- Análises relacionadas, já mergeadas: `prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md` e `prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md`. Esta análise é independente e não as revisa.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/domain/curriculo.py` | primary | source-code | production | python | arquivo inteiro | commit `e711a98` |
| `src/backend/domain/value_objects.py` | primary | source-code | production | python | `IdItemPerfil` e `ReferenciaCurriculo` | commit `e711a98` |
| `src/backend/domain/itens_perfil.py` | supporting | source-code | production | python | declarações (listagem) | commit `e711a98` |
| `src/backend/domain/__init__.py` | supporting | source-code | production | python | exportações (listagem) | commit `e711a98` |
| `docs/modelagem_der.md` | primary | diagram-model | schema-contract | markdown-with-mermaid | linhas 17-34 e 117-146 | commit `e711a98` |
| `docs/requisitos_funcionais.md` | supporting | prose | documentation | markdown | arquivo inteiro | commit `e711a98` |
| `docs/mapeamento_jornadas.md` | supporting | prose | documentation | markdown | linhas 40-60 e busca textual | commit `e711a98` |
| `docs/wireframes/07-revisao.md` | supporting | prose | documentation | markdown | arquivo inteiro | commit `e711a98` |
| `docs/wireframes/02-painel-inicial.md` | context | prose | documentation | markdown | linhas 1-40 | commit `e711a98` |
| `prompts/backend/20260914-camada-dominio-v001.md` | supporting | prose | documentation | markdown | linhas 164-168, 188-195, 238-244 e 405-418 | commit `e711a98` |
| `src/backend/application/ports.py` | supporting | source-code | production | python | portas de repositório/geração e currículo | commit `e711a98` |
| `src/backend/application/versao_curriculo.py` | supporting | source-code | production | python | arquivo inteiro | commit `e711a98` |
| `src/backend/infrastructure/persistence/sqlalchemy/curriculo.py` | supporting | source-code | production | python | arquivo inteiro | commit `e711a98` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py` | supporting | source-code | production | python | arquivo inteiro | commit `e711a98` |
| `.../alembic/versions/20261005_0002_criar_curriculos.py` | supporting | source-code | schema-contract | python | somente nome e existência | commit `e711a98` |
| `src/backend/api/versao_curriculo.py` | supporting | source-code | production | python | arquivo inteiro | commit `e711a98` |
| `src/backend/api/factory.py` | supporting | source-code | production | python | arquivo inteiro | commit `e711a98` |
| `src/backend/tests/fixtures/curriculo_exportacao.py` | context | source-code | data-fixture | python | linhas 1-45 e trechos com `incluir_referencia` | commit `e711a98` |
| `README.md` | context | prose | documentation | markdown | linhas de responsabilidades da equipe | commit `e711a98` |
| `prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md` | context | prose | documentation | markdown | arquivo inteiro | commit `e711a98` |
| `prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md` | context | prose | documentation | markdown | arquivo inteiro | commit `e711a98` |
| `.agents/skills/backend-domain-orchestration-v2/SKILL.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `e711a98` |
| `.agents/skills/backend-adapters-drivers-v2/SKILL.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `e711a98` |
| `AGENTS.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `e711a98` |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `e711a98` |

`subjects.kind` é `mixed` porque a demanda é curta e a decisão depende, em peso equivalente, do agregado existente, do DER e das decisões de domínio já registradas.

### Limites da evidência dos artefatos

- A evidência corresponde ao estado do commit `e711a98bac2de4b1477d6d1939989dddab794e6a` (cabeça da `dev` na consulta). O working tree examinado estava na branch local `task-109` (já mergeada); `git diff --stat` entre ela e a `dev` não mostrou diferença em `src/backend/domain`, `application`, `infrastructure` nem `api`, de modo que o conteúdo lido coincide com o da `dev` para esses arquivos.
- O fixture de exportação foi lido a partir da `dev` (`git show`), pois ainda não estava no working tree.
- Arquivos com recorte parcial sustentam somente os fatos citados dos trechos indicados.
- A inexistência de tabelas e de portas de consulta para os itens baseia-se na listagem de `__tablename__` em `src/backend/infrastructure`, na listagem das revisões Alembic e na listagem de declarações de portas; não resultou da leitura de todos os arquivos.
- A migration `20261005_0002` foi examinada somente por nome; o seu conteúdo é conhecido de análise anterior.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md` e suas referências; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário e os documentos de análise existentes.

## Problema enriquecido

### Resultado desejado

Um estudante consegue selecionar e desselecionar, para uma versão de currículo sua, os itens do seu próprio perfil (formação, experiência, projeto, competência, idioma e documento) que compõem essa versão, e a seleção fica persistida. Item inexistente ou de outro usuário é recusado sem efeito. A entrega atravessa Application, Infrastructure e Interface, com testes unitários.

### Atores e interesses

- **Estudante dono da versão:** montar versões distintas com conjuntos diferentes de itens (caso de uso "Gerenciar versões").
- **Outro estudante:** seus itens não podem ser incluídos em versão alheia (RNF04).
- **Equipes responsáveis pelos itens (perfil, formação, experiências; informações complementares e documentos):** serão donas das consultas de propriedade e das tabelas dos itens.
- **Equipe de backend e líder técnico:** fronteiras entre camadas, tamanho do PR e registro da decisão.

### Evidências e fatos observados

1. `Curriculo` já encapsula as referências: `incluir_referencia` rejeita duplicata, `remover_referencia` rejeita item ausente e `referencias` expõe um `frozenset` (`src/backend/domain/curriculo.py`). `ReferenciaCurriculo` aceita somente os identificadores dos seis tipos de item e **não consulta outros agregados**; a docstring afirma que a propriedade do item é regra transagregados (`src/backend/domain/value_objects.py`).
2. O prompt de domínio da equipe determina que a regra "referência e currículo pertencem ao mesmo usuário" atravessa agregados e que "o caso de uso deve coordená-la por portas", e que as tabelas de associação poderiam ganhar ordenação ou customização, o que exigiria reavaliar a decisão "antes de migrations e contratos públicos" (`prompts/backend/20260914-camada-dominio-v001.md`). Perguntas em aberto lá: ordenação ou personalização por versão e política de remoção de itens referenciados.
3. O DER prevê seis tabelas de associação (`CURRICULO_FORMACAO`, `_EXPERIENCIA`, `_PROJETO`, `_COMPETENCIA`, `_IDIOMA`, `_DOCUMENTO`), cada uma com `curriculo_id` e o identificador do item, ambos chave estrangeira (`docs/modelagem_der.md`).
4. O banco possui somente as tabelas `usuarios` e `curriculos`; **nenhum dos seis itens tem tabela, modelo ORM ou migration** (listagem de `__tablename__` e de revisões).
5. Nenhum item tem porta de consulta: as portas existentes são `RepositorioFormacaoAcademica`, `RepositorioExperienciaProfissional` e `RepositorioProjetoAcademico`, todas só com `salvar`; competência, idioma e documento não têm porta (`src/backend/application/ports.py`, por listagem).
6. `RepositorioCurriculo` declara `obter_por_id`, `atualizar` e `salvar`; o adapter SQLAlchemy reconstrói o agregado **sem referências** e `atualizar` grava somente `titulo_versao`, `layout` e `is_public` (`repositorio_curriculo.py`, `curriculo.py`; limitação registrada como H5 na análise de edição).
7. Os wireframes descrevem uma jornada única que inclui todas as seções, sem tela para escolher itens por versão (`docs/wireframes/07-revisao.md`, `02-painel-inicial.md`). RF14 prevê múltiplos currículos por estudante, e o caso de uso "Gerenciar versões" prevê versões para objetivos diferentes.
8. O fixture de exportação do time monta um currículo chamando `incluir_referencia` para formação, experiência, projeto, competências e idiomas (`tests/fixtures/curriculo_exportacao.py`).
9. O README atribui formação e experiências a uma área, e competências, idiomas, projetos e documentos complementares a outra; a gestão de versões é a área do autor desta tarefa.
10. As rotas de currículo existentes recebem `usuario_id` no caminho, sem autenticação, e `main.py` compõe a aplicação sem executores (análises relacionadas).
11. As skills de implementação exigem que o núcleo (portas, casos de uso) preceda os adapters, que adapter não crie porta ou regra de negócio, que testes de rota substituam o caso de uso por double e que cada trecho novo traga o comentário de proveniência.

### Hipóteses

- **H1.** "Selecionar" inclui um item na versão e "desselecionar" o remove; ambas operam um item por vez.
- **H2.** A verificação de propriedade do item fica na Application, por uma nova porta `ConsultaProprietarioItem` com `obter_proprietario(referencia)`, e a ausência do item e a propriedade alheia produzem a mesma falha (`ItemNaoEncontrado`).
- **H3.** A desseleção não consulta o proprietário do item: a referência só existe se já passou pela verificação ao ser incluída.
- **H4.** A seleção de um item já selecionado e a desseleção de um item não selecionado resultam em violação de domínio (422), reaproveitando as regras do agregado, sem exceções novas de duplicidade.
- **H5.** A persistência usa **uma tabela única** `curriculo_itens` (`curriculo_id` com chave estrangeira para `curriculos`, `tipo` e `item_id`, chave primária composta), sem chave estrangeira para os itens, cujas tabelas não existem.
- **H6.** O adapter passa a **reconstruir as referências** ao carregar e a **sincronizar as referências** em `atualizar` e `salvar` (inserir as novas, remover as ausentes), o que também elimina a limitação H5 da análise de edição.
- **H7.** O tipo do item trafega como texto estável (`formacao_academica`, `experiencia_profissional`, `projeto_academico`, `competencia`, `idioma`, `documento`), mapeado separadamente na API e na persistência.
- **H8.** O adapter real de `ConsultaProprietarioItem` não pode ser implementado agora; cada tipo de item o fornecerá quando sua tabela existir.
- **H9.** A resposta de seleção devolve a seleção atual da versão em ordem determinística; a ordem dos itens na versão não é definida.

### Perguntas em aberto

1. Selecionar duas vezes ou desselecionar item ausente deve ser 422 (H4) ou 409 e 404?
2. Os textos de tipo de item (H7) estão aceitos?
3. Qual é a política de exclusão de um item que está selecionado em alguma versão (bloquear, remover a referência ou deixar órfã)?
4. Haverá ordenação ou personalização dos itens por versão? Se sim, a escolha pela tabela única deve ser reavaliada.
5. Quem implementa os adapters de `ConsultaProprietarioItem` por tipo e em qual fatia?
6. Deve haver limite de itens por versão?
7. A consulta da seleção atual (listagem) será outra tarefa?

### Escopo

- Porta `ConsultaProprietarioItem`, exceção `ItemNaoEncontrado` e os casos de uso `SelecionarItemVersaoCurriculo` e `DesselecionarItemVersaoCurriculo`, com suas entradas.
- Modelo `CurriculoItemRegistro`, migration encadeada à `20261005_0002`, mapeadores de referência, e alteração do adapter de currículo para reconstruir e sincronizar referências.
- Rotas `POST` (seleção) e `DELETE` (desseleção), DTOs, registro em `factory.py`.
- Testes unitários de cada camada com doubles apropriados.

### Fora do escopo

- Adapters reais de `ConsultaProprietarioItem` e tabelas dos itens.
- Listagem ou consulta da seleção atual; ordenação e personalização por versão; limite de itens.
- Política de exclusão de itens referenciados.
- Autenticação, sessão e autorização; composição de engine, sessão e transação reais.
- Testes de integração com banco real.

### Critérios de sucesso

- Selecionar um item do próprio usuário inclui a referência na versão e solicita a atualização uma vez; desselecionar a remove.
- Versão inexistente, versão de outro usuário, item inexistente e item de outro usuário geram falhas que não revelam a diferença entre ausência e posse alheia, sem atualização.
- Duplicidade e remoção de item não selecionado são recusadas pelo domínio sem atualização.
- O adapter reconstrói as referências ao carregar e persiste somente a diferença ao atualizar, sem apagar seleções em edições de título, layout ou visibilidade.
- A migration cria e remove somente `curriculo_itens`, encadeada à revisão anterior, e o modelo coincide com ela.
- As rotas respondem 201, 204, 404, 422 e 503 conforme o contrato; nenhuma entidade de domínio é exposta.
- A suíte unitária do ambiente `backend` passa, inclusive no CI, sem banco, rede ou relógio reais.

## Restrições aplicáveis

- Domain não depende de Application, Infrastructure, API ou ORM; Application não depende de Infrastructure nem da API; regras de negócio não ficam em controllers nem repositórios (`src/backend/AGENTS.md`).
- A regra de propriedade do item atravessa agregados e é coordenada pelo caso de uso por portas (`prompts/backend/20260914-camada-dominio-v001.md`).
- Persistência com ORM Code First e migrations Alembic; mapeamentos na infraestrutura (`src/backend/AGENTS.md`).
- DTOs na fronteira; entidades não são expostas pela API (`src/backend/AGENTS.md`).
- Testes unitários no ambiente `backend`, com doubles; docstring em toda função e classe (`AGENTS.md`).
- Núcleo antes dos adapters; adapter não cria porta nem regra; testes de rota substituem o caso de uso por double; proveniência em todo trecho novo (skills de implementação).
- Propriedade do recurso deve ser verificada e acesso a recurso de outro usuário negado (`docs/requisitos-seguranca.md`, RNF04).

## Classificação comentada

- `sphere: engineering`: construção técnica de funcionalidade prevista em RF14 e no caso de uso "Gerenciar versões".
- `concerns: domain, security, data`: composição da versão; propriedade dos itens (risco de expor dados alheios em exportações); nova tabela e migration.
- `decision_kind: design`, `scope: component`, `lifecycle: delivery`, `urgency: normal`.
- `uncertainty: medium`: há perguntas abertas sobre ordenação, exclusão de itens e códigos de resposta.
- `reversibility: moderate`: a migration é reversível enquanto a tabela não tiver dados, mas migrar de tabela única para seis tabelas depois exigiria migração de dados.
- `risk: high`: uma falha na verificação de propriedade permitiria incluir item de outro estudante em uma versão e expô-lo ao exportar; a gravidade é mitigada porque a identidade ainda não é autenticada e porque a aplicação real ainda não compõe os casos de uso.

## Decisão de roteamento

Roteada para `prompts/backend`, a mesma pasta das análises relacionadas de edição e criação de versão. Candidatas: `prompts/backend` e `prompts/requisitos`; esta última foi descartada porque a análise não levanta nem refina requisitos. Confiança alta. Não existem `AGENTS.md` ou `AGENTS.override.md` específicos em `prompts/` (busca por nome de arquivo na árvore de trabalho, feita nesta consulta).

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | 1 | Nenhum item alheio selecionado; seleção preservada em edições; contrato de persistência verificado | A versão selecionada alimenta a exportação |
| `security` | 1 | Propriedade do item verificada antes de incluir | RNF04 e risco de vazamento em PDF/DOCX |
| `simplicity` | 2 | PR revisável e sem refatorar o domínio | Preferência do usuário por entregas menores |
| `modifiability` | 2 | Não impedir ordenação futura nem tabelas dos itens | O prompt de domínio prevê reavaliação se houver ordenação |
| `time-to-value` | 3 | Entregar em etapas testáveis na mesma branch | Fatias verticais com revisão por camada |

## Alternativas consideradas

**Estado atual.** O agregado tem os métodos de inclusão e remoção, mas nenhum caso de uso, persistência ou rota permite selecionar itens, e as referências não são persistidas.

**Alternativa A — Tabela única `curriculo_itens` (recomendada, escolhida pelo usuário).** Application: porta `ConsultaProprietarioItem`, `ItemNaoEncontrado`, dois casos de uso. Infrastructure: modelo, migration, mapeadores e adapter que reconstrói e sincroniza referências. Interface: `POST /estudantes/{usuario_id}/curriculos/{curriculo_id}/itens` (201; corpo com tipo e id do item; resposta com a seleção atual) e `DELETE .../itens/{tipo}/{item_id}` (204), em um módulo de rota próprio, com 404, 422 e 503.

**Alternativa B — Seis tabelas do DER.** Mesma Application e Interface, mas seis modelos de associação, uma migration com seis tabelas e despacho por tipo no adapter. Fiel ao DER; as chaves estrangeiras para os itens também não poderiam existir ainda.

**Alternativa C — Sem persistência nesta tarefa.** Somente Application e Interface, com doubles. As referências continuam fora do banco e a infraestrutura entra depois das tabelas dos itens. Não entrega a fatia vertical.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | 1 | +1 | +1 | -1 | média | A e B verificam em testes a reconstrução e a sincronização de referências e a migration; C deixa o contrato de persistência sem verificação |
| `security` | 1 | 0 | 0 | 0 | média | A verificação de propriedade é a mesma nas três (Application); nenhuma pode ter chave estrangeira para os itens agora |
| `simplicity` | 2 | +1 | -2 | +2 | média | B soma seis modelos, seis tabelas e despacho por tipo; A tem um modelo e uma tabela; C não toca a infraestrutura |
| `modifiability` | 2 | -1 | +1 | -1 | baixa | B já segue a estrutura do DER; A exigiria migração de dados se o time adotar seis tabelas; C adia a decisão de persistência |
| `time-to-value` | 3 | +1 | -1 | +1 | média | A e C entregam menos código; C entrega sem uso fora dos testes |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**, com **seleção e desseleção** (H1), entregue em etapas na mesma branch e no mesmo pull request: (1) Application com testes; (2) Infrastructure com testes; (3) Interface com testes. A propriedade do item é verificada na Application por porta (H2), com a mesma falha para ausência e propriedade alheia; a persistência usa a tabela `curriculo_itens` (H5) e o adapter passa a reconstruir e sincronizar referências (H6), o que corrige a limitação de edição e criação. O adapter real da porta de propriedade fica como handoff para as áreas dos itens (H8). O status é `proposed`: a decisão exige aprovação humana, em especial sobre as perguntas 1, 3 e 4.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | prioritized | Seleção preservada em edições e contrato de persistência verificado | Testes do adapter para reconstrução e diferença de referências; teste de que editar título não apaga a seleção |
| `security` | prioritized | Item de outro usuário nunca entra na versão | Teste do caso de uso com item de proprietário diferente e com item inexistente, sem atualização |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | PR revisável, sem refatorar o domínio | O domínio não muda; uma tabela, uma migration e dois casos de uso pequenos |
| `time-to-value` | Cada etapa testável isoladamente | Etapas por camada com suíte própria |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `security` | Item de outro estudante incluído em uma versão e exposto na exportação | Alta | Estudantes donos dos itens |
| `correctness` | Seleção apagada silenciosamente ao editar título, layout ou visibilidade | Alta | Estudantes donos das versões |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | Tabela única sem chave estrangeira para os itens e fora do DER | `modifiability` | Aceitável porque as tabelas dos itens não existem; a migração para seis tabelas, se necessária, é uma tarefa posterior |
| `correctness` | A alteração do adapter muda o comportamento de `obter_por_id` e `atualizar` já usados por edição e criação | `simplicity` | Aceitável com testes de regressão dessas operações |
| `simplicity` | Duplicidade e item não selecionado respondem 422, e não 409 e 404 | `user-value` | Aceitável nesta fatia, sujeito à pergunta 1 |

## Riscos e efeitos de segunda ordem

- **Seleção apagada por um adapter incompleto.** Se o adapter sincronizar referências sem reconstruí-las ao carregar, qualquer edição apagaria a seleção. Mitigação: reconstrução e sincronização na mesma etapa, com teste de regressão da edição.
- **Item selecionado e depois excluído.** Sem chave estrangeira para os itens e sem política de exclusão, a referência pode ficar órfã. Mitigação: pergunta 3 e handoff às áreas dos itens.
- **Adapter de propriedade inexistente.** Enquanto as áreas dos itens não o fornecerem, a seleção não funciona contra banco real; a rota continuará respondendo 503 até a composição.
- **Decisão de modelagem prematura.** Se a ordenação por versão for adotada, a tabela única precisará ser reavaliada. Mitigação: tabela pequena, reversível enquanto vazia.
- **Condição de corrida.** Duas seleções simultâneas do mesmo item colidiriam na chave primária e resultariam em erro de integridade, e não em falha de negócio. Mitigação: aceitável nesta fatia; tratar na composição.
- **Textos de tipo duplicados.** O mapeamento de tipo existirá na API e na persistência. Mitigação: testes de ida e volta para os seis tipos.
- **Múltiplas cabeças no Alembic.** Nova revisão encadeada à `20261005_0002`; integrar a `dev` antes do pull request.
- **Tamanho do PR.** Esta fatia é maior que as anteriores; o corte natural é por etapa (um commit por camada).

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Item alheio ou inexistente é recusado | `atualizar` não é chamado e a mesma falha é levantada | Teste unitário do caso de uso com spy e double da porta de propriedade | Qualquer atualização observada |
| Duplicidade e remoção de ausente são recusadas | Violação de domínio sem atualização | Teste unitário do caso de uso | Atualização com item duplicado |
| O adapter reconstrói a seleção ao carregar | Agregado devolvido com as referências das linhas | Teste unitário com sessão simulada | Agregado sem referências |
| O adapter persiste só a diferença | Linhas inseridas e removidas corretas, sem toque quando nada mudou | Teste unitário com sessão simulada | Remoção de linhas não alteradas |
| Editar título não apaga a seleção | Nenhuma remoção de linha em `atualizar` sem mudança de referências | Teste unitário do adapter | Qualquer remoção sem mudança |
| O modelo coincide com a migration | Colunas, tipos, chave primária e chave estrangeira iguais | Teste de metadata e migration em memória | Divergência entre modelo e `upgrade()` |
| As rotas traduzem falhas | 201, 204, 404, 422 e 503 | Teste unitário da rota com double do caso de uso | Status diferente do contrato |
| Persistência funciona em banco real | Inserção, remoção e violação de chave primária observadas | Teste de integração no ambiente `tests` | Falha de DDL ou comportamento diferente |

## Handoffs e atividades posteriores

- **`$backend-domain-orchestration-v2`:** porta `ConsultaProprietarioItem`, exceção `ItemNaoEncontrado`, entradas e casos de uso `SelecionarItemVersaoCurriculo` e `DesselecionarItemVersaoCurriculo`, e testes unitários com todas as portas substituídas por doubles.
- **`$backend-adapters-drivers-v2`:** modelo `CurriculoItemRegistro`, migration, mapeadores, alteração do adapter de currículo (reconstrução e sincronização de referências), módulo de rota, DTOs, registro em `factory.py` e testes unitários dessas unidades.
- **Áreas dos itens (perfil, formação e experiências; informações complementares e documentos):** tabelas e adapters por tipo de `ConsultaProprietarioItem`, e política de exclusão de item selecionado.
- **`$cross-cutting-implementation-v1`:** autenticação e autorização com identidade da sessão; transações.
- **`$integration-system-testing-v1`:** testes de integração do adapter e da migration contra banco real.
- **Composição:** definir quem compõe engine, sessão, transação e a combinação dos adapters de propriedade.
- **Próximas fatias:** listar a seleção da versão; ordenação ou personalização por versão (reavaliar a tabela única); limite de itens; exclusão de versão com a política das referências.
- **Rastreabilidade:** conferir se os comentários `# Proveniência` do código usam o nome definitivo deste arquivo.

## Síntese

O agregado já sabe incluir e remover referências; o que falta é o caso de uso que **garante que o item é do mesmo dono**, a persistência da seleção e a rota. A decisão entrega as quatro camadas com uma tabela única, uma porta nova de propriedade e dois casos de uso pequenos, e aproveita para corrigir o adapter de currículo, que hoje ignora as referências. Duas limitações definem o risco: as tabelas e as consultas de propriedade dos itens pertencem a outras fatias, então a seleção só funciona de ponta a ponta quando elas existirem, e a escolha da tabela única precisa ser reavaliada se a ordenação por versão for adotada. As perguntas sobre duplicidade (422 ou 409 e 404), exclusão de item selecionado e ordenação devem ser respondidas antes da aprovação.
