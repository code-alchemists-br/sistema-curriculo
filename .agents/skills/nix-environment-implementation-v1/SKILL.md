---
name: nix-environment-implementation-v1
description: "Implementa ou modifica exclusivamente código e artefatos de ambiente Nix a partir de uma análise de decisão v4. Valida a hierarquia de AGENTS.md, a versão da análise, o contexto real do repositório e a aderência ao ecossistema Nix; rejeita mudanças em código da aplicação, Docker, CI, Terraform, Kubernetes, scripts genéricos e outros artefatos não Nix. Use somente por invocação explícita com a referência da análise e instruções adicionais opcionais."
---

# Nix Environment Implementation v1

Transforme uma análise aprovada somente em código ou artefatos próprios do Nix. A finalidade da mudança deve ser definir, compor, fixar ou verificar um ambiente, pacote, módulo ou sistema por meio de Nix — não implementar indiretamente uma funcionalidade da aplicação.

## Entrada

Exija uma referência inequívoca a exatamente um arquivo de análise de decisão. Aceite instruções adicionais opcionais em texto livre.

Se a referência estiver ausente, ambígua, inacessível ou apontar para mais de uma análise, peça o caminho exato e não altere arquivos.

## Gate antes de qualquer escrita

Permita somente inspeções e comandos não mutáveis até concluir, nesta ordem:

1. Leia integralmente os `AGENTS.md` aplicáveis, da raiz até o artefato e os possíveis arquivos-alvo.
2. Leia [references/analysis-input-contract.md](references/analysis-input-contract.md) e valide identidade, esquema, versão, status, linhagem, evidência e instruções adicionais.
3. Leia [references/nix-scope-boundary.md](references/nix-scope-boundary.md) e classifique cada resultado e arquivo como `nix-source`, `nix-managed-artifact`, `non-nix`, `system-activation` ou `inseparable`.
4. Leia [references/nix-fit-check.md](references/nix-fit-check.md), inspecione o repositório e determine `valid`, `ambiguous` ou `mismatch`.
5. Somente com `valid`, leia [references/implementation-protocol.md](references/implementation-protocol.md), implemente e verifique.

Não considere uma tarefa Nix apenas porque ela trata de ambiente, dependências, desenvolvimento ou infraestrutura.

## Escopo permitido

Implemente ou modifique somente:

- expressões `*.nix`, incluindo `flake.nix`, `default.nix` e `shell.nix`;
- flakes, inputs, outputs e composição de sistemas;
- derivations, packages, overlays e overrides;
- dev shells, toolchains e ambientes reprodutíveis;
- módulos e configurações NixOS, Home Manager e nix-darwin;
- configuração própria do Nix, como `nix.conf`, quando pertencente ao repositório;
- `flake.lock` e metadados gerenciados por ferramentas Nix já adotadas pelo projeto;
- testes ou checks expressos em Nix.

Leia arquivos não Nix quando forem evidência necessária, mas não os modifique.

## Escopo proibido

Não modifique:

- código-fonte, testes ou configuração funcional da aplicação;
- manifestos e lockfiles dos gerenciadores da linguagem, como `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `Cargo.toml`, `Cargo.lock`, `pyproject.toml` ou equivalentes;
- `Dockerfile`, Compose, CI/CD, Terraform, OpenTofu, Pulumi, Kubernetes, Helm ou manifests de cloud;
- Makefiles, Taskfiles, `.envrc`, scripts shell, PowerShell, Python ou outros auxiliares genéricos;
- documentação, ADRs, análises ou arquivos em `prompts`;
- conteúdo do Nix store, outputs de build ou o symlink `result`;
- configuração global ou estado ativo da máquina.

Não esconda alterações de aplicação em `runCommand`, fases de build, patches inline ou substituições de texto. Comandos dentro de uma derivation devem servir somente ao empacotamento ou à construção do ambiente descrito pela análise.

## Ativação e efeitos externos

Esta skill edita artefatos; não aplica ambientes ao host. Não execute `nixos-rebuild switch`, `home-manager switch`, `darwin-rebuild switch`, instalação em perfil, alteração de registry, configuração global do daemon ou operação equivalente. Se a análise exigir ativação, registre-a como passo posterior que requer autorização e contexto próprios.

Avaliação, checks e builds sem ativação são permitidos para verificar a implementação. Prefira opções que não criem links ou artefatos no workspace.

## Escopo misto

- Se a fatia Nix estiver claramente separada, implemente apenas essa parte e registre os demais arquivos como handoffs.
- Se o resultado Nix depender de editar código ou configuração não Nix, não faça a alteração indireta nem entregue uma solução parcial enganosa; solicite decomposição da análise.
- Se toda a demanda for de outra tecnologia ou atividade, classifique como `mismatch` e encerre sem alterações.

## Aprovação

A invocação explícita desta skill com o caminho exato de uma análise `status: proposed` aprova somente aquela versão e sua fatia Nix elegível. Não transfira aprovação para outra versão nem para arquivos ou ativações excluídos.

Não altere a análise referenciada. Quando escopo, decisão ou critérios precisarem mudar, solicite uma nova versão com `$decision-analysis-v4`.

## Comunicação

Antes da primeira escrita, informe a análise usada, as evidências de aderência, os artefatos Nix que serão modificados e os handoffs não Nix.

Na resposta final, inclua análise e versão, veredito, ambiente Nix entregue, arquivos alterados, instruções adicionais tratadas, verificações e atividades excluídas ou bloqueadas.
