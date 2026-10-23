# Evidências — caracterização estática do CSS móvel da página de vagas

## 1. Identificação

- Card: **“Validar a página de vagas na largura móvel definida em F1.1.”**
- Análise: [v002](../../../prompts/frontend/20261021-205543-validacao-vagas-largura-movel-f11-v002.md), `status: proposed`, aprovada pela autorização explícita desta tarefa direta. As skills de implementação frontend e integração não foram invocadas.
- Branch: `test/validacao-largura-mobile`.
- HEAD: `ab2b8bc28c19bd55cacef41a4401ad9e34040276`.
- Data de execução: **21/10/2026**, fuso **America/Sao_Paulo (UTC−03:00)**.
- Baseline antes de editar: início do Vitest **21:01:07**. Suíte direcionada final: **21:12:09**; captura detalhada: **21:12:29**. Suíte completa final: **21:12:45**. Registro dos gates concluídos: **2026-10-21T21:14:56-03:00**, obtido do relógio durante a execução, não do timestamp da análise.
- Executor: Codex, tarefa direta com autorização para somente o teste novo e este documento; sem commit.
- Teste: [vagas-responsividade-css.test.ts](../../../src/frontend/app/test/vagas-responsividade-css.test.ts).
- CSS examinados: `src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.css` e `src/frontend/app/styles/global.css`. Os componentes `PaginaVagasGrupo2.tsx` e `TelaVagasGrupo2.tsx` foram lidos somente para localizar os seletores.
- Nenhuma instalação, auditoria, atualização de dependências, alteração de configuração ou chamada a serviço real foi executada.

Preflight realizado antes de editar, com Git fora do Nix:

```sh
git branch --show-current
git status --short --untracked-files=all
git log --oneline origin/dev..HEAD
git status --short -- nix flake.nix flake.lock src/frontend/package.json src/frontend/package-lock.json
```

Saídas da branch e do status inicial:

```text
test/validacao-largura-mobile
?? prompts/frontend/20261021-201727-validacao-vagas-largura-movel-f11-v001.md
?? prompts/frontend/20261021-205543-validacao-vagas-largura-movel-f11-v002.md
```

`origin/dev..HEAD` e o status dos caminhos de ambiente/manifests não produziram linhas. `src/frontend/node_modules` estava presente; não foi executado `npm ci`.

## 2. Objetivo e limites

Caracterizar **texto e estrutura do CSS atual**, em Vitest/jsdom, avaliando explicitamente as condições de mídia e a seleção das declarações em **360, 480 e 640px**, com **1rem = 16px** passado ao avaliador.

A escolha das larguras tem origem **fornecida pelo usuário** na revisão v002. A fonte é secundária: RNF03 (`docs/requisitos_nao_funcionais.md`) → análises de prévia #366/#409 → [evidência #409](f11-11-responsividade-previa.md) → matriz fornecida pelo usuário. A cadeia não estabelece uma definição primária independente: RNF03 deixa dispositivos/navegadores e matriz a aprovar, enquanto a análise #409 cita “F1.1 (RNF03)” como se os números já estivessem consolidados. Essa circularidade histórica é preservada como ressalva. A autorização atual resolve o recorte desta entrega, sem reescrever as fontes anteriores.

Os **valores esperados** vêm do CSS real, não das colunas “Layout Clássico/Compacto” da matriz. São **caracterização do que está implementado, não aceite de produto/design**. Os valores foram escritos literalmente no teste, de forma independente do avaliador.

481px aparece **somente como controle de fronteira em S0**, não como largura de F1.1. Tablet e desktop ficam fora. Altura, DPR, orientação e áreas seguras não foram definidos pela matriz e não participam deste ensaio estático.

Não foi renderizada a página repetidamente por largura. A árvore JavaScript de vagas não depende de largura no código lido; esse exercício não acrescentaria prova. Uma sonda DOM descartável é usada apenas para detectar seletores concorrentes, sem renderizar componentes de produção, medir geometria ou simular viewport.

## 3. Matriz de resultados — caracterização do CSS atual

