# Compatibilidade e Responsividade

## Objetivo

Este documento define a matriz de navegadores e larguras de tela suportadas pelo Sistema Currículo e estabelece os critérios mínimos para considerar uma interface responsiva.

A decisão detalha o RNF03 — Compatibilidade e adaptação da interface — e serve como referência para desenvolvimento, revisão e testes das interfaces do sistema.

## Navegadores suportados

O Sistema Currículo deve manter seus fluxos principais funcionais nas duas versões estáveis mais recentes dos seguintes navegadores:

| Navegador | Plataformas consideradas | Suporte |
|---|---|---|
| Google Chrome | Desktop e dispositivos móveis | Duas versões estáveis mais recentes |
| Microsoft Edge | Desktop | Duas versões estáveis mais recentes |
| Mozilla Firefox | Desktop | Duas versões estáveis mais recentes |
| Safari | macOS e iOS | Duas versões estáveis mais recentes |

O uso de versões relativas, em vez de números fixos de versão, evita que a matriz se torne obsoleta a cada atualização dos navegadores.

Internet Explorer e navegadores sem manutenção ativa não fazem parte da matriz de compatibilidade suportada.

## Larguras de tela de referência

A responsividade das interfaces deve considerar a seguinte matriz de larguras:

| Largura | Categoria de referência | Objetivo da verificação |
|---:|---|---|
| 360 px | Celular compacto | Verificar a menor largura suportada |
| 480 px | Celular | Verificar adaptação em telas móveis maiores |
| 640 px | Celular amplo / tablet compacto | Verificar a transição entre layouts móveis e intermediários |
| 768 px | Tablet | Verificar organização em telas intermediárias |
| 1024 px | Desktop compacto / tablet amplo | Verificar o início da experiência de desktop |
| 1280 px | Desktop | Verificar o layout padrão em computadores |

Essas larguras são pontos de referência para verificação e não representam os únicos tamanhos em que a interface deve funcionar.

A interface deve se adaptar continuamente entre essas larguras, sem depender de um modelo específico de aparelho.

## Largura mínima suportada

A menor largura prevista na matriz é **360 px**.

Abaixo desse valor não existe compromisso formal de suporte nesta versão do projeto.

Isso não impede que determinadas telas continuem funcionando em larguras menores, mas esse comportamento não faz parte do critério obrigatório de aceite.

## Orientação da interface

O suporte principal considera o uso em orientação vertical para dispositivos móveis e a utilização normal de tablets e computadores.

A interface não deve depender de uma orientação específica quando o conteúdo puder ser apresentado de forma adequada nas dimensões disponíveis.

## Critério de aceite de responsividade

Uma tela é considerada responsiva quando, dentro da matriz de larguras suportadas:

- todas as funcionalidades necessárias ao fluxo permanecem acessíveis;
- não ocorre rolagem horizontal causada pelo layout da aplicação;
- textos relevantes permanecem legíveis;
- botões, campos, links e demais controles continuam utilizáveis;
- elementos não apresentam sobreposição que impeça leitura ou interação;
- conteúdos extensos não rompem o layout;
- ações principais permanecem disponíveis ao usuário;
- informações essenciais não são ocultadas apenas por causa da largura da tela;
- a adaptação de layout não altera a regra de negócio nem remove funcionalidades;
- a navegação por teclado continua utilizável quando aplicável.

Rolagem horizontal intencional dentro de componentes cuja natureza exija esse comportamento deve ser analisada separadamente e não caracteriza, por si só, falha de responsividade.

## Critério de aceite de compatibilidade entre navegadores

Um navegador da matriz é considerado compatível quando os fluxos principais podem ser executados sem perda de funcionalidade causada pelo navegador.

Diferenças puramente visuais e não funcionais entre mecanismos de renderização são aceitáveis quando não prejudicam:

- leitura do conteúdo;
- navegação;
- preenchimento de formulários;
- utilização dos controles;
- visualização do currículo;
- exportação;
- autenticação;
- busca de vagas;
- associação entre currículo e vaga.

## Fluxos prioritários para verificação

A matriz deve ser aplicada prioritariamente aos fluxos críticos do produto:

1. cadastro e autenticação;
2. recuperação de acesso;
3. preenchimento e edição dos dados do estudante;
4. criação e edição de currículo;
5. revisão dos dados;
6. visualização do currículo;
7. exportação do currículo;
8. busca de vagas;
9. associação entre currículo e vaga.

Quando uma funcionalidade ainda não estiver implementada, sua validação deve ocorrer quando a respectiva interface for entregue.

## Estratégia de verificação

Alterações de interface devem considerar a matriz definida neste documento.

Testes automatizados de responsividade podem verificar propriedades observáveis e regras de layout que sejam representáveis no ambiente de testes.

Quando o ambiente automatizado não reproduzir de forma confiável geometria, renderização ou comportamento real de navegador, a evidência automatizada não deve ser apresentada como se fosse uma validação visual completa.

Verificações manuais ou end-to-end em navegador real podem complementar os testes automatizados quando necessário.

## Relação com o RNF03

Esta decisão detalha o requisito não funcional RNF03, segundo o qual a interface deve manter suas funcionalidades em computadores e dispositivos móveis.

A matriz aprovada passa a ser composta pelos navegadores e pelas larguras registrados neste documento.

## Limites desta decisão

Esta definição trata de compatibilidade de navegador e responsividade.

Ela não estabelece:

- nível de conformidade de acessibilidade;
- critérios de contraste;
- requisitos específicos de leitores de tela;
- política de zoom;
- requisitos de desempenho;
- suporte a aplicativos nativos;
- suporte a navegadores obsoletos.

Os critérios específicos de acessibilidade pertencem à decisão correspondente ao RNF02.

## Rastreabilidade

- **Issue:** #168 — F1.1
- **Requisito relacionado:** RNF03 — Compatibilidade e adaptação da interface
- **WBS:** 1.1.1.4, 1.1.2.4, 1.2.1.4, 1.7.2.4, 1.8.2.4
