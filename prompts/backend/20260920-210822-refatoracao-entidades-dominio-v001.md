---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: 2026-09-20T21:08:22-03:00
lineage:
  mode: initial
  root: null
  supersedes: null
  change_type: initial
  secondary_change_types: []
  decision_impact: initial
subjects:
  kind: file-set
  files:
    - path: src/backend/domain/entities.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "88f08a4"
      availability: available
    - path: src/backend/domain/curriculo.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "88f08a4"
      availability: available
    - path: src/backend/domain/__init__.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "88f08a4"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "88f08a4"
      availability: available
    - path: src/backend/application/cadastro_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "88f08a4"
      availability: available
    - path: src/backend/application/perfil_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "88f08a4"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "88f08a4"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_usuario.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "88f08a4"
      availability: available
    - path: src/backend/tests/test_domain_entities.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "88f08a4"
      availability: available
    - path: src/backend/tests/test_domain_curriculo.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "88f08a4"
      availability: available
    - path: prompts/backend/20260914-camada-dominio-v001.md
      relationship: context
      representation: prose
      function: decision-analysis
      format: markdown
      analysis_scope: "sections: Escopo, Restrições aplicáveis, Decisão recomendada"
      locator: null
      content_state: commit
      revision: "88f08a4"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "A decisão trata exclusivamente da organização interna do domínio e dos seus consumidores no backend."
classification:
  sphere: engineering
  concerns: [domain, architecture, maintainability]
  decision_kind: change
  scope: component
  lifecycle: evolution
  urgency: normal
  uncertainty: low
  reversibility: moderate
  risk: medium
---

# Análise de decisão — refatoração das entidades do domínio

## Solicitação original

`$decision-analysis-v4 Vamos refatorar as entidades do projeto. Há dois arquivos "src\backend\domain\entities.py" e "src\backend\domain\curriculo.py". O arquivo "src\backend\domain\curriculo.py" reunia entidades pequenas, mas agora com o crescimento previsto da complexidade é necessário refatorá-lo bem como outros arquivos que dele dependem. Faça um plano de refatoração.`

## Informações complementares

- A premissa sobre os arquivos está invertida no estado analisado: `curriculo.py`
  contém somente o aggregate root `Curriculo`; `entities.py` contém `Usuario` e
  as seis entidades reutilizáveis do perfil.
- A decisão de domínio anterior estabeleceu `Usuario` e `Curriculo` como
  aggregate roots separados e os itens de perfil como entidades independentes
  pertencentes ao usuário. Esta refatoração não altera esses limites.
- Existem cinco importadores internos diretos de `backend.domain.entities`:
  três na Application e dois adapters SQLAlchemy. Os testes usam a superfície
  pública `backend.domain` e não dependem diretamente do módulo atual.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Organização das entidades | Uma análise anterior definiu os agregados, mas não a modularização após seu crescimento | v001 inicial desta decisão de refatoração | O arquivo genérico concentra conceitos com ritmos de mudança distintos | Nenhum comportamento de negócio deve mudar |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/domain/entities.py` | Principal | Código-fonte | Produção | Python | Arquivo completo | Commit `88f08a4` |
| `src/backend/domain/curriculo.py` | Principal | Código-fonte | Produção | Python | Arquivo completo | Commit `88f08a4` |
| `src/backend/domain/__init__.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `88f08a4` |
| Application e adapters SQLAlchemy listados no front matter | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `88f08a4` |
| Testes de domínio listados no front matter | Apoio | Código-fonte | Teste | Python | Arquivo completo | Commit `88f08a4` |
| `prompts/backend/20260914-camada-dominio-v001.md` | Contexto | Prosa | Análise de decisão | Markdown | Escopo, restrições e decisão | Commit `88f08a4` |

### Limites da evidência dos artefatos

O repositório não declara uma API pública consumida por projetos externos.
Portanto, a remoção de `entities.py` é segura apenas após uma busca completa
pelos importadores internos e pela confirmação da equipe de que não há
consumidores fora deste repositório. A proposta não introduz novos conceitos de
domínio, nem decide regras ainda abertas para os itens de perfil.

## Problema enriquecido

### Resultado desejado

Organizar o pacote `backend.domain` por responsabilidade de negócio, para que
o crescimento de `Usuario` e dos itens reutilizáveis do perfil não transforme
um módulo genérico em ponto de acoplamento. A refatoração deve preservar os
comportamentos, as identidades, a independência de frameworks e a API pública
do pacote `backend.domain`.

### Atores e interesses

- Desenvolvedores de domínio precisam localizar regras de conta, currículo e
  itens de perfil sem navegar por um arquivo guarda-chuva.
- Casos de uso e adapters precisam de imports explícitos e estáveis para o
  agregado `Usuario`.
- Testes precisam continuar expressando comportamento de domínio, sem adotar
  a organização de arquivos como detalhe funcional.
