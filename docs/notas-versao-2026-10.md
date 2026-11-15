# Notas de Versão — Sistema Currículo

**Projeto:** Sistema Currículo — FATEC-SP  
**Issue:** #434 — F12.14  
**WBS:** 1.1.2.4, 1.8.2.1–1.8.2.4  
**Atualização documental:** 09/11/2026  
**Branch de referência:** `dev`  
**Status:** Notas de versão em preparação para entrega e validação final.

## 1. Apresentação

Este documento apresenta o estado das principais funcionalidades desenvolvidas no Sistema Currículo, as limitações identificadas e as pendências que precisam ser verificadas antes da entrega final.

O objetivo é oferecer uma visão clara do que está implementado, quais recursos possuem evidências técnicas e quais ainda dependem de integração, demonstração ou aprovação.

As informações foram organizadas a partir dos documentos e das implementações consultadas no repositório.

Estas notas não representam um anúncio de implantação em produção nem confirmam o aceite final do produto.

## 2. Identificação da versão

| Informação | Registro |
|---|---|
| Projeto | Sistema Currículo |
| Instituição | FATEC São Paulo |
| Versão de referência | Estado de desenvolvimento da branch `dev` |
| Número de release | Ainda não definido |
| Data de publicação | Não definida |
| Ambiente de produção | Não comprovado |
| Situação do aceite | Aguardando confirmação formal |

O commit exato deverá ser registrado quando a equipe definir a versão candidata à entrega.

Enquanto isso, este documento apresenta uma consolidação das funcionalidades e evidências conhecidas, sujeita à atualização conforme a evolução do projeto.

## 3. Resumo das entregas

O Sistema Currículo reúne funcionalidades destinadas ao cadastro de informações do estudante, à montagem de versões de currículo e à preparação de documentos para processos seletivos.

O desenvolvimento contempla recursos de autenticação, gerenciamento de dados, criação e edição de versões, seleção de itens, prévia, revisão, exportação e integração com serviços de vagas.

Parte dessas capacidades está implementada em módulos do backend ou em componentes específicos do frontend.

Entretanto, a existência desses recursos não garante, isoladamente, que a jornada completa já funcione em um único ambiente integrado.

## 4. Funcionalidades implementadas e documentadas

### 4.1. Autenticação e controle de acesso

O projeto possui mecanismos de autenticação e contratos relacionados ao acesso do estudante às funcionalidades protegidas.

Entre os recursos identificados estão:

- autenticação de usuários;
- identificação de sessões;
- proteção de operações que exigem autenticação;
- regras de autorização e acesso aos dados próprios;
- respostas controladas para solicitações não autorizadas.

**Situação:** mecanismos e contratos documentados, com necessidade de validação no ambiente final.

### 4.2. Cadastro de informações pessoais e profissionais

O backend possui funcionalidades e contratos destinados ao registro de informações que compõem o perfil do estudante.

As categorias contempladas incluem:

- dados pessoais e de contato;
- formação acadêmica;
- experiências profissionais;
- competências;
- idiomas;
- projetos acadêmicos;
- cursos e outras informações complementares, conforme os módulos disponíveis.

Esses dados servem como base para a elaboração das versões de currículo.

**Situação:** implementações específicas identificadas; a jornada completa de cadastro e edição ainda precisa de confirmação integrada.

### 4.3. Criação e edição de versões de currículo

O sistema possui operações para criar e editar versões de currículo.

Cada versão permite organizar informações do perfil de acordo com um objetivo profissional.

Os contratos disponíveis contemplam informações como:

- título da versão;
- modelo de apresentação;
- visibilidade;
- vínculo com o estudante;
- organização das seções.

A utilização de diferentes versões permite preparar currículos com seleções distintas sem exigir um novo cadastro completo.

**Situação:** operações implementadas no backend; interação completa pela interface sujeita à validação.

### 4.4. Seleção de informações

O projeto possui operações para selecionar e desselecionar informações associadas às versões de currículo.

Os tipos de itens contemplados incluem formação acadêmica, experiência profissional, projetos acadêmicos, competências, idiomas e documentos.

A seleção determina quais informações serão utilizadas em uma versão específica.

A operação não deve excluir os registros originais do perfil.

