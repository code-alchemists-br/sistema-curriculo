# Matriz de rastreabilidade inicial — Sistema Currículo

## Objetivo

Esta matriz estabelece uma rastreabilidade inicial entre a estrutura de
trabalho do projeto (WBS), os requisitos funcionais, os cards ativos no GitHub
e as evidências de teste atualmente documentadas.

O objetivo é facilitar a identificação de quais atividades em andamento estão
relacionadas a cada requisito funcional e quais cenários de teste podem ser
utilizados como referência para sua validação.

Esta matriz não substitui os documentos de requisitos nem a matriz de testes.
Ela apenas relaciona as informações existentes para facilitar o acompanhamento
do projeto.

## Fontes utilizadas

A matriz foi construída a partir das seguintes fontes do projeto:

- `docs/requisitos_funcionais.md`, considerando os requisitos RF01 a RF15;
- `docs/matriz_testes.md`, considerando os cenários CT-RF01 a CT-RF15;
- cards atualmente abertos no GitHub;
- informações de WBS registradas nos próprios cards.

Quando um card antigo não informa uma WBS em sua descrição, essa ausência é
registrada explicitamente em vez de atribuir uma WBS por inferência.

Os cenários `CT-RFxx` representam evidências de teste definidas na matriz de
aceitação. A presença de um cenário nesta tabela não significa, por si só, que
o teste já foi executado com sucesso.

## Situações utilizadas

- **Rastreado:** existe relação clara entre requisito, card ativo e evidência de teste.
- **Parcial:** existe rastreabilidade, mas os cards ativos cobrem apenas parte do requisito ou ainda existem etapas pendentes.
- **Lacuna:** não foi identificado card ativo que cubra diretamente toda a necessidade do requisito.
- **WBS não informada:** o card está ativo, mas sua descrição não registra uma WBS.

## Matriz de rastreabilidade

