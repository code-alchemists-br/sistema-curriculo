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
    - path: docs/fundamentos-backend.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "657e328"
      availability: available
    - path: docs/modelagem_der.md
      relationship: primary
      representation: diagram-model
      function: schema-contract
      format: markdown with mermaid erDiagram
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "b49dc9e"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "657e328"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "657e328"
      availability: available
    - path: src/backend/main.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "657e328"
      availability: available
    - path: prompts/backend/20260913-fundamentos-fastapi-v001.md
      relationship: supporting
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "657e328"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A decisão define o modelo de domínio e seus limites no backend; os documentos de requisitos são evidência e não o destino principal."
classification:
  sphere: engineering
  concerns: [domain, architecture, data]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: high
---

# Análise de decisão — camada de domínio do sistema de currículos

## Solicitação original

`$decision-analysis-v4 faça uma análise para implementação da camada de domínio. Use os documentos 'docs\fundamentos-backend.md' e 'docs\modelagem_der.md' como referencia para as entidades, value objects etc.`

## Informações complementares

- A fundação atual contém somente uma fábrica FastAPI e a entrada ASGI; não há
  entidades, casos de uso, rotas, ORM, banco de dados ou migrations.
- A análise anterior da fundação FastAPI delimitou expressamente o domínio como
  trabalho posterior. Ela é contexto de continuidade técnica, não uma versão
  anterior desta decisão.
- O DER enumera estruturas e relacionamentos, mas não especifica regras de
  negócio, estados permitidos, regras de exclusão, ordenação dos itens no
  currículo nem fluxos de autenticação e integração.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem desta decisão | Nenhum identificado | v001 inicial | Não há análise anterior sobre a camada de domínio | Nenhum histórico a preservar |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `docs/fundamentos-backend.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Commit `657e328` |
| `docs/modelagem_der.md` | Principal | Modelo de diagrama | Contrato de schema | Markdown/Mermaid | Arquivo completo | Commit `b49dc9e` |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução para agentes | Markdown | Arquivo completo | Commit `657e328` |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `657e328` |
| `src/backend/main.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `657e328` |
| `prompts/backend/20260913-fundamentos-fastapi-v001.md` | Apoio | Prosa | Instrução de implementação | Markdown | Arquivo completo | Commit `657e328` |

### Limites da evidência dos artefatos

O DER é uma representação estrutural, não uma especificação completa de
comportamentos. Em particular, ele não define quais alterações são permitidas
após uma exportação, o significado dos níveis e status textuais, regras de
unicidade além do e-mail, nem o ciclo de vida de sessão, recuperação de senha,
documento e integração externa. A análise, portanto, recomenda invariantes
dedutíveis da estrutura e adia regras que dependeriam de invenção de produto.

## Problema enriquecido

### Resultado desejado

Definir uma camada de domínio Python independente de FastAPI, SQLAlchemy,
Pydantic, banco de dados, serialização e serviços externos. Ela deve expressar
os conceitos do DER como entidades e value objects, proteger invariantes locais
e permitir que a persistência Code First seja mapeada posteriormente na camada
de infraestrutura, sem reproduzir o DER como modelos ORM.

### Atores e interesses

- Estudantes/usuários precisam manter dados profissionais e compor versões de
  currículo com esses dados.
- Desenvolvedores de domínio precisam de limites de agregados que mantenham
  regras locais consistentes e testáveis em memória.
- Desenvolvedores de aplicação e infraestrutura precisam de identidades,
  contratos e relações claras para orquestrar casos de uso e implementar
  repositórios e mapeamentos SQLAlchemy posteriormente.
- Equipe de segurança precisa evitar que segredos, como senha e token de
  acesso, sejam tratados como texto comum ou expostos pela interface.

### Evidências e fatos observados

- A arquitetura prescrita coloca entidades, value objects e portas no domínio;
  mapeamentos ORM, sessões, repositórios concretos e migrations pertencem à
  infraestrutura.
- O DER associa formação, experiência, projeto, competência, idioma e documento
  a um usuário; um currículo referencia esses itens por associações próprias.
