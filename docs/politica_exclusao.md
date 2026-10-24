# Política de Exclusão de Dados e Recursos

## Objetivo

Este documento define a política de exclusão aplicável aos principais recursos do Sistema Currículo.

A decisão cobre:

- versões de currículo;
- associações entre currículo e vaga;
- documentos complementares;
- perfil e dados pessoais do estudante.

A política existe para tornar explícito quando uma exclusão é física ou lógica, como recursos relacionados devem ser tratados e quais garantias de autorização e integridade devem ser preservadas.

## Princípios gerais

Toda operação de exclusão deve respeitar os seguintes princípios:

- somente o proprietário ou uma operação explicitamente autorizada pode excluir um recurso;
- a autorização deve ser verificada no backend;
- um identificador enviado pelo cliente não constitui prova de propriedade;
- ausência do recurso e tentativa de acesso a recurso alheio não devem provocar vazamento desnecessário de informação;
- a exclusão deve preservar a integridade referencial;
- recursos relacionados não devem permanecer em estados inválidos;
- uma operação de exclusão não deve reativar recursos anteriormente excluídos;
- quando a exclusão for lógica, consultas normais devem ocultar o recurso excluído;
- quando a exclusão for física, os registros dependentes que impedem a remoção devem ser tratados de forma explícita;
- períodos de retenção e purga física que ainda não foram definidos não devem ser inventados nesta política.

## Matriz de exclusão

| Recurso | Política | Resultado esperado |
|---|---|---|
| Currículo | Exclusão física | A versão é removida definitivamente após validação de propriedade |
| Associação currículo-vaga | Exclusão física | A associação e suas classificações deixam de representar vínculo ativo |
| Documento complementar | Exclusão lógica | O registro é marcado com `deleted_at` e deixa de aparecer nas consultas normais |
| Perfil e dados pessoais | Exclusão lógica | O perfil é marcado com `deleted_at` e deixa de ser tratado como perfil ativo |

## Exclusão de currículo

A exclusão de uma versão de currículo é considerada **física**.

Após a validação de que o currículo pertence ao estudante autenticado, a versão pode ser removida definitivamente.

Antes da remoção da versão, os dados dependentes que utilizem o currículo como proprietário ou referência devem ser tratados para preservar a integridade do banco.

### Itens selecionados no currículo

As linhas que representam a seleção de itens da versão devem ser removidas antes ou juntamente com a exclusão do currículo.

A exclusão de uma versão de currículo não deve excluir os itens de perfil originais do estudante, como:

- formação acadêmica;
- experiência profissional;
- competências;
- idiomas;
- projetos;
- documentos complementares.

Esses itens pertencem ao perfil e podem ser utilizados em outras versões de currículo.

### Associações com vagas

Se o currículo possuir associações com vagas, essas associações devem ser removidas antes ou juntamente com a exclusão definitiva da versão.

Uma associação não deve permanecer referenciando um currículo inexistente.

As classificações pertencentes à associação também devem ser eliminadas junto com a associação.

A implementação concreta dessa remoção deve respeitar o contrato das operações de associação definido nas funcionalidades correspondentes.

## Exclusão de associação currículo-vaga

A associação entre currículo e vaga utiliza **exclusão física**.

A remoção elimina o vínculo ativo entre:

- a versão de currículo;
- a vaga;
- suas classificações associadas.

A remoção da associação:

- não exclui o currículo;
- não exclui a vaga externa;
- não exclui dados do perfil do estudante;
- deve remover ou invalidar as classificações vinculadas ao mesmo par currículo-vaga.

A associação é identificada pelo par:

`curriculo_id + vaga_id`

A operação deve respeitar a propriedade do currículo associado.

### Idempotência

As operações públicas de remoção devem seguir a decisão das funcionalidades específicas de associação.

As issues responsáveis pela remoção da associação devem garantir comportamento previsível para uma tentativa repetida de exclusão e impedir acesso indevido a associações de outro estudante.

## Exclusão de documento complementar

Documentos complementares utilizam **exclusão lógica**.

Ao solicitar a exclusão de um documento próprio:

- o registro deve permanecer persistido;
- `deleted_at` deve receber o instante da exclusão;
- consultas normais não devem retornar o documento;
- o documento não deve continuar disponível para download ou uso ativo;
- um estudante não pode excluir documento pertencente a outro usuário.

A exclusão lógica permite preservar o estado necessário enquanto a política de retenção e purga física ainda não estiver definida.

Esta decisão não estabelece um prazo automático para remoção física do registro ou do conteúdo armazenado.

## Exclusão do perfil e dos dados pessoais

A exclusão do perfil do estudante utiliza **exclusão lógica**.

