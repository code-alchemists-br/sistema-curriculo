# Contratos de integração — Grupo 1 e Grupo 2

**Status:** proposta para validação entre as equipes. Este documento descreve um contrato sugerido; não representa uma API já implementada ou confirmada pelo repositório.

## 1. Objetivo e responsabilidades

- **Grupo 1:** mantém os currículos e fornece os dados necessários à busca de vagas.
- **Grupo 2:** recebe os dados autorizados do currículo, identifica vagas potencialmente compatíveis e devolve vagas sugeridas.
- **Importante:** conforme os requisitos atuais do sistema, a associação entre currículo e vaga é uma ação do estudante. Portanto, a resposta do Grupo 2 deve ser tratada inicialmente como **sugestões de vagas**, e não como associações persistidas automaticamente.

## 2. Contrato 1 — Envio de currículo do Grupo 1

### Payload proposto

```json
{
  "curriculo_id": "550e8400-e29b-41d4-a716-446655440000",
  "curriculo": {
    "titulo_versao": "Currículo para estágio em desenvolvimento",
    "formacoes": [
      {
        "curso": "Análise e Desenvolvimento de Sistemas",
        "instituicao": "Instituto de Tecnologia",
        "situacao": "Em andamento"
      }
    ],
    "experiencias": [
      {
        "cargo": "Desenvolvedor júnior",
        "descricao": "Desenvolvimento de aplicações e APIs"
      }
    ],
    "competencias": ["Python", "SQL", "Git"],
    "projetos": [
      {
        "nome": "API de gerenciamento",
        "descricao": "API desenvolvida com Python"
      }
    ],
    "idiomas": [
      {
        "idioma": "Inglês",
        "nivel": "Intermediário"
      }
    ]
  }
}
```

> **Atenção:** os campos aninhados acima são ilustrativos. O modelo de domínio atual do Grupo 1 representa o currículo por referências a itens de perfil; os nomes e a estrutura finais precisam ser mapeados para a serialização real da aplicação.

### Regras propostas

- `curriculo_id` é obrigatório e deve identificar de forma estável o currículo no Grupo 1.
- `curriculo` contém somente os dados necessários à análise de vagas.
- Enviar apenas dados que o estudante esteja autorizado a compartilhar com o Grupo 2.
- Não enviar credenciais, tokens, segredos ou dados pessoais desnecessários.
- A equipe deve decidir se o Grupo 1 envia o payload ao Grupo 2 ou se o Grupo 2 consulta uma API autenticada do Grupo 1. Não se deve presumir que ambas as modalidades estejam implementadas.

## 3. Contrato 2 — Modelo de vaga do Grupo 2

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---:|---|
| `id` | string | Sim | Identificador estável da vaga no Grupo 2 |
| `titulo` | string | Sim | Título da vaga |
| `empresa` | string | Sim | Nome da empresa contratante |
| `descricao` | string | Sim | Descrição das atividades e da oportunidade |
| `requisitos` | array de strings | Sim | Requisitos; pode ser uma lista vazia |
| `localizacao` | string ou `null` | A confirmar | Cidade, estado ou indicação de trabalho remoto |
| `modalidade` | string ou `null` | A confirmar | Modalidade de trabalho |
| `url_candidatura` | string ou `null` | A confirmar | Link para detalhes ou candidatura |

### Exemplo

```json
{
  "id": "vaga-g2-001",
  "titulo": "Estágio em Desenvolvimento Backend Python",
  "empresa": "Tech Inovação Soluções",
  "descricao": "Desenvolvimento de serviços e testes automatizados.",
  "requisitos": ["Python", "FastAPI", "SQL", "Git"],
  "localizacao": "São Paulo - SP",
  "modalidade": "HIBRIDO",
  "url_candidatura": "https://grupo2.exemplo.com/vagas/vaga-g2-001"
}
```

### Regras propostas

- `id` deve ser estável e único no contexto do Grupo 2. Recomenda-se tratá-lo como string, pois pode não ser UUID.
- `requisitos` deve ser sempre uma lista, inclusive quando não houver requisitos informados.
- Se as equipes concordarem, padronizar `modalidade` com `PRESENCIAL`, `REMOTO` e `HIBRIDO`, definindo também como representar valores desconhecidos.
- Validar `url_candidatura` como URL HTTP ou HTTPS quando preenchida.
- Confirmar com o Grupo 2 a obrigatoriedade de `localizacao`, `modalidade` e `url_candidatura`.

## 4. Contrato 3 — Resposta do Grupo 2 com vagas sugeridas

A resposta identifica o currículo em cada resultado e não repete os dados do currículo em cada vaga.

