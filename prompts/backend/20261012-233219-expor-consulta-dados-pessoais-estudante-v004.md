---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v004"
status: proposed
created_at: "2026-10-12T23:32:19-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261012-230050-expor-consulta-dados-pessoais-estudante-v001.md
  supersedes: prompts/backend/20261012-232254-expor-consulta-dados-pessoais-estudante-v003.md
  change_type: enrichment
  secondary_change_types: []
  decision_impact: strengthened
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
    - path: "Complemento do usuário: campos da consulta e identidade via sessão de task94"
      relationship: primary
      representation: prose
      function: documentation
      format: text
      analysis_scope: whole-file
      locator: null
      content_state: external
      revision: null
      availability: available
    - path: prompts/backend/20261012-232254-expor-consulta-dados-pessoais-estudante-v003.md
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
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "GerenciadorSessoesSqlAlchemy.obter_usuario"
      content_state: commit
      revision: "0f896f4, branch origin/task94; fora da referência local origin/dev"
      availability: available
    - path: src/backend/api/cadastro_acesso.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "NOME_COOKIE_SESSAO, emissão do cookie no cadastro/login, GET /sessao"
      content_state: commit
      revision: "0f896f4, branch task94"
      availability: available
    - path: src/backend/api/runtime.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: Python
      analysis_scope: selected-section
      locator: "RuntimeBackend.obter_usuario"
      content_state: commit
      revision: "0f896f4, branch task94"
      availability: available
    - path: src/backend/api/experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "uso do cookie e runtime para derivar usuario_id no handler"
      content_state: commit
      revision: "0f896f4, branch task94"
      availability: available
    - path: src/backend/infrastructure/composicao.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "RuntimeBackendSqlAlchemy e provider transacional por requisição"
      content_state: commit
      revision: "0f896f4, branch task94"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "Endereco, Telefone e DadosContato; ausência de value object/campo Cidade"
      content_state: commit
      revision: "0f896f4, branch task94"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "0f896f4, branch task94"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "0f896f4, branch task94"
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
  concerns: [security, privacy, data]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: high
---

# Análise de decisão — consulta de dados pessoais do estudante

## Solicitação original

`$decision-analysis-v4 Faça uma analise para o card Expor consulta de dados pessoais do estudante. Inclua testes unitarios adequados`

## Informações complementares

Na solicitação inicial, nenhum critério ou identificador do card, lista fechada de campos ou dependência de sessão foi fornecido. O complemento desta versão fecha os campos e escolhe a origem da identidade, embora o código escolhido ainda precise ser integrado à branch de entrega.

Solicitação desta revisão, preservada literalmente: `$decision-analysis-v4 Revise prompts/backend/20261012-230050-expor-consulta-dados-pessoais-estudante-v001.md`

Informação posterior, preservada literalmente: `faça um pull da main para trazer as ultimas alterações para essa branch`

Solicitação desta nova revisão, preservada literalmente: `$decision-analysis-v4 Revise novamente prompts/backend/20261012-230050-expor-consulta-dados-pessoais-estudante-v001.md`

