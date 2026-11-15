---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-11-07T17:57:12-03:00"
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
    - path: "AGENTS.md"
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/AGENTS.md"
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/api/experiencia_profissional.py"
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "DTOs POST/PUT e resposta, linhas 1–95; handlers de cadastro/edição examinados na sessão"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/domain/itens_perfil.py"
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "constantes de limites, linhas 35–94; ExperienciaProfissional, linhas 285–370"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/domain/value_objects.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "Periodo, linhas 446–475"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/application/cadastro_experiencia_profissional.py"
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/application/edicao_experiencia_profissional.py"
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/application/ports.py"
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: Python
      analysis_scope: selected-section
      locator: "Relogio, linhas 206–224"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/infrastructure/persistence/sqlalchemy/experiencia_profissional.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/domain/revisao_curriculo.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "_revisar_consistencia_de_datas, linhas 165–237"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/tests/test_domain_experiencia_profissional.py"
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "criação e edição, linhas 1–110"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "Correção do contrato de gravação de experiências nas camadas de domínio, Application e API; backend é o destino semântico mais específico."
classification:
  sphere: engineering
  concerns: [domain, data, architecture]
  decision_kind: remediation
  scope: component
  lifecycle: evolution
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — validar datas e textos na gravação de experiências

## Solicitação original

> $decision-analysis-v4 Dois problemas encontrados que devem ser corrigidos: 1. Os campos de data em POST e PUT de experiencias-profissionais permitem datas posteriores a data atual. 2. Os campos de cargo, empresa e descrição permitem textos infinitos.

## Informações complementares

Resposta literal do usuário à escolha de limites nesta análise:

> 200 / 200 / 5.000 caracteres

A pergunta oferecia limites para empresa/cargo/descrição medidos após remover espaços das extremidades. Interpretação adotada: empresa até 200, cargo até 200 e descrição até 5.000 caracteres, após strip. Os números foram escolhidos pelo usuário; o fuso e a estratégia de tratamento de legados abaixo são propostas desta análise, não instruções explícitas dele.

## Mudanças desde a versão anterior

Nenhum identificado: modo initial para uma demanda corretiva que abrange POST e PUT. As análises de cadastro e listagem existentes são antecedentes, não versões desta correção. A busca encontrou limites de texto anteriormente deixados para definição pelo produto; a resposta atual fornece os valores. Não se reabre a decisão do GET nem se altera retrospectivamente outro artefato.

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `AGENTS.md` | context | prose | prompt-instruction | Markdown | whole-file: arquivo completo | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao HEAD |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | Markdown | whole-file: arquivo completo | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao HEAD |
| `src/backend/api/experiencia_profissional.py` | primary | source-code | production | Python | selected-section: DTOs POST/PUT e resposta, linhas 1–95; handlers de cadastro/edição examinados na sessão | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao HEAD |
| `src/backend/domain/itens_perfil.py` | primary | source-code | production | Python | selected-section: constantes de limites, linhas 35–94; ExperienciaProfissional, linhas 285–370 | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao HEAD |
| `src/backend/domain/value_objects.py` | supporting | source-code | production | Python | selected-section: Periodo, linhas 446–475 | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao HEAD |
| `src/backend/application/cadastro_experiencia_profissional.py` | primary | source-code | production | Python | whole-file: arquivo completo | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao HEAD |
| `src/backend/application/edicao_experiencia_profissional.py` | primary | source-code | production | Python | whole-file: arquivo completo | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao HEAD |
| `src/backend/application/ports.py` | supporting | source-code | schema-contract | Python | selected-section: Relogio, linhas 206–224 | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao HEAD |
| `src/backend/infrastructure/persistence/sqlalchemy/experiencia_profissional.py` | supporting | source-code | production | Python | whole-file: arquivo completo | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao HEAD |
| `src/backend/domain/revisao_curriculo.py` | supporting | source-code | production | Python | selected-section: _revisar_consistencia_de_datas, linhas 165–237 | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao HEAD |
| `src/backend/tests/test_domain_experiencia_profissional.py` | supporting | source-code | test | Python | selected-section: criação e edição, linhas 1–110 | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao HEAD |

