# Matriz de testes de aceitação — Sistema Currículo

## Objetivo e escopo

Consolidar os cenários de aceitação da plataforma de apoio à preparação e construção de currículos profissionais, com rastreabilidade a cada requisito funcional do documento [requisitos_funcionais.md](requisitos_funcionais.md).

Os identificadores dos requisitos (RF01 a RF15) e das regras de negócio (RN01 a RN04) foram preservados. Nenhum requisito foi criado ou alterado. Cada cenário referencia o ID do requisito funcional correspondente e, quando aplicável, a regra de negócio envolvida. A matriz cobre o comportamento definido nos requisitos e não pretende ser exaustiva.

## Convenções

| Item | Descrição |
|---|---|
| ID do cenário | Formato `CT-RFxx-nn`, em que `RFxx` é o requisito rastreado e `nn` é a sequência do cenário. |
| Tipo | **Positivo**: fluxo esperado com sucesso. **Negativo**: entrada ou ação inválida que deve ser rejeitada. **Exceção**: falha de ambiente ou serviço externo, ou condição atípica. |

Premissa geral: salvo indicação contrária, o estudante está autenticado (RF13).

## Cadastro e organização das informações

### RF01 — Cadastro de dados do estudante

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF01-01 | RF01 | Positivo | Cadastrar dados pessoais | Estudante autenticado sem dados pessoais cadastrados | Preencher os dados pessoais com valores válidos e salvar | Dados pessoais são salvos e confirmados ao estudante |
| CT-RF01-02 | RF01 | Positivo | Cadastrar formação acadêmica | Estudante autenticado | Informar uma formação acadêmica com valores válidos e salvar | Formação acadêmica é salva e passa a constar nas informações do estudante |
| CT-RF01-03 | RF01 | Positivo | Cadastrar experiência | Estudante autenticado | Informar uma experiência com valores válidos e salvar | Experiência é salva e passa a constar nas informações do estudante |
| CT-RF01-04 | RF01 | Positivo | Cadastrar competência | Estudante autenticado | Informar uma competência com valores válidos e salvar | Competência é salva e passa a constar nas informações do estudante |
| CT-RF01-05 | RF01 | Exceção | Falha ao gravar as informações | Estudante autenticado; banco de dados indisponível | Preencher dados válidos e salvar | Sistema informa que não foi possível salvar e não registra informação parcial |

### RF02 — Consulta, edição e exclusão das informações

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF02-01 | RF02 | Positivo | Consultar informações cadastradas | Estudante com dados pessoais, formação, experiência e competência cadastrados | Acessar a área de informações cadastradas | Todas as informações cadastradas são exibidas corretamente |
| CT-RF02-02 | RF02 | Positivo | Editar uma informação | Estudante com experiência cadastrada | Alterar um campo da experiência com valor válido e salvar | Alteração é salva e a consulta exibe o valor atualizado |
| CT-RF02-03 | RF02 | Positivo | Excluir uma informação | Estudante com competência cadastrada | Excluir a competência | Competência deixa de ser exibida na consulta |
| CT-RF02-04 | RF02 | Exceção | Editar ou excluir informação já removida | Informação removida em outra sessão do mesmo estudante | Tentar editar ou excluir a informação a partir de tela desatualizada | Sistema informa que a informação não existe mais e atualiza a listagem |

### RF03 — Centralização das informações

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF03-01 | RF03 | Positivo | Reutilizar informações na construção do currículo | Estudante com informações cadastradas | Iniciar a construção de um currículo | Informações cadastradas ficam disponíveis para uso, sem necessidade de nova digitação |
| CT-RF03-02 | RF03 | Positivo | Reutilizar as mesmas informações em currículos distintos | Estudante com informações cadastradas | Construir dois currículos | Ambos utilizam as informações do mesmo cadastro centralizado |
| CT-RF03-03 | RF03 | Negativo | Isolamento entre estudantes | Dois estudantes com cadastros distintos | Estudante A inicia a construção de um currículo | Somente as informações do estudante A são disponibilizadas |

### RF04 — Projetos acadêmicos e orientação de descrição

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF04-01 | RF04 | Positivo | Registrar projeto acadêmico | Estudante autenticado | Preencher os dados do projeto com valores válidos e salvar | Projeto é salvo e passa a constar nas informações do estudante |
| CT-RF04-02 | RF04 | Positivo | Receber orientação para descrever o projeto | Estudante na tela de registro de projeto | Acessar a orientação de descrição | Sistema apresenta orientação para descrever o projeto de forma clara e objetiva |
| CT-RF04-03 | RF04 | Positivo | Assistente funciona sem inteligência artificial | Módulo de IA não incorporado | Registrar um projeto utilizando a orientação | Orientação é apresentada normalmente, sem dependência de IA |

