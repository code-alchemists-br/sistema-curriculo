# Check de aderência ao frontend funcional

Confirme:

1. a responsabilidade pertence à superfície cliente;
2. a finalidade é uma funcionalidade de tela do negócio ou teste unitário de uma unidade dessa superfície;
3. qualquer teste solicitado está realmente isolado.

Inspecione análise, páginas, componentes, rotas, contratos cliente, testes, imports e `AGENTS.md`. Use somente leitura durante o gate.

## `valid`

Exija pelo menos dois sinais independentes, um semântico: capacidade de negócio na tela, unidade cliente existente, critério local observável ou teste com dependências substituídas.

Antes de escrever:

> Análise `<caminho>` (`<versão>`) validada para frontend funcional. Implementarei <fatia> e somente os testes unitários de <unidades>. Testes superiores e demais handoffs: <lista ou “nenhum”>.

## `ambiguous`

Use quando camada, finalidade ou isolamento do teste não estiver claro. Não altere arquivos e informe a evidência conflitante ou a informação ausente.

## `mismatch`

Use para backend, infraestrutura, preocupação transversal ou demanda composta apenas por teste integrado/sistêmico. Informe que nenhum arquivo foi alterado e encaminhe à skill adequada.

## Casos limítrofes

- Componente isolado com API mockada: pode ser unitário.
- Página com router, backend ou browser real: integração/E2E.
- Ocultar botão por permissão: autorização, mesmo com teste unitário.
- Dashboard operacional: observabilidade; painel de indicadores do negócio pode ser funcional.
- Pasta `frontend` não torna um teste E2E elegível para esta skill.
