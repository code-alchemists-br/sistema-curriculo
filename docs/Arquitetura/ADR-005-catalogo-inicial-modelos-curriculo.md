# ADR-004 — Catálogo inicial de modelos de currículo

- Status: Proposto
- Data: 2026-10-26

## Contexto

O sistema já possui uma prévia estruturada independente de layout. A ADR-003
determina que um novo modelo precisa de identificador centralizado, componente
de apresentação, prévia/exportação capaz de compreendê-lo e testes. A criação
de versão ainda recebia `layout` como texto livre, ao passo que a edição já
usava `ModeloCurriculo`.

Os documentos `docs/modelos_curriculo.md` e
`docs/adequacao_semantica_ia.md` definem que o modelo altera somente a ordem,
visibilidade e apresentação das mesmas informações. A recomendação pelo
objetivo é uma orientação inicial: ela não pode restringir a escolha da pessoa
estudante nem acionar IA.

## Decisão proposta

Reconhecer os seguintes identificadores estáveis no catálogo central:

| Identificador      | Rótulo público        | Papel                                                                                    |
| ------------------ | --------------------- | ---------------------------------------------------------------------------------------- |
| `classico`         | Profissional clássico | Modelo já existente.                                                                     |
| `compacto`         | Compacto              | Mantido por compatibilidade e disponível no seletor; não recebe recomendação automática. |
| `ats-simples`      | ATS simples           | Coluna única textual, sem barras de nível ou elementos gráficos decorativos.             |
| `moderno`          | Moderno               | Modelo visual já previsto no catálogo.                                                   |
| `criativo`         | Criativo              | Modelo visual já previsto no catálogo.                                                   |
| `academico`        | Acadêmico             | Prioriza formação, projetos e documentos disponíveis.                                    |
| `primeiro-emprego` | Primeiro emprego      | Prioriza formação, projetos, competências e idiomas antes da experiência.                |

A API de criação passa a validar `layout` com a mesma enumeração da edição e
entrega o valor textual ao caso de uso. O construtor de domínio permanece
permissivo ao carregar versões históricas, conforme a compatibilidade prevista
na ADR-003.

## Regras de apresentação

- Nenhum modelo cria, infere ou modifica dados da prévia.
- Seções sem itens são omitidas; os campos opcionais continuam opcionais.
- O modelo acadêmico não cria resumo, título profissional, publicações, linhas
  de pesquisa, docência ou projetos que não existam no contrato atual.
- O modelo de primeiro emprego não inventa experiência profissional: apenas a
  desloca para depois das evidências disponíveis.
- O modelo ATS simples mantém leitura linear, sem duas colunas, gráficos,
  barras de nível ou conteúdo escondido apenas por interação visual.
- A recomendação por objetivo não bloqueia nenhum dos sete modelos reconhecidos.
- A seleção de modelo não envia dados à IA nem prepara integração automática
  com IA.

## Consequências

O frontend e o backend passam a compartilhar o mesmo vocabulário, e o OpenAPI
documenta os valores aceitos. A exportação futura deve mapear esses mesmos
identificadores, sem alterar o contrato `PreviaCurriculo`. A aprovação deste
ADR é necessária antes de considerar o catálogo uma decisão arquitetural final.
