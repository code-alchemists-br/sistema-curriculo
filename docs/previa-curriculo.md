# Prévia de currículo: contrato e estados

**Escopo:** contrato da API e componentes visuais presentes na branch `dev`, commit `ab2b8bc` (19/10/2026). A existência de componentes e testes isolados não significa que toda a jornada já esteja ligada à aplicação executável.

## Consulta

`GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/previa` retorna `curriculo_id`, `titulo_versao`, `layout`, `estudante` e listas ordenadas de `formacoes`, `experiencias`, `projetos`, `competencias`, `idiomas` e `documentos`. Itens não selecionados não aparecem. A resposta omite credenciais e caminho interno de armazenamento dos documentos.

Uma versão inexistente ou que não pertença ao estudante resulta em `404`; executor não configurado resulta em `503`. UUIDs inválidos são rejeitados pela validação HTTP (`422`). A rota não deve ser interpretada como exportação de arquivo PDF/DOCX.

## Estados da apresentação

| Estado | Contrato/componente observado | Orientação para a interface |
| --- | --- | --- |
| Carregando | É o período assíncrono antes da resposta da API; não há código HTTP específico para esse estado. | Indicar progresso e evitar apresentar uma prévia antiga como se fosse atual. O estado deve permanecer visível enquanto a requisição estiver pendente. |
| Sucesso com conteúdo | DTO da prévia com uma ou mais listas preenchidas. Os modelos clássico e compacto apresentam as seções conforme o layout e a ordem recebidos. | Mostrar os dados selecionados sem alterar o perfil de origem. |
| Seção vazia | Uma lista pode vir vazia. `EstadoVazioSecao` apresenta mensagem acessível (“Nenhum item selecionado ou cadastrado para…”) e ação opcional. | Explicar a seção vazia sem inventar dados nem ocultar o restante do currículo. |
| Falha | `404`, `422` ou `503` conforme a causa da requisição. | Exibir explicação em português, oferecer retorno para edição/tentativa quando aplicável e não mostrar detalhes técnicos. |

Os testes dos modelos verificam apresentação e estados vazios; os testes de API verificam contrato, seleção e falhas. A API não define texto de carregamento: esse texto é responsabilidade da integração de tela.

## Referências

- Backend: [`api/previa_versao_curriculo.py`](../src/backend/api/previa_versao_curriculo.py), `tests/test_api_previa_versao_curriculo.py` e `tests/test_application_previa_versao_curriculo.py`.
- Interface: [`ModeloClassico.tsx`](../src/frontend/features/visualizar-curriculo/ui/ModeloClassico.tsx), [`ModeloCompacto.tsx`](../src/frontend/features/visualizar-curriculo/ui/ModeloCompacto.tsx), [`EstadoVazioSecao.tsx`](../src/frontend/features/visualizar-curriculo/ui/EstadoVazioSecao.tsx) e seus testes.

**Card:** #427.
