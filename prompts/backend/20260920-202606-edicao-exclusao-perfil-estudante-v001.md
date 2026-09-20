---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-09-20T20:26:06-03:00"
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
    - path: https://github.com/code-alchemists-br/sistema-curriculo/issues/39
      relationship: primary
      representation: prose
      function: documentation
      format: github-issue
      analysis_scope: whole-file
      locator: "issue #39"
      content_state: external
      revision: "state CLOSED at consultation"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "359244f7b7532a528908e63cf80b1752b26ebbaa"
      availability: available
    - path: docs/modelagem_der.md
      relationship: primary
      representation: diagram-model
      function: schema-contract
      format: markdown-with-mermaid
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "359244f7b7532a528908e63cf80b1752b26ebbaa"
      availability: available
    - path: src/backend/domain/entities.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "359244f7b7532a528908e63cf80b1752b26ebbaa"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "359244f7b7532a528908e63cf80b1752b26ebbaa"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "359244f7b7532a528908e63cf80b1752b26ebbaa"
      availability: available
    - path: src/backend/tests/test_application_cadastro_estudante.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "359244f7b7532a528908e63cf80b1752b26ebbaa"
      availability: available
    - path: prompts/backend/20260914-camada-dominio-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Problema enriquecido, Perguntas em aberto e Fora do escopo"
      content_state: commit
      revision: "359244f7b7532a528908e63cf80b1752b26ebbaa"
      availability: available
    - path: docs/requisitos-seguranca.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "3.12 Requisitos e 4.9 a 4.16"
      content_state: commit
      revision: "359244f7b7532a528908e63cf80b1752b26ebbaa"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "359244f7b7532a528908e63cf80b1752b26ebbaa"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "359244f7b7532a528908e63cf80b1752b26ebbaa"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A decisão define comportamento de domínio, casos de uso e portas do backend; requisitos e segurança são evidências, não o destino principal."
classification:
  sphere: engineering
  concerns: [domain, architecture, privacy]
  decision_kind: design
  scope: component
  lifecycle: evolution
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: high
---

# Análise de decisão — edição e exclusão do perfil do estudante/candidato

## Solicitação original

`$decision-analysis-v4 Faça uma análise para a atividade "Implementar edição e exclusão do perfil." O perfil a que se refere é o estudando ou canditado a vagas.`

## Informações complementares

