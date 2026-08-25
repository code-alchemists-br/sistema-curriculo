# Configuração do ambiente de desenvolvimento

- [Instalando o Linux no Windows com o WSL](#instalando-o-linux-no-windows-com-o-wsl)
- [Instalando o Nix](#instalando-o-nix)
- [Instalando o GitHub CLI](#instalando-o-github-cli)
- [Clonando o repositório do projeto](#clonando-o-repositório-do-projeto)
- [Utilizando um ambiente Nix do projeto](#utilizando-um-ambiente-nix-do-projeto)

**Todos os integrantes do projeto devem utilizar o Nix como ambiente de desenvolvimento**, garantindo que as ferramentas, dependências e versões utilizadas sejam padronizadas para toda a equipe.

O Nix deve ser utilizado em um ambiente Linux, seja por meio de uma instalação nativa ou através do WSL no Windows. Essa padronização reduz problemas relacionados a diferenças entre sistemas operacionais e configurações individuais.

## Instalando o Linux no Windows com o WSL

O Subsistema do Windows para Linux (WSL) permite que os desenvolvedores instalem uma distribuição do Linux (como Ubuntu, OpenSUSE, Kali, Debian, Arch Linux etc) e usem aplicativos Linux, utilitários e ferramentas de linha de comando bash diretamente no Windows, sem modificação, sem a sobrecarga de uma máquina virtual tradicional ou configuração dualboot.

Abra o PowerShell no modo de administrador clicando com o botão direito do mouse e selecionando "Executar como administrador", insira o comando `wsl --install` e reinicie o computador.

```powershell
wsl --install
```

Esse comando habilitará os recursos necessários para executar o WSL e instalar a distribuição do Ubuntu do Linux.

Na primeira vez que você iniciar uma distribuição do Linux recém-instalada, uma janela do console será aberta e você será solicitado a aguardar que os arquivos sejam descompactados e armazenados em seu computador. Todos os lançamentos futuros devem levar menos de um segundo.

**Observação:** O comando acima só funcionará se o WSL não estiver instalado.

Para mais informações sobre o WSL: https://learn.microsoft.com/pt-br/windows/wsl/

## Instalando o Nix

Independentemente de utilizar o Linux instalado nativamente ou através do WSL no Windows, a instalação do Nix deve ser realizada dentro do ambiente Linux.

Para iniciar a instalação, abra o terminal do Linux e digite o seguinte comando:

```bash
curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install | sh -s -- --no-daemoncurl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install | sh -s -- --no-daemon
```

Os comandos utilizados pelo projeto dependem dos recursos experimentais `nix-command` e `flakes`.

Crie a pasta de configuração, caso ela ainda não exista:

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

Feche e abra novamente o terminal ou recarregue o ambiente do Nix.

Para mais informações sobre o Nix: https://nixos.org/learn/

## Instalando o GitHub CLI

O GitHub CLI, identificado pelo comando `gh`, será utilizado para realizar a autenticação no GitHub e facilitar o acesso ao repositório.

Com o Nix instalado, execute:

```bash
nix profile install nixpkgs#gh
```

Para fazer login no GitHub, execute:

```bash
gh auth login
```

Durante o processo, selecione as opções adequadas para sua conta. Para a maioria dos casos:

```text
GitHub.com
HTTPS
Login with a web browser
```

O terminal fornecerá um código e solicitará a confirmação do login pelo navegador. Caso a página não seja aberta, acesse o seguinte link no navegador:

```text
https://github.com/login/device
```

## Clonando o repositório do projeto

Escolha uma pasta para armazenar seus projetos, por exemplo:

```bash
mkdir -p ~/projetos
cd ~/projetos
```

Depois, clone o repositório utilizando:

```bash
gh repo clone code-alchemists-br/sistema-curriculo
```

Entre na pasta criada:

```bash
cd sistema-curriculo
```

O repositório não precisa ser clonado novamente nas próximas vezes. Basta acessar a pasta onde ele já está armazenado.

## Utilizando um ambiente Nix do projeto

Os ambientes encontram-se na pasta **nix** de **sistema-curriculo**.

Dentro da pasta do repositório, execute o ambiente necessário para a tarefa.

Por exemplo, para utilizar o ambiente de backend:

```bash
nix develop .#backend
```

O comando `nix develop` lê o arquivo `flake.nix` do projeto e disponibiliza temporariamente as ferramentas definidas para aquele ambiente.

Por exemplo, caso o ambiente `backend` inclua python3, mesmo que o Python não esteja instalado globalmente no sistema, ele poderá ser utilizado enquanto o ambiente Nix estiver ativo. Você pode conferir usando o seguinte comando:

```bash
python3 --version
```

Para sair do ambiente:

```bash
exit
```
