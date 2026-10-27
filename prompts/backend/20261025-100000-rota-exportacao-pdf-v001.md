---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-25T10:00:00-03:00"
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
    - path: src/backend/api/exportacao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "cac53a7"
      availability: available
    - path: src/backend/application/exportacao_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "cac53a7"
      availability: available
    - path: src/backend/infrastructure/exportacao/renderizador_pdf.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "classe RenderizadorDocumentoCurriculoPdf e assinatura de renderizar (linhas 1-80)"
      content_state: commit
      revision: "cac53a7"
      availability: partial
    - path: src/backend/tests/test_api_exportacao_curriculo.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "cac53a7"
      availability: available
    - path: "GitHub issue #122"
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
      revision: "cac53a7"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "cac53a7"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "Completa a exportação de currículo (cadeia F6.9 a F6.12) publicando a rota de download em PDF sobre o gerador e o caso de uso já existentes."
classification:
  sphere: engineering
  concerns: [delivery, user-experience]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: time-critical
  uncertainty: low
  reversibility: easy
  risk: low
---

# Análise de decisão — rota de download do currículo em PDF

## Solicitação original

```text
Implementar exportação de currículo em PDF
#122
Tarefa da fatia vertical atribuída a @regazzio. Inclua os testes unitários pertinentes.
```

## Informações complementares

