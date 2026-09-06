---
name: frontend-implementation-v3
description: "Implementa funcionalidades de telas ligadas ao negócio e, opcionalmente, somente seus testes unitários, a partir de uma análise de decisão v4. Valida AGENTS.md, a versão da análise e a aderência ao frontend funcional; exclui testes de integração ou superiores, observabilidade, resiliência, segurança, autenticação, autorização e outras preocupações transversais. Use somente por invocação explícita com a referência da análise e instruções adicionais opcionais."
---

# Frontend Implementation v3

Transforme uma análise aprovada somente em comportamento funcional de telas ligado a um objetivo de negócio e, quando pertinente, em testes unitários dessa mesma unidade de frontend.

## Entrada

Exija uma referência inequívoca a exatamente um arquivo de análise de decisão. Aceite instruções adicionais opcionais. Se a referência estiver ausente, ambígua ou inacessível, peça o caminho exato e não altere arquivos.

## Gate antes de qualquer escrita

1. Leia integralmente os `AGENTS.md` aplicáveis, da raiz até o artefato e os possíveis alvos.
2. Leia [references/analysis-input-contract.md](references/analysis-input-contract.md) e valide análise, versão, evidência e instruções adicionais.
3. Leia [references/scope-boundary.md](references/scope-boundary.md) e classifique comportamento e testes.
4. Leia [references/frontend-fit-check.md](references/frontend-fit-check.md), inspecione o repositório e determine `valid`, `ambiguous` ou `mismatch`.
5. Somente com `valid`, leia [references/implementation-protocol.md](references/implementation-protocol.md), implemente e verifique.

Até concluir o gate, permita somente inspeções e comandos não mutáveis. Pasta, linguagem ou nome de arquivo não são prova suficiente de aderência.

## Escopo permitido

- páginas, formulários, tabelas, filtros, navegação e interações de um caso de uso de negócio;
- apresentação e edição de dados usando contratos cliente existentes;
- estado local necessário ao fluxo funcional;
- testes unitários que isolem componente, hook, função, formatter, view model ou outra unidade de frontend pertencente ao mesmo escopo;
- alteração composta somente por testes unitários de uma unidade de frontend elegível.

Em teste unitário, substitua dependências externas por doubles e não atravesse rede, backend, browser E2E, múltiplas páginas ou outro processo. Renderização isolada em DOM de teste pode ser unitária quando a unidade e suas dependências estiverem delimitadas.

## Escopo proibido

- testes de integração, contrato, API, sistema, aceitação, E2E, visual end-to-end ou não funcionais;
- alteração de runner, harness ou configuração global de testes;
- observabilidade, resiliência, segurança, autenticação ou autorização;
- infraestrutura transversal, contratos de API inexistentes, backend ou banco de dados;
- iniciativas transversais de acessibilidade, internacionalização, performance, theming, design system ou dependências;
- refatorações e mudanças não relacionadas.

Encaminhe testes acima da unidade para `$integration-system-testing-v1`. Executar uma suíte existente de outro nível como verificação é permitido; criar ou modificar seus testes não é.

Preserve mecanismos existentes sem ampliar suas políticas. Não altere a análise referenciada; quando ela precisar mudar, solicite nova versão com `$decision-analysis-v4`.

## Escopo misto

- Implemente a fatia funcional e seus testes unitários quando estiverem claramente separados.
- Registre testes superiores e preocupações transversais como handoffs.
- Se um item excluído for inseparável do resultado, interrompa e solicite decomposição.
- Se toda a demanda estiver fora do frontend funcional e de suas unidades, use `mismatch`.

## Aprovação e comunicação

A invocação explícita com uma análise `status: proposed` aprova somente a versão referenciada e sua fatia elegível.

Antes da primeira escrita, informe análise, evidências, funcionalidade, unidades que poderão ser testadas e handoffs. Na resposta final, inclua versão, veredito, alterações, testes unitários criados ou modificados, verificações e itens excluídos.
