# Roteiro de aceitação da jornada completa com estudante representativo

## 1. Natureza, objetivo e status

**Documento operacional para execução humana futura. Este documento não é um teste e não é aceite. Status da sessão: não executado.** Nenhuma sessão foi executada e nenhum resultado foi preenchido na elaboração deste roteiro.

Base decisória: [análise v001, status proposed, alternativa A][AN]. Autoria documental direta autorizada pelo usuário, sem skill implementadora. O título fornecido é “Criar roteiro de aceitação com estudante representativo para a jornada completa.”; não há descrição ou critérios oficiais fornecidos. **O aceite oficial do card não é verificável.** Autorizar a escrita não aprova produto, participante ou política de aceite.

**Fotografia técnica por leitura:** commit d45115dc5d9fd75f336cc86281b687f49e3e0ffc, branch test-roteiro-jornada-completa. O git fetch origin concluiu com sucesso; origin/dev permaneceu nesse mesmo hash, e git log --oneline origin/dev..HEAD e git log --oneline HEAD..origin/dev não retornaram commits. Os dois destinos estavam ausentes antes da escrita; a análise já estava presente como arquivo não rastreado.

A jornada completa **não é executável na aplicação que sobe** nessa fotografia. As classes da seção 8 são planejamento, nunca resultados da pessoa. **Antes de qualquer sessão, engenharia deve repetir a leitura da composição, reclassificar cada etapa e registrar a versão efetivamente avaliada.** Mudança de hash, dependência ou composição invalida o uso automático desta fotografia.

O objetivo é observar ações, compreensão, ajuda e obstáculos de uma pessoa real usando somente dados sintéticos. O roteiro pode ser produzido com bloqueios; a execução futura depende das pré-condições. Não se inicia sessão apenas porque há componentes ou testes parciais.

## 2. Escopo e resultados do processo

O recorte combina a trilha de [mapeamento_jornadas.md][MJ], §§5–7, e [wireframes/README.md][WF00], com os ramos sistêmicos de [requisitos_funcionais.md][RF] e [casos-de-uso-v2.md][UC].

- **Trilha guiada:** J00 primeiro acesso; J01 cadastro/login; J03 painel/iniciar/retomar; J04 dados pessoais; J05 formação; J06 experiência; J07 complementares/projetos/orientação; J10 construção/itens/seções/modelo; J11 revisão/edição; J12 prévia; J13 geração/download PDF e DOCX.
- **Ramo alternativo de acesso:** J02 recuperação.
- **Gestão adicional:** J08 documentos complementares e J09 versões, conforme necessidade do cenário e confirmação de produto.
- **Oportunidades:** J14 busca/listagem/vazio/erro; J15 escolha de currículo, associação manual, classificação e consulta.

Os IDs J00–J15 são identificadores locais deste roteiro, não novos requisitos ou CT. A posição numérica não impõe sequência única. Documento complementar não é importação de currículo. Versões podem ser preparadas em ramo próprio; múltiplas versões não são requisito inventado para toda exportação. Busca/associação e exportação não se tornam obrigatórias entre si. Não se exige candidatura para gerar PDF.

Resultados previstos pelos artefatos: dados gerenciados e reutilizáveis; currículo organizado, revisado e visualizado; arquivo gerado/baixado; e, em ramo próprio, associação manual persistida. **Classificação “candidatura” não implica envio externo**, conforme RF12 e CT-RF12-08. Não abrir inscrição externa ou contatar anunciante.

Recrutador, IA, importação de currículo e exportação JSON não são adicionados como tarefas obrigatórias. Recrutador é opcional nos casos de uso; RF09 confirma PDF/DOCX; a trilha não exige IA. Ramos obrigatórios da sessão e entradas/retornos ainda são **a confirmar** em L02, seção 13.

## 3. Origem dos critérios

**Definido** indica comportamento explicitamente descrito em um artefato citado; não significa critério oficial fornecido para este card. **Inferido** indica método de observação, vínculo local, preparação ou regra propostos neste roteiro/análise; depende da confirmação indicada. A seção 10 identifica ambos em cada J.

A ação de referência do facilitador descreve a intenção para planejar; não é uma sequência de cliques a ensinar. A rastreabilidade J→RF/CT é interpretação documentada, sem criar ou ampliar os cenários da matriz.

Os critérios documentais por ID local estão resumidos abaixo. A interpretação de compreensão humana e a preparação de cada tarefa são inferidas, a confirmar em L02/L06/L09/L10; não alteram o comportamento definido citado. As condições e alternativas completas ficam na seção 10.

| ID local | Origem                                                            | Caminho, seção e trecho curto                                                                                            | Rastreabilidade                                     |
| -------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| J00      | Definido para acesso previsto; reconhecimento da landing inferido | [docs/wireframes/01-acesso.md][WF01], Objetivo: “Representar cadastro, login e recuperação de senha”                     | UC01/UC02; sem CT dedicado à landing                |
| J01      | Definido                                                          | [docs/wireframes/01-acesso.md][WF01], Navegação: “Após autenticação → Painel inicial”                                    | RF13, CT-RF13-01                                    |
| J02      | Definido                                                          | [docs/wireframes/01-acesso.md][WF01], Recuperação: “Enviar link” e “Retorno para login”                                  | UC02/RF-AUT-05; sem CT dedicado na matriz RF01–RF15 |
| J03      | Definido                                                          | [docs/wireframes/02-painel-inicial.md][WF02], Em preenchimento: “Continuar preenchimento”                                | RF03/RF14 relacionados; sem CT dedicado de retomada |
| J04      | Definido                                                          | [docs/matriz_testes.md][MT], CT-RF01-01: “Dados pessoais são salvos e confirmados ao estudante”                          | RF01/RF02, CT-RF01-01                               |
| J05      | Definido                                                          | [docs/wireframes/04-formacao.md][WF04], Lista: “curso, instituição, período e situação de conclusão”                     | RF01/RF02, CT-RF01-02                               |
| J06      | Definido; avanço sem experiência condicional                      | [docs/wireframes/05-experiencias.md][WF05], Lista: “organização, cargo, período e descrição”                             | RF01/RF02, CT-RF01-03                               |
| J07      | Definido                                                          | [docs/requisitos_funcionais.md][RF], RF04: “oferecer orientação para descrevê-los de forma clara e objetiva”             | RF04, CT-RF04-01–03                                 |
| J08      | Definido para capacidade; percurso humano inferido                | [docs/casos-de-uso-v2.md][UC], Armazenar documentos: “arquivos complementares, como certificados de cursos”              | RF-DADOS-07; sem CT dedicado na matriz RF01–RF15    |
| J09      | Definido                                                          | [docs/requisitos_funcionais.md][RF], RF14: “múltiplos currículos vinculados à sua conta”                                 | RF03/RF14, CT-RF14-01–04                            |
| J10      | Definido                                                          | [docs/matriz_testes.md][MT], CT-RF06-02: “Modelo é associado ao currículo em construção”                                 | RF03/RF05/RF06; CT-RF05-02/CT-RF06-02               |
| J11      | Definido                                                          | [docs/wireframes/07-revisao.md][WF07], Ações: “A edição retorna à etapa correspondente e depois à revisão”               | RF02/RF08, CT-RF08-01–03                            |
| J12      | Definido                                                          | [docs/wireframes/08-visualizacao-curriculo.md][WF08]: “A prévia representa os dados fornecidos e confirmados pelo aluno” | RF06/RF07, CT-RF07-01–03                            |
| J13      | Definido; método de abertura humana inferido                      | [docs/matriz_testes.md][MT], CT-RF09-03: “Conteúdo dos arquivos corresponde ao exibido na visualização”                  | RF09/RF15, CT-RF09-01–05                            |
| J14      | Definido                                                          | [docs/matriz_testes.md][MT], CT-RF11-03: “Página exibe mensagem de ausência de vagas”                                    | RF10/RF11, CT-RF10-01–04/CT-RF11-01–04              |
| J15      | Definido                                                          | [docs/requisitos_funcionais.md][RF], RN03: “Candidatura implica interesse”                                               | RF12/RF15, CT-RF12-02/05/08 e CT-RF15-02            |

RNF01–RNF03 se aplicam transversalmente como contexto de observação e limites, conforme a tabela seguinte; não constituem aprovação automática de todas essas qualidades.

| Base                        | Caminho, seção e trecho curto                                                                                                   | Origem e uso                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Dados e projetos            | [docs/requisitos_funcionais.md][RF], RF01–RF04: “cadastrar dados pessoais”, “centralizar” e “oferecer orientação”               | Definido: capacidade; passos J04–J10 delimitam o alcance de cada CT                           |
| Construção e resultado      | [docs/requisitos_funcionais.md][RF], RF05–RF09: organização, modelos, visualização, revisão e “PDF e DOCX”                      | Definido: comportamento J10–J13                                                               |
| Gestão e oportunidades      | [docs/requisitos_funcionais.md][RF], RF10–RF15/RN01–RN07: “iniciada manualmente” e “Candidatura implica interesse”              | Definido: J09/J14/J15, sem envio externo                                                      |
| Usabilidade                 | [docs/requisitos_nao_funcionais.md][RNF], RNF01: “critério de aceitação a validar”; verificação proposta: “sem auxílio externo” | A situação pendente é definida; perfil/amostra e política de ajuda são inferidos, a confirmar |
| Acessibilidade              | [docs/requisitos_nao_funcionais.md][RNF], RNF02; [docs/acessibilidade.md][AC], Padrão e Limites                                 | Definido: referência WCAG 2.2 AA; sessão não certifica conformidade integral                  |
| Compatibilidade             | [docs/requisitos_nao_funcionais.md][RNF], RNF03; [docs/compatibilidade-responsividade.md][CR], Navegadores/Larguras             | Definido: matriz de suporte; configuração da sessão a confirmar, sem generalização            |
| Falhas e retornos           | [docs/mapeamento_jornadas.md][MJ], §7: preservar valores, retomar e tentar novamente                                            | Definido, com opcionalidade de seções condicionada ao produto                                 |
| Casos rastreados            | [docs/matriz_testes.md][MT], cenários detalhados                                                                                | Definido: esperado do cenário, não evidência de execução                                      |
| Protocolo/estados/gravidade | [análise][AN], Especificação implementável, e este documento §§5–12                                                             | Inferido: política local proposta, a confirmar em L03–L08/L13/L15                             |

