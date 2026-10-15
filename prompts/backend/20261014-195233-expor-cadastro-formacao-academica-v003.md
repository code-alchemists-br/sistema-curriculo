---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v003"
status: proposed
created_at: "2026-10-14T19:52:33-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261014-193425-expor-cadastro-formacao-academica-v001.md
  supersedes: prompts/backend/20261014-194443-expor-cadastro-formacao-academica-v002.md
  change_type: correction
  secondary_change_types: [reassessment]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20261014-193425-expor-cadastro-formacao-academica-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked; versão anterior da linhagem"
      availability: available
    - path: prompts/backend/20261014-194443-expor-cadastro-formacao-academica-v002.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "untracked; versão anterior da linhagem"
      availability: available
    - path: src/backend/domain/itens_perfil.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "FormacaoAcademica e enums do módulo"
      content_state: commit
      revision: "43c1ea3"
      availability: available
    - path: src/backend/application/perfil_estudante.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "CadastrarFormacaoAcademicaEntrada e CadastrarFormacaoAcademica"
      content_state: commit
      revision: "43c1ea3"
      availability: available
    - path: src/backend/tests/test_domain_entities.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "teste de construção de FormacaoAcademica"
      content_state: commit
      revision: "43c1ea3"
      availability: available
    - path: src/backend/tests/test_application_perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "testes e helper de CadastrarFormacaoAcademica"
      content_state: commit
      revision: "43c1ea3"
      availability: available
    - path: src/backend/api/experiencia_profissional.py
      relationship: context
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "DTO, tratamento de RegraDeDominioViolada e resposta 422"
      content_state: commit
      revision: "43c1ea3"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/competencia.py
      relationship: context
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "43c1ea3"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/experiencia_profissional.py
      relationship: context
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "43c1ea3"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: Markdown/DER
      analysis_scope: selected-section
      locator: "FORMACAO_ACADEMICA"
      content_state: commit
      revision: "43c1ea3"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF01, RF02 e detalhamentos ainda necessários"
      content_state: commit
      revision: "43c1ea3"
      availability: available
    - path: docs/contrato-credenciais-sessao.md
      relationship: context
      representation: prose
      function: schema-contract
      format: Markdown
      analysis_scope: selected-section
      locator: "validação em rotas protegidas e identidade do proprietário"
      content_state: commit
      revision: "43c1ea3"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "instruções fornecidas e arquivo lido"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "43c1ea3"
      availability: available
---

# Análise de decisão — expor cadastro de formação acadêmica

## Solicitação original

v001: `$decision-analysis-v4 Implementar "Expor cadastro de formação acadêmica". Task para o back-end. Identifique as necessidades e siga de acordo com as documentações e requisitos.`

v002: `$decision-analysis-v4 Revisar a análise prompts/backend/20261014-193425-expor-cadastro-formacao-academica-v001.md, incorporando as decisões abaixo para resolver as perguntas em aberto. Gere a v002 como revisão da v001, atualizando linhagem, "Mudanças desde a versão anterior", decisão recomendada, validação e handoffs.`

v003: `$decision-analysis-v4 Revisar prompts/backend/20261014-194443-expor-cadastro-formacao-academica-v002.md e gerar a v003, corrigindo somente uma contradição interna da v002.

## Contradição

A v002 exige que `em_andamento` tenha data de fim nula e, ao mesmo tempo, permite datas futuras para registrar conclusão prevista. As duas regras são incompatíveis: uma formação em andamento não consegue informar a previsão de conclusão.

## Decisão de produto (tratar como requisito)

A coerência entre `status` e data de fim passa a ser:

- `em_andamento`: data de fim **opcional**, interpretada como previsão de conclusão.
- `concluido`: data de fim **obrigatória**.
- `interrompido`: data de fim opcional (sem mudança).

Em todos os casos, a data de fim não pode ser anterior à de início, e datas futuras continuam permitidas (sem mudança).

## Instruções

- Altere apenas o que a decisão exigir: regra de coerência no Domain, critérios de sucesso, CHECKs do modelo e da migration, matriz de testes, riscos e os trechos de DER e requisitos a atualizar.
- Verifique se a mudança afeta o nome ou a descrição de campos, a documentação (DER, requisitos) e os DTOs de request e response. Se a data de fim passar a ter dupla semântica (fim real ou previsão, conforme o status), registre isso como ponto de atenção e como a documentação deve explicitá-lo.
- Mantenha as demais decisões e o escopo da v002 sem mudança (POST, enums, limites de texto, rota, proprietário pela sessão).
- Registre a contradição e sua resolução em "Mudanças desde a versão anterior" e ajuste o impacto da revisão.
- Não implemente nada.`

