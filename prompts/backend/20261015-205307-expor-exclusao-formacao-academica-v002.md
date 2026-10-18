---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v002"
status: proposed
created_at: "2026-10-15T20:53:07-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261015-204510-expor-exclusao-formacao-academica-v001.md
  supersedes: prompts/backend/20261015-204510-expor-exclusao-formacao-academica-v001.md
  change_type: enrichment
  secondary_change_types: [reassessment]
  decision_impact: strengthened
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20261015-204510-expor-exclusao-formacao-academica-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "v001; versão anterior desta linhagem"
      availability: available
    - path: prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "contexto implementado indicado pelo usuário; não reaberto"
      content_state: working-tree
      revision: "v003"
      availability: available
    - path: prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "edição implementada e questão anterior sobre currículos"
      content_state: working-tree
      revision: "v001"
      availability: available
    - path: src/backend/domain/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "estado excluído e operação idempotente de Usuario"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ExcluirPerfil, EditarFormacaoAcademica e CadastrarFormacaoAcademica"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioFormacaoAcademica e ConsultaItemPerfil"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "coluna deleted_at do usuário"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/formacao_academica.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_formacao_academica.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "CurriculoItemRegistro e mapeamento das referências polimórficas"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/previa_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "GerarPreviaVersaoCurriculo consulta ConsultaItemPerfil.obter_item"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_application_perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "testes de EditarFormacaoAcademica e doubles do repositório"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_infrastructure_formacao_academica.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "testes da consulta e atualização SQLAlchemy de formação"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_api_edicao_formacao_academica.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "contrato HTTP de edição e resposta de não encontrada"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261014_0007_criar_formacoes_academicas.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python/Alembic
      analysis_scope: selected-section
      locator: "CHECKs e schema existente que a nova migration não deve alterar"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: Markdown/Mermaid ER
      analysis_scope: selected-section
      locator: "CURRICULO_FORMACAO, FORMACAO_ACADEMICA e modelo de associações"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF02 e detalhamentos"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/requisitos-seguranca.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "4.10 retenção e exclusão; 4.11 direitos do usuário; prazo não definido"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/fundamentos-backend.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "PostgreSQL e Psycopg como banco/driver do backend"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/formacao_academica.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "rotas e handlers de cadastro/edição"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "DELETE de perfil autenticado: 204/404/503"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/exclusao_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "DELETE de currículo: 204/404/503"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "tabela curriculo_itens, chave para currículo e sem FK para item"
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "Continuidade da linhagem de exclusão de formação, cujo objeto é operação do backend e persistência."
classification:
  sphere: engineering
  concerns: [domain, data, privacy]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: low
  reversibility: moderate
  risk: medium
---

# Análise de decisão — expor exclusão de formação acadêmica

## Solicitação original

Preservada literalmente da v001:

> `$decision-analysis-v4 Implementar "Expor exclusão de formação acadêmica". Task para o back-end. Identifique as necessidades e siga de acordo com as documentações, os requisitos e o que já está implementado.
>
> ## Contexto (já implementado, não reabrir)
>
> Cadastro e edição de formação acadêmica estão implementados. Use como artefatos de apoio, sem revisá-los (esta é uma nova linhagem):
> - prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md
> - prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md
>
> Isso inclui:
> - Domain: `FormacaoAcademica` (com `editar`), enums de nível e status, constantes de tamanho.
> - Application: `CadastrarFormacaoAcademica`, `EditarFormacaoAcademica`, `FormacaoAcademicaNaoEncontrada`; a porta `RepositorioFormacaoAcademica` com `salvar`, `obter_por_id_e_usuario` e `atualizar`.
> - API: `POST /formacoes-academicas` e `PUT /formacoes-academicas/{formacao_id}`, proprietário só pela sessão, 404 idêntico para ausente e alheio.
> - Persistência: modelo SQLAlchemy, repositório concreto, migration 20261014_0007 com CHECKs.
>
> Nada disso deve mudar de comportamento, exceto onde a exclusão exigir (por exemplo, edição de uma formação já excluída).
>
> ## O que investigar
>
> - **Estratégia de exclusão:** exclusão lógica (marcador como `deleted_at`) ou física. Já existe `ExcluirPerfil` com exclusão lógica e `deleted_at`; verifique se algum outro item (versão de currículo, competência, experiência) tem exclusão, qual o padrão, e o que os documentos dizem (DER, requisitos funcionais, RF02 e qualquer menção a retenção, LGPD ou purga). Recomende uma estratégia com justificativa.
> - **Impacto em currículos:** versões de currículo referenciam formações? Existe chave estrangeira, tabela de associação ou cópia dos dados? O que acontece com um currículo já gerado quando a formação é excluída (bloqueia a exclusão, remove a referência, mantém uma cópia)? Esta pergunta ficou sem resposta na análise de edição e agora é central. Se depender de decisão de produto, separe com clareza e apresente as opções com recomendação.
> - **Repetição (idempotência):** excluir uma formação já excluída deve retornar 404 ou sucesso? Compare com `ExcluirPerfil` (que trata repetição como sucesso sem novo efeito) e recomende, considerando que ausente e alheio devem continuar indistinguíveis.
> - **Contrato HTTP:** método DELETE em `/formacoes-academicas/{formacao_id}`, código de sucesso (204 ou 200), 404 uniforme, 401, 503 e o padrão dos handlers existentes.
> - **Efeito sobre o que já existe:** se a exclusão for lógica, formações excluídas não podem ser encontradas por `obter_por_id_e_usuario`, nem editadas por `PUT`. Avalie o impacto na porta, no repositório concreto, nos testes e em qualquer consulta futura. Se for física, avalie integridade referencial.
> - **Persistência:** se a mudança exige migration (coluna de exclusão lógica, índice, ajuste de constraints) e qual o impacto sobre os CHECKs e a migration 20261014_0007. Confirme o banco-alvo (PostgreSQL via psycopg, com SQLite nos testes) e a compatibilidade da migration com os dois.
> - **Concorrência:** avalie edição e exclusão simultâneas sobre o mesmo registro (last-write-wins é aceitável?).
> - **Documentação:** necessidade de atualizar docs/modelagem_der.md e docs/requisitos_funcionais.md (RF02).
>
> ## Escopo
>
> Somente a exclusão de formação acadêmica pelo próprio estudante autenticado. Fora do escopo: consulta de formação, front-end, purga física posterior de registros excluídos logicamente (a menos que a análise a identifique como obrigatória por requisito), e qualquer mudança nas regras de cadastro e edição além do necessário.
>
> ## Instruções
>
> - Recomende as decisões técnicas e separe o que depende de decisão de produto, para eu decidir antes da implementação.
> - Indique a divisão entre Domain/Application (`$backend-domain-orchestration-v2`) e API/persistência (`$backend-adapters-drivers-v2`), e o que fica fora das duas skills (documentação, testes de integração com `$integration-system-testing-v1`). Se a migration for necessária, indique em qual das duas ela entra.
> - Registre na validação o comando do gate de lint do CI, `ruff check src/backend`, executado com `nix develop .#quality --command`, para que as execuções o rodem ao final.
> - Não implemente nada.`

## Informações complementares

Decisões fornecidas pelo usuário nesta revisão, tratadas como requisito:

1. Exclusão lógica com `deleted_at` anulável, sem purga física e sem remover linhas de `curriculo_itens`.
2. Opção A para currículos: manter seleções existentes; não criar leitura histórica nova nesta entrega. Se não existir consulta concreta, registrar a obrigação para implementação futura de prévia/exportação; se existir, indicar seu ponto e ajuste.
3. Repetição pelo dono retorna 204 e preserva o primeiro `deleted_at`; ausente/alheio continuam 404 idêntico. Adicionar método de porta que localize item próprio inclusive quando excluído, usado apenas pelo fluxo de exclusão.
4. Exclusão vence edição concorrente: edição usa UPDATE condicional por ID, dono e `deleted_at IS NULL`, verifica linhas afetadas e traduz zero linhas a não encontrada; exclusão também marca condicionalmente somente quando `deleted_at IS NULL`.
5. Retenção e purga permanecem pendência de governança. Não inferir obrigação nem prazo; reconhecer que direito de eliminação pode requerer purga física.
6. Contrato HTTP: DELETE `/formacoes-academicas/{formacao_id}`, 204 sem corpo, 404 uniforme, 401 pelo middleware, 503 conforme padrão; proprietário somente da sessão.
7. Migration aditiva apenas com coluna timestamp com timezone anulável; sem índice e sem alterar CHECKs existentes; compatível com PostgreSQL e SQLite.
8. Atualizar DER e RF02; corrigir no DER a representação da relação polimórfica `curriculo_itens` e explicar a manutenção de seleções.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Status e decisão de produto | `pending` por comportamento de currículo e retenção sem decisão | `proposed`; comportamento de currículo definido; retenção apenas como pendência de governança fora da entrega | Decisões explícitas do usuário | Não bloqueia implementação nos itens resolvidos |
| Leitura de currículo | V001 não localizou consulta concreta e tratou renderização como aberta | Há caso de uso `GerarPreviaVersaoCurriculo` que chama `ConsultaItemPerfil.obter_item`, mas não foi encontrada implementação concreta da porta nem fluxo de exportação produtivo | Nova inspeção de código solicitada | Sem ajuste de leitura agora; futuras implementações devem incluir formação excluída quando o ID estiver em seleção persistida |
| Associação/DER | DER desenhava relação muitos-para-muitos dedicada `CURRICULO_FORMACAO` | Schema atual usa `curriculo_itens`, polimórfica, com FK apenas para currículo e sem FK/cópia do item | Correção de divergência documental exigida | Atualizar DER para refletir tipo + item_id e ausência de integridade referencial para o item |
| Repetição e porta | Sucesso repetido recomendado, método de porta adicional não especificado | DELETE usa `obter_por_id_e_usuario_incluindo_excluidas`, com filtro simultâneo por ID e proprietário; repetição retorna sem regravar timestamp | Decisão de produto e contrato interno explicitados | Mantém não divulgação; busca adicional só é usada pela exclusão |
| Edição concorrente | Exclusão deveria prevalecer, detalhes de adapter pendentes | `atualizar` passa a confirmar resultado e executar UPDATE com ID + usuário + `deleted_at IS NULL`; zero linhas equivale a não encontrada | Requisito de concorrência especificado | Domain/Application transforma falha de atualização em `FormacaoAcademicaNaoEncontrada`; atualizar doubles e testes |
| Exclusão concorrente | Repetição idempotente sem condição SQL definida | UPDATE de marcação inclui `deleted_at IS NULL`; zero linhas seguido de leitura própria incluindo excluída confirma repetição sem mudar instante | Requisito de concorrência | Preserva primeiro instante e impede sobrescrever marcador |
| Schema | Migration nova com coluna anulável era recomendação | Migration aditiva somente com timestamp com timezone nullable; sem índice ou mudanças de CHECK | Decisão de produto/implementação | Nova migration em adapters/drivers; não reescrever migration existente |
| Documentação | Atualizar DER/RF02, mas detalhe de currículo aberto | Atualizar ambos com exclusão lógica, seleção preservada e representação real de `curriculo_itens` | Escopo fechado | Atividade documental separada das skills de código |
| Retenção | Sem política/prazo; validação necessária | Exclusão lógica basta agora; prazo/purga e possível direito de eliminação ficam em governança | Requisito explícito | Não bloqueia v002; pode motivar decisão futura de purga |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261015-204510-expor-exclusao-formacao-academica-v001.md` | Principal | Prosa | Documentação de decisão | Markdown | Arquivo completo | Working tree, v001 |
| `prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md` | Apoio | Prosa | Documentação de decisão | Markdown | Contexto implementado | Working tree, v003 |
| `prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md` | Apoio | Prosa | Documentação de decisão | Markdown | Contexto de edição e questão curricular | Working tree, v001 |
| `src/backend/domain/usuario.py` | Apoio | Código-fonte | Produção | Python | Exclusão lógica idempotente | Working tree |
| `src/backend/application/perfil_estudante.py` | Apoio | Código-fonte | Produção | Python | Exclusão de perfil e edição de formação | Working tree |
| `src/backend/application/ports.py` | Apoio | Código-fonte | Produção | Python | Porta de formação e consulta genérica de item | Working tree |
| `src/backend/infrastructure/persistence/sqlalchemy/usuario.py` | Apoio | Código-fonte | Produção | Python | Persistência de deleted_at do usuário | Working tree |
| `src/backend/infrastructure/persistence/sqlalchemy/formacao_academica.py` e `repositorio_formacao_academica.py` | Principal | Código-fonte | Produção | Python | Modelo e adapter completos | Working tree |
| `src/backend/infrastructure/persistence/sqlalchemy/curriculo.py` | Apoio | Código-fonte | Produção | Python | Registro de seleção polimórfica | Working tree |
| `src/backend/application/previa_versao_curriculo.py` | Apoio | Código-fonte | Produção | Python | Leitura dos itens pela porta e montagem da prévia | Working tree |
| `src/backend/tests/test_application_perfil_estudante.py` | Apoio | Código-fonte | Teste | Python | Edição e doubles/repositórios de Application | Working tree |
| `src/backend/tests/test_infrastructure_formacao_academica.py` | Apoio | Código-fonte | Teste | Python | SQLAlchemy, busca e atualização | Working tree |
| `src/backend/tests/test_api_edicao_formacao_academica.py` | Apoio | Código-fonte | Teste | Python | Contrato de edição HTTP | Working tree |
| `src/backend/infrastructure/persistence/alembic/versions/20261014_0007_criar_formacoes_academicas.py` | Apoio | Código-fonte | Produção | Python/Alembic | CHECKs e schema atual | Working tree |
| `docs/modelagem_der.md` | Apoio | Modelo | Contrato de schema | Markdown/Mermaid | Entidades formação e currículo | Working tree |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF02 e detalhamentos | Working tree |
| `docs/requisitos-seguranca.md` | Contexto | Prosa | Documentação | Markdown | Retenção, purga e direitos | Working tree |
| `docs/fundamentos-backend.md` | Contexto | Prosa | Documentação | Markdown | PostgreSQL/Psycopg | Working tree |
| `src/backend/api/formacao_academica.py` | Apoio | Código-fonte | Produção | Python | Padrão de proprietário pela sessão e respostas | Working tree |
| `src/backend/api/perfil_estudante.py` e `src/backend/api/exclusao_versao_curriculo.py` | Contexto | Código-fonte | Produção | Python | Handlers de exclusão e códigos HTTP | Working tree |