Não há tempo-alvo, taxa de sucesso ou exigência global de “zero defeitos”. O RNF01 não contém metas aprovadas. Tempos, tentativas e ajuda podem ser descritos posteriormente, sem corte quantitativo inventado. Não transpor regras de UI, exportação ou testes alheios à jornada sem fonte aplicável.

## 4. Ambiente e pré-condições

Usar ambiente autorizado e isolado com dados sintéticos. A preparação futura segue [docs/configuracao-ambiente.md][ENV], especialmente “Utilizando um ambiente Nix do projeto” e “Execução local segura”. Operações de repositório usam git fora de Nix; ferramentas de desenvolvimento usam o ambiente correspondente. Este roteiro não instala dependências, sobe serviços ou aplica migrations.

Na composição documentada, uvicorn backend.main:app é o ponto ASGI. Readiness/health não provam negócio: DATABASE_URL pode tornar o probe disponível sem conectar conta, currículo ou exportação. VITE_API_URL não resolve, sozinha, sessão e integração.

**Campos de sessão — preencher somente na cópia de execução futura, mantidos em branco aqui:**

- Referência/versão do roteiro:
- Commit/branch efetivamente avaliados:
- Ambiente/URL pública autorizada:
- Entrypoint/composição frontend e backend:
- Dependências reais e dependências simuladas:
- Conta sintética/estado inicial, sem credencial:
- Massa/variante e procedimento de reset:
- Sistema operacional:
- Navegador/versão:
- Dispositivo/viewport:
- Tecnologia assistiva pertinente, sem diagnóstico:
- Leitores de PDF/DOCX e versões:
- Responsável técnico pelo preflight:
- Reclassificação J00–J15 e referência de evidência:
- Confirmações de produto/design aplicáveis:
- Referência restrita do protocolo/consentimento:
- Restrições/condições de interrupção:

Conta, sessão, persistência, versões, seleção/modelo, revisão, prévia, download e vagas/associação devem ter dependências verificadas para cada tarefa prevista. Estado preparado ou harness deve ser declarado; não pode ser apresentado como percurso humano da aplicação. Os campos acima não registram a fotografia da autoria nem qualquer sessão realizada.

## 5. Perfil e recrutamento

**Recomendação condicional, padrão recomendado, a confirmar:** uma pessoa real estudante FATEC, buscando estágio ou próxima à conclusão, com pouca ou nenhuma experiência em elaborar currículo. O público vem de RF/UC; o foco em iniciante vem do RNF01. Pouca experiência em fazer currículo não equivale a ausência de experiência profissional.

Produto/design definem elegibilidade, quantidade e inclusão antes do convite, sem escolher nomes neste documento. Levantar dispositivo habitual, familiaridade com web e necessidade assistiva só no grau necessário para preparar a sessão, sem diagnóstico ou dado sensível. Não excluir pessoa por conveniência de suporte.

O ensaio é **qualitativo**: uma pessoa não representa toda a instituição e não fornece conclusão estatística ou taxa populacional. Persona/massa sintética fornece conteúdo; não substitui a pessoa real observada. Se a equipe exigir múltiplos perfis/configurações, aprovar plano de sessões separado.

Papéis propostos: produto confirma escopo/políticas e designa autoridade; design revisa neutralidade/acessibilidade; engenharia prepara/reclassifica; autor técnico/QA mantém rastreabilidade; facilitador observa e registra; participante realiza tarefas. Facilitador e observador podem ser o mesmo papel operacional. Validação do relato e decisão de aceite são responsabilidades distintas.

## 6. Privacidade e participação

Este protocolo adota a minimização e proteção de [docs/requisitos-seguranca.md][SEG], §§4.2/4.6–4.8/4.12–4.14, e o uso de dados fictícios de [docs/manual-estudante.md][MAN]. As regras de pesquisa são recomendações locais que exigem aprovação; não se presume que política de consentimento de outra funcionalidade as resolva.

Antes de iniciar, informar finalidade, atividades, forma de registro, acesso, voluntariedade, possibilidade de parar e como solicitar retirada. **Consentimento antes de iniciar; sem protocolo aprovado não se inicia sessão.** A aprovação deve existir mesmo se houver apenas notas. Registre somente uma referência restrita da autorização; nenhum termo assinado entra no Git.

Usar pseudônimo sem tabela de reidentificação no repositório. A pessoa usa **somente dados sintéticos**, não seu currículo, contato ou histórico reais. Sem gravação por padrão. Notas devem preferir paráfrases sem identificação; captura só quando necessária, autorizada e sanitizada.

- Acesso às evidências: **a definir**.
- Retenção: **a definir**.
- Descarte/retirada: **a definir**.
- Responsável pela guarda/protocolo: **a definir**.
- Local/provedor de guarda restrita: **a definir**.

Não aplicar o prazo de logs operacionais à evidência humana. Não versionar imagens, vídeos, PDF, DOCX, logs, cookies, tokens, credenciais, termo assinado ou dados reais. Credenciais só por canal restrito, fora do Git. Nenhum telefone/LinkedIn da massa deve ser contatado/aberto; nenhuma comunicação externa é autorizada por este roteiro. [docs/contrato-campos-obrigatorios-grupo2.md][CG2], §2, restringe identificadores diretos no intercâmbio; isso não autoriza transmitir dados de participante.

Se aparecer dado real ou segredo, interromper a captura/atividade pertinente, limitar registro ao necessário e encaminhar ao responsável. Não copiar o valor para relatar o incidente.

## 7. Massa e preparação

M1 é referência ao currículo fictício de **Ana Beatriz Souza**, em [docs/massa_teste_curriculos.json][MASSA], primeiro item de curriculos. Não é o nome da participante. Objetivo: estágio em desenvolvimento web; graduação em andamento, experiência, projeto de controle de estudos, competências e idiomas; documentos vazios.

| Conteúdo de M1                                | Uso planejado                                 | Limite                                                                        |
| --------------------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------------- |
| Identificação/contato sintéticos              | Cadastro e cabeçalho J01/J04                  | Credencial não está na massa; não copiar hash de fixture como senha           |
| Formação na Universidade Estadual de Campinas | J05                                           | Ana é da Unicamp na massa, não FATEC; adequação ao público é parcial          |
| Experiência/projeto/competências/idiomas      | J06/J07 e reutilização J10–J13                | Não define experiência em fazer currículo, dispositivo ou acessibilidade      |
| Versão privada/layout da massa                | Referência de conteúdo, não conta operacional | JSON/fixture não provisiona ambiente ou sessão                                |
| Telefone e LinkedIn com aparência plausível   | Apenas conteúdo sintético quando pertinente   | Não contatar, abrir, publicar como pessoa real ou usar para receber mensagens |

**M2 — variantes condicionais a preparar posteriormente**, a confirmar L05/L09/L10, sem editar o JSON:

- Sem experiência: usar conteúdo sintético de M1 com seção vazia no cenário autorizado, sem inventar emprego. Não presumir que a revisão permite avançar até produto confirmar a regra aplicável.
- Sem formação: só conforme política confirmada; não transformar opcionalidade condicional em obrigatoriedade ou permissão global.
- Vazio/rascunho/concluído e segunda versão: preparar estados identificáveis e reset seguro, sem alegar que fixture prova navegação.
- Documento complementar, curso/certificação e vaga: dados/arquivo sintéticos aprovados antes da sessão; Ana não fornece documento, nem a massa fornece integração de vagas.
- Erro de exportação e busca resultado/vazio/erro: engenharia prepara cenários seguros e identifica a simulação. Não provocar falha externa ou usar produção.

O contrato de integração [CG2], §3.6/§6, **define** não bloquear estudante sem experiência nesse contrato. O mapeamento §7 mantém avanço sem formação/experiência condicional ao produto; não transferir regra do matcher ou de um harness para revisão/exportação. Essa divergência é registrada em 13.2.

## 8. Preflight de engenharia e planejamento de executabilidade

E = executável na aplicação que sobe, somente no alcance descrito. T = parcial apenas com composição de teste; não é homologação humana. B = finalidade funcional bloqueada por ausência de implementação/composição. **As classes abaixo são planejamento por leitura, não resultado de sessão.** B pode coexistir com apoio T ou interação visual E; o apoio não muda o estado da finalidade.

### 8.1. Evidências de composição relidas

Todos os caminhos abaixo são relativos à raiz do repositório.

