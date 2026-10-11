---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v004"
status: proposed
created_at: "2026-10-11T10:29:43-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261011-093707-rejeicao-requisicoes-sem-credenciais-validas-v001.md
  supersedes: prompts/backend/20261011-101515-rejeicao-requisicoes-sem-credenciais-validas-v003.md
  change_type: scope-change
  secondary_change_types: [correction, reassessment]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20261011-101515-rejeicao-requisicoes-sem-credenciais-validas-v003.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "v003; não rastreado no estado examinado"
      availability: available
    - path: src/backend/api/listagem_versoes_curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "criar_router e GET /estudantes/{usuario_id}/curriculos"
      content_state: commit
      revision: "9531b6b; conteúdo coincidente com o estado de trabalho examinado"
      availability: available
    - path: src/backend/api/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "rotas PUT e DELETE de perfil; nenhuma rota GET"
      content_state: commit
      revision: "9531b6b; conteúdo coincidente com o estado de trabalho examinado"
      availability: available
    - path: src/backend/api/dados_contato.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "rota PUT de dados de contato"
      content_state: commit
      revision: "9531b6b; conteúdo coincidente com o estado de trabalho examinado"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "create_app e registro dos routers"
      content_state: commit
      revision: "9531b6b; conteúdo coincidente com o estado de trabalho examinado"
      availability: available
    - path: src/backend/main.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "app ASGI exposta por create_app() sem executores"
      content_state: commit
      revision: "9531b6b; conteúdo coincidente com o estado de trabalho examinado"
      availability: available
    - path: docs/matriz_testes.md
      relationship: supporting
      representation: prose
      function: test
      format: Markdown
      analysis_scope: selected-section
      locator: "RF13 e CT-RF13-02/03, linhas 165–175"
      content_state: commit
      revision: "9531b6b"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF13"
      content_state: commit
      revision: "9531b6b"
      availability: available
    - path: docs/contrato-credenciais-sessao-9.md
      relationship: supporting
      representation: prose
      function: schema-contract
      format: Markdown
      analysis_scope: selected-section
      locator: "Seção 9: dependência conceitual, falha 401 e contrato dos testes de rota protegida"
      content_state: working-tree
      revision: "arquivo não rastreado no estado examinado; a seção 3 referenciada não está neste arquivo"
      availability: available
    - path: prompts/README.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "9531b6b"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao, prompts/templates, prompts/frontend, prompts/ambientes]
  confidence: high
  rationale: "A linhagem permanece na pasta backend e a decisão trata de uma rota HTTP backend existente e de sua futura suíte de testes."
classification:
  sphere: engineering
  concerns: [security, integration, observability]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: high
---

# Análise de decisão — Relatório de lacuna de autenticação em rotas de leitura

## Solicitação original

`$decision-analysis-v4 Prepare o cenário de integração que verifica a rejeição de requisições sem credenciais válidas. Considere a matriz de testes, requisitos e contrato-credenciais-sessao-9.md.`

## Informações complementares

Entrada preservada da v002:

`$decision-analysis-v4 Revise 20261011-093707-rejeicao-requisicoes-sem-credenciais-validas-v001.md. Como os endpoints protegidos ainda não existem, use placeholders até que sejam definidos.`

Entrada preservada da v003:

`$decision-analysis-v4 $decision-analysis-v4 Revise a v002.

Os placeholders {{...}} não bastam. Substitua-os por endpoints e payloads
PROVISÓRIOS concretos, marcados como fictícios (ex.: /__fixture__/dados-pessoais,
/__fixture__/curriculos), numa tabela única separada da lógica do teste.

Inclua: rota-semente de fixture protegida por usuario_autenticado; teste de
sanidade (rota desprotegida de propósito faz o cenário falhar); casos reais de
CT-RF13-02/03 como skip/xfail com motivo "endpoint não definido"; e declare que
a cobertura é do mecanismo, não das rotas reais. Mantenha os 4 estados, 401,
executor não chamado e estado inalterado.`

Nova entrada desta revisão, preservada literalmente:

`$decision-analysis-v4 $decision-analysis-v4 Revise a v003.

Restrição nova: não é permitido implementar nada no backend; só testes, sobre o
que existe hoje. Rotas atuais não têm autenticação e usuario_autenticado não existe.

Abandone as fixtures e a rota-semente. Defina o alvo como as rotas REAIS
existentes que expõem dados pessoais ou currículos (inventarie-as no código).
Cenário: teste black-box com TestClient na app real, sem overrides de
dependência inexistentes. Casos testáveis: sem cookie e cookie inválido,
esperando 401 e corpo sem dados privados. Marcar xfail(strict=True) com motivo
"RF13 não implementada". Expirada e revogada: skip com motivo "validador de
sessão não existe". Declare que o resultado é um relatório de lacuna do RF13,
não cobertura de um mecanismo integrado. Se não houver rota real de dados
pessoais ou currículos, diga isso e não invente alvo.`

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Alvo do teste | Duas rotas de fixture e uma rota-controle criadas em app isolada | Só a rota GET real de listagem de currículos encontrada no código | Restrição explícita a testes do backend existente | Remove qualquer endpoint fictício e reduz cobertura candidata ao que existe |
| Dados pessoais | Fixture fictícia representava esse recurso | Não há rota GET real de dados pessoais; não será criado alvo | Inventário das rotas atuais | CT-RF13-02 fica sem alvo executável; registrar lacuna |
| Autenticação | Simulada por override de dependência conceitual | Nenhum override; `usuario_autenticado` não existe no produto | Evitar que teste valide uma dependência inventada | O resultado descreve ausência de RF13, não integração de autenticação |
| Resultados esperados | Casos protegidos deveriam passar com 401; controle verificava sensibilidade | Sem cookie e cookie inválido esperam 401/corpo sem dado e ficam `xfail(strict=True)`; expirada/revogada ficam `skip` | Estado atual não implementa RF13 nem validador de sessão | Relatório evidencia lacuna sem simular implementação |
| Alcance declarado | Cobertura do wiring do gate no harness | Relatório de lacuna de RF13 na rota real, sem cobertura de mecanismo integrado | Correção da alegação de cobertura | Evita atribuir ao sistema mecanismo que ainda não existe |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261011-101515-rejeicao-requisicoes-sem-credenciais-validas-v003.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree, v003 não rastreada |
| `src/backend/api/listagem_versoes_curriculo.py` | Principal | Código-fonte | Produção | Python | Arquivo completo; rota de listagem | Commit `9531b6b`, sem diferença observada |
| `src/backend/api/perfil_estudante.py` | Apoio | Código-fonte | Produção | Python | Rotas de perfil | Commit `9531b6b`, sem diferença observada |
| `src/backend/api/dados_contato.py` | Apoio | Código-fonte | Produção | Python | Rota de contato | Commit `9531b6b`, sem diferença observada |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Composição dos routers | Commit `9531b6b`, sem diferença observada |
| `src/backend/main.py` | Apoio | Código-fonte | Produção | Python | Aplicação ASGI | Commit `9531b6b`, sem diferença observada |
| `docs/matriz_testes.md` | Apoio | Prosa | Teste | Markdown | RF13/CT-RF13-02/03 | Commit `9531b6b` |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF13 | Commit `9531b6b` |
| `docs/contrato-credenciais-sessao-9.md` | Apoio | Prosa | Contrato de interface | Markdown | Seção 9 | Working tree, não rastreado |
| `prompts/README.md` | Contexto | Prosa | Instrução de prompt | Markdown | Arquivo completo | Commit `9531b6b` |

### Limites da evidência dos artefatos

O inventário dos decorators HTTP no backend encontrou `GET /estudantes/{usuario_id}/curriculos` em `src/backend/api/listagem_versoes_curriculo.py`. A composição de `src/backend/main.py` usa `create_app()` sem executor; portanto, atualmente essa rota responde `503 Listagem indisponível.` antes de obter dados. O handler aceita um executor injetado pela fábrica, mas não declara autenticação.

Não foi encontrada rota GET de perfil nem de dados pessoais: `perfil_estudante.py` contém PUT e DELETE, e `dados_contato.py` contém PUT. Há operações de escrita com dados pessoais, mas a solicitação desta revisão foca rotas que expõem dados; elas não são convertidas em alvos de leitura. A rota existente de listagem cobre currículos apenas no sentido de rota de consulta; não existe neste inventário rota GET de currículo individual por ID.