Complemento do usuário, preservado literalmente: `consultar nome, e-mail, telefone, cidade e contatos profissionais identifique o estudante com a sessão encontrada na task 94`

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Escopo funcional | Campos em aberto: perfil básico ou dados de contato | Definidos como nome, e-mail, telefone, cidade e contatos profissionais | Complemento explícito do usuário | Elimina a ambiguidade entre as alternativas de escopo |
| Identidade autenticada | Usar uma sessão integrada ainda era pré-condição sem fonte escolhida | Usar o principal resolvido pela sessão em `task94`; o cookie/runtime dessa branch são a referência técnica | Complemento explícito do usuário e inspeção do contrato em `0f896f4` | A escolha está definida; integração da dependência segue como atividade de implementação |
| Persistência dos campos | Dados de contato não mapeados no modelo SQLAlchemy da base analisada | Reconfirmado em `task94`: telefone/contatos existem no domínio, mas persistência de usuário continua sem esses campos; cidade e `deleted_at` não são mapeados separadamente | Inspeção dos modelos e repository no commit `0f896f4` | O DTO não pode prometer valores duráveis nem excluir logicamente perfis antes de completar mapeamento e migration |
| Decisão e testes | Direção condicional e status `pending` | GET de perfil próprio com os campos definidos e identidade via sessão; status passa a `proposed`. Testes unitários permanecem com doubles em Application, API e persistência | O usuário resolveu as decisões de produto/identidade; limitações restantes são trabalho técnico conhecido | Impacto `strengthened`; sem execução de testes, pois nenhum código foi alterado |
| Histórico de `main` | `origin/main` já era ancestral do HEAD `530e8f6` | Sem mudança desde v003; a referência continua não trazendo alterações ao código da análise | Contexto mantido da revisão anterior | Nenhuma mudança |
| Demais seções decisórias | Problema, restrições, alternativas, perfil de pagamento, perdas, riscos, validação e handoffs descritos na v003 | Reavaliados: alternativas passam a comparar GET unificado com consultas separadas; riscos e handoffs incorporam persistência e integração da sessão | O escopo informado é específico, mas a implementação possui lacunas de dados e composição | Recomendação agora definida, com pré-requisitos técnicos explícitos |
| Classificação e roteamento | `engineering`, preocupações `security`, `privacy`, `implementation`; incerteza alta; `prompts/backend` | `engineering`, preocupações `security`, `privacy`, `data`; incerteza média; pasta mantida | A definição de campos/sessão reduz incerteza de produto; persistência de cidade e contato vira foco técnico | Roteamento inalterado; classificação refinada |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| Solicitação do usuário: card Expor consulta de dados pessoais do estudante | Principal | Prosa | Documentação | Texto | Solicitação integral | Externa, recebida nesta conversa |
| Complemento do usuário: campos da consulta e sessão de `task94` | Principal | Prosa | Documentação | Texto | Mensagem integral | Externa, recebida nesta revisão |
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
| `src/backend/infrastructure/security/sessoes.py` | Apoio | Código-fonte | Produção | Python | Criação e resolução do token opaco, expiração e revogação | Commit `0f896f4` em `task94`, fora da referência local `origin/dev` |
| `src/backend/api/cadastro_acesso.py` | Apoio | Código-fonte | Produção | Python | Cookie de sessão, emissão em login e `GET /sessao` | Commit `0f896f4` em `task94` |
| `src/backend/api/runtime.py` | Apoio | Código-fonte | Contrato | Python | `RuntimeBackend.obter_usuario` | Commit `0f896f4` em `task94` |
| `src/backend/api/experiencia_profissional.py` | Apoio | Código-fonte | Produção | Python | Resolução do proprietário via cookie e runtime | Commit `0f896f4` em `task94` |
| `src/backend/infrastructure/composicao.py` | Apoio | Código-fonte | Produção | Python | Runtime SQLAlchemy e provider transacional por requisição | Commit `0f896f4` em `task94` |
| `src/backend/domain/value_objects.py` | Apoio | Código-fonte | Produção | Python | `Endereco`, `Telefone`, `DadosContato`; não há campo `Cidade` | Commit `0f896f4` em `task94` |
| `src/backend/infrastructure/persistence/sqlalchemy/usuario.py` | Apoio | Código-fonte | Produção | Python | Modelo ORM e mapper de usuário | Commit `0f896f4` em `task94` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py` | Apoio | Código-fonte | Produção | Python | Métodos de consulta/persistência de usuário | Commit `0f896f4` em `task94` |
| `prompts/backend/20261011-102943-rejeicao-requisicoes-sem-credenciais-validas-v004.md` | Contexto | Prosa | Documentação | Markdown | Inventário e lacuna de leitura/autenticação | Commit `530e8f6`; conclusões cotejadas com código atual |
| `AGENTS.md` e `src/backend/AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Arquivos completos | Commit `530e8f6` |
| `prompts/backend/20261012-232254-expor-consulta-dados-pessoais-estudante-v003.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree baseado em `530e8f6` |
| Histórico Git: `task88` / `origin/main` | Contexto | Dados estruturados | Metadados Git | Git | Ancestralidade entre `aff3b76` e `530e8f6` | Referências remotas consultadas nesta revisão |

### Limites da evidência dos artefatos

O código da branch de implementação está em `task88`, commit `530e8f6`; `origin/main` (`aff3b76`) é ancestral dele e não acrescentou código. A referência local `origin/dev` coincide com `task88`, mas não foi atualizada contra o servidor nesta revisão. O working tree contém as análises v001–v003 não rastreadas. A sessão escolhida pelo usuário foi examinada em `task94`, commit `0f896f4`, fora da referência local `origin/dev`. A análise usa o código da branch apenas como contrato de referência; não afirma que ele já esteja integrado à branch de entrega. O identificador e os critérios completos do card não foram fornecidos.

## Problema enriquecido

### Resultado desejado

Permitir que um estudante consulte, por API, seus próprios dados pessoais persistidos, com resposta limitada aos campos definidos para o card e sem expor credenciais ou dados de outra conta.

### Atores e interesses

- Estudante: recuperar os dados previamente cadastrados para conferência e continuidade do preenchimento.
- API: traduzir a requisição autenticada para uma consulta e devolver DTO explícito.
- Segurança: permitir leitura somente do proprietário autenticado e negar por padrão.
- Backend/persistência: consultar e reconstruir os dados duráveis sem vazar modelo ORM ou hash de senha.
- Produto/gestão: validar que os campos definidos pelo usuário correspondem ao critério de aceite do card e à jornada 6.3, sem reabrir a lista já informada.

### Evidências e fatos observados

- RF02 requer consulta, edição e exclusão de informações cadastradas; CT-RF02-01 espera exibir informações cadastradas, mas agrega dados pessoais, formação, experiência e competência.
- A jornada da seção 6.3 agrupa nome, e-mail, telefone, cidade e meios profissionais de contato sob “dados pessoais e contato”.
- RF13 exige autenticação para acesso a dados pessoais e currículos. O RNF04 e os requisitos de autorização restringem o acesso aos recursos próprios e proíbem confiar somente no identificador enviado pelo cliente.
- O usuário definiu o payload como nome, e-mail, telefone, cidade e contatos profissionais e determinou que a identidade seja obtida da sessão existente em `task94`.
- Em `task94`, o cookie `sistema_curriculo_sessao` (`HttpOnly`, `Secure`, `SameSite=Lax`) é resolvido por `RuntimeBackend.obter_usuario`; a sessão compara o hash do token e exige expiração futura. A rota de experiência profissional demonstra o padrão de obter `usuario_id` do runtime, sem receber o proprietário do cliente.
- A estrutura de contato em `task94` representa telefones como lista e contatos profissionais como LinkedIn e currículo Lattes. `Endereco` é texto livre e não há campo/value object `Cidade`; o DTO de consulta deve representar cidade explicitamente, sem tentar extraí-la de endereço livre.
- O modelo SQLAlchemy `UsuarioRegistro` em `task94` persiste apenas id, nome, e-mail e hash de senha; não tem colunas para contato/cidade nem para o `deleted_at` do agregado. O repository não implementa `obter_por_id`, e o mapper não persiste/restaura esses estados. Logo, telefone, contatos profissionais, cidade e exclusão lógica não têm leitura durável nesse adapter.
- Na base `task88`, `perfil_estudante.py` expõe PUT e DELETE, sem GET, e `dados_contato.py` expõe PUT, sem GET; a única rota GET observada nessa base é a listagem de versões de currículo. Em `task94`, há também `GET /sessao`, que valida a sessão corrente e retorna a identidade autenticada.
- Não existe caso de uso de consulta de perfil/dados pessoais na base atual; há casos de uso de edição, exclusão e atualização de contato.
- A porta `RepositorioUsuario` declara `obter_por_id`, mas o repository SQLAlchemy em `task88` e `task94` não implementa esse método. O modelo SQLAlchemy de usuário guarda id, nome, e-mail e hash; não mapeia os campos de contato presentes no agregado.
- O login da base `task88` valida credenciais sem estabelecer sessão. A implementação de sessão escolhida está em `task94`, mas não está integrada à referência local `origin/dev`.
- `origin/main` no commit `aff3b76` é ancestral de `task88` no commit `530e8f6`; a atualização solicitada não acrescenta commits à branch nem altera as evidências de código e requisitos desta análise.
- Os testes existentes cobrem edição e contato com doubles; não há teste unitário de consulta desses dados.

### Hipóteses

- A consulta é somente leitura e não deve alterar o agregado nem registrar uma nova versão dos dados.
- “Telefone” preserva a representação atual de `DadosContato.telefones` como lista; “contatos profissionais” cobre os campos disponíveis `linkedin` e `curriculo_lattes`.
- Cidade será armazenada como campo explícito. O endereço livre existente não será interpretado nem transformado em cidade.
- Formação, experiência, competências e currículos continuam em consultas próprias, fora desta fatia.
- O usuário comum consulta somente os dados da própria conta; o identificador será derivado do cookie de sessão via runtime de `task94`, sem ID de proprietário no path, query ou corpo.

### Perguntas em aberto

O escopo dos campos e a origem da identidade foram definidos pelo usuário. Continua como decisão de contrato HTTP definir a resposta para perfil inexistente/excluído; recomendação para implementação: `404` sem detalhes que revelem dados de outra conta. A sessão de `task94` e o armazenamento durável dos campos precisam ser integrados/implementados como dependências técnicas conhecidas, sem nova decisão de produto.

### Escopo

- Expor uma consulta somente leitura do perfil do estudante autenticado, recomendada como `GET /estudantes/me`.
- Devolver nome, e-mail, telefone(s), cidade e contatos profissionais (LinkedIn e currículo Lattes), com DTO explícito e sem hash, token ou modelo ORM.
- Derivar `UsuarioId` do cookie `sistema_curriculo_sessao` por `RuntimeBackend.obter_usuario` conforme o contrato de `task94`; não aceitar o proprietário do cliente.
- Completar o caso de uso e a leitura do repository por ID autenticado, persistência/mapeamento de telefone, cidade e contatos profissionais, e estado de exclusão lógica necessário para não servir perfil excluído.
- Especificar testes unitários para Application, handler HTTP, runtime/identidade quando aplicável e repository adapter, todos isolados com doubles.

### Fora do escopo

- Consultar ou consolidar currículos, formação acadêmica, experiências, competências ou projetos.
- Expor endereço completo ou outros atributos que não foram pedidos.
- Editar ou excluir dados pessoais.
- Criar mecanismo de sessão alternativo; a referência escolhida é a sessão de `task94` e sua integração é pré-requisito.
- Testes com servidor ASGI e banco reais, que pertencem à atividade de integração.
- Acrescentar campos ou regras de autorização além dos informados sem uma nova decisão de produto/segurança.

### Critérios de sucesso

- A resposta representa exatamente o conjunto de campos aceito para o card e não inclui hash de senha, segredo de sessão ou modelo ORM.
- A identidade da consulta vem do cookie validado pelo runtime de `task94`; um usuário não consegue selecionar outra conta pelo path, query ou corpo.
- Nome/e-mail, telefone(s), cidade, LinkedIn e currículo Lattes são lidos de armazenamento durável e mapeados de forma explícita; perfis logicamente excluídos não são servidos.
- Perfil inexistente/excluído segue o comportamento HTTP definido, recomendado como `404` sem expor dados de terceiros.
- A leitura é sem efeito colateral e consulta os valores persistidos atuais.
- Testes unitários cobrem sessão ausente/inválida, derivação da identidade somente pelo runtime, perfil encontrado/ausente, mapeamento exato do DTO, ausência de hash/token e leitura do repository com ORM substituído.
- Testes integrados validam sessão, HTTP e banco em atividade separada; não são substituídos por testes unitários.

## Restrições aplicáveis

- RF13 exige autenticação; RNF04 e requisitos de autorização limitam leitura aos dados autorizados e do próprio estudante.
- A identidade deve vir da sessão de `task94`, conforme instrução do usuário; não confiar em ID fornecido pelo cliente.
- Domínio/Application não dependem de FastAPI, SQLAlchemy ou transporte. Entidades não são respostas HTTP.
- Persistência relacional segue Code First/Alembic; dados que não estejam persistidos não podem ser apresentados como consulta durável.
- Usar DTO explícito para não devolver hash de senha, token, endereço completo ou propriedades internas.
- Novas funções, classes e DTOs devem documentar responsabilidade, abordagem e finalidade.
- Testes unitários backend usam `nix develop .#backend`; integração usa `nix develop .#tests`.

