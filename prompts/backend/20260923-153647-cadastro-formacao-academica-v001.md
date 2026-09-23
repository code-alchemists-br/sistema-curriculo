---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-09-23T15:36:47-03:00"
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
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 462535e"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 462535e"
      availability: available
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 462535e"
      availability: available
    - path: src/backend/application/perfil_estudante.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 462535e"
      availability: available
    - path: src/backend/application/cadastro_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 462535e"
      availability: available
    - path: src/backend/domain/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 462535e"
      availability: available
    - path: src/backend/tests/test_application_perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 462535e"
      availability: available
    - path: src/backend/tests/test_domain_entities.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 462535e"
      availability: available
    - path: prompts/backend/20260914-camada-dominio-v001.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Evidências, Escopo, Perguntas em aberto, Decisão recomendada e Riscos"
      content_state: working-tree
      revision: "working-tree based on 462535e"
      availability: available
    - path: prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Informações complementares, Problema enriquecido e Restrições aplicáveis"
      content_state: working-tree
      revision: "working-tree based on 462535e"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 462535e"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 462535e"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A decisão define a orquestração Application, uma porta interna e o uso da entidade de domínio existente no backend."
classification:
  sphere: engineering
  concerns: [domain, architecture, implementation]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — cadastro da formação acadêmica

## Solicitação original

`$decision-analysis-v4 Implementar cadastro da formação acadêmica com relação às camadas de casos de uso e domain. Use doubles de teste apropriados para testes unitários.`

## Informações complementares

- A entidade `FormacaoAcademica`, `FormacaoAcademicaId`, `UsuarioId` e `Periodo` já existem no domínio.
- A formação é uma entidade reutilizável pertencente ao usuário, não uma coleção do agregado `Usuario` nem do agregado `Curriculo`.
- A Application possui apenas a porta de usuário e casos de uso de cadastro de conta e edição/exclusão de perfil; não há porta nem adapter para formações.
- O estado atual da árvore de trabalho estava limpo e foi observado sobre o commit `462535e`.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem | Nenhum artefato anterior para este cadastro | v001 inicial | A análise de domínio anterior excluiu explicitamente casos de uso e portas | Nova decisão, sem revisão de decisão anterior |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/domain/itens_perfil.py` | Principal | Código-fonte | Produção | Python | Arquivo completo | Árvore de trabalho baseada em `462535e` |
| `src/backend/domain/value_objects.py` | Principal | Código-fonte | Produção | Python | Arquivo completo | Árvore de trabalho baseada em `462535e` |
| `src/backend/application/ports.py` | Principal | Código-fonte | Produção | Python | Arquivo completo | Árvore de trabalho baseada em `462535e` |
| `src/backend/application/perfil_estudante.py` | Principal | Código-fonte | Produção | Python | Arquivo completo | Árvore de trabalho baseada em `462535e` |
| `cadastro_estudante.py`, `usuario.py` e os dois testes listados no front matter | Apoio | Código-fonte | Produção/teste | Python | Arquivos completos | Árvore de trabalho baseada em `462535e` |
| Análises de domínio e refatoração listadas no front matter | Contexto | Prosa | Documentação | Markdown | Seções indicadas | Árvore de trabalho baseada em `462535e` |
| `AGENTS.md` e `src/backend/AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Arquivos completos | Árvore de trabalho baseada em `462535e` |

### Limites da evidência dos artefatos

Não há requisito aprovado para vocabulários de `nivel` e `status`, limites de texto, unicidade de formação, nem endpoint ou schema de persistência. Esta decisão não inventa essas regras, nem implementa ORM, migration, API ou adapter concreto.

## Problema enriquecido

### Resultado desejado

Permitir que um usuário ativo cadastre uma `FormacaoAcademica` válida usando a entidade e os value objects já existentes, por um caso de uso testável que dependa apenas de portas internas.

### Atores e interesses