- `USUARIO` é proprietário de currículos, sessões e tokens de recuperação.
- O DER prevê exportação de currículo e registro de integração com sistema
  externo, mas não descreve suas políticas comportamentais.
- A camada API existente é uma base vazia e não deve ser importada pelo domínio.

### Hipóteses

- Um usuário pode manter os itens de perfil independentemente e reutilizá-los
  em mais de uma versão de currículo; isso decorre das associações muitos-para-
  muitos do DER.
- A inclusão no currículo pode ser representada por referências identificadas,
  sem transformar as tabelas de associação em entidades de domínio enquanto não
  houver ordem, visibilidade ou outros atributos próprios.
- Identificadores UUID tipados, e-mail, intervalo de datas e hash de senha têm
  semântica suficiente para serem value objects iniciais.
- Campos textuais de nível, status, layout e formato não devem virar enums até
  que seus vocabulários e transições sejam especificados.

### Perguntas em aberto

- Quais são os valores e transições válidos para `nivel`, `status`, `layout` e
  `formato`?
- Uma formação, experiência, projeto, competência, idioma ou documento pode ser
  removido quando é referenciado por um currículo? A remoção é lógica ou física?
- Qual é a regra de propriedade que garante que um currículo só referencie itens
  do mesmo usuário?
- Currículos e seus itens possuem ordenação ou personalização por versão?
- Quais regras de expiração, revogação, tentativas de login e bloqueio aplicam-
  se a sessão e ao token de recuperação?
- Qual é o comportamento de negócio das exportações e integrações externas?

### Escopo

- Criar o pacote `src/backend/domain` e seus módulos internos sem dependências
  de frameworks ou I/O.
- Modelar `Usuario` e `Curriculo` como aggregate roots separados.
- Modelar formação acadêmica, experiência profissional, projeto acadêmico,
  competência, idioma e documento como entidades independentes, cada qual
  pertencente a um usuário por identidade.
- Modelar value objects de identidade tipada, `Email`, `Nome`, `Periodo` e
  `HashSenha`; introduzir value objects adicionais somente onde houver
  invariantes verificáveis.
- Fazer `Curriculo` manter referências tipadas aos itens selecionados e impedir
  referência duplicada do mesmo tipo dentro da mesma versão.
- Garantir invariantes locais: identificadores presentes, e-mail estruturalmente
  válido, início não posterior ao fim em períodos e impossibilidade de um
  currículo sem proprietário.
- Criar testes unitários de domínio para construção válida, rejeição de dados
  inválidos e gestão de referências, executados no ambiente Nix de backend.
- Documentar funções e classes conforme as regras do repositório e registrar a
  proveniência desta análise nos arquivos de código que forem criados.

### Fora do escopo

- Casos de uso, comandos, DTOs, portas de repositório, injeção de dependência,
  API HTTP, routers e serialização.
- SQLAlchemy, modelos declarativos, mapeamento imperativo, banco de dados,
  migrations Alembic, scripts SQL e implementação de repositórios.
- Autenticação, hashing de senha, geração ou validação criptográfica de tokens,
  autorização, política de bloqueio e gerenciamento efetivo de sessão.
- Upload ou armazenamento de arquivos, geração de exportações, comunicação com
  sistemas externos e persistência de logs.
- Vocabulários de `nivel`, `status`, `layout` e `formato`, regras de exclusão,
  ordenação e regras transagregados ainda não especificadas.

### Critérios de sucesso

- O domínio pode ser importado e testado sem FastAPI, SQLAlchemy, Pydantic,
  banco, rede, relógio do sistema ou filesystem.
- Cada entidade possui identidade explícita, comportamento de construção e
  invariantes documentados; cada value object é imutável e validado na criação.
- `Curriculo` encapsula suas referências e não expõe coleção mutável que permita
  duplicatas ou alteração externa sem passar por seu comportamento.
- Nenhum modelo ORM, DTO ou detalhe de tabela/junção aparece no domínio.
- A decisão sobre o vínculo entre currículos e itens permanece reversível até a
  especificação de ordenação ou atributos da associação.

