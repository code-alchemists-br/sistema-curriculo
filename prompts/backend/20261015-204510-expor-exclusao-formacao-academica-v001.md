---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: pending
created_at: "2026-10-15T20:45:10-03:00"
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
    - path: prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "Implementado e explicitamente fora de revisão conforme a solicitação"
      content_state: working-tree
      revision: "v003"
      availability: available
    - path: prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "Contrato de edição existente e pendência sobre impacto em currículos"
      content_state: working-tree
      revision: "v001"
      availability: available
    - path: src/backend/domain/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "Estado excluído e operação idempotente de Usuario"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ExcluirPerfil e EditarFormacaoAcademica"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioFormacaoAcademica e consulta de item referenciado por currículo"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "coluna deleted_at de usuarios"
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
      locator: "CurriculoItemRegistro e conversão de referências"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: Markdown/Mermaid ER
      analysis_scope: selected-section
      locator: "FORMACAO_ACADEMICA, CURRICULO e CURRICULO_FORMACAO"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF02 e detalhamentos ainda necessários"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/requisitos-seguranca.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "4.10 Retenção e exclusão; 4.11 Direitos do usuário; definição de retenção pendente"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/fundamentos-backend.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "PostgreSQL/Psycopg como alvo do backend"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/formacao_academica.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "handlers de cadastro/edição e mapeamento 401/503"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "DELETE de perfil autenticado, resposta 204, erro 404/503"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/exclusao_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "DELETE de currículo, resposta 204, erro 404/503"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261014_0007_criar_formacoes_academicas.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python/Alembic
      analysis_scope: selected-section
      locator: "colunas e CHECKs da formação acadêmica"
      content_state: working-tree
      revision: null
      availability: available
---

# Análise de decisão — expor exclusão de formação acadêmica

## Solicitação original

