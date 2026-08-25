# Configuração do ambiente de desenvolvimento

## Sumário

* [Instalando o Linux no Windows com o WSL](#instalando-o-linux-no-windows-com-o-wsl)
* [Instalando o Nix](#instalando-o-nix)
* [Instalando o GitHub CLI](#instalando-o-github-cli)
* [Clonando o repositório do projeto](#clonando-o-repositório-do-projeto)
* [Utilizando um ambiente Nix do projeto](#utilizando-um-ambiente-nix-do-projeto)

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
