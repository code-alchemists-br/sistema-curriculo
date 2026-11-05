# Manual do Estudante — Sistema Currículo

**Projeto:** Sistema Currículo — FATEC-SP  
**Atualização:** 04/11/2026  
**Issues:** #432 — F12.12 e #433 — F12.13  
**Status:** Manual atualizado com orientações sobre a jornada do estudante, exportação PDF/DOCX e tratamento de falhas comuns.

## 1. Apresentação

O Sistema Currículo foi desenvolvido para ajudar estudantes a organizar suas informações pessoais, acadêmicas e profissionais e utilizá-las na elaboração de currículos.

O sistema permite cadastrar informações, preparar diferentes versões de currículo, selecionar conteúdos e visualizar a apresentação das versões.

Também possui funcionalidades de geração de arquivos PDF e DOCX, destinadas ao compartilhamento de currículos e à edição dos documentos em aplicativos compatíveis.

Este manual apresenta a jornada prevista para o estudante, desde o cadastro das informações até a criação, seleção, revisão, visualização e exportação do currículo.

**Importante:** algumas funcionalidades possuem implementação no backend, mas a integração completa de todos os controles à interface web ainda precisa ser confirmada em demonstração. Por isso, os procedimentos apresentados descrevem a utilização esperada, sem afirmar que todas as opções já estejam disponíveis na navegação atual.

## 2. Acesso ao sistema

O estudante deve utilizar sua própria conta para acessar as funcionalidades protegidas do Sistema Currículo.

Na interface de acesso, o usuário poderá utilizar as opções disponibilizadas para autenticação e cadastro.

Para proteger seus dados:

- não compartilhe sua senha;
- evite acessar sua conta em computadores públicos;
- encerre a sessão quando terminar de utilizar o sistema;
- não divulgue códigos de acesso ou informações de sessão.

O sistema utiliza a identidade autenticada para controlar o acesso aos currículos e aos dados cadastrados.

## 3. Cadastro das informações do perfil

O estudante pode organizar suas informações por categorias, incluindo:

- dados pessoais e de contato;
- formação acadêmica;
- experiências profissionais;
- cursos e certificações;
- competências;
- idiomas;
- projetos acadêmicos;
- links profissionais.

As informações devem ser preenchidas de forma clara e atualizada.

Os dados cadastrados poderão ser utilizados na composição das diferentes versões de currículo, conforme as funcionalidades disponíveis.

## 4. Criação de uma versão de currículo

O sistema permite trabalhar com diferentes versões de currículo.

Essa funcionalidade é útil para organizar informações conforme o tipo de vaga ou área profissional desejada.

O procedimento previsto envolve:

1. Acessar a área de currículos.
2. Criar uma versão.
3. Informar um título para identificá-la.
4. Escolher o modelo de apresentação.
5. Selecionar as informações que deverão compor a versão.
6. Conferir o conteúdo na prévia.

As versões permitem reutilizar dados do perfil sem precisar realizar um novo cadastro completo para cada currículo.

## 5. Seleção e organização das informações

O estudante pode utilizar itens previamente cadastrados em seu perfil para montar uma versão de currículo.

Entre os tipos de informações selecionáveis estão:

- formações acadêmicas;
- experiências profissionais;
- projetos acadêmicos;
- competências;
- idiomas;
- documentos complementares.

Também existe uma organização das seções do currículo.

A escolha dos itens de uma versão não deve apagar as informações originais do perfil nem impedir sua utilização em outras versões.

## 6. Escolha do modelo

O sistema possui componentes de apresentação identificados como clássico e compacto:

| Modelo | Identificador |
|---|---|
| Clássico | `classico` |
| Compacto | `compacto` |

O catálogo do projeto também prevê outros modelos, que devem ser diferenciados daqueles efetivamente disponíveis na versão utilizada.

O modelo determina a apresentação das informações selecionadas.

A escolha do modelo não altera automaticamente os dados acadêmicos ou profissionais do estudante.

Antes de exportar, recomenda-se verificar se o conteúdo está legível e organizado no modelo selecionado.

## 7. Revisão e prévia do currículo

A prévia permite conferir o conteúdo e a organização de uma versão antes do compartilhamento.

O estudante deve verificar:

1. Nome e informações de contato.
2. Formação acadêmica.
3. Experiências profissionais.
4. Competências e idiomas.
5. Projetos e outras informações selecionadas.
6. Ordem das seções.
7. Apresentação geral do documento.

