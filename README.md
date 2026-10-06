# sistema-curriculo — Projeto de Apoio Profissional

## Sobre o projeto

Este projeto propõe uma plataforma de apoio profissional para ajudar estudantes a reunir, organizar e apresentar suas experiências de forma clara e estratégica na preparação para o mercado de trabalho.

## Objetivo geral

Criar um sistema que apoie alunos na preparação e construção de um currículo profissional.

## Público-alvo

- Alunos da FATEC-SP e de outros cursos da instituição;
- Estudantes em busca de estágio;
- Alunos próximos à conclusão do curso.

## Problema que resolve

Muitos alunos encontram dificuldade para:

- Organizar informações pessoais e profissionais;
- Planejar a estrutura do currículo;
- Descrever projetos acadêmicos com objetividade;
- Construir um currículo com layout profissional;
- Busca de vagas.

## Proposta de solução

A plataforma poderá centralizar as informações do estudante e guiá-lo na criação de currículos melhores, com recursos como:

- Cadastro de dados pessoais, formação, experiências e competências;
- Assistente para descrição de projetos acadêmicos;
- Modelos de currículo com layouts profissionais;
- Revisão guiada de conteúdo e organização;
- Exportação do currículo para compartilhamento com recrutadores;
- O sistema deve acessar uma engine de busca via API para coletar uam lista de vagas via json;
- Deve mostrar os resutados da busca de vagas numa página web;
- A associação entre currículo e vagas deve ser guardada num banco de dados.

## Impacto esperado

Facilitar a entrada dos estudantes no mercado de trabalho, tornando a construção do currículo mais simples, organizada e acessível.


---

# Equipe e Atribuições

| Pessoa | Função |
| --- | --- |
| André Luiz da Silva Lima | Funcionalidades de vagas e associações currículo–vaga; integração com o Sistema Externo do Grupo 2; módulo opcional de recrutador/empresa parceira |
| Ricardo Galdino de Sampaio | Front End/UI/UX |
| Nathan Campos Nagano | Front End/UI/UX |
| Kelly Daiane Miranda Mendes | CI&CD/Ambientes e Cross-Cutting; implementação do sistema de login em middleware |
| Maria Carolina Cardozo Yamamoto | Funcionalidades de informações complementares (competências, idiomas, cursos, certificações, projetos e links profissionais) e armazenamento de documentos complementares |
| Vinicius Regazio Farias | Gestão de versões de currículo; revisão e visualização do currículo; geração, exportação e download em PDF e DOCX |
| Matheus Gnann Cardoso | Funcionalidades de perfil e dados pessoais; formação acadêmica; experiências profissionais |
| Daniel Lacerda Xavier | Testes/Controle de qualidade |
| Gustavo Minoru Haga |  Testes/Controle de qualidade|
| Thiago Jose Miranda Matias | Documentação |
| Marcelo Aparecido da Rosa | Documentação |
| Rodolpho P. M. Ferreira | Gerente de projeto/líder técnico e QA arquitetural|


# Descrição das Camadas e/ou Funções

- **Front End/UI/UX**: Responsáveis pelo design de UX e implementação de UI.

- **Testes/Controle de qualidade**: Responsáveis pelos testes integrados e E2E. Avaliação do design de UX bem como os testes da UI. Testes do backend. Criação de `doubles` de testes para si mesmos e para outros membros da equipe conforme necessidade. Os atributos de qualidade observados aqui se referem a todos que são obseváveis pela execução do sistema tais como aderencia às funcionalidades pretendidas bem como certos requisitos não funcionais como resiliência

- **CI&CD/Ambientes**: Responsável pelo estabelecimento, mudança e manutenção de ambientes de desenvolvimento, testes e produção. Controla o repositório e seus acessos e outros mecanismos de automação de implantação.

- **Backend - camada 'interface adapters' e 'frameworks and drives'**: Responsáveis pelas camadas mais externas do sistema como interfaces de comunição voltadas para o usuário (web) e orquestração.

- **Backend - camada domain e 'use cases'**: Responsáveis pelo núcleo e pela camada de orquestração.

- **Documentação**: Documentação geral. Verificação de comentários no código. Pode documentar tanto por comentários como por documentos externos. Verifica se a documentação e o código ou arquitetura estão compatíveis e sincronizados.

- **Cross-Cutting**: observabilidade: implementação e avaliação de logging e outras telemetrias de código, resiliência, segurança e autorização.

- **QA arquitetural**: Controle da qualidade referente a todos que não são obseváveis pela execução do sistema como manutenibilidade etc.
