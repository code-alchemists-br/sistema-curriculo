# Dossiê de Aceitação — Resultados, Pendências e Decisão de Entrega

**Projeto:** Sistema Currículo — FATEC-SP  
**Issue principal:** #389 — F10.7  
**Data de atualização documental:** 01/11/2026  
**Branch de referência:** `dev`  
**Estado:** Consolidação documental realizada; aceite e decisão final de entrega pendentes de validação formal.

## 1. Objetivo

Este documento reúne as evidências técnicas disponíveis, os resultados registrados de validação, as pendências conhecidas e a situação da decisão de entrega do Sistema Currículo.

O objetivo é facilitar a revisão da equipe e do Gerente de Projeto (GP), permitindo identificar quais funcionalidades possuem evidências de implementação e testes e quais ainda precisam de demonstração ou confirmação.

A existência de código, testes automatizados ou documentação não representa, isoladamente, o aceite final do produto. Por isso, os resultados técnicos são apresentados separadamente da decisão formal de entrega.

## 2. Escopo da aceitação

A avaliação considera as principais funcionalidades previstas para o estudante:

1. Cadastro e autenticação.
2. Gerenciamento de dados pessoais e profissionais.
3. Criação e edição de versões de currículo.
4. Seleção e organização dos itens do currículo.
5. Visualização da prévia e dos modelos disponíveis.
6. Exportação em PDF e DOCX.
7. Busca de vagas e integração com o Grupo 2.
8. Associação entre currículos e vagas.
9. Segurança, autorização e tratamento de falhas.
10. Funcionamento integrado da jornada do estudante.

O aceite final deverá considerar tanto os requisitos funcionais quanto os requisitos não funcionais aplicáveis.

## 3. Critérios utilizados na avaliação

Foram considerados os seguintes tipos de evidência:

- existência de implementação correspondente no repositório;
- testes unitários e de integração documentados;
- registros de validação funcional;
- resultados de testes de legibilidade e exportação;
- documentos de contrato e arquitetura;
- demonstrações executadas com registro de ambiente, versão e resultados;
- identificação de pendências e limitações conhecidas.

Os critérios devem ser avaliados conforme as evidências realmente disponíveis.

Não se considera uma funcionalidade completamente aceita apenas porque o endpoint correspondente existe ou porque um teste isolado foi criado.

## 4. Resultados técnicos identificados

A tabela apresenta a situação verificável na documentação e no código consultados. Ela não substitui uma execução completa da homologação.

| Área | Evidência identificada | Resultado documental | Limitação |
|---|---|---|---|
| Autenticação e sessão | Contrato de credenciais e testes de autenticação | Contrato e mecanismos documentados | Necessária validação no ambiente final |
| Perfil e dados complementares | Rotas e testes específicos no backend | Implementações e testes identificados | Não comprova toda a jornada pelo frontend |
| Versões de currículo | Casos de uso, rotas e persistência | Estruturas disponíveis para composição das versões | Verificar fluxo completo na demonstração |
| Seções e modelos | Domínio e componentes de apresentação | Modelos e regras documentados | Confirmar comportamento integrado na interface |
| Prévia | Endpoint e testes de prévia | Contrato e testes existentes | Prévia isolada não comprova jornada completa |
| Exportação DOCX | Caso de uso, rota e testes de exportação | Suporte técnico identificado no backend | Confirmar download pela interface final |
| Exportação PDF | Rota, gerador e relatório de legibilidade | Validação técnica documentada | Confirmar o fluxo integrado na demonstração |
| Busca de vagas | Endpoint, adapter e testes | Consulta e tratamento de erros documentados | Integração real com Grupo 2 ainda exige comprovação |
| Associação currículo-vaga | Modelos e operações relacionadas | Implementações identificadas | Conferir fluxo completo com vagas externas |
| Segurança e falhas | Middleware, regras de propriedade e testes | Controles implementados e documentados | Exige validação nos cenários integrados |

**Interpretação:** a tabela comprova a existência de entregas e evidências técnicas consultadas, mas não autoriza marcar todas as áreas como aprovadas na homologação final.

## 5. Resultado registrado para exportação PDF

O relatório `docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md`, relacionado à issue #410, registra uma avaliação realizada em 26/10/2026.

Os cenários documentados foram:

| Cenário | Resultado registrado |
|---|---|
| Currículo padrão com uma página | Nenhuma falha registrada |
| Currículo extenso com duas páginas | Nenhuma falha registrada |
| Geometria e dimensões A4 | Validação documentada |
| Organização dos blocos e títulos | Sem falhas registradas nos cenários |
| Apresentação dos modelos | Testes específicos identificados |

O relatório apresenta o veredito **APROVADO**, com zero falhas por página nos cenários avaliados.

Esse resultado deve ser interpretado como aprovação da validação técnica descrita no relatório, e não como aprovação automática de toda a funcionalidade na interface web ou da entrega completa do projeto.

## 6. Situação da exportação PDF e DOCX

A implementação atual do backend disponibiliza as rotas:

- `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/pdf`
- `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/docx`

As rotas estão relacionadas aos mecanismos de autenticação, propriedade da versão e geração dos arquivos.

A documentação de uso para estudantes está vinculada à issue #386, já encerrada no backlog consultado.

**Pendência de aceitação:** confirmar, em demonstração, que o estudante consegue selecionar sua versão e baixar os arquivos pelos controles da interface, utilizando o ambiente que será entregue.

## 7. Situação da integração com o Grupo 2

O Sistema Currículo possui estruturas internas para consulta de vagas, incluindo a porta `BuscadorVagas`, o caso de uso `ConsultarVagas`, o DTO `VagaExternaDto` e o adapter de comunicação externa.

Também existe documentação arquitetural sobre o contrato do Grupo 2, relacionada à issue #428.

Entretanto, a existência desse contrato não comprova, por si só, que os dois sistemas já foram executados de forma integrada em um mesmo ambiente.

A aceitação dessa funcionalidade deve confirmar:

- disponibilidade do endpoint externo efetivamente acordado;
- compatibilidade do payload de currículo;
- funcionamento do parâmetro `limit`, de 1 a 100, com padrão inicial de 10;
- ausência de paginação, conforme alinhamento entre as equipes;
- interpretação correta das vagas retornadas;
- tratamento de respostas vazias e falhas externas;
- apresentação dos resultados na interface;
- preservação da regra de associação manual entre currículo e vaga.

Até que existam evidências da execução integrada, essa validação permanece pendente.

## 8. Pendências conhecidas

As pendências a seguir devem ser consideradas na preparação da decisão final de entrega.

| ID | Pendência | Impacto | Situação |
|---|---|---|---|
| P01 | Executar demonstração completa da jornada do estudante | Impede comprovar o fluxo de ponta a ponta | A validar |
| P02 | Confirmar download de PDF e DOCX pela interface | Impede confirmar a experiência completa de exportação | A validar |
| P03 | Validar comunicação real com o Grupo 2 | Impede comprovar a integração entre os projetos | A validar |
| P04 | Confirmar tratamento de falhas com serviços integrados | Pode afetar a recuperação diante de erros | A validar |
| P05 | Registrar ambiente, commit e evidências da demonstração | Dificulta reproduzir e auditar os resultados | Pendente de registro |
| P06 | Registrar responsáveis e prazos de correção para falhas eventualmente identificadas | Dificulta o acompanhamento pós-avaliação | Pendente de definição |
| P07 | Obter decisão formal sobre aceite e entrega | Impede registrar a conclusão da homologação | Pendente |

As pendências listadas como "A validar" representam ausência de comprovação suficiente nesta consolidação documental. Não significam necessariamente defeitos confirmados na implementação.

Caso uma pendência seja resolvida, deve ser registrada a evidência correspondente antes da alteração de sua situação.

## 9. Registro dos testes de aceitação

A execução formal deverá utilizar o roteiro `docs/checklist-demonstracao.md` e registrar os resultados observados.

| Cenário | Resultado esperado | Resultado da aceitação |
|---|---|---|
| Acesso do estudante | Autenticação e acesso aos recursos próprios | Aguardando registro da demonstração |
| Cadastro e edição de informações | Dados válidos salvos corretamente | Aguardando registro da demonstração |
| Criação de versão | Versão vinculada ao estudante | Aguardando registro da demonstração |
| Seleção e organização de itens | Conteúdo e ordem correspondentes à escolha | Aguardando registro da demonstração |
| Prévia do currículo | Apresentação coerente com a versão | Aguardando registro da demonstração |
| Exportação PDF | Arquivo válido e legível | Evidência técnica disponível; fluxo completo a validar |
| Exportação DOCX | Arquivo válido e editável | Evidência técnica disponível; fluxo completo a validar |
| Consulta de vagas | Resultados coerentes com os critérios | Integração externa a validar |
| Tratamento de falhas | Mensagens seguras e comportamento controlado | Execução integrada a validar |