### Limites da evidência dos artefatos

Inspeção estática; não foram executados testes ou requisições nesta análise. “Textos infinitos” é o relato do usuário: o código confirma ausência de limite de produto, não capacidade literalmente infinita de rede/banco. Não houve inspeção de dados persistidos, portanto a existência e quantidade de registros fora dos novos limites são desconhecidas. Buscas em prompts serviram à descoberta, sem auditoria completa das linhagens anteriores. O working tree contém entregas anteriores ainda não commitadas, a preservar. As referências metodológicas da skill foram consultadas como instruções, não como prova de produto.

## Problema enriquecido

### Resultado desejado

POST e PUT devem rejeitar datas posteriores ao dia atual e textos acima dos limites escolhidos antes de gravar, com regra consistente, resposta 422 e nenhuma alteração parcial. Hoje e datas passadas válidas continuam aceitos; data_fim nula continua indicando experiência em andamento.

### Atores e interesses

- Estudante: entender os limites e corrigir dados pelo Swagger ou outro consumidor.
- Consumidor: conhecer os limites estáticos no OpenAPI e receber erros previsíveis.
- Equipe do backend: uma regra de domínio testável, tempo determinístico e dados existentes acessíveis.

### Evidências e fatos observados

1. Os DTOs usam str sem min_length/max_length e date sem comparação com hoje. PUT herda os textos de POST e exige data_fim presente, embora anulável.
2. ExperienciaProfissional valida apenas tipo e conteúdo não vazio após strip; não impõe máximos e atualmente preserva os textos recebidos.
3. Periodo garante tipos e fim >= início, mas é compartilhado com formação e não compara com o dia atual.
4. Os casos de cadastro/edição não recebem relógio: constroem ou editam a entidade e escrevem pela porta. A edição localiza o recurso pelo dono antes de aplicar a transição.
5. O ORM armazena os três textos como Text e reconstrói a entidade na leitura. Endurecer indiscriminadamente __post_init__ pode fazer GET, PUT e DELETE falharem ao carregar registros antigos.
6. Existe porta Relogio.agora() para tempo injetável. Seu texto documental atual descreve exclusão; deve ser atualizado se reutilizada para as novas gravações.
7. A revisão de currículo possui regra distinta, com tolerância de um dia e verificação de início futuro. Ela não atende à nova exigência estrita de ambas as datas e não deve ser transplantada nem modificada implicitamente.
8. Outros campos de perfil possuem limites próprios, inclusive 200 para textos de formação e 2.000 para descrição de projeto. São precedentes de implementação, não valores aplicáveis automaticamente a experiência. O usuário escolheu 5.000 para sua descrição.

### Hipóteses

H1: “data atual” é o dia civil em America/Sao_Paulo, coerente com o contexto desta sessão. Aplicar esse fuso explicitamente no servidor, independente do fuso do SO ou do navegador. Se o produto operar com outro fuso, revisar esta hipótese antes de implementar.

H2: experiências representam fatos profissionais, portanto nem início nem término admitem previsão futura; data_fim nula é o mecanismo para atividade em andamento.

H3: a correção deve restringir novas gravações sem tornar registros legados ilegíveis. Não há evidência para truncar ou apagar dados antigos automaticamente.

### Perguntas em aberto

Nenhuma sobre os máximos: definidos pelo usuário. Permanecem a confirmação de H1 para o produto e o inventário de dados legados antes de qualquer restrição nova no banco. Essas lacunas não impedem propor o contrato de gravação, mas não autorizam saneamento destrutivo.

### Escopo

