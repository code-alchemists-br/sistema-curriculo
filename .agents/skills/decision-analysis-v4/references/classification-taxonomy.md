# Taxonomia de classificação e valor

Use campos estruturados e selecione somente valores que mudem entendimento, roteamento ou revisão.

## Esfera primária: `sphere`

Escolha exatamente uma: `business`, `product`, `engineering`, `operations`, `governance`, `organization` ou `mixed`.

- `business`: modelo econômico, política comercial, custos, receita ou operação do negócio.
- `product`: resultado para usuários, comportamento, descoberta ou priorização.
- `engineering`: construção ou evolução técnica.
- `operations`: produção, suporte, incidentes, capacidade ou continuidade.
- `governance`: conformidade, auditoria, política ou risco institucional.
- `organization`: responsabilidades, coordenação, competências ou processo de equipe.
- `mixed`: somente quando nenhuma esfera dominar; justifique.

## Preocupações: `concerns`

Escolha até três: `domain`, `architecture`, `implementation`, `data`, `integration`, `security`, `privacy`, `reliability`, `observability`, `performance`, `delivery`, `user-experience`, `compliance` ou `collaboration`.

Não use `technical`: prefira `sphere: engineering` com preocupação específica.

## Tipo: `decision_kind`

Escolha um: `clarification`, `prioritization`, `policy`, `design`, `selection`, `change`, `remediation` ou `experiment`.

## Metadados

- `scope`: `local`, `component`, `system`, `multi-system`, `organization`.
- `lifecycle`: `discovery`, `design`, `delivery`, `operation`, `evolution`, `retirement`.
- `urgency`: `normal`, `time-critical`.
- `uncertainty`: `low`, `medium`, `high`.
- `reversibility`: `easy`, `moderate`, `costly`, `effectively-irreversible`.
- `risk`: `low`, `medium`, `high`, `critical`.

Classifique risco por impacto e dificuldade de recuperação, não pelo tamanho do trabalho.

## Dimensões de valor

Escolha de três a sete: `business-value`, `user-value`, `correctness`, `time-to-value`, `delivery-speed`, `simplicity`, `modifiability`, `reliability`, `security`, `privacy`, `observability`, `performance`, `scalability`, `interoperability`, `compliance`, `operability`, `cost-efficiency`, `team-autonomy`, `cognitive-load` ou `optionality`.

## Perfil de pagamento

Use `+2`, `+1`, `0`, `-1` e `-2` para melhora forte, melhora moderada, neutro/desconhecido, piora moderada e piora forte. Registre prioridade, confiança e justificativa; não some automaticamente uma escala ordinal.

Classifique o efeito escolhido como `maximized`, `prioritized`, `satisficed`, `sacrificed` ou `unresolved`.

Separe `loss_if_not_prioritized` de `cost_of_prioritization` para não racionalizar a decisão preferida.