## Classificação comentada

`engineering` domina. `security`, `privacy` e `data` são as preocupações principais: a leitura deve ser limitada pela sessão, a resposta contém dados pessoais e cidade/contatos exigem persistência explícita. O usuário resolveu a lista de campos e a fonte de identidade; a incerteza passa de alta para média porque a sessão de referência ainda precisa ser integrada e os campos de contato/cidade ainda não são duráveis. O risco permanece alto devido ao impacto de acesso cruzado ou exposição de credenciais.

## Decisão de roteamento

Destino `prompts/backend`: a finalidade principal é especificar uma consulta por API e sua integração com sessão e persistência. `prompts/requisitos` foi considerada porque o pedido inicial não trazia critérios detalhados; a lista foi complementada pelo usuário. `prompts/revisao` permanece apenas como contexto de análise anterior, sem mudar o foco técnico desta decisão.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Security | Muito alta | Consultar apenas a conta vinculada ao principal autenticado | Evita IDOR e divulgação entre estudantes |
| Privacy | Muito alta | Resposta mínima e sem credenciais/atributos internos | Dados pessoais não devem vazar por serialização ampla |
| Correctness | Muito alta | Retornar exatamente nome, e-mail, telefone(s), cidade, LinkedIn e Lattes a partir do armazenamento | Evita payload incompleto ou conteúdo não persistido |
| Simplicity | Média | Um GET do próprio perfil, sem ID do usuário no pedido e sem agregar currículo | Mantém cliente e autorização simples |

