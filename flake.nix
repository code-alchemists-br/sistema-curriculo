{
  description = "Ambientes de desenvolvimento do projeto";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";

      pkgs = import nixpkgs {
        inherit system;
      };
    in
    {
      devShells.${system} = {
        backend = import ./nix/backend.nix {
          inherit pkgs;
        };

        frontend = import ./nix/frontend.nix {
          inherit pkgs;
        };

        tests = import ./nix/tests.nix {
          inherit pkgs;
        };
      };
    };
}