| ID  | Evidência de leitura                                                                                                                                                | Constatação                                                                                                                             |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| E01 | [src/backend/main.py][MAIN] e [autenticador_sessao_indisponivel.py][AUTH]                                                                                           | main não injeta executores de negócio; autenticador sempre rejeita token                                                                |
| E02 | [src/backend/api/factory.py][FACTORY] e routers listados abaixo                                                                                                     | Recebe None, registra capacidades/indisponibilidade; assistente determinístico tem default; não inclui router de associação/recuperação |
| E03 | [src/frontend/app/App.tsx][APP]                                                                                                                                     | Landing, acesso e etapas locais; não compõe painel autenticado, recuperação, documentos, gestão, prévia/download ou vagas/associação    |
| E04 | [PaginaAcessoEstudante.tsx][PACCESS] e [cliente-acesso-estudante.ts][CACCESS]                                                                                       | Cliente HTTP existe, sem transição ao painel autenticado; sessão entre origens não comprovada                                           |
| E05 | [PaginaRecuperacaoSenha.tsx][PREC] e [cliente-recuperacao-senha.ts][CREC]                                                                                           | Cliente indisponível; página independente não montada em App                                                                            |
| E06 | [PaginaDadosPessoais.tsx][PDATA] e [cliente-dados-pessoais.ts][CDATA]                                                                                               | Default indisponível, sem integração de salvar                                                                                          |
| E07 | [PaginaFormacaoAcademica.tsx][PFORM] e [cliente-formacao-academica.ts][CFORM]                                                                                       | Default indisponível; escrita backend não significa consulta integrada                                                                  |
| E08 | [PaginaExperienciasProfissionais.tsx][PEXP] e [FormularioExperiencias.tsx][FEXP]                                                                                    | onSalvar opcional não fornecido por App                                                                                                 |
| E09 | [PaginaCursosIdiomas.tsx][PCOURSE], [PaginaCompetencias.tsx][PSKILL], [PaginaCadastroProjetosAcademicos.tsx][PPROJECT] e [cliente-projetos-academicos.ts][CPROJECT] | Cursos/idiomas/competências/certificações sem salvamento remoto composto; projeto indisponível                                          |
| E10 | [PaginaSelecaoModeloCurriculo.tsx][PMODEL] e App                                                                                                                    | Seleção local; callback de App só muda etapa                                                                                            |
| E11 | [PaginaValidacaoCurriculo.tsx][PREVIEW] e App                                                                                                                       | Defaults em vez dos dados salvos; sem callbacks de prévia/PDF/confirmação                                                               |
| E12 | [PaginaVagasGrupo2.tsx][PJOBS] e [cliente-vagas-grupo2.ts][CJOBS]                                                                                                   | Default indisponível, clientes substituíveis; página ausente em App                                                                     |

Routers existentes e relidos como capacidades, não como integração operacional: [cadastro/acesso][RACCESS], [perfil][RPROFILE], [contato][RCONTACT], [formação][RFORM], [experiência][REXP], [documento][RDOC], [versão][RVERSION], [itens][RITEM], [listagem][RLIST], [exclusão de versão][RDELETE], [revisão][RREVIEW], [prévia][RPREVIEW], [exportação][REXPORT] e [vagas][RJOBS]. Ausência de executor pode levar a indisponibilidade; autenticação pode negar antes. Não presumir status 503 para toda requisição.

### 8.2. Classificação por finalidade

| Etapa | Classe de planejamento | Evidência/alcance                                         |
| ----- | ---------------------- | --------------------------------------------------------- |
| J00   | E                      | E03: apresentação e navegação pública local               |
| J01   | B; apoio T             | E01/E02/E04: conta/sessão sem composição de negócio       |
| J02   | B                      | E02/E03/E05: recuperação independente e indisponível      |
| J03   | B                      | E01/E03: sem painel persistido/retomada                   |
| J04   | B; apoio T             | E01/E02/E06: cliente indisponível                         |
| J05   | B; apoio T             | E01/E02/E07: escrita não ligada, consulta incompleta      |
| J06   | B                      | E01/E02/E08: onSalvar sem conexão                         |
| J07   | B; apoio T             | E01/E02/E09: defaults/callbacks sem persistência          |
| J08   | B; apoio T             | E01/E02/E03: documentos sem percurso composto             |
| J09   | B; apoio T             | E01/E02/E03: gestão de versões não composta               |
| J10   | B; visual E e apoio T  | E01/E02/E03/E10: escolha local não persistida             |
| J11   | B; apoio T             | E01/E02/E03/E11: revisão com defaults                     |
| J12   | B; apoio T             | E01/E02/E03/E11: sem prévia conectada                     |
| J13   | B; apoio T             | E01/E02/E03/E11: download sem callbacks/exportadores      |
| J14   | B; apoio T             | E01/E02/E03/E12: vagas sem cliente/rota integrada ao App  |
| J15   | B; apoio T             | E02/E03 e apoio técnico: sem interface/HTTP de associação |

Não houve mudança de executabilidade em relação à fotografia da análise, pois a base permanece no mesmo commit. Refinamento da notação: a finalidade fica B e T aparece como apoio, evitando chamar uma etapa humana completa de executável em teste. Nova leitura de J02 confirma diretamente o default indisponível da página que a análise apenas havia inventariado.

### 8.3. Protocolo para liberar ou bloquear a sessão futura

1. Registrar versão, diferenças de ambiente e situação de cada confirmação L01–L15 na cópia futura; não preencher este original.
2. Reler MAIN/FACTORY/APP, páginas/clientes/rotas do alvo; reclassificar J00–J15 e identificar cada dependência real/simulada.
3. Verificar, na atividade técnica futura autorizada, conta e sessão reais, salvamento e releitura, versões/seleções/modelo, revisão/retorno, prévia e exportação por formato; vagas e associação quando incluídas. Não equiparar probe disponível a integração.
4. Confirmar reset seguro e dados sintéticos, configurações, critérios e protocolo/consentimento antes do convite e da sessão.
5. Se faltar implementação/composição, não prescrever cliques ou trocar silenciosamente por harness. Registrar futuramente o impedimento na tarefa e nas dependentes; tarefas independentes só com escopo declarado, sem alegar percurso contínuo.
6. Engenharia pode usar evidência técnica existente como apoio, separada do relato humano. Simulação requer identificação de fronteira; não libera aceite sistêmico.
7. Interromper se houver dado real, exposição indevida, risco não previsto ou retirada da pessoa. Não corrigir produto durante a sessão sob autorização deste roteiro.

Bloqueios preexistentes não são escopo de correção: composição de negócio ausente; autenticação fechada; rotas/fluxos faltantes; defaults locais; consultas incompletas e, conforme leitura dos metadados de migrations na análise, revisões duplicadas. A preparação do alvo deve confirmar a cadeia vigente; não linearizar migrations, editar Nix ou inventar seed/conta operacional nesta tarefa.

## 9. Protocolo do facilitador

1. Após preflight e consentimento aprovados, informar que se observa o sistema, não o desempenho escolar/profissional da pessoa. Oferecer interrupção livre e dados sintéticos.
2. Apresentar apenas o objetivo neutro de cada tarefa elegível da seção 10. Não fornecer sequência de cliques ou resposta esperada; os campos de referência são preparação do facilitador.
3. Observar ação espontânea, compreensão, hesitação, erro, retorno e pedido de ajuda. Perguntar de forma neutra o que a pessoa entendeu do retorno. Pensar em voz alta é opcional.
4. Registrar tempo/tentativas apenas como medida descritiva se acordado. Separar **sem ajuda** de **concluído com ajuda**, anotando intervenção e momento; ajuda não satisfaz silenciosamente a proposta “sem auxílio externo” do RNF01.
5. Manter a tentativa assistida distinguível da tentativa inicial. Se faltar regra/oráculo, não forçar passa/falha: registrar futuramente a falta de conclusão e encaminhar ao responsável.
6. Não solicitar ataque a outra conta, falha externa, exposição de token ou todas as combinações técnicas. Usar apenas estados previamente preparados, com fonte real/simulada declarada.
7. Ao encerrar, contabilizar tarefas realmente realizadas e impedimentos, revisar paráfrases com a pessoa quando ela desejar e encaminhar a decisão ao signatário autorizado. Fim da sessão não é aceite.

## 10. Passos da trilha e dos ramos

As intenções abaixo descrevem a sessão futura. Em classe B, ficam registradas como intenção, pré-condição e impedimento; **não executar nem inventar uma interface**. Não há células de resultado preenchidas nesta seção. Cada confirmação da compreensão é observação qualitativa inferida sob RNF01/L06, não meta já aprovada.

### 10.1. J00 — Primeiro acesso

- **ID e ramo:** J00; Entrada comum.
- **Objetivo para o estudante:** “Conheça o sistema e identifique por onde começaria a preparar seu currículo.”
- **Ação de referência do facilitador:** Observar o reconhecimento das ações de acesso e criação, sem indicar qual escolher.
- **Pré-condição:** Instância acessível e configuração registrada; não requer dados curriculares prévios.
- **Dados:** Nenhum dado pessoal ou credencial.
- **Resultado esperado:** Ponto de entrada compreensível para acessar/criar conta e iniciar a preparação.
- **Critério e origem:** **Definido:** representação do acesso em [WF01], seção Objetivo. **Inferido:** observar se a pessoa identifica o início sem orientação, conforme RNF01 e L06; o wireframe não especifica a landing atual.
- **Requisito e caso de teste:** UC01/UC02; RNF01–RNF03 como observação contextual; **sem CT dedicado** à landing.
- **Evidência mínima futura:** Nota do caminho percebido, ação espontânea e eventual ajuda, sem captura de credenciais.
- **Classe de planejamento, não resultado:** **E**, restrito à apresentação e navegação pública local. E01 e E03: App monta PaginaInicio e pode mostrar acesso ou dados pessoais; leitura não atesta renderização/usabilidade.
- **Dependência:** Pode ser observado separadamente. Prosseguir a J01 depende de composição de conta; entrar em formulário sem sessão não demonstra autenticação.
- **Alternativa/falha:** Pessoa pode preferir cadastro ou login. Não converter entrada direta em dados em prova de acesso autorizado.
- **Limite atual:** Não demonstra criação de conta, painel autenticado ou continuidade da jornada.

### 10.2. J01 — Cadastro e login

