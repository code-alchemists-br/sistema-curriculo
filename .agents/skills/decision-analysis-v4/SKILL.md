---
name: decision-analysis-v4
description: Cria ou revisa uma análise decisória de demandas e artefatos antes da implementação, identifica os arquivos analisados e escolhe dinamicamente a subpasta apropriada em prompts. Use para delimitar problemas, comparar decisões e incorporar informações posteriores sem apagar versões; não use para implementar a decisão.
---

# Análise de decisão com proveniência de artefatos

Produza uma especificação revisável do problema e da decisão, preservando proveniência dos insumos, artefatos examinados, evolução e localização semântica da saída.

## Autoridade e escopo

- Obedeça à cadeia de `AGENTS.md` aplicável ao workspace, aos artefatos analisados e ao diretório de destino. Instruções mais específicas governam restrições, nomenclatura e escrita naquele local.
- Trate a solicitação explícita do usuário como objetivo, sem ampliar autorização ou escopo.
- Não implemente código, configuração, infraestrutura ou a decisão analisada. A única escrita permitida é um novo artefato Markdown de análise.
- Se uma instrução aplicável impedir ou contradizer materialmente a análise, explique o conflito e solicite direção; não improvise uma exceção.
- Registre necessidades de outras atividades como handoffs, sem executá-las.

## Referências

Antes de qualquer análise, leia:

1. [Taxonomia de classificação e valor](references/classification-taxonomy.md).
2. [Esquema do artefato](references/output-schema.md).
3. [Protocolo de roteamento](references/output-routing.md).

Leia também:

- [Classificação de artefatos](references/artifact-classification.md) quando a demanda mencionar ou exigir examinar arquivo, conjunto de arquivos, diretório, diff ou repositório.
- [Protocolo de revisão](references/revision-protocol.md) quando houver artefato anterior, pedido de melhoria ou informação posterior sobre o mesmo problema.

## Seleção do modo

- Use `initial` quando não existir análise anterior identificada.
- Use `revision` quando o usuário referenciar análise anterior ou pedir atualização, correção, enriquecimento ou reavaliação.
- Se faltarem a nova informação ou a identificação inequívoca do artefato anterior, peça somente o dado ausente antes de escrever.
- Não transforme informação complementar em análise independente quando ela claramente altera uma linhagem existente.

## Identificação do objeto analisado

- Determine se a análise trata somente de uma demanda ou também de arquivos, diretórios, diff ou repositório.
- Para cada arquivo efetivamente usado como evidência, registre caminho, relação com a análise, representação, função, formato, recorte examinado e estado do conteúdo.
- Não classifique apenas pela extensão. Use nome, conteúdo e papel no sistema.
- Diferencie artefato principal de contexto de apoio. Não liste arquivos apenas descobertos, mas não examinados.
- Se um arquivo essencial não estiver disponível, não finja tê-lo analisado: registre a indisponibilidade e use `status: pending` quando ela impedir uma decisão responsável.

## Método comum

1. Consulte somente o contexto necessário e separe fatos observados, declarações do usuário e inferências.
2. Preserve literalmente os insumos do usuário. Redija somente credenciais, segredos ou dados pessoais desnecessários, marcando cada remoção como `[REDACTED]`.
3. Registre os artefatos analisados conforme a referência aplicável.
4. Classifique o problema em eixos independentes: uma esfera primária, até três preocupações e metadados relevantes.
5. Enriqueça o problema sem mudar sua intenção: resultado, atores, fatos, hipóteses, dúvidas, escopo, não objetivos e critérios de sucesso.
6. Faça perguntas somente quando respostas plausíveis levarem a decisões materialmente diferentes. Caso contrário, prossiga com hipóteses explícitas e defina como validá-las.
7. Identifique restrições duras antes de comparar alternativas. Alternativas que as violem são inviáveis.
8. Compare estado atual e pelo menos duas alternativas viáveis quando existir decisão real. Se houver somente uma opção legítima, demonstre por que as demais são inviáveis.
9. Avalie apenas dimensões que diferenciem alternativas. Use escala ordinal, confiança e evidência; não some pontuações como medida cardinal.
10. Recomende decisão somente com evidência suficiente. Caso contrário, use `status: pending` e indique a menor investigação capaz de destravá-la.
11. Diferencie dimensões maximizadas ou priorizadas, dimensões satisfeitas por limiar, perdas se prioridades não forem atendidas e custos aceitos para priorizá-las.
12. Defina validação e sinais que justificariam revisar a decisão.

## Roteamento do artefato

- Localize `prompts` na raiz do projeto e inventarie dinamicamente suas subpastas imediatas existentes.
- Não presuma lista fixa nem crie categoria ausente.
- Escolha uma pasta existente usando classificação do problema, propósito, artefatos analisados e convenções observáveis.
- Leia instruções `AGENTS.md` ou `AGENTS.override.md` aplicáveis à pasta candidata antes de confirmar o destino.
- Não escolha `templates` apenas por se tratar de prompt, nem `revisao` apenas porque `lineage.mode` é `revision`.
- Revisões ordinárias preferem a pasta da linhagem anterior, salvo mudança material de assunto.
- Se `prompts` não existir, não houver subpastas ou nenhuma candidata for defensável, não escreva: solicite destino ou criação da estrutura.
- Registre pasta escolhida, candidatas, confiança e justificativa no frontmatter.

## Regras para revisão

- Leia e valide o artefato anterior antes de revisar.
- Preserve o primeiro prompt da linhagem e registre novas entradas literalmente.
- Reavalie também os artefatos de entrada: arquivos podem ter sido adicionados, removidos, alterados ou examinados em outro recorte.
- Classifique a mudança e seu impacto sobre a decisão.
- Reavalie classificação, problema, restrições, alternativas, pagamento, decisão, perdas, riscos e validação.
- Explique diferenças materiais em `Mudanças desde a versão anterior`.
- Produza versão autossuficiente e nunca altere retrospectivamente a anterior.

## Saída e versionamento

- Gere exatamente um novo `.md` diretamente na subpasta selecionada de `prompts`.
- Use `<YYYYMMDD>-<slug>-vNNN.md`, salvo regra mais específica do `AGENTS.md` do destino.
- Nunca sobrescreva. Comece em `v001`; em revisão, incremente a maior versão da linhagem, mesmo ao mudar de pasta.
- Use o esquema completo e escreva `Nenhum identificado` em seções inaplicáveis.
- Ao terminar, informe modo, classificação, objeto analisado, decisão, impacto da revisão e principal incerteza.
- Termine sempre com: `Arquivo criado em <caminho>. Avalie se o local escolhido é de fato o mais adequado.`

## Critérios de qualidade

- O problema enriquecido deve permanecer reconhecível como o problema apresentado.
- A recomendação deve decorrer da comparação.
- Fatos, hipóteses, entradas posteriores e conteúdo de arquivos devem permanecer distinguíveis.
- A saída deve permitir saber exatamente quais artefatos sustentaram a análise e qual recorte foi examinado.
- Uma revisão não pode ocultar mudança nos arquivos ou na decisão anterior.
- Benefícios, perdas por não priorizar e custos de priorização devem ser distintos.
- A pasta escolhida requer justificativa semântica, não apenas correspondência por extensão.
- Não use `maximized` sem comparação nem esconda incerteza com pontuações artificiais.