**Situação:** contratos e operações de seleção disponíveis no backend; fluxo visual completo ainda sujeito à demonstração.

### 4.5. Modelos e apresentação do currículo

O projeto possui definições de modelos e componentes responsáveis pela apresentação visual do currículo.

A implementação documentada inclui componentes dos modelos Clássico e Compacto, além de um catálogo mais amplo de modelos planejados.

Os modelos são responsáveis pela apresentação das informações, sem alterar o significado dos dados cadastrados.

**Situação:** componentes e regras documentados; a disponibilidade dos modelos na interface final precisa ser confirmada.

### 4.6. Prévia do currículo

O backend possui uma operação de consulta à prévia da versão.

A resposta reúne as informações selecionadas e organizadas, permitindo que o frontend apresente o conteúdo antes da exportação.

A documentação também contempla diferentes estados de apresentação:

- carregamento;
- prévia disponível;
- seções vazias;
- falha na consulta.

A prévia deve apresentar somente os itens correspondentes à versão consultada.

**Situação:** contrato e testes específicos identificados; funcionamento completo na interface depende de validação integrada.

### 4.7. Revisão do currículo

O projeto dispõe de funcionalidades para analisar informações obrigatórias e apontar pendências na versão do currículo.

A revisão diferencia erros e avisos.

Erros indicam situações que impedem a aprovação da revisão, enquanto avisos representam recomendações que não possuem o mesmo efeito bloqueante.

Essa funcionalidade permite orientar a conferência do conteúdo antes da visualização ou exportação.

**Situação:** mecanismos de revisão identificados no backend; apresentação e interação pela interface devem ser confirmadas.

### 4.8. Exportação em PDF

O backend possui uma rota de exportação de currículos em PDF:

`GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/pdf`

A operação está relacionada à geração de um arquivo a partir da versão solicitada, considerando as regras de autenticação e propriedade.

O projeto também possui um relatório de validação técnica da legibilidade de PDFs, vinculado à issue #410.

Esse relatório registra aprovação nos cenários avaliados, incluindo currículo de uma página, currículo extenso e conferência de dimensões e organização.

**Situação:** geração e evidência técnica documentadas no backend. O download completo pela interface ainda precisa ser confirmado em demonstração.

### 4.9. Exportação em DOCX

O backend também possui uma rota de exportação em DOCX:

`GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/docx`

O formato permite obter uma versão do currículo compatível com aplicativos de edição de documentos.

O sistema possui contratos e testes relacionados à exportação.

**Situação:** suporte técnico identificado no backend. A experiência completa de download e abertura do arquivo deve ser verificada na versão final.

### 4.10. Consulta de vagas e integração com o Grupo 2

O projeto possui estruturas relacionadas à consulta de oportunidades profissionais.

Entre os componentes identificados estão a porta `BuscadorVagas`, o caso de uso `ConsultarVagas`, o DTO `VagaExternaDto` e o adaptador de comunicação externa.

O contrato documentado contempla critérios de consulta, limites de resultados e tratamento de falhas.

A integração também prevê a utilização das oportunidades em funcionalidades relacionadas ao currículo.

**Situação:** estrutura interna e contrato documentados; a comunicação real com o serviço do Grupo 2 ainda exige comprovação em ambiente integrado.

### 4.11. Associação entre currículo e vagas

O projeto possui modelos e operações relacionadas à associação de oportunidades profissionais às versões de currículo.

Essa capacidade permite organizar relações entre currículos e vagas consultadas.

**Situação:** implementações relacionadas identificadas; fluxo completo com dados externos ainda precisa de validação.

### 4.12. Tratamento de falhas e segurança

Os módulos de backend contemplam respostas para diferentes situações de erro.

Entre os cenários previstos estão:

- ausência ou invalidade da autenticação;
- recursos não encontrados;
- dados inválidos;
- tentativa de acesso a recursos não autorizados;
- indisponibilidade de operações;
- falhas de serviços externos;
- problemas na geração de arquivos.

Esses mecanismos são importantes para evitar a exposição de informações técnicas desnecessárias e oferecer respostas adequadas.

**Situação:** controles e testes específicos identificados; comportamento integrado ainda sujeito à validação.

## 5. Documentação disponibilizada