POST/PUT de experiências: limites de texto e sua documentação, regra temporal de gravação, relógio injetado, composição dos executores afetados, respostas 422 e testes por nível. Atualização de documentação de funções/portas e fixtures afetadas. Sem mudança de campos da resposta ou do formato da coleção.

### Fora do escopo

Outros recursos (especialmente previsões futuras de formação), mudança global de Periodo, alteração de ordenação ou da revisão curricular, limite global de payload, frontend, truncamento, exclusão ou saneamento automático de legados, migrations com novas constraints nesta primeira correção e alteração de autenticação/propriedade.

### Critérios de sucesso

- Nos dois métodos: data_inicio <= hoje e, se não nula, data_fim <= hoje. Hoje é aceito; amanhã é rejeitado, sem tolerância adicional.
- Fim anterior ao início continua inválido; fim igual ao início continua válido. POST pode omitir data_fim; PUT continua exigindo o campo, aceitando null.
- Empresa e cargo têm 1–200 caracteres; descrição 1–5.000, após strip. Valores no máximo são aceitos; máximo+1 e branco são rejeitados, sem truncamento.
- Textos normalizados são os gravados e retornados. Contagem por pontos de código Unicode, compatível com len(str), não bytes nem grafemas; preservar quebras de linha internas da descrição.
- Rejeição resulta em 422 sem salvar/atualizar. PUT inválido preserva a versão persistida anterior.
- Regra temporal também é aplicada ao invocar os casos de uso sem HTTP; a fonte de tempo é substituível em testes.
- Leitura/exclusão de legados não depende de hoje nem da conformidade aos novos máximos. PUT pode corrigir um legado ao enviar um estado completo válido.

## Restrições aplicáveis

- Clean Architecture/DDD: regras de gravação ficam no domínio; Application coordena tempo e portas; API trata formato, documentação e tradução de falhas.
- Domínio não consulta date.today(), datetime.now(), ambiente ou banco. Recebe a referência temporal por parâmetro explícito.
- Hoje deve ser obtido uma única vez por operação a partir do relógio injetado; o cliente não fornece hoje ou um fuso que altere a validação.
- Não colocar um limite de hoje congelado no import ou em default de classe; a comparação é dinâmica por requisição, incluindo depois da meia-noite sem reinício.
- Preservar a identificação do dono, a consulta escopada, os sete campos de resposta e a semântica de data_fim nula.
- Não adicionar CHECK dependente de CURRENT_DATE ou de relógio externo ao schema: tempo de gravação pertence ao fluxo de domínio.
- ORM e migrations continuam Code First se houver reforço estático posterior no banco; não usar SQL manual como fonte de schema.
- Testes unitários no Nix backend; integração e superiores no Nix tests; Ruff no Nix quality; operações Git fora do Nix.
- Nesta atividade, somente este novo Markdown pode ser escrito; implementação depende de aprovação posterior da análise.

## Classificação comentada

Engineering/remediation: corrigir regras observáveis em duas operações já entregues. Domain, data e architecture distinguem regra temporal, tamanho/compatibilidade dos registros e responsabilidade por camada. Objeto mixed: demanda e arquivos definem conjuntamente o problema. Risco médio por endurecer gravações e possivelmente afetar dados antigos; reversibilidade moderada de um contrato que passa a rejeitar entradas antes aceitas. Incerteza média por legados e H1.

## Decisão de roteamento

Inventário observado: ambientes, backend, frontend, requisitos, revisao e templates. Selecionado prompts/backend com confiança alta, por tratar de correção da API e núcleo de domínio. Requisitos seria menos específico; revisao não é escolhido apenas por se investigar um defeito. Não foram encontrados AGENTS/overrides adicionais em prompts ou candidatas; a escrita segue o AGENTS da raiz.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | Alta | Rejeitar ambas as datas futuras e excesso de texto | Resolve os dois problemas declarados |
| modifiability | Alta | Uma regra de domínio reutilizada | Evita divergência POST/PUT e chamadas internas |
| reliability | Alta | Não bloquear leitura ou correção de legados | Preserva acesso aos dados existentes |
| user-value | Alta | Erros 422 e limites visíveis | Permite corrigir entradas conscientemente |
| simplicity | Média | Menor mudança sem relógio no domínio | Reduz acoplamento e escopo de migração |

