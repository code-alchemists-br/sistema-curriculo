# Mapeamento das Jornadas do Usuário --- Sistema Currículo

## 1. Objetivo

Mapear as principais jornadas do usuário no Sistema Currículo, tendo
como foco o **Aluno** e como fluxo central o envio de um currículo
existente, sua análise, a apresentação de melhorias e a posterior
revisão e exportação do currículo.

O objetivo deste documento é servir como base para a criação dos
wireframes e, posteriormente, para a definição da identidade visual, dos
componentes e da implementação do front-end.

------------------------------------------------------------------------

## 2. Contexto do produto

O Sistema Currículo tem como protagonista o **Aluno**, que utiliza a
plataforma para criar, gerenciar, revisar e exportar seu currículo.

A experiência principal deve evitar que o aluno precise montar todo o
currículo manualmente. O fluxo prioritário é:

> **Enviar currículo → Processar → Analisar → Receber melhorias →
> Revisar → Visualizar → Gerar → Exportar**

As funcionalidades de cadastro, formação, experiência, documentos e
versões continuam fazendo parte do sistema, mas devem apoiar esse fluxo
principal.

------------------------------------------------------------------------

## 3. Atores

### 3.1 Aluno

É o principal usuário do sistema.

Responsável por:

-   Cadastrar uma conta;
-   Fazer login ou recuperar a senha;
-   Enviar e revisar seu currículo;
-   Cadastrar ou corrigir informações curriculares;
-   Armazenar documentos complementares;
-   Gerenciar versões do currículo;
-   Visualizar o currículo;
-   Gerar e exportar o currículo.

### 3.2 Sistema Externo --- Grupo 2

Sistema parceiro que poderá se integrar ao Sistema Currículo por meio de
API para consumir ou enviar dados relacionados aos candidatos.

A integração deve permanecer como uma funcionalidade complementar ao
fluxo principal do aluno.

### 3.3 Recrutador / Gestor

O documento de casos de uso prevê esse ator para busca, filtragem e
visualização de currículos.

Entretanto, no contexto do Projeto 01, o foco principal é o Aluno.
Portanto, as funcionalidades do recrutador não fazem parte da jornada
principal apresentada neste documento, salvo exigência específica do
projeto.

------------------------------------------------------------------------

# 4. Casos de uso considerados

As jornadas foram relacionadas aos casos de uso definidos no documento
do projeto:

  Código   Caso de uso
  -------- --------------------------------
  UC01     Cadastrar usuário
  UC02     Fazer login ou Recuperar senha
  UC03     Cadastrar formação
  UC04     Cadastrar experiência
  UC05     Editar currículo
  UC06     Visualizar currículo
  UC07     Gerar PDF
  UC08     Gerar DOCX
  UC09     Consultar dados do Grupo 2

Além desses casos de uso, o documento também apresenta funcionalidades
de **armazenamento de documentos**, **gerenciamento de versões** e
**integração via API**.

------------------------------------------------------------------------

# 5. Jornada principal do usuário

A jornada principal representa a experiência desejada para o Aluno:

``` text
CADASTRO / LOGIN
       ↓
ENVIAR CURRÍCULO
       ↓
PROCESSAMENTO
       ↓
ANÁLISE DO CURRÍCULO
       ↓
MELHORIAS SUGERIDAS
       ↓
ALUNO REVISA
       ↓
APLICAR / EDITAR / IGNORAR
       ↓
CURRÍCULO MELHORADO
       ↓
VISUALIZAÇÃO FINAL
       ↓
GERAR CURRÍCULO
       ↓
EXPORTAR PDF / DOCX
```

Essa jornada deve ser considerada o principal fluxo de experiência do
produto.

------------------------------------------------------------------------

# 6. Jornada 1 --- Criação / Importação do currículo

## Objetivo

Permitir que o aluno entre no sistema e forneça um currículo existente
para que a plataforma possa processá-lo e iniciar sua análise.

## Fluxo principal

``` text
Landing Page
     ↓
Criar conta / Login
     ↓
Dashboard
     ↓
"Enviar meu currículo"
     ↓
Upload do arquivo
     ↓
Processamento
     ↓
Currículo importado
     ↓
Análise inicial
```

## Etapas

### 1. Entrada no sistema

O aluno acessa a plataforma e pode:

-   Criar uma conta;
-   Fazer login;
-   Recuperar a senha caso necessário.