O backend também possui uma funcionalidade de revisão que identifica informações obrigatórias ausentes e recomendações de melhoria.

A revisão distingue erros e avisos. Erros impedem que a revisão seja considerada aprovada, enquanto avisos representam sugestões.

Caso alguma informação esteja incorreta, o estudante deve realizar a alteração na funcionalidade correspondente e conferir novamente o currículo.

## Jornada detalhada — Criação, seleção e visualização do currículo

Esta seção apresenta o caminho previsto para o estudante desde o preenchimento dos dados até a visualização de uma versão de currículo.

A jornada utiliza as informações cadastradas pelo próprio estudante. Não depende do envio de um currículo pronto nem da importação de arquivos externos.

As etapas descritas seguem o mapeamento da jornada do aluno e os contratos disponíveis no projeto. Alguns controles ainda precisam de validação na interface integrada, portanto os nomes e a disponibilidade das ações devem ser conferidos no ambiente utilizado.

### 1. Iniciar o preenchimento do currículo

Depois de acessar sua conta, o estudante deve localizar as opções de preenchimento do currículo.

O fluxo principal segue esta sequência:

1. Informar dados pessoais e de contato.
2. Cadastrar formação acadêmica.
3. Cadastrar experiências profissionais.
4. Preencher informações complementares.
5. Revisar as informações.
6. Preparar a versão do currículo.
7. Selecionar os itens desejados.
8. Visualizar a prévia.
9. Prosseguir para a exportação, quando disponível.

O estudante deve conseguir revisar as informações preenchidas e retornar às etapas anteriores para realizar correções.

A navegação completa e a persistência do progresso precisam ser verificadas no ambiente integrado antes de serem consideradas funcionalidades homologadas.

### 2. Preencher as informações do perfil

O estudante começa informando os dados que serão utilizados em seu currículo.

**Dados pessoais e contato**

Incluem identificação e informações necessárias para que empresas possam entrar em contato.

É importante conferir principalmente o nome, o e-mail e o telefone.

**Formação acadêmica**

Permite registrar informações como instituição, curso, período e situação da formação.

**Experiências profissionais**

Permite organizar experiências anteriores, incluindo empresa, cargo, período e atividades realizadas.

**Informações complementares**

Podem incluir competências, idiomas, cursos, certificações e projetos acadêmicos.

Esses dados ficam associados ao perfil e podem ser utilizados na composição de versões de currículo.

O estudante não precisa inserir informações fictícias para completar seções opcionais. Entretanto, deve observar as validações e regras obrigatórias aplicadas pelo sistema.

### 3. Criar uma versão de currículo

Depois de preparar as informações do perfil, o estudante pode criar uma versão de currículo.

Uma versão representa uma composição específica das informações cadastradas.

Isso permite preparar currículos diferentes para objetivos profissionais distintos, reutilizando o conteúdo do mesmo perfil.

O procedimento previsto é:

1. Acessar a área destinada às versões de currículo.
2. Escolher a opção de criação de uma nova versão.
3. Informar um título que facilite sua identificação.
4. Selecionar um modelo de apresentação disponível.
5. Confirmar a criação.
6. Prosseguir para a seleção das informações.

**Exemplo:**

Um estudante pode preparar uma versão chamada "Estágio em Desenvolvimento de Software" e outra chamada "Estágio em Suporte de TI".

Cada versão pode utilizar uma seleção diferente das informações cadastradas, sem exigir um novo perfil.

O backend possui um contrato de criação com título, layout e visibilidade da versão. A visibilidade inicial é privada, salvo escolha explícita diferente conforme as regras disponíveis.

### 4. Selecionar as informações do currículo

A seleção permite determinar quais informações do perfil farão parte de determinada versão.

O sistema possui operações de seleção e desseleção de itens.

Entre as informações que podem ser associadas a uma versão estão:

- formações acadêmicas;
- experiências profissionais;
- projetos acadêmicos;
- competências;
- idiomas;
- documentos.

**Como realizar a seleção no fluxo previsto:**

1. Abrir a versão do currículo.
2. Localizar as informações cadastradas.
3. Selecionar os itens que deseja utilizar.
4. Conferir os itens incluídos.
5. Remover da seleção informações que não devem aparecer.
6. Prosseguir para a prévia.