- A issue GitHub nº 39 descreve literalmente: `Implementar edição e exclusão do perfil com relação às camadas de casos de uso e domain. Use doubles de teste apropriados para testes unitários.`
- A informação do usuário delimita “perfil” como a identidade do estudante ou candidato a vagas, e não como uma versão de currículo.
- A issue estava `CLOSED` no momento da consulta, embora a implementação correspondente não esteja presente no commit analisado e a atividade tenha sido solicitada nesta branch.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem desta decisão | Nenhum identificado | v001 inicial | Não foi localizada análise anterior para edição e exclusão do perfil | Nenhum histórico a preservar |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `https://github.com/code-alchemists-br/sistema-curriculo/issues/39` | Principal | Prosa | Documentação da demanda | Issue GitHub | Conteúdo completo | Externo; fechada na consulta |
| `docs/requisitos_funcionais.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Commit `359244f` |
| `docs/modelagem_der.md` | Principal | Diagrama/modelo | Contrato de schema | Markdown/Mermaid | Arquivo completo | Commit `359244f` |
| `src/backend/domain/entities.py` | Principal | Código-fonte | Produção | Python | Arquivo completo | Commit `359244f` |
| `src/backend/application/ports.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `359244f` |
| `src/backend/infrastructure/persistence/sqlalchemy/usuario.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `359244f` |
| `src/backend/tests/test_application_cadastro_estudante.py` | Apoio | Código-fonte | Teste | Python | Arquivo completo | Commit `359244f` |
| `prompts/backend/20260914-camada-dominio-v001.md` | Apoio | Prosa | Documentação | Markdown | Problema, dúvidas e limites | Commit `359244f` |
| `docs/requisitos-seguranca.md` | Apoio | Prosa | Documentação | Markdown | Seções 3.12 e 4.9–4.16 | Commit `359244f` |
| `AGENTS.md` | Contexto | Prosa | Instrução para agentes | Markdown | Arquivo completo | Commit `359244f` |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução para agentes | Markdown | Arquivo completo | Commit `359244f` |

### Limites da evidência dos artefatos

Os requisitos não enumeram explicitamente quais campos constituem o perfil do candidato nem definem prazo de retenção, purga, reutilização de e-mail ou cascata de exclusão. O DER prevê `deleted_at` em `USUARIO`, mas o modelo ORM e a migration atuais persistem somente `id`, `nome`, `email` e `hash_senha`. Sessões, tokens, itens profissionais, currículos e associações ainda não estão persistidos. A análise pode decidir o limite de domínio e a intenção de exclusão lógica, mas a eliminação física completa depende de uma política posterior de retenção e de dados relacionados.

## Problema enriquecido

### Resultado desejado

Permitir que o estudante/candidato altere os dados identitários atualmente representados pelo agregado `Usuario` e exclua logicamente seu perfil, preservando identidade, invariantes, unicidade do e-mail, propriedade dos dados e possibilidade de uma futura purga controlada. Os fluxos devem permanecer independentes de FastAPI, SQLAlchemy e banco, e ser verificáveis com doubles assíncronos.

### Atores e interesses

- O estudante/candidato precisa corrigir seus dados e retirar seu perfil de uso sem alterar uma versão específica de currículo.
- O domínio precisa preservar a identidade do usuário, a validade de nome/e-mail e o estado de exclusão.
- A aplicação precisa impedir edição de perfil inexistente ou excluído, conflito de e-mail e efeitos fora do agregado correto.
- Segurança e privacidade precisam bloquear acesso após exclusão, evitar alteração de outro usuário e preparar retenção/purga auditável.
- A equipe precisa evoluir o modelo atual sem criar um conceito paralelo de perfil sem evidência de produto.

### Evidências e fatos observados

- A demanda limita a atividade às camadas Domain e Application e exige doubles nos testes unitários.
- `Usuario` já é o aggregate root da conta e identidade, proprietário conceitual dos currículos e itens profissionais.
- O perfil hoje possui apenas `id`, `nome`, `email` e `hash_senha`; nome e e-mail já são value objects validados.
- `Usuario` é uma dataclass imutável, portanto a edição precisa ser uma transição explícita que produza novo estado com o mesmo ID, em vez de mutação externa de atributos.
- `RepositorioUsuario` é assíncrono e oferece consulta por e-mail e salvamento, mas não oferece busca por ID nem atualização explícita.
- RF02 permite consultar, editar e excluir informações cadastradas; RF03 centraliza essas informações no estudante.
- O DER usa `deleted_at` em `USUARIO`, indicando exclusão lógica como intenção estrutural anterior.
- Os requisitos de segurança exigem acesso somente aos próprios dados, autorização no servidor e mecanismos de correção e solicitação de exclusão.
- A análise original de domínio deixou regras de exclusão explicitamente em aberto.

### Hipóteses

- Nesta atividade, “perfil” corresponde ao agregado `Usuario`, não a `Curriculo` nem a um novo agregado `PerfilCandidato`.
- A edição inicial abrange somente `nome` e `email`; senha pertence a fluxo próprio de credenciais e itens profissionais possuem casos de uso próprios.
- O ID do usuário será obtido futuramente de um contexto autenticado confiável, não de um identificador arbitrário fornecido pelo cliente.
- Exclusão nesta fatia significa transição lógica e bloqueio imediato de uso; purga física é uma atividade posterior condicionada à política de retenção.
- O instante de exclusão será fornecido por uma porta de relógio ou como valor já controlado pela Application, para manter testes determinísticos.

### Perguntas em aberto

- Qual é o prazo de retenção antes da purga física e quais obrigações legais ou acadêmicas se aplicam?
- O e-mail de um perfil excluído pode ser reutilizado imediatamente, apenas após purga ou nunca?
- Quais itens, currículos, documentos, sessões, tokens, exportações e logs devem ser apagados, anonimizados ou retidos na purga?
- A exclusão exige confirmação recente de senha ou outro mecanismo de reautenticação?
- Nome e e-mail são todos os campos editáveis desta primeira entrega, ou haverá dados pessoais/de contato adicionais?

### Escopo

- Definir `Usuario` como raiz do perfil do estudante/candidato.
- Definir transições de domínio para editar nome/e-mail e marcar exclusão lógica sem alterar ID ou hash de senha.
- Definir casos de uso separados `EditarPerfil` e `ExcluirPerfil`.
- Evoluir a porta de usuário com busca por ID e atualização explícita, reutilizando consulta por e-mail para verificar conflito.
- Definir falhas de aplicação para perfil inexistente, perfil excluído e e-mail pertencente a outro usuário.
- Especificar testes unitários de domínio e Application com doubles assíncronos e relógio controlado.

### Fora do escopo

- Implementar código, testes, API, DTOs HTTP, autenticação, autorização, ORM, migration ou alteração de banco nesta análise.
- Editar senha, itens profissionais, documentos, currículos ou associações currículo–vaga.
- Executar purga física, definir cascatas, reter backups, anonimizar auditoria ou revogar sessões concretas.
- Criar um agregado `PerfilCandidato` separado sem novo requisito que o diferencie de `Usuario`.

### Critérios de sucesso

- A edição conserva `UsuarioId` e `HashSenha`, aplica `Nome` e `Email` válidos e rejeita conflito com outro usuário.
- Perfil inexistente ou logicamente excluído não pode ser editado.
- A exclusão lógica registra uma única data/hora, é segura para repetição e torna o perfil indisponível aos fluxos de acesso.
- Os casos de uso aguardam somente portas de I/O; regras e transições de domínio permanecem síncronas.
- Testes unitários cobrem sucesso, ausência, conflito, estado excluído, preservação de identidade e ausência de efeitos indevidos.
- A decisão não confunde exclusão de perfil com exclusão de um currículo ou item profissional.

## Restrições aplicáveis

- Domain não pode depender de Application, Infrastructure, API, ORM, banco, serialização ou relógio do sistema.
- Application depende de portas internas e não acessa banco, API ou filesystem diretamente.
- Alterações do agregado devem ocorrer pela raiz e invariantes precisam permanecer próximas aos dados protegidos.
- I/O de repositório permanece assíncrono; transições do domínio permanecem síncronas.
- Toda função, classe e DTO futuro precisa documentar o que faz, como faz e qual finalidade atende.
- Mudanças de comportamento futuras exigem testes unitários no ambiente `nix develop .#backend`.
- A análise não autoriza implementação nem mudanças fora deste novo Markdown.

