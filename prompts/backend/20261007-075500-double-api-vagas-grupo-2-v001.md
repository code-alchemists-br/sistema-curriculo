---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-07T07:55:00-03:00"
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
      locator: "RF10 a RF12 (Busca de vagas e associações)"
      content_state: commit
      revision: "e403b36"
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RNF06 (Tolerância a falhas de integração com API de vagas)"
      content_state: commit
      revision: "e403b36"
      availability: available
    - path: docs/casos-de-uso-v2.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "UC09 e Módulo de integração com o Grupo 2"
      content_state: commit
      revision: "e403b36"
      availability: available
    - path: README.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "Equipe e Atribuições: Testes/Controle de qualidade e integração com Grupo 2"
      content_state: commit
      revision: "e403b36"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "e403b36"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "O double implementa a simulação determinística do cliente de integração da API externa de vagas do Grupo 2 (RF10/RNF06) para uso no backend e em testes integrados."
classification:
  sphere: engineering
  concerns: [reliability, testability, resilience]
  decision_kind: design
  scope: subsystem
  lifecycle: development
  urgency: normal
  uncertainty: low
  reversibility: high
  risk: low
---

# Análise de decisão — Preparar double da API de vagas do Grupo 2

## Solicitação original

```text
Issue #151: Preparar double da API de vagas do Grupo 2
Crie um double determinístico para respostas de sucesso, lista vazia, erro e indisponibilidade da API de vagas.
```

## Informações complementares

- Atribuição de Gustavo Minoru Haga (Testes/Controle de qualidade): *"Criação de doubles de testes para si mesmos e para outros membros da equipe conforme necessidade."*
- Atribuição de André Luiz da Silva Lima: *"Funcionalidades de vagas e associações currículo–vaga; integração com o Sistema Externo do Grupo 2"*.
- Requisitos vinculados:
  - **RF10:** Consultar ferramenta de busca de vagas por meio de API e processar a lista retornada em JSON.
  - **RNF06:** Tolerância a falhas de integração tratando indisponibilidade, demora e respostas inválidas de forma controlada.
- Todas as funções, métodos, DTOs e classes devem conter docstrings completas com o que faz, como faz e qual finalidade atende, em conformidade com o `AGENTS.md`.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Início da linhagem | N/A | v001 | Criação inicial da análise de decisão para a Issue #151 | Define contrato, dados sintéticos e modos do double |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `docs/requisitos_funcionais.md` | Primária | Prosa | Documentação | Markdown | RF10, RF11 e RF12 | Commit e403b36 |
| `docs/requisitos_nao_funcionais.md` | Primária | Prosa | Documentação | Markdown | RNF06 (Tolerância a falhas de integração) | Commit e403b36 |
| `docs/casos-de-uso-v2.md` | Apoio | Prosa | Documentação | Markdown | UC09 (Módulo de integração Grupo 2) | Commit e403b36 |
| `README.md` | Contexto | Prosa | Documentação | Markdown | Atribuições de papéis na equipe | Commit e403b36 |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Clean Architecture e docstrings | Commit e403b36 |

### Limites da evidência dos artefatos

O Grupo 2 é um sistema externo em desenvolvimento por outra equipe. O contrato da API externa ainda não possui endpoint de produção; portanto, a comunicação é abstrata e deve ser modelada por uma porta/protocolo independente de detalhes HTTP, permitindo que o double simule o comportamento esperado pela aplicação.

## Problema enriquecido

### Resultado desejado

Disponibilizar um test double determinístico, configurável e assíncrono para a API de vagas do Grupo 2, capaz de simular fielmente os quatro cenários exigidos:
1. Sucesso com lista populada de vagas estruturadas;
2. Lista vazia (busca válida sem resultados);
3. Erro de resposta (resposta corrompida, HTTP 500 ou formato inesperado);
4. Indisponibilidade externa (timeout ou falha de conexão de rede, validando o RNF06).

### Atores e interesses