## Informações complementares

Decisões de produto registradas na solicitação da v002, preservadas literalmente como histórico. A regra de status/período desse trecho foi corrigida pela decisão da v003 registrada acima:

> 1. Rota: `POST /formacoes-academicas`, confirmada. O proprietário continua vindo exclusivamente da sessão autenticada.
>
> 2. `nivel` passa a ser vocabulário controlado (enum), não texto livre. Valores:
>    - `ensino_fundamental`
>    - `ensino_medio`
>    - `tecnico`
>    - `tecnologo`
>    - `graduacao`
>    - `especializacao`
>    - `mestrado`
>    - `doutorado`
>
> 3. `status` passa a ser vocabulário controlado (enum). Valores:
>    - `em_andamento`
>    - `concluido`
>    - `interrompido`
>
> 4. Coerência entre `status` e período:
>    - `em_andamento` exige data de fim nula.
>    - `concluido` exige data de fim preenchida.
>    - `interrompido` aceita data de fim opcional.
>    - Em todos os casos, a data de fim não pode ser anterior à de início (regra já coberta pelo `Periodo`).
>    - Não validar data futura, pois o estudante pode informar conclusão prevista.
>
> 5. Limites de tamanho (em caracteres, após `strip`):
>    - `instituicao`: 1 a 200.
>    - `curso`: 1 a 200.
>    - `nivel` e `status`: sem limite de tamanho, pois são enums.
>    - Rejeitar valores vazios ou só com espaços.
>    - Rejeitar caracteres de controle.
>    - Os mesmos limites valem no DTO (API), na entidade/domínio e nas colunas do modelo SQLAlchemy e da migration, sem divergência entre camadas.

Instruções da análise v002, preservadas literalmente como histórico:

> - Os enums e a regra de coerência entre status e período são invariantes de negócio e devem ficar no Domain, como value objects/enums, não só na validação do DTO. Verifique como `FormacaoAcademica` e `CadastrarFormacaoAcademica` representam hoje `nivel` e `status` e avalie o impacto da mudança no caso de uso, na entrada e nos testes existentes da v001. Se a mudança no Domain/Application se mostrar desproporcional, apresente a alternativa de validar só na fronteira da API e justifique a recomendação.
> - O DTO da API deve usar os mesmos enums e traduzir violações em erro de validação (HTTP 422 ou o padrão já usado nas rotas existentes), sem expor detalhes internos.
> - Na persistência, armazenar os enums como texto, com constraint de tamanho compatível, sem tipo ENUM nativo do banco, para facilitar migrations futuras. Avalie se uma CHECK constraint é adequada ao padrão já usado no projeto.
> - Atualizar os critérios de sucesso e a validação com testes para: cada valor de enum, valor inválido, combinações válidas e inválidas de status e período, e limites de tamanho (mínimo, máximo e acima do máximo).
> - Registrar as perguntas antes em aberto como resolvidas, com a decisão e a justificativa. Se houver relação com o DER, verificar se `docs/modelagem_der.md` e `docs/requisitos_funcionais.md` precisam ser atualizados para refletir o vocabulário e os limites, e incluir isso no escopo.
> - Escopo mantido: apenas o cadastro (POST). Consulta, edição e exclusão ficam fora desta entrega. Não criar handoff para cards separados; mencionar apenas como fora do escopo, sem encaminhamento.
> - Não implementar nada; o resultado é somente a análise v002.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Rota | `POST /formacoes-academicas` como hipótese sujeita a confirmação | Caminho confirmado; proprietário somente pela sessão | Decisão de produto | Remove a incerteza do contrato de rota e reforça a regra de propriedade |
| Vocabulários | `nivel` e `status` sem valores aprovados, mantidos como strings | Enums controlados com oito níveis e três status definidos | Decisão de produto | Invariantes passam a residir no Domain; entrada e DTO tornam-se tipados |
| Coerência temporal | A v002 exigia `data_fim` nula para `em_andamento`, mas também permitia data futura como previsão | `em_andamento` aceita `data_fim` opcional como previsão; `concluido` exige data; `interrompido` mantém data opcional; cronologia e datas futuras permanecem como antes | Contradição apontada e resolvida pela decisão de produto desta revisão | Corrige a regra no Domain, DTO, CHECKs, testes e documentação; elimina a incompatibilidade sem alterar as demais decisões |
| Semântica do campo | `data_fim` era tratada genericamente como fim do período, embora previsões futuras fossem permitidas | O campo mantém nome e tipo, mas sua interpretação depende do status: previsão em `em_andamento`, data efetiva em `concluido` ou `interrompido` | Verificação do efeito solicitado sobre campos e contratos | DTO de request/response, DER e requisitos precisam explicitar a semântica condicional |
| Limites e caracteres | Limites e vocabulários pendentes | Instituição e curso de 1 a 200 após `strip`; rejeitar vazio e caracteres de controle; mesma faixa no DTO, domínio, coluna e migration | Decisão de produto | Normalização e tamanho devem ser uniformes; enum não recebe limite textual próprio |
| Domain/Application e testes | Tipos atuais são `str`; testes existentes cobrem apenas cenário nominal e usam strings | Atualizar entidade/entrada/caso de uso e fixtures para enums; adicionar testes de invariantes e faixas | Inspeção dos arquivos atuais mais requisito de produto | Impacto localizado e proporcional; validação não fica restrita à API |
| Documentação de dados | DER representa os campos genericamente como `string`; requisitos deixam limites em aberto | Atualizar DER e detalhamento funcional com limites, enumerações e coerência de período | Inspeção dos documentos atuais e decisão de produto | Documentação passa a ser contrato alinhado à implementação |
| Escopo | Cadastro por POST já recomendado; itens de RF02 listados como futuros | Somente cadastro POST; consulta, edição e exclusão continuam fora, sem handoff | Instrução explícita desta revisão | Mantém a entrega focada |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261014-193425-expor-cadastro-formacao-academica-v001.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree, não rastreado; análise anterior |
| `src/backend/domain/itens_perfil.py` | Principal | Código-fonte | Produção | Python | Entidade de formação e enums do módulo | Commit `43c1ea3` |
| `src/backend/application/perfil_estudante.py` | Principal | Código-fonte | Produção | Python | Entrada e caso de uso de formação | Commit `43c1ea3` |
| `src/backend/tests/test_domain_entities.py` | Apoio | Código-fonte | Teste | Python | Construção da entidade de formação | Commit `43c1ea3` |
| `src/backend/tests/test_application_perfil_estudante.py` | Apoio | Código-fonte | Teste | Python | Casos de cadastro e helper de entrada | Commit `43c1ea3` |
| `src/backend/api/experiencia_profissional.py` | Contexto | Código-fonte | Produção | Python | DTO, erro 422 e resposta | Commit `43c1ea3` |
| Modelos SQLAlchemy de competência e experiência | Contexto | Código-fonte | Produção | Python | Arquivos completos | Commit `43c1ea3` |
| `docs/modelagem_der.md` | Apoio | Modelo/diagrama | Contrato de schema | Markdown/DER | Entidade `FORMACAO_ACADEMICA` | Commit `43c1ea3` |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF01/RF02 e detalhamentos | Commit `43c1ea3` |
| `docs/contrato-credenciais-sessao.md` | Contexto | Prosa | Contrato | Markdown | Propriedade e rotas protegidas | Commit `43c1ea3` |
| `AGENTS.md` e `src/backend/AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Arquivos completos | Workspace/commit `43c1ea3` |

### Limites da evidência dos artefatos

Os módulos atuais comprovam que a entidade e a entrada usam `str` para `nivel` e `status`; o caso de uso encaminha esses valores diretamente à entidade. O teste de domínio usa `tecnologo`/`em_andamento`, e os testes de Application têm helper com os mesmos textos e um cenário nominal, além dos casos de perfil ausente/excluído. O módulo consultado de `Periodo` já rejeita data final anterior à inicial. Não encontrei `CheckConstraint` nos modelos de persistência examinados; portanto, CHECK é uma decisão nova a aplicar ao modelo e migration da formação, não uma convenção existente comprovada. O DER usa `string` sem limites explícitos para esses campos. Os arquivos de código e documentação estão no commit `43c1ea3`; a v001 da análise está no working tree e não será alterada.

## Problema enriquecido

### Resultado desejado

Expor `POST /formacoes-academicas` como fluxo durável, autenticado e coerente em todas as camadas. Formação válida usa somente os enums aprovados, texto de instituição/curso dentro dos limites após trim, status compatível com período e identidade de proprietário derivada da sessão.

### Atores e interesses

- Estudante: registrar formação em andamento, concluída ou interrompida, inclusive conclusão prevista, sem escolher outra conta como proprietária.
- API: validar o contrato de transporte com os enums e limites compartilhados, invocar o caso de uso e mapear violações para 422 sem revelar detalhes internos.
- Domain/Application: impedir que caminhos não HTTP ou objetos reconstruídos violem os valores e invariantes definidos pelo produto.
- Persistência: armazenar strings de enum e comprimentos compatíveis, reforçando valores e coerência com constraints relacionais sem enum nativo do banco.
- Consumidores e mantenedores: contar com requisito, DER, modelo, migration e testes alinhados.

### Evidências e fatos observados

- `FormacaoAcademica.nivel` e `.status` são atualmente strings; `CadastrarFormacaoAcademicaEntrada` também as declara como strings e o caso de uso transfere os valores à entidade.
- A entidade `FormacaoAcademica` hoje não declara `__post_init__` com validação própria. `Periodo` valida a cronologia, mas não conhece status.
- Testes atuais exercitam um cadastro nominal com `nivel="tecnologo"` e `status="em_andamento"`; cobrem proprietário ativo, inexistente e excluído, mas não os novos vocabulários, combinações, tamanhos ou caracteres de controle.
- `POST /formacoes-academicas` e a propriedade pela sessão foram confirmados pelo produto. O contrato de sessão já determina que a identidade confiável venha do contexto autenticado.
- O DER representa instituição, curso, nível e status como strings genéricas. O documento de requisitos ainda aponta limites dos dados cadastrados como detalhamento necessário.
- Modelos SQLAlchemy examinados usam `String`, `Text` e constraints relacionais usuais, mas não apresentam `CheckConstraint`. A formação ainda precisará de modelo, repositório e migration, conforme a análise v001.

### Hipóteses

- `strip` significa remover espaços externos e persistir o valor normalizado, de modo que DTO, entidade e armazenamento aceitem e guardem a mesma representação. A implementação deve aplicar a normalização uma vez de modo explícito e manter equivalência entre as camadas.
- Caracteres de controle devem ser rejeitados nos campos textuais `instituicao` e `curso`; enumerações só aceitam os valores listados e não são tratadas como texto livre com um limite de comprimento independente.
- Restrições de tamanho relacionais usam colunas `String(200)` e CHECK para mínimo após trim; constraints de valores enum e coerência status/período são CHECKs sobre texto/data. A regra de caracteres de controle deve ser implementada no Domain/API e, se o dialeto usado permitir expressão portável, reforçada no banco sem divergência semântica.
- Não deve haver rejeição por data futura: `Periodo` só mantém a ordem cronológica e as regras de status/fim definidas pelo produto.

### Perguntas em aberto

As decisões de produto já fecharam as questões de rota, vocabulário e limites na v002. A única contradição identificada nesta revisão — exigência de fim nulo para `em_andamento` simultânea à permissão de datas futuras como previsão — fica resolvida pelo novo requisito de `data_fim` opcional para esse status. Não restam perguntas de produto sobre este ponto.

- **Rota e proprietário:** resolvido para `POST /formacoes-academicas`; o proprietário vem somente da sessão autenticada, pois o contrato de sessão proíbe confiar em identificador fornecido pelo cliente.
- **Vocabulário de `nivel`:** resolvido como enum com `ensino_fundamental`, `ensino_medio`, `tecnico`, `tecnologo`, `graduacao`, `especializacao`, `mestrado` e `doutorado`.
- **Vocabulário de `status`:** resolvido como enum com `em_andamento`, `concluido` e `interrompido`.
- **Relação status/período:** resolvida; `em_andamento` aceita fim nulo ou preenchido (se preenchido, representa previsão de conclusão), `concluido` requer fim preenchido e `interrompido` aceita fim nulo ou preenchido; sempre rejeitar fim anterior ao início; data futura é permitida.
- **Limites e conteúdo textual:** resolvidos; `instituicao` e `curso` devem ter de 1 a 200 caracteres após `strip`, rejeitar branco e controles, e cumprir a mesma regra no DTO, entidade, colunas e migration. Os campos enum não recebem limite de texto.
- **Atualização documental:** resolvida como necessária, pois DER e requisitos atuais ainda não declaram a nova semântica.

### Escopo

- Criar o contrato HTTP `POST /formacoes-academicas`, com DTO tipado pelos mesmos enums do Domain, sem `usuario_id` controlável no request; resposta com DTO explícito e HTTP 201 conforme padrão de cadastro. Request e response mantêm o nome `data_fim`, mas documentam que, para `em_andamento`, a data é uma previsão, e para os demais status representa a data efetiva informada.
- Definir enums/value objects de `NivelFormacaoAcademica` e `StatusFormacaoAcademica` no Domain e atualizar `FormacaoAcademica` para validar enums, `instituicao`/`curso`, coerência com `Periodo` e rejeição de caracteres de controle.
- Atualizar `CadastrarFormacaoAcademicaEntrada` e `CadastrarFormacaoAcademica` para transportar os tipos de domínio, preservando geração/persistência e as regras de perfil existente; a validação não deve ficar duplicada como fonte de verdade na Application.
- Na API, validar enums, normalizar e limitar textos de acordo com a política de `strip`, converter datas em `Periodo` e traduzir enum desconhecido, campo inválido ou regra de domínio em HTTP 422, usando mensagens seguras e padrão coerente com rotas existentes.
- Criar modelo SQLAlchemy com `instituicao` e `curso` de comprimento 200 e campos enum armazenados como texto, sem tipo ENUM nativo. Adicionar CHECKs para tamanhos mínimos/máximos após trim, valores aceitos e coerência status/período: `em_andamento` pode ter `data_fim` nula ou preenchida; `concluido` exige valor; `interrompido` aceita ambos; valor preenchido deve ser igual ou posterior à data de início. Assegurar equivalência no modelo e migration; não aplicar CHECK de data futura.
- Criar migration Alembic e repositório concreto, conectar o caso de uso na composição e registrar o router.
- Atualizar `docs/modelagem_der.md` para declarar comprimentos, vocabulários, nulabilidade e semântica de `data_fim` conforme o status; atualizar `docs/requisitos_funcionais.md` para substituir a pendência genérica por validações decididas e explicar que a data de fim pode ser previsão ou data efetiva.
- Atualizar testes de Domain, Application, API e persistência/migration: todos os valores de enums; enum inválido; combinações válidas e inválidas de status/fim; cronologia; ausência de rejeição de data futura; textos no mínimo e máximo, vazios, só espaços, acima do máximo e com controle; alinhamento dos constraints.
- Atualizar docstrings e proveniência dos códigos e documentos envolvidos.

### Fora do escopo

- Consultar, editar ou excluir formação acadêmica; a entrega se limita ao cadastro `POST`.
- Alterar limites de agregados, implementar funcionalidades do frontend ou introduzir enum nativo do banco.
- Impor limite de tamanho a `nivel`/`status` ou rejeitar data futura.
- Criar encaminhamento/handoff para cards de consulta, edição ou exclusão.

### Critérios de sucesso

- `POST /formacoes-academicas` responde 201 para sessão válida e corpo que satisfaz o contrato; proprietário é atribuído exclusivamente do contexto da sessão.
- Todos os oito níveis e três status aceitos são representados por enums do Domain e pelo DTO; qualquer valor não listado falha em 422 sem chamar persistência.
- Domain, não somente API, rejeita enum inválido, texto vazio/só espaços, texto com controle, texto com mais de 200 após strip, `concluido` sem data final e data final anterior à inicial.
- Combinações válidas são aceitas: `em_andamento` sem data fim ou com previsão; `concluido` com data fim; `interrompido` com ou sem data fim. Data futura não é rejeitada quando coerente com as demais regras.
- `instituicao` e `curso` aceitam limites 1 e 200 após strip; aceitam valores maiores em caracteres somente até 200 depois da normalização; 201 após strip é rejeitado. DTO, entidade, colunas e migration mantêm critérios equivalentes.
- SQLAlchemy persiste enums como texto com CHECK constraints, não enum nativo; migration é Code First e preserva as mesmas faixas e regras.
- DER e requisitos descrevem o novo contrato, os limites, a nulabilidade e o significado condicional de `data_fim`, sem manter a antiga afirmação de que os limites ainda estão pendentes.
- Testes unitários pertinentes rodam em `nix develop .#backend`; testes de integração/modelo de dados, se usados, rodam em `nix develop .#tests`.

