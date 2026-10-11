---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v004"
status: proposed
created_at: "2026-10-10T18:32:57-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261010-180647-isolamento-dados-estudantes-integracao-v001.md
  supersedes: prompts/backend/20261010-182539-isolamento-dados-estudantes-integracao-v003.md
  change_type: correction
  secondary_change_types: [enrichment]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20261010-182539-isolamento-dados-estudantes-integracao-v003.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_integracao_rejeicao_referencia_curriculo.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: "convenções unittest e cenário ASGI existente, conforme evidência registrada em v002/v003"
      content_state: working-tree
      revision: null
      availability: available
    - path: nix/tests.nix
      relationship: context
      representation: executable-script
      function: configuration
      format: Nix
      analysis_scope: whole-file
      locator: "ambiente formal de testes contém somente Git"
      content_state: working-tree
      revision: null
      availability: available
    - path: .github/workflows/ci.yml
      relationship: context
      representation: executable-script
      function: configuration
      format: YAML
      analysis_scope: selected-section
      locator: "comando atual de descoberta unittest para backend"
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao, prompts/frontend]
  confidence: high
  rationale: "A linhagem descreve um cenário A/B de integração no backend e a revisão trata de como expressar falhas esperadas na suíte existente."
classification:
  sphere: engineering
  concerns: [security, integration, reliability]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: low
  reversibility: easy
  risk: high
---

# Análise de decisão — Cenário A/B de isolamento de dados entre estudantes

## Solicitação original

`$decision-analysis-v4 Issue #150 Testar isolamento de dados entre estudantes.`

## Informações complementares

