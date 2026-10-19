---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-19T11:00:00-03:00"
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
    - path: src/backend/api/documento.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "678906c"
      availability: available
    - path: src/backend/application/exclusao_documento.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "678906c"
      availability: available
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "portas ArmazenadorDocumentos e RepositorioDocumento (linhas 855-920)"
      content_state: commit
      revision: "678906c"
      availability: partial
    - path: src/backend/infrastructure/storage/armazenador_documentos_local.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "678906c"
      availability: available
    - path: "GitHub issue #205 (F4.15)"
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: external
      revision: null
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "678906c"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "678906c"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "Decide a leitura autorizada de documentos complementares, na linhagem de armazenamento e exclusão de documentos de prompts/backend."
classification:
  sphere: engineering
  concerns: [security, domain, delivery]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: time-critical
  uncertainty: medium
  reversibility: easy
  risk: medium
---

# Análise de decisão — download autorizado de documento complementar

## Solicitação original

```text
[F4.15] Expor download autorizado de documento complementar sem revelar o caminho de armazenamento.
WBS: 1.3.2.3, 1.3.3.1–1.3.3.4 — Início: 2026-10-19 — Entrega: 2026-10-25
Responsável único: @mariacarolinayamamoto
Critério de aceite: A alteração é verificável isoladamente, inclui os testes pertinentes e pode ser revisada em cerca de 10 minutos.
```

## Informações complementares

- Modo de trabalho pedido: a assistente escreve os arquivos e o usuário faz os commits.
- Esta análise é independente das anteriores e não as revisa.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `678906c` (cabeça da `dev` na consulta).
- O corpo da issue #205 foi visto somente pelo texto colado pelo usuário.
- A leitura contra um diretório real em ambiente de execução não foi exercitada fora dos testes com diretório temporário.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

O estudante autenticado baixa o arquivo de um documento complementar seu; ninguém baixa documento alheio, excluído ou inexistente, e a resposta não revela onde o arquivo está guardado.

### Evidências e fatos observados

1. A porta de storage só tem `armazenar`; não há leitura (`ports.py`).
2. O cadastro devolve `url_armazenamento` na resposta e a exclusão lógica já responde 404 uniforme para documento alheio ou ausente (`api/documento.py`, `exclusao_documento.py`).
3. O adaptador local grava o arquivo com uma chave UUID hexadecimal de 32 caracteres e devolve `prefixo/chave` (`armazenador_documentos_local.py`).
4. O nome do arquivo é validado no domínio contra barras, `..` e caracteres de controle; o tipo é restrito a PDF, PNG e JPEG (`itens_perfil.py`).
5. As rotas fora de `ROTAS_PUBLICAS` exigem sessão, e o usuário autenticado vem de `request.state.usuario_id`.

### Hipóteses

- **H1.** A porta ganha `ler(url_armazenamento) -> bytes | None`, em vez de lançar exceção, de modo que ausência e localização inválida sejam o mesmo resultado.
- **H2.** O adaptador local só lê se a localização tiver o prefixo configurado e a chave tiver 32 caracteres hexadecimais minúsculos, o que impede navegação de diretório.
- **H3.** O caso de uso `BaixarDocumento` recusa documento ausente, excluído ou de outro estudante antes de tocar o storage, e trata arquivo físico ausente do mesmo modo (`DocumentoNaoEncontrado`, 404 uniforme).
- **H4.** O resultado `ConteudoDocumento` tem só nome, tipo e bytes, sem a localização.
- **H5.** A rota `GET /documentos/{documento_id}` responde com os bytes, o tipo do arquivo, `Content-Disposition: attachment` (com `filename*` em UTF-8), `X-Content-Type-Options: nosniff` e `Cache-Control: private, no-store`.

### Perguntas em aberto

1. A resposta de cadastro deve continuar expondo `url_armazenamento`, já que o card pede para não revelar o caminho? (Fora do escopo deste card; registrado.)
2. O download deve ser `attachment` ou `inline` para imagens e PDF?
3. Quando o arquivo físico some e o registro existe, 404 é suficiente ou deve gerar alerta operacional?

### Escopo

- Porta de leitura, leitura no adaptador local, caso de uso, rota GET, registro na fábrica e testes.

### Fora do escopo

- Armazenamento em nuvem; mudança da resposta de cadastro; URLs assinadas; auditoria de downloads.

### Critérios de sucesso

