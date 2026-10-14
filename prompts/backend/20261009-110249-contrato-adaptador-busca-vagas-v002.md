---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v002"
status: proposed
created_at: "2026-10-09T11:02:49-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261008-100634-contrato-adaptador-busca-vagas-v001.md
  supersedes: prompts/backend/20261008-100634-contrato-adaptador-busca-vagas-v001.md
  change_type: reassessment
  secondary_change_types: [enrichment]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: "github:code-alchemists-br/sistema-curriculo#124"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: selected-section
      locator: "título, descrição, atribuição, labels e atividade visíveis"
      content_state: external
      revision: "consultada em 2026-10-08; sem identificador imutável"
      availability: partial
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: e711a98
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: e711a98
      availability: available
    - path: docs/Arquitetura/ADR-001-arquitetura-do-sistema.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: e711a98
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF10 a RF12, RN01 a RN04 e definições pendentes de busca"
      content_state: commit
      revision: e711a98
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RNF06, RNF08 e definição pendente de integração de vagas"
      content_state: commit
      revision: e711a98
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: e711a98
      availability: available
    - path: prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "decisão, escopo e riscos do double da Issue #151"
      content_state: commit
      revision: e711a98
      availability: available
    - path: src/backend/tests/doubles/api_vagas_grupo2.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "VagaExternaDto, ClienteApiVagasGrupo2.buscar_vagas e implementação do double"
      content_state: commit
      revision: e711a98
      availability: available
    - path: src/backend/tests/test_double_api_vagas_grupo2.py
      relationship: context
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "asserções sobre campos e filtragem por termo"
      content_state: commit
      revision: e711a98
      availability: available
    - path: prompts/backend/20261008-100634-contrato-adaptador-busca-vagas-v001.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: "v001 desta linhagem; decisão pendente e proveniência"
      content_state: working-tree
      revision: "artefato anterior não rastreado, preservado sem alteração"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A decisão continua limitada ao contrato de uma porta interna do backend; a continuidade com v001 e a análise correlata do double sustentam prompts/backend."
classification:
  sphere: engineering
  concerns: [architecture, integration, data]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — Contrato interno do adaptador de busca de vagas

## Solicitação original

Issue #124 — “Definir contrato do adaptador de busca de vagas”. A descrição disponível na issue diz: “Tarefa da fatia vertical atribuída a Andre-LSL. Inclua os testes unitários pertinentes.” A issue não apresenta critérios de busca, modelo de retorno nem campos da vaga.

Objetivo e restrições informados na solicitação original:

> Analise a issue #124 "Definir contrato do adaptador de busca de vagas".
>
> Objetivo: definir somente o contrato interno necessário para permitir busca de vagas por uma API externa futura, sem implementar o adapter externo nesta etapa.
>
> Considere a arquitetura existente do backend, os AGENTS.md aplicáveis, o ADR-001, os requisitos funcionais relacionados à busca de vagas e o padrão já existente em src/backend/application/ports.py.
>
> Examine somente os arquivos necessários e evite ampliar o escopo.
>
> Não implemente código.
>
> Identifique também qualquer informação ainda indefinida que impeça uma decisão responsável, como critérios de busca, modelo de retorno ou campos obrigatórios da vaga.

## Informações complementares

A nova evidência de decisão foi recebida literalmente:

> Nova evidência de decisão:
>
> O líder técnico Rodolpho confirmou que, para a issue #124, devemos usar por enquanto como referência o modelo existente em:
>
> src/backend/tests/doubles/api_vagas_grupo2.py
>
> Incluindo buscar_vagas, VagaExternaDto e os campos atualmente definidos nesse double.
>
> A orientação recebida foi: "Usa esse por enquanto".
>
> Atualize a decisão considerando essa autorização como suficiente para destravar a implementação da #124.
>
> Mantenha o escopo estritamente na definição do contrato interno na camada Application.
>
> Não implemente código nesta etapa.
>
> Não adicione novos campos, filtros, paginação, regras de erro ou requisitos além do que já estiver sustentado pelo double existente e pela arquitetura do projeto.
>
> Preserve a independência da Application em relação ao Grupo 2 e ao transporte HTTP.
>
> Gere uma nova versão da análise, mantendo a lineage com a v001.