| Requisito | Resumo do requisito | WBS relacionada nos cards ativos | Cards ativos relacionados | Evidências de teste | Situação |
|---|---|---|---|---|---|
| **RF01** | Cadastrar dados pessoais, formação, experiências e competências | `1.7.1.*`, `1.7.2.*`, `1.8.1.*`; WBS não informada em cards antigos | #31 – interface de formação acadêmica; #34 – interface de competências; #44 – cadastro de competências; #397 – integração do CRUD de formação | `CT-RF01-01` a `CT-RF01-05` | **Parcial** |
| **RF02** | Consultar, editar e excluir informações cadastradas | `1.3.1.2–1.3.2.4`; `1.7.1.*`, `1.7.2.*`, `1.8.1.*`; WBS não informada em cards antigos | #93 – exclusão de formação; #95 – edição de experiência; #183–#190 – consulta, atualização, exclusão e propriedade de formação/experiência; #369 – CRUD de perfil; #397 – CRUD de formação; #398 – CRUD de informações complementares | `CT-RF02-01` a `CT-RF02-06` | **Rastreado** |
| **RF03** | Centralizar as informações do estudante para utilização nos currículos | `1.4.1.*`, `1.4.2.*`; `1.7.1.*`, `1.7.2.*`, `1.8.1.*` | #210 – validar propriedade de referência; #213 – projetar currículo somente com referências selecionadas; #400 – integração da seleção e ordenação de itens | `CT-RF03-01` a `CT-RF03-03` | **Parcial** |
| **RF04** | Registrar projetos acadêmicos e oferecer orientação para descrevê-los | `1.3.2.3`, `1.3.3.1–1.3.3.4`; WBS não informada no card #102 | #102 – cadastro de projeto acadêmico; #198 – contrato do assistente; #199 – estratégia determinística; #200 – exposição da sugestão; #201 – aceitar, editar ou rejeitar sugestão | `CT-RF04-01` a `CT-RF04-03` | **Rastreado** |
| **RF05** | Orientar o estudante na estruturação e organização das seções do currículo | `1.4.1.*`, `1.4.2.*`; `1.7.1.*`, `1.7.2.*`, `1.8.1.*` | #209 – seções e ordem padrão; #211 – persistência da ordem; #212 – atualização da ordem; #400 – integração da seleção e ordenação | `CT-RF05-01` e `CT-RF05-02` | **Rastreado** |
| **RF06** | Disponibilizar modelos de currículo com layouts profissionais | `1.4.1.*`, `1.4.2.*`; `1.1.2.4`, `1.8.2.1–1.8.2.4` | #214 – modelo clássico; #215 – modelo compacto; #216 – seleção do modelo; #217 – alternador de modelo; #219 e #220 – legibilidade dos modelos; #426 – ADR de seções, referências e modelos | `CT-RF06-01` a `CT-RF06-03` | **Rastreado** |
| **RF07** | Gerar visualização do currículo com informações cadastradas e modelo selecionado | `1.4.1.*`, `1.4.2.*`; `1.2.1.3–1.2.1.4`, `1.4.2.4`, `1.5.2.4`; `1.7.1.*`, `1.7.2.*`, `1.8.1.*`; `1.1.2.4`, `1.8.2.1–1.8.2.4` | #213 – projeção do currículo; #217 – alternador na prévia; #218 – estado vazio; #366 – validação móvel; #409 – responsividade da prévia; #427 – documentação técnica da prévia | `CT-RF07-01` a `CT-RF07-03` | **Rastreado** |
| **RF08** | Oferecer revisão guiada do conteúdo e organização do currículo | `1.4.3.*`, `1.4.4.*`; `1.1.2.4`, `1.8.2.1–1.8.2.4` | #221–#228 – contrato, regras, resultados e decisões da revisão; #235 e #236 – interface e decisão de recomendações; #430 – documentação do fluxo de revisão | `CT-RF08-01` a `CT-RF08-03` | **Rastreado** |
| **RF09** | Exportar currículos nos formatos PDF e DOCX | `1.4.3.*`, `1.4.4.*`; `1.7.1.*`, `1.7.2.*`, `1.8.1.*`; `1.8.2.1–1.8.2.4`; `1.1.1.4`, `1.1.2.4`, `1.2.1.4`, `1.7.2.4`, `1.8.2.4` | #172 – critérios de aceite; #229–#234 – DTO, PDF, DOCX e validações; #386 – instruções de exportação; #410 – validação do PDF; #412 – validação do DOCX; #433 – manual de exportação | `CT-RF09-01` a `CT-RF09-05` | **Rastreado** |
| **RF10** | Consultar ferramenta de busca de vagas por API e processar o JSON retornado | `1.5.*`, `1.6.*`; `1.7.1.*`, `1.7.2.*`, `1.8.1.*`; `1.8.2.1–1.8.2.4`; WBS não informada no card #128 | #128 – resultados da busca; #241 – estado vazio; #242 – erro da busca; #374 – cenário E2E; #383 – contrato público e erros; #428 – contrato e mapeamento do Grupo 2; #429 – catálogo de erros | `CT-RF10-01` a `CT-RF10-04` | **Rastreado** |
| **RF11** | Apresentar os resultados da busca de vagas em página web | `1.5.*`, `1.6.*`; `1.2.1.3–1.2.1.4`, `1.4.2.4`, `1.5.2.4`; `1.7.1.*`, `1.7.2.*`, `1.8.1.*`; WBS não informada no card #128 | #128 – exposição dos resultados; #241 e #281 – estado vazio; #242 e #288 – estado de erro; #363 – validação móvel da página; #407 – leitor de tela e teclado | `CT-RF11-01` a `CT-RF11-04` | **Rastreado** |
| **RF12** | Permitir associações manuais entre currículos e vagas e armazenar suas classificações | `1.5.*`, `1.6.*`; `1.7.1.*`, `1.7.2.*`, `1.8.1.*`; WBS não informada no card #130 | #130 – criação da associação; #243–#267 – consulta, remoção e histórico de associações; #371 – cenário de integração; #408 – integração com candidatura e interesse implícito | `CT-RF12-01` a `CT-RF12-09` e `CT-RF12-C01` a `CT-RF12-C07` | **Rastreado** |
| **RF13** | Exigir autenticação para acesso a informações pessoais e currículos | `1.8.2.1–1.8.2.4`; `1.7.1.*`, `1.7.2.*`, `1.8.1.*` | #382 – contrato de autenticação e sessão; #391 – validação de credenciais; #393 – recusa de acesso a perfil alheio; #394 – recusa de acesso a currículo alheio | `CT-RF13-01` a `CT-RF13-03` | **Rastreado** |
| **RF14** | Permitir criar, consultar, editar e excluir múltiplos currículos por estudante | `1.4.1.*`, `1.4.2.*`; `1.7.1.*`, `1.7.2.*`, `1.8.1.*` em atividades relacionadas | #213 – consulta/projeção do currículo; #394 – proteção de currículo alheio; #400 – seleção e ordenação de itens | `CT-RF14-01` a `CT-RF14-05` | **Lacuna / Parcial** |
| **RF15** | Selecionar qual currículo será exportado ou associado a uma vaga | `1.4.1.*`, `1.4.2.*`; `1.7.1.*`, `1.7.2.*`, `1.8.1.*` | #213 – projeção por referências selecionadas; #400 – seleção e ordenação de itens; #408 – associação currículo–vaga | `CT-RF15-01` a `CT-RF15-04` | **Parcial** |

