# Adequação semântica com inteligência artificial

## Objetivo

Definir como a assistência de inteligência artificial deve adaptar um currículo
ao cargo-alvo ou à vaga sem enviar dados desnecessários ao modelo. A abordagem
deve reduzir custo, tempo de resposta e exposição de dados pessoais, mantendo o
estudante no controle do conteúdo final.

## Papel da IA

A IA é uma assistência opcional de escrita e personalização. Ela pode sugerir
melhorias de texto, palavras-chave, destaque de competências e organização de
itens, mas não altera o currículo automaticamente. O estudante deve poder
revisar, aceitar, editar ou descartar cada sugestão.

A adequação semântica considera principalmente o cargo-alvo e, quando
fornecida, a descrição da vaga. A categoria do perfil serve apenas como
orientação inicial de layout e ordem de seções.

## Preparação de contexto

Antes de invocar um modelo de IA, o sistema deve montar um contexto específico
para a ação solicitada. O currículo completo não deve ser enviado por padrão.

```text
Currículo completo salvo
        ↓
Estudante escolhe uma ação de IA
        ↓
Sistema seleciona apenas os dados necessários
        ↓
Aplica limites por campo e orçamento total
        ↓
Envia o contexto reduzido para a IA
```

### Contexto por ação

| Ação solicitada | Dados que podem ser enviados |
| --- | --- |
| Melhorar uma experiência | Empresa, cargo, descrição da experiência e cargo-alvo opcional. |
| Adequar o currículo a uma vaga | Cargo-alvo, descrição da vaga, competências e experiências/projetos selecionados como relevantes. |
| Gerar resumo profissional | Formação, experiências recentes, competências e objetivo profissional. |

Dados que não contribuem para a ação, como telefones, endereço, documentos ou
outros itens não relacionados, devem ser omitidos do contexto enviado.

## Limites recomendados

Os limites abaixo equilibram espaço suficiente para conteúdo profissional e
controle previsível de custo.

| Campo | Limite recomendado |
| --- | ---: |
| Empresa | 120 caracteres |
| Cargo | 120 caracteres |
| Descrição de experiência | 1.000 caracteres |
| Descrição de competência | 100 caracteres |
| Nível de competência | 50 caracteres |
| Descrição da vaga | 6.000 caracteres |

Além dos limites individuais, cada requisição de IA deve respeitar um orçamento
agregado de, no máximo, 10.000 caracteres, aproximadamente 2.500 tokens. O
limite definitivo pode ser ajustado após medir a qualidade das sugestões e o
custo do modelo adotado.

## Priorização de itens

Quando o contexto ultrapassar o orçamento agregado, o sistema deve reduzir os
itens enviados de forma determinística e compreensível:

1. Incluir os itens explicitamente selecionados pelo estudante.
2. Priorizar experiências mais recentes.
3. Incluir projetos mais relacionados ao cargo ou à vaga.
4. Limitar competências às mais relevantes.
5. Omitir os demais itens daquela solicitação, sem removê-los do currículo.

Como referência inicial, uma análise pode conter até três experiências, três
projetos e dez competências, desde que respeite o orçamento total.

A interface deve informar os itens utilizados. Exemplo: "A análise usou as
três experiências mais recentes. Selecione outras experiências para incluí-las."

## Privacidade e controle

O envio de dados a um provedor externo de IA deve depender do consentimento
explícito do estudante. O sistema deve informar quais conteúdos serão enviados
e não deve incluir credenciais, telefones, endereço ou documentos sem uma
justificativa direta para a ação solicitada.