## Restrições aplicáveis

- As dependências devem apontar para dentro: domínio não pode depender de API,
  aplicação, infraestrutura, frameworks, banco ou serviços externos.
- O modelo e os mapeamentos Code First são a fonte de verdade do schema, mas os
  mapeamentos devem ficar na infraestrutura; o DER não autoriza scripts SQL
  manuais nem entidades ORM no domínio.
- Regras e invariantes devem estar no modelo de domínio próximo aos dados que
  protegem; DTOs não substituem entidades ou value objects.
- Agregados devem ter limites claros e serem alterados por sua aggregate root.
- Toda função e classe deve ter docstring que declare responsabilidade,
  abordagem e finalidade; testes unitários do backend usam `nix develop
  .#backend`.

## Classificação comentada

É uma decisão de engenharia de design para uma camada de domínio. Ela combina
as preocupações de domínio, arquitetura e dados: traduz o modelo estrutural em
comportamentos independentes de persistência, fixa limites de consistência e
preserva a futura implementação Code First. O risco é alto porque limites de
agregado e vocabulário ubíquo se propagam para casos de uso, persistência e API;
a revisão é moderadamente custosa após esses consumidores existirem.

## Decisão de roteamento

`prompts/backend` é a categoria mais específica para uma decisão sobre código
de domínio no backend. `prompts/requisitos` foi considerada porque os documentos
de entrada descrevem necessidades e estrutura, mas não é o destino principal da
implementação. `prompts/revisao` não se aplica: esta é uma nova linhagem, não a
revisão da análise de FastAPI.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Correção | Alta | Satisfazer | Invariantes locais devem impedir objetos inválidos desde a criação. |
| Separação arquitetural | Alta | Satisfazer | O domínio deve permanecer alheio a FastAPI, ORM e persistência. |
| Modificabilidade | Alta | Maximizar | Novas regras e mapeamentos precisam evoluir sem reescrever o modelo. |
| Simplicidade | Média | Priorizar | Não criar entidades, enums ou serviços para semântica não comprovada. |
| Testabilidade | Média | Satisfazer | Regras precisam ser exercitáveis de forma determinística em memória. |
| Segurança | Média | Satisfazer | Hashes e tokens não devem ser reduzidos a dados de apresentação ou expostos. |

## Alternativas consideradas

### Alternativa A — um agregado `Usuario` com todo o perfil e todos os currículos

Modelar usuário, todos os itens de perfil e todos os currículos como uma árvore
mutável de um único agregado. A propriedade indicada pelo DER ficaria simples,
mas qualquer alteração em um item reutilizável ou currículo exigiria carregar e
proteger uma unidade de consistência grande. A alternativa prejudica limites de
agregado, concorrência e evolução independente das versões de currículo.

### Alternativa B — agregados pequenos, com `Curriculo` proprietário de referências

Modelar `Usuario` e `Curriculo` como aggregate roots separados; modelar cada
item de perfil como entidade independente proprietária de `Usuario`; e fazer
`Curriculo` guardar referências tipadas aos itens selecionados. As associações
do DER não se tornam entidades de domínio sem atributos próprios. A propriedade
cruzada de referências é validada pelo caso de uso/porta de leitura apropriado,
enquanto `Curriculo` protege suas invariantes locais. Esta é a alternativa
recomendada.

### Alternativa C — espelhar o DER em entidades ORM e tabelas de associação

Criar modelos SQLAlchemy para todas as entidades e tratar as tabelas de junção
como objetos do domínio. Isso favorece um mapeamento imediato, mas viola a
separação obrigatória entre domínio e infraestrutura e dá às tabelas o papel de
modelo de negócio sem evidência de atributos ou comportamento próprios. É
inviável pelas restrições arquiteturais.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Correção | Alta | +1 | +2 | 0 | Média | Limites locais e encapsulamento de referências |
| Separação arquitetural | Alta | +2 | +2 | -2 | Alta | Regras de Clean Architecture e Code First |
| Modificabilidade | Alta | -1 | +2 | 0 | Alta | Itens reutilizáveis e versões de currículo no DER |
| Simplicidade | Média | 0 | +1 | -1 | Média | Evita árvore grande e entidades de junção sem comportamento |
| Testabilidade | Média | 0 | +2 | -1 | Alta | Objetos puros e invariantes locais em memória |
| Segurança | Média | 0 | +1 | -1 | Média | Value objects isolam dados sensíveis de transporte e ORM |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### Decisão recomendada nesta versão

