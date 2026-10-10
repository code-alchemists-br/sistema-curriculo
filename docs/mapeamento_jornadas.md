# Mapeamento da jornada do aluno — Sistema Currículo

## 1. Objetivo

Mapear a única jornada principal do aluno no Sistema Currículo: informar seus
dados de forma guiada por wireframes, revisar o resultado e gerar seu currículo
para exportação.

Este documento usa [Casos de uso v2](casos-de-uso-v2.md) como referência. Ele
orienta a criação dos wireframes e, posteriormente, das telas e componentes.

## 2. Decisão de escopo

O currículo é construído exclusivamente a partir das informações preenchidas
pelo aluno. A experiência é um único fluxo progressivo; cada tela coleta,
confirma ou apresenta uma parte desse conteúdo.

Não fazem parte desta jornada:

- upload, importação ou processamento de currículo existente;
- análise automática, IA, diagnóstico, pontuação ou sugestões de melhoria;
- comparação entre currículo original e currículo melhorado;
- fluxos paralelos de criação e revisão.

Armazenamento de documentos, gerenciamento de versões, integração com o Grupo
2 e recursos de recrutador permanecem como capacidades descritas nos casos de
uso, mas não entram no recorte dos wireframes desta jornada.

## 3. Atores

### Aluno

É o ator principal. Cria ou acessa a conta, informa seus dados curriculares,
revisa o currículo montado pelo sistema e escolhe o formato de exportação.

### Sistema Currículo

Guia o preenchimento, valida os dados obrigatórios, mantém o rascunho e
estrutura visualmente o currículo com os dados confirmados pelo aluno.

## 4. Casos de uso relacionados

| Código | Caso de uso | Papel na jornada |
|---|---|---|
| UC01 | Cadastrar usuário | Permite criar o acesso antes do preenchimento. |
| UC02 | Fazer login ou recuperar senha | Permite acessar ou recuperar o acesso à jornada. |
| UC03 | Cadastrar formação acadêmica | Coleta as formações do aluno. |
| UC04 | Cadastrar experiência profissional | Coleta as experiências do aluno. |
| UC05 | Editar currículo | Permite revisar e alterar dados e organização. |
| UC06 | Visualizar currículo | Apresenta a prévia antes da exportação. |
| UC07 | Gerar PDF | Gera o currículo no formato PDF. |
| UC08 | Gerar DOCX | Gera o currículo no formato DOCX. |

UC09, a integração com o Grupo 2, não integra a jornada guiada do aluno.

## 5. Jornada única: preencher, revisar e gerar o currículo

A jornada começa após o cadastro ou login do aluno. No painel inicial, o sistema apresenta as ações disponíveis conforme o estado do currículo: iniciar um novo preenchimento, continuar um rascunho ou acessar um currículo já concluído para visualização e edição.

Quando o aluno inicia ou continua o preenchimento, o sistema conduz o processo por etapas: dados pessoais e contato, formação acadêmica, experiências profissionais e informações complementares.

Ao concluir o preenchimento, o aluno acessa a revisão, na qual pode conferir os dados de cada seção e selecionar aquela que deseja alterar. Após as correções, pode retornar à revisão e abrir a prévia do currículo.

Na prévia, o aluno confere a apresentação final e pode voltar à edição antes de escolher o formato de exportação. Ao selecionar PDF ou DOCX, o sistema gera o arquivo e disponibiliza o download.

```text
CADASTRO / LOGIN
        ↓
PAINEL INICIAL
        ↓
INICIAR CURRÍCULO
        ↓
DADOS PESSOAIS E CONTATO
        ↓
FORMAÇÃO ACADÊMICA
        ↓
EXPERIÊNCIAS PROFISSIONAIS
        ↓
INFORMAÇÕES COMPLEMENTARES
        ↓
REVISAR E EDITAR
        ↓
VISUALIZAR CURRÍCULO
        ↓
GERAR PDF OU DOCX
        ↓
DOWNLOAD
```

O aluno pode retornar a uma etapa anterior para corrigir ou completar dados.
Essa volta permanece dentro da mesma jornada: não cria um segundo fluxo nem
depende de análise externa.

