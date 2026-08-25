{ pkgs }:

pkgs.mkShell {
  name = "backend";

  packages = [
    # Dependências do ambiente backend
    pkgs.python3
  ];

  shellHook = ''
    echo "Ambiente de desenvolvimento do backend"
  '';
}
