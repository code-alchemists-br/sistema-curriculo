---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v002"
status: proposed
created_at: "2026-10-13T14:29:42-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261013-120827-cadastro-competencias-api-v001.md
  supersedes: prompts/backend/20261013-120827-cadastro-competencias-api-v001.md
  change_type: enrichment
  secondary_change_types: [reassessment]
  decision_impact: strengthened
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20261013-120827-cadastro-competencias-api-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "v001; working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: src/backend/domain/itens_perfil.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "classe Competencia"
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "protocolos análogos de repositório e gerador de ID"
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: src/backend/api/experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "rota autenticada de cadastro e DTOs de fronteira"
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: mermaid-markdown
      analysis_scope: selected-section
      locator: "entidade COMPETENCIA e relação com USUARIO"
      content_state: working-tree
      revision: "working-tree based on 376eb7db510475aed7048b5adf05b2b700dbc0f8"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "A revisão continua definindo regra de domínio, contrato de repositório, índice de dados e comportamento da API de backend."
classification:
  sphere: engineering
  concerns: [domain, data, reliability]
  decision_kind: policy
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — Cadastro de competências técnicas e comportamentais pela API

## Solicitação original

> Faça a análise para implementar no backend o cadastro de competências técnicas e comportamentais pela API. Deve incluir o endpoint de criação, validação do payload, conversão para DTO/comando, chamada do caso de uso, persistência por meio do repositório e resposta HTTP apropriada — sem expor entidades de domínio. Também precisa de testes unitários cobrindo o fluxo e suas regras, como dados obrigatórios e possíveis duplicidades.

## Informações complementares

> Com relação a 'prompts\backend\20261013-120827-cadastro-competencias-api-v001.md' vamos revisar decidindo o critério de duplicação. Diferenças de caixa e espaços não significam registros diferentes.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Regra de caixa | Hipótese de que caixa não diferencia registros. | Decisão confirmada: comparação não distingue maiúsculas/minúsculas. | Informação explícita do usuário. | A chave canônica deve aplicar `casefold()`. |
| Regra de espaços | Hipótese de remover extremidades e reduzir espaços internos. | Decisão confirmada: diferenças de espaços não diferenciam registros. | Informação explícita do usuário. | A chave canônica deve aparar e colapsar sequências de espaço em um único espaço. |
| Status da política | Parcialmente pendente de produto. | Confirmada para caixa e espaços; acentos, pontuação e sinônimos continuam fora da decisão. | A nova informação resolve somente parte da equivalência. | A recomendação é fortalecida, sem ampliar a normalização. |
| Artefatos de código | Estado de referência da v001. | Nenhuma alteração de código observada; `HEAD` permanece `376eb7d`. | Revisão documental. | A arquitetura e o roteamento da v001 permanecem válidos. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261013-120827-cadastro-competencias-api-v001.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | v001 no working tree, baseada em `376eb7d` |
| `src/backend/domain/itens_perfil.py` | Apoio | Código-fonte | Produção | Python | Classe `Competencia` | Working tree baseada em `376eb7d` |
| `src/backend/application/ports.py` | Apoio | Código-fonte | Produção | Python | Protocolos análogos | Working tree baseada em `376eb7d` |
| `src/backend/api/experiencia_profissional.py` | Apoio | Código-fonte | Produção | Python | Cadastro autenticado e DTOs | Working tree baseada em `376eb7d` |
| `docs/modelagem_der.md` | Apoio | Modelo de diagrama | Contrato de schema | Mermaid/Markdown | Competência e proprietário | Working tree baseada em `376eb7d` |

### Limites da evidência dos artefatos

Não houve alteração observada nos artefatos de produção desde a v001. O DER e os requisitos não especificam equivalência de texto; a regra para caixa e espaços decorre diretamente da nova declaração do usuário. Acentos, pontuação, abreviações e sinônimos continuam sem regra aprovada e não serão tratados como equivalentes por esta versão.

## Problema enriquecido

### Resultado desejado

Permitir que o estudante autenticado registre uma competência técnica ou comportamental, com descrição e nível válidos, sem criar duas competências logicamente iguais devido apenas a diferenças de maiúsculas, minúsculas ou espaços.

### Atores e interesses

- O estudante precisa de uma lista limpa de competências, sem duplicatas como `Python`, `python` e ` Python `.
- A API precisa devolver conflito compreensível sem expor dados de outro estudante.
- O domínio e a Application precisam aplicar uma política determinística, independente de banco e HTTP.
- A infraestrutura precisa preservar a mesma regra sob requisições concorrentes.

