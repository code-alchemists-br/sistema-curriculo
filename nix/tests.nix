{ pkgs }:

pkgs.mkShell {
  name = "tests";

  packages = [
    # Dependências e ferramentas de testes
  ];

  shellHook = ''
    echo "Ambiente de testes"
  '';
}
