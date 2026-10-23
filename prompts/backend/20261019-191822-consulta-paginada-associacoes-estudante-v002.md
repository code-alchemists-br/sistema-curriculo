---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v002"
status: proposed
created_at: "2026-10-19T19:18:22-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md
  supersedes: prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md
  change_type: scope-change
  secondary_change_types: [enrichment, reassessment]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: "Solicitação de implementação da issue #243 (2026-10-19)"
      relationship: primary
      representation: prose
      function: documentation
      format: mensagem de usuário
      analysis_scope: selected-section
      locator: "objetivo, decisões de implementação, cobertura de testes e restrições"
      content_state: external
      revision: null
      availability: available
    - path: "Resposta do usuário: Criar análise v002 para teste SQLite de integração (Recomendado)"
      relationship: primary
      representation: prose
      function: documentation
      format: resposta do usuário
      analysis_scope: whole-file
      locator: "escolha explícita de revisão para autorizar teste SQLite de integração"
      content_state: external
      revision: null
      availability: available
    - path: prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md
      relationship: primary
      representation: prose
      function: decision-record
      format: Markdown
      analysis_scope: whole-file
      locator: "solicitação, evidências, decisão, testes unitários, validação e handoffs"
      content_state: working-tree
      revision: v001
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: selected-section
      locator: "Clean Architecture, responsabilidades de camadas e níveis de teste"
      content_state: working-tree
      revision: null
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: Markdown
      analysis_scope: selected-section
      locator: "ambientes Nix backend/tests e execução unitária versus integrada"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/application/consulta_associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: "validação dos parâmetros e delegação ao port"
      content_state: working-tree
      revision: "alteração local não commitada"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: Python
      analysis_scope: selected-section
      locator: "RepositorioAssociacaoCurriculoVaga.listar_por_usuario"
      content_state: working-tree
      revision: "alteração local não commitada"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "join com currículo, filtro do proprietário, ordenação, paginação e conversão dos agregados"
      content_state: working-tree
      revision: "alteração local não commitada"
      availability: available
    - path: src/backend/tests/test_application_consulta_associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: "delegação, retorno vazio e validação de offset/limit"
      content_state: working-tree
      revision: "alteração local não commitada"
      availability: available
    - path: src/backend/tests/test_infrastructure_repositorio_associacao_curriculo_vaga.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "query compilada, filtro, ordenação, parâmetros de página e mapeamento sob AsyncSession simulada"
      content_state: working-tree
      revision: "alteração local não commitada"
      availability: available
    - path: src/backend/tests/test_persistencia_associacao_curriculo_vaga_integracao.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: "padrão existente de persistência SQLite real síncrona com metadata SQLAlchemy"
      content_state: working-tree
      revision: null
      availability: available
    - path: nix/tests.nix
      relationship: supporting
      representation: configuration
      function: build
      format: Nix
      analysis_scope: whole-file
      locator: "composição do ambiente dedicado de testes"
      content_state: working-tree
      revision: null
      availability: available
    - path: nix/backend-python-packages.nix
      relationship: supporting
      representation: configuration
      function: build
      format: Nix
      analysis_scope: whole-file
      locator: "dependências Python compartilhadas pelo backend e pelo ambiente de testes"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/fixtures/curriculos_autenticados_integracao.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: selected-section
      locator: "uso de AsyncSession e SQLite aiosqlite com verificação opcional do driver"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/configuracao-ambiente.md
      relationship: context
      representation: prose
      function: documentation
      format: Markdown
      analysis_scope: selected-section
      locator: "ambientes Nix backend, tests e quality"
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories:
    - prompts/backend
    - prompts/requisitos
    - prompts/revisao
    - prompts/templates
    - prompts/ambientes
    - prompts/frontend
  confidence: high
  rationale: "Continuidade da linhagem #243 e foco em backend, adapter SQLAlchemy e testes de persistência; a alternativa requisitos trata necessidades, não a decisão de implementação e validação."
classification:
  sphere: engineering
  concerns: [integration, implementation, reliability]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: medium
---

# Análise de decisão — Consulta paginada das associações de um estudante (#243)

## Solicitação original

> Modelar consulta paginada das associações de um estudante.
>
> Objetivo: determinar a implementação mínima, verificável isoladamente e compatível com a arquitetura atual.
>
> Restrições da análise:
>
> - não implementar código;
> - não alterar arquivos existentes;
> - não fazer commits, push ou PR;
> - não ampliar o escopo para endpoints HTTP da #244;
> - não redesenhar a arquitetura;
> - evitar leituras fora da fatia vertical;
> - basear a decisão em contratos, casos de uso, modelos e testes existentes das associações currículo-vaga, incluindo as integrações das issues #130, #131 e #132.