## Construção, revisão e exportação de currículos

### RF05 — Orientação para estruturação das seções

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF05-01 | RF05 | Positivo | Receber orientação sobre as seções | Estudante com informações cadastradas | Iniciar a construção de um currículo | Sistema orienta a estruturação e a organização das seções do currículo |
| CT-RF05-02 | RF05 | Positivo | Organizar as seções conforme a orientação | Orientação de seções apresentada | Organizar as seções do currículo seguindo a orientação | Currículo reflete a estrutura e a ordem de seções escolhidas |

### RF06 — Modelos de currículo

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF06-01 | RF06 | Positivo | Listar modelos disponíveis | Estudante construindo um currículo | Acessar a seleção de modelos | Sistema apresenta os modelos de currículo com layouts profissionais |
| CT-RF06-02 | RF06 | Positivo | Selecionar um modelo | Modelos listados | Selecionar um modelo | Modelo é associado ao currículo em construção |
| CT-RF06-03 | RF06 | Positivo | Trocar de modelo preservando o conteúdo | Currículo com modelo selecionado e conteúdo preenchido | Selecionar outro modelo | Novo modelo é aplicado e o conteúdo do currículo é mantido |

### RF07 — Visualização do currículo

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF07-01 | RF07 | Positivo | Gerar visualização do currículo | Informações cadastradas e modelo selecionado | Solicitar a visualização do currículo | Sistema exibe o currículo com as informações cadastradas no modelo selecionado |
| CT-RF07-02 | RF07 | Positivo | Visualização reflete alteração de modelo | Visualização gerada | Trocar o modelo e solicitar nova visualização | Visualização exibe o mesmo conteúdo no novo layout |
| CT-RF07-03 | RF07 | Positivo | Visualização reflete informação editada | Visualização gerada anteriormente | Editar uma informação do currículo e visualizar novamente | Visualização exibe o conteúdo atualizado |

### RF08 — Revisão guiada

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF08-01 | RF08 | Positivo | Executar revisão guiada de currículo adequado | Currículo com conteúdo e organização adequados | Iniciar a revisão guiada | Sistema conduz a revisão do conteúdo e da organização, sem apontar pendências indevidas |
| CT-RF08-02 | RF08 | Positivo | Revisão apresenta orientações de melhoria | Currículo com seções incompletas ou mal organizadas | Iniciar a revisão guiada | Sistema apresenta orientações sobre conteúdo e organização a serem ajustados |
| CT-RF08-03 | RF08 | Positivo | Revisão funciona sem inteligência artificial | Módulo de IA não incorporado | Iniciar a revisão guiada | Revisão é conduzida normalmente, sem dependência de IA |

### RF09 — Exportação em PDF e DOCX

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF09-01 | RF09 | Positivo | Exportar currículo em PDF | Currículo com modelo selecionado | Solicitar a exportação em PDF | Arquivo PDF é gerado com o conteúdo e o layout do currículo |
| CT-RF09-02 | RF09 | Positivo | Exportar currículo em DOCX | Currículo com modelo selecionado | Solicitar a exportação em DOCX | Arquivo DOCX é gerado com o conteúdo e o layout do currículo |
| CT-RF09-03 | RF09 | Positivo | Conteúdo exportado é consistente com a visualização | Currículo visualizado | Exportar nos dois formatos | Conteúdo dos arquivos corresponde ao exibido na visualização |
| CT-RF09-04 | RF09 | Negativo | Exportar sem estar autenticado | Usuário sem sessão ativa | Tentar acessar a exportação de um currículo | Acesso é negado e o usuário é direcionado à autenticação |
| CT-RF09-05 | RF09 | Exceção | Falha na geração do arquivo | Erro no processo de geração do arquivo | Solicitar a exportação | Sistema informa a falha e permite nova tentativa, sem entregar arquivo inválido |

### RF14 — Múltiplos currículos por estudante

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF14-01 | RF14 | Positivo | Criar múltiplos currículos | Estudante autenticado com um currículo | Criar um segundo currículo | Os dois currículos ficam vinculados à conta do estudante |
| CT-RF14-02 | RF14 | Positivo | Consultar currículos | Estudante com mais de um currículo | Acessar a listagem de currículos | Todos os currículos do estudante são listados |
| CT-RF14-03 | RF14 | Positivo | Editar um currículo | Estudante com mais de um currículo | Editar um dos currículos e salvar | Alteração é aplicada somente ao currículo editado |
| CT-RF14-04 | RF14 | Positivo | Excluir um currículo | Estudante com mais de um currículo | Excluir um dos currículos | Currículo excluído deixa de ser listado e os demais permanecem inalterados |
| CT-RF14-05 | RF14 | Negativo | Isolamento entre contas | Currículos de dois estudantes | Estudante A consulta seus currículos e tenta acessar um currículo do estudante B | Somente currículos do estudante A são exibidos e o acesso ao currículo de B é negado |