### Limites da evidência dos artefatos

A v001 foi integralmente lida e não foi alterada. Os dois artefatos de cadastro/edição foram usados só como contexto, sem reabrir suas decisões. A inspeção ampliada identificou o consumidor de leitura de currículo em `GerarPreviaVersaoCurriculo`, mas a busca no backend de produção não encontrou adapter concreto para `ConsultaItemPerfil` nem fluxo implementado de exportação que consulte formações; referências em fixtures e testes não foram tratadas como implementação produtiva. Por isso, a decisão do usuário não exige código de leitura histórica nesta entrega.

Os arquivos de código e documentação representam o working tree observado, sem hash de commit fixado. O pedido de atualizar DER/RF02 define trabalho posterior, não altera esses documentos nesta análise.

## Problema enriquecido

### Resultado desejado

Expor a exclusão lógica de formação própria por DELETE autenticado, preservando as linhas de seleção curricular, tornando repetição segura e impedindo que uma edição concorrente ou posterior restaure um registro excluído.

### Atores e interesses

- Estudante: retirar formação do perfil ativo sem alterar silenciosamente as seleções de currículos montados.
- API: obter proprietário apenas da sessão e manter ausência/alheio indistinguíveis.
- Application/Domain: coordenar a transição de exclusão, idempotência e falha uniforme sem acoplar HTTP ou ORM.
- Adapter relacional: filtrar perfil ativo, aplicar UPDATEs condicionais e preservar primeiro instante de exclusão.
- Responsáveis de governança: definir futuramente retenção e purga conforme finalidade e obrigações aplicáveis.

