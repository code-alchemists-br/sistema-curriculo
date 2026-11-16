{ pkgs }:

let
  backendPythonPackages = import ./backend-python-packages.nix { inherit pkgs; };
in
pkgs.mkShell {
  name = "tests";

  packages = [
    # Dependências e ferramentas de testes
    pkgs.git
    # Servidor e clientes para os testes de integração descartáveis.
    pkgs.postgresql
    # Proveniência: decision-analysis prompts/backend/20261019-191822-consulta-paginada-associacoes-estudante-v002.md#v002
    # aiosqlite já faz parte das dependências do backend.
    (pkgs.python3.withPackages backendPythonPackages)
  ];

  shellHook = ''
    echo "Ambiente de testes"
  '';
}
