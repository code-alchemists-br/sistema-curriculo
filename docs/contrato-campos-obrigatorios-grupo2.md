# Especificação Técnica — Formato e Campos Obrigatórios de Integração

- **Referência:** Task `[F1.6] #173` (Definir o formato e os campos obrigatórios do contrato com o Grupo 2)
- **Fatia Técnica Relacionada:** `[F7.1–F7.6]`, `[Card #124]`
- **Sistema Emissor (Grupo 1):** `sistema-curriculo`
- **Sistema Receptor (Grupo 2):** `esw3_cvmatcher`
- **Documentador Oficial:** Marcelo Aparecido da Rosa ([@marcelo-3com](https://github.com/marcelo-3com))
- **Líder Técnico (Grupo 1):** Rodolpho P. M. Ferreira
- **Responsável Técnico Integração (Grupo 1):** André Luiz da Silva Lima
- **Líder Técnico (Grupo 2):** Carybé
- **Versão:** 1.0.0
- **Data:** Outubro de 2026

---

## 1. Objetivo

Definir de maneira exaustiva o formato dos dados, os tipos primitivos, as regras de validação e a **obrigatoriedade de cada campo** trafegado entre o **Sistema Currículo (Grupo 1)** e a engine de correspondência de vagas **CV Matcher (Grupo 2)**.

Este documento atua como contrato vinculante para:
1. A camada de validação e serialização do Grupo 1 (desenvolvida por André Luiz).
2. O parser de ingestão e algoritmo de matching do Grupo 2 (coordenado por Carybé).

---

## 2. Princípio de Privacidade e LGPD (*Privacy by Design*)

Para garantir conformidade com a LGPD (Lei Geral de Proteção de Dados):
* **Nenhum dado pessoal sensível ou identificador direto** (como CPF, RG, número de telefone, e-mail pessoal ou endereço residencial) deve ser transmitido ao Grupo 2.
* A identificação do candidato ocorre exclusivamente através de um identificador anônimo e opaco: **`curriculo_id`** (UUID v4 ou código alfanumérico com prefixo `cur_`).
* A associação entre a identidade real do estudante e o `curriculo_id` permanece sob controle estrito do banco de dados do Grupo 1.

---

## 3. Dicionário de Dados do Currículo (Request Payload)

Endpoint de destino no Grupo 2: `POST /api/v1/vagas/match`

### 3.1. Campos Raiz (*Root Level*)

| Campo | Tipo | Obrigatório? | Regra de Validação / Restrição | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `curriculo_id` | String | **SIM** | Não nulo, alfanumérico, min: 8, max: 64 chars. | Identificador único anônimo da submissão do currículo. |
| `dados_pessoais` | Object | **SIM** | Não nulo. | Objeto com critérios de localização e preferências do aluno. |
| `formacao_academica` | Array[Obj] | **SIM** | Mínimo 1 item. | Histórico escolar universitário (público-alvo: FATEC-SP). |
| `competencias` | Array[Obj] | **SIM** | Mínimo 1 item. | Lista de competências técnicas/interpessoais para o matching. |
| `idiomas` | Array[Obj] | NÃO | Array opcional (pode ser vazio `[]`). | Idiomas conhecidos e níveis de fluência. |
| `experiencias_profissionais`| Array[Obj] | NÃO | Array opcional (pode ser vazio `[]`). | Experiências de trabalho/estágios anteriores. |
| `projetos_academicos` | Array[Obj] | NÃO | Array opcional (pode ser vazio `[]`). | Projetos integradores, TCCs e projetos práticos acadêmicos. |

---

### 3.2. Detalhamento do Objeto `dados_pessoais`

| Campo | Tipo | Obrigatório? | Valores Aceitos / Validação | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `cidade` | String | NÃO | Min: 2, Max: 60 chars. | `"São Paulo"` |
| `estado` | String | NÃO | UF com exatamente 2 letras maiúsculas. | `"SP"` |
| `modalidade_preferencial` | String | **SIM** | Enum: `["presencial", "remoto", "hibrido", "indiferente"]` | `"hibrido"` |

---

### 3.3. Detalhamento dos Itens de `formacao_academica`

| Campo | Tipo | Obrigatório? | Regra de Validação | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `curso` | String | **SIM** | Min: 3, Max: 100 chars. | `"Análise e Desenvolvimento de Sistemas"` |
| `instituicao` | String | **SIM** | Min: 2, Max: 100 chars. Default: `"FATEC-SP"` | `"FATEC-SP"` |
| `status` | String | **SIM** | Enum: `["em_andamento", "concluido", "trancado"]` | `"em_andamento"` |
| `previsao_conclusao` | String | NÃO | Formato de data ISO: `YYYY-MM` ou `YYYY` | `"2026-12"` |

---

### 3.4. Detalhamento dos Itens de `competencias`

> **Importante para o Matching:** As competências constituem o peso primário no cálculo do algoritmo de aderência do Grupo 2. Pelo menos 1 competência deve ser informada.

| Campo | Tipo | Obrigatório? | Regra de Validação | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `nome` | String | **SIM** | Min: 1, Max: 50 chars. | `"Java"`, `"Spring Boot"` |
| `nivel` | String | **SIM** | Enum: `["basico", "intermediario", "avancado"]` | `"intermediario"` |

---

### 3.5. Detalhamento dos Itens de `idiomas` (Opcional)

| Campo | Tipo | Obrigatório? | Regra de Validação | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `idioma` | String | **SIM** *(se array não vazio)* | Min: 2, Max: 40 chars. | `"Inglês"`, `"Espanhol"` |
| `nivel` | String | **SIM** *(se array não vazio)* | Enum: `["basico", "intermediario", "avancado", "fluente"]` | `"intermediario"` |

---

### 3.6. Detalhamento dos Itens de `experiencias_profissionais` (Opcional)

> **Justificativa de Não-Obrigatoriedade:** Como a plataforma é voltada a alunos universitários e candidatos a estágios iniciais, muitos não possuem experiência formal prévia. O sistema **não deve bloquear** estudantes sem experiência profissional.

| Campo | Tipo | Obrigatório? | Regra de Validação | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `cargo` | String | **SIM** *(se informado)* | Min: 2, Max: 80 chars. | `"Estagiário de TI"` |
| `empresa` | String | **SIM** *(se informado)* | Min: 2, Max: 80 chars. | `"Tech Solutions"` |
| `descricao` | String | NÃO | Max: 1000 chars. Resumo das responsabilidades. | `"Atuação em APIs REST..."` |

---

### 3.7. Detalhamento dos Itens de `projetos_academicos` (Opcional)

| Campo | Tipo | Obrigatório? | Regra de Validação | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `titulo` | String | **SIM** *(se informado)* | Min: 3, Max: 100 chars. | `"Sistema de Apoio Profissional"` |
| `tecnologias` | Array[String]| NÃO | Lista de tags de tecnologias utilizadas. | `["Java", "Clean Architecture"]` |
| `descricao` | String | NÃO | Max: 1000 chars. | `"Projeto de Engenharia de Software 3."`|

---

## 4. Dicionário de Dados dos Parâmetros de Consulta (Query Params)

| Parâmetro | Tipo | Obrigatório? | Default | Faixa Válida | Descrição |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `limit` | Integer | NÃO | `10` | `1 <= limit <= 100` | Quantidade máxima de vagas retornadas ordenadas por compatibilidade. |
| `offset` | Integer | NÃO | `0` | `offset >= 0` | Deslocamento de registros para fins de paginação. |

---

## 5. Dicionário de Dados da Resposta de Vagas (Response Payload - Grupo 2 $\rightarrow$ Grupo 1)

| Campo | Tipo | Obrigatório? | Descrição |
| :--- | :--- | :--- | :--- |
| `status` | String | **SIM** | `"sucesso"` ou `"erro"`. |
| `meta.curriculo_id` | String | **SIM** | Eco do identificador do currículo avaliado. |
| `meta.total_disponiveis` | Integer | **SIM** | Total de vagas na base que atingiram o limiar mínimo de match. |
| `meta.limit` | Integer | **SIM** | Limite aplicado na consulta (1..100). |
| `meta.offset` | Integer | **SIM** | Deslocamento aplicado. |
| `meta.retornadas` | Integer | **SIM** | Quantidade de itens no array `vagas` da resposta. |
| `vagas[].vaga_id` | String | **SIM** | Identificador único da vaga na base do Grupo 2. |
| `vagas[].titulo` | String | **SIM** | Cargo/título da oportunidade. |
| `vagas[].empresa` | String | **SIM** | Nome da empresa anunciante. |
| `vagas[].localizacao` | String | **SIM** | Cidade/Estado da vaga. |
| `vagas[].modalidade` | String | **SIM** | Enum: `["presencial", "remoto", "hibrido"]`. |
| `vagas[].faixa_bolsa` | String | NÃO | Faixa de remuneração ou bolsa-auxílio (ex: `"R$ 2.000,00"`). |
| `vagas[].descricao` | String | **SIM** | Resumo das atividades da vaga. |
| `vagas[].requisitos_obrigatorios` | Array[Str] | **SIM** | Habilidades indispensáveis. |
| `vagas[].diferenciais` | Array[Str] | NÃO | Habilidades desejáveis. |
| `vagas[].compatibilidade.score_percentual` | Float | **SIM** | Nota de aderência calculada entre 0.0 e 100.0. |
| `vagas[].compatibilidade.pontos_aderentes` | Array[Str] | **SIM** | Competências do estudante que casaram com os requisitos da vaga. |
| `vagas[].compatibilidade.habilidades_desejaveis_faltantes` | Array[Str] | NÃO | Oportunidades de aprendizado para o aluno. |
| `vagas[].url_candidatura`| String | **SIM** | Link externo para inscrição na oportunidade. |

---

## 6. Matriz de Resiliência e Fallbacks

| Situação | Ação do Grupo 1 (Frontend/Backend) | Ação do Grupo 2 (API Vagas) |
| :--- | :--- | :--- |
| **Estudante sem competências informadas** | Bloqueia envio no frontend: exige ao menos 1 competência cadastrada. | Se receber sem competências, rejeita com HTTP `422 Unprocessable Entity`. |
| **Estudante sem experiência profissional** | Permite envio normalmente com `experiencias_profissionais: []`. | Processa o matching considerando apenas formação e competências. |
| **`limit` omitido na requisição** | Envia sem o parâmetro na URL. | Assume automaticamente o valor padrão de **10 vagas**. |
| **`limit` inválido (< 1 ou > 100)** | Valida antes de disparar. Se passar, recebe erro. | Responde imediatamente com HTTP `400 Bad Request`. |
| **Falha de rede / Timeout do Grupo 2** | Retorna última busca em cache ou mensagem amigável de indisponibilidade. | Registra erro no log de telemetria/observabilidade. |

---

## 7. Rastreabilidade com o Backlog

* **Card #173 (`[F1.6]`):** Cumpre integralmente o requisito de definição de campos obrigatórios e formatos de intercâmbio de dados.
* **Card #124:** Alinhado com a modelagem preliminar do contrato de busca de vagas.
* **Card #383 (`[F10.2]`):** Complementa o contrato público e o catálogo de erros entregue no PR #586.