- **Equipe de Testes e QA (Gustavo Minoru Haga):** Requer controle total sobre os cenários da API externa para testar integração, resiliência (RNF06) e a jornada E2E (#153) sem dependência de rede.
- **Desenvolvedor de Vagas e Integração (André Luiz):** Requer um substituto confiável de testes para desenvolver o adaptador e os casos de uso de associação currículo–vaga antes que o Grupo 2 publique a API real.
- **Pipeline de CI:** Exige execução de testes rápida, isolada e sem chamadas de rede para serviços externos.

### Evidências e fatos observados

- RF10 e ADR-001 especificam que a integração ocorre via JSON.
- RNF06 exige tratamento explícito de respostas inválidas e indisponibilidade.
- O double deve ser compatível com assincronismo (`async def`) para integrar-se ao fluxo FastAPI / Clean Architecture do backend.

### Hipóteses

- Definir uma enumeração com os modos `SUCESSO`, `LISTA_VAZIA`, `ERRO_RESPOSTA` e `INDISPONIBILIDADE` oferece interface declarativa e simples para os testes alternarem comportamentos.
- Registrar histórico de buscas no double (termo pesquisado e parâmetros) permite que testes façam asserções de espionagem (*spy*).

### Escopo

- Criar pacote `src/backend/tests/doubles/` com módulo `api_vagas_grupo2.py`.
- Definir DTO imutável de vaga externa (`VagaExternaDto`), tipos de exceção e contrato de porta (`ClienteApiVagasGrupo2`).
- Implementar a classe `DoubleApiVagasGrupo2` com modos determinísticos e gravação de histórico de chamadas.
- Implementar testes unitários em `src/backend/tests/test_double_api_vagas_grupo2.py` exercitando os 4 modos e as invariantes de cada cenário.

### Fora do escopo

- Implementar chamadas HTTP reais com `httpx` ou `requests` para servidores externos (responsabilidade do adaptador real).
- Implementar telas web de exibição de vagas (responsabilidade do frontend).
- Persistir associações currículo-vaga no banco de dados (escopo de André Luiz).

### Critérios de sucesso

- O double deve responder com sucesso reproduzível, lista vazia, exceção de resposta inválida ou exceção de indisponibilidade conforme configurado.
- Cobertura de testes unitários de 100% dos métodos e modos do double.
- Conformidade estrita com as regras de docstrings do `AGENTS.md`.
- Suíte de testes do projeto executando via Nix com código de saída 0.

## Restrições aplicáveis

- `[CRITICAL]` Clean Architecture e separação de contratos.
- `[CRITICAL]` Execução obrigatória via Nix (`nix develop .#backend`).
- `[REQUIRED]` Docstrings com O que faz, Como faz e Qual finalidade atende.

## Classificação comentada

- **Esfera:** Engenharia.
- **Preocupações:** Confiabilidade (`reliability`), testabilidade (`testability`) e resiliência (`resilience`).
- **Nível de decisão:** Design de test doubles e contratos de integração.

## Decisão de roteamento

Alocado em `prompts/backend` por se tratar de componente de teste do subsistema backend de vagas e integração externa.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `determinism` | 1 | Resultados idênticos sem flakiness | Garante estabilidade nos testes automatizados |
| `completeness` | 2 | Atendimento dos 4 cenários exigidos | Cumpre os requisitos estipulados na Issue #151 |
| `observability` | 3 | Registro de chamadas (spy) | Permite verificar se o adaptador repassou filtros e termos corretos |

## Alternativas consideradas

- **Alternativa A (Recomendada):** Double configurável em memória com modos explícitos, DTOs tipados e gravação de chamadas, sem dependência externa.
- **Alternativa B:** Mock dinâmico com `unittest.mock.AsyncMock`. (Inferior porque não provê massa estável de vagas realistas nem tipagem de contrato compartilhável com outros testes).
- **Alternativa C:** Servidor HTTP mock local rodando em porta TCP. (Mais complexo, lento e desnecessário para a camada de aplicação/testes unitários e de integração).

## Histórico e decisão atual

### Decisão recomendada nesta versão

Implementar o módulo `DoubleApiVagasGrupo2` em `src/backend/tests/doubles/api_vagas_grupo2.py` com modos declarativos e testes unitários dedicados em `src/backend/tests/test_double_api_vagas_grupo2.py`.

## Riscos e efeitos de segunda ordem

- Risco de discrepância entre os campos do DTO e a API real quando ela for entregue pelo Grupo 2.
- Mitigação: O DTO concentra a tradução em um único ponto, permitindo adaptação imediata quando o contrato final for consolidado.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Cenário Sucesso retorna dados ricos | Asserção do tamanho e campos das vagas | Teste unitário | Vagas vazias ou campos ausentes |
| Cenário Lista Vazia retorna lista vazia | Asserção `len(resultado) == 0` | Teste unitário | Exceção ou vagas presentes |
| Cenário Erro levanta falha de formato | Asserção `assertRaises(RespostaInvalidaApiVagas)` | Teste unitário | Retorno silencioso |
| Cenário Indisponibilidade levanta falha de conexão | Asserção `assertRaises(ApiVagasIndisponivel)` | Teste unitário | Retorno silencioso |

## Handoffs e atividades posteriores

- Handoff para André Luiz utilizar o double nos testes do caso de uso de vagas e associações.
- Reutilização na Issue #153 (cenário E2E de preenchimento do currículo).

## Síntese

O double da API de vagas do Grupo 2 fornece um simulador completo e determinístico de sucesso, lista vazia, erro e indisponibilidade, desacoplando o desenvolvimento local da dependência externa.

Arquivo criado em prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md. Avalie se o local escolhido é de fato o mais adequado.
