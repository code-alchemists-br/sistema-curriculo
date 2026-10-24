# Padrão de Acessibilidade

## Objetivo

Este documento define o padrão e o nível-alvo de acessibilidade do Sistema Currículo e estabelece a lista mínima de verificações que deve ser considerada nas telas da aplicação.

A decisão detalha o RNF02 — Acessibilidade — e serve como referência para desenvolvimento, revisão e testes das interfaces do sistema.

## Padrão de referência

O Sistema Currículo adota como referência:

**Web Content Accessibility Guidelines — WCAG 2.2**

O nível-alvo definido para a aplicação é:

**WCAG 2.2 — Nível AA**

O nível AA inclui os critérios aplicáveis dos níveis A e AA.

Esta definição representa um objetivo de conformidade para o desenvolvimento e a validação das interfaces. Ela não constitui, por si só, uma declaração de certificação ou conformidade integral de todas as telas existentes.

## Princípios

As verificações de acessibilidade devem considerar os quatro princípios da WCAG:

- perceptível;
- operável;
- compreensível;
- robusto.

As interfaces devem permitir que informações e funcionalidades essenciais possam ser percebidas, utilizadas e compreendidas por usuários com diferentes necessidades e tecnologias assistivas.

## Lista mínima de verificações por tela

Toda tela nova ou alterada deve ser analisada considerando, quando aplicável, os critérios mínimos abaixo.

### Estrutura e semântica

- utilizar elementos HTML semânticos adequados;
- manter hierarquia lógica de títulos;
- identificar regiões e agrupamentos de conteúdo de forma compreensível;
- utilizar elementos nativos antes de recorrer a ARIA;
- evitar o uso de elementos puramente visuais como substitutos de controles semânticos.

### Navegação por teclado

- todas as funcionalidades interativas devem ser acessíveis pelo teclado;
- a ordem de foco deve acompanhar uma sequência lógica;
- o foco deve permanecer visível;
- não deve existir armadilha de teclado;
- diálogos, menus e conteúdos dinâmicos devem manter comportamento previsível de foco.

### Campos de formulário

- todo campo deve possuir nome ou rótulo acessível;
- campos obrigatórios devem ser identificados de forma compreensível;
- instruções relevantes devem estar associadas ao campo correspondente;
- mensagens de erro devem identificar claramente o problema;
- erros devem estar associados programaticamente ao respectivo campo;
- estados inválidos devem ser comunicados às tecnologias assistivas quando aplicável.

### Botões, links e controles

- botões e links devem possuir nomes acessíveis que expliquem sua finalidade;
- o usuário não deve depender exclusivamente de ícones sem identificação;
- controles com a mesma aparência e função devem possuir comportamento consistente;
- elementos desabilitados ou indisponíveis devem possuir estado compreensível.

### Foco

- elementos interativos devem apresentar indicação visual de foco;
- alterações de tela ou abertura de componentes devem posicionar ou preservar o foco de forma previsível;
- o foco não deve ser movido sem necessidade ou contexto para o usuário.

### Conteúdo visual

- informação importante não deve depender exclusivamente de cor;
- textos devem possuir contraste suficiente em relação ao fundo;
- ícones e elementos gráficos relevantes devem possuir alternativa acessível quando necessário;
- imagens decorativas não devem gerar informação redundante para tecnologias assistivas.

### Mensagens e mudanças de estado

- erros, sucessos, alertas e demais mensagens importantes devem ser comunicados de forma compreensível;
- mudanças relevantes que ocorram sem recarregar a página devem ser disponibilizadas para tecnologias assistivas quando necessário;
- mensagens de erro não devem desaparecer antes que o usuário tenha oportunidade razoável de compreendê-las.

### Conteúdo e linguagem

- textos de botões, mensagens e instruções devem ser objetivos;
- mensagens de erro devem indicar o que aconteceu e, quando possível, como corrigir;
- abreviações ou termos técnicos desnecessários devem ser evitados na interface destinada ao estudante.

### Ampliação e adaptação

- a interface deve permanecer utilizável quando o conteúdo textual for ampliado;
- a ampliação não deve causar perda de informação ou funcionalidade;
- conteúdos devem se adaptar sem exigir interação exclusivamente por precisão visual.