- **ID e ramo:** J01; Acesso à conta.
- **Objetivo para o estudante:** “Obtenha acesso à sua conta de demonstração para preparar um currículo.”
- **Ação de referência do facilitador:** Distinguir criação e acesso com conta sintética; observar entendimento do retorno e da sessão, sem instruir navegação inexistente.
- **Pré-condição:** Cadastro/login realmente compostos, conta de demonstração e credenciais fornecidas fora do Git; transição autenticada validada no preflight.
- **Dados:** Nome/e-mail sintéticos da massa M1; credencial própria do ambiente por canal restrito.
- **Resultado esperado:** Conta criada quando aplicável; credenciais válidas concedem acesso aos próprios dados e ao painel previsto.
- **Critério e origem:** **Definido:** [WF01], Navegação: “Após autenticação → Painel inicial”; [MT], CT-RF13-01: “Acesso é concedido”. **Inferido:** desdobrar cadastro/login em tentativas separadas na sessão; L02/L06.
- **Requisito e caso de teste:** UC01/UC02, RF13; CT-RF13-01. CT-RF13-02/03 e RNF04 são referências técnicas de negação, sem ataque a conta alheia.
- **Evidência mínima futura:** Confirmação observada e continuidade com a própria conta, sem nome de login, senha, cookie ou token no relato.
- **Classe de planejamento, não resultado:** **B** na aplicação; **T** apenas como apoio técnico parcial. E01/E02 não injetam cadastro/acesso/sessão; E04 tem cliente HTTP, sem navegação autenticada ao painel.
- **Dependência:** Entrada J00; condiciona operações pessoais seguintes. Apoio T não é instância de homologação.
- **Alternativa/falha:** Campo/credencial inválida têm estados definidos em WF01. Observar erro compreensível e correção somente em cenário seguro previamente preparado.
- **Limite atual:** Não verifica conta persistida, sessão em navegador nem continuidade real. O teste de ciclo de perfil não certifica main.

### 10.3. J02 — Recuperar senha

- **ID e ramo:** J02; Alternativo de acesso, não obrigatório a cada login.
- **Objetivo para o estudante:** “Recupere o acesso à conta de demonstração se não lembrar sua credencial.”
- **Ação de referência do facilitador:** Registrar a intenção de recuperação; não prescrever botões, URL ou envio enquanto o fluxo não estiver composto.
- **Pré-condição:** Conta e caixa de mensagens de demonstração controlada pela engenharia; serviço e tela conectados; nenhum e-mail para pessoa externa.
- **Dados:** Identificador sintético M1; tokens/links de recuperação permanecem fora da evidência.
- **Resultado esperado:** Solicitação de recuperação por e-mail e retorno ao acesso; fluxo de segurança prevê credencial atualizada sem exposição do token.
- **Critério e origem:** **Definido:** [WF01], Recuperação: “Enviar link” e “Retorno para login”; [UC], Realizar login e recuperar senha; [SEG], §2.8. **Inferido:** forma de preparar o canal de demonstração, L10.
- **Requisito e caso de teste:** UC02, RF-AUT-05; **sem CT dedicado** na matriz RF01–RF15. RNF02/RNF03 são contexto, não aceite integral.
- **Evidência mínima futura:** Nota de solicitação e retorno alcançados, sem transcrever endereço, link ou código.
- **Classe de planejamento, não resultado:** **B**. E05: página independente com cliente indisponível; não montada por App; E02 não registra recuperação.
- **Dependência:** Ramo de J01 com pré-condições próprias; sua ausência não exige executar recuperação para gerar PDF.
- **Alternativa/falha:** Falha controlada ou campo inválido só quando cenário e esperado forem definidos; não simular sucesso de envio.
- **Limite atual:** Não verifica envio/recebimento, validade/uso único do token ou retorno efetivo ao acesso.

### 10.4. J03 — Painel, iniciar e retomar

- **ID e ramo:** J03; Continuidade da trilha guiada.
- **Objetivo para o estudante:** “Identifique o estado do currículo e continue o que já tiver começado.”
- **Ação de referência do facilitador:** Preparar, em execução futura autorizada, os estados vazio, rascunho e concluído; observar decisão sem ensinar caminho.
- **Pré-condição:** Conta autenticada; painel com estado persistido e rascunho/retomada implementados; massa inicial identificada.
- **Dados:** M1 e variantes M2 de vazio/rascunho/concluído, preparadas somente em ambiente autorizado.
- **Resultado esperado:** Estado vazio permite iniciar; rascunho indica etapa/progresso e retomada; concluído permite visualizar/exportar.
- **Critério e origem:** **Definido:** [WF02], estados; [MJ], §6.2 e §7: “continuar de onde parou”. **Inferido:** modo de preparar/resetar estados e evidência de retomada, L05/L10.
- **Requisito e caso de teste:** RF03/RF14 como vínculo inferido; CT-RF03-01 e CT-RF14-02 relacionados; **sem CT dedicado** de rascunho/retomada.
- **Evidência mínima futura:** Nota do estado apresentado, ponto interrompido e ponto retomado, sem preencher isso durante a autoria.
- **Classe de planejamento, não resultado:** **B**. E03 compõe landing pública, não painel por estado curricular; E01/E02 não fornecem composição de rascunho.
- **Dependência:** J01; dados podem ser iniciados ou retomados conforme estado. Não presumir que selecionar uma URL recupere progresso.
- **Alternativa/falha:** Interrupção solicitada → salvar rascunho → retomada, segundo MJ §7; não confundir estado React com persistência.
- **Limite atual:** Não verifica painel autenticado, salvamento ou recuperação do ponto interrompido.

### 10.5. J04 — Dados pessoais

- **ID e ramo:** J04; Preenchimento guiado.
- **Objetivo para o estudante:** “Prepare os dados fictícios de identificação e contato que devem aparecer no currículo.”
- **Ação de referência do facilitador:** Observar preenchimento, tentativa de salvar, reconhecimento de erro e correção, apenas após ligação real ser confirmada.
- **Pré-condição:** Conta própria, salvamento/releitura integrados e campos efetivos confrontados com o contrato antes da sessão.
- **Dados:** M1: identificação, e-mail, telefone e cidade sintéticos; não contatar telefone/links da massa.
- **Resultado esperado:** Informações válidas salvas e confirmadas; inválidas recebem mensagem contextual sem perda dos demais valores.
- **Critério e origem:** **Definido:** [WF03], Campos/Comportamentos; [MT], CT-RF01-01: “salvos e confirmados”; [MJ], §7 preserva dados em erro. **Inferido:** observar compreensão/ajuda, L06.
- **Requisito e caso de teste:** RF01/RF02/RF13; CT-RF01-01/05 e CT-RF02-01/05. CT-RF02-06 é referência técnica de autorização.
- **Evidência mínima futura:** Nota da confirmação, releitura dos campos sintéticos e entendimento do erro; nunca corpo bruto de requisição.
- **Classe de planejamento, não resultado:** **B**; **T** só parcial. E06: PaginaDadosPessoais usa cliente Indisponivel; E01/E02 não ligam perfil/contato. Há validação local, não salvamento integrado.
- **Dependência:** J01/J03 ou estado inicial equivalente explicitamente preparado; precede uso dos dados na revisão.
- **Alternativa/falha:** Campo obrigatório ausente/inválido → corrigir preservando valores. Falha de gravação CT-RF01-05 só em cenário técnico autorizado, não provocada pelo estudante.
- **Limite atual:** Não verifica salvamento, releitura ou propagação ao cabeçalho do currículo; validação local não basta.

### 10.6. J05 — Formação acadêmica

- **ID e ramo:** J05; Preenchimento guiado.
- **Objetivo para o estudante:** “Organize as formações fictícias pertinentes ao currículo.”
- **Ação de referência do facilitador:** Observar inclusão, conferência, edição e remoção de item sintético; não prometer listagem ainda ausente.
- **Pré-condição:** Conta, cadastro/consulta/edição/remoção integrados e política de ausência de formação confirmada.
- **Dados:** M1: graduação em andamento da massa; item adicional para edição/remoção a preparar com L09, sem alterar JSON.
- **Resultado esperado:** Formação salva e exibida com curso, instituição, período e situação; alterações/remoção se refletem na consulta.
- **Critério e origem:** **Definido:** [MJ], §6.4; [WF04], Lista/Ações; [MT], CT-RF01-02 e RF02. **Inferido:** aplicar o percurso de edição/remoção à formação como observação humana, sem atribuir CT-RF02-02/03 especificamente a ela.
- **Requisito e caso de teste:** UC03, RF01/RF02; CT-RF01-02 e CT-RF02-01. CT-RF02-02 descreve experiência e 03 competência; não são casos dedicados de edição/exclusão de formação.
- **Evidência mínima futura:** Nota comparando item sintético antes/depois e sua presença/ausência na consulta.
- **Classe de planejamento, não resultado:** **B**; **T** parcial. E07 usa cliente Indisponivel; E02 registra escrita de formação, E01 não injeta. Apoio técnico de formação declara ausência de GET/listagem HTTP.
- **Dependência:** J01 e dados do cenário; próxima etapa segundo WF04 é experiência, sem obrigar presença de item fictício.
- **Alternativa/falha:** Sem formação: esperado é condicional à política de produto (MJ §7, L05). Item já removido CT-RF02-04 é referência técnica, sem corrida provocada pela pessoa.
- **Limite atual:** Não verifica CRUD completo ou consulta pela interface real.

### 10.7. J06 — Experiência profissional

- **ID e ramo:** J06; Preenchimento; variante sem experiência.
- **Objetivo para o estudante:** “Organize as experiências fictícias que fizerem sentido, ou indique que não há experiência.”
- **Ação de referência do facilitador:** Observar organização, inclusão, edição, remoção e ordem sem induzir invenção de trabalho; usar variante sem experiência quando confirmada.
- **Pré-condição:** Conta e persistência/lista/ordem conectadas; política de opcionalidade e regra da revisão confirmadas em L05.
- **Dados:** M1: experiência sintética; variante M2 sem experiência, sem modificar a massa versionada.
- **Resultado esperado:** Quando informadas, organização, cargo, período e descrição são mantidos; edição/remover/ordenar controlados pelo aluno. Ausência não exige item fictício; avanço depende da regra confirmada.
- **Critério e origem:** **Definido:** [MJ], §6.5 e §7; [WF05], Lista/Ações. [CG2], §3.6 permite ausência no contrato de integração; não define sozinho avanço na revisão. **Inferido:** variante humana sem experiência como padrão recomendado, a confirmar.
- **Requisito e caso de teste:** UC04, RF01/RF02; CT-RF01-03, CT-RF02-02/04; sem CT dedicado à ausência de experiência na trilha.
- **Evidência mínima futura:** Nota de conteúdo/ordem percebidos ou da barreira encontrada pela variante, sem biografia real.
- **Classe de planejamento, não resultado:** **B**. E08: página repassa onSalvar opcional, App não o fornece. E02 registra casos de escrita, E01 não injeta.
- **Dependência:** J01; na trilha vem após formação. Não generalizar bloqueio de harness para regra de produto.
- **Alternativa/falha:** Validar campo e preservar valores; ramo sem experiência é condicional; interrupção/rascunho depende de J03.
- **Limite atual:** Não verifica persistência, ordenação final nem avanço integrado sem experiência.

