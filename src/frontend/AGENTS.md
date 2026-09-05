# Frontend — Regras para agentes

Estas instruções se aplicam a todo o conteúdo de `src/frontend` e complementam
o `AGENTS.md` da raiz. Em caso de conflito, a regra mais restritiva DEVE ser
seguida.

## Níveis de instrução

- `[CRITICAL]` — violar esta regra torna a solução inválida.
- `[REQUIRED]` — esta regra DEVE ser cumprida.
- `[FORBIDDEN]` — esta prática NÃO DEVE ser utilizada.
- `[PREFERRED]` — adote como padrão; desvios exigem justificativa técnica.
- `[CONSIDER]` — avalie a aplicação conforme o contexto.

# Architecture Rules

## CRITICAL — Feature-Sliced Design

**O frontend DEVE ser modular, orientado a funcionalidades e organizado pelas
camadas do Feature-Sliced Design (FSD).**

[CRITICAL] Toda mudança ou adição de código DEVE preservar os limites entre as
camadas, slices e segmentos definidos neste documento.

[REQUIRED] O código da aplicação DEVE ser organizado nas seguintes camadas, da
mais alta para a mais baixa:

```text
app → pages → widgets → features → entities → shared
```

[REQUIRED] Uma camada somente DEVE importar módulos de camadas posicionadas
abaixo dela nessa hierarquia.

[FORBIDDEN] Uma camada inferior NÃO DEVE importar uma camada superior.

[FORBIDDEN] Slices distintos da mesma camada NÃO DEVEM importar diretamente uns
dos outros.

[REQUIRED] Cada slice DEVE expor uma API pública explícita. Consumidores externos
DEVEM importar por essa API pública e NÃO DEVEM acessar a estrutura interna do
slice.

[REQUIRED] Ciclos de dependência NÃO DEVEM existir.

## Responsabilidades das camadas

- **App:** inicialização, configuração global, roteamento, providers, estilos
  globais e composição das dependências da aplicação.
- **Pages:** composição de páginas associadas às rotas e aos casos de navegação.
- **Widgets:** grandes blocos autônomos de interface que compõem páginas e podem
  reunir múltiplas features e entities.
- **Features:** ações e fluxos que entregam valor ao usuário, como autenticar,
  criar currículo, exportar currículo ou classificar uma associação.
- **Entities:** conceitos de negócio usados pela interface, como estudante,
  currículo, vaga e associação currículo–vaga.
- **Shared:** recursos genéricos sem conhecimento das regras ou dos termos
  específicos do domínio, como UI básica, cliente HTTP, configuração e funções
  utilitárias.

[REQUIRED] Código DEVE ser colocado na camada mais baixa que ainda represente
corretamente sua responsabilidade e seu nível de conhecimento.

[FORBIDDEN] `shared` NÃO DEVE conhecer features, entities, páginas, regras ou
vocabulário específico do domínio deste projeto.

[FORBIDDEN] `pages` e `widgets` NÃO DEVEM concentrar regras de negócio. Eles
DEVEM atuar principalmente como composição e apresentação.

[PREFERRED] Uma funcionalidade usada por apenas uma página deve permanecer
local à página até que exista uma necessidade concreta de reutilização ou uma
fronteira de negócio que justifique promovê-la a `features`.

## Estrutura de slices e segmentos

[PREFERRED] Quando aplicável, organize cada slice utilizando segmentos com
responsabilidades explícitas:

- `ui` — componentes visuais do slice;
- `model` — estado, regras, seletores e comportamento da interface;
- `api` — operações remotas específicas do slice;
- `lib` — funções internas de apoio;
- `config` — configuração específica do slice;
- `index` — API pública do slice.

[FORBIDDEN] Segmentos genéricos como `components`, `utils`, `helpers` ou `misc`
NÃO DEVEM ser criados quando ocultarem a finalidade real do código.

[REQUIRED] A API pública DEVE expor somente o necessário para os consumidores e
DEVE preservar os detalhes internos do slice.

[FORBIDDEN] Arquivos agregadores globais que reexportem toda a aplicação NÃO
DEVEM ser usados.

# Regras de domínio e dados

## CRITICAL — Separação entre API, domínio e interface

[CRITICAL] Respostas externas, DTOs e detalhes de transporte NÃO DEVEM se tornar
automaticamente modelos internos da interface.

[REQUIRED] Dados recebidos da API DEVEM ser validados e convertidos na fronteira
para os modelos utilizados pelo frontend quando os formatos ou significados
forem diferentes.

[REQUIRED] Regras relevantes para a experiência da interface DEVEM permanecer
em `model` da feature ou entity apropriada, nunca em componentes puramente
visuais.

[CRITICAL] Validação no frontend NÃO substitui validação, autorização ou
proteção de invariantes no backend. O frontend DEVE tratar o backend como fonte
de verdade para segurança e persistência.

[FORBIDDEN] Componentes de UI NÃO DEVEM realizar chamadas HTTP diretamente.

[REQUIRED] Integrações remotas DEVEM ser acessadas por funções ou serviços com
contratos explícitos e respostas tipadas.

[REQUIRED] Erros, timeouts, indisponibilidade e respostas inválidas DEVEM ser
tratados de modo controlado e apresentados ao usuário em linguagem
compreensível, preservando dados locais sempre que possível.

## Estado

[PREFERRED] Estado DEVE permanecer local ao componente ou slice que o utiliza.

[FORBIDDEN] Estado NÃO DEVE ser globalizado apenas para antecipar reutilização
futura.

