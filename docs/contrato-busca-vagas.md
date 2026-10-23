# Busca de vagas: contrato e erros

**Escopo:** estado da branch `dev` no commit `ab2b8bc` (19/10/2026). Este documento separa a API do próprio projeto da integração externa do Grupo 2. A palavra “público” neste contrato significa contrato HTTP para consumidores; a rota exige autenticação.

## API do sistema: `GET /vagas`

A rota consulta o caso de uso de vagas para a sessão autenticada. O identificador do estudante vem do middleware (`request.state.usuario_id`), não de um parâmetro enviado pelo cliente.

| Parâmetro de query | Obrigatório | Significado |
| --- | --- | --- |
| `termo` | Não; padrão `""` | Cargo, empresa ou palavra-chave. |
| `localizacao` | Não | Cidade, estado ou modelo geográfico. |
| `modalidade` | Não | Modalidade, por exemplo `REMOTO`, `HIBRIDO` ou `PRESENCIAL`. |

Resposta `200 OK`:

```json
{
  "termo": "python",
  "filtros": {"localizacao": "São Paulo - SP", "modalidade": "HIBRIDO"},
  "total": 1,
  "vagas": [
    {
      "id": "vaga-101",
      "titulo": "Desenvolvedor Python Júnior",
      "empresa": "Tech Soluções",
      "descricao": "Atuação em backend e APIs.",
      "requisitos": ["Python", "FastAPI"],
      "localizacao": "São Paulo - SP",
      "modalidade": "HIBRIDO",
      "url_candidatura": "https://vagas.exemplo.com/101"
    }
  ]
}
```

`localizacao`, `modalidade` e `url_candidatura` podem ser `null` na vaga. `requisitos` é uma lista de textos. Uma busca sem resultados também retorna `200`, com `total: 0` e `vagas: []`, preservando `termo` e `filtros` para a interface poder explicar/refinar a busca.

## Erros da rota

| HTTP | Quando ocorre | Comportamento esperado |
| --- | --- | --- |
| `401` | A requisição não tem uma identidade de sessão UUID válida. | Solicitar autenticação; não repetir automaticamente. |
| `422` | Query incompatível com os tipos esperados. | Exibir orientação de correção; não mostrar stack trace. |
| `502` | O serviço externo falhou ou devolveu resposta inválida. | Informar indisponibilidade temporária e permitir nova tentativa. |
| `503` | O executor da consulta não foi configurado. | Tratar como recurso indisponível; não sugerir que a busca foi concluída. |
| `504` | A consulta externa excedeu o tempo limite. | Informar demora e oferecer nova tentativa. |

As respostas `502` e `504` usam mensagens controladas e não propagam detalhes, URLs ou exceções internas do provedor.

## Integração Grupo 2 e limite atual

A interface possui um cliente separado para sugestões/associações do Grupo 2. Ele espera um objeto com `associacoes`, cada uma com `curriculo_id` e `vaga`; valida os dados recebidos e traduz falhas em `indisponivel`, `resposta-invalida` ou `tempo-limite`. As mensagens mostradas ao estudante são genéricas e seguras.

Na branch `dev` consultada, o cliente padrão da interface é deliberadamente indisponível até existir um endpoint real confirmado. O arquivo [`contratos_integracao_grupo2.md`](contratos_integracao_grupo2.md) é uma proposta para validação entre equipes; não deve ser citado como contrato externo implementado. A busca `GET /vagas` do backend e a integração Grupo 2 não são intercambiáveis.

## Referências de verificação

- Backend: [`api/vagas.py`](../src/backend/api/vagas.py), [`test_api_vagas.py`](../src/backend/tests/test_api_vagas.py).
- Interface: [`cliente-vagas-grupo2.ts`](../src/frontend/features/listar-vagas/api/cliente-vagas-grupo2.ts), [`mensagem-erro-vagas.ts`](../src/frontend/features/listar-vagas/model/mensagem-erro-vagas.ts) e `mensagem-erro-vagas.test.ts`.

**Cards:** #383 (contrato de busca) e #429 (catálogo de falhas e resposta da interface).