- A equipe precisa de uma transição pequena, verificável e reversível, sem
  alterar o schema, ORM, API ou contratos de caso de uso.

### Evidências e fatos observados

- `Curriculo` já está isolado em `curriculo.py`, protege sua coleção de
  referências e não importa as entidades de perfil.
- `entities.py` agrupa `Usuario`, `FormacaoAcademica`,
  `ExperienciaProfissional`, `ProjetoAcademico`, `Competencia`, `Idioma` e
  `Documento`.
- `Usuario` possui comportamento próprio de edição e exclusão lógica; os itens
  de perfil são hoje entidades imutáveis de dados, com proprietário comum
  `UsuarioId`.
- `backend.domain.__init__` já é a superfície pública usada pela API e pelos
  testes; imports diretos de `entities.py` concentram-se em código interno.
- O domínio não deve importar Application, Infrastructure, API, SQLAlchemy ou
  qualquer outro framework.

### Hipóteses

- Os seis itens de perfil continuarão crescendo em conjunto, por serem dados
  reutilizáveis pertencentes ao usuário, mas ainda não justificam um módulo por
  classe.
- `Usuario` terá mais regras de ciclo de vida e merece módulo próprio.
- `Curriculo` continuará sendo agregado separado, sem absorver itens de perfil
  nem mover suas referências para um módulo de entidades genérico.

### Perguntas em aberto

- Há consumidores externos que importam `backend.domain.entities` diretamente?
- A evolução próxima demanda comportamentos próprios para algum item de perfil
  que justifique separá-lo de `itens_perfil.py`?
- O nome de domínio futuro deve continuar sendo `Usuario` ou será explicitado
  como estudante/candidato em uma decisão de produto posterior?

### Escopo

- Criar `src/backend/domain/usuario.py` para o aggregate root `Usuario` e seu
  comportamento de perfil.
- Criar `src/backend/domain/itens_perfil.py` para formação, experiência,
  projeto, competência, idioma e documento.
- Manter `src/backend/domain/curriculo.py` como o módulo exclusivo do aggregate
  root `Curriculo`.
- Atualizar `src/backend/domain/__init__.py` para reexportar os mesmos símbolos
  públicos a partir dos novos módulos.
- Atualizar os importadores diretos internos na Application e na Infrastructure
  para importar `Usuario` de `backend.domain.usuario`.
- Renomear testes somente quando seu nome descreve a antiga estrutura, mantendo
  ou ampliando a cobertura de construção e transições de `Usuario`, itens de
  perfil e `Curriculo`.
- Remover `entities.py` na mesma mudança, depois da auditoria de imports e da
  confirmação de ausência de consumidores externos.

### Fora do escopo

- Alterar regras, campos, identidades, mutabilidade ou limites de agregados.
- Criar casos de uso, DTOs, endpoints, migrations, tabelas, modelos ORM ou
  mapeamentos novos.
- Resolver as pendências existentes de persistência da exclusão lógica.
- Separar cada item de perfil em seu próprio módulo sem evidência de coesão de
  mudança independente.

### Critérios de sucesso

- `Usuario` é definido apenas em `domain/usuario.py`; itens reutilizáveis são
  definidos apenas em `domain/itens_perfil.py`; `Curriculo` permanece apenas em
  `domain/curriculo.py`.
- `from backend.domain import ...` continua expondo todos os símbolos atuais.
- Não restam imports de `backend.domain.entities` no repositório após a
  remoção do arquivo, exceto uma compatibilidade temporária explicitamente
  aprovada caso existam consumidores externos.
- Os testes unitários de domínio e dos casos de uso afetados passam em `nix
  develop .#backend` e comprovam que a refatoração não muda comportamento.
- O domínio continua sem dependências de camadas externas e todas as docstrings
  mantêm responsabilidade, abordagem e finalidade.

## Restrições aplicáveis

- Preservar Clean Architecture: dependências apontam para dentro; o domínio não
  conhece infraestrutura, Application ou API.
- Preservar DDD: `Usuario` e `Curriculo` são aggregate roots separados; itens
  reutilizáveis não passam a pertencer ao agregado `Curriculo`.
- Não misturar esta mudança estrutural com schema, migration, correções de
  persistência ou alteração de comportamento.
- Executar verificações e testes unitários do backend somente com `nix develop
  .#backend`.
- Documentar toda classe e função criada ou movida conforme `AGENTS.md`.

## Alternativas consideradas

| Alternativa | Benefícios | Custos e riscos | Decisão |
|---|---|---|---|
| Manter `entities.py` como está | Nenhuma migração imediata | Agrava o módulo genérico e reduz a descoberta por responsabilidade | Rejeitada |
| Um módulo por entidade | Máxima separação futura | Fragmenta sete conceitos pequenos, aumenta imports e não acompanha a coesão atual | Adiada |
| `usuario.py`, `itens_perfil.py` e `curriculo.py` | Alinha arquivos aos agregados e à coesão atual, com transição limitada | Exige atualizar importadores e validar consumidores externos | Recomendada |
| Manter `entities.py` como reexportador permanente | Evita quebra para importadores diretos | Preserva o nome genérico e cria dupla superfície sem prazo de remoção | Rejeitada como estado final |

