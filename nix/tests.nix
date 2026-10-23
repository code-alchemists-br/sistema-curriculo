{ pkgs }:

let
  backendPythonPackages = import ./backend-python-packages.nix { inherit pkgs; };
in
pkgs.mkShell {
  name = "tests";

  packages = [
    # Dependências e ferramentas de testes
    pkgs.git
    # Proveniência: decision-analysis prompts/backend/20261019-191822-consulta-paginada-associacoes-estudante-v002.md#v002
    (pkgs.python3.withPackages (
      ps: backendPythonPackages ps ++ [ ps.aiosqlite ]
    ))
  ];

  shellHook = ''
    echo "Ambiente de testes"
  '';
}