Adotar a Alternativa B e implementar o domínio em módulos coesos, com a seguinte
direção inicial:

1. criar IDs UUID tipados como value objects (`UsuarioId`, `CurriculoId` e IDs
   dos itens de perfil) para evitar troca acidental de identidades distintas;
2. criar `Email`, `Nome`, `Periodo` e `HashSenha` como value objects imutáveis;
   `Periodo` aceita fim ausente e rejeita fim anterior ao início; `HashSenha`
   apenas encapsula um hash já produzido, sem escolher algoritmo no domínio;
3. criar `Usuario` como aggregate root de identidade e dados de conta, sem
   acoplar autenticação, sessão ou token de recuperação à primeira entrega;
4. criar `Curriculo` como aggregate root com proprietário obrigatório,
   título/versão e referências encapsuladas aos itens escolhidos;
5. criar `FormacaoAcademica`, `ExperienciaProfissional`, `ProjetoAcademico`,
   `Competencia`, `Idioma` e `Documento` como entidades de perfil com proprietário
   obrigatório. Elas não devem ser coleções internas de `Usuario` nem de
   `Curriculo`, pois são reutilizáveis entre versões;
6. representar as associações `CURRICULO_*` como coleções de referências
   tipadas dentro de `Curriculo`, não como entidades ou tabelas no domínio. Se
   ordem, texto customizado, visibilidade ou outra regra própria surgir, criar
   uma nova análise para promover a associação a entidade interna;
7. manter `Exportacao`, `SistemaExterno`, `IntegracaoLog`, `TokenResetSenha` e
   `Sessao` fora do primeiro corte de domínio. O DER os sinaliza, mas faltam
   regras suficientes para escolher aggregate roots, value objects e políticas
   corretas;
8. validar que uma referência pertence ao usuário do currículo no caso de uso
   que reúne os agregados. A aggregate root `Curriculo` deve validar apenas a
   ausência de duplicata e a consistência de suas próprias referências, sem
   carregar outros agregados ou infraestrutura.

### Impacto da revisão

Análise inicial; nenhum impacto de revisão.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Modificabilidade | maximized | Perfil e currículo evoluem sem transações de agregado excessivamente grandes | Itens de perfil são reutilizados por associações no DER |
| Simplicidade | prioritized | Apenas conceitos com invariantes observáveis entram no primeiro corte | Campos de vocabulário e fluxos não estão especificados |
| Correção | prioritized | Referências duplicadas e períodos cronologicamente inválidos são rejeitados perto do dado | Regras locais dedutíveis do modelo |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Separação arquitetural | Nenhum import de framework, ORM ou I/O no domínio | Entidades e value objects são objetos Python puros; mapeamento fica na infraestrutura |
| Testabilidade | Regras exercitáveis sem recursos externos | Construção e métodos de agregados são cobertos por testes unitários em memória |
| Segurança | Segredos não são tratados como DTO ou texto de apresentação | `HashSenha` encapsula valor já derivado; tokens e integrações aguardam política própria |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Modificabilidade | Um agregado de usuário grande força carregamento e conflitos desnecessários entre versões e itens | Alta | Desenvolvedores e usuários concorrentes |
| Separação arquitetural | ORM e tabelas se tornam o modelo de negócio e contaminam regras internas | Alta | Backend e manutenção futura |
| Correção | DTOs ou coleções mutáveis permitem estados inválidos e referências duplicadas | Alta | Usuários e equipe de qualidade |
| Segurança | Segredos podem atravessar camadas como strings sem intenção explícita | Média | Usuários e equipe de segurança |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Modificabilidade | Mais tipos de ID e referências explícitas | Simplicidade | Aceitável para impedir mistura de identidades e preservar limites |
| Separação arquitetural | Mapeamento ORM é adiado para uma etapa de infraestrutura | Time-to-value | Aceitável porque Code First exige mapeamentos fora do domínio |
| Correção | Validação de propriedade entre agregados ocorre no caso de uso, não no método local | Localidade da regra | Aceitável enquanto os agregados permanecem independentes |
| Simplicidade | Entidades de sessão, token, exportação e integração ficam sem implementação inicial | Cobertura funcional | Aceitável pela falta de políticas de negócio observáveis |

