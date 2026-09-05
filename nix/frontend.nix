{ pkgs }:

pkgs.mkShell {
  name = "frontend";

  packages = [
    # Dependências do ambiente frontend
    pkgs.git
  ];

  shellHook = ''
    echo "Ambiente de desenvolvimento do frontend"
  '';
}
