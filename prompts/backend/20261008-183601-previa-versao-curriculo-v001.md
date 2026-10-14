---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-08T18:36:01-03:00"
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
      analysis_scope: selected-section
      locator: "campos do agregado, validação e leitura de referências (linhas 1-80 e uso por listagem)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: src/backend/domain/itens_perfil.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: available
    - path: src/backend/domain/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "campos da entidade Usuario (por listagem)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "declarações de identificadores, Nome, Email, Endereco, Telefone, DadosContato, Periodo e ReferenciaCurriculo (por listagem)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "RepositorioUsuario.obter_por_id, RepositorioCurriculo e GeradorCurriculoId (linhas 32-80 e 245-300) e lista de portas (por listagem)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: src/backend/application/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 1-60 (importações, CurriculoNaoEncontrado e padrão do caso de uso de edição)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: src/backend/application/__init__.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 60-140 (importações e __all__)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: src/backend/api/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "linhas 100-140 (criar_router, nota sobre identidade e rota de edição)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: src/backend/tests/fixtures/curriculo_exportacao.py
      relationship: context
      representation: source-code
      function: data-fixture
      format: python
      analysis_scope: selected-section
      locator: "linhas 1-80 (módulo, importações, identificadores e DTO da fixture)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: docs/wireframes/08-visualizacao-curriculo.md
      relationship: primary
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
      locator: "linhas 50, 176, 199, 201, 224 (menções à prévia, por busca textual)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF07, RF13, RF14 e RF15 (por busca textual)"
      content_state: commit
      revision: "e711a98bac2de4b1477d6d1939989dddab794e6a"
      availability: partial
    - path: prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
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
  rationale: "O propósito é decidir a construção de uma fatia de backend (porta, caso de uso e rota de leitura) sobre o agregado Curriculo; a linhagem relacionada de versões de currículo está em prompts/backend."
classification:
  sphere: engineering
  concerns: [domain, security, privacy]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: medium
---

# Análise de decisão — prévia de versão de currículo

## Solicitação original

Texto literal fornecido pelo usuário:

```text
Implementar prévia de versão de currículo
#120 da pra fazer esse?  Inclua os testes unitários pertinentes.
```

## Informações complementares

Insumos literais registrados na conversa (grafia preservada):

- Respostas do usuário às perguntas de escopo feitas antes desta análise: branch "Criar task-120 a partir da dev"; item inexistente ou alheio na prévia: "Omitir o item e seguir (Recomendada)"; escrita: "Sim, direto, etapa por etapa (Recomendada)".
- Sobre uma tarefa anterior, tomado como preferência por PRs pequenos: "descricao menor, dá? to achando muito grande esse PR"
- Mensagem do gestor reproduzida pelo usuário em conversa anterior: "No começo as coisas não estavam muito bem definidas, mas agora as funcionalidades já são claras. Os time serão reorganizados para lidar com slices verticais agora ao invés de horizontais. Isso só afeta backend. Frontend fica do mesmo jeito"
- O texto da issue #120 não foi lido: a GitHub CLI não está disponível neste ambiente e o usuário informou somente o título e o número.
- A análise `prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md` (tarefa 117, ainda em revisão no momento desta análise) é relacionada, mas esta análise é independente e não a revisa.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/domain/curriculo.py` | primary | source-code | production | python | campos, validação e leitura de referências | commit `e711a98` |
| `src/backend/domain/itens_perfil.py` | primary | source-code | production | python | arquivo inteiro | commit `e711a98` |
| `src/backend/domain/usuario.py` | supporting | source-code | production | python | campos (listagem) | commit `e711a98` |
| `src/backend/domain/value_objects.py` | supporting | source-code | production | python | declarações (listagem) | commit `e711a98` |
| `src/backend/application/ports.py` | supporting | source-code | production | python | portas de usuário e de currículo | commit `e711a98` |
| `src/backend/application/versao_curriculo.py` | supporting | source-code | production | python | linhas 1-60 | commit `e711a98` |
| `src/backend/application/__init__.py` | supporting | source-code | production | python | linhas 60-140 | commit `e711a98` |
| `src/backend/api/versao_curriculo.py` | supporting | source-code | production | python | linhas 100-140 | commit `e711a98` |
| `src/backend/tests/fixtures/curriculo_exportacao.py` | context | source-code | data-fixture | python | linhas 1-80 | commit `e711a98` |
| `docs/wireframes/08-visualizacao-curriculo.md` | primary | prose | documentation | markdown | arquivo inteiro | commit `e711a98` |
| `docs/mapeamento_jornadas.md` | supporting | prose | documentation | markdown | menções à prévia | commit `e711a98` |
| `docs/requisitos_funcionais.md` | supporting | prose | documentation | markdown | RF07, RF13, RF14, RF15 | commit `e711a98` |
| `prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md` | primary | prose | documentation | markdown | arquivo inteiro | working tree (branch `task-117`) |
| `.agents/skills/backend-domain-orchestration-v2/SKILL.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `e711a98` |
| `.agents/skills/backend-adapters-drivers-v2/SKILL.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `e711a98` |
| `AGENTS.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `e711a98` |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | markdown | arquivo inteiro | commit `e711a98` |

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `e711a98bac2de4b1477d6d1939989dddab794e6a` (cabeça da `dev`, sobre a qual a branch `task-120` foi criada). **O código da tarefa 117 não está nesta base**: o adapter de currículo da `dev` ainda não reconstrói as referências ao carregar, e a porta `ConsultaProprietarioItem` não existe nela.
- O documento da tarefa 117 foi lido do working tree da branch `task-117` antes da troca de branch; seu conteúdo é conhecido, mas ele ainda não está na `dev`.
- Arquivos com recorte parcial sustentam somente os fatos dos trechos indicados. A ausência de tabelas e de portas de leitura dos itens baseia-se na listagem de declarações de portas e, para as tabelas, na análise da tarefa 117 (listagem de `__tablename__` e de revisões, feita naquela análise); não foi refeita aqui.
- O texto da issue #120 não foi lido. Os critérios de aceite da issue podem diferir das hipóteses abaixo.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md` e suas referências; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

