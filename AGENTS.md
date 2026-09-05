# Regras gerais para agentes

Estas instruções se aplicam a todo o repositório. Arquivos `AGENTS.md`
existentes em subpastas definem regras adicionais para o conteúdo e as
atividades realizadas dentro de seus respectivos escopos.

## Níveis de instrução

- `[CRITICAL]` — violar esta regra torna a solução inválida.
- `[REQUIRED]` — esta regra DEVE ser cumprida.
- `[FORBIDDEN]` — esta prática NÃO DEVE ser utilizada.
- `[PREFERRED]` — adote como padrão; desvios exigem justificativa técnica.
- `[CONSIDER]` — avalie a aplicação conforme o contexto.

# Regras de escopo

## CRITICAL — Instruções de subpastas

**Todo `AGENTS.md` aplicável DEVE ser lido antes de qualquer atividade.**

[CRITICAL] Antes de alterar, adicionar, remover, executar ou avaliar conteúdo
em uma pasta, o agente DEVE procurar e ler os arquivos `AGENTS.md` existentes
no caminho entre a raiz do repositório e a pasta-alvo.

[REQUIRED] Este arquivo define as regras gerais do repositório. Um `AGENTS.md`
de subpasta define regras locais adicionais para todos os arquivos, comandos e
atividades dentro daquela pasta e de suas descendentes.

[REQUIRED] Ao trabalhar em múltiplas pastas, o agente DEVE identificar e seguir
separadamente o conjunto de instruções aplicável a cada uma delas.

[REQUIRED] Regras de subpastas DEVE ser tratadas como especializações das
regras da raiz. Em caso de conflito, a instrução mais específica DEVE ser
seguida, exceto quando ela reduzir uma restrição `[CRITICAL]` ou `[FORBIDDEN]`
de um nível superior; nesse caso, prevalece a regra mais restritiva.

[FORBIDDEN] NEVER presuma que apenas este arquivo contém todas as instruções do
projeto. A ausência de leitura de um `AGENTS.md` aplicável não isenta o agente
de cumprir suas regras.

# Ambientes de desenvolvimento

## CRITICAL — Uso obrigatório do Nix

**Toda ferramenta de desenvolvimento DEVE ser executada pelo ambiente Nix do
projeto correspondente à atividade.**

[CRITICAL] Comandos de desenvolvimento, instalação ou execução de
dependências, builds, testes, linters, formatadores, verificações, scripts e
ferramentas auxiliares DEVE utilizar os ambientes Nix definidos pelo projeto.

[FORBIDDEN] Ferramentas instaladas globalmente na máquina NÃO DEVE ser usadas
para realizar atividades de desenvolvimento deste repositório.

[REQUIRED] Antes de executar comandos, siga a seção
[Utilizando um ambiente Nix do projeto](docs/configuracao-ambiente.md#utilizando-um-ambiente-nix-do-projeto).

[REQUIRED] Entre no ambiente apropriado com `nix develop .#<ambiente>` ou
execute um comando pontual com
`nix develop .#<ambiente> --command <comando>`.

## Ambientes disponíveis

- **Backend:** use `nix develop .#backend` para atividades em `src/backend`.
- **Frontend:** use `nix develop .#frontend` para atividades em `src/frontend`.
- **Testes:** use `nix develop .#tests` para os testes formais do projeto. Esse
  ambiente é obrigatório para testes de integração e níveis superiores.

[REQUIRED] O agente DEVE selecionar o ambiente correspondente à atividade. Um
comando de backend deve usar `backend`; um comando de frontend deve usar
`frontend`; e testes de integração ou de nível superior devem usar `tests`.

## Exceção — Testes unitários

[REQUIRED] Toda mudança de comportamento DEVE incluir e executar os testes
unitários pertinentes durante a atividade de desenvolvimento.

[REQUIRED] Testes unitários DEVE ser executados no ambiente do componente ao
qual pertencem: `backend` ou `frontend`.

[PREFERRED] Os testes unitários devem permanecer próximos ao ciclo de
desenvolvimento do componente e ser rápidos, isolados e determinísticos.

[FORBIDDEN] O ambiente `tests` NÃO DEVE ser exigido para executar somente
testes unitários. Essa exceção não se aplica a testes de integração, de sistema,
end-to-end ou de nível superior, que DEVE utilizar `nix develop .#tests`.

# Documentação do código

## REQUIRED — Funções, classes e DTOs

[REQUIRED] Toda função e toda classe, inclusive DTOs, DEVE possuir uma docstring
ou o formato de documentação equivalente da linguagem.

[REQUIRED] A documentação DEVE explicar explicitamente:

- **O que faz:** sua responsabilidade e seu comportamento.
- **Como faz:** a abordagem, o fluxo ou as regras utilizadas.
- **Qual finalidade atende:** por que existe e qual necessidade do sistema
  resolve.

[REQUIRED] As três informações DEVE estar presentes mesmo em implementações
simples.

[REQUIRED] A documentação DEVE refletir o comportamento atual e DEVE ser
atualizada junto com qualquer alteração correspondente no código.
