# Guia de Configuração de Ambientes e Execução Local com Docker

- **Referência:** Task `[F12.4] #422` (Documentar configuração de ambientes, variáveis necessárias e procedimento seguro de execução local)
- **Documentador Oficial:** Marcelo Aparecido da Rosa ([@marcelo-3com](https://github.com/marcelo-3com))
- **Líder Técnico e QA Arquitetural:** Rodolpho P. M. Ferreira
- **Responsável CI&CD e Ambientes:** Kelly Daiane Miranda Mendes
- **Versão:** 1.0.0
- **Data:** Outubro de 2026

---

## 1. Visão Geral da Arquitetura com Docker

Conforme diretriz do líder técnico (**Rodolpho**), o **Sistema Currículo (Grupo 1)** adota **conteinerização total com Docker** para garantir:
1. **Paridade entre Ambientes:** Garantir que o sistema rode de forma idêntica na máquina de qualquer estudante, na máquina dos professores avaliadores e na esteira de CI/CD.
2. **Zero Poluição do Sistema Operacional Host:** O desenvolvedor não precisa instalar servidores de banco de dados ou ferramentas de infraestrutura diretamente no Windows/Linux; tudo roda isolado em contêineres.
3. **Isolamento de Segurança:** Serviços rodam em rede virtual interna do Docker (`bridge`), expondo apenas as portas estritamente necessárias.

---

## 2. Pré-requisitos da Máquina Local

Antes de inicializar o ambiente, o desenvolvedor ou avaliador deve ter instalado:
* **Docker Engine & Docker Compose:** Versão 24.0+ / Docker Compose v2.20+ (ou [Docker Desktop](https://www.docker.com/products/docker-desktop/) no Windows/macOS com suporte a WSL2 ativo).
* **Git:** Para clonagem e versionamento do repositório.
* **Navegador Web / Insomnia / Postman / cURL:** Para testes funcionais e consumo dos endpoints.

---

## 3. Dicionário de Variáveis de Ambiente (`.env`)

O projeto utiliza um arquivo `.env` na raiz para parametrizar a aplicação. O template padrão é versionado no repositório como [`.env.example`](file:///.env.example).

### 3.1. Variáveis da Aplicação (*Core App*)

| Variável | Tipo | Obrigatória? | Valor Padrão para Dev | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `NODE_ENV` / `APP_ENV` | String | **SIM** | `development` | Define o ambiente de execução (`development`, `test`, `production`). |
| `APP_PORT` | Integer | **SIM** | `3000` | Porta local mapeada no host para acesso web e API. |
| `LOG_LEVEL` | String | NÃO | `debug` | Nível de detalhamento dos logs (`debug`, `info`, `warn`, `error`). |

### 3.2. Variáveis de Conexão com o Banco de Dados Local

| Variável | Tipo | Obrigatória? | Valor Padrão para Dev | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `DB_HOST` | String | **SIM** | `db` | Host do banco (no Docker Compose, o nome do serviço é `db`). |
| `DB_PORT` | Integer | **SIM** | `5432` | Porta interna do banco de dados relacional (ex: PostgreSQL). |
| `DB_NAME` | String | **SIM** | `sistema_curriculo_dev` | Nome da base de dados da aplicação. |
| `DB_USER` | String | **SIM** | `curriculo_app_user` | Usuário da aplicação com permissão de leitura/escrita. |
| `DB_PASSWORD` | String | **SIM** | `dev_secret_password_local` | Senha segura de desenvolvimento (apenas para ambiente local). |

### 3.3. Integração com a API do Grupo 2 (`CV Matcher`)

| Variável | Tipo | Obrigatória? | Valor Padrão para Dev | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `GRUPO2_API_URL` | String | **SIM** | `http://host.docker.internal:8000` | URL base do serviço de recomendação de vagas do Grupo 2. |
| `GRUPO2_API_TIMEOUT_MS`| Integer | NÃO | `5000` | Tempo limite em milissegundos para resposta do Grupo 2. |
| `GRUPO2_DEFAULT_LIMIT` | Integer | NÃO | `10` | Quantidade padrão de vagas a solicitar (regra de 1 a 100). |

### 3.4. Segurança e Sessão (Middleware da Kelly Mendes)

| Variável | Tipo | Obrigatória? | Valor Padrão para Dev | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `JWT_SECRET` | String | **SIM** | `dev_local_jwt_secret_token_12345` | Segredo para assinatura de tokens de autenticação. |
| `SESSION_TTL_HOURS` | Integer | NÃO | `24` | Tempo de vida da sessão do estudante. |

---

## 4. Procedimento Seguro de Execução Local (Passo a Passo)

### Passo 1: Obter o Código
```bash
git clone https://github.com/code-alchemists-br/sistema-curriculo.git
cd sistema-curriculo
```

### Passo 2: Criar o Arquivo de Configuração Local
Copie o template de exemplo para criar seu arquivo `.env` local:
* **No Windows (PowerShell / Prompt):**
  ```powershell
  copy .env.example .env
  ```
* **No Linux / macOS / WSL:**
  ```bash
  cp .env.example .env
  ```

> ⚠️ **Atenção:** Nunca altere ou comite o arquivo `.env` para o Git. Ele contém credenciais e é automaticamente ignorado pelo `.gitignore`.

### Passo 3: Inicializar os Contêineres com Docker Compose
Para compilar e subir todos os serviços em segundo plano:
```bash
docker compose up -d --build
```

### Passo 4: Verificar a Saúde dos Serviços (*Healthcheck*)
Aguarde alguns segundos e confira o status dos contêineres:
```bash
docker compose ps
```
Você deverá ver os serviços `app` e `db` com o status `healthy` ou `running (Up)`.

Para testar a resposta do servidor localmente pelo terminal:
```bash
curl http://localhost:3000/health
```
Resposta esperada:
```json
{
  "status": "UP",
  "banco_de_dados": "conectado",
  "versao": "1.0.0"
}
```

---

## 5. Diretrizes de Segurança para o Time (*Security Guidelines*)

Conforme exigido pelo QA Arquitetural e pelas boas práticas de Engenharia de Software:

1. **Proteção de Segredos no Git:**
   * O arquivo `.env` **JAMAIS** deve ser comitado.
   * Apenas o arquivo `.env.example` com valores falsos/mockados pode ser versionado.
   * Se alguma credencial real for comitada acidentalmente, a chave deve ser imediatamente revogada e o commit reescrito.

2. **Princípio do Menor Privilégio (*Least Privilege*):**
   * O contêiner da aplicação Docker não deve executar como usuário `root`.
   * Deve ser utilizado um usuário de sistema não privilegiado (ex: `USER node` ou `USER appuser`) no `Dockerfile`.

3. **Isolamento de Portas:**
   * A porta do banco de dados (`5432`) não deve ser exposta publicamente na internet. Apenas o contêiner da aplicação tem acesso direto a ela através da rede interna do Docker Compose.

4. **Sanitização de Logs:**
   * Dados sensíveis de estudantes (senhas, tokens e dados cadastrais pessoais) **não devem** ser registrados nos logs da aplicação em nenhuma hipótese.

---

## 6. Comandos Úteis do Dia a Dia

| Ação | Comando Docker |
| :--- | :--- |
| **Ver logs em tempo real** | `docker compose logs -f app` |
| **Reiniciar a aplicação** | `docker compose restart app` |
| **Parar todos os contêineres** | `docker compose stop` |
| **Derrubar e remover contêineres e redes** | `docker compose down` |
| **Limpeza total (incluindo dados do banco)** | `docker compose down -v` |
| **Entrar no terminal do contêiner da aplicação**| `docker compose exec app sh` |