### 10.8. J07 — Complementares, projetos e orientação

- **ID e ramo:** J07; Preenchimento guiado com grupos pertinentes.
- **Objetivo para o estudante:** “Complete o perfil fictício com habilidades, idiomas, cursos e projetos; use a orientação disponível se precisar.”
- **Ação de referência do facilitador:** Observar escolha dos grupos, manutenção de itens e compreensão da orientação; não sugerir texto nem exigir IA.
- **Pré-condição:** Conta e grupos a avaliar definidos; cadastro/consulta/manutenção conectados; assistência sem IA verificada pela engenharia.
- **Dados:** M1: projeto, competências e idiomas; cursos/certificações/links só com dados sintéticos previamente aprovados em L09.
- **Resultado esperado:** Informações fornecidas pelo aluno organizadas e salvas; projeto passa a constar no perfil; orientação clara disponível sem IA.
- **Critério e origem:** **Definido:** [WF06], Grupos/Ações; [MT], CT-RF04-01–03 e CT-RF01-04; [RF], RF04. **Inferido:** seleção de grupos por sessão, L02/L09.
- **Requisito e caso de teste:** RF01/RF02/RF04, RNF09/RNF10; CT-RF01-04/05, CT-RF04-01–03; não estender teste de curso/documento a todo o CRUD complementar.
- **Evidência mínima futura:** Nota de orientação compreendida, conteúdo sintético mantido e confirmação observada, sem ditar resposta.
- **Classe de planejamento, não resultado:** **B**; **T** parcial. E09: cursos/idiomas/competências/certificações sem onSalvar integrado; projetos com cliente Indisponivel. Assistente default na E02 não conecta etapa em E03.
- **Dependência:** J01; grupos não preenchidos seguem política de produto. Reutilizar na construção depende de J09/J10.
- **Alternativa/falha:** Campo inválido → corrigir preservando valores; não exigir upload de currículo ou sugestão de IA. Documento complementar pertence a J08.
- **Limite atual:** Não verifica persistência conjunta nem orientação utilizada numa jornada integrada.

### 10.9. J08 — Documentos complementares

- **ID e ramo:** J08; Gestão adicional fora do recorte guiado.
- **Objetivo para o estudante:** “Guarde e consulte um comprovante fictício pertinente ao perfil, se esse ramo fizer parte da sessão.”
- **Ação de referência do facilitador:** Descrever a intenção de guardar/consultar/remover documento, sem inventar interface ou local de armazenamento.
- **Pré-condição:** Conta, armazenamento/download protegido e interface compostos; arquivo sintético permitido pelo contrato e aprovado antes da sessão.
- **Dados:** M2: comprovante sintético a preparar; documentos de Ana estão vazios. Não usar certificado/portfólio real ou abrir URL externa da massa.
- **Resultado esperado:** Documento complementar guardado e acessível somente ao usuário autorizado; ações de download/exclusão só avaliadas no escopo confirmado.
- **Critério e origem:** **Definido:** [UC], Armazenar documentos; [SEG], §§4.6/4.14. **Inferido:** percurso humano de guardar/consultar/remover e preparação do arquivo, L02/L09.
- **Requisito e caso de teste:** Capacidade em UC, RF-DADOS-07; **sem CT dedicado** na matriz RF01–RF15. Não chamar importação de currículo de documento complementar.
- **Evidência mínima futura:** Nota da disponibilidade/remoção do arquivo sintético e proteção observável; sem anexar binário.
- **Classe de planejamento, não resultado:** **B**; **T** parcial. E03 não conecta documento; E02 registra armazenar/baixar/excluir e E01 não injeta.
- **Dependência:** J01 e estado de arquivo preparado. Não é pré-requisito presumido para PDF ou candidatura.
- **Alternativa/falha:** Documento ausente não exige fabricar arquivo real. Negativos de permissão são referências técnicas.
- **Limite atual:** Não verifica upload/download protegido pelo estudante, armazenamento real ou descarte.

### 10.10. J09 — Versões de currículo

- **ID e ramo:** J09; Gestão de versões, independente da busca de vagas.
- **Objetivo para o estudante:** “Organize versões do currículo fictício para objetivos diferentes e identifique qual deseja usar.”
- **Ação de referência do facilitador:** Observar criar, consultar, editar e excluir versão própria, preservando outra; sem instruir tela inexistente.
- **Pré-condição:** Conta e gestão de versões compostas; dados centralizados e estado inicial/reset autorizados.
- **Dados:** M1 e M2: duas versões sintéticas com objetivos distintos, segundo UC; preparar sem editar massa.
- **Resultado esperado:** Versões vinculadas à conta; informações reutilizadas; edição/exclusão de uma não altera as demais.
- **Critério e origem:** **Definido:** [RF], RF03/RF14; [MT], CT-RF03-01/02 e CT-RF14-01–04. **Inferido:** ordem das tarefas e preparação da segunda versão na sessão.
- **Requisito e caso de teste:** RF03/RF14; CT-RF03-01/02, CT-RF14-01–04. CT-RF03-03 e CT-RF14-05 são isolamento técnico.
- **Evidência mínima futura:** Nota da versão reconhecida, conteúdo reaproveitado e separação das alterações, usando identificadores sintéticos.
- **Classe de planejamento, não resultado:** **B**; **T** parcial. E03 não compõe lista/gestão; E02 registra criação/edição/listagem/exclusão, E01 não injeta.
- **Dependência:** J01 e dados próprios. Necessidade de múltiplas versões depende da tarefa; não exigir criar outra versão para toda exportação.
- **Alternativa/falha:** Editar/excluir só recursos sintéticos do cenário, sem atingir dados compartilhados; erro de seleção encaminha J10/J15.
- **Limite atual:** Não verifica CRUD de versões pela aplicação; versões prontas em fixture não provam criação humana.

### 10.11. J10 — Itens, seções e modelo

- **ID e ramo:** J10; Construção do currículo escolhido.
- **Objetivo para o estudante:** “Escolha as informações e a apresentação que deseja usar no currículo fictício.”
- **Ação de referência do facilitador:** Observar reaproveitamento, seleção/remoção de itens, organização das seções e escolha de modelo, sem confundir seleção visual com gravação.
- **Pré-condição:** Versão própria e catálogo de itens acessíveis; seleção, ordem e modelo persistidos e usados na prévia.
- **Dados:** M1; itens/versão identificados sinteticamente; segundo modelo disponível no catálogo efetivo.
- **Resultado esperado:** Dados centralizados disponíveis sem redigitar; seções seguem organização escolhida; modelo fica associado ao currículo preservando conteúdo.
- **Critério e origem:** **Definido:** [RF], RF03/RF05/RF06; [MT], CT-RF03-01, CT-RF05-02 e CT-RF06-02/03. **Inferido:** sequência de seleção/ordem da sessão, sem prometer ordem manual de itens.
- **Requisito e caso de teste:** RF03/RF05/RF06/RF15; CT-RF03-01–03, CT-RF05-01/02, CT-RF06-01–03. CT-RF15-01/03/04 tratam escolha do currículo para ações, não seleção dos seus itens.
- **Evidência mínima futura:** Nota dos itens/seções/modelo reconhecidos e conferência posterior da versão, sem alegar persistência por cor de card.
- **Classe de planejamento, não resultado:** **B** funcional; **E** apenas escolha visual local e **T** apoio parcial. E10 mantém seleção local; E03 só muda etapa; E02 prevê itens/ordem/versão sem E01.
- **Dependência:** Versão e dados J04–J09 conforme cenário; prévia J12 confirma efeito. Escolher modelo não pressupõe associação a vaga.
- **Alternativa/falha:** Trocar modelo preservando conteúdo; sem item não inventar obrigatório: confirmar L05. Recusas de propriedade e duplicidade são técnicas.
- **Limite atual:** Não verifica associação persistida de modelo/itens, ordem final das seções ou escolha efetiva de versão.

### 10.12. J11 — Revisar e editar

- **ID e ramo:** J11; Conferência com retorno às seções.
- **Objetivo para o estudante:** “Confira o currículo fictício e corrija o que julgar necessário antes de visualizá-lo.”
- **Ação de referência do facilitador:** Observar compreensão do resumo/pendências e escolha da seção a corrigir; não apontar a resposta nem usar defaults como dados da pessoa.
- **Pré-condição:** Versão construída; revisão recebe os dados sintéticos efetivamente salvos na conta de demonstração; edição/retorno e orientações determinísticas conectados.
- **Dados:** M1 e uma alteração sintética identificável; variantes incompletas só com obrigatoriedade confirmada.
- **Resultado esperado:** Resumo por seção; pendência aponta campo/seção; edição retorna à etapa e depois à revisão refletindo a mudança; sem dependência de IA.
- **Critério e origem:** **Definido:** [WF07], Pendências/Ações; [MJ], §6.7; [MT], CT-RF08-01–03. **Inferido:** escolher uma correção observável na sessão, L06/L09.
- **Requisito e caso de teste:** UC05, RF02/RF08; CT-RF07-03 e CT-RF08-01–03; não atribuir regra de outro recurso à revisão.
- **Evidência mínima futura:** Nota de pendência compreendida, seção escolhida, alteração reencontrada e ajuda fornecida.
- **Classe de planejamento, não resultado:** **B**; **T** parcial. E11 recebe DADOS_VALIDACAO_PADRAO e callbacks opcionais; E03 não fornece dados/callbacks. Revisão registrada em E02 sem E01.
- **Dependência:** Construção do currículo; retorno a J04–J07/J10 conforme informação; J12 só após conteúdo confirmado.
- **Alternativa/falha:** Campo pendente → retornar/corrigir/conferir; sem formação/experiência permanece condicional L05; não importar exigência de harness.
- **Limite atual:** Não verifica revisão dos dados cadastrados, volta persistida ou liberação válida para exportação.

