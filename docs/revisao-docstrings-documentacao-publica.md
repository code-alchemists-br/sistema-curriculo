# Revisão de Docstrings e Documentação Pública

**Projeto:** Sistema Currículo — FATEC-SP  
**Issue:** #435 — F12.15  
**Data da revisão:** 01/11/2026  
**Branch de referência:** `dev`  
**Situação:** Revisão documental realizada sobre os módulos e documentos indicados neste relatório.

## 1. Objetivo

Este documento registra a revisão das docstrings e da documentação pública dos principais módulos entregues no Sistema Currículo.

O objetivo é identificar informações desatualizadas, diferenças entre documentação e implementação e pontos que precisam de correção ou confirmação pela equipe.

A revisão considera especialmente as funcionalidades de exportação de currículos, revisão guiada, busca de vagas e integração com o Grupo 2.

As divergências são registradas com indicação do arquivo, comportamento identificado, impacto e encaminhamento recomendado.

Esta atividade não altera as regras de negócio nem substitui os testes de software.

## 2. Critérios de revisão

Foram considerados os seguintes critérios:

1. Correspondência entre a descrição da funcionalidade e o código.
2. Clareza da finalidade de classes, funções e módulos.
3. Coerência entre parâmetros documentados e parâmetros implementados.
4. Correspondência entre resultados declarados e respostas realmente definidas.
5. Descrição correta do tratamento de erros.
6. Consistência das regras de autenticação e autorização.
7. Atualização das referências utilizadas pela documentação.
8. Identificação de funcionalidades planejadas que ainda não podem ser apresentadas como implementadas.

A revisão distingue divergências confirmadas, documentação desatualizada e decisões externas ainda não incorporadas ao código.

## 3. Escopo analisado

A análise foi concentrada nos seguintes módulos:

| Área | Arquivo |
|---|---|
| Exportação | `src/backend/api/exportacao_curriculo.py` |
| Revisão guiada | `src/backend/api/revisao_versao_curriculo.py` |
| Revisão guiada | `src/backend/application/revisao_versao_curriculo.py` |
| Busca de vagas | `src/backend/api/vagas.py` |
| Integração externa | `src/backend/infrastructure/integrations/cliente_vagas_grupo2.py` |
| Interface | `src/frontend/app/App.tsx` |

Também foram considerados os documentos:

- `docs/manual-estudante.md`;
- `docs/exportacao-pdf-docx.md`;
- `docs/contrato-busca-vagas.md`.

A revisão é delimitada aos arquivos indicados. Não representa auditoria exaustiva de todas as docstrings do repositório.

## 4. Resultado geral

Os módulos analisados apresentam docstrings que identificam suas responsabilidades e descrevem o funcionamento principal de classes, funções e operações.

A separação entre camadas também aparece na documentação interna, principalmente entre API, Application e Infrastructure.

Entretanto, foram identificadas divergências relacionadas ao estado atual das funcionalidades e ao tratamento de falhas externas.

As diferenças mais relevantes estão na documentação de exportação e na descrição do comportamento do cliente HTTP do Grupo 2.

Os resultados estão detalhados a seguir.

## 5. Divergências encontradas

### DIV-01 — Documento de exportação desatualizado

**Prioridade:** Alta  
**Tipo:** Documentação pública desatualizada

**Arquivo:**

`docs/exportacao-pdf-docx.md`

**Descrição:**

O documento informa que a branch `dev` ainda não possui geradores de PDF e DOCX integrados.

Entretanto, o backend atual possui as rotas:

- `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/pdf`;
- `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/docx`.

O módulo `src/backend/api/exportacao_curriculo.py` registra os endpoints e os contratos de download.

**Impacto:**

A documentação pode levar o leitor a concluir que a exportação ainda não possui implementação no backend, mesmo existindo suporte técnico para os dois formatos.

**Encaminhamento recomendado:**

Atualizar o documento para reconhecer os geradores e as rotas existentes.

A atualização deve preservar a distinção entre a disponibilidade no backend e a integração dos controles de exportação na interface web.

**Situação:** Divergência identificada; correção documental a encaminhar.

### DIV-02 — Manual do estudante com informações antigas sobre exportação

**Prioridade:** Média  
**Tipo:** Documentação desatualizada

**Arquivo:**

`docs/manual-estudante.md`

**Descrição:**

A versão consultada do manual ainda utiliza como referência uma fotografia técnica de 19/10/2026.

Nela, a exportação PDF/DOCX é apresentada como uma funcionalidade sem gerador real integrado.

Essa informação ficou desatualizada em relação às rotas existentes no backend.

**Impacto:**

O estudante ou avaliador pode receber informações inconsistentes sobre a disponibilidade dos formatos de exportação.

