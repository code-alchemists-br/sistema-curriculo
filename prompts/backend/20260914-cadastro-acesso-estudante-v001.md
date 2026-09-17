---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: 2026-09-14
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
    - path: docs/requisitos_funcionais.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "3a5451e"
      availability: available
    - path: docs/casos-de-uso-v2.md
      relationship: primary
      representation: diagram-model
      function: documentation
      format: markdown with mermaid
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "3a5451e"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "3a5451e"
      availability: available
    - path: src/backend/domain/entities.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "3a5451e"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "UsuarioId, Email, Nome e HashSenha"
      content_state: commit
      revision: "3a5451e"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A decisão define um caso de uso interno, suas portas e sua relação com o agregado Usuario no backend."
classification:
  sphere: engineering
  concerns: [domain, architecture, implementation]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — cadastro do estudante em casos de uso e domínio

## Solicitação original

`$decision-analysis-v4 Faça uma análise para implementação de cadastro e acesso do estudante com relação às camadas de casos de uso e domain. Autorização e autenticação não deve entrar porque são de outro card. Leve em conta o documento 'docs\requisitos_funcionais.md' e o 'docs\casos-de-uso-v2.md'`

## Informações complementares

- O requisito RF13 exige autenticação para acesso a informações pessoais e
  currículos, mas a solicitação exclui explicitamente autenticação e autorização
  desta entrega.
- O documento de casos de uso separa **Cadastrar conta** de **Realizar login** e
  **Recuperar senha**.
- O domínio atual já contém o aggregate root `Usuario`, seus IDs e os value
  objects `Nome`, `Email` e `HashSenha`; ainda não há caso de uso, porta de
  repositório ou adaptador de persistência.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem | Nenhum identificado | v001 inicial | Não há análise anterior identificada para o caso de uso de cadastro do estudante | Nenhum histórico a preservar |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `docs/requisitos_funcionais.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Commit `3a5451e` |
| `docs/casos-de-uso-v2.md` | Principal | Modelo de diagrama | Documentação | Markdown/Mermaid | Arquivo completo | Commit `3a5451e` |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução para agentes | Markdown | Arquivo completo | Commit `3a5451e` |
| `src/backend/domain/entities.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `3a5451e` |
| `src/backend/domain/value_objects.py` | Apoio | Código-fonte | Produção | Python | `UsuarioId`, `Email`, `Nome` e `HashSenha` | Commit `3a5451e` |

### Limites da evidência dos artefatos

Os requisitos não definem campos obrigatórios, regras de unicidade de e-mail,
política de senha, mecanismo de autenticação, perfis de acesso ou recuperação
de senha. O DER e o domínio existente indicam um hash de senha, mas não definem
como produzi-lo. Por isso, esta análise não autoriza receber senha em texto
claro, derivar hash, comparar credenciais, emitir token, criar sessão ou decidir
permissões.

## Problema enriquecido

### Resultado desejado

Criar o caso de uso interno **Cadastrar estudante**, que orquestra a criação de
um `Usuario` válido e solicita sua persistência por uma porta interna. O caso de
uso deve ser independente de HTTP, ORM e banco de dados, e receber uma credencial
já derivada na fronteira responsável pela segurança, sem realizar acesso/login.

### Atores e interesses

- **Aluno:** precisa obter uma conta que o identifique como proprietário dos
  dados e currículos que cadastrará posteriormente.
- **Caso de uso de cadastro:** precisa coordenar a criação e a persistência do
  agregado sem conhecer interface, banco ou algoritmo de senha.
- **Domínio:** precisa preservar os invariantes locais de nome, e-mail, hash e
  identidade tipada do usuário.
- **Camada de infraestrutura futura:** precisa implementar a porta de
  persistência e a garantia de unicidade sem contaminar o núcleo.

### Evidências e fatos observados

- RF01 requer o cadastro das informações do estudante e RF03 prevê a
  centralização dessas informações para uso nos currículos.
