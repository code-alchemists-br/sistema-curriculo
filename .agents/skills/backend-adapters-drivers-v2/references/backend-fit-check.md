# Check de aderência às camadas externas

Confirme:

1. a demanda pertence ao backend;
2. há contrato interno suficiente;
3. a responsabilidade é interface adapter ou framework/driver funcional;
4. não é frontend nem transversal;
5. qualquer teste a criar isola uma única unidade externa.

Inspecione análise, casos de uso, portas, adapters, drivers, imports, testes e `AGENTS.md`. Use somente leitura no gate.

## `valid`

Exija dois sinais independentes, um semântico: tradução de fronteira, implementação de porta existente, mecanismo externo funcional, ou teste com todas as fronteiras substituídas.

Antes de escrever:

> Análise `<caminho>` (`<versão>`) validada para adapters/drivers. Implementarei <responsabilidades> e somente testes unitários de <unidades>. Contratos usados: <lista>. Testes superiores e demais handoffs: <lista ou “nenhum”>.

## `ambiguous`

Use quando contrato, camada ou isolamento do teste não estiver claro. Não altere arquivos; informe lacuna ou conflito.

## `mismatch`

Use para frontend, núcleo, preocupação transversal ou demanda composta apenas por testes superiores. Informe que nenhum arquivo foi alterado e encaminhe à skill apropriada.

## Casos limítrofes

- Controller fino é adapter; regra de negócio no controller pertence ao núcleo.
- Repository concreto é externo; a porta e sua semântica pertencem ao núcleo.
- Controller mockado é unidade; controller via HTTP real é integração.
- Repository com ORM mockado é unidade; com banco real é integração.
- Consumer isolado é unidade; consumer conectado ao broker é integração.
- Pasta `infrastructure` não torna um teste integrado elegível nesta skill.