## Alternativas consideradas

### A — GET unificado do próprio perfil, com todos os campos definidos

Criar `GET /estudantes/me`, resolver `UsuarioId` pelo cookie/runtime de `task94` e devolver nome, e-mail, telefones, cidade, LinkedIn e currículo Lattes. Completar o use case, o repository e o armazenamento Code First dos campos ausentes. É a recomendação: um contrato só atende ao escopo confirmado e à jornada, com trabalho de persistência conhecido.

### B — Duas consultas próprias, perfil e contato separados

Separar os dados básicos e contato em endpoints/DTOs diferentes, ambos derivados da mesma sessão. Continua atendendo o escopo e pode preservar limites do agregado, mas exige duas chamadas ou composição no cliente e não evita o trabalho de persistir telefone, cidade e links.

### C — GET com `usuario_id` do cliente, protegido pela sessão

Incluir ID na rota, mas conferir que corresponde ao `UsuarioId` da sessão. É implementável, porém redundante para consultar o próprio perfil e abre caminho a erros de autorização; não segue a instrução de derivar o estudante somente da sessão.

### D — Agregar todos os dados do estudante em uma única resposta

Incluir também formação, experiência, competências e currículos. O CT-RF02-01 é amplo, mas o usuário delimitou campos pessoais; esta opção excede o pedido e mistura recursos.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | A | B | C | D | Confiança | Base |
|---|---:|---:|---:|---:|---:|---|---|
| Security | Muito alta | +2 | +2 | -1 | +1 | Alta | A/B derivam propriedade pela sessão; C mantém ID redundante e exige checagem; D amplia recursos expostos |
| Privacy | Muito alta | +2 | +2 | 0 | -2 | Alta | A/B limitam resposta aos campos pedidos; D expõe outras áreas do currículo |
| User-value | Alta | +2 | +2 | +1 | +1 | Alta | A/B atendem a lista explícita do usuário; C pode atender com regra extra |
| Correctness | Muito alta | +2 | +2 | +1 | -1 | Média | A/B exigem completar armazenamento; C aumenta risco de seleção divergente; D mistura contratos |
| Simplicity | Média | +2 | 0 | -1 | -2 | Média | Um GET próprio evita duas chamadas, ID redundante ou agregação ampla |