- Modo de trabalho pedido: a assistente escreve os arquivos e o usuário faz os commits.
- Quando esta tarefa foi analisada, o documento neutro, o gerador de PDF, o gerador de DOCX, o caso de uso `ExportarCurriculo` e a rota de DOCX já estavam na `dev` (cards #229 a #232). Faltava apenas a rota do PDF.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nenhum identificado | — | — | Versão inicial | — |

## Artefatos analisados

Ver o frontmatter. Fatos sustentados por recortes parciais valem somente para os trechos indicados.

### Limites da evidência dos artefatos

- O código-fonte corresponde ao commit `cac53a7` (cabeça da `dev` na consulta).
- O corpo da issue #122 tem só uma frase e não traz critérios; o escopo desta análise é o que falta na cadeia de exportação.
- A rota não foi exercitada com o gerador de PDF contra dados reais de produção; os testes usam a fixture de exportação.
- Este documento foi redigido manualmente por um assistente seguindo `.agents/skills/decision-analysis-v4/SKILL.md`; **não** foi produzido pela invocação `$decision-analysis-v4`. O `status` é `proposed` e exige aprovação humana.
- O fuso `-03:00` segue o relógio da máquina do usuário.

## Problema enriquecido

### Resultado desejado

O estudante autenticado baixa o PDF de uma versão de currículo própria, com o mesmo contrato de segurança, erros e cabeçalhos do download em DOCX.

### Evidências e fatos observados

1. `RenderizadorDocumentoCurriculoPdf` já gera o PDF a partir do documento renderizado (`renderizador_pdf.py`).
2. `ExportarCurriculo(gerador_previa, renderizador, formato)` serve a qualquer formato, mudando só a composição (`exportacao_curriculo.py`).
3. A API só registra a rota de DOCX; não há `FORMATO_PDF`, rota de PDF nem parâmetro de PDF na fábrica.
4. A rota de DOCX responde 404 uniforme, 500 genérico, 401 e 503, com cabeçalhos de anexo privados.

### Hipóteses

- **H1.** Acrescentar `FORMATO_PDF` (`pdf`, `application/pdf`) ao lado de `FORMATO_DOCX`.
- **H2.** Extrair o handler da rota para uma função que recebe caminho, executor e formato, de modo que PDF e DOCX compartilhem a mesma tradução de falhas, em vez de copiar o handler.
- **H3.** `criar_router(exportar_docx, exportar_pdf=None)` mantém compatibilidade; a fábrica ganha `exportar_curriculo_pdf`.
- **H4.** Cada formato depende só do seu executor; sem o do PDF, o endpoint responde 503 e o DOCX não é afetado.
- **H5.** A exportação **não** é bloqueada por pendências da revisão (comportamento atual do DOCX).

### Perguntas em aberto

1. A exportação deve ser bloqueada (409) quando a revisão tiver erro, ou só avisar?
2. O PDF deve poder ser aberto no navegador (`inline`) em vez de baixado?

### Escopo

- Constante de formato, rota de PDF, parâmetro na fábrica e testes da rota.

### Fora do escopo

- Bloqueio por revisão; mudança do layout do PDF; composição real com banco e sessão.

### Critérios de sucesso

- `GET …/exportacao/pdf` devolve um PDF legível, com tipo, nome e cabeçalhos corretos.
- 404 para versão ausente ou alheia, 403 para outro estudante na URL, 401 sem sessão, 500 genérico e 503 sem executor.
- Compor só um formato não habilita o outro; o Swagger documenta a rota.
- A suíte unitária e o `ruff check` passam.

## Restrições aplicáveis

- Adapter sem regra de negócio; testes da rota com doubles; docstring e proveniência em todo trecho novo (`AGENTS.md`).

## Classificação comentada

- `uncertainty: low` e `risk: low`: reaproveita gerador, caso de uso e contrato HTTP já testados no DOCX.

## Decisão de roteamento

Roteada para `prompts/backend`. Candidatas: `prompts/backend` e `prompts/requisitos`; a segunda foi descartada por não levantar requisitos. Confiança alta.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `simplicity` | 1 | Sem duplicar o handler do DOCX | Revisão em cerca de 10 minutos |
| `correctness` | 1 | Mesmas garantias de segurança do DOCX | Dado pessoal do estudante |
| `modifiability` | 2 | Novo formato = caminho + executor + tipo | Outros formatos são previsíveis |

## Alternativas consideradas

**Estado atual.** Só o DOCX é baixável.

**Alternativa A — Handler compartilhado, registrado por formato (recomendada).**

**Alternativa B — Copiar o handler do DOCX para o PDF.** Mais rápido de escrever, mas duplica ~40 linhas e permite divergir os dois formatos.

**Alternativa C — Rota única com o formato como parâmetro (`/exportacao/{formato}`).** Remove caminhos fixos, mas muda o contrato público do DOCX e dificulta documentar cada tipo no Swagger.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `simplicity` | 1 | +1 | 0 | 0 | média | B duplica código; C altera contrato |
| `correctness` | 1 | +1 | 0 | +1 | média | B pode divergir do DOCX |
| `modifiability` | 2 | +1 | -1 | +1 | média | C tem custo de contrato |

A escala é ordinal e não foi somada.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhuma identificada nesta linhagem; o desenho do DOCX (cards #229 a #232) foi decidido por outra pessoa do grupo.

### Decisão recomendada nesta versão

Adotar a **Alternativa A**. Status `proposed`: aprovação humana, em especial sobre as perguntas 1 e 2.

### Impacto da revisão

Não aplicável — versão inicial.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `simplicity` | prioritized | Um handler para os dois formatos | Rota de DOCX inalterada nos testes |
| `correctness` | prioritized | Mesmas garantias nos dois formatos | Testes espelhados |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `modifiability` | Novo formato sem copiar o handler | `_registrar_download` recebe caminho, executor e formato |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | PDF com garantias diferentes das do DOCX | Média | Estudantes |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `simplicity` | Refatora o handler existente do DOCX | Risco de regressão | Aceitável: os 9 testes do DOCX permanecem e cobrem o handler |

## Riscos e efeitos de segunda ordem

- **Regressão no DOCX.** Mitigação: os testes da rota de DOCX não foram alterados e rodam sobre o handler compartilhado.
- **Exportação sem revisão.** Um currículo incompleto pode ser exportado; pergunta 1 registrada.
- **Composição real.** No sistema em execução a rota responde 503 até o executor ser composto com banco e sessão.
- **Conflitos de integração.** `api/factory.py` é alterado por quase toda tarefa.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| PDF legível com cabeçalhos corretos | Corpo começa com `%PDF`, texto extraído, MIME e nome | Teste da rota com o gerador real | Arquivo inválido |
| Mesmas garantias do DOCX | 404, 403, 401, 500 e 503 | Testes espelhados | Status diferente |
| Formatos independentes | DOCX responde 503 só com o PDF composto | Teste da rota | DOCX habilitado |
| DOCX preservado | Testes existentes passam | Suíte do DOCX | Falha em teste do DOCX |

## Handoffs e atividades posteriores

- **Grupo:** decidir o bloqueio por revisão (pergunta 1) e `inline` ou anexo (pergunta 2).
- **Composição:** injetar `ExportarCurriculo` com `RenderizadorDocumentoCurriculoPdf` e `FORMATO_PDF`.
- **Documentação (#386):** atualizar `docs/exportacao-pdf-docx.md`, que ainda diz que não há gerador conectado.

## Síntese

O PDF já era gerado, e o caso de uso já servia a qualquer formato, mas só o DOCX tinha rota. A decisão acrescenta `FORMATO_PDF` e a rota do PDF, reaproveitando um handler comum com o DOCX, para que os dois formatos tenham as mesmas garantias. A principal incerteza é se a exportação deve ser bloqueada quando a revisão acusar erro.