**Encaminhamento recomendado:**

Acompanhar a atualização do manual realizada na issue #433, evitando criar alterações concorrentes no mesmo arquivo.

**Situação:** Identificada; atualização relacionada ao PR #624.

### DIV-03 — Tratamento de HTTP 5xx na docstring do adapter externo

**Prioridade:** Alta  
**Tipo:** Divergência entre documentação interna e tratamento de exceções

**Arquivo:**

`src/backend/infrastructure/integrations/cliente_vagas_grupo2.py`

**Descrição:**

A docstring do módulo informa que respostas HTTP 5xx do Grupo 2 são traduzidas para `RespostaInvalidaVagas`.

Entretanto, a implementação utiliza `urllib.request.urlopen` para executar a comunicação HTTP.

Uma resposta HTTP de erro pode gerar `urllib.error.HTTPError`, que é uma especialização de `urllib.error.URLError`.

O tratamento atual captura `URLError` no bloco de falhas de comunicação e pode converter a ocorrência em `TimeoutIntegracaoVagas`, mesmo quando o problema original é uma resposta HTTP de erro.

**Impacto:**

A classificação incorreta pode fazer com que falhas HTTP do serviço externo sejam tratadas como problemas de conexão ou indisponibilidade temporária.

Isso também pode alterar a resposta apresentada pela API interna, já que categorias diferentes de falha são traduzidas para status HTTP distintos.

**Encaminhamento recomendado:**

Solicitar revisão técnica do tratamento explícito de `HTTPError`.

A equipe deve definir se respostas HTTP 5xx devem ser classificadas como resposta inválida, indisponibilidade externa ou outra categoria adequada.

Após a decisão, alinhar a implementação, os testes e a docstring.

**Situação:** Divergência técnica identificada; correção depende do responsável pela integração.

### DIV-04 — Novo parâmetro `limit` ainda não aparece no contrato público da busca

**Prioridade:** Média  
**Tipo:** Documentação pendente de atualização

**Arquivo:**

`docs/contrato-busca-vagas.md`

**Descrição:**

O contrato atualmente documenta os parâmetros:

- `termo`;
- `localizacao`;
- `modalidade`.

O alinhamento posterior entre o Grupo 1 e o Grupo 2 acrescentou a decisão de utilizar o parâmetro `limit`, com intervalo de 1 a 100 e quantidade inicial padrão de 10 vagas.

Também foi informado que a integração não utilizará paginação.

Essas decisões ainda não aparecem no documento consultado.

**Impacto:**

A documentação não apresenta todo o alinhamento mais recente entre as equipes.

**Encaminhamento recomendado:**

Atualizar o contrato quando a implementação correspondente estiver definida, indicando claramente:

- parâmetros atualmente disponíveis na API interna;
- parâmetro `limit` acordado com o Grupo 2;
- valor padrão inicial de 10;
- intervalo permitido de 1 a 100;
- decisão de não utilizar paginação.

A documentação não deve afirmar que `limit` já está disponível na API interna antes da implementação.

**Situação:** Alinhamento externo registrado; atualização e implementação a acompanhar.

### DIV-05 — Diferença entre o acordo de integração e a rota `GET /vagas`

**Prioridade:** Média  
**Tipo:** Diferença entre decisão acordada e contrato implementado

**Arquivo:**

`src/backend/api/vagas.py`

**Descrição:**

A rota interna `GET /vagas` recebe atualmente os parâmetros `termo`, `localizacao` e `modalidade`.

No contrato consultado, não existe parâmetro `limit` declarado na assinatura pública da rota.

Isso representa uma diferença em relação ao novo acordo de integração com o Grupo 2, que prevê controle da quantidade de vagas.

**Impacto:**

O frontend ainda não pode utilizar essa rota, no estado analisado, para definir diretamente a quantidade de resultados através de `limit`.

**Encaminhamento recomendado:**

Encaminhar a decisão ao responsável pela implementação da busca de vagas.

Quando o parâmetro for incorporado, atualizar a documentação OpenAPI, os testes e o contrato público correspondente.

**Situação:** Diferença de implementação identificada; não corrigida por esta tarefa documental.

## 6. Módulos sem divergências relevantes identificadas no escopo consultado

### 6.1. Exportação de currículo

O módulo `src/backend/api/exportacao_curriculo.py` possui docstrings que descrevem as responsabilidades de geração e download dos arquivos.

As operações documentadas correspondem aos caminhos de PDF e DOCX declarados no código.

Também foram identificados tratamentos para versão não encontrada, falha de geração e ausência do executor.

Não foi identificada divergência relevante nas descrições principais examinadas desse módulo.

### 6.2. Revisão guiada

Os módulos:

- `src/backend/api/revisao_versao_curriculo.py`;
- `src/backend/application/revisao_versao_curriculo.py`;

apresentam uma separação coerente entre transporte HTTP e aplicação das regras de revisão.

A Application solicita a prévia da versão, utiliza a data disponibilizada pelo relógio e executa a revisão de domínio.

A API converte o resultado para um contrato público com o campo `aprovado` e a lista de `pendencias`.

Não foi identificada divergência relevante nas descrições principais examinadas.

### 6.3. Busca de vagas

O módulo `src/backend/api/vagas.py` documenta a consulta autenticada, o tratamento do resultado vazio e a tradução de falhas de integração.

Esses comportamentos estão representados na implementação.

A principal observação relacionada ao módulo é a diferença entre os parâmetros atuais e o novo `limit` acordado com o Grupo 2, já registrada como DIV-05.

## 7. Quadro de encaminhamento

| ID | Prioridade | Encaminhamento | Responsabilidade sugerida |
|---|---|---|---|
| DIV-01 | Alta | Atualizar documento de exportação | Documentação |
| DIV-02 | Média | Acompanhar PR da atualização do manual | Documentação |
| DIV-03 | Alta | Revisar classificação de `HTTPError` e docstring | Backend / integração |
| DIV-04 | Média | Atualizar contrato de busca após alinhamento técnico | Documentação e integração |
| DIV-05 | Média | Avaliar implementação do parâmetro `limit` | Backend / integração |

Os responsáveis definitivos e os prazos devem ser confirmados pelo GP ou pelos responsáveis técnicos de cada área.

Este relatório não atribui automaticamente novas tarefas aos integrantes.

## 8. Critérios para considerar divergências resolvidas

Uma divergência poderá ser marcada como resolvida quando existir evidência verificável da alteração correspondente.

Para alterações documentais, devem ser conferidos:

- conteúdo atualizado;
- coerência com a implementação;
- ausência de duplicação contraditória;
- links e referências corretos;
- revisão do PR.

Para divergências que envolvem comportamento de código, também devem ser considerados os testes pertinentes.

A abertura de um PR não é, por si só, evidência de que a divergência foi corrigida.

## 9. Limitações da revisão

Esta atividade foi realizada pela inspeção dos arquivos e contratos disponíveis no repositório.

Não foram executados novos testes automatizados, testes de integração ou demonstrações nesta revisão.

Portanto, as conclusões não devem ser interpretadas como comprovação de funcionamento completo do produto.

O relatório registra diferenças identificadas no escopo examinado e não garante ausência de outras divergências em arquivos não revisados.

Também não altera automaticamente issues, PRs ou código de produção.

## 10. Recomendações para a documentação futura

A documentação pública deve ser atualizada sempre que uma funcionalidade relevante for incorporada à `dev`.

Documentos que descrevem uma fotografia técnica de determinada data devem manter essa informação explícita e evitar utilizar o estado antigo como se fosse o estado atual.

Quando uma decisão envolver integração com outro grupo, é importante distinguir o contrato acordado do comportamento efetivamente implementado.

As docstrings devem descrever os parâmetros e as exceções de acordo com o código. Quando o comportamento for alterado, as descrições e os testes também devem ser revisados.

## 11. Referências

- `src/backend/api/exportacao_curriculo.py`
- `src/backend/api/revisao_versao_curriculo.py`
- `src/backend/application/revisao_versao_curriculo.py`
- `src/backend/api/vagas.py`
- `src/backend/infrastructure/integrations/cliente_vagas_grupo2.py`
- `src/frontend/app/App.tsx`
- `docs/manual-estudante.md`
- `docs/exportacao-pdf-docx.md`
- `docs/contrato-busca-vagas.md`
- `docs/guia-exportacao-pdf-docx.md`

## 12. Rastreabilidade

- **Issue:** #435 — F12.15
- **WBS:** 1.1.2.4, 1.8.2.1–1.8.2.4
- **Tipo de atividade:** revisão documental e registro de divergências
- **Resultado:** cinco divergências registradas no escopo analisado
- **Mudanças de produção:** nenhuma

## 13. Conclusão

A revisão identificou que os principais módulos analisados possuem docstrings que descrevem suas responsabilidades e seu funcionamento.

Entretanto, foram encontradas diferenças entre algumas descrições e o estado atual da implementação, principalmente na exportação PDF/DOCX e na integração externa de vagas.

As divergências foram registradas com suas evidências, impactos e encaminhamentos recomendados.

A resolução dos pontos identificados deve ser acompanhada pelos responsáveis correspondentes, com atualização da documentação e dos testes quando necessário.

Este documento conclui o registro de revisão previsto na issue #435 para o escopo declarado, sem afirmar que todas as divergências já foram corrigidas.
