---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: pending
created_at: "2026-10-08T10:06:34-03:00"
lineage:
  mode: initial
  root: null
  supersedes: null
  change_type: initial
  secondary_change_types: []
  decision_impact: initial
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
      locator: "VagaExternaDto e ClienteApiVagasGrupo2"
      content_state: commit
      revision: e711a98
      availability: available
    - path: src/backend/tests/test_double_api_vagas_grupo2.py
      relationship: context
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "asserções sobre campos e busca por termo"
      content_state: commit
      revision: e711a98
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A decisão é sobre uma porta interna do backend para integração externa; prompts/backend mantém as análises técnicas de backend e já contém a análise relacionada ao double de vagas."
classification:
  sphere: engineering
  concerns: [architecture, integration, data]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: high
  reversibility: moderate
  risk: medium
---

# Análise de decisão — Contrato interno do adaptador de busca de vagas

## Solicitação original

Issue #124 — “Definir contrato do adaptador de busca de vagas”. A descrição disponível na issue diz: “Tarefa da fatia vertical atribuída a Andre-LSL. Inclua os testes unitários pertinentes.” A issue não apresenta critérios de busca, modelo de retorno nem campos da vaga.

Objetivo e restrições informados pelo solicitante:

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

- A página da issue mostra status aberto, sem labels ou comentários visíveis. A descrição não oferece critérios de aceitação adicionais.
- RF10 prevê consulta a uma ferramenta de busca por API e processamento da lista de vagas em JSON; RF11 prevê apresentação dos resultados. RF12 prevê associação manual entre currículo e vaga.
- O contrato deve ser interno e não deve depender de um provedor HTTP específico. A implementação do adaptador externo está fora do escopo desta análise.
- A análise relacionada à Issue #151 e o double existente oferecem um protótipo de assinatura e dados, mas não constituem requisitos aprovados para a aplicação.

## Mudanças desde a versão anterior

Nenhum — análise inicial; não há análise anterior identificada para a Issue #124.

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
| `src/backend/tests/doubles/api_vagas_grupo2.py` | supporting | source-code | test | Python | DTO e Protocol do double | commit `e711a98` |
| `src/backend/tests/test_double_api_vagas_grupo2.py` | context | source-code | test | Python | asserções de campos e filtragem por termo | commit `e711a98` |

### Limites da evidência dos artefatos

A issue foi consultada pela página pública; sua descrição curta não explicita requisitos nem havia comentários visíveis. A árvore de trabalho estava limpa na referência `e711a98`. A evidência do double de vagas limita-se à camada de testes: seu DTO e sua `Protocol` são escolhas de um simulador, não prova de um contrato de produção ou do contrato real do Grupo 2. O documento da Issue #151 é uma análise `proposed` e registra risco de divergência com a API futura. Não foi localizada entidade ou modelo de vaga na camada de produção do backend.

## Problema enriquecido

### Resultado desejado

Definir uma fronteira de aplicação que permita ao caso de uso solicitar vagas sem conhecer HTTP, JSON bruto, autenticação ou peculiaridades do fornecedor, deixando o adapter externo para uma etapa posterior. A assinatura concreta só deve ser aprovada quando os dados necessários ao fluxo estiverem claros.

### Atores e interesses

- Estudante: pesquisar vagas e visualizar resultados úteis; associar manualmente uma vaga a um currículo.
- Aplicação/backend: orquestrar a busca sem depender de um fornecedor ou protocolo externo.
- Implementador futuro do adapter: traduzir a API externa para o contrato interno e comunicar falhas de forma controlada.
- Equipe de produto/requisitos: decidir o que pode ser pesquisado e quais informações de vaga precisam ser exibidas ou associadas.

### Evidências e fatos observados