`$decision-analysis-v4 Implementar "Expor exclusão de formação acadêmica". Task para o back-end. Identifique as necessidades e siga de acordo com as documentações, os requisitos e o que já está implementado.

## Contexto (já implementado, não reabrir)

Cadastro e edição de formação acadêmica estão implementados. Use como artefatos de apoio, sem revisá-los (esta é uma nova linhagem):
- prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md
- prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md

Isso inclui:
- Domain: `FormacaoAcademica` (com `editar`), enums de nível e status, constantes de tamanho.
- Application: `CadastrarFormacaoAcademica`, `EditarFormacaoAcademica`, `FormacaoAcademicaNaoEncontrada`; a porta `RepositorioFormacaoAcademica` com `salvar`, `obter_por_id_e_usuario` e `atualizar`.
- API: `POST /formacoes-academicas` e `PUT /formacoes-academicas/{formacao_id}`, proprietário só pela sessão, 404 idêntico para ausente e alheio.
- Persistência: modelo SQLAlchemy, repositório concreto, migration 20261014_0007 com CHECKs.

Nada disso deve mudar de comportamento, exceto onde a exclusão exigir (por exemplo, edição de uma formação já excluída).

## O que investigar

- **Estratégia de exclusão:** exclusão lógica (marcador como `deleted_at`) ou física. Já existe `ExcluirPerfil` com exclusão lógica e `deleted_at`; verifique se algum outro item (versão de currículo, competência, experiência) tem exclusão, qual o padrão, e o que os documentos dizem (DER, requisitos funcionais, RF02 e qualquer menção a retenção, LGPD ou purga). Recomende uma estratégia com justificativa.
- **Impacto em currículos:** versões de currículo referenciam formações? Existe chave estrangeira, tabela de associação ou cópia dos dados? O que acontece com um currículo já gerado quando a formação é excluída (bloqueia a exclusão, remove a referência, mantém uma cópia)? Esta pergunta ficou sem resposta na análise de edição e agora é central. Se depender de decisão de produto, separe com clareza e apresente as opções com recomendação.
- **Repetição (idempotência):** excluir uma formação já excluída deve retornar 404 ou sucesso? Compare com `ExcluirPerfil` (que trata repetição como sucesso sem novo efeito) e recomende, considerando que ausente e alheio devem continuar indistinguíveis.
- **Contrato HTTP:** método DELETE em `/formacoes-academicas/{formacao_id}`, código de sucesso (204 ou 200), 404 uniforme, 401, 503 e o padrão dos handlers existentes.
- **Efeito sobre o que já existe:** se a exclusão for lógica, formações excluídas não podem ser encontradas por `obter_por_id_e_usuario`, nem editadas por `PUT`. Avalie o impacto na porta, no repositório concreto, nos testes e em qualquer consulta futura. Se for física, avalie integridade referencial.
- **Persistência:** se a mudança exige migration (coluna de exclusão lógica, índice, ajuste de constraints) e qual o impacto sobre os CHECKs e a migration 20261014_0007. Confirme o banco-alvo (PostgreSQL via psycopg, com SQLite nos testes) e a compatibilidade da migration com os dois.
- **Concorrência:** avalie edição e exclusão simultâneas sobre o mesmo registro (last-write-wins é aceitável?).
- **Documentação:** necessidade de atualizar docs/modelagem_der.md e docs/requisitos_funcionais.md (RF02).

## Escopo

Somente a exclusão de formação acadêmica pelo próprio estudante autenticado. Fora do escopo: consulta de formação, front-end, purga física posterior de registros excluídos logicamente (a menos que a análise a identifique como obrigatória por requisito), e qualquer mudança nas regras de cadastro e edição além do necessário.

## Instruções

- Recomende as decisões técnicas e separe o que depende de decisão de produto, para eu decidir antes da implementação.
- Indique a divisão entre Domain/Application (`$backend-domain-orchestration-v2`) e API/persistência (`$backend-adapters-drivers-v2`), e o que fica fora das duas skills (documentação, testes de integração com `$integration-system-testing-v1`). Se a migration for necessária, indique em qual das duas ela entra.
- Registre na validação o comando do gate de lint do CI, `ruff check src/backend`, executado com `nix develop .#quality --command`, para que as execuções o rodem ao final.
- Não implemente nada.`

## Informações complementares

Nenhum — não houve informação adicional posterior à solicitação original.

## Mudanças desde a versão anterior

Nenhuma — análise inicial de uma nova linhagem. As duas análises indicadas pelo usuário foram tratadas somente como contexto de apoio, sem revisão ou alteração.

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md` | Apoio | Prosa | Documentação | Markdown | Contexto implementado de cadastro e invariantes, sem reavaliar decisões | Working tree, v003, disponível |
| `prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md` | Apoio | Prosa | Documentação | Markdown | Contexto implementado de edição e pendência de currículos | Working tree, v001, disponível |
| `src/backend/domain/usuario.py` | Apoio | Código-fonte | Produção | Python | Estado excluído e operação idempotente | Working tree, sem revisão fixada |
| `src/backend/application/perfil_estudante.py` | Apoio | Código-fonte | Produção | Python | `ExcluirPerfil` e `EditarFormacaoAcademica` | Working tree |
| `src/backend/application/ports.py` | Apoio | Código-fonte | Produção | Python | Porta da formação e consulta de item de currículo | Working tree |
| `src/backend/infrastructure/persistence/sqlalchemy/usuario.py` | Apoio | Código-fonte | Produção | Python | Persistência de `deleted_at` do usuário | Working tree |
| `src/backend/infrastructure/persistence/sqlalchemy/formacao_academica.py` e `repositorio_formacao_academica.py` | Principal | Código-fonte | Produção | Python | Modelo e repositório completos | Working tree |
| `src/backend/infrastructure/persistence/sqlalchemy/curriculo.py` | Apoio | Código-fonte | Produção | Python | Representação de associação e ausência de snapshot/FK do item | Working tree |
| `src/backend/api/formacao_academica.py` | Apoio | Código-fonte | Produção | Python | Contratos de autenticação e erros para cadastro/edição | Working tree |
| `src/backend/api/perfil_estudante.py`, `src/backend/api/exclusao_versao_curriculo.py` | Apoio | Código-fonte | Produção | Python | Padrões de DELETE, 204, 404 e 503 | Working tree |
| `src/backend/infrastructure/persistence/alembic/versions/20261014_0007_criar_formacoes_academicas.py` | Apoio | Código-fonte | Produção | Python/Alembic | Colunas e CHECKs | Working tree |
| `docs/modelagem_der.md` | Apoio | Modelo/diagrama | Contrato de schema | Markdown/Mermaid ER | Relação formação-currículo e colunas | Working tree |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF02 e detalhamentos pendentes | Working tree |
| `docs/requisitos-seguranca.md` | Contexto | Prosa | Documentação | Markdown | Retenção, exclusão e direitos do usuário | Working tree |
| `docs/fundamentos-backend.md` | Contexto | Prosa | Documentação | Markdown | Banco-alvo e driver | Working tree |
| `src/backend/api/exclusao_versao_curriculo.py` | Contexto | Código-fonte | Produção | Python | Contrato DELETE, 204 e indisponibilidade | Working tree |

