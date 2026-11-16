---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v005"
status: proposed
created_at: "2026-11-05T18:17:51-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261020-163820-adequacao-semantica-gpt-nano-v001.md
  supersedes: prompts/backend/20261105-181201-adequacao-semantica-gpt-nano-v004.md
  change_type: enrichment
  secondary_change_types: [correction]
  decision_impact: strengthened
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20261105-181201-adequacao-semantica-gpt-nano-v004.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on bd36f0d"
      availability: available
    - path: docs/adequacao_semantica_ia.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Papel da IA; Preparação de contexto; Privacidade e controle"
      content_state: commit
      revision: bd36f0d
      availability: available
    - path: src/backend/application/adequacao_semantica.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "SolicitarAdequacaoCurriculoVagaEntrada e SolicitarAdequacaoCurriculoVaga"
      content_state: commit
      revision: bd36f0d
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/frontend]
  confidence: high
  rationale: "A clarificação define o estado do fluxo e a responsabilidade de API/Application; a tela é handoff."
classification:
  sphere: engineering
  concerns: [architecture, privacy, user-experience]
  decision_kind: clarification
  scope: system
  lifecycle: evolution
  urgency: normal
  uncertainty: low
  reversibility: moderate
  risk: high
---

# Análise de decisão — aceite do estudante para sugestão de modelo por IA

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

```text
"se o consentimento atual" a ideia é a IA sugerir e na tela o usuário consentir ou não
```

- Interpretação: o consentimento posterior é o **aceite ou recusa da sugestão** apresentada na tela. Ele não autoriza aplicar automaticamente o modelo. O consentimento explícito já presente no DTO continua sendo prévio e necessário para enviar contexto ao provedor de IA; são decisões diferentes e não devem ser confundidas.

## Mudanças desde a versão anterior

