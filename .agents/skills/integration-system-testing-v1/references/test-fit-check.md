# Check de aderência à atividade de testes

O veredito exige quatro confirmações:

1. O resultado é um teste, não uma implementação do produto.
2. O nível é integração ou superior, ou avalia atributo não funcional do sistema integrado.
3. Existe um oráculo verificável e evidência suficiente do sistema sob teste.
4. A implementação e eventual execução permanecem dentro de artefatos e alvos seguros de teste.

Somente quatro respostas positivas permitem `valid`.

## Evidências a inspecionar

Na análise, examine risco, comportamento, nível, ambiente, dados, critérios, limiares, decisão, handoffs, arquivos e roteamento. No repositório, examine suites, runners, fixtures, contratos, comandos, ambientes de teste e `AGENTS.md` aplicáveis.

Use apenas leitura e busca durante o gate. Não instale dependências, suba ambientes, gere artefatos ou execute testes ainda.

## Sinais positivos

- cenário cruza fronteira real entre componentes ou exercita sistema implantável;
- objetivo valida contrato, API, jornada ou critério de aceitação;
- atributo não funcional possui método e oráculo definidos;
- existe suíte ou local apropriado para artefatos exclusivamente de teste;
- alvo é local, isolado ou explicitamente autorizado;
- nenhuma mudança no produto é necessária para escrever o teste.

Exija pelo menos dois sinais independentes, incluindo um ligado ao nível do teste.

## Sinais negativos

- cenário isola somente uma função, classe, entidade, use case ou componente;
- demanda pede corrigir ou implementar frontend, backend, adapter, ambiente ou infraestrutura;
- objetivo real é adicionar logging, retry, controle de segurança ou outro mecanismo, não testá-lo;
- teste depende de hook, endpoint, regra ou contrato ainda inexistente;
- teste não funcional não possui carga, condição ou limiar necessário;
- única execução possível atingiria produção ou ambiente compartilhado sem autorização;
- tarefa principal é configurar CI, deploy ou provisionamento permanente.

## Vereditos e mensagens

### `valid`

Antes de escrever:

> Análise `<caminho>` (`<versão>`) validada para testes de integração ou superiores: <evidências>. Implementarei <níveis e atributos>. Alvo de execução: <ambiente>. Handoffs excluídos: <lista ou “nenhum”>.

### `ambiguous`

Use quando nível, oráculo, limiar, ambiente ou separação da mudança de produto não estiver claro. Não altere arquivos:

> A implementação foi interrompida porque não está claro se a demanda pertence a testes integrados ou superiores, ou porque falta um oráculo seguro. Evidências: <lacuna ou conflito>. Nenhum arquivo foi alterado.

Faça somente a pergunta necessária ou recomende revisar a análise.

### `mismatch`

Use quando a demanda for unitária, implementação do produto ou operação externa:

> A implementação foi interrompida porque a análise não descreve testes de integração ou níveis superiores compatíveis com esta skill. Evidências: <sinais concretos>. Nenhum arquivo foi alterado. Encaminhe a atividade ao perfil correspondente ou revise a referência.

## Casos limítrofes

- Teste de repository com banco descartável pode ser integração; repository com dependência totalmente mockada tende a ser unitário.
- Teste de contrato pode executar sem o provedor real quando o contrato versionado representa a fronteira entre equipes.
- E2E pode ser escrito antes da funcionalidade quando a análise pedir especificação executável; reporte o estado vermelho esperado e não implemente o produto.
- Performance sem limiar mensurável é exploração, não teste de aceitação concluído.
- Teste de autorização é permitido; criar roles, guards ou tokens produtivos não é.
- Teste de observabilidade é permitido; adicionar logs, métricas ou traces não é.
- Playwright para uma jornada é E2E; teste isolado de componente com Playwright Component Testing continua fora.
