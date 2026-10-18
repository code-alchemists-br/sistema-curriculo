---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v004"
status: proposed
created_at: "2026-10-17T18:43:13-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261011-001011-associacao-curriculo-vaga-v001.md
  supersedes: prompts/backend/20261012-162550-associacao-curriculo-vaga-v003.md
  change_type: reassessment
  secondary_change_types: [enrichment]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: "code-alchemists-br/sistema-curriculo#130"
      relationship: primary
      representation: prose
      function: documentation
      format: GitHub issue
      analysis_scope: whole-file
      locator: "título e corpo consultados via gh issue view, conforme evidência registrada em v003"
      content_state: external
      revision: null
      availability: available
    - path: "Solicitação original da linhagem — análise das issues #130, #131 e #132"
      relationship: primary
      representation: prose
      function: documentation
      format: mensagem de usuário
      analysis_scope: whole-file
      locator: "reproduzida em Solicitação original"
      content_state: external
      revision: null
      availability: available
    - path: "Nova decisão de negócio fornecida para a revisão v004"
      relationship: primary
      representation: prose
      function: documentation
      format: mensagem de usuário
      analysis_scope: whole-file
      locator: "reproduzida em Informações complementares"
      content_state: external
      revision: null
      availability: available
    - path: prompts/backend/20261012-162550-associacao-curriculo-vaga-v003.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: whole-file
      locator: "decisões anteriores, evidências, arquivos prováveis, pendências e handoffs"
      content_state: working-tree
      revision: v003
      availability: available
    - path: prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md
      relationship: supporting
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "decisão de Domain implementada pela #131 e divisão de responsabilidades"
      content_state: working-tree
      revision: v002
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: selected-section
      locator: "arquitetura, ambiente, Code First, testes e documentação"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: primary
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "RF12 e regras de negócio relacionadas, conforme recorte da v003"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/matriz_testes.md
      relationship: primary
      representation: prose
      function: test
      format: Markdown
      analysis_scope: selected-section
      locator: "CT-RF12-01..09, CT-RF12-C01..C07"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/Arquitetura/ADR-001-arquitetura-do-sistema.md
      relationship: context
      representation: prose
      function: architecture
      format: Markdown
      analysis_scope: selected-section
      locator: "Clean Architecture, fronteiras de camada e persistência, conforme recorte da v003"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram
      function: data-model
      format: Markdown
      analysis_scope: selected-section
      locator: "modelo atual e relações relevantes, conforme recorte da v003"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/contrato-credenciais-sessao.md
      relationship: supporting
      representation: prose
      function: contract
      format: Markdown
      analysis_scope: selected-section
      locator: "identidade confiável, dependência de sessão e respostas de autenticação/autorização"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: domain-model
      format: Python
      analysis_scope: whole-file
      locator: "agregado, classificações e regra candidatura implica interesse, conforme análise v003"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: domain-model
      format: Python
      analysis_scope: selected-section
      locator: "CurriculoId, UsuarioId, VagaId e ClassificacaoAssociacao"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: application-contract
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioCurriculo e contratos de repositório atuais"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/cadastro_estudante.py
      relationship: supporting
      representation: source-code
      function: application-use-case
      format: Python
      analysis_scope: selected-section
      locator: "EmailJaCadastrado e verificação de duplicidade antes de salvar"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/selecao_itens_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: application-use-case
      format: Python
      analysis_scope: selected-section
      locator: "verificação de propriedade do currículo e delegação de regras ao Domain"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/cadastro_acesso.py
      relationship: supporting
      representation: source-code
      function: api-adapter
      format: Python
      analysis_scope: selected-section
      locator: "tradução de EmailJaCadastrado para HTTP 409 e RegraDeDominioViolada para HTTP 422"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/itens_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: api-adapter
      format: Python
      analysis_scope: selected-section
      locator: "tradução de ausência para HTTP 404 e violação de domínio para HTTP 422"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py
      relationship: supporting
      representation: source-code
      function: persistence-adapter
      format: Python
      analysis_scope: selected-section
      locator: "salvamento, flush e ausência de commit no adapter"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: supporting
      representation: source-code
      function: persistence-mapping
      format: Python
      analysis_scope: selected-section
      locator: "curriculo_itens com identidade composta"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261007_0003_criar_curriculo_itens.py
      relationship: supporting
      representation: source-code
      function: database-migration
      format: Python
      analysis_scope: selected-section
      locator: "constraint de chave primária composta para tabela associativa"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_application_cadastro_estudante.py
      relationship: supporting
      representation: test
      function: unit-test
      format: Python
      analysis_scope: selected-section
      locator: "teste unitário de rejeição da duplicidade antes de gerar ID/salvar"
      content_state: working-tree
      revision: null
      availability: available
---

# Análise de decisão — Criação manual de associação currículo-vaga (#130)

## Solicitação original