### Evidências e fatos observados

- `ExcluirPerfil` usa `deleted_at`, consulta relógio e não altera o instante quando repetido.
- A formação não tem marcador de exclusão. O repositório atual busca por ID e dono sem filtro de status e atualiza buscando o registro, copiando campos e chamando `flush`; essa atualização pode conflitar com exclusão se não mudar para escrita condicional.
- `EditarFormacaoAcademica` localiza por `obter_por_id_e_usuario`, valida pelo domínio e chama `atualizar`. A interface atual de `atualizar` retorna `None`, portanto não sinaliza que o registro desapareceu entre leitura e escrita.
- `GerarPreviaVersaoCurriculo` percorre as referências do currículo e chama `ConsultaItemPerfil.obter_item`, descartando item ausente ou de outro proprietário. Não foi encontrada implementação concreta da porta no backend de produção. Não há leitura operacional existente para ajustar nesta entrega.
- `CurriculoItemRegistro` armazena `curriculo_id`, `tipo` e `item_id`; a FK cobre somente `curriculos.id`. Não há FK para a formação nem snapshot dos dados. A migration de `curriculo_itens` e o ORM confirmam isso.
- O DER anterior desenhava associação específica muitos-para-muitos `CURRICULO_FORMACAO`; não representa o schema implementado e deve ser corrigido no trabalho documental.
- RF02 prevê consultar, editar e excluir dados. O documento de segurança pede critérios de retenção/exclusão, mas deixa prazos para definição posterior. Não há base documental para inferir prazo ou obrigação de purga física neste escopo.
- Backend usa PostgreSQL/Psycopg e SQLite em testes. A alteração nullable de timestamp é aditiva e não interfere nos CHECKs existentes.

### Hipóteses

- UPDATE condicional com confirmação de rowcount é a garantia necessária para que a exclusão vença uma edição concorrente, desde que a transação trate zero linhas como conflito de não encontrado no núcleo.
- Na disputa entre duas exclusões, a escrita que primeiro preencher `deleted_at` mantém seu timestamp; a operação seguinte detecta que já está excluído e conclui com sucesso sem substituir o valor.
- As seleções preservadas podem apontar para uma formação excluída sem violar FK, pois não existe FK do item.

### Perguntas em aberto

Resolvidas pelas decisões desta revisão:

1. **Currículos existentes:** manter os registros de `curriculo_itens`; não criar leitura histórica agora. A prévia já tem caso de uso consumidor, mas falta implementação concreta de `ConsultaItemPerfil`. Quando a prévia ou exportação for implementada, seu adapter deve incluir formação excluída se e somente se a referência de seleção persistida a apontar e o proprietário corresponder. Não permitir que a formação excluída seja incluída em nova seleção, conforme a consulta de proprietário para seleção ativa. Nenhum ponto de produção precisa ser ajustado nesta entrega.
2. **Idempotência e porta:** adicionar `obter_por_id_e_usuario_incluindo_excluidas(formacao_id, usuario_id)`, usado exclusivamente pelo caso de uso de exclusão. A consulta sempre restringe simultaneamente ID e proprietário. Retorna a entidade própria ativa ou excluída; retorna `None` para ID ausente ou de terceiro. Assim a exclusão pode distinguir repetição legítima sem revelar registros alheios.
3. **Concorrência edição/exclusão:** `atualizar` deve tornar-se uma escrita condicional no adapter, com `UPDATE formacoes_academicas SET ... WHERE id = :id AND usuario_id = :usuario AND deleted_at IS NULL`; deve devolver resultado explícito (por exemplo, booleano ou contagem). Zero linhas significa não encontrada, e Application converte para `FormacaoAcademicaNaoEncontrada`, que o handler existente traduz em 404. Isso também cobre exclusão que ocorreu após a leitura da edição. O repositório atual, que faz SELECT, muta ORM e flush, precisa ser substituído por UPDATE condicional, sem permitir que campos imutáveis sejam escritos.
   
   A operação de exclusão também precisa ser condicional: preencher `deleted_at` apenas com `WHERE id, usuario_id, deleted_at IS NULL`. Se atualizar zero linhas, a Application deve repetir a consulta escopada incluindo excluídas: se ainda houver formação própria já excluída, retorna sucesso e preserva o timestamp; se não houver, mantém falha uniforme. O resultado dessa operação deve permitir distinguir transição nova de repetição concorrente sem expor estado alheio.
   
   Impacto nos testes existentes: doubles de `RepositorioFormacaoAcademica` e testes de `EditarFormacaoAcademica` devem cobrir `atualizar` retornando sucesso/falha; teste de zero linhas espera `FormacaoAcademicaNaoEncontrada`. Testes do adapter deixam de esperar `SELECT` seguido de mutação/`flush` e passam a verificar UPDATE com os três predicados, campos editáveis e rowcount. Testes de API de edição confirmam 404 para falha de atualização concorrente. Testes unitários de domínio/Application para a nova operação de exclusão são adicionados separadamente.
4. **HTTP:** DELETE `/formacoes-academicas/{formacao_id}`; 204 sem corpo; 404 público igual para ausente e alheio; 401 do middleware; 503 no padrão dos handlers. O proprietário é obtido exclusivamente da sessão. Repetição para item próprio retorna 204.
5. **Persistência:** migration nova, aditiva, com somente `deleted_at TIMESTAMP WITH TIME ZONE NULL`; sem índice novo e sem alteração de CHECKs da migration existente. Aplicar e reverter em PostgreSQL e SQLite.
6. **Retenção:** exclusão lógica atende esta entrega. Prazo e procedimento de purga ficam fora do escopo e pendentes de governança. Um direito de eliminação do titular pode exigir decisão futura de purga física; isso é risco a encaminhar, sem presumir obrigação ou prazo.

## Escopo

- Domain/Application: estado/ação de exclusão e caso de uso idempotente; novo método de leitura da porta que inclui excluídas; resultado explícito de atualização condicional e tradução de zero linhas para a falha já usada pela edição.
- API/adapters: DELETE autenticado pela sessão; busca escopada incluindo excluídas só no DELETE; busca normal ignora excluídas; persistência condicional para edição e exclusão.
- Migration aditiva de uma coluna timestamp com timezone anulável, sem índice ou CHECK novo/alterado.
- Testes unitários para domínio, caso de uso e adapter.
- Testes de integração para API, banco, migrations e comportamentos concorrentes.
- Atualizar DER e RF02; no DER substituir relação fictícia `CURRICULO_FORMACAO` pela representação real de `curriculo_itens`, explicando que referências permanecem após exclusão.
- Gate final das execuções de implementação: `nix develop .#quality --command ruff check src/backend`.

## Fora do escopo

Consulta geral de formação, front-end, purga nesta entrega, prazo de retenção, mudança das regras de cadastro/edição exceto não encontrar formação excluída, mecanismo novo para leitura histórica, remoção de seleções, snapshots de currículo e exclusão de outros itens.

## Critérios de sucesso