## Informações complementares

### Entrada posterior do usuário — instruções de implementação e testes (literal)

> **Objetivo:** entregar a consulta paginada das associações currículo-vaga pertencentes a um estudante, com implementação mínima, testes e persistência funcional.
>
> Decisões de implementação:
>
> 1. Criar um caso de uso na Application para consultar as associações do estudante identificado por `usuario_id`.
> 2. Estender o port `RepositorioAssociacaoCurriculoVaga` com a operação mínima necessária de leitura paginada.
> 3. Utilizar paginação interna por `offset` e `limit`, validando entradas inválidas.
> 4. Garantir ordenação determinística pelo par `(curriculo_id, vaga_id)`.
> 5. Aplicar o filtro de propriedade antes de `offset` e `limit`, garantindo que nenhuma associação de outro usuário seja retornada.
> 6. Implementar o método correspondente no repositório SQLAlchemy, reaproveitando mappings e infraestrutura existentes.
> 7. Retornar dados do domínio, sem criar DTO ou endpoint HTTP.
> 8. Criar testes unitários e os testes de persistência pertinentes, incluindo isolamento entre usuários, ordenação, páginas subsequentes, resultado vazio e parâmetros inválidos.
>
> Restrições:
>
> - Não implemente a issue #244.
> - Não crie endpoints HTTP.
> - Não altere autenticação.
> - Não redesenhe a arquitetura.
> - Não introduza dependências desnecessárias.
> - Não crie migrations se o esquema existente for suficiente.
> - Não faça commit, push ou PR.
> - Não crie nova versão da análise sem necessidade técnica.
> - Execute testes e verificações de qualidade nos ambientes Nix exigidos.
>
> Se a skill de Application não autorizar alterações na Infrastructure, conclua sua etapa e faça o handoff para a skill apropriada. Ao terminar, informe objetivamente os arquivos alterados, os testes executados, o resultado das validações e eventuais bloqueios. Diferencie implementação concluída de integração pendente.

### Entrada posterior do usuário — autorização da revisão (literal)

> Criar análise v002 para teste SQLite de integração (Recomendado)

### Motivo da revisão

A v001 autorizava validação em testes unitários isolados, mas não decidia teste contra banco real. A cobertura unitária do adapter verifica a forma da query compilada; não executa o filtro, a ordenação e o recorte da página numa engine SQL. A instrução posterior exige cobertura de persistência e o usuário selecionou explicitamente uma revisão para tratar esse nível. Esta v002 mantém o escopo funcional da #243 e decide somente o teste de integração e o suporte de ambiente estritamente necessário.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Nível de evidência da consulta | Testes unitários isolados | Unitários e um teste de integração SQLAlchemy/SQLite | A query e a precedência de filtro/paginação precisam ser exercitadas contra uma engine real | Aumenta confiança funcional sem alterar o comportamento de produção |
| Driver assíncrono de SQLite | Não necessário à validação unitária | Necessário no ambiente `.#tests`; `aiosqlite` não está disponível atualmente | O repositório usa `AsyncSession` e o ambiente de testes não fornece o driver | Recomenda-se dependência exclusivamente de teste, sujeita à aprovação desta versão |
| Estado dos arquivos de produto | Contratos e implementação eram evidência existente | Caso de uso, port, query SQLAlchemy e testes unitários foram adicionados no working tree | A implementação da #243 ocorreu sob a v001 e esta solicitação posterior | Reavaliação baseada no código local; nenhuma alteração de produto é autorizada por esta revisão |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| Solicitação de implementação da issue #243 (2026-10-19) | primary | prose | documentação | Mensagem do usuário | Decisões 1–8, restrições e testes solicitados | external |
| Resposta do usuário sobre v002 | primary | prose | documentação | Resposta do usuário | Autorização para análise da alternativa SQLite | external |
| prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md | primary | prose | decision-record | Markdown | Conteúdo integral e decisão anterior | working-tree / v001 |
| src/backend/application/consulta_associacao_curriculo_vaga.py | supporting | source-code | production | Python | Entrada, validação e delegação | working-tree |
| src/backend/application/ports.py | supporting | source-code | application-contract | Python | Novo contrato de consulta paginada | working-tree |
| src/backend/infrastructure/persistence/sqlalchemy/repositorio_associacao_curriculo_vaga.py | supporting | source-code | production | Python | Consulta SQL e mapeamento de classificações | working-tree |
| src/backend/tests/test_application_consulta_associacao_curriculo_vaga.py | supporting | source-code | test | Python | Cenários unitários de parâmetros, delegação e página vazia | working-tree |
| src/backend/tests/test_infrastructure_repositorio_associacao_curriculo_vaga.py | supporting | source-code | test | Python | Testes unitários do adapter e inspeção da query compilada | working-tree |
| src/backend/tests/test_persistencia_associacao_curriculo_vaga_integracao.py | supporting | source-code | test | Python | Setup de SQLite síncrono, metadata, seed e cleanup existentes | working-tree |
| src/backend/tests/fixtures/curriculos_autenticados_integracao.py | supporting | source-code | test | Python | Padrão de engine assíncrona e detecção de `aiosqlite` | working-tree |
| nix/tests.nix | supporting | executable-script | build | Nix | Dependências instaladas pelo shell de testes | working-tree |
| nix/backend-python-packages.nix | supporting | executable-script | build | Nix | Pacotes compartilhados nos shells Python | working-tree |
| docs/configuracao-ambiente.md | context | prose | documentation | Markdown | Regras de seleção dos ambientes Nix | working-tree |
| AGENTS.md | context | prose | prompt-instruction | Markdown | Ambientes e política de testes | working-tree |
| src/backend/AGENTS.md | context | prose | prompt-instruction | Markdown | Limites arquiteturais e níveis de teste | working-tree |

