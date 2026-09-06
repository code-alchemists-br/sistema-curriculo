# Protocolo de implementação Cross-Cutting

Use em `implementation-only` e `evaluation-and-implementation` após `valid`.

## Delimitar

1. Mapeie critérios a policy, ponto de integração, unidade, arquivo e verificação.
2. Liste funcionalidade, testes superiores, ambiente e operação externa como handoffs.
3. Preserve arquitetura e comportamento de negócio existentes.
4. Escolha o menor mecanismo coerente que cubra os pontos aprovados.
5. Confirme o `AGENTS.md` específico antes de editar cada caminho.

## Implementar por concern

### Observabilidade

Use schemas, nomes, níveis, propagação e exporters já aprovados. Prefira contexto estruturado e baixa cardinalidade. Redacte dados conforme policy; não registre payload, token ou segredo por conveniência. Evite emissão duplicada por múltiplas camadas.

### Resiliência

Aplique policy na fronteira técnica apropriada, respeite budget e evite retries aninhados. Retry somente operação aprovada como segura; fallback não pode alterar silenciosamente o resultado funcional. Use relógio e aleatoriedade injetáveis quando a arquitetura permitir testes unitários.

### Segurança

Implemente somente o controle ligado à ameaça definida. Use primitives e bibliotecas estabelecidas; nunca criptografia própria. Não incorpore segredo ao repositório e limite remediação de dependência ao conjunto aprovado.

### Identidade e acesso

Implemente a matriz/policy existente sem inventar roles ou ownership. Faça enforcement no lado confiável; guarda ou ocultação no cliente é suplementar. Preserve comportamento de negação e não enfraqueça controle para compatibilidade.

## Testes permitidos

- Crie ou modifique somente testes unitários das unidades transversais no escopo.
- Substitua clock, randomness, exporter, collector, IdP, storage, rede, framework e demais dependências por doubles.
- Cubra policy, redaction, formatação, decisões, limites e transições observáveis da unidade.
- Reuse runner existente; não crie infraestrutura global de teste.
- Encaminhe integração e testes não funcionais para `$integration-system-testing-v1`.

## Verificar

Execute testes unitários afetados, lint, análise estática/typecheck e build. Suítes existentes de níveis superiores podem ser executadas, mas não modificadas. Não execute scanner ativo, carga, chaos ou chamada externa sem autorização específica.

Revise o diff e confirme:

- toda alteração tem finalidade Cross-Cutting rastreável;
- semântica funcional e contratos de negócio não mudaram;
- nenhum segredo ou dado sensível foi introduzido;
- apenas testes unitários foram criados ou modificados;
- ambiente, CI/deploy e recursos externos permaneceram intactos;
- mudanças preexistentes foram preservadas;
- resultados relatados correspondem aos comandos executados.

## Relatar

Informe análise e versão, modo, baseline, critérios avaliados, delta implementado, pontos de integração, testes unitários, verificações, riscos residuais e handoffs para `$integration-system-testing-v1` ou áreas funcionais.