- DELETE da formação própria ativa marca `deleted_at` e retorna 204 sem corpo; proprietário deriva apenas da sessão.
- Repetir DELETE como dono retorna 204 e preserva exatamente o primeiro instante.
- Ausente e pertencente a outro usuário produzem o mesmo 404 e detalhe.
- Sem autenticação: 401 pelo middleware; executor indisponível: 503 no padrão existente.
- `obter_por_id_e_usuario` não retorna excluída; PUT posterior retorna o mesmo 404 de recurso não encontrado.
- A edição executa UPDATE condicional por ID, proprietário e `deleted_at IS NULL`; rowcount zero torna-se `FormacaoAcademicaNaoEncontrada`/404.
- Exclusão concorrente também atualiza somente com `deleted_at IS NULL`; primeira marca permanece e edição não ressuscita o registro.
- A porta adicional `obter_por_id_e_usuario_incluindo_excluidas` só consulta por ID e proprietário juntos e é consumida pelo fluxo de exclusão; ausência e item alheio são ambos `None`.
- Exclusão não altera nem apaga a linha de seleção existente em `curriculo_itens`.
- Nesta entrega nenhuma consulta de prévia/exportação é mudada. Uma implementação futura da leitura de currículo deve resolver a referência selecionada mesmo com `deleted_at` preenchido, mantendo a verificação de proprietário.
- Migration contém somente coluna nullable com timezone, sem índice e sem alterar CHECKs, e aplica/reverte em PostgreSQL e SQLite.
- DER reflete tabela polimórfica `curriculo_itens`, vínculo com currículo e ausência de FK/cópia para o item; RF02 explica exclusão lógica e manutenção das seleções.
- Política de retenção/purga permanece documentada como pendência de governança, sem prazo ou obrigação inventados.

## Restrições aplicáveis

- Decisões numeradas desta revisão são requisitos, não hipóteses.
- Contexto de cadastro/edição não deve ser reaberto; a única mudança de comportamento de edição é excluir registros marcados do acesso e devolver 404.
- Ausente e alheio continuam indistinguíveis em API e na consulta por proprietário.
- Nenhuma linha de `curriculo_itens` deve ser apagada ou alterada pela exclusão.
- Não inferir prazo ou obrigação legal de purga; encaminhar a questão à governança.

## Classificação comentada

A esfera primária é engenharia: contrato, núcleo e persistência backend. As preocupações são domínio, dados e privacidade devido ao estado de ciclo de vida, referências curriculares e retenção. A revisão fortalece a decisão e reduz a incerteza funcional; risco médio pela concorrência e retenção de dados pessoais, com mudança reversível por nova política de purge.

## Decisão de roteamento

A pasta anterior `prompts/backend` permanece a melhor candidata para a linhagem de operação e persistência do backend. As alternativas inventariadas incluem `prompts/requisitos` e `prompts/revisao`; a revisão não mudou o objeto central para documentação funcional nem para análise genérica.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | alta | Edição não pode restaurar exclusão; replays preservam o primeiro timestamp | Consistência concorrente |
| privacy | alta | Item sai do perfil ativo; dado retido somente conforme política ainda a definir | Evita exposição ativa |
| reliability | alta | Referências de currículos não são alteradas silenciosamente | Preserva seleções existentes |
| simplicity | média | Sem snapshot, FK ou mecanismo histórico novo nesta entrega | Mantém escopo limitado |
| compliance | limiar | Prazo fica pendente de governança; nenhum prazo presumido | Documentação deixa política em aberto |

## Alternativas consideradas

- **Lógica e seleção preservada (escolhida):** marcador anulável; esconde item de consultas/edição do perfil; mantém associação; leitura histórica futura atende ID selecionado.
- **Física e apagar seleção:** requer modificar dependências e destruir seleção; contradiz requisito explícito.
- **Física e bloquear referenciada:** não há FK para formar bloqueio relacional confiável; aumenta escopo e exige erro funcional sem decisão.
- **Lógica removendo seleção:** contradiz instrução de preservar cada linha de `curriculo_itens`.

As alternativas rejeitadas são inviáveis sob os requisitos desta revisão; não se atribui pontuação a opções que os violam.

## Perfil de pagamento comparativo

Escala ordinal: +2 melhora forte, +1 melhora moderada, 0 neutro/desconhecido, -1 piora moderada, -2 piora forte. Confiança alta para persistência/contratos inspecionados e média para o comportamento futuro da prévia.

| Dimensão | Prioridade | A: lógica e manter seleção | B: física e remover seleção | C: física e bloquear referenciada | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Correctness de edição | alta | +2 | 0 | 0 | alta | UPDATE condicional com deleted_at |
| Preservação de currículo | alta | +2 | -2 | +1 | alta | Associação permanece e não há snapshot |
| Privacy no perfil ativo | alta | +1 | +2 | +1 | alta | Todos tiram item do perfil, só purga apaga dado |
| Simplicidade da entrega | média | +1 | -1 | -2 | alta | Lógica aditiva sem reestruturar associação |
| Flexibilidade de retenção | limiar | +1 | -2 | -1 | média | Prazo ainda não definido e purge fora de escopo |