O projeto possui documentos voltados ao desenvolvimento, à utilização e à aceitação das funcionalidades.

Entre as principais entregas documentais estão:

| Documento | Finalidade |
|---|---|
| `docs/manual-estudante.md` | Orientar a utilização do sistema |
| `docs/guia-exportacao-pdf-docx.md` | Detalhar a exportação e os cuidados com arquivos |
| `docs/mapeamento_jornadas.md` | Descrever a jornada do estudante |
| `docs/checklist-demonstracao.md` | Preparar a demonstração com dados sintéticos |
| `docs/dossie-aceite.md` | Consolidar evidências e pendências de aceitação |
| `docs/registro-aceite-licoes.md` | Registrar lições aprendidas e decisão de encerramento |
| `docs/previa-curriculo.md` | Documentar o contrato e os estados da prévia |
| `docs/modelos_curriculo.md` | Definir o catálogo e as características dos modelos |

A existência de um documento não significa que todas as funcionalidades nele descritas tenham sido validadas de ponta a ponta.

## 6. Limitações conhecidas

### L01 — Jornada completa ainda não comprovada

Embora existam operações de backend e componentes de interface, a documentação consultada ainda não apresenta evidência suficiente de execução e aprovação de toda a jornada do estudante em um único ambiente.

**Impacto:** não é possível declarar o fluxo completo como homologado apenas com base nos módulos isolados.

### L02 — Exportação pela interface depende de confirmação

As operações de PDF e DOCX existem no backend, mas a integração do download aos controles finais da interface precisa ser demonstrada.

**Impacto:** a disponibilidade dos endpoints não comprova a experiência completa de exportação pelo estudante.

### L03 — Integração externa com o Grupo 2 depende de validação

O projeto possui contratos e componentes internos para consulta de vagas.

Entretanto, a documentação de aceite ainda exige comprovação da comunicação real entre os sistemas.

**Impacto:** não se deve considerar a busca de vagas integrada como homologada sem evidência dessa execução.

### L04 — Catálogo de modelos e interface

O catálogo planejado contém mais opções do que os componentes de visualização especificamente documentados.

**Impacto:** modelos previstos no planejamento não devem ser anunciados como disponíveis sem confirmação na implementação e na interface.

### L05 — Testes isolados não equivalem a homologação

O projeto possui testes automatizados e evidências técnicas para determinadas funcionalidades.

Entretanto, esses resultados não substituem a demonstração das operações realizadas pelo estudante.

**Impacto:** o aceite final deve considerar o comportamento integrado e os critérios da entrega.

### L06 — Ambiente de produção não confirmado

As evidências consultadas se referem principalmente ao desenvolvimento, aos testes e à documentação do projeto.

**Impacto:** estas notas não podem ser utilizadas para afirmar que o sistema já foi publicado e disponibilizado em produção.

## 7. Pendências conhecidas

A tabela utiliza como referência as pendências apresentadas no dossiê de aceitação.

| ID | Pendência | Situação documental |
|---|---|---|
| P01 | Executar e comprovar a jornada completa do estudante | A validar |
| P02 | Confirmar download PDF/DOCX na interface final | A validar |
| P03 | Validar a comunicação real com o Grupo 2 | A validar |
| P04 | Confirmar o tratamento de falhas em serviços integrados | A validar |
| P05 | Registrar ambiente, commit e evidências da demonstração | Pendente de comprovação |
| P06 | Identificar responsáveis e prazos para correções eventualmente necessárias | A definir |
| P07 | Registrar a decisão formal de aceite e entrega | Pendente |

As pendências indicadas como "A validar" não representam necessariamente defeitos confirmados.

Elas demonstram que a documentação consultada ainda não apresenta comprovação suficiente para considerar determinadas verificações concluídas.

A situação deverá ser atualizada quando forem produzidas novas evidências.

## 8. Resultados de validação disponíveis

O projeto possui registros técnicos que podem apoiar o processo de aceitação.

Entre as evidências identificadas estão:

**Validação de PDF:** o relatório `docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md`, relacionado à issue #410, apresenta resultado aprovado para os cenários avaliados em 26/10/2026.

**Testes de contratos e APIs:** o repositório possui testes específicos de operações de cadastro, currículo, prévia, revisão, exportação e consulta de vagas.