## Riscos e efeitos de segunda ordem

- Tratar todo campo textual do DER como enum pode congelar vocabulário de produto
  sem requisitos; usar strings validadas apenas estruturalmente até definição de
  uma linguagem ubíqua aprovada.
- Permitir remoção de itens referenciados sem política explícita pode deixar
  currículos inconsistentes; esse fluxo precisa de decisão antes de repositórios
  e exclusão lógica.
- A regra de que referência e currículo pertencem ao mesmo usuário atravessa
  agregados. Tentar resolvê-la carregando repositórios no domínio violaria as
  fronteiras; o caso de uso deve coordená-la por portas.
- `HashSenha` não implementa segurança por si só. Algoritmo, salt, comparação,
  rotação, expiração e bloqueio precisam de análise específica de segurança.
- As tabelas de associação podem ganhar ordenação ou customização. Caso isso
  ocorra, a decisão de tratá-las como referências deve ser reavaliada antes de
  migrations e contratos públicos.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Entidades e VOs são independentes da borda | Grafo de imports sem FastAPI, SQLAlchemy, Pydantic ou I/O | Revisão de imports e testes unitários no ambiente `.#backend` | Qualquer dependência externa no pacote `domain` |
| `Curriculo` preserva referências locais válidas | Testes de adição, remoção e duplicata para cada tipo de referência | Testes unitários determinísticos | Coleção pode ser alterada externamente ou aceita duplicata |
| Limites pequenos suportam o uso previsto | Um item de perfil pode ser compartilhado entre duas versões sem carregar usuário inteiro | Teste de domínio e revisão de casos de uso posteriores | Regra exige consistência transacional de toda a árvore do usuário |
| VOs cobrem invariantes atuais | Testes para e-mail, ID e período inválidos | Testes unitários | Requisitos ampliam formato, internacionalização ou calendário |
| Associações ainda não são entidades | Ausência de ordem, atributos ou ciclo de vida próprio nos requisitos | Revisão dos requisitos funcionais antes da infraestrutura | Novo atributo ou regra por inclusão no currículo |

## Handoffs e atividades posteriores

- `$backend-domain-orchestration-v2`: implementar os value objects, entidades,
  aggregate roots e testes unitários conforme a decisão, sem criar caso de uso,
  porta, ORM ou API.
- Nova análise de domínio/produto: definir vocabulários e transições de nível,
  status, layout e formato; política de remoção e ordenação/personalização das
  associações de currículo.
- Nova análise de segurança: definir credenciais, hash, bloqueio, sessão e
  recuperação de senha antes de implementar `TOKEN_RESET_SENHA` e `SESSAO`.
- Nova análise de integração: definir comportamento de exportação, sistemas
  externos e logs antes de modelar esses conceitos.
- Após estabilizar o domínio: analisar portas de repositório e mapeamentos
  SQLAlchemy/Alembic na infraestrutura Code First.

## Síntese

Recomenda-se iniciar o domínio com agregados pequenos e independentes:
`Usuario`, `Curriculo` e os itens reutilizáveis de perfil, apoiados por IDs
tipados e value objects de invariantes observáveis. `Curriculo` encapsula as
referências que compõem cada versão, enquanto a aplicação validará a propriedade
entre agregados. Essa direção respeita DDD, Clean Architecture e Code First sem
confundir o DER com o modelo ORM. As políticas que o diagrama não define devem
permanecer fora da implementação até que requisitos explícitos as tornem
decidíveis.
