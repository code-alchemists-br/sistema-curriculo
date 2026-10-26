# Relatório de Evidência: Validação do PDF Gerado e Registro de Falhas por Página (F11.12)

- **Issue:** [#410](https://github.com/code-alchemists-br/sistema-curriculo/issues/410) — `[F11.12] Validar PDF gerado contra o roteiro de legibilidade de F1.5 e registrar falhas por página.`
- **Requisitos Vinculados:** RF09 (Exportação de currículo), RNF07 (Qualidade e legibilidade da exportação) e F1.5 (Critérios de aceite e validação de exportação)
- **Análise Decisória de Origem:** `prompts/backend/20261026-082930-validacao-pdf-paginacao-v001.md`
- **Responsável:** Gustavo Minoru Haga (`@minoruhaga`)
- **Data de Execução:** 26/10/2026

---

## 1. Objetivo da Avaliação

Realizar a auditoria estrutural e visual detalhada, página por página, do arquivo PDF gerado pelo sistema (`RenderizadorDocumentoCurriculoPdf`) através da rota HTTP de download da API (`GET /estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/pdf`), catalogando sistematicamente a ausência de cortes, sobreposições, títulos órfãos e registrando quaisquer falhas encontradas por página.

---

## 2. Padrões Geométricos e Parâmetros de Diagramação (F1.5)

| Parâmetro                | Padrão Esperado (ISO / A4) | Modelo Clássico                 | Modelo Compacto                 |
| ------------------------ | -------------------------- | ------------------------------- | ------------------------------- |
| **Padrão de Página**     | ISO 216 / A4               | A4 (`595.27 × 841.89 pt`)       | A4 (`595.27 × 841.89 pt`)       |
| **Margens de Página**    | Simétricas                 | `2.0 cm` (56.7 pt)              | `1.5 cm` (42.5 pt)              |
| **Tipografia Base**      | Família Neutra Legível     | Helvetica 10.5 pt               | Helvetica 9.0 pt                |
| **Espaçamento de Linha** | Proporcional               | `leading = base * 1.3`          | `leading = base * 1.3`          |
| **Prevenção de Órfãos**  | Agrupamento de Cabeçalho   | `KeepTogether([Título, Bloco])` | `KeepTogether([Título, Bloco])` |

---

## 3. Catálogo de Auditoria e Registro de Falhas por Página

### 3.1 Cenário A — Currículo Padrão (1 Página)

| Página     | Elemento Auditado           | Critério de Aceite F1.5                                                                    | Comportamento Aferido                                          |                    Falhas Detectadas                    |
| ---------- | --------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------- | :-----------------------------------------------------: |
| **Pág. 1** | **Cabeçalho Principal**     | Nome do estudante em destaque no topo com estilo Title (`fontSize: 21 pt`, cor `#1F3A5F`). | Renderizado perfeitamente no topo com hierarquia clara.        |                     **Nenhuma (0)**                     |
| **Pág. 1** | **Linha de Contatos**       | E-mail, telefones, endereço e links com separador `                                        | `.                                                             | Contatos limpos em linha única sem quebras indesejadas. | **Nenhuma (0)** |
| **Pág. 1** | **Formação Acadêmica**      | Título de seção destacado seguido de curso, instituição e datas.                           | Diagramação equilibrada, subtítulo e período em itálico.       |                     **Nenhuma (0)**                     |
| **Pág. 1** | **Histórico Profissional**  | Cargo, empresa, período e descrição das atribuições.                                       | Texto descritivo justificado/alinhado com espaçamento regular. |                     **Nenhuma (0)**                     |
| **Pág. 1** | **Projetos e Competências** | Títulos dos projetos e lista de competências técnicas.                                     | Distribuição vertical limpa e espaçamento proporcional.        |                     **Nenhuma (0)**                     |
| **Pág. 1** | **Final da Página**         | Ausência de linhas cortadas ou encavaladas no rodapé.                                      | Margem inferior de 2.0 cm respeitada com folga.                |                     **Nenhuma (0)**                     |

_Total de falhas no Cenário A (Página 1):_ **0 falhas**.

---

### 3.2 Cenário B — Currículo Extenso (2 Páginas)

| Página     | Elemento Auditado             | Critério de Aceite F1.5                                                                                | Comportamento Aferido                                                                                     | Falhas Detectadas |
| ---------- | ----------------------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- | :---------------: |
| **Pág. 1** | **Cabeçalho e Contatos**      | Nome e canais de contato no topo da primeira folha.                                                    | Presença integral e legível sem compressão.                                                               |  **Nenhuma (0)**  |
| **Pág. 1** | **Formações e Experiências**  | Blocos iniciais de histórico acadêmico e profissional.                                                 | Renderização contínua e sequencial.                                                                       |  **Nenhuma (0)**  |
| **Pág. 1** | **Rodapé e Transição**        | Uma seção NÃO pode deixar seu título órfão no rodapé da Página 1 se seus blocos estiverem na Página 2. | O `KeepTogether` transpôs a seção inteira ("Idiomas") para o topo da Página 2, eliminando títulos órfãos. |  **Nenhuma (0)**  |
| **Pág. 2** | **Topo da Segunda Página**    | Início com título de seção e seu respectivo bloco ou continuação limpa.                                | A seção "Idiomas" inicia a Página 2 com o título e itens agregados.                                       |  **Nenhuma (0)**  |
| **Pág. 2** | **Documentos Complementares** | Exibição do nome amigável do certificado/diploma.                                                      | Nome amigável apresentado sem revelar URLs privadas.                                                      |  **Nenhuma (0)**  |
| **Pág. 2** | **Rodapé da Segunda Página**  | Ausência de vazamento de storage ou dados sensíveis.                                                   | Margem inferior preservada, metadados limpos.                                                             |  **Nenhuma (0)**  |

_Total de falhas no Cenário B:_

- **Página 1:** **0 falhas**.
- **Página 2:** **0 falhas**.

---

## 4. Testes de Integração Automatizados (CI)

A conformidade com a paginação e legibilidade do PDF é verificada no pipeline de CI através de:
`src/backend/tests/test_integracao_validacao_pdf_legibilidade.py`

### Casos de Teste Executados:

1. `test_geometria_a4_e_abertura_do_pdf_com_leitor_externo`: Valida assinatura `%PDF-`, abertura via `pypdf` e dimensões exatas A4 (`595.27 × 841.89 pt`).
2. `test_auditoria_de_legibilidade_por_pagina_modelo_classico`: Audita texto e cabeçalhos da Página 1 no modelo clássico.
3. `test_auditoria_de_paginacao_em_curriculo_extenso_sem_titulos_orfaos`: Audita a quebra para a Página 2, garantindo que `KeepTogether` previna títulos isolados.
4. `test_modelo_compacto_mantem_mesmo_texto_com_alta_densidade_e_margens_menores`: Comprova 100% de equivalência textual entre os modelos clássico e compacto com margens de 1.5 cm.
5. `test_higienizacao_de_metadados_e_omissao_de_caminhos_privados`: Audita os metadados do documento e a ausência absoluta de URLs confidenciais de storage.

---

## 5. Comandos de Validação Local no Ambiente Nix

```bash
# Execução da suíte de integração de validação de PDF
nix develop .#tests --command bash -c "PYTHONPATH=src python3 -m unittest src/backend/tests/test_integracao_validacao_pdf_legibilidade.py"

# Verificação de qualidade de código
nix develop .#quality --command bash -c "ruff check src/backend/tests/test_integracao_validacao_pdf_legibilidade.py && ruff format --check src/backend/tests/test_integracao_validacao_pdf_legibilidade.py"
```

---

## 6. Conclusão e Veredito

O arquivo PDF exportado atende integralmente a todas as exigências de legibilidade, proporção, geometria e paginação estabelecidas por F1.5 e RNF07. Não foram observadas quebras órfãs, sobreposições de blocos ou cortes de texto em nenhuma página avaliada.

**Veredito:** **APROVADO** com **0 falhas por página**.