O estudante dono de uma versão de currículo consegue obter uma prévia estruturada dessa versão: a identificação do estudante e os dados completos dos itens selecionados, agrupados por seção, prontos para o cliente apresentar antes da exportação. Itens que não existam mais ou que não pertençam ao estudante não aparecem. A entrega atravessa Application e Interface, com testes unitários.

### Atores e interesses

- **Estudante dono da versão:** conferir como o currículo ficará antes de exportar (UC06 "Visualizar currículo").
- **Outro estudante:** seus dados não podem aparecer na prévia de uma versão alheia (RNF04, RF13).
- **Equipes responsáveis pelos itens:** serão donas da leitura dos itens (adapters e tabelas).
- **Frontend:** consome a resposta estruturada e apresenta o documento conforme o modelo (layout) da versão.
- **Equipe de backend e líder técnico:** fronteiras entre camadas e tamanho do PR.

### Evidências e fatos observados

1. O wireframe 08 descreve a prévia como estrutura de identificação do aluno, resumo profissional (quando preenchido), formação acadêmica, experiência profissional e "habilidades e demais informações complementares", e afirma que ela "representa os dados fornecidos e confirmados pelo aluno" (`docs/wireframes/08-visualizacao-curriculo.md`).
2. UC06 "Visualizar currículo" apresenta a prévia antes da exportação, e RF07 prevê "uma visualização do currículo com as informações cadastradas e o modelo selecionado" (`docs/mapeamento_jornadas.md`, `docs/requisitos_funcionais.md`).
3. O agregado `Curriculo` guarda `titulo_versao`, `layout`, `is_public` e expõe `referencias` (frozenset de `ReferenciaCurriculo`, que aceita os seis identificadores de item); a ordem das referências não é definida (`src/backend/domain/curriculo.py`).
4. As seis entidades de item são imutáveis, têm `usuario_id` e campos descritivos: formação (instituição, curso, nível, período, status), experiência (empresa, cargo, descrição, período), projeto (título, descrição, tecnologias), competência (descrição, nível), idioma (idioma, nível) e documento (nome, tipo e `url_armazenamento`) (`src/backend/domain/itens_perfil.py`).
5. `Usuario` guarda nome, email, hash de senha, `deleted_at` e `dados_contato` opcional (endereço, telefones, LinkedIn e Lattes opcionais) (`src/backend/domain/usuario.py`, `value_objects.py`, por listagem).
6. A porta `RepositorioUsuario.obter_por_id` já existe; `RepositorioCurriculo.obter_por_id` também. Não existe nenhuma porta que **leia** itens por referência: `RepositorioFormacaoAcademica`, `RepositorioExperienciaProfissional` e `RepositorioProjetoAcademico` só declaram `salvar`, e competência, idioma e documento não têm porta (`src/backend/application/ports.py`, por listagem).
7. Pela análise da tarefa 117, nenhum dos seis itens tem tabela, modelo ORM ou migration, e a tarefa 117 define a porta `ConsultaProprietarioItem` (apenas propriedade) cujo adapter real também é um handoff.
8. As rotas de currículo existentes recebem `usuario_id` no caminho, sem autenticação, e `main.py` compõe a aplicação sem executores, de modo que elas respondem 503 no app real (análises relacionadas).
9. `CurriculoNaoEncontrado` já agrupa ausência e propriedade alheia da versão sob a mesma falha, traduzida em 404 pela API (`src/backend/application/versao_curriculo.py`).
10. A fixture de exportação reúne `Usuario`, `Curriculo` e as entidades de item "desreferenciadas", como entrada de futuros motores de exportação (`src/backend/tests/fixtures/curriculo_exportacao.py`).
11. As skills de implementação exigem núcleo antes dos adapters, testes de rota com o caso de uso substituído por double, adapter sem criar porta ou regra de negócio, e comentário de proveniência em todo trecho novo.

