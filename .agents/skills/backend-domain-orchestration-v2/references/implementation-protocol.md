# Protocolo do núcleo e testes unitários

Use somente após `valid`.

## Implementar

1. Mapeie critérios a regras, casos de uso, unidades e verificações.
2. Liste adapters, drivers, testes superiores e transversais como handoffs.
3. Mantenha dependências apontando para dentro e código livre de framework/transporte/persistência.
4. Expresse invariantes perto do estado e coordene portas sem duplicar regras.
5. Não implemente adapters nem preocupação transversal.
6. Confirme o `AGENTS.md` específico antes de editar.

## Testes permitidos

- Crie ou modifique somente testes unitários de domínio ou orquestração no escopo.
- Substitua todas as portas e recursos externos por mocks, stubs, spies ou fakes do teste.
- Cubra invariantes, transições, políticas, falhas e decisões de fluxo observáveis.
- Reuse runner existente; não crie infraestrutura global de teste.
- Não adicione nem altere contrato, integração, API, persistência, sistema, E2E ou não funcional.

## Verificar

Execute testes unitários afetados, lint, análise estática/typecheck e build do módulo. Suítes existentes de níveis superiores podem ser executadas para regressão, mas não modificadas.

Revise o diff: cada teste criado deve ser unitário; nenhuma camada externa ou preocupação transversal pode ter mudado. Preserve alterações preexistentes e relate apenas comandos executados.

## Relatar

Informe análise e versão, veredito, regras/casos de uso, unidades testadas, arquivos, verificações e handoffs para `$integration-system-testing-v1`. Diferencie teste criado de suíte apenas executada.