### Limites da evidência dos artefatos

Os testes unitários existentes do adapter usam `AsyncSession` simulada e verificam a query compilada, não o resultado de um banco. O teste de persistência já existente usa SQLite real síncrono e valida mapeamentos/constraints, mas não chama a operação assíncrona nova. A fixture de integração existente documenta o uso de `sqlite+aiosqlite` e uma checagem explícita do driver; a verificação no ambiente `nix develop .#tests` retornou `None` para `aiosqlite`. Portanto, um teste funcional da operação async requer habilitar esse driver exclusivamente no ambiente de testes. Não foi examinada nem alterada qualquer rota HTTP ou código da #244.

## Problema enriquecido

### Resultado desejado

Completar a evidência da consulta paginada da #243 com um teste que execute o repositório SQLAlchemy contra SQLite real, provando isolamento por proprietário antes de `offset`/`limit`, ordenação por `(curriculo_id, vaga_id)`, páginas subsequentes e resultado vazio. Os parâmetros inválidos continuam comprovados no teste unitário da Application.

### Atores e interesses

- Estudante: não deve receber associações ligadas a currículos de outro usuário.
- Application e repositório: preservam o contrato interno de consulta sem introduzir transporte HTTP.
- Equipe: quer detectar regressões de predicado, ordenação e paginação sem depender de serviço externo.

### Evidências e fatos observados

1. A Application recebe `usuario_id`, `offset` e `limit`, valida offset inteiro não negativo e limite inteiro positivo, e delega pelo port.
2. O port novo especifica listagem pelo proprietário, filtro antes da paginação e retorno de agregados de domínio.
3. O adapter implementa join com `CurriculoRegistro`, predicado por `usuario_id`, ordem pelas duas partes da identidade e paginação SQL; carrega classificações somente para as associações da página.
4. Os testes unitários adicionados verificam valores inválidos, encaminhamento dos parâmetros, resultado vazio e estrutura da query SQL compilada com `AsyncSession` substituída.
5. O teste de persistência existente usa SQLite real, mas não exercita o adapter assíncrono.
6. O ambiente Nix `.#tests` não tem `aiosqlite` disponível no momento; a lista de pacotes Python compartilhada também não o declara.
7. Não há mudança de schema, migration ou resposta HTTP necessária para o teste proposto.

### Hipóteses

- `aiosqlite` pode ser disponibilizado somente em `.#tests`, sem entrar no ambiente de runtime/backend.
- O teste pode reutilizar a metadata e os registros ORM existentes, criar schema efêmero SQLite, sem executar migrations nem abrir conexão externa.
- Uma massa com associação alheia ordenada entre associações próprias consegue detectar aplicação indevida de `offset`/`limit` antes do filtro do proprietário.

### Perguntas em aberto

- A disponibilidade do atributo de pacote `aiosqlite` na versão de nixpkgs do flake deve ser confirmada ao implementar a dependência de teste.
- A resposta desta análise é `proposed`; a execução integrada somente fica autorizada após aprovação explícita desta versão.

### Escopo