## Alternativas consideradas

- A — Estado atual: tipo, texto não vazio e cronologia. Referência comparativa; não satisfaz a demanda.
- B — Regra de gravação no domínio, coordenada por Application com relógio injetado; API explicita os mesmos limites; reconstrução legada permanece estrutural. Viável e recomendada.
- C — B mais endurecimento imediato na construção de todas as entidades e constraints estáticas no banco, após saneamento prévio dos dados. Viável como entrega condicionada a inventário/correção explícita de legados, mas mais ampla e sem evidência de necessidade nesta correção.
- D — Somente validadores HTTP para datas e textos. Implementável, mas inviável como solução completa neste repositório: viola a exigência de proteger regras de negócio no domínio e permite contornar a regra por outros chamadores dos casos de uso.

B/C são alternativas legítimas de alcance. C não é aprovada para execução sobre um banco desconhecido; depende de atividade prévia autorizada e não pode truncar dados para fazer uma migration passar.

## Perfil de pagamento comparativo

Escala ordinal relativa a A: +2 melhora forte, +1 moderada, 0 neutro/desconhecido, -1 piora moderada, -2 forte. Não somar.

| Dimensão | Prioridade | A | B | C | Confiança | Base |
|---|---|---|---|---|---|---|
| correctness | Alta | 0 | +2 | +2 | Alta | Ambas protegem gravações; C reforça também todos os estados/armazenamento |
| modifiability | Alta | 0 | +1 | +1 | Alta | Política central e limites compartilhados |
| reliability | Alta | 0 | 0 | -1 | Média | B mantém leitura legada; C acrescenta risco/custo de transição e auditoria |
| user-value | Alta | 0 | +1 | +1 | Alta | 422/documentação nas duas alternativas |
| simplicity | Média | 0 | -1 | -2 | Alta | B adiciona tempo e política; C soma saneamento e migration |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado nesta linhagem. A leitura de experiências mantém seu contrato; esta proposta acrescenta regras somente às gravações.

### Decisão recomendada nesta versão

Adotar B, status proposed para aprovação humana, incorporando os máximos escolhidos:

1. Definir constantes de domínio específicas para experiência: mínimo 1, máximos de empresa/cargo 200 e descrição 5.000. Não reutilizar limites de projeto como se fossem a mesma política de produto.
2. Centralizar no domínio uma política pura de gravação que normaliza os três textos com strip e valida seus tamanhos e o período contra hoje: início <= hoje, fim nulo ou <= hoje. Usar a validação cronológica já existente de Periodo sem alterá-la globalmente.
3. Expor um caminho de criação de experiência para gravação (fábrica de domínio) e fazer a transição editar usar a mesma política, recebendo hoje explicitamente. Os casos de uso devem usar esses caminhos. A construção estrutural usada pela reconstituição do ORM continua sem relógio e sem rejeitar máximos legados. Documentar a distinção: os novos máximos são contrato das gravações, não uma promessa retroativa de conformidade de todos os registros armazenados.
4. Injetar a porta Relogio existente nos casos de cadastro e edição e atualizar sua documentação para o uso temporal mais amplo. Ler agora uma vez e converter o instante com fuso para America/Sao_Paulo antes de obter date; passar hoje à política de domínio. A conversão usa mecanismo explícito na Application/composição, não o fuso implícito do SO. Relógios e suas chamadas devem ser doubles nos unitários; implementar sem parâmetro temporal controlável pelo cliente ou default de relógio real no núcleo.
5. Na edição, manter a busca por ID/dono antes da transição de domínio. Não introduzir consulta extra, escrita antes da validação ou diferenciação de recursos alheios. Ajustar os adapters de cadastro/edição e main.app para fornecer o relógio já composto, preservando sessão curta e transação por chamada. GET e DELETE não passam pela nova política de gravação.
6. Nos DTOs de POST/PUT, declarar min_length/max_length a partir das constantes do domínio e aplicar strip antes da medição, com tipos estritos de texto na fronteira. A validação de formato na API pode espelhar limites estáticos para resposta rápida/OpenAPI; a autoridade de negócio continua no domínio. Não aplicar controles novos a todos os caracteres ou proibir quebras de linha de descrição por analogia com formação.
7. Não colocar a regra de hoje somente em DTO nem usar FutureDate/PastDate que exclua indevidamente o próprio dia atual. Documentar a restrição dinâmica nas datas e atualizar os exemplos Swagger. Não declarar maximum fixo no schema que expire no dia seguinte.
8. Rejeitar violações com 422 e mensagens públicas seguras. Evitar devolver os textos enormes ou dados pessoais no detail/log. Usar mensagem de cadastro genérica como já ocorre na edição para as novas falhas de domínio, sem alterar autenticação e os 404 existentes.
9. Não alterar o schema nesta primeira entrega. Text continua suportando legados; a aplicação bloqueia gravações inválidas. Constraints estáticas opcionais ficam para atividade posterior, depois de medir legado e aprovar sua transição; datas dependentes de hoje não pertencem a CHECK do banco.
10. Não truncar, apagar ou normalizar retroativamente dados existentes. GET pode devolver legado acima do limite ou com datas futuras; o cliente pode corrigi-lo por PUT completo válido. Testar que leitura e exclusão continuam possíveis e que os DTOs de resposta não herdam os novos limites de entrada. A revisão curricular existente permanece independente, inclusive sua tolerância histórica.

Proposta H1: dia civil America/Sao_Paulo sem tolerância. Exemplo com relógio fixo: hoje=2026-11-07 aceita 2026-11-07 e rejeita 2026-11-08 em cada campo; fim null é aceito. O exemplo é um oráculo de teste, não um limite congelado em produção.

### Impacto da revisão

Nenhum identificado: modo initial. Complemento recebido nesta mesma análise fixa os máximos em 200/200/5.000 antes da criação do primeiro artefato.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | As mesmas regras para POST, PUT e Application direta | Demanda e caminhos de gravação existentes |
| modifiability | prioritized | Política de domínio e limites compartilhados | Comparação B/C/D |
| reliability | prioritized | Legados continuam legíveis e corrigíveis | ORM reconstrói entidade; H3 |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| user-value | 422 e máximos legíveis no Swagger | DTOs com schema e mensagens sem refletir entradas enormes |
| simplicity | Sem saneamento/migration automática | Limita a entrega ao contrato de novas gravações |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | Datas futuras e textos sem limite continuam graváveis | Alta | Estudante e integradores |
| modifiability | POST/PUT ou outros chamadores divergem | Alta | Equipe e consumidores |
| reliability | Novos validadores tornam legados ilegíveis | Alta | Donos de registros existentes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | Introduzir relógio nos dois casos e atualizar seus chamadores/testes | delivery-speed | Necessário para validar hoje de modo determinístico |
| modifiability | Separar gravação validada de reconstituição estrutural | simplicity | Evita relógio/legado no construtor usado pelo ORM |
| reliability | Manter leitura de dados antigos fora da nova política | correctness | Aceito como compatibilidade explícita, não conformidade retroativa |
| user-value | PUT deve enviar conjunto inteiro corrigido, não só um campo antigo | cognitive-load | Coerente com substituição completa já existente |

## Riscos e efeitos de segunda ordem

