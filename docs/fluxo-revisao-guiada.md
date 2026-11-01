# Fluxo de Revisão Guiada de Currículos

**Projeto:** Sistema Currículo — FATEC-SP  
**Issue:** #430 — F12.11  
**Data:** 01/11/2026  
**Status:** Documentação dos contratos e regras implementados na branch `dev`

## 1. Objetivo

Este documento apresenta as regras, os resultados e as decisões do fluxo de revisão guiada de currículos do Sistema Currículo.

A funcionalidade permite analisar uma versão do currículo do estudante, identificar informações ausentes ou inconsistentes e retornar orientações para melhorar seu preenchimento.

A revisão diferencia problemas obrigatórios de recomendações opcionais. Também permite registrar quando o estudante aceita ou rejeita uma recomendação apresentada.

O objetivo é orientar a revisão do currículo sem alterar automaticamente as informações cadastradas.

## 2. Visão geral do fluxo

A revisão é realizada sobre uma versão específica do currículo e considera os dados vinculados a ela.

O fluxo segue as etapas:

1. O estudante solicita a revisão de uma versão do currículo.
2. O sistema verifica se a versão existe e pertence ao estudante.
3. O caso de uso obtém a prévia da versão.
4. As regras do domínio verificam informações obrigatórias e consistência das datas.
5. O sistema organiza as pendências encontradas.
6. O resultado informa se a revisão foi aprovada e apresenta os erros e avisos.
7. O estudante pode corrigir os dados ou registrar uma decisão sobre as recomendações opcionais.
8. As decisões registradas podem ser consultadas posteriormente.

A revisão utiliza as informações da versão e não modifica os dados originais do perfil durante sua execução.

## 3. Classificação das pendências

O sistema trabalha com duas severidades:

| Severidade | Identificador | Comportamento |
|---|---|---|
| Erro | `erro` | Impede que a revisão seja considerada aprovada |
| Aviso | `aviso` | Apresenta uma recomendação, sem reprovar a revisão |

### 3.1. Erros

Os erros representam informações obrigatórias ausentes ou inconsistências que precisam ser corrigidas.

Quando a revisão identifica pelo menos um erro, o resultado apresenta:

`aprovado: false`

O estudante deve corrigir o problema correspondente e solicitar uma nova revisão.

### 3.2. Avisos

Os avisos representam sugestões de melhoria.

A presença exclusiva de avisos não impede a aprovação da revisão.

Nesse caso, o resultado pode apresentar:

`aprovado: true`

O estudante pode registrar uma decisão de aceitar ou rejeitar a recomendação, desde que ela faça parte dos avisos da revisão atual.

## 4. Regras de identificação e contato

A revisão verifica a existência das informações de contato do estudante.

| Situação | Código | Severidade |
|---|---|---|
| Dados de contato ausentes | `CONTATO_AUSENTE` | Erro |
| Cidade não informada | `CIDADE_AUSENTE` | Aviso |
| LinkedIn e currículo Lattes não informados | `LINK_PROFISSIONAL_AUSENTE` | Aviso |

Quando os dados de contato estão ausentes, a revisão solicita endereço e pelo menos um telefone.

Quando a cidade não está informada, o sistema recomenda seu preenchimento.

Caso não exista LinkedIn nem currículo Lattes, a revisão recomenda informar pelo menos uma dessas referências profissionais.

Nome e e-mail não são novamente verificados como campos vazios nessa regra, pois suas entidades de domínio já possuem validações próprias.

## 5. Regras de completude das seções

O sistema verifica a presença dos itens necessários na versão do currículo.

| Seção | Código | Severidade |
|---|---|---|
| Formação acadêmica | `FORMACAO_AUSENTE` | Erro |
| Experiências profissionais | `EXPERIENCIA_AUSENTE` | Erro |
| Competências | `COMPETENCIA_AUSENTE` | Erro |
| Projetos acadêmicos | `PROJETO_AUSENTE` | Aviso |
| Idiomas | `IDIOMA_AUSENTE` | Aviso |

### 5.1. Formação acadêmica

