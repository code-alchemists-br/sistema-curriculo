# Protocolo de revisão

Use somente no modo `revision`.

## Linhagem e mudança

1. Resolva o artefato anterior e leia versão, solicitação, classificação, objetos analisados, roteamento e decisão.
2. Confirme que a nova informação pertence ao mesmo problema.
3. Use a próxima versão da linhagem, sem preencher lacunas.
4. Escolha `change_type`: `enrichment`, `correction`, `scope-change` ou `reassessment`; registre tipos secundários separadamente.
5. Escolha `decision_impact`: `unchanged`, `strengthened`, `revised`, `reopened` ou `invalidated`.

## Proveniência

- Preserve a primeira solicitação e registre novos textos do usuário literalmente, por versão.
- Não apresente interpretação como entrada do usuário.
- Reavalie todas as seções afetadas e verifique explicitamente as demais.
- Produza versão autossuficiente e tabela de mudanças materiais.
- Não modifique nem apague artefatos substituídos.

## Mudança nos artefatos analisados

- Compare a lista, o recorte e o estado dos arquivos com a versão anterior.
- Arquivo adicionado ou removido, conteúdo alterado ou recorte ampliado deve aparecer no delta.
- Releia arquivos alterados; não reutilize conclusões como se a evidência fosse idêntica.
- Se o artefato principal mudou materialmente, considere `change_type: reassessment`.
- Se um arquivo essencial se tornou indisponível, considere `decision_impact: reopened` e `status: pending`.

## Roteamento

- Prefira o diretório anterior e reavalie contra as pastas atuais de `prompts`.
- Mudança de pasta deve aparecer no delta, preservando `root` e `supersedes`.
- Se o usuário rejeitar o destino, gere nova versão na pasta aprovada; não apague a anterior.
