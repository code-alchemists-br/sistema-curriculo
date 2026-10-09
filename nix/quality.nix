{ pkgs }:

let
  backendPythonPackages = import ./backend-python-packages.nix { inherit pkgs; };
in
pkgs.mkShell {
  name = "quality";

  packages = [
    # Ferramentas de gate para o backend Python e geração de baseline.
    pkgs.git
    pkgs.ruff
    (pkgs.python3.withPackages (ps: with ps;
      (backendPythonPackages ps) ++ [
        bandit
        coverage
        radon
      ]
    ))
  ];

  shellHook = ''
    echo "Ambiente de quality gates do backend Python"
  '';
}
