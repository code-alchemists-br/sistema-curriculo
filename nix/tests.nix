{ pkgs }:

let
  backendPythonPackages = import ./backend-python-packages.nix { inherit pkgs; };
in
pkgs.mkShell {
  name = "tests";

  packages = [
    # Dependências e ferramentas de testes
    pkgs.git
    # Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
    (pkgs.python3.withPackages backendPythonPackages)
  ];

  shellHook = ''
    echo "Ambiente de testes"
  '';
}