A versão deve possuir pelo menos uma formação acadêmica para atender à regra atual de completude.

A ausência de formação gera uma pendência de erro.

### 5.2. Experiência profissional

A regra atual exige pelo menos uma experiência profissional na versão.

Quando nenhuma experiência é encontrada, a revisão gera um erro.

Essa exigência representa o comportamento implementado atualmente. Uma eventual flexibilização para estudantes sem experiência profissional deverá ser tratada como alteração de regra de negócio, e não apenas como mudança documental.

### 5.3. Competências

A revisão exige pelo menos uma competência selecionada.

A ausência de competências gera uma pendência de erro.

### 5.4. Projetos acadêmicos

A ausência de projetos acadêmicos gera apenas um aviso.

O sistema recomenda incluir projetos, mas não reprova a revisão somente por essa ausência.

### 5.5. Idiomas

A ausência de idiomas também gera apenas um aviso.

O estudante recebe uma recomendação para complementar o currículo, sem que isso impeça a aprovação.

## 6. Regras de consistência das datas

Além dos campos obrigatórios, o sistema verifica inconsistências temporais em formações acadêmicas e experiências profissionais.

A verificação utiliza a data atual fornecida por um relógio da aplicação e considera tolerância de um dia.

| Situação | Código | Severidade |
|---|---|---|
| Formação concluída com data final no futuro | `FORMACAO_CONCLUIDA_COM_FIM_FUTURO` | Erro |
| Formação em andamento com data final já ultrapassada | `FORMACAO_EM_ANDAMENTO_COM_FIM_PASSADO` | Aviso |
| Experiência profissional com início no futuro | `EXPERIENCIA_INICIO_FUTURO` | Erro |

A tolerância de um dia evita que pequenas diferenças de data relacionadas ao fuso horário produzam pendências indevidas.

A validação da ordem entre início e fim de um período já é responsabilidade do modelo de período utilizado pelo domínio.

As regras de revisão não precisam repetir essa validação.

## 7. Organização dos resultados

Cada pendência possui quatro informações:

| Campo | Descrição |
|---|---|
| `codigo` | Identificador estável da pendência |
| `secao` | Seção do currículo relacionada |
| `mensagem` | Orientação apresentada ao estudante |
| `severidade` | Classificação como erro ou aviso |

As pendências são organizadas de maneira determinística.

A ordenação segue:

1. Erros antes dos avisos.
2. Ordem das seções definida pelo domínio da revisão.
3. Código da pendência para desempate.

Essa organização permite apresentar primeiro os problemas que precisam ser corrigidos.

## 8. Resultado da revisão

O resultado utiliza o contrato `ResultadoRevisao`, que contém as pendências encontradas.

O campo `aprovado` é calculado a partir das severidades.

A revisão é considerada aprovada quando não existe nenhuma pendência com severidade `erro`.

Portanto:

- nenhuma pendência: aprovado;
- somente avisos: aprovado;
- pelo menos um erro: não aprovado.

O resultado não depende de uma aprovação manual registrada separadamente.

## 9. Consulta da revisão pela API

A rota atual é:

`GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/revisao`

A operação retorna:

`200 OK`

com o resultado da revisão.

### Exemplo ilustrativo de resposta

```json
{
  "aprovado": false,
  "pendencias": [
    {
      "codigo": "COMPETENCIA_AUSENTE",
      "secao": "competencias",
      "mensagem": "Inclua ao menos uma competência na versão.",
      "severidade": "erro"
    },
    {
      "codigo": "IDIOMA_AUSENTE",
      "secao": "idiomas",
      "mensagem": "Considere incluir um idioma na versão.",
      "severidade": "aviso"
    }
  ]
}
```

O exemplo apresenta apenas parte das pendências possíveis. O resultado real depende das informações existentes na versão analisada.

### Principais respostas HTTP

| Status | Situação |
|---|---|
| `200` | Revisão executada e resultado devolvido |
| `401` | Sessão ausente ou inválida |
| `403` | Identidade da rota não autorizada pelo mecanismo de autenticação |
| `404` | Versão inexistente ou pertencente a outro estudante |
| `422` | Identificadores ou parâmetros inválidos |
| `503` | Executor de revisão não configurado |