### Limites da evidência dos artefatos

As análises de cadastro e edição foram consultadas somente como apoio contextual, conforme solicitado; não se reabrem suas decisões. A análise da edição registra que o impacto em currículos estava em aberto. A inspeção do repositório descreve o estado visível no working tree, sem hash de commit registrado para estes arquivos. O DER é um modelo consolidado, não prova de que todas as relações já estejam implementadas em banco. A consulta concreta usada na prévia do currículo não foi localizada na infraestrutura SQLAlchemy inspecionada; assim, não se afirma que currículos atuais tenham snapshot ou que a prévia inclua dados excluídos. A decisão sobre conteúdo de currículos precisa ser especificada antes de implementar o comportamento ponta a ponta.

## Problema enriquecido

### Resultado desejado

Permitir que o estudante autenticado retire uma formação acadêmica do seu perfil através de `DELETE /formacoes-academicas/{formacao_id}`, com propriedade garantida pela sessão, tratamento seguro de ausência/alheio, sem corrupção dos dados necessários a currículos existentes.

### Atores e interesses

- Estudante: remover formação incorreta ou que não deseja mais manter no perfil.
- Consumidores de currículo: manter coerência entre seleções já feitas e conteúdo exibido/exportado.
- API: autenticar a requisição, obter proprietário exclusivamente da sessão e evitar revelar IDs de outros estudantes.
- Domain/Application: representar uma exclusão inequívoca e orquestrar idempotência sem depender de HTTP ou ORM.
- Persistência: manter integridade referencial e tratar concorrência com edição.
- Responsáveis pelo produto e governança: definir efeitos em currículos gerados e a semântica de retenção sem inferir política jurídica que ainda não está documentada.

### Evidências e fatos observados