- RF13 trata autenticação como requisito separado.
- UC01 descreve o cadastro de conta; UC02 descreve login e recuperação de senha
  como casos de uso distintos.
- `Usuario` já é o aggregate root de conta e identidade, exigindo ID, `Nome`,
  `Email` e `HashSenha`.
- As regras arquiteturais permitem use cases e portas internas, mas proíbem que
  aplicação dependa de infraestrutura ou API.

### Hipóteses

- A fronteira externa ou o card de segurança fornecerá um `HashSenha` já
  derivado; este caso de uso apenas o aceita como dado de domínio válido.
- Uma porta de repositório de usuário pode declarar a consulta de e-mail e o
  salvamento do agregado sem escolher ORM, banco ou SQL.
- A unicidade do e-mail será garantida pelo caso de uso por meio dessa porta e
  reforçada posteriormente pela infraestrutura, pois o e-mail é a única
  unicidade indicada pelo modelo já existente.

### Perguntas em aberto

- Qual componente de segurança produzirá o hash antes de chamar o caso de uso?
- Quais campos adicionais, limites e regras de validação serão obrigatórios no
  cadastro de estudante?
- Qual resposta de negócio deve representar um e-mail já cadastrado?
- A criação da conta requer confirmação de e-mail ou aprovação administrativa?

### Escopo

- Criar um modelo de entrada independente de transporte para o cadastro, com
  nome, e-mail e hash de senha já derivado.
- Criar uma porta interna para consultar existência por e-mail e salvar
  `Usuario`.
- Criar o caso de uso `CadastrarEstudante`, que gera um `UsuarioId`, constrói o
  agregado existente, impede e-mail já registrado e delega o salvamento à porta.
- Criar falha de negócio explícita para e-mail já cadastrado, sem convertê-la em
  resposta HTTP.
- Criar testes unitários com doubles de repositório e de gerador de ID, cobrindo
  cadastro válido, e-mail duplicado e ausência de chamada de salvamento na
  duplicidade.
- Documentar classes e funções e inserir a proveniência desta análise no código
  criado.

### Fora do escopo

- Login, verificação de senha, geração de hash, política de complexidade, salt,
  tokens, recuperação de senha, sessão, autenticação e autorização.
- HTTP, FastAPI, routers, DTOs de transporte, serialização, CORS e middleware.
- ORM, repositório concreto, banco de dados, migrations, SQL e configuração de
  ambiente.
- Cadastro, edição ou exclusão das demais informações do currículo; elas têm
  casos de uso próprios.
- Confirmação de e-mail, papéis de acesso, recrutador e integração com Grupo 2.

### Critérios de sucesso

- O use case constrói e persiste um `Usuario` somente quando o e-mail não está
  cadastrado.
- Um e-mail existente gera uma falha de negócio clara e não aciona salvamento.
- Os objetos criados não importam FastAPI, SQLAlchemy, Pydantic, banco, rede ou
  filesystem.
- Os testes são unitários e substituem a porta e o gerador de ID por doubles.
- Não há código de login, sessão, token, derivação ou comparação de senha,
  autenticação ou autorização no diff.

## Restrições aplicáveis

- O domínio não pode depender de Application, Infrastructure, API ou framework;
  Application não pode depender de Infrastructure ou API.
- A entrada externa deve ser convertida antes do caso de uso, mas o modelo de
  entrada desta análise permanece independente de transporte.
- O domínio não expõe entidades diretamente por uma API e casos de uso não
  acessam banco ou arquivos diretamente.
- O hash é somente um value object já preparado; aplicar criptografia, autenticar
  ou autorizar é responsabilidade excluída desta entrega.
- Testes unitários de backend devem usar o ambiente Nix `.#backend` e não podem
  usar adapter real, banco, rede ou framework iniciado.

## Classificação comentada

Trata-se de uma decisão de engenharia para orquestrar a criação de conta do
estudante entre Application e Domain. As preocupações de domínio, arquitetura e
implementação distinguem o agregado já existente, a porta interna que preserva
as dependências para dentro e o fluxo testável de cadastro. O risco é médio:
o contrato de cadastro será consumido por adaptadores futuros, mas permanece
reversível antes da definição de HTTP e persistência.