Não foram atribuídos resultados "Aprovado" ou "Reprovado" à demonstração completa sem registros observáveis da sua execução.

## 10. Registro da demonstração

Os campos abaixo deverão ser preenchidos após a realização da demonstração:

| Informação | Registro |
|---|---|
| Data de execução | Pendente |
| Ambiente utilizado | Pendente |
| Branch e commit avaliados | Pendente |
| Responsáveis pela execução | Pendente |
| Participantes da avaliação | Pendente |
| Roteiro utilizado | `docs/checklist-demonstracao.md` |
| Evidências da execução | Pendente |
| Falhas observadas | Pendente |
| Resultado consolidado | Pendente |

As evidências devem utilizar dados sintéticos, sem exposição de senhas, tokens ou informações pessoais reais.

## 11. Critérios para decisão de entrega

A decisão final deverá considerar:

1. O cumprimento dos requisitos acordados para a versão.
2. Os resultados efetivamente observados na demonstração.
3. A disponibilidade das funcionalidades essenciais.
4. A existência de falhas que impeçam a utilização do produto.
5. O impacto das pendências conhecidas.
6. A existência de responsáveis e prazos para eventuais correções.
7. A concordância dos responsáveis pela avaliação e do GP.

A decisão pode resultar em aceite, aceite com ressalvas ou não aceite, conforme o processo de aprovação adotado pela equipe.

Nenhuma dessas alternativas deve ser registrada como decisão definitiva sem manifestação dos responsáveis.

## 12. Situação da decisão de entrega

**Situação atual: aguardando deliberação formal.**

A documentação e o código consultados demonstram avanços técnicos relevantes, mas não apresentam registro suficiente para afirmar que o sistema completo já foi homologado e aceito para entrega.

A decisão definitiva deverá ser tomada pelo GP e pelos responsáveis pela aceitação, considerando a demonstração e as pendências efetivamente verificadas.

**Decisão formal:** pendente.

**Responsável pela aprovação:** a confirmar com o GP.

**Data da decisão:** pendente.

**Justificativa final:** preencher após a avaliação.

Este registro não representa reprovação do projeto. Ele indica que a aceitação formal ainda não foi comprovada pelas evidências disponíveis.

## 13. Próximas ações

Para concluir o processo de aceitação:

1. Executar os cenários previstos no checklist de demonstração.
2. Registrar ambiente, versão e evidências de cada cenário.
3. Identificar eventuais falhas e classificá-las conforme o impacto.
4. Confirmar responsáveis e prazos para correções necessárias.
5. Submeter os resultados ao GP.
6. Registrar a decisão de entrega após sua aprovação.
7. Atualizar o documento de lições aprendidas no encerramento.

## 14. Rastreabilidade

| Referência | Relação com o aceite |
|---|---|
| #386 — F10.4 | Instruções de exportação |
| #388 — F10.6 | Roteiro de demonstração |
| #389 — F10.7 | Resultados, pendências e decisão de entrega |
| #390 — F10.8 | Registro final de lições e aceite |
| #410 — F11.12 | Evidência de legibilidade do PDF |
| #428 — F12.9 | Decisão do contrato de integração com Grupo 2 |
| #436 — F12.16 | Consolidação final do dossiê de aceite |

## 15. Documentos e evidências relacionados

- `docs/checklist-demonstracao.md`
- `docs/registro-aceite-licoes.md`
- `docs/notas-versao-2026-10.md`
- `docs/exportacao-pdf-docx.md`
- `docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md`
- `src/backend/api/exportacao_curriculo.py`
- `src/backend/api/vagas.py`
- `src/backend/application/exportacao_curriculo.py`
- `src/backend/application/consulta_vagas.py`

## 16. Conclusão

A consolidação apresenta os resultados técnicos identificados e as principais pendências que precisam ser verificadas antes da decisão final de entrega.

O projeto possui implementações e evidências documentadas em áreas relevantes, incluindo autenticação, gerenciamento de currículo, exportação e busca de vagas.

Entretanto, a aprovação definitiva depende da execução dos cenários integrados e do registro formal da decisão pelos responsáveis.

Este documento deverá ser atualizado quando novas evidências forem produzidas, mantendo a rastreabilidade entre os resultados observados, as pendências e a decisão de entrega.