## Verificações específicas por tipo de tela

### Formulários

Além da lista mínima geral, formulários devem verificar:

- associação entre `label` e controle;
- indicação de campos obrigatórios;
- ordem lógica de tabulação;
- associação entre erros e campos;
- preservação dos valores preenchidos quando ocorrer erro;
- comunicação acessível de sucesso ou falha.

### Listagens e resultados

Devem ser verificados:

- títulos ou identificação da listagem;
- estado vazio compreensível;
- estado de carregamento compreensível;
- mensagens de erro acessíveis;
- ações associadas a cada item com nome acessível;
- ordenação e agrupamento compreensíveis.

### Diálogos e elementos sobrepostos

Quando existirem, devem:

- receber foco de forma previsível;
- manter a navegação por teclado dentro do contexto necessário;
- permitir fechamento pelo mecanismo previsto;
- devolver o foco de forma adequada ao elemento de origem;
- possuir nome acessível.

### Mensagens de confirmação e alerta

Devem:

- informar claramente o resultado da ação;
- utilizar semântica apropriada;
- não depender exclusivamente de cor;
- ser anunciadas por tecnologias assistivas quando a alteração exigir comunicação imediata.

## Critério mínimo de aceite por tela

Uma tela pode ser considerada apta para revisão de acessibilidade quando:

- todas as funcionalidades essenciais são utilizáveis por teclado;
- a ordem de foco é lógica e previsível;
- os elementos interativos possuem nomes acessíveis;
- campos possuem identificação apropriada;
- erros são compreensíveis e associados aos controles correspondentes;
- mudanças importantes de estado são comunicadas de maneira acessível;
- a informação não depende exclusivamente de cor;
- não são encontradas barreiras evidentes que impeçam a conclusão do fluxo principal por teclado ou tecnologia assistiva.

O atendimento dessa lista mínima não substitui a avaliação dos critérios aplicáveis da WCAG 2.2 nível AA.

## Estratégia de verificação

A acessibilidade deve ser verificada por uma combinação de técnicas.

Testes automatizados podem validar propriedades como:

- existência de nomes acessíveis;
- associação entre rótulos e campos;
- atributos e estados ARIA;
- ordem de foco em fluxos conhecidos;
- mensagens de status e alerta;
- determinadas violações detectáveis automaticamente.

Entretanto, testes automatizados não comprovam sozinhos conformidade integral com a WCAG.

Aspectos como qualidade da experiência com leitor de tela, clareza da ordem de leitura, contraste visual real, comportamento de zoom e adequação semântica podem exigir revisão manual ou validação em navegador real.

## Relação com os testes existentes

O projeto já possui verificações automatizadas de acessibilidade no formulário de dados pessoais.

Essas verificações incluem:

- rótulos acessíveis;
- navegação sequencial com teclado;
- associação de mensagens de erro por `aria-invalid` e `aria-describedby`;
- remoção do estado de erro após correção;
- comunicação de sucesso por `role="status"`;
- comunicação de falha por `role="alert"`.

Esses padrões devem servir como referência para testes semelhantes nas demais telas, quando aplicáveis.

## Relação com o RNF02

Esta decisão detalha o requisito não funcional RNF02 — Acessibilidade.

O RNF02 passa a adotar:

- WCAG 2.2 como padrão de referência;
- nível AA como nível-alvo;
- a lista mínima deste documento como base obrigatória de revisão das telas.

## Limites desta decisão

Esta definição não afirma que todas as telas atuais já possuem conformidade integral com WCAG 2.2 AA.

Também não substitui:

- testes específicos de cada funcionalidade;
- avaliações manuais quando necessárias;
- testes com tecnologias assistivas;
- verificações de contraste e apresentação visual em ambiente real;
- futuras auditorias formais de acessibilidade.

## Rastreabilidade

- **Issue:** #169 — F1.2
- **Requisito relacionado:** RNF02 — Acessibilidade
- **WBS:** 1.1.1.4, 1.1.2.4, 1.2.1.4, 1.7.2.4, 1.8.2.4