Quando o estudante solicita a exclusão da própria conta ou perfil:

- o registro do usuário recebe `deleted_at`;
- o perfil deixa de ser considerado ativo;
- consultas normais não devem retornar o perfil como disponível;
- operações de edição não devem reativar implicitamente o usuário;
- novas operações que dependam de perfil ativo devem ser bloqueadas.

A exclusão deve ser idempotente: repetir a solicitação sobre o próprio perfil já excluído não deve gerar uma nova data de exclusão nem reativar o registro.

## Recursos pertencentes a um perfil excluído

A exclusão lógica do perfil não implica, nesta definição, purga física imediata de todos os recursos vinculados ao usuário.

Currículos, documentos, itens profissionais e demais recursos persistidos permanecem sujeitos às respectivas políticas de exclusão e retenção.

Uma política futura de purga poderá definir a remoção física coordenada desses dados.

Enquanto essa política não existir, recursos pertencentes a perfil excluído não devem voltar a ser disponibilizados por fluxos normais de usuário.

## Autorização

Toda operação de exclusão de recurso privado deve utilizar a identidade autenticada como fonte confiável.

O backend deve verificar a propriedade antes da exclusão.

Não deve ser suficiente enviar:

- `usuario_id`;
- `curriculo_id`;
- `documento_id`;
- `vaga_id`;

sem validação da identidade autenticada e da propriedade correspondente.

Tentativas de exclusão de recursos pertencentes a outro estudante devem ser recusadas.

## Integridade referencial

A exclusão deve respeitar relações entre registros.

Antes de remover fisicamente um recurso, a aplicação ou a persistência deve garantir que:

- dependências sejam removidas de forma apropriada;
- nenhuma chave estrangeira fique apontando para um registro inexistente;
- nenhuma associação semanticamente inválida seja preservada.

Não deve ser utilizada cascata indiscriminada para apagar dados que possuem ciclo de vida próprio.

## Exclusão lógica

Quando a política definir exclusão lógica, o campo `deleted_at` representa o estado removido.

As regras mínimas são:

- `deleted_at = NULL` representa recurso ativo;
- `deleted_at != NULL` representa recurso logicamente excluído;
- consultas de uso normal devem considerar apenas recursos ativos;
- edição não deve restaurar silenciosamente recurso excluído;
- a primeira data de exclusão deve ser preservada quando a operação for idempotente.

## Exclusão física

Quando a política definir exclusão física, o registro deixa de existir na persistência após a conclusão da operação.

A remoção deve ocorrer apenas depois das verificações de:

- existência;
- autorização;
- propriedade;
- integridade dos relacionamentos.

## Retenção e purga

Esta política não define prazo de retenção geral para dados pessoais, documentos ou perfis excluídos logicamente.

Também não define:

- quantidade de dias antes da purga;
- procedimento automático de purga;
- comportamento de backups após exclusão;
- prazo jurídico de retenção;
- anonimização definitiva.

Essas decisões dependem de uma política específica de retenção e governança de dados.

Até que essa política exista, a exclusão lógica não deve ser descrita como eliminação física definitiva dos dados.

## Logs e auditoria

Uma operação de exclusão pode gerar registro operacional ou de auditoria quando necessário.

Esses registros não devem armazenar:

- senhas;
- tokens;
- conteúdo completo de documentos;
- dados pessoais desnecessários.

A política de logs e seu prazo de retenção devem seguir os requisitos de segurança do projeto.

## Relação com o RNF05

Esta decisão detalha o tratamento de exclusões relacionado ao RNF05 — Integridade dos dados.

A integridade deve ser preservada durante a remoção de currículos, associações e demais recursos relacionados.

## Relação com segurança e proteção de dados

Esta política complementa os requisitos de segurança do projeto referentes a:

- propriedade dos recursos;
- autorização no backend;
- proteção de dados pessoais;
- retenção;
- exclusão;
- menor privilégio.

## Estado atual de implementação

A política representa a decisão esperada para o produto.

No estado atual do projeto:

- a exclusão física de versões de currículo já possui caso de uso;
- documentos complementares já utilizam exclusão lógica;
- o perfil do estudante já utiliza exclusão lógica;
- a remoção de associações currículo-vaga está sendo tratada pelas issues específicas responsáveis por essa funcionalidade.

A existência desta política não deve ser interpretada como evidência de que todas as operações descritas já estão implementadas.

## Rastreabilidade

- **Issue:** #170 — F1.3
- **Requisito relacionado:** RNF05 — Integridade dos dados
- **Requisitos de segurança relacionados:** autorização, propriedade, retenção e exclusão
- **WBS:** 1.1.1.4, 1.1.2.4, 1.2.1.4, 1.7.2.4, 1.8.2.4
