# Checklist de demonstração com dados sintéticos

Este roteiro foi preparado para a branch `dev` no commit `ab2b8bc` (19/10/2026). Execute-o somente em ambiente de demonstração, com serviços e dados de teste. A lista é um roteiro, não um registro de execução ou aceite.

## Antes da demonstração

- [ ] Confirmar branch/commit e ambiente que serão exibidos.
- [ ] Iniciar os serviços seguindo [`configuracao-ambiente.md`](configuracao-ambiente.md); verificar health/readiness separadamente.
- [ ] Usar somente os exemplos sintéticos de [`massa_teste_curriculos.json`](massa_teste_curriculos.json) ou [`src/backend/tests/fixtures/massa_teste_curriculos.py`](../src/backend/tests/fixtures/massa_teste_curriculos.py).
- [ ] Conferir que nenhum token, senha, arquivo real ou dado pessoal aparece na tela.
- [ ] Preparar o estado inicial e capturar o commit exibido. Não apresentar mock ou teste unitário como integração executável.

## Roteiro

| Etapa | Ação | Resultado esperado | Evidência a registrar |
| --- | --- | --- | --- |
| 1. Acesso | Abrir a aplicação no estado disponível em `dev`. | Tela de acesso visível. | Screenshot sem credenciais. |
| 2. Contratos | Em ambiente controlado, consultar uma rota de API autorizada com dados sintéticos. | Resposta coerente com o contrato e identidade autenticada. | Método, rota, status e exemplo sanitizado. |
| 3. Versão e seleção | Se a UI completa estiver ligada no ambiente, criar versão privada e selecionar itens sintéticos. | Itens associados somente à versão escolhida. | ID fictício e estado de seleção. Se estiver usando o harness E2E, identificar claramente como simulação. |
| 4. Prévia | Consultar/renderizar a prévia com itens e testar uma seção vazia. | Campos ordenados e mensagem de estado vazio sem dados inventados. | Screenshot, layout e commit. |
| 5. Vagas | Demonstrar o erro controlado da integração Grupo 2 quando o serviço não estiver configurado. | Mensagem compreensível, sem stack trace ou URL interna. | Código de cenário e captura sanitizada. |
| 6. Exportação | Verificar se existe gerador real integrado antes de tentar baixar. | Em `dev` do commit indicado, não declarar PDF/DOCX funcional: o gerador do cenário E2E é simulado. | Registrar “não disponível” até integração real. |

## Falhas esperadas para ensaio

- sessão ausente → `401` em rota protegida;
- UUID ou corpo inválido → `422`;
- estudante/versão não encontrado → `404` na prévia;
- executor indisponível → `503`;
- busca externa inválida/indisponível/timeout → mensagens controladas; no backend de busca, `502`/`504`;
- listas sem resultados → estado vazio, mantendo os demais dados e critérios.

Não provoque falhas em produção, não use dados de estudantes reais e não transforme uma expectativa deste roteiro em evidência de que a execução ocorreu.

## Registro da sessão

- Data e responsável: **preencher após executar**.
- Ambiente e commit: **preencher**.
- Etapas realmente executadas: **marcar**.
- Falhas observadas e evidências: **anexar links sanitizados**.
- Limitações/diferenças em relação ao roteiro: **descrever**.

**Card:** #388. O checklist está elaborado; a execução de demonstração continua pendente.