## Decisão recomendada

Adotar três módulos semânticos de entidades: `usuario.py`, `itens_perfil.py` e
`curriculo.py`. `Usuario` deixa `entities.py`; as seis entidades reutilizáveis
vão para `itens_perfil.py`; `Curriculo` não é movido. O `__init__.py` preserva
a fachada pública do pacote. Os consumidores internos diretos passam a usar o
módulo específico, e `entities.py` é removido numa alteração atômica após a
auditoria de consumidores externos.

Se a auditoria identificar consumidor externo sem janela coordenada de
migração, manter temporariamente um `entities.py` que apenas reexporta os
símbolos, com data e tarefa explícitas para removê-lo. Isso é uma contingência,
não a arquitetura final.

## Plano de refatoração

1. Registrar a árvore-alvo e a matriz de migração antes de alterar código:

   | Origem | Destino | Consumidores a atualizar |
   |---|---|---|
   | `Usuario` em `entities.py` | `domain/usuario.py` | `ports.py`, `cadastro_estudante.py`, `perfil_estudante.py`, mapper e repositório SQLAlchemy |
   | Itens reutilizáveis em `entities.py` | `domain/itens_perfil.py` | `domain/__init__.py` e eventuais consumidores encontrados na auditoria |
   | `Curriculo` em `curriculo.py` | sem mudança | `domain/__init__.py` e seus consumidores permanecem |

2. Criar `usuario.py` e mover `Usuario` sem alterar seus campos, métodos,
   docstrings, imports de value objects ou comentários de proveniência.

3. Criar `itens_perfil.py` e mover as seis entidades de perfil sem alterar suas
   identidades, proprietário, campos, imutabilidade ou docstrings.

4. Atualizar `domain/__init__.py` para importar dos novos módulos e manter
   `__all__` idêntico. Este é o contrato de import recomendado para API, testes
   e futuros consumidores internos.

5. Trocar os cinco imports internos diretos de `entities` por
   `backend.domain.usuario`. Não trocar dependências do domínio por imports de
   camadas externas.

6. Renomear `test_domain_entities.py` para um nome que reflita o objeto testado
   (por exemplo, `test_domain_usuario_e_itens_perfil.py`) se a ferramenta de
   testes e o histórico do repositório preservarem a movimentação de forma
   clara. Revisar também os testes de currículo para assegurar que permanecem
   independentes da estrutura dos itens.

7. Rodar uma busca final por `backend.domain.entities`, executar os testes
   unitários afetados e a suíte unitária de backend no ambiente Nix. Remover
   `entities.py` somente se a busca não revelar consumidores pendentes.

8. Revisar a alteração para garantir que não contém migration, mudança de ORM,
   modificação de API ou alteração de comportamento. Atualizar esta análise
   para uma nova versão somente se a auditoria exigir compatibilidade externa
   ou uma organização materialmente diferente.

## Impacto e riscos

| Área | Impacto esperado | Mitigação |
|---|---|---|
| Contratos de import internos | Médio | Atualizar todos os importadores diretos identificados e fazer busca final |
| API pública `backend.domain` | Baixo | Preservar reexports e `__all__` |
| Comportamento de domínio | Nenhum esperado | Não alterar corpos, campos, VOs ou testes de regra durante a extração |
| Consumidor externo desconhecido | Médio | Confirmar com a equipe; usar shim temporário somente se necessário |
| Crescimento futuro | Positivo | Evoluir um item para módulo próprio apenas quando houver regras e ritmo de mudança próprios |

## Estratégia de validação

- Validar a árvore final e a ausência de `backend.domain.entities` com `rg`.
- Executar os testes unitários de domínio, Application e Infrastructure
  afetados usando `nix develop .#backend --command ...`.
- Executar a suíte unitária de backend no mesmo ambiente.
- Verificar que o diff contém somente movimentos, ajustes de imports, nomes de
  testes e documentação correspondente; conferir também `git diff --check`.

## Plano de reversão

Reverter o commit de refatoração restaura os módulos e imports anteriores sem
migração de dados. Se a falha for um consumidor externo descoberto após a
entrega, restaurar temporariamente `entities.py` como reexportador e abrir uma
migração coordenada para esse consumidor; não duplicar as definições de classe.

## Próximos passos

- Confirmar se há consumidores fora deste repositório que importam
  `backend.domain.entities`.
- Implementar o plano em uma branch dedicada, com mudanças estruturais isoladas
  da evolução funcional de perfil e persistência.
- Reavaliar a divisão quando algum item de perfil adquirir comportamento rico
  ou dependências próprias.
