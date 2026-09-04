# Requisitos funcionais — Sistema Currículo

## Objetivo e escopo

Consolidar as funcionalidades da plataforma de apoio à preparação e construção de currículos profissionais para estudantes da FATEC-SP e de outros cursos da instituição, estudantes em busca de estágio e alunos próximos à conclusão do curso.

Fonte: [descrição_atividades.md](descrição_atividades.md) e definições fornecidas pelo responsável pelo projeto durante o levantamento de requisitos.

Os identificadores da versão inicial foram preservados. RF02 e RF07 são requisitos derivados do fluxo de uso, mantidos nesta consolidação. Os demais se baseiam nas funcionalidades descritas no documento ou nas definições posteriores do responsável pelo projeto.

## Cadastro e organização das informações

| ID | Requisito |
|---|---|
| RF01 | O sistema deve permitir cadastrar dados pessoais, formação acadêmica, experiências e competências do estudante. |
| RF02 | O sistema deve permitir consultar, editar e excluir as informações cadastradas. |
| RF03 | O sistema deve centralizar as informações do estudante para utilização na construção de seus currículos. |
| RF04 | O sistema deve permitir registrar projetos acadêmicos e oferecer orientação para descrevê-los de forma clara e objetiva. |

## Construção, revisão e exportação de currículos

| ID | Requisito |
|---|---|
| RF05 | O sistema deve orientar o estudante na estruturação e organização das seções do currículo. |
| RF06 | O sistema deve disponibilizar modelos de currículo com layouts profissionais para seleção pelo estudante. |
| RF07 | O sistema deve gerar uma visualização do currículo com as informações cadastradas e o modelo selecionado. |
| RF08 | O sistema deve oferecer revisão guiada do conteúdo e da organização do currículo. |
| RF09 | O sistema deve permitir exportar currículos nos formatos PDF e DOCX para compartilhamento com recrutadores. |
| RF14 | O sistema deve permitir que cada estudante crie, consulte, edite e exclua múltiplos currículos vinculados à sua conta. |
| RF15 | O sistema deve permitir selecionar qual currículo será exportado ou associado a uma vaga. |

O assistente de descrição de projetos e a revisão guiada não exigem inteligência artificial. A possibilidade de incorporar um módulo de IA está prevista nos requisitos de modularidade do documento de [requisitos não funcionais](requisitos_nao_funcionais.md).

## Busca de vagas e associações

| ID | Requisito |
|---|---|
| RF10 | O sistema deve consultar uma ferramenta de busca de vagas por meio de API e processar a lista de vagas retornada em JSON. |
| RF11 | O sistema deve apresentar os resultados da busca de vagas em uma página web. |
| RF12 | O sistema deve permitir que o estudante crie manualmente associações entre seus currículos e vagas, com uma ou mais classificações entre interesse, compatibilidade e candidatura, e deve armazenar essas associações e suas classificações em banco de dados. |

### Regras de negócio das associações

| ID | Regra |
|---|---|
| RN01 | A criação de uma associação currículo–vaga deve ser sempre iniciada manualmente pelo estudante. |
| RN02 | Uma mesma associação currículo–vaga pode ter mais de uma classificação simultaneamente, inclusive as três: interesse, compatibilidade e candidatura. |
| RN03 | Candidatura implica interesse. Toda associação classificada como candidatura deve também possuir a classificação interesse, e essa condição deve ser preservada em qualquer alteração. |
| RN04 | Compatibilidade é uma classificação atribuída manualmente pelo estudante; não exige cálculo automático de aderência entre currículo e vaga. |

A inclusão de interesse como consequência de uma candidatura manual atende à RN03 e não constitui criação automática de uma associação.

| Classificações da associação | Situação |
|---|---|
| Interesse | Permitida |
| Compatibilidade | Permitida |
| Candidatura | Não permitida sem interesse |
| Interesse e compatibilidade | Permitida |
| Interesse e candidatura | Permitida |
| Compatibilidade e candidatura | Não permitida sem interesse |
| Interesse, compatibilidade e candidatura | Permitida |

O registro da classificação candidatura não define, por si só, uma funcionalidade de envio de currículos ou realização de candidaturas em serviços externos.

## Autenticação

| ID | Requisito |
|---|---|
| RF13 | O sistema deve exigir autenticação para acesso às informações pessoais e aos currículos do estudante. |

O controle de autorização sobre dados pessoais, currículos e associações está definido no RNF04.

## Definições pendentes

- Provedor da API de vagas.
- Parâmetros de busca de vagas e campos apresentados nos resultados.
- Método de autenticação e existência de perfis de acesso distintos.

## Detalhamentos ainda necessários

Os pontos abaixo não representam funcionalidades adicionais aprovadas; são decisões necessárias ao detalhamento dos fluxos:

- Campos obrigatórios, validações e limites dos dados cadastrados.
- Modelos de currículo e orientações oferecidas pelo assistente e pela revisão guiada.
- Como alterações nas informações centralizadas afetam currículos já existentes.
- Comportamento da interface ao tentar retirar interesse de uma associação com candidatura, sempre preservando a RN03.
- Fluxo de consulta, alteração e exclusão das associações, além da criação manual já definida.
- Tratamento das associações quando um currículo for excluído ou uma vaga deixar de estar disponível.