## Classificação comentada

A esfera é `engineering` porque a decisão define a evolução técnica do domínio e dos casos de uso. As preocupações principais são `domain`, pelo significado de perfil e suas transições; `architecture`, pelas portas e limites entre camadas; e `privacy`, porque exclusão lógica não equivale a eliminação definitiva dos dados. O risco é alto: uma decisão incorreta pode permitir acesso posterior à exclusão, apagar dados relacionados sem política ou deixar dados pessoais retidos indefinidamente.

## Decisão de roteamento

As subpastas imediatas existentes são `prompts/ambientes`, `prompts/backend`, `prompts/frontend`, `prompts/requisitos`, `prompts/revisao` e `prompts/templates`. O destino escolhido é `prompts/backend`, pois o propósito principal é orientar Domain, Application e suas portas. `prompts/requisitos` foi considerada por haver lacunas de produto e privacidade, mas os requisitos funcionam como evidência. `prompts/revisao` não se aplica porque esta é uma análise inicial, não uma revisão de implementação. Não há instrução adicional sob `prompts/backend`.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Correctness | Alta | Priorizar | Edição e exclusão devem preservar identidade, invariantes e unicidade. |
| Security | Alta | Priorizar | Perfil excluído ou de outro usuário não pode ser alterado nem acessado. |
| Privacy | Alta | Não confundir desativação com purga | Dados pessoais exigem retenção e eliminação explícitas. |
| Modifiability | Média | Priorizar | A primeira fatia deve aceitar itens e políticas futuras sem duplicar o conceito de perfil. |
| Simplicity | Média | Satisfazer | Evitar novo agregado e abstrações sem regra própria. |

## Alternativas consideradas

### Alternativa A — `Usuario` como perfil, edição por transição e exclusão lógica

Adicionar ao agregado operações que produzam uma nova representação com o mesmo ID e hash: uma para trocar `Nome`/`Email` e outra para registrar `deleted_at` uma única vez. `EditarPerfil` obtém por ID, verifica conflito de e-mail com outro usuário, executa a transição e solicita atualização. `ExcluirPerfil` obtém por ID, recebe um instante controlado, executa uma transição idempotente e solicita atualização. A porta ganha `obter_por_id` e `atualizar`; consultas funcionais devem desconsiderar excluídos. É a alternativa recomendada.