- Acrescentar um teste de integração local do adapter assíncrono de associações com SQLite descartável.
- Acrescentar `aiosqlite` apenas ao ambiente Nix `.#tests`, se necessário e disponível.
- Verificar isolamento, ordem e páginas sucessivas em dados sintéticos; verificar página vazia.
- Manter a cobertura de entradas inválidas nos testes unitários da Application.

### Fora do escopo

- Alterar produção, regras, ports, caso de uso ou query já implementada.
- Endpoint, DTO, autenticação ou qualquer código da #244.
- Migrations, schema novo, banco externo, CI ou serviço compartilhado.
- Duplicar no teste integrado a validação unitária de parâmetros.
- Alterar dependências do ambiente `.#backend` ou de runtime.

### Critérios de sucesso

- Criar usuários distintos e currículos próprios correspondentes no banco SQLite efêmero.
- Persistir associações de ambos; posicionar por ordenação uma associação de outro usuário entre duas associações próprias.
- A primeira página e a página seguinte contêm somente associações próprias, ordenadas pelo par composto; a página subsequente não fica vazia por causa da linha alheia.
- Consulta de usuário sem associações retorna tupla vazia.
- O teste usa sessão e adapter reais com banco local temporário e cleanup garantido; não inicia API nem serviço externo.
- Os testes unitários existentes continuam cobrindo offset/limit inválidos.

## Restrições aplicáveis

- Acesso a desenvolvimento e teste somente nos ambientes Nix documentados.
- Testes integrados devem usar `nix develop .#tests`.
- Não introduzir dependência de runtime: eventual driver deve ser restrito a teste.
- Não alterar aplicação, adapter, autenticação, schema ou endpoint nesta revisão.
- A #244 e resultados HTTP permanecem excluídos.

## Classificação comentada

A esfera primária é engenharia. A mudança é uma revisão de escopo da validação: inclui integração de persistência real para demonstrar a semântica de filtro e paginação do adapter, sem alterar o comportamento funcional. As preocupações principais são integração, correção e implementação de teste.

## Decisão de roteamento

- Local selecionado: `prompts/backend`.
- Alternativas consideradas: `prompts/requisitos`, `prompts/revisao`, `prompts/templates`, além das demais pastas imediatas inventariadas (`ambientes`, `frontend`).
- Confiança: alta.
- Justificativa: a revisão pertence à linhagem backend da consulta currículo-vaga e decide teste contra o adapter SQLAlchemy; não é um requisito novo, template ou revisão genérica.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| correctness | alta | exercitar SQL real com associação alheia intercalada | comprova que filtro precede paginação, não apenas que a query contém um predicado |
| reliability | alta | páginas repetidas com ordem estável e resultado vazio | evita perdas ou duplicações entre páginas |
| simplicity | média | um teste integrado focado, reutilizando schema e sessão locais | mantém o custo do teste limitado |
| cost-efficiency | média | dependência somente em `.#tests` | não aumenta runtime nem ambiente de desenvolvimento |

## Alternativas consideradas

**A — Manter apenas testes unitários de Application e adapter.** É segura, rápida e já verifica validação e estrutura SQL, mas não executa o predicado e a paginação em um banco; portanto não demonstra o comportamento solicitado quando há linhas de terceiros antes do offset.

**B — Adicionar teste com AsyncSession e SQLite local descartável, habilitando `aiosqlite` somente em `.#tests`.** Testa o adapter real e o banco, isola o alvo e comprova a precedência do filtro, a ordenação e as páginas subsequentes. É a recomendação.

**C — Usar PostgreSQL compartilhado ou provisionar um serviço externo.** Não é adequado: adiciona ambiente/credenciais e operação externa sem benefício necessário para esta consulta nem autorização de alvo compartilhado.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| correctness | alta | -1 | +2 | +2 | alta | somente B/C executam a query contra banco; C exige alvo não autorizado |
| reliability | alta | 0 | +2 | +1 | média | SQLite local controla setup e cleanup sem dependência de serviço |
| simplicity | média | +2 | +1 | -2 | alta | A não demanda harness; B adiciona apenas driver de teste |
| cost-efficiency | média | +2 | +1 | -2 | alta | a dependência de B fica isolada em `.#tests` |

## Histórico e decisão atual

### Decisão da versão anterior

A v001 recomendava caso de uso e port na Application, filtro por proprietário, paginação simples e retorno de agregados. Para validação, apontava testes unitários isolados e deixava persistência como handoff; não autorizava teste contra banco real.

### Decisão recomendada nesta versão