## Decisão de roteamento

`prompts/backend` é o local mais específico para uma decisão de caso de uso,
porta interna e agregado de backend. `prompts/requisitos` foi considerada porque
os requisitos são evidência principal, mas não é o destino do desenho de
implementação. `prompts/revisao` não se aplica porque não há linhagem anterior
deste problema.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Correção | Alta | Satisfazer | Usuários com e-mail duplicado não podem ser persistidos silenciosamente. |
| Separação arquitetural | Alta | Satisfazer | O cadastro deve continuar independente de HTTP, ORM e banco. |
| Testabilidade | Alta | Satisfazer | A orquestração precisa ser validada com doubles determinísticos. |
| Simplicidade | Média | Priorizar | O caso de uso deve criar somente a conta, sem antecipar acesso ou segurança. |
| Modificabilidade | Média | Maximizar | A porta permite trocar persistência e a fronteira de segurança posteriormente. |

## Alternativas consideradas

### Alternativa A — caso de uso de cadastro com porta interna e hash já derivado

Criar `CadastrarEstudante` com uma entrada independente de transporte, uma porta
de repositório e um gerador de ID interno. O caso de uso consulta o e-mail,
constrói `Usuario` com `HashSenha` recebido e salva o agregado. Não recebe senha
em texto claro nem executa login. Esta é a alternativa recomendada.

### Alternativa B — cadastrar e realizar login no mesmo caso de uso

Após persistir o usuário, o fluxo verificaria senha, criaria sessão ou token e
devolveria acesso autenticado. Embora pareça reduzir etapas para o aluno, viola
a exclusão explícita de autenticação e autorização e mistura UC01 com UC02. É
inviável nesta entrega.

### Alternativa C — cadastrar diretamente em controller ou repositório ORM

O adapter HTTP ou um modelo SQLAlchemy validaria e salvaria os dados sem caso de
uso interno. A implementação seria curta, porém colocaria regra de unicidade e
orquestração em camada externa e violaria Clean Architecture. É inviável pelas
restrições arquiteturais.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Correção | Alta | +2 | +1 | 0 | Alta | Verificação explícita de duplicidade pelo caso de uso |
| Separação arquitetural | Alta | +2 | 0 | -2 | Alta | Regras de backend aplicáveis |
| Testabilidade | Alta | +2 | 0 | -1 | Alta | Porta e gerador substituíveis por doubles |
| Simplicidade | Média | +1 | -1 | +2 | Média | Escopo limitado sem segurança ou adaptadores |
| Modificabilidade | Média | +2 | 0 | -1 | Alta | Persistência e fronteira de segurança ficam substituíveis |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### Decisão recomendada nesta versão

Implementar a Alternativa A. A fatia elegível compreende:

1. `CadastrarEstudanteEntrada`, modelo interno imutável com `Nome`, `Email` e
   `HashSenha` já construídos, sem campo de senha em texto claro;
2. `RepositorioUsuario`, porta de Application com operações mínimas para
   consultar e-mail e salvar um `Usuario`;
3. `GeradorUsuarioId`, porta ou dependência interna para produzir `UsuarioId`
   de forma substituível em testes;
4. `CadastrarEstudante`, caso de uso que consulta a existência de e-mail,
   falha se já houver conta, constrói `Usuario` e solicita persistência;
5. `EmailJaCadastrado`, falha de negócio independente de transporte;
6. testes unitários com fake ou spy de repositório e stub de gerador de ID.

O termo **acesso** desta demanda fica limitado a preparar a conta do estudante
para um fluxo posterior. O login e qualquer decisão que conceda acesso são
explicitamente encaminhados ao card de autenticação/autorização.

### Impacto da revisão