Resultados obtidos em S1/S2 e registrados na captura detalhada. “Ativa” significa **avaliada pelo helper estático explícito**, não aplicada nativamente pelo jsdom.

| Categoria       | Entrada CSS px | Base rem px | mediaText extraída   | Limiar px | Regime                    | Grid da busca         | Grid-column do label | Padding shell / conteúdo | Resultado real             |
| --------------- | -------------: | ----------: | -------------------- | --------: | ------------------------- | --------------------- | -------------------- | ------------------------ | -------------------------- |
| Mobile Compacto |            360 |          16 | `(max-width: 30rem)` |       480 | ativa                     | `1fr`                 | `auto`               | `0.75rem` / `1.25rem`    | caracterização concordante |
| Mobile Médio    |            480 |          16 | `(max-width: 30rem)` |       480 | ativa, igualdade incluída | `1fr`                 | `auto`               | `0.75rem` / `1.25rem`    | caracterização concordante |
| Mobile Clássico |            640 |          16 | `(max-width: 30rem)` |       480 | inativa                   | `minmax(0, 1fr) auto` | `1 / -1`             | `1.5rem` / `2rem`        | caracterização concordante |

Não se reutilizou o “Aprovado” da prévia como resultado para vagas.

## 4. Comportamento declarado

Em `src/frontend/features/listar-vagas/ui/TelaVagasGrupo2.css`:

```css
.vagas-grupo2__pesquisa {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 0.5rem;
  align-items: end;
}
.vagas-grupo2__pesquisa label {
  grid-column: 1 / -1;
  font-weight: 700;
}
@media (max-width: 30rem) {
  .vagas-grupo2__pesquisa {
    grid-template-columns: 1fr;
  }
  .vagas-grupo2__pesquisa label {
    grid-column: auto;
  }
}
```

Em `src/frontend/app/styles/global.css`, os trechos relevantes de base são `.app-shell { padding: 1.5rem; }` e `.app-shell__content { padding: 2rem; }`; o bloco móvel real é:

```css
@media (max-width: 30rem) {
  .app-shell {
    padding: 0.75rem;
  }
  .app-shell__content {
    padding: 1.25rem;
  }
}
```

| Propriedade/seletor                             | Base preservada no CSSOM | Dentro da mídia 30rem |
| ----------------------------------------------- | ------------------------ | --------------------- |
| grid-template-columns / .vagas-grupo2__pesquisa | `minmax(0, 1fr) auto`    | `1fr`                 |
| grid-column / .vagas-grupo2__pesquisa label     | `1 / -1`                 | `auto`                |
| padding / .app-shell                            | `1.5rem`                 | `0.75rem`             |
| padding / .app-shell__content                   | `2rem`                   | `1.25rem`             |

Os verificadores conferem tanto a seleção por regime quanto a localização das declarações em base/mídia e a preservação das bases. O limite `max-width` é inclusivo: **480 ≤ 30 × 16**; 640 usa o padrão de vagas.

O breakpoint `40rem` pertence à prévia, em `features/visualizar-curriculo/ui/ModeloClassico.css`, conforme a inspeção registrada na v002. Não é breakpoint de vagas. As colunas Clássico/Compacto da matriz não descrevem esta página. O mínimo 320px do body e a expressão de largura `min(100%, 42rem)` do shell não foram convertidos em novas larguras de F1.1.

## 5. Evidência de execução

Todos os comandos de desenvolvimento utilizaram os ambientes Nix do projeto, **um comando por vez**, sem paralelismo entre comandos. O paralelismo interno padrão do Vitest permaneceu intacto.

A primeira tentativa de baseline no sandbox terminou antes do Vitest, com exit 1:

```text
error: opening lock file "/nix/var/nix/db/big-lock": Read-only file system
```

O comando foi repetido pelo mecanismo autorizado fora do sandbox; não houve mudança no Nix.

### Versões reais

Sondagem executada em `.#frontend`, sem instalar nada:

```sh
nix develop .#frontend --command bash -c 'node --version
npm --version
node --input-type=module -e '\''import { readFileSync } from "node:fs"; for (const nome of ["vitest", "jsdom", "typescript", "eslint", "prettier"]) { console.log(nome, JSON.parse(readFileSync("src/frontend/node_modules/" + nome + "/package.json", "utf8")).version); }'\'''
```

Saída real (exit 0):

```text
Ambiente de desenvolvimento do frontend
v24.20.0
11.19.0
vitest 5.0.1
jsdom 30.1.0
typescript 7.0.2
eslint 9.39.5
prettier 3.9.9
```

| Ferramenta | Versão observada |
| ---------- | ---------------- |
| Node       | v24.20.0         |
| npm        | 11.19.0          |
| Vitest     | 5.0.1            |
| jsdom      | 30.1.0           |
| TypeScript | 7.0.2            |
| ESLint     | 9.39.5           |
| Prettier   | 3.9.9            |

Uma sondagem auxiliar inicial presumiu um caminho interno do pacote npm e recebeu ENOENT; foi substituída pelos comandos públicos acima. Isso não alterou o baseline nem qualquer arquivo.

### Baseline antes e depois

| Verificação            | Antes                                                     | Depois                                                    | Comparação                                   |
| ---------------------- | --------------------------------------------------------- | --------------------------------------------------------- | -------------------------------------------- |
| test / frontend        | exit 0; 48 arquivos, 256 aprovados, 0 falhos, 0 ignorados | exit 0; 49 arquivos, 273 aprovados, 0 falhos, 0 ignorados | 256 antigos + 17 novos; nenhum antigo oculto |
| lint / frontend        | exit 0; nenhum diagnóstico                                | exit 0; nenhum diagnóstico                                | sem diagnóstico novo                         |
| check / frontend       | exit 0; nenhum diagnóstico                                | exit 0; nenhum diagnóstico                                | novo arquivo alcançado                       |
| lint / quality         | exit 0; nenhum diagnóstico                                | exit 0; nenhum diagnóstico                                | sem diagnóstico novo                         |
| format:check / quality | exit 0                                                    | exit 0                                                    | formatação do frontend concordante           |
| check / quality        | exit 0; nenhum diagnóstico                                | exit 0; nenhum diagnóstico                                | sem diagnóstico novo                         |

Os dois timeouts da v002 eram em `app/jornada-curriculo.e2e.test.tsx:194` (“conclui a jornada com sucesso desde o preenchimento de dados pessoais até a liberação e disparo das ações de exportação”) e `app/jornada-selecao-previa-exportacao.e2e.test.tsx:258` (“conclui criação, edição, seleção, prévia e exportação com download simulado”). **Não se reproduziram no baseline sequencial desta tarefa, nem na suíte completa final.** Não foi alterado timeout ou teste antigo. A mudança de resultado não estabelece a causa dos timeouts anteriores.

As contagens de zero ignorados decorrem de todos os casos coletados terem passado; não houve skip de recurso. Lint/check não informaram total de arquivos; não se inventou essa contagem.

### test

Comando real, executado isoladamente antes e depois:

```sh
nix develop .#frontend --command npm --prefix src/frontend test
```

Antes (exit 0):

```text
Ambiente de desenvolvimento do frontend

> sistema-curriculo@0.1.0 test
> vitest run


 RUN  v5.0.1 /home/daniel/projetos/sistema-curriculo/src/frontend


 Test Files  48 passed (48)
      Tests  256 passed (256)
   Start at  21:01:07
   Duration  42.79s (environment 53%, tests 33%, setup 7%, import 5%, transform 3%)

Environment  jsdom was created 48 times · 143.58s total, 53% of tracked time
             create it once per worker with pool: 'vmThreads' (keeps per-file isolation) or isolate: false (shares it across files)
             learn more: https://vitest.dev/guide/improving-performance#test-environments
```

Depois (exit 0):

