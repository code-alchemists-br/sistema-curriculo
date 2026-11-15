# Registro de Lições Aprendidas e Aceite do Projeto

**Projeto:** Sistema Currículo — FATEC-SP  
**Issue:** #390 — F10.8  
**WBS:** 1.8.2.1–1.8.2.4  
**Data da atualização:** 04/11/2026  
**Branch de referência:** `dev`  
**Situação:** Lições preliminares documentadas; decisão formal de aceite pendente.

## 1. Objetivo

Este documento reúne as principais lições identificadas a partir do desenvolvimento e da documentação do Sistema Currículo, além de preparar o registro da decisão de aceite ou não aceite no encerramento do projeto.

As observações apresentadas foram baseadas nos documentos e nas entregas disponíveis no repositório. Elas devem ser confirmadas pela equipe durante a avaliação final.

A decisão de aceite será registrada somente após a manifestação dos responsáveis pela avaliação do projeto.

## 2. Contexto do projeto

O Sistema Currículo foi desenvolvido para permitir que estudantes organizem informações pessoais, acadêmicas e profissionais, criem versões de currículo e realizem exportações em PDF e DOCX.

O sistema também prevê integração com o Grupo 2 para consulta de vagas e associação de oportunidades a currículos.

Durante o desenvolvimento, foram produzidos componentes de interface, funcionalidades de backend, contratos de integração, testes e documentos técnicos.

Essas entregas servem de referência para identificar práticas que podem ser mantidas e pontos que merecem melhorias em projetos futuros.

## 3. Situação das atividades de encerramento

| Issue | Atividade | Situação documental |
|---|---|---|
| #388 | Checklist de demonstração | PR preparado; execução da demonstração ainda precisa ser comprovada |
| #389 | Resultados, pendências e decisão de entrega | PR #622 incorporado à `dev` |
| #390 | Lições aprendidas e aceite | Registro preliminar em elaboração |
| #436 | Consolidação final do dossiê | Aguardando informações finais de encerramento |

O merge da #389 confirma que sua documentação foi incorporada ao projeto, mas não substitui a decisão formal sobre o aceite do sistema.

## 4. Lições aprendidas preliminares

### LA-01 — Manter a documentação atualizada

**Situação identificada:**

Durante o desenvolvimento, algumas funcionalidades avançaram enquanto documentos existentes ainda descreviam versões anteriores do sistema.

Um exemplo foi a exportação PDF e DOCX, que passou a contar com rotas no backend, exigindo a atualização dos materiais de orientação.

**Impacto:** documentos desatualizados podem causar dúvidas sobre quais funcionalidades já estão disponíveis e quais ainda dependem de integração.

**Lição aprendida proposta:** a documentação deve acompanhar as alterações implementadas, principalmente quando uma funcionalidade passa a ter novos comportamentos ou contratos.

**Melhoria recomendada:** incluir a conferência da documentação pública entre as verificações necessárias para concluir uma funcionalidade.

**Evidências:** `docs/manual-estudante.md`, `docs/exportacao-pdf-docx.md` e `src/backend/api/exportacao_curriculo.py`.

**Validação pela equipe:** pendente.

### LA-02 — Alinhar os contratos de integração entre equipes

**Situação identificada:**

A integração com o Grupo 2 exigiu alinhamentos sobre os dados enviados, respostas esperadas e parâmetros de consulta de vagas.

Entre os pontos registrados estão a utilização do parâmetro `limit` e a decisão de não utilizar paginação.

**Impacto potencial:** diferenças entre o contrato acordado e o comportamento implementado podem gerar incompatibilidades e retrabalho.

**Lição aprendida proposta:** os contratos de integração devem ser definidos e revisados em conjunto pelas equipes envolvidas.

**Melhoria recomendada:** manter um documento de contrato compartilhado, incluindo exemplos de requisições, respostas e tratamento de falhas.

**Evidências:** issue #428 e documentação de integração com o Grupo 2.