### Evidências e fatos observados

- A v001 definiu competência como item de perfil dedicado, com categoria, descrição e nível; a entidade atual ainda não contém categoria nem invariantes de texto.
- A v001 já propunha chave por proprietário, categoria e descrição normalizada, mas a equivalência de caixa/espaços era hipótese.
- A nova informação do usuário estabelece que diferenças de caixa e espaços não representam registros distintos.
- Não há modelo, repositório ou restrição de dados atuais para competência; a regra pode ser introduzida sem migração de registros legados.
- O padrão de cadastro autenticado de experiência demonstra que o proprietário deve vir de `request.state`, e não do cliente.

### Hipóteses

- Espaços referem-se a espaços no início/fim e a sequências internas de caracteres de espaço, tabulação ou quebra de linha, todos convertidos para um único espaço ASCII entre palavras.
- A comparação será Unicode-aware por `casefold()`, mais apropriada que `lower()` para texto humano; a descrição original, aparada mas com capitalização digitada, será preservada para exibição.
- A categoria permanece parte da identidade lógica: a mesma descrição em categorias distintas é permitida até que o produto decida o contrário.
- O nível não participa da duplicidade, pois é atributo de proficiência a ser editado no futuro, e não uma competência nova.

### Perguntas em aberto

- `Python` e `Pýthon` devem ser tratados como equivalentes ou diferentes?
- `Node.js`, `Node JS` e `NodeJS` devem ser tratados como equivalentes ou diferentes?
- Abreviações e sinônimos, como `C#` e `C Sharp`, devem ser consolidados?
- A categoria deve continuar diferenciando registros de mesma descrição?

### Escopo

- Fixar a normalização de duplicidade para caixa e espaços.
- Definir a chave `usuario_id + categoria + descricao_normalizada` e a regra de resposta `409` para conflito da própria conta.
- Requerer que domínio/Application, adapter SQLAlchemy e índice único compartilhem essa mesma política.
- Definir cenários unitários que comprovem equivalência de caixa e espaços.

### Fora do escopo

- Normalizar ou remover acentos, pontuação, hífens, símbolos, abreviações ou sinônimos.
- Alterar categoria, nível, rota, autenticação, estrutura de camadas ou demais decisões da v001.
- Migrar dados existentes, listar, editar ou excluir competências.

### Critérios de sucesso

- Para o mesmo estudante e categoria, `Python`, `python` e ` PYTHON ` têm a mesma chave normalizada; em nomes compostos, `Power BI` e `Power   BI` também têm a mesma chave. A segunda criação responde `409`.
- Para estudantes distintos, a mesma chave normalizada é permitida.
- Para categorias distintas, a mesma chave normalizada é permitida.
- A descrição exibida não é substituída pela chave normalizada; somente seu contorno é aparado para evitar exibir espaços acidentais.
- A restrição única do banco usa exatamente `usuario_id`, `categoria` e `descricao_normalizada`, preservando a proteção contra corrida.
- Testes unitários cobrem sucesso, caixa, espaços externos, sequências internas, categoria distinta, usuário distinto e nível distinto.

## Restrições aplicáveis

- A regra de equivalência é regra de domínio/Application; o ORM só persiste e reforça a chave, e a API só a traduz em `409`.
- A comparação não pode depender da collation ou das funções específicas do banco, para manter comportamento testável e consistente; `descricao_normalizada` deve ser calculada antes da persistência.
- Persistência continua Code First: modelo SQLAlchemy, metadata e migration versionada são a fonte de verdade do schema.
- O endpoint não expõe entidade de domínio nem aceita proprietário controlado pelo cliente.
- Cada função, classe e DTO novos deve documentar responsabilidade, abordagem e finalidade; testes unitários devem rodar pelo ambiente Nix de backend.

## Classificação comentada

A revisão é uma decisão de política técnica dentro de um componente de engenharia. Ela afeta domínio e dados ao determinar igualdade lógica, e confiabilidade ao exigir que a mesma chave seja reforçada por restrição única. A incerteza diminuiu para caixa e espaços, mas permanece média por não haver definição para outras variações textuais.

## Decisão de roteamento

