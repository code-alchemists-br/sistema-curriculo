# Configuração do ambiente de desenvolvimento

Todos os integrantes do projeto devem utilizar o Nix como ambiente de desenvolvimento, garantindo que as ferramentas, dependências e versões utilizadas sejam padronizadas para toda a equipe.

O Nix deve ser utilizado em um ambiente Linux, seja por meio de uma instalação nativa ou através do WSL no Windows. Essa padronização reduz problemas relacionados a diferenças entre sistemas operacionais e configurações individuais.

## Como instalar o Linux no Windows com o WSL

O Subsistema do Windows para Linux (WSL) permite que os desenvolvedores instalem uma distribuição do Linux (como Ubuntu, OpenSUSE, Kali, Debian, Arch Linux etc) e usem aplicativos Linux, utilitários e ferramentas de linha de comando bash diretamente no Windows, sem modificação, sem a sobrecarga de uma máquina virtual tradicional ou configuração dualboot.

### Pré-requisitos

Você deve estar executando o Windows 10 versão 2004 e superior (Build 19041 e superior) ou Windows 11 para usar os comandos abaixo.

### Instalar comando WSL

Agora você pode instalar tudo o que precisa para executar o WSL com um único comando. Abra o PowerShell no modo de administrador clicando com o botão direito do mouse e selecionando "Executar como administrador", insira o comando wsl --install e reinicie o computador.

```powershell
wsl --install
```

Esse comando habilitará os recursos necessários para executar o WSL e instalar a distribuição do Ubuntu do Linux.

Na primeira vez que você iniciar uma distribuição do Linux recém-instalada, uma janela do console será aberta e você será solicitado a aguardar que os arquivos sejam descompactados e armazenados em seu computador. Todos os lançamentos futuros devem levar menos de um segundo.

**Observação:** O comando acima só funcionará se o WSL não estiver instalado.

Para mais informações sobre o WSL: https://learn.microsoft.com/pt-br/windows/wsl/

## Como instalar o Nix

Independentemente de utilizar o Linux instalado nativamente ou através do WSL no Windows, a instalação do Nix deve ser realizada dentro do ambiente Linux.

Para iniciar a instalação, abra o terminal do Linux e digite o seguinte comando:

```bash
sudo curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install | sh -s -- --no-daemon
```

Para mais informações sobre o Nix: https://nixos.org/learn/