## Restrições aplicáveis

- Clean Architecture e DDD: enums e coerência status/período são invariantes do domínio; DTO não substitui entidade/value object nem se torna única defesa.
- API: DTO usa os enums do domínio e converte violações a erro de validação público 422, sem mensagens internas sensíveis; identidade exclusivamente da sessão.
- Persistência: Code First com migration; enum armazenado em texto e checks relacionais, sem ENUM nativo.
- Texto: `instituicao` e `curso` normalizados com `strip`, 1–200 caracteres, sem controles, com consistência em DTO, Domain e schema relacional.
- Sem data futura como violação; cronologia continua protegida por `Periodo`.
- Escopo restrito a POST; funções, classes e DTOs novos ou alterados requerem documentação conforme regras do repositório.
- Testes unitários backend usam o ambiente Nix `backend`; testes de integração usam `tests`.

## Classificação comentada

`engineering` permanece a esfera primária. As preocupações são `domain`, `data` e `integration`: as decisões agora definem invariantes, restrições de armazenamento e o contrato HTTP/Domain. O escopo continua em um componente e no ciclo de entrega. A incerteza cai de média para baixa para os requisitos de produto; há incerteza técnica residual quanto à expressão relacional portável para caracteres de controle e à sintaxe exata do dialecto, sem alterar a regra de domínio. Risco médio decorre de dados pessoais, autorização por propriedade e migration de schema.