O destino permanece `prompts/backend` por continuidade de linhagem e porque a política será aplicada por código de domínio/Application, repositório, schema e API. `prompts/requisitos` continua somente como candidata de contexto, pois não contém a implementação nem o contrato técnico da regra.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| correctness | Alta | Priorizar | Equivalências declaradas devem produzir exatamente a mesma decisão de cadastro. |
| reliability | Alta | Satisfazer | Consulta e índice único devem concordar, inclusive em concorrência. |
| simplicity | Média | Priorizar | A normalização precisa ser previsível, pequena e independente de banco. |
| modifiability | Média | Satisfazer | A política deve poder ser ampliada posteriormente sem reescrever fronteiras. |
| user-value | Média | Priorizar | O estudante não deve acumular duplicatas visuais triviais. |

## Alternativas consideradas

**Alternativa A — Normalizar caixa e espaços antes de consultar e persistir (recomendada).** Construir `descricao_normalizada` com `" ".join(descricao.split()).casefold()`, após validar que o resultado não está vazio. Usar essa chave no repositório e no índice único, preservando uma versão aparada da descrição para apresentação. Atende exatamente à decisão informada e não infere equivalência de símbolos ou acentos.

**Alternativa B — Comparar somente caixa e preservar todos os espaços.** Aplicar apenas `casefold()` e guardar espaços como recebidos. É menor, mas contradiz a decisão de que diferenças de espaços não criam registros distintos; `Python` e ` Python ` continuariam coexistindo.

**Alternativa C — Normalização ampla de acentos, pontuação e sinônimos.** Remover diacríticos/símbolos ou manter dicionário de equivalências. Pode reduzir mais duplicatas, mas excede a decisão fornecida e pode consolidar competências que o produto queira manter distintas; é inviável no escopo atual.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| correctness | Alta | +2 | -2 | 0 | Alta | A nova informação exige equivalência de caixa e espaços, sem autorização para ampliar a equivalência. |
| reliability | Alta | +2 | 0 | +1 | Alta | A gera chave única determinística para consulta e banco. |
| simplicity | Média | +2 | +1 | -2 | Alta | `split`/`join`/`casefold` é pequeno e não exige catálogo semântico. |
| modifiability | Média | +1 | 0 | -1 | Média | Centralizar a função permite revisão futura; C introduz política ampla prematura. |
| user-value | Média | +2 | -1 | 0 | Alta | Evita duplicatas visíveis por preenchimento acidental. |

## Histórico e decisão atual

### Decisão da versão anterior

A v001 recomendou recurso dedicado de competência, com chave normalizada por proprietário, categoria e descrição; caixa e espaços foram tratados como hipótese, enquanto acentos e pontuação ficaram pendentes.

### Decisão recomendada nesta versão

Manter a arquitetura recomendada na v001 e tornar explícito o critério de duplicidade: duas competências são duplicadas somente se possuírem o mesmo `usuario_id`, a mesma `categoria` e o mesmo valor de `descricao_normalizada`, onde:

1. a descrição é convertida em uma sequência de palavras por `split()`;
2. sequências de espaços, tabulações e quebras de linha são colapsadas em um único espaço por `" ".join(...)`;
3. o resultado é convertido com `casefold()`.

Assim, `"Python"`, `" python "` e `"PYTHON"` são comparados pelo mesmo valor; para um nome composto, `"Power\tBI"` e `"Power   BI"` também são equivalentes a `"Power BI"`. Inserir espaço dentro de uma palavra, como `"Py thon"`, não é uma mera variação de separação entre termos e continua distinto de `"Python"`. A validação deve rejeitar a descrição cujo valor normalizado seja vazio. A descrição original aparada é preservada como dado apresentado; `descricao_normalizada` é campo técnico interno.

O caso de uso deve gerar a chave uma vez, consultar o repositório por `(usuario_id, categoria, descricao_normalizada)` e lançar `CompetenciaJaCadastrada` caso encontre registro. O banco deve ter `UNIQUE(usuario_id, categoria, descricao_normalizada)`; se o `flush` acusar especificamente essa violação, o adapter deve traduzi-la para a mesma falha. A API traduz a falha em `409 Conflict`, sem dizer se existe uma competência em outra conta.

Não há decisão para acentos, pontuação, abreviações ou sinônimos: estes permanecem distintos. O nível não compõe a chave; mudar proficiência deverá ser operação de edição futura, não novo cadastro.

### Impacto da revisão