O contrato de credenciais fornecido contém apenas a seção 9 e remete ao cookie da seção 3, que não está incluída no arquivo analisado. Assim, o nome protocolar do cookie não está confirmado por essa evidência. Para o caso de credencial inválida, um valor de cookie sintaticamente comum como `sessao=credencial-invalida` pode ser usado como entrada negativa do relatório, sem alegar que `sessao` seja nome definitivo do contrato. A ausência de implementação torna esse detalhe incapaz de transformar o cenário em prova de validação de cookie.

As instruções aplicáveis no caminho `prompts/backend` foram verificadas; não há `AGENTS.md` nem `AGENTS.override.md` nessa pasta. O `AGENTS.md` da raiz foi fornecido pelo usuário nesta conversa.

## Problema enriquecido

### Resultado desejado

Definir uma especificação de teste black-box executável contra a aplicação ASGI real existente, que documente a lacuna de RF13 para a leitura de currículos. O resultado deve deixar visível que o endpoint real não exige sessão e que ainda não há autenticação nem validador de sessão.

### Atores e interesses

- Cliente HTTP de teste envia requisição sem cookie ou com cookie inválido.
- A rota real de listagem de currículos representa uma fronteira que deveria proteger dados de currículo.
- Responsáveis por backend precisam de um relatório honesto da lacuna até a implementação de RF13.
- Estudantes precisam que dados pessoais e currículos não sejam expostos sem autenticação.

### Evidências e fatos observados

- RF13 determina autenticação para acesso a informações pessoais e currículos.
- CT-RF13-02 trata a consulta de informações pessoais sem autenticação; CT-RF13-03 trata listagem ou acesso direto a currículo sem autenticação.
- A única rota GET atual no escopo desses dados que foi encontrada é `GET /estudantes/{usuario_id}/curriculos`.
- A rota recebe `usuario_id` no caminho, chama o executor injetado se houver, e não declara dependência de autenticação.
- A aplicação exportada em `backend.main.app` foi criada sem executor de listagem e a rota retorna 503 nessa composição atual.
- `usuario_autenticado` não existe no backend atual. Não há validador de sessão na API examinada.
- A rota real não precisa de corpo ou query adicional; um UUID de caminho sintaticamente válido permite alcançar o handler. O resultado normal atual com executor ausente é 503, não 401.

### Hipóteses

- O teste usará o `TestClient` do FastAPI contra `backend.main.app`, sem `dependency_overrides` nem fixtures/rotas adicionadas ao produto.
- O objetivo do xfail é preservar asserções futuras de segurança contra a aplicação real e registrar que o comportamento não está implementado hoje; não se espera que o caso passe agora.
- O corpo da resposta deve ser inspecionado para ausência dos campos/valores que identificariam conteúdo pessoal ou de currículo, sem depender de dados reais. Como a app atual retorna 503, o corpo não representa uma resposta protegida bem-sucedida.
- O caso de cookie inválido usa entrada sintética apenas para tentar a interface HTTP atual; não demonstra que o cookie foi lido ou validado.

### Perguntas em aberto

- Qual é o nome definitivo do cookie e como ele é codificado? A seção 3 do contrato referenciada não foi fornecida no arquivo analisado.
- Quando a API terá uma rota real de consulta a dados pessoais e um endpoint individual de currículo, caso necessários aos CTs?
- Quando autenticação e validador de sessão serão implementados para que xfails/skips possam ser reclassificados?

### Escopo

- Alvo existente: `GET /estudantes/00000000-0000-4000-8000-000000000001/curriculos`, usando `backend.main.app` e `TestClient`.
- Caso sem cookie: esperar status 401 e corpo sem dados privados; registrar como `xfail(strict=True)` com motivo literal `RF13 não implementada` enquanto a autenticação não existir.
- Caso com cookie inválido: enviar um cookie sintético inválido, esperar status 401 e corpo sem dados privados; registrar como `xfail(strict=True)` com o mesmo motivo literal `RF13 não implementada`.
- Sessão expirada e sessão revogada: registrar separadamente como `skip` com motivo literal `validador de sessão não existe`; sem validador, esses estados não podem ser representados black-box de forma verificável.
- Informar que o executor ausente na app padrão atualmente faz o endpoint responder 503. Esse resultado é evidência adicional da incompletude da rota e não deve ser convertido em sucesso de segurança.
- O artefato é um relatório de lacuna de RF13, não cobertura de um mecanismo integrado.

