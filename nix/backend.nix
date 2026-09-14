{ pkgs }:

pkgs.mkShell {
  name = "backend";

  packages = [
    # Dependências do ambiente backend
    pkgs.git
    # Proveniência: decision-analysis prompts/ambientes/20260913-fundamentos-backend-nix-v001.md#v001
    (pkgs.python3.withPackages (ps: with ps; [
      fastapi
      uvicorn
      sqlalchemy
      alembic
      psycopg
      pydantic-settings
    ]))
  ];

  shellHook = ''
    echo "Ambiente de desenvolvimento do backend"
  '';
}