A orientação autoriza usar o double como referência temporária para esta issue. Ela não transforma o formato do double em contrato da API externa nem em requisito definitivo do produto.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Evidência decisória | Sem aprovação para promover o double de teste | Líder técnico autoriza literalmente “Usa esse por enquanto” como referência para a #124 | Nova informação fornecida pelo solicitante | Destrava a definição do contrato interno nesta issue |
| Decisão | Pendente para campos e assinatura concretos | Recomenda-se adotar a assinatura e o DTO existentes como baseline temporária | A autorização cobre o risco de decidir esses dados com base apenas em requisitos incompletos | Decisão revisada; sem ampliar o escopo para o contrato externo |
| Limites do contrato | Critérios, campos, filtros, resultado e falhas em aberto | Preservar os parâmetros e campos existentes; não acrescentar filtros nem semântica inexistentes | Pedido explícito de não ampliar o double | Sem novos requisitos, campos, paginação ou política de erro |
| Nome da abstração interna | Sem nome recomendado | Nome da porta deve ser neutro, sem `Grupo2` ou transporte no contrato da Application | O `Protocol` do double chama-se `ClienteApiVagasGrupo2`, incompatível com a independência exigida | Mantém a assinatura funcional sem vazar o fornecedor |
| Artefatos analisados | Evidência da estrutura do double já consultada | Recorte do double relido; v001 incluída como antecessora não rastreada | Verificar o modelo vigente e preservar proveniência | Nenhuma mudança de código ou de requisitos de produto |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| Issue #124 | primary | prose | documentation | GitHub issue | título, descrição e metadados visíveis | externa, consultada em 2026-10-08; sem revisão imutável |
| `AGENTS.md` | context | prose | prompt-instruction | Markdown | arquivo completo | commit `e711a98` |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | Markdown | arquivo completo | commit `e711a98` |
| `docs/Arquitetura/ADR-001-arquitetura-do-sistema.md` | supporting | prose | documentation | Markdown | arquivo completo | commit `e711a98` |
| `docs/requisitos_funcionais.md` | supporting | prose | documentation | Markdown | RF10–RF12, RN01–RN04 e definições pendentes | commit `e711a98` |
| `docs/requisitos_nao_funcionais.md` | supporting | prose | documentation | Markdown | RNF06, RNF08 e pendências de integração | commit `e711a98` |
| `src/backend/application/ports.py` | supporting | source-code | production | Python | arquivo completo | commit `e711a98` |
| `prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md` | supporting | prose | documentation | Markdown | decisão e limitações do double da Issue #151 | commit `e711a98` |
| `src/backend/tests/doubles/api_vagas_grupo2.py` | supporting | source-code | test | Python | DTO, assinatura do protocolo e comportamento de `buscar_vagas` | commit `e711a98` |
| `src/backend/tests/test_double_api_vagas_grupo2.py` | context | source-code | test | Python | asserções de campos e busca textual | commit `e711a98` |
| `prompts/backend/20261008-100634-contrato-adaptador-busca-vagas-v001.md` | supporting | prose | documentation | Markdown | análise anterior completa | working tree, artefato não rastreado preservado |

### Limites da evidência dos artefatos

A issue #124 continua sem critérios de aceitação adicionais visíveis. A v001 e o double não foram alterados desde a análise anterior; o double foi relido e sua assinatura/DTO foram confirmados no commit `e711a98`. A evidência nova sobre a autorização do líder técnico é uma declaração fornecida pelo solicitante, não um comentário recuperado da issue.

A autorização é suficiente para escolher esse modelo como referência temporária de implementação da #124. Não confirma que a futura API do Grupo 2 terá o mesmo JSON, nem que os campos são requisitos permanentes. O argumento `filtros` existe na assinatura, mas o double atual não define nomes nem comportamento para filtros: apenas registra o valor recebido. A implementação de `buscar_vagas` faz busca textual por termo; não aplica filtros.

## Problema enriquecido

### Resultado desejado

Definir o contrato interno na Application para a busca de vagas, usando como baseline temporária a assinatura e o DTO existentes no double, sem implementar o adapter externo e sem permitir que tipos, nomes ou protocolo HTTP do Grupo 2 atravessem a fronteira interna.