### Fora do escopo

- Criar ou modificar qualquer código no backend, inclusive endpoints, dependências, cookies, validadores, fixtures de rota ou hooks de teste.
- Inventar endpoint de dados pessoais ou endpoint individual de currículo.
- Simular mecanismo de autenticação que não existe ou usar override de dependência inexistente.
- Afirmar que a rota atual protege dados por retornar 503 sem executor.
- Validar assinatura, expiração, revogação, sessão válida, persistência, autorização por proprietário, executor não chamado por efeito de autenticação ou estado inalterado.
- Remover `xfail`/`skip` antes de a implementação real fornecer os comportamentos e contratos necessários.

### Critérios de sucesso

- O alvo escolhido corresponde a uma rota GET real inventariada no código; nenhuma rota fictícia é criada.
- A aplicação usada é `backend.main.app` através de `TestClient`, sem overrides de dependência de autenticação.
- Ausência de cookie e cookie inválido preservam as asserções futuras de 401 e resposta sem dados privados e são marcados `xfail(strict=True, reason="RF13 não implementada")`.
- Expirada e revogada aparecem como casos distintos em skip com razão exata `validador de sessão não existe`.
- CT-RF13-02 fica explicitamente sem alvo de consulta de dados pessoais; CT-RF13-03 pode ser relacionado à listagem existente, sem alegar cobertura aprovada enquanto xfail.
- A conclusão e o relatório declaram lacuna de RF13, sem dizer que mecanismo integrado foi coberto.

## Restrições aplicáveis

- Não é permitido implementar nada no backend; somente especificar/implementar testes sobre o código que existe.
- Não existe `usuario_autenticado` nem autenticação nas rotas analisadas.
- RF13 exige autenticação para consultas de dados pessoais e currículos.
- `TestClient` deve chamar a app real disponível; não criar rotas, overrides ou dependências para fazer a expectativa passar.
- A matriz prevê acesso negado para CT-RF13-02/03. O contrato indica 401 na fronteira, mas seu nome de cookie está fora do documento disponível.
- `xfail(strict=True)` comunica que a falha atual é esperada e faz um futuro passe inesperado falhar até que a classificação do caso seja revista; `skip` comunica que o estado não é exercitável sem validador.

## Classificação comentada

Esfera `engineering`: a decisão trata de especificação de testes de API existentes. As preocupações são `security`, `integration` e `observability`: verificar a fronteira HTTP real, não ocultar a ausência de controle e deixar explícitos os casos não executáveis. A saída atual é um relatório de lacuna; não constitui teste aprovado de segurança nem cobertura funcional do mecanismo.

## Decisão de roteamento

Manter `prompts/backend`. O inventário dinâmico das subpastas de `prompts` encontrou `backend`, `ambientes`, `frontend`, `templates`, `revisao` e `requisitos`. A continuidade da linhagem e o alvo ser a API backend prevalecem. Não foram encontradas instruções locais em `prompts/backend`.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `security` | Alta | Preservar expectativa 401 e não aceitar sucesso como cobertura | Currículos são dados privados e RF13 ainda não está implementada |
| `observability` | Alta | Distinguir xfail, skip e ausência de rota pessoal | Evita relatório enganoso sobre o que foi testado |
| `correctness` | Alta | Exercitar apenas interface real encontrada | Fixtures ou dependências inventadas não representam o sistema |
| `time-to-value` | Média | Documentar lacuna com código atual | Oferece evidência antes da implementação da segurança |

## Alternativas consideradas

