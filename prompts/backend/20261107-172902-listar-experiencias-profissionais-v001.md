---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-11-07T17:29:02-03:00"
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
    - path: "AGENTS.md"
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/AGENTS.md"
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "prompts/README.md"
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/api/experiencia_profissional.py"
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/application/ports.py"
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioExperienciaProfissional, linhas 279–344"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/infrastructure/persistence/sqlalchemy/repositorio_experiencia_profissional.py"
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/domain/itens_perfil.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "_chave_ordenacao_experiencia e ordenar_experiencias, linhas 371–406"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/application/previa_versao_curriculo.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "referências a ordenar_experiencias: import, docstring e chamada, linhas 30, 138 e 170"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/api/factory.py"
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "fim da assinatura de create_app e registro dos routers, linhas 290–308 e 415–445"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/main.py"
      relationship: primary
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "app = create_app, linhas 250–293"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/api/formacao_academica.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "DTO de coleção, protocolo, assinatura do router e GET, linhas 179–288"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "src/backend/api/middleware_autenticacao.py"
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ROTAS_PUBLICAS e atribuição do dono autenticado, linhas 36–52 e 100–120"
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "docs/wireframes/05-experiencias.md"
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
    - path: "prompts/backend/20261017-100000-expor-ordenacao-experiencias-consulta-v001.md"
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 66af3007161ecdf5eca6f8cb08557b468aafafa6"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "Desenho de contrato HTTP, consulta interna e composição do servidor; backend é mais específico que levantamento de requisitos ou revisão geral."
classification:
  sphere: engineering
  concerns: [architecture, security, integration]
  decision_kind: design
  scope: component
  lifecycle: evolution
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — listar experiências profissionais do estudante autenticado

## Solicitação original

> $decision-analysis-v4 Precisamos de um endpoint GET para experiencias-profissionais. Ele deve fazer sentido com os endpoints já existentes.

## Informações complementares

Nenhum identificado para esta demanda. Contexto observado na sessão: o GET de formações acadêmicas foi desenvolvido em atividades anteriores. Esse padrão é apoio de desenho, não aprovação automática do contrato de experiências. Não há pedido de implementação nesta atividade.

## Mudanças desde a versão anterior

