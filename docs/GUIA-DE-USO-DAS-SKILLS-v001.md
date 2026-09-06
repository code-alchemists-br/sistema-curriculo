# Guia resumido das skills

As skills deste projeto são usadas por invocação explícita. Escreva o nome da skill com `$` e forneça os dados exigidos.

## Fluxo recomendado

1. Analise a demanda com `$decision-analysis-v4`.
2. Revise a análise, se necessário, usando novamente `$decision-analysis-v4` e informando o arquivo anterior.
3. Passe o caminho exato da análise aprovada para a skill de implementação apropriada.

As skills de implementação validam o contexto e obedecem à hierarquia de `AGENTS.md` antes de alterar arquivos. Use sempre as versões mais recentes listadas abaixo.

## Skills

### `$decision-analysis-v4`

**Serve para:** esclarecer e delimitar uma demanda, comparar alternativas, registrar a decisão, os benefícios priorizados, as perdas e os arquivos examinados. Cria uma análise Markdown versionada dentro de `prompts`.

**Uso:**

```text
$decision-analysis-v4 Analise a necessidade de permitir cancelamento de pedidos.
```

Para revisar:

```text
$decision-analysis-v4 Revise prompts/backend/20260905-cancelamento-v001.md considerando que pedidos faturados não podem ser cancelados.
```

**Não faz:** implementação de código ou configuração.

### `$frontend-implementation-v3`

**Serve para:** implementar telas e interações funcionais ligadas ao negócio, além de testes exclusivamente unitários de frontend.

**Uso:**

```text
$frontend-implementation-v3 Implemente a análise prompts/frontend/20260905-cancelamento-v001.md. Preserve os componentes visuais existentes.
```

**Não faz:** backend, testes integrados, observabilidade, resiliência, segurança, autenticação ou autorização.

### `$backend-domain-orchestration-v2`

**Serve para:** implementar entidades, regras de domínio, casos de uso, portas internas e orquestração, além de seus testes exclusivamente unitários.

**Uso:**

```text
$backend-domain-orchestration-v2 Implemente prompts/backend/20260905-cancelamento-v001.md.
```

**Não faz:** frontend, adapters, drivers, testes integrados ou preocupações Cross-Cutting.

### `$backend-adapters-drivers-v2`

**Serve para:** implementar controllers, endpoints, persistência, mensageria, clientes externos e demais adapters/drivers, usando contratos internos existentes. Pode criar somente testes unitários dessas unidades.

**Uso:**

```text
$backend-adapters-drivers-v2 Implemente prompts/backend/20260905-persistencia-cancelamento-v001.md.
```

**Não faz:** regras de domínio, casos de uso, frontend, testes integrados ou preocupações Cross-Cutting.

### `$nix-environment-implementation-v1`

**Serve para:** implementar ou modificar exclusivamente artefatos Nix, como flakes, derivations, packages, overlays, dev shells e módulos NixOS/Home Manager.

**Uso:**

```text
$nix-environment-implementation-v1 Implemente prompts/ambiente/20260905-dev-shell-v001.md.
```

**Não faz:** código da aplicação, Docker, CI/CD, Terraform, Kubernetes, scripts genéricos ou ativação do ambiente no host.

### `$integration-system-testing-v1`

**Serve para:** implementar testes de integração, contrato, API, sistema, aceitação, E2E e testes não funcionais.

**Uso:**

```text
$integration-system-testing-v1 Implemente os testes definidos em prompts/testes/20260905-cancelamento-v001.md.
```

**Não faz:** testes unitários, correções no produto, funcionalidade, deploy ou infraestrutura de produção.

### `$cross-cutting-implementation-v1`

**Serve para:** avaliar ou implementar observabilidade, logging, métricas, tracing, resiliência, segurança, autenticação e autorização. Pode criar somente testes unitários da própria preocupação transversal.

**Uso:**

```text
$cross-cutting-implementation-v1 Implemente prompts/backend/20260905-telemetria-cancelamento-v001.md.
```

**Não faz:** funcionalidade de negócio, telas, regras de domínio, testes integrados, ambientes ou operações externas.

## Regra prática

Se a análise misturar áreas, não peça que uma única skill implemente tudo. Divida a demanda ou execute as skills adequadas separadamente, sempre usando a análise correspondente como referência.
