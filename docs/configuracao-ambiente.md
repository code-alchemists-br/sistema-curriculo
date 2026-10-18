# Configuração do ambiente de desenvolvimento

## Sumário

* [Instalando o Linux no Windows com o WSL](#instalando-o-linux-no-windows-com-o-wsl)
* [Instalando o Nix](#instalando-o-nix)
* [Instalando o GitHub CLI](#instalando-o-github-cli)
* [Clonando o repositório do projeto](#clonando-o-repositório-do-projeto)
* [Utilizando um ambiente Nix do projeto](#utilizando-um-ambiente-nix-do-projeto)
* [Variáveis de ambiente](#variáveis-de-ambiente)
* [Execução local segura](#execução-local-segura)

**Todos os integrantes do projeto devem utilizar o Nix como ambiente de desenvolvimento**, garantindo a padronização das ferramentas, dependências e versões utilizadas pela equipe.

O Nix deve ser utilizado em um ambiente Linux, seja por meio de uma instalação nativa ou do WSL no Windows. Essa padronização reduz problemas causados por diferenças entre sistemas operacionais, ferramentas instaladas e configurações individuais.

## Instalando o Linux no Windows com o WSL

O **Subsistema do Windows para Linux (WSL)** permite executar uma distribuição Linux diretamente no Windows, incluindo ferramentas de linha de comando e aplicações compatíveis com Linux, sem a necessidade de configurar dual boot ou utilizar uma máquina virtual tradicional.

Para instalar o WSL, abra o **PowerShell como administrador**. Para isso, clique com o botão direito no PowerShell e selecione **Executar como administrador**.

Em seguida, execute:

```powershell
wsl --install
```

Reinicie o computador após a conclusão da instalação.

Esse comando habilita os recursos necessários para executar o WSL e, por padrão, instala uma distribuição Linux compatível, normalmente o Ubuntu.

Na primeira inicialização da distribuição, será necessário aguardar a configuração inicial do sistema e criar um nome de usuário e uma senha para o ambiente Linux.

> **Observação:** O comando `wsl --install` é destinado principalmente à instalação inicial do WSL. Caso o WSL já esteja instalado, podem ser necessários outros comandos para instalar ou configurar distribuições adicionais.

Para mais informações sobre o WSL, consulte a documentação da Microsoft:

[Documentação do WSL](https://learn.microsoft.com/pt-br/windows/wsl/)

## Instalando o Nix

Independentemente de o Linux estar instalado nativamente ou sendo utilizado por meio do WSL, a instalação do Nix deve ser realizada **dentro do ambiente Linux**.

Abra o terminal Linux e execute:

```bash
curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install | sh -s -- --no-daemon
```

Após a instalação, feche e abra novamente o terminal para carregar o ambiente do Nix.

Os ambientes utilizados pelo projeto dependem dos recursos experimentais `nix-command` e `flakes`. Para habilitá-los, crie a pasta de configuração, caso ela ainda não exista:

```bash
mkdir -p ~/.config/nix
```

Em seguida, abra o arquivo de configuração:

```bash
nano ~/.config/nix/nix.conf
```

Adicione a seguinte linha:

```text
experimental-features = nix-command flakes
```

Salve o arquivo utilizando:

```text
Ctrl + O
Enter
Ctrl + X
```

Depois, feche e abra novamente o terminal para garantir que a configuração seja carregada.

Para mais informações sobre o Nix, consulte:

[Documentação do Nix](https://nixos.org/learn/)

## Instalando o GitHub CLI

O **GitHub CLI**, acessado pelo comando `gh`, será utilizado para realizar a autenticação no GitHub e facilitar o acesso ao repositório do projeto.

Com o Nix instalado, execute:

```bash
nix profile install nixpkgs#gh
```

Para autenticar sua conta do GitHub, execute:

```bash
gh auth login
```

Durante o processo, para a maioria dos casos, selecione:

```text
GitHub.com
HTTPS
Login with a web browser
```

O terminal exibirá um código e solicitará a confirmação do login no navegador. Caso a página não seja aberta automaticamente, acesse:

[GitHub Device Login](https://github.com/login/device)

## Clonando o repositório do projeto

Escolha uma pasta para armazenar seus projetos. Por exemplo:

```bash
mkdir -p ~/projetos
cd ~/projetos
```

Em seguida, clone o repositório:

```bash
gh repo clone code-alchemists-br/sistema-curriculo
```

Entre na pasta criada:

```bash
cd sistema-curriculo
```

Para consultar o fluxo de branches, commits, envio ao GitHub e Pull Requests,
veja o [manual de uso do Git](manual-git.md).

O repositório não precisa ser clonado novamente nas próximas utilizações. Basta acessar a pasta onde ele já está armazenado:

```bash
cd ~/projetos/sistema-curriculo
```

## Utilizando um ambiente Nix do projeto

Os ambientes de desenvolvimento estão definidos na pasta `nix` do repositório `sistema-curriculo`.

Dentro da pasta do projeto, execute o ambiente necessário para a tarefa que será realizada.

Por exemplo, para utilizar o ambiente de backend:

```bash
nix develop .#backend
```

Para executar os gates e gerar métricas de qualidade do backend Python, use o
ambiente dedicado:

```bash
nix develop .#quality
```

Ele disponibiliza Ruff, Bandit, Radon, coverage.py, Gitleaks e as ferramentas
do frontend; os testes existentes continuam executados com
`python -m unittest`.

O workflow do GitHub Actions varre o histórico completo do Git com Gitleaks em
pull requests e falha com código de saída `1` quando encontra um segredo. A
saída da varredura é redigida para não repetir o valor detectado. A mesma
verificação pode ser executada localmente com:

```bash
nix develop .#quality --command gitleaks git --redact --no-banner --exit-code 1
```

O comando `nix develop` utiliza a configuração definida no arquivo `flake.nix` e disponibiliza temporariamente as ferramentas e dependências configuradas para o ambiente selecionado.

Por exemplo, caso o ambiente `backend` inclua o `python3`, não é necessário que o Python esteja instalado globalmente no sistema. Enquanto o ambiente Nix estiver ativo, o comando estará disponível.

Para verificar a versão instalada no ambiente:

```bash
python3 --version
```

Para sair do ambiente Nix, execute:

```bash
exit
```

Ao sair, as ferramentas disponibilizadas exclusivamente pelo ambiente deixam de estar disponíveis no terminal atual.

## Variáveis de ambiente

O projeto lê as variáveis abaixo. Defina-as somente quando o fluxo usado
precisar delas; os exemplos locais não devem ser reutilizados em produção.

| Variável | Componente | Obrigatória | Comportamento |
|---|---|---|---|
| `LOG_LEVEL` | Backend | Não | Nível de log. Padrão `INFO`; aceita `DEBUG`, `INFO`, `WARNING`, `ERROR` ou `CRITICAL`. |
| `LOG_ACTOR_HMAC_KEY` | Backend | Não | Chave de pelo menos 32 bytes para gerar referências estáveis de atores nos logs. Sem ela, o processo usa uma chave aleatória temporária. |
| `DATABASE_URL` | Backend e Alembic | Não para iniciar a API; sim para executar migrations | URL de um PostgreSQL local. Sem ela, `/ready` retorna HTTP 503. |
| `VITE_API_URL` | Frontend | Sim para chamadas à API | URL base pública da API, por exemplo `http://127.0.0.1:8000`. O Vite disponibiliza variáveis `VITE_*` no código do navegador; nunca coloque senhas, tokens ou outras credenciais nelas. |

Credenciais de banco devem usar uma conta local de desenvolvimento com acesso
somente ao banco de desenvolvimento. Se a senha contiver caracteres especiais
em uma URL, faça o percent-encoding desses caracteres. Não use credenciais de
produção nem inclua URLs com senha em arquivos versionados, mensagens de log ou
capturas de tela.

## Execução local segura

Execute backend e frontend em terminais separados. Os exemplos vinculam os
servidores somente à própria máquina (`127.0.0.1`), usam a configuração de
desenvolvimento e não ativam o modo de depuração do servidor. Mantenha o nível de
log padrão `INFO`, a menos que precise diagnosticar um problema.

No primeiro terminal, a partir da raiz do repositório:

```bash
nix develop .#backend
export PYTHONPATH=src
export LOG_LEVEL=INFO
export LOG_ACTOR_HMAC_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
# Evita reutilizar por acidente uma URL de banco herdada do ambiente.
unset DATABASE_URL
# Opcional, somente se houver um PostgreSQL local de desenvolvimento:
# export DATABASE_URL='postgresql+psycopg://curriculo_dev:senha-local@127.0.0.1:5432/curriculo_dev'
# Opcional, depois de configurar a URL local e antes de iniciar a API:
# alembic upgrade head
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

A URL de banco no exemplo é fictícia. Substitua-a somente se houver um
PostgreSQL local configurado; a API pode iniciar sem banco, mas `/ready` ficará
indisponível. Para aplicar migrations, configure deliberadamente a URL do banco
local, retire o `#` da linha `alembic upgrade head` e execute-a antes de iniciar
a API.

No segundo terminal, também a partir da raiz do repositório:

```bash
nix develop .#frontend
cd src/frontend
export VITE_API_URL=http://127.0.0.1:8000
npm ci
npm run dev -- --host 127.0.0.1
```

Abra no navegador o endereço local informado pelo Vite. Não use `--host 0.0.0.0`
em uma execução local comum, pois isso pode expor o servidor a outros
dispositivos da rede. O `npm ci` instala as dependências listadas no lockfile
em `src/frontend/node_modules`.

Ao encerrar o backend, use `Ctrl + C`. As variáveis exportadas ficam somente nos
terminais em que foram definidas; ao fechar esses terminais, defina-as novamente
na próxima execução. Não execute migrations contra bancos compartilhados ou de
produção sem o procedimento e a autorização da equipe responsável.

## Nível de logging do backend

O backend lê a variável de ambiente `LOG_LEVEL` durante a inicialização para
definir o nível mínimo enviado ao logging padrão do Python. Se a variável não
estiver definida, o valor utilizado será `INFO`. Os valores são aceitos sem
diferenciação entre maiúsculas e minúsculas e com espaços externos ignorados.

Valores permitidos:

| Valor | Uso |
|---|---|
| `DEBUG` | Diagnóstico detalhado para desenvolvimento. |
| `INFO` | Eventos normais de execução; nível padrão. |
| `WARNING` | Situações inesperadas que não interrompem o fluxo. |
| `ERROR` | Falhas que impedem uma operação. |
| `CRITICAL` | Falhas graves que podem comprometer a aplicação. |

Exemplo para iniciar o backend com logs de diagnóstico:

```bash
PYTHONPATH=src LOG_LEVEL=DEBUG uvicorn backend.main:app
```

Um valor fora da lista interrompe a inicialização com uma mensagem que informa
as opções aceitas.

### Mascaramento e retenção

O backend mascara e-mails, CPFs, telefones e valores associados a campos como
`nome`, `endereco`, `ator_id`, `senha`, `token`, cookies, IDs de usuário e
credenciais de acesso. A sanitização é instalada nos handlers existentes,
incluindo os handlers nomeados do servidor ASGI. Negações de autorização
registram `ator_referencia`, um HMAC do identificador original, para permitir
auditoria sem expor o ID da conta. Configure `LOG_ACTOR_HMAC_KEY` como segredo
compartilhado com ao menos 32 bytes entre as instâncias para manter referências
estáveis entre processos e reinicializações. Se a variável faltar, cada
processo usa uma chave aleatória temporária e as referências não serão
correlacionáveis após reinício.

A aplicação emite logs para a saída padrão; portanto, a retenção deve ser aplicada pelo
coletor configurado no ambiente de implantação. O prazo operacional definido
para logs de aplicação e segurança é de **30 dias**, seguido de exclusão também
das cópias temporárias controladas pelo coletor. A implantação deve configurar
esse prazo no destino de logs; o backend não mantém arquivos locais de log.

Logs devem conter apenas os campos necessários à operação ou auditoria. A
mascaração é uma defesa adicional e não autoriza incluir dados pessoais,
credenciais ou corpos de requisição em mensagens de log.

## Health check

A API expõe `GET /health` sem autenticação. A resposta contém somente
`{"status":"ok"}` quando todos os verificadores injetados concluem com sucesso,
ou `{"status":"indisponivel"}` com HTTP 503 quando algum falha, lança exceção ou
ultrapassa dois segundos. A resposta não informa nomes, endereços ou mensagens
de erro das dependências. A composição atual não possui probes externos
configurados; nesse caso, o endpoint confirma apenas que a API está ativa.

## Readiness da persistência

A API expõe `GET /ready` sem autenticação. A rota retorna `{"status":"ok"}`
somente quando o banco configurado responde a uma consulta assíncrona `SELECT 1`.
Configure `DATABASE_URL` com uma URL PostgreSQL compatível com SQLAlchemy e
Psycopg, preferencialmente no formato `postgresql+psycopg://...`; URLs
`postgresql://...` são convertidas para esse driver na composição.
Se o verificador estiver ausente, retornar falso, lançar exceção ou exceder dois
segundos, a resposta será HTTP 503 com `{"status":"indisponivel"}`. A resposta
não inclui URL, credenciais, nome do banco ou mensagem da exceção. Como a
URL é opcional para desenvolvimento local, sua ausência mantém `/ready` em 503.
O pool assíncrono é liberado no encerramento da aplicação.
