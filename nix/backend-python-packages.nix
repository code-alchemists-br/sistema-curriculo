# Produz a lista de bibliotecas Python necessárias para executar o backend.
# Centraliza as dependências usadas pelos shells de desenvolvimento e qualidade
# para mantê-los consistentes e permitir que o gate execute os testes isoladamente.
{ pkgs }:
ps: with ps; [
  fastapi
  uvicorn
  sqlalchemy
  alembic
  psycopg
  pydantic-settings
  # Geração do currículo exportado em DOCX e PDF (RF09).
  python-docx
  reportlab
  # Leitura de PDF usada pelos testes de conteúdo do arquivo exportado.
  pypdf
]