- O ADR-001 separa aplicação e infraestrutura e prevê que integrações externas sejam acessadas por interfaces desacopladas na camada interna.
- `src/backend/application/ports.py` usa `typing.Protocol`; métodos que fazem I/O são assíncronos e seus tipos representam conceitos internos, não respostas HTTP.
- O backend deve obedecer à Clean Architecture: a camada Application não depende de Infrastructure nem da API.
- RF10 especifica API e lista JSON em termos gerais; RF11 cobre apresentação e RF12 a associação manual. Os requisitos não informam filtros nem esquema dos resultados.
- RF10/RF11 e RNF06/RNF08 registram como pendentes o provedor, os parâmetros de busca, os campos retornados e metas mensuráveis de desempenho.
- O double existente propõe `ClienteApiVagasGrupo2.buscar_vagas(termo: str = "", filtros: dict[str, Any] | None = None) -> list[VagaExternaDto]`, com `VagaExternaDto` contendo id, título, empresa, descrição, requisitos, localização, modalidade e URL de candidatura. Essa proposta está em `tests/doubles`, não em `application`.
- Os testes do double verificam pesquisa por termo e alguns campos, mas não definem que todos esses campos sejam obrigatórios para o produto nem esclarecem paginação, filtros ou semântica de associação.

### Hipóteses

- O acesso à API será I/O assíncrono, seguindo as portas existentes do backend.
- A Application deve receber um modelo interno validado, em vez de `dict[str, Any]` ou JSON bruto; o adapter deve traduzir a resposta externa.
- A busca não precisa criar ou persistir uma entidade de domínio `Vaga` até que requisitos confirmem identidade, ciclo de vida e regras próprias para a vaga.
- O DTO e os filtros do double são sugestões exploratórias e podem ser reutilizados apenas após validação dos campos e critérios com produto e com o contrato da API parceira.

### Perguntas em aberto

1. **Critérios de busca:** quais parâmetros o estudante pode informar? Termo livre é suficiente ou são necessários filtros por localização, modalidade, área, tipo de vínculo, faixa salarial ou outros? Quais são opcionais, quais combinações são válidas e o que significa uma consulta sem critérios?
2. **Paginação e ordenação:** a API pode retornar mais resultados do que uma resposta comporta? O fluxo precisa de cursor/página, limite, ordenação ou total de resultados? O contrato interno deve expor esses conceitos?
3. **Modelo e campos da vaga:** quais campos são obrigatórios para apresentar um resultado e quais são opcionais? O protótipo lista `id`, `titulo`, `empresa`, `descricao`, `requisitos`, `localizacao`, `modalidade` e `url_candidatura`; cada campo, cardinalidade, nulabilidade e formato precisam de confirmação.
4. **Identidade para associação:** qual identificador estável permite associar uma vaga ao currículo? A identidade é global ou depende do provedor? A URL de candidatura basta, ou a associação deve preservar provedor e identificador externo?
5. **Forma do retorno:** a busca retorna apenas uma coleção ou também metadados de paginação? Uma resposta parcial/incompleta é permitida? Como representar lista vazia, duplicatas e itens inválidos?
6. **Falhas:** quais categorias internas o caso de uso precisa distinguir para cumprir RNF06 (indisponibilidade/timeout, resposta inválida e outras)? Quem converte cada categoria em mensagem compreensível? Política de retry e limites não estão definidos e não devem ser introduzidos implicitamente no contrato.
7. **Provedor:** qual API será consumida e qual o contrato JSON real? O provedor não é requisito para desenhar uma porta vendor-neutral, mas seu contrato é necessário para validar que a tradução proposta é realizável e para resolver semânticas ausentes.

### Escopo

- Decidir a responsabilidade e a localização arquitetural da abstração interna de busca.
- Comparar alternativas para entrada, resultado e fronteira de erros sem inventar requisitos.
- Determinar quais definições de produto/API precisam preceder a assinatura final.

### Fora do escopo

- Implementar ou testar código nesta análise.
- Implementar cliente HTTP, autenticação, adapter externo, retries ou tratamento de resiliência.
- Definir telas, persistência de vagas ou associações, regras de autorização, compatibilidade currículo-vaga ou ordenação de relevância.
- Promover automaticamente o DTO do double a contrato de produção.

