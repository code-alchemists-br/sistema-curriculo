# Especificação Técnica — Formato e Campos Obrigatórios de Integração

- **Referência:** Task `[F1.6] #173` (Definir o formato e os campos obrigatórios do contrato com o Grupo 2)
- **Fatia Técnica Relacionada:** `[F7.1–F7.6]`, `[Card #124]`, `[Card #383]`
- **Sistema Emissor (Grupo 1):** `sistema-curriculo`
- **Sistema Receptor (Grupo 2):** `esw3_cvmatcher` (`cvmatch`)
- **Versão:** 2.0.0 (alinhada ao contrato autoritativo do `cvmatch`)
- **Data:** Novembro de 2026

---

## 1. Objetivo

Definir o formato exato dos dados, tipos primitivos, regras de validação e obrigatoriedade de cada campo trafegado entre o backend do **Sistema Currículo (Grupo 1)** e a engine **CV Matcher (Grupo 2)** em `POST /matches`.

---

## 2. Princípio de Privacidade e LGPD (*Privacy by Design*)

* **Nenhum dado pessoal sensível ou identificador direto** (nome, e-mail, CPF, telefone, endereço, links pessoais, cursos complementares, certificações ou documentos) é transmitido ao Grupo 2.
* A identificação da requisição usa exclusivamente `curriculo_id` (UUID válido), mantido apenas no escopo da requisição e nunca persistido, registrado em logs ou devolvido na resposta do `cvmatch`.
* A projeção rejeita campos desconhecidos (`extra="forbid"`).

---

## 3. Dicionário de Dados do Currículo (Request Payload `POST /matches`)

### 3.1. Campos Raiz (*Root Level*)

| Campo | Tipo | Obrigatório? | Regra de Validação / Restrição | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `curriculo_id` | String (UUID) | **SIM** | UUID válido (persistido em `CurriculoRegistro.id` ou gerado por requisição). | Identificador opaco da requisição. |
| `formacoes` | Array[Obj] | **SIM** | Lista obrigatória; pode ser vazia `[]`. | Formações acadêmicas do estudante. |
| `experiencias` | Array[Obj] | **SIM** | Lista obrigatória; pode ser vazia `[]`. | Experiências profissionais/estágios. |
| `projetos` | Array[Obj] | **SIM** | Lista obrigatória; pode ser vazia `[]`. | Projetos acadêmicos. |
| `competencias` | Array[Obj] | **SIM** | Lista obrigatória; pode ser vazia `[]`. | Competências do estudante. |
| `idiomas` | Array[Obj] | **SIM** | Lista obrigatória; pode ser vazia `[]`. | Idiomas conhecidos. |

> **Observação:** Todas as cinco listas são aceitas inclusive vazias (`[]`). Não há objeto `dados_pessoais` nem valor padrão `FATEC-SP`.

### 3.2. Itens de `formacoes`

| Campo | Tipo | Obrigatório? | Regra de Validação | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `instituicao` | String | **SIM** | 1–200 chars, sem caracteres de controle (`Cc`). | `"FATEC-SP"` |
| `curso` | String | **SIM** | 1–200 chars, sem caracteres de controle (`Cc`). | `"Análise e Desenvolvimento de Sistemas"` |
| `nivel` | String | **SIM** | Enum: `ensino_fundamental`, `ensino_medio`, `tecnico`, `tecnologo`, `graduacao`, `especializacao`, `mestrado`, `doutorado`. | `"tecnologo"` |
| `status` | String | **SIM** | Enum: `em_andamento`, `concluido`, `interrompido`. | `"em_andamento"` |
| `inicio` | String | **SIM** | Data ISO `YYYY-MM-DD`. | `"2024-02-01"` |
| `fim` | String \| `null` | **SIM** (chave obrigatória) | Data ISO `YYYY-MM-DD` (`fim >= inicio`) ou `null`. Obrigatória não-nula se `status == "concluido"`. | `"2026-12-01"` ou `null` |

### 3.3. Itens de `experiencias`

| Campo | Tipo | Obrigatório? | Regra de Validação | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `empresa` | String | **SIM** | String não vazia após trim. | `"Tech Solutions"` |
| `cargo` | String | **SIM** | String não vazia após trim. | `"Estagiário de TI"` |
| `descricao` | String | **SIM** | String não vazia após trim. | `"Atuação em APIs REST."` |
| `inicio` | String | **SIM** | Data ISO `YYYY-MM-DD`. | `"2025-01-01"` |
| `fim` | String \| `null` | **SIM** (chave obrigatória) | Data ISO `YYYY-MM-DD` (`fim >= inicio`) ou `null` para emprego atual. | `null` |

