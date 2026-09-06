---
name: cross-cutting-implementation-v1
description: "Avalia e implementa exclusivamente preocupações Cross-Cutting de observabilidade, logging, métricas, tracing, outras telemetrias de código, resiliência, segurança, autenticação e autorização, a partir de uma análise de decisão v4. Valida AGENTS.md, versão, evidência e aderência da demanda; exclui funcionalidade de negócio, implementação própria de frontend/backend, ambientes e testes acima da unidade. Use somente por invocação explícita com a referência da análise e instruções adicionais opcionais."
---

# Cross-Cutting Implementation v1

Avalie ou implemente mecanismos transversais sem assumir a responsabilidade funcional das camadas atravessadas. Uma alteração pode tocar frontend, aplicação, adapters ou drivers apenas no ponto estritamente necessário ao concern aprovado, preservando a semântica de negócio.

## Entrada e modos

Exija uma referência inequívoca a exatamente um arquivo de análise de decisão. Aceite instruções adicionais opcionais.

Determine pela análise um dos modos:

- `evaluation-only`: avalie o estado existente e não altere código;
- `implementation-only`: inspecione o baseline necessário e implemente a decisão aprovada;
- `evaluation-and-implementation`: avalie, identifique o delta contra os critérios e implemente somente esse delta.

Se referência ou modo estiverem ausentes, ambíguos ou inacessíveis, peça a informação exata e não altere arquivos.

## Gate antes de qualquer escrita

1. Leia integralmente os `AGENTS.md` aplicáveis, da raiz até a análise e todos os possíveis pontos de integração.
2. Leia [references/analysis-input-contract.md](references/analysis-input-contract.md) e valide artefato, versão, status, evidência, concern, modo e instruções adicionais.
3. Leia [references/scope-boundary.md](references/scope-boundary.md) e classifique cada responsabilidade.
4. Leia [references/cross-cutting-fit-check.md](references/cross-cutting-fit-check.md), inspecione o repositório e determine `valid`, `ambiguous` ou `mismatch`.
5. Com `valid`, leia [references/evaluation-protocol.md](references/evaluation-protocol.md) quando houver avaliação e [references/implementation-protocol.md](references/implementation-protocol.md) quando houver implementação.

Até concluir o gate, permita somente inspeções e comandos não mutáveis. Classifique pela finalidade e pelo efeito, não pelo nome da pasta, tecnologia ou dispersão dos arquivos.

## Escopo permitido

- observabilidade: logging estruturado, métricas, tracing, correlação, propagação de contexto, telemetria, error reporting e auditoria técnica;
- resiliência: timeout, retry, backoff, circuit breaker, bulkhead, fallback, degradação, rate limiting, idempotência técnica, recuperação e tratamento de falhas;
- segurança: hardening, validação/sanitização de segurança, headers e políticas, criptografia, segredos, mitigação de ameaças e remediação direcionada de dependência;
- identidade e acesso: autenticação, sessão, tokens, guards, RBAC, ABAC, policy enforcement e autorização;
- configuração, middleware, interceptor, decorator, policy, adapter ou ponto de instrumentação dedicado ao concern;
- avaliação do mecanismo existente contra critérios explícitos;
- testes unitários das unidades Cross-Cutting implementadas ou avaliadas.

Prefira mecanismos de borda, composição ou decoração quando preservarem as dependências arquiteturais existentes. Não injete logging, framework ou autorização no domínio por conveniência.

## Escopo proibido

- criar ou modificar funcionalidade de negócio, regra de domínio, fluxo de caso de uso, contrato funcional, tela, endpoint funcional ou modelo de persistência de negócio;
- implementar adapters ou drivers cuja finalidade principal não seja Cross-Cutting;
- alterar Nix, CI/CD, deploy, infraestrutura/cloud ou configuração de ambiente operacional;
- provisionar ou configurar serviços externos de telemetria, identidade, segurança ou infraestrutura;
- inventar eventos de negócio, papéis, permissões, ownership, ameaças, SLOs, budgets, limiares ou política de fallback;
- testes de integração, contrato, API, sistema, aceitação, E2E ou não funcionais;
- varredura ativa, carga, chaos ou mudança em sistema externo sem autorização específica.

Encaminhe testes acima da unidade para `$integration-system-testing-v1`. Executar suítes existentes como verificação é permitido; criar ou modificar seus testes não é.

## Segurança da mudança

- Nunca registre ou exponha segredo, token, credencial, dado pessoal ou payload sensível sem política explícita e proteção adequada.
- Não reduza controle de segurança, autorização ou resiliência para obter sucesso em teste.
- Não aplique retry a operação não segura ou não idempotente sem decisão explícita.
- Não envie telemetria a serviço externo nem altere tenant, conta ou recurso remoto sem autorização própria.
- Não faça alteração live, deploy, rotação de segredo ou mudança de acesso como consequência implícita da edição do código.

## Escopo misto

Implemente somente a fatia Cross-Cutting quando separável, registrando funcionalidade, testes superiores, ambiente e operação externa como handoffs. Se o concern depender de decisão funcional ou operacional não definida, use `ambiguous` e solicite decomposição. Se não houver responsabilidade transversal elegível, use `mismatch`.

Não altere a análise. Quando concern, política ou critério precisarem mudar, solicite nova versão com `$decision-analysis-v4`.

## Aprovação e comunicação

A invocação explícita com `status: proposed` aprova somente a versão referenciada e a fatia Cross-Cutting descrita; não autoriza operação externa ou execução de teste arriscado.

Antes da escrita, informe análise, modo, concern, evidências, pontos de integração, testes unitários previstos e handoffs. No final, inclua baseline avaliado, delta implementado, arquivos, verificações, riscos residuais e itens excluídos.
