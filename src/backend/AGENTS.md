# Backend — Regras para agentes

Estas instruções se aplicam a todo o conteúdo de `src/backend` e complementam
o `AGENTS.md` da raiz. Em caso de conflito, a regra mais restritiva DEVE ser
seguida.

## Níveis de instrução

- `[CRITICAL]` — violar esta regra torna a solução inválida.
- `[REQUIRED]` — esta regra DEVE ser cumprida.
- `[FORBIDDEN]` — esta prática NÃO DEVE ser utilizada.
- `[PREFERRED]` — adote como padrão; desvios exigem justificativa técnica.
- `[CONSIDER]` — avalie a aplicação conforme o contexto.

# Architecture Rules

## CRITICAL — Clean Architecture

**As dependências DEVE apontar para dentro, em direção ao domínio.**

[CRITICAL] Toda mudança ou adição de código DEVE respeitar os princípios e as
práticas da **Clean Architecture**.

[CRITICAL] O domínio DEVE permanecer independente de frameworks, banco de
dados, interface web, mecanismos de serialização e serviços externos.

[REQUIRED] Organize as responsabilidades segundo os limites abaixo, ainda que
os nomes concretos dos diretórios sejam adaptados à linguagem e ao framework:

- **Domain:** entidades, value objects, agregados, eventos, serviços e regras
  de negócio.
- **Application:** casos de uso, portas, contratos e orquestração do fluxo da
  aplicação.
- **Adapters/Infrastructure:** persistência, clientes externos, mensageria e
  implementações das portas.
- **Interface/API:** transporte, autenticação/autorização de entrada,
  desserialização, validação de formato e composição da resposta.

[FORBIDDEN] Domain NÃO DEVE depender de Application, Infrastructure, API,
frameworks ou detalhes externos.

[FORBIDDEN] Application NÃO DEVE depender de Infrastructure nem da API.

[FORBIDDEN] Controllers, handlers de transporte, repositórios e adaptadores
NÃO DEVE conter regras de negócio.

[REQUIRED] Dependências externas DEVE ser acessadas por abstrações definidas na
camada interna que necessita delas e implementadas por adaptadores externos.

[REQUIRED] A composição e a injeção das dependências DEVE ocorrer na camada
mais externa da aplicação.

## CRITICAL — Domain-Driven Design

[CRITICAL] Toda mudança ou adição de código DEVE seguir as práticas de
**Domain-Driven Design (DDD)**.

[REQUIRED] Código, testes e documentação DEVE utilizar a linguagem ubíqua do
domínio de forma consistente com os requisitos do projeto.

[REQUIRED] Regras e invariantes de negócio DEVE ser protegidas pelo modelo de
domínio, no ponto mais próximo dos dados e comportamentos aos quais pertencem.

[REQUIRED] Agregados DEVE definir limites claros de consistência, e alterações
internas DEVE ocorrer por meio de sua raiz.

[PREFERRED] Entidades e value objects devem permanecer válidos desde sua
criação. Use fábricas quando a construção direta não expressar adequadamente
as invariantes.

[PREFERRED] Value objects devem ser imutáveis e comparados pelo seu valor.

[CONSIDER] Use um **Domain Service** quando uma regra de domínio não pertencer
naturalmente a uma única entidade ou value object.

[CONSIDER] Use eventos de domínio para representar fatos relevantes já
ocorridos e desacoplar consequências entre partes do domínio.

[FORBIDDEN] DTOs NÃO DEVE substituir entidades ou value objects no domínio.

## Design Patterns e decisões arquiteturais

[REQUIRED] Design Patterns ou outros designs arquiteturais DEVE ser utilizados
quando forem aplicáveis e resolverem concretamente um problema de design.

[REQUIRED] A escolha DEVE preservar baixo acoplamento, alta coesão,
testabilidade e clareza das fronteiras arquiteturais.

[REQUIRED] Ao introduzir um pattern ou uma decisão arquitetural relevante,
documente o problema resolvido, a razão da escolha e suas consequências no
local apropriado do projeto.

[PREFERRED] Prefira padrões compatíveis com as fronteiras da aplicação, como
Repository, Factory, Strategy, Specification, Adapter e Dependency Injection,
quando o problema justificar seu uso.

[FORBIDDEN] NEVER introduza abstrações ou padrões apenas para antecipar uma
necessidade hipotética. Patterns NÃO DEVE adicionar complexidade sem benefício
demonstrável para o caso atual.

## Fluxo de entrada e saída

[REQUIRED] Entradas externas DEVE ser convertidas em DTOs ou comandos antes de
invocar um caso de uso.

[REQUIRED] Formato, tipo e campos obrigatórios da entrada DEVE ser validados na
fronteira; invariantes e regras de negócio DEVE ser validadas pelo domínio.

[FORBIDDEN] NEVER exponha entidades de domínio diretamente pela API.

[FORBIDDEN] NEVER acesse banco de dados, sistema de arquivos ou API externa
diretamente a partir de controllers ou casos de uso.

[PREFERRED] Casos de uso devem representar uma intenção do usuário e possuir
uma única responsabilidade de orquestração.

## Qualidade e testes

[REQUIRED] Cada mudança de comportamento DEVE incluir testes unitários para as
regras, invariantes e casos de uso afetados.

[REQUIRED] Testes DEVE respeitar as regras de ambientes Nix definidas no
`AGENTS.md` da raiz: testes unitários do backend rodam no ambiente `backend`, e
testes de integração ou de nível superior rodam no ambiente `tests`.

[REQUIRED] Testes de domínio DEVE ser independentes de banco de dados, rede,
relógio do sistema e framework. Essas dependências devem ser controladas por
portas ou substitutos de teste.

[PREFERRED] Nomeie os testes de modo que expressem o comportamento e o resultado
esperado, com atenção especial às invariantes do domínio.

## Documentação

[REQUIRED] Toda função e classe, inclusive DTOs, DEVE possuir docstring ou
documentação equivalente que explique **o que faz**, **como faz** e **qual
finalidade atende**, conforme determinado pelo `AGENTS.md` da raiz.

[REQUIRED] A documentação DEVE refletir o comportamento atual e DEVE ser
atualizada junto com qualquer alteração correspondente no código.

## Terminologia

Os termos abaixo têm significado preciso e DEVE ser usados consistentemente:

- **Entity:** objeto de domínio definido por identidade e ciclo de vida.
- **Value Object:** objeto imutável definido por seus valores e sem identidade
  própria.
- **Aggregate:** limite de consistência formado por objetos de domínio.
- **Aggregate Root:** única porta de entrada para alterações em um agregado.
- **Use Case:** orquestração de uma intenção no nível da aplicação.
- **Port:** abstração que define uma fronteira necessária pela camada interna.
- **Adapter:** implementação que conecta uma porta a uma tecnologia externa.
- **Repository:** abstração para recuperar e persistir agregados sem expor
  detalhes de armazenamento.
- **Domain Service:** comportamento de domínio que não pertence naturalmente a
  uma única entidade ou value object.
- **DTO:** estrutura de transferência de dados sem comportamento de domínio.