- `ExcluirPerfil` executa exclusão lógica: busca agregado, consulta relógio, marca o primeiro `deleted_at`, atualiza e devolve estado; repetição retorna sucesso sem mudar o instante original.
- O perfil usa `deleted_at`. A entidade usuário documenta que isso bloqueia o uso do perfil sem executar purga física.
- Versões de currículo são excluídas fisicamente por seu handler e recebem `204`; o adapter apaga as linhas de associação antes da versão por integridade referencial.
- Competência e experiência não têm exclusão visível no recorte examinado; o código inspecionado não oferece mecanismo compartilhado de exclusão lógica para todos os itens.
- O modelo ORM da formação tem FK para `usuarios` e CHECKs de texto, vocabulário e coerência temporal. A migration correspondente representa o mesmo conjunto de CHECKs. Os CHECKs validam campos da formação; uma nova coluna anulável `deleted_at` não exige mudar seu predicado.
- O modelo de currículo persiste seleções em `curriculo_itens`: tipo e UUID, sem FK para `formacoes_academicas` e sem cópia dos dados da formação. A tabela de associação não assegura que o item permaneça disponível nem contém os campos necessários para reconstruí-lo.
- O DER desenha `CURRICULO_FORMACAO` e relação muitos-para-muitos; o schema em uso para seleção é uma tabela polimórfica `curriculo_itens`. Esta diferença é relevante à documentação, mas não implica mudar a arquitetura dentro desta tarefa.
- RF02 autoriza genericamente consulta, edição e exclusão de informações. Requisitos de segurança pedem critérios para retenção e exclusão e consideração da LGPD, mas deixam períodos de retenção e descarte a definir; não estabelecem purga física imediata ou retenção específica para formação.
- O backend aponta PostgreSQL com Psycopg; SQLite é usado em testes. Uma coluna nullable `deleted_at` e filtros por nulidade são portáveis entre ambos. Não é necessária expressão de CHECK dependente de dialeto.
- Os handlers existentes de exclusão usam 204 sem corpo, 404 para ausência/propriedade alheia e 503 quando o executor não está disponível. A rota de perfil usa o principal autenticado, sem ID de estudante fornecido pelo cliente.
- A formação hoje não contém `deleted_at`; a consulta e a atualização existentes por ID e proprietário não filtram exclusão.

### Hipóteses

- A exclusão não deve reescrever nem apagar seleções de currículo em cascata. A seleção armazena referência, sem snapshot; remover a associação poderia alterar currículos inesperadamente.
- A recomendação técnica de exclusão lógica não define automaticamente a política funcional de visualização/exportação de currículos que referenciam uma formação excluída.
- Uma formação marcada excluída continua retida para integridade histórica e possível renderização de versões antigas, mas deixa de ser editável e selecionável em novos usos do perfil.
- Não haverá purga automática nesta entrega. Uma eventual purga deverá respeitar política de retenção institucional e dependências de currículos, ainda não definidas.
- Last-write-wins para edições concorrentes só é aceitável se uma exclusão não puder ser revertida por uma edição concorrente; portanto, a marcação de exclusão deve prevalecer e atualização de item ativo deve ter condição atômica de não excluído.

### Perguntas em aberto

1. **Comportamento de currículos existentes — decisão de produto necessária.** Quando uma formação selecionada for excluída, deve um currículo previamente configurado continuar a exibi-la? Opções:
   - A. Preservar o conteúdo já selecionado/exibido, mantendo o registro lógico e permitindo leitura histórica das versões que já o referenciam (recomendado para evitar mudança inesperada em currículo existente; exige distinguir leitura de perfil ativo de leitura histórica).
   - B. Remover a formação também de todas as seleções existentes, fazendo os currículos refletirem imediatamente o perfil ativo (mais simples para privacidade funcional, mas altera conteúdo previamente montado e selecionado).
   - C. Copiar dados da formação para cada versão ao selecionar/gerar (snapshot estável, mas amplia escopo e modelo de dados; não há cópia atualmente).
   A decisão recomendada é A para esta entrega, por preservar referências e evitar cascade; contudo, precisa confirmar qual experiência de produto é desejada. Sem essa confirmação, os critérios de renderização não são fechados.
2. **Retenção/LGPD:** a documentação exige critérios de retenção, mas não define prazo ou purga. A demanda explicitamente exclui purga posterior. Confirma-se que a exclusão lógica é suficiente para retirar do perfil nesta entrega, ficando prazo de retenção para governança/produto? A recomendação é sim; não cabe inferir obrigação legal de apagar imediatamente nem prazo jurídico.
3. **Sucesso repetido:** a recomendação técnica é 204 idempotente para dono que já tem o item marcado, alinhada a `ExcluirPerfil`; uma formação ausente ou pertencente a terceiro continua 404 indistinguível. Produto pode preferir 404 para todo estado inativo, mas isso diverge do padrão estabelecido e perde idempotência observável.
4. **Concorrência:** assumir que exclusão vence edição concorrente e que nova tentativa de editar registro já excluído responde 404. A recomendação evita ressurreição. Confirmar se não há requisito de edição concorrente que demande conflito 409/controle de versão.

