# Protocolo de avaliação

Use em `evaluation-only` e `evaluation-and-implementation`.

## Avaliar o baseline

1. Delimite concern, componentes, dados, fluxos e critérios da análise.
2. Localize mecanismo, configuração, pontos de aplicação e testes existentes.
3. Trace o caminho relevante ponta a ponta somente por leitura e verificações autorizadas.
4. Para cada critério, classifique `satisfied`, `partial`, `not-satisfied` ou `unknown` e associe evidência concreta.
5. Registre lacunas, efeitos colaterais, riscos e dependências sem ampliar o escopo.

## Perguntas por concern

### Observabilidade

- O sinal existe no ponto correto e possui semântica estável?
- Nível, campos, correlação, cardinalidade e propagação seguem o contrato?
- Segredos e dados sensíveis estão ausentes ou protegidos?
- Duplicação, ruído e custo estão dentro dos critérios definidos?

### Resiliência

- A policy cobre o modo de falha aprovado e respeita o budget?
- Retry é seguro, limitado e não multiplicado por camadas?
- Timeout, isolamento, fallback e recuperação preservam a semântica aprovada?
- Há risco de tempestade, duplicidade ou falha silenciosa?

### Segurança

- O controle está na fronteira de confiança correta e mitiga a ameaça definida?
- Segredos, dados, primitives e dependências seguem a policy aprovada?
- A mudança evita redução de proteção ou exposição adicional?

### Identidade e acesso

- A decisão cobre sujeito, ação, recurso e contexto aprovados?
- Todos os pontos de entrada relevantes aplicam a mesma policy?
- Negação e ausência de identidade seguem o comportamento definido sem vazar dados?
- A UI, se tocada, é apenas conveniência e não o enforcement exclusivo?

## Saída da avaliação

Em `evaluation-only`, não altere código. Responda com escopo, evidências, estado por critério, lacunas, riscos e handoffs. Não crie relatório em arquivo salvo quando a análise ou o usuário pedir explicitamente.

Em `evaluation-and-implementation`, converta somente lacunas `not-satisfied` ou `partial` cobertas pela decisão em delta implementável. Itens `unknown` que exigem nova policy permanecem bloqueados.