### Critérios de sucesso

- A porta é localizada na Application e não expõe detalhes de transporte/provedor.
- A entrada cobre somente critérios aprovados; o retorno contém somente dados necessários à apresentação e associação definidos pelos requisitos.
- A assinatura deixa explícitos tipos, opcionalidade, semântica de vazio e eventuais metadados de paginação.
- O contrato descreve as falhas que o caso de uso precisa tratar, sem embutir comportamento de resiliência não aprovado.
- A interface pode ser testada com doubles sem rede; qualquer forma final deve ter testes unitários pertinentes quando implementada.

## Restrições aplicáveis

- `[CRITICAL]` Clean Architecture: dependências apontam para dentro; Application define a abstração necessária e não depende do adapter.
- `[REQUIRED]` Código de backend deve seguir DDD e a linguagem ubíqua. Não introduzir entidade ou value object sem necessidade de domínio demonstrada.
- `[REQUIRED]` APIs externas são acessadas por abstrações internas; controllers e casos de uso não acessam diretamente a API.
- `[REQUIRED]` Alteração de comportamento exige testes unitários no ambiente `backend`; testes de integração e níveis superiores usam `tests`.
- `[REQUIRED]` Toda função, classe e DTO novos deverão ter documentação completa, conforme `AGENTS.md`.
- O pedido exclui a implementação do adapter externo e qualquer código nesta etapa.

## Classificação comentada

- `sphere: engineering`: decisão de design de uma fronteira do backend.
- `concerns: architecture, integration, data`: a escolha delimita a dependência externa e o vocabulário/tipagem dos dados.
- `decision_kind: design`, `scope: component`, `lifecycle: design`: trata do contrato da camada Application para a funcionalidade de busca.
- Incerteza alta: critérios, forma de retorno e campos da vaga constam como pendências explícitas nos requisitos.
- Risco médio e reversibilidade moderada: corrigir um contrato antes de consumidores é possível, mas sua adoção por casos de uso, adapters e testes pode tornar mudanças posteriores custosas.

## Decisão de roteamento

Selecionado `prompts/backend`. `prompts/requisitos` é uma alternativa plausível porque há decisões de requisitos em aberto, mas o objeto imediato é o contrato da porta da Application; `prompts/revisao` não é adequado porque não se trata de revisão de artefato anterior. Não há instrução local de subpasta que altere o destino. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | 1 | Não congelar critérios nem campos sem evidência funcional | Evita criar contrato incompatível com o uso real ou API futura. |
| `interoperability` | 2 | A Application deve permanecer independente do fornecedor e do transporte | Permite substituir ou integrar o provider por um adapter. |
| `modifiability` | 3 | Evitar que a forma provisória do double vire dependência de produção | Reduz custo de revisão quando os requisitos/API forem confirmados. |
| `time-to-value` | 4 | Adiar somente o que depende de decisão ausente | Mantém progresso sem cristalizar suposições nos tipos públicos. |

## Alternativas consideradas