### Escopo

- Domain/Application: operação de exclusão da formação, resultado/falha, entrada e porta interna, usando abstrações para instante se for necessário.
- API/persistência: `DELETE /formacoes-academicas/{formacao_id}`, proprietário derivado da sessão, 204, 404 uniforme, 401 do mecanismo de autenticação e 503 indisponibilidade conforme os handlers existentes.
- Persistência lógica com coluna `deleted_at`, filtros para impedir edição de excluída e comportamento de leitura histórica escolhido para referências de currículo.
- Testes unitários do domínio/caso de uso e dos adapters elegíveis.
- Testes de integração API/persistência, incluindo repetição, isolamento de proprietário, concorrência relevante e migration, em atividade própria.
- Atualização de `docs/modelagem_der.md` e `docs/requisitos_funcionais.md` para indicar exclusão lógica e efeito escolhido sobre currículo.
- Gate de lint do CI registrado na validação para as execuções de implementação.

### Fora do escopo

- Consulta pública de formação, front-end, alterações às regras de cadastro/edição além de impedir PUT após exclusão, purga física automática ou manual, política geral de retenção, snapshots de currículo, exclusão de outros itens, implementação ou opinião jurídica sobre LGPD.
- Não se deve remover seleções de currículo por cascata sem decisão explícita de produto.

### Critérios de sucesso

- Somente estudante autenticado exclui formação pertencente à própria sessão; ID do proprietário não vem de corpo ou path.
- A ausência e a propriedade alheia produzem a mesma resposta 404, status e detalhe público.
- DELETE tem sucesso 204 sem corpo; chamada sem autenticação recebe 401 pelo middleware; executor/serviço indisponível recebe 503 conforme padrão atual.
- Repetir DELETE de formação própria já excluída devolve 204 e preserva o primeiro instante de exclusão. Ausente/alheia continuam 404.
- Formação excluída não pode ser obtida por `obter_por_id_e_usuario` para edição e PUT não pode alterá-la; remoção lógica não altera `id`, proprietário nem dados de cadastro.
- A semântica dos currículos existentes segue a decisão de produto registrada acima, sem exclusão silenciosa da referência ou desaparecimento não documentado.
- Edição e exclusão simultâneas não ressuscitam formação excluída; conflito com edição posterior à exclusão é percebido como ausência.
- Migration adiciona somente os campos/índices aprovados, conserva constraints existentes e funciona em PostgreSQL e SQLite.
- DER e RF02 descrevem corretamente a estratégia e efeito selecionado.
- Testes unitários cobrem transição/idempotência, não encontrado, proprietário, filtro de excluídos, atualização concorrente e mapeamentos elegíveis; testes superiores cobrem rota, sessão, banco, migration e efeito sobre currículo.
- Ao final das execuções de implementação, rodar o gate: `nix develop .#quality --command ruff check src/backend`.

## Restrições aplicáveis

- O contexto implementado listado na solicitação não deve ser reaberto; alterar apenas o necessário para excluir e bloquear edição posterior.
- Identidade do estudante vem exclusivamente da sessão autenticada.
- Ausente e alheio permanecem indistinguíveis.
- Não inventar obrigação ou prazo de purga a partir de menções gerais à LGPD; requisitos de segurança deixam o período de retenção a definir.
- A análise não autoriza implementação nem mudança nos artefatos de apoio.

## Classificação comentada

