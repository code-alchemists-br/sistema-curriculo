# Checklist de Demonstração do Sistema Currículo

**Projeto:** Sistema Currículo — FATEC-SP  
**Issue:** #388 — F10.6  
**WBS:** 1.8.2.1–1.8.2.4  
**Atualização do roteiro:** 01/11/2026  
**Branch de referência:** `dev`  
**Situação:** Roteiro preparado; execução e resultados pendentes de registro.

## 1. Objetivo

Este documento apresenta o checklist de demonstração do Sistema Currículo, utilizando dados sintéticos e cenários que representam as principais funcionalidades da aplicação.

O objetivo é orientar a equipe durante a apresentação, permitir a conferência dos resultados esperados e registrar possíveis falhas sem comprometer informações reais de estudantes.

O roteiro contempla o acesso ao sistema, cadastro de informações, criação de versões de currículo, seleção de itens, revisão, prévia, exportação PDF/DOCX e busca de vagas.

Também apresenta cenários de erro que devem ser verificados em ambiente controlado.

**Este documento é um planejamento de execução.** A presença de um cenário na lista não significa que ele foi executado ou aprovado.

## 2. Preparação do ambiente

Antes da demonstração, a equipe deve verificar as condições necessárias para a execução.

### Checklist inicial

- [ ] Identificar o responsável pela apresentação.
- [ ] Confirmar a data e o horário da demonstração.
- [ ] Identificar a branch e o commit da aplicação.
- [ ] Confirmar o ambiente utilizado.
- [ ] Verificar a disponibilidade do backend.
- [ ] Verificar a disponibilidade do frontend.
- [ ] Verificar a conexão com o banco de dados.
- [ ] Confirmar quais funcionalidades estão integradas.
- [ ] Verificar a configuração do serviço externo do Grupo 2, quando aplicável.
- [ ] Preparar contas e currículos fictícios.
- [ ] Confirmar que nenhuma credencial ou dado pessoal real será apresentado.
- [ ] Preparar um local para registrar capturas e resultados.
- [ ] Conferir os arquivos que poderão ser utilizados na demonstração.

Os serviços devem ser iniciados conforme as instruções técnicas de configuração existentes no repositório.

A demonstração deve ocorrer em ambiente de teste ou apresentação, evitando operações destrutivas em produção.

## 3. Massa de dados sintéticos

O projeto já possui dados fictícios utilizados para testes e apresentação.

As principais referências são:

- `docs/massa_teste_curriculos.json`
- `src/backend/tests/fixtures/massa_teste_curriculos.py`

O arquivo JSON apresenta diferentes perfis fictícios com formações, experiências, competências, idiomas e projetos.

Esses registros podem servir de referência para construir os cenários da apresentação.

### Perfis disponíveis

| Perfil fictício | Área principal | Utilização sugerida |
|---|---|---|
| Ana Beatriz Souza | Desenvolvimento web | Cadastro e prévia de currículo de tecnologia |
| Bruno Henrique Lima | Área financeira | Currículo com múltiplas formações e experiências |
| Carolina Mendes Rocha | Design | Verificação de projetos, competências e modelo compacto |

Os nomes e informações acima pertencem à massa sintética versionada no projeto.

A utilização desses dados na demonstração depende de eles estarem carregados no ambiente ou serem preparados conforme os contratos válidos da aplicação.

**Importante:** o arquivo JSON é uma massa de referência. Sua existência não significa que os registros já estejam cadastrados no banco de dados da demonstração.

### 3.1. Preparação dos cenários

Preparar, quando possível:

- uma conta fictícia com informações completas;
- uma versão de currículo com formação, experiência e competências;
- uma versão com seções opcionais vazias;
- uma versão com conteúdo suficiente para avaliar a apresentação;
- um cenário de busca de vagas com resultados;
- um cenário de busca sem resultados;
- cenários de falha simulada, em ambiente controlado.

