# Manual do estudante: cadastro, currículo e prévia

**Estado da branch `dev`:** fotografia técnica do commit `ab2b8bc` (19/10/2026), não um guia de uma aplicação publicada. A tela raiz em `src/frontend/app/App.tsx` apresenta atualmente o acesso do estudante. Há páginas e componentes de funcionalidades em desenvolvimento, mas nem todas estão conectadas à navegação executável.

## Jornada prevista e capacidades existentes

1. **Acessar a conta.** A interface raiz apresenta a página de acesso. Use uma conta própria do ambiente de desenvolvimento; não compartilhe credenciais em demonstrações.
2. **Cadastrar dados do perfil.** A API possui cadastro/edição de informações e rotas de criação para competência, idioma, curso, certificação, projeto acadêmico e link profissional. Os dados são vinculados ao estudante autenticado.
3. **Criar uma versão de currículo.** O backend permite criar uma versão com título, layout e visibilidade. O padrão de visibilidade é privado.
4. **Escolher itens para a versão.** A API possui operações de seleção/desseleção de itens por tipo e identificador. O cenário E2E demonstra esse passo com dados e telas simulados localmente; a integração completa da jornada ainda não está conectada em `dev`.
5. **Revisar e visualizar.** A API fornece uma prévia com dados selecionados, layout e seções ordenadas. Os modelos clássico e compacto são componentes visuais disponíveis, não confirmação de que uma página de navegação já esteja publicada.
6. **Exportar.** PDF/DOCX ainda não tem gerador real integrado em `dev`; consulte [`exportacao-pdf-docx.md`](exportacao-pdf-docx.md). Não ofereça ao estudante uma ação de download que o produto ainda não fornece.

## Privacidade e uso de dados

Use somente dados fictícios da massa de teste para demonstrações. Não copie nomes, documentos, tokens ou currículos reais para screenshots, logs ou issues. A API associa cadastros à sessão e não deve aceitar um `usuario_id` arbitrário no corpo para alterar o proprietário.

## Referências verificadas

- Jornada de produto planejada: [`mapeamento_jornadas.md`](mapeamento_jornadas.md).
- Modelos de currículo: [`modelos_curriculo.md`](modelos_curriculo.md).
- Contratos complementares: [`contratos-informacoes-complementares.md`](contratos-informacoes-complementares.md).
- Prévia: [`previa-curriculo.md`](previa-curriculo.md).
- Estado inicial da aplicação: `src/frontend/app/App.tsx`.
- Cenário de jornada simulado: `src/frontend/app/jornada-selecao-previa-exportacao.e2e.test.tsx`.

**Card:** #432. Antes de divulgar como manual operacional, validar cada etapa numa instância integrada e registrar as rotas/telas efetivamente expostas nessa versão.