- **A — Manter fixtures isoladas para exercitar wiring:** inviável nesta revisão, pois nenhum mecanismo de autenticação integrado existe e a restrição veda adicionar backend ou substituir dependência inexistente. Validaria um harness inventado.
- **B — Testar black-box apenas a rota GET real de currículo e reportar a lacuna com xfail/skip:** recomendada. Mantém a fronteira real, asserções de segurança futuras e estados não exercitáveis explicitamente classificados.
- **C — Aguardar a implementação de RF13 para criar qualquer cenário:** evita testes esperadamente falhos, mas não oferece relatório rastreável da lacuna presente nem deixa as expectativas de recusa registradas.
- **D — Inventar rota GET para dados pessoais ou currículo individual:** inviável porque contraria a restrição de alvo real e pode ser confundida com interface existente.

## Perfil de pagamento comparativo

Escala ordinal: `+2` melhora forte, `+1` melhora moderada, `0` neutro/desconhecido, `-1` piora moderada e `-2` piora forte. Pontuações não são somadas.

| Dimensão | Prioridade | A: fixtures | B: TestClient real | C: aguardar | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `security` | Alta | -2 | +1 | 0 | Alta | A simula gate ausente do sistema; B registra expectativas sem mascarar a falta; C não deixa oráculo pronto |
| `correctness` | Alta | -2 | +2 | +1 | Alta | B usa caminho real e comportamento observado; C também evita alvo inventado mas posterga a especificação |
| `observability` | Alta | 0 | +2 | -1 | Alta | xfail/skip e ausência de GET pessoal tornam as lacunas visíveis |
| `time-to-value` | Média | +1 | +2 | -2 | Média | B dá relatório imediato com interface existente; C posterga toda evidência |
| `simplicity` | Média | 0 | +1 | +2 | Média | C não cria teste agora; B limita-se a uma rota existente e duas entradas negativas |

## Histórico e decisão atual

### Decisão da versão anterior

A v003 recomendou duas rotas-semente de fixture protegidas por `usuario_autenticado`, controle negativo sem proteção, quatro estados inválidos e CTs reais em skip. Declarou cobertura do wiring no harness, não das rotas de produto.

### Decisão recomendada nesta versão

Abandonar fixtures e controle negativo. O único alvo real de leitura no escopo encontrado é `GET /estudantes/{usuario_id}/curriculos`; exercitá-lo black-box com `TestClient` contra `backend.main.app`, sem overrides. Preservar asserções de 401 e ausência de dados privados para falta de cookie e cookie inválido, em xfail estrito pelo motivo `RF13 não implementada`. Manter expirada e revogada como skips pelo motivo `validador de sessão não existe`. Registrar que a rota pessoal de consulta do CT-RF13-02 não existe e não inventar caminho. Resultado: relatório de lacuna de RF13, não cobertura de mecanismo integrado.

### Impacto da revisão

`revised`: a inspeção do código e a restrição nova invalidam a decisão de criar harnesses com autenticação simulada. O teste passa a mirar apenas a interface HTTP real existente e a reportar o comportamento atualmente ausente. A rota real retorna 503 na app padrão porque o executor não está configurado; isso não atende RF13 e não prova rejeição de credenciais.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | prioritized | Nenhum alvo de API inventado e classificação fiel do resultado atual | Inventário de decorators HTTP e composição real |
| `observability` | prioritized | Diferenciar falha esperada, skip e CT sem endpoint | Motivos literais e relatório de lacuna explícito |
| `security` | prioritized | Manter a expectativa 401 sem afirmar proteção existente | RF13 e contrato, contrastados com rota sem dependência |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `privacy` | Não expor nem semear dados reais em teste | Requisição usa UUID sintético; teste verifica corpo sem conteúdo privado; app padrão não tem executor |
| `reliability` | Execução determinística sem banco, cookie real ou sessão | `TestClient` em memória e ausência de dependências externas |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `security` | Resposta 503/200 atual ou futura pode ser confundida com rejeição segura | Alta | Estudantes e equipe backend |
| `observability` | A lacuna de RF13 e ausência de rota de dados pessoais ficam ocultas | Alta | Equipe e responsáveis por aceite |
| `correctness` | Um teste com fixtures pode passar sem qualquer autenticação no produto | Alta | Usuários e mantenedores |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `observability` e `security` | Casos permanecem xfail/skip até implementação | Sinal verde imediato da suíte | Aceitável: a falha esperada documenta a lacuna |
| `correctness` | CT-RF13-02 não terá chamada HTTP enquanto não existir rota GET pessoal | Abrangência atual | Necessário para não inventar interface |
| `privacy` | A app padrão sem executor não consegue demonstrar vazamento de resposta de sucesso | Profundidade do oráculo sem fixture de dados | Aceitável sob a restrição de usar somente estado atual |