### Hipóteses

- **H1.** "Prévia" é uma **consulta**: não altera estado nem solicita atualização no repositório.
- **H2.** A prévia é uma **estrutura de dados** (seções com os dados dos itens), e não texto formatado, HTML, PDF nem DOCX; a apresentação visual conforme o `layout` é responsabilidade do frontend. A resposta devolve o valor de `layout` sem interpretá-lo.
- **H3.** Uma única porta nova, `ConsultaItemPerfil.obter_item(referencia)`, devolve a entidade de item correspondente ou `None`, no mesmo formato da porta de propriedade da tarefa 117. Isso evita seis portas por tipo e não altera as portas de repositório existentes.
- **H4.** A prévia só inclui item cujo `usuario_id` seja o do solicitante: item ausente (`None`) ou de outro proprietário é **omitido** sem erro e sem revelar sua existência (resposta do usuário). Essa conferência é redundante com a seleção da tarefa 117 e funciona como defesa em profundidade.
- **H5.** A versão ausente ou pertencente a outro usuário falha com `CurriculoNaoEncontrado` (404), como nos demais casos de uso de versão.
- **H6.** O estudante também é lido por `RepositorioUsuario.obter_por_id`; estudante ausente ou com `deleted_at` preenchido falha com `CurriculoNaoEncontrado`, pois a identificação é parte indispensável da prévia.
- **H7.** A ordem é determinística, já que as referências são um conjunto: formação e experiência em ordem cronológica decrescente pelo início do período; projetos por título, competências por descrição, idiomas por nome e documentos por nome do arquivo, com desempate pelo texto do identificador.
- **H8.** A prévia inclui as seis seções, mas **não** expõe `url_armazenamento` do documento (apenas nome e tipo), por tratar-se de detalhe de armazenamento. O resumo profissional do wireframe não tem campo no domínio atual e fica fora.
- **H9.** Por ser leitura de um recurso existente e não criar nada, a rota é `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/previa` com 200, 404 e 503.
- **H10.** Nesta fatia **não há infraestrutura**: sem tabelas dos itens, não há adapter possível para a porta nova; ele é um handoff.

### Perguntas em aberto

1. O texto e os critérios de aceite da issue #120 coincidem com H1 a H9?
2. A prévia deve incluir documentos (H8) e, em caso afirmativo, somente metadados?
3. A ordem de apresentação (H7) deve ser fixa ou personalizável pelo estudante? Se personalizável, a tarefa 117 também precisa ser reavaliada (tabela única sem ordem).
4. Versão pública (`is_public`) terá prévia visível a outros usuários no futuro? Por ora a rota é restrita ao dono.
5. Quem implementa o adapter de `ConsultaItemPerfil` por tipo e quando as tabelas dos itens existirão?
6. O frontend precisa de campos calculados (por exemplo, duração de período ou texto de nível)?

