# Contratos de Perfil, Formação Acadêmica e Experiência Profissional

## Objetivo

Este documento consolida os contratos HTTP atualmente implementados para:

- consulta, atualização e exclusão do perfil do estudante;
- cadastro, edição e exclusão de formações acadêmicas;
- cadastro, edição e exclusão de experiências profissionais.

Os contratos refletem o comportamento atual das rotas e não antecipam
funcionalidades ainda não expostas pela API.

## Regras gerais

As operações documentadas neste arquivo são protegidas por autenticação.

A identidade do proprietário deve vir da sessão autenticada, disponibilizada
internamente em `request.state.usuario_id`.

O cliente não deve poder escolher o proprietário de uma formação ou experiência
por meio do corpo da requisição.

Quando uma operação exigir um identificador de recurso, esse identificador pode
vir da rota, mas a propriedade deve continuar sendo validada em relação à
identidade autenticada.

Recurso ausente e recurso pertencente a outro estudante devem ser tratados de
forma que não haja exposição indevida de dados.

---

# Perfil do estudante

## Consultar perfil

### Endpoint

`GET /estudantes/{usuario_id}`

### Autenticação

Obrigatória.

O `usuario_id` da rota deve corresponder ao usuário autenticado.

Quando o identificador solicitado pertencer a outro estudante, a API responde
como perfil não encontrado.

### Resposta de sucesso

Status:

`200 OK`

Campos:

| Campo | Tipo |
|---|---|
| `nome` | string |
| `email` | string |
| `telefones` | lista de strings |
| `cidade` | string ou null |
| `linkedin` | string ou null |
| `curriculo_lattes` | string ou null |

O contrato de consulta não expõe:

- hash de senha;
- `deleted_at`;
- detalhes internos de persistência.

### Erros relevantes

| Status | Situação |
|---|---|
| `401` | sessão ausente ou inválida |
| `404` | perfil inexistente, excluído ou pertencente a outro usuário |
| `503` | serviço de consulta não configurado |

---

## Atualizar perfil completo

### Endpoint

`PUT /estudantes/me/perfil`

### Autenticação

Obrigatória.

O proprietário é obtido exclusivamente da sessão autenticada.

O endpoint não recebe `usuario_id` no corpo ou na rota.

### Corpo da requisição

```json
{
  "nome": "Maria da Silva",
  "email": "maria@example.com",
  "endereco": "Rua Exemplo, 100",
  "cidade": "São Paulo",
  "telefones": ["11999999999"],
  "linkedin": "https://linkedin.com/in/exemplo",
  "curriculo_lattes": "https://lattes.cnpq.br/exemplo"
}
```

### Regras principais

- `nome` é obrigatório;
- `email` é obrigatório;
- `endereco` é obrigatório;
- `cidade` é obrigatória;
- deve existir ao menos um telefone;
- são aceitos no máximo cinco telefones;
- LinkedIn é opcional;
- Currículo Lattes é opcional;
- ausência dos campos opcionais no PUT representa substituição pelo valor nulo.

### Resposta de sucesso

Status:

`200 OK`

Campos:

| Campo | Tipo |
|---|---|
| `id` | UUID |
| `nome` | string |
| `email` | string |
| `endereco` | string |
| `cidade` | string ou null |
| `telefones` | lista de strings |
| `linkedin` | string ou null |
| `curriculo_lattes` | string ou null |

### Erros relevantes

| Status | Situação |
|---|---|
| `401` | sessão ausente ou inválida |
| `404` | perfil não encontrado |
| `409` | perfil excluído ou e-mail já utilizado |
| `422` | dados violam regras do domínio |
| `503` | serviço de atualização indisponível |

---

## Editar nome e e-mail do perfil

### Endpoint

`PUT /estudantes/{usuario_id}`

### Corpo

```json
{
  "nome": "Maria da Silva",
  "email": "maria@example.com"
}
```

### Autorização

O UUID da rota deve corresponder à identidade autenticada.

### Resposta de sucesso

Status:

`200 OK`

```json
{
  "id": "uuid-do-estudante",
  "nome": "Maria da Silva",
  "email": "maria@example.com"
}
```

### Erros relevantes

| Status | Situação |
|---|---|
| `401` | autenticação ausente |
| `403` | tentativa de alterar perfil de outro estudante |
| `404` | perfil inexistente |
| `409` | perfil excluído ou e-mail já cadastrado |
| `422` | dados inválidos |
| `503` | serviço de edição indisponível |