## Lacunas identificadas

A rastreabilidade inicial evidencia alguns pontos que devem ser acompanhados nas
próximas atualizações da matriz.

### Cards antigos sem WBS registrada

Foram encontrados cards ativos criados antes do padrão atual de planejamento
que não apresentam WBS em sua descrição. Entre os exemplos diretamente
relacionados aos requisitos estão:

- #31 — interface para cadastro de formação acadêmica;
- #34 — interface para cadastro de competências;
- #44 — cadastro de competências;
- #93 — exclusão de formação acadêmica;
- #95 — edição de experiência profissional;
- #102 — cadastro de projeto acadêmico;
- #128 — exposição de resultados de busca de vagas;
- #130 — criação de associação currículo–vaga.

A matriz mantém esses cards rastreados, porém registra a WBS como não informada
quando não existe evidência explícita no próprio card.

### RF14 com cobertura ativa incompleta

Os cenários `CT-RF14-01` a `CT-RF14-05` definem a validação de múltiplos
currículos, incluindo criação, consulta, edição, exclusão e isolamento entre
contas.

Na consulta aos cards atualmente abertos, foram identificadas atividades
relacionadas à consulta, composição e autorização de currículos, mas não foi
identificado um conjunto de cards ativos que represente de forma inequívoca
todo o CRUD previsto pelo RF14.

Por isso, o requisito permanece marcado como **Lacuna / Parcial** nesta versão.

### RF15 com rastreabilidade parcial

Há cards ativos relacionados à seleção de itens e à associação currículo–vaga,
mas a rastreabilidade da seleção explícita de um currículo para exportação e
para associação ainda não está igualmente representada por cards ativos.

Por esse motivo, o requisito permanece como **Parcial**.

### Divergência na cobertura resumida de RF02

A seção de RF02 em `docs/matriz_testes.md` contém atualmente os cenários
`CT-RF02-01` a `CT-RF02-06`.

Entretanto, a tabela de cobertura localizada ao final do mesmo documento ainda
resume RF02 como `CT-RF02-01 a CT-RF02-04`.

Nesta matriz foi considerado o conjunto efetivamente descrito na seção do RF02,
ou seja, `CT-RF02-01` a `CT-RF02-06`.

Esta matriz não altera o documento original e apenas registra a divergência para
revisão futura.

## Critério de manutenção

A matriz deve ser atualizada quando ocorrer pelo menos uma das seguintes
situações:

- criação ou encerramento de card relacionado a um requisito funcional;
- alteração da WBS associada a uma atividade;
- inclusão, remoção ou alteração de requisito funcional;
- criação de novo cenário ou evidência de teste;
- conclusão de uma lacuna identificada nesta matriz.

Cards encerrados podem permanecer no histórico do projeto, mas a coluna
**Cards ativos relacionados** desta matriz deve representar prioritariamente o
trabalho ainda aberto no momento da revisão.

## Limites desta versão

Esta é uma matriz inicial baseada nos requisitos funcionais e nos cards ativos
identificados no repositório no momento de sua elaboração.

A associação entre requisito e card é feita somente quando o objetivo descrito
no card possui relação funcional identificável com o requisito. Não foi
atribuída WBS a cards que não possuem essa informação registrada.

Os cenários da `docs/matriz_testes.md` são utilizados como evidências de teste
especificadas. Resultados de execução, relatórios de CI, screenshots ou outros
artefatos de execução poderão ser adicionados em revisões futuras quando
estiverem disponíveis.