### Escopo

- Porta `ConsultaItemPerfil`, saída `PreviaVersaoCurriculo` (modelo de leitura com entidades por seção) e caso de uso `GerarPreviaVersaoCurriculo`, com sua entrada.
- Rota `GET .../previa`, DTOs de resposta e registro em `factory.py`.
- Testes unitários de cada unidade com doubles.

### Fora do escopo

- Adapter real de `ConsultaItemPerfil` e tabelas dos itens.
- Renderização visual (HTML), geração de PDF ou DOCX, e seleção de modelo de layout.
- Autenticação, sessão e autorização; composição de engine e sessão reais.
- Compartilhamento público da prévia.
- Resumo profissional (sem campo no domínio atual).
- Testes de integração com banco real.

### Critérios de sucesso

- A prévia de uma versão própria devolve título, layout e identificação do estudante, e os itens selecionados em seções e em ordem determinística.
- Versão inexistente ou de outro usuário, e estudante ausente, produzem a mesma falha de não encontrado, sem consultar itens.
- Item ausente ou de outro proprietário não aparece na prévia, e a prévia não falha por causa dele.
- A operação não chama `atualizar` nem `salvar` do repositório de currículo.
- A resposta HTTP não expõe entidades de domínio nem `url_armazenamento`, nem dados de outro estudante.
- A rota responde 200, 404 e 503 conforme o contrato.
- A suíte unitária do ambiente `backend` passa sem banco, rede ou relógio reais.

## Restrições aplicáveis

- Domain não depende de Application, Infrastructure, API ou ORM; Application não depende de Infrastructure nem da API; regras de negócio não ficam em controllers nem repositórios (`src/backend/AGENTS.md`).
- Portas pertencem à camada interna que as exige e são implementadas por adapters; a composição ocorre na camada externa (`src/backend/AGENTS.md`).
- Entradas externas viram DTOs antes do caso de uso; entidades de domínio não são expostas pela API (`src/backend/AGENTS.md`).
- Testes unitários no ambiente `backend`, com doubles; docstring (o que faz, como faz, finalidade) em toda função e classe (`AGENTS.md`).
- Núcleo antes dos adapters; adapter não cria porta nem regra; testes de rota substituem o caso de uso por double; proveniência em todo trecho novo (skills de implementação).
- Propriedade do recurso verificada e acesso a recurso de outro usuário negado (RNF04, RF13).

## Classificação comentada

- `sphere: engineering`: construção técnica de funcionalidade prevista em RF07 e UC06.
- `concerns: domain, security, privacy`: a prévia reúne dados pessoais e profissionais do estudante; um erro de propriedade exporia dados alheios.
- `decision_kind: design`, `scope: component`, `lifecycle: delivery`, `urgency: normal`.
- `uncertainty: medium`: o texto da issue não foi lido e há perguntas abertas sobre documentos e ordenação.
- `reversibility: easy`: é uma consulta sem migração; o contrato da resposta pode evoluir antes de haver cliente.
- `risk: medium`: a gravidade do vazamento de dados é alta, mas a mitigação por defesa em profundidade é simples e a aplicação real ainda não compõe os casos de uso nem autentica.

## Decisão de roteamento

Roteada para `prompts/backend`, pasta das análises relacionadas de versões de currículo. Candidatas: `prompts/backend` e `prompts/requisitos`; esta foi descartada porque a análise não levanta nem refina requisitos. Confiança alta. Não há `AGENTS.md` ou `AGENTS.override.md` específico em `prompts/` (verificado na análise relacionada; não refeito aqui).

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `security` | 1 | Nenhum dado alheio aparece; ausência e posse alheia são indistinguíveis | A prévia reúne dados pessoais (RNF04, RF13) |
| `privacy` | 1 | Não expor `url_armazenamento` nem dados além do necessário | Minimização de dados na resposta |
| `correctness` | 1 | Prévia determinística e fiel à seleção da versão | O estudante confirma o que será exportado |
| `simplicity` | 2 | PR revisável, sem alterar portas existentes nem o domínio | Preferência do usuário por entregas menores |
| `modifiability` | 2 | Contrato permite ordenação e novos campos | Frontend e exportação evoluirão |
| `time-to-value` | 3 | Entrega em duas etapas testáveis | Fatias verticais com revisão por camada |

