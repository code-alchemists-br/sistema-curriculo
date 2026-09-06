---
name: backend-domain-orchestration-v2
description: "Implementa regras de domínio e orquestração de casos de uso no núcleo de um backend em Clean Architecture e, opcionalmente, somente seus testes unitários, a partir de uma análise de decisão v4. Valida AGENTS.md, versão e fronteiras; exclui testes de integração ou superiores, frontend, adapters, drivers, observabilidade, resiliência, segurança, autorização e outras preocupações transversais. Use somente por invocação explícita com a referência da análise e instruções adicionais opcionais."
---

# Backend Domain and Orchestration v2

Transforme uma análise aprovada somente em comportamento de domínio ou orquestração de casos de uso e, quando pertinente, em testes unitários dessas mesmas unidades internas.

## Entrada e gate

Exija uma referência inequívoca a uma análise e aceite instruções adicionais opcionais. Sem referência exata e legível, não altere arquivos.

Antes de qualquer escrita:

1. Leia os `AGENTS.md` aplicáveis, da raiz aos possíveis alvos.
2. Leia [references/analysis-input-contract.md](references/analysis-input-contract.md).
3. Leia [references/clean-boundary.md](references/clean-boundary.md) e classifique responsabilidades e testes.
4. Leia [references/backend-fit-check.md](references/backend-fit-check.md) e determine `valid`, `ambiguous` ou `mismatch`.
5. Somente com `valid`, leia [references/implementation-protocol.md](references/implementation-protocol.md), implemente e verifique.

Até concluir o gate, permita somente inspeções e comandos não mutáveis. Classifique por responsabilidade e dependências, não por nomes de pasta ou classe.

## Escopo permitido

- entidades, value objects, aggregates, invariantes, políticas e serviços de domínio;
- falhas, resultados e fatos do negócio;
- casos de uso, interactors e application services;
- modelos de entrada/saída independentes de transporte e portas pertencentes ao núcleo;
- testes unitários das unidades acima;
- alteração composta somente por testes unitários de uma unidade interna elegível.

Um teste de use case continua unitário somente quando o use case é a unidade sob teste e todas as portas, relógio, geradores e demais dependências externas são doubles. Não use banco, rede, filesystem, fila, container, framework iniciado ou adapter real.

## Escopo proibido

- testes de integração, contrato, API, persistência, sistema, aceitação, E2E, arquitetura ou não funcionais;
- configuração global de runner ou harness de testes;
- frontend, interface adapters, frameworks and drivers;
- observabilidade, resiliência, segurança, autenticação, autorização e infraestrutura transversal;
- código externo para satisfazer uma porta interna.

Encaminhe testes acima da unidade para `$integration-system-testing-v1`. Executar suítes existentes de outro nível como verificação é permitido; criar ou modificar seus testes não é.

## Escopo misto

Implemente somente domínio, orquestração e seus testes unitários quando separáveis. Registre adapters, drivers, testes superiores e preocupações transversais como handoffs. Se forem inseparáveis do resultado, solicite decomposição. Se não houver responsabilidade interna elegível, use `mismatch`.

Não altere a análise. Quando decisão ou critérios precisarem mudar, solicite revisão com `$decision-analysis-v4`.

## Aprovação e comunicação

A invocação explícita com `status: proposed` aprova somente a versão referenciada e sua fatia elegível.

Antes da escrita, informe análise, evidências, responsabilidades internas, unidades que poderão ser testadas e handoffs. No final, inclua regras e casos de uso entregues, testes unitários, arquivos, verificações e itens excluídos.