- Usuário estudante/candidato: registra uma formação que poderá ser reutilizada em currículos.
- Application: coordena existência e estado do proprietário, identidade e persistência sem conhecer I/O.
- Domínio: mantém identidade tipada e cronologia do período livre de framework e repositório.
- Desenvolvedores e QA: verificam a orquestração sem banco, ORM, rede, relógio ou UUID aleatório.

### Evidências e fatos observados

- `FormacaoAcademica` recebe `id`, `usuario_id`, `instituicao`, `curso`, `nivel`, `periodo` e `status`; `Periodo` rejeita datas invertidas.
- `Usuario.excluido` representa o ciclo de vida do proprietário e os casos existentes rejeitam edição de perfil excluído.
- `RepositorioUsuario` já fornece `obter_por_id`; o fluxo de cadastro de estudante usa protocolo assíncrono, gerador de ID injetado e persistência via porta.
- Os testes de `perfil_estudante.py` adotam spy de repositório em memória e stub de relógio, sem infraestrutura.

### Hipóteses

- Cadastrar uma formação para proprietário inexistente ou excluído deve ser rejeitado, pois a formação pertence ao perfil ativo e a Application coordena regras entre agregados.
- Não há regra de duplicidade de formação: duas formações com mesmos textos e período podem ser distintas até que requisito de produto determine o contrário.
- A persistência futura garantirá integridade referencial por migration Code First, mas a implementação desta fatia limita-se ao contrato interno e aos testes unitários.

### Perguntas em aberto

- Quais valores são permitidos para `nivel` e `status`?
- `instituicao` e `curso` exigem normalização, tamanho mínimo/máximo ou regra de preenchimento?
- A formação deve permitir duplicidade, edição e exclusão; e qual comportamento é exigido quando já estiver referenciada por currículo?

### Escopo

- Acrescentar a porta específica de formação e um gerador substituível de `FormacaoAcademicaId` em `application/ports.py`.
- Acrescentar `CadastrarFormacaoAcademicaEntrada` e `CadastrarFormacaoAcademica` junto às intenções de perfil, em `application/perfil_estudante.py`.
- Consultar o `RepositorioUsuario`, rejeitar perfil ausente ou excluído, criar a entidade de domínio e solicitar seu salvamento pela nova porta.
- Reexportar a nova superfície de Application e escrever testes unitários de domínio/Application com doubles próprios.

### Fora do escopo

- Alterar limites de agregados, mover a formação para `Usuario` ou `Curriculo`, ou fazer o domínio consultar repositórios.
- Criar API HTTP, DTO de transporte, autenticação/autorização, modelo SQLAlchemy, migration, tabela ou adapter concreto.
- Definir políticas novas de vocabulário, duplicidade, edição, exclusão ou referências a currículo.

### Critérios de sucesso

- O caso de uso constrói e devolve `FormacaoAcademica` com ID gerado, proprietário e `Periodo` recebidos.
- Perfil inexistente ou excluído não gera ID nem solicita salvamento.
- A Application depende de protocolos internos; domínio não importa Application, API, ORM ou infraestrutura.
- Os testes unitários usam doubles controlados e passam no ambiente Nix `backend`.

## Restrições aplicáveis

- Clean Architecture: dependências apontam para dentro; casos de uso não acessam banco, API ou filesystem diretamente.
- DDD: formação permanece entidade independente pertencente ao usuário; `Usuario` e `Curriculo` continuam aggregate roots separados.
- As invariantes locais continuam no domínio: UUID tipado e `Periodo` válido; coordenação de proprietário ocorre na Application por portas.
- Toda classe, função e DTO/entrada criados devem documentar o que fazem, como fazem e para qual finalidade existem.
- Testes unitários do backend devem executar em `nix develop .#backend` e controlar dependências externas com doubles.

## Classificação comentada

