# Requisitos não funcionais — Sistema Currículo

## Objetivo e origem

Consolidar os atributos de qualidade e as restrições arquiteturais da plataforma de apoio à construção de currículos profissionais.

Fonte: [descrição_atividades.md](descrição_atividades.md) e definições fornecidas pelo responsável pelo projeto durante o levantamento de requisitos. As funcionalidades relacionadas constam em [requisitos_funcionais.md](requisitos_funcionais.md).

Os identificadores da versão inicial foram preservados. O documento de origem não estabelece metas quantitativas de qualidade. Os requisitos abaixo distinguem definições confirmadas de propostas derivadas que ainda precisam de validação; critérios de verificação propostos não representam metas já aprovadas.

## Requisitos consolidados

| ID | Categoria | Requisito | Origem ou situação |
|---|---|---|---|
| RNF01 | Usabilidade | A interface deve ser simples e compreensível para estudantes sem experiência na elaboração de currículos. | Derivado do objetivo do projeto; critério de aceitação a validar. |
| RNF02 | Acessibilidade | A interface deve oferecer recursos de acessibilidade, incluindo navegação por teclado, identificação dos campos e apresentação compreensível de erros. | Proposta derivada; escopo e metas a definir. |
| RNF03 | Compatibilidade e adaptação da interface | A interface web deve manter suas funcionalidades em computadores e dispositivos móveis. | Proposta derivada; dispositivos e navegadores suportados a definir. |
| RNF04 | Segurança e autorização | O sistema deve proteger dados pessoais, currículos e associações com vagas, permitindo consulta e alteração somente por usuários autorizados. | Derivado da proteção dos dados e da autenticação confirmada; regras de autorização a detalhar. |
| RNF05 | Integridade dos dados | A persistência deve preservar a integridade das associações entre currículos e vagas, impedir referências inválidas e garantir que toda associação com candidatura também possua interesse. | Derivado da persistência prevista e da regra de negócio confirmada. |
| RNF06 | Tolerância a falhas de integração | O sistema deve tratar indisponibilidade, demora e respostas inválidas da API de vagas de forma controlada, apresentando mensagem compreensível e preservando as informações dos currículos. | Proposta derivada da integração externa. |
| RNF07 | Qualidade da exportação | A exportação em PDF e DOCX deve preservar o conteúdo, a organização e a legibilidade do currículo, sem cortes ou sobreposições. | Derivado dos dois formatos confirmados e da proposta de layouts profissionais. |
| RNF08 | Desempenho | As operações de salvar dados, visualizar currículos, exportar currículos e consultar vagas devem responder em tempos adequados ao uso interativo. | Proposta derivada; metas mensuráveis a definir. |
| RNF09 | Modularidade e extensibilidade | O assistente de descrição de projetos e a revisão guiada devem possuir arquitetura modular e plugável, com interfaces definidas que permitam adicionar ou substituir módulos, inclusive de inteligência artificial, sem alterar o fluxo principal de criação de currículos. | Confirmado pelo responsável pelo projeto. |
| RNF10 | Independência de módulo opcional | O fluxo principal de criação, edição e exportação de currículos deve funcionar sem um módulo de inteligência artificial instalado ou habilitado. | Consequência proposta do caráter opcional da IA. |

## Critérios de verificação propostos

| Requisito | Verificação |
|---|---|
| RNF01 | Observar estudantes representativos realizando cadastro de informações e exportação de um currículo sem auxílio externo; taxa de sucesso e tempo esperado a definir. |
| RNF02 | Verificar navegação por teclado, identificação dos campos e compreensão das mensagens de erro; padrão de referência e nível de conformidade a definir. |
| RNF03 | Executar os fluxos principais na matriz de navegadores, dispositivos e tamanhos de tela que vier a ser aprovada. |
| RNF04 | Verificar que usuários não autenticados ou sem autorização não conseguem consultar ou alterar dados protegidos de outro estudante. |
| RNF05 | Verificar a rejeição de referências inválidas e de estados em que candidatura exista sem interesse; validar o tratamento de exclusões conforme a regra que vier a ser definida. |
| RNF06 | Simular indisponibilidade, tempo limite excedido e JSON inválido; verificar mensagens de erro e preservação dos dados dos currículos. |
| RNF07 | Exportar currículos em PDF e DOCX e conferir conteúdo, legibilidade e organização nos modelos suportados; aplicativos usados para validar DOCX a definir. |
| RNF08 | Medir os tempos das operações sob carga e volume de dados acordados; limites, percentis e condições de medição a definir. |
| RNF09 | Demonstrar a inclusão ou substituição de um módulo de assistência ou revisão usando a interface definida, sem alterar o fluxo principal de criação do currículo. |
| RNF10 | Executar criação, edição e exportação de currículos com o módulo de IA ausente ou desabilitado. |

## Definições pendentes

- **Desempenho:** limites de tempo de resposta, volume de dados e quantidade de usuários simultâneos.
- **Disponibilidade:** meta de disponibilidade, período de medição e condições de manutenção; nenhum valor foi definido.
- **Acessibilidade:** padrão de referência, nível de conformidade e metas de verificação.
- **Autenticação e autorização:** método de autenticação, existência de perfis distintos e regras específicas de acesso.
- **Integração de vagas:** provedor da API, parâmetros de busca e campos retornados, que influenciarão os limites e o tratamento de falhas.

## Detalhamentos ainda necessários

- Matriz de navegadores e dispositivos suportados.
- Aplicativos e versões utilizados para verificar os arquivos DOCX exportados.
- Política de tratamento das associações na exclusão de currículos ou indisponibilidade de vagas.
- Contratos dos módulos plugáveis, incluindo entradas, saídas e tratamento de falhas.

A integração com inteligência artificial é uma possibilidade futura. Sua implementação não é obrigatória nesta definição de escopo; a arquitetura deve estar preparada para recebê-la.