Recomenda-se B: acrescentar um teste de integração de `RepositorioAssociacaoCurriculoVagaSqlAlchemy` com `AsyncSession` real e SQLite efêmero. Usar massa em que uma associação de outro usuário apareça na ordenação global entre associações próprias; buscar páginas consecutivas do usuário e confirmar que a linha alheia não consome posição. Validar a ordem pelo par composto e o caso sem associações. Preservar o teste unitário para entradas inválidas. Adicionar `aiosqlite` apenas ao shell `.#tests` se o pacote estiver disponível no nixpkgs do flake.

### Impacto da revisão

A revisão altera o nível de teste autorizado, não o contrato nem o comportamento de produção. O teste integrado e qualquer dependência de teste continuam pendentes até aprovação explícita desta versão proposta.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| correctness | prioritized | verificar o efeito real do filtro sobre a janela paginada | os testes unitários atuais inspecionam SQL compilado, não resultado SQL |
| reliability | prioritized | comprovar páginas estáveis e vazias | adapter usa ordenação e offset/limit SQL |
| simplicity | satisficed | manter um cenário SQLite local e pequeno | harness de persistência existente já usa metadata local |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| isolamento | nenhum registro de outro usuário no retorno | join e filtro por `CurriculoRegistro.usuario_id` exercitados contra SQLite |
| determinismo | par `(curriculo_id, vaga_id)` crescente | assert da ordem em páginas obtidas do banco |
| segurança do alvo | sem rede ou serviço compartilhado | engine e schema descartáveis locais |
| custo de dependência | nenhuma dependência de runtime | driver limitado a `.#tests` |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| correctness | predicado presente na query mas sem prova funcional da precedência perante paginação | média | estudantes e revisão da implementação |
| reliability | regressão de página subsequente ou ordem pode passar despercebida | média | consumidores da consulta e equipe |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| correctness | adicionar um teste com engine SQLite e seed local | simplicidade do setup | aceitável, limitada a um cenário |
| isolamento e reprodutibilidade | incluir `aiosqlite` apenas no shell de testes | manutenção da configuração de teste | aceitável se o pacote estiver disponível no flake |

## Riscos e efeitos de segunda ordem

- Dependência ausente bloqueia a execução até ser adicionada ao ambiente exclusivo de testes; não se deve contornar usando ferramenta global.
- Massa ordenada inadequadamente pode não detectar paginação antes do filtro; a associação alheia deve ocupar uma posição que altere o resultado da página subsequente se o predicado for removido.
- Reutilizar metadata sem migration valida o adapter e o mapping atual, não a execução das migrations; este último aspecto permanece fora desta decisão.
- O teste integrado não substitui a validação unitária de parâmetros inválidos nem deve duplicá-la.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| SQLite assíncrono é seguro e disponível no ambiente de teste | `aiosqlite` resolvido pelo Nix e engine local criada | executar teste em `nix develop .#tests` | indisponibilidade do pacote/driver ou dependência de serviço externo |
| filtro precede paginação | dados sintéticos com linha alheia intercalada | obter duas páginas pela implementação SQLAlchemy real | uma associação alheia aparece ou uma própria é omitida |
| ordem é determinística | resultados retornados em ordem pelo par composto | asserção de pares nas páginas | ordem depende de inserção ou varia |
| retorno vazio é estável | usuário sem associação | consulta integrada | exceção ou estrutura diferente de tupla vazia |
| parâmetros inválidos são cobertos uma vez | testes unitários da entrada da Application | suíte unitária no ambiente `.#backend` | regressão nos testes unitários existentes |

## Handoffs e atividades posteriores

- Aguardar aprovação desta v002 antes de alterar testes integrados ou `nix/tests.nix`.
- Após aprovação, adicionar somente a cobertura SQLite integrada e, se necessário, a dependência `aiosqlite` exclusivamente a `.#tests`; executar no ambiente `nix develop .#tests`.
- Application e adapter já foram alterados sob a solicitação de implementação e não são autorizados por esta revisão de análise de teste.
- Não alterar API, endpoint, DTO, autenticação, migration, CI ou serviço externo; #244 continua fora do escopo.

## Síntese

A v001 permitiu entregar e testar isoladamente o caso de uso e o adapter, mas a consulta real ainda não foi exercitada contra uma engine SQL. Como o usuário solicitou especificamente persistência funcional, isolamento e páginas subsequentes, recomenda-se acrescentar um teste SQLite assíncrono com massa que detecte paginação aplicada antes do filtro. O ambiente `.#tests` atualmente não dispõe de `aiosqlite`; a mudança recomendada é adicioná-lo somente ao ambiente de teste. Esta versão é `proposed`: o teste de integração e a dependência ainda não foram implementados e exigem aprovação explícita da v002.