## Alternativas consideradas

**Estado atual.** Existe o agregado com as referências, mas nenhuma forma de ler os itens referenciados, nenhum caso de uso de consulta de versão e nenhuma rota de leitura.

**Alternativa A — Porta única de leitura de item + caso de uso de leitura + rota estruturada (recomendada).** Application: porta `ConsultaItemPerfil`, saída `PreviaVersaoCurriculo`, caso de uso `GerarPreviaVersaoCurriculo(repositorio_curriculo, repositorio_usuario, consulta_item)`. Interface: `GET .../previa` com DTOs por seção. Sem infraestrutura (handoff).

**Alternativa B — Estender as portas de repositório existentes por tipo.** Adicionar `obter_por_id` às três portas existentes e criar três portas novas (competência, idioma, documento), com o caso de uso usando seis portas. Segue o padrão de repositórios, mas altera contratos de outras áreas, multiplica portas e dependências do caso de uso e gera mais risco de conflito entre equipes.

**Alternativa C — Prévia renderizada no backend (HTML ou texto).** O caso de uso ou a rota produziria o documento formatado. Atende a leitura literal de "visualização", mas mistura apresentação com dados, depende do modelo (layout) ainda não definido e duplica o que o frontend fará. É inviável como primeira entrega por restrição de escopo (H2).

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `security` | 1 | +1 | +1 | 0 | média | A e B conferem a propriedade na Application; C não altera o risco, mas amplia a superfície com texto formatado |
| `privacy` | 1 | +1 | +1 | -1 | média | A e B devolvem só campos necessários; C tende a incluir o que o modelo renderizar |
| `correctness` | 1 | +1 | +1 | 0 | média | Resultado determinístico por testes nas duas primeiras |
| `simplicity` | 2 | +1 | -2 | -1 | média | B soma seis portas e altera três existentes; C acopla apresentação ao backend |
| `modifiability` | 2 | +1 | 0 | -2 | baixa | A expõe dados estruturados reutilizáveis na exportação; C engessa o formato |
| `time-to-value` | 3 | +1 | -1 | -1 | média | A é a menor entrega testável |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**, em duas etapas na mesma branch: (1) Application, com a porta `ConsultaItemPerfil`, `PreviaVersaoCurriculo` e `GerarPreviaVersaoCurriculo`, mais testes com portas substituídas por doubles; (2) Interface, com a rota `GET .../previa`, DTOs por seção e registro em `factory.py`, mais testes com o caso de uso substituído por double. A infraestrutura fica como handoff (H10). O status é `proposed`: a decisão exige aprovação humana, em especial sobre as perguntas 1 e 2.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `security` | prioritized | Nenhum item ou estudante alheio aparece na prévia | Teste do caso de uso com item de outro proprietário e com versão alheia, sem consulta de itens |
| `privacy` | prioritized | Resposta sem `url_armazenamento` e sem hash de senha | Teste da rota e do mapeamento de resposta |
| `correctness` | prioritized | Ordem e seções determinísticas | Testes com referências fora de ordem |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | PR revisável, sem alterar portas existentes | Uma porta nova, um caso de uso e uma rota |
| `time-to-value` | Cada etapa testável isoladamente | Duas etapas com suíte própria |
| `modifiability` | Contrato por seção, extensível | DTOs por seção permitem novos campos sem quebrar clientes que ignoram campos extras |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `security` | Dados pessoais e profissionais de outro estudante exibidos na prévia | Alta | Estudantes donos dos dados |
| `privacy` | Exposição de caminho de armazenamento de documentos | Média | Estudantes donos dos documentos |
| `correctness` | Ordem instável entre chamadas, confundindo o estudante na conferência | Baixa | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `security` | Uma consulta por item e conferência de propriedade mesmo já feita na seleção | `performance` | Aceitável: poucas dezenas de itens por versão; otimização cabe ao adapter |
| `simplicity` | Prévia sem renderização e sem resumo profissional | `user-value` | Aceitável nesta fatia; o frontend apresenta e o resumo não tem campo |
| `simplicity` | Sem adapter real, a rota responde 503 no app real | `time-to-value` | Aceitável: a composição e as tabelas dos itens são handoffs |

