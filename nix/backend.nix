{ pkgs }:

let
  backendPythonPackages = import ./backend-python-packages.nix { inherit pkgs; };
in
pkgs.mkShell {
  name = "backend";

  packages = [
    # Dependências do ambiente backend
    pkgs.git
    # Proveniência: decision-analysis prompts/ambientes/20260913-fundamentos-backend-nix-v001.md#v001
    (pkgs.python3.withPackages backendPythonPackages)
  ];

  shellHook = "echo \"Ambiente de desenvolvimento do backend\"";
}
