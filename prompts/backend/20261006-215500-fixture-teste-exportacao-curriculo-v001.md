---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-06T21:55:00-03:00"
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
    - path: docs/requisitos_funcionais.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF05 a RF09 e RF14 a RF15 (Construção, revisão e exportação de currículos)"
      content_state: commit
      revision: "5d5b185"
      availability: available
    - path: src/backend/domain/curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5d5b185"
      availability: available
    - path: src/backend/domain/itens_perfil.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5d5b185"
      availability: available
    - path: src/backend/domain/usuario.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5d5b185"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5d5b185"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "5d5b185"
      availability: available
    - path: README.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Equipe e Atribuições: Testes/Controle de qualidade e Gestão de versões/exportação"
      content_state: commit
      revision: "5d5b185"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A fixture instancia e consolida entidades e agregados do backend de forma determinística para os testes de geração e exportação de arquivos previstos no RF09."
classification:
  sphere: engineering
  concerns: [reliability, correctness, testability]
  decision_kind: design
  scope: subsystem
  lifecycle: development
  urgency: normal
  uncertainty: low
  reversibility: high
  risk: low
---

# Análise de decisão — Preparar fixture para teste de exportação de currículo

## Solicitação original

```text
Issue #154: Preparar fixture para teste de exportação de currículo
Crie um currículo estável para os futuros testes de geração e download de arquivos.
```

## Informações complementares

- Atribuição do membro Gustavo Minoru Haga (Testes/Controle de qualidade) conforme o `README.md`.
- Conforme o RF09 em `docs/requisitos_funcionais.md`, o sistema deve permitir exportar currículos nos formatos PDF e DOCX para compartilhamento com recrutadores.
- A responsabilidade de implementação dos geradores de PDF e DOCX cabe a Vinicius Regazio Farias, e a equipe de QA necessita de uma fixture estável, rica e determinística para validar layout, conteúdo, dados pessoais, formação, experiências, competências, idiomas e projetos.
- Todas as classes e funções devem conter docstrings completas (o que faz, como faz, qual finalidade atende), respeitando `AGENTS.md` e `src/backend/AGENTS.md`.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Início da linhagem | N/A | v001 | Criação inicial da análise de decisão para a Issue #154 | Delimita escopo, dados estáveis e formato da fixture |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `docs/requisitos_funcionais.md` | Primária | Prosa | Documentação | Markdown | Seção RF05 a RF09 e RF14 a RF15 | Commit 5d5b185 |
| `src/backend/domain/curriculo.py` | Primária | Código-fonte | Produção | Python | Agregado `Curriculo` e referências | Commit 5d5b185 |
| `src/backend/domain/itens_perfil.py` | Primária | Código-fonte | Produção | Python | Entidades reutilizáveis de perfil | Commit 5d5b185 |
| `src/backend/domain/usuario.py` | Primária | Código-fonte | Produção | Python | Agregado `Usuario` e dados de contato | Commit 5d5b185 |
| `src/backend/domain/value_objects.py` | Primária | Código-fonte | Produção | Python | Identificadores tipados, períodos e contatos | Commit 5d5b185 |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Regras de Clean Architecture, DDD e docstrings | Commit 5d5b185 |
| `README.md` | Contexto | Prosa | Documentação | Markdown | Atribuições de papéis na equipe | Commit 5d5b185 |

### Limites da evidência dos artefatos

Os contratos das entidades do domínio estão consolidados no commit `5d5b185`. Os renderizadores reais de PDF/DOCX ainda não existem no repositório; portanto, a fixture deve fornecer os dados de domínio e uma representação canônica pronta para consumo por qualquer adaptador de exportação.

## Problema enriquecido

### Resultado desejado

Disponibilizar uma fixture de currículo completa, estável e imutável que sirva de insumo confiável e determinístico para os futuros testes de exportação de currículo (PDF, DOCX e visualização de dados).

### Atores e interesses

- **Engenharia de Testes / QA (Gustavo Minoru Haga):** Necessita de um currículo totalmente populado com dados válidos, sem depender de banco de dados ou chamadas externas, para estruturar testes previsíveis.
- **Desenvolvedor de Exportação (Vinicius Regazio Farias):** Necessita de massa de dados padronizada que cubra todas as seções do currículo para implementar e validar os motores de exportação PDF e DOCX.
- **Pipeline de CI:** Necessita que os testes executem de forma rápida, isolada e determinística, sem flakiness por causa de datas relativas ou UUIDs aleatórios.

### Evidências e fatos observados

- O aggregate root `Curriculo` armazena apenas `ReferenciaCurriculo` para cada item associado.
- Os dados reais dos itens (textos de formação, experiência, projetos, competências, idiomas) residem nas entidades de `itens_perfil.py`.
- Os dados pessoais e de contato residem no aggregate `Usuario` e no value object `DadosContato`.
- Para testar uma exportação (PDF ou DOCX), o mecanismo exportador precisa de todos os dados consolidados (dados pessoais + versão do currículo + itens desreferenciados).

### Hipóteses

- O uso de UUIDs fixos (determinísticos) e datas fixas permite que testes de exportação validem a saída gerada (texto exato, checksum ou estrutura) sem variações indesejadas a cada execução.
- Fornecer tanto os agregados/entidades isolados quanto um modelo consolidado (`CurriculoExportacaoDados`) atende tanto a testes de integração do repositório/serviço quanto a testes do motor gerador de documentos.