A proteção de autenticação é realizada pelo mecanismo comum da aplicação.

## 10. Decisões do estudante sobre recomendações

O fluxo permite registrar decisões sobre as pendências classificadas como avisos.

Existem duas decisões possíveis:

| Identificador | Significado |
|---|---|
| `aceita` | O estudante aceita a recomendação |
| `rejeitada` | O estudante rejeita a recomendação |

A decisão registrada representa a escolha do estudante sobre aquela recomendação.

Ela não realiza automaticamente a alteração sugerida nos dados do currículo.

### 10.1. Recomendações que podem receber decisão

Uma recomendação só pode receber decisão quando:

- está presente na revisão atual;
- possui severidade `aviso`;
- pertence à versão do estudante autenticado.

O sistema não permite registrar uma decisão sobre um erro obrigatório.

Também não aceita códigos de recomendação inexistentes na revisão atual.

### 10.2. Registro da decisão

A rota utilizada é:

`PUT /estudantes/{usuario_id}/curriculos/{curriculo_id}/recomendacoes/{codigo}`

Exemplo de corpo:

```json
{
  "decisao": "aceita"
}
```

Ou:

```json
{
  "decisao": "rejeitada"
}
```

### Resposta

O registro devolve o código da recomendação, a decisão e o instante em que ela foi tomada.

Exemplo ilustrativo:

```json
{
  "codigo": "IDIOMA_AUSENTE",
  "decisao": "aceita",
  "decidida_em": "2026-10-25T14:30:00-03:00"
}
```

O instante apresentado é apenas ilustrativo. Na operação real, o horário é obtido do relógio da aplicação.

### Erros relevantes

| Status | Situação |
|---|---|
| `404` | Versão ou recomendação não encontrada, ou código que não corresponde a um aviso |
| `422` | Decisão fora dos valores permitidos |
| `503` | Serviço responsável pelo registro indisponível |

As proteções comuns de autenticação e autorização também são aplicáveis.

## 11. Atualização de uma decisão

O sistema permite alterar uma decisão já registrada.

Quando o estudante registra uma nova decisão para o mesmo código de recomendação e a mesma versão, o registro anterior é substituído.

Exemplo:

Uma recomendação foi inicialmente marcada como:

`rejeitada`

Posteriormente, o estudante pode registrar:

`aceita`

O novo registro passa a representar a decisão atual.

Essa operação deve continuar exigindo que o código corresponda a um aviso da revisão atual.

## 12. Consulta das decisões registradas

As decisões de uma versão podem ser consultadas pela rota:

`GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/recomendacoes`

A resposta contém uma lista de decisões registradas.

Exemplo ilustrativo:

```json
{
  "decisoes": [
    {
      "codigo": "IDIOMA_AUSENTE",
      "decisao": "aceita",
      "decidida_em": "2026-10-25T14:30:00-03:00"
    },
    {
      "codigo": "PROJETO_AUSENTE",
      "decisao": "rejeitada",
      "decidida_em": "2026-10-25T14:35:00-03:00"
    }
  ]
}
```

A consulta verifica se a versão existe e pertence ao estudante antes de devolver as decisões.

Os registros são devolvidos em ordem estável pelo repositório responsável.

## 13. Segurança e propriedade

O fluxo de revisão deve respeitar as regras de autenticação e propriedade dos recursos do estudante.

A aplicação deve impedir que uma pessoa consulte a revisão ou registre decisões sobre o currículo de outro usuário.

As verificações incluem:

- autenticação na entrada das rotas protegidas;
- verificação de propriedade da versão;
- reaproveitamento da prévia filtrada por proprietário;
- recusa de recomendações inexistentes;
- recusa de decisões sobre erros;
- consulta de decisões limitada à versão autorizada.

Uma versão inexistente e uma versão pertencente a outro estudante são tratadas como não encontradas pelos casos de uso correspondentes.

Essa regra evita a exposição indevida de informações.

## 14. Separação entre revisão e alteração de dados