Não utilizar CPF, e-mail pessoal, senha real, token ou currículo verdadeiro nas evidências.

## 4. Roteiro de demonstração funcional

Cada etapa deve ser executada somente quando a funcionalidade estiver disponível no ambiente selecionado.

Caso uma etapa ainda não esteja integrada à interface, registrar essa limitação e, se necessário, demonstrar separadamente seu contrato técnico.

### DEM-01 — Acesso ao sistema

**Objetivo:** verificar o acesso inicial e a autenticação do estudante.

Procedimento:

1. Abrir a aplicação.
2. Localizar a área de acesso.
3. Utilizar uma conta fictícia válida.
4. Confirmar o comportamento após a autenticação.

**Resultado esperado:** acesso autorizado aos recursos disponíveis para a conta.

**Evidência:** captura da interface autenticada, sem mostrar senha ou informações de sessão.

**Resultado da execução:** pendente.

### DEM-02 — Cadastro das informações pessoais

**Objetivo:** demonstrar o registro e a edição de informações do estudante.

Procedimento:

1. Acessar o cadastro de dados pessoais.
2. Preencher informações sintéticas.
3. Salvar os dados.
4. Consultar ou retornar à tela correspondente, quando disponível.
5. Verificar se os valores foram preservados.

**Resultado esperado:** informações válidas registradas e vinculadas ao estudante correto.

**Evidência:** captura dos campos preenchidos e do estado após o salvamento.

**Resultado da execução:** pendente.

### DEM-03 — Formação e experiência profissional

**Objetivo:** demonstrar o cadastro das informações acadêmicas e profissionais.

Procedimento:

1. Cadastrar uma formação acadêmica fictícia.
2. Informar instituição, curso, período e situação.
3. Cadastrar uma experiência profissional fictícia.
4. Informar empresa, cargo, descrição e período.
5. Confirmar o resultado das operações.

**Resultado esperado:** os dados válidos são registrados sem associação a outro estudante.

**Evidência:** telas ou respostas das operações realizadas.

**Resultado da execução:** pendente.

### DEM-04 — Competências, idiomas e projetos

**Objetivo:** verificar o cadastro de informações complementares.

Procedimento:

1. Cadastrar competências fictícias.
2. Informar um idioma.
3. Cadastrar um projeto acadêmico.
4. Conferir os resultados disponíveis.

**Resultado esperado:** as informações válidas ficam disponíveis para utilização nas funcionalidades correspondentes.

**Evidência:** registros apresentados ou respostas das APIs, identificando o método utilizado.

**Resultado da execução:** pendente.

### DEM-05 — Criação de versão do currículo

**Objetivo:** demonstrar a criação de uma versão de currículo.

Procedimento:

1. Acessar a funcionalidade de currículos.
2. Criar uma versão com título identificável.
3. Selecionar o modelo de apresentação permitido.
4. Conferir a versão criada.

**Resultado esperado:** versão associada ao estudante autenticado.

**Evidência:** identificação fictícia da versão e resultado da criação.

**Resultado da execução:** pendente.

### DEM-06 — Seleção e organização das informações

**Objetivo:** conferir a composição de uma versão.

Procedimento:

1. Selecionar a versão criada.
2. Incluir informações disponíveis do perfil.
3. Conferir os itens selecionados.
4. Alterar a ordem das seções, caso o recurso esteja disponível na interface.
5. Consultar novamente a composição.

**Resultado esperado:** a versão utiliza somente os itens selecionados, preservando os dados originais do perfil.

**Evidência:** seleção realizada, ordem das seções e identificação da versão.

**Resultado da execução:** pendente.

### DEM-07 — Revisão guiada

**Objetivo:** verificar a identificação de informações ausentes e recomendações.

Procedimento:

1. Solicitar a revisão de uma versão.
2. Conferir os erros e avisos retornados.
3. Identificar a seção correspondente a cada pendência.
4. Quando possível, registrar uma decisão sobre um aviso.
5. Consultar as decisões registradas.

