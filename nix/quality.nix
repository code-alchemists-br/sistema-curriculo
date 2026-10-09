{ pkgs }:

let
  backendPythonPackages = import ./backend-python-packages.nix { inherit pkgs; };
in
pkgs.mkShell {
  name = "quality";

  packages = [
    # Ferramentas de gate estático para backend e frontend.
    pkgs.git
    pkgs.gitleaks
    pkgs.nodejs
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
    echo "Ambiente de quality gates"
  '';
}