A revisão é uma operação de consulta e avaliação.

Ela identifica problemas e recomenda melhorias, mas não modifica automaticamente o currículo.

Da mesma forma, registrar uma decisão sobre um aviso não equivale a atualizar os dados do estudante.

Para corrigir uma informação, devem ser utilizadas as funcionalidades próprias de cadastro e edição.

Depois da correção, uma nova revisão pode apresentar resultados diferentes.

## 15. Limites do fluxo atual

A documentação considera os contratos e regras identificados no backend.

Não são declarados como comportamentos automáticos:

- correção de dados pelo próprio mecanismo de revisão;
- alteração de campos ao aceitar uma recomendação;
- autorização para ignorar erros obrigatórios;
- utilização de inteligência artificial como parte da revisão descrita;
- aprovação manual do currículo por um avaliador externo;
- envio automático do currículo para empresas;
- garantia de que todas as telas já estejam integradas ao fluxo.

A presença das rotas e dos casos de uso não comprova, isoladamente, a execução completa pela interface web.

## 16. Critérios de verificação

A documentação pode ser conferida utilizando os testes existentes da aplicação.

Os principais comportamentos que devem permanecer cobertos são:

1. Revisão de currículo sem pendências.
2. Revisão contendo somente avisos.
3. Revisão contendo pelo menos um erro.
4. Verificação das informações de contato.
5. Identificação de seções obrigatórias ausentes.
6. Consistência de datas de formações e experiências.
7. Ordenação determinística das pendências.
8. Recusa de versão inexistente ou de outro estudante.
9. Registro de decisão válida sobre aviso.
10. Recusa de decisão sobre erro ou código inexistente.
11. Substituição de decisão anterior sobre a mesma recomendação.
12. Consulta das decisões registradas.

Esses são critérios para conferir a implementação e seus testes, não uma declaração de que uma nova execução completa foi realizada durante esta alteração documental.

## 17. Consequências das decisões adotadas

A separação entre erros e avisos permite que o estudante identifique quais problemas são obrigatórios e quais são apenas sugestões.

A apresentação ordenada facilita a priorização das correções.

O registro de decisões sobre recomendações permite acompanhar as escolhas do estudante sem alterar automaticamente os dados.

A utilização de códigos estáveis reduz a dependência de textos de mensagens na comunicação entre backend e interface.

A verificação de propriedade garante que revisão e decisões estejam vinculadas à versão correta.

Como limitação, mudanças futuras nas regras de completude, nos códigos de pendência ou nas decisões disponíveis exigirão atualização dos testes e desta documentação.

## 18. Referências

- `src/backend/domain/revisao_curriculo.py`
- `src/backend/domain/decisao_recomendacao.py`
- `src/backend/application/revisao_versao_curriculo.py`
- `src/backend/application/decisao_recomendacao.py`
- `src/backend/api/revisao_versao_curriculo.py`
- `src/backend/api/decisao_recomendacao.py`
- `src/backend/tests/test_api_revisao_versao_curriculo.py`
- `docs/requisitos_funcionais.md`

## 19. Rastreabilidade

- **Issue:** #430 — F12.11
- **WBS:** 1.1.2.4, 1.8.2.1–1.8.2.4
- **Funcionalidade:** revisão guiada de versões de currículo
- **Contratos documentados:** revisão, pendências, severidades e decisões sobre recomendações
- **Fontes:** regras de domínio, casos de uso e rotas HTTP presentes na `dev`

## 20. Conclusão

O fluxo de revisão guiada permite verificar a completude e a consistência de uma versão de currículo, apresentando erros e avisos de forma organizada.

A aprovação da revisão depende da ausência de erros. As recomendações classificadas como avisos podem ser aceitas ou rejeitadas pelo estudante, com registro da decisão correspondente.

O fluxo mantém separadas a análise das informações, as decisões do estudante e a alteração efetiva dos dados, respeitando as regras de propriedade do currículo.

Esta documentação consolida os contratos atualmente identificados e deve acompanhar futuras mudanças nas regras de revisão ou no funcionamento das recomendações.
