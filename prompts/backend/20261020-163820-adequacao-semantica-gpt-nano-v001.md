---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-20T16:38:20-03:00"
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
    - path: docs/adequacao_semantica_ia.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "ab2b8bc"
      availability: available
    - path: docs/modelos_curriculo.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "ab2b8bc"
      availability: available
    - path: src/backend/application/politica_limites_contexto_ia.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "ab2b8bc"
      availability: available
    - path: src/backend/infrastructure/configuracao/politica_limites_contexto_ia.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "ab2b8bc"
      availability: available
    - path: src/backend/config/limites_contexto_ia.json
      relationship: supporting
      representation: structured-data
      function: configuration
      format: json
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "ab2b8bc"
      availability: available
    - path: src/backend/application/assistente_descricao_projeto.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "ab2b8bc"
      availability: available
    - path: src/backend/api/projeto_academico.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "DTOs e POST /projetos-academicos/sugestao-descricao, linhas 116-241"
      content_state: commit
      revision: "ab2b8bc"
      availability: partial
    - path: src/backend/domain/modelo_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "ab2b8bc"
      availability: available
    - path: prompts/backend/20261017-140000-modelo-curriculo-edicao-versao-v001.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "ab2b8bc"
      availability: available
    - path: "OpenAI API: GPT-5 nano model"
      relationship: context
      representation: prose
      function: documentation
      format: html
      analysis_scope: selected-section
      locator: "modelo e API disponível"
      content_state: external
      revision: "consultado em 2026-10-20"
      availability: available
    - path: "OpenAI API Overview"
      relationship: context
      representation: prose
      function: documentation
      format: html
      analysis_scope: selected-section
      locator: "autenticação, Responses API, tratamento operacional"
      content_state: external
      revision: "consultado em 2026-10-20"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/frontend, prompts/requisitos]
  confidence: high
  rationale: "A decisão principal define portas, caso de uso, contexto minimizado e adapter HTTP de um provedor externo; a UI e o catálogo são handoffs coordenados."
classification:
  sphere: engineering
  concerns: [integration, privacy, architecture]
  decision_kind: design
  scope: system
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: high
---

# Análise de decisão — melhoria semântica de currículo com GPT nano

## Solicitação original

```text
Faça uma análise usando os documentos 'docs/adequacao_semantica_ia.md' e 'docs/modelos_curriculo.md' para implentar a funcionalidade de melhoria de currículo. Vamos usar como modelo o GPT nano e comunicação por API.
```

## Informações complementares