Selecionar ou desselecionar um item em uma versão não significa excluir o registro original do perfil.

Por exemplo, uma experiência profissional pode ser relevante para um currículo e desnecessária para outro. O estudante pode escolher em qual versão utilizá-la.

### 5. Organizar as seções

Além dos itens selecionados, o currículo possui uma organização visual.

As seções podem incluir identificação, formação, experiência, projetos, competências e idiomas.

O backend possui uma operação específica para atualizar a ordem das seções de uma versão.

Quando o controle estiver disponível na interface, o estudante poderá utilizar essa funcionalidade para organizar a apresentação do currículo.

A ordem escolhida deve ser conferida novamente na prévia.

A reorganização das seções não deve modificar os dados originais cadastrados pelo estudante.

### 6. Escolher o modelo de apresentação

O modelo define como as informações selecionadas serão apresentadas.

O projeto possui um catálogo de modelos planejados e componentes de visualização desenvolvidos para diferentes apresentações.

O estudante deve escolher somente entre as opções realmente disponibilizadas na versão do sistema que estiver utilizando.

**Antes de confirmar o modelo, recomenda-se observar:**

- legibilidade dos textos;
- organização da formação e das experiências;
- destaque das competências e projetos;
- apresentação das informações de contato;
- adequação do documento ao objetivo profissional.

A troca de modelo não deve apagar os itens selecionados.

Os modelos disponíveis na interface devem ser confirmados durante a demonstração integrada.

### 7. Revisar as informações antes da visualização

Depois de montar uma versão, o estudante deve conferir seu conteúdo.

A revisão permite verificar se existem informações incorretas, ausentes ou que precisam de atualização.

O backend possui uma funcionalidade de revisão que organiza as pendências em duas categorias:

| Categoria | Significado |
|---|---|
| Erro | Problema obrigatório que impede a aprovação da revisão |
| Aviso | Recomendação que não impede a aprovação |

Entre as situações verificadas estão:

- ausência de informações de contato;
- falta de formação acadêmica;
- falta de experiência profissional, conforme a regra atual;
- ausência de competências;
- inconsistências nas datas;
- ausência de projetos ou idiomas, apresentada como recomendação.

Quando houver um erro, o estudante deverá corrigir a informação correspondente e solicitar uma nova revisão.

Avisos não reprovam a revisão e podem representar sugestões de melhoria.

Essa etapa não altera automaticamente os dados do estudante.

### 8. Visualizar a prévia do currículo

A prévia apresenta o currículo organizado a partir das informações selecionadas na versão.

Ela permite verificar o resultado antes de gerar o arquivo.

O procedimento previsto é:

1. Selecionar a versão desejada.
2. Acessar a funcionalidade de visualização.
3. Conferir os dados pessoais e de contato.
4. Verificar as seções e informações selecionadas.
5. Conferir a ordem das seções.
6. Avaliar a apresentação do modelo.
7. Retornar à edição se alguma informação precisar de correção.

A prévia não deve acrescentar informações que não tenham sido cadastradas ou selecionadas pelo estudante.

Também não deve exibir credenciais ou dados internos de armazenamento dos documentos.

### 9. Entender os estados da prévia

A apresentação pode assumir diferentes estados conforme a consulta realizada.

| Estado | O que significa | Orientação |
|---|---|---|
| Carregando | O sistema está obtendo os dados | Aguardar a conclusão da consulta |
| Prévia disponível | Os dados da versão foram obtidos | Conferir o conteúdo |
| Seção vazia | Não há itens selecionados ou cadastrados naquela seção | Verificar se deseja incluir informações |
| Falha | A prévia não pôde ser apresentada | Conferir a versão e tentar novamente |

Uma seção vazia não significa necessariamente que todo o currículo está incorreto.

O estudante deve verificar se deseja realmente apresentar aquela seção e, quando necessário, selecionar os itens correspondentes.

### 10. Corrigir dados após visualizar

Caso encontre alguma informação incorreta na prévia, o estudante deverá retornar à etapa correspondente.

Por exemplo:

- nome ou telefone incorreto: revisar os dados pessoais;
- formação ausente: conferir o cadastro e a seleção da formação;
- experiência não apresentada: verificar se foi selecionada;
- projeto incorreto: editar o registro do projeto;
- seção fora da ordem desejada: revisar a organização da versão.

Após realizar os ajustes, o estudante deve consultar novamente a prévia.