## Decisão de roteamento

Manter `prompts/backend`, destino da v001 e ainda semântico para Domain, Application, API e persistência do backend. A revisão adiciona contratos de produto/documentação como artefatos de apoio, sem mudar o objetivo principal. As demais subpastas imediatas existentes (`ambientes`, `frontend`, `requisitos`, `revisao` e `templates`) foram consideradas; não se escolhe `requisitos` porque a decisão central especifica uma mudança de implementação integrada ao backend e a continuidade da linhagem favorece o diretório anterior.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| Correção | Alta | Maximizar | Vocabulários e coerência de período passam a ser invariantes explícitas |
| Segurança e privacidade | Alta | Satisfazer | Somente a sessão define o proprietário dos dados pessoais |
| Interoperabilidade | Alta | Priorizar | DTO, Domain, banco e documentos devem aceitar a mesma linguagem e limites |
| Modificabilidade | Média | Satisfazer | Enum serializado como texto e migration evitam acoplamento a enum nativo |
| Simplicidade | Média | Satisfazer | Mudança fica concentrada no cadastro e não cria CRUD adicional |

## Alternativas consideradas

### Alternativa A — invariantes no Domain, DTO tipado e persistência textual com CHECK

Usar enums/value objects de domínio para nível/status; validar no Domain conteúdo, faixa e coerência com o período; transportar esses tipos em Application e DTO; armazenar valores como texto com tamanho e CHECK constraints; alinhar DER/requisitos/testes. Recomendada. A mudança é localizada: dois campos existentes passam de `str` a tipos de domínio, a entidade recebe invariantes, o caso de uso apenas encaminha valores tipados e fixtures existentes são atualizadas.

