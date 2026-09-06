---
name: integration-system-testing-v1
description: "Implementa testes de integração e níveis superiores, incluindo contrato, API, sistema, aceitação, E2E e testes não funcionais, a partir de uma análise de decisão v4. Valida a hierarquia de AGENTS.md, a versão da análise, o contexto e a aderência à atividade de testes; exclui testes unitários isolados, implementação ou correção do produto, CI/deploy e infraestrutura não dedicada a testes. Use somente por invocação explícita com a referência da análise e instruções adicionais opcionais."
---

# Integration and System Testing v1

Transforme uma análise aprovada somente em testes integrados ou de nível superior. Cubra comportamento funcional e atributos não funcionais sem assumir responsabilidade pela implementação do produto avaliado.

## Entrada

Exija uma referência inequívoca a exatamente um arquivo de análise de decisão. Aceite instruções adicionais opcionais em texto livre.

Se a referência estiver ausente, ambígua, inacessível ou apontar para mais de uma análise, peça o caminho exato e não altere arquivos.

## Gate antes de qualquer escrita

Permita somente inspeções e comandos não mutáveis até concluir, nesta ordem:

1. Leia integralmente os `AGENTS.md` aplicáveis, da raiz até o artefato e os possíveis arquivos de teste.
2. Leia [references/analysis-input-contract.md](references/analysis-input-contract.md) e valide identidade, esquema, versão, status, linhagem, evidência, oráculos e instruções adicionais.
3. Leia [references/test-scope-boundary.md](references/test-scope-boundary.md) e classifique cada responsabilidade como `integration`, `contract`, `system-acceptance-e2e`, `non-functional`, `unit`, `product-change`, `external-test-operations` ou `inseparable`.
4. Leia [references/test-fit-check.md](references/test-fit-check.md), inspecione o repositório e determine `valid`, `ambiguous` ou `mismatch`.
5. Somente com `valid`, leia [references/implementation-protocol.md](references/implementation-protocol.md), implemente e verifique dentro de um alvo seguro.

O nome da pasta, a presença da palavra “test” ou a possibilidade de escrever uma asserção não bastam para validar a atividade.

## Escopo permitido

Implemente somente:

- testes de integração entre módulos, processos, adapters, bancos, filas ou serviços;
- testes de contrato entre consumidores e provedores;
- testes de API e de componentes implantáveis exercitados por sua interface real;
- testes de sistema, aceitação, jornadas e E2E;
- testes não funcionais de performance, carga, stress, endurance, escalabilidade, concorrência, confiabilidade, resiliência, recuperação, segurança, acessibilidade, compatibilidade, observabilidade e operabilidade;
- fixtures, builders, doubles, dados sintéticos, stubs, simuladores e harnesses dedicados a esses testes;
- configuração e dependências exclusivamente de teste, quando aprovadas e compatíveis com as convenções existentes;
- snapshots, golden files ou contratos versionados que sejam entradas intencionais do teste.

Um teste não funcional só é implementável quando há cenário, alvo, método de medição e oráculo verificável. Para limiares quantitativos, exija valor e condições de medição aprovados.

## Escopo proibido

Não implemente:

- testes unitários isolados de função, classe, entidade, componente visual ou caso de uso;
- funcionalidade ou correção em código de produção, mesmo quando necessária para o teste passar;
- regras de domínio, telas, casos de uso, adapters, drivers, instrumentação, controles de segurança ou mecanismos de resiliência;
- hooks de teste, endpoints auxiliares ou atributos adicionados ao produto;
- CI/CD, deploy, ambientes compartilhados, infraestrutura de produção ou configuração operacional;
- Nix, Docker, Terraform, Kubernetes ou scripts de ambiente, salvo harness descartável e exclusivamente de teste já previsto pela análise e pelas convenções do repositório;
- relatórios gerados, coverage output, resultados de benchmark ou evidências temporárias como código-fonte, salvo convenção explícita do projeto.

Quando um teste revelar defeito ou ausência no produto, preserve o teste e reporte o handoff; não corrija outra área nesta skill.

## Segurança da execução

Não execute carga, stress, chaos, fault injection, varredura de segurança ou teste destrutivo contra produção, ambiente compartilhado ou serviço externo sem autorização explícita para o alvo, intensidade e janela. Prefira ambiente local, isolado e descartável, dados sintéticos e credenciais próprias de teste.

Se o alvo seguro não estiver disponível, implemente o teste quando ainda for possível validá-lo estaticamente, declare que ele não foi executado e informe as condições necessárias. Não faça chamadas externas reais por conveniência.

## Escopo misto

- Se os testes elegíveis estiverem claramente separados, implemente apenas essa fatia e registre unitários, mudanças de produto e operações externas como handoffs.
- Se o teste exigir mudança de produção, ambiente compartilhado ou critério ainda indefinido, não atravesse a fronteira; solicite decomposição ou a decisão ausente.
- Se toda a demanda pertencer a outra área, classifique como `mismatch` e encerre sem alterações.

## Aprovação

A invocação explícita desta skill com o caminho exato de uma análise `status: proposed` aprova somente aquela versão e sua fatia elegível de testes. Não transfira aprovação para outra versão, correções no produto ou execução arriscada.

Não altere a análise referenciada. Quando escopo, oráculo ou critérios precisarem mudar, solicite uma nova versão com `$decision-analysis-v4`.

## Comunicação

Antes da primeira escrita, informe a análise usada, as evidências de aderência, os níveis e atributos cobertos, o alvo seguro de execução e os handoffs excluídos.

Na resposta final, inclua análise e versão, veredito, testes implementados, artefatos alterados, instruções adicionais tratadas, execuções e resultados, defeitos observados e atividades encaminhadas.
