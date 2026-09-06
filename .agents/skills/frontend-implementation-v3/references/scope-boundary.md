# Fronteira do frontend e dos testes unitários

Classifique cada tarefa como `functional-screen`, `unit-test`, `higher-level-test`, `excluded-cross-cutting` ou `inseparable`.

## `functional-screen`

Permite visualizar, informar, escolher ou acionar algo em um fluxo de negócio por uma tela: páginas, componentes, formulários, tabelas, filtros, navegação, estado local e consumo de contratos cliente existentes.

## `unit-test`

Exercita uma unidade de frontend isoladamente:

- um componente com filhos e serviços relevantes substituídos;
- hook, função, formatter, reducer, store local ou view model isolado;
- estados e interações locais observáveis da unidade;
- snapshot restrito à unidade quando essa for a convenção existente.

O teste pode usar DOM simulado e doubles. Não pode usar backend real, rede, navegação entre páginas, browser E2E, serviço externo ou composição de múltiplas camadas. O arquivo estar em `tests` ou usar um test runner não determina o nível.

## `higher-level-test`

Inclui integração entre componentes/camadas, contrato, API, sistema, aceitação, E2E, visual regression de jornada, performance, acessibilidade sistêmica, segurança e outros testes não funcionais. Encaminhe para `$integration-system-testing-v1`.

## `excluded-cross-cutting`

Exclua observabilidade, resiliência, segurança, identidade/acesso, infraestrutura cliente, políticas globais, i18n, performance, theming, design system e upgrades. Testar uma dessas preocupações em nível não unitário também pertence à skill de testes integrados.

## Distinções

- Testar isoladamente a validação local de um formulário é unitário; enviar o formulário ao backend é integração/E2E.
- Renderizar um componente com services mockados pode ser unitário; renderizar rota completa com providers reais tende a ser integração.
- Testar reducer isolado é unitário; testar fluxo entre store, router e API não é.
- Verificar um atributo ARIA da unidade pode integrar seu teste unitário funcional; uma auditoria de acessibilidade da página é não funcional.

## Escopo misto

- `functional-screen` e `unit-test`: permitido.
- Mistura separável: implemente somente os itens permitidos e registre handoffs.
- `inseparable`: interrompa e solicite decomposição.
- Somente itens excluídos: use `mismatch`.

Não declare implementada a parte de testes integrada ou superior.