### 10.13. J12 — Prévia e troca de modelo

- **ID e ramo:** J12; Visualização.
- **Objetivo para o estudante:** “Confira a aparência do currículo fictício e veja se outra apresentação mantém as informações.”
- **Ação de referência do facilitador:** Observar reconhecimento do conteúdo e retorno para editar; comparar modelos apenas disponíveis no alvo futuro.
- **Pré-condição:** Versão e modelo escolhidos, prévia integrada e dados selecionados identificados; navegação de retorno.
- **Dados:** M1 e versão selecionada; mesma massa na comparação.
- **Resultado esperado:** Prévia representa dados confirmados; troca de modelo mantém conteúdo; correções aparecem; opção de voltar à revisão.
- **Critério e origem:** **Definido:** [WF08], Estrutura/Ações; [MT], CT-RF07-01–03 e CT-RF06-03. **Inferido:** forma de observar clareza/legibilidade na configuração da sessão.
- **Requisito e caso de teste:** UC06, RF06/RF07; CT-RF06-03, CT-RF07-01–03; RNF02/RNF03 são limites contextuais.
- **Evidência mínima futura:** Nota de consistência entre dados/versão/modelos e dificuldades percebidas; captura só autorizada e sanitizada.
- **Classe de planejamento, não resultado:** **B**; **T** parcial. E03 não monta prévia conectada; E02 registra consulta sem E01. Harness de apoio simula seleção/prévia.
- **Dependência:** J10/J11; retorno a J11 para corrigir. Não confundir componente renderizado em teste com página publicada.
- **Alternativa/falha:** Conteúdo editado → nova conferência; seções vazias conforme regra de produto. Não presumir exportação a partir de prévia isolada.
- **Limite atual:** Não verifica fidelidade cadastro→prévia, geometria real no navegador ou todas apresentações.

### 10.14. J13 — PDF, DOCX e download

- **ID e ramo:** J13; Resultado de exportação, independente de candidatura.
- **Objetivo para o estudante:** “Obtenha o currículo fictício no formato desejado e confira se ele corresponde ao que viu.”
- **Ação de referência do facilitador:** Em sessão futura com integração confirmada, observar escolha, geração, download e abertura; separar PDF e DOCX e conferir conteúdo.
- **Pré-condição:** Conta/sessão válida, currículo próprio explicitamente escolhido quando houver versões, prévia/modelo e exportadores conectados; leitores definidos.
- **Dados:** M1 e versão/modelo selecionados; aplicativos e versões registrados em branco até a sessão.
- **Resultado esperado:** PDF e DOCX gerados com conteúdo/layout correspondentes; download disponível; falha comunicada sem arquivo inválido, permitindo tentativa sem perder dados/prévia.
- **Critério e origem:** **Definido:** [RF], RF09/RF15; [MT], CT-RF09-01–05; [WF09], Estados. **Inferido:** abertura/conferência observada na sessão e escolha de aplicativos, L15; não meta de tempo.
- **Requisito e caso de teste:** UC07/UC08, RF09/RF15; CT-RF09-01–05, CT-RF15-01/03. CT-RF15-04 e RF09-04 permanecem referências técnicas de acesso.
- **Evidência mínima futura:** Nota separada por formato: arquivo realmente obtido/aberto, consistência e obstáculo; sem versionar binário.
- **Classe de planejamento, não resultado:** **B**; **T** parcial. E11/E03 não ligam callbacks de download; E02 possui routers PDF/DOCX, E01 não injeta exportadores; renderizadores reais não completam o caminho.
- **Dependência:** Versão pronta J10–J12 ou estado preparado declarado. Não depende de J14/J15 nem exige candidatura.
- **Alternativa/falha:** Falha de geração e nova tentativa só em alvo controlado preparado pela engenharia; escolha ausente deve solicitar versão; não substituir por impressão/conversor/Blob fictício.
- **Limite atual:** Não verifica download no navegador, abertura por pessoa ou equivalência do digitado aos dois arquivos.

### 10.15. J14 — Vagas: resultado, vazio e erro

- **ID e ramo:** J14; Oportunidades, sem ordem obrigatória com exportação.
- **Objetivo para o estudante:** “Procure oportunidades pertinentes ao cenário fictício e interprete o retorno.”
- **Ação de referência do facilitador:** Observar entendimento da listagem, ausência e mensagem de falha; engenharia prepara estados seguros sem solicitar falha externa à pessoa.
- **Pré-condição:** Conta, página/cliente/backend conectados e origem dos dados identificada como real/controlada; cenários de resultado/vazio/erro autorizados.
- **Dados:** Critérios e vagas sintéticos previamente preparados (M2), sem contatos ou candidatura externa.
- **Resultado esperado:** Vagas retornadas exibidas; vazio explicado; indisponibilidade/JSON inválido não exibem dados corrompidos/detalhes internos e permitem tentar novamente sem interromper uso.
- **Critério e origem:** **Definido:** [MT], CT-RF10-01–04 e CT-RF11-01/03/04; [RF], RF10/RF11. **Inferido:** perguntas neutras e preparação de cenários humanos, L06/L10.
- **Requisito e caso de teste:** RF10/RF11, RNF06 proposto; CT-RF10-01–04, CT-RF11-01/03/04. CT-RF11-02 conecta intenção manual a J15.
- **Evidência mínima futura:** Nota separada por cenário com fonte real/simulada declarada, retorno compreendido, ajuda e possibilidade de continuidade.
- **Classe de planejamento, não resultado:** **B**; **T** parcial. E12 usa cliente padrão indisponível e não é montada por E03; E02 prevê GET /vagas, E01 sem executor.
- **Dependência:** J01; vagas não exigem exportar antes. J15 só se houver vaga e versão; estado vazio não força associação.
- **Alternativa/falha:** Resultado/vazio/erro são cenários distintos; não generalizar sucesso de um aos demais nem chamar fixture de Grupo 2 ativo.
- **Limite atual:** Não verifica serviço externo ativo, integração front↔back ou preservação do currículo em falha real.

### 10.16. J15 — Selecionar currículo, associar, classificar e consultar

- **ID e ramo:** J15; Associação manual, resultado distinto do download.
- **Objetivo para o estudante:** “Registre seu interesse na oportunidade fictícia com o currículo escolhido e confira o que ficou registrado.”
- **Ação de referência do facilitador:** Observar escolha de versão/vaga e classificação manual; comparar entendimento com registro posterior; não exigir candidatura ou todas combinações técnicas.
- **Pré-condição:** Conta, versão própria e vaga de cenário; interface/HTTP/casos/persistência compostos; nova consulta/sessão de demonstração controlada.
- **Dados:** M1 e M2: duas versões para evidenciar escolha e vaga sintética; nenhuma URL externa aberta.
- **Resultado esperado:** Associação somente por ação manual, com currículo escolhido e classificação persistida; candidatura inclui interesse e não envia currículo a serviço externo; consulta posterior mantém registro.
- **Critério e origem:** **Definido:** [RF], RF12/RF15/RN01–RN07; [MT], CT-RF12-02/05/07/08 e CT-RF15-02. **Inferido:** observar compreensão de uma escolha, sem repetir matriz combinatória.
- **Requisito e caso de teste:** RF11/RF12/RF15; CT-RF11-02, CT-RF12-01–15/C01–C07 e CT-RF15-02–04 como mapa; só casos pertinentes à tarefa humana, demais técnicos.
- **Evidência mínima futura:** Nota de versão/vaga/classificações reconhecidas e consulta posterior; sem alegar envio externo ou registrar biografia.
- **Classe de planejamento, não resultado:** **B**; **T** parcial. E02/E03 não compõem associação; leitura dos testes declara ausência de router/DTO/handler. Casos/repositórios existem apenas como apoio de componentes no percurso examinado.
- **Dependência:** J01 e versão J09/J10, vaga J14 ou estado preparado declarado; não depende de gerar PDF.
- **Alternativa/falha:** Sem versão/classificação solicita escolha; candidatura implica interesse; remoção de candidatura preserva interesse. Recusas de autorização/integridade são técnicas, sem atacar conta alheia ou provocar banco indisponível.
- **Limite atual:** Não verifica associação por interface/HTTP, persistência na aplicação que sobe, vaga externa existente ou candidatura externa.

## 11. Regras de resultado e gravidade

As regras desta seção são **inferidas/propostas**, a confirmar por produto/QA em L06/L07/L13. Elas orientam preenchimento futuro e não atribuem resultado a nenhum passo agora.

| Estado de resultado futuro | Quando usar                                                                                        | Alegação permitida                                                              |
| -------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Não executado              | Ação não foi realizada, inclusive adiamento                                                        | Não há evidência da ação; registrar motivo                                      |
| Bloqueado                  | Falta pré-condição, implementação ou composição para tentativa válida                              | Impedimento identificado; sem aprovar ou reprovar automaticamente a ação        |
| Executado e aprovado       | Tentativa real, esperado rastreado observado e evidência suficiente; ajuda/configuração declaradas | Aprovação limitada ao passo, pessoa, versão e condições efetivamente observadas |
| Executado e reprovado      | Tentativa válida contradiz esperado definido ou critério inferido já confirmado                    | Achado específico com fonte/evidência, sem generalização                        |
| Inconclusivo               | Houve tentativa, mas faltam regra/oráculo/evidência ou existe conflito não resolvido               | Não afirmar conformidade; encaminhar confirmação                                |

A classe E/T/B do planejamento não preenche o estado da execução. Um cenário de falha compreensível pode cumprir seu esperado sem provar a operação de sucesso. Conclusão com ajuda deve ser declarada separadamente da condição sem ajuda; tempo/taxa não geram veredito quantitativo sem política aprovada.