## 6. Etapas e wireframes necessários

### 6.1 Acesso à conta

O aluno cria a conta, faz login ou recupera a senha. Após autenticação, o
sistema apresenta o painel inicial.

**Wireframes:** cadastro, login e recuperação de senha.

**Casos de uso:** UC01 e UC02.

### 6.2 Painel inicial

O painel mostra o estado do currículo do aluno e uma ação principal clara:

> **Criar meu currículo**

Se houver rascunho, a ação passa a ser **Continuar preenchimento**. Caso o
currículo já tenha sido concluído, o painel também pode oferecer
**Visualizar currículo** e **Exportar**, sem desviar da mesma jornada.

**Wireframe:** painel inicial com estado vazio, em preenchimento e concluído.

### 6.3 Dados pessoais e contato

O aluno informa os dados que serão exibidos no cabeçalho do currículo, como
nome, e-mail, telefone, cidade e meios profissionais de contato aplicáveis.

O wireframe deve indicar campos obrigatórios, validar o preenchimento antes de
avançar e permitir salvar o progresso.

**Wireframe:** formulário de dados pessoais, ação `Salvar e continuar` e ação
secundária `Salvar rascunho`.

### 6.4 Formação acadêmica

O aluno inclui uma ou mais formações. Cada item deve permitir informar, no
mínimo, curso, instituição, período e situação de conclusão quando aplicável.

O usuário pode adicionar, editar ou remover itens antes de prosseguir. A tela
não interpreta nem recomenda conteúdo; ela apenas torna o cadastro claro.

**Wireframe:** lista de formações cadastradas e formulário para adicionar ou
editar uma formação.

**Caso de uso:** UC03.

### 6.5 Experiências profissionais

O aluno inclui uma ou mais experiências, com organização, cargo, período e
descrição das atividades. A interface permite adicionar, editar, remover e
ordenar os itens conforme a necessidade do currículo.

**Wireframe:** lista de experiências cadastradas e formulário para adicionar
ou editar uma experiência.

**Caso de uso:** UC04.

### 6.6 Informações complementares

O aluno preenche informações que complementam seu perfil, como habilidades,
idiomas, cursos, projetos ou links profissionais, conforme os campos definidos
pelo produto.

Esta etapa organiza os dados fornecidos pelo próprio aluno. Ela não recebe um
arquivo de currículo nem oferece conteúdo produzido por IA.

**Wireframe:** grupos de campos complementares com inclusão, edição e remoção
de itens quando necessário.

### 6.7 Revisar e editar

O sistema apresenta um resumo organizado das informações preenchidas pelo aluno, separado por seção. A revisão permite conferir dados pessoais, formação acadêmica, experiências profissionais e informações complementares antes da visualização final.

Para cada seção, a interface deve indicar seu conteúdo e disponibilizar uma ação para edição. Ao selecionar essa ação, o aluno retorna à etapa correspondente, altera os dados necessários e pode voltar à revisão para conferir as mudanças.

A interface também deve indicar eventuais pendências obrigatórias, quando aplicável, e orientar o aluno sobre como resolvê-las antes de avançar.

A revisão é uma conferência dos dados informados pelo próprio aluno. Não envolve análise automática, pontuação, comparação com currículos importados ou sugestões geradas por IA.

**Wireframe:** resumo por seção, indicador de pendências obrigatórias e ações
`Editar`, `Voltar` e `Visualizar currículo`.

**Caso de uso:** UC05  — Editar currículo.

### 6.8 Visualizar currículo

O sistema estrutura os dados confirmados em um currículo visual. O aluno pode
ver o resultado antes de gerar o arquivo e voltar à revisão para corrigir
informações.

**Wireframe:** prévia do currículo e ações `Editar dados`, `Gerar PDF` e
`Gerar DOCX`.

**Caso de uso:** UC06.

### 6.9 Gerar e exportar

O aluno escolhe PDF ou DOCX. A geração usa os dados confirmados e o layout
selecionado; quando terminada, o sistema disponibiliza o download.

Exportar sempre inclui gerar o currículo. Se a geração falhar, o aluno recebe
uma mensagem objetiva e pode tentar novamente sem perder os dados preenchidos.

