{ pkgs }:

pkgs.mkShell {
  name = "tests";

  packages = [
    # Dependências e ferramentas de testes
    pkgs.git
  ];

  shellHook = ''
    echo "Ambiente de testes"
  '';
}