**Gravidade local proposta**, independente do roteiro de responsividade:

| Gravidade | Definição para esta jornada                                      | Conduta proposta                                                                    |
| --------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Crítica   | Exposição indevida de dados/credenciais ou perda/corrupção grave | Interromper a atividade pertinente e registrar somente informação mínima sanitizada |
| Alta      | Impede resultado principal sem alternativa segura                | Registrar barreira e dependências, encaminhar ao responsável                        |
| Média     | Exige contorno ou ajuda relevante para concluir                  | Distinguir conclusão assistida e descrever impacto                                  |
| Baixa     | Problema não impeditivo de uso/compreensão/apresentação          | Registrar alcance sem minimizar ocorrência                                          |

Gravidade não é prioridade de correção. Não há política global de “zero defeitos”. Tolerância a defeitos e aceite de risco continuam a confirmar.

**Encerramento da sessão:** contabilizar cada tarefa prevista e sua evidência, ajuda, motivo de ausência/impedimento e decisão pendente. Interrupção por tempo disponível, opção da pessoa ou infraestrutura é encerramento, não aceite.

A expressão **“jornada aceita” só poderá ser usada futuramente** após execução e aprovação de todos os passos obrigatórios confirmados por produto, sem bloqueio ou inconclusivo obrigatório e com decisão expressa de signatário autorizado. Se o escopo excluir ramos, a decisão deve declarar esse recorte e não se apresentar como aceite do processo completo. Aprovar este documento não aceita o produto nem verifica o aceite oficial do card.

## 12. Registro e revisão

Usar o [modelo de registro vazio](evidencias/modelo-registro-aceitacao-jornada-completa-estudante.md), que é formulário, não laudo. Nada deve ser preenchido pela autoria deste roteiro.

Somente após autorização e execução, criar cópia textual com identificador sem nome pessoal, no padrão:

    docs/testes/evidencias/aceitacao-jornada-completa-estudante-<identificador-da-sessao>.md

Esse caminho é recomendação de saída futura; nenhuma cópia de sessão é criada nesta entrega. Preservar o modelo vazio e separar notas/resultados do planejamento. Referenciar massa, versão e composição realmente usadas; não copiar resultados de testes ou laudos antigos.

Facilitador/observador registra ações e ajuda; participante pode validar a fidelidade do relato, sem ser signatário automático de aceite. QA revisa rastreabilidade/sanitização; produto/equipe designa signatário e autoridade para decisão/risco (L13). Papéis são distintos mesmo se pessoas acumularem funções; não selecionar nomes aqui.

Evidência mínima é nota textual sanitizada do observado por tarefa. Capturas têm precedentes em [checklist][CHECK] e [dossiê][DOS], mas não são obrigação deste roteiro nem autorização para versionar binários. Não versionar imagens, vídeos, PDF/DOCX, logs, cookies, credenciais, termo assinado ou dados reais. Se evidência restrita adicional for necessária, definir primeiro finalidade, consentimento, acesso, retenção e descarte, mantendo apenas referência sanitizada.

Os documentos de [aceite/lições][LESSON] e [dossiê][DOS] são referências de separação entre demonstração e decisão; não são alterados ou preenchidos por esta entrega. Não usar responsável/data/veredito de outro documento como identificação desta sessão.

## 13. Cobertura, divergências, confirmações e limites

### 13.1. Apoio automatizado existente e fronteiras

A tabela identifica evidência de código, não execução nova. Nenhum teste foi executado nesta autoria. Não repetir no ensaio humano todas as combinações que a automação procura cobrir; observar compreensão e uso do processo. Também não alegar que presença de automação comprova experiência humana.

| Etapas      | Apoio existente e nível                                                         | O que pode sustentar / o que não sustenta                                                                                                                               |
| ----------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| J00/J01     | [App.test.tsx][TAPP] e [ciclo de perfil autorizado][TPROFILE]                   | Composição local e integração ASGI/SQLite do perfil; não main operacional, cookie/browser ou painel humano                                                              |
| J02/J03     | Sem caso dedicado equivalente na matriz; tela de recuperação isolada            | Não comprova recuperação/rascunho/retomada integrados                                                                                                                   |
| J04/J11     | [jornada de currículo em harness][TJOURNEY] e [a11y de dados pessoais][TA11Y]   | Integração cliente/revisão simulada e propriedades locais de acessibilidade; não persistência pela aplicação ou WCAG integral                                           |
| J05         | [integração de formação][TFORM]                                                 | Escritas HTTP/casos/SQLite e leitura interna; não GET/listagem HTTP nem CRUD humano completo                                                                            |
| J06         | [FormularioExperiencias.test.tsx][TEXP]                                         | Unidade de formulário/callbacks; não salvamento/ordem na aplicação                                                                                                      |
| J07/J08     | [integração complementar][TCOMP]                                                | Curso/documentos com adapters em memória; não todo CRUD complementar, arquivo real ou navegação humana                                                                  |
| J09/J10/J12 | [seleção e ordenação][TSELECT] e [harness seleção/prévia/exportação][TEXPORTUI] | Integração parcial e harness local; consultas de itens substituídas, limites de ordem explícitos e seleção/prévia simuladas; não gestão completa ou persistência por UI |
| J13         | [integração DOCX][TDOCX] e [integração PDF][TPDF]                               | Exportador/renderizadores reais com prévia/autenticação stubs; não download browser, abertura visual pelo participante ou todos os modelos/aplicativos                  |
| J14         | [busca-vagas.integracao.test.tsx][TJOBS]                                        | Página/cliente com remoto simulado, resultado/vazio/erro; não Grupo 2 ativo ou front↔back real                                                                          |
| J15         | [integração de associação][TASSOC]                                              | Casos/adapters/SQLite e classificações; não HTTP/handler, existência de vaga, navegação humana ou envio externo                                                         |

Casos da matriz são especificações, não resultados. Recuperação, rascunho e documentos não têm CT dedicado equivalente no conjunto RF01–RF15. A matriz de rastreabilidade declara RF14 incompleto e RF15 parcial. RNF01 não define metas; a observação humana não preenche por inferência essas lacunas.

### 13.2. Divergências e limites das fontes

| Divergência                                         | Tratamento explícito                                                                                                                                                                                                                                      |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Jornada guiada × sistema inteiro                    | MJ §2/WF00 excluem versões/documentos/Grupo 2 do recorte visual; RF/UC sustentam ramos do sistema. Usar trilha+ramos, confirmar obrigatoriedade L02, sem sequência inventada                                                                              |
| Revisão sem análise automática × orientações        | MJ §6.7/WF07 e RF08 usam recortes diferentes. Distinguir conferência/validação determinística de IA/scoring; linguagem/fluxo a confirmar em L14                                                                                                           |
| Manual/checklist/dossiê antigos × código            | Fotografias antigas citam ab2b8bc; App atual tem landing/wizard. Renderizadores reais existem, mas main/App não integram download. Composição atual governa executabilidade, sem corrigir os textos                                                       |
| Integração/sincronização/matching × GET /vagas      | UC/CG2 descrevem intercâmbio/matching; [ADR-004][ADR4] e factory descrevem contrato implementado de busca. Não inventar envio ao matcher; engenharia/produto reconciliam L14                                                                              |
| Sem experiência × bloqueio de harness/revisão       | CG2 §§3.6/6 explicitamente permite ausência no contrato de integração; MJ §7 condiciona avanço à regra de produto; harness bloqueia sua variante. Não copiar bloqueio ou permissão para toda jornada. Mantém L05 a confirmar                              |
| Resumos RF02/RF12                                   | MT detalha CT-RF02-05/06, resumo encerra em 04; MR lista RF12 até 09, MT detalha até 15. Usar cenários detalhados sem ampliar o que cada um prova; documentos originais intactos                                                                          |
| Laudo PDF × alcance real do ensaio                  | [Evidência PDF anterior][PDFEVID] declara aprovação; código do ensaio tem stubs e leitura automatizada. Não importar aprovação para esta sessão ou afirmar abertura visual/todos os modelos                                                               |
| RNF02 × checklist/sessão                            | AC define alvo WCAG 2.2 AA e limites da automação/checklist. Relato de uma pessoa não certifica conformidade                                                                                                                                              |
| RNF03 × roteiro F1.1                                | CR governa suporte/limites; [roteiro de responsividade][RESP] usado somente como formato documental. Não copiar critérios, gravidade, plataformas, células preenchidas ou vereditos desse roteiro                                                         |
| Fotografia da análise × reverificação desta autoria | Mesmo HEAD após fetch, sem mudança de classificação funcional. A página de recuperação foi agora lida diretamente e confirma default indisponível. L01/L12 têm autorização documental explícita nesta tarefa, sem aprovação das políticas/aceite oficiais |

**Achados preexistentes, sem correção:** frontend com clientes indisponíveis/callbacks locais e defaults de revisão, sem percurso integrado; backend com autenticação fechada e executores ausentes, associação sem HTTP e consulta de formação incompleta; preparação de persistência com duplicidades de revisão relatadas na análise; documentação/matrizes com os conflitos acima. Padrões pessoais de defaults da validação não foram certificados sintéticos e não devem virar evidência.

### 13.3. Confirmações pendentes da análise

Todos os itens abaixo ficam **a confirmar** no âmbito indicado. A autorização atual resolve a permissão para produzir os dois documentos; não é motivo para pedir autorização novamente para esta autoria.