```text
Ambiente de desenvolvimento do frontend

> sistema-curriculo@0.1.0 test
> vitest run


 RUN  v5.0.1 /home/daniel/projetos/sistema-curriculo/src/frontend


 Test Files  49 passed (49)
      Tests  273 passed (273)
   Start at  21:12:45
   Duration  39.78s (environment 52%, tests 32%, setup 7%, import 5%, transform 3%)

Environment  jsdom was created 49 times · 131.02s total, 52% of tracked time
             create it once per worker with pool: 'vmThreads' (keeps per-file isolation) or isolate: false (shares it across files)
             learn more: https://vitest.dev/guide/improving-performance#test-environments
```

### lint frontend

Comando real, executado isoladamente antes e depois:

```sh
nix develop .#frontend --command npm --prefix src/frontend run lint
```

Antes (exit 0):

```text
Ambiente de desenvolvimento do frontend

> sistema-curriculo@0.1.0 lint
> eslint .
```

Depois (exit 0):

```text
Ambiente de desenvolvimento do frontend

> sistema-curriculo@0.1.0 lint
> eslint .
```

### check frontend

Comando real, executado isoladamente antes e depois:

```sh
nix develop .#frontend --command npm --prefix src/frontend run check
```

Antes (exit 0):

```text
Ambiente de desenvolvimento do frontend

> sistema-curriculo@0.1.0 check
> tsc -b --pretty false
```

Depois (exit 0):

```text
Ambiente de desenvolvimento do frontend

> sistema-curriculo@0.1.0 check
> tsc -b --pretty false
```

### lint quality

Comando real, executado isoladamente antes e depois:

```sh
nix develop .#quality --command npm --prefix src/frontend run lint
```

Antes (exit 0):

```text
Ambiente de quality gates

> sistema-curriculo@0.1.0 lint
> eslint .
```

Depois (exit 0):

```text
Ambiente de quality gates

> sistema-curriculo@0.1.0 lint
> eslint .
```

### format:check quality

Comando real, executado isoladamente antes e depois:

```sh
nix develop .#quality --command npm --prefix src/frontend run format:check
```

Antes (exit 0):

```text
Ambiente de quality gates

> sistema-curriculo@0.1.0 format:check
> prettier --check .

Checking formatting...
All matched files use Prettier code style!
```

Depois (exit 0):

```text
Ambiente de quality gates

> sistema-curriculo@0.1.0 format:check
> prettier --check .

Checking formatting...
All matched files use Prettier code style!
```

### check quality

Comando real, executado isoladamente antes e depois:

```sh
nix develop .#quality --command npm --prefix src/frontend run check
```

Antes (exit 0):

```text
Ambiente de quality gates

> sistema-curriculo@0.1.0 check
> tsc -b --pretty false
```

Depois (exit 0):

```text
Ambiente de quality gates

> sistema-curriculo@0.1.0 check
> tsc -b --pretty false
```

### Suíte direcionada final e contagens por cenário

Comando exato solicitado:

```sh
nix develop .#frontend --command npm --prefix src/frontend test -- app/test/vagas-responsividade-css.test.ts
```

Saída real final (exit 0):

```text
Ambiente de desenvolvimento do frontend

> sistema-curriculo@0.1.0 test
> vitest run app/test/vagas-responsividade-css.test.ts


 RUN  v5.0.1 /home/daniel/projetos/sistema-curriculo/src/frontend


 Test Files  1 passed (1)
      Tests  17 passed (17)
   Start at  21:12:09
   Duration  1.82s (environment 46%, tests 43%, transform 5%, setup 5%, import 1%)
```

| Cenário                                                                                 | Executados | Aprovados | Falhos | Ignorados |
| --------------------------------------------------------------------------------------- | ---------: | --------: | -----: | --------: |
| S0 — fixture, leitura e controles de fronteira                                          |          1 |         1 |      0 |         0 |
| S0 — guardas: condição, !important, seletor, at-rule, padding parcial e lados distintos |          6 |         6 |      0 |         0 |
| S1 — CSS vagas, 360/480/640                                                             |          3 |         3 |      0 |         0 |
| S2 — CSS global, 360/480/640                                                            |          3 |         3 |      0 |         0 |
| S3 — dois mutantes por arquivo                                                          |          4 |         4 |      0 |         0 |
| Total da suíte nova                                                                     |         17 |        17 |      0 |         0 |