**Wireframe:** escolha de formato, estado de geração, sucesso e falha.

**Casos de uso:** UC07 e UC08.

## 7. Fluxos alternativos dentro da jornada

| Situação | Resposta esperada da interface | Continuidade |
|---|---|---|
| Campo obrigatório ausente ou inválido | Explica o erro junto ao campo e preserva os dados já preenchidos. | O aluno corrige e continua na mesma etapa. |
| Aluno interrompe o preenchimento | Salva o rascunho quando essa ação for solicitada. | O painel oferece continuar de onde parou. |
| Aluno precisa corrigir informação na revisão ou prévia | Oferece ação `Editar` para a seção correspondente. | Retorna à etapa necessária e depois à revisão. |
| Não há formação ou experiência | Explica que a seção pode ser opcional quando a regra de produto permitir. | O aluno avança sem criar item fictício. |
| Falha ao gerar PDF ou DOCX | Informa a falha e disponibiliza nova tentativa. | Mantém a prévia e os dados confirmados. |

## 8. Pontos de decisão

| Momento | Decisão do aluno | Resultado |
|---|---|---|
| Acesso | Criar conta, entrar ou recuperar senha | Acessa o painel inicial. |
| Painel | Iniciar um currículo ou continuar um rascunho | Entra na próxima etapa pendente. |
| Preenchimento | Adicionar, editar ou remover informações | Mantém os dados sob controle do aluno. |
| Revisão | Corrigir ou confirmar os dados | Libera a visualização. |
| Visualização | Editar ou gerar | Retorna à revisão ou inicia a exportação. |
| Exportação | PDF ou DOCX | Gera o arquivo escolhido para download. |

## 9. Princípios de UX

1. **Uma única trilha clara.** O próximo passo deve ser visível em cada tela,
   com indicador de progresso e possibilidade de voltar sem perder dados.
2. **Dados sob controle do aluno.** O conteúdo do currículo provém do que ele
   preenche, confirma, edita ou remove.
3. **Progressão por etapas.** Cada wireframe solicita somente as informações
   necessárias para a seção atual.
4. **Validação compreensível.** Erros aparecem no contexto do campo e indicam
   como prosseguir.
5. **Prévia antes da exportação.** O aluno vê o currículo estruturado antes de
   gerar PDF ou DOCX.
6. **Sem IA e sem upload.** A interface não promete análise, recomendação,
   processamento de arquivo ou transformação automática de conteúdo.

## 10. Mapa geral da experiência

```text
                         SISTEMA CURRÍCULO
                                │
                                ▼
                       CADASTRO / LOGIN
                                │
                                ▼
                         PAINEL INICIAL
                                │
                                ▼
                        CRIAR CURRÍCULO
                                │
                                ▼
                 PREENCHIMENTO GUIADO POR ETAPAS
       ┌────────────────┬──────────────────┬──────────────────┐
       ▼                ▼                  ▼                  ▼
 DADOS PESSOAIS     FORMAÇÃO          EXPERIÊNCIAS      COMPLEMENTARES
       └────────────────┴──────────────────┴──────────────────┘
                                │
                                ▼
                         REVISAR / EDITAR
                                │
                                ▼
                       VISUALIZAR CURRÍCULO
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
                GERAR PDF               GERAR DOCX
                    └───────────┬───────────┘
                                ▼
                             DOWNLOAD
```

## 11. Critério de aceite

O mapeamento estará atendido quando permitir compreender, sem consultar o
código, como um aluno cria ou acessa a conta, preenche progressivamente os
dados do currículo, revisa o resultado, visualiza a prévia e exporta o
documento em PDF ou DOCX.

Nenhuma etapa da jornada deve exigir upload de currículo, análise por IA ou
sugestões automatizadas de conteúdo.

## 12. Próxima atividade

Criar os wireframes na ordem da jornada única:

```text
Login / cadastro
  ↓
Painel inicial
  ↓
Dados pessoais
  ↓
Formação
  ↓
Experiências
  ↓
Informações complementares
  ↓
Revisão
  ↓
Prévia do currículo
  ↓
Exportação e download
```