[REQUIRED] Estado remoto, estado de formulário, estado de navegação e estado
visual DEVEM ser tratados conforme seus ciclos de vida distintos.

[FORBIDDEN] Dados que possam ser derivados de outro estado NÃO DEVEM ser
armazenados como uma segunda fonte de verdade.

[REQUIRED] Efeitos colaterais DEVEM permanecer explícitos, isolados e
controláveis em testes.

# Componentes e experiência do usuário

## CRITICAL — Acessibilidade e responsividade

[CRITICAL] Toda interface nova ou alterada DEVE ser utilizável por teclado,
possuir semântica adequada e apresentar campos, estados e erros de forma
compreensível.

[REQUIRED] Elementos HTML semânticos DEVEM ser preferidos. ARIA DEVE ser usada
quando a semântica nativa não for suficiente, e NÃO DEVE substituir elementos
nativos apropriados.

[REQUIRED] Campos DEVEM possuir identificação acessível; mensagens de erro
DEVEM estar associadas aos respectivos campos; mudanças relevantes de estado
DEVEM ser comunicadas de forma acessível.

[REQUIRED] A navegação por foco DEVE permanecer previsível, inclusive em
diálogos, menus e fluxos com conteúdo dinâmico.

[CRITICAL] Os fluxos principais DEVEM funcionar em computadores e dispositivos
móveis, sem perda de funcionalidade.

[PREFERRED] Componentes visuais devem ser pequenos, coesos, previsíveis e
componíveis.

[REQUIRED] Estados de carregamento, vazio, sucesso, erro e ausência de permissão
DEVEM ser considerados quando aplicáveis.

# Módulos opcionais e extensibilidade

[CRITICAL] O fluxo principal de criação, edição, visualização e exportação de
currículos DEVE funcionar sem qualquer módulo de inteligência artificial.

[REQUIRED] Assistência de descrição e revisão guiada DEVEM depender de contratos
explícitos que permitam adicionar ou substituir implementações sem alterar o
fluxo principal.

[PREFERRED] Integrações opcionais devem ser conectadas por Adapter, Strategy ou
outro pattern que expresse claramente a substituição da implementação.

[FORBIDDEN] Componentes visuais NÃO DEVEM depender diretamente de SDKs de
inteligência artificial ou de outros fornecedores externos.

# Design Patterns e decisões arquiteturais

[REQUIRED] Design Patterns ou outros designs arquiteturais DEVEM ser utilizados
quando resolverem concretamente um problema de design.

[REQUIRED] A escolha DEVE preservar baixo acoplamento, alta coesão,
testabilidade, acessibilidade e clareza das fronteiras arquiteturais.

[REQUIRED] Ao introduzir um pattern ou uma decisão arquitetural relevante,
documente o problema resolvido, a razão da escolha e suas consequências no
local apropriado do projeto.

[CONSIDER] Use Adapter para integrações externas, Strategy para comportamentos
substituíveis, Factory para construções complexas e Facade para simplificar uma
API interna extensa, quando o contexto justificar.

[FORBIDDEN] NEVER introduza abstrações ou patterns para necessidades apenas
hipotéticas. A complexidade adicionada DEVE ter benefício demonstrável para o
problema atual.

# Qualidade e testes

[REQUIRED] Toda mudança de comportamento DEVE incluir testes unitários dos
modelos, transformações, validações, estados e componentes afetados.

[REQUIRED] Testes DEVEM validar comportamento observável pelo usuário e contratos
públicos, evitando dependência excessiva de detalhes internos de implementação.

[REQUIRED] Fluxos críticos de autenticação, cadastro, criação e edição de
currículos, exportação, busca de vagas e associações DEVEM possuir cobertura no
nível apropriado ao risco.

[REQUIRED] Testes de acessibilidade e responsividade DEVEM ser incluídos nas
verificações aplicáveis.

[REQUIRED] Testes DEVEM respeitar os ambientes Nix definidos no `AGENTS.md` da
raiz: testes unitários do frontend rodam no ambiente `frontend`; testes de
integração ou de nível superior rodam no ambiente `tests`.

[PREFERRED] Testes unitários devem ser rápidos, determinísticos e independentes
de rede, relógio e serviços externos.

# Documentação

[REQUIRED] Toda função e classe, inclusive DTOs, DEVE possuir docstring ou
documentação equivalente que explique **o que faz**, **como faz** e **qual
finalidade atende**, conforme determinado pelo `AGENTS.md` da raiz.

[REQUIRED] A documentação DEVE refletir o comportamento atual e DEVE ser
atualizada junto com qualquer alteração correspondente no código.

# Terminologia

Os termos abaixo têm significado preciso e DEVEM ser usados consistentemente:

- **Layer:** nível arquitetural do FSD com regras próprias de dependência.
- **Slice:** módulo coeso organizado por domínio, funcionalidade ou finalidade
  dentro de uma layer.
- **Segment:** subdivisão técnica de um slice, como `ui`, `model` ou `api`.
- **Public API:** ponto explícito pelo qual consumidores acessam um slice.
- **Feature:** ação ou fluxo que entrega valor reconhecível ao usuário.
- **Entity:** representação de um conceito de negócio relevante para a
  interface.
- **Widget:** bloco autônomo e significativo que compõe uma página.
- **Page:** composição da interface associada a uma rota ou etapa de navegação.
- **DTO:** estrutura que representa dados transferidos por uma fronteira externa.
- **UI state:** estado transitório que controla a apresentação e a interação.
- **Server state:** dado cuja fonte de verdade pertence ao backend.