Os valores são ordinais e não são somados. A e B são as alternativas viáveis que respeitam campos e sessão indicados. Ambas exigem completar a persistência: em A a resposta é um único contrato; em B o cliente compõe dois contratos. C e D são inferiores porque contrariam a identidade somente pela sessão ou ultrapassam o escopo.

## Histórico e decisão atual

### Decisão da versão anterior

A v003 manteve `pending` porque faltavam lista de campos e escolha da sessão. Também registrou que `origin/main` não trazia novos commits para a branch. A direção de consulta do próprio perfil permaneceu, mas os campos e a dependência de identidade ainda eram condicionais.

### Decisão recomendada nesta versão

Recomendo a alternativa A: `GET /estudantes/me`, obtendo `UsuarioId` de `RuntimeBackend.obter_usuario` pelo cookie `sistema_curriculo_sessao` da sessão em `task94`. O DTO deve conter nome, e-mail, telefones (lista), cidade explícita, LinkedIn e currículo Lattes; não recebe ID de usuário do cliente e não expõe hash/token/endereço completo. O caso de uso consulta o perfil próprio e o repository implementa `obter_por_id`. Para tornar a resposta durável e respeitar exclusão lógica, completar o modelo de domínio/ORM, o mapper e a migration para telefone, cidade, contatos profissionais e `deleted_at`.