**Caso de uso relacionado:** - UC01 --- Cadastrar usuário - UC02 ---
Fazer login ou Recuperar senha

### 2. Dashboard

Após o login, o aluno deve visualizar o estado atual do seu currículo e
ter uma ação principal clara:

> **Enviar meu currículo**

O dashboard deve orientar o usuário para a próxima ação sem exigir que
ele procure a funcionalidade.

### 3. Envio do currículo

O aluno seleciona ou arrasta seu currículo para a área de upload.

Formatos previstos para a experiência:

-   PDF;
-   DOCX.

### 4. Processamento

O sistema processa o arquivo enviado.

Durante essa etapa, a interface deve informar ao usuário que o currículo
está sendo analisado.

### 5. Currículo importado

Após o processamento, as informações identificadas podem ser
apresentadas para conferência e eventual correção.

A edição manual permanece disponível como suporte ao usuário.

**Casos de uso relacionados:** - UC03 --- Cadastrar formação - UC04 ---
Cadastrar experiência - UC05 --- Editar currículo

------------------------------------------------------------------------

# 7. Jornada 2 --- Revisão e melhorias

## Objetivo

Permitir que o aluno compreenda os pontos fortes e os pontos que podem
ser melhorados em seu currículo e decida quais alterações deseja
aplicar.

Essa é a **jornada central do produto**.

## Fluxo principal

``` text
Currículo enviado
       ↓
Análise
       ↓
Resultado da análise
       ↓
Pontos fortes / pontos de melhoria
       ↓
Sugestões de melhoria
       ↓
Aplicar / Editar / Ignorar
       ↓
Currículo melhorado
       ↓
Visualização final
```

## Etapas

### 1. Análise

O sistema apresenta o resultado da análise do currículo.

A interface deve permitir que o aluno compreenda rapidamente:

-   O que está bom;
-   O que pode ser melhorado;
-   Quais pontos precisam de atenção;
-   Quais melhorias foram identificadas.

### 2. Sugestões

Cada melhoria deve apresentar uma explicação clara.

A estrutura recomendada é:

``` text
ANTES
Conteúdo atual do currículo

SUGESTÃO
Melhoria recomendada

AÇÃO
[Aplicar] [Editar] [Ignorar]
```

### 3. Decisão do aluno

O usuário mantém o controle sobre as alterações.

Para cada sugestão, ele poderá:

-   Aplicar;
-   Editar;
-   Ignorar.

A IA deve atuar como apoio à revisão, e não substituir silenciosamente o
conteúdo do usuário.

### 4. Currículo melhorado

Após a aplicação das melhorias, o sistema apresenta uma nova versão do
currículo.

**Casos de uso relacionados:** - UC05 --- Editar currículo - UC06 ---
Visualizar currículo

------------------------------------------------------------------------

# 8. Jornada 3 --- Exportação

## Objetivo

Permitir que o aluno transforme o currículo revisado em um documento
final e faça o download no formato desejado.

## Fluxo

``` text
Currículo melhorado
        ↓
Visualização final
        ↓
Exportar
       ↙ ↘
     PDF DOCX
       ↓
Gerar currículo
       ↓
Download
```

## Etapas

### 1. Visualização final

O aluno visualiza o currículo antes da exportação.

Isso permite verificar se as informações e alterações estão corretas.

**Caso de uso relacionado:** - UC06 --- Visualizar currículo

### 2. Escolha do formato

O aluno escolhe o formato desejado:

-   PDF;
-   DOCX.

### 3. Geração

O sistema processa e gera o documento final.

**Caso de uso relacionado:** - UC07 --- Gerar PDF - UC08 --- Gerar DOCX

### 4. Download

Após a geração, o sistema informa que o currículo está pronto e
disponibiliza o arquivo para download.

------------------------------------------------------------------------

# 9. Jornada secundária --- Gerenciamento de versões

O sistema permite manter diferentes versões do currículo para áreas ou
objetivos diferentes.

Exemplo:

``` text
Currículo principal
       │
       ├── Desenvolvedor — Estágio
       │
       ├── Gestão / Administração
       │
       └── Dados / IA
```

## Fluxo

``` text
Meus currículos
       ↓
Criar nova versão
       ↓
Enviar ou duplicar currículo
       ↓
Editar
       ↓
Analisar
       ↓
Salvar versão
```