> Analise em conjunto as issues:
>
> #130 "Implementar criação de associação currículo-vaga"
> #131 "Implementar regra de candidatura implica interesse"
> #132 "Implementar atualização de classificações da associação"
>
> Objetivo principal desta análise:
>
> Definir o modelo mínimo e as regras necessárias para que essas três issues compartilhem uma implementação coerente, com foco em permitir que a primeira implementação seja a issue #131.
>
> Não implemente código nesta etapa.
>
> IMPORTANTE
>
> 1. Leia todos os AGENTS.md aplicáveis antes da análise.
> 2. Consulte o conteúdo atual das issues #130, #131 e #132 no GitHub, se possível usando `gh issue view`.
> 3. Leia somente os arquivos necessários.
> 4. Não faça revisão geral do repositório.
> 5. Não altere arquitetura existente.
> 6. Não implemente API, banco, migration ou adapter nesta etapa.
> 7. Não invente classificações, estados ou regras que não estejam sustentados pelos requisitos ou testes existentes.
> 8. Se alguma decisão realmente não puder ser tomada com a evidência disponível, registre-a como pendente.
>
> CONTEXTO
>
> As três issues tratam da mesma associação entre currículo e vaga:
>
> #130 cria a associação.
>
> #131 estabelece a regra "candidatura implica interesse".
>
> #132 atualiza as classificações da associação.
>
> A análise deve determinar como essas responsabilidades se relacionam e garantir que a #130 e a #132 reutilizem a mesma regra de domínio definida para a #131.
>
> Há indícios na documentação e na matriz de testes de que as classificações atualmente previstas são:
>
> interesse
> compatibilidade
> candidatura
>
> Não introduza classificações adicionais sem evidência.
>
> QUESTÕES QUE A ANÁLISE DEVE RESPONDER
>
> 1. Qual deve ser o modelo mínimo da associação currículo-vaga?
> 2. Quais dados ela precisa possuir para suportar #130, #131 e #132?
> 3. Como currículo e vaga devem ser identificados?
> 4. As classificações devem ser representadas como conjunto, enum, flags ou outra estrutura já compatível com os padrões do projeto?
> 5. Qual é exatamente a regra da #131?
> 6. Quando `candidatura` for adicionada, `interesse` deve ser adicionado automaticamente?
> 7. O que deve acontecer se alguém tentar remover `interesse` enquanto `candidatura` continua presente?
>
> Não invente a resposta. Determine-a a partir dos requisitos, matriz de testes e padrões existentes. Caso não haja evidência suficiente, registre a decisão como pendente.
>
> 8. Remover `candidatura` deve remover `interesse`?
>
> Verifique se existe evidência. Não infira automaticamente.
>
> 9. A regra "candidatura implica interesse" deve ficar no Domain?
> 10. A #131 pode ser implementada antes da persistência da #130?
> 11. Qual parte mínima do modelo precisa existir para implementar #131 isoladamente?
> 12. Quais responsabilidades pertencem à:
>
> Domain
> Application
> Infrastructure
> API
>
> 13. O que a #130 deve reutilizar da #131?
> 14. O que a #132 deve reutilizar da #130 e da #131?
> 15. Quais decisões precisam ser tomadas agora e quais podem esperar a implementação de persistência?
> 16. Quais testes unitários são pertinentes especificamente para #131?
> 17. Quais testes pertencem depois à #130 ou #132 e não devem entrar na implementação da #131?
>
> ARQUIVOS PRIORITÁRIOS
>
> Leia somente quando necessário:
>
> AGENTS.md
>
> src/backend/AGENTS.md
>
> docs/Arquitetura/ADR-001-arquitetura-do-sistema.md
>
> docs/requisitos_funcionais.md
>
> docs/matriz_testes.md
>
> docs/modelagem_der.md
>
> src/backend/domain/
>
> src/backend/domain/curriculo.py
>
> src/backend/domain/value_objects.py
>
> src/backend/application/ports.py
>
> exemplos existentes de entidades e invariantes de domínio
>
> qualquer análise em prompts/ diretamente relacionada a currículo-vaga ou às issues #130, #131 e #132
>
> Procure por `RegraDeDominioViolada` e por padrões existentes de validação de invariantes somente se forem relevantes.
>
> ESCOPO DA PRIMEIRA IMPLEMENTAÇÃO
>
> Embora a análise cubra #130, #131 e #132, a primeira implementação será somente a #131.
>
> Portanto, ao final, indique explicitamente:
>
> 1. quais arquivos a #131 provavelmente precisará criar ou alterar;
> 2. qual comportamento exato deve ser implementado;
> 3. quais testes unitários devem acompanhar a #131;
> 4. o que deve permanecer fora dessa implementação para #130 e #132.
>
> RESULTADO ESPERADO
>
> Quero uma decisão técnica pequena e implementável que permita executar #131 primeiro sem criar um modelo incompatível com #130 e #132.
>
> Não implemente código.
>
> Gere o artefato de análise no diretório apropriado de `prompts/`, seguindo as regras da skill e mantendo a rastreabilidade exigida pelo projeto.

## Informações complementares

As solicitações intermediárias e evidências registradas em v003 permanecem parte desta linhagem e estão preservadas literalmente em [v003](./20261012-162550-associacao-curriculo-vaga-v003.md), seção “Informações complementares”. A solicitação abaixo é a nova entrada desta revisão.

### Entrada posterior — decisão de negócio (literal)

