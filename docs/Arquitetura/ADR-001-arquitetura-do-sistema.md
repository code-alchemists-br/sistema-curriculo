# ADR-001 — Arquitetura do Sistema Currículo

* **Status:** Proposta
* **Data:** 2026-09-15
* **Projeto:** Sistema Currículo

## 1. Contexto

O Sistema Currículo tem como objetivo apoiar principalmente alunos da FATEC-SP na preparação, construção, gerenciamento e exportação de seus currículos.

O sistema possui como ator principal o **Aluno**, que pode cadastrar seus dados pessoais, formação acadêmica, experiências profissionais, habilidades e idiomas, armazenar documentos complementares, manter diferentes versões de currículo e gerar/exportar seus currículos.

O sistema também prevê integração com o **Sistema Externo do Grupo 2**, por meio de API, para permitir a comunicação e sincronização de informações entre os sistemas.

O módulo de recrutamento, envolvendo busca, filtragem e visualização de currículos por recrutadores ou empresas parceiras, é considerado **opcional** e não faz parte do escopo principal quando o foco está no apoio ao aluno.

## 2. Decisões arquiteturais

### 2.1. Arquitetura do backend

O backend será estruturado de forma a separar as responsabilidades da aplicação, buscando manter o domínio independente dos detalhes externos de infraestrutura e comunicação.

A arquitetura deve permitir a separação entre:

* domínio e regras de negócio;
* casos de uso e regras de aplicação;
* interfaces de comunicação com o sistema;
* mecanismos de persistência e demais detalhes de infraestrutura.

Essa separação tem como objetivo facilitar a manutenção, evolução e realização de testes no sistema.

### 2.2. Organização do domínio

As regras relacionadas ao funcionamento do Sistema Currículo devem permanecer concentradas no domínio da aplicação.

Entidades, objetos de valor e regras de negócio não devem depender diretamente de detalhes específicos de infraestrutura.

A aplicação deve utilizar casos de uso para representar as operações realizadas pelo sistema, mantendo a lógica de aplicação separada dos mecanismos utilizados para entrada, saída e persistência dos dados.

### 2.3. Separação entre dados de entrada, domínio e persistência

Os dados recebidos pelas interfaces da aplicação devem ser tratados de forma separada das entidades e regras do domínio.

A arquitetura deve evitar que os modelos utilizados diretamente pela API ou pela persistência sejam utilizados indiscriminadamente como representação das regras de negócio.

Essa separação reduz o acoplamento entre as diferentes partes do sistema e facilita futuras alterações nas interfaces ou nos mecanismos de armazenamento.

### 2.4. Persistência dos dados

Os dados necessários ao funcionamento do Sistema Currículo devem ser persistidos de maneira estruturada, permitindo o armazenamento das informações dos usuários, currículos e demais dados necessários às funcionalidades previstas.

A evolução da estrutura do banco de dados deve ser controlada por mecanismos de migração, evitando alterações manuais não rastreáveis.

A tecnologia e a configuração definitiva da persistência devem permanecer alinhadas à implementação efetivamente adotada pelo projeto.

### 2.5. Organização do frontend

O frontend deve manter uma organização modular, separando responsabilidades de acordo com as funcionalidades e componentes da aplicação.

A estrutura deve favorecer a reutilização de componentes e a separação entre elementos de interface, funcionalidades e entidades utilizadas pela aplicação.

A organização definitiva deve acompanhar a estrutura efetivamente implementada no frontend.

### 2.6. Comunicação entre frontend e backend

A comunicação entre frontend e backend deve ocorrer por meio de interfaces bem definidas, permitindo que o frontend consuma as funcionalidades disponibilizadas pelo backend.

O backend deve concentrar as regras de negócio e o processamento das operações, enquanto o frontend deve ser responsável principalmente pela interação com o usuário e apresentação das informações.

### 2.7. Funcionalidades principais

A arquitetura deve suportar as funcionalidades previstas para o sistema, incluindo:

* cadastro de conta;
* login e recuperação de senha;
* cadastro de dados do currículo;
* cadastro de formação acadêmica;
* cadastro de experiência profissional;
* armazenamento de documentos complementares;
* gerenciamento de diferentes versões de currículo;
* geração de currículo;
* exportação do currículo em diferentes formatos;
* integração com o Sistema Externo do Grupo 2.

A documentação de casos de uso define que a exportação inclui obrigatoriamente a geração do currículo.

### 2.8. Integração com o Sistema Externo do Grupo 2

A integração com o Grupo 2 será realizada por meio de API.

O sistema deverá possuir uma interface de integração que permita a comunicação com o sistema externo sem acoplar as regras principais do domínio diretamente à implementação específica dessa integração.

A documentação também prevê a possibilidade de utilização de autenticação por token de API quando a política de segurança exigir.

### 2.9. Segurança e autenticação

A arquitetura deve considerar mecanismos de autenticação e proteção das informações dos usuários.

