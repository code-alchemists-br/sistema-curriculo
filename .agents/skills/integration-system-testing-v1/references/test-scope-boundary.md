# Fronteira dos testes integrados para cima

Classifique cada objetivo, cenário, arquivo e efeito antes de escrever.

## Níveis permitidos

### `integration`

Exercita colaboração real entre pelo menos duas unidades ou uma fronteira técnica relevante, como aplicação e adapter, adapter e banco, produtor e broker de teste, ou serviço e dependência controlada.

### `contract`

Verifica compatibilidade entre consumidor e provedor, schema, protocolo ou porta pública. Pode usar ferramentas de contrato, mas precisa representar uma fronteira entre partes independentes.

### `system-acceptance-e2e`

Exercita um componente implantável completo, uma API pela interface real, uma jornada de usuário ou um critério de aceitação através das camadas relevantes.

### `non-functional`

Avalia atributo de qualidade do sistema integrado:

- performance, latência, throughput, carga, stress e endurance;
- escalabilidade, capacidade, concorrência e integridade sob disputa;
- confiabilidade, resiliência, recuperação e comportamento sob falhas;
- segurança, autenticação e autorização já implementadas;
- acessibilidade, compatibilidade e comportamento entre plataformas;
- observabilidade e operabilidade já implementadas.

Testar uma característica não autoriza implementar ou corrigir o mecanismo correspondente.

## Fora do nível

### `unit`

Teste isolado de uma função, classe, entidade, use case ou componente, normalmente sem fronteira real. Encaminhe ao perfil que implementa a unidade correspondente.

### `product-change`

Qualquer alteração no produto: regra, interface, endpoint, adapter, persistência, instrumentação, controle de acesso, retry ou hook de testabilidade. Não faça nem mesmo uma pequena correção para obter verde.

### `external-test-operations`

Mudança em CI/CD, deploy, ambiente compartilhado, infraestrutura operacional, provisionamento permanente ou execução contra alvo externo não autorizado.

Harness efêmero e exclusivamente de teste pode entrar quando a análise e o repositório já o atribuem à suíte. Infraestrutura reutilizada por desenvolvimento, homologação ou produção não é exclusivamente de teste.

## Artefatos permitidos

- specs, suites e código sob diretórios de teste;
- fixtures, builders, doubles, stubs, simuladores e dados sintéticos;
- configuração de runner, browser ou ferramenta de teste;
- dependências marcadas como test/dev quando necessárias e aprovadas;
- schemas de contrato, snapshots e golden files usados como entradas versionadas;
- harness descartável e claramente identificado como exclusivo da suíte.

Relatórios, traces, screenshots de execução, coverage e benchmarks são outputs. Não os versione salvo convenção explícita e finalidade de baseline aprovada.

## Distinções importantes

- Testar endpoint com banco real de teste é integração; testar um controller com mocks isolados tende a ser unitário.
- Exercitar jornada pelo navegador é E2E; testar isoladamente um componente visual é unitário e pertence ao frontend.
- Validar matriz de permissões existente é teste não funcional; implementar guard ou role é mudança de produto.
- Injetar falha em ambiente descartável pode ser teste de resiliência; adicionar retry é implementação de resiliência.
- Verificar logs ou traces existentes pode ser teste de observabilidade; adicionar instrumentação não é teste.
- Criar massa sintética é teste; corrigir migration ou seed produtivo é outra área.
- Adicionar biblioteca de teste pode ser suporte da suíte; atualizar dependências não relacionadas não é.
- Configurar execução local da suíte pode entrar; editar pipeline de CI não entra.

## Escopo misto

Classifique cada critério como `integration`, `contract`, `system-acceptance-e2e`, `non-functional`, `unit`, `product-change`, `external-test-operations` ou `inseparable`.

- Somente níveis permitidos: prossiga.
- Mistura separável: implemente apenas os testes permitidos e registre handoffs.
- Qualquer item `inseparable` necessário ao resultado: interrompa e solicite decomposição.
- Nenhum teste integrado ou superior: use `mismatch`.

Não declare a análise inteira implementada quando entregar somente a fatia de testes.