### 3.4. Itens de `projetos`

| Campo | Tipo | Obrigatório? | Regra de Validação | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `titulo` | String | **SIM** | 1–200 chars, sem caracteres de controle (`Cc`). | `"Sistema de Apoio Profissional"` |
| `descricao` | String | **SIM** | 1–2000 chars, sem caracteres de controle (`Cc`). | `"Plataforma de currículos e vagas."` |
| `tecnologias` | String | **SIM** | String única (não array), 1–300 chars, sem `Cc`. | `"Python, FastAPI, Docker"` |

### 3.5. Itens de `competencias`

| Campo | Tipo | Obrigatório? | Regra de Validação | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `descricao` | String | **SIM** | String não vazia após trim. | `"Python"` |
| `nivel` | String | **SIM** | Texto livre não vazio após trim (não enviar `categoria`). | `"intermediario"` |

### 3.6. Itens de `idiomas`

| Campo | Tipo | Obrigatório? | Regra de Validação | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `idioma` | String | **SIM** | String não vazia após trim. | `"Inglês"` |
| `nivel` | String | **SIM** | Texto livre não vazio após trim. | `"B2"` |

---

## 4. Parâmetro de Consulta (Query Param)

| Parâmetro | Tipo | Obrigatório? | Default | Faixa Válida | Descrição |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `limit` | Integer | NÃO | `10` | `1 <= limit <= 100` | Quantidade máxima de vagas retornadas ranqueadas. |

---

## 5. Dicionário de Dados da Resposta (`MatchesResponse` — `200 OK`)

| Campo | Tipo | Obrigatório? | Descrição |
| :--- | :--- | :--- | :--- |
| `matches[]` | Array[Obj] | **SIM** | Lista ordenada de recomendações (pode ser vazia `[]`). |
| `matches[].rank` | Integer | **SIM** | Posição no ranking (`>= 1`). |
| `matches[].score` | Float | **SIM** | Pontuação determinística de compatibilidade em `[0, 100]`. |
| `matches[].eligibility` | Boolean | **SIM** | `true` para vaga ativa; `false` para vaga inativa/expirada (nunca geográfica). |
| `matches[].matched_skills` | Array[Str] | **SIM** | Habilidades do currículo reconhecidas na vaga. |
| `matches[].missing_requirements` | Array[Str] | **SIM** | Requisitos faltantes identificados no matching. |
| `matches[].embedding_model` | String | **SIM** | Identificador do modelo de embeddings usado. |
| `matches[].algorithm_version` | String | **SIM** | Versão do algoritmo de matching. |
| `matches[].job.id` | Integer | **SIM** | Identificador positivo estável da vaga no `cvmatch` (`>= 1`). |
| `matches[].job.title` | String | **SIM** | Título da vaga. |
| `matches[].job.company` | String \| `null` | NÃO | Empresa anunciante. |
| `matches[].job.description` | String \| `null` | NÃO | Descrição da vaga. |
| `matches[].job.keywords` | Array[Str] \| `null` | NÃO | Palavras-chave extraídas. |
| `matches[].job.location` | Object \| `null` | NÃO | Dicionário com `city`, `state`, `country`, `raw`. |
| `matches[].job.work_arrangement` | String \| `null` | NÃO | `REMOTE`, `HYBRID` ou `ON_SITE`. |
| `matches[].job.seniority_level` | String \| `null` | NÃO | `INTERN`, `JUNIOR`, `MID`, `SENIOR`, `SPECIALIST` ou `COORDINATOR`. |
| `matches[].job.skills` | Array[Str] \| `null` | NÃO | Habilidades associadas à vaga. |
| `matches[].job.salary` | Object \| `null` | NÃO | Objeto com faixa numérica (ex.: `min`, `max`). |
| `matches[].job.currency` | String \| `null` | NÃO | Código da moeda (ex.: `"BRL"`). |
| `matches[].job.job_url` | String \| `null` | NÃO | URL externa da oportunidade. |
| `matches[].job.publication_date` | String \| `null` | NÃO | Data/hora ISO de publicação. |

---

## 6. Rastreabilidade

* **Card #173 (`[F1.6]`):** Define formato e campos obrigatórios conforme contrato implementado entre `sistema-curriculo` e `esw3_cvmatcher`.
* **Card #124 e Card #383 (`[F10.2]`):** Alinhados com [`contrato-busca-vagas.md`](contrato-busca-vagas.md) e [`cliente_vagas_grupo2.py`](../src/backend/infrastructure/integrations/cliente_vagas_grupo2.py).