**Validação pela equipe:** pendente.

### LA-03 — Diferenciar testes isolados da validação completa do sistema

**Situação identificada:**

O projeto possui testes de funcionalidades específicas, como revisão de currículo e exportação, além de um checklist preparado para demonstrar a jornada do estudante.

Entretanto, os testes isolados e o funcionamento integrado da aplicação representam verificações diferentes.

**Impacto:** considerar um módulo isolado como comprovação de toda a jornada pode levar a uma avaliação incompleta da entrega.

**Lição aprendida proposta:** a equipe deve separar os resultados dos testes técnicos das evidências de demonstração e aceitação.

**Melhoria recomendada:** preparar o roteiro de demonstração com antecedência e registrar os resultados realmente observados, incluindo ambiente, commit e evidências.

**Evidências:** `docs/checklist-demonstracao.md` e `docs/dossie-aceite.md`.

**Validação pela equipe:** pendente.

### LA-04 — Considerar falhas desde o planejamento

**Situação identificada:**

As funcionalidades do sistema precisam lidar com situações como ausência de autenticação, currículos não encontrados, falhas na geração de arquivos e indisponibilidade de serviços externos.

Esses comportamentos foram considerados nos contratos das APIs e no roteiro de demonstração.

**Impacto potencial:** falhas sem tratamento adequado podem comprometer a experiência do estudante e dificultar a identificação dos problemas.

**Lição aprendida proposta:** os cenários negativos precisam ser planejados e testados juntamente com os fluxos principais.

**Melhoria recomendada:** documentar as falhas esperadas e garantir que os testes verifiquem as respostas e mensagens apresentadas.

**Evidências:** `src/backend/api/exportacao_curriculo.py`, `src/backend/api/vagas.py` e `docs/checklist-demonstracao.md`.

**Validação pela equipe:** pendente.

### LA-05 — Utilizar dados sintéticos nas demonstrações

**Situação identificada:**

O projeto possui uma massa de dados fictícios com diferentes perfis de estudantes e currículos.

Esses registros podem apoiar testes e demonstrações sem exigir a utilização de informações pessoais reais.

**Impacto esperado:** a utilização de dados sintéticos facilita a reprodução de cenários e diminui riscos relacionados à exposição de informações pessoais.

**Lição aprendida proposta:** preparar dados de teste consistentes desde o desenvolvimento facilita a validação e a apresentação das funcionalidades.

**Melhoria recomendada:** manter a massa de teste atualizada e verificar sua compatibilidade com os modelos de domínio antes de cada demonstração.

**Evidências:** `docs/massa_teste_curriculos.json` e `src/backend/tests/fixtures/massa_teste_curriculos.py`.

**Validação pela equipe:** pendente.

## 5. Lições adicionais da equipe

As lições anteriores são observações preliminares baseadas no repositório.

Durante a reunião de encerramento, os integrantes poderão confirmar essas observações, complementar informações ou registrar outras situações vivenciadas no desenvolvimento.

| Tema | Situação observada | Impacto | Melhoria recomendada |
|---|---|---|---|
| Organização das tarefas | A confirmar pela equipe | Pendente | Pendente |
| Comunicação entre integrantes | A confirmar pela equipe | Pendente | Pendente |
| Integração entre funcionalidades | A confirmar pela equipe | Pendente | Pendente |
| Testes e validações | A confirmar pela equipe | Pendente | Pendente |
| Distribuição das responsabilidades | A confirmar pela equipe | Pendente | Pendente |

## 6. Critérios para o aceite final

A decisão de aceite deverá considerar:

1. Atendimento aos requisitos definidos para a entrega.
2. Resultados da demonstração das principais funcionalidades.
3. Funcionamento da criação, revisão e visualização de currículos.
4. Exportação em PDF e DOCX.
5. Situação da integração com o Grupo 2.
6. Tratamento das principais falhas esperadas.
7. Pendências conhecidas e seus impactos.
8. Avaliação dos responsáveis pelo projeto.