## Riscos e efeitos de segunda ordem

- **Dependência da tarefa 117.** O adapter de currículo da `dev` não reconstrói as referências; a prévia só terá o que exibir de ponta a ponta após a tarefa 117. Mitigação: a prévia depende somente do contrato de `Curriculo.referencias`.
- **Conflitos de integração.** A tarefa 117 também edita `ports.py`, `application/__init__.py` e `api/factory.py`. Mitigação: integrar a `dev` após o merge da 117 e resolver os trechos aditivos.
- **Omissão silenciosa de item.** Um item excluído some da prévia sem aviso, e o estudante pode não perceber. Mitigação: aceita pelo usuário; avaliar um indicador de itens omitidos em fatia posterior.
- **Dados pessoais na resposta.** A prévia inclui email, endereço e telefones. Mitigação: rota restrita ao dono, sem autenticação ainda; handoff de autenticação.
- **Vazamento de campos internos.** Reuso acidental de entidades como resposta. Mitigação: DTOs explícitos e teste de campos expostos.
- **Ordem implícita.** Se a ordenação passar a ser personalizável, a regra H7 e a tabela da 117 precisarão ser reavaliadas.
- **Desempenho.** N consultas sequenciais por item. Mitigação: aceitável agora; consulta em lote seria nova decisão.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| A prévia é somente leitura | `atualizar` e `salvar` nunca chamados | Teste do caso de uso com spy | Qualquer escrita observada |
| Versão alheia ou ausente não consulta itens | Nenhuma chamada à porta de itens | Teste do caso de uso com spy | Consulta de item após falha |
| Item ausente ou alheio é omitido | Prévia sem o item e sem erro | Teste do caso de uso com stub | Falha ou presença do item alheio |
| Ordem determinística | Mesma saída para referências em ordens diferentes | Teste do caso de uso | Saída dependente da ordem de inserção |
| Resposta sem dados internos | Campos da resposta enumerados | Teste da rota com double | Presença de `url_armazenamento` ou hash |
| Rota traduz falhas | 200, 404 e 503 | Teste da rota com double do caso de uso | Status diferente do contrato |
| Leitura funciona em banco real | Itens lidos por referência | Teste de integração no ambiente `tests` | Divergência entre adapter e porta |

## Handoffs e atividades posteriores

- **`$backend-domain-orchestration-v2`:** porta `ConsultaItemPerfil`, `PreviaVersaoCurriculo`, entrada e caso de uso `GerarPreviaVersaoCurriculo`, e testes unitários com todas as portas substituídas por doubles.
- **`$backend-adapters-drivers-v2`:** rota `GET .../previa`, DTOs de resposta, mapeamento de fronteira, registro em `factory.py` e testes unitários dessas unidades.
- **Áreas dos itens (perfil, formação e experiências; informações complementares e documentos):** tabelas e adapter de `ConsultaItemPerfil` por tipo.
- **`$cross-cutting-implementation-v1`:** autenticação e autorização com identidade da sessão.
- **`$integration-system-testing-v1`:** testes de integração do adapter e da rota contra banco real.
- **Composição:** engine, sessão, transação e combinação dos adapters de leitura de itens.
- **Próximas fatias:** exportação PDF/DOCX reutilizando a prévia; indicador de itens omitidos; resumo profissional; consulta em lote.
- **Rastreabilidade:** conferir se os comentários `# Proveniência` do código usam o nome definitivo deste arquivo.

## Síntese

O agregado já guarda as referências e o domínio já tem as seis entidades de item; falta um caso de uso de **leitura** que junte versão, estudante e itens, uma porta para ler os itens e uma rota. A decisão entrega isso em duas etapas, com uma única porta nova e uma resposta estruturada, deixando a renderização para o frontend e a leitura real dos itens para as áreas que mantêm suas tabelas. A principal incerteza é o texto da issue, não lido, e a principal exigência de segurança é que nenhum item ou estudante alheio apareça, o que a Application garante mesmo com a seleção já validada na tarefa 117.
