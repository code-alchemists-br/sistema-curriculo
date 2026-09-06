# Fronteira de código e artefatos Nix

Classifique cada resultado, tarefa e arquivo antes de escrever.

## `nix-source`

Código declarativo interpretado pelo Nix:

- qualquer expressão `*.nix`;
- `flake.nix`, `default.nix`, `shell.nix` e módulos importados;
- derivations, packages, overlays, overrides e funções Nix;
- dev shells e toolchains;
- módulos NixOS, Home Manager e nix-darwin;
- checks e testes definidos como outputs ou derivations Nix.

Scripts embutidos em strings Nix podem existir como parte legítima de uma derivation, mas devem construir ou configurar o ambiente. Não os use para contornar a proibição de editar ou implementar a aplicação.

## `nix-managed-artifact`

Artefato não escrito na linguagem Nix, mas pertencente diretamente ao funcionamento ou pinagem do Nix:

- `flake.lock`;
- `nix.conf` versionado no repositório;
- arquivos de lock ou metadados de ferramentas Nix já adotadas, como fontes pinadas por mecanismo existente.

Prefira gerar locks com a ferramenta correspondente, sem edição manual. Atualize somente inputs necessários à decisão; não faça atualização global oportunista.

## `non-nix`

Mesmo quando relacionado ao ambiente, fica fora:

- código e testes da aplicação;
- manifestos ou locks de npm, pnpm, Yarn, Cargo, Python, Go, Maven, Gradle e outros ecossistemas;
- Docker, Compose, CI/CD, Terraform/OpenTofu, Pulumi, Kubernetes, Helm e cloud;
- `.envrc`, Makefile, Taskfile e scripts auxiliares;
- documentação e artefatos de análise;
- patches ou arquivos-fonte criados para alterar a aplicação.

Esses arquivos podem ser lidos para descobrir versões, comandos e estrutura, mas nunca modificados por esta skill.

## `system-activation`

É ativação ou mutação externa, não implementação de artefato:

- `nixos-rebuild switch`, `home-manager switch` e `darwin-rebuild switch`;
- `nix profile install`, upgrade ou remove;
- mudanças em registry, channels, daemon, substituters ou configuração global;
- deploy, switch ou boot de uma configuração;
- edição direta no Nix store ou em caminhos fora do workspace.

Não execute. Registre como passo posterior quando aplicável.

## Artefatos gerados

- Não edite caminhos de `/nix/store` ou equivalentes.
- Não versione nem substitua outputs de build.
- Evite criar `result`; use `nix build --no-link` quando disponível.
- Não remova um `result` preexistente, pois pode pertencer ao usuário.
- Trate `flake.lock` como fonte versionada permitida, não como output descartável.

## Escopo misto

Classifique cada critério como `nix-source`, `nix-managed-artifact`, `non-nix`, `system-activation` ou `inseparable`.

- Somente as duas categorias Nix: prossiga.
- Mistura separável: implemente apenas a fatia Nix e registre handoffs.
- Item não Nix necessário e inseparável: interrompa e solicite decomposição.
- Nenhum artefato Nix: use `mismatch`.

Não declare a análise inteira implementada quando entregar somente os artefatos Nix.
