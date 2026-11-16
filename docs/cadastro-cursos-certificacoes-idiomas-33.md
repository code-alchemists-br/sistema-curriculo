# Cadastro de cursos, certificações e idiomas — issue #33

## Escopo e decisões

As telas existentes foram preservadas. O PR #552 havia entregue somente uma
correção parcial do backend; esta entrega liga validação, navegação e cadastro
nas etapas de cursos/certificações e idiomas.

- São seções opcionais: uma entrada totalmente vazia não gera cadastro.
- Uma entrada parcialmente preenchida precisa ser corrigida ou removida antes
  de avançar. O primeiro campo inválido recebe foco e descrição acessível.
- Carga horária é opcional. Quando informada, deve conter um inteiro decimal
  de 1 a 10000; não há arredondamento silencioso.
- As páginas usam a validação pública dos formulários por referências tipadas,
  mantendo regras e normalização nas respectivas features, sem chamadas HTTP
  na UI. Isso reutiliza a validação em vez de duplicá-la no App.
- Próximo aguarda a persistência, bloqueia nova submissão e edição durante o
  envio e preserva o rascunho se houver falha. Erro não é tratado como sucesso.
- Cada cliente lembra apenas payloads confirmados durante sua instância para
  não reenviar cadastros anteriores ao voltar à etapa ou tentar novamente após
  sucesso parcial. O App mantém instâncias separadas por conta.
- A aplicação ASGI passa a conectar o cadastro de idiomas ao executor
  transacional existente; o endpoint real antes retornava 503 mesmo com banco.
  Não há alteração de schema, migração ou regra de autenticação.

## Limites explícitos

Não é uma implementação de edição/exclusão remota nem de carregamento dos
cadastros do servidor. A lembrança de confirmações é local à instância, não uma
garantia de exactly-once após recarregar a página ou perder a resposta de rede.
HTTP 409 continua sendo uma falha visível, nunca uma confirmação presumida.
Sem `VITE_API_URL`, permanece o fluxo local. Com API configurada, falhas reais
não são escondidas: HTTP 409 explica que criação não atualiza o perfil; a pessoa
pode restaurar seus valores anteriores ou escolher explicitamente continuar
apenas com o rascunho local. Essa opção não faz novos POSTs nem confirma
sincronização e não altera os registros existentes no perfil. Cadastros de
outras etapas não foram alterados.

## Validação realizada

Em WSL com os ambientes Nix definidos pelo projeto:

- Frontend: 591 testes em 92 arquivos; tipagem, ESLint e build aprovados.
- A revisão independente identificou e motivou regressões adicionais: envios
  são cancelados na saída/histórico/logout e não restauram dados da conta
  anterior; Enter usa o mesmo coordenador de envio de Próximo; conflitos de
  criação explicam que o perfil não foi atualizado e permitem continuar apenas
  com o rascunho local por decisão explícita da pessoa.
- Backend: execução canônica de 1324 testes, aprovada com 126 testes de
  integração pulados por ausência deliberada de banco no ambiente unitário;
  os 26 testes focais de idiomas/composição e regressão da #33 também passaram.
- Formatação aprovada com `--end-of-line auto` para acomodar o checkout CRLF
  do Windows sem reformatação global não relacionada.
- PostgreSQL descartável: 37 testes do comando de integração da CI aprovados,
  incluindo os cinco novos cenários de idiomas e regressões de associações,
  infraestrutura PostgreSQL e cursos/certificações.
- Os testes unitários substituem apenas as fronteiras externas necessárias
  por doubles (`fetch`, engine/factory); a validação e os componentes são reais.
- Regressões foram observadas falhando antes das correções: avanço inválido,
  envio duplicado, falha ocultada e ausência de `cadastrar_idioma` na composição.

### Roteiro no navegador com API e PostgreSQL reais

1. Preencher apenas o nome do curso e clicar Próximo: não avançar nem enviar
   HTTP; instituição inválida deve receber foco.
2. Completar instituição e informar carga `1.5`: impedir envio sem arredondar.
3. Corrigir carga para `40`, preencher certificação sem emissor: impedir ambos
   os cadastros até corrigir o emissor.
4. Completar e avançar: observar HTTP 201 em `/cursos` e `/certificacoes`.
5. Informar idioma sem nível: impedir avanço. Selecionar nível por teclado e
   avançar: observar HTTP 201 em `/idiomas`.
6. Voltar a cursos, adicionar outro com carga vazia e avançar: enviar somente o
   novo curso, com `carga_horaria: null`, sem duplicar os confirmados.
7. Conferir por conexão independente: a conta sintética possui dois cursos,
   uma certificação e um idioma persistidos.
8. Verificar as duas telas em larguras reais de 360 e 1280 pixels: documento e
   controles sem overflow horizontal.

Os passos acima foram executados. Os logs e a massa sintética ficam fora do
repositório; não usam contas, dados ou banco de produção.

## Observações do ambiente

O build mantém aviso de chunk acima de 500 kB. A instalação da base já reportava
vulnerabilidades de dependências; esta correção não altera lockfile nem tenta
resolvê-las com atualização não relacionada. Os shells Nix em checkout Windows
podem emitir aviso de CRLF. Para validar alterações Windows pelo Vite no WSL,
use polling de arquivos ou reinicie o servidor antes do roteiro; um watcher
inotify pode continuar servindo código antigo.