Para observar os diagnósticos que o reporter padrão omite em casos aprovados, foi executado adicionalmente, em sequência:

```sh
nix develop .#frontend --command npm --prefix src/frontend test -- app/test/vagas-responsividade-css.test.ts --reporter=verbose --disableConsoleIntercept
```

Exit 0: 17/17 casos aprovados, nenhum ignorado. Trechos literais dos logs dessa execução:

```text
S0 recursos {"matchMedia":"undefined","CSSStyleSheet":"function","replaceSync":"function","caminho":"CSSStyleSheet.replaceSync","importCss":"não executado: leitura direta com fs; import lateral não é prova de CSS no runner (v002, F10–F11)"}
S0 calibração F1.1 {"larguraPx":360,"baseRemPx":16,"mediaText":"(max-width: 30rem)","limiarPx":480,"ativa":true,"valores":["1rem"]}
S0 calibração F1.1: igualdade {"larguraPx":480,"baseRemPx":16,"mediaText":"(max-width: 30rem)","limiarPx":480,"ativa":true,"valores":["1rem"]}
S0 calibração F1.1 {"larguraPx":640,"baseRemPx":16,"mediaText":"(max-width: 30rem)","limiarPx":480,"ativa":false,"valores":["2rem"]}
S0 calibração controle S0; não F1.1 {"larguraPx":481,"baseRemPx":16,"mediaText":"(max-width: 30rem)","limiarPx":480,"ativa":false,"valores":["2rem"]}
S1 vagas {"larguraPx":360,"baseRemPx":16,"mediaText":"(max-width: 30rem)","limiarPx":480,"ativa":true,"valores":["1fr","auto"]}
S1 vagas {"larguraPx":480,"baseRemPx":16,"mediaText":"(max-width: 30rem)","limiarPx":480,"ativa":true,"valores":["1fr","auto"]}
S1 vagas {"larguraPx":640,"baseRemPx":16,"mediaText":"(max-width: 30rem)","limiarPx":480,"ativa":false,"valores":["minmax(0, 1fr) auto","1 / -1"]}
S3 vagas sem mídia .vagas-grupo2__pesquisa | grid-template-columns | 360px | valor selecionado: esperado 1fr, obtido minmax(0, 1fr) auto
S3 vagas sem mídia .vagas-grupo2__pesquisa | grid-template-columns | 480px | valor selecionado: esperado 1fr, obtido minmax(0, 1fr) auto
S3 vagas sem mídia original intacto e novamente concordante
S3 vagas 40rem .vagas-grupo2__pesquisa | grid-template-columns | 640px | valor selecionado: esperado minmax(0, 1fr) auto, obtido 1fr
S3 vagas 40rem original intacto e novamente concordante
S2 shell {"larguraPx":360,"baseRemPx":16,"mediaText":"(max-width: 30rem)","limiarPx":480,"ativa":true,"valores":["0.75rem","1.25rem"]}
S2 shell {"larguraPx":480,"baseRemPx":16,"mediaText":"(max-width: 30rem)","limiarPx":480,"ativa":true,"valores":["0.75rem","1.25rem"]}
S2 shell {"larguraPx":640,"baseRemPx":16,"mediaText":"(max-width: 30rem)","limiarPx":480,"ativa":false,"valores":["1.5rem","2rem"]}
S3 shell sem mídia .app-shell | padding | 360px | valor selecionado: esperado 0.75rem, obtido 1.5rem
S3 shell sem mídia .app-shell | padding | 480px | valor selecionado: esperado 0.75rem, obtido 1.5rem
S3 shell sem mídia original intacto e novamente concordante
S3 shell 40rem .app-shell | padding | 640px | valor selecionado: esperado 1.5rem, obtido 0.75rem
S3 shell 40rem original intacto e novamente concordante
```

