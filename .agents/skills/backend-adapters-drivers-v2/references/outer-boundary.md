# Fronteira das camadas externas e dos testes

Classifique cada item como `interface-adapter`, `framework-driver`, `unit-test`, `higher-level-test`, `inner-layer`, `frontend`, `excluded-cross-cutting` ou `inseparable`.

## Camadas permitidas

`interface-adapter` traduz entre interfaces externas e contratos internos: controllers, handlers, DTOs de transporte, serializers, presenters, validação estrutural, mapeamentos e implementações de gateways/repositories.

`framework-driver` realiza mecanismos externos: rotas, ORM, persistência, queries, migrations, filesystem, APIs externas, SDKs, mensageria, schedulers e bindings locais.

## `unit-test`

Exercita uma unidade externa isoladamente:

- controller/handler com caso de uso substituído;
- presenter, serializer ou mapper isolado;
- repository adapter com client/ORM substituído, sem banco real;
- wrapper de SDK ou gateway com dependência externa substituída;
- consumer com mensagem sintética e use case/broker substituídos.

Não inicie servidor, framework application context, banco, container, broker, filesystem real, rede ou outro processo. Teste de migration, contrato, endpoint real ou persistência real não é unitário.

## Fora do escopo

`higher-level-test` inclui contrato, integração, API, persistência, migration integrada, sistema, aceitação, E2E e não funcional. Encaminhe para `$integration-system-testing-v1`.

`inner-layer` inclui domínio, casos de uso, modelos independentes e portas pertencentes ao núcleo. Encaminhe para `$backend-domain-orchestration-v2`.

`frontend` inclui telas, componentes e estado cliente. `excluded-cross-cutting` inclui observabilidade, resiliência, segurança, identidade/acesso, cache, transações, middleware, interceptors e políticas globais.

## Distinções

- Controller com use case mockado pode ser unitário; endpoint por servidor real é API/integração.
- Mapper puro pode ser unitário; repository contra banco é integração.
- Gateway com SDK mockado pode ser unitário; sandbox externo é integração.
- Mapear erro para HTTP é adapter; criar a falha de negócio é domínio.
- Migration pode ser implementada aqui, mas sua execução integrada não é teste unitário.
- Configurar rota local é driver; iniciar framework para testá-la é integração.

## Escopo misto

Permita `interface-adapter`, `framework-driver` e `unit-test`. Implemente mistura separável e faça handoff do restante. Para `inseparable`, interrompa. Sem item externo elegível, use `mismatch`.
