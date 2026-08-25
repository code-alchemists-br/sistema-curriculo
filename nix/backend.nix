{ pkgs }:

pkgs.mkShell {
  name = "backend";

  packages = [
    # Dependências do ambiente backend
  ];

  shellHook = ''
    echo "Ambiente de desenvolvimento do backend"
  '';
}
