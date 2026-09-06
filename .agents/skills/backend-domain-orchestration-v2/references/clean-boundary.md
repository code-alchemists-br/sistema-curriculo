# Fronteira das camadas internas e dos testes

Classifique cada item como `domain`, `use-case-orchestration`, `unit-test`, `higher-level-test`, `external-layer`, `excluded-cross-cutting` ou `inseparable`.

## Camadas permitidas

`domain` inclui entidades, value objects, aggregates, invariantes, políticas, serviços, falhas e fatos do negócio independentes de framework.

`use-case-orchestration` inclui use cases, interactors, application services, modelos independentes de transporte, sequência entre domínio e portas e definição de portas pertencentes ao núcleo.

## `unit-test`

Exercita uma unidade interna isoladamente:

- entidade, value object, aggregate, política ou serviço de domínio;
- use case/interactor como unidade, com todas as portas substituídas;
- funções e modelos internos puros;
- propriedades e invariantes da unidade, inclusive por teste parametrizado ou property-based.

Um fake em memória pode ser double quando pertence ao teste e substitui uma porta. Usar adapter produtivo, banco, ORM, filesystem, rede, fila, container ou framework iniciado transforma o teste em integração.

## Fora do escopo

`higher-level-test` inclui contrato, integração, API, persistência, sistema, E2E, aceitação, arquitetura e teste não funcional. Encaminhe para `$integration-system-testing-v1`.

`external-layer` inclui frontend, controllers, presenters, serializers, repositórios concretos, ORM, migrations, drivers, SDKs, configuração e composição.

`excluded-cross-cutting` inclui observabilidade, resiliência, segurança, identidade/acesso, cache, transações, middleware, interceptors e políticas globais.

## Distinções

- Testar aggregate puro é unitário; salvá-lo em banco é integração.
- Testar use case com repository mockado é unitário; usar repository concreto não é.
- Verificar a decisão de fluxo do use case é unitário; chamar endpoint HTTP é API/integração.
- Regra baseada no estado do negócio é domínio; regra por role ou permission é autorização.
- Domain event pode ser fato interno; dispatcher, broker e publicação são externos.

## Escopo misto

Permita `domain`, `use-case-orchestration` e `unit-test`. Implemente mistura separável e faça handoff do restante. Para `inseparable`, interrompa. Sem item interno elegível, use `mismatch`.