### Atores e interesses

- Estudante: receber os resultados de busca que a aplicação disponibilizar e associar manualmente uma vaga a um currículo conforme RF12.
- Application: depender de uma porta interna tipada, assíncrona e independente do fornecedor.
- Implementador da #124: reproduzir na camada Application a assinatura e a estrutura de vaga autorizadas, sem acrescentar comportamento.
- Futuro adapter externo: adaptar o provedor escolhido ao contrato interno, sem exigir que a Application conheça HTTP ou o Grupo 2.
- Líder técnico: permitir que a implementação da #124 avance com o modelo atual enquanto referência.

### Evidências e fatos observados

- ADR-001 e `src/backend/AGENTS.md` estabelecem separação entre Application e Infrastructure; integrações externas devem ser abstraídas internamente.
- `src/backend/application/ports.py` usa `typing.Protocol`; métodos que fazem I/O são assíncronos e os tipos do contrato pertencem ao núcleo interno.
- O double define `ClienteApiVagasGrupo2.buscar_vagas(termo: str = "", filtros: dict[str, Any] | None = None) -> list[VagaExternaDto]` como método assíncrono.
- `VagaExternaDto` é imutável (`frozen=True`, `slots=True`) e define os campos sem valores padrão: `id: str`, `titulo: str`, `empresa: str`, `descricao: str`, `requisitos: tuple[str, ...]`, `localizacao: str`, `modalidade: str` e `url_candidatura: str`.
- A busca no double retorna lista de `VagaExternaDto`, aceita termo vazio e filtra por ocorrência do termo no título, descrição ou requisito. Quando não há termo, retorna a coleção configurada.
- O parâmetro `filtros` é recebido e registrado pelo double, mas não há chaves nem semântica de filtro implementadas. Portanto a assinatura pode preservá-lo, mas esta decisão não define conteúdo ou efeito para esse mapa.
- O double modela modos de sucesso, lista vazia, erro de resposta e indisponibilidade por exceções. A `Protocol` declara somente a assinatura de sucesso/retorno; não declara exceções em sua tipagem.
- A porta atual do double se chama `ClienteApiVagasGrupo2`. Esse nome não deve ser copiado para a Application, pois acoplaria o contrato ao Grupo 2, contrariando o escopo e a arquitetura.
- O líder técnico autorizou o uso temporário do modelo existente para a issue #124.

### Hipóteses

- O contrato interno deve reter nome do método `buscar_vagas`, os argumentos e tipos da assinatura do double, e o tipo de retorno `list[VagaExternaDto]`.
- A porta de produção será nomeada de modo neutro em relação ao provider; o double permanece em sua localização de teste e poderá satisfazer estruturalmente a `Protocol`.
- Os oito campos e seus tipos atuais serão adotados sem inferir nulabilidade opcional, valores padrão ou campos extras.
- O argumento `filtros` permanece opaco nesta etapa: sua presença faz parte da assinatura autorizada, mas não cria filtros funcionais além dos que o double efetivamente implementa.
- A autorização vale como decisão temporária para a #124 e não substitui atualização futura de requisitos ou validação contra a API externa.

### Perguntas em aberto

1. Os nomes e efeitos dos filtros continuam indefinidos. Isso não bloqueia a assinatura baseline para a #124, mas nenhum filtro específico deve ser adicionado ou considerado funcional nesta etapa.
2. A especificação da API futura e a compatibilidade de seus campos com `VagaExternaDto` permanecem desconhecidas. Essa verificação pertence à implementação do adapter, não à definição interna atual.
3. O double expõe exceções de indisponibilidade e resposta inválida, mas seu `Protocol` não define um contrato de exceções. Esta decisão não adiciona tipos, políticas ou regras de erro à Application; a implementação da porta deve manter a independência de nomes de exceção específicos do Grupo 2.

### Escopo

- Definir o contrato interno de busca na camada Application com base no `buscar_vagas` e no `VagaExternaDto` do double vigente.
- Preservar exatamente os parâmetros, campos e tipos existentes no double.
- Determinar os limites de independência entre a porta, o Grupo 2, a camada de testes e o transporte HTTP.

### Fora do escopo

