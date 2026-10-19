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

Os limites abaixo são os valores-padrão da política de contexto. Eles
equilibram espaço suficiente para conteúdo profissional e controle previsível
de custo, mas não devem ficar fixos no código nem depender de valores enviados
pela interface.

| Campo | Chave de configuração | Valor-padrão |
| --- | --- | ---: |
| Empresa | `limites_campos.empresa` | 120 caracteres |
| Cargo | `limites_campos.cargo` | 120 caracteres |
| Descrição de experiência | `limites_campos.descricao_experiencia` | 1.000 caracteres |
| Descrição de competência | `limites_campos.descricao_competencia` | 100 caracteres |
| Nível de competência | `limites_campos.nivel_competencia` | 50 caracteres |
| Descrição da vaga | `limites_campos.descricao_vaga` | 6.000 caracteres |

Além dos limites individuais, cada requisição de IA deve respeitar um orçamento
agregado configurável, com valor-padrão de 10.000 caracteres, aproximadamente
2.500 tokens. O orçamento é identificado por `orcamento_total_caracteres`.

### Política configurável

A configuração deve ser mantida no servidor, versionada e aplicada antes de
montar o contexto. Ela pode definir valores globais e substituições específicas
por ação solicitada ou por modelo de IA. A ordem de resolução é:

1. limite específico da combinação ação e modelo;
2. limite específico da ação;
3. limite específico do modelo;
4. valor-padrão global.

No backend, a política fica exclusivamente no arquivo
`src/backend/config/limites_contexto_ia.json`. Não há endpoint para alterá-la.
O processo consulta a assinatura do arquivo antes de obter a política: uma
versão válida substitui a política em uso na próxima requisição, sem reiniciar
a aplicação. Se o arquivo estiver temporariamente inválido durante a edição, o
backend mantém a última versão válida e registra o erro até que uma nova versão
válida seja publicada.

Por exemplo, uma política pode manter o orçamento global em 10.000 caracteres
e reduzir `orcamento_total_caracteres` para 6.000 ao adequar o currículo a uma
vaga em um modelo de menor capacidade. As substituições devem indicar somente
os valores que diferem do padrão.

Os limites efetivos usados em cada requisição devem ser registrados junto da
versão da política e do identificador do modelo. Isso permite comparar custo e
qualidade das sugestões, ajustar os valores com evidência e reproduzir o
comportamento posteriormente.

O estudante não pode aumentar esses valores pelo cliente. A configuração deve
aceitar apenas números inteiros positivos e continuar sujeita a tetos de
segurança definidos no mesmo arquivo e validados pelo serviço. O total
efetivamente enviado nunca pode ultrapassar o menor valor entre o orçamento
resolvido e o teto de segurança.
Uma alteração de política deve ser revisada e publicada pelo responsável
técnico, sem exigir nova implantação quando o mecanismo de configuração já
estiver disponível.

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