| Elemento | v004 | v005 | Motivo | Impacto |
|---|---|---|---|---|
| Incerteza principal | Cobertura do consentimento para nova finalidade | Resolvida: estudante aceita ou recusa a sugestão na tela | Clarificação explícita do usuário | Fluxo de revisão fica definido. |
| Termo “consentimento” | Podia significar permissão ao provedor ou adoção do resultado | Separa autorização prévia de IA e aceite posterior da recomendação | Evitar ambiguidade | Mantém proteção de dados e autonomia. |
| Aplicação do modelo | Não automática | Continua não automática; só ocorre após aceite explícito | Confirmar comportamento | Exige ação posterior distinta da rota de sugestão. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261105-181201-adequacao-semantica-gpt-nano-v004.md` | Primário | Prosa | Documentação | Markdown | Integral | working tree baseado em `bd36f0d` |
| `docs/adequacao_semantica_ia.md` | Apoio | Prosa | Documentação | Markdown | Papel, preparação e privacidade | commit `bd36f0d` |
| `src/backend/application/adequacao_semantica.py` | Apoio | Código-fonte | Produção | Python | Entrada e orquestração | commit `bd36f0d` |

### Limites da evidência dos artefatos

- Não foram analisadas telas ou endpoints de aplicação de layout; a decisão apenas define o handoff após a tela aceitar a sugestão.
- A redação legal e visual do controle de aceite permanece responsabilidade de produto/frontend.

## Problema enriquecido

### Resultado desejado

Exibir uma recomendação de modelo gerada por IA e permitir que o estudante a aceite ou recuse na interface, sem alterar o currículo na geração da sugestão.

### Atores e interesses

- **Estudante:** vê a sugestão, sua justificativa e controla se a adota.
- **Backend:** gera somente proposta revisável e não persiste layout durante a sugestão.
- **Frontend:** apresenta ações explícitas de aceitar e recusar, sem inferir aceite.

### Evidências e fatos observados

1. O documento de IA prevê revisão, aceitação, edição ou descarte de sugestões e proíbe alteração automática.
2. A entrada atual contém `consentimento_explicito`, validado antes da chamada ao gerador.
3. A versão v004 já definiu que a recomendação usa o DTO e o contexto limitado da adequação.

### Hipóteses

- H1: o controle de `consentimento_explicito` continuará claramente apresentado antes do envio ao provedor.
- H2: aceitar a sugestão será uma ação explícita posterior e autenticada, não um efeito da resposta de recomendação.

### Perguntas em aberto

Nenhuma identificada para decidir o fluxo. A escolha de persistir ou apenas pré-selecionar o modelo após o aceite requer decisão de implementação posterior.

### Escopo

- A rota de recomendação por IA recebe o DTO compartilhado, exige consentimento prévio para a chamada e devolve proposta sem escrita.
- A tela mostra modelo recomendado e justificativa, com ações claras de aceitar e recusar.
- O aceite deve disparar uma ação posterior, distinta e autenticada, caso o produto queira atualizar o layout da versão.

### Fora do escopo

- Aplicar automaticamente a recomendação, presumir aceite por ausência de recusa, ou enviar dados ao provedor após recusa do consentimento prévio.
- Definir persistência, endpoint ou interface detalhada da alteração de modelo.

### Critérios de sucesso

- A IA não altera nem escolhe definitivamente o layout.
- O estudante pode recusar sem efeito colateral no currículo.
- Nenhum contexto sai do sistema sem `consentimento_explicito` prévio.
- Qualquer futura mudança de modelo decorre de aceite inequívoco do estudante.

## Restrições aplicáveis

- Permissão para processar dados pela IA precede a requisição; aceite da sugestão ocorre depois da resposta.
- O DTO compartilhado continua carregando a primeira permissão, e não pode representar o aceite posterior por antecipação.
- O backend não deve persistir escolha de layout no endpoint de sugestão.

## Classificação comentada

É uma clarificação de engenharia, privacidade e experiência: fixa duas decisões de usuário em fases distintas do fluxo e reduz o risco de tratar uma sugestão como alteração autorizada.

## Decisão de roteamento

`prompts/backend` permanece adequado pela continuidade da linhagem e pelos contratos de entrada/saída. `prompts/frontend` é consumidor do handoff de tela, não o destino principal.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| User-value | 1 | Aceite e recusa compreensíveis | O estudante controla a apresentação final. |
| Privacidade | 1 | Autorização ao provedor antes do envio | Contexto profissional não sai sem permissão. |
| Correção | 2 | Sugestão não produz escrita | Evita alteração implícita de currículo. |

## Alternativas consideradas

**A — Autorização prévia para uso de IA e aceite posterior da sugestão, recomendada.** Separa processamento externo de decisão sobre layout.

**B — Tratar `consentimento_explicito` do DTO como aceite antecipado do modelo.** Inviável: não há sugestão conhecida para o estudante aceitar no momento da requisição.

**C — Aplicar automaticamente e oferecer apenas reversão.** Inviável: contradiz o controle explícito definido pelo usuário e a documentação de revisão.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| User-value | 1 | +2 | -1 | -2 | alta | Clarificação do usuário. |
| Privacidade | 1 | +2 | 0 | 0 | alta | Consentimento antes de enviar. |
| Correção | 2 | +2 | -1 | -2 | alta | Proposta não é comando. |

## Histórico e decisão atual

### Decisão da versão anterior

`v004` recomendou IA com o DTO compartilhado e identificou o sentido do consentimento como principal incerteza.

### Decisão recomendada nesta versão

Adotar A. A recomendação é gerada por IA somente após a autorização explícita de uso do provedor já representada no DTO. A resposta é proposta revisável. Na tela, o estudante aceita ou recusa a sugestão; a recusa não escreve nada, e o aceite não deve ser implícito nem ocorrer no mesmo endpoint de geração. Uma futura ação de aplicação de layout deverá receber confirmação explícita e atualizar somente a versão própria autenticada.

### Impacto da revisão

Fortalecida: não altera o reuso do DTO, a IA ou a separação de intenções de v004; resolve a ambiguidade entre autorização de processamento e aceitação do resultado.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| User-value | maximized | Decisão final permanece com estudante | Informação complementar do usuário. |
| Privacidade | prioritized | Permissão explícita antes da transferência | DTO e documentação existentes. |
| Correção | prioritized | Nenhuma escrita em fluxo de sugestão | Separação proposta/ação. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Simplicidade | Dois momentos explícitos | Checkbox/ação antes da IA e aceite/recusa após resposta. |
| Modificabilidade | Aplicação desacoplada | Aceite pode evoluir sem alterar o gerador. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| User-value | Modelo é aplicado sem escolha consciente | Alta | Estudantes. |
| Privacidade | IA recebe conteúdo antes de autorização | Alta | Estudantes. |
| Correção | Aceite e geração se confundem | Média | Backend e suporte. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| User-value | Uma interação adicional na tela | Delivery-speed | Aceitável: é a decisão expressa pelo usuário. |
| Correção | Futuro comando separado para aplicar modelo | Simplicidade | Aceitável: preserva fronteiras e auditoria. |

## Riscos e efeitos de segunda ordem

- Rotular os dois controles apenas como “consentimento” pode confundir o estudante; a interface deve distinguir “permitir análise por IA” de “usar este modelo”.
- Se a sessão mudar entre proposta e aceite, a futura ação de aplicação deve revalidar propriedade e o modelo escolhido.
- A sugestão pode ficar obsoleta após alterações no currículo; o produto deve decidir posteriormente se exibirá aviso ou regeneração.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| IA só é chamada com permissão prévia | Spy do gerador | Teste unitário/API | Gerador invocado com `consentimento_explicito` falso. |
| Recusar não altera versão | Snapshot e teste de UI | Teste de fluxo | Repositório recebe escrita após recusa. |
| Aceite é inequívoco | Teste de aceitação | Verificar ação explícita na tela | Layout muda ao apenas visualizar sugestão. |

## Handoffs e atividades posteriores

- **Frontend:** expor primeiro a autorização para análise por IA e, após resposta, botões distintos “usar este modelo” e “manter modelo atual”.
- **Backend:** manter sugestão sem escrita; se a aplicação for implementada, criar comando autenticado e separado para alterar layout após aceite.
- **Produto/privacidade:** revisar rótulos para não confundir autorização de processamento com aceite de recomendação.

## Síntese

A IA sugere; o estudante decide na tela se usa ou não o modelo recomendado. A autorização para enviar o contexto à IA continua anterior e independente desse aceite. A principal incerteza restante é apenas a política de persistência ou pré-seleção após o aceite, que está fora desta análise.
