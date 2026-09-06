# Classificação dos artefatos analisados

Registre somente artefatos cujo conteúdo ou metadados foram efetivamente usados como evidência. Não transforme uma listagem de arquivos em prova de análise.

## Objeto da análise: `subjects.kind`

Escolha exatamente um:

- `demand-only`: somente a demanda textual foi analisada.
- `single-file`: um arquivo é o objeto principal.
- `file-set`: vários arquivos formam o objeto principal.
- `directory`: estrutura e conteúdo selecionado de um diretório.
- `repository`: estrutura ou comportamento amplo do repositório.
- `diff`: mudanças entre versões, commits ou estados do workspace.
- `mixed`: demanda e artefatos possuem importância equivalente; justifique.

## Relação: `relationship`

- `primary`: objeto principal sobre o qual a decisão é feita.
- `supporting`: evidência necessária para compreender o objeto principal.
- `context`: consultado para restrições ou convenções, sem ser avaliado diretamente.

## Representação: `representation`

Classifica como a informação está representada:

- `source-code`: linguagem de programação compilada ou interpretada.
- `executable-script`: script operacional ou de automação.
- `stylesheet`: CSS, pré-processadores ou linguagem de estilo.
- `markup`: HTML, XML, templates de interface ou marcação semelhante.
- `prose`: documentação narrativa ou texto estruturado para pessoas.
- `structured-data`: JSON, YAML, CSV, SQL de dados ou formato equivalente.
- `diagram-model`: diagrama, modelo ou notação arquitetural.
- `binary-media`: imagem, áudio, vídeo, PDF binário ou documento de escritório.
- `generated`: artefato derivado cujo formato principal não basta para descrever sua origem.
- `unknown`: somente quando o conteúdo não puder ser determinado.

## Função: `function`

Classifica para que o artefato serve:

- `production`: participa do comportamento entregue pelo sistema.
- `test`: verifica comportamento ou propriedades.
- `documentation`: explica sistema, processo ou decisão.
- `configuration`: controla comportamento de ferramenta ou aplicação.
- `build`: participa de compilação, empacotamento ou dependências.
- `deployment`: entrega ou provisiona ambientes.
- `infrastructure`: define ou opera recursos de infraestrutura.
- `schema-contract`: define estrutura, interface ou contrato verificável.
- `prompt-instruction`: orienta modelos ou agentes, como `AGENTS.md` e `SKILL.md`.
- `data-fixture`: fornece dados de teste, exemplo ou carga controlada.
- `visual-asset`: recurso visual ou estilístico.
- `generated-output`: saída produzida por ferramenta ou processo.
- `unknown`: função não determinável com a evidência disponível.

Representação e função são independentes. Exemplos:

| Arquivo | Representação | Função |
|---|---|---|
| `BillingService.java` | `source-code` | `production` |
| `BillingServiceTest.java` | `source-code` | `test` |
| `theme.css` | `stylesheet` | `production` |
| `ADR-007.md` | `prose` | `documentation` |
| `AGENTS.md` | `prose` | `prompt-instruction` |
| `openapi.yaml` | `structured-data` | `schema-contract` |
| `Dockerfile` | `executable-script` | `deployment` |

## Recorte: `analysis_scope`

- `whole-file`: conteúdo completo examinado.
- `selected-section`: seção ou linhas específicas; informe `locator`.
- `diff`: somente mudanças examinadas; informe base e alvo quando disponíveis.
- `metadata-only`: apenas nome, tamanho, tipo ou metadados; não alegue análise do conteúdo.

## Estado do conteúdo

Registre:

- `content_state`: `working-tree`, `staged`, `commit`, `external` ou `unknown`.
- `revision`: commit, referência, versão externa ou `null` quando indisponível.
- `availability`: `available`, `partial` ou `unavailable`.

Se o arquivo estiver modificado no working tree, `revision` não deve alegar que o conteúdo é idêntico ao `HEAD`. Use, por exemplo, `working-tree based on <commit>`.

## Forma do registro

```yaml
subjects:
  kind: single-file
  files:
    - path: src/billing/BillingService.java
      relationship: primary
      representation: source-code
      function: production
      format: java
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on abc1234"
      availability: available
```

No corpo, explique limitações como conteúdo parcial, arquivo inacessível ou ausência de referência de versão.