A atualização na tela ou no perfil não deve ser confundida com uma exportação já realizada. Arquivos baixados anteriormente não são atualizados automaticamente.

### 11. Problemas comuns durante a jornada

| Problema | Possível causa | Orientação |
|---|---|---|
| Não consegue criar uma versão | Informações obrigatórias inválidas ou serviço indisponível | Conferir os campos e tentar novamente |
| Um item não aparece na versão | Item não selecionado ou inexistente | Conferir o cadastro e a seleção |
| A prévia apresenta uma seção vazia | Não há itens associados à seção | Selecionar informações, quando necessário |
| A prévia apresenta dados antigos | Alterações ainda não refletidas na consulta | Conferir o salvamento e atualizar a prévia |
| A versão não é encontrada | Identificador inexistente ou acesso não permitido | Selecionar uma versão pertencente à própria conta |
| A revisão apresenta erros | Informação obrigatória ausente ou inconsistente | Corrigir a pendência indicada |
| A visualização não está disponível | Serviço indisponível ou integração ainda não concluída | Tentar novamente e comunicar a equipe responsável |

As mensagens exatas dependem do contrato e do ambiente utilizado.

### 12. Exemplo de jornada com dados fictícios

Considere uma estudante fictícia que deseja preparar um currículo para uma vaga de estágio em desenvolvimento web.

**Etapa 1 — Perfil**

Ela registra suas informações pessoais, uma formação acadêmica, uma experiência em desenvolvimento, competências e um projeto acadêmico.

**Etapa 2 — Criação da versão**

Cria uma versão denominada "Estágio em Desenvolvimento Web".

**Etapa 3 — Seleção**

Seleciona a formação, as competências técnicas e o projeto que deseja apresentar.

**Etapa 4 — Organização**

Confere a organização das seções e utiliza um modelo disponível.

**Etapa 5 — Revisão**

Verifica as pendências retornadas e corrige eventuais erros.

**Etapa 6 — Visualização**

Acessa a prévia para conferir se o currículo apresenta as informações desejadas.

**Etapa 7 — Exportação**

Após a conferência, poderá gerar o arquivo em PDF ou DOCX pelo fluxo disponível.

Esse exemplo é ilustrativo e utiliza a lógica da jornada documentada. Não representa um teste integrado executado.

### 13. Limitações e cuidados

A documentação da jornada considera os casos de uso, os contratos do backend e os componentes desenvolvidos.

Isso não significa que todas as etapas já estejam disponíveis em um único fluxo executável na interface.

A disponibilidade dos controles de criação de versões, seleção de itens, ordenação e visualização deve ser confirmada no ambiente integrado.

Também não se deve apresentar uma simulação de teste como se fosse uma operação real concluída pelo estudante.

A documentação deverá ser atualizada sempre que os nomes das ações, os modelos ou o comportamento das telas forem alterados.

### 14. Referências da jornada

- [Mapeamento da jornada do estudante](mapeamento_jornadas.md)
- [Prévia do currículo](previa-curriculo.md)
- [Modelos de currículo](modelos_curriculo.md)
- `src/backend/api/versao_curriculo.py`
- `src/backend/api/itens_versao_curriculo.py`
- `src/backend/api/previa_versao_curriculo.py`
- `src/backend/api/revisao_versao_curriculo.py`

**Rastreabilidade:** issue #432 — F12.12. Esta seção complementa o manual atualizado na issue #433, sem substituir as instruções de exportação e tratamento de falhas.

## 8. Exportação do currículo

A exportação permite obter um arquivo correspondente à versão de currículo selecionada.

Os formatos disponíveis no backend são:

| Formato | Extensão | Finalidade |
|---|---|---|
| PDF | `.pdf` | Compartilhar uma versão final do currículo |
| DOCX | `.docx` | Abrir e editar o documento em aplicativos compatíveis |

O PDF é recomendado para envio a empresas e processos seletivos quando se deseja preservar a apresentação.

O DOCX é recomendado quando o estudante precisa realizar ajustes adicionais em um editor de texto.

## 9. Como exportar o currículo

O fluxo previsto para o estudante é:

1. Acessar o sistema com sua conta.
2. Localizar as versões de currículo disponíveis.
3. Selecionar a versão desejada.
4. Conferir as informações e o modelo na prévia.
5. Escolher o formato PDF ou DOCX.
6. Solicitar a geração do arquivo.
7. Salvar o documento disponibilizado pelo navegador.
8. Abrir o arquivo para conferir seu conteúdo.