```json
{
  "associacoes": [
    {
      "curriculo_id": "550e8400-e29b-41d4-a716-446655440000",
      "vaga": {
        "id": "vaga-g2-001",
        "titulo": "Estágio em Desenvolvimento Backend Python",
        "empresa": "Tech Inovação Soluções",
        "descricao": "Desenvolvimento de serviços e testes automatizados.",
        "requisitos": ["Python", "FastAPI", "SQL", "Git"],
        "localizacao": "São Paulo - SP",
        "modalidade": "HIBRIDO",
        "url_candidatura": "https://grupo2.exemplo.com/vagas/vaga-g2-001"
      }
    }
  ]
}
```

### Regras propostas

- `associacoes` é uma lista e pode estar vazia se nenhuma vaga for encontrada.
- Cada item contém `curriculo_id` e `vaga`.
- O `curriculo_id` deve corresponder ao currículo usado na consulta.
- O objeto `vaga` segue o contrato da seção 3.
- Não repetir os dados completos do currículo em cada resultado.
- Se houver pontuação ou justificativa de compatibilidade, adicioná-las somente após acordo entre as equipes, por exemplo `pontuacao_compatibilidade` numérica e `motivos` como lista de strings.
- Até que haja decisão explícita diferente, os resultados são **sugestões**. A confirmação do estudante deve continuar necessária para criar uma associação persistida no Grupo 1.

## 5. Fluxo de integração proposto

1. O estudante seleciona um currículo e solicita a busca de vagas.
2. O Grupo 1 valida o acesso do estudante ao currículo.
3. O Grupo 1 envia ao Grupo 2 apenas os dados autorizados, ou o Grupo 2 consulta uma API autenticada do Grupo 1 — conforme decisão de arquitetura.
4. O Grupo 2 procura e ordena vagas compatíveis.
5. O Grupo 2 devolve a lista no formato da seção 4.
6. O Grupo 1 apresenta as sugestões ao estudante.
7. Se o estudante escolher uma vaga, o Grupo 1 executa o fluxo próprio para registrar a associação, conforme as regras de negócio existentes.

## 6. Autenticação e segurança

As equipes devem acordar e documentar:

- mecanismo de autenticação entre serviços;
- forma de provisionar, armazenar, renovar e revogar credenciais;
- permissões mínimas para cada integração;
- uso obrigatório de HTTPS;
- expiração e rotação de tokens;
- limites de acesso aos dados do currículo e registro de auditoria;
- comportamento para token ausente, inválido ou expirado.

Tokens e segredos nunca devem ser incluídos nos payloads de currículo ou vaga, nem gravados em logs. O método de autenticação definitivo não está especificado neste contrato.

## 7. Erros e comportamento operacional

Formato de erro sugerido, sujeito à convenção adotada pelas equipes:

```json
{
  "erro": {
    "codigo": "CURRICULO_NAO_ENCONTRADO",
    "mensagem": "O currículo informado não foi encontrado."
  }
}
```

Definir antes da implementação:

- códigos HTTP e códigos de erro de negócio;
- timeout e política de tentativas;
- idempotência para evitar processamento duplicado;
- paginação, limite máximo de resultados e ordenação;
- versionamento do contrato;
- identificador de correlação para rastrear requisições.

## 8. Decisões pendentes entre as equipes

- [ ] Os resultados são sugestões ou associações persistidas?
- [ ] O currículo será enviado no corpo da requisição ou consultado por uma API autenticada?
- [ ] Quais campos de currículo são indispensáveis para o matching?
- [ ] O Grupo 2 fornecerá pontuação ou justificativa de compatibilidade?
- [ ] Quais são o endpoint, o método HTTP e o mecanismo de autenticação?
- [ ] Quais campos do modelo de vaga são obrigatórios?
- [ ] Qual será o padrão de modalidade e como representar valores desconhecidos?
- [ ] Quais são as regras de paginação, timeout, tentativas e versionamento?

## 9. Referências do repositório do Grupo 1

- Modelo de domínio do currículo: [src/backend/domain/curriculo.py](https://github.com/code-alchemists-br/sistema-curriculo/blob/dev/src/backend/domain/curriculo.py)
- DTO de vaga usado em teste: [src/backend/tests/doubles/api_vagas_grupo2.py](https://github.com/code-alchemists-br/sistema-curriculo/blob/dev/src/backend/tests/doubles/api_vagas_grupo2.py)
- Requisitos funcionais: [docs/requisitos_funcionais.md](https://github.com/code-alchemists-br/sistema-curriculo/blob/dev/docs/requisitos_funcionais.md)
- Modelo de dados: [docs/modelagem_der.md](https://github.com/code-alchemists-br/sistema-curriculo/blob/dev/docs/modelagem_der.md)
- Registro de rotas da aplicação: [src/backend/api/factory.py](https://github.com/code-alchemists-br/sistema-curriculo/blob/dev/src/backend/api/factory.py)

**Nota de implementação:** o DTO encontrado no código de testes é uma referência útil para o modelo de vaga, mas não comprova por si só o contrato de uma API de produção do Grupo 2. Validar este documento com ambas as equipes antes de implementar.