**Resultado esperado:** o sistema diferencia erros obrigatórios de avisos e somente permite aceitar ou rejeitar recomendações classificadas como aviso.

**Evidência:** resultado da revisão e decisões registradas.

**Resultado da execução:** pendente.

### DEM-08 — Prévia e modelos de currículo

**Objetivo:** verificar a apresentação do currículo.

Procedimento:

1. Abrir a prévia da versão.
2. Conferir as informações selecionadas.
3. Verificar a ordem das seções.
4. Conferir a apresentação no modelo clássico ou compacto.
5. Verificar uma seção sem itens, quando aplicável.

**Resultado esperado:** a prévia apresenta as informações da versão sem inserir dados que não foram cadastrados.

**Evidência:** captura da prévia com dados fictícios, modelo e versão identificados.

**Resultado da execução:** pendente.

### DEM-09 — Exportação em PDF

**Objetivo:** verificar a geração e o download de um currículo em PDF.

Procedimento:

1. Selecionar a versão desejada.
2. Solicitar a exportação PDF pelo fluxo disponível.
3. Aguardar a geração do arquivo.
4. Conferir o arquivo disponibilizado.
5. Abrir o PDF em aplicativo compatível.
6. Verificar legibilidade, conteúdo e organização.

**Resultado esperado:** arquivo PDF correspondente à versão solicitada, com conteúdo válido e apresentação legível.

**Evidência:** arquivo gerado, resultado HTTP quando aplicável e capturas das páginas, sem dados reais.

**Resultado da execução:** pendente.

**Observação:** existe implementação de exportação PDF no backend. A disponibilidade do controle de download na interface deve ser confirmada no ambiente apresentado.

### DEM-10 — Exportação em DOCX

**Objetivo:** verificar a geração e o download do currículo em DOCX.

Procedimento:

1. Selecionar uma versão de currículo.
2. Solicitar a exportação DOCX pelo fluxo disponível.
3. Conferir o arquivo gerado.
4. Abrir o documento em editor compatível.
5. Verificar conteúdo e formatação.

**Resultado esperado:** documento DOCX válido e correspondente à versão selecionada.

**Evidência:** arquivo, resultado da operação e registro de abertura em editor compatível.

**Resultado da execução:** pendente.

**Observação:** a existência da rota de exportação no backend não substitui a demonstração da integração com a interface.

### DEM-11 — Busca de vagas

**Objetivo:** verificar a consulta de oportunidades profissionais.

Procedimento:

1. Acessar a funcionalidade de vagas, quando disponível.
2. Informar um termo de busca.
3. Utilizar filtros de localização e modalidade, se aplicável.
4. Solicitar a consulta.
5. Conferir os resultados apresentados.

**Resultado esperado:** vagas apresentadas conforme a resposta do serviço configurado.

**Evidência:** termo, filtros e resultados retornados, sem informações técnicas sensíveis.

**Resultado da execução:** pendente.

**Observação:** o funcionamento real da integração com o Grupo 2 deve ser confirmado. Respostas simuladas não devem ser apresentadas como resultados do serviço externo real.

### DEM-12 — Associação currículo-vaga

**Objetivo:** conferir o comportamento da associação entre currículo e oportunidade.

Procedimento:

1. Selecionar uma vaga disponível.
2. Selecionar uma versão de currículo.
3. Executar a associação, quando a funcionalidade estiver disponível.
4. Conferir o registro realizado.

**Resultado esperado:** a associação ocorre mediante ação do estudante, sem criação automática apenas pela realização de uma busca.

**Evidência:** resposta da operação e identificação fictícia da associação.

**Resultado da execução:** pendente.

## 5. Roteiro de falhas esperadas

Os cenários abaixo devem ser executados somente em ambiente controlado.

Os resultados descritos são expectativas baseadas nos contratos disponíveis, e não evidências de que os testes tenham sido executados.