- **A — Promover o contrato do double:** mover a assinatura atual para a Application e reaproveitar o `VagaExternaDto` com oito campos, termo vazio por padrão e `dict[str, Any]` para filtros. Vantagem: implementação rápida e compatibilidade imediata com o double. Desvantagem: assume critérios e obrigatoriedade de campos sem requisitos; mistura filtros não tipados com um retorno que se autodenomina canônico, embora tenha sido criado para simulação.
- **B — Contrato genérico de transporte:** receber/devolver dicionários JSON ou tipos amplos para acomodar qualquer API. Vantagem: pouca fricção inicial com respostas variadas. Desvantagem: faz a Application consumir dados sem semântica/validação estável e transfere o acoplamento do provider para casos de uso e interface.
- **C — Fixar agora a fronteira, pendendo a assinatura de dados:** registrar que a Application terá uma porta assíncrona, tipada e independente de fornecedor, implementada por adapter externo, mas adiar os campos de consulta, o modelo de resultado e o mapa de falhas até obter as definições mínimas. Vantagem: conserva as decisões arquiteturais sustentadas sem declarar como requisito o protótipo. Desvantagem: a assinatura e implementação do contrato ficam bloqueadas por uma curta etapa de refinamento.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | 1 | -1 | -2 | +2 | alta | RF10/RF11 e NFR de integração declaram critérios/campos pendentes; C não os inventa. |
| `interoperability` | 2 | 0 | -1 | +2 | média | A é vinculada ao Grupo 2 e a campos hipotéticos; B vaza formato sem tipagem; C deixa o provider no adapter. |
| `modifiability` | 3 | -1 | -2 | +1 | média | A congela premissas do double e B espalha estruturas dinâmicas; C mantém dados internos por definir. |
| `time-to-value` | 4 | +2 | +1 | -1 | média | A e B permitem começar imediatamente; C aguarda respostas de produto/API antes de completar a assinatura. |
| `simplicity` | 5 | +1 | -1 | 0 | média | A parece simples no início, mas filtros livres e campos impostos deslocam complexidade; C limita a decisão ao que já é conhecido. |

## Histórico e decisão atual

### Decisão da versão anterior

Não aplicável: análise inicial desta demanda. A análise `proposed` da Issue #151 propôs um DTO e uma `Protocol` para um double, não aprovou o contrato de produção tratado aqui.

### Decisão recomendada nesta versão

**Pendente para a assinatura concreta.** Com a evidência atual, é responsável fixar somente a direção arquitetural: uma porta no nível Application, seguindo o padrão `Protocol` existente; assíncrona para a chamada de I/O; tipada em termos internos; sem JSON bruto, HTTP ou tipos do provedor; implementada futuramente por um adapter externo. O adapter fará a tradução entre contrato externo e modelo interno.

Não aprovar, por enquanto, nome/método final, campos dos critérios de busca, filtros, modelo de vaga, obrigatoriedade/nulabilidade, paginação ou conjunto de falhas. O DTO de teste pode orientar uma discussão, mas não deve ser movido ou copiado como contrato sem validação. Também não há evidência para introduzir agora uma entidade de domínio `Vaga` ou um contrato de persistência.

A decisão permanece `pending` porque os itens em aberto mudam materialmente tipos, comportamento e responsabilidades do consumidor. Isso não impede documentar a fronteira arquitetural acima; impede declarar completa a definição solicitada pelo título da issue.

### Impacto da revisão

Não há revisão de versão anterior. O principal impacto é separar a estrutura demonstrável do backend (porta interna assíncrona e independente) das decisões de dados ainda não apoiadas por requisitos.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | maximized | Evitar contrato construído a partir de necessidades presumidas | Requisitos registram explicitamente filtros e campos como pendentes. |
| `interoperability` | prioritized | Permitir que a Application não conheça API externa nem JSON | ADR-001 e `ports.py` sustentam dependência por abstração interna. |
| `modifiability` | prioritized | Evitar institucionalizar o DTO experimental do double | O protótipo está na camada de testes e reconhece risco de divergência. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | Uma fronteira assíncrona tipada, sem abstrações adicionais não justificadas | Reaproveita o padrão `Protocol` e não cria entidade, paginação ou política de resiliência sem decisão de necessidade. |
| `time-to-value` | Fazer avanço arquitetural sem aguardar o provedor para definir uma abstração vendor-neutral | Define responsabilidade/localização agora; o bloqueio limita-se ao shape de consulta/resultado. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | Interface pode omitir filtros necessários ou exigir campos que a API e o fluxo não fornecem | alta | estudante, Application, implementação do adapter |
| `interoperability` | Casos de uso podem ficar acoplados a payload, nomes ou semântica do Grupo 2 | média | backend e futuras integrações |
| `modifiability` | Mudanças no protótipo propagam-se por doubles, casos de uso e apresentação | média | equipe backend/testes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `correctness` e `modifiability` | Exige uma rodada curta de decisão de requisitos antes de fechar os tipos | `time-to-value` | Aceitável: evita codificar e depois migrar um contrato arbitrário. |
| `interoperability` | Exige mapear e validar dados na fronteira externa quando o provider for conhecido | simplicidade inicial do adapter | Aceitável: é responsabilidade própria do adapter e preserva o núcleo. |