- Implementar ou testar código nesta análise.
- Implementar o adapter externo, cliente HTTP, autenticação ou integração com o Grupo 2.
- Acrescentar campos, argumentos, filtros funcionais, paginação, ordenação, requisitos ou política de erro.
- Definir persistência, entidade de domínio `Vaga`, associações currículo–vaga ou apresentação na interface.
- Declarar o double como contrato final da API externa ou requisito definitivo de produto.

### Critérios de sucesso

- A porta e o DTO ficam no limite interno da Application e não importam módulos sob `tests`, nomes do Grupo 2 ou tipos HTTP.
- A porta preserva `buscar_vagas`, `termo`, `filtros` e o tipo de retorno da assinatura do double, sem novo parâmetro ou filtro.
- `VagaExternaDto` preserva somente os oito campos e tipos atuais do double.
- A assinatura pode ser exercitada pelo double existente sem rede; nenhum payload ou detalhe do transporte externo é exposto ao consumidor da Application.
- A decisão é entendida como baseline temporária restrita à #124.

## Restrições aplicáveis

- `[CRITICAL]` Clean Architecture: dependências apontam para dentro; a Application não depende de Infrastructure, API ou adapters.
- `[REQUIRED]` Dependências externas são acessadas por abstrações definidas na camada interna que delas necessita.
- `[REQUIRED]` O contrato deve usar a linguagem ubíqua e não introduzir entidade ou value object sem regra de domínio demonstrada.
- `[REQUIRED]` Alterações futuras de comportamento exigirão testes unitários no ambiente `backend`; esta atividade é análise documental e não executa testes nem altera código.
- `[REQUIRED]` Qualquer implementação futura deve documentar funções, classes e DTOs conforme os `AGENTS.md` aplicáveis.
- A autorização do líder técnico é específica e temporária para a issue #124; não amplia o escopo para adapter externo ou requisitos adicionais.

## Classificação comentada

- `sphere: engineering`: decisão sobre um contrato do backend.
- `concerns: architecture, integration, data`: fronteira interna, integração externa futura e formato dos dados.
- `decision_kind: design`, `scope: component`, `lifecycle: design`: definição localizada na Application.
- Incerteza média: a assinatura interna está autorizada; a semântica de filtros e a compatibilidade com a futura API não foram definidas, mas estão fora do escopo atual e não bloqueiam a #124.
- Risco médio e reversibilidade moderada: a adoção pode levar consumidores internos a depender dos campos; a natureza temporária deve ficar documentada e a revisão é viável antes de consolidar o provider.

## Decisão de roteamento

Mantido `prompts/backend`, destino da v001. `prompts/requisitos` continua alternativa porque parte da evidência trata de dados de busca, mas a decisão é sobre a interface da Application; `prompts/revisao` não representa o assunto principal. Confiança alta, por continuidade da linhagem e natureza técnica da decisão.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | 1 | Igualar somente o modelo autorizado, sem sugerir compatibilidade externa ainda não verificada | Cumpre a decisão temporária sem converter hipóteses em requisitos permanentes. |
| `interoperability` | 2 | Porta interna sem nomes do Grupo 2 ou de HTTP | Permite que o adapter traduza fornecedor para Application. |
| `time-to-value` | 3 | Destravar o trabalho da #124 com o double existente | Atende à orientação técnica explícita. |
| `modifiability` | 4 | Manter a condição temporária visível e evitar novos campos | Facilita revisão se requisitos ou API mudarem. |

## Alternativas consideradas