**Testes de interface:** existem componentes e testes relacionados à apresentação do currículo e aos estados de seções vazias.

**Cenários E2E:** o repositório possui cenários de teste da jornada, mas a utilização de partes simuladas precisa ser diferenciada da execução real integrada.

Esses resultados demonstram avanços técnicos, mas não autorizam declarar toda a aplicação como aceita sem avaliação correspondente.

## 9. Orientações para utilização

As funcionalidades devem ser utilizadas conforme o ambiente e os recursos realmente disponibilizados.

Para consultar a jornada prevista do estudante, utilizar `docs/manual-estudante.md`.

Para informações sobre os formatos de exportação, consultar `docs/guia-exportacao-pdf-docx.md`.

Para verificar cenários de demonstração e falhas esperadas, utilizar `docs/checklist-demonstracao.md`.

Caso uma funcionalidade ainda não esteja disponível na interface, sua existência no backend deve ser tratada como uma capacidade técnica do projeto, não como uma ação já acessível ao usuário final.

## 10. Critérios para publicação de uma release

Antes da publicação de uma versão destinada aos estudantes, recomenda-se:

1. Definir a versão e registrar o commit correspondente.
2. Confirmar o ambiente de execução.
3. Executar os principais cenários da jornada do estudante.
4. Validar a exportação de arquivos pela interface.
5. Confirmar a situação da integração com o Grupo 2.
6. Registrar os resultados e as evidências de teste.
7. Classificar as pendências conhecidas conforme seu impacto.
8. Obter a decisão formal dos responsáveis pela entrega.
9. Atualizar estas notas para refletir somente as funcionalidades da versão publicada.

Essas atividades representam verificações necessárias para que as notas correspondam ao produto efetivamente entregue.

## 11. Rastreabilidade das entregas

| Issue | Relação com as notas de versão |
|---|---|
| #386 — F10.4 | Instruções de exportação PDF/DOCX |
| #388 — F10.6 | Checklist de demonstração |
| #389 — F10.7 | Resultados e pendências de aceitação |
| #390 — F10.8 | Lições aprendidas e aceite |
| #410 — F11.12 | Validação técnica de PDF |
| #428 — F12.9 | Contrato de integração com Grupo 2 |
| #432 — F12.12 | Jornada no manual do estudante |
| #433 — F12.13 | Orientações de exportação e falhas |
| #434 — F12.14 | Notas de versão |
| #436 — F12.16 | Consolidação do dossiê de aceitação |

A rastreabilidade relaciona os documentos e as funcionalidades às atividades correspondentes, sem presumir que todas as issues tenham sido encerradas.

## 12. Referências técnicas

As informações foram organizadas com base nos seguintes documentos e módulos:

- `docs/dossie-aceite.md`
- `docs/manual-estudante.md`
- `docs/checklist-demonstracao.md`
- `docs/registro-aceite-licoes.md`
- `docs/previa-curriculo.md`
- `docs/modelos_curriculo.md`
- `docs/testes/evidencias/f11-12-validacao-pdf-legibilidade.md`
- `src/backend/api/versao_curriculo.py`
- `src/backend/api/itens_versao_curriculo.py`
- `src/backend/api/previa_versao_curriculo.py`
- `src/backend/api/exportacao_curriculo.py`
- `src/backend/api/vagas.py`

## 13. Conclusão

O Sistema Currículo possui funcionalidades implementadas e documentadas em áreas importantes, como autenticação, gerenciamento de informações, versões de currículo, prévia, revisão, exportação e consulta de vagas.

As evidências disponíveis demonstram a existência de diferentes componentes e testes técnicos, mas ainda precisam ser complementadas com os resultados finais de integração e aceitação.

As principais limitações estão relacionadas à comprovação da jornada completa, ao download pela interface e à integração real com o Grupo 2.

Estas notas apresentam uma visão organizada do estado técnico e documental do projeto e poderão ser atualizadas quando a equipe definir a versão final, concluir as verificações pendentes e registrar a decisão formal de entrega.

**Estado da issue #434:** notas de versão elaboradas com funcionalidades, limitações, pendências conhecidas e referências de validação. A publicação de uma release final permanece condicionada à definição da versão e ao aceite do projeto.
