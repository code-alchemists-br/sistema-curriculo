---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v003"
status: proposed
created_at: "2026-11-02T23:56:45-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261020-163820-adequacao-semantica-gpt-nano-v001.md
  supersedes: prompts/backend/20261102-234111-adequacao-semantica-gpt-nano-v002.md
  change_type: scope-change
  secondary_change_types: [enrichment]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20261102-234111-adequacao-semantica-gpt-nano-v002.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on d6ea9b1"
      availability: available
    - path: docs/modelos_curriculo.md
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
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d6ea9b1"
      availability: available
    - path: src/backend/domain/modelo_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "d6ea9b1"
      availability: available
    - path: src/backend/domain/curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "Curriculo e edição de layout"
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
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "injeção de executores e inclusão de routers"
      content_state: commit
      revision: "d6ea9b1"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/frontend]
  confidence: high
  rationale: "A revisão define núcleo, contratos HTTP e composição de backend; a interface é handoff."
classification:
  sphere: engineering
  concerns: [architecture, integration, user-experience]
  decision_kind: scope-change
  scope: system
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: high
---

# Análise de decisão — recomendação de modelo e adequação a vaga

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

- Interpretação: a recomendação segue a seleção determinística orientada por objetivo definida no documento; a versão é usada para propriedade, não para inferência generativa do perfil.

## Mudanças desde a versão anterior