- **A — Adotar o modelo do double como baseline temporária (recomendada):** expor uma `Protocol` de nome neutro na Application com `buscar_vagas(termo: str = "", filtros: dict[str, Any] | None = None) -> list[VagaExternaDto]` e DTO de oito campos exatamente como existente. Mantém método, parâmetros e retorno autorizados, mas não copia o nome `ClienteApiVagasGrupo2` para a camada interna. Vantagem: implementa a decisão expressa pelo líder sem inventar conteúdo de filtros. Custo: aceita provisoriamente um mapa de filtros sem semântica definida e os campos atuais do double.
- **B — Continuar pendente até definição funcional e contrato externo:** evita qualquer hipótese sobre campos e busca. Vantagem: maior confirmação de requisitos definitivos. Desvantagem: contraria a nova orientação, que autoriza o modelo atual para destravar a issue, e atrasa trabalho limitado ao contrato interno.
- **C — Usar JSON/dicionários genéricos na Application:** aceita payloads variados sem DTO tipado. Vantagem: flexibilidade aparente. Desvantagem: diverge do modelo expressamente indicado, espalha validação e transfere o acoplamento do payload externo para consumidores internos.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | 1 | +1 | 0 | -2 | alta | A corresponde à autorização específica; B não viola campos, mas não atende à decisão; C abandona o DTO tipado. |
| `interoperability` | 2 | +2 | +2 | -2 | alta | A mantém a porta neutra e transfere tradução ao adapter; B também permite neutralidade, C vaza a estrutura dinâmica. |
| `time-to-value` | 3 | +2 | -2 | +1 | alta | A destrava a #124; B posterga; C também permite avançar, porém com contrato fraco. |
| `modifiability` | 4 | 0 | +1 | -1 | média | A é baseline explicitamente temporária; B evita compromisso; C espalha payloads não tipados. |
| `simplicity` | 5 | +1 | -1 | 0 | média | A reutiliza estrutura já existente; B mantém a indefinição; C simplifica tipos localmente às custas de validação posterior. |

## Histórico e decisão atual

### Decisão da versão anterior

A v001 recomendou manter pendente a assinatura concreta, pois apenas os requisitos e o double não bastavam para tratar os campos como aprovados. Já identificava como direção arquitetural uma porta assíncrona, tipada e independente de fornecedor na Application.

### Decisão recomendada nesta versão

**Adotar como baseline temporária da #124 o modelo existente no double**, conforme autorização do líder técnico. A Application deve declarar uma porta `Protocol` assíncrona, com nome neutro de fornecedor, contendo `buscar_vagas` com os mesmos parâmetros e retorno atuais do double:

- `termo: str = ""`;
- `filtros: dict[str, Any] | None = None`;
- retorno `list[VagaExternaDto]`.

`VagaExternaDto` deve preservar somente os campos obrigatórios e tipos existentes: `id: str`, `titulo: str`, `empresa: str`, `descricao: str`, `requisitos: tuple[str, ...]`, `localizacao: str`, `modalidade: str` e `url_candidatura: str`. Não acrescentar paginação ou metadados. Não definir chaves nem comportamento para `filtros`, pois o double não os implementa.

A Application não deve importar `ClienteApiVagasGrupo2`, `DoubleApiVagasGrupo2` ou qualquer módulo de `tests`; também não deve assumir HTTP, JSON bruto ou semântica própria do Grupo 2. O contrato deve ser independente, e o adapter futuro traduzirá para esse vocabulário interno. O helper `para_dicionario` é utilitário do DTO no double para simular JSON e não integra o contrato solicitado, pois sua inclusão transportaria detalhe de teste/serialização à Application sem necessidade arquitetural demonstrada.

Esta decisão trata como autorizada a baseline interna da #124, não declara que o futuro provedor implementa o mesmo payload nem que esses campos são requisitos permanentes. Não são introduzidas novas regras de erro: a `Protocol` mantém a assinatura e retorno declarados no double; modos e exceções do double continuam como comportamento de teste e seus nomes específicos de Grupo 2 não devem vazar para a Application.

### Impacto da revisão