É uma decisão de engenharia, de design de componente, que conecta uma intenção de perfil à entidade de domínio já modelada. Há incerteza média porque regras de conteúdo e ciclo de vida da formação não foram especificadas; ela não impede um cadastro mínimo que preserve as regras conhecidas.

## Decisão de roteamento

`prompts/backend` foi escolhido porque os artefatos principais e a decisão tratam das fronteiras Domain/Application do backend. `prompts/requisitos` foi considerado para as perguntas de produto, mas não é o propósito principal; `prompts/revisao` não se aplica a uma linhagem inicial.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Correção | Alta | Satisfazer: só criar formação para perfil ativo e período válido | Evita item órfão ou uso de perfil removido |
| Separação arquitetural | Alta | Maximizar | Mantém I/O e ORM fora do domínio e dos casos de uso |
| Testabilidade | Alta | Maximizar | Permite provar fluxo e ausência de efeitos com doubles determinísticos |
| Modificabilidade | Média | Priorizar | Permite adapter e regras futuras sem refazer o caso de uso |
| Simplicidade | Média | Satisfazer | Evita abstração genérica para seis tipos de item sem requisito comum |

## Alternativas consideradas

### Alternativa A — anexar formações ao agregado e repositório de `Usuario`

Estender `Usuario` com uma coleção de formações e persistir tudo por `RepositorioUsuario`. É inviável: contradiz a decisão já registrada de que itens de perfil são entidades independentes e reutilizáveis, e aumenta a transação do agregado sem regra que o justifique.

### Alternativa B — caso de uso específico com portas específicas de formação

Criar `CadastrarFormacaoAcademica` em `perfil_estudante.py`, entrada com `UsuarioId`, textos e `Periodo`, `GeradorFormacaoAcademicaId` e `RepositorioFormacaoAcademica.salvar`. O caso consulta `RepositorioUsuario.obter_por_id`, rejeita ausência e exclusão pelas exceções já existentes, constrói `FormacaoAcademica` e a salva. É a alternativa recomendada.

### Alternativa C — repositório genérico de itens de perfil

Criar agora uma porta única com união de seis entidades e operações genéricas. Embora reduza nomes hoje, é abstração antecipada: cada item ainda não compartilha regras ou operações suficientes para um contrato coeso, e o cadastro de formação ficaria menos explícito.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Correção | Alta | -2 | +2 | +1 | Alta | Limites de agregados e `Periodo` existentes |
| Separação arquitetural | Alta | -1 | +2 | +1 | Alta | Regras de Clean Architecture e portas atuais |
| Testabilidade | Alta | -1 | +2 | +1 | Alta | Spies e stubs dos testes de Application |
| Modificabilidade | Média | -1 | +2 | 0 | Média | Entidade independente e adapter futuro |
| Simplicidade | Média | 0 | +1 | -1 | Média | Não há comportamento comum aprovado aos seis itens |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado. A análise de domínio anterior decidiu os limites da entidade, mas não esta intenção de cadastro.

### Decisão recomendada nesta versão

Implementar a Alternativa B. O caso de uso deve permanecer no módulo de perfil, pois cadastrar formação é uma intenção do perfil do usuário. Recebe `RepositorioUsuario`, `RepositorioFormacaoAcademica` e `GeradorFormacaoAcademicaId`; primeiro obtém o proprietário, aplica as falhas já semânticas de perfil ausente/excluído, gera o ID tipado, instancia `FormacaoAcademica` e aguarda `salvar`.