### RF15 — Seleção do currículo para exportação ou associação a vaga

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF15-01 | RF15 | Positivo | Selecionar currículo para exportação | Estudante com mais de um currículo | Escolher um currículo e exportá-lo | Somente o currículo escolhido é exportado |
| CT-RF15-02 | RF15 | Positivo | Selecionar currículo para associar a uma vaga | Estudante com mais de um currículo e vaga exibida | Escolher um currículo para a associação com a vaga | Currículo escolhido é o utilizado na associação |
| CT-RF15-03 | RF15 | Negativo | Exportar ou associar sem selecionar currículo | Estudante com currículos, nenhum selecionado | Tentar exportar ou associar sem escolher um currículo | Ação não é concluída e o sistema solicita a seleção de um currículo |
| CT-RF15-04 | RF15 | Negativo | Selecionar currículo de outro estudante | Currículo pertencente a outro estudante | Tentar selecionar esse currículo | Seleção é negada; apenas currículos da própria conta são selecionáveis |

## Busca de vagas e associações

### RF10 — Consulta à API de vagas

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF10-01 | RF10 | Positivo | Consultar vagas com retorno válido | API de vagas disponível retornando JSON válido com vagas | Realizar uma busca de vagas | Sistema consulta a API e processa a lista de vagas retornada em JSON |
| CT-RF10-02 | RF10 | Negativo | Retorno sem vagas | API retorna lista vazia em JSON válido | Realizar uma busca de vagas | Sistema processa o retorno vazio sem erro e sinaliza que não há vagas |
| CT-RF10-03 | RF10 | Negativo | JSON malformado | API retorna JSON malformado | Realizar uma busca de vagas | Sistema não apresenta dados corrompidos e informa que não foi possível obter as vagas |
| CT-RF10-04 | RF10 | Exceção | API indisponível ou sem resposta | API fora do ar ou tempo de resposta excedido | Realizar uma busca de vagas | Sistema informa a indisponibilidade da busca e permite nova tentativa, sem interromper o restante da aplicação |

### RF11 — Apresentação dos resultados da busca

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF11-01 | RF11 | Positivo | Exibir resultados em página web | Busca de vagas com resultados | Acessar a página de resultados | Vagas retornadas são apresentadas na página web |
| CT-RF11-02 | RF11 | Positivo | Iniciar associação a partir do resultado | Resultados exibidos; estudante com currículo | Selecionar uma vaga exibida | Sistema permite ao estudante iniciar manualmente a associação com um currículo (RF12) |
| CT-RF11-03 | RF11 | Negativo | Busca sem resultados | Busca sem vagas retornadas | Acessar a página de resultados | Página exibe mensagem de ausência de vagas, sem listagem vazia ou quebrada |
| CT-RF11-04 | RF11 | Exceção | Erro na busca | Falha na consulta à API | Acessar a página de resultados | Página exibe mensagem de erro compreensível, sem detalhes técnicos internos |

### RF12 — Associações entre currículos e vagas

As combinações de classificações previstas em [requisitos_funcionais.md](requisitos_funcionais.md) são verificadas na tabela de combinações, ao final desta seção.

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF12-01 | RF12, RN04 | Positivo | Compatibilidade atribuída manualmente | Estudante com currículo e vaga exibida | Marcar a classificação compatibilidade na associação | Classificação é registrada conforme escolha do estudante, sem cálculo automático de aderência |
| CT-RF12-02 | RF12, RN03 | Positivo | Inclusão de interesse não é criação automática de associação | Estudante com dois currículos e uma vaga | Criar manualmente uma associação de um currículo com a vaga, classificada como candidatura | Interesse é incluído apenas na associação criada; nenhuma outra associação é criada |
| CT-RF12-03 | RF12, RN03 | Positivo | Remover candidatura mantendo interesse | Associação com interesse e candidatura | Remover somente a classificação candidatura | Associação permanece com interesse |
| CT-RF12-04 | RF12, RN03 | Positivo | Alteração preserva interesse em associação com candidatura | Associação com interesse e candidatura | Alterar as classificações da associação, adicionando compatibilidade | Associação mantém candidatura e interesse, além da compatibilidade |
| CT-RF12-05 | RF12 | Positivo | Persistência das associações em banco de dados | Associação criada | Encerrar a sessão, autenticar-se novamente e consultar a associação | Associação e suas classificações permanecem armazenadas e idênticas |
| CT-RF12-06 | RF12 | Negativo | Criar associação sem classificação | Estudante com currículo e vaga exibida | Tentar criar a associação sem selecionar classificação | Associação não é criada e o sistema solicita ao menos uma classificação |
| CT-RF12-07 | RF12, RN01 | Negativo | Associação só é criada por ação manual | Estudante com currículos | Realizar busca, visualizar resultados e selecionar ou exportar currículos, sem solicitar associação | Nenhuma associação currículo–vaga é criada |
| CT-RF12-08 | RF12 | Negativo | Candidatura não envia currículo a serviço externo | Associação com candidatura criada | Registrar a classificação candidatura | Sistema apenas registra a classificação; nenhum envio ou candidatura em serviço externo é realizado |
| CT-RF12-09 | RF12, RN03 | Exceção | Falha ao armazenar a associação | Banco de dados indisponível | Criar associação com classificações válidas | Sistema informa a falha e não armazena associação parcial nem candidatura sem interesse |