- `sphere: engineering`: a análise define contrato e persistência de uma operação backend.
- `concerns: [domain, data, privacy]`: ciclo de vida do item, associações referenciais e retenção de dados são os eixos que diferenciam as alternativas.
- `decision_kind: design`, escopo de componente e fase de entrega.
- Incerteza alta e risco médio: mudança é localizada, mas alterar dados já referenciados por currículos pode mudar conteúdo percebido e retenção de dados pessoais.

## Decisão de roteamento

`prompts/backend` foi escolhida entre `prompts/backend`, `prompts/ambientes`, `prompts/frontend`, `prompts/templates`, `prompts/revisao` e `prompts/requisitos`. A linhagem é nova, e o objeto principal é o contrato e armazenamento de uma operação de backend; a pasta backend contém os artefatos de apoio e é semanticamente mais específica. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | alta | Ausente/alheio ocultos; exclusão não pode ser revertida por edição concorrente | Protege isolamento e ciclo de vida |
| privacy | alta | Remover do perfil ativo; retenção/purga não presumida | Evita exposição contínua e afirmações jurídicas não sustentadas |
| reliability | alta | Currículos não devem mudar por cascata silenciosa | Preserva dados já referenciados |
| modifiability | média | Reusar padrão de `ExcluirPerfil` sem generalizar todos itens | Evita framework prematuro |
| compliance | limiar | Documentar retenção como decisão ainda aberta e não inventar prazo | Requisitos de segurança deixam prazo a definir |
| user-value | alta | Resposta idempotente e comportamento previsível em currículo já existente | Evita erro enganoso e alterações inesperadas |

## Alternativas consideradas

### Alternativa A — Exclusão lógica com leitura histórica (recomendada, sujeita à decisão de produto)

Adicionar `deleted_at`; excluir das consultas de perfil ativo e da edição; permitir, por mecanismo específico, que currículos que já possuem a referência continuem lendo o dado excluído. DELETE repetido pelo dono retorna 204. Não purgar nem remover associações nesta entrega.

### Alternativa B — Exclusão lógica e remoção das referências de currículo

Adicionar `deleted_at`, marcar e apagar as linhas de seleção relacionadas. Respeita a retirada do perfil ativo e minimiza a possibilidade de o dado aparecer em futuras prévias/exportações; porém muda os currículos existentes e cria efeito em cascata funcional que não está em RF02 nem no contrato atual.

### Alternativa C — Exclusão física bloqueada por referência

Apagar formação somente quando nenhum currículo a referencia; caso contrário devolver conflito. Preserva integridade referencial se adicionada FK real, mas a tabela atual é polimórfica e sem FK; não existe mecanismo de bloqueio relacional. Exigiria mudança estrutural e uma decisão de produto sobre erro/recusa.

### Alternativa D — Exclusão física com limpeza das referências

Excluir formação e apagar associações correspondentes. Simples no sentido de não reter o item, mas destrói a informação usada em currículos sem confirmação, sem FK dedicada para garantir atomicidade e sem política de retenção; não recomendada.

## Perfil de pagamento comparativo

Escala ordinal: +2 melhora forte, +1 moderada, 0 neutro/desconhecido, -1 piora moderada, -2 forte. Confiança nas avaliações: média, pois o comportamento concreto de leitura para prévia não foi encontrado nesta inspeção.

| Dimensão | Prioridade | A: lógica + histórico | B: lógica + remover referência | C: física + bloquear | D: física + limpar | Confiança | Base |
|---|---:|---:|---:|---:|---:|---|---|
| Correctness de currículos | alta | +2 | -1 | +1 | -2 | média | Associação guarda ID, sem snapshot nem FK |
| Privacy no uso futuro | alta | +1 | +2 | +1 | +2 | média | A remove perfil ativo, mas preserva leitura histórica já escolhida |
| Modifiability | média | 0 | 0 | -1 | -1 | média | C/D pedem controle de relações polimórficas |
| Simplicity | média | +1 | 0 | -1 | 0 | média | A acrescenta marcador e caminho de leitura histórica |
| Retention flexibility | limiar | +2 | +1 | -1 | -2 | média | Exclusão lógica permite política posterior; sem prazo ainda definido |
| User-value | alta | +2 | -1 | -1 | -2 | média | A mantém versões construídas; B/D as alteram |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma; análise inicial desta linhagem.