| Elemento | v002 | v003 | Motivo | Impacto |
|---|---|---|---|---|
| Entradas | Só adequação à vaga | Duas rotas POST separadas | O usuário separou apresentação e adequação | Nova fatia de domínio, Application, API e composição. |
| Modelo | Trilha coordenada sem endpoint | Recomendação determinística por objetivo | A documentação fornece a tabela de mapeamento | Não usa OpenAI nem consentimento. |
| Catálogo | Não tratado no contrato | Reconciliação exigida | Enum contém `compacto`, ausente no catálogo de seis modelos | Não expor modelo sem renderizador confirmado. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261102-234111-adequacao-semantica-gpt-nano-v002.md` | Primário | Prosa | Documentação | Markdown | Integral | working tree baseado em `d6ea9b1` |
| `docs/modelos_curriculo.md` | Primário | Prosa | Documentação | Markdown | Integral | commit `d6ea9b1` |
| `docs/adequacao_semantica_ia.md` | Apoio | Prosa | Documentação | Markdown | Integral | commit `d6ea9b1` |
| `src/backend/domain/modelo_curriculo.py` | Apoio | Código | Produção | Python | Integral | commit `d6ea9b1` |
| `src/backend/domain/curriculo.py` | Apoio | Código | Produção | Python | Seleção e layout | commit `d6ea9b1` |
| `src/backend/application/adequacao_semantica.py` | Apoio | Código | Produção | Python | Integral | working tree baseado em `d6ea9b1` |
| `src/backend/api/factory.py` | Apoio | Código | Produção | Python | Composição | commit `d6ea9b1` |

### Limites da evidência dos artefatos

- A documentação não define heurística para inferir objetivo a partir dos itens; por isso o objetivo deve entrar no DTO.
- Não há evidência de renderização para todos os modelos. A composição deve disponibilizar somente valores que tenham prévia/exportação.

## Problema enriquecido

### Resultado desejado

Permitir que o estudante peça, para uma versão própria, orientação de apresentação e, separadamente, proposta textual para uma vaga. Nenhuma das duas intenções altera o layout ou conteúdo automaticamente.

### Atores e interesses

- **Estudante:** informa objetivo para receber orientação e consente antes da adequação a vaga.
- **Backend:** protege propriedade, mantém a recomendação explicável e limita a IA à escrita.
- **Frontend:** apresenta motivo, modelos disponíveis e proposta revisável.

### Evidências e fatos observados

1. O documento mapeia objetivos a ATS simples, Moderno, Criativo, Acadêmico/pesquisador e Primeiro emprego; administrativo aceita ATS simples ou Profissional clássico.
2. O objetivo orienta, mas não restringe, a seleção final do estudante.
3. A análise `v001` separa recomendação de apresentação da IA e não atribui ao modelo externo a decisão de layout.
4. `Curriculo` não possui objetivo persistido; o primeiro fluxo pode recebê-lo sem salvar.
5. `SolicitarAdequacaoCurriculoVaga` já representa a segunda intenção.

### Hipóteses

- H1: o frontend consegue enviar uma categoria de objetivo no pedido de recomendação.
- H2: para administrativo/corporativo, ATS simples é a recomendação única inicial e Profissional clássico aparece como alternativa explicada.

### Perguntas em aberto

- `compacto` é legado, alias ou deve ser removido? É obrigatório reconciliar essa divergência antes de expor o catálogo final.
- Uma heurística futura baseada nos itens requer nova decisão, pois não está no documento.

### Escopo

- **Rota 1:** `POST /curriculos/{curriculo_id}/recomendacao-modelo`.
  - Corpo: `{"objetivo": "primeiro_emprego" | "tecnologia" | "administrativo_corporativo" | "criativo_design" | "academico_pesquisador" | "outro"}`.
  - Resposta: `{"modelo_recomendado": "...", "justificativa": "..."}`.
  - Usa sessão para o estudante, verifica a versão e recomenda; não chama OpenAI, não persiste nem altera `layout`.
- **Rota 2:** `POST /curriculos/{curriculo_id}/adequacoes-semanticas`.
  - Mantém o DTO de `v002`: `cargo_alvo`, `descricao_vaga` opcional, `referencias_selecionadas` tipadas e `consentimento_explicito`.
  - Devolve proposta revisável, sem alteração do currículo.
- **Domain:** `ObjetivoCurriculo`, política pura objetivo→modelo, resultado tipado e reconciliação do enum `ModeloCurriculo` com catálogo/renderizadores.
- **Application:** `RecomendarModeloCurriculo` deve verificar propriedade por `RepositorioCurriculo` e delegar a política; permanece separado de `SolicitarAdequacaoCurriculoVaga`.
- **API:** DTOs, presenters, routers e respostas 401, 404, 422 e 503 quando aplicável; `usuario_id` nunca integra o JSON.
- **Infrastructure/composição:** factory injeta os dois executores. Somente adequação recebe cliente OpenAI; recomendação não usa adapter externo.
- **Frontend:** coleta objetivo, exibe justificativa e modelos renderizáveis, e mantém revisão granular da adequação.
- **Testes:** unitários de política, caso de uso e adapters; ASGI, persistência e OpenAI real são testes superiores.

### Fora do escopo

- Alterar automaticamente modelo/layout, persistir objetivo, enviar currículo ao provedor para escolher visual, criar renderizadores ou tipos acadêmicos ausentes.
- Credenciais, timeout, rate limiting, telemetria, autenticação nova e avaliações do modelo.

### Critérios de sucesso

- As rotas possuem contrato, caso de uso e responsabilidade independentes.
- A recomendação reproduz a tabela documental, é explicável e não faz I/O externo além da consulta da versão.
- A adequação preserva consentimento, minimização e revisão humana.
- Nenhuma rota aceita identidade do estudante no cliente ou muda a versão implicitamente.

## Restrições aplicáveis

- Clean Architecture: regras de recomendação no núcleo; FastAPI e OpenAI somente nas bordas.
- A recomendação é determinística; a IA só sugere texto para a vaga.
- O catálogo público deve ser subconjunto de modelos renderizáveis enquanto houver lacunas de visualização.

## Classificação comentada

É uma mudança de escopo de engenharia, integração e experiência de uso. A separação evita que uma escolha visual seja opaca ou amplie a transferência de dados pessoais.

## Decisão de roteamento

`prompts/backend` preserva a linhagem e concentra os efeitos em domínio, Application, API e composição. `prompts/requisitos` e `prompts/frontend` são handoffs, não o destino principal.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Correção | 1 | IA não escolhe layout; política reflete a tabela | Evita critério opaco. |
| User-value | 1 | Explicação e liberdade de escolha | Orienta sem restringir. |
| Modificabilidade | 2 | Casos de uso independentes | Evolui IA e catálogo separadamente. |
| Privacidade | 2 | Recomendação sem envio ao provedor | Evita transferência desnecessária. |

## Alternativas consideradas

**A — duas rotas e política determinística por objetivo, recomendada.**

**B — uma rota de IA que escolhe modelo e adequa vaga.** Viola a separação documental e amplia exposição de dados.

**C — seleção automática de layout durante criação/edição.** Remove a decisão explícita do estudante.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | A | B | C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Correção | 1 | +2 | -1 | -2 | alta | Documento separa layout e IA. |
| User-value | 1 | +2 | +1 | -1 | alta | Recomendação explicada e reversível. |
| Modificabilidade | 2 | +2 | -1 | 0 | alta | Contratos e casos separados. |
| Privacidade | 2 | +2 | -2 | +1 | alta | Não transmite perfil para layout. |

## Histórico e decisão atual

### Decisão da versão anterior

`v002` definiu apenas a entrada de adequação a vaga e manteve apresentação como trilha coordenada.

### Decisão recomendada nesta versão

Adotar A. A recomendação de modelo torna-se fluxo local, determinístico e explicável, acionado por objetivo explícito. A adequação à vaga mantém integralmente o contrato de `v002` e é a única rota que usa IA. Ambas são `POST`, aninhadas na versão de currículo e autenticadas pela sessão.

### Impacto da revisão

Revisada: adiciona segunda rota e exige alterações coordenadas de domínio, Application, API e composição, preservando a decisão de não usar IA para layout.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Correção | maximized | Objetivo mapeado de forma auditável | Tabela de seleção documental. |
| User-value | prioritized | Motivo claro e escolha final livre | Princípios de implementação. |
| Privacidade | prioritized | Nenhum perfil enviado ao provedor | Política local. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como atende |
|---|---|---|
| Modificabilidade | Trocar gerador não muda recomendação | Casos de uso independentes. |
| Simplicidade | Um POST por intenção | Paths e DTOs distintos. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Correção | Layout recomendado sem regra documentada | Alta | Estudantes e manutenção. |
| Privacidade | Perfil enviado para escolher apresentação | Alta | Estudantes. |
| User-value | Layout aplicado sem aceite | Alta | Estudantes. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Correção | Nova política e caso de uso | Delivery-speed | Aceitável: a regra é explícita. |
| User-value | Campo de objetivo e justificativa na UI | Simplicidade | Aceitável: preserva autonomia. |

## Riscos e efeitos de segunda ordem

- Recomendar modelo sem renderizador cria expectativa incorreta; filtrar catálogo até a entrega visual.
- Persistir objetivo depois exigirá decisão de schema e migração; agora é efêmero.
- Heurística baseada em itens do perfil requer nova análise.

## Validação da decisão

| Resultado | Evidência | Método | Sinal para revisar |
|---|---|---|---|
| Objetivo gera modelo documentado | Tabela de casos | Teste unitário da política | Divergência da tabela. |
| Recomendação não altera versão | Snapshot do agregado | Teste do caso de uso | Repository recebe atualização. |
| Rotas não se misturam | Spies dos executores | Testes unitários de handlers | Recomendação chama OpenAI. |
| Modelo recomendado é exibível | Inventário de renderizadores | Teste superior | Catálogo promete visual inexistente. |

## Handoffs e atividades posteriores

- **`$backend-domain-orchestration-v2`:** implementar `ObjetivoCurriculo`, política, resultado e `RecomendarModeloCurriculo`; reconciliar `ModeloCurriculo` e catálogo.
- **`$backend-adapters-drivers-v2`:** implementar ambos routers, DTOs, presenters e bindings; não inserir regra de recomendação na API.
- **`$integration-system-testing-v1`:** validar sessão, composição, ausência de alteração e modelos renderizáveis.
- **Frontend:** coletar objetivo, oferecer cards/prévias disponíveis e revisão de sugestões.
- **Produto:** decidir persistência do objetivo e futura heurística baseada no perfil.

## Síntese

O sistema terá duas entradas: recomendação determinística de modelo por objetivo e adequação textual a vaga por IA. A separação preserva privacidade, explicabilidade e decisão final do estudante. A maior incerteza é reconciliar catálogo, enumeração e renderizadores efetivamente disponíveis antes de expor todas as opções.