O gerenciamento de versões deve ser apresentado como uma funcionalidade
de apoio e não como o primeiro passo da experiência.

------------------------------------------------------------------------

# 10. Jornada secundária --- Documentos

O aluno pode armazenar documentos complementares, como certificados e
portfólio.

## Fluxo

``` text
Documentos
     ↓
Adicionar arquivo
     ↓
Selecionar documento
     ↓
Upload
     ↓
Documento armazenado
```

Essa funcionalidade deve ficar disponível no sistema sem competir
visualmente com o fluxo principal de análise do currículo.

------------------------------------------------------------------------

# 11. Jornada secundária --- Perfil e conta

## Cadastro

``` text
Criar conta
    ↓
Informar dados
    ↓
Criar acesso
    ↓
Dashboard
```

## Login

``` text
Login
  ↓
Credenciais válidas?
  ├── Sim → Dashboard
  └── Não → Mensagem de erro
```

## Recuperação de senha

``` text
Recuperar senha
      ↓
Informar e-mail
      ↓
Solicitação processada
      ↓
Orientação enviada ao e-mail
```

------------------------------------------------------------------------

# 12. Fluxos alternativos

## 12.1 Arquivo inválido

``` text
Upload
  ↓
Arquivo inválido
  ↓
Mensagem de erro
  ↓
Selecionar outro arquivo
```

A mensagem deve explicar o problema e orientar o usuário sobre como
continuar.

------------------------------------------------------------------------

## 12.2 Falha no processamento

``` text
Upload
  ↓
Processamento
  ↓
Erro
  ↓
Informar usuário
  ↓
Tentar novamente
```

O usuário não deve ficar preso em uma tela de carregamento indefinida.

------------------------------------------------------------------------

## 12.3 Usuário rejeita uma melhoria

``` text
Sugestão
   ↓
Ignorar
   ↓
Manter conteúdo original
   ↓
Próxima sugestão
```

------------------------------------------------------------------------

## 12.4 Usuário edita uma sugestão

``` text
Sugestão
   ↓
Editar
   ↓
Alterar conteúdo
   ↓
Salvar
   ↓
Atualizar currículo
```

------------------------------------------------------------------------

## 12.5 Usuário deseja alterar o currículo depois da análise

``` text
Currículo analisado
       ↓
Editar currículo
       ↓
Alteração
       ↓
Salvar
       ↓
Atualizar visualização
```

------------------------------------------------------------------------

## 12.6 Erro na geração do arquivo

``` text
Exportar
   ↓
Gerar documento
   ↓
Erro
   ↓
Informar usuário
   ↓
Tentar novamente
```

------------------------------------------------------------------------

# 13. Pontos de decisão da jornada

Os principais pontos de decisão são:

  Momento         Decisão
  --------------- -------------------------------------------
  Cadastro        Usuário já possui conta?
  Login           Credenciais são válidas?
  Upload          Arquivo é válido?
  Processamento   Currículo foi processado corretamente?
  Análise         Existem melhorias identificadas?
  Revisão         Usuário aplica, edita ou ignora?
  Edição          Usuário deseja alterar alguma informação?
  Exportação      PDF ou DOCX?
  Geração         Documento foi gerado corretamente?

------------------------------------------------------------------------

# 14. Pontos de interação com a IA

A IA deve aparecer principalmente em três momentos:

### 14.1 Análise

``` text
Currículo
   ↓
IA analisa
   ↓
Diagnóstico
```

### 14.2 Sugestões

``` text
Problema identificado
        ↓
IA apresenta sugestão
        ↓
Aluno decide
```

### 14.3 Melhoria

``` text
Aluno aprova
      ↓
Alteração aplicada
      ↓
Currículo atualizado
```

A IA deve ser apresentada de forma transparente, deixando claro ao
usuário o que foi identificado e o que está sendo sugerido.

------------------------------------------------------------------------

# 15. Mapa geral da experiência