| Lacuna | Confirmação a obter                                                                                                                 | Tipo                      | Responsável por fornecer                      |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | --------------------------------------------- |
| L01    | A confirmar descrição/aceite oficial do card e se sua conclusão inclui execução; natureza documental desta tarefa já autorizada     | Produto                   | Responsável de produto                        |
| L02    | A confirmar ramos obrigatórios/opcionais e entradas/retornos, sem ordem única                                                       | Produto/design            | Produto com design                            |
| L03    | A confirmar elegibilidade, número e responsável pelo recrutamento real                                                              | Produto/design            | Produto com design                            |
| L04    | A confirmar experiência em elaborar currículo, dispositivo habitual e inclusão assistiva necessária                                 | Produto/design            | Produto com design                            |
| L05    | A confirmar seções/quantidades, ausência de formação/experiência, avanço e retomada                                                 | Produto/design            | Produto com design e contratos de engenharia  |
| L06    | A confirmar tarefas obrigatórias, ajuda, tentativas, encerramento e eventual meta; sem meta inventada                               | Produto/design            | Produto com design/QA                         |
| L07    | A confirmar estados, gravidade local e tolerância a defeitos/risco                                                                  | Produto/engenharia        | Produto com QA                                |
| L08    | A confirmar protocolo/consentimento, acesso, retenção, descarte, retirada e responsável                                             | Produto/privacidade       | Produto e responsável por governança de dados |
| L09    | A confirmar adequação da massa e variantes; conta/reset e canal de credencial                                                       | Produto/engenharia        | Produto e engenharia                          |
| L10    | A confirmar instância integrada, URL/commit/entrypoint/dependências reais e simuladas, reset e preflight                            | Engenharia                | Responsável técnico pelo ambiente             |
| L11    | A confirmar cobertura ausente, níveis/fronteiras e evidência futura por identidade                                                  | Engenharia                | QA e engenharia                               |
| L12    | A confirmar formalização do fluxo de autoria/manutenção documental; a produção destes dois arquivos fora de skill já foi autorizada | Organização/engenharia    | Responsável de processo/QA                    |
| L13    | A confirmar signatário, autoridade sobre risco e relação entre aprovação do documento e aceite do produto                           | Produto                   | Produto/equipe                                |
| L14    | A confirmar reconciliação de revisão, integração e suporte diante de fontes divergentes                                             | Produto/design/engenharia | Responsável de cada domínio                   |
| L15    | A confirmar leitores PDF/DOCX, configurações da sessão e alcance RNF; nenhum limiar presume-se aprovado                             | Produto/design/engenharia | Produto/design com QA                         |

A falta dessas definições não impediu escrever o roteiro condicional. Protocolo de participação, recrutamento, alvo integrado e autoridade de decisão são pré-condições de atividades futuras; não são resultados preenchidos.

### 13.4. Alegações proibidas

- Declarar jornada aceita sem execução e decisão expressa.
- Generalizar de uma pessoa para estudantes ou toda a instituição.
- Afirmar RNF01 atendido sem política confirmada.
- Afirmar E2E real a partir de jsdom/harness.
- Dizer que callback ou Blob prova download.
- Declarar WCAG AA com base em checklist/sessão isolada.
- Dizer que um navegador comprova toda a matriz.
- Afirmar candidatura enviada por registrar classificação.
- Afirmar Grupo 2 ativo por fixture.
- Copiar aprovação de laudo antigo.

### 13.5. Limite desta entrega documental

Somente este roteiro e seu modelo vazio. Sem sessão, resultados, testes, build, instalação, mudanças de ambiente/produto ou commit. Não altera matrizes, dossiê, lições, manuais, checklist, roteiro de responsividade ou a análise.

Gates de autoria: status/diff restritos aos destinos e análise preexistente; leitura integral dos dois novos documentos (diff não cobre untracked); Prettier pelo Nix dirigido aos dois caminhos; revisão manual e rg de dados/segredos; modelo vazio; existência dos links/caminhos. Gitleaks git verifica histórico, não o conteúdo untracked. A execução desses gates não é sessão de aceitação e seu resultado é relatado separadamente pelo autor.

### 13.6. Referências

As fontes abaixo são do planejamento, não campos de resultado.

[AN]: ../../prompts/requisitos/20261031-212054-roteiro-aceitacao-jornada-completa-estudante-v001.md
[RF]: ../requisitos_funcionais.md
[RNF]: ../requisitos_nao_funcionais.md
[MJ]: ../mapeamento_jornadas.md
[UC]: ../casos-de-uso-v2.md
[MT]: ../matriz_testes.md
[MR]: ../matriz_rastreabilidade.md
[WF00]: ../wireframes/README.md
[WF01]: ../wireframes/01-acesso.md
[WF02]: ../wireframes/02-painel-inicial.md
[WF03]: ../wireframes/03-dados-pessoais.md
[WF04]: ../wireframes/04-formacao.md
[WF05]: ../wireframes/05-experiencias.md
[WF06]: ../wireframes/06-informacoes-complementares.md
[WF07]: ../wireframes/07-revisao.md
[WF08]: ../wireframes/08-visualizacao-curriculo.md
[WF09]: ../wireframes/09-exportacao.md
[SEG]: ../requisitos-seguranca.md
[MAN]: ../manual-estudante.md
[CG2]: ../contrato-campos-obrigatorios-grupo2.md
[ENV]: ../configuracao-ambiente.md
[MASSA]: ../massa_teste_curriculos.json
[AC]: ../acessibilidade.md
[CR]: ../compatibilidade-responsividade.md
[CHECK]: ../checklist-demonstracao.md
[DOS]: ../dossie-aceite.md
[LESSON]: ../registro-aceite-licoes.md
[RESP]: roteiro-teste-responsividade-f1-1.md
[ADR4]: ../Arquitetura/ADR-004-integracao-grupo2-busca-vagas.md
[PDFEVID]: evidencias/f11-12-validacao-pdf-legibilidade.md
[MAIN]: ../../src/backend/main.py
[FACTORY]: ../../src/backend/api/factory.py
[AUTH]: ../../src/backend/infrastructure/security/autenticador_sessao_indisponivel.py
[APP]: ../../src/frontend/app/App.tsx
[PACCESS]: ../../src/frontend/pages/acesso-estudante/ui/PaginaAcessoEstudante.tsx
[CACCESS]: ../../src/frontend/features/acesso-estudante/api/cliente-acesso-estudante.ts
[PREC]: ../../src/frontend/pages/recuperar-senha/ui/PaginaRecuperacaoSenha.tsx
[CREC]: ../../src/frontend/features/recuperar-senha/api/cliente-recuperacao-senha.ts
[PDATA]: ../../src/frontend/pages/personal-data/ui/PaginaDadosPessoais.tsx
[CDATA]: ../../src/frontend/features/edit-personal-data/api/cliente-dados-pessoais.ts
[PFORM]: ../../src/frontend/pages/formacao-academica/ui/PaginaFormacaoAcademica.tsx
[CFORM]: ../../src/frontend/features/cadastrar-formacao-academica/api/cliente-formacao-academica.ts
[PEXP]: ../../src/frontend/pages/experiencias-profissionais/ui/PaginaExperienciasProfissionais.tsx
[FEXP]: ../../src/frontend/features/edit-professional-experience/ui/FormularioExperiencias.tsx
[PCOURSE]: ../../src/frontend/pages/cursos-idiomas/ui/PaginaCursosIdiomas.tsx
[PSKILL]: ../../src/frontend/pages/competencias/ui/PaginaCompetencias.tsx
[PPROJECT]: ../../src/frontend/pages/projetos-academicos/ui/PaginaCadastroProjetosAcademicos.tsx
[CPROJECT]: ../../src/frontend/features/cadastro-projeto-academico/api/cliente-projetos-academicos.ts
[PMODEL]: ../../src/frontend/pages/selecionar-modelo-curriculo/ui/PaginaSelecaoModeloCurriculo.tsx
[PREVIEW]: ../../src/frontend/pages/validacao-curriculo/ui/PaginaValidacaoCurriculo.tsx
[PJOBS]: ../../src/frontend/pages/vagas/ui/PaginaVagasGrupo2.tsx
[CJOBS]: ../../src/frontend/features/listar-vagas/api/cliente-vagas-grupo2.ts
[RACCESS]: ../../src/backend/api/cadastro_acesso.py
[RPROFILE]: ../../src/backend/api/perfil_estudante.py
[RCONTACT]: ../../src/backend/api/dados_contato.py
[RFORM]: ../../src/backend/api/formacao_academica.py
[REXP]: ../../src/backend/api/experiencia_profissional.py
[RDOC]: ../../src/backend/api/documento.py
[RVERSION]: ../../src/backend/api/versao_curriculo.py
[RITEM]: ../../src/backend/api/itens_versao_curriculo.py
[RLIST]: ../../src/backend/api/listagem_versoes_curriculo.py
[RDELETE]: ../../src/backend/api/exclusao_versao_curriculo.py
[RREVIEW]: ../../src/backend/api/revisao_versao_curriculo.py
[RPREVIEW]: ../../src/backend/api/previa_versao_curriculo.py
[REXPORT]: ../../src/backend/api/exportacao_curriculo.py
[RJOBS]: ../../src/backend/api/vagas.py
[TAPP]: ../../src/frontend/app/App.test.tsx
[TPROFILE]: ../../src/backend/tests/test_integracao_ciclo_vida_perfil_autorizado.py
[TJOURNEY]: ../../src/frontend/app/jornada-curriculo.e2e.test.tsx
[TA11Y]: ../../src/frontend/features/edit-personal-data/ui/FormularioDadosPessoais.a11y.test.tsx
[TFORM]: ../../src/backend/tests/test_integracao_crud_formacao_academica.py
[TEXP]: ../../src/frontend/features/edit-professional-experience/ui/FormularioExperiencias.test.tsx
[TCOMP]: ../../src/backend/tests/test_integracao_crud_informacoes_complementares.py
[TSELECT]: ../../src/backend/tests/test_integracao_selecao_ordenacao_curriculo.py
[TEXPORTUI]: ../../src/frontend/app/jornada-selecao-previa-exportacao.e2e.test.tsx
[TDOCX]: ../../src/backend/tests/test_integracao_exportacao_docx.py
[TPDF]: ../../src/backend/tests/test_integracao_validacao_pdf_legibilidade.py
[TJOBS]: ../../src/frontend/app/busca-vagas.integracao.test.tsx
[TASSOC]: ../../src/backend/tests/test_integracao_associacao_candidatura_interesse.py
