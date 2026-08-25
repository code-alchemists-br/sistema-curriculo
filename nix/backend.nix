{ pkgs }:

pkgs.mkShell {
  name = "backend";

  packages = [
    # Dependências do ambiente backend
    pkgs.python3
    pkgs.git
  ];

  shellHook = ''
    echo "Ambiente de desenvolvimento do backend"
  '';
}
