{ pkgs }:

pkgs.mkShell {
  name = "frontend";

  packages = [
    # Dependências do ambiente frontend
  ];

  shellHook = ''
    echo "Ambiente de desenvolvimento do frontend"
  '';
}
