# Relatório de Evidência e Roteiro de Teste: Legibilidade em Tela Larga para Modelos de Currículo (F5.12)

- **Issue:** [#220](https://github.com/code-alchemists-br/sistema-curriculo/issues/220) — `[F5.12] Criar teste visual/manual de legibilidade em tela larga para cada modelo.`
- **Requisitos Vinculados:** RF06 (Layouts profissionais), RNF03 (Adaptação desktop/móvel) e RNF07 (Qualidade e legibilidade da apresentação)
- **Análise Decisória de Origem:** `prompts/frontend/20261026-081230-legibilidade-modelos-tela-larga-v001.md`
- **Responsável:** Gustavo Minoru Haga (`@minoruhaga`)
- **Data de Execução:** 26/10/2026

---

## 1. Objetivo da Avaliação

Comprovar, através de testes automatizados unitários de componente e procedimento de inspeção visual/manual, que os modelos de currículo do sistema (`ModeloClassico` e `ModeloCompacto`) mantêm alta ergonomia de leitura, densidade tipográfica adequada e perfeita organização estrutural quando visualizados em resoluções de tela larga (≥ 1024px e 1280px+), conforme especificado em F1.1 (`docs/compatibilidade-responsividade.md`).

---

## 2. Matriz de Resoluções de Tela Larga (F1.1)

| Resolução Alvo | Categoria F1.1     | Dimensões de Teste | Densidade / Ratio | Objetivo de Legibilidade                                |
| -------------- | ------------------ | ------------------ | ----------------- | ------------------------------------------------------- |
| **1024px**     | Desktop Padrão     | 1024 × 768 px      | 1.0x (100%)       | Transição fluida do tablet para layout desktop completo |
| **1280px**     | Desktop Amplo      | 1280 × 800 px      | 1.0x (100%)       | Medida de linha contida em folha centralizada           |
| **1920px**     | Full HD Widescreen | 1920 × 1080 px     | 1.0x (100%)       | Blindagem contra dispersão lateral de texto             |

---

## 3. Checklist de Critérios de Legibilidade em Tela Larga

| ID      | Critério de Legibilidade                 | Comportamento Esperado no Modelo Clássico                                                           | Comportamento Esperado no Modelo Compacto                                                |    Status    |
| ------- | ---------------------------------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | :----------: |
| **C01** | **Contenção de Largura Máxima**          | Delimitado em `max-width: 52rem` (~832px) com `margin: 0 auto`.                                     | Delimitado em `max-width: 56rem` (~896px) com `margin: 0 auto`.                          | **Aprovado** |
| **C02** | **Comprimento Ergonômico de Linha**      | Medida de leitura entre 55 e 80 caracteres por linha nos parágrafos descritivos.                    | Medida densa e ágil sem linhas esticadas desnecessariamente.                             | **Aprovado** |
| **C03** | **Alinhamento Bi-Coluna de Cabeçalhos**  | Título do item (cargo/curso) à esquerda e período à direita via flexbox com `space-between`.        | Cabeçalho e metadados estruturados verticalmente com período em destaque sutil.          | **Aprovado** |
| **C04** | **Multi-coluna em Competências/Idiomas** | Grid responsivo de duas ou mais colunas (`repeat(auto-fill, minmax(14rem, 1fr))`).                  | Listas compactas com disposição inline e marcadores sutis.                               | **Aprovado** |
| **C05** | **Formatação de Contatos e Links**       | Contatos em linha horizontal com separadores de ponto central (`•`) e quebra segura.                | Contatos horizontais compactos com links acessíveis e legíveis.                          | **Aprovado** |
| **C06** | **Hierarquia e Contraste Tipográfico**   | Contraste de texto escuro (`#111827`, `#1f2937`) sobre fundo branco (`#ffffff`), atendendo WCAG AA. | Títulos em azul escuro (`#1e3a8a`) sobre fundo branco com peso tipográfico diferenciado. | **Aprovado** |
| **C07** | **Ausência de Overflow ou Cortes**       | Barra de rolagem horizontal ausente (`overflow-x: hidden`), margens e paddings simétricos.          | Zero transbordamento lateral ou sobreposição de blocos.                                  | **Aprovado** |

---

## 4. Procedimento Operacional de Teste Visual/Manual

1. **Inicialização do Ambiente:**
   ```bash
   nix develop .#frontend --command bash -c "cd src/frontend && npm run dev"
   ```
2. **Navegação:**
   Acessar a página de prévia de currículo (`/visualizar-curriculo` ou módulo de seleção de modelo).
3. **Configuração da Ferramenta de Inspeção (DevTools):**
   - Abrir o Google Chrome ou Firefox e acionar `F12` / `Ctrl+Shift+I`.
   - Ativar o modo de emulação de dispositivos responsivos (`Ctrl+Shift+M`).
   - Definir a resolução para **1024 × 768 px** (Desktop Padrão).
   - Alternar entre **Modelo Clássico** e **Modelo Compacto**.
   - Conferir os itens C01 a C07 do checklist.
   - Alterar a resolução para **1280 × 800 px** e posteriormente **1920 × 1080 px**.
   - Inspecionar a contenção central (`margin: 0 auto`) e o conforto da leitura em tela cheia.
4. **Critério de Aceite Visual:**
   - Nenhum bloco de texto deve se espalhar por toda a tela de 1920px.
   - O alinhamento dos períodos de experiência e formação deve coincidir visualmente com a margem direita da folha no Modelo Clássico.

---

## 5. Cobertura de Teste Automatizado

A conformidade contínua no pipeline de CI é garantida pela suíte de componentes:
`src/frontend/features/visualizar-curriculo/ui/PreviaCurriculo.legibilidade-larga.test.tsx`

### Testes Executados:

1. `Modelo Clássico` — Contenção de largura e integridade em 1024px (Desktop Padrão).
2. `Modelo Clássico` — Contenção de largura e integridade em 1280px (Desktop Amplo).
3. `Modelo Clássico` — Contenção de largura e integridade em 1920px (Full HD).
4. `Modelo Clássico` — Alinhamento de cabeçalhos bi-coluna com `space-between` para itens de formação e experiência.
5. `Modelo Clássico` — Distribuição de competências e idiomas em grade multi-colunas.
6. `Modelo Clássico` — Apresentação horizontal com separadores de contato.
7. `Modelo Compacto` — Contenção de largura e densidade tipográfica em 1024px.
8. `Modelo Compacto` — Contenção de largura e densidade tipográfica em 1280px.
9. `Modelo Compacto` — Contenção de largura e densidade tipográfica em 1920px.
10. `Modelo Compacto` — Disposição inline de listas secundárias com alta legibilidade.
11. `Modelo Compacto` — Escaneabilidade e hierarquia de títulos h2.

---

## 6. Comandos de Validação Local no Ambiente Nix

```bash
# Execução da suíte de legibilidade em tela larga
nix develop .#frontend --command bash -c "cd src/frontend && npx vitest run features/visualizar-curriculo/ui/PreviaCurriculo.legibilidade-larga.test.tsx"

# Verificação estática de tipos
nix develop .#frontend --command bash -c "cd src/frontend && npm run check"

# Verificação de formatação e linter
nix develop .#quality --command bash -c "cd src/frontend && npm run format:check && npm run lint"
```

---

## 7. Conclusão e Veredito

Ambos os modelos de currículo (`ModeloClassico` e `ModeloCompacto`) foram rigorosamente testados e comprovados para visualização em telas largas (1024px, 1280px e 1920px+). A contenção geométrica de largura, o alinhamento de datas, o espaçamento generoso e a alta densidade de leitura cumprem plenamente os requisitos RF06, RNF03 e RNF07.

**Veredito:** **APROVADO** sem ressalvas.