### Alternativa B — validar enums e regras somente no DTO da API

Manter os campos como strings em Domain/Application e aceitar apenas valores válidos no POST. É mais curta para a rota, mas deixa entidades criáveis por chamadas internas, testes, adapters e reconstrução de registros sem as mesmas invariantes. Também permite divergência futura entre a camada de transporte e o modelo persistido. Inadequada para regras que o produto definiu como invariantes de negócio.

### Alternativa C — validar apenas na Application, sem tornar a entidade tipada

Fazer o caso de uso verificar strings e coerência antes de construir a entidade. Centraliza a regra fora da API, porém mantém a entidade inválida representável e duplica semântica com construtores/reconstituição. Não atende tão diretamente à instrução de colocar invariantes no Domain.

### Alternativa D — usar ENUM nativo do banco como autoridade de vocabulário

Mapear enumeração diretamente ao tipo ENUM do banco. Pode impor valores na persistência, mas cria acoplamento e migrations potencialmente mais difíceis; não protege instâncias de domínio e não resolve DTO/HTTP. Contraria a decisão de serializar como texto com CHECK.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Alternativa D | Confiança | Base |
|---|---:|---:|---:|---:|---:|---|---|
| Correção | Alta | +2 | -2 | +1 | +1 | Alta | Requisitos do produto e atual entidade sem invariantes |
| Segurança e privacidade | Alta | +2 | +1 | +1 | 0 | Alta | Identidade da sessão e defesa de camada interna |
| Interoperabilidade | Alta | +2 | 0 | +1 | -1 | Média | Limites comuns por camadas; dialeto de banco ainda não confirmado |
| Modificabilidade | Média | +2 | +1 | 0 | -2 | Alta | Textos com CHECK evitam enum específico do banco |
| Simplicidade | Média | +1 | +2 | 0 | -1 | Média | Domain/Application exigem atualização pequena; CHECK adiciona schema |

O delta desta versão restringe a comparação à correção da regra temporal: manter a regra contraditória da v002 seria inviável porque impede registrar previsão para `em_andamento`; tornar `data_fim` opcional para esse status preserva o contrato de data futura e satisfaz a decisão de produto.

## Histórico e decisão atual

### Decisão da versão anterior

A v001 recomendou fluxo durável em `POST /formacoes-academicas`, sessão como fonte de proprietário, DTO explícito, caso de uso, adapter e migration Code First. Nível/status permaneceriam como representados no domínio até decisão de produto; campos e limites estavam em aberto; atualizar DER/requisitos era condicional à confirmação. O fim da data futura não tinha posição definida.