A disponibilidade dos controles e seus nomes definitivos depende da integração da funcionalidade às telas da aplicação.

As rotas de download já estão implementadas no backend, mas sua existência não comprova, isoladamente, que todos os passos estejam disponíveis em uma interface web integrada.

Para orientações específicas sobre cada formato, consulte o [Guia de exportação PDF e DOCX](guia-exportacao-pdf-docx.md).

## 10. Exportação em PDF

O PDF é indicado principalmente para envio de currículos.

Ao gerar esse formato, o estudante deve conferir se:

- o documento abre corretamente;
- os textos estão legíveis;
- as seções estão organizadas;
- não existem informações cortadas;
- todas as páginas estão completas;
- os dados pessoais e profissionais estão corretos.

Depois dessa conferência, o arquivo poderá ser utilizado em processos seletivos.

## 11. Exportação em DOCX

O DOCX pode ser aberto em aplicativos de edição de documentos compatíveis com esse formato.

Ele é útil quando o estudante deseja realizar alterações diretamente no arquivo baixado.

Entretanto, essas alterações não modificam automaticamente as informações cadastradas no Sistema Currículo.

Caso queira que a alteração apareça em futuras exportações, o estudante deve atualizar os dados na própria aplicação.

A apresentação do DOCX também pode variar conforme o aplicativo utilizado para abrir o arquivo.

## 12. Problemas comuns e soluções

Durante o uso do sistema podem ocorrer situações que impeçam a consulta, revisão ou exportação do currículo.

A tabela apresenta orientações para os problemas mais comuns.

| Problema | Possível causa | O que fazer |
|---|---|---|
| Não consegue acessar a conta | Sessão inválida ou expirada | Realizar novamente o login |
| Currículo não aparece | Versão não encontrada ou indisponível | Conferir a versão selecionada |
| Informações estão incorretas | Dados do perfil desatualizados | Corrigir os dados no sistema e conferir novamente |
| Exportação não funciona | Serviço indisponível ou falha na geração | Tentar novamente e comunicar a equipe se persistir |
| PDF não abre corretamente | Download incompleto ou arquivo inválido | Realizar novo download e utilizar leitor compatível |
| DOCX apresenta diferenças visuais | Variações entre editores de documentos | Abrir em aplicativo compatível e conferir a formatação |
| Arquivo baixado não contém a informação desejada | Versão ou itens selecionados incorretos | Revisar a seleção e gerar novamente |
| Busca de vagas não retorna resultados | Nenhuma oportunidade encontrada ou serviço externo indisponível | Conferir os critérios e tentar novamente quando necessário |

## 13. Falhas relacionadas à exportação

### 13.1. Autenticação necessária

A exportação exige que o estudante esteja autenticado.

Se a sessão estiver inválida ou ausente, a solicitação poderá ser recusada.

**Orientação:** entrar novamente na conta e repetir a operação.

### 13.2. Currículo não encontrado

A exportação só pode ser realizada para versões às quais o estudante tem acesso.

Se a versão não existir ou pertencer a outro usuário, a solicitação não será concluída.

**Orientação:** selecionar uma versão pertencente à própria conta.

### 13.3. Falha na geração do arquivo

Caso ocorra um problema interno durante a geração, o sistema poderá apresentar:

> Não foi possível gerar o arquivo. Tente novamente.

**Orientação:** repetir a solicitação. Se a falha continuar, comunicar a equipe responsável.

### 13.4. Exportação indisponível

A exportação poderá estar indisponível quando o serviço responsável pela geração do formato não estiver configurado ou disponível no ambiente.

**Orientação:** tentar novamente após a normalização do serviço.

### 13.5. Download incompleto

Se o arquivo não abrir ou estiver incompleto, o estudante deve verificar se o navegador concluiu o download.

**Orientação:** realizar uma nova exportação e conferir a extensão do arquivo.

## 14. Conferência do documento após o download

Após exportar, recomenda-se realizar uma revisão final.

O estudante deve observar:

1. Se o nome e os contatos estão corretos.
2. Se o currículo corresponde à versão escolhida.
3. Se as informações selecionadas foram incluídas.
4. Se os textos estão completos.
5. Se não existem cortes ou sobreposições visíveis.
6. Se o arquivo abre normalmente.
7. Se o formato corresponde ao solicitado pela empresa.

