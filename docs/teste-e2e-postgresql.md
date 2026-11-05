# Teste E2E local com PostgreSQL persistente

Este roteiro inicia um PostgreSQL local e persistente para testar manualmente
backend e frontend em conjunto. O servidor é fornecido pelo ambiente Nix do
projeto; não é necessário instalar PostgreSQL globalmente.

O cluster só aceita conexões por socket local e usa exclusivamente o banco
`sistema_curriculo_e2e`. Escolha um diretório de estado fora do repositório e
que não possua espaços no caminho.

## Iniciar o banco e o backend

No primeiro terminal, a partir da raiz do repositório, defina onde os dados do
cluster serão persistidos e inicie-o:

```bash
export POSTGRES_E2E_STATE_DIR="/caminho/local/sistema-curriculo-e2e"
nix develop .#tests --command ./scripts/postgres-e2e iniciar
```

Obtenha a URL do banco e inicie o backend. O `tail` retém somente a URL porque
o ambiente Nix também mostra uma mensagem de entrada no terminal:

```bash
export DATABASE_URL="$(
  nix develop .#tests --command ./scripts/postgres-e2e url | tail -n 1
)"

nix develop .#backend --command sh -c \
  'PYTHONPATH=src uvicorn backend.main:app --host 127.0.0.1 --port 8000'
```

O comando `iniciar` preserva os dados existentes e executa as migrations antes
de disponibilizar o banco.

## Iniciar o frontend

No segundo terminal, também na raiz do repositório, aponte o frontend para o
backend local e inicie o Vite:

```bash
nix develop .#frontend --command npm --prefix src/frontend ci
VITE_API_URL=http://127.0.0.1:8000 \
  nix develop .#frontend --command npm --prefix src/frontend run dev
```

Abra no navegador o endereço informado pelo Vite e execute o cenário E2E
manual desejado. Os dados criados permanecerão no diretório definido em
`POSTGRES_E2E_STATE_DIR`.

## Consultar, resetar e parar

Use os comandos abaixo no terminal que possuir `POSTGRES_E2E_STATE_DIR`
definida:

```bash
nix develop .#tests --command ./scripts/postgres-e2e status
nix develop .#tests --command ./scripts/postgres-e2e reset
nix develop .#tests --command ./scripts/postgres-e2e parar
```

`reset` encerra conexões ativas do banco E2E, recria somente
`sistema_curriculo_e2e` e reaplica todas as migrations. Pare o backend antes
do reset para que a aplicação não tente reutilizar conexões que foram
encerradas.

Não aponte `POSTGRES_E2E_STATE_DIR` para dados de desenvolvimento ou produção.