- A expressão "GPT nano" foi interpretada como o identificador de API `gpt-5-nano`: a documentação oficial da OpenAI o lista na família GPT-5. A escolha deve ficar configurável no servidor para permitir substituição ou fixação futura de uma versão do modelo, sem alterar o contrato da aplicação.
- A documentação oficial consultada indica a Responses API para requisições diretas ao modelo e determina que a credencial permaneça no servidor, carregada de variável de ambiente ou serviço de segredos; ela não deve alcançar o navegador. Fontes: [GPT-5 nano](https://developers.openai.com/api/docs/models/gpt-5-nano) e [API Overview](https://developers.openai.com/api/reference/overview).
- Não foi fornecida uma chave, organização, projeto, limite financeiro ou requisito de retenção de dados. Nenhum segredo foi solicitado, lido ou registrado.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado nesta linhagem | — | Análise inicial | A análise de 2026-10-17 trata somente da enumeração de dois layouts na edição; não decide integração de IA, privacidade ou adequação semântica. | Nova linhagem, sem substituir a decisão anterior. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `docs/adequacao_semantica_ia.md` | Primário | Prosa | Documentação | Markdown | Integral | commit `ab2b8bc` |
| `docs/modelos_curriculo.md` | Primário | Prosa | Documentação | Markdown | Integral | commit `ab2b8bc` |
| Política de limites, fonte de arquivo e JSON | Apoio | Código/JSON | Produção/configuração | Python/JSON | Integrais | commit `ab2b8bc` |
| Contrato e rota do assistente de projeto | Apoio | Código | Produção | Python | Contrato integral; rota de sugestão | commit `ab2b8bc` |
| `src/backend/domain/modelo_curriculo.py` | Apoio | Código | Produção | Python | Integral | commit `ab2b8bc` |
| Análise anterior de modelos | Contexto | Prosa | Documentação | Markdown | Integral | commit `ab2b8bc` |
| Documentação oficial OpenAI | Contexto | Prosa | Documentação | HTML | Modelo/API/autenticação | externa, consultada em 2026-10-20 |

### Limites da evidência dos artefatos

- A análise não executou chamadas à OpenAI, não mediu qualidade, custo, latência ou limites de conta; tais dados não podem ser presumidos.
- O catálogo de seis modelos é uma especificação, enquanto o código atual reconhece somente `classico` e `compacto`. Não foi examinada uma implementação dos seis layouts, porque ela não existe no recorte analisado.
- A política de limites existe e é testada, mas nenhum caso de uso atual a consome para montar ou registrar um contexto de IA.
- A rota de versões ainda contém caminhos legados com `usuario_id` na URL; a nova integração não deve repetir esse padrão e deve derivar o estudante da sessão autenticada.

## Problema enriquecido

### Resultado desejado

Oferecer ao estudante uma melhoria semântica opcional do currículo, para cargo-alvo e descrição de vaga, por uma API de servidor que usa `gpt-5-nano`. A resposta deve ser uma proposta revisável, nunca uma gravação automática, e deve expor somente o contexto profissional mínimo que foi autorizado e selecionado.

### Atores e interesses

- **Estudante:** informa objetivo/vaga, consente com o envio, escolhe itens e aceita, edita ou descarta cada proposta.
- **Backend:** aplica autorização, reduz e limita contexto, chama o provedor, normaliza falhas e registra telemetria sem conteúdo sensível.
- **OpenAI:** provedor externo chamado exclusivamente pelo adapter de infraestrutura.
- **Responsável técnico:** define modelo, política de limites, credencial e orçamento operacional; revisa alterações de configuração.
- **Frontend:** explica o consentimento e itens enviados, mantém os dados locais em caso de erro e não conhece chave ou SDK do provedor.

### Evidências e fatos observados

1. O documento de adequação determina contexto específico por ação, teto configurável de caracteres, priorização determinística e consentimento explícito; telefone, endereço, documentos e credenciais devem ser omitidos.
2. A `PoliticaLimitesContextoIa` já resolve limites por modelo, ação e combinação, respeita teto de segurança e a fonte de arquivo mantém a última política válida durante edição inválida.
3. O backend já possui precedente de porta de Application e estratégia substituível para sugestões de descrição de projeto; sua estratégia padrão é determinística e não chama serviços externos.
4. Não há referência atual a `OPENAI_API_KEY`, SDK OpenAI, cliente HTTP do provedor ou composição de uma integração de IA.
5. A OpenAI documenta `gpt-5-nano` como membro da família GPT-5; a API aceita credenciais bearer e orienta manter chaves em ambiente/serviço de segredos no servidor.
6. O documento de modelos prevê seis apresentações e recomendação por objetivo, porém domínio e frontend conhecidos suportam somente os layouts `classico` e `compacto`.

### Hipóteses

- **H1.** `gpt-5-nano` consegue produzir propostas úteis quando o prompt é estrito, em português, limitado a uma ação e exige saída estruturada; isso precisa ser medido com avaliações antes de habilitação ampla.
- **H2.** O fluxo pode começar pela ação de maior valor documental, `adequar_curriculo_vaga`, e reutilizar a mesma montagem de contexto para melhorar experiência e gerar resumo em entregas posteriores.
- **H3.** O estudante pode compreender e exercer consentimento granular se a tela apresentar finalidade, provedor, modelo, campos enviados e itens selecionados antes da chamada.
- **H4.** A recomendação de modelo de apresentação pode ser determinística a partir do objetivo do currículo; não precisa ser decidida pelo modelo de IA nem bloquear a primeira entrega de adequação textual.

### Perguntas em aberto

1. Qual base jurídica, texto de consentimento, prazo de retenção e política de exclusão são aprovados para o envio a provedor externo?
2. Qual orçamento financeiro, taxa por estudante, timeout e política de retentativa são aceitos?
3. A proposta deve conter apenas texto reescrito e justificativas, ou também mudanças de ordem/destaque e palavras-chave como itens estruturados?
4. Qual versão/snapshot de `gpt-5-nano` e quais parâmetros serão aprovados após a avaliação de qualidade?

### Escopo

- Caso de uso autenticado de adequação a vaga que recebe objetivo, descrição e referências de itens explicitamente escolhidos.
- Serviço de preparação que consulta a política existente, seleciona/trunca itens deterministicamente, registra o conjunto enviado e constrói o prompt sem PII vedada.
- Porta interna para gerar uma proposta; adapter de infraestrutura HTTP para a Responses API da OpenAI, configurado com `gpt-5-nano` e credencial exclusivamente no servidor.
- DTO/rota que requer consentimento explícito e devolve proposta, itens efetivamente usados, identificador do modelo e versão/limites da política, sem persistir alteração no currículo.
- UI em feature própria para consentir, iniciar a análise, revisar cada proposta e só então reutilizar as rotas de edição já existentes para aplicar a escolha do estudante.
- Catálogo de modelos como trilha coordenada: expor objetivo do currículo e recomendação determinística, sem condicionar a adequação textual à construção imediata dos seis layouts.

### Fora do escopo

- Enviar currículo integral por padrão, documentos, contatos, senha, endereço ou chave de API ao provedor.
- Persistir ou publicar automaticamente texto/modelo sugerido.
- Chat contínuo, agentes, ferramentas remotas, upload de currículo ou busca web pelo modelo.
- Treino/fine-tuning, avaliação de candidatos, ranqueamento automático ou decisão de contratação.
- Implementar nesta entrega os seis renderizadores de currículo ou novos tipos acadêmicos ainda ausentes do domínio.

### Critérios de sucesso

- Uma solicitação válida envia somente o contexto permitido, dentro dos limites efetivos, com itens escolhidos/rankeados de modo reproduzível.
- Sem consentimento, não ocorre chamada externa; nenhuma proposta altera o currículo sem comando posterior do estudante.
- A chave não aparece no frontend, respostas, logs ou repositório; falhas, timeout e limites do provedor resultam em mensagem controlada e dados locais preservados.
- O adapter é substituível por double em testes e pode ser desabilitado, mantendo criação, edição, prévia e exportação sem IA.
- Avaliação com massa sintética e casos de privacidade comprova utilidade mínima e ausência dos campos vedados antes de liberar a funcionalidade.

## Restrições aplicáveis

- Clean Architecture: domínio e Application não dependem de SDK, HTTP ou OpenAI; a implementação concreta fica em Infrastructure e é conectada na composição externa.
- A IA é opcional e só sugere; o estudante mantém a decisão final.
- A política de limites é exclusiva do backend, versionada, sujeita ao teto de segurança e não pode ser aumentada pelo cliente.
- A interface não chama o provedor nem contém credencial; deve funcionar com teclado, informar estados e manter os dados no erro.
- Toda alteração futura de comportamento terá docstrings exigidas e testes unitários no ambiente Nix correspondente.

## Classificação comentada

- `sphere: engineering`: a decisão central é a arquitetura de uma integração externa e o contrato do caso de uso.
- `concerns: [integration, privacy, architecture]`: o valor depende da separação do provedor, minimização de dados e fronteiras testáveis.
- `scope: system` e `risk: high`: atravessa backend, frontend e dados pessoais enviados a terceiro; uma exposição é difícil de desfazer.
- `uncertainty: medium`: a solução técnica é conhecida, mas qualidade, custo, consentimento e parâmetros de produção ainda precisam de evidência.

## Decisão de roteamento

Foram consideradas `prompts/backend`, `prompts/frontend` e `prompts/requisitos`. `prompts/backend` é o destino escolhido porque a principal decisão é a porta, preparação de contexto, autenticação e adapter para API externa. A interface e a ampliação do catálogo serão handoffs; `prompts/requisitos` não é o melhor destino pois os dois documentos já descrevem os requisitos de produto.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| `privacy` | 1 | Nenhum dado vedado sai do backend; envio só após consentimento | Currículos contêm dados pessoais e o provedor é externo. |
| `correctness` | 1 | Sugestão rastreável, limitada e não persistida automaticamente | Evita alteração indevida e torna a revisão humana efetiva. |
| `security` | 1 | Chave somente no servidor e logs sem conteúdo sensível | Impede vazamento e uso indevido da conta. |
| `modifiability` | 2 | Troca de provedor/modelo sem reescrever caso de uso | O modelo e o provedor podem mudar. |
| `cost-efficiency` | 2 | Contexto submetido ao orçamento e telemetria suficiente | A previsibilidade de custo é objetivo expresso do documento. |
| `user-value` | 2 | Proposta útil e compreensível, com controle do estudante | A funcionalidade só se justifica se melhorar a candidatura. |

## Alternativas consideradas

**Alternativa A — porta de Application, montador de contexto e adapter HTTP OpenAI (recomendada).** Criar uma intenção de adequação a vaga independente do provedor; o caso de uso recupera somente itens próprios, valida consentimento, resolve limites e chama uma porta. Um adapter em Infrastructure usa a Responses API com `gpt-5-nano`; a Factory decide habilitação e credencial. O retorno é uma proposta estruturada, não uma mutação.

**Alternativa B — chamar OpenAI diretamente pelo router/API HTTP.** A rota recebe o currículo e usa a chave para chamar o provedor, devolvendo texto livre.

**Alternativa C — manter apenas o assistente determinístico atual.** Reutilizar o padrão de descrição de projeto, sem chamada externa e sem adequar currículo à vaga.

**Alternativa D — implementar primeiro os seis layouts e usar o modelo para escolher um.** Concentrar a primeira entrega nos renderizadores e delegar a recomendação de apresentação ao modelo.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `privacy` | 1 | +2 | -2 | +2 | alta | A limita contexto e consente; B tende a misturar transporte/contexto; C não envia dados. |
| `correctness` | 1 | +2 | -1 | 0 | média | A valida seleção e devolve proposta estruturada; B retorna texto livre; C não executa adequação. |
| `security` | 1 | +2 | -1 | +2 | alta | A isola a chave no adapter; B aumenta risco de acoplamento na rota; C não usa chave. |
| `modifiability` | 2 | +2 | -2 | +1 | alta | Porta permite double e troca de provedor; B fixa fornecedor na interface. |
| `cost-efficiency` | 2 | +1 | 0 | +2 | média | A reutiliza a política existente; C não gera custo externo. |
| `user-value` | 2 | +2 | +1 | -1 | média | A realiza o objetivo com controle; B realiza de modo menos controlável; C não adequa à vaga. |

A alternativa D não entra na tabela: ela viola o princípio de separar dados e layout e posterga a necessidade principal de melhoria textual sem evidência de que a IA deva escolher apresentação.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma nesta linhagem. A análise de modelos de 2026-10-17 continua válida para o vocabulário atualmente suportado (`classico` e `compacto`), mas não decide esta integração.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**, em duas trilhas coordenadas e incrementalmente liberadas:

1. **Trilha de adequação semântica:** implementar a ação `adequar_curriculo_vaga`, a montagem de contexto com a política existente, a porta de geração e o adapter HTTP da Responses API usando o modelo configurado inicialmente como `gpt-5-nano`.
2. **Trilha de apresentação:** tratar o objetivo do currículo e a recomendação determinística de layout como fluxo separado. Evoluir os seis layouts por entregas próprias; a primeira versão não deve prometer renderização de um modelo ainda inexistente.

O adapter deve permanecer desabilitável na ausência de credencial/configuração e resultar em indisponibilidade controlada somente para a assistência. A liberação deve depender de consentimento aprovado, testes de privacidade e uma avaliação com massa sintética.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `privacy` | maximized | Envio mínimo, explícito e auditável | Regras documentais e política já disponível. |
| `correctness` | prioritized | Sugestões revisáveis e reprodução da seleção/limites | Contrato novo e telemetria planejada. |
| `security` | prioritized | Chave fora do cliente e do log | Orientação oficial da API. |
| `modifiability` | prioritized | Mudança de provedor/modelo por adapter e configuração | Fronteiras de Clean Architecture e precedente do assistente atual. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `cost-efficiency` | Todo contexto respeita orçamento e teto existentes | O montador resolve a política antes da chamada e registra limites efetivos. |
| `user-value` | Nenhuma alteração sem aceite individual | A API devolve proposta; aplicar usa comandos de edição já autorizados pelo estudante. |
| `reliability` | Erro externo não interrompe fluxo principal | Porta opcional, timeout/erros traduzidos e estado local preservado. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `privacy` | Envio excessivo de contatos/documentos ou conteúdo sem consentimento | Alta | Estudantes e instituição. |
| `security` | Exposição de chave ou dados nos logs/cliente | Alta | Organização e estudantes. |
| `correctness` | Sugestão aplicada como fato, sem rastreabilidade ou revisão | Alta | Estudantes. |
| `user-value` | Texto genérico ou inadequado reduz confiança na ferramenta | Média | Estudantes. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `privacy` | Tela e confirmação adicionais antes da chamada | `delivery-speed` | Aceitável: consentimento é requisito explícito. |
| `modifiability` | Porta, DTOs e doubles extras em vez de uma chamada direta | `simplicity` | Aceitável: há fornecedor externo e alternativa determinística. |
| `correctness` | Proposta estruturada e validações, em vez de texto livre imediato | `time-to-value` | Aceitável: evita persistência/contratos ambíguos. |
| `cost-efficiency` | Truncamento pode omitir item relevante | `user-value` | Aceitável se itens usados/omitidos forem visíveis e selecionáveis. |

## Riscos e efeitos de segunda ordem

- **Qualidade insuficiente do nano:** pode produzir texto genérico ou inferir fatos. Mitigação: prompt proíbe invenção, saída distingue sugestão de evidência, e avaliação humana bloqueia liberação ampla.
- **Ambiguidade de modelo/versão:** aliases podem mudar comportamento. Mitigação: identificador configurável, telemetria do modelo efetivo e decisão posterior sobre versão fixada.
- **Prompt injection na vaga:** descrição de vaga é conteúdo não confiável. Mitigação: separar instruções fixas do conteúdo, declarar que textos de currículo/vaga são dados e não comandos, limitar tamanho e não oferecer ferramentas ao modelo.
- **Repetição/custo abusivo:** endpoint pode ser chamado em ciclo. Mitigação: limite por usuário/ação, timeout, orçamento operacional e métricas; os valores exigem decisão do responsável técnico.
- **Registro excessivo:** telemetria pode reter conteúdo pessoal. Mitigação: registrar IDs/referências, contagens, limites, versão de política, modelo e `x-request-id` quando disponível; não registrar prompt, resposta integral, chave, telefone ou endereço.
- **Catálogo prometido antes de existir:** recomendar layout não renderizável cria expectativa enganosa. Mitigação: listar somente modelos implementados e tratar os demais como entregas independentes.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Contexto exclui PII vedada | Payload capturado por fake do adapter não contém campos vedados | Testes unitários do montador com massa fictícia | Telefone/endereço/documento aparece no payload. |
| Política limita de fato o envio | Soma de caracteres e limites por campo no payload | Testes de borda para ação/modelo e teto | Qualquer payload excede limite efetivo. |
| Consentimento bloqueia chamada | Double do provedor não é invocado sem consentimento | Teste de caso de uso/API | Chamada externa ocorre antes da confirmação. |
| Sugestão não muta currículo | Snapshot do agregado antes/depois | Teste de caso de uso | Referência, texto ou layout muda após solicitar proposta. |
| `gpt-5-nano` é útil no domínio | Amostra sintética rotulada e revisão humana de aderência/não-invenção | Evals offline com critérios definidos | Taxa de invenção ou rejeição supera limiar aprovado. |
| Falhas externas são controladas | Simulações de timeout, 4xx/5xx e resposta inválida | Testes do adapter e da API | Erro interno, vazamento de detalhe ou perda de dados locais. |

## Handoffs e atividades posteriores

- **Produto/privacidade:** aprovar texto de consentimento, base legal, retenção e informação ao estudante sobre o provedor.
- **Backend:** especificar DTOs de entrada/saída e a taxonomia de sugestões; implementar montador de contexto, porta, adapter HTTP, composição por variável de ambiente, timeout e rate limiting.
- **Segurança/operação:** fornecer `OPENAI_API_KEY` por mecanismo de segredos, estabelecer orçamento e alertas; nunca versionar a chave.
- **Frontend:** criar feature FSD de adequação, com seleção de itens, revisão granular, estados acessíveis de carregamento/erro e preservação das edições locais.
- **Qualidade:** criar massa sintética sem PII real, rubrica de avaliação e testes de não envio de dados vedados; decidir snapshot/parâmetros após os resultados.
- **Modelos:** definir roadmap para os seis layouts e a migração do vocabulário atual sem anunciar opções ainda não renderizáveis.

## Síntese

A melhoria semântica deve ser uma assistência opcional e revisável, não uma edição automática. A base já possui uma política de limites segura, mas ela ainda não participa de nenhum fluxo de IA. A decisão recomenda conectá-la a um novo caso de uso autenticado de adequação a vaga, com contexto mínimo e determinístico, porta interna e adapter HTTP da Responses API configurado inicialmente para `gpt-5-nano`. A implementação dos seis layouts não deve bloquear a adequação textual: recomendação de modelo por objetivo é determinística e evolui em uma trilha própria. A principal incerteza é a qualidade/custo efetivos de `gpt-5-nano` sob a rubrica do produto, que requer avaliação antes da ativação ampla.