- O dono baixa o arquivo com o tipo e o nome corretos; documento alheio, excluído ou inexistente responde 404 idêntico.
- O storage não é consultado antes da autorização.
- Nenhuma localização de armazenamento aparece no resultado, nos cabeçalhos ou no corpo.
- Localizações com `..`, barras ou chaves fora do padrão não leem arquivo algum.
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Application não depende de Infrastructure; o acesso ao sistema de arquivos ocorre só no adaptador (`src/backend/AGENTS.md`).
- Docstring e proveniência em todo trecho novo.

## Classificação comentada

- `risk: medium`: o endpoint entrega arquivo de usuário e envolve controle de acesso e leitura de disco.
- `uncertainty: medium`: o comportamento em ambiente real não foi exercitado e o card não traz critérios detalhados.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `security` | 1 | Nenhum acesso a documento alheio; sem leitura fora do diretório base | Dado pessoal do estudante |
| `simplicity` | 1 | Revisável em cerca de 10 minutos | Critério de aceite |
| `modifiability` | 2 | Trocar o storage sem mudar a Application | Nuvem é previsível |

## Alternativas consideradas

**Estado atual.** O arquivo pode ser gravado, mas não lido pela API.

**Alternativa A — Rota que lê pela porta e devolve os bytes (recomendada).** A autorização fica no caso de uso e o caminho nunca sai do servidor.

**Alternativa B — Devolver a URL de armazenamento para o cliente baixar direto.** Simples, mas revela o caminho, contraria o card e depende de o storage impor a autorização.

**Alternativa C — URL assinada de curta duração.** Boa para storage em nuvem, mas exige assinatura, expiração e provedor que o projeto ainda não tem.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `security` | 1 | +1 | -2 | +1 | média | B expõe o caminho e delega a autorização |
| `simplicity` | 1 | +1 | +1 | -2 | média | C exige assinatura e expiração |
| `modifiability` | 2 | +1 | -1 | +1 | baixa | B acopla o cliente ao storage |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**. Status `proposed`: aprovação humana e alinhamento com a responsável pelo card, em especial sobre as perguntas 1 e 2.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `security` | prioritized | Download só do dono, sem caminho exposto | Testes do caso de uso e do adaptador |
| `simplicity` | prioritized | Uma porta, um caso de uso e uma rota | Sem nova infraestrutura |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `modifiability` | Trocar o storage sem mexer na Application | A leitura passa pela porta `ArmazenadorDocumentos` |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `security` | Exposição de documentos pessoais de outros estudantes | Alta | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | O arquivo inteiro é lido em memória e devolvido pela API | Escalabilidade para arquivos grandes | Aceitável: o tamanho máximo do documento já é limitado no cadastro |

## Riscos e efeitos de segunda ordem

- **Conflito com a responsável pelo card.** Mitigação: alinhar antes do PR e manter a porta `ArmazenadorDocumentos` como único ponto compartilhado.
- **Resposta de cadastro ainda expõe a URL.** Pergunta 1; fora do escopo.
- **Arquivo lido por inteiro em memória.** Aceito pelo limite de tamanho do documento.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Só o dono baixa | 404 idêntico para ausente, excluído e alheio, sem ler o storage | Testes do caso de uso | Leitura do storage antes da autorização |
| Caminho não vaza | Resultado sem URL e cabeçalhos sem localização | Testes do caso de uso e da API | Localização em resposta |
| Sem leitura fora do diretório | `None` para `..`, barras e chaves inválidas | Testes do adaptador | Conteúdo devolvido |
| Rota registrada e protegida | Rota GET no OpenAPI, fora de `ROTAS_PUBLICAS` | Teste da fábrica | Rota ausente |

## Handoffs e atividades posteriores

- **Responsável pelo card (#205):** revisar e integrar a entrega.
- **Futuro:** tratar a URL exposta na resposta de cadastro (pergunta 1) e decidir `attachment` ou `inline` (pergunta 2).

## Síntese

O storage só gravava arquivos e o card pede o download sem revelar o caminho. A decisão acrescenta uma leitura à porta de storage, um caso de uso que autoriza antes de ler e trata ausência, exclusão e posse alheia como o mesmo 404, e uma rota GET que devolve os bytes sem a localização. O adaptador local só lê chaves no formato que ele mesmo gera. A principal incerteza é o alinhamento com a responsável pelo card.
