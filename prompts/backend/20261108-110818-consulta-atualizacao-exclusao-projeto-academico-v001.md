---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-11-08T11:08:18-03:00"
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
    - {path: src/backend/api/projeto_academico.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/main.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "imports e composição app = create_app", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/factory.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "parâmetro e inclusão do router de projeto", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/domain/itens_perfil.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "constantes de projeto; ProjetoAcademico; _normalizar_texto_projeto", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/ports.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: selected-section, locator: "RepositorioProjetoAcademico e GeradorProjetoAcademicoId", content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/application/cadastro_projeto_academico.py, relationship: supporting, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/infrastructure/persistence/sqlalchemy/projeto_academico.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_projeto_academico.py, relationship: primary, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/api/middleware_autenticacao.py, relationship: supporting, representation: source-code, function: production, format: Python, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md, relationship: context, representation: prose, function: documentation, format: Markdown, analysis_scope: selected-section, locator: "frontmatter e trechos de decisão, limites e handoffs disponíveis na leitura", content_state: working-tree, revision: null, availability: partial}
    - {path: prompts/README.md, relationship: context, representation: prose, function: documentation, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: AGENTS.md, relationship: context, representation: prose, function: prompt-instruction, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
    - {path: src/backend/AGENTS.md, relationship: context, representation: prose, function: prompt-instruction, format: Markdown, analysis_scope: whole-file, locator: null, content_state: working-tree, revision: null, availability: available}
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "Demanda de evolução de API, domínio e persistência do backend; não é revisão de código nem levantamento isolado."
classification:
  sphere: engineering
  concerns: [implementation, domain, security]
  decision_kind: design
  scope: component
  lifecycle: evolution
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — consulta, atualização e exclusão de projeto acadêmico

## Solicitação original

$decision-analysis-v4 Para a parte de projeto-academico precisamos de um endpoint para consultar, um para atualizar e outro para excluir. Além disso, eles precisam poder ser testados pelo Swagger, ou seja, devem estar no main. O título e a descrição devem ser limitados pela quantidade de caracteres

## Informações complementares

Nenhuma informação adicional de produto identificada. A skill fornecida delimita esta atividade à análise, permitindo escrever somente este Markdown. Limites numéricos e interpretação de consulta abaixo são propostas baseadas no código, não declarações do usuário.

## Mudanças desde a versão anterior

Nenhum identificado — modo inicial. As análises anteriores de cadastro são contexto de uma capacidade distinta; a nova demanda acrescenta três operações, sem pedir revisão do cadastro. A linhagem de cadastro não é substituída.

## Artefatos analisados

O inventário individual, recorte, representação, função, formato e estado de cada arquivo estão em `subjects.files`, que integra esta seção. API, composição, domínio, porta e persistência são objetos principais; cadastro e middleware são apoio; instruções, convenções e análise histórica são contexto.

### Limites da evidência dos artefatos

Leitura estática do working tree, sem referência de commit fixada e sem executar código ou testes. A saída conjunta de leitura da análise histórica sofreu truncamento; somente os trechos disponíveis sustentam contexto, sem validação integral daquela análise. Não foram examinados testes existentes, todas as migrations nem os consumidores de referências a projetos. Não se conclui que exclusão física seja segura. Foram lidas também as referências da skill e a orientação Nix de `docs/configuracao-ambiente.md` como instruções operacionais.

## Problema enriquecido

### Resultado desejado

Permitir ao estudante consultar, atualizar e excluir seu projeto persistido, com operações funcionais pela aplicação `backend.main:app` e pelo Swagger, mantendo limites coerentes de texto.

### Atores e interesses

Estudante administra seus projetos; consumidores de currículos precisam de referências consistentes; equipe precisa de contratos documentados e testáveis.

### Evidências e fatos observados

- O router atual oferece POST de cadastro e POST de sugestão de descrição; os três métodos solicitados não estão nele.
- A factory inclui esse router, mas `main.py` não injeta executor de cadastro de projeto nem executores das novas operações. Registro em OpenAPI e execução persistida são critérios diferentes.
- A porta e o repositório concreto de projeto examinados só oferecem `salvar`; o adapter usa `add` e `flush`, portanto não deve ser presumido como implementação de atualização.
- O domínio limita título a 1–200, descrição a 1–2000 e tecnologias a 1–300 caracteres após `strip`, recusa controles Unicode Cc e normaliza os textos. O ORM declara checks correspondentes.
- O DTO valida comprimentos por validator; suas declarações `str` não expressam explicitamente `minLength`/`maxLength` no schema. O corpo aparece por `openapi_extra`.
- O middleware autentica por cookie e popula `request.state.usuario_id`. Sua comparação de UUIDs de proprietário no caminho cobre perfil/currículo, não projetos; autenticação não substitui autorização do recurso.

### Hipóteses

Consultar significa obter um projeto por ID. Atualizar significa substituir os três textos via PUT; identidade e proprietário permanecem imutáveis. Os limites atuais atendem à demanda. Exclusão lógica é preferível até validar referências em currículos. Estas são hipóteses revisáveis.

### Perguntas em aberto

A consulta pretendida é detalhe por ID ou listagem? A exclusão deve preservar versões de currículo? Produto deseja limites diferentes de 200/2000? Nenhuma resposta é inventada: a proposta usa detalhe e limites existentes; a política de referências requer investigação antes de implementar exclusão.

### Escopo

GET, PUT e DELETE por ID, contratos internos, autorização por proprietário, persistência transacional, composição em factory/main, documentação OpenAPI de corpo, limites e respostas, testes pertinentes. Conectar também o cadastro já existente ao main é uma dependência funcional para testar o ciclo pelo Swagger.

### Fora do escopo

Listagem, paginação, tela, reformulação do assistente, novos campos, PATCH e redesenho de currículos. Nenhuma implementação nesta atividade.

### Critérios de sucesso

- GET `/projetos-academicos/{projeto_id}` retorna 200 com DTO explícito para projeto próprio ativo.
- PUT no mesmo caminho recebe título, descrição e tecnologias obrigatórios e retorna 200 com DTO atualizado; nenhuma mudança de ID/proprietário.
- DELETE no mesmo caminho retorna 204 sem corpo; consultas e mutações posteriores tratam o projeto como ausente.
- Projeto inexistente, excluído ou de outro usuário retorna 404 uniforme, sem vazamento e sem alteração; sessão ausente/inválida retorna 401.
- UUID ou corpo inválido retorna 422; dependência persistida não configurada retorna 503 para usuário autenticado.
- As rotas aparecem em `/openapi.json` e `/docs` da aplicação do main; com banco configurado, migrations aplicadas e sessão válida executam operações reais.
- Título e descrição aceitam exatamente os limites, rejeitam excesso sem truncamento e mantêm a semântica atual de normalização; o schema informa esses limites.

## Restrições aplicáveis

Clean Architecture e DDD: invariantes no domínio, portas e casos de uso internos, infraestrutura externa, DTOs na borda e composição externa. Toda função/classe/DTO alterada deve documentar o que faz, como e por quê. Alteração de schema usa ORM Code First e migration. Testes unitários pertinentes obrigatórios no Nix backend; integração e níveis superiores no Nix tests. Git fora do Nix. Não tornar rotas públicas para viabilizar Swagger. A única escrita nesta análise é este novo Markdown.

## Classificação comentada

Engenharia de componente em evolução, com implementação de API, invariantes de domínio e segurança de propriedade. Risco médio por mutações e exclusão sobre dados reutilizados. Objeto misto: intenção do usuário e comportamento observado no conjunto de arquivos têm importância equivalente.

## Decisão de roteamento

Inventário observado: `ambientes`, `backend`, `frontend`, `requisitos`, `revisao`, `templates`. Backend é o destino específico para contratos HTTP, composição e persistência; requisitos seria menos específico e revisão sugeriria avaliação de uma implementação pronta. Não há instruções locais adicionais encontradas em prompts.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | Alta | Invariantes e operações atômicas | Evitar projeto inválido ou mudança parcial |
| security | Alta | Somente o proprietário | Isolar dados de estudantes |
| reliability | Alta | Preservar referências existentes | Evitar perda em currículos |
| simplicity | Média | Contratos explícitos mínimos | Reduzir variações de entrada |
| delivery-speed | Média | Reutilizar limites e composição | Entregar capacidade utilizável |

## Alternativas consideradas

A — Estado atual: somente cadastro/sugestão no router, sem novas operações ou composição de projeto no main. Inviável frente à solicitação.

B — GET por ID, PUT de substituição completa e DELETE lógico; preservar limites atuais, autorização no fluxo interno e composição real. Viável como proposta, condicionada à investigação das referências; recomendada pela menor variedade de estados de entrada.

C — GET por ID, PATCH parcial e DELETE lógico, com a mesma autorização e composição. Viável, mas precisa definir ausência versus nulo, composição dos valores atuais e validação do resultado completo. Beneficia clientes que editam campos isoladamente, necessidade não demonstrada.

Exclusão física não é considerada viável sem examinar referências e política de versões; validação apenas no Swagger ou somente no DTO viola a proteção de invariantes no domínio.

## Perfil de pagamento comparativo

Escala ordinal relativa ao estado atual: +2 melhora forte, +1 moderada, 0 neutro/desconhecido, -1 piora moderada, -2 forte. Não somar.

| Dimensão | Prioridade | A | B | C | Confiança | Base |
|---|---|---:|---:|---:|---|---|
| correctness | Alta | 0 | +2 | +2 | Média | Modelo validado na atualização completa |
| security | Alta | 0 | +1 | +1 | Média | Novas operações filtradas por dono |
| reliability | Alta | 0 | +1 | +1 | Baixa | Preservação por exclusão lógica depende de consumidores |
| simplicity | Média | 0 | -1 | -2 | Média | PATCH acrescenta estados de entrada |
| delivery-speed | Média | 0 | +2 | +1 | Média | PUT reutiliza contrato dos três textos |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado nesta linhagem. O cadastro anterior é contexto e não comprovação do estado atual.

### Decisão recomendada nesta versão

Adotar B como proposta: consulta de detalhe e substituição por ID, exclusão lógica sujeita à política de referências, com proprietário exclusivamente da sessão. Acrescentar casos de uso específicos e portas para recuperar projeto próprio ativo, atualizar e excluir; definir assinaturas durante implementação respeitando o modelo de agregados. O adapter deve filtrar por ID, proprietário e estado ativo também nas mutações, usando transação e verificando ausência, sem confiar apenas em leitura prévia.

Manter 200/2000 e tecnologias 300, medir texto normalizado com a mesma regra do domínio, rejeitar excesso em vez de cortar. Expressar limites no OpenAPI sem trocar acidentalmente validação de texto normalizado por comprimento bruto; documentar a contagem Unicode usada por Python, distinta de bytes ou grafemas visuais. Validar invariantes ao construir a nova versão da entidade.

Ampliar factory e main para injetar executores reais, inclusive cadastro existente para o ciclo de teste. Ausência de banco preserva rotas documentadas e indisponibilidade explícita. No Swagger, autenticar pelo fluxo de sessão existente na mesma origem e validar envio do cookie; em HTTP local usar configuração deliberada de cookie compatível, sem enfraquecer o padrão seguro.

### Impacto da revisão

Nenhum identificado — análise inicial. A proposta acrescenta capacidade além do cadastro, sem alterar arquivos anteriores.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| simplicity | prioritized | PUT evita regras de atualização parcial | Comparação B/C |
| delivery-speed | prioritized | Reutiliza textos e limites existentes | DTO e domínio atuais |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| correctness | Nenhuma mutação inválida ou parcial | Entidade válida e transação |
| security | Nenhum acesso entre proprietários | Sessão e filtros internos |
| reliability | Sem perda de referências sem política | Exclusão lógica proposta e investigação prévia |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| security | Acesso ou alteração de projeto alheio | Alta | Estudantes |
| correctness | Textos inconsistentes entre cadastro e edição | Média | Estudantes e clientes |
| reliability | Currículo perde projeto referenciado | Alta | Estudantes e leitores |
| delivery-speed | Endpoints visíveis, mas inexequíveis no main | Média | Equipe e usuário |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| simplicity | Cliente envia os três textos no PUT | user-value | Aceitável sem necessidade comprovada de edição parcial |
| reliability | Estado de exclusão, migration e filtros nos consumidores | delivery-speed | Aceitável após validar política de referências |
| security | Consultas e testes por proprietário | simplicity | Obrigatório para isolamento |

## Riscos e efeitos de segunda ordem

Exclusão lógica isolada não garante compatibilidade: consumidores podem deixar de encontrar projetos excluídos e alterar currículos antigos. Investigar consultas e snapshots antes da migration. PUT pode sobrescrever edição concorrente; avaliar controle de concorrência se houver fluxo simultâneo real. `maxLength` isolado pode descrever tamanho bruto enquanto o runtime mede após strip; o contrato deve explicar essa diferença e cobrir espaços/Unicode. Cookie seguro pode impedir sessão no HTTP local se a configuração não for deliberadamente ajustada. Schema visível não prova executor persistido funcional.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Consulta é detalhe | Aprovação do contrato por ID | Revisão do consumidor esperado | Usuário precisa listar projetos |
| Limites atuais atendem | Aceite de título 200 e descrição 2000 | Revisão de produto e testes 0, 1, N, N+1, espaços, Unicode e controles | Limites novos ou contagem por grafemas |
| Isolamento preservado | Ausente/alheio/excluído não retorna nem altera | Unitários com doubles; integração de sessão e dois usuários | Qualquer vazamento ou mutação indevida |
| Atualização é atômica | Falha não altera campos nem proprietário | Unitários e integração com rollback | Persistência parcial ou colisão de identidade |
| Exclusão preserva currículos | Mapa dos consumidores e política de snapshots | Leitura dirigida antes de implementar; integração posterior | Referências quebradas ou mudança histórica indesejada |
| Swagger executa o ciclo | Login, POST, GET, PUT, DELETE pelo main com banco | Integração Nix tests e ensaio manual no Swagger | Rotas ausentes, cookie não enviado ou 503 com banco válido |
| OpenAPI expressa limites | Corpo, UUIDs, respostas e min/max documentados | Inspeção do schema e testes do contrato | Documentação diverge do runtime |

## Handoffs e atividades posteriores

1. Confirmar detalhe por ID e limites propostos durante revisão desta especificação; mudança de entendimento exige revisão do artefato.
2. Antes da exclusão, examinar migrations, seleção/consulta de projetos em currículos e política de versões para fechar semântica e planejar migration Code First. Se não for possível decidir, manter essa parte pendente.
3. Implementar Domain/Application com testes unitários e doubles, adicionando operações estreitas sem dependências de ORM/HTTP no núcleo.
4. Implementar API, DTOs, OpenAPI, adapters transacionais, factory e main; completar composição do cadastro como dependência do ensaio.
5. Executar unitários no `nix develop .#backend`; executar integração de persistência, middleware e main no `nix develop .#tests`, seguindo a configuração documentada. Nenhum teste foi executado nesta atividade exclusivamente documental.

## Síntese

Modo initial; engenharia com implementação, domínio e segurança; objeto misto de demanda e arquivos backend. Propõe GET por ID, PUT e DELETE lógico, mantendo título 200 e descrição 2000, com composição persistida em main e uso autenticado no Swagger. Sem impacto de revisão. A principal incerteza é o efeito da exclusão nas referências de currículos; consulta por ID e valores dos limites também precisam de aceite da especificação.