- Da versão v002, literalmente: `Prepare o cenário de integração que impede um estudante de consultar ou alterar dados de outro.`
- Decisão registrada na v003, literalmente: `Decisão: entregue o cenário A/B de integração como testes que descrevem o comportamento correto, sem alterar código de produção. Os casos que dependem de autenticação ainda inexistente (A lê recurso de B, A altera recurso de B, requisição sem credencial ou com credencial inválida) devem ficar marcados com xfail(strict=True), com o motivo "identidade vem do usuario_id da rota; falta dependência de autenticação injetável". O controle positivo (A lê e altera o próprio recurso) deve passar. Use repositório em memória com estado para conferir o estado de B após a tentativa, e isole a injeção de identidade em um único helper para que o override futuro não altere o resto do teste.`
- Nova instrução do usuário, literalmente: `Atualize a v003 da Issue #150.  Substitua xfail(strict=True) por unittest.expectedFailure, que também falha a suíte em caso de unexpected success. Mantenha o motivo literal "identidade vem do usuario_id da rota; falta dependência de autenticação injetável" em uma constante única, referenciada em comentário acima de cada um dos quatro casos.`

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Marcação de casos dependentes de autenticação | `pytest.mark.xfail(strict=True)` | `unittest.expectedFailure` nos quatro casos | Compatibilidade com o runner `unittest` usado pela suíte/CI | Remove a necessidade de pytest e mantém unexpected success como falha de suíte conforme decisão do usuário |
| Motivo dos casos esperados falhar | Texto passado como `reason` em cada marcação | Literal definido uma única vez em constante e referenciado por comentário acima de cada caso | Evitar repetição e manter razão visível no ponto de leitura | Uma fonte de verdade para a causa técnica dos quatro casos |
| Contexto de execução | Uso de xfail sugeria runner pytest não presente | Confirmadas as convenções `unittest` e CI atual | Corrigir incompatibilidade constatada durante o gate da skill de testes | Mantém implementação no runner já adotado, sem introduzir dependências ou editar CI |
| Decisão e escopo | Testes A/B sem mudanças de produção | Mesmo escopo e mesmos oráculos; apenas substitui o mecanismo de expected failure | Pedido posterior restringe como marcar os casos | Impacto de decisão revisado, sem mudança no comportamento-alvo |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261010-182539-isolamento-dados-estudantes-integracao-v003.md` | primary | prose | documentation | Markdown | arquivo completo; decisão, escopo e quatro casos | working-tree; revisão não fixada |
| `src/backend/tests/test_integracao_rejeicao_referencia_curriculo.py` | supporting | source-code | test | Python | convenções `unittest`, helper ASGI e matriz existente, conforme evidência anterior | working-tree; revisão não fixada |
| `nix/tests.nix` | context | executable-script | configuration | Nix | composição do shell formal de testes | working-tree; revisão não fixada |
| `.github/workflows/ci.yml` | context | executable-script | configuration | YAML | comando de descoberta de testes backend | working-tree; revisão não fixada |

### Limites da evidência dos artefatos

A v003 continua sendo a fonte da decisão A/B e dos oráculos; esta revisão não altera os fatos de produção registrados nela. O contexto da suíte confirma o uso de `unittest` e que o workflow atual executa `python -m unittest discover`; o shell `tests` não fornece pytest. Nenhum conteúdo de Issue #150 foi alterado, e não há mudança de produção autorizada.

## Problema enriquecido

### Resultado desejado

Preparar testes A/B de integração com o runner `unittest`: A deve conseguir ler e alterar o próprio recurso; quatro comportamentos que dependem da autenticação ainda ausente devem expressar suas asserções corretas e usar `unittest.expectedFailure`. As falhas esperadas devem compartilhar um motivo literal definido uma única vez, referenciado por comentário antes de cada caso.

### Atores e interesses

- Estudantes A e B, titulares de recursos privados e distinguíveis.
- Mantenedores, que precisam de controle positivo ativo e de detecção de unexpected success no runner adotado.
- Implementador dos testes, que precisa conservar a helper única de injeção de identidade e uma razão técnica centralizada.

### Evidências e fatos observados

- A Issue #150, registrada nas versões anteriores, demanda cenário de integração contra consulta e alteração de dados de outro estudante.
- A v003 definiu um controle positivo, quatro casos dependentes de autenticação, repositório em memória com estado, helper de identidade e nenhuma mudança em produção.
- A suíte backend utiliza `unittest`; o workflow observado executa `python -m unittest discover`. O ambiente Nix formal `tests` não inclui pytest.
- A nova instrução troca especificamente a marcação dos quatro casos por `unittest.expectedFailure` e pede constante única para o motivo, referenciada nos comentários locais.

### Hipóteses

- Os quatro casos podem ser implementados como métodos de `unittest.TestCase`/`IsolatedAsyncioTestCase` e usar `@unittest.expectedFailure` sem dependência adicional.
- Unexpected success permanece sinalizado como falha do resultado do runner, conforme afirmado pelo usuário.
- A constante do motivo serve como referência documental nos comentários; `unittest.expectedFailure` não recebe nem exibe uma razão textual como argumento de decorator.

### Perguntas em aberto

Nenhum identificado. Recurso, atores, comportamento, runner e marcação esperada foram definidos pela linhagem e pelo novo complemento.

### Escopo

- Manter os testes A/B de leitura e alteração de currículo no fluxo de integração HTTP/aplicação existente.
- Usar repositório em memória com estado e verificar que B não muda após tentativa de escrita cruzada.
- Concentrar a origem/injeção da identidade em uma única helper.
- Ter um controle positivo sem `expectedFailure` e quatro casos decorados individualmente com `@unittest.expectedFailure`: leitura cruzada, alteração cruzada, sem credencial e credencial inválida.
- Definir o texto literal `identidade vem do usuario_id da rota; falta dependência de autenticação injetável` uma vez em uma constante; inserir comentário acima de cada um dos quatro casos que referencie o nome dessa constante.
- Não alterar código de produção, dependências, ambiente Nix, workflow CI ou mecanismo de autenticação.

### Fora do escopo

- Adicionar pytest, alterar o runner ou mudar configuração/CI.
- Alterar produção para criar autenticação ou autorização.
- Generalizar a matriz para todos os recursos do estudante.
- Tratar `expectedFailure` como proteção ativa; é documentação executável da lacuna atual.

### Critérios de sucesso

1. O controle positivo de A lendo e alterando o próprio recurso executa normalmente e passa.
2. Os quatro casos negativos estão individualmente marcados com `unittest.expectedFailure`.
3. A razão literal existe uma única vez como valor de constante e cada caso possui comentário que referencia essa constante.
4. O runner `unittest` registra os casos como expected failures e reporta qualquer unexpected success como falha de suíte.
5. O repository double mantém e atualiza estado; após a tentativa de alteração cruzada, o estado relevante de B é comparado com o snapshot anterior.
6. A tentativa de leitura cruzada contém asserções contra divulgação de conteúdo privado.
7. A futura troca de estratégia de identidade é localizada na única helper.
8. Nenhuma mudança ocorre fora dos artefatos de teste aprovados; sem código produtivo, pytest, Nix ou CI.

## Restrições aplicáveis

- A aprovação cobre somente testes; produção permanece inalterada.
- Usar o runner existente `unittest`, sem instalar ou introduzir pytest.
- Aplicar `unittest.expectedFailure` a exatamente os quatro casos indicados; manter o controle positivo ativo.
- Manter o motivo exato em uma única constante, e comentários nos quatro pontos devem referenciar o nome da constante sem duplicar o literal.
- Usar helper única para identidade e verificar estado de B após mutação tentada.

## Classificação comentada

- `sphere: engineering`; `concerns: security, integration, reliability`.
- `decision_kind: design`, `scope: component`, `lifecycle: delivery`.
- `uncertainty: low`: a nova decisão resolve a compatibilidade do runner sem mexer no escopo do teste.
- `risk: high`: o comportamento protege dados pessoais, enquanto os quatro casos permanecem falhas esperadas até auth existir.

## Decisão de roteamento

Manter `prompts/backend`: a linhagem é do cenário backend e a decisão se refere à integração HTTP e suíte backend. `requisitos`, `revisao` e `frontend` são menos específicos ao objeto.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | Alta | Controle próprio passa; negativos preservam oráculos explícitos | Evita ocultar bloqueio total ou vazamento |
| `reliability` | Alta | Runner oficial identifica unexpected success como falha | Evita que a marcação fique obsoleta silenciosamente |
| `modifiability` | Média | Um helper e uma constante para pontos de substituição/explicação | Reduz retrabalho futuro e divergência de motivo |
| `security` | Alta | A intenção de negação de acesso cruzado fica explícita | Resultado central da Issue #150 |
| `simplicity` | Média | Reutilizar runner e harness existentes | Evita ferramentas paralelas para cinco cenários |

## Alternativas consideradas

- **A — `unittest.expectedFailure` e constante única (recomendada).** Compatível com a suíte e CI existentes, preserva testes esperados e permite detectar unexpected success; comentário local referencia o motivo central. Não adiciona suporte pytest.
- **B — `pytest.mark.xfail(strict=True)`.** Expressa nativamente motivo/strict, mas requer pytest e fluxo de descoberta diferente do runner existente; está substituída pela decisão mais recente.
- **C — Não marcar os quatro casos, deixando a suíte falhar.** Mostra lacuna diretamente, mas impede a suíte de permanecer utilizável enquanto o sistema ainda não tem autenticação; não atende à decisão de caracterizar falhas esperadas.

## Perfil de pagamento comparativo

Escala ordinal: `+2` melhora forte, `+1` melhora moderada, `0` neutro/desconhecido, `-1` piora moderada, `-2` piora forte.

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | Alta | +2 | +2 | +1 | Alta | A e B preservam oráculos; C interrompe a suíte apesar de caracterização correta |
| `reliability` | Alta | +2 | +1 | -1 | Alta | A é descoberta pelo runner atual e unexpected success é sinalizado; B não está no fluxo; C gera falha persistente conhecida |
| `simplicity` | Média | +2 | -1 | +1 | Alta | A não adiciona dependência; B exige runner/dependência; C tem menos marcações, mas não é executável como suíte estável |
| `modifiability` | Média | +2 | +1 | 0 | Média | A centraliza texto e mantém helper/runner; B exige adaptar ambiente; C não oferece transição organizada |
| `security` | Alta | +1 | +1 | +1 | Média | Nos três casos a proteção continua ausente em produção; testes apenas documentam ou sinalizam a lacuna |

## Histórico e decisão atual

### Decisão da versão anterior

A v003 recomendou `pytest.mark.xfail(strict=True)` para os quatro cenários dependentes da autenticação, junto com controle positivo, repository double com estado e helper única de identidade. A intenção era deixar unexpected pass provocar falha.

### Decisão recomendada nesta versão

Substituir a marcação pela alternativa A. Usar `@unittest.expectedFailure` nos quatro casos: A lê recurso de B; A altera recurso de B; requisição sem credencial; requisição com credencial inválida. Declarar uma constante única cujo valor literal seja `identidade vem do usuario_id da rota; falta dependência de autenticação injetável`. Colocar comentário imediatamente acima de cada caso/decorator referindo essa constante, já que o decorator de unittest não aceita argumento de motivo. Manter o caso positivo e os demais critérios da v003 sem alteração.

Não adicionar pytest, dependências, configuração Nix ou CI. A razão é a compatibilidade direta com o runner `unittest` já adotado pelo projeto.

### Impacto da revisão

`revised`: substitui somente o mecanismo de expected failure e sua documentação local. Os atores, endpoints, oráculos, dados, helper e limite de não alteração de produção permanecem os mesmos.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | prioritized | Controle positivo ativo e comportamento negativo explicitado | Decisão da Issue #150 e v003 |
| `reliability` | prioritized | Unexpected success reportado pelo runner atual | Requisito explícito e convenção de execução unittest |
| `simplicity` | prioritized | Não introduzir novo framework ou ambiente | Nix e CI atuais usam unittest |
| `modifiability` | prioritized | Motivo e origem de identidade substituíveis em pontos únicos | Constante e helper solicitadas |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `security` | Não confundir falha esperada com proteção real | Quatro expected failures deixam explícita a lacuna enquanto controle positivo demonstra funcionalidade própria |
| `simplicity` | Cobrir somente leitura/alteração e duas condições de credencial | Mantém matriz restrita ao escopo aprovado |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | Falta de controle positivo pode confundir indisponibilidade geral com isolamento | Alta | Estudantes e mantenedores |
| `reliability` | Se unexpected success não falhar, os expected failures podem ficar obsoletos | Alta | Equipe backend |
| `modifiability` | Motivo copiado em vários lugares pode divergir ou ficar desatualizado | Média | Mantenedores |
| `security` | Sem os quatro casos, lacuna contra consulta/escrita cruzada e credenciais inválidas fica menos visível | Alta | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Runner existente | `expectedFailure` não carrega reason nativo no relatório | `observability` | Aceitável porque comentário por caso referencia constante descritiva única |
| Motivo centralizado | Leitor precisa seguir nome da constante para ver o texto | `cognitive-load` | Aceitável para evitar duplicação literal |
| Suíte estável antes de auth | Casos negativos não representam bloqueio de runtime ainda | `security` ativa | Custo temporário e explícito até autenticação ser entregue |

## Riscos e efeitos de segunda ordem

- A constante e os comentários explicam a causa, mas não associam automaticamente reason ao relatório de `unittest`; deve-se manter comentário imediatamente acima de cada caso.
- A análise não autoriza interpretar unexpected success como sucesso silencioso: o runner empregado deve retornar resultado não aprovado para unexpected success, conforme decisão e comportamento adotado pelo projeto.
- Um caso expected failure pode passar a ser inesperado por mudança no teste, não necessariamente por autenticação correta; revisar assertiva, caminho e helper antes de remover a marcação.
- A origem da identidade deve permanecer num único helper; distribuir IDs de ator diretamente pelos requests enfraquece a futura substituição por dependência injetável.
- O repositório em memória verifica estado no teste, não transação/ORM real; essa limitação permanece registrada desde v003.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Controle positivo funciona | Leitura e alteração próprias com resultado esperado | Executar teste unittest sem expectedFailure | Falha: corrigir setup/oráculo do teste sem mascarar como falha de auth |
| Quatro casos dependentes são esperados | Runner lista exatamente quatro expected failures | Executar suíte pelo comando unittest do backend | Erro de import/setup ou falha inesperada aponta problema no teste |
| Unexpected success falha a suíte | Resultado do runner não é aprovado quando expected failure passa | Confirmar pela semântica do runner configurado ou teste demonstrativo isolado | Unexpected success não altera status: rever mecanismo antes de implementação |
| Motivo não é duplicado | Literal aparece numa constante; quatro comentários apontam ao símbolo | Inspecionar arquivo de teste | Literal repetido ou caso sem comentário |
| B permanece intacto | Snapshot pós-tentativa igual ao inicial | Comparar todos os campos protegidos no repository double | Qualquer diferença indica violação do oráculo |
| Identidade tem uma origem | Todos os casos usam a helper única | Inspecionar chamadas e executar cenários | Injeção direta de identidade fora da helper |

## Handoffs e atividades posteriores

- Implementar somente testes com `unittest.expectedFailure`, constante e comentários especificados.
- Quando autenticação injetável for implementada em trabalho próprio, reavaliar cada expected failure, retirar a decoração dos casos que passarem e manter asserções ativas.
- Não alterar produção, pytest, Nix, CI ou dependências nesta entrega.

## Síntese

A v004 mantém o cenário A/B da v003 e resolve a incompatibilidade com o runner do projeto: usar `unittest.expectedFailure` nos quatro casos dependentes de autenticação e deixar o controle positivo passar normalmente. O motivo literal fica uma única vez numa constante; comentário imediatamente acima de cada caso referencia seu nome. Repository double com estado e helper única de identidade permanecem. A principal incerteza é se a futura autenticação injetável permitirá converter cada falha esperada em teste ativo sem mudar os oráculos.
