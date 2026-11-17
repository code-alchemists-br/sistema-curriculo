# Busca de vagas: contrato e erros

**Escopo:** estado integrado com o `cvmatch` (`esw3_cvmatcher`) no backend e frontend do `sistema-curriculo`. Este documento separa a API HTTP autenticada do próprio sistema (`GET /vagas`) da comunicação server-to-server com o serviço externo do Grupo 2 (`POST /matches`). A rota exige sessão autenticada.

## API do sistema: `GET /vagas`

A rota consulta o caso de uso `ConsultarVagas` para o estudante autenticado. O identificador do estudante vem do middleware (`request.state.usuario_id`), nunca de um parâmetro enviado pelo cliente. Quando `GRUPO2_API_URL` e a persistência estão configuradas, o backend lê `CurriculoCompleto` do estudante, projeta os campos autorizados e consulta `POST /matches?limit=...` no `cvmatch`.

| Parâmetro de query | Obrigatório | Significado |
| --- | --- | --- |
| `termo` | Não; padrão `""` | Termo opcional ecoado na resposta e aceito na interface. |
| `localizacao` | Não | Parâmetro opcional preservado em `filtros` (não gera filtragem geográfica de elegibilidade). |
| `modalidade` | Não | Parâmetro opcional preservado em `filtros`. |
| `limit` | Não; padrão `GRUPO2_DEFAULT_LIMIT` (`10`) | Quantidade máxima de recomendações (`1` a `100`). |

Resposta `200 OK`:

```json
{
  "termo": "",
  "filtros": {},
  "total": 1,
  "vagas": [
    {
      "id": "101",
      "titulo": "Estágio em Desenvolvimento Backend Python",
      "empresa": "Tech Soluções",
      "descricao": "Atuação em backend e APIs.",
      "requisitos": ["Python", "FastAPI"],
      "localizacao": "São Paulo - SP",
      "modalidade": "HYBRID",
      "url_candidatura": "https://vagas.exemplo.com/101",
      "ranque": 1,
      "pontuacao_compatibilidade": 92.5,
      "elegivel": true,
      "nivel_senioridade": "INTERN",
      "salario": "R$ 1.800 – R$ 2.200",
      "moeda": "BRL",
      "palavras_chave": ["API", "Backend"],
      "data_publicacao": "2026-11-01T12:00:00Z",
      "requisitos_atendidos": ["Python"],
      "requisitos_faltantes": ["FastAPI"]
    }
  ]
}
```

`localizacao`, `modalidade` e `url_candidatura` podem ser `null` ou string vazia conforme o adaptador; o cliente frontend normaliza textos vazios para `null` antes da exibição. Uma busca sem resultados retorna `200 OK`, com `total: 0` e `vagas: []`, preservando `termo` e `filtros`. Quando `elegivel` for `false` (vaga expirada/inativa no `cvmatch`), a interface mantém o item após as vagas ativas com selo visual de vaga encerrada ou inativa.

## Erros da rota

| HTTP | Quando ocorre | Comportamento esperado |
| --- | --- | --- |
| `401` | A requisição não tem uma identidade de sessão UUID válida. | Solicitar autenticação; não repetir automaticamente. |
| `422` | Query incompatível com os tipos ou limites esperados (ex.: `limit < 1` ou `limit > 100`). | Exibir orientação de correção; não mostrar stack trace. |
| `502` | O `cvmatch` devolveu erro HTTP (`422`, `429`, `500`, `503`), JSON/schema inválido ou falha de conexão. | Informar indisponibilidade temporária ou resposta inválida e permitir nova tentativa. |
| `503` | `GRUPO2_API_URL` ou o banco não foi configurado (`consultar_vagas` é `None`). | Tratar como recurso indisponível; não substituir falhas reais por vagas de demonstração quando `VITE_API_URL` estiver configurada. |
| `504` | A consulta externa excedeu o tempo limite (`GRUPO2_API_TIMEOUT_MS`). | Informar demora e oferecer nova tentativa. |

As respostas `502` e `504` usam mensagens controladas e não propagam URLs, payloads de currículo ou exceções internas do provedor.

## Integração Grupo 2 na interface

Quando `VITE_API_URL` está configurada, o frontend usa [`cliente-vagas-http.ts`](../src/frontend/features/listar-vagas/api/cliente-vagas-http.ts) contra `GET /vagas` (sem fallback silencioso para dados fictícios de demonstração em erro de rede ou `5xx`/`429`), exibindo estado de erro recuperável em [`TelaVagasGrupo2.tsx`](../src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.tsx). Sem `VITE_API_URL`, o frontend mantém o cliente de demonstração local para preview isolado. O documento [`contrato-integracao-grupo2.md`](contrato-integracao-grupo2.md) consolida o contrato autoritativo com o `cvmatch`.

## Referências de verificação

- Backend: [`api/vagas.py`](../src/backend/api/vagas.py), [`consulta_vagas.py`](../src/backend/application/consulta_vagas.py), [`cliente_vagas_grupo2.py`](../src/backend/infrastructure/integrations/cliente_vagas_grupo2.py), [`main.py`](../src/backend/main.py), [`test_api_vagas.py`](../src/backend/tests/test_api_vagas.py), [`test_cliente_vagas_grupo2_http.py`](../src/backend/tests/test_cliente_vagas_grupo2_http.py) e [`test_integracao_busca_vagas.py`](../src/backend/tests/test_integracao_busca_vagas.py).
- Interface: [`cliente-vagas-http.ts`](../src/frontend/features/listar-vagas/api/cliente-vagas-http.ts), [`cliente-vagas-grupo2.ts`](../src/frontend/features/listar-vagas/api/cliente-vagas-grupo2.ts), [`TelaVagasGrupo2.tsx`](../src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.tsx), [`mensagem-erro-vagas.ts`](../src/frontend/features/listar-vagas/model/mensagem-erro-vagas.ts) e testes correspondentes.

**Cards:** #383 (contrato de busca), #173 (campos obrigatórios Grupo 2) e #429 (catálogo de falhas e resposta da interface).
