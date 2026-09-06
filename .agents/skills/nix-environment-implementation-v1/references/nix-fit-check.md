# Check de aderência ao Nix

O veredito exige três confirmações:

1. O resultado desejado é um ambiente, pacote, módulo ou sistema definido por Nix.
2. A implementação pode ser concluída alterando somente código ou artefatos Nix permitidos.
3. A tarefa não exige ativar ou modificar o estado global da máquina.

Somente três respostas positivas permitem `valid`.

## Evidências a inspecionar

Na análise, examine resultado, sistemas alvo, versões, escopo, critérios, decisão, handoffs, arquivos e roteamento. No repositório, examine `*.nix`, `flake.lock`, configurações Nix, imports, manifests somente para leitura, documentação de comandos e `AGENTS.md` dos possíveis alvos.

Se não houver Nix no repositório, uma introdução ainda pode ser válida quando a análise aprovar explicitamente a adoção, os sistemas alvo e os outputs esperados. Não inicialize Nix apenas porque seria conveniente.

Use somente leitura e busca durante o gate. Não execute avaliação, geração de lock, build ou outro comando mutável.

## Sinais positivos

- análise pede flake, derivation, package, dev shell, overlay ou módulo Nix;
- resultado depende de pinagem ou composição declarativa de inputs Nix;
- arquivos-alvo são `*.nix` ou artefatos Nix permitidos;
- critérios podem ser demonstrados por parse, eval, flake check ou build Nix;
- nenhuma mudança na aplicação ou em outra tecnologia é necessária.

Exija pelo menos dois sinais independentes, incluindo um ligado ao resultado Nix.

## Sinais negativos

- demanda é funcionalidade de frontend ou backend;
- solução real pertence a Docker, CI, Terraform, Kubernetes, scripts ou gerenciador da linguagem;
- Nix aparece apenas como ambiente no qual outro código seria alterado;
- implementação exige modificar fonte, teste ou manifesto não Nix;
- pedido principal é instalar, ativar, fazer switch ou alterar configuração global;
- análise não define sistemas alvo, outputs ou versões suficientes.

## Vereditos e mensagens

### `valid`

Antes de escrever:

> Análise `<caminho>` (`<versão>`) validada para ambiente Nix: <evidências>. Modificarei somente <artefatos Nix>. Handoffs não Nix: <lista ou “nenhum”>. Nenhuma ativação do sistema será executada.

### `ambiguous`

Use quando a análise não distinguir Nix de outra tecnologia, faltar sistema alvo/output ou houver dependência não Nix incerta. Não altere arquivos:

> A implementação foi interrompida porque não está claro se a demanda pode ser atendida exclusivamente com artefatos Nix. Evidências: <lacuna ou conflito>. Nenhum arquivo foi alterado.

Faça somente a pergunta necessária ou recomende revisar a análise.

### `mismatch`

Use quando a atividade pertencer a outra tecnologia ou ao código da aplicação:

> A implementação foi interrompida porque a análise não descreve uma mudança exclusiva de código ou artefatos Nix. Evidências: <sinais concretos>. Nenhum arquivo foi alterado. Encaminhe a atividade ao perfil correspondente ou revise a referência.

## Casos limítrofes

- Adicionar uma ferramenta ao `devShell` é Nix; alterar `package.json` para usá-la não é.
- Empacotar aplicação existente com uma derivation é Nix; corrigir a aplicação dentro da derivation não é.
- Atualizar apenas um input de `flake.lock` pode ser Nix; atualizar todos os inputs sem necessidade não é parte implícita da tarefa.
- Definir serviço em módulo NixOS é Nix; executar `switch` para ativá-lo não é.
- Criar check Nix é permitido; modificar testes da aplicação para fazê-lo passar não é.
- `.envrc` que chama `use flake` não é artefato Nix para esta skill.