## Riscos e efeitos de segunda ordem

- A marcação xfail pode normalizar uma falha de segurança se permanecer após RF13 ser implementada. O motivo literal e o critério de reclassificação devem ficar visíveis; uma implementação que passe inesperadamente gera XPASS e falha por `strict=True` até a revisão do teste.
- O 503 atual decorre do executor ausente, não da autenticação. O teste/relatório não deve descrevê-lo como acesso negado.
- Um UUID sintético no caminho ainda é uma identidade fornecida pelo cliente, prática que o contrato pretende substituir pelo contexto autenticado; esse defeito de desenho deve permanecer reportado.
- O teste de cookie inválido não valida nome, parsing ou assinatura porque o backend não tem validador e o nome do cookie não está no documento examinado.
- Sem uma rota GET de dados pessoais, CT-RF13-02 não pode ser coberto sem mudança de produto; sem GET individual por currículo, o escopo limita-se à listagem real.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| A listagem de currículos é rota real | Decorator GET e inclusão do router na composição | Inspecionar módulo e `create_app` | Rota removida ou path alterado |
| App padrão não implementa autenticação | Ausência de `usuario_autenticado`/dependência na rota e composição | Busca estática no backend e requisição TestClient | Dependência real introduzida |
| Falta de cookie não recebe 401 no estado atual | Resultado HTTP atual versus oráculo 401 | TestClient com `backend.main.app` | Status 401 após implementação deve virar XPASS estrito e acionar revisão |
| Cookie inválido não tem validador | Ausência de parser/validador de sessão no código | Inspeção do backend; caso permanece xfail | Validador e formato de cookie documentados |
| Dados pessoais não têm alvo GET existente | Inventário das rotas de perfil e contato | Buscar decorators HTTP e revisar módulos | Nova rota GET implementada e especificada |
| Expiração/revogação não são testáveis | Ausência de validador e estado de sessão | Inspeção de componentes | Infraestrutura real de sessão disponível |
| Relatório não afirma cobertura integrada | Revisar texto, marks e resumo de execução | Confirmar xfail/skip e declaração de escopo | Saída descrita como teste aprovado de mecanismo |

## Handoffs e atividades posteriores

- Handoff para implementação de produto: adicionar a autenticação e o validador de sessão conforme contrato; esta análise não autoriza nem executa essas mudanças.
- Handoff para especificação: fornecer a seção 3 do contrato de credenciais ou definir o nome e o formato do cookie antes de interpretar o caso inválido como teste de protocolo.
- Handoff para requisitos/API: definir e implementar rota real de leitura de dados pessoais e rota individual de currículo se necessárias à matriz; então associar CT-RF13-02/03 a alvos concretos.
- Após RF13 existir, remover xfails e skips individualmente, executar os casos na API real com sessão e dados sintéticos apropriados e atualizar alegações de cobertura conforme resultados observados.
- Nenhum teste unitário, alteração de backend, CI, deploy ou operação externa faz parte desta decisão.

## Síntese

A v004 corrige o alvo com base no código existente. Há uma rota real `GET /estudantes/{usuario_id}/curriculos`, sem autenticação, mas a aplicação padrão responde 503 porque não possui executor configurado. Não há rota GET para dados pessoais nem rota individual de currículo encontrada; portanto, CT-RF13-02 não recebe um endpoint inventado. Recomenda-se especificar casos black-box por `TestClient` contra `backend.main.app`: ausência de cookie e cookie inválido mantêm expectativa 401/corpo sem dados privados em `xfail(strict=True, reason="RF13 não implementada")`; sessão expirada e revogada ficam em skip com motivo `validador de sessão não existe`. Esse resultado é relatório de lacuna de RF13, não cobertura de mecanismo integrado. A incerteza principal é quando o mecanismo e o contrato completo do cookie serão definidos.