A decisão é fortalecida. A v001 já recomendava normalização de caixa e espaços, mas agora essa parte deixa de ser hipótese e vira contrato verificável. Nenhuma fronteira arquitetural, rota ou modelo de persistência foi alterado.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | Mesmas palavras, variando apenas caixa/espaços, nunca geram registros paralelos. | Declaração explícita do usuário. |
| reliability | prioritized | A consulta preventiva e o índice usam uma chave idêntica. | Chave canônica persistida. |
| user-value | prioritized | Lista de competências permanece organizada e sem duplicatas triviais. | Inferência direta da regra de igualdade. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| simplicity | Sem dicionário, IA ou dependência de collation. | Função determinística de normalização textual. |
| modifiability | Regra pode ser ampliada sem alterar contrato HTTP. | Normalização é centralizada antes da porta e sua chave é explícita no schema. |
| security | Conflito não revela competência de outro estudante. | Escopo da chave inclui proprietário e API retorna conflito genérico. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | `Python`, `python` e variações de espaços coexistem como competências distintas. | Alta | Estudantes e consumidores futuros de currículo. |
| reliability | Consulta e banco podem discordar, permitindo duplicata sob concorrência. | Média | Estudantes e manutenção de dados. |
| user-value | O usuário precisa limpar manualmente registros visualmente idênticos. | Média | Estudantes. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness e reliability | Coluna técnica adicional, índice e testes de normalização. | simplicity | Aceitável: a regra declarada precisa ser persistida de forma consistente. |
| simplicity | Não consolidar acentos, símbolos ou sinônimos ainda. | user-value | Aceitável: evita falsos positivos sem regra de produto. |
| user-value | Aparar espaços da descrição apresentada. | fidelidade literal da entrada | Aceitável: espaços de contorno não têm significado segundo a decisão. |

## Riscos e efeitos de segunda ordem

- `split()` trata tabulações e quebras de linha como espaço; isso é coerente com “espaços”, mas deve ser refletido nos testes para evitar surpresa.
- A distinção entre caracteres visualmente parecidos Unicode (por exemplo, letras de alfabetos diferentes) não é resolvida por `casefold()` e permanece fora do escopo.
- O uso de `casefold()` pode fazer algumas equivalências Unicode mais amplas que `lower()`; é uma escolha deliberada para igualdade de texto, e deve ser aplicada igualmente no comando e na persistência.
- Futuras regras de remoção de acentos ou de equivalência semântica exigirão reavaliar registros existentes e índice único; não devem ser adicionadas silenciosamente.
- A categoria ainda integra a chave. Se produto decidir que uma descrição não pode existir em ambas as categorias, a migration e a regra precisarão de revisão.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Caixa não diferencia competência | Segunda tentativa com `Python`/`python` recebe `CompetenciaJaCadastrada` e `409`. | Testes unitários de caso de uso e rota. | Resultado diferente entre consulta e API. |
| Espaços não diferenciam competência | ` Python `, `Python`, `Python\t` e `Power   BI`/`Power BI` geram a mesma chave em seus respectivos pares. | Testes da função de normalização e do repositório. | Uma variante cria segundo registro. |
| Outras variações continuam distintas | Casos com acento/pontuação diferente podem coexistir. | Teste explícito por exemplo aprovado pela equipe. | Produto aprovar equivalência adicional. |
| Concorrência é protegida | Índice único contém os três campos da chave e sua violação vira falha de aplicação conhecida. | Teste de mapping/repository e teste de integração posterior. | Dois registros com a mesma chave forem persistidos. |
| Proprietário/categoria delimitam a regra | Mesmo texto é aceito para usuário ou categoria diferentes. | Testes unitários de caso de uso. | Produto exigir unicidade global ou entre categorias. |

## Handoffs e atividades posteriores

- Implementar uma função única e testada de normalização, usada para gerar o campo técnico e validar vazio; não duplicar a transformação em API e adapter.
- Confirmar posteriormente se acentos, pontuação, abreviações e sinônimos devem integrar a equivalência.
- Implementar os demais elementos da v001: categoria explícita, caso de uso, repositório, modelo SQLAlchemy, migration, endpoint e testes.
- Planejar migração de dados somente se a regra for alterada após existirem competências persistidas.

## Síntese

Esta v002 confirma que caixa e espaços não distinguem competências. A unicidade é por proprietário, categoria e descrição obtida por colapso de espaços seguido de `casefold()`, com `409` para nova tentativa equivalente e restrição única no banco para concorrência. A principal incerteza restante é se outras diferenças textuais — sobretudo acentos, pontuação e sinônimos — também devem significar a mesma competência.