A entrada não deve receber UUID cru, sessão, modelo ORM ou dados HTTP. Ela deve transportar `UsuarioId` e `Periodo` já válidos; os textos permanecem como `str` porque o domínio atual os modela assim. Novas validações de texto ou vocabulário só devem ser introduzidas com requisito aprovado e testes de domínio correspondentes.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Separação arquitetural | maximized | Portas isolam persistência e geração de ID | Protocolos existentes seguem esse desenho |
| Testabilidade | maximized | Fluxo observado sem I/O | Doubles atuais exercitam casos assíncronos |
| Modificabilidade | prioritized | Adapter SQLAlchemy pode ser adicionado sem mudar o caso | Formação já é entidade independente |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Correção | Perfil ativo e período cronologicamente válido | Application verifica proprietário; `Periodo` valida cronologia |
| Simplicidade | Uma porta e um gerador específicos, sem genericidade prematura | Contrato expressa exatamente o item cadastrado |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Correção | Formação pode ser criada para perfil inexistente ou removido | Alta | Usuários e suporte |
| Separação arquitetural | Regras passam a depender de ORM ou repositório concreto | Alta | Backend e testes |
| Testabilidade | Cenários exigem banco ou UUID aleatório | Média | Desenvolvimento e QA |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Separação arquitetural | Definir duas abstrações internas antes do adapter | Simplicidade | Aceitável; correspondem a capacidades reais do caso |
| Correção | Uma leitura adicional do proprietário | Delivery-speed | Aceitável; protege associação entre agregados |
| Testabilidade | Manter doubles explícitos no teste | Brevidade do teste | Aceitável; torna efeitos e chamadas verificáveis |

## Riscos e efeitos de segunda ordem

- Sem constraint de chave estrangeira até a futura persistência Code First, outro produtor ainda pode tentar inserir registro órfão; o adapter e migration devem reforçar a integridade sem substituir a verificação do caso de uso.
- Consultar e depois inserir não substitui uma transação no adapter; a composição externa deverá agrupar o fluxo quando houver persistência concreta.
- Tratar `nivel` e `status` como texto preserva flexibilidade, mas admite valores semanticamente inconsistentes até haver vocabulário aprovado.
- Reutilizar `PerfilNaoEncontrado` e `PerfilExcluido` mantém a semântica uniforme enquanto a formação permanecer uma intenção do perfil; caso futuras intenções precisem das mesmas falhas em outros módulos, extrair as exceções para módulo Application comum deve ser analisado separadamente.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Cadastro válido cria e salva a entidade correta | ID fixo, usuário ativo e formação capturada | Stub de gerador + stub de usuário + spy de formações | Entidade exigir regra adicional não coberta pelo construtor |
| Ausência de usuário interrompe sem efeito | Nenhuma chamada ao gerador ou spy | Stub que retorna `None` e contadores | Requisito permitir rascunho sem usuário |
| Perfil excluído interrompe sem efeito | Nenhuma chamada ao gerador ou spy | Stub com `Usuario.excluir` | Política permitir cadastro após exclusão |
| Domínio preserva invariantes | Falha para período invertido e IDs não tipados | Testes de value object/entidade em memória | Vocabulário ou texto receber regra formal |
| Aplicação não depende de infraestrutura | Imports e suíte unitária verde | `rg` e testes no Nix backend | Necessidade de transação ou consulta não expressável pela porta |

## Handoffs e atividades posteriores

- Implementar a porta, gerador, entrada, caso de uso, reexports e os testes unitários especificados, com docstrings completas e proveniência desta análise.
- Quando o escopo incluir persistência, criar adapter SQLAlchemy, modelo, metadata e migration Alembic Code First para formação; testar a integração no ambiente `tests`.
- Submeter os vocabulários e políticas de duplicidade, edição, exclusão e referências de currículo a uma decisão de requisitos/domínio antes de codificá-los.

## Síntese

O cadastro deve usar a entidade `FormacaoAcademica` existente, sem transformar itens reutilizáveis em coleção de `Usuario` ou `Curriculo`. Um caso de uso específico de perfil, apoiado por repositórios de usuário e formação e por um gerador de ID, preserva as fronteiras e permite testes determinísticos com stub e spy. A principal incerteza é a ausência de regras aprovadas para os campos textuais e o ciclo de vida posterior da formação.