---

## Excluir perfil

### Endpoint

`DELETE /estudantes/atual`

### Autenticação e propriedade

A operação utiliza exclusivamente a identidade da sessão.

Nenhum identificador de usuário é aceito no corpo ou na URL para selecionar o
perfil a excluir.

### Resultado

Status:

`204 No Content`

A exclusão é lógica.

O perfil passa a ser tratado como excluído e o cookie da sessão é removido da
resposta.

A repetição da exclusão não deve substituir o primeiro instante de exclusão.

### Erros relevantes

| Status | Situação |
|---|---|
| `401` | sessão ausente ou inválida |
| `404` | perfil não encontrado |
| `503` | serviço de exclusão indisponível |

---

# Formação acadêmica

## Vocabulário de nível

O campo `nivel` aceita os valores:

- `ensino_fundamental`;
- `ensino_medio`;
- `tecnico`;
- `tecnologo`;
- `graduacao`;
- `especializacao`;
- `mestrado`;
- `doutorado`.

## Vocabulário de status

O campo `status` aceita:

- `em_andamento`;
- `concluido`;
- `interrompido`.

---

## Cadastrar formação acadêmica

### Endpoint

`POST /formacoes-academicas`

### Autenticação

Obrigatória.

O proprietário da formação é obtido da sessão e não é enviado pelo cliente.

### Corpo

```json
{
  "instituicao": "FATEC São Paulo",
  "curso": "Análise e Desenvolvimento de Sistemas",
  "nivel": "tecnologo",
  "data_inicio": "2025-02-01",
  "data_fim": null,
  "status": "em_andamento"
}
```

### Regras principais

- `instituicao` e `curso` são obrigatórios;
- os textos são normalizados removendo espaços externos;
- caracteres de controle são rejeitados;
- instituição e curso devem possuir entre 1 e 200 caracteres após normalização;
- `data_inicio` é obrigatória;
- `data_fim` pode ser nula;
- formação com status `concluido` exige data final;
- as datas devem formar um período válido.

Quando `status` for `em_andamento`, `data_fim` pode representar uma previsão de
conclusão.

Nos demais status, quando informada, representa a data efetiva de conclusão ou
interrupção.

### Resposta

Status:

`201 Created`

Campos:

| Campo | Tipo |
|---|---|
| `id` | UUID |
| `usuario_id` | UUID |
| `instituicao` | string |
| `curso` | string |
| `nivel` | enum |
| `data_inicio` | date |
| `data_fim` | date ou null |
| `status` | enum |

### Erros relevantes

| Status | Situação |
|---|---|
| `401` | sessão ausente |
| `422` | formação viola regras de cadastro |
| `503` | serviço de cadastro indisponível |

---

## Editar formação acadêmica

### Endpoint

`PUT /formacoes-academicas/{formacao_id}`

O endpoint realiza substituição dos campos editáveis da formação.

### Corpo

Usa os mesmos campos do cadastro.

Em edição, `data_fim` deve estar explicitamente presente, embora possa receber
`null`.

Exemplo:

```json
{
  "instituicao": "FATEC São Paulo",
  "curso": "Análise e Desenvolvimento de Sistemas",
  "nivel": "tecnologo",
  "data_inicio": "2025-02-01",
  "data_fim": "2027-12-01",
  "status": "em_andamento"
}
```

### Autorização

A formação só pode ser alterada pelo seu proprietário autenticado.

O proprietário não pode ser alterado pela requisição.

### Resposta

Status:

`200 OK`

A resposta utiliza o mesmo contrato de `FormacaoAcademicaResposta` do cadastro.

### Erros relevantes

| Status | Situação |
|---|---|
| `401` | sessão ausente |
| `404` | formação inexistente, excluída ou pertencente a outro usuário |
| `422` | dados violam regras de edição |
| `503` | serviço de edição indisponível |

---

## Excluir formação acadêmica

### Endpoint

`DELETE /formacoes-academicas/{formacao_id}`

### Resultado

Status:

`204 No Content`

A exclusão é lógica.

O estudante só pode excluir uma formação própria.

Uma repetição da exclusão da própria formação é tratada de forma idempotente.

### Erros relevantes

| Status | Situação |
|---|---|
| `401` | sessão ausente |
| `404` | formação inexistente ou pertencente a outro estudante |
| `503` | serviço de exclusão indisponível |

---

# Experiência profissional

## Cadastrar experiência profissional

### Endpoint

