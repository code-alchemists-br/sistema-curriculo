# Contrato de credenciais de sessão

## Objetivo e escopo

Este documento define como a API emite, transporta, valida e revoga a
credencial que representa uma sessão autenticada. Ele complementa o
[planejamento de autenticação](requisitos-seguranca.md#26-sessão) e a
[interface das rotas protegidas](requisitos-seguranca.md#9-interface-de-autenticação-para-rotas-protegidas).

O contrato cobre sessões da aplicação web. Integrações entre serviços e tokens
de API pertencem a contratos separados.

## Decisões do contrato

- A sessão é **opaca e mantida no servidor**; não é JWT nem contém dados de
  identidade ou autorização legíveis pelo cliente.
- A credencial é transportada exclusivamente por cookie. A API NÃO DEVE aceitá-la
  em `Authorization`, query string ou corpo da requisição.
- Uma sessão dura no máximo **8 horas** desde sua criação. Não há renovação
  automática nem extensão por atividade; após expirar, o usuário autentica-se
  novamente.
- Uma conta pode manter mais de uma sessão ativa, por exemplo em dispositivos
  diferentes. Logout revoga somente a sessão apresentada naquela requisição.

## Credencial e armazenamento

Após validar as credenciais, a API gera 32 bytes usando um gerador
criptograficamente seguro e codifica-os em Base64 URL-safe sem padding. O valor
resultante é o token opaco da sessão. Ele não contém `usuario_id`, papel,
permissões, timestamps ou outros atributos interpretáveis pelo cliente.

O token em claro só é entregue uma vez no cabeçalho `Set-Cookie`. A persistência
guarda somente seu resumo SHA-256, com índice único, nunca o token em claro. A
entropia de 256 bits torna inviável adivinhar o token; o resumo permite localizar
a sessão sem manter uma credencial reutilizável no banco.

O registro de sessão contém, no mínimo:

| Campo | Significado |
|---|---|
| `sessao_id` | Identificador interno UUID, sem valor de autenticação para o cliente. |
| `usuario_id` | Conta proprietária da sessão. |
| `token_hash` | SHA-256 do token recebido no cookie; único e nunca devolvido pela API. |
| `criada_em` | Instante UTC de emissão. |
| `expira_em` | Instante UTC igual a `criada_em + 8 horas`. |
| `revogada_em` | Instante UTC da revogação, nulo enquanto ativa. |

O mapeamento e as migrations ficam na infraestrutura. A identidade confiável
entregue à API é um contexto mínimo `UsuarioAutenticado(usuario_id: UUID)`;
token, hash, timestamps e estado de persistência não são expostos ao caso de uso.

## Cookie HTTP

Em produção, o nome do cookie é `__Host-sessao`. O cabeçalho de sucesso no
login deve equivaler a:

```http
Set-Cookie: __Host-sessao=<token-opaco>; Path=/; Max-Age=28800; Secure; HttpOnly; SameSite=Lax
```

O cookie não define `Domain`, conforme os requisitos do prefixo `__Host-`. Ele
é enviado apenas em HTTPS. A aplicação cliente não lê, copia nem armazena o
token em local storage, session storage, JavaScript ou estado persistente.

O ambiente local pode usar configuração própria de cookie para HTTP em
`localhost`, isolada da configuração de produção. Essa exceção não pode reduzir
os atributos de produção nem ser habilitada em implantação pública.

## Operações HTTP

### Criar sessão — `POST /acessos`

Requisição:

```json
{
  "email": "estudante@example.com",
  "senha": "senha-informada"
}
```

Com credenciais válidas e conta não excluída, a API cria um registro de sessão,
define o cookie de sessão e responde `204 No Content`. A senha não é devolvida
nem persistida em texto claro.

Para e-mail inexistente, senha incorreta ou conta excluída, responde `401
Unauthorized` com mensagem uniforme e sem `Set-Cookie`. A API não revela qual
condição falhou. Falhas de validação do formato permanecem `422`; limitação de
tentativas pode responder `429 Too Many Requests` sem revelar a existência da
conta.

### Consultar sessão — `GET /sessao/atual`

Com sessão válida, responde `200 OK` com a identidade pública mínima:

```json
{
  "usuario_id": "uuid-da-conta"
}
```

Sem cookie, com token desconhecido, expirado, revogado ou ligado a conta
excluída, responde `401 Unauthorized`. A resposta não distingue esses casos.
Essa rota não prolonga a sessão.

### Encerrar sessão — `DELETE /sessao/atual`

A API revoga a sessão correspondente ao cookie, se houver, e remove o cookie
com `Max-Age=0`, `Path=/`, `Secure`, `HttpOnly` e `SameSite=Lax`. Responde
`204 No Content` mesmo quando o cookie está ausente, inválido ou expirado,
tornando o encerramento idempotente. A revogação impede o uso do mesmo token em
requisições posteriores.

## Validação em rotas protegidas

A dependência comum de autenticação lê somente `__Host-sessao`, calcula seu
SHA-256 e busca o registro correspondente. A sessão é válida somente se:

1. o registro existe;
2. `revogada_em` é nulo;
3. `expira_em` é posterior ao instante UTC atual;
4. a conta existe e não está logicamente excluída (`deleted_at` nulo).

Se alguma condição falhar, a dependência responde `401` antes de chamar o caso
de uso. Caso todas sejam satisfeitas, fornece `UsuarioAutenticado` à rota. A
autorização e a propriedade de cada recurso usam o `usuario_id` desse contexto,
nunca identidade enviada pelo cliente. A sessão não concede papel ou permissão
por si só.

## CSRF e limites de transporte

Como o navegador envia cookies automaticamente, operações que alteram estado
DEVEM validar o cabeçalho `Origin` contra uma lista explícita de origens
permitidas e aplicar proteção CSRF. `SameSite=Lax` é defesa adicional, não
substitui esses controles. O formato, a emissão e a verificação do token CSRF
devem ser definidos antes de habilitar operações mutáveis autenticadas por
cookie em produção. O login também deve validar origem e limitar tentativas;
credenciais e cookies só podem trafegar por HTTPS em produção.

Tokens, senhas e cabeçalhos `Cookie`/`Set-Cookie` não podem aparecer em logs,
mensagens de erro, métricas ou rastreamentos.

## Revogação e limpeza

- Logout revoga somente o registro associado ao token apresentado.
- Exclusão lógica da conta invalida todas as sessões da conta; a validação
  também rejeita imediatamente uma conta com `deleted_at` preenchido.
- Uma futura alteração ou redefinição de senha deve revogar todas as sessões
  existentes da conta após a atualização bem-sucedida da credencial.
- Registros expirados ou revogados podem ser removidos por rotina de limpeza,
  desde que a remoção não restaure sua validade nem afete auditoria exigida.

## Testes de contrato

Os testes de API devem cobrir emissão do cookie após login válido, ausência de
cookie e resposta uniforme para credenciais inválidas, atributos do cookie,
acesso com sessão ativa, rejeição de token desconhecido/expirado/revogado,
rejeição de conta excluída e revogação idempotente no logout. Os testes devem
controlar gerador aleatório, relógio e repositório de sessões por doubles; não
devem usar banco ou relógio real para validar regras de sessão.