### Decisão recomendada nesta versão

Manter a Alternativa A e corrigir a contradição da v002. Confirmar a rota `POST /formacoes-academicas`; criar no Domain enums tipados para os oito níveis e três status e fazer `FormacaoAcademica` proteger a relação status/período. `em_andamento` aceita `data_fim` nula ou preenchida; quando preenchida, significa previsão de conclusão. `concluido` exige `data_fim` preenchida, e `interrompido` aceita ambas as formas. Em todos os casos, `Periodo` impede fim anterior ao início. Datas futuras continuam permitidas.

Validar e normalizar instituição/curso por `strip`; rejeitar vazio, controle e mais de 200 caracteres depois do trim. Para evitar divergência, o DTO aplica a mesma normalização/limites e usa os mesmos enums; a entidade continua sendo a autoridade das invariantes. A resposta de violações é 422 no padrão de API existente. No banco, usar colunas de texto limitadas a 200 para instituição/curso, texto para valores enum e CHECKs para vocabulários, tamanho/trim e coerência status/período. O CHECK temporal aceita `data_fim` nula ou preenchida em `em_andamento` e `interrompido`, exige valor em `concluido` e exige que qualquer valor preenchido seja igual ou posterior ao início. Não usar enum nativo nem CHECK de data futura.

Manter o nome `data_fim` nos DTOs de request/response e nas colunas: o campo continua representando o limite temporal do registro, com interpretação condicional pelo status. Documentar a dupla semântica — previsão em `em_andamento`, data efetiva em `concluido` e `interrompido` — nas descrições de request/response, no DER e nos requisitos funcionais. Não é necessário renomear o campo.

Atualizar `docs/modelagem_der.md` com tamanhos e vocabulários/regras e `docs/requisitos_funcionais.md` para registrar esses critérios, removendo-os da lista de detalhamentos pendentes. A alteração no Domain/Application é proporcional: entidade e entrada hoje usam `str`, caso de uso apenas repassa valores, e os testes existentes precisam atualizar duas strings e ampliar cobertura. Validar apenas na API é uma alternativa insuficiente.

### Impacto da revisão

`revised`: corrige uma contradição da v002 que impedia informar previsão de conclusão em formação `em_andamento`. Arquitetura, rota, enums, limites, proprietário pela sessão e escopo POST permanecem inalterados; regra de Domain, critérios, CHECK, testes, riscos e documentação passam a aceitar `data_fim` opcional nesse status e explicitar seu significado.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Correção | maximized | Cada instância e registro respeita enums e coerência revisada entre status/período, incluindo previsão em `em_andamento` | Decisão de produto desta revisão e contradição registrada na v002 |
| Segurança e privacidade | prioritized | Propriedade sempre vinculada à sessão autenticada | Rota confirmada e contrato de sessão |
| Interoperabilidade | prioritized | Mesmo vocabulário, trim e faixas no DTO, Domain, schema e documentação | Decisão explícita de equivalência entre camadas |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Simplicidade | Uma única operação de criação | Consulta, edição e exclusão permanecem fora do escopo |
| Modificabilidade | Sem acoplamento ao enum do banco | Valores enum persistidos como texto e protegidos por CHECK |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Correção | Formações inconsistentes entre status e datas, ou com vocabulário inválido, podem aparecer em currículos | Alta | Estudantes, consumidores e suporte |
| Segurança e privacidade | Dados de formação podem ser associados a outro usuário | Crítica | Estudantes e instituição |
| Interoperabilidade | API, banco e cliente divergem em valores ou limites e rejeitam dados de forma inconsistente | Alta | Frontend, backend e dados persistidos |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Correção | Adicionar enums, invariantes e testes ao Domain, atualizar Application/fixtures | Velocidade de entrega | Aceitável; alteração localizada e protege todos os caminhos |
| Correção/interoperabilidade | Adicionar CHECKs e limites no modelo/migration e atualizar documentos | Simplicidade do schema | Aceitável; reduz divergência silenciosa |
| Segurança | Rejeitar requisições sem sessão e não aceitar proprietário externo | Facilidade de chamada manual | Aceitável para dado pessoal |

## Riscos e efeitos de segunda ordem