- Em UTC já pode ser amanhã enquanto em São Paulo ainda é hoje. Testar a conversão explícita e o processamento após meia-noite, sem confiar no fuso do CI.
- Alterações de assinatura afetam unitários, fixtures, executores e composição. Não usar relógio real opcional para esconder falta de injeção; atualizar todos os chamadores pertinentes.
- Limites no DTO de resposta podem bloquear GET de legados. Separar contratos de entrada e saída.
- Mudar Periodo pode proibir previsões válidas de formação. Restringir a nova regra a experiências e ao caminho de gravação.
- A revisão curricular mantém tolerância diferente: pode não sinalizar um legado que o novo POST rejeitaria. Isso é diferença entre revisão histórica e elegibilidade de nova gravação; reavaliar somente se o produto pedir alinhamento.
- len conta pontos de código; caracteres compostos/emoji podem ocupar mais de uma unidade. Documentar e testar a semântica, sem prometer caracteres visuais.
- Normalizar strip altera novos valores devolvidos para entradas com espaços periféricos; não remover espaços internos ou linhas da descrição.
- Constraints de banco ainda não protegem gravações fora da aplicação. Esse custo é aceito na alternativa B; avaliar C quando houver inventário e necessidade concreta.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Ambas as datas não futuras | Ontem/hoje/amanhã, fim null, início=fim e fim<início em POST/PUT | Unitários de domínio/Application com relógio fixo; integração HTTP posterior | Qualquer data futura aceita ou hoje rejeitado |
| Limites escolhidos | 0, branco, 1, máximo e máximo+1 em cada texto após strip | Unitários parametrizados e DTOs com Unicode e multilinha | Diferença de medida/normalização entre camadas |
| Tempo confiável | Uma leitura por operação, UTC perto da meia-noite e dois dias consecutivos sem reinício | Relógio double e testes de conversão do fuso | Hoje congelado ou inferido do cliente/SO |
| Rejeição sem persistência | salvar/atualizar não chamados; snapshot inalterado em PUT inválido | Unitários com spies e integração em PostgreSQL temporário | Escrita parcial, 500 ou vazamento de dados no erro |
| Compatibilidade legada | Registro com texto longo/data futura pode ser listado, excluído e corrigido com PUT válido | Mapper/unidades e fixtures integradas dedicadas | Falha de reconstrução antes de a correção ser aplicada |
| Swagger | minLength/maxLength corretos e descrição temporal dinâmica para ambos métodos | Teste de contrato OpenAPI posterior | Limite errado, DTO de saída restrito ou data máxima congelada |
| H1 | Revisão humana do fuso proposto | Aprovação desta especificação ou informação complementar | Produto define outro dia civil |
| Reforço futuro no banco | Inventário de dados fora dos novos limites | Atividade separada com acesso deliberado e autorizado ao banco-alvo | Necessidade de escrita externa ou constraints aprovadas |

## Handoffs e atividades posteriores

1. Aprovar esta proposta e H1 antes da implementação. Os máximos já foram escolhidos pelo usuário nesta sessão; não pedir novamente os números.
2. `$backend-domain-orchestration-v2`: constantes/política pura, caminho de criação e edição de gravação, injeção de Relogio e unitários com datas e textos determinísticos; preservar reconstrução legada e não modificar Periodo globalmente.
3. `$backend-adapters-drivers-v2`: DTOs/documentação/422 seguro, passagem do relógio pelos executores e composição, testes unitários isolados. Nenhuma migration ou saneamento nesta fatia inicial.
4. `$integration-system-testing-v1`: PostgreSQL efêmero migrado, POST/PUT nos limites, datas relativas ao relógio controlado, identidade da sessão, ausência de mutação e compatibilidade legada; atualizar fixtures de novas gravações que usem datas futuras.
5. Auditoria/saneamento de dados e eventual reforço estático de schema são atividades separadas, com proposta própria. Não executar contra dados reais nesta análise.

## Síntese

Proposta B: validar novas gravações no domínio com hoje explícito e relógio injetado, impedindo início/fim futuros e limitando empresa/cargo/descrição a 200/200/5.000 após strip. API documenta e traduz as falhas; leitura legada permanece disponível. Nenhum código foi alterado ou teste executado nesta análise.
