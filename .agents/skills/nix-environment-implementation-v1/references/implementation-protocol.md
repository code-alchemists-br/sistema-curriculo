# Protocolo de implementação Nix

Use somente após o gate resultar em `valid`.

## Delimitar

1. Mapeie critérios `nix-source` e `nix-managed-artifact` a arquivos e verificações.
2. Liste `non-nix` e `system-activation` como handoffs antes de escrever.
3. Identifique estilo, estrutura, sistemas suportados e mecanismo de pinagem já existentes.
4. Escolha o menor conjunto coeso de alterações Nix necessário à decisão.
5. Confirme o `AGENTS.md` mais específico antes de editar cada caminho.

## Implementar

- Preserve o estilo do repositório: flake ou legado, organização de módulos, formatter e convenções de argumentos.
- Mantenha pinagem e reprodutibilidade; não introduza referência flutuante quando o projeto usa locks.
- Reutilize inputs, overlays, helpers e módulos existentes antes de duplicar composição.
- Suporte somente os sistemas aprovados; não alegue portabilidade não verificada.
- Atualize `flake.lock` por comando Nix direcionado ao input necessário, quando a análise exigir mudança de lock.
- Não edite locks manualmente salvo convenção documentada e necessidade excepcional comprovada.
- Não altere arquivo não Nix, mesmo para “completar” a experiência do ambiente.
- Não aplique a configuração ao host nem modifique estado global.

## Verificar

Descubra comandos pelas instruções e estrutura do projeto. Conforme o tipo de artefato e a disponibilidade do Nix, considere:

- formatter apenas nos arquivos Nix alterados;
- parse ou avaliação dos atributos afetados;
- `nix flake check` com escopo apropriado;
- `nix build --no-link` dos outputs relevantes;
- avaliação de módulos para os sistemas aprovados;
- entrada não interativa em dev shell apenas quando necessária para confirmar ferramentas e versões.

Não ative módulos nem instale profiles. Se Nix não estiver disponível, faça inspeção estática, diga quais verificações não rodaram e não simule sucesso.

Depois, inspecione o diff e confirme:

- todos os arquivos alterados são `nix-source` ou `nix-managed-artifact` aprovados;
- nenhum código da aplicação, manifesto de linguagem, script ou infraestrutura não Nix mudou;
- nenhum output, store path ou `result` foi criado para versionamento;
- atualizações de lock ficaram restritas aos inputs pretendidos;
- mudanças preexistentes foram preservadas;
- verificações relatadas foram executadas de fato.

## Relatar

Informe:

1. análise e versão aplicadas;
2. evidências do veredito `valid`;
3. ambiente, pacote, módulo ou output Nix entregue;
4. artefatos alterados e mudanças de pinagem;
5. verificações e sistemas avaliados;
6. instruções adicionais incorporadas;
7. arquivos não Nix e ativações deixados como handoff.

Se somente a fatia Nix foi entregue, diga explicitamente que a análise completa depende dos handoffs.
