# Fronteira Cross-Cutting

Classifique cada objetivo, responsabilidade e arquivo como `observability`, `resilience`, `security`, `identity-access`, `unit-test`, `higher-level-test`, `business-functionality`, `environment-operation` ou `inseparable`.

## `observability`

- logs estruturados, eventos técnicos, níveis e schemas;
- métricas, dimensões e instrumentos;
- spans, traces e propagação de contexto;
- correlação, error reporting e auditoria técnica;
- redaction e controle de cardinalidade/custo da telemetria de código.

Não invente evento de negócio para instrumentar. Use eventos e fronteiras já definidos pela análise e pelo sistema.

## `resilience`

- timeout e orçamento temporal;
- retry, backoff e jitter;
- circuit breaker, bulkhead e isolamento;
- fallback e degradação aprovados;
- idempotência técnica, rate limiting e recuperação;
- política de falha em integrações e pontos de entrada.

Fallback que muda resultado do negócio exige decisão funcional; retry em operação não idempotente exige decisão explícita.

## `security`

- mitigação de ameaça e hardening definidos;
- sanitização de segurança, headers, CSP, CORS/CSRF quando aplicáveis;
- proteção de segredo, token e dado sensível;
- criptografia e uso de primitives já aprovadas;
- remediação direcionada de vulnerabilidade ou dependência.

Não projete criptografia própria nem faça upgrade amplo sob pretexto de segurança.

## `identity-access`

- autenticação, sessão e validação de identidade;
- enforcement de policy, guard, role, permission, RBAC ou ABAC;
- decisão sujeito–ação–recurso–contexto;
- propagação de identidade e negação consistente.

A matriz de autorização deve existir. Estado de negócio como “pedido faturado não pode ser cancelado” é domínio; “este ator não pode cancelar este pedido” é autorização.

## Testes

`unit-test` isola logger/enricher/redactor, policy evaluator, authorizer, guard, mecanismo de retry/circuit breaker com relógio/dependências substituídos, sanitizer ou outra unidade transversal. Não usa rede, collector, provedor de identidade, banco, broker, servidor ou framework iniciado.

`higher-level-test` inclui integração com collector/provider, teste de autorização por API, security scan, carga, chaos, recuperação e qualquer teste não funcional integrado. Encaminhe para `$integration-system-testing-v1`.

## Fora do escopo

`business-functionality` inclui tela, regra, fluxo, endpoint, persistência ou integração cujo resultado principal seja funcional. Tocar esses arquivos é permitido apenas para inserir o mecanismo transversal sem mudar sua semântica.

`environment-operation` inclui Nix, CI/CD, deploy, IaC, configuração live, provisionamento de collector/IdP, rotação de segredo e alteração de recurso remoto.

## Distinções

- Adicionar trace ao endpoint é observabilidade; criar o endpoint é adapter.
- Aplicar timeout ao client é resiliência; implementar a chamada funcional é driver.
- Guardar uma rota por policy é autorização; construir a tela é frontend.
- Redactar token em log é segurança/observabilidade; alterar o payload de negócio não é.
- Decorar um use case sem mudar o fluxo pode ser transversal; editar sua regra é orquestração.
- Validar authorizer isolado é unitário; validar acesso pela API é integração/não funcional.

## Escopo misto

Permita os quatro concerns e `unit-test`. Implemente a fatia separável e faça handoff do restante. Para `inseparable`, interrompa e solicite decisão/decomposição. Sem concern elegível, use `mismatch`.
