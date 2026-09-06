# Check de aderência Cross-Cutting

Confirme:

1. o resultado principal pertence a observabilidade, resiliência, segurança ou identidade/acesso;
2. a análise define policy e critérios suficientes;
3. mudanças em outras camadas são somente pontos de integração transversais;
4. o modo de avaliação/implementação está claro;
5. qualquer teste a criar é unitário.

Inspecione análise, mecanismos existentes, configuração, imports, fluxo de dados, testes e `AGENTS.md`. Use somente leitura durante o gate.

## Sinais positivos

- objetivo é produzir ou avaliar sinais de telemetria;
- objetivo é controlar comportamento sob falha técnica;
- objetivo é mitigar ameaça ou proteger dado/segredo;
- objetivo é autenticar identidade ou decidir/enforçar acesso;
- implementação pode envolver várias camadas sem mudar comportamento funcional;
- critérios são verificáveis e a policy não precisa ser inventada.

Exija dois sinais independentes, incluindo um semântico ligado ao concern.

## Sinais negativos

- resultado principal é tela, regra de negócio, caso de uso, endpoint, persistência ou ambiente;
- logging, retry ou autorização aparecem apenas como detalhe incidental de outra demanda;
- análise pede teste não funcional, mas não implementação/avaliação do mecanismo;
- faltam matriz de acesso, ameaça, budget, segurança de retry ou schema de telemetria essenciais;
- mudança exigiria provisionar serviço, alterar CI/deploy/Nix ou operar sistema externo;
- teste solicitado atravessa uma fronteira real.

## Vereditos

### `valid`

> Análise `<caminho>` (`<versão>`) validada para Cross-Cutting no modo `<modo>`: <evidências>. Concerns: <lista>. Pontos de integração: <lista>. Testes superiores e operações externas em handoff: <lista ou “nenhum”>.

### `ambiguous`

Não altere arquivos quando concern, policy, modo, fronteira ou critério estiver indefinido. Informe a lacuna concreta e faça somente a pergunta necessária ou peça revisão da análise.

### `mismatch`

Não altere arquivos quando a finalidade pertencer a outra área. Informe as evidências, declare que nenhum arquivo foi alterado e encaminhe ao perfil correspondente.

## Casos limítrofes

- Dashboard de negócio é frontend; instrumentação e exportação das métricas técnicas são observabilidade.
- Retry no gateway é resiliência; a chamada e seu mapeamento funcional pertencem ao adapter/driver.
- Matriz de permissões e enforcement são autorização; regra de elegibilidade baseada em estado é domínio.
- Testar logs por collector real é integração; testar formatter/redactor isolado é unitário.
- Corrigir vulnerabilidade específica aprovada pode ser segurança; atualização geral de dependências não é automaticamente elegível.