Análise inicial; nenhum impacto de revisão.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Modificabilidade | maximized | Persistência, UUID e fronteira de segurança podem mudar sem reescrever o fluxo | Portas internas isolam dependências externas |
| Simplicidade | prioritized | Apenas cadastro é entregue; UC02 permanece separado | Solicitação exclui autenticação e autorização |
| Correção | prioritized | E-mail duplicado é interrompido antes da persistência | E-mail é a unicidade identificada no modelo atual |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Separação arquitetural | Nenhum acesso a framework, ORM ou banco pelo caso de uso | Use case depende de domínio e de portas internas |
| Testabilidade | Fluxo exercitável inteiramente em memória | Repositório e gerador de ID são doubles de teste |
| Correção | E-mail repetido não gera persistência | Consulta precede construção e salvamento |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Correção | Contas duplicadas podem disputar os mesmos dados e currículos | Alta | Alunos e equipe de suporte |
| Separação arquitetural | Regras de cadastro ficam acopladas ao adapter ou banco escolhido | Alta | Desenvolvedores de backend |
| Testabilidade | Testar cadastro exige infraestrutura real e torna falhas menos determinísticas | Média | Equipe de qualidade |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Separação arquitetural | Definir interfaces internas antes do repositório concreto | Simplicidade | Aceitável para impedir dependência de infraestrutura |
| Testabilidade | Passar gerador de ID como dependência do caso de uso | Simplicidade | Aceitável para tornar resultados determinísticos |
| Escopo | Não entregar login após o cadastro | Time-to-value | Obrigatório, pois autenticação é outro card |

## Riscos e efeitos de segunda ordem

- A verificação por porta não substitui restrição de unicidade na persistência;
  o adapter Code First futuro deve reforçá-la sem modificar esta regra de uso.
- Aceitar `HashSenha` pronto pressupõe uma fronteira de segurança ainda não
  definida. O caso de uso não deve inventar algoritmo ou receber senha clara.
- Se e-mail institucional obrigatório, confirmação de e-mail ou perfis de acesso
  forem exigidos, a análise precisa de revisão antes da implementação.
- A criação de uma conta não autentica o aluno nem permite acesso às informações;
  o card de autenticação/autorização deve tratar essas transições.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Cadastro constrói o agregado correto | Spy registra um `Usuario` com entrada e ID esperados | Teste unitário do use case com doubles | Campos diferentes ou valor de transporte no agregado |
| E-mail duplicado é bloqueado | Fake informa existência e spy não recebe salvamento | Teste unitário determinístico | Salvamento ocorre após a duplicidade |
| Núcleo não conhece infraestrutura | Imports não incluem framework, ORM, banco ou API | Revisão de imports e testes no ambiente `.#backend` | Dependência externa aparece em Domain/Application |
| Escopo não inclui autenticação | Diff não contém hash de senha, comparação, token ou sessão | Revisão de diff | Código concede acesso ou processa credencial clara |
| Porta cobre persistência futura | Adapter pode implementar consulta e salvamento sem alterar o use case | Revisão de contrato quando infraestrutura for analisada | Nova regra exige transação ou consulta adicional |

## Handoffs e atividades posteriores

- `$backend-adapters-drivers-v2`: implementar adaptador de persistência Code
  First e restrição de unicidade de e-mail depois de uma análise de
  infraestrutura/migrations.
- Card de autenticação/autorização: derivar e verificar senha, login, sessão,
  token, recuperação de senha e políticas de acesso.
- `$integration-system-testing-v1`: criar testes de integração de persistência
  e API somente após existirem adapter e interface de transporte.
- Análise de requisitos: definir campos obrigatórios, limites, e-mail
  institucional, confirmação e resposta de negócio para duplicidade, se esses
  pontos alterarem o contrato de cadastro.

## Síntese

O cadastro do estudante deve ser entregue como um caso de uso interno que
orquestra o agregado `Usuario` já existente por portas substituíveis. A entrada
recebe somente value objects, incluindo um hash já derivado, e o fluxo impede
e-mail duplicado antes de persistir. Essa direção atende UC01 e prepara a conta
para uso futuro, sem fundir cadastro com UC02 nem introduzir autenticação ou
autorização antes do card responsável.
