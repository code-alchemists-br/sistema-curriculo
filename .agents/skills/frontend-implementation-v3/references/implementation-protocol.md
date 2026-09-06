# Protocolo de implementação funcional

Use somente após `valid`.

## Implementar

1. Mapeie critérios a comportamento, unidades, arquivos e verificações.
2. Liste testes superiores e preocupações excluídas como handoffs.
3. Reutilize componentes, tokens, padrões e contratos existentes.
4. Limite a lógica à apresentação e interação do caso de uso.
5. Não adicione observabilidade, resiliência, segurança, autorização, backend ou infraestrutura global.
6. Confirme o `AGENTS.md` específico antes de editar.

## Testes permitidos

- Crie ou modifique somente testes unitários das unidades frontend no escopo.
- Substitua API, storage, relógio, router e outros colaboradores por doubles quando forem externos à unidade.
- Teste comportamento observável da unidade, evitando detalhes frágeis de implementação.
- Reuse runner e configuração existentes; não crie harness ou política global.
- Não adicione nem altere integração, contrato, API, sistema, E2E ou teste não funcional.

## Verificar

Execute os testes unitários afetados, lint, typecheck e build quando relevantes. Suítes existentes de níveis superiores podem ser executadas para regressão, mas não modificadas.

Inspecione o diff e confirme que cada teste criado é unitário, nenhum arquivo de backend ou infraestrutura mudou e nenhuma preocupação transversal foi adicionada. Preserve mudanças preexistentes e relate somente comandos realmente executados.

## Relatar

Informe análise e versão, veredito, funcionalidade, unidades testadas, arquivos, verificações e handoffs para `$integration-system-testing-v1`. Diferencie teste criado de suíte apenas executada.