> Revise:
>
> prompts/backend/20261012-162550-associacao-curriculo-vaga-v003.md
>
> Nova decisão de negócio para a issue #130:
>
> - um mesmo currículo só pode ser associado uma vez à mesma vaga;
> - o par `curriculo_id + vaga_id` representa uma associação única;
> - se uma tentativa de criação ocorrer para um par que já possui associação, a nova criação deve ser rejeitada;
> - a criação duplicada não deve atualizar classificações;
> - alterações posteriores nas classificações pertencem exclusivamente à #132.
>
> Com base nessa decisão:
>
> 1. revise a política de duplicidade;
> 2. determine a estratégia de persistência mais coerente com os padrões existentes do projeto;
> 3. decida entre:
>    - chave composta;
>    - ID técnico próprio + UNIQUE(curriculo_id, vaga_id);
> 4. defina em qual camada a duplicidade deve ser detectada/tratada;
> 5. defina a proteção contra condição de corrida no banco;
> 6. determine o erro de Application adequado;
> 7. determine a tradução HTTP adequada seguindo os padrões já existentes do projeto;
> 8. mantenha a autenticação como dependência de implementação já especificada pelo contrato, sem transformar isso novamente em dúvida de regra;
> 9. não implemente funcionalidades da #132;
> 10. não implemente código nesta etapa.
>
> Preserve a linhagem da análise e gere uma nova versão v004.
>
> O objetivo é sair de `pending` para uma decisão implementável da #130, salvo se surgir algum bloqueio técnico novo e concreto.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Política de repetição | Pendente por falta de evidência | Repetição do mesmo par é rejeitada; não há atualização | Decisão de negócio explícita do usuário | Fecha semântica pública da criação |
| Identidade persistida | Chave e ID próprio pendentes | Chave primária composta `(curriculo_id, vaga_id)`; sem ID técnico próprio | O par foi definido como identidade única e não há necessidade demonstrada de terceiro identificador | Constraint representa diretamente a regra |
| Detecção duplicada | Pendente | Pré-checagem Application e constraint única; o adapter traduz conflito de corrida para o mesmo erro Application | Combina erro claro no fluxo comum com garantia atômica do banco | Fecha risco de concorrência sem confiar só em consulta |
| Erro e transporte | Pendente | `AssociacaoCurriculoVagaJaExiste` e HTTP `409 Conflict` | Padrão próximo de `EmailJaCadastrado`/409 para recurso já existente | Contrato de erro definido |
| Autenticação | Dependência concreta precisava ser confirmada | Regra de sessão é fixa pelo contrato; integração da dependência comum é handoff de implementação | Pedido explícito para não reabrir regra já especificada | Não bloqueia a decisão da #130 |
| Status | `pending` | `proposed` | Não resta bloqueio de evidência para a decisão analisada | A implementação pode iniciar após aprovação |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `code-alchemists-br/sistema-curriculo#130` | primário | prosa | documentação da demanda | issue GitHub | título/corpo consultados conforme v003 | externo; disponível |
| Solicitação original acima | primário | prosa | requisito | mensagem | conteúdo integral reproduzido | externo; disponível |
| Nova decisão acima | primário | prosa | decisão de negócio | mensagem | conteúdo integral reproduzido | externo; disponível |
| `prompts/backend/20261012-162550-associacao-curriculo-vaga-v003.md` | apoio | prosa | decisão anterior e proveniência | Markdown | conteúdo integral, com foco em decisão, pendências e evidências | working tree; v003 |
| `prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md` | apoio | prosa | decisão de Domain da #131 | Markdown | domínio implementado e separação de responsabilidade | working tree; v002 |
| `AGENTS.md`; `src/backend/AGENTS.md` | contexto | prosa | instruções de arquitetura e trabalho | Markdown | instruções relevantes e arquivo local | working tree |
| `docs/requisitos_funcionais.md`; `docs/matriz_testes.md` | primários | prosa/teste | requisitos RF12 e critérios | Markdown | RF12 e CT-RF12 pertinentes | working tree |
| `docs/Arquitetura/ADR-001-arquitetura-do-sistema.md`; `docs/modelagem_der.md` | apoio | arquitetura/modelo | fronteiras e persistência | Markdown | recortes registrados em v003 | working tree |
| `docs/contrato-credenciais-sessao.md` | apoio | contrato | principal autenticado e identidade de rota | Markdown | dependência comum, principal e respostas de segurança | working tree |
| `src/backend/domain/associacao_curriculo_vaga.py`; `src/backend/domain/value_objects.py` | apoio | código | agregado e tipos | Python | implementação da #131 e identificadores | working tree |
| `src/backend/application/ports.py` | apoio | código | contratos de persistência | Python | `RepositorioCurriculo` e repositórios existentes | working tree |
| `src/backend/application/cadastro_estudante.py` | apoio | código | padrão de erro/duplicidade | Python | `EmailJaCadastrado` e verificação antes de salvar | working tree |
| `src/backend/application/selecao_itens_versao_curriculo.py` | apoio | código | padrão de propriedade | Python | busca de currículo e comparação de proprietário | working tree |
| `src/backend/api/cadastro_acesso.py` | apoio | código | tradução HTTP | Python | 409 para e-mail repetido, 422 para regra de domínio | working tree |
| `src/backend/api/itens_versao_curriculo.py` | apoio | código | tradução HTTP | Python | 404 para ausência e 422 para regra de domínio | working tree |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_curriculo.py` | apoio | código | persistência e transação | Python | flush e responsabilidade externa por commit/rollback | working tree |
| `src/backend/infrastructure/persistence/sqlalchemy/curriculo.py`; `src/backend/infrastructure/persistence/alembic/versions/20261007_0003_criar_curriculo_itens.py` | apoio | código | padrão de chave associativa | Python | chave composta de `curriculo_itens` | working tree |
| `src/backend/tests/test_application_cadastro_estudante.py` | apoio | teste | padrão de teste unitário | Python | teste de rejeição sem salvar | working tree |

### Limites da evidência dos artefatos

- A v003 consultou a issue #130 e os requisitos/matriz; a demanda não continha política de repetição. A regra nova é decisão de negócio fornecida diretamente pelo usuário, não inferência documental.
- A migration de `curriculo_itens` demonstra que chave composta é usada em uma relação associativa, mas não obriga todas as tabelas a adotá-la. A escolha da v004 decorre também da identidade lógica agora declarada.
- O endpoint de cadastro já converte duplicidade para 409; seleção repetida de item de currículo, por ser violação de regra do agregado, usa 422. A decisão da associação é um conflito com uma associação persistida, portanto aproxima-se do primeiro caso.
- O adapter existente não traduz violações de constraint em erro de Application: não havia esse caso de uso. A v004 define essa tradução somente para a constraint nomeada da associação, sem propor tratamento genérico de `IntegrityError`.
- O contrato da sessão define a origem da identidade; a composição concreta dessa dependência deve ser integrada pela implementação. Isso não é pendência sobre a regra de ownership.

## Problema enriquecido

### Resultado desejado

Completar a #130 como fatia vertical de criação manual e persistência de uma associação currículo-vaga válida, pertencente ao estudante autenticado e identificada unicamente por `(curriculo_id, vaga_id)`. Repetir a criação do mesmo par deve ser rejeitado, sem modificar classificações existentes.

### Atores e interesses

- Estudante autenticado: cria a associação para currículo próprio, com ao menos uma classificação inicial.
- Application: valida ownership e política de duplicidade, cria o agregado e solicita persistência.
- Infrastructure: preserva unicidade sob concorrência e persiste atomicamente associação e classificações.
- API: obtém identidade da dependência comum de sessão, valida transporte e comunica conflito como HTTP 409.

### Evidências e fatos observados

1. A decisão do usuário estabelece unicidade/rejeição para o par e proíbe que a criação repetida atualize classificações.
2. A #131 já entregou `AssociacaoCurriculoVaga`, `ClassificacaoAssociacao` e `VagaId`; o Domain exige ao menos uma classificação, elimina duplicatas e aplica `candidatura => interesse`.
3. O caso `CadastrarEstudante` consulta `existe_por_email` e lança `EmailJaCadastrado` antes de salvar; a API traduz essa exceção para 409.
4. Seleção de item de currículo consulta `RepositorioCurriculo`, oculta ausência e propriedade alheia como `CurriculoNaoEncontrado`, deixa o agregado validar e persiste pelo repository.
5. `RepositorioCurriculo` não persiste associações. A Application necessita de port próprio para essa responsabilidade, com consulta de par existente e salvamento.
6. A tabela `curriculo_itens` usa chave primária composta, evidenciando precedente interno para identidade de relação sem ID técnico.
7. O adapter existente aguarda `flush`, não faz `commit`; o limite de transação externo controla commit/rollback.
8. Contrato de sessão: rota protegida obtém `UsuarioAutenticado` pela dependência comum e nunca aceita a identidade do proprietário declarada pelo cliente. Ownership ausente/alheio pode ser ocultado com 404.
9. RF12 e CT-RF12 exigem criação/persistência e ausência de gravação parcial; não exigem uma consulta à vaga no Grupo 2.

### Hipóteses

- **H1.** A persistência relacional representa a associação numa linha própria cuja PK é o par, e as classificações em registros dependentes desse par. Ambas as partes compartilham uma transação. O formato concreto das colunas de classificação segue o mapping relacional existente; não se acrescentam campos de negócio.
- **H2.** A consulta preventiva `existe_por_par` é útil para rejeição comum com erro de Application; a constraint única, não essa consulta, é a garantia de concorrência.
- **H3.** O erro específico de unicidade é definido pela Application e reconhecido pelo adapter para a constraint correspondente, mantendo HTTP e banco fora da regra do caso de uso.
- **H4.** O principal da sessão é adaptado para `UsuarioId` na API e então incluído na entrada da Application; não há `usuario_id` enviado pelo cliente.

### Perguntas em aberto

Nenhum bloqueio de decisão da #130 identificado. A implementação ainda deve confirmar o ponto existente de composição da dependência de sessão e o limite transacional externo, sem alterar as regras decididas neste documento.

### Escopo

- Caso de uso `CriarAssociacaoCurriculoVaga`.
- Entrada mínima: `UsuarioId` proveniente do principal confiável, `CurriculoId`, `VagaId` e classificações iniciais.
- Verificação de currículo e ownership por `RepositorioCurriculo`.
- Rejeição de duplicata por par, criação do agregado já existente e salvamento por novo port específico.
- API protegida por sessão, com erro de duplicidade 409.
- ORM, migration/constraint, adapter, composição transacional e documentação de modelo necessários para persistência completa.

### Fora do escopo

- Consultar Grupo 2 ou revalidar existência de vaga; nenhum requisito analisado exige essa chamada.
- Gerar UUID/ID técnico para associação ou adicionar campos sem evidência.
- Atualizar, adicionar ou remover classificações depois da criação.
- Tratar tentativa duplicada como idempotente, como upsert, ou como edição.
- Alterar o agregado #131 ou repetir sua normalização em Application/API.

### Critérios de sucesso

1. Entrada válida de currículo próprio não associado cria uma única associação persistida.
2. Classificações gravadas são exatamente as do agregado após a normalização da #131.
3. Classificação inicial vazia ou inválida falha antes de qualquer persistência.
4. Currículo inexistente/alheio falha sem expor ownership e sem gravar.
5. Par existente gera `AssociacaoCurriculoVagaJaExiste` e HTTP 409; classificações não são alteradas.
6. Duas criações concorrentes do mesmo par não produzem duas associações nem classificações divergentes; a constraint decide o vencedor.
7. Falha durante gravação reverte a associação e suas classificações conjuntamente.

## Restrições aplicáveis

- Preservar as fronteiras DDD/Clean Architecture: Application coordena, Domain valida o agregado e Infrastructure implementa os ports.
- Reusar integralmente o agregado da #131.
- Identidade única imposta no banco, não somente por consulta de aplicação.
- Não fazer commit parcial: association row e registros de classificações pertencem a uma unidade transacional.
- A API não aceita identidade do estudante em campo controlado pelo cliente.
- Não antecipar operações da #132.
- A demanda deve resultar em persistência Code First/migration; não foi encontrada issue que separe a implementação concreta.

## Classificação comentada

- **Esfera primária:** engineering.
- **Preocupações:** domain, architecture, data.
- **Tipo de decisão:** design de caso de uso, port, identidade persistida e tradução de conflito.
- **Escopo:** componente vertical do backend.
- **Ciclo:** delivery.
- **Urgência:** normal.
- **Incerteza:** baixa para decisões de negócio; detalhes ordinários de composição ficam para a implementação.
- **Reversibilidade:** moderada; mudança futura de PK exigiria migration e atualização de referências.
- **Risco:** médio, principalmente concorrência, ownership e atomicidade.

## Decisão de roteamento

Salvar em `prompts/backend`, continuando a linhagem do artefato anterior de backend sobre o mesmo agregado e a issue #130. Foram consideradas `prompts/backend`, `prompts/requisitos` e `prompts/revisao`; as duas últimas não são o objeto principal. Confiança alta. O inventário de diretórios e o README de `prompts/` confirmam a categoria de backend como local semântico adequado.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | Alta | Um par gera no máximo uma associação; candidato sempre implica interesse | Regra funcional e integridade do estado persistido |
| reliability | Alta | Nenhum estado parcial; constraint arbitra concorrência | Duas escritas e requisições concorrentes |
| security | Alta | Principal confiável e ownership validado antes de persistir | Dados de currículo são privados |
| simplicity | Alta | Identidade física coincide com identidade lógica; não criar id sem uso demonstrado | Reduz esquema e referências desnecessários |
| modifiability | Média | #132 pode localizar a associação pelo par e persistir classificações relacionadas | Próxima operação modificará estado sem mudar identidade |
| delivery-speed | Média | Reusar padrões e não integrar Grupo 2 | Evita dependência externa sem requisito |

## Alternativas consideradas

### Alternativa A — Chave primária composta pelo par (selecionada)

`(curriculo_id, vaga_id)` é a PK da associação e, por consequência, a constraint de unicidade. Corresponde diretamente à identidade declarada, não exige gerador/coluna de ID e permite localizar a associação em #132 com os IDs já conhecidos. Há precedente em `curriculo_itens`. O custo é carregar as duas colunas em eventuais referências dependentes, o que é coerente com a identidade relacional.

### Alternativa B — ID técnico próprio mais UNIQUE no par

Um UUID serviria de PK, com constraint adicional `UNIQUE(curriculo_id, vaga_id)`. Também protege concorrência e é válida tecnicamente, mas não há consumidor, contrato, requisito ou padrão da relação que necessite do UUID. Adiciona geração, coluna, índice e opção de identidade duplicada sem benefício demonstrado. Não selecionada por simplicidade e aderência à identidade informada.

### Alternativa C — Unicidade verificada somente em Application

Consultar antes de inserir, sem constraint no banco. Inviável: duas transações podem consultar simultaneamente “não existe” e inserir ambas. A consulta é conveniência para resposta previsível, não garantia de integridade.

### Alternativa D — Upsert/idempotência ou atualização da associação existente

Inviável diante da decisão explícita: duplicata deve ser rejeitada e não deve alterar classificações. Um upsert mudaria o comportamento de negócio e anteciparia #132.

## Perfil de pagamento comparativo

Escala ordinal: `+2` melhora fortemente; `+1` melhora moderadamente; `0` neutro; `-1` piora moderadamente; `-2` piora fortemente. Os valores não são somados.

| Dimensão | Prioridade | A: par composto | B: ID + UNIQUE | C: só Application | Confiança | Base |
|---|---:|---:|---:|---|---|
| correctness | Alta | +2 | +2 | -2 | Alta | Regra explícita e necessidade de constraint |
| reliability | Alta | +2 | +2 | -2 | Alta | Ambos garantem unicidade no banco; consulta não |
| simplicity | Alta | +2 | 0 | +1 | Alta | O par já é identidade e nenhum requisito pede ID |
| modifiability | Média | +1 | 0 | -1 | Média | #132 já recebe ambos os IDs; B cria identidade alternativa |
| security | Alta | 0 | 0 | 0 | Alta | Todas dependem da mesma checagem de ownership/sessão |
| delivery-speed | Média | +2 | 0 | +1 | Média | Composto evita coluna/gerador sem reduzir a proteção |

## Histórico e decisão atual

### Decisão da versão anterior

A v003 concluiu que a #130 deve ser uma fatia vertical, recomendou caso de uso na Application, reuso do Domain da #131, verificação de ownership, port específico e persistência/migration transacional. Deixou `pending` a política de duplicidade, a identidade física e o erro/HTTP.

### Decisão recomendada nesta versão

1. A Application expõe o caso de uso `CriarAssociacaoCurriculoVaga`. Sua entrada contém:
   - `usuario_id: UsuarioId`, derivado do `UsuarioAutenticado`;
   - `curriculo_id: CurriculoId`;
   - `vaga_id: VagaId`;
   - coleção de `ClassificacaoAssociacao` iniciais.
   Não recebe ID de associação, nome de vaga, timestamp, usuário declarado pelo cliente ou outros campos sem requisito.
2. O handler exige a dependência comum de sessão prevista em `docs/contrato-credenciais-sessao.md`. O cliente não controla o `usuario_id`; o handler converte `usuario.usuario_id` para a entrada de Application. Falha de autenticação ocorre antes do caso de uso. A rota segue a política de ocultação de ownership do contrato e do caso de uso existente.
3. A Application consulta `RepositorioCurriculo.obter_por_id`. Currículo ausente ou pertencente a outro usuário gera `CurriculoNaoEncontrado`, conforme padrão atual, sem revelar qual condição ocorreu.
4. Antes de construir/gravar, a Application chama `RepositorioAssociacaoCurriculoVaga.existe_por_par(curriculo_id, vaga_id)`. Se verdadeiro, lança `AssociacaoCurriculoVagaJaExiste`, definida na Application e sem detalhes HTTP/SQL. Nenhuma chamada de atualização ocorre.
5. Se não duplicado, a Application constrói diretamente `AssociacaoCurriculoVaga(curriculo_id, vaga_id, classificacoes)`. O agregado #131 é a autoridade para lista não vazia, classificação válida, ausência de duplicatas e normalização `candidatura => interesse`. Não há factory existente necessária nem validação paralela na Application.
6. A Application chama uma vez `RepositorioAssociacaoCurriculoVaga.salvar(associacao)`. Esse port é novo: `RepositorioCurriculo` não deve aceitar agregado de outro tipo.
7. A persistência usa PK composta `(curriculo_id, vaga_id)`. Uma tentativa que encontre a associação existente no passo 4 é rejeitada; a persistência não executa upsert. O adapter faz flush sem commit, dentro do limite transacional externo já usado pelo backend.
8. Se duas requisições passarem ao mesmo tempo pela pré-checagem, a PK composta impede a segunda inserção. O adapter reconhece exclusivamente a violação dessa constraint e a converte para `AssociacaoCurriculoVagaJaExiste`; falhas de banco não relacionadas continuam explícitas. O boundary externo faz rollback da transação em erro.
9. A API traduz `AssociacaoCurriculoVagaJaExiste` para `409 Conflict`, como `EmailJaCadastrado`. O HTTP 422 continua reservado a entrada inválida/violação de domínio, como classificação vazia/inválida. Ownership oculto segue 404 conforme o padrão existente.
10. Association e classificações iniciais são persistidas dentro da mesma transação. O estado gravado vem do agregado já normalizado; falha em qualquer escrita causa rollback integral. O adapter não faz commit.
11. Não consultar a vaga no Grupo 2: a vaga é uma referência recebida pelo fluxo manual e não foi encontrado requisito de revalidação externa.

### Respostas diretas às questões da análise

| Questão | Decisão |
|---|---|
| Responsabilidade da #130 | Criar e persistir uma associação válida, uma única vez por par, pertencente ao estudante autenticado |
| Camada principal | Application coordena a fatia vertical; API e Infrastructure completam transporte e persistência |
| Caso de uso | `CriarAssociacaoCurriculoVaga` com entrada explícita |
| Entrada mínima | principal autenticado adaptado para `UsuarioId`, `CurriculoId`, `VagaId` e classificações iniciais |
| Lista de classificações vazia | Domain já exige pelo menos uma; é autoritativo. API pode validar estrutura/vazio cedo, sem duplicar a regra como fonte de verdade |
| Reuso da #131 | Construir o mesmo agregado; nenhuma cópia da regra de candidatura/interesse |
| Factory | Construção direta; não foi identificada fábrica existente que deva ser usada |
| Ownership | Consultar currículo pelo port existente e comparar com principal autenticado; ocultar ausente/alheio como 404 |
| Existência da vaga | Não validar via Grupo 2 sem requisito explícito |
| Persistência | Novo port `RepositorioAssociacaoCurriculoVaga`; não reutilizar `RepositorioCurriculo` para salvar |
| Política de duplicidade | Rejeitar; não atualizar classificações e não tratar como idempotência |
| Identidade | PK composta `(curriculo_id, vaga_id)`; nenhum ID técnico próprio |
| Concorrência | PK composta/constraint única é fonte final de integridade; checagem Application não substitui |
| Erro de Application | `AssociacaoCurriculoVagaJaExiste`; mesmo erro para duplicidade vista na checagem e conflito reconhecido pelo adapter |
| HTTP | 409 para duplicidade; 422 para entrada/invariante inválida; 404 para currículo ausente/alheio |
| Migration/ORM | Necessários para concluir a criação persistente da #130; não há separação documentada em issue posterior |
| Atomicidade | Um limite transacional para associação e classificações; rollback completo; adapter sem commit |
| Pendências materiais | Nenhuma. Integração da dependência de sessão e boundary transacional são handoffs de implementação, não dúvidas de regra |

### Responsabilidades por camada

| Camada | Responsabilidade na #130 | Não deve |
|---|---|---|
| Domain | Manter `AssociacaoCurriculoVaga` e suas invariantes da #131 | Consultar persistência, usuário, API ou vaga externa; atualizar/remover classificações |
| Application | Verificar ownership e duplicidade, criar agregado existente, chamar port e expor erro sem HTTP/SQL | Replicar normalização; acessar ORM; fazer upsert |
| Infrastructure | Implementar port, mapping/ORM, migration, PK composta e traduzir somente a constraint esperada | Commit próprio; engolir erros; alterar classificação |
| API | Autenticar pela dependência comum, derivar ator, validar formato, invocar Application, produzir DTO/erros | Receber identidade do cliente; mapear erro para sucesso; normalizar classes |

### Arquivos prováveis para a #130

**Criar:**

- `src/backend/application/associacao_curriculo_vaga.py` — entrada, erro `AssociacaoCurriculoVagaJaExiste` e caso de uso.
- `src/backend/api/associacao_curriculo_vaga.py` — DTO e endpoint autenticado; tradução de duplicidade para 409.
- `src/backend/infrastructure/persistence/sqlalchemy/associacao_curriculo_vaga.py` — registros/mapping usando o par como identidade e representação persistida das classificações.
- `src/backend/infrastructure/persistence/sqlalchemy/repositorio_associacao_curriculo_vaga.py` — implementação de consulta de duplicidade e salvamento; mapeamento específico da violação de unicidade.
- Nova migration Alembic — association com PK `(curriculo_id, vaga_id)` e estrutura necessária às classificações.
- Testes unitários Application/API e testes de mapping/repository; teste de integração de persistência/transação.

**Alterar provavelmente:**

- `src/backend/application/ports.py` — port `RepositorioAssociacaoCurriculoVaga`, com `existe_por_par` e `salvar`.
- `src/backend/application/__init__.py` — exports, se o padrão público atual exigir.
- `src/backend/infrastructure/persistence/sqlalchemy/metadata.py` — registrar mapping para Alembic.
- `src/backend/api/factory.py` — compor executor, dependency de sessão e router.
- `docs/modelagem_der.md` — registrar associação e unicidade após mapping definido.

Não alterar o Domain #131 para duplicar validação ou introduzir remoções. Nomes finais de tabela/coluna e forma física de representar a classificação devem seguir o mapping atual, mantendo a PK e a regra de unicidade decididas aqui.

### Testes específicos da #130

**Unitários de Application:**

- currículo próprio, par ainda inexistente: constrói o agregado existente e chama `salvar` uma vez;
- entrada com `candidatura`: o agregado enviado ao port contém `interesse` automaticamente, sem normalização na Application;
- par já existente: lança `AssociacaoCurriculoVagaJaExiste`, não cria/salva e não chama qualquer operação de atualização;
- currículo inexistente/alheio: mesmo erro de ocultação existente, sem consultar/gravar associação;
- lista vazia ou classificações inválidas: erro do agregado antes de chamar o port de salvamento;
- falha de repositório não vira sucesso nem é ocultada.

**Unitários de API:**

- principal autenticado fornece `usuario_id`; identidade enviada pelo cliente é ignorada/não aceita;
- sem sessão não executa o caso de uso e devolve 401 conforme contrato;
- duplicidade de Application resulta em 409;
- classificação inválida resulta em 422; currículo ausente/alheio segue 404;
- sucesso usa resposta pública/DTO, sem serializar agregado interno.

**Infrastructure e testes de persistência:**

- mapping/round-trip preserva currículo, vaga e classificações normalizadas;
- chave primária composta impede inserir duas linhas de associação para o mesmo par;
- duplicata detectada no flush por corrida é mapeada para o erro Application específico; violações não relacionadas continuam explícitas;
- uma falha ao persistir classificações reverte também a associação, e vice-versa, pela mesma transação;
- integração no banco/migration valida constraint real; teste transacional verifica ausência de estado parcial.

Testes unitários pertencem ao ambiente `backend`; persistência/integração de sistema usa o ambiente `tests` conforme a hierarquia de instruções do projeto.

### Impacto da revisão

A regra de repetição e a identidade, antes pendentes, agora decorrem de uma decisão explícita e são concretizadas em chave primária composta. A consulta preventiva e erro de Application seguem o padrão de duplicidade existente; a constraint do banco acrescenta a proteção necessária contra corrida. O precedente de HTTP 409 para duplicata de conta é mais próximo que 422 de violação de invariante do agregado. A dependência de autenticação deixa de ser questão de regra e permanece integração técnica mandatória pelo contrato. Status muda de `pending` para `proposed`.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | Priorizada | O par tem uma única identidade e criação repetida não altera classes | Decisão explícita de negócio |
| reliability | Priorizada | Constraint fecha a condição de corrida; transação elimina persistência parcial | Padrão Code First e CT-RF12-09 |
| simplicity | Priorizada | Não há UUID sem consumidor; identidade natural é chave persistida | Par explicitamente único; precedente de chave composta |
| security | Limiar alto | Só principal confiável cria associação de currículo próprio | Contrato de sessão e caso de uso existente |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| modifiability | #132 localiza a associação sem migrar a chave | Usa o mesmo par que identifica a relação |
| delivery-speed | Evitar chamadas externas e conceitos redundantes | Não consulta Grupo 2 nem cria ID técnico |
| observabilidade de erro | Duplicidade deve ser distinguível de entrada inválida | Exceção Application específica e HTTP 409 |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | Sem constraint, corrida pode duplicar associação; upsert pode sobrescrever classes | Alta | Estudante e integridade dos dados |
| reliability | Escritas fora de transação podem deixar associação sem classes ou estado incompleto | Alta | Estudante, suporte e operação |
| security | Aceitar usuário do request permite associar currículo alheio | Alta | Estudantes |
| simplicity | ID surrogate sem necessidade amplia modelo sem resolver requisito adicional | Baixa | Manutenção |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness/reliability | Pré-consulta e tratamento nominal de constraint além da PK | Simplicity | Aceitável; protege resposta comum e concorrência |
| simplicity | PK composta deve acompanhar referências futuras da associação | Conveniência de usar um único ID | Aceitável; o contrato conhece o par |
| security | A rota depende da composição da autenticação compartilhada | Delivery-speed | Necessário pelo contrato de sessão |
| reliability | Boundary transacional deve abranger association e classificações | Simplicity | Aceitável; já é necessário para CT-RF12-09 |

## Riscos e efeitos de segunda ordem

- Constraint nomeada incorretamente ou mapeamento genérico de todo `IntegrityError` pode transformar falhas distintas em duplicidade. Adapter deve identificar exclusivamente a constraint correspondente; outros erros propagam.
- Depois de `flush` com violação, a sessão/transação fica em erro até rollback. O boundary externo deve sempre executar rollback antes de reutilizar a sessão; não mascarar a falha como se a sessão estivesse íntegra.
- Pré-checagem e insert não são atômicos entre si; só a constraint DB dá garantia. A aplicação deve tratar conflito detectado no flush como o mesmo erro público e garantir rollback.
- A chave composta exige que operações futuras da #132 recebam o par completo. Isso é compatível com a identidade aprovada e não cria dependência de ID omitido.
- Um currículo inexistente pode falhar na leitura/ownership antes da constraint; a resposta segue o tratamento atual e não revela dados privados.
- Ausência de consulta ao Grupo 2 aceita referência potencialmente obsoleta porque nenhum requisito analisado exige revalidação. Revisar se requisito futuro tornar existência de vaga um invariante local.
- A dependência comum de sessão deve ser integrada antes de expor a rota. Não é permitido substituir essa dependência por `usuario_id` de rota/corpo.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Par é identidade única | Decisão de negócio aprovada e schema | Teste de constraint no banco com mesmo par e classificações diferentes | Qualquer requisito autorizado passar a permitir múltiplas associações do par |
| Pré-checagem rejeita sem alteração | Caso de uso e spy de repository | Unitário verifica erro e ausência de `salvar`/`atualizar` | Consulta retornar existente e ainda haver mutação |
| Constraint protege concorrência | Migration e engine relacional de teste | Repository/integration executa inserção concorrente ou segunda inserção e verifica uma associação | Duas linhas aceitas ou conflito escapar sem política definida |
| Conflito de corrida vira erro público correto | Adapter e API | Integration provoca a constraint; unitário API confirma 409 | Erro bruto vazado ou traduzido como 422/5xx indevido |
| Criação é atômica | Boundary transacional e dados persistidos | Falhar escrita de classificação e confirmar rollback de ambas as partes | Qualquer linha da operação permanece após rollback |
| Domain da #131 é reutilizado | Agregado e teste Application | Entrada com candidatura e inspeção do agregado persistido | API/Application mantêm normalizador paralelo ou estado persistido diverge |
| Ownership é sessão-confiável | Contrato e composição de rota | Teste sem sessão, principal autenticado e tentativa de identidade de cliente | Caso de uso aceita principal ausente ou usa valor do cliente |

## Handoffs e atividades posteriores

### Implementação #130

1. Criar erro Application `AssociacaoCurriculoVagaJaExiste`, port próprio, consulta `existe_por_par` e método `salvar`.
2. Implementar o caso de uso com verificação de currículo/ownership, rejeição antes do salvamento e construção direta do agregado.
3. Integrar a dependência comum de sessão descrita no contrato; não expor rota protegida enquanto ausente.
4. Criar mapping/migration com PK composta `(curriculo_id, vaga_id)`, adapter de persistência e mapeamento nominal da violação dessa constraint.
5. Garantir rollback completo no transaction boundary externo; adapter não comita.
6. Traduzir duplicata para HTTP 409. Manter 422 para validação/invariantes Domain, e 404 para currículo oculto por ausência/ownership alheio conforme padrão.
7. Implementar os testes unitários e de persistência listados acima; atualizar DER conforme mapping.

### Explicitamente fora da #130 — #132

- Adicionar classificação após a criação.
- Remover classificação, inclusive `candidatura` ou `interesse`.
- Remover `candidatura` e decidir se isso afeta `interesse`.
- Remover `interesse` enquanto há candidatura.
- Remover a última classificação ou decidir comportamento de associação sem classificação.
- Atualizar as classificações em associação já existente.
- Fazer duplicata virar upsert/idempotência: ela deve ser rejeitada, sem alteração.
- Acrescentar métodos de mutação ao agregado para atender antecipadamente a #132.

### Fora desta decisão

Não implementar código, executar testes, consultar Grupo 2, criar política de vagas inexistentes ou alterar a regra de negócio aprovada. Qualquer mudança futura na unicidade do par exige nova decisão e migração, não ajuste silencioso.

## Síntese

A #130 deve criar uma associação manual por caso de uso Application, com identidade confiável obtida pela dependência comum de sessão, ownership validado pela leitura do currículo e agregado `AssociacaoCurriculoVaga` da #131 construído uma única vez. O par `(curriculo_id, vaga_id)` é a identidade natural e a chave primária composta persistida. A Application rejeita duplicata com `AssociacaoCurriculoVagaJaExiste`; o banco impõe a constraint para fechar condição de corrida e o adapter reconhece somente essa violação, traduzindo-a para o mesmo erro. A API responde 409, sem atualizar classificações. Association e classificações são persistidas atomicamente pelo limite transacional externo. Não há bloqueio material de decisão: a composição concreta da autenticação e do transaction boundary é um handoff de implementação. A #132 permanece responsável por alterações posteriores de classificação.
