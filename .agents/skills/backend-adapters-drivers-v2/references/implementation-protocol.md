# Protocolo das camadas externas e testes unitários

Use somente após `valid`.

## Implementar

1. Mapeie critérios a adapters, drivers, unidades e verificações.
2. Liste núcleo, frontend, testes superiores e transversais como handoffs.
3. Preserve contratos internos e mantenha controllers/handlers finos.
4. Restrinja ORM, migrations, rotas, bindings e integrações à fatia funcional.
5. Não adicione regra de negócio nem política transversal.
6. Confirme o `AGENTS.md` específico antes de editar.

## Testes permitidos

- Crie ou modifique somente testes unitários de adapters/drivers no escopo.
- Substitua use cases, portas, ORM, SDKs, rede, filesystem, filas e framework por doubles.
- Cubra tradução, mapeamento, delegação e representação observáveis da unidade.
- Reuse runner existente; não crie infraestrutura global de teste.
- Não adicione nem altere contrato, integração, API, persistência real, sistema, E2E ou não funcional.

## Verificar

Execute testes unitários afetados, lint, análise estática/typecheck e build. Suítes existentes de níveis superiores podem ser executadas para regressão, mas não modificadas. Migration pode ser validada por mecanismo existente, sem criar teste integrado nesta skill.

Revise o diff: cada teste criado deve ser unitário; nenhum núcleo, frontend ou preocupação transversal pode ter mudado. Preserve alterações preexistentes e relate apenas comandos executados.

## Relatar

Informe análise e versão, veredito, adapters/drivers, contratos, unidades testadas, arquivos, verificações e handoffs para `$integration-system-testing-v1` e `$backend-domain-orchestration-v2`. Diferencie teste criado de suíte apenas executada.