### Decisão recomendada nesta versão

Recomendar exclusão lógica com `deleted_at`, preservação das associações atuais e do dado histórico para evitar alteração retroativa de currículos. Esta recomendação não fecha a experiência de currículo: é necessário confirmar se versões já montadas devem continuar exibindo a formação, ser atualizadas para removê-la ou passar a usar snapshots. Por essa dependência material de produto, o artefato fica `status: pending`; não implementar até registrar a escolha.

No contrato técnico, recomenda-se DELETE 204 idempotente para repetição da exclusão do proprietário; 404 único para ausente/alheio; 401 pelo middleware; 503 quando o executor não estiver disponível. A operação é escopada pela identidade da sessão. A data de exclusão deve ser definida uma vez e preservada em chamadas repetidas.

### Impacto da revisão

Não aplicável: primeira versão.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Privacy | prioritized | Formação deixa de compor o perfil ativo | Recomendação de exclusão lógica |
| Correctness | prioritized | Referências de currículos antigos não são apagadas implicitamente | Associação guarda apenas referência |
| User-value | prioritized | Repetição segura e resposta sem corpo previsível | Padrão de ExcluirPerfil e DELETE existentes |
| Retention flexibility | satisficed | Dados retidos para política futura sem inventar prazo | Segurança exige política, mas período está pendente |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Ausência indistinguível | Mesmo 404 para alheio e inexistente | Consulta restringe simultaneamente por id e proprietário |
| Retenção | Sem purga no escopo; prazo não inferido | Marcador retém dados e documenta pendência de política |
| Compatibilidade SQL | Mesma alteração viável em PostgreSQL/SQLite | Coluna anulável e filtro de nulidade, sem expressão específica de dialeto |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Correctness | Exclusão física ou remoção de associação pode mudar versões de currículo já configuradas sem ação do usuário | Alta | Estudante e destinatários de versões previamente montadas |
| Privacy | Manter formação exposta no perfil depois de excluir | Alta | Estudante |
| Reliability | Edição concorrente pode remover `deleted_at` ou atualizar um item já excluído | Alta | Estudante e dados persistidos |
| Compliance | Purga ou retenção sem prazo aprovado pode divergir da política institucional | Média/alta | Estudante e responsáveis pelo tratamento |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Preservar currículo histórico | Mais um caminho de leitura que pode incluir registro excluído apenas para referência já existente | Simplicidade | Aceitável se produto confirmar A |
| Evitar exposição ativa | Registro fica no banco após DELETE e necessita futura política de retenção/purga | Minimização imediata de dados | Aceitável somente no escopo autorizado e com política posterior |
| Evitar ressurreição | Atualização deve ser condicional a `deleted_at IS NULL` e tratar atualização concorrente sem sucesso como não encontrado | Simplicidade do adapter | Necessário para consistência |

## Riscos e efeitos de segunda ordem