#### Combinações de classificações

| ID do cenário | Requisito | Classificações informadas | Situação | Resultado esperado |
|---|---|---|---|---|
| CT-RF12-C01 | RF12, RN02 | Interesse | Permitida | Associação armazenada somente com interesse |
| CT-RF12-C02 | RF12, RN02 | Compatibilidade | Permitida | Associação armazenada somente com compatibilidade |
| CT-RF12-C03 | RF12, RN03 | Candidatura | Não permitida sem interesse | Associação armazenada com candidatura e interesse; candidatura não é armazenada isoladamente |
| CT-RF12-C04 | RF12, RN02 | Interesse e compatibilidade | Permitida | Associação armazenada com as duas classificações |
| CT-RF12-C05 | RF12, RN02 | Interesse e candidatura | Permitida | Associação armazenada com as duas classificações |
| CT-RF12-C06 | RF12, RN03 | Compatibilidade e candidatura | Não permitida sem interesse | Associação armazenada com compatibilidade, candidatura e interesse |
| CT-RF12-C07 | RF12, RN02 | Interesse, compatibilidade e candidatura | Permitida | Associação armazenada com as três classificações |

## Autenticação

### RF13 — Autenticação para acesso às informações

| ID do cenário | Requisito | Tipo | Cenário de aceitação | Pré-condições | Ação do usuário | Resultado esperado |
|---|---|---|---|---|---|---|
| CT-RF13-01 | RF13 | Positivo | Acessar informações estando autenticado | Estudante autenticado | Acessar suas informações pessoais e seus currículos | Acesso é concedido e as informações do estudante são exibidas |
| CT-RF13-02 | RF13 | Negativo | Acessar informações pessoais sem autenticação | Usuário sem sessão ativa | Tentar acessar a área de informações pessoais | Acesso é negado e o usuário é direcionado à autenticação |
| CT-RF13-03 | RF13 | Negativo | Acessar currículos sem autenticação | Usuário sem sessão ativa | Tentar acessar a listagem ou o endereço direto de um currículo | Acesso é negado, sem exibição de qualquer conteúdo do currículo |

O controle de autorização sobre dados pessoais, currículos e associações é verificado a partir do RNF04. Os cenários de isolamento entre estudantes desta matriz (CT-RF03-03, CT-RF14-05 e CT-RF15-04) verificam o comportamento funcional correspondente.

## Cobertura por requisito

| Requisito | Cenários |
|---|---|
| RF01 | CT-RF01-01 a CT-RF01-05 |
| RF02 | CT-RF02-01 a CT-RF02-04 |
| RF03 | CT-RF03-01 a CT-RF03-03 |
| RF04 | CT-RF04-01 a CT-RF04-03 |
| RF05 | CT-RF05-01 e CT-RF05-02 |
| RF06 | CT-RF06-01 a CT-RF06-03 |
| RF07 | CT-RF07-01 a CT-RF07-03 |
| RF08 | CT-RF08-01 a CT-RF08-03 |
| RF09 | CT-RF09-01 a CT-RF09-05 |
| RF10 | CT-RF10-01 a CT-RF10-04 |
| RF11 | CT-RF11-01 a CT-RF11-04 |
| RF12 (e RN01 a RN04) | CT-RF12-01 a CT-RF12-09 e CT-RF12-C01 a CT-RF12-C07 |
| RF13 | CT-RF13-01 a CT-RF13-03 |
| RF14 | CT-RF14-01 a CT-RF14-05 |
| RF15 | CT-RF15-01 a CT-RF15-04 |