## Histórico e decisão atual

### Decisão da versão anterior

A v001 recomendou exclusão lógica, 204 idempotente e ocultação de ausente/alheio, mas deixou pendentes efeito em currículos e confirmação do limite de retenção. Também não especificou o nome da nova consulta da porta nem o retorno condicional da atualização.

### Decisão recomendada nesta versão

Aprovar como proposta a exclusão lógica com coluna nullable `deleted_at`; DELETE usa proprietário de sessão, 204 sem corpo e idempotência para item do dono; ausente/alheio permanecem 404 indistinguíveis. A porta recebe `obter_por_id_e_usuario_incluindo_excluidas`, usada exclusivamente pela exclusão, e a busca normal de edição filtra excluídas.

A atualização de edição deve ser uma escrita condicional e reportar zero linhas. A Application converte essa condição em `FormacaoAcademicaNaoEncontrada`, mantendo o 404 existente. A exclusão condicional preserva o primeiro timestamp, e disputa edição/exclusão favorece exclusão.

Seleções curriculares são preservadas sem novo caminho de leitura histórica agora. O caso de uso de prévia existente delega a consulta a `ConsultaItemPerfil`, mas a implementação concreta de leitura por ID não foi encontrada; fica registrado que futuros adapters de prévia/exportação devem incluir a formação excluída quando já selecionada e própria. A retenção e eventual purga são handoff de governança, fora desta entrega.

### Impacto da revisão

Fortalece a estratégia inicial e fecha as decisões de produto sobre currículo, repetição, HTTP, concorrência, migration e documentação. A incerteza que tornava a v001 pending foi resolvida; a v002 fica proposed. A política de retenção continua fora do escopo sem impedir implementação da exclusão lógica agora.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Correctness | prioritized | Concorrência não ressuscita item; retry não altera timestamp | UPDATE condicionado e rowcount |
| Reliability | prioritized | Currículos mantêm suas seleções atuais | Sem DELETE de associação |
| Privacy | prioritized | Exclusão retira formação do perfil/edição ativos | Filtro de deleted_at |
| Simplicity | satisficed | Nenhum mecanismo histórico/snapshot nesta entrega | Sem consulta produtiva concreta a alterar |
| Retention | unresolved | A coluna mantém dados até política posterior | Governança ainda deve definir prazo |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Privacidade de existência alheia | Mesmo 404 para ausente e alheio | Consultas sempre filtram pelo dono na mesma operação |
| Idempotência | Repetição do dono não falha nem muda instante | Consulta de exclusão inclui registros excluídos |
| Integridade de seleção | Linhas existentes permanecem | Nenhuma operação de DELETE em `curriculo_itens` |
| Portabilidade | Migration roda nos dois bancos | Coluna nullable timezone, sem expressão por dialeto |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Correctness | UPDATE sem predicado pode ressuscitar formação excluída | Alta | Estudante e integridade do perfil |
| Reliability | Remover associações pode mudar currículo já configurado | Alta | Estudante e destinatários |
| Privacy | Sem filtro de ativo, item excluído permanece editável/exposto no perfil | Alta | Estudante |
| Governança | Sem prazo definido, registros podem permanecer além do período pretendido | A definir | Titular e responsáveis pelo tratamento |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Preservar seleções | Dados marcados permanecem no banco e futura prévia terá de incluir referência histórica | Minimização e simplicidade futura | Aceito conforme requisito; prazo de retenção segue governança |
| Impedir ressurreição | UPDATE retorna resultado e casos de uso/test doubles precisam tratar falha de concorrência | Simplicidade da edição | Necessário para garantir a regra |
| Repetição segura | Porta oferece leitura específica que inclui tombstones | Pequena complexidade de API interna | Aceito e restrito ao caso de exclusão |

## Riscos e efeitos de segunda ordem