- Marcar excluída e filtrar todos os caminhos de leitura pode fazer a formação desaparecer de uma prévia já selecionada, embora a associação persista. Deve haver decisão de leitura histórica antes de adotar filtros globais.
- A tabela `curriculo_itens` não usa FK para o item; exclusão física não é bloqueada pelo banco e pode deixar referência órfã.
- Soft delete preserva dado pessoal por mais tempo. O requisito de segurança prevê critérios de retenção/exclusão, mas a duração está pendente; esta operação não resolve a política geral.
- Uma coluna nullable não afeta os CHECKs atuais de texto, enum e período. A migration de alteração precisa ser aditiva e testada contra PostgreSQL e SQLite.
- Índice adicional não é necessário para localizar um registro por sua chave primária. Índice em `(usuario_id, deleted_at)` só se justifica quando houver listagem ativa em volume; consulta de formação está fora do escopo. Evitar antecipar esse índice.
- Last-write-wins para duas edições é aceitável como padrão atual; em disputa edição/exclusão, prevalece exclusão e update condicional evita ressuscitar.
- A API de formação já tem mapeamento de indisponibilidade 503 para cadastro/edição; DELETE deve preservar mensagem genérica e não vazar exceções de banco.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Formação excluída deixa perfil ativo e PUT de fora | Provas de consulta ativa e teste de edição após exclusão | Unitários de Domain/Application/adapter + integração API e persistência | Algum fluxo ativo continua retornando ou atualizando excluída |
| Repetição é idempotente | Mesmo registro conserva primeiro `deleted_at`; DELETE repetido retorna 204 | Teste unitário do caso de uso e teste de integração da rota | Atualiza timestamp ou retorna resultado incoerente |
| Currículos antigos mantêm semântica aprovada | Leitura da formação por referência já persistida e teste de prévia/exportação | Teste de integração de currículo conforme decisão de produto | Item some, muda ou aparece em nova versão contra decisão |
| Migration portável | Adicionar `deleted_at` e aplicar/rollback em PostgreSQL e SQLite | Testes de migration no ambiente `tests` | Divergência de tipo, timezone ou alteração de CHECK |
| Concorrência não ressuscita | Interleavings de UPDATE e DELETE com filtro ativo | Teste de integração concorrente/serialização | UPDATE regrava formação depois da exclusão |
| Gate obrigatório do CI | Lint passa no backend completo | `nix develop .#quality --command ruff check src/backend` ao final de cada execução de implementação | Erros Ruff introduzidos ou preexistentes exigindo triagem |

A solicitação requer explicitamente que o gate de lint seja registrado para as execuções posteriores. Esta análise não executa lint nem qualquer teste.

## Handoffs e atividades posteriores

| Atividade | Destino | Conteúdo |
|---|---|---|
| Regras de domínio e orquestração | `$backend-domain-orchestration-v2` | Novo estado/operação de exclusão da formação, fluxo idempotente, not found uniforme, entrada/saída e porta necessária; editar deve tratar excluída como não encontrada |
| API e persistência | `$backend-adapters-drivers-v2` | DELETE autenticado pela sessão, mapeamentos 204/404/503, coluna e repositório; migration de schema pertence a esta skill |
| Testes integrados e de nível superior | `$integration-system-testing-v1` | API com autenticação, integração de persistência/migration em PostgreSQL e SQLite, concorrência e semântica curricular decidida |
| Documentação | Fora das skills de implementação acima | Atualizar DER e RF02 com marcador lógico e efeito em referências/currículos escolhido |
| Produto | Decisão necessária antes de aprovar implementação | Escolher comportamento de currículos existentes e confirmar ausência de purge no escopo |
| Gate de qualidade | Execuções posteriores | `nix develop .#quality --command ruff check src/backend` ao final |

A migration adicionando `deleted_at` é responsabilidade de adapters/drivers porque altera schema e implementação concreta de persistência. Se a decisão de produto exigir snapshot ou alteração de relações curriculares, isso requer análise e decomposição adicional, não deve ser absorvido automaticamente neste handoff.

## Síntese

A estratégia tecnicamente recomendada é exclusão lógica, coerente com `ExcluirPerfil`, que conserva dado e referências sem exigir purga não definida. O DELETE deve ser idempotente para o proprietário (204), ocultar ausência e propriedade alheia com o mesmo 404, exigir sessão (401 sem ela) e usar 503 quando indisponível. A formação excluída sai do caminho de edição, e a exclusão deve prevalecer sobre edição concorrente. Como o currículo contém referências por UUID, sem FK para formação e sem cópia do conteúdo, o comportamento de currículos existentes é decisão de produto ainda pendente. Não implementar até confirmá-la.
