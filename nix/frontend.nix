{ pkgs }:

pkgs.mkShell {
  name = "frontend";

  packages = [
    # Dependências do ambiente frontend
    pkgs.git
    # Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
    pkgs.nodejs
  ];

  shellHook = ''
    echo "Ambiente de desenvolvimento do frontend"
  '';
}