A nova informação muda a decisão de `pending` para uma recomendação executável, portanto `decision_impact: revised`. A fronteira arquitetural continua igual; a autorização remove o bloqueio sobre a escolha temporária de assinatura e campos. O escopo permanece restrito ao contrato na Application.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `interoperability` | maximized | Application independente de Grupo 2 e HTTP | ADR-001, regras backend e nome neutro recomendado para a porta. |
| `time-to-value` | prioritized | Implementação da #124 destravada com o modelo de referência indicado | Declaração do líder técnico fornecida pelo solicitante. |
| `correctness` | prioritized | Contrato interno segue exatamente uma referência aprovada para esta issue, sem alegar equivalência externa | Assinatura e campos relidos no double e autorização temporária. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | Reutilizar assinatura e DTO disponíveis, sem abstrações de consulta adicionais | A porta usa método, argumentos e modelo existentes; somente sua abstração interna deve ser neutra. |
| `modifiability` | Tornar explícita a natureza provisória e conter dependência aos campos adotados | Revisitar se a API real ou os requisitos divergirem; não ampliar a decisão para provider. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `interoperability` | Application pode depender de identificadores ou formatos do Grupo 2/HTTP | alta | Application e futuros adapters |
| `time-to-value` | A issue permanece bloqueada embora haja autorização para usar o double como baseline | média | implementação da #124 |
| `correctness` | Campos ou comportamento do double podem ser confundidos com contrato futuro definitivo | média | produto, backend e equipe de integração |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `time-to-value` | Aceitar temporariamente os oito campos e a forma de busca do double sem confirmação da API real | estabilidade de longo prazo | Aceitável apenas para o contrato interno da #124 e sujeito a revisão quando o provider for definido. |
| `interoperability` | Manter nome neutro na porta embora o double use nome específico do Grupo 2 | conveniência de copiar literalmente o `Protocol` | Aceitável e necessário para obedecer à arquitetura e ao pedido. |

## Riscos e efeitos de segunda ordem

- **Confusão entre baseline interna e contrato externo:** consumidores podem assumir que o Grupo 2 devolverá os mesmos campos. Mitigação: documentar o caráter temporário e manter tradução no adapter.
- **Filtros sem semântica:** a assinatura recebe `filtros`, mas o double apenas os registra. Mitigação: não criar chaves, validação ou comportamento de filtragem nesta issue.
- **Vazamento de fornecedor:** copiar `ClienteApiVagasGrupo2` ou suas exceções para Application acoplaria o núcleo ao Grupo 2. Mitigação: nome de porta neutro e sem imports do pacote de testes.
- **Campos requeridos:** o DTO atual não oferece valores padrão. Essa forma é preservada por autorização; não inferir campos opcionais nem introduzir outros.
- **Mudança futura do provider:** incompatibilidade entre API real e DTO requer tradução/decisão posterior, não modificação silenciosa do contrato externo nesta análise.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Contrato interno reproduz a referência autorizada | Método, assinatura e oito campos exatamente iguais ao double atual | Revisar a implementação da porta/DTO na #124 contra `api_vagas_grupo2.py` | Parâmetro, campo ou tipo novo/removido sem nova decisão |
| Application permanece independente | Nenhum import/nome de Grupo 2, HTTP ou pacote `tests` na porta de produção | Revisão de dependências e imports | Porta exige classe do double, cliente HTTP ou modelo do provider |
| `filtros` não ganhou semântica inventada | Nenhuma chave, regra de validação ou efeito ausente no double | Revisar assinatura e testes unitários pertinentes | Implementação filtra por critérios não definidos ou altera o tipo |
| Baseline não é confundida com API externa definitiva | Tradução fica no adapter futuro e os campos externos são confirmados quando o contrato estiver disponível | Revisar implementação futura da integração | API não consegue mapear campos ou surgem requisitos divergentes |
| Comportamento de sucesso/erro do double continua testável | Testes unitários da porta/consumidor usando o double existente | Executar testes do backend quando a implementação ocorrer | Uso requer rede ou importa o adapter real |

## Handoffs e atividades posteriores

- Handoff para a implementação da #124: definir na Application a porta neutra e o DTO segundo a baseline descrita, com testes unitários pertinentes. Esta análise não altera código.
- Manter o double em `src/backend/tests/doubles`; não fazer da Application uma dependência de `tests`.
- Quando o provedor/API externa for definido, validar o mapeamento e revisar a decisão somente se os campos ou a assinatura não puderem ser atendidos.
- A implementação do adapter externo permanece fora da #124 conforme o escopo informado.

## Síntese

A autorização do líder técnico, registrada pelo solicitante como “Usa esse por enquanto”, é suficiente para destravar a definição do contrato interno da #124 usando a assinatura e o DTO atuais do double: `buscar_vagas`, seus parâmetros existentes e os oito campos tipados de `VagaExternaDto`. A porta deve ter nome neutro e residir na Application, sem dependência de Grupo 2, HTTP ou código de teste. Nenhum filtro funcional, campo, paginação ou regra de erro adicional é definido; a compatibilidade com a API real fica para a etapa futura do adapter.
