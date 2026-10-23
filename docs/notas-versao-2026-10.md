# Notas de versão — fotografia da branch `dev` (19/10/2026)

**Commit consultado:** `ab2b8bc28c19bd55cacef41a4401ad9e34040276`. Estas notas descrevem o estado do código da branch `dev`; não afirmam implantação em produção nem aceite de produto.

## Funcionalidades e entregas observadas

- Perfil e cadastro de informações profissionais/complementares por contratos HTTP específicos, com validação e vínculo ao usuário autenticado.
- Criação/listagem de versões de currículo, seleção de itens e endpoint de prévia estruturada.
- Componentes visuais para modelos clássico e compacto, com teste de seções vazias e responsividade.
- Contrato de consulta de vagas e tratamento seguro de falhas de integração.
- Assistente determinístico para descrição de projetos acadêmicos; não equivale a geração por serviço de IA.
- Política de limites recarregável da adequação semântica, adicionada no PR #564. Isso não significa que a adequação completa do currículo a vagas esteja pronta.

## Limitações conhecidas nesta fotografia

- A raiz da aplicação web ainda apresenta a tela de acesso; páginas/componentes e testes isolados não comprovam jornada integrada.
- O cliente de sugestões do Grupo 2 está em modo indisponível enquanto não existir endpoint externo confirmado.
- O cenário E2E de seleção/prévia/exportação simula partes da jornada; não há gerador real de PDF/DOCX integrado.
- A prévia JSON não é arquivo exportado.
- Algumas operações de informações complementares documentadas estão disponíveis como cadastro (`POST`); não pressupor endpoints de CRUD que não aparecem no código.
- “Adequação semântica”, recomendações automáticas e disponibilidade de produção não são afirmadas por esta versão.

## Pendências

1. Integrar e validar a jornada de estudante na aplicação.
2. Confirmar contrato e disponibilidade do serviço de vagas externo.
3. Implementar e validar exportação real em PDF e DOCX antes de publicar instruções de download.
4. Executar demonstração com ambiente e dados sintéticos; registrar evidências e decisão formal de entrega.

## Fontes

- Branch `dev` no commit acima; PR #564: <https://github.com/code-alchemists-br/sistema-curriculo/pull/564>.
- Código de preview e modelos: `src/backend/api/previa_versao_curriculo.py`, `src/frontend/features/visualizar-curriculo/`.
- Cenário de jornada: `src/frontend/app/jornada-selecao-previa-exportacao.e2e.test.tsx`.
- Limites de adequação: [`adequacao_semantica_ia.md`](adequacao_semantica_ia.md).

**Card:** #434. Atualizar esta fotografia depois da próxima integração/revisão; não usar como nota de release publicada.
