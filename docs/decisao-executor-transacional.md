# Decisão: executor transacional genérico para ligar rotas ao banco

## Problema

Cada rota que precisa de persistência exige um adaptador de composição que abre
a sessão, cria a transação, monta o caso de uso com os repositórios
SQLAlchemy e devolve o resultado. Com uma classe por operação (padrão de
`operacoes_formacao_academica.py`), ligar as rotas de versão do currículo
significaria repetir o mesmo código de sessão e transação várias vezes.

## Decisão

`ExecutorTransacionalSqlAlchemy`
(`src/backend/infrastructure/persistence/sqlalchemy/executor_transacional.py`)
recebe a fábrica de sessões e uma função que monta o caso de uso a partir de uma
sessão. A cada chamada ele abre `sessoes.begin()`, monta o caso de uso e delega
`executar`. Sucesso confirma a transação; exceção reverte e é propagada.
`criar_executor_transacional` devolve `None` quando não há banco, mantendo a
rota em 503.

No `main.py`, cada rota vira uma expressão curta:

```python
_listar_versoes_curriculo = criar_executor_transacional(
    _sessoes_persistencia,
    lambda sessao: ListarVersoesCurriculo(RepositorioCurriculoSqlAlchemy(sessao)),
)
```

## Consequências

- Menos código repetido e um único ponto de controle de transação.
- A composição continua na camada externa (`main.py`); Application e Domain não
  mudam e não conhecem SQLAlchemy.
- Convive com o padrão antigo de uma classe por operação, ainda usado por
  formação, experiência e projeto acadêmico. Migrar esses é opcional e deve ser
  decidido pelo time.
- Casos de uso que precisam de uma sessão por operação diferente da transação
  única por chamada não se encaixam sem adaptação.

## Autorização por proprietário

As rotas de versão do currículo recebem o `usuario_id` na URL, mas o
`MiddlewareAutenticacaoSessao` compara esse valor com o da sessão e responde 403
quando diferem, antes de o executor ser chamado. O executor transacional não
participa dessa decisão.
