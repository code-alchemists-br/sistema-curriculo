# Contrato de credenciais de sessão

## Objetivo e escopo

Este documento define como a API emite, transporta, valida e revoga a
credencial que representa uma sessão autenticada. Ele complementa o
[planejamento de autenticação](requisitos-seguranca.md#26-sessão) e a
[interface das rotas protegidas](requisitos-seguranca.md#9-interface-de-autenticação-para-rotas-protegidas).

O contrato cobre sessões da aplicação web. Integrações entre serviços e tokens
de API pertencem a contratos separados.

## Credenciais da conta

O cadastro `POST /estudantes` e o login `POST /acessos` recebem `email` e
`senha` em JSON. A senha aceita de 8 a 1024 caracteres na interface HTTP. O
e-mail é normalizado para minúsculas e validado pelo domínio antes da busca da
conta.

No cadastro, a senha é derivada com scrypt (`N=16384`, `r=8`, `p=1`), salt
aleatório de 16 bytes e saída de 64 bytes. O formato persistido identifica o
algoritmo e seus parâmetros; a persistência guarda esse valor derivado, nunca a
senha em texto claro. No login, o mesmo adapter recalcula o hash e compara o
resultado em tempo constante. Uma conta inexistente, excluída ou com senha
incorreta produz a mesma falha de credenciais.

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

## Ciclo de vida da sessão

A sessão autenticada passa pelos estados e transições abaixo.

```mermaid
flowchart LR
    A[Credenciais informadas] --> B{Credenciais válidas?}

    B -->|Não| C[401 Unauthorized]
    B -->|Sim| D[Criar sessão]

    D --> E[Gerar token opaco]
    E --> F[Persistir hash e validade]
    F --> G[Enviar cookie __Host-sessao]

    G --> H[Sessão ativa]

    H --> I{Requisição protegida}
    I --> J{Sessão válida?}

    J -->|Sim| K[Associar usuario_id à requisição]
    K --> L[Executar rota protegida]

    J -->|Não| M[401 Unauthorized]

    H --> N[Logout]
    N --> O[Revogar sessão]
    O --> P[Remover cookie]
    P --> Q[Sessão revogada]

    H --> R[Expiração após 8 horas]
    R --> S[Sessão expirada]

    H --> T[Exclusão lógica da conta]
    T --> U[Sessões da conta deixam de autenticar]

## Credencial e armazenamento

Após validar as credenciais, a API gera 32 bytes usando um gerador
criptograficamente seguro e codifica-os em Base64 URL-safe sem padding. O valor
resultante é o token opaco da sessão. Ele não contém `usuario_id`, papel,
permissões, timestamps ou outros atributos interpretáveis pelo cliente.

O token em claro só é entregue uma vez no cabeçalho `Set-Cookie`. A persistência
guarda somente seu resumo SHA-256, com índice único, nunca o token em claro. A
entropia de 256 bits torna inviável adivinhar o token; o resumo permite localizar
a sessão sem manter uma credencial reutilizável no banco.

O registro de sessão persistido contém:

| Campo | Significado |
|---|---|
| `id` | Identificador interno UUID, sem valor de autenticação para o cliente. |
| `usuario_id` | Conta proprietária da sessão. |
| `token_hash` | SHA-256 do token recebido no cookie; único e nunca devolvido pela API. |
| `criada_em` | Instante UTC de emissão. |
| `expira_em` | Instante UTC igual a `criada_em + 8 horas`. |
| `revogada_em` | Instante UTC da revogação, nulo enquanto ativa. |

O mapeamento e as migrations ficam na infraestrutura. O middleware de sessão
valida a credencial antes de encaminhar uma rota protegida e disponibiliza o
UUID autenticado em `request.state.usuario_id`. Token, hash, timestamps e estado
de persistência não são entregues aos handlers como dados da requisição.

## Cookie HTTP

O código atual usa o cookie `__Host-sessao` e define os atributos abaixo no
login, inclusive no ambiente local:

```http
Set-Cookie: __Host-sessao=<token-opaco>; Path=/; Max-Age=28800; Secure; HttpOnly; SameSite=Lax
```

O cookie não define `Domain`, conforme os requisitos do prefixo `__Host-`. Ele
é enviado apenas em HTTPS. A aplicação cliente não lê, copia nem armazena o
token em local storage, session storage, JavaScript ou estado persistente.

Na implementação atual, a API também define `Secure` no cookie local; não há
configuração separada para HTTP em `localhost`. Não remova esse atributo para
contornar problemas de ambiente sem uma decisão de segurança e uma alteração
explícita da configuração.

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
condição falhou. Campos ausentes ou fora dos limites do DTO são rejeitados pelo
FastAPI com `422`; um e-mail que passa pelos limites do DTO, mas falha na
validação estrutural de domínio, é convertido pelo handler em `401`. Os cards
implementados não configuram limitação de tentativas nem resposta `429`. Se o
caso de uso de acesso ou o criador de sessões não estiver configurado, responde
`503 Service Unavailable` sem criar cookie.

### Encerrar sessão — `DELETE /sessao/atual`

A API revoga a sessão correspondente ao cookie, se houver, e remove o cookie
com `Max-Age=0`, `Path=/`, `Secure`, `HttpOnly` e `SameSite=Lax`. Com o serviço
de revogação configurado, responde `204 No Content` quando o cookie está
ausente, desconhecido, expirado ou já revogado, tornando o encerramento
idempotente. Se o cookie estiver presente e o serviço de revogação indisponível,
responde `503` e não sinaliza sucesso. A revogação impede o uso do mesmo token
em requisições posteriores.

## Validação em rotas protegidas

O middleware comum de autenticação lê somente `__Host-sessao`, calcula seu
SHA-256 e busca o registro correspondente a cada requisição protegida. A sessão
é válida somente se:

1. o registro existe;
2. `revogada_em` é nulo;
3. `expira_em` é posterior ao instante UTC atual;
4. a conta existe e não está logicamente excluída (`deleted_at` nulo).

Se alguma condição falhar, o middleware responde `401` antes de chamar o
handler. Caso todas sejam satisfeitas, grava o UUID em
`request.state.usuario_id`. A autorização e a propriedade de recursos usam essa
identidade autenticada, nunca uma identidade enviada pelo cliente. A sessão não
concede papel ou permissão por si só.

### Comportamento HTTP do middleware

O middleware exige sessão em todas as rotas que não estejam explicitamente
liberadas. No estado atual, são públicas o cadastro `POST /estudantes`, o login
`POST /acessos`, o logout `DELETE /sessao/atual`, a documentação OpenAPI, os
health checks e requisições CORS `OPTIONS`. O token é lido somente do cookie;
valores em caminho, query, corpo ou `Authorization` não autenticam a chamada.

Não existe atualmente uma rota `GET /sessao/atual` para retornar a identidade da
sessão. A identidade validada fica disponível internamente ao handler por
`request.state.usuario_id`.

Falha de autenticação responde `401 Unauthorized` antes de executar o caso de
uso. Nas verificações de propriedade implementadas, uma sessão válida que tenta
acessar o recurso de outro estudante responde `403 Forbidden`. O middleware
atual não mascara esses recursos com `404`. A propriedade compara o
identificador do recurso com o usuário autenticado, nunca com o proprietário
declarado pelo cliente.

### Classificação de rotas

O cadastro `POST /estudantes`, o login `POST /acessos`, o logout
`DELETE /sessao/atual`, as rotas de documentação e as verificações operacionais
estão liberados pelo middleware atual. Requisições `OPTIONS` também passam sem
autenticação. O login só cria sessão depois de validar credenciais e confirmar
que a conta não está excluída. A implementação destes cards não configura
limitação de tentativas nem proteção CSRF.

Qualquer operação que leia ou altere informações pessoais ou profissionais do
estudante DEVE exigir sessão. Na API atual, isso inclui:

| Operação | Regra de interface |
|---|---|
| `PUT /estudantes/{usuario_id}` | Permitir alteração somente quando o UUID da rota corresponder a `request.state.usuario_id`. |
| `DELETE /estudantes/atual` | Exigir sessão; o handler usa a identidade autenticada da requisição. |
| `PUT /estudantes/{usuario_id}/dados-contato` | Permitir alteração somente quando o UUID da rota corresponder à identidade autenticada. |
| Rotas sob `/estudantes/{usuario_id}/curriculos` | Exigir sessão e permitir acesso somente quando o UUID da rota corresponder à identidade autenticada. |

Outras rotas não públicas também exigem cookie válido por padrão do middleware.
Uma exceção precisa ser explicitamente adicionada à lista de rotas públicas e
ter sua exposição justificada.

### Testes de rotas protegidas

Cada rota protegida DEVE ter teste de API sem cookie de sessão que confirme
`401 Unauthorized`, ausência de execução do caso de uso e ausência de alteração
de estado. Use entrada válida para isolar autenticação de erros de validação.
Cubra também cookie inválido, sessão expirada ou revogada e sessão válida. No
caso válido, confirme que o identificador recebido pelo caso de uso veio do
contexto autenticado e que valores enviados pelo cliente não permitem acesso à
conta de outra pessoa.

Os testes devem substituir a dependência de autenticação e os executores por
doubles determinísticos, sem banco ou relógio real. Testes unitários de API
executam no ambiente `backend`; testes de integração que exercitem persistência
ou infraestrutura seguem o ambiente `tests` definido no `AGENTS.md` raiz.

## Rastreabilidade das entregas de autenticação

Este contrato consolida as decisões e comportamentos implementados pelas
atividades #80 a #87.

| Issue | Entrega | Reflexo neste contrato |
|---|---|---|
| #80 | Definir contrato de credenciais de sessão | Define formato, transporte, validade e regras da credencial de sessão |
| #81 | Emitir token de acesso no login | Login válido cria token opaco e envia o cookie de sessão |
| #82 | Persistir sessão revogável do estudante | Sessão possui registro persistido, validade e estado de revogação |
| #83 | Implementar middleware de autenticação | Rotas privadas validam a sessão antes de executar o handler |
| #84 | Proteger rota de perfil com middleware | Operações de perfil exigem identidade autenticada e propriedade |
| #85 | Proteger rota de currículo com middleware | Operações de currículo exigem sessão e respeitam a identidade autenticada |
| #86 | Registrar revogação de sessão no logout | Logout revoga a sessão apresentada e remove o cookie |
| #87 | Testar respostas não autenticadas do middleware | Cookie ausente ou sessão inválida resulta em resposta uniforme `401 Unauthorized` |

A documentação deve acompanhar alterações futuras nesses contratos. Mudanças no
formato da credencial, duração da sessão, atributos do cookie, rotas públicas,
regras de revogação ou forma de propagação da identidade autenticada exigem
revisão deste documento.

## Resumo do contrato

| Item | Decisão atual |
|---|---|
| Método de autenticação | E-mail e senha |
| Tipo de sessão | Sessão opaca mantida no servidor |
| Transporte | Cookie HTTP |
| Nome do cookie | `__Host-sessao` |
| Token | 32 bytes aleatórios codificados em Base64 URL-safe |
| Persistência do token | Somente SHA-256 |
| Duração | 8 horas |
| Renovação automática | Não |
| Sessões simultâneas | Permitidas |
| Logout | Revoga somente a sessão atual |
| Cookie `Secure` | Sim |
| Cookie `HttpOnly` | Sim |
| `SameSite` | `Lax` |
| Rotas protegidas sem sessão | `401 Unauthorized` |
| Identidade autenticada | `request.state.usuario_id` |
| Sessão revogada | Não autentica |
| Sessão expirada | Não autentica |
| Conta excluída | Sessões deixam de autenticar |

## Limites e controles ainda não implementados

O cookie `SameSite=Lax` é uma defesa adicional, mas o fluxo descrito não
implementa validação de `Origin`, token CSRF nem limitação de tentativas de
login. Esses controles precisam de definição e implementação próprias antes de
serem tratados como garantias do sistema. Em produção, credenciais e cookies
devem trafegar por HTTPS.

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
