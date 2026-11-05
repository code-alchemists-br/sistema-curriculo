---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v002"
status: proposed
created_at: "2026-11-02T23:41:11-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261020-163820-adequacao-semantica-gpt-nano-v001.md
  supersedes: prompts/backend/20261020-163820-adequacao-semantica-gpt-nano-v001.md
  change_type: enrichment
  secondary_change_types: [scope-change]
  decision_impact: strengthened
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20261020-163820-adequacao-semantica-gpt-nano-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d6ea9b1"
      availability: available
    - path: docs/adequacao_semantica_ia.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d6ea9b1"
      availability: available
    - path: src/backend/application/adequacao_semantica.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on d6ea9b1"
      availability: available
    - path: src/backend/infrastructure/integrations/cliente_openai_adequacao.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "contrato ClienteOpenAiAdequacaoHttp e ContextoAdequacaoCurriculoVaga"
      content_state: working-tree
      revision: "working-tree based on d6ea9b1"
      availability: available
    - path: src/backend/api/projeto_academico.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "DTOs, Protocol e criar_router"
      content_state: commit
      revision: "d6ea9b1"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "create_app e inclusão de routers"
      content_state: commit
      revision: "d6ea9b1"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "É uma revisão da linhagem de integração backend e define um contrato HTTP que adapta o caso de uso existente."
classification:
  sphere: engineering
  concerns: [architecture, integration, privacy]
  decision_kind: clarification
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: low
  reversibility: moderate
  risk: high
---

# Análise de decisão — contrato HTTP da adequação semântica de currículo

## Solicitação original

```text
Faça uma análise usando os documentos 'docs/adequacao_semantica_ia.md' e 'docs/modelos_curriculo.md' para implentar a funcionalidade de melhoria de currículo. Vamos usar como modelo o GPT nano e comunicação por API.
```

## Informações complementares

```text
Antes de usar $decision-analysis-v4 vamos definiri. método deve ser post, pois um json contendo partes do currículo vai ser mandado. A rota você pode sugerir. Vamos montar um dto com os campos definidos a serem mandados
```

