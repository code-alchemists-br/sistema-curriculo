# Check de aderência ao núcleo do backend

Confirme:

1. a demanda pertence ao backend;
2. a responsabilidade é domínio ou orquestração;
3. não é preocupação transversal;
4. qualquer teste a criar isola uma unidade interna.

Inspecione análise, módulos, dependências, imports, portas, testes e `AGENTS.md`. Use somente leitura no gate.

## `valid`

Exija dois sinais independentes, um semântico: regra/invariante, caso de uso independente, dependências apontando para dentro, ou teste com todas as fronteiras substituídas.

Antes de escrever:

> Análise `<caminho>` (`<versão>`) validada para o núcleo do backend. Implementarei <responsabilidades> e somente testes unitários de <unidades>. Testes superiores e demais handoffs: <lista ou “nenhum”>.

## `ambiguous`

Use quando não for possível separar núcleo, detalhe externo ou nível do teste. Não altere arquivos; informe lacuna ou conflito.

## `mismatch`

Use para frontend, adapters/drivers, preocupação transversal ou demanda composta apenas por testes superiores. Informe que nenhum arquivo foi alterado e encaminhe à skill apropriada.

## Casos limítrofes

- Interface de repository pode ser porta interna; sua implementação é externa.
- DTO independente de transporte pode ser interno; request HTTP é adapter.
- Handler puro de comando pode ser use case; handler web ou de fila é adapter.
- Use case com doubles é unitário; use case com banco ou broker é integração.
- Pasta `application` ou nome `service` não determina a camada.
