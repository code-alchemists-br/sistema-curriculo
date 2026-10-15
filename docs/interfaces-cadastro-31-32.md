# Validação das interfaces de cadastro — issues #31 e #32

## Base e escopo da entrega

Validação realizada sobre `dev` no commit `2286d03`, com testes adicionais na
branch `feature/issues-31-32-interfaces-cadastro`.

O patch preparado em 28/09/2026 não é compatível com a fábrica atual. A aplicação
foi recusada por `git apply --check`; nenhum trecho foi aplicado à força.
A `dev` já contém implementações autenticadas de cadastro:

| Interface | Endpoint | Implementação existente |
| --- | --- | --- |
| Formação acadêmica (#31) | `POST /formacoes-academicas` | `src/backend/api/formacao_academica.py` |
| Experiência profissional (#32) | `POST /experiencias-profissionais` | `src/backend/api/experiencia_profissional.py` |

A fábrica registra ambos os routers. O proprietário vem do UUID em
`request.state.usuario_id`, não de uma identidade escolhida pelo cliente na
URL. As datas do JSON são `data_inicio` e `data_fim`; formação utiliza os enums
de nível e status existentes. Reintroduzir as rotas e DTOs do patch antigo
criaria contratos concorrentes e perderia essas decisões atuais.

Esta entrega complementa os testes das interfaces existentes; não reivindica
sua implementação original. Não entrega telas frontend nem altera persistência,
autenticação ou composição da aplicação.

## Cobertura adicional

`src/backend/tests/test_api_cadastros_regressao.py` usa `AsyncMock(spec=...)`
como substituto dos executores. Os sete métodos exercitam ambos os cadastros:

- Comando tipado e resposta pública completos, com período aberto e fechado.
- Cronologia inválida sem invocar o executor.
- Propagação de falhas inesperadas, sem mascará-las como validação.
- Tradução de violações de domínio para 422.
- Rejeição de identidade textual no estado autenticado, sem efeitos.
- Retorno 503 quando o executor não foi composto.
- Campos obrigatórios ausentes e datas impossíveis rejeitados pelos DTOs.

Os handlers são chamados diretamente: esses testes não provam trânsito HTTP
real, autenticação completa, banco ou comportamento visual.

## Resultados reais no Nix

### Cadastros (testes existentes e novos)

```sh
nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python -m unittest backend.tests.test_api_formacao_academica \
  backend.tests.test_api_experiencia_profissional \
  backend.tests.test_api_cadastros_regressao -v
```

Resultado: **18 testes, OK**, sem testes ignorados ou falhas esperadas nesse grupo.

### Descoberta completa conforme o roteiro

```sh
nix develop .#backend --command env PYTHONDONTWRITEBYTECODE=1 \
  python -m unittest discover -s src/backend/tests -t src -v
```

Resultado: **378 testes, OK (skipped=2, expected failures=6)**. Antes dos testes
adicionais, o mesmo comando executou 371 testes, com as mesmas ressalvas.

A descoberta completa inclui arquivos denominados `test_integracao*.py`.
Eles também foram executados separadamente no ambiente `tests`, conforme as
regras do repositório. Como `nix/tests.nix` fornece apenas Git, foi usado nesse
shell o interpretador e as dependências já fornecidos pelo ambiente Nix backend
(não Python global). O caminho exato do interpretador desta execução foi
`/nix/store/50p17s0yh84ix8frd7j43f84r3qp99n1-python3-3.14.7-env/bin/python`.

```sh
nix develop .#tests --command env PYTHONDONTWRITEBYTECODE=1 \
  /nix/store/50p17s0yh84ix8frd7j43f84r3qp99n1-python3-3.14.7-env/bin/python \
  -m unittest discover -s src/backend/tests -t src -p 'test_integracao*.py' -v
```

Resultado: **17 testes, OK (skipped=2, expected failures=6)**. Em outra máquina,
obtenha o caminho correspondente com `nix develop .#backend --command python -c
'import sys; print(sys.executable)'`; o caminho do store não é universal.

As falhas esperadas pertencem aos testes existentes de isolamento entre
estudantes e rejeição de credenciais inválidas/ausentes. Os testes ignorados
referem-se a sessão expirada e revogada. Esses resultados não certificam a
segurança do sistema completo. Existem também avisos preexistentes de
obsolescência de `HTTP_422_UNPROCESSABLE_ENTITY`.

### Qualidade

```sh
nix develop .#quality --command ruff check src/backend
nix develop .#quality --command ruff format --check src/backend/tests/test_api_cadastros_regressao.py
```

Resultado: lint de todo o backend aprovado (`All checks passed!`) e arquivo
adicionado formatado (`1 file already formatted`).

## Revisão e entrega

As issues consultadas permaneciam abertas. A cobertura adicional atende à
exigência de doubles nos testes unitários; a equipe deve confirmar se os
critérios de aceite das interfaces existentes satisfazem o restante do escopo.

O PR deve ser destinado a `dev`, referenciar #31 e #32, explicar que as rotas já
existiam e apresentar esta cobertura complementar. Não fechar automaticamente
as issues nem fazer merge sem a confirmação da equipe sobre os critérios de
aceitação. CI remoto, revisão e aprovação continuam sendo etapas distintas dos
testes locais descritos aqui.