Nenhum identificado. Modo `initial`: não foi localizada análise de listagem dedicada de experiências. O antecedente de 17/10 trata exclusivamente da ordenação na prévia e deixa a listagem dedicada fora de seu escopo; não é uma versão anterior desta linhagem. A análise de formações trata de outro recurso.

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `AGENTS.md` | context | prose | prompt-instruction | Markdown | whole-file: arquivo completo | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `src/backend/AGENTS.md` | context | prose | prompt-instruction | Markdown | whole-file: arquivo completo | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `prompts/README.md` | context | prose | documentation | Markdown | whole-file: arquivo completo | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `src/backend/api/experiencia_profissional.py` | primary | source-code | production | Python | whole-file: arquivo completo | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `src/backend/application/ports.py` | supporting | source-code | schema-contract | Python | selected-section: RepositorioExperienciaProfissional, linhas 279–344 | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_experiencia_profissional.py` | primary | source-code | production | Python | whole-file: arquivo completo | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `src/backend/domain/itens_perfil.py` | supporting | source-code | production | Python | selected-section: _chave_ordenacao_experiencia e ordenar_experiencias, linhas 371–406 | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `src/backend/application/previa_versao_curriculo.py` | supporting | source-code | production | Python | selected-section: referências a ordenar_experiencias: import, docstring e chamada, linhas 30, 138 e 170 | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `src/backend/api/factory.py` | primary | source-code | production | Python | selected-section: fim da assinatura de create_app e registro dos routers, linhas 290–308 e 415–445 | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `src/backend/main.py` | primary | source-code | production | Python | selected-section: app = create_app, linhas 250–293 | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `src/backend/api/formacao_academica.py` | supporting | source-code | production | Python | selected-section: DTO de coleção, protocolo, assinatura do router e GET, linhas 179–288 | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `src/backend/api/middleware_autenticacao.py` | supporting | source-code | production | Python | selected-section: ROTAS_PUBLICAS e atribuição do dono autenticado, linhas 36–52 e 100–120 | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `docs/wireframes/05-experiencias.md` | supporting | prose | documentation | Markdown | whole-file: arquivo completo | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |
| `prompts/backend/20261017-100000-expor-ordenacao-experiencias-consulta-v001.md` | supporting | prose | documentation | Markdown | whole-file: arquivo completo | working-tree baseado em `66af300`; conteúdo não necessariamente idêntico ao commit |

### Limites da evidência dos artefatos

Inspeção estática dos recortes indicados, sem executar testes, banco, Uvicorn ou chamadas HTTP. O working tree contém alterações anteriores em formação, Application, composição e testes; devem ser preservadas. Não se presume equivalência ao HEAD. Buscas em nomes e referências serviram somente à descoberta; arquivos não lidos não sustentam decisões. Não foram consultadas issues externas, volume de dados, consumidores reais ou metas de desempenho. Instruções da skill e referências metodológicas foram lidas para orientar o processo, não como evidência de comportamento do produto.

## Problema enriquecido

### Resultado desejado

Permitir ao estudante recuperar suas experiências profissionais e respectivos IDs para consultar a lista, editar e remover itens sem depender da resposta de criação ou de uma seleção de currículo.

### Atores e interesses

- Estudante: recuperar e gerenciar sua coleção de experiências.
- Consumidor da API/Swagger: contrato previsível, campos já conhecidos e coleção vazia representada como sucesso.
- Equipe de backend: isolamento entre usuários, regra de apresentação centralizada e dependências realmente compostas no servidor.

### Evidências e fatos observados

1. `api/experiencia_profissional.py` publica POST na coleção e PUT/DELETE no item, sem GET. O dono é resolvido por `_usuario_autenticado(request)`, exclusivamente de `request.state.usuario_id`.
2. `ExperienciaProfissionalResposta` expõe sete campos: `id`, `usuario_id`, `empresa`, `cargo`, `descricao`, `data_inicio`, `data_fim`. Não contém enum de status ou `deleted_at`; término nulo significa experiência em andamento.
3. `_resposta` já projeta a entidade nesses campos. Pode atender a leitura com atualização de documentação, mantendo POST/PUT inalterados.
4. A porta e o repositório consultam por ID/dono e suportam exclusão lógica. A consulta ativa usa `deleted_at IS NULL`. Ainda não oferecem listagem por proprietário.
5. `ordenar_experiencias` existe no domínio e já é chamado pela prévia. A ordenação primária é início decrescente; experiência em andamento tem prioridade somente em empate de início.
6. A factory registra o router de experiências com executores opcionais, mas a chamada atual de `main.app` não fornece cadastro, edição ou exclusão de experiências. Não presumir uma jornada de escrita funcional no Uvicorn.
7. O novo GET de formações é um precedente de coleção própria em envelope, com DTO público existente, estado autenticado e respostas 200/401/503.
8. O wireframe 05 prevê múltiplas experiências e ações Adicionar, Editar, Remover e Ordenar. Não estabelece protocolo de ordenação manual nem campo persistido de posição.
9. O recorte do middleware mostra que experiências não são públicas e que o dono validado é instalado no estado da requisição.

### Hipóteses

H1: GET significa listagem da coleção própria, não consulta individual por ID. A lista do wireframe e a necessidade de descobrir os IDs sustentam essa leitura.

H2: a coleção por estudante admite leitura integral sem paginação nesta primeira entrega. Não há volumetria que comprove capacidade; tratar como hipótese a validar antes de uso amplo.

H3: a lista deve usar a ordenação automática atual do domínio. A ação Ordenar no wireframe não é suficiente para introduzir ordenação manual nesta demanda; o antecedente da prévia também a exclui de seu escopo.

### Perguntas em aberto

- Qual é o volume representativo de experiências por estudante e o tamanho típico de descricao? Isso pode justificar paginação futura.
- O produto precisa de ordenação manual em outra entrega? Não bloqueia o GET com a regra já existente; deve motivar decisão separada se for necessário mudar essa regra.
- Quando será composta a escrita de experiências em `main.app`? A resposta condiciona a jornada integrada completa, não a definição do contrato de leitura.

### Escopo

Definir GET da coleção própria, DTO de listagem, entrada/caso de uso de leitura, porta e consulta SQLAlchemy por dono/estado ativo, executor de sessão curta, registro na factory e ligação em `main.app`, documentação e validação por níveis separados.

### Fora do escopo

GET por ID, outros estudantes, busca, filtros, paginação inicial, ordenação manual, frontend, novas regras de texto/período, enum de status, restauração, purga, migration sem necessidade demonstrada, alteração da prévia e mudanças de comportamento de POST/PUT/DELETE. A composição ausente dos executores de escrita fica como handoff separado, sem correção implícita nesta análise.

### Critérios de sucesso

- `GET /experiencias-profissionais` recupera somente experiências ativas do dono da sessão, sem parâmetros e sem corpo.
- Resposta 200 com `{"experiencias": [...]}`; vazio é `{"experiencias": []}`, nunca 404.
- Cada item contém exatamente os sete campos públicos existentes, com data_fim anulável, sem deleted_at ou novos campos derivados.
- Resultado usa `ordenar_experiencias`, independentemente da ordem incidental do armazenamento; o transporte não reordena.
- Dono informado pelo cliente em query, caminho ou corpo nunca modifica o dono da consulta.
- Executor ausente tem 503 controlado, e requisição não autenticada segue o mecanismo existente.
- Consulta não escreve, não confirma mutações e não interfere nos dados usados por operações existentes.
- Factory e `main.app` recebem o executor de leitura quando a persistência está configurada; aprovação por teste unitário não substitui validação real com PostgreSQL.

## Restrições aplicáveis

- Clean Architecture/DDD conforme AGENTS da raiz e do backend: domínio independente de HTTP/ORM; Application depende de portas; composição fica na camada externa.
- Propriedade e exclusão ativa devem filtrar a consulta no armazenamento. Não carregar coleção global para filtrar no handler.
- Presentation order pertence à regra de domínio existente; não copiá-la para SQL, DTO ou controller.
- Identidade da sessão existente; não criar política de autenticação/autorização, rotas públicas, novos canais de token ou CORS especial.
- Persistência Code First; a leitura usa schema existente e, por si só, não exige migration.
- Funções, classes e DTOs devem documentar responsabilidade, abordagem e finalidade; código novo deve registrar proveniência quando implementado pelas skills correspondentes.
- Nix backend para desenvolvimento e unitários; Nix tests para integração e níveis superiores; Nix quality para gates; Git fora do Nix.
- Nesta análise, somente um novo Markdown pode ser escrito. Não alterar código, outras análises ou mudanças anteriores do working tree.

## Classificação comentada

`engineering` é a esfera primária: a demanda define uma capacidade da API e suas conexões ao núcleo e armazenamento. Preocupações: `architecture` pelas fronteiras; `security` pelo isolamento entre contas; `integration` pela ligação efetiva ao servidor. Objeto `mixed`, pois demanda e contratos existentes têm importância equivalente. Incerteza média por volumetria e composição de escrita ausente; risco médio pelo impacto de exposição de dados e reversibilidade moderada de um contrato público consumido.

## Decisão de roteamento

Inventário observado das subpastas imediatas de prompts: `ambientes`, `backend`, `frontend`, `requisitos`, `revisao`, `templates`. Destino: `prompts/backend`, confiança alta. O propósito é desenhar contrato e implementação de servidor; requisitos seria menos específico e revisão não descreve a atividade principal. O README confirma essa organização. Não foram encontrados AGENTS adicionais ou overrides em prompts e suas candidatas; a raiz governa a escrita. Nenhuma categoria nova será criada.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| user-value | Alta | Recuperar coleção e IDs | Completa a navegação necessária para editar/remover |
| correctness | Alta | Mesmos campos, somente ativas e regra única de ordem | Evita divergência com escrita e prévia |
| security | Obrigatória | Somente dono autenticado | Evita vazamento de histórico profissional |
| simplicity | Média | Menor contrato útil e coerente com formações | Reduz parâmetros e duplicação sem demanda |
| scalability | Média | Validar limites com volume representativo | Coleção integral e descrições aumentam resposta |

## Alternativas consideradas

- A — Estado atual: manter escrita e consulta indireta pela prévia. Referência comparativa; não atende a nova demanda e a prévia contém seleção de currículo, não toda a coleção.
- B — GET da coleção própria sem paginação, envelope experiencias, DTO existente e ordenação de domínio. Viável e recomendado como entrega inicial.
- C — GET da coleção própria com paginação desde a primeira versão. Viável, mas exige protocolo de páginas e ordenar globalmente antes de recortar; não há evidência de volume que pague esse custo agora.
- D — Somente GET por ID. Viável tecnicamente; permite consultar item conhecido, mas não descobrir coleção/IDs e não atende H1. Pode ser demanda complementar.

Listagem global ou escolha arbitrária de usuário sem autorização são inviáveis pelas restrições de propriedade e não participam da comparação de benefícios.

## Perfil de pagamento comparativo

Escala ordinal relativa a A: +2 melhora forte, +1 moderada, 0 neutro/desconhecido, -1 piora moderada, -2 forte. Não somar. Zero em segurança indica manutenção do limiar obrigatório, não ausência de trabalho de proteção.

| Dimensão | Prioridade | A | B | C | Confiança | Base |
|---|---|---|---|---|---|---|
| user-value | Alta | 0 | +2 | +2 | Alta | Ambas recuperam coleção; C exige navegação entre páginas |
| correctness | Alta | 0 | +1 | +1 | Alta | Regra e DTO existentes; C precisa manter a ordem global |
| security | Obrigatória | 0 | 0 | 0 | Alta | B/C só são viáveis com identidade resolvida e consulta escopada |
| simplicity | Média | 0 | -1 | -2 | Alta | Novo fluxo em B; C também introduz protocolo de paginação |
| scalability | Média | 0 | 0 | +1 | Baixa | C limita a resposta; volume real ainda desconhecido |

D entrega ganho parcial de user-value, mas deixa a descoberta pendente. B prevalece sobre D pelo resultado desejado e sobre C pela simplicidade, aceitando o custo de ler a coleção inteira sob H2.

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado nesta linhagem. A decisão de 17/10 sobre prévia é um antecedente independente e continua válida no próprio escopo.

### Decisão recomendada nesta versão

Adotar B, com `status: proposed` para revisão e aprovação humana:

1. Publicar `GET /experiencias-profissionais`, sem corpo e sem parâmetros de query/caminho. Nenhum usuario_id fornecido pelo cliente pode afetar a consulta. Não criar GET individual neste escopo.
2. Devolver `ListagemExperienciasProfissionaisResposta` com `experiencias: list[ExperienciaProfissionalResposta]`; 200 inclusive para coleção vazia. Atualizar documentação do DTO e de `_resposta` para contemplar leitura, sem alterar campos/valores de POST e PUT.
3. Reutilizar `_usuario_autenticado(request)` no handler. Montar `ListarExperienciasProfissionaisEntrada(usuario_id: UsuarioId)` a partir do estado validado e chamar executor com contrato assíncrono.
4. Acrescentar a `RepositorioExperienciaProfissional` a capacidade `listar_ativas_por_usuario(usuario_id: UsuarioId) -> Sequence[ExperienciaProfissional]`, sem modificar métodos existentes. Documentar somente do dono, somente ativas e sem ordem de apresentação garantida.
5. Criar `ListarExperienciasProfissionais`: consultar a porta uma vez e devolver `ordenar_experiencias(resultado)`. Resultado vazio é tupla vazia. Não validar texto, enum ou período novamente, não escrever e não adicionar regras de negócio.
6. Implementar a porta no repositório SQLAlchemy com `WHERE usuario_id = dono AND deleted_at IS NULL`, converter por `para_experiencia` e não adicionar ORDER BY de apresentação, escrita, flush ou commit ao método.
7. Usar a regra existente: início mais recente primeiro; somente em empate de início, sem término primeiro; depois término decrescente e ID textual para desempate. Não colocar todas as experiências em andamento antes de todas as encerradas, pois isso contradiz o domínio.
8. Criar executor de leitura com uma sessão assíncrona curta por chamada, delegando ao caso existente e preservando o resultado; nenhum commit de mutação, sessão global ou engine nova por requisição.
9. Adicionar o parâmetro opcional de leitura ao fim de `create_app` e ao fim de `criar_router`, preservando chamadas posicionais existentes. Registrar no router e injetar em `main.app` com a fábrica de sessões e ciclo de vida da engine já existentes. A ligação da leitura é parte do aceite, não um detalhe opcional.
10. Reutilizar política de erros existente: 503 `Listagem indisponível.` para executor ausente; defesa local de identidade inválida com 401 `Autenticação necessária.`; requisição sem sessão válida passa pelo middleware e recebe seu 401 uniforme antes do handler. Não prometer 503 para requisição sem autenticação. Coleção vazia não gera 404; falha do armazenamento não pode ser convertida em lista vazia artificial nem expor SQL/credenciais.
11. OpenAPI documenta resumo, descrição, cookie de sessão, ordem, ausência de corpo/parâmetros/paginação e respostas 200/401/503, mantendo a configuração global existente.

Exemplo meramente ilustrativo de item sintético:

```json
{
  "experiencias": [
    {
      "id": "00000000-0000-0000-0000-000000000001",
      "usuario_id": "00000000-0000-0000-0000-000000000101",
      "empresa": "Empresa Exemplo",
      "cargo": "Desenvolvedor",
      "descricao": "Desenvolvimento de aplicações.",
      "data_inicio": "2024-02-01",
      "data_fim": null
    }
  ]
}
```

### Impacto da revisão

Nenhum identificado: análise inicial. O antecedente da prévia é reutilizado para a ordem, sem alteração retrospectiva.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| user-value | prioritized | Recuperar coleção sem guardar IDs de criação | Wireframe e H1 |
| correctness | prioritized | Mesmos campos e uma regra de apresentação | DTO, mapper e ordenar_experiencias |
| simplicity | prioritized | Uma rota sem filtros ou protocolo de páginas | Comparação B/C/D |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| security | Nenhum item de outro dono ou excluído | Consulta obrigatoriamente escopada e identidade da sessão |
| scalability | Leitura integral sob H2 validada com massa representativa | Sem capacidade certificada nesta análise; medir antes de uso amplo |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| user-value | Dependência de IDs conhecidos ou de seleção curricular | Alta | Estudante e consumidores |
| correctness | Datas/ordem divergentes, itens excluídos reaparecendo | Alta | Estudante |
| simplicity | Navegação e parâmetros extras sem necessidade demonstrada | Média | Consumidores e manutenção |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| user-value | Implementar uma fatia vertical nova com testes | delivery-speed | Necessário para consulta da coleção |
| correctness | Ordenar em memória após leitura integral | scalability | Aceito provisoriamente sob H2 |
| simplicity | Adiar paginação, GET individual e ordenação manual | optionality | Demandas específicas justificam reavaliação |

## Riscos e efeitos de segunda ordem

- O wireframe cita Ordenar, mas a proposta só usa a ordenação automática atual. Necessidade de ordenação manual exige decisão específica; não implementar posição persistida por inferência.
- Descrições podem tornar a resposta grande mesmo com poucos itens. Não introduzir resumo truncado silenciosamente; reavaliar paginação ou projeção mediante evidência.
- Confundir `data_fim: null` com status de formação produziria regra incorreta: experiência não possui esse enum no DTO.
- Um SELECT sem ambos os filtros expõe itens alheios ou excluídos; verificar predicados e isolamento real em níveis distintos.
- Um teste de handler/factory verde não prova `main.app` nem persistência. A integração precisa usar o caminho real configurado.
- Os executores de POST/PUT/DELETE de experiências não estão injetados em `main.app`. Isso limita a jornada completa; não atribuir eventual 503 desses métodos ao GET nem corrigi-los silenciosamente nesta fatia.
- A leitura histórica de currículos pode ter critérios diferentes de exclusão. Não substituir consultas históricas pela nova listagem ativa.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| H1: coleção atende ao consumidor | IDs recuperáveis e campos suficientes para selecionar item | Revisão do contrato/Swagger com dados sintéticos | Consumidor exige consulta individual adicional |
| H2: resposta integral adequada | Quantidade e tamanho representativos de descrições | Medição local isolada, sem limiar inventado nesta análise | Limites definidos pela equipe não atendidos |
| H3: ordem atual adequada | Inícios distintos e iguais, fins nulos, fins diferentes e IDs empatados por datas | Unitários do caso com porta double comparados a ordenar_experiencias | Necessidade de ordem manual ou diferente da prévia |
| Sem efeitos de escrita | Única chamada à porta com dono da entrada; nenhuma escrita | Unitários e snapshot persistido em integração | Qualquer salvar/atualizar/marcar_excluida no GET |
| Tradução HTTP | Sete campos exatos, ordem preservada, vazio e erros locais | Unitários do handler com executor double, sem servidor | DTO ou estado de dono divergentes |
| Predicados do adapter | Dono e deleted_at na mesma consulta; conversão e ausência de ORDER BY de apresentação | Unitários com AsyncSession double e inspeção da query | Um filtro ausente ou regra de ordem duplicada |
| Isolamento real | Duas contas com ativos/excluídos, coleção vazia e cookie real | Integração em PostgreSQL efêmero, ambiente Nix tests | Qualquer item alheio/excluído ou vazamento de detalhe interno |
| Binding no Uvicorn | Executor presente com fábrica configurada e ciclo de sessão curto | Unitário de composição e teste integrado de main.app | Rota registrada mas executor ausente, sessão global ou commit de mutação |
| Jornada POST → GET → PUT → GET → DELETE → GET | Escritas compostas e mudanças visíveis entre sessões | Integração posterior após resolver o handoff de escrita | 503 de escrita por composição ausente; relatar dependência, não mascarar |

## Handoffs e atividades posteriores

1. Aprovar ou revisar esta proposta; a solicitação atual autoriza análise, não implementação.
2. `$backend-domain-orchestration-v2`: porta, entrada, caso de uso e exportações; somente unitários do núcleo com doubles. Reutilizar ordenar_experiencias sem alterar sua regra.
3. `$backend-adapters-drivers-v2`: consulta SQLAlchemy, handler/DTO/protocolo de transporte, executor de leitura, factory e main.app; somente testes unitários isolados. Preservar o working tree anterior e os comportamentos de escrita.
4. `$integration-system-testing-v1`: PostgreSQL temporário migrado, autenticação, duas contas, excluídas, ausência de mutação, OpenAPI e composição real. Não confundir teste de main.app via ASGI com certificação de processo Uvicorn; indicar qual alvo foi executado.
5. Registrar atividade separada para ligar os executores de escrita de experiências no main.app. Enquanto isso, validar o GET integrado com dados sintéticos preparados pela fixture de teste; a jornada completa permanece condicionada a essa atividade.
6. Reavaliar paginação e ordenação manual somente com evidência de necessidade. Não alterar análises anteriores, ambiente, cache ou frontend nesta entrega.

## Síntese

Proposta B: GET autenticado da coleção própria em experiencias, com os sete campos existentes, apenas itens ativos e a regra ordenar_experiencias. O GET deve ser composto no main.app. A principal incerteza é a volumetria; a composição de escrita ausente é uma dependência explícita da jornada completa. Nenhuma implementação ou validação dinâmica foi realizada nesta atividade.
