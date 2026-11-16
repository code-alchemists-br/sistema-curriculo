---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v004"
status: proposed
created_at: "2026-11-05T18:12:01-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261020-163820-adequacao-semantica-gpt-nano-v001.md
  supersedes: prompts/backend/20261102-235645-adequacao-semantica-gpt-nano-v003.md
  change_type: reassessment
  secondary_change_types: [scope-change]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20261102-235645-adequacao-semantica-gpt-nano-v003.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: bd36f0d
      availability: available
    - path: docs/modelos_curriculo.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: bd36f0d
      availability: available
    - path: docs/adequacao_semantica_ia.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: bd36f0d
      availability: available
    - path: src/backend/application/adequacao_semantica.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "SolicitarAdequacaoCurriculoVagaEntrada, ContextoAdequacaoCurriculoVaga, GeradorPropostaAdequacao e SolicitarAdequacaoCurriculoVaga (linhas 1-190)"
      content_state: commit
      revision: bd36f0d
      availability: available
    - path: src/backend/application/recomendacao_modelo_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: bd36f0d
      availability: available
    - path: src/backend/domain/recomendacao_modelo_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: bd36f0d
      availability: available
    - path: src/backend/api/adequacao_semantica.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: bd36f0d
      availability: available
    - path: src/backend/infrastructure/integrations/cliente_openai_adequacao.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "montar_requisicao_openai, mapeamento de resposta e ClienteOpenAiAdequacaoHttp (linhas 1-250)"
      content_state: commit
      revision: bd36f0d
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/frontend]
  confidence: high
  rationale: "A decisão revisa contratos, casos de uso, porta de IA e adaptador do backend; requisitos e interface são consumidores da decisão."
classification:
  sphere: engineering
  concerns: [architecture, integration, privacy]
  decision_kind: change
  scope: system
  lifecycle: evolution
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: high
---

# Análise de decisão — recomendação de modelo por IA no fluxo de adequação

## Solicitação original

```text
Faça uma análise usando os documentos 'docs/adequacao_semantica_ia.md' e 'docs/modelos_curriculo.md' para implentar a funcionalidade de melhoria de currículo. Vamos usar como modelo o GPT nano e comunicação por API.
```

## Informações complementares

```text
Antes de usar $decision-analysis-v4 vamos definiri. método deve ser post, pois um json contendo partes do currículo vai ser mandado. A rota você pode sugerir. Vamos montar um dto com os campos definidos a serem mandados
```

```text
Nós precisamos de duas rotas de entrada na verdade. Uma rota vai servir para sugerir com base no currículo algum modelo de currículo como ATS simples, Criativo, Acadêmico/pesquisador etc conforme o doc 'docs\modelos_curriculo.md'. Outra rota terá por objetivo adequar o currículo à uma determinada vaga. Atualize a decisão com os ajustes de todas as camadas necessárias a mais isso em 'prompts\backend\20261102-234111-adequacao-semantica-gpt-nano-v002.md'
```

```text
A sugestão de modelos de currículos deve ser feita por IA também usando mesmo dto que o fluxo de adequação do currículo à vaga usa.
```

- Interpretação: “mesmo DTO” significa reutilizar o corpo HTTP `SolicitarAdequacaoCurriculoVagaRequisicao` e sua tradução para `SolicitarAdequacaoCurriculoVagaEntrada`, incluindo cargo-alvo, descrição opcional da vaga, referências selecionadas e consentimento; não significa devolver uma proposta textual de adequação quando a intenção é recomendar um modelo.

## Mudanças desde a versão anterior

