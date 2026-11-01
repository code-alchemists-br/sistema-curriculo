#!/usr/bin/env bash

# Executa testes de integração com um PostgreSQL efêmero e isolado.
#
# Como faz: inicializa um cluster em diretório temporário, cria um banco local,
# exporta DATABASE_URL apenas para o comando recebido e encerra o servidor ao
# término da execução. Ele existe para que os testes de integração validem o
# dialeto PostgreSQL sem instalação global ou dados persistentes.

set -euo pipefail

if [ "$#" -eq 0 ]; then
  echo "Uso: $0 <comando-de-teste> [argumentos...]" >&2
  exit 64
fi

diretorio_temporario="$(mktemp -d -t sistema-curriculo-postgresql.XXXXXX)"
diretorio_dados="$diretorio_temporario/dados"
diretorio_socket="$diretorio_temporario/socket"
porta="$(python -c 'import socket; sock = socket.socket(); sock.bind(("127.0.0.1", 0)); print(sock.getsockname()[1]); sock.close()')"
servidor_iniciado=false

# Remove o cluster temporário e encerra o servidor iniciado pelo próprio script.
#
# Como faz: interrompe o processo somente quando o início foi confirmado e
# apaga exclusivamente o diretório criado por mktemp nesta execução. Existe
# para impedir processos órfãos e o reaproveitamento acidental de dados de teste.
limpar() {
  if [ "$servidor_iniciado" = true ]; then
    pg_ctl --pgdata="$diretorio_dados" --wait stop --mode=immediate >/dev/null
  fi
  rm -rf "$diretorio_temporario"
}

trap limpar EXIT INT TERM

mkdir "$diretorio_socket"
initdb \
  --pgdata="$diretorio_dados" \
  --username=postgres \
  --auth=trust \
  --encoding=UTF8 \
  --no-locale \
  >/dev/null
pg_ctl \
  --pgdata="$diretorio_dados" \
  --wait \
  --options="-k $diretorio_socket -p $porta" \
  start \
  >/dev/null
servidor_iniciado=true
createdb \
  --host="$diretorio_socket" \
  --port="$porta" \
  --username=postgres \
  sistema_curriculo_test

export DATABASE_URL="postgresql+psycopg://postgres@/sistema_curriculo_test?host=$diretorio_socket&port=$porta"
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}src"
export PYTHONDONTWRITEBYTECODE=1

alembic upgrade head

"$@"