- Mudanças para enums tipados afetam construtores, exportações e fixtures que hoje passam strings. Procurar usos em todo o backend antes de implementação e preservar serialização `.value` nas fronteiras.
- `strip` precisa significar o mesmo nas camadas e o valor persistido deve ser canônico; validar tamanho antes do trim produziria divergência, sobretudo para entradas de 201 caracteres com espaços externos.
- CHECKs de trim, enum e status/período precisam ser expressos de forma compatível com a versão do banco usada nos testes e produção. Não usar ENUM nativo nem deixar migration mais permissiva que o modelo.
- Rejeição de caracteres de controle tem de cobrir os campos institucionais e do curso em HTTP e Domain. Uma expressão SQL não portável não deve virar falsa garantia; a regra primária permanece no Domain e eventual reforço deve ser demonstrado no dialecto adotado.
- `data_fim` tem semântica condicional: previsão de conclusão em `em_andamento`, data efetiva de conclusão em `concluido` e data de interrupção/fim em `interrompido`. O nome permanece; descrições dos DTOs request/response, DER e requisitos devem explicitar o significado para impedir que consumidores interpretem previsão como conclusão ocorrida.
- Em `em_andamento`, uma previsão futura pode ser preenchida ou permanecer nula. O Domain e o banco não podem impor nulidade para esse status; `concluido` continua exigindo data.
- DER e RF descrevem contratos diferentes se apenas um for alterado; ambos devem ser atualizados junto com código e migration.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Cada nível/status permitido é aceito e convertido corretamente | Um caso para cada um dos oito níveis e três status | Testes unitários Domain/API e comparação da serialização de enum | Diferença entre valor aceito no DTO, Domain ou banco |
| Valores enum desconhecidos são rejeitados antes de persistir | Exemplos desconhecidos ou com caixa/grafia diferentes | Teste HTTP 422 e teste de construção Domain; verificar zero chamadas ao repositório | Produto definir aliases ou normalização de enum |
| Coerência de status com fim é preservada | `em_andamento` com fim nulo e com previsão; `concluido` com data e sem data; `interrompido` com data e sem data | Matriz de testes Domain/API, incluindo chamadas diretas ao construtor | Qualquer combinação aprovada divergir das regras de produto |
| Cronologia continua válida e datas futuras podem representar previsão | Fim antes do início e previsão futura em formação `em_andamento` | Teste de domínio para erro cronológico e aceite de previsão futura | Produto alterar regra de previsão ou `Periodo` |
| Limites textuais são iguais após strip | Tamanho 1, 200 e 201 depois do trim; vazio, espaços e prefixo/sufixo em branco | Testes em DTO, entidade e persistência/migration | Uma camada medir antes da normalização ou aplicar limite distinto |
| Controles não entram por nenhum caminho | Exemplos de caracteres de controle em instituição/curso | Testes de API e construção direta Domain; validar CHECK se implementado | Dialeto não permitir reforço semântico equivalente no banco |
| Migration e modelo refletem o mesmo contrato | Comprimento de colunas e CHECKs observáveis; fim opcional em andamento/interrompido, obrigatório em concluído, nunca anterior ao início | Teste de metadados/migration e integração no banco do projeto | Modelo e migration diferirem ou CHECK não ser suportado no alvo |
| Campo e documentação explicam a semântica condicional | Mesmo `data_fim` em request/response, com descrição de previsão para andamento e data efetiva para concluído/interrompido; DER/RF equivalentes | Revisar schema OpenAPI/DTOs e trechos documentais | Consumidores confundirem previsão com fim ocorrido ou produto pedir distinção de campos |
| Proprietário só vem da sessão | Requisição com identidade externa contraditória | Teste de API com executor spy e contexto autenticado | Framework não fornecer contexto confiável comum |

## Handoffs e atividades posteriores

- Implementar a atualização tipada no Domain/Application, a rota/DTO autenticados, o modelo SQLAlchemy, o repositório e a migration para o cadastro POST.
- Adicionar os testes de domínio, Application, API e persistência descritos na validação; executar unitários com `nix develop .#backend` e integração com `nix develop .#tests` quando aplicável.
- Atualizar `docs/modelagem_der.md` e `docs/requisitos_funcionais.md` para publicar os vocabulários, limites, coerência temporal e semântica condicional de `data_fim`, além da rota/proprietário já decididos.
- Confirmar no banco-alvo a sintaxe das CHECKs e documentar qualquer limite técnico para checks de caracteres de controle, mantendo a regra de domínio obrigatória.

## Síntese

Esta revisão corrige a contradição da v002: `em_andamento` aceita `data_fim` opcional como previsão; `concluido` requer data e `interrompido` continua opcional. A cronologia segue protegida e datas futuras são permitidas. O nome `data_fim` permanece nos DTOs e no modelo, mas suas descrições e a documentação (DER e requisitos) devem explicitar a semântica condicional. Rota, sessão, enums, limites, persistência textual, constraints e escopo de cadastro POST não mudam. A análise não implementa nada.