O escopo e a fonte de identidade foram escolhidos pelo usuário; por isso a análise passa a `proposed`, não `pending`. A implementação continua condicionada a trazer/integrar a sessão de `task94` e adicionar o armazenamento durável dos campos. São pré-requisitos técnicos conhecidos, não questões abertas de produto. Recomendo `404` genérico quando o perfil próprio não existir ou estiver excluído.

### Impacto da revisão

`strengthened`: o usuário fechou as duas decisões que mantinham a v003 pendente. A sessão escolhida foi verificada no commit `0f896f4`, e seu uso como fonte da identidade ficou explícito. A recomendação agora fixa os campos, propõe `/estudantes/me` e sai de `pending` para `proposed`. A lacuna de persistência foi reavaliada e permanece como trabalho técnico obrigatório. A análise contextual sobre rejeição de credenciais continua fora desta linhagem.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Security | prioritized | Leitura sempre limitada ao principal autenticado | RF13, RNF04 e propriedade da conta descrita nos requisitos de segurança |
| Privacy | prioritized | DTO explícito e mínimo, sem hash/token | Tabela de usuário inclui hash e não deve ser serializada |
| Correctness | prioritized | Resposta completa baseada nos campos confirmados e persistidos | Usuário definiu os campos; `task94` ainda não os mapeia de forma durável |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Simplicity | Uma chamada para recuperar os campos pessoais aprovados | Um GET `/estudantes/me` entrega o conjunto em DTO explícito |
| Reversibility | Mudanças de armazenamento versionadas e revisáveis | Alterações no domínio/ORM devem usar migrations Code First; rota e DTO são contratos versionáveis |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Security | Usuário lê dados de outra conta ou acesso anônimo obtém perfil | Alta | Estudantes e operação |
| Privacy | Hash, sessão ou campos fora do propósito aparecem no payload | Alta | Estudantes |
| User-value | Consulta omite telefone, cidade ou contato profissional do escopo já definido | Alta | Estudantes e frontend |
| Correctness | API apresenta contato/cidade apenas em memória ou deriva cidade de endereço livre | Alta | Estudantes e produto |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Security | Integrar o runtime de sessão de `task94` e derivar proprietário do cookie | Delivery-speed | Necessário por RF13, RNF04 e instrução explícita do usuário |
| Privacy | Restringir DTO aos campos pedidos, sem endereço completo, hash ou token | Flexibilidade imediata do payload | Aceitável para minimizar exposição |
| Correctness | Adicionar campos de cidade/contato ao domínio, ORM, mapper e migration | Simplicity e velocidade | Necessário para atender a lista definida com valores duráveis |