- As seleções mantidas apontam para UUIDs sem FK ao item; podem ficar órfãs se houver futura purga física. Essa futura política deve tratar associações.
- A prévia existente possui caso de uso, mas adapter concreto ausente. Quando esse caminho for implementado, filtrar sempre `deleted_at IS NULL` faria desaparecer a seleção; a consulta histórica por referência deve permitir item excluído apenas quando a seleção persistida o referencia e conferir o dono.
- Não implementar leitura histórica agora evita aumentar o escopo de exclusão; não há fluxo produtivo concreto identificado para ajustar.
- UPDATE SQL condicional deve ter testes que confirmem rowcount e não pode usar o padrão atual de carregar ORM, mutar e flush sem predicado atômico.
- A coluna anulável não altera os CHECKs, mas downgrade remove `deleted_at`; como isso descarta os instantes de exclusão, reversão deve ocorrer em migration isolada e explicitamente validada.
- O marcador lógico retém dados pessoais. A documentação não fornece prazo; existe risco de um exercício futuro do direito de eliminação requerer purga física.
- Last-write-wins continua aceitável entre edições concorrentes, mas entre edição e exclusão a regra específica é exclusão vence.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Primeira exclusão | Registro ativo recebe um único timestamp e 204 | Unitário de Application + API/persistência integrada | Item permanece ativo ou há corpo no 204 |
| Repetição pelo dono | Segunda chamada 204 e timestamp original inalterado | Integração serial e caso concorrente | Timestamp sobrescrito ou resposta diferente |
| Ausente e alheio uniformes | Status e detalhe idênticos 404 | API integrada com dois cenários | Diferença observável |
| PUT após exclusão | Consulta normal ignora registro; 404 | Integração API/persistência | PUT altera ou revela estado |
| Disputa exclusão/edição | UPDATE condicional retorna zero após exclusão; marcador permanece | Integração concorrente com transações | Registro ressuscitado ou update aceito após exclusão |
| Associação preservada | Linha em `curriculo_itens` continua igual após DELETE | Teste de integração no banco | Linha apagada/alterada |
| Migration PostgreSQL | Upgrade e downgrade da coluna | Teste de migration em PostgreSQL | Tipo, nullability ou reversão divergente |
| Migration SQLite | Upgrade e downgrade da coluna | Teste de migration em SQLite | Incompatibilidade do dialeto |
| Documentação consistente | DER representa `curriculo_itens`, RF02 declara exclusão e associação mantida | Revisão documental | Relação dedicada fictícia ou efeito omitido |
| Gate de lint | Lint de todo backend sem erros | `nix develop .#quality --command ruff check src/backend` ao final de cada execução de implementação | Falhas do Ruff |

O lint e os testes não foram executados nesta atividade de análise.

## Handoffs e atividades posteriores

| Atividade | Destino | Entrega |
|---|---|---|
| Domain/Application | `$backend-domain-orchestration-v2` | Transição idempotente e caso de uso de exclusão; adicionar à porta `obter_por_id_e_usuario_incluindo_excluidas(id, usuario)`, usado só pela exclusão; mudar `atualizar` para resultado explícito e tratar zero linhas como `FormacaoAcademicaNaoEncontrada`; edição de registro excluído retorna não encontrada |
| API/persistência | `$backend-adapters-drivers-v2` | DELETE com proprietário da sessão e mapeamentos 204/404/503; filtro de excluídos na consulta normal; implementação da consulta incluindo tombstones com ID e dono; UPDATE condicional para edição e marcação condicional para exclusão; migration aditiva da coluna `deleted_at TIMESTAMP WITH TIME ZONE NULL`, sem índice ou mudança nos CHECKs |
| Testes unitários | Skills de camada correspondentes | Atualizar doubles e testes de edição Application para resultado booleano/zero linhas; mudar testes do adapter de SELECT+mutação+flush para UPDATE+rowcount; cobrir porta e caso de uso |
| Integração e níveis superiores | `$integration-system-testing-v1` | DELETE/PUT com autenticação, propriedade/404, repetição, concorrência, preservação de `curriculo_itens`, migrations PostgreSQL/SQLite |
| Documentação | Fora das skills de implementação | Corrigir DER para schema polimórfico real e registrar `deleted_at); RF02 explica exclusão lógica e seleções mantidas |
| Governança | Fora desta entrega | Definir período de retenção e purga, considerando eventual direito de eliminação, sem presumir prazo ou conclusão jurídica |
| Execução de qualidade | Execuções posteriores | `nix develop .#quality --command ruff check src/backend` ao final |

A migration é responsabilidade de adapters/drivers por alterar schema e persistência concreta. Alterações no Domain/Application não incluem SQL nem ORM. Os testes de integração de migrations e concorrência são encaminhados à skill de testes superiores. A documentação é uma atividade independente e autorizada pelo requisito, mas não pertence às duas skills de implementação de backend.

## Síntese

A decisão de produto está fechada: exclusão lógica, currículos mantêm linhas de seleção, repetição própria é sucesso 204 e retenção/purga fica para governança. O repositório precisa de uma consulta escopada que inclua excluídas para o DELETE, e de atualizações condicionais com rowcount para impedir ressurreição em concorrência. A prévia tem um caso de uso que consome uma porta, mas não existe adapter produtivo dessa consulta identificado; nenhuma leitura histórica será criada agora. O artefato está proposto para implementação segundo os handoffs registrados.