S0 usou **CSSStyleSheet.replaceSync**. `matchMedia` estava `undefined`; o construtor e `replaceSync` estavam disponíveis como funções. O fallback `style.sheet.cssRules` ficou previsto no código, mas não foi necessário nesta execução. Não houve skip por indisponibilidade.

O import lateral de CSS **não foi executado**, conforme a proibição do método. Seu efeito não foi “medido” por uma importação proibida: a v002/F10–F11 e as configurações lidas registram ausência de `test.css` explícito e desabilitação padrão no runner. S0 registra essa restrição e testa a leitura direta dos arquivos; não apresenta parsing CSSOM como aplicação nativa de mídia. Não se mediu `getComputedStyle` por largura nem geometria.

S3 criou **quatro mutantes em memória** e observou **seis divergências esperadas**: duas larguras por arquivo sem mídia, uma por arquivo com 40rem. Parsing/extração dos mutantes ocorreram fora do catch de verificação; cada falha capturada precisou ser `FalhaVerificacao` com seletor, propriedade, largura e divergência de **valor selecionado**. Erro genérico ou de parser não satisfaz o controle. O original foi relido, comparado byte a byte e novamente verificado nas três larguras, em cada caso.

### Alcance do check e achado A6

Comando executado, exit 0:

```sh
nix develop .#frontend --command bash -c 'cd src/frontend && npm exec --offline --no -- tsc -p tsconfig.app.json --listFilesOnly --pretty false'
```

A lista real inclui:

```text
/home/daniel/projetos/sistema-curriculo/src/frontend/app/test/vagas-responsividade-css.test.ts
```

Não há entrada para `TelaVagasGrupo2.a11y.test.tsx`. A chamada com dois argumentos em suas linhas 168–171 continua existente, fora do alcance do check, e não foi corrigida. Nenhum import de produção foi adicionado ao teste CSS para expandir esse grafo.

### Ajustes realizados somente no teste novo

As verificações intermediárias detectaram problemas do próprio teste, corrigidos antes dos resultados finais acima:

- Primeiro ensaio direcionado: 16 casos, 11 falhos/5 aprovados; `new URL(...css, import.meta.url)` foi transformado pelo Vite em URL de asset, recusada pelo fs (“The URL must be of scheme file”). O construtor Node passou a ser importado como alias; a URL continua relativa ao arquivo, sem cwd.
- Ensaio seguinte: 16 casos, 6 falhos/10 aprovados; o CSSOM expande `padding` em longhands. O teste passou a reconhecer sua recomposição uniforme e acrescentou uma sexta guarda contra lados distintos, totalizando os 17 casos finais.
- Primeiro check do arquivo novo: seis diagnósticos; módulos builtin sem tipos e inferência de callbacks `it.each`. A instalação não contém `@types/node`, divergindo da suposição da v002. O ajuste ficou no próprio arquivo: duas diretivas `@ts-expect-error TS2591` estritamente nas importações builtin, assinaturas locais para leitura UTF-8/construtor URL e casos parametrizados por laços com contexto tipado pelo Vitest. Não há desativação global de tipos, alteração de configuração ou dependência nova; a fronteira builtin usa assinaturas locais, não declarações oficiais de `@types/node`. Se os tipos forem instalados no futuro, diretivas desnecessárias serão sinalizadas pelo TypeScript.

Trecho real do check intermediário, não persistente no resultado final:

```text
Ambiente de desenvolvimento do frontend

> sistema-curriculo@0.1.0 check
> tsc -b --pretty false

app/test/vagas-responsividade-css.test.ts(2,30): error TS2591: Cannot find name 'node:fs'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node` and then add 'node' to the types field in your tsconfig.
app/test/vagas-responsividade-css.test.ts(3,35): error TS2591: Cannot find name 'node:url'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node` and then add 'node' to the types field in your tsconfig.
app/test/vagas-responsividade-css.test.ts(267,31): error TS2345: Argument of type 'string' is not assignable to parameter of type 'never'.
app/test/vagas-responsividade-css.test.ts(585,51): error TS2345: Argument of type 'string' is not assignable to parameter of type 'TestContext'.
app/test/vagas-responsividade-css.test.ts(610,23): error TS2345: Argument of type 'number' is not assignable to parameter of type 'TestContext'.
app/test/vagas-responsividade-css.test.ts(621,34): error TS2345: Argument of type 'string' is not assignable to parameter of type 'TestContext'.
  Type 'string' is not assignable to type 'TestContext'.
```