## Riscos e efeitos de segunda ordem

- Um GET que aceite `usuario_id` sem verificação de propriedade cria risco de acesso horizontal entre contas.
- A sessão escolhida no commit `0f896f4` está em branch separada; ela deve ser integrada à base de entrega sem perder os atributos de segurança do cookie e o vínculo com o runtime transacional.
- O modelo ORM atual contém hash de senha; devolver o agregado inteiro em `response_model` ou serialização implícita pode expor credencial derivada.
- O agregado possui telefones e links de contato, mas o mapper/modelo SQLAlchemy não os persiste; cidade nem sequer existe como campo explícito. Uma leitura pode aparentar funcionar em memória e falhar após novo carregamento.
- CT-RF02-01 inclui também formação, experiência e competência; usar esse critério como exigência do card pode expandir a task indevidamente.
- O merge/adaptação de `task94` para `task88` pode revelar conflitos de composição; a análise não pressupõe que as branches possam ser mescladas sem resolução.
- A resposta após exclusão lógica é recomendada como `404` genérico; esse comportamento deve ser coberto no contrato e nos testes.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Campos da consulta refletem o escopo acordado | Nome, e-mail, telefone(s), cidade, LinkedIn e Lattes no DTO | Revisão de contrato e teste unitário de serialização | Campo omitido, extra ou endereço completo no payload |
| Principal autenticado vem da sessão escolhida | Integração do runtime de `task94` e teste do handler | Teste unitário com runtime stub para sessão válida, ausente e inválida | ID enviado pelo cliente altera o usuário consultado |
| Consulta lê somente o perfil próprio | Caso de uso recebe apenas `UsuarioId` do runtime e rejeita ausência/perfil excluído | Teste unitário da Application; integração posterior para sessão real | Usuário obtém dados de outro ID ou sessão expirada é aceita |
| Dados e estado de perfil são duráveis | Modelo/mapper/migration e query por ID cobrem campos e exclusão lógica | Testes unitários do repository/mapper; integração com banco depois | Valores só existem no agregado em memória ou perfil excluído continua consultável |
| Resposta não expõe credenciais | DTO não serializa hash/token/modelo ORM | Teste unitário do handler/DTO | Hash ou token presente na resposta |

## Handoffs e atividades posteriores

- `$backend-domain-orchestration-v2`: caso de uso de consulta somente leitura, usando `UsuarioId` da sessão e tratando perfil inexistente/excluído.
- `$backend-adapters-drivers-v2`: GET `/estudantes/me`, DTO explícito e integração com `RuntimeBackend.obter_usuario` da sessão de `task94`.
- Persistência: implementar `obter_por_id`, armazenar/restaurar telefones, cidade explícita, LinkedIn/Lattes e estado `deleted_at` no modelo Code First e criar migration.
- Testes unitários backend: cobrir Application, handler/DTO e repository/mapper com doubles, incluindo sessão ausente/inválida, perfil ausente, campos exatos e ausência de hash/token.
- `$integration-system-testing-v1`: teste HTTP com sessão real e banco descartável para propriedade, ausência de sessão e dados persistidos.
- Frontend: consumir o payload aprovado e tratar ausência de sessão/perfil conforme contrato, em atividade própria.

## Síntese

O usuário definiu que a consulta retorna nome, e-mail, telefone(s), cidade e contatos profissionais e que o estudante seja identificado pela sessão de `task94`. A recomendação é um `GET /estudantes/me` com identidade derivada de `RuntimeBackend.obter_usuario`, sem ID enviado pelo cliente e sem agregar outras seções do currículo. A análise passa de `pending` para `proposed` porque as escolhas de produto e identidade foram respondidas. Antes da entrega, é necessário integrar a sessão e completar caso de uso, repository e persistência Code First: o modelo atual não armazena contato e não possui cidade explícita. Os testes unitários devem cobrir Application, handler/DTO e repository/mapper com doubles; integração de sessão/HTTP/banco fica separada.