Essa conferência é importante porque o currículo será utilizado fora do sistema e poderá ser compartilhado com recrutadores e empresas.

## 15. Segurança e privacidade

Os currículos podem conter informações pessoais, acadêmicas e profissionais.

Por isso, recomenda-se:

- compartilhar o documento somente quando necessário;
- verificar o destinatário antes do envio;
- evitar armazenar currículos em computadores compartilhados;
- remover arquivos baixados de dispositivos públicos;
- não utilizar serviços externos desconhecidos para converter documentos que contenham dados pessoais;
- não compartilhar credenciais de acesso ao sistema.

As rotas de exportação exigem autenticação e verificam a propriedade da versão solicitada.

O estudante não pode exportar um currículo de outra pessoa apenas por conhecer seu identificador.

## 16. Informações técnicas de referência

O backend disponibiliza as seguintes operações:

| Formato | Método | Endpoint |
|---|---|---|
| PDF | GET | `/estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/pdf` |
| DOCX | GET | `/estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/docx` |

As respostas de sucesso utilizam os tipos de conteúdo correspondentes e disponibilizam o arquivo para download.

Os principais códigos HTTP são:

| Código | Significado |
|---|---|
| `200` | Arquivo gerado e devolvido |
| `401` | Autenticação ausente ou inválida |
| `403` | Acesso não autorizado à identidade solicitada |
| `404` | Versão não encontrada ou indisponível para o estudante |
| `500` | Falha na geração do arquivo |
| `503` | Serviço de exportação não configurado |

Essas informações são destinadas à manutenção da documentação e ao suporte. O estudante não precisa utilizar diretamente os endpoints para seguir o fluxo previsto na interface.

## 17. Estado atual da funcionalidade

As rotas e os casos de uso de exportação PDF e DOCX estão presentes no backend atual.

A aplicação também possui componentes relacionados a cadastro, seleção de informações, modelos e validação de currículo.

Entretanto, ainda é necessário confirmar em ambiente integrado a disponibilidade dos controles de exportação e o funcionamento completo da jornada do estudante.

Por esse motivo, este manual diferencia as capacidades técnicas existentes dos procedimentos previstos para a interface.

A documentação deve ser revisada após a demonstração integrada, utilizando os nomes definitivos das opções disponíveis e os resultados observados.

## 18. Documentação complementar

Para informações mais detalhadas, consulte:

- [Guia de exportação PDF e DOCX](guia-exportacao-pdf-docx.md)
- [Mapeamento da jornada do estudante](mapeamento_jornadas.md)
- [Modelos de currículo](modelos_curriculo.md)
- [Contratos de informações complementares](contratos-informacoes-complementares.md)
- [Prévia do currículo](previa-curriculo.md)

## 19. Rastreabilidade

- **Issue #432 — F12.12:** jornada de criação, seleção e visualização do currículo.
- **Issue #433 — F12.13:** orientações de exportação PDF/DOCX e tratamento de falhas comuns.
- **Issue relacionada:** #386 — F10.4.
- **Requisito:** RF09 — Exportação de currículos em PDF e DOCX.
- **Casos de uso:** UC01 a UC08, conforme as etapas correspondentes.
- **WBS:** 1.1.2.4, 1.8.2.1–1.8.2.4.
- **Documento atualizado:** `docs/manual-estudante.md`.
- **Guia complementar:** `docs/guia-exportacao-pdf-docx.md`.
- **Referência da jornada:** `docs/mapeamento_jornadas.md`.

## 20. Conclusão

O Sistema Currículo reúne funcionalidades para organizar as informações do estudante, preparar diferentes versões de currículo e visualizar o conteúdo antes do compartilhamento.

A jornada documentada apresenta as etapas de preenchimento, criação de versões, seleção dos itens, organização das seções, revisão e visualização do currículo.

A exportação em PDF e DOCX permite utilizar essas versões em processos seletivos ou em aplicativos de edição de documentos compatíveis.

Este manual também apresenta orientações para resolver problemas comuns e destaca a importância da conferência das informações antes da geração dos arquivos.

A documentação diferencia as capacidades implementadas no backend das etapas que ainda dependem de validação integrada na interface, permitindo que o manual acompanhe a evolução do sistema sem apresentar funcionalidades não verificadas como concluídas.