Uma tentativa de formatar o arquivo com npm exec usando prefix e caminho relativo não encontrou o arquivo por causa do cwd; o comando foi corrigido para `cd src/frontend` e formatou **somente o teste novo**. Nenhum formatador foi aplicado ao repositório inteiro. Esses ajustes não modificaram critérios ou oráculos da v002.

O build do CI não foi necessário para esta fatia estática e **não foi executado**. Não se afirma que passou. Seu comando permanece `nix develop .#quality --command npm --prefix src/frontend run build`; nenhum dist novo foi gerado por esta tarefa.

### Formatação deste documento

`format:check` do CI executa Prettier com cwd em `src/frontend` e alvo `.`; **não cobre docs/**. Este documento precisa de verificação explícita:

```sh
nix develop .#quality --command bash -c 'cd src/frontend && npm exec --offline --no -- prettier --check ../../docs/testes/evidencias/f11-vagas-responsividade-movel.md'
```

Resultado observado: **exit 0**, após formatar somente este documento novo. A primeira verificação havia retornado exit 1 com aviso de estilo; nenhuma alteração foi aplicada ao documento da #409.

Saída real da verificação após a formatação:

```text
Ambiente de quality gates
Checking formatting...
All matched files use Prettier code style!
```

## 6. O que a evidência permite afirmar

**As regras responsivas declaradas no CSS de vagas estão presentes e se aplicam no regime esperado para 360, 480 e 640px, conforme avaliadas em jsdom por um avaliador estático explícito, com 1rem = 16px.**

Foi verificada a **estrutura do CSS atual e a seleção das declarações**, não a aplicação nativa da media query pelo jsdom. A palavra “regime” designa a avaliação aritmética explícita da condição extraída do CSSOM. A suíte mostrou sensibilidade a remoção/alteração do bloco e preservação do original.

## 7. O que a evidência NÃO permite afirmar

Esta suíte **não prova**:

- ausência de overflow;
- ausência de corte ou sobreposição;
- “layout validado a 360px”;
- “aprovado em dispositivo móvel”;
- tamanho ou usabilidade dos alvos de toque;
- legibilidade;
- viewport móvel renderizado;
- aprovação completa de RNF03.

Não foram mockados `getBoundingClientRect`, `scrollWidth`, `clientWidth` ou `matchMedia`; não há wrapper com overflow escondido. Também não se usaram métricas geométricas zeradas do jsdom como aprovação.

O seguimento em navegador real precisará de viewport efetivo medido, página/CSS reais, dados e rede isolados, oráculos de design para scroll/corte/sobreposição/toque e controles de sensibilidade. Poderá provar essas propriedades **nas condições de ambiente ensaiadas**, sem provar automaticamente todos os aparelhos ou legibilidade humana. Nenhum recurso de browser é pré-requisito desta entrega concluída de caracterização.

## 8. Divergências e riscos

| Referência da v002 | Registro nesta execução                                                                                                                                                                                  |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D1                 | A análise #409 declara incerteza baixa e nenhuma pergunta, mas RNF03 deixa matriz/dispositivos a definir. Não corrigido                                                                                  |
| D2                 | #409 chama faixa 360–480 de Mobile Compacto; a matriz fornecida separa 480 como Mobile Médio. Os nomes recebidos foram usados, sem converter nomes em regra CSS                                          |
| D3                 | A tabela da prévia atribui transição para flex em 480, mas max-width 30rem é inclusivo; “supera 30rem” é a descrição coerente para sair desse regime. As colunas dos modelos não foram aplicadas a vagas |
| D4                 | Propriedades como overflow-wrap não comprovam ausência de overflow. O teste atual limita sua alegação a declarações                                                                                      |
| D5                 | Workflow lido não executa npm test do frontend, apesar da declaração de execução contínua no relatório #409. Não alterado                                                                                |
| D6                 | “Aprovado” da prévia não foi reutilizado para vagas                                                                                                                                                      |
| D7                 | A6 continua fora do check e não corrigido                                                                                                                                                                |
| D8                 | docs/ continua fora de format:check do CI. A reprovação do documento #409 no check explícito foi registrada na v002; não foi repetida nem corrigida aqui                                                 |
| D9                 | Timeouts históricos da v002 não se reproduziram antes nem depois na execução sequencial atual; nenhuma causa foi estabelecida                                                                            |

Aviso de depreciação do ESLint 9.39.5 e **9 vulnerabilidades (2 moderadas, 6 altas, 1 crítica)** são informações **fornecidas pelo usuário e não verificadas** nesta tarefa. A versão instalada do ESLint foi observada; a depreciação e os advisories não foram auditados. Não foi executado `npm audit fix`, nem `npm audit`.

O avaliador é deliberadamente restrito: max-width em rem/px, base explícita, declarações selecionadas por ordem de origem e regras equivalentes. Não implementa cascata CSS geral, validação completa de toda sintaxe CSS, nesting, especificidade arbitrária ou cálculo de layout. Recusa prioridades, seletores concorrentes, shorthands não modelados e at-rules desconhecidas; essa política conservadora pode exigir revisão se a linguagem do CSS evoluir. Não enfraquecer o teste trocando esperado por dado derivado do próprio CSS.

O import local de tokens do global é reconhecido e retirado da cópia analisada; não se segue @import nem se busca recurso. O texto original em disco é preservado. As sondas de seletores não substituem uma página em navegador. Fallback CSSOM não necessário nesta sessão permanece sem exercício dinâmico.

## 9. Conclusão e preservação

**Caracterização estática concluída:** S0–S3 passaram integralmente, com **17 casos aprovados, 0 falhos e 0 ignorados**. A suíte completa final passou com **273/273**, preservando os **256 casos anteriores**. Os cinco gates de lint/tipos/formatação passaram em sequência, sem diagnóstico novo persistente.

Não há bloqueio técnico pendente para essa caracterização. Permanecem como seguimentos: prova geométrica/visual em browser com oráculos de design, origem normativa primária da matriz, A6/alcance de tipos, CI de testes frontend/formatação docs e triagem separada dos avisos de dependências. Esses itens não foram corrigidos nem declarados validados.

A execução direta e os dois arquivos novos respeitam a autorização específica de L9. As adaptações de URL, tipos locais e serialização CSSOM são ajustes do método dentro do arquivo autorizado; não mudam o escopo ou os valores de referência. A inexistência de @types/node e a ausência de medição de import lateral foram registradas explicitamente, em vez de perpetuar a suposição da análise.

Hashes Git de conteúdo, iguais antes e depois das execuções:

```text
12105bca4a783d65b2b28361c58b7ed087168f17  v001
7e5784115eaea60197e2942a03a26271a6a65749  v002
79b9e41a1f79a90d07d83f6f32d50289fc807905  TelaVagasGrupo2.css
910354e7e7ef317ff2bfc0619d9c43f221ebfad9  global.css
```

`git status --short -- nix flake.nix flake.lock src/frontend/package.json src/frontend/package-lock.json` permaneceu vazio nas verificações antes e depois. **Nenhuma alteração temporária de ambiente**: não houve diff a restaurar nem git restore. Não houve commit ou stage. Somente o teste novo e este documento foram criados no repositório, além das duas análises já existentes e preservadas.

Logs brutos desta sessão: `/tmp/sistema-curriculo-vagas-css-execucao.log`, fora do repositório. Caches habituais sob node_modules são ignorados por `src/frontend/.gitignore`; nenhum relatório bruto, dependência, captura ou cache foi adicionado ao commit.
