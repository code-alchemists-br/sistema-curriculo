---
name: backend-adapters-drivers-v2
description: "Implementa interface adapters e frameworks and drivers funcionais do backend e, opcionalmente, somente seus testes unitários, a partir de uma análise de decisão v4. Valida AGENTS.md, versão, contratos internos e fronteiras; exclui testes de integração ou superiores, frontend, domínio, orquestração, observabilidade, resiliência, segurança, autorização e outras preocupações transversais. Use somente por invocação explícita com a referência da análise e instruções adicionais opcionais."
---

# Backend Adapters and Drivers v2

Transforme uma análise aprovada somente em adapters e drivers que conectem contratos internos existentes ao mundo externo e, quando pertinente, em testes unitários dessas unidades externas. Adaptar não autoriza decidir regras de negócio.

## Entrada e gate

Exija uma referência inequívoca a uma análise e aceite instruções adicionais opcionais. Sem referência exata e legível, não altere arquivos.

Antes de qualquer escrita:

1. Leia os `AGENTS.md` aplicáveis, da raiz aos possíveis alvos.
2. Leia [references/analysis-input-contract.md](references/analysis-input-contract.md).
3. Leia [references/outer-boundary.md](references/outer-boundary.md) e classifique responsabilidades e testes.
4. Leia [references/backend-fit-check.md](references/backend-fit-check.md) e determine `valid`, `ambiguous` ou `mismatch`.
5. Somente com `valid`, leia [references/implementation-protocol.md](references/implementation-protocol.md), implemente e verifique.

Até concluir o gate, permita somente inspeções e comandos não mutáveis. Pasta, linguagem ou framework não provam a camada.

## Escopo permitido

- controllers, endpoints, resolvers, handlers, consumers e comandos CLI;
- DTOs de transporte, serializers, presenters e mapeamentos de fronteira;
- implementações concretas de portas existentes, repositórios, gateways e clientes;
- ORM, persistência, queries, migrations, mensageria, filesystem, rotas e bindings locais;
- testes unitários que isolem uma unidade de adapter ou driver pertencente ao escopo;
- alteração composta somente por testes unitários de uma unidade externa elegível.

Um teste unitário deve substituir caso de uso, porta, ORM/driver, SDK, rede, banco, filesystem, fila, relógio e framework por doubles conforme a fronteira da unidade. Não inicie servidor, application context, container ou processo externo.

## Escopo proibido

- testes de integração, contrato, API, persistência real, migration integrada, sistema, aceitação, E2E ou não funcionais;
- configuração global de runner ou harness de testes;
- frontend, domínio, casos de uso, orquestração ou novas portas internas;
- observabilidade, resiliência, segurança, autenticação, autorização e infraestrutura transversal;
- política global, upgrade ou refatoração arquitetural ampla.

Encaminhe testes acima da unidade para `$integration-system-testing-v1`. Executar suítes existentes de outro nível como verificação é permitido; criar ou modificar seus testes não é.

## Pré-condição e escopo misto

Casos de uso, modelos e portas devem existir. Se faltarem, não os invente nem esconda regras no adapter; faça handoff para `$backend-domain-orchestration-v2`.

Implemente somente adapters/drivers e seus testes unitários quando separáveis. Registre núcleo, frontend, testes superiores e transversais como handoffs. Se forem inseparáveis, solicite decomposição. Sem responsabilidade externa elegível, use `mismatch`.

Reutilize mecanismos transversais existentes sem mudar sua política. Não altere a análise; solicite revisão com `$decision-analysis-v4` quando necessário.

## Aprovação e comunicação

A invocação explícita com `status: proposed` aprova somente a versão referenciada e sua fatia elegível.

Antes da escrita, informe análise, evidências, adapters/drivers, unidades que poderão ser testadas, contratos internos e handoffs. No final, inclua integrações entregues, testes unitários, arquivos, verificações e itens excluídos.