### Perguntas em aberto

- Nenhum bloqueio identificado: o vocabulário de dados já está totalmente definido pelas entidades de domínio existentes.

### Escopo

- Criar o pacote `src/backend/tests/fixtures/` com módulo `curriculo_exportacao.py`.
- Definir constantes estáveis com UUIDs fixos e dados representativos de um estudante da FATEC.
- Fornecer função fábrica `obter_curriculo_exportacao_fixture()` retornando a estrutura consolidada estável e imutável.
- Incluir testes unitários rigorosos em `src/backend/tests/test_fixture_exportacao_curriculo.py` para validar todas as invariantes e o determinismo da fixture.

### Fora do escopo

- Implementar o renderizador de PDF ou DOCX (responsabilidade do desenvolvedor de exportação).
- Persistir dados no banco de dados real PostgreSQL.
- Criar endpoints HTTP ou rotas de download (responsabilidade das fatias de API/adaptadores).

### Critérios de sucesso

- A fixture deve fornecer:
  1. Usuário com nome, email e dados de contato completos (telefone, endereço, LinkedIn, Lattes).
  2. Pelo menos uma formação acadêmica completa com período válido.
  3. Pelo menos uma experiência profissional descrita com período válido.
  4. Pelo menos um projeto acadêmico detalhado com tecnologias.
  5. Competências categorizadas e idiomas com níveis.
  6. Agregado `Curriculo` válido contendo referências a todos os itens acima.
- Execuções consecutivas devem gerar resultados idênticos (determinismo).
- 100% de conformidade com as regras de docstring do `AGENTS.md`.
- Suíte de testes do projeto passando com código de saída 0 no ambiente `nix develop .#backend`.

## Restrições aplicáveis

- `[CRITICAL]` Clean Architecture e DDD em todas as construções.
- `[CRITICAL]` Uso obrigatório do Nix para execução de comandos e testes.
- `[REQUIRED]` Testes unitários executados no ambiente `backend`.
- `[REQUIRED]` Toda classe e função com docstring contendo O que faz, Como faz e Qual finalidade atende.

## Classificação comentada

- **Esfera:** Engenharia.
- **Preocupações:** Confiabilidade (`reliability`), corretude (`correctness`) e testabilidade (`testability`).
- **Nível de decisão:** Design de módulo de testes e fixtures.

## Decisão de roteamento

O artefato foi alocado em `prompts/backend` por se tratar da base de testes e entidades do backend de currículo que alimentará o pipeline do sistema.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `determinism` | 1 | UUIDs e datas 100% fixos | Impede testes flaky em comparações de layout de exportação |
| `completeness` | 2 | Todas as seções de RF01 a RF09 contempladas | Permite que os testes de PDF/DOCX cubram todas as seções visuais |
| `immutability` | 3 | Estruturas congeladas ou instanciadas limpas | Evita contaminação entre testes que consomem a fixture |

## Alternativas consideradas

- **Alternativa A (Recomendada):** Módulo de fixture estruturado com classes imutáveis/dataclasses e entidades do domínio, com IDs fixos determinísticos e dados ricos realistas de um estudante FATEC.
- **Alternativa B:** Gerar dados dinâmicos com `uuid4()` e datas dinâmicas a cada chamada de teste. (Inviável para testes de exportação estável de arquivos, pois quebra comparadores de checksum, extração de texto ou snapshots).
- **Alternativa C:** Fixture baseada em arquivo estático JSON externo. (Inferior pois não se integra diretamente com a tipagem forte dos value objects e entidades de domínio em Python).

## Histórico e decisão atual

### Decisão recomendada nesta versão

Implementar o módulo de fixture em `src/backend/tests/fixtures/curriculo_exportacao.py`, disponibilizando constantes determinísticas e uma função fábrica que entrega tanto os agregados do domínio quanto o agrupamento consolidado de dados de exportação, acompanhado de testes unitários em `src/backend/tests/test_fixture_exportacao_curriculo.py`.

## Riscos e efeitos de segunda ordem

- Risco de dessincronização futura caso novos campos obrigatórios sejam adicionados às entidades de domínio.
- Mitigação: A fixture possui teste unitário dedicado que falhará no CI se qualquer invariante de domínio for alterada sem atualizar a fixture.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Fixture é válida perante o domínio | Testes unitários executando com sucesso | `unittest discover` via Nix | Falha de validação ou exceção de domínio |
| Dados são determinísticos | Múltiplas instanciações produzem igualdade estrutural | Asserções no teste unitário | IDs ou atributos divergentes |

## Handoffs e atividades posteriores

- Handoff para Vinicius Regazio Farias (implementador do módulo de exportação) utilizar a fixture nos testes de geração de PDF e DOCX.
- Utilização da fixture para testes de integração e E2E nas issues subsequentes (#153).

## Síntese

A fixture de currículo para exportação consolida todos os itens do perfil em um cenário rico e determinístico, viabilizando testes robustos e confiáveis de geração de arquivos.

Arquivo criado em prompts/backend/20261006-215500-fixture-teste-exportacao-curriculo-v001.md. Avalie se o local escolhido é de fato o mais adequado.