### Alternativa B — Exclusão física imediata de `Usuario`

Adicionar `excluir(usuario_id)` ao repositório e remover a linha assim que o caso de uso for executado. A opção elimina o dado principal mais rapidamente, mas não há política definida para itens, currículos, documentos, sessões, tokens, exportações, logs ou backups. Ela pode gerar cascata indevida, órfãos ou falsa promessa de eliminação completa.

### Alternativa C — Criar agregado `PerfilCandidato` separado de `Usuario`

Manter `Usuario` apenas para credenciais e criar uma identidade adicional para o perfil editável/excluível. A separação seria útil se conta e perfil possuíssem ciclos de vida distintos, mas os requisitos e o modelo atual tratam `Usuario` como proprietário e identidade do estudante. A alternativa adiciona sincronização, mapeamento e autorização sem necessidade comprovada.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Correctness | Alta | +2 | -1 | 0 | Alta | DER, agregado atual e lacunas de cascata. |
| Security | Alta | +2 | +1 | 0 | Média | Bloqueio lógico é modelável; revogação concreta ainda é handoff. |
| Privacy | Alta | +1 | 0 | -1 | Média | A prepara purga; B não garante apagar dados relacionados; C duplica dados. |
| Modifiability | Média | +2 | -2 | -1 | Alta | A preserva o limite atual e deixa política física substituível. |
| Simplicity | Média | +1 | +1 | -2 | Alta | A acrescenta um estado; B é simples apenas antes de existirem relações; C cria novo agregado. |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada para esta linhagem. A análise inicial da camada de domínio definiu `Usuario` como aggregate root e deixou regras de exclusão em aberto.

### Decisão recomendada nesta versão

Adotar a Alternativa A. Interpretar perfil como o agregado `Usuario`, limitado nesta entrega a nome e e-mail. Preservar a imutabilidade externa por transições explícitas que retornem o novo estado com o mesmo `UsuarioId` e `HashSenha`. Representar exclusão como `deleted_at` e manter o primeiro instante em chamadas repetidas.

Na Application, criar casos de uso distintos. `EditarPerfil` deve obter o usuário por ID, rejeitar ausência ou exclusão, verificar se o novo e-mail pertence a outro ID, aplicar a transição e chamar `atualizar`. `ExcluirPerfil` deve obter o usuário por ID, aplicar a exclusão lógica com instante controlado e chamar `atualizar`. A identidade deve vir de contexto autenticado confiável quando houver API; aceitar um ID do cliente sem autorização não satisfaz esta decisão.

Essa decisão não declara os dados fisicamente eliminados. A purga e suas cascatas permanecem bloqueadas até definição de retenção, reutilização de e-mail e tratamento de dependências.

### Impacto da revisão

Inicial; não há versão anterior a alterar.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Correctness | prioritized | Preserva identidade, credencial e invariantes durante a edição. | `Usuario`, `Nome`, `Email` e unicidade já existem. |
| Security | prioritized | Impede operações normais em perfil excluído e exige identidade confiável. | Requisitos RF-AUTZ-03, 05, 06 e 07. |
| Modifiability | prioritized | Permite adicionar persistência, API e purga sem criar outro conceito de perfil. | O agregado atual já é proprietário conceitual. |
| Privacy | unresolved | Separa bloqueio imediato de eliminação definitiva para não prometer purga inexistente. | Retenção e cascatas não estão definidas. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Simplicity | Nenhum agregado adicional sem ciclo de vida próprio | Reutiliza `Usuario` e os value objects existentes. |
| Reliability | Repetir exclusão não muda o primeiro instante nem reativa o perfil | A transição de exclusão é idempotente. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Correctness | Troca de e-mail pode violar unicidade ou sobrescrever credenciais/identidade. | Alta | Estudante e dados da conta. |
| Security | Um ID controlado pelo cliente pode editar ou excluir perfil alheio. | Crítica | Todos os usuários. |
| Privacy | “Exclusão” pode deixar dados acessíveis ou alegar eliminação que não ocorreu. | Alta | Titular dos dados e projeto. |
| Modifiability | Um novo agregado redundante fragmenta propriedade e autorização. | Média | Equipe de backend. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Correctness | Novas operações de porta, falhas explícitas e cenários de teste. | Simplicity | Aceitável para evitar atualização ambígua. |
| Security | Toda leitura/autenticação futura deve excluir perfis logicamente removidos. | Cognitive-load | Aceitável, mas exige contrato centralizado no repositório. |
| Modifiability | Exclusão física vira handoff separado. | Time-to-value | Aceitável porque a política necessária ainda não existe. |
| Privacy | Manter tombstone temporário até política de purga. | Cost-efficiency | Aceitável somente com prazo e finalidade definidos posteriormente. |

