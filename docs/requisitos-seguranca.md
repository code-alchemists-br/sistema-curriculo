# Requisitos de Segurança

## Requisitos funcionais - Autenticação

**RF-AUT-01**
O sistema deverá permitir o cadastro de usuários mediante e-mail e senha.

**RF-AUT-02**
O sistema deverá permitir que usuários cadastrados realizem login utilizando suas credenciais.

**RF-AUT-03**
O sistema deverá manter uma conta persistente associada ao usuário.

**RF-AUT-04**
O sistema deverá permitir que o usuário encerre sua sessão por meio da função de logout.

**RF-AUT-05**
O sistema deverá disponibilizar mecanismo de recuperação de senha.

**RF-AUT-06**
O sistema deverá permitir a alteração da senha pelo usuário autenticado.

**RF-AUT-07**
O sistema deverá utilizar mecanismos seguros para armazenamento das senhas, não mantendo as credenciais em texto puro.

**RF-AUT-08**
O sistema deverá proteger o mecanismo de autenticação contra tentativas excessivas de acesso.

**RF-AUT-09**
O sistema deverá utilizar comunicação segura entre cliente e servidor durante o processo de autenticação.

**RF-AUT-10**
O sistema deverá controlar a validade das sessões autenticadas.

## Requisitos funcionais - Autorização

**RF-AUTZ-01**
O sistema deverá controlar o acesso às funcionalidades de acordo com as permissões do usuário autenticado.

**RF-AUTZ-02**
O sistema deverá possuir, inicialmente, os papéis de usuário comum e administrador.

**RF-AUTZ-03**
O usuário comum deverá acessar somente os dados e recursos pertencentes à sua própria conta.

**RF-AUTZ-04**
O usuário deverá poder criar, visualizar, editar e excluir seus próprios currículos, conforme as funcionalidades disponibilizadas pelo sistema.

**RF-AUTZ-05**
O sistema deverá impedir que um usuário acesse ou modifique currículos pertencentes a outro usuário.

**RF-AUTZ-06**
O sistema deverá verificar a autorização no servidor para todas as operações protegidas.

**RF-AUTZ-07**
O sistema não deverá confiar exclusivamente em identificadores fornecidos pelo cliente para determinar a autorização de acesso a um recurso.

**RF-AUTZ-08**
As permissões administrativas deverão ser concedidas somente aos usuários que possuam o papel correspondente.

**RF-AUTZ-09**
O sistema deverá aplicar o princípio do menor privilégio às permissões dos usuários e componentes do sistema.

**RF-AUTZ-10**
O sistema deverá negar, por padrão, operações para as quais o usuário não possua autorização explícita.

**RF-AUTZ-11**
Caso seja implementado compartilhamento de currículos, o sistema deverá permitir definir o nível de visibilidade do recurso.

**RF-AUTZ-12**
Operações administrativas relevantes deverão ser registradas para fins de auditoria.

## Requisitos funcionais - Proteção de dados

**RF-DADOS-01**
O sistema deverá coletar somente os dados necessários para suas funcionalidades.

**RF-DADOS-02**
O sistema deverá proteger os dados pessoais contra acesso, alteração, divulgação ou exclusão não autorizados.

**RF-DADOS-03**
A transmissão de dados entre cliente e servidor deverá utilizar comunicação segura.

**RF-DADOS-04**
As senhas deverão ser armazenadas de forma segura, não sendo mantidas em texto puro.

**RF-DADOS-05**
O acesso aos dados deverá ser condicionado à autenticação, autorização e, quando aplicável, à propriedade do recurso.

**RF-DADOS-06**
Os currículos deverão ser privados por padrão.

**RF-DADOS-07**
O sistema deverá controlar o acesso aos arquivos e documentos gerados.

**RF-DADOS-08**
O sistema não deverá armazenar credenciais ou tokens em código-fonte ou logs.

**RF-DADOS-09**
Os backups deverão possuir proteção e controle de acesso adequados.

**RF-DADOS-10**
O sistema deverá possuir política de retenção e exclusão de dados.

**RF-DADOS-11**
O sistema deverá permitir, conforme aplicável, que o usuário consulte, altere e solicite a exclusão de seus dados.

**RF-DADOS-12**
Operações relevantes relacionadas aos dados deverão poder ser auditadas sem exposição desnecessária de informações pessoais ou credenciais.