| ID | Cenário | Resultado esperado | Evidência |
|---|---|---|---|
| FAL-01 | Requisição protegida sem autenticação | Recusa da operação, normalmente HTTP `401` | Status e mensagem |
| FAL-02 | Identificador UUID inválido | Erro de validação HTTP `422` | Resposta sanitizada |
| FAL-03 | Dados obrigatórios inválidos | Recusa de validação conforme o contrato da rota | Campos e status |
| FAL-04 | Currículo inexistente | HTTP `404` nas operações que utilizam versão | Status e mensagem |
| FAL-05 | Tentativa de acesso a currículo alheio | Acesso recusado, sem exposição de dados | Resposta sanitizada |
| FAL-06 | Executor de funcionalidade indisponível | HTTP `503` no contrato correspondente | Status e mensagem |
| FAL-07 | Falha na geração de PDF ou DOCX | HTTP `500` com mensagem controlada | Status sem stack trace |
| FAL-08 | Serviço de vagas com resposta inválida | HTTP `502` na rota de busca | Mensagem controlada |
| FAL-09 | Timeout na consulta de vagas | HTTP `504` na rota de busca | Mensagem controlada |
| FAL-10 | Busca de vagas sem resultados | HTTP `200`, `total: 0` e lista vazia | Resposta com filtros |
| FAL-11 | Revisão com pendência obrigatória | `aprovado: false` e erro identificado | Resultado da revisão |
| FAL-12 | Decisão sobre código que não é aviso válido | Recusa da decisão, com HTTP `404` no contrato específico | Resposta sanitizada |

Em operações envolvendo a identidade do estudante, os códigos `403` e `404` devem ser conferidos conforme o middleware e o caso de uso correspondente.

Não é necessário provocar falhas reais no banco, derrubar serviços compartilhados ou utilizar dados de outros estudantes para executar esses cenários.

## 6. Detalhamento dos ensaios de falha

### 6.1. Sessão ausente

Executar uma chamada protegida sem uma sessão válida, em ambiente de teste.

Verificar se a operação é recusada e se não ocorre exposição de dados.

### 6.2. Currículo inexistente ou de outro estudante

Utilizar identificadores fictícios preparados para a demonstração.

Verificar se a aplicação impede o acesso e mantém a privacidade das informações.

### 6.3. Falha de exportação

Utilizar um teste controlado ou double configurado para representar falha de geração.

A resposta não deve disponibilizar arquivo parcial ou detalhes internos da biblioteca utilizada.

### 6.4. Indisponibilidade do Grupo 2

Quando a integração real não estiver configurada, demonstrar o estado indisponível de forma identificada.

Caso seja utilizado um double, registrar que o resultado é simulado.

### 6.5. Busca vazia

Realizar uma consulta cujo retorno de teste seja uma lista vazia.

O resultado esperado da API interna é manter os critérios de consulta e devolver:

- `total` igual a `0`;
- `vagas` como lista vazia;
- HTTP `200`.

### 6.6. Revisão com erros e avisos

Utilizar um currículo sintético preparado para apresentar pendências.

Conferir se os erros impedem a aprovação da revisão e se os avisos são apresentados separadamente.

A decisão de aceitar ou rejeitar deve ficar restrita às recomendações válidas.

## 7. Critérios de apresentação

Durante a demonstração:

- não apresentar dados pessoais reais;
- não mostrar senhas ou tokens;
- não utilizar serviços de produção para provocar falhas;
- identificar quando um cenário for simulado;
- informar quando uma funcionalidade ainda não estiver integrada;
- não declarar aprovação antes da conferência do resultado;
- registrar o commit e o ambiente utilizados.

A existência de testes unitários ou de integração isolada não comprova automaticamente o funcionamento de toda a jornada pela interface.

## 8. Registro dos resultados

Após executar o roteiro, preencher a situação de cada cenário.

Utilizar as classificações:

- **Aprovado:** resultado observado corresponde ao esperado.
- **Reprovado:** resultado observado diverge do esperado.
- **Não executado:** cenário não foi realizado.
- **Bloqueado:** não foi possível executar por dependência ou indisponibilidade.
- **Simulado:** cenário executado com double, mock ou ambiente controlado, sem comprovar integração real.

| ID | Resultado | Evidência | Observações |
|---|---|---|---|
| DEM-01 | Não executado | Pendente | — |
| DEM-02 | Não executado | Pendente | — |
| DEM-03 | Não executado | Pendente | — |
| DEM-04 | Não executado | Pendente | — |
| DEM-05 | Não executado | Pendente | — |
| DEM-06 | Não executado | Pendente | — |
| DEM-07 | Não executado | Pendente | — |
| DEM-08 | Não executado | Pendente | — |
| DEM-09 | Não executado | Pendente | — |
| DEM-10 | Não executado | Pendente | — |
| DEM-11 | Não executado | Pendente | — |
| DEM-12 | Não executado | Pendente | — |

Os resultados de FAL-01 a FAL-12 também deverão ser registrados quando os respectivos ensaios forem executados.

## 9. Identificação da sessão de demonstração

| Informação | Registro |
|---|---|
| Data e horário | Pendente |
| Responsável pela execução | Pendente |
| Participantes | Pendente |
| Ambiente | Pendente |
| Branch | Pendente |
| Commit | Pendente |
| Serviços utilizados | Pendente |
| Massa sintética utilizada | Pendente |
| Evidências | Pendente |
| Falhas encontradas | Pendente |

## 10. Tratamento das pendências

Se alguma etapa não puder ser concluída, registrar:

1. Identificação do cenário.
2. Resultado esperado.
3. Resultado observado.
4. Evidência disponível.
5. Impacto na demonstração.
6. Responsável pelo acompanhamento.
7. Prazo de correção, quando definido.

A pendência deverá ser comunicada ao responsável técnico ou ao GP, conforme sua área.

Não registrar como aprovado um cenário que foi somente preparado, mas não executado.

## 11. Relação com a aceitação do projeto

Este checklist serve como base para a demonstração e a coleta de evidências.

Os resultados efetivamente observados deverão apoiar:

- a issue #389, referente aos resultados da aceitação e à decisão de entrega;
- a issue #390, referente ao encerramento e às lições aprendidas;
- a issue #436, referente à consolidação do dossiê de aceite.

O checklist não representa decisão formal de entrega nem substitui o aceite do GP.

## 12. Referências

- `docs/massa_teste_curriculos.json`
- `src/backend/tests/fixtures/massa_teste_curriculos.py`
- `docs/configuracao-ambiente.md`
- `docs/dossie-aceite.md`
- `docs/registro-aceite-licoes.md`
- `docs/manual-estudante.md`
- `docs/guia-exportacao-pdf-docx.md`
- `src/backend/api/exportacao_curriculo.py`
- `src/backend/api/revisao_versao_curriculo.py`
- `src/backend/api/vagas.py`
- `src/frontend/app/jornada-selecao-previa-exportacao.e2e.test.tsx`

## 13. Rastreabilidade

- **Issue:** #388 — F10.6
- **WBS:** 1.8.2.1–1.8.2.4
- **Entrega documental:** checklist de demonstração e roteiro de falhas esperadas
- **Massa de dados:** perfis sintéticos versionados no repositório
- **Situação da execução:** pendente

## 14. Conclusão

Este roteiro reúne as principais etapas da demonstração do Sistema Currículo, os dados sintéticos disponíveis e os cenários de falha que devem ser verificados.

A preparação permite organizar a apresentação, identificar dependências e registrar os resultados de maneira padronizada.

A execução deverá ocorrer no ambiente escolhido pela equipe, com identificação da versão apresentada e das evidências produzidas.

**O checklist está documentado, mas os resultados da demonstração permanecem pendentes até a realização dos testes correspondentes.**