## Riscos e efeitos de segunda ordem

- Consultas que esquecerem o filtro de exclusão podem autenticar ou expor perfil removido; o comportamento deve ficar centralizado no adapter/repositório.
- Manter unicidade do e-mail após exclusão pode impedir novo cadastro; liberá-lo pode dificultar auditoria e recuperação. A política precisa ser explícita antes da persistência.
- Sessões e tokens ativos precisam ser revogados quando a infraestrutura correspondente existir; marcar `deleted_at` sozinho não os invalida.
- Itens profissionais e currículos pertencentes ao usuário podem permanecer acessíveis por rotas indiretas se autorização e filtros não forem consistentes.
- Uma futura purga precisa tratar chaves estrangeiras, documentos externos, exportações, logs e backups sem apagar registros que tenham obrigação legítima de retenção.
- O estado fechado da issue nº 39 pode produzir divergência de rastreabilidade; a equipe deve confirmar se houve fechamento administrativo ou implementação em outra referência.
- Se o produto definir conta e perfil com ciclos de vida independentes, a decisão de não criar `PerfilCandidato` deverá ser reaberta.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Perfil e usuário são o mesmo agregado nesta entrega | Aprovação do responsável e ausência de ciclo de vida separado | Revisar análise e requisitos | Necessidade de vários perfis por conta ou conta sem perfil. |
| Edição preserva identidade e credencial | Testes de domínio com mesmo ID/hash e novo nome/e-mail | Unitários no ambiente backend | Mutação externa, novo ID ou alteração do hash. |
| Conflito de e-mail considera o próprio usuário | Double retorna ausência, mesmo ID e ID diferente | Testes de Application | O próprio e-mail bloqueia edição ou duplicidade é aceita. |
| Perfil excluído não é editável nem autenticável | Casos de uso e consultas recusam `deleted_at` preenchido | Unitários e, depois, integração | Login ou edição funciona após exclusão. |
| Exclusão é idempotente | Repetição conserva o primeiro instante e não duplica efeito | Teste unitário com relógio controlado | Segundo pedido altera estado ou produz efeito inconsistente. |
| Exclusão física futura é segura | Política aprovada de retenção, cascata e e-mail | Análise específica de privacidade/persistência | Obrigação de apagamento imediato ou retenção incompatível. |

## Handoffs e atividades posteriores

- Implementar, em atividade autorizada separada, as transições do agregado, casos de uso, exceções, portas e testes unitários com doubles; executar somente em `nix develop .#backend`.
- Definir política de retenção, purga, reutilização de e-mail e tratamento de currículos, itens, documentos, logs e backups antes de alegar exclusão definitiva.
- Evoluir adapter, modelo Code First e migration para `deleted_at`, atualização por ID e filtros de perfis excluídos.
- Compor API e autorização usando a identidade autenticada, sem confiar no ID recebido do cliente; avaliar reautenticação para exclusão.
- Revogar sessões e tokens no mesmo limite transacional quando esses recursos existirem.
- Verificar com a equipe por que a issue nº 39 está fechada e ajustar sua rastreabilidade sem reabrir ou alterar o GitHub nesta atividade.

## Síntese

O perfil do estudante/candidato deve ser representado pelo agregado `Usuario`, e não por um currículo nem por uma nova entidade paralela. A primeira implementação deve editar somente nome e e-mail, preservar ID e hash, rejeitar conflitos e modelar a exclusão como transição lógica idempotente com `deleted_at`. Casos de uso separados coordenam repositório assíncrono e domínio síncrono. Essa escolha bloqueia acesso rapidamente e preserva a arquitetura atual, mas não substitui a decisão posterior de retenção e purga física dos dados relacionados.