| Elemento | v003 | v004 | Motivo | Impacto |
|---|---|---|---|---|
| Origem da recomendação | Política local objetivo→modelo | IA com contexto profissional autorizado | Nova informação explícita do usuário | A política determinística deixa de decidir o modelo. |
| Entrada | `objetivo` em DTO próprio | Mesmo DTO da adequação à vaga | Reuso explícito solicitado | A categoria `ObjetivoCurriculo` deixa de ser entrada obrigatória. |
| Dados enviados | Nenhum dado ao provedor | Vaga e itens profissionais já selecionados e limitados | A IA deve fundamentar a sugestão | Consentimento, minimização e limites passam a valer também para recomendação. |
| Saída | `modelo_recomendado` e justificativa local | Modelo sugerido, justificativa e rastreabilidade da política/IA | Separar decisão revisável de alteração | Não aplicar `layout` automaticamente. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261102-235645-adequacao-semantica-gpt-nano-v003.md` | Primário | Prosa | Documentação | Markdown | Integral | commit `bd36f0d` |
| `docs/modelos_curriculo.md` | Apoio | Prosa | Documentação | Markdown | Integral | commit `bd36f0d` |
| `docs/adequacao_semantica_ia.md` | Apoio | Prosa | Documentação | Markdown | Integral | commit `bd36f0d` |
| `src/backend/application/adequacao_semantica.py` | Primário | Código-fonte | Produção | Python | Entrada, contexto, porta e caso de uso | commit `bd36f0d` |
| `src/backend/application/recomendacao_modelo_curriculo.py` | Primário | Código-fonte | Produção | Python | Integral | commit `bd36f0d` |
| `src/backend/domain/recomendacao_modelo_curriculo.py` | Primário | Código-fonte | Produção | Python | Integral | commit `bd36f0d` |
| `src/backend/api/adequacao_semantica.py` | Apoio | Código-fonte | Produção | Python | Integral | commit `bd36f0d` |
| `src/backend/infrastructure/integrations/cliente_openai_adequacao.py` | Apoio | Código-fonte | Produção | Python | Montagem, mapeamento e cliente | commit `bd36f0d` |

### Limites da evidência dos artefatos

- Não foi definido qual modelo de currículo deve ser usado quando a saída da IA for inválida, indisponível ou apontar modelo ainda não renderizável.
- O adaptador atual tem schema de saída exclusivo para sugestões de adequação; ele não pode ser reutilizado literalmente para uma recomendação sem um contrato de saída adicional.

## Problema enriquecido

### Resultado desejado

Permitir que o estudante solicite, com o mesmo contexto mínimo e consentido de adequação à vaga, uma recomendação de modelo de currículo produzida por IA e revisável antes de qualquer escolha ou alteração de layout.

### Atores e interesses

- **Estudante:** obtém uma recomendação contextualizada e continua escolhendo o modelo final.
- **Backend:** evita duplicar DTO, autorização, seleção de itens e política de limites; valida a saída externa.
- **Produto:** mantém o catálogo documentado como limite de opções válidas.
- **Provedor de IA:** recebe exclusivamente o contexto autorizado para a ação.

### Evidências e fatos observados

1. O DTO atual já contém cargo-alvo, descrição de vaga, referências profissionais escolhidas e consentimento explícito.
2. A Application valida propriedade, materializa somente experiências, projetos e competências, e limita o contexto antes de chamar a porta de IA.
3. O documento de adequação exige contexto específico, minimização e consentimento para cada ação de IA.
4. O catálogo documental define seis modelos e preserva a decisão final do estudante.
5. A implementação de v003 recomenda por tabela determinística e não chama a IA; essa decisão é superada pela nova solicitação.

### Hipóteses

- H1: `cargo_alvo`, vaga e itens selecionados oferecem sinal suficiente para uma primeira recomendação de apresentação.
- H2: a IA pode ser instruída e validada para retornar apenas valores do catálogo efetivamente disponibilizado.
- H3: o consentimento existente cobre explicitamente a nova finalidade de recomendação; caso a tela ou aviso atual cite somente “adequação”, ele deverá ser atualizado antes da entrega.

### Perguntas em aberto

- O consentimento deve ser granular por ação (“adequar” e “recomendar modelo”) ou o texto atual já as abrange de forma clara?
- Quais dos seis modelos possuem prévia e exportação disponíveis para compor o enum de saída permitido?

### Escopo

- Manter duas rotas POST e duas intenções: adequar texto à vaga e recomendar modelo.
- Fazer `POST /curriculos/{curriculo_id}/recomendacao-modelo` aceitar exatamente `SolicitarAdequacaoCurriculoVagaRequisicao`.
- Traduzir ambas as rotas para a mesma `SolicitarAdequacaoCurriculoVagaEntrada` e compartilhar a preparação autorizada do contexto.
- Criar caso de uso e porta específicos para recomendação por IA, com resposta estruturada `modelo_recomendado` e `justificativa`; aceitar somente modelos do catálogo disponível.
- Reutilizar o cliente OpenAI apenas após generalizá-lo para ações e schemas distintos, sem fazer a Application depender de HTTP ou OpenAI.

### Fora do escopo

- Aplicar automaticamente o modelo, persistir objetivo, inferir dados não selecionados, enviar contatos/documentos ou alterar o currículo.
- Alterar catálogo, criar renderizadores, decidir o texto legal do consentimento ou unificar as respostas das duas intenções.

### Critérios de sucesso

- Ambas as rotas aceitam o mesmo contrato de requisição e derivam a identidade exclusivamente da sessão.
- Somente itens próprios, selecionados e limitados chegam ao provedor nas duas ações.
- A saída de recomendação é um modelo permitido e justificativa, validada antes de chegar à API.
- Falha ou indisponibilidade da IA não muda a versão nem seleciona modelo silenciosamente.

## Restrições aplicáveis

- Clean Architecture: preparação de contexto e contratos internos não dependem de FastAPI, HTTP ou OpenAI.
- O DTO público compartilhado não deve transportar `usuario_id`, conteúdo livre de currículo, limites ou identificador de modelo externo.
- A recomendação por IA exige consentimento explícito, política de limites e filtros de privacidade iguais aos da adequação.
- A IA só pode recomendar modelo pertencente ao subconjunto renderizável e exposto pelo sistema.
- A resposta permanece orientação revisável, não comando de alteração do layout.

## Classificação comentada

É uma mudança de engenharia de integração: altera a fonte da recomendação e reutiliza o pipeline de IA, com risco de privacidade se o reuso ignorar a finalidade de consentimento ou o catálogo fechado.

## Decisão de roteamento

`prompts/backend` preserva a linhagem e contém os contratos, casos de uso, portas e adaptador afetados. `prompts/requisitos` e `prompts/frontend` recebem handoffs para consentimento e apresentação, mas não são o núcleo da decisão.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Correção | 1 | Modelo sempre pertence ao catálogo permitido | A IA não pode inventar ou aplicar layout. |
| Privacidade | 1 | Reutilizar apenas contexto já autorizado e limitado | A nova finalidade não amplia os dados enviados. |
| Modificabilidade | 2 | Um preparador de contexto, intenções e respostas separadas | Evita dois fluxos de autorização divergentes. |
| User-value | 2 | Recomendação contextualizada e justificável | A escolha continua informada e livre. |

## Alternativas consideradas

**A — Reutilizar o DTO e a preparação de contexto; criar caso de uso, porta e schema de saída próprios para recomendação por IA. Recomendada.** A entrada e as salvaguardas são comuns, mas a intenção e o resultado continuam explícitos.

**B — Substituir a política local por uma chamada de IA usando somente `objetivo`.** Não atende ao reuso do DTO e perde o contexto profissional selecionado que a solicitação exige.

**C — Fazer a própria rota de adequação devolver também o modelo recomendado.** Mistura duas intenções, torna a resposta maior e impede indisponibilidade/revisão independentes.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Correção | 1 | +2 | 0 | -1 | alta | Schema dedicado e catálogo fechado. |
| Privacidade | 1 | +2 | +1 | -1 | alta | Preparação já minimiza e exige consentimento. |
| Modificabilidade | 2 | +2 | 0 | -2 | alta | Compartilha preparação, não resultados. |
| User-value | 2 | +2 | 0 | +1 | média | Contexto da vaga e itens melhora justificativa. |

## Histórico e decisão atual

### Decisão da versão anterior

`v003` manteve a recomendação de modelo local, determinística e baseada no objetivo, reservando a IA à adequação textual para vaga.

### Decisão recomendada nesta versão

Adotar a alternativa A. A recomendação de modelo passa a usar IA e o mesmo DTO de adequação. As duas rotas devem traduzir esse DTO para a mesma entrada de Application e compartilhar uma unidade interna de autorização, consulta, materialização e limitação de contexto. Após esse ponto, cada intenção segue por caso de uso e porta próprios: adequação produz sugestões textuais; recomendação produz um único modelo do catálogo permitido e justificativa. O adaptador OpenAI deve receber uma ação explícita e escolher prompt/schema de saída correspondente; não deve reutilizar o schema de sugestões textuais para representar modelo.

### Impacto da revisão

Revisada: a recomendação deixa de ser puramente determinística e passa a depender da infraestrutura de IA, com os mesmos controles de dados da adequação. Permanecem inalteradas a autonomia do estudante, a ausência de alteração automática e a separação entre as duas respostas.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Correção | maximized | Somente modelos reconhecidos chegam ao cliente | Schema e enum fechados no adaptador/domínio. |
| Privacidade | prioritized | Não há novo conjunto de dados enviado | DTO e materialização existentes. |
| Modificabilidade | prioritized | Regras de contexto não se duplicam | Handoff de extração do preparador compartilhado. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| User-value | Modelo e motivo podem ser revisados | Resposta tipada, sem atualização automática. |
| Confiabilidade | Falha externa é explícita | 503 por indisponibilidade; nenhuma seleção implícita. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Correção | Modelo inexistente ou não renderizável é sugerido | Alta | Estudantes e suporte. |
| Privacidade | Dados além dos itens selecionados chegam ao provedor | Alta | Estudantes. |
| Modificabilidade | Fluxos de filtro e limite divergem | Média | Backend e manutenção. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Correção | Novo schema de resposta e validação de catálogo | Delivery-speed | Aceitável: protege a fronteira externa. |
| Privacidade | Consentimento e aviso podem requerer revisão de interface | Simplicidade | Aceitável: a finalidade agora inclui recomendação. |
| Modificabilidade | Extração do preparador compartilhado | Delivery-speed | Aceitável: evita duplicação de salvaguardas. |

## Riscos e efeitos de segunda ordem

- O modelo pode justificar uma recomendação de forma persuasiva mas fraca; a interface deve explicitar que é sugestão e permitir escolher qualquer modelo.
- A dependência da IA torna uma função antes disponível offline sujeita a custo, latência e 503.
- Um consentimento genérico pode não comunicar suficientemente a finalidade de escolha de apresentação; isso exige validação de produto/privacidade.
- O reuso literal da classe `ClienteOpenAiAdequacaoHttp` sem generalização acoplaria a recomendação ao schema errado.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Ambas as rotas usam a mesma entrada | Teste de handlers e spies | Comparar entradas enviadas aos executores | DTOs começam a divergir. |
| Nenhum dado extra é enviado | Captura de contexto/payload com double | Teste unitário do preparador e adaptador | Contato, documento ou item não selecionado aparece. |
| Modelo é sempre válido | Teste de schema e enum | Simular resposta inventada da IA | Resposta externa inválida chega à API. |
| Consentimento é compreensível | Revisão de UX e texto legal | Teste de aceitação | Usuário não identifica que recomendação usa IA. |

## Handoffs e atividades posteriores

- **Backend/domain:** retirar ou rebaixar `PoliticaRecomendacaoModeloCurriculo` como fallback somente se uma decisão posterior o autorizar; definir resultado tipado de recomendação por IA e enum do catálogo disponível.
- **Backend/application:** extrair a preparação comum de `SolicitarAdequacaoCurriculoVagaEntrada`; criar `RecomendarModeloCurriculoComIa` e a porta de geração estruturada, sem acoplar à infraestrutura.
- **Backend/adapters-drivers:** expor a rota de recomendação com o DTO compartilhado; generalizar o cliente OpenAI por ação e schema; mapear falhas em 401/404/422/503.
- **Testes:** cobrir identidade, consentimento, seleção, limites, catálogo, resposta externa inválida e ausência de escrita para ambas as intenções.
- **Frontend/produto:** reaproveitar o formulário de contexto, diferenciar as duas ações e revisar a redação do consentimento.

## Síntese

A recomendação de modelo deve passar a usar IA com exatamente o DTO de adequação, mas não deve fundir as duas intenções. A entrada e a preparação segura são compartilhadas; o resultado, a porta e o schema de cada ação permanecem específicos. A principal incerteza é se o consentimento atual comunica essa finalidade adicional e quais modelos estão efetivamente renderizáveis.
