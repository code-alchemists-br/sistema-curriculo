# Exportação de currículo em PDF e DOCX

**Estado da branch `dev`:** ainda não há um gerador de arquivo PDF/DOCX conectado ao sistema. Este documento registra o limite atual para evitar instruções que levem o estudante a procurar uma ação inexistente.

## O que já existe

- O backend disponibiliza a prévia de uma versão de currículo em `GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/previa`.
- O frontend possui modelos visuais de prévia e testes de responsividade.
- O cenário `jornada-selecao-previa-exportacao.e2e.test.tsx` simula localmente etapas de seleção e um exportador PDF que devolve um `Blob`. O próprio teste documenta que a UI/API de seleção e o gerador real de binários não estão integrados em `dev`.

## Instrução para estudantes

No estado atual da branch, não é possível orientar uma sequência real de cliques para baixar PDF ou DOCX. A prévia na tela não é um arquivo exportado. Quando o gerador e os controles estiverem integrados, atualizar este guia com: tela de origem, escolha de formato, nome/extensão do arquivo, comportamento durante a geração, local de download, erros recuperáveis e dispositivos/navegadores verificados.

Não solicite que estudantes usem impressão do navegador, conversores externos ou enviem dados pessoais para serviços de terceiros como substituto da exportação do produto.

## Evidências consultadas

- `src/frontend/app/jornada-selecao-previa-exportacao.e2e.test.tsx` (exportação simulada, não entrega de binário real).
- `src/backend/api/previa_versao_curriculo.py` (prévia JSON; não gera PDF/DOCX).
- `src/frontend/features/visualizar-curriculo/ui/ModeloClassico.tsx` e `ModeloCompacto.tsx` (apresentação visual).

**Card:** #386. A documentação de uma ação utilizável por estudantes depende de a exportação real ser implementada e integrada; este registro factual não fecha esse critério.
