# Currículo guiado por IA (branch `teste-IA`)

Experimento. A IA **não gera o currículo**. Ela faz duas coisas:

1. **Revisa os textos** que o estudante escreve no formulário, um campo por vez.
2. **Recomenda o modelo** de currículo que combina com o perfil salvo.

O currículo continua sendo montado pelo fluxo normal do sistema. A IA está
integrada ao frontend existente em três lugares:

- **Experiências** (`?etapa=experiencias-profissionais`): botão "Revisar com IA"
  abaixo da descrição de cada experiência.
- **Projetos** (`?etapa=projetos-academicos`): o mesmo botão abaixo da descrição
  de cada projeto.
- **Seleção de modelo** (`?etapa=selecionar-modelo`): botão "Recomendar modelo
  com IA", que marca o modelo recomendado no seletor.

Se a IA marcar uma descrição como inválida, o formulário não salva até o texto
ser reescrito (ou um modelo sugerido ser completado) e revisado de novo. Sem IA
ou sem login, os formulários funcionam como antes.

A feature fica em `src/frontend/features/assistente-ia`. Os formulários só
ganharam um espaço opcional abaixo da descrição, e as páginas encaixam o painel
da IA nesse espaço.

## Endpoints

Os dois exigem a sessão de `POST /acessos`.

- **`POST /assistente/revisoes`**
  - Recebe `campo`, `texto`, `pergunta` (opcional) e `contexto` (opcional).
  - Devolve `situacao` (`valido`, `melhorado` ou `invalido`), `motivo`, 3
    `sugestoes` e `pode_manter_texto`.
  - Se o texto for inválido, as sugestões são modelos com [colchetes] e
    `pode_manter_texto` vem `false`.
  - Não grava nada.
- **`POST /assistente/recomendacao-modelo`**
  - Recebe `extras`, uma lista de pares pergunta e resposta, por exemplo a
    carreira desejada e o objetivo.
  - Devolve `modelo`, `motivo` e `alternativa`, todos entre os modelos de
    `ModeloCurriculo`.
  - Lê só o conteúdo profissional salvo. Nome, e-mail, telefone, endereço e
    links não são enviados ao Gemini.

## Rodar localmente

Sem `DATABASE_URL`, a API usa um SQLite em memória, e os dados se perdem ao
fechar.

```bash
pip install -r src/backend/requirements-teste-ia.txt
```

Variáveis de ambiente:

| Variável | Valor |
| --- | --- |
| `GEMINI_API_KEY` | A sua chave do Gemini. |
| `GEMINI_MODEL` | Opcional. O padrão é `gemini-3.5-flash-lite`. |
| `SESSION_COOKIE_SECURE` | `false`, para o login funcionar em `http://`. |

Para subir a API, rode de dentro de `src`:

```bash
..\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

Para subir o frontend, rode de dentro de `src/frontend`, com
`VITE_API_URL=http://localhost:8000`:

```bash
npm.cmd run dev
```

## PostgreSQL persistente no Windows (sem Nix)

Equivale ao roteiro de `docs/teste-e2e-postgresql.md`, usando o PostgreSQL 17
instalado em `C:\Program Files\PostgreSQL\17`. O cluster fica em
`C:\Users\<usuário>\sistema-curriculo-e2e`, separado do serviço do PostgreSQL,
sem senha (`trust`) e aceitando conexões só de `127.0.0.1:54329`. O banco é
`sistema_curriculo_e2e`.

Para iniciar o cluster depois de reiniciar o computador:

```bash
& "C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe" -D "$env:USERPROFILE\sistema-curriculo-e2e\dados" -l "$env:USERPROFILE\sistema-curriculo-e2e\postgres.log" -o "-p 54329 -c listen_addresses=127.0.0.1" start
```

Para parar o cluster:

```bash
& "C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe" -D "$env:USERPROFILE\sistema-curriculo-e2e\dados" stop
```

Para aplicar as migrations novas, rode da raiz do repositório:

```bash
$env:DATABASE_URL="postgresql+psycopg://postgres@127.0.0.1:54329/sistema_curriculo_e2e"; $env:PYTHONPATH="src"; .\.venv\Scripts\python.exe -m alembic upgrade head
```

Para subir a API ligada ao banco, defina a variável e rode de dentro de `src`:

```bash
$env:DATABASE_URL="postgresql+psycopg://postgres@127.0.0.1:54329/sistema_curriculo_e2e"
```

```bash
..\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

No Windows, mantenha o `--reload`. Sem ele, o uvicorn usa um laço de eventos
com o qual o psycopg assíncrono não funciona, e a API não consegue falar com o
banco.

A sessão de login dura 60 minutos.

## Currículo salvo no banco

O frontend lê e grava o currículo inteiro pelo banco, sem duplicar itens:

| Rota | O que faz |
|---|---|
| `GET /estudantes/me/curriculo` | Devolve tudo o que o estudante logado salvou (dados pessoais, formações, experiências, projetos, competências, idiomas, cursos, certificações e modelo). |
| `PUT /estudantes/me/curriculo/{secao}` | Troca a seção inteira pela lista enviada em `itens` (`formacoes`, `experiencias`, `projetos`, `competencias`, `idiomas`, `cursos`, `certificacoes`). Em `formacoes`, aceita também `curriculo_lattes`. |
| `PUT /estudantes/me/curriculo/modelo` | Guarda o modelo visual escolhido. |

Dados pessoais continuam em `PUT /estudantes/me/perfil`.

- Ao entrar (ou abrir o sistema já logado), o currículo é carregado do banco.
- Cada etapa só avança depois de salvar. Se a API falhar, a etapa mostra o motivo e mantém o que foi digitado.
- Não existe mais "modo demonstração" no login quando a API está fora do ar.