## Riscos e efeitos de segunda ordem

- Copiar o DTO do double pode transformar uma massa de teste em contrato implícito, especialmente porque sua documentação o chama de modelo canônico sem evidência funcional correspondente.
- Um `dict[str, Any]` genérico pode parecer neutro, mas espalha validação e conhecimento do JSON por consumidores internos.
- Adiar toda decisão, inclusive a fronteira arquitetural, poderia incentivar o futuro cliente HTTP diretamente no caso de uso; a direção recomendada evita essa deriva.
- Sem um identificador externo estável, RF12 pode não conseguir representar de forma inequívoca uma associação currículo–vaga.
- O contrato de falhas pode ficar incompleto frente a RNF06 se o refinamento tratar apenas de sucesso e lista vazia.
- As perguntas sobre desempenho e resiliência devem permanecer fora do escopo da assinatura até que limites ou políticas sejam aprovados; timeout do transporte poderá continuar sob responsabilidade do adapter.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Critérios refletem a busca desejada pelo estudante | Lista aprovada de filtros, opcionalidade e consulta sem critérios | Refinar RF10/RF11 com responsável de produto | Novo critério altera entrada, validação ou paginação |
| Modelo contém somente dados necessários ao resultado e associação | Campos obrigatórios/opcionais, formatos e identificador estável aprovados | Mapear telas/fluxos de resultado e associação; validar com requisito da API | Campo não fornecido pelo provider ou consumidor requer dado ausente |
| A API externa pode ser traduzida para o modelo interno | Contrato JSON/API do provider, quando disponível | Revisão de mapeamento, sem acoplar tipos externos à Application | Semântica incompatível ou dado necessário indisponível |
| Falhas podem ser tratadas conforme RNF06 | Categorias observáveis e tratamento esperado definidos | Validar casos de timeout, indisponibilidade e resposta inválida; depois testar adapter | Consumidor não distingue falha necessária ou mensagem não é compreensível |
| Porta se mantém testável sem rede | Contrato final e consumidor correspondente | Testes unitários com double substituindo a porta, no ambiente `backend` | Testes precisam de HTTP/rede para verificar comportamento do caso de uso |

## Handoffs e atividades posteriores

- Handoff para o responsável por RF10/RF11: aprovar critérios e comportamento de busca, incluindo consulta vazia, paginação e ordenação se necessários.
- Handoff para o responsável por RF11/RF12: definir campos exibidos e identificador estável necessário para associar a vaga ao currículo; declarar campos obrigatórios, opcionais e formatos.
- Handoff para a equipe do Grupo 2/provedor: obter a especificação ou exemplo oficial do JSON e confirmar disponibilidade dos dados necessários. Não é necessário esperar o provedor para definir os requisitos internos.
- Após resolver essas definições, revisar esta análise e então implementar somente o contrato interno na Application e seus testes unitários pertinentes. A criação do adapter externo permanece em etapa separada.

## Síntese

A arquitetura já sustenta uma porta assíncrona, tipada e independente de fornecedor na camada Application, em linha com `ports.py` e ADR-001. Porém, a issue e os requisitos não definem entrada e retorno suficientes para aprovar a assinatura concreta. O DTO de oito campos e os filtros livres do double da Issue #151 são propostas de teste, não requisitos de produção. A análise fica `pending` até que critérios de busca, forma do resultado e campos/identidade da vaga sejam confirmados.