``` text
                         SISTEMA CURRÍCULO
                                │
                                ▼
                       CADASTRO / LOGIN
                                │
                                ▼
                           DASHBOARD
                                │
                                ▼
                       ENVIAR CURRÍCULO
                                │
                                ▼
                          PROCESSAMENTO
                                │
                                ▼
                       ANÁLISE PELA IA
                                │
                 ┌──────────────┴──────────────┐
                 ▼                             ▼
            PONTOS FORTES                PONTOS DE MELHORIA
                                               │
                                               ▼
                                      SUGESTÕES DA IA
                                               │
                              ┌────────────────┼────────────────┐
                              ▼                ▼                ▼
                           APLICAR           EDITAR          IGNORAR
                              │                │                │
                              └────────────────┼────────────────┘
                                               ▼
                                      CURRÍCULO MELHORADO
                                               │
                                               ▼
                                        REVISÃO FINAL
                                               │
                                               ▼
                                      VISUALIZAÇÃO FINAL
                                               │
                                               ▼
                                         GERAR CURRÍCULO
                                               │
                                      ┌────────┴────────┐
                                      ▼                 ▼
                                     PDF               DOCX
                                      │                 │
                                      └────────┬────────┘
                                               ▼
                                            DOWNLOAD
```

------------------------------------------------------------------------

# 16. Relação entre jornadas e casos de uso

  Jornada      Etapa                                Caso de uso
  ------------ ------------------------------------ -------------
  Criação      Cadastro                             UC01
  Criação      Login                                UC02
  Criação      Importação/correção de formação      UC03
  Criação      Importação/correção de experiência   UC04
  Revisão      Edição                               UC05
  Revisão      Visualização                         UC06
  Exportação   Geração do documento                 UC07 / UC08
  Exportação   PDF                                  UC07
  Exportação   DOCX                                 UC08
  Integração   Dados externos                       UC09

------------------------------------------------------------------------

# 17. Princípios de UX derivados das jornadas

## 17.1 O envio do currículo deve ser a ação principal

O sistema deve conduzir o aluno rapidamente para:

> **Enviar meu currículo**

Não deve obrigá-lo a preencher dezenas de campos antes de experimentar o
principal benefício da plataforma.

## 17.2 A IA deve explicar suas sugestões

O usuário deve compreender:

-   O que foi identificado;
-   Por que pode ser melhorado;
-   Qual alteração está sendo sugerida;
-   Qual alteração foi aplicada.

## 17.3 O aluno mantém o controle

Nenhuma alteração importante deve acontecer de forma silenciosa.

As ações principais devem ser:

> **Aplicar → Editar → Ignorar**

## 17.4 O fluxo deve ser progressivo

A interface deve mostrar somente as informações necessárias para a etapa
atual.

## 17.5 O resultado deve ser visível

Depois da análise, o usuário deve conseguir perceber claramente a
diferença entre:

**Currículo original → Currículo melhorado**

## 17.6 Exportação deve ser simples

Depois de revisar o currículo, o caminho até o download deve ser curto:

> Visualizar → Exportar → PDF/DOCX → Download

------------------------------------------------------------------------

# 18. Entregável desta atividade

Ao finalizar esta atividade, devem estar disponíveis:

1.  **Mapa da jornada principal do aluno**;
2.  **Jornada de criação/importação**;
3.  **Jornada de revisão e melhorias**;
4.  **Jornada de exportação**;
5.  **Jornada de gerenciamento de versões**;
6.  **Jornada de documentos**;
7.  **Fluxos alternativos e tratamento de erros**;
8.  **Pontos de decisão**;
9.  **Pontos de interação com a IA**;
10. **Relação entre jornadas e casos de uso**.

------------------------------------------------------------------------

# 19. Critério de aceite

A atividade será considerada concluída quando as jornadas permitirem
compreender, sem necessidade de consultar o código:

> **Como um aluno entra no sistema, envia um currículo existente, recebe
> uma análise, avalia e aplica melhorias, visualiza a versão final e
> exporta o currículo em PDF ou DOCX.**

As jornadas secundárias de conta, documentos e versões também devem
estar identificadas e relacionadas aos respectivos casos de uso.

------------------------------------------------------------------------

# 20. Próxima atividade

Com as jornadas definidas, o próximo passo é:

> **Criar os wireframes das páginas principais com base nesses fluxos.**

A prioridade dos wireframes deve seguir o fluxo principal:

``` text
Login
  ↓
Dashboard
  ↓
Enviar currículo
  ↓
Processamento
  ↓
Análise
  ↓
Melhorias
  ↓
Comparação / revisão
  ↓
Currículo final
  ↓
Exportação
```

Esse fluxo deve orientar a estrutura das telas antes da definição da
identidade visual e dos componentes definitivos.