- A informação complementar pertence à mesma linhagem: resolve a lacuna de contrato HTTP anotada como handoff em `v001`.
- A rota proposta abaixo não recebe `usuario_id`: o principal deve continuar vindo da sessão já instalada na requisição.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Método e rota | DTO/rota eram handoff sem forma pública | `POST /curriculos/{curriculo_id}/adequacoes-semanticas` | O usuário definiu POST e autorizou sugestão de rota | Permite criar adapter de entrada sem inventar protocolo. |
| Corpo de entrada | Apenas intenção interna | DTO com alvo, vaga opcional, referências e consentimento | O caso de uso já exige esses dados | Identidade e conteúdo completo do currículo ficam fora do corpo. |
| Resposta | Proposta estruturada descrita sem wire format | DTO explícito de proposta e sugestões | Evita expor objetos de domínio | Interface pode revisar cada sugestão. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261020-163820-adequacao-semantica-gpt-nano-v001.md` | Primário | Prosa | Documentação | Markdown | Integral | commit `d6ea9b1` |
| `docs/adequacao_semantica_ia.md` | Primário | Prosa | Documentação | Markdown | Integral | commit `d6ea9b1` |
| `src/backend/application/adequacao_semantica.py` | Apoio | Código | Produção | Python | Integral | working tree baseado em `d6ea9b1` |
| `src/backend/infrastructure/integrations/cliente_openai_adequacao.py` | Apoio | Código | Produção | Python | Contrato do cliente | working tree baseado em `d6ea9b1` |
| `src/backend/api/projeto_academico.py` | Apoio | Código | Produção | Python | DTO, Protocol e router | commit `d6ea9b1` |
| `src/backend/api/factory.py` | Apoio | Código | Produção | Python | Composição de routers | commit `d6ea9b1` |

### Limites da evidência dos artefatos

- `src/backend/application/adequacao_semantica.py` e o cliente OpenAI estão no working tree, ainda sem commit; seus contratos foram usados somente como evidência da interface já existente.
- Esta revisão não decide composição de credenciais, timeout, limite de taxa, telemetria, persistência ou frontend.

## Problema enriquecido

### Resultado desejado

Expor uma requisição autenticada que inicie uma proposta revisável de adequação de uma versão de currículo a uma vaga, sem aceitar identidade do estudante nem o currículo completo no JSON.

### Atores e interesses

- **Estudante:** informa cargo, vaga, consentimento e quais itens já incluídos na versão devem ser usados.
- **API:** valida a forma do JSON, usa a sessão para a identidade e traduz o resultado do caso de uso.
- **Application:** valida propriedade, limites e consentimento; não conhece HTTP.
- **Frontend:** recebe proposta e itens efetivamente usados para revisão, sem receber segredo do provedor.

### Evidências e fatos observados

1. A documentação exige consentimento explícito, contexto mínimo e revisão sem edição automática.
2. `SolicitarAdequacaoCurriculoVagaEntrada` já recebe `usuario_id`, `curriculo_id`, `cargo_alvo`, `descricao_vaga`, referências ordenadas e consentimento.
3. `PropostaAdequacaoCurriculoVaga` já preserva modelo, versão da política, referências utilizadas e sugestões.
4. Os routers existentes recebem o principal de `request.state.usuario_id`, e a fábrica recebe executores injetados.

### Hipóteses

- H1: o frontend já possui UUIDs dos itens da versão e pode enviá-los na ordem de preferência do estudante.
- H2: `descricao_vaga: null` representa ausência da descrição; string vazia deve ser rejeitada pelo domínio.

### Perguntas em aberto

- Nenhuma bloqueia o contrato inicial. O texto legal de consentimento, retenção, orçamento, timeout e disponibilidade do provedor continuam handoffs da `v001`.

### Escopo

- `POST /curriculos/{curriculo_id}/adequacoes-semanticas`.
- Identidade exclusivamente derivada de sessão autenticada.
- DTO de entrada:

```json
{
  "cargo_alvo": "Desenvolvedora Backend",
  "descricao_vaga": "Opcional; quando presente, descreve a vaga.",
  "referencias_selecionadas": [
    {"tipo": "experiencia", "id": "UUID"},
    {"tipo": "competencia", "id": "UUID"}
  ],
  "consentimento_explicito": true
}
```

- `tipo` aceita somente `experiencia`, `projeto` ou `competencia`; `id` é UUID. A ordem da lista é preservada. Campos desconhecidos são ignorados conforme convenção atual dos DTOs da API.
- DTO de resposta HTTP 200:

```json
{
  "modelo": "gpt-5-nano",
  "versao_politica": "1",
  "referencias_utilizadas": [{"tipo": "experiencia", "id": "UUID"}],
  "sugestoes": [
    {
      "codigo": "EXPERIENCIA_1",
      "tipo": "experiencia",
      "referencia_item": {"tipo": "experiencia", "id": "UUID"},
      "texto_sugerido": "...",
      "justificativa": "..."
    }
  ]
}
```

- Respostas: 401 sem principal; 404 para versão ou item ausente/alheio; 422 para formato inválido ou invariante de domínio; 503 quando o executor não estiver composto ou o provedor estiver indisponível, sem detalhes externos.

### Fora do escopo

- Aceitar `usuario_id`, conteúdo integral do currículo, telefone, endereço, documentos, credenciais ou modelo no corpo.
- Aplicar ou persistir sugestões, criar chat, retornar payload bruto da OpenAI, alterar autenticação/sessão, rate limiting ou timeout.

### Critérios de sucesso

- O handler cria exatamente a entrada interna a partir de rota, DTO e sessão.
- O JSON não permite escolher o estudante ou enviar conteúdo profissional livre.
- A resposta usa DTOs públicos e a proposta permanece revisável.
- Testes unitários chamam o handler com executor e `Request` sintéticos, sem servidor, rede ou banco.

## Restrições aplicáveis

- HTTP permanece na API; domínio e Application não importam FastAPI nem Pydantic.
- O consentimento é transmitido ao caso de uso, que continua como fonte autoritativa da regra.
- As referências aceitas refletem somente os três tipos que o contexto interno atualmente materializa.

## Classificação comentada

É uma decisão de engenharia, integração e privacidade: define a fronteira pública que controla a identidade e minimiza os dados enviados ao fluxo de IA. O risco é alto porque uma forma inadequada poderia ampliar a exposição de dados pessoais.

## Decisão de roteamento

`prompts/backend` preserva a linhagem anterior e contém decisões de contratos e integração de backend. `prompts/requisitos` foi considerado por tocar a jornada do estudante, mas não é o objetivo principal; `prompts/revisao` não é escolhido apenas pelo modo de revisão.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Privacidade | 1 | Sem currículo integral ou identidade no corpo | A IA recebe somente o conteúdo selecionado pelo caso de uso. |
| Correção | 1 | Rota e DTO mapeiam integralmente o comando existente | Evita adaptar regras na API. |
| Interoperabilidade | 2 | Contrato explícito e estável para frontend | A revisão granular depende de campos previsíveis. |
| Modificabilidade | 2 | Caminho centrado no currículo e resposta desacoplada do provedor | Mantém troca de gerador sem mudar cliente. |

## Alternativas consideradas

**A — rota aninhada na versão, recomendada.** `POST /curriculos/{curriculo_id}/adequacoes-semanticas`, com principal da sessão e corpo mínimo.

**B — rota sob estudante.** `POST /estudantes/{usuario_id}/curriculos/{curriculo_id}/adequacoes-semanticas`.

**C — rota global com IDs no corpo.** `POST /adequacoes-semanticas`, contendo `usuario_id` e `curriculo_id`.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Privacidade | 1 | +2 | 0 | -2 | alta | A não expõe nem aceita o estudante no caminho/corpo. |
| Correção | 1 | +2 | +1 | -1 | alta | A corresponde ao comando e à diretriz de derivar sessão. |
| Interoperabilidade | 2 | +2 | 0 | +1 | média | A nomeia claramente o recurso que recebe a proposta. |
| Modificabilidade | 2 | +2 | 0 | -1 | média | A evita campos redundantes e compatibilidade legada. |

## Histórico e decisão atual

### Decisão da versão anterior

`v001` recomendou DTO e rota autenticada, mas deixou sua especificação como handoff.

### Decisão recomendada nesta versão

Adotar a Alternativa A e os DTOs definidos no escopo. A API deve derivar `usuario_id` da sessão, converter referências `{tipo, id}` em value objects e invocar `SolicitarAdequacaoCurriculoVaga` injetado. A resposta omite `curriculo_id`, pois já está no caminho, e expõe somente modelo, versão de política, referências efetivamente usadas e sugestões revisáveis.

### Impacto da revisão

A decisão é fortalecida: a lacuna que impedia o adapter de entrada foi eliminada sem mudar regras de domínio ou a integração externa escolhida.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Privacidade | maximized | Identidade e dados vedados ficam fora do payload | Documentação e comando interno. |
| Correção | prioritized | Uma única representação de referências atravessa a borda | Tipos existentes no domínio e Application. |
| Interoperabilidade | prioritized | Frontend recebe contrato explícito para revisão | DTO de resposta proposto. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Modificabilidade | Troca de provedor não altera a rota | DTO não revela o adapter OpenAI. |
| Simplicidade | Um comando por versão de currículo | O path contém somente `curriculo_id`. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Privacidade | Cliente envia dados ou identidade desnecessários | Alta | Estudantes e instituição. |
| Correção | API duplica ou contorna regras do caso de uso | Alta | Estudantes e manutenção. |
| Interoperabilidade | Frontend depende de forma implícita do domínio/provedor | Média | Frontend e backend. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Privacidade | Converter UUIDs tipados no adapter | Simplicidade | Aceitável: evita payload livre de currículo. |
| Correção | DTOs explícitos de pedido e resposta | Delivery-speed | Aceitável: estabiliza a integração. |

## Riscos e efeitos de segunda ordem

- O frontend pode enviar uma referência obsoleta; o caso de uso deve continuar a ocultar ausência/propriedade alheia em 404.
- Uma descrição extensa pode ser aceita estruturalmente; os limites efetivos continuam no caso de uso e política de servidor.
- HTTP 503 não distingue credencial ausente, rede ou resposta inválida: essa generalização é intencional para não expor detalhes operacionais.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Sessão é a única fonte do estudante | Handler recebe UUID de `request.state` | Teste unitário direto da rota | Campo de usuário aparece no DTO. |
| Corpo é mínimo | Executor spy observa a entrada | Teste unitário com DTO e Request sintéticos | Conteúdo livre de currículo alcança Application. |
| Proposta é revisável | Resposta contém sugestões sem operação de escrita | Teste unitário de presenter | Handler chama persistência ou retorna entidade. |
| Falhas não vazam detalhes | Exceções conhecidas viram mensagens genéricas | Testes unitários da rota | Payload do provedor aparece em HTTP. |

## Handoffs e atividades posteriores

- **`$backend-adapters-drivers-v2`:** implementar router, DTOs, presenter e binding na factory com executor injetado; criar somente seus testes unitários.
- **`$backend-domain-orchestration-v2`:** somente se a taxonomia interna ou o contrato de geração precisar mudar; não é necessário para esta rota.
- **`$integration-system-testing-v1`:** criar testes de API/ASGI, composição com sessão e integração real/simulada do provedor.
- **Operação e segurança:** compor segredo, timeout, rate limiting, orçamento, retenção e telemetria aprovada.
- **Frontend:** selecionar referências da versão, coletar consentimento e revisar a resposta sem aplicar automaticamente sugestões.

## Síntese

O contrato público agora é suficientemente específico para o adapter de entrada: `POST /curriculos/{curriculo_id}/adequacoes-semanticas`, sessão como fonte de identidade e corpo limitado a objetivo, vaga, referências e consentimento. A escolha reduz exposição de dados, preserva o caso de uso como autoridade de regras e oferece ao frontend uma proposta tipada para revisão. A principal incerteza restante não bloqueia o adapter: a política operacional de credencial, timeout e disponibilidade do provedor.