O sistema prevê cadastro de conta, login e recuperação de senha, portanto essas funcionalidades devem ser tratadas como parte da camada de acesso da aplicação.

As credenciais e informações de autenticação devem ser tratadas de forma segura, evitando exposição indevida de dados sensíveis.

A comunicação com sistemas externos também deve considerar mecanismos de autenticação apropriados, incluindo token de API quando aplicável.

### 2.10. Controle de acesso aos currículos

O acesso às informações dos currículos deve respeitar as permissões associadas ao usuário e ao contexto de utilização do sistema.

O aluno deve possuir controle sobre os dados relacionados aos seus próprios currículos.

Caso o módulo de recrutamento seja incluído no escopo, deverão ser definidas regras específicas para determinar quais currículos podem ser consultados por recrutadores ou empresas parceiras.

Como esse módulo é considerado opcional na documentação atual, suas regras definitivas de autorização permanecem dependentes da confirmação do escopo.

### 2.11. Modularidade

As funcionalidades opcionais devem ser mantidas de maneira modular para evitar que alterações em um módulo causem dependências desnecessárias em outras partes do sistema.

Essa abordagem é especialmente importante para o módulo de recrutamento e para integrações externas, que podem sofrer alterações de escopo durante o desenvolvimento.

### 2.12. Testes e qualidade

As alterações de comportamento do sistema devem ser acompanhadas dos testes pertinentes.

De acordo com as regras do projeto, testes unitários devem ser executados no ambiente do componente correspondente, enquanto testes de integração, sistema, end-to-end ou de nível superior devem utilizar o ambiente de testes definido pelo projeto.

### 2.13. Documentação

A documentação deve acompanhar a evolução da implementação.

As regras do projeto determinam que funções, classes e DTOs possuam documentação equivalente a docstrings, explicando o que fazem, como funcionam e qual finalidade atendem. A documentação também deve refletir o comportamento atual do código e ser atualizada junto com alterações correspondentes.

Além da documentação do código, os documentos arquiteturais e funcionais devem permanecer alinhados ao estado atual do sistema.

### 2.14. Ambiente de desenvolvimento

O desenvolvimento do projeto deve utilizar os ambientes Nix definidos no repositório.

O ambiente correspondente deve ser selecionado de acordo com a atividade:

* `nix develop .#backend` para atividades do backend;
* `nix develop .#frontend` para atividades do frontend;
* `nix develop .#tests` para testes de integração e níveis superiores.

As operações de Git e GitHub possuem exceção específica e podem ser realizadas fora do ambiente Nix.

## 3. Consequências

A adoção dessas decisões proporciona uma organização com responsabilidades separadas, facilitando a manutenção e evolução do Sistema Currículo.

A separação entre domínio, aplicação, interfaces e infraestrutura reduz o acoplamento entre as partes do sistema e permite que componentes sejam modificados sem exigir alterações generalizadas.

A utilização de interfaces para comunicação com sistemas externos também facilita a manutenção da integração com o Grupo 2.

Por outro lado, a separação das responsabilidades aumenta a quantidade de estruturas e arquivos do projeto, exigindo que a equipe mantenha uma organização consistente e atualize a documentação conforme o sistema evolui.

A existência de funcionalidades opcionais também exige que o escopo seja controlado para evitar a implementação de módulos que não façam parte da versão atual do projeto.

## 4. Decisões ainda pendentes

Alguns pontos não possuem definição suficientemente consolidada nos documentos analisados e, portanto, não devem ser tratados como decisões definitivas neste ADR:

* mecanismo específico de autenticação utilizado pelo sistema;
* tecnologia e configuração definitiva de persistência, caso ainda não estejam consolidadas na implementação;
* regras definitivas de autorização para recrutadores ou empresas parceiras;
* especificação definitiva da API do Grupo 2;
* formato final e parâmetros da comunicação com o Grupo 2;
* requisitos quantitativos de desempenho e disponibilidade;
* regras definitivas para armazenamento e exclusão de documentos;
* implementação definitiva das funcionalidades opcionais.

Esses pontos devem ser atualizados neste ADR ou documentados em ADRs específicos quando forem definidos pelo projeto.

## 5. Referências

* `fundamentos-backend.md`
* `requisitos_funcionais.md`
* `requisitos_nao_funcionais.md`
* `requisitos-seguranca.md`
* `casos-de-uso-v2.md`
* `AGENTS.md`
* `src/backend/AGENTS.md`
* `src/frontend/AGENTS.md`

## 6. Observação

Este ADR consolida as decisões arquiteturais identificadas na documentação existente do projeto. Ele não substitui os documentos de requisitos ou as regras dos arquivos `AGENTS.md`.

Os arquivos `AGENTS.md` continuam sendo documentos de instrução do ambiente e do processo de desenvolvimento e não devem ser alterados como parte desta consolidação.