As evidências deverão ser relacionadas ao ambiente e à versão efetivamente avaliados.

## 7. Registro da avaliação final

| Informação | Registro |
|---|---|
| Data da avaliação | Pendente |
| Responsáveis pela avaliação | Pendente |
| Participantes | Pendente |
| Ambiente utilizado | Pendente |
| Branch e commit avaliados | Pendente |
| Evidências da demonstração | Pendente |
| Pendências identificadas | A confirmar |
| Resultado da avaliação | Pendente |

## 8. Decisão de aceite ou não aceite

**Situação atual: aguardando decisão formal.**

Após a avaliação, registrar a alternativa correspondente:

- [ ] Aceito.
- [ ] Não aceito.

**Responsável pela decisão:** pendente.

**Data:** pendente.

**Justificativa:** pendente.

**Evidências utilizadas:** pendente.

Se a equipe utilizar formalmente a modalidade de aceite com ressalvas, essa opção também poderá ser registrada conforme os critérios adotados para o encerramento.

### Em caso de não aceite

Se o produto não for aceito, registrar:

- requisitos ou critérios não atendidos;
- problemas encontrados durante a avaliação;
- evidências que justificam a decisão;
- correções necessárias;
- responsáveis e prazos definidos;
- necessidade de uma nova demonstração ou avaliação.

A ausência de uma decisão formal não deve ser interpretada automaticamente como reprovação.

## 9. Pendências para o encerramento

Conforme o dossiê de aceitação, os seguintes pontos ainda precisam ter suas evidências confirmadas:

| ID | Pendência | Situação |
|---|---|---|
| P01 | Demonstração completa da jornada do estudante | A confirmar |
| P02 | Download de PDF e DOCX pela interface | A confirmar |
| P03 | Integração com o Grupo 2 | A confirmar |
| P04 | Tratamento de falhas em ambiente integrado | A confirmar |
| P05 | Registro dos resultados e evidências da demonstração | Pendente de comprovação |
| P06 | Responsáveis e prazos para eventuais correções | A definir |
| P07 | Decisão formal sobre aceite e entrega | Pendente |

Essas pendências representam o estado das evidências documentais consultadas. Sua presença não significa necessariamente que exista um defeito no sistema.

## 10. Próximas ações

Para concluir o encerramento, será necessário:

1. Confirmar os resultados da demonstração do sistema.
2. Registrar as evidências e possíveis falhas.
3. Discutir as lições aprendidas com os integrantes.
4. Confirmar quais melhorias devem ser mantidas no registro final.
5. Obter a decisão formal de aceite ou não aceite.
6. Registrar a justificativa da decisão.
7. Atualizar o dossiê consolidado de encerramento.

## 11. Referências

- `docs/checklist-demonstracao.md`
- `docs/dossie-aceite.md`
- `docs/manual-estudante.md`
- `docs/massa_teste_curriculos.json`
- `docs/exportacao-pdf-docx.md`
- `src/backend/api/exportacao_curriculo.py`
- `src/backend/api/vagas.py`
- Issue #388 — Checklist de demonstração
- Issue #389 — Resultados e pendências de aceitação
- Issue #390 — Lições aprendidas e aceite
- Issue #436 — Dossiê consolidado

## 12. Conclusão

A revisão documental permitiu identificar observações relevantes sobre a atualização dos documentos, o alinhamento entre equipes, os testes integrados, o tratamento de falhas e a utilização de dados sintéticos.

Essas observações foram organizadas como lições preliminares e recomendações para futuros trabalhos, sujeitas à confirmação dos integrantes.

O registro está preparado para receber as informações do encerramento. Entretanto, a decisão final de aceite ou não aceite permanece pendente até a avaliação formal pelos responsáveis.

**Estado da issue #390:** documentação preliminar preparada, aguardando confirmação das lições e decisão de encerramento.