`POST /experiencias-profissionais`

### Autenticação

Obrigatória.

O proprietário é obtido exclusivamente da sessão autenticada.

### Corpo

```json
{
  "empresa": "Empresa Exemplo",
  "cargo": "Desenvolvedor",
  "descricao": "Desenvolvimento e manutenção de aplicações.",
  "data_inicio": "2025-01-01",
  "data_fim": null
}
```

### Regras principais

- `empresa` deve estar preenchida;
- `cargo` deve estar preenchido;
- `descricao` deve estar preenchida;
- `data_inicio` é obrigatória;
- `data_fim` pode ser nula;
- `data_fim = null` representa experiência em andamento;
- o período deve ser cronologicamente válido.

### Resposta

Status:

`201 Created`

Campos:

| Campo | Tipo |
|---|---|
| `id` | UUID |
| `usuario_id` | UUID |
| `empresa` | string |
| `cargo` | string |
| `descricao` | string |
| `data_inicio` | date |
| `data_fim` | date ou null |

### Erros relevantes

| Status | Situação |
|---|---|
| `401` | sessão ausente |
| `422` | experiência viola regras do domínio |
| `503` | serviço de cadastro indisponível |

---

## Editar experiência profissional

### Endpoint

`PUT /experiencias-profissionais/{experiencia_id}`

A edição substitui o conjunto de campos editáveis da experiência.

### Corpo

```json
{
  "empresa": "Empresa Exemplo",
  "cargo": "Desenvolvedor Pleno",
  "descricao": "Desenvolvimento e manutenção de sistemas.",
  "data_inicio": "2025-01-01",
  "data_fim": null
}
```

Na edição, `data_fim` deve ser enviado explicitamente, podendo receber `null`
para indicar experiência em andamento.

### Autorização

Somente o proprietário autenticado pode editar a experiência.

### Resposta

Status:

`200 OK`

Usa o mesmo contrato público de resposta do cadastro.

### Erros relevantes

| Status | Situação |
|---|---|
| `401` | sessão ausente |
| `404` | experiência inexistente, excluída ou pertencente a outro usuário |
| `422` | experiência viola regras de edição |
| `503` | serviço de edição indisponível |

---

## Excluir experiência profissional

### Endpoint

`DELETE /experiencias-profissionais/{experiencia_id}`

### Resultado

Status:

`204 No Content`

A exclusão é lógica.

A operação é limitada ao proprietário autenticado.

Repetir a exclusão da própria experiência já excluída é tratado como sucesso
idempotente.

### Erros relevantes

| Status | Situação |
|---|---|
| `401` | sessão ausente |
| `404` | experiência inexistente ou pertencente a outro usuário |
| `503` | serviço de exclusão indisponível |

---

# Regras de propriedade e segurança

Os três conjuntos de rotas seguem as mesmas regras fundamentais:

1. a identidade do usuário deve vir da sessão autenticada;
2. o cliente não pode escolher outro proprietário no payload;
3. IDs de recurso não concedem autorização por si só;
4. operações de formação e experiência combinam ID do recurso com a identidade
   autenticada;
5. dados de outro estudante não devem ser expostos;
6. recursos logicamente excluídos não devem ser tratados como recursos ativos;
7. autenticação e autorização devem ser verificadas no backend.

O contrato de sessão utilizado por essas operações está descrito em
[contrato-credenciais-sessao.md](contrato-credenciais-sessao.md).

# Operações ainda não documentadas como existentes

Este documento descreve somente endpoints presentes atualmente na API.

Não são declarados aqui como implementados:

- endpoint próprio de listagem/consulta de formações acadêmicas;
- endpoint próprio de listagem/consulta de experiências profissionais;
- restauração de formação excluída;
- restauração de experiência excluída;
- purga física dos registros excluídos logicamente.

Essas operações somente devem ser acrescentadas ao contrato quando existirem
rotas correspondentes aprovadas.

# Relação com requisitos funcionais

Os contratos detalham especialmente:

- RF01 — cadastro de dados pessoais, formação e experiências;
- RF02 — consulta, edição e exclusão das informações cadastradas;
- RF03 — centralização das informações do estudante;
- RF13 — exigência de autenticação para informações pessoais.

# Rastreabilidade

- **Issue:** #423 — F12.5
- **WBS:** 1.1.2.4, 1.8.2.1–1.8.2.4
- **Fontes de implementação:** rotas atuais de perfil, formação acadêmica e
  experiência profissional.
