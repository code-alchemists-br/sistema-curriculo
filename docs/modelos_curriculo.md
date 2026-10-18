# Modelos de currículo

## Objetivo

Definir um catálogo inicial de modelos de currículo que permita adequar a
apresentação ao objetivo profissional do estudante sem duplicar os dados do seu
perfil. Cada versão de currículo reutiliza os mesmos itens cadastrados e escolhe
um modelo para determinar a ordem, a visibilidade e a apresentação das seções.

## Catálogo inicial

O sistema terá seis modelos base. Não haverá um modelo exclusivo por profissão:
as diferenças entre áreas serão atendidas pela configuração de seções do modelo
e pelo conteúdo selecionado para cada versão de currículo.

| Modelo | Público principal | Características |
| --- | --- | --- |
| ATS simples | Candidaturas em plataformas de recrutamento | Layout de uma coluna, leitura direta e sem elementos gráficos que prejudiquem sistemas ATS. |
| Profissional clássico | Administração, finanças, direito e áreas tradicionais | Hierarquia visual sóbria e foco em experiência e formação. |
| Moderno | Tecnologia, produto, marketing e negócios | Apresentação contemporânea, com destaque equilibrado para competências, projetos e experiência. |
| Criativo | Design, audiovisual, comunicação e portfólio | Maior liberdade visual para destacar identidade profissional e projetos. |
| Acadêmico/pesquisador | Docentes, mestrandos, doutorandos e pesquisadores | Valoriza produção científica, formação e atividades de pesquisa. |
| Primeiro emprego | Estágio, trainee e pessoas com pouca experiência | Evidencia formação, projetos, competências e atividades relevantes antes da experiência profissional. |

## Modelo acadêmico/pesquisador

Para currículos acadêmicos, as seções devem aparecer preferencialmente na ordem
abaixo, ocultando seções que não possuam itens selecionados:

1. Identificação e contatos profissionais.
2. Resumo ou objetivo acadêmico.
3. Formação acadêmica.
4. Linhas de pesquisa e áreas de interesse.
5. Publicações e produção científica.
6. Projetos de pesquisa e extensão.
7. Bolsas, prêmios e certificações.
8. Docência, monitoria, orientação e experiência profissional relevante.
9. Participação em eventos.
10. Competências técnicas e idiomas.

As seções de publicações, linhas de pesquisa, bolsas, atividades de docência e
eventos poderão exigir novos tipos de itens no perfil. Enquanto esses itens não
existirem no domínio, o modelo deve apresentar somente as seções já suportadas,
como formação, projetos, competências, idiomas e documentos.

## Princípios de implementação

- Os dados do currículo permanecem estruturados e independentes do layout.
- A troca de modelo não remove nem altera os itens selecionados pelo estudante.
- Cada modelo define a ordem, a ênfase visual e as seções opcionais, mas não
  altera o significado dos dados.
- Modelos voltados a ATS devem priorizar conteúdo textual, títulos de seção
  claros e estrutura simples.
- Novos modelos só devem ser adicionados quando representarem uma necessidade
  de apresentação distinta que não possa ser atendida pela configuração dos
  modelos existentes.

## Seleção orientada por categoria

Ao criar uma versão de currículo, a interface deve apresentar um campo de
seleção denominado **Objetivo do currículo**. Esse campo pode ser implementado
como um dropdown com as seguintes categorias iniciais:

- Primeiro emprego / estágio.
- Tecnologia.
- Administrativo / corporativo.
- Criativo / design.
- Acadêmico / pesquisador.
- Outro.

A categoria escolhida serve para orientar, e não restringir, a escolha de
layout. O sistema recomenda um modelo inicial e informa de forma clara o motivo
da recomendação. Por exemplo: "Recomendamos o modelo Acadêmico porque seu
objetivo é pesquisa."

| Categoria | Modelo inicialmente recomendado |
| --- | --- |
| Primeiro emprego / estágio | Primeiro emprego |
| Tecnologia | Moderno |
| Administrativo / corporativo | ATS simples ou Profissional clássico |
| Criativo / design | Criativo |
| Acadêmico / pesquisador | Acadêmico/pesquisador |
| Outro | Moderno |

Após receber a recomendação, o estudante pode selecionar qualquer modelo do
catálogo. A interface pode exibir os modelos em cards e utilizar um segundo
dropdown ou a própria seleção dos cards para confirmar o layout final. Dessa
forma, a orientação reduz escolhas inadequadas para pessoas iniciantes, sem
retirar a autonomia de quem já sabe qual apresentação deseja usar.
