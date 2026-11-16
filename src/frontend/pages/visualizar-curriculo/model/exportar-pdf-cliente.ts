import { jsPDF } from "jspdf";
import type {
  DocumentoPreviaCurriculo,
  PreviaCurriculo,
} from "../../../entities/curriculo";
import type { ModeloApresentacaoCurriculo } from "../../../features/alternar-modelo-curriculo";

export interface OpcoesExportacaoPdf {
  elemento?: HTMLElement | null;
  previa?: PreviaCurriculo;
  nomeArquivo?: string;
}

const LARGURA_PAGINA = 210;
const ALTURA_PAGINA = 297;
const MARGEM_INFERIOR = 18;

/** Formata datas ISO (YYYY-MM-DD) para o padrão brasileiro DD/MM/AAAA, preservando outros formatos. */
export function formatarDataPdf(data?: string | null): string {
  if (!data) return "";
  const limpo = data.trim();
  if (/^\d{4}-\d{2}-\d{2}$/.test(limpo)) {
    try {
      return new Intl.DateTimeFormat("pt-BR", { timeZone: "UTC" }).format(
        new Date(`${limpo}T00:00:00Z`),
      );
    } catch {
      return limpo;
    }
  }
  return limpo;
}

/** Formata o intervalo de datas de acordo com a convenção de cada modelo. */
export function formatarPeriodoPdf(
  inicio: string,
  fim: string | null,
  usarTracoQuandoAtual = false,
): string {
  const iniFormatado = formatarDataPdf(inicio);
  const fimFormatado = fim
    ? formatarDataPdf(fim)
    : usarTracoQuandoAtual
      ? "—"
      : "Atual";
  return `${iniFormatado} — ${fimFormatado}`;
}

/** Formata um documento complementar exibindo o tipo/emissor entre parênteses. */
export function formatarDocumentoPdf(
  documento: DocumentoPreviaCurriculo,
): string {
  return documento.tipo_arquivo
    ? `${documento.nome_arquivo} (${documento.tipo_arquivo})`
    : documento.nome_arquivo;
}

/** Preenche um retângulo colorido com segurança mesmo em ambientes de teste com mocks parciais. */
function preencherRetangulo(
  doc: jsPDF,
  x: number,
  y: number,
  largura: number,
  altura: number,
  r: number,
  g: number,
  b: number,
): void {
  const docAny = doc as unknown as {
    setFillColor?: (r: number, g: number, b: number) => void;
    rect?: (x: number, y: number, w: number, h: number, style?: string) => void;
  };
  docAny.setFillColor?.(r, g, b);
  docAny.rect?.(x, y, largura, altura, "F");
}

/** Calcula a largura aproximada de um texto em mm para sublinhados curtos (inline-block). */
function medirLarguraTextoMm(
  doc: jsPDF,
  texto: string,
  tamanhoFontePt: number,
): number {
  const docAny = doc as unknown as {
    getTextWidth?: (t: string) => number;
  };
  if (typeof docAny.getTextWidth === "function") {
    const largura = docAny.getTextWidth(texto);
    if (typeof largura === "number" && largura > 0) {
      return largura;
    }
  }
  return Math.max(18, texto.length * tamanhoFontePt * 0.21);
}

/** Extrai a lista de contatos na mesma ordem exibida pelos componentes de prévia. */
function obterItensContato(
  previa: PreviaCurriculo,
  mostrarUrlCompletaLinks = false,
): string[] {
  const { estudante } = previa;
  const contato = estudante?.contato;
  const itens: string[] = [];

  if (estudante?.email?.trim()) {
    itens.push(estudante.email.trim());
  }
  if (contato?.telefones) {
    for (const tel of contato.telefones) {
      if (tel && tel.trim()) {
        itens.push(tel.trim());
      }
    }
  }
  if (contato?.endereco?.trim()) {
    itens.push(contato.endereco.trim());
  }
  if (contato?.linkedin?.trim()) {
    itens.push(
      mostrarUrlCompletaLinks
        ? contato.linkedin.trim()
        : `LinkedIn: ${contato.linkedin.trim()}`,
    );
  }
  if (contato?.curriculo_lattes?.trim()) {
    itens.push(
      mostrarUrlCompletaLinks
        ? contato.curriculo_lattes.trim()
        : `Currículo Lattes: ${contato.curriculo_lattes.trim()}`,
    );
  }
  return itens;
}

// ============================================================================
// 1. MODELO PROFISSIONAL CLÁSSICO
// ============================================================================
function renderizarModeloClassico(doc: jsPDF, previa: PreviaCurriculo): void {
  const margemX = 20;
  const larguraUtil = LARGURA_PAGINA - margemX * 2;
  let y = 22;

  const verificarQuebra = (espaco: number) => {
    if (y + espaco > ALTURA_PAGINA - MARGEM_INFERIOR) {
      doc.addPage();
      y = 20;
    }
  };

  // Cabeçalho centralizado em maiúsculas
  const nome = (previa.estudante?.nome || "Currículo").trim().toUpperCase();
  doc.setFont("helvetica", "bold");
  doc.setFontSize(18);
  doc.setTextColor(17, 24, 39); // #111827
  doc.text(nome, LARGURA_PAGINA / 2, y, { align: "center" });
  y += 6;

  const contatos = obterItensContato(previa).join(" • ");
  if (contatos) {
    doc.setFont("helvetica", "normal");
    doc.setFontSize(9);
    doc.setTextColor(71, 85, 105); // #475569
    const linhasContato = doc.splitTextToSize(contatos, larguraUtil);
    for (const linha of linhasContato) {
      verificarQuebra(4.5);
      doc.text(linha, LARGURA_PAGINA / 2, y, { align: "center" });
      y += 4.5;
    }
  }

  y += 1.5;
  doc.setDrawColor(17, 24, 39); // #111827
  doc.setLineWidth(0.6);
  doc.line(margemX, y, LARGURA_PAGINA - margemX, y);
  y += 7;

  const adicionarTituloSecao = (titulo: string) => {
    verificarQuebra(15);
    y += 2;
    doc.setFont("helvetica", "bold");
    doc.setFontSize(10.5);
    doc.setTextColor(17, 24, 39); // #111827
    doc.text(titulo.toUpperCase(), margemX, y);
    y += 1.8;
    doc.setDrawColor(203, 213, 225); // #cbd5e1
    doc.setLineWidth(0.45);
    doc.line(margemX, y, LARGURA_PAGINA - margemX, y);
    y += 5.5;
  };

  // 1. Formação acadêmica
  if (previa.formacoes.length > 0) {
    adicionarTituloSecao("Formação acadêmica");
    for (const f of previa.formacoes) {
      verificarQuebra(12);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(15, 23, 42); // #0f172a
      doc.text(f.curso, margemX, y);

      const periodo = formatarPeriodoPdf(f.inicio, f.fim);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(8.5);
      doc.setTextColor(100, 116, 139); // #64748b
      doc.text(periodo, LARGURA_PAGINA - margemX, y, { align: "right" });
      y += 4.5;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      doc.setTextColor(51, 65, 85); // #334155
      doc.text(`${f.instituicao} • ${f.nivel} — ${f.status}`, margemX, y);
      y += 5.5;
    }
  }

  // 2. Experiência profissional
  if (previa.experiencias.length > 0) {
    adicionarTituloSecao("Experiência profissional");
    for (const e of previa.experiencias) {
      verificarQuebra(14);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(15, 23, 42);
      doc.text(e.cargo, margemX, y);

      const periodo = formatarPeriodoPdf(e.inicio, e.fim);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(8.5);
      doc.setTextColor(100, 116, 139);
      doc.text(periodo, LARGURA_PAGINA - margemX, y, { align: "right" });
      y += 4.5;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      doc.setTextColor(51, 65, 85);
      doc.text(e.empresa, margemX, y);
      y += 4.5;

      if (e.descricao) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9);
        doc.setTextColor(55, 65, 81); // #374151
        const linhas = doc.splitTextToSize(e.descricao, larguraUtil);
        for (const linha of linhas) {
          verificarQuebra(4.5);
          doc.text(linha, margemX, y);
          y += 4.2;
        }
      }
      y += 2.5;
    }
  }

  // 3. Projetos acadêmicos
  if (previa.projetos.length > 0) {
    adicionarTituloSecao("Projetos acadêmicos");
    for (const p of previa.projetos) {
      verificarQuebra(12);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(15, 23, 42);
      doc.text(p.titulo, margemX, y);
      y += 4.5;

      if (p.descricao) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9);
        doc.setTextColor(55, 65, 81);
        const linhas = doc.splitTextToSize(p.descricao, larguraUtil);
        for (const linha of linhas) {
          verificarQuebra(4.5);
          doc.text(linha, margemX, y);
          y += 4.2;
        }
      }
      if (p.tecnologias) {
        verificarQuebra(4.5);
        doc.setFont("helvetica", "bold");
        doc.setFontSize(8.5);
        doc.setTextColor(71, 85, 105);
        doc.text(`Tecnologias: ${p.tecnologias}`, margemX, y);
        y += 4.5;
      }
      y += 2;
    }
  }

  // 4. Competências (grade de 3 colunas como no ModeloClassico.css)
  if (previa.competencias.length > 0) {
    adicionarTituloSecao("Competências");
    const larguraColuna = larguraUtil / 3;
    for (let i = 0; i < previa.competencias.length; i += 3) {
      verificarQuebra(5.5);
      const fatia = previa.competencias.slice(i, i + 3);
      fatia.forEach((c, idx) => {
        const xCol = margemX + idx * larguraColuna;
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9);
        doc.setTextColor(31, 41, 55);
        const textoItem = c.nivel ? `${c.descricao} (${c.nivel})` : c.descricao;
        const linhas = doc.splitTextToSize(textoItem, larguraColuna - 4);
        doc.text(linhas[0] || textoItem, xCol, y);
      });
      y += 5;
    }
    y += 1.5;
  }

  // 5. Idiomas (grade de 3 colunas)
  if (previa.idiomas.length > 0) {
    adicionarTituloSecao("Idiomas");
    const larguraColuna = larguraUtil / 3;
    for (let i = 0; i < previa.idiomas.length; i += 3) {
      verificarQuebra(5.5);
      const fatia = previa.idiomas.slice(i, i + 3);
      fatia.forEach((idioma, idx) => {
        const xCol = margemX + idx * larguraColuna;
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9);
        doc.setTextColor(31, 41, 55);
        const textoItem = idioma.nivel
          ? `${idioma.idioma} — ${idioma.nivel}`
          : idioma.idioma;
        doc.text(textoItem, xCol, y);
      });
      y += 5;
    }
    y += 1.5;
  }

  // 6. Documentos complementares
  if (previa.documentos.length > 0) {
    adicionarTituloSecao("Documentos complementares");
    for (const d of previa.documentos) {
      verificarQuebra(5);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      doc.setTextColor(51, 65, 85);
      const linhas = doc.splitTextToSize(formatarDocumentoPdf(d), larguraUtil);
      for (const linha of linhas) {
        doc.text(linha, margemX, y);
        y += 4.5;
      }
    }
  }
}

// ============================================================================
// 2. MODELO COMPACTO
// ============================================================================
function renderizarModeloCompacto(doc: jsPDF, previa: PreviaCurriculo): void {
  const margemX = 16;
  const larguraUtil = LARGURA_PAGINA - margemX * 2;
  let y = 18;

  const verificarQuebra = (espaco: number) => {
    if (y + espaco > ALTURA_PAGINA - 15) {
      doc.addPage();
      y = 16;
    }
  };

  // Cabeçalho alinhado à esquerda, sem uppercase, borda azul #2563eb
  const nome = (previa.estudante?.nome || "Currículo").trim();
  doc.setFont("helvetica", "bold");
  doc.setFontSize(17);
  doc.setTextColor(31, 41, 55); // #1f2937
  doc.text(nome, margemX, y);
  y += 5;

  const contatos = obterItensContato(previa, true).join(" • ");
  if (contatos) {
    doc.setFont("helvetica", "normal");
    doc.setFontSize(8.5);
    doc.setTextColor(71, 85, 105);
    const linhasContato = doc.splitTextToSize(contatos, larguraUtil);
    for (const linha of linhasContato) {
      verificarQuebra(4);
      doc.text(linha, margemX, y);
      y += 4;
    }
  }

  y += 1.5;
  doc.setDrawColor(37, 99, 235); // #2563eb
  doc.setLineWidth(0.65);
  doc.line(margemX, y, LARGURA_PAGINA - margemX, y);
  y += 5.5;

  // Títulos de seção em #1e3a8a, sem uppercase e sem linha divisória
  const adicionarTituloSecaoCompacto = (titulo: string) => {
    verificarQuebra(11);
    y += 1.5;
    doc.setFont("helvetica", "bold");
    doc.setFontSize(10.5);
    doc.setTextColor(30, 58, 138); // #1e3a8a
    doc.text(titulo, margemX, y);
    y += 4.5;
  };

  // 1. Formação acadêmica
  if (previa.formacoes.length > 0) {
    adicionarTituloSecaoCompacto("Formação acadêmica");
    for (const f of previa.formacoes) {
      verificarQuebra(12);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(9.5);
      doc.setTextColor(31, 41, 55);
      doc.text(f.curso, margemX, y);
      y += 3.8;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(8.5);
      doc.setTextColor(71, 85, 105);
      doc.text(f.instituicao, margemX, y);
      y += 3.6;

      doc.text(`${f.nivel} · ${f.status}`, margemX, y);
      y += 3.6;

      doc.text(formatarPeriodoPdf(f.inicio, f.fim, true), margemX, y);
      y += 4.8;
    }
  }

  // 2. Experiência profissional
  if (previa.experiencias.length > 0) {
    adicionarTituloSecaoCompacto("Experiência profissional");
    for (const e of previa.experiencias) {
      verificarQuebra(13);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(9.5);
      doc.setTextColor(31, 41, 55);
      doc.text(e.cargo, margemX, y);
      y += 3.8;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(8.5);
      doc.setTextColor(71, 85, 105);
      doc.text(e.empresa, margemX, y);
      y += 3.6;

      doc.text(formatarPeriodoPdf(e.inicio, e.fim, true), margemX, y);
      y += 3.8;

      if (e.descricao) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9);
        doc.setTextColor(31, 41, 55);
        const linhas = doc.splitTextToSize(e.descricao, larguraUtil);
        for (const linha of linhas) {
          verificarQuebra(4);
          doc.text(linha, margemX, y);
          y += 3.8;
        }
      }
      y += 2;
    }
  }

  // 3. Projetos acadêmicos
  if (previa.projetos.length > 0) {
    adicionarTituloSecaoCompacto("Projetos acadêmicos");
    for (const p of previa.projetos) {
      verificarQuebra(11);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(9.5);
      doc.setTextColor(31, 41, 55);
      doc.text(p.titulo, margemX, y);
      y += 3.8;

      if (p.descricao) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9);
        doc.setTextColor(31, 41, 55);
        const linhas = doc.splitTextToSize(p.descricao, larguraUtil);
        for (const linha of linhas) {
          verificarQuebra(4);
          doc.text(linha, margemX, y);
          y += 3.8;
        }
      }
      if (p.tecnologias) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8.5);
        doc.setTextColor(71, 85, 105);
        doc.text(p.tecnologias, margemX, y);
        y += 4;
      }
      y += 1.5;
    }
  }

  // 4. Competências (inline separado por •)
  if (previa.competencias.length > 0) {
    adicionarTituloSecaoCompacto("Competências");
    const textoCompetencias = previa.competencias
      .map((c) => (c.nivel ? `${c.descricao} — ${c.nivel}` : c.descricao))
      .join("  •  ");
    doc.setFont("helvetica", "normal");
    doc.setFontSize(9);
    doc.setTextColor(31, 41, 55);
    const linhas = doc.splitTextToSize(textoCompetencias, larguraUtil);
    for (const linha of linhas) {
      verificarQuebra(4.2);
      doc.text(linha, margemX, y);
      y += 4;
    }
    y += 1.5;
  }

  // 5. Idiomas (inline separado por •)
  if (previa.idiomas.length > 0) {
    adicionarTituloSecaoCompacto("Idiomas");
    const textoIdiomas = previa.idiomas
      .map((i) => (i.nivel ? `${i.idioma} — ${i.nivel}` : i.idioma))
      .join("  •  ");
    doc.setFont("helvetica", "normal");
    doc.setFontSize(9);
    doc.setTextColor(31, 41, 55);
    const linhas = doc.splitTextToSize(textoIdiomas, larguraUtil);
    for (const linha of linhas) {
      verificarQuebra(4.2);
      doc.text(linha, margemX, y);
      y += 4;
    }
    y += 1.5;
  }

  // 6. Documentos complementares (inline separado por •)
  if (previa.documentos.length > 0) {
    adicionarTituloSecaoCompacto("Documentos complementares");
    const textoDocs = previa.documentos
      .map((d) => formatarDocumentoPdf(d))
      .join("  •  ");
    doc.setFont("helvetica", "normal");
    doc.setFontSize(9);
    doc.setTextColor(31, 41, 55);
    const linhas = doc.splitTextToSize(textoDocs, larguraUtil);
    for (const linha of linhas) {
      verificarQuebra(4.2);
      doc.text(linha, margemX, y);
      y += 4;
    }
  }
}

// ============================================================================
// 3. MODELO ATS SIMPLES
// ============================================================================
function renderizarModeloAtsSimples(doc: jsPDF, previa: PreviaCurriculo): void {
  const margemX = 22;
  const larguraUtil = LARGURA_PAGINA - margemX * 2;
  let y = 24;

  const verificarQuebra = (espaco: number) => {
    if (y + espaco > ALTURA_PAGINA - MARGEM_INFERIOR) {
      doc.addPage();
      y = 22;
    }
  };

  // Cabeçalho linear à esquerda em azul #397bd1 e texto #29435d
  const nome = (previa.estudante?.nome || "Currículo").trim();
  doc.setFont("helvetica", "bold");
  doc.setFontSize(20);
  doc.setTextColor(57, 123, 209); // #397bd1
  doc.text(nome, margemX, y);
  y += 5.5;

  if (previa.titulo_versao) {
    doc.setFont("helvetica", "bold");
    doc.setFontSize(10);
    doc.setTextColor(41, 67, 93); // #29435d
    doc.text(previa.titulo_versao, margemX, y);
    y += 5;
  }

  const contatos = obterItensContato(previa).join("   ");
  if (contatos) {
    doc.setFont("helvetica", "normal");
    doc.setFontSize(8.8);
    doc.setTextColor(41, 67, 93);
    const linhasContato = doc.splitTextToSize(contatos, larguraUtil);
    for (const linha of linhasContato) {
      verificarQuebra(4.2);
      doc.text(linha, margemX, y);
      y += 4.2;
    }
  }

  y += 2;
  doc.setDrawColor(185, 204, 229); // #b9cce5
  doc.setLineWidth(0.5);
  doc.line(margemX, y, LARGURA_PAGINA - margemX, y);
  y += 7;

  // Títulos em maiúsculas azul #397bd1 sem linha divisória
  const adicionarTituloSecaoAts = (titulo: string) => {
    verificarQuebra(14);
    y += 2;
    doc.setFont("helvetica", "bold");
    doc.setFontSize(10.5);
    doc.setTextColor(57, 123, 209); // #397bd1
    doc.text(titulo.toUpperCase(), margemX, y);
    y += 5.5;
  };

  // 1. Experiência profissional (PRIMEIRA seção no ATS simples!)
  if (previa.experiencias.length > 0) {
    adicionarTituloSecaoAts("Experiência profissional");
    for (const e of previa.experiencias) {
      verificarQuebra(14);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(41, 67, 93);
      doc.text(e.cargo, margemX, y);
      y += 4.5;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9.2);
      doc.setTextColor(41, 67, 93);
      doc.text(
        `${e.empresa} · ${formatarPeriodoPdf(e.inicio, e.fim)}`,
        margemX,
        y,
      );
      y += 4.5;

      if (e.descricao) {
        const linhas = doc.splitTextToSize(e.descricao, larguraUtil);
        for (const linha of linhas) {
          verificarQuebra(4.5);
          doc.text(linha, margemX, y);
          y += 4.2;
        }
      }
      y += 3;
    }
  }

  // 2. Formação acadêmica
  if (previa.formacoes.length > 0) {
    adicionarTituloSecaoAts("Formação acadêmica");
    for (const f of previa.formacoes) {
      verificarQuebra(13);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(41, 67, 93);
      doc.text(f.curso, margemX, y);
      y += 4.5;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9.2);
      doc.setTextColor(41, 67, 93);
      doc.text(`${f.instituicao} · ${f.nivel} · ${f.status}`, margemX, y);
      y += 4.2;

      doc.text(formatarPeriodoPdf(f.inicio, f.fim), margemX, y);
      y += 5.5;
    }
  }

  // 3. Projetos acadêmicos
  if (previa.projetos.length > 0) {
    adicionarTituloSecaoAts("Projetos acadêmicos");
    for (const p of previa.projetos) {
      verificarQuebra(12);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(41, 67, 93);
      doc.text(p.titulo, margemX, y);
      y += 4.5;

      if (p.descricao) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9.2);
        doc.setTextColor(41, 67, 93);
        const linhas = doc.splitTextToSize(p.descricao, larguraUtil);
        for (const linha of linhas) {
          verificarQuebra(4.5);
          doc.text(linha, margemX, y);
          y += 4.2;
        }
      }
      if (p.tecnologias) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9);
        doc.setTextColor(41, 67, 93);
        doc.text(`Tecnologias: ${p.tecnologias}`, margemX, y);
        y += 4.5;
      }
      y += 2.5;
    }
  }

  // 4. Competências (lista textual inline)
  if (previa.competencias.length > 0) {
    adicionarTituloSecaoAts("Competências");
    const texto = previa.competencias
      .map((c) => (c.nivel ? `${c.descricao} — ${c.nivel}` : c.descricao))
      .join("    ");
    doc.setFont("helvetica", "normal");
    doc.setFontSize(9.2);
    doc.setTextColor(41, 67, 93);
    const linhas = doc.splitTextToSize(texto, larguraUtil);
    for (const linha of linhas) {
      verificarQuebra(4.5);
      doc.text(linha, margemX, y);
      y += 4.2;
    }
    y += 2.5;
  }

  // 5. Idiomas (lista textual inline)
  if (previa.idiomas.length > 0) {
    adicionarTituloSecaoAts("Idiomas");
    const texto = previa.idiomas
      .map((i) => (i.nivel ? `${i.idioma} — ${i.nivel}` : i.idioma))
      .join("    ");
    doc.setFont("helvetica", "normal");
    doc.setFontSize(9.2);
    doc.setTextColor(41, 67, 93);
    const linhas = doc.splitTextToSize(texto, larguraUtil);
    for (const linha of linhas) {
      verificarQuebra(4.5);
      doc.text(linha, margemX, y);
      y += 4.2;
    }
    y += 2.5;
  }

  // 6. Documentos complementares
  if (previa.documentos.length > 0) {
    adicionarTituloSecaoAts("Documentos complementares");
    const texto = previa.documentos
      .map((d) => formatarDocumentoPdf(d))
      .join("    ");
    doc.setFont("helvetica", "normal");
    doc.setFontSize(9.2);
    doc.setTextColor(41, 67, 93);
    const linhas = doc.splitTextToSize(texto, larguraUtil);
    for (const linha of linhas) {
      verificarQuebra(4.5);
      doc.text(linha, margemX, y);
      y += 4.2;
    }
  }
}

// ============================================================================
// 4. MODELO CRIATIVO (LATERAL VERDE ESMERALDA #075647 + COLUNA DE DATA)
// ============================================================================
function renderizarModeloCriativo(doc: jsPDF, previa: PreviaCurriculo): void {
  const larguraLateral = 61; // ~29% de 210mm
  const margemLateralX = 7.5;
  const larguraDisponivelLateral = larguraLateral - margemLateralX * 2;

  const margemConteudoX = larguraLateral + 12; // 73mm
  const larguraColunaData = 24;
  const xConteudoItem = margemConteudoX + larguraColunaData; // 97mm
  const larguraConteudoItem = LARGURA_PAGINA - xConteudoItem - 14; // 99mm
  const larguraConteudoTotal = LARGURA_PAGINA - margemConteudoX - 14;

  let yLateral = 22;
  let yPrincipal = 22;

  const desenharFundoLateral = () => {
    preencherRetangulo(doc, 0, 0, larguraLateral, ALTURA_PAGINA, 7, 86, 71);
  };

  desenharFundoLateral();

  // Cabeçalho na lateral (Georgia/Times bold branco centralizado)
  doc.setFont("times", "bold");
  doc.setFontSize(17);
  doc.setTextColor(255, 255, 255);
  const linhasNome = doc.splitTextToSize(
    (previa.estudante?.nome || "Currículo").trim(),
    larguraDisponivelLateral,
  );
  for (const l of linhasNome) {
    doc.text(l, larguraLateral / 2, yLateral, { align: "center" });
    yLateral += 6.2;
  }

  doc.setFont("helvetica", "bold");
  doc.setFontSize(7.5);
  doc.setTextColor(168, 221, 208); // #a8ddd0
  const linhasVersao = doc.splitTextToSize(
    (previa.titulo_versao || "CURRÍCULO").toUpperCase(),
    larguraDisponivelLateral,
  );
  for (const l of linhasVersao) {
    doc.text(l, larguraLateral / 2, yLateral, { align: "center" });
    yLateral += 3.8;
  }
  yLateral += 7;

  // Lateral 1: Dados de contato
  const contatos = obterItensContato(previa);
  if (contatos.length > 0) {
    doc.setFont("times", "bold");
    doc.setFontSize(10.5);
    doc.setTextColor(255, 255, 255);
    doc.text("Dados de contato", margemLateralX, yLateral);
    yLateral += 5;

    doc.setFont("helvetica", "normal");
    doc.setFontSize(8.2);
    doc.setTextColor(255, 255, 255);
    for (const item of contatos) {
      const linhas = doc.splitTextToSize(item, larguraDisponivelLateral);
      for (const linha of linhas) {
        doc.text(linha, margemLateralX, yLateral);
        yLateral += 4;
      }
      yLateral += 1.2;
    }
    yLateral += 5;
  }

  // Lateral 2: Competências (com linha inferior #a8ddd0 em cada item)
  if (previa.competencias.length > 0) {
    doc.setFont("times", "bold");
    doc.setFontSize(10.5);
    doc.setTextColor(255, 255, 255);
    doc.text("Competências", margemLateralX, yLateral);
    yLateral += 5;

    for (const c of previa.competencias) {
      doc.setFont("helvetica", "bold");
      doc.setFontSize(8.5);
      doc.setTextColor(255, 255, 255);
      const linhasDesc = doc.splitTextToSize(
        c.descricao,
        larguraDisponivelLateral,
      );
      for (const l of linhasDesc) {
        doc.text(l, margemLateralX, yLateral);
        yLateral += 3.8;
      }
      if (c.nivel) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(7.8);
        doc.setTextColor(168, 221, 208);
        doc.text(c.nivel, margemLateralX, yLateral);
        yLateral += 2.5;
      }
      doc.setDrawColor(168, 221, 208);
      doc.setLineWidth(0.35);
      doc.line(
        margemLateralX,
        yLateral,
        larguraLateral - margemLateralX,
        yLateral,
      );
      yLateral += 4.5;
    }
    yLateral += 3;
  }

  // Lateral 3: Idiomas (com linha inferior #a8ddd0 em cada item)
  if (previa.idiomas.length > 0) {
    doc.setFont("times", "bold");
    doc.setFontSize(10.5);
    doc.setTextColor(255, 255, 255);
    doc.text("Idiomas", margemLateralX, yLateral);
    yLateral += 5;

    for (const i of previa.idiomas) {
      doc.setFont("helvetica", "bold");
      doc.setFontSize(8.5);
      doc.setTextColor(255, 255, 255);
      doc.text(i.idioma, margemLateralX, yLateral);
      yLateral += 3.8;
      if (i.nivel) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(7.8);
        doc.setTextColor(168, 221, 208);
        doc.text(i.nivel, margemLateralX, yLateral);
        yLateral += 2.5;
      }
      doc.setDrawColor(168, 221, 208);
      doc.setLineWidth(0.35);
      doc.line(
        margemLateralX,
        yLateral,
        larguraLateral - margemLateralX,
        yLateral,
      );
      yLateral += 4.5;
    }
  }

  // Coluna principal à direita
  const verificarQuebraPrincipal = (espaco: number) => {
    if (yPrincipal + espaco > ALTURA_PAGINA - MARGEM_INFERIOR) {
      doc.addPage();
      desenharFundoLateral();
      yPrincipal = 22;
    }
  };

  // No ModeloCriativo.css, cada seção tem border-top: 0.1rem solid #075647 ACIMA do h2
  const adicionarTituloSecaoCriativo = (titulo: string) => {
    verificarQuebraPrincipal(16);
    doc.setDrawColor(7, 86, 71); // #075647
    doc.setLineWidth(0.4);
    doc.line(margemConteudoX, yPrincipal, LARGURA_PAGINA - 14, yPrincipal);
    yPrincipal += 6;

    doc.setFont("times", "bold");
    doc.setFontSize(13);
    doc.setTextColor(30, 41, 59); // #1e293b
    doc.text(titulo, margemConteudoX, yPrincipal);
    yPrincipal += 6.5;
  };

  // 1. Projetos acadêmicos (recuado em xConteudoItem como no ModeloCriativo.css)
  if (previa.projetos.length > 0) {
    adicionarTituloSecaoCriativo("Projetos acadêmicos");
    for (const p of previa.projetos) {
      verificarQuebraPrincipal(13);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(9.5);
      doc.setTextColor(30, 41, 59);
      doc.text(p.titulo, xConteudoItem, yPrincipal);
      yPrincipal += 4.5;

      if (p.descricao) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8.8);
        doc.setTextColor(30, 41, 59);
        const linhas = doc.splitTextToSize(p.descricao, larguraConteudoItem);
        for (const l of linhas) {
          verificarQuebraPrincipal(4.2);
          doc.text(l, xConteudoItem, yPrincipal);
          yPrincipal += 4.2;
        }
      }
      if (p.tecnologias) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8.5);
        doc.setTextColor(82, 96, 109);
        const linhasTec = doc.splitTextToSize(
          `Tecnologias: ${p.tecnologias}`,
          larguraConteudoItem,
        );
        for (const l of linhasTec) {
          verificarQuebraPrincipal(4.2);
          doc.text(l, xConteudoItem, yPrincipal);
          yPrincipal += 4.2;
        }
      }
      yPrincipal += 3;
    }
    yPrincipal += 2;
  }

  // 2. Experiência profissional (período na subcoluna esquerda, conteúdo em xConteudoItem)
  if (previa.experiencias.length > 0) {
    adicionarTituloSecaoCriativo("Experiência profissional");
    for (const e of previa.experiencias) {
      verificarQuebraPrincipal(15);
      const yTopoItem = yPrincipal;

      // Período na coluna esquerda
      const periodo = formatarPeriodoPdf(e.inicio, e.fim);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(7.8);
      doc.setTextColor(82, 96, 109); // #52606d
      const linhasPeriodo = doc.splitTextToSize(periodo, larguraColunaData - 3);
      let yPeriodo = yTopoItem;
      for (const lp of linhasPeriodo) {
        doc.text(lp, margemConteudoX, yPeriodo);
        yPeriodo += 3.6;
      }

      // Cargo, empresa e descrição na subcoluna direita
      doc.setFont("helvetica", "bold");
      doc.setFontSize(9.5);
      doc.setTextColor(30, 41, 59);
      doc.text(e.cargo, xConteudoItem, yPrincipal);
      yPrincipal += 4.5;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      doc.setTextColor(30, 41, 59);
      doc.text(e.empresa, xConteudoItem, yPrincipal);
      yPrincipal += 4.5;

      if (e.descricao) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8.8);
        doc.setTextColor(30, 41, 59);
        const linhas = doc.splitTextToSize(e.descricao, larguraConteudoItem);
        for (const l of linhas) {
          verificarQuebraPrincipal(4.2);
          doc.text(l, xConteudoItem, yPrincipal);
          yPrincipal += 4.2;
        }
      }
      yPrincipal = Math.max(yPrincipal, yPeriodo) + 3;
    }
    yPrincipal += 2;
  }

  // 3. Formação acadêmica (período na subcoluna esquerda, conteúdo em xConteudoItem)
  if (previa.formacoes.length > 0) {
    adicionarTituloSecaoCriativo("Formação acadêmica");
    for (const f of previa.formacoes) {
      verificarQuebraPrincipal(14);
      const yTopoItem = yPrincipal;

      const periodo = formatarPeriodoPdf(f.inicio, f.fim);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(7.8);
      doc.setTextColor(82, 96, 109);
      const linhasPeriodo = doc.splitTextToSize(periodo, larguraColunaData - 3);
      let yPeriodo = yTopoItem;
      for (const lp of linhasPeriodo) {
        doc.text(lp, margemConteudoX, yPeriodo);
        yPeriodo += 3.6;
      }

      doc.setFont("helvetica", "bold");
      doc.setFontSize(9.5);
      doc.setTextColor(30, 41, 59);
      doc.text(f.curso, xConteudoItem, yPrincipal);
      yPrincipal += 4.5;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(8.8);
      doc.setTextColor(30, 41, 59);
      doc.text(f.instituicao, xConteudoItem, yPrincipal);
      yPrincipal += 4.2;

      doc.text(`${f.nivel} · ${f.status}`, xConteudoItem, yPrincipal);
      yPrincipal += 4.5;

      yPrincipal = Math.max(yPrincipal, yPeriodo) + 2.5;
    }
    yPrincipal += 2;
  }

  // 4. Documentos complementares
  if (previa.documentos.length > 0) {
    adicionarTituloSecaoCriativo("Documentos complementares");
    for (const d of previa.documentos) {
      verificarQuebraPrincipal(5);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      doc.setTextColor(30, 41, 59);
      const linhas = doc.splitTextToSize(
        formatarDocumentoPdf(d),
        larguraConteudoTotal,
      );
      for (const l of linhas) {
        doc.text(l, margemConteudoX, yPrincipal);
        yPrincipal += 4.5;
      }
    }
  }
}

// ============================================================================
// 5. MODELO MODERNO (CABEÇALHO LARGO + 2 COLUNAS COM DIVISOR VERTICAL)
// ============================================================================
function renderizarModeloModerno(doc: jsPDF, previa: PreviaCurriculo): void {
  const margemX = 20;
  let yCabecalho = 24;

  // Cabeçalho largo no topo (Nome em maiúsculas grande + titulo_versao)
  const nome = (previa.estudante?.nome || "Currículo").trim().toUpperCase();
  doc.setFont("helvetica", "bold");
  doc.setFontSize(23);
  doc.setTextColor(22, 24, 29); // #16181d
  doc.text(nome, margemX, yCabecalho);
  yCabecalho += 6.5;

  if (previa.titulo_versao) {
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.setTextColor(94, 102, 114); // #5e6672
    doc.text(previa.titulo_versao, margemX, yCabecalho);
    yCabecalho += 5.5;
  }

  yCabecalho += 2;
  doc.setDrawColor(213, 217, 223); // #d5d9df
  doc.setLineWidth(0.45);
  doc.line(margemX, yCabecalho, LARGURA_PAGINA - margemX, yCabecalho);

  const yInicioColunas = yCabecalho + 8;
  let yLateral = yInicioColunas;
  let yPrincipal = yInicioColunas;

  const larguraLateral = 44; // 20mm a 64mm
  const xDivisorVertical = margemX + larguraLateral + 6; // 70mm
  const xPrincipal = xDivisorVertical + 8; // 78mm
  const larguraPrincipal = LARGURA_PAGINA - margemX - xPrincipal; // 112mm

  // Título com sublinhado curto na largura do texto (inline-block border-bottom #16181d)
  const desenharTituloModerno = (
    titulo: string,
    x: number,
    yAtual: number,
  ): number => {
    const textoUpper = titulo.toUpperCase();
    doc.setFont("helvetica", "bold");
    doc.setFontSize(9.5);
    doc.setTextColor(22, 24, 29); // #16181d
    doc.text(textoUpper, x, yAtual);
    const larguraLinha = medirLarguraTextoMm(doc, textoUpper, 9.5);
    doc.setDrawColor(22, 24, 29);
    doc.setLineWidth(0.6);
    doc.line(x, yAtual + 1.5, x + larguraLinha, yAtual + 1.5);
    return yAtual + 6.5;
  };

  // COLUNA LATERAL ESQUERDA: Informações, Competências, Idiomas
  const contatos = obterItensContato(previa);
  if (contatos.length > 0) {
    yLateral = desenharTituloModerno("Informações", margemX, yLateral);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(8.2);
    doc.setTextColor(22, 24, 29);
    for (const item of contatos) {
      const linhas = doc.splitTextToSize(item, larguraLateral);
      for (const l of linhas) {
        doc.text(l, margemX, yLateral);
        yLateral += 3.8;
      }
      yLateral += 1.4;
    }
    yLateral += 5;
  }

  if (previa.competencias.length > 0) {
    yLateral = desenharTituloModerno("Competências", margemX, yLateral);
    for (const c of previa.competencias) {
      doc.setFont("helvetica", "bold");
      doc.setFontSize(8.5);
      doc.setTextColor(22, 24, 29);
      const linhas = doc.splitTextToSize(c.descricao, larguraLateral);
      for (const l of linhas) {
        doc.text(l, margemX, yLateral);
        yLateral += 3.8;
      }
      if (c.nivel) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8);
        doc.setTextColor(94, 102, 114);
        doc.text(c.nivel, margemX, yLateral);
        yLateral += 2.5;
      }
      doc.setDrawColor(27, 29, 33); // #1b1d21
      doc.setLineWidth(0.45);
      doc.line(margemX, yLateral, margemX + larguraLateral, yLateral);
      yLateral += 4.5;
    }
    yLateral += 4;
  }

  if (previa.idiomas.length > 0) {
    yLateral = desenharTituloModerno("Idiomas", margemX, yLateral);
    for (const i of previa.idiomas) {
      doc.setFont("helvetica", "bold");
      doc.setFontSize(8.5);
      doc.setTextColor(22, 24, 29);
      doc.text(i.idioma, margemX, yLateral);
      yLateral += 3.8;
      if (i.nivel) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8);
        doc.setTextColor(94, 102, 114);
        doc.text(i.nivel, margemX, yLateral);
        yLateral += 2.5;
      }
      doc.setDrawColor(27, 29, 33);
      doc.setLineWidth(0.45);
      doc.line(margemX, yLateral, margemX + larguraLateral, yLateral);
      yLateral += 4.5;
    }
  }

  // COLUNA PRINCIPAL DIREITA: Experiência -> Projetos -> Formação -> Documentos
  const verificarQuebraPrincipal = (espaco: number) => {
    if (yPrincipal + espaco > ALTURA_PAGINA - MARGEM_INFERIOR) {
      doc.setDrawColor(213, 217, 223);
      doc.setLineWidth(0.35);
      doc.line(
        xDivisorVertical,
        yInicioColunas - 2,
        xDivisorVertical,
        Math.max(yLateral, yPrincipal),
      );
      doc.addPage();
      yPrincipal = 22;
      yLateral = 22;
    }
  };

  const desenharDivisorSecaoPrincipal = () => {
    yPrincipal += 2;
    doc.setDrawColor(213, 217, 223); // #d5d9df
    doc.setLineWidth(0.3);
    doc.line(xPrincipal, yPrincipal, LARGURA_PAGINA - margemX, yPrincipal);
    yPrincipal += 6;
  };

  // 1. Experiência profissional
  if (previa.experiencias.length > 0) {
    verificarQuebraPrincipal(16);
    yPrincipal = desenharTituloModerno(
      "Experiência profissional",
      xPrincipal,
      yPrincipal,
    );
    for (const e of previa.experiencias) {
      verificarQuebraPrincipal(14);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(22, 24, 29);
      doc.text(e.cargo, xPrincipal, yPrincipal);

      const periodo = formatarPeriodoPdf(e.inicio, e.fim);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(8);
      doc.setTextColor(94, 102, 114);
      doc.text(periodo, LARGURA_PAGINA - margemX, yPrincipal, {
        align: "right",
      });
      yPrincipal += 4.5;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      doc.setTextColor(22, 24, 29);
      doc.text(e.empresa, xPrincipal, yPrincipal);
      yPrincipal += 4.5;

      if (e.descricao) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8.8);
        doc.setTextColor(22, 24, 29);
        const linhas = doc.splitTextToSize(e.descricao, larguraPrincipal);
        for (const l of linhas) {
          verificarQuebraPrincipal(4.2);
          doc.text(l, xPrincipal, yPrincipal);
          yPrincipal += 4.2;
        }
      }
      yPrincipal += 3;
    }
    desenharDivisorSecaoPrincipal();
  }

  // 2. Projetos acadêmicos (com barra vertical esquerda #16181d em cada card)
  if (previa.projetos.length > 0) {
    verificarQuebraPrincipal(16);
    yPrincipal = desenharTituloModerno(
      "Projetos acadêmicos",
      xPrincipal,
      yPrincipal,
    );
    for (const p of previa.projetos) {
      verificarQuebraPrincipal(13);
      const yInicioCard = yPrincipal - 3;
      const xCard = xPrincipal + 3.5;

      doc.setFont("helvetica", "bold");
      doc.setFontSize(9.8);
      doc.setTextColor(22, 24, 29);
      doc.text(p.titulo, xCard, yPrincipal);
      yPrincipal += 4.2;

      if (p.descricao) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8.8);
        doc.setTextColor(22, 24, 29);
        const linhas = doc.splitTextToSize(p.descricao, larguraPrincipal - 4);
        for (const l of linhas) {
          verificarQuebraPrincipal(4.2);
          doc.text(l, xCard, yPrincipal);
          yPrincipal += 4.2;
        }
      }
      if (p.tecnologias) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8.5);
        doc.setTextColor(94, 102, 114);
        doc.text(`Tecnologias: ${p.tecnologias}`, xCard, yPrincipal);
        yPrincipal += 4.2;
      }

      doc.setDrawColor(22, 24, 29);
      doc.setLineWidth(0.6);
      doc.line(xPrincipal, yInicioCard, xPrincipal, yPrincipal - 1.5);
      yPrincipal += 3;
    }
    desenharDivisorSecaoPrincipal();
  }

  // 3. Formação acadêmica
  if (previa.formacoes.length > 0) {
    verificarQuebraPrincipal(15);
    yPrincipal = desenharTituloModerno(
      "Formação acadêmica",
      xPrincipal,
      yPrincipal,
    );
    for (const f of previa.formacoes) {
      verificarQuebraPrincipal(13);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(9.8);
      doc.setTextColor(22, 24, 29);
      doc.text(f.curso, xPrincipal, yPrincipal);

      const periodo = formatarPeriodoPdf(f.inicio, f.fim);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(8);
      doc.setTextColor(94, 102, 114);
      doc.text(periodo, LARGURA_PAGINA - margemX, yPrincipal, {
        align: "right",
      });
      yPrincipal += 4.2;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      doc.setTextColor(22, 24, 29);
      doc.text(f.instituicao, xPrincipal, yPrincipal);
      yPrincipal += 4.2;

      doc.setFontSize(8.5);
      doc.setTextColor(94, 102, 114);
      doc.text(`${f.nivel} · ${f.status}`, xPrincipal, yPrincipal);
      yPrincipal += 5;
    }
    if (previa.documentos.length > 0) {
      desenharDivisorSecaoPrincipal();
    }
  }

  // 4. Documentos complementares
  if (previa.documentos.length > 0) {
    verificarQuebraPrincipal(14);
    yPrincipal = desenharTituloModerno(
      "Documentos complementares",
      xPrincipal,
      yPrincipal,
    );
    for (const d of previa.documentos) {
      verificarQuebraPrincipal(5);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(8.8);
      doc.setTextColor(22, 24, 29);
      const linhas = doc.splitTextToSize(
        formatarDocumentoPdf(d),
        larguraPrincipal,
      );
      for (const l of linhas) {
        doc.text(l, xPrincipal, yPrincipal);
        yPrincipal += 4.2;
      }
    }
  }

  // Linha divisória vertical entre a coluna lateral e a coluna principal
  doc.setDrawColor(213, 217, 223); // #d5d9df
  doc.setLineWidth(0.35);
  doc.line(
    xDivisorVertical,
    yInicioColunas - 2,
    xDivisorVertical,
    Math.max(yLateral, yPrincipal),
  );
}

// ============================================================================
// 6. MODELO ACADÊMICO (BARRA AZUL-PETRÓLEO #146384 + GRADE DUPLA NO RODAPÉ)
// ============================================================================
function renderizarModeloAcademico(doc: jsPDF, previa: PreviaCurriculo): void {
  const margemX = 20;
  const larguraUtil = LARGURA_PAGINA - margemX * 2;
  const yTopoCabecalho = 20;

  // Bloco esquerdo do cabeçalho (Nome em #146384 + titulo_versao em #63707a)
  const xTextoCabecalho = margemX + 4.5;
  let yEsquerda = yTopoCabecalho + 5;
  doc.setFont("helvetica", "bold");
  doc.setFontSize(19);
  doc.setTextColor(20, 99, 132); // #146384
  doc.text(
    (previa.estudante?.nome || "Currículo").trim(),
    xTextoCabecalho,
    yEsquerda,
  );
  yEsquerda += 5.5;

  if (previa.titulo_versao) {
    doc.setFont("helvetica", "bold");
    doc.setFontSize(9.5);
    doc.setTextColor(99, 112, 122); // #63707a
    doc.text(previa.titulo_versao, xTextoCabecalho, yEsquerda);
    yEsquerda += 5;
  }

  // Bloco direito do cabeçalho (Contatos empilhados alinhados à direita)
  const contatos = obterItensContato(previa);
  let yDireita = yTopoCabecalho + 3.5;
  doc.setFont("helvetica", "normal");
  doc.setFontSize(8.2);
  doc.setTextColor(38, 50, 56); // #263238
  for (const item of contatos) {
    doc.text(item, LARGURA_PAGINA - margemX, yDireita, { align: "right" });
    yDireita += 3.8;
  }

  const yFimCabecalho = Math.max(yEsquerda, yDireita) + 2;

  // Barra vertical esquerda #146384 e linha inferior #cbd5dc
  preencherRetangulo(
    doc,
    margemX,
    yTopoCabecalho - 1,
    1.2,
    yFimCabecalho - yTopoCabecalho + 1,
    20,
    99,
    132,
  );
  doc.setDrawColor(203, 213, 220); // #cbd5dc
  doc.setLineWidth(0.35);
  doc.line(margemX, yFimCabecalho, LARGURA_PAGINA - margemX, yFimCabecalho);

  let y = yFimCabecalho + 7;

  const verificarQuebra = (espaco: number) => {
    if (y + espaco > ALTURA_PAGINA - MARGEM_INFERIOR) {
      doc.addPage();
      y = 20;
    }
  };

  const adicionarTituloSecaoAcademico = (titulo: string) => {
    verificarQuebra(14);
    y += 2;
    doc.setFont("helvetica", "bold");
    doc.setFontSize(11);
    doc.setTextColor(20, 99, 132); // #146384
    doc.text(titulo, margemX, y);
    y += 5.5;
  };

  // 1. Formação acadêmica
  if (previa.formacoes.length > 0) {
    adicionarTituloSecaoAcademico("Formação acadêmica");
    for (const f of previa.formacoes) {
      verificarQuebra(13);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(38, 50, 56); // #263238
      doc.text(f.curso, margemX, y);

      const periodo = formatarPeriodoPdf(f.inicio, f.fim);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(8.5);
      doc.setTextColor(99, 112, 122);
      doc.text(periodo, LARGURA_PAGINA - margemX, y, { align: "right" });
      y += 4.3;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9.2);
      doc.setTextColor(38, 50, 56);
      doc.text(f.instituicao, margemX, y);
      y += 4.2;

      doc.text(`${f.nivel} · ${f.status}`, margemX, y);
      y += 5.2;
    }
  }

  // 2. Projetos acadêmicos
  if (previa.projetos.length > 0) {
    adicionarTituloSecaoAcademico("Projetos acadêmicos");
    for (const p of previa.projetos) {
      verificarQuebra(12);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(38, 50, 56);
      doc.text(p.titulo, margemX, y);
      y += 4.3;

      if (p.descricao) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9.2);
        doc.setTextColor(38, 50, 56);
        const linhas = doc.splitTextToSize(p.descricao, larguraUtil);
        for (const l of linhas) {
          verificarQuebra(4.3);
          doc.text(l, margemX, y);
          y += 4.2;
        }
      }
      if (p.tecnologias) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8.8);
        doc.setTextColor(99, 112, 122);
        doc.text(`Tecnologias: ${p.tecnologias}`, margemX, y);
        y += 4.5;
      }
      y += 2;
    }
  }

  // 3. Documentos complementares (antes de Experiência no modelo Acadêmico!)
  if (previa.documentos.length > 0) {
    adicionarTituloSecaoAcademico("Documentos complementares");
    for (const d of previa.documentos) {
      verificarQuebra(5);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(9.2);
      doc.setTextColor(38, 50, 56);
      const linhas = doc.splitTextToSize(formatarDocumentoPdf(d), larguraUtil);
      for (const l of linhas) {
        doc.text(l, margemX, y);
        y += 4.3;
      }
    }
    y += 1.5;
  }

  // 4. Experiência profissional relevante
  if (previa.experiencias.length > 0) {
    adicionarTituloSecaoAcademico("Experiência profissional relevante");
    for (const e of previa.experiencias) {
      verificarQuebra(14);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(38, 50, 56);
      doc.text(e.cargo, margemX, y);

      const periodo = formatarPeriodoPdf(e.inicio, e.fim);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(8.5);
      doc.setTextColor(99, 112, 122);
      doc.text(periodo, LARGURA_PAGINA - margemX, y, { align: "right" });
      y += 4.3;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9.2);
      doc.setTextColor(38, 50, 56);
      doc.text(e.empresa, margemX, y);
      y += 4.3;

      if (e.descricao) {
        const linhas = doc.splitTextToSize(e.descricao, larguraUtil - 28);
        for (const l of linhas) {
          verificarQuebra(4.3);
          doc.text(l, margemX, y);
          y += 4.2;
        }
      }
      y += 2.5;
    }
  }

  // 5. Grade dupla no rodapé: Competências | Idiomas
  if (previa.competencias.length > 0 || previa.idiomas.length > 0) {
    verificarQuebra(20);
    y += 2;
    const yTopoGrade = y;
    let yCol1 = yTopoGrade;
    let yCol2 = yTopoGrade;
    const xCol2 = margemX + larguraUtil / 2 + 4;
    const larguraCol = larguraUtil / 2 - 4;

    if (previa.competencias.length > 0) {
      doc.setFont("helvetica", "bold");
      doc.setFontSize(11);
      doc.setTextColor(20, 99, 132);
      doc.text("Competências", margemX, yCol1);
      yCol1 += 5.5;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      doc.setTextColor(38, 50, 56);
      for (const c of previa.competencias) {
        const txt = c.nivel ? `${c.descricao} — ${c.nivel}` : c.descricao;
        const linhas = doc.splitTextToSize(txt, larguraCol);
        for (const l of linhas) {
          doc.text(l, margemX, yCol1);
          yCol1 += 4.2;
        }
      }
    }

    if (previa.idiomas.length > 0) {
      const xIdiomas = previa.competencias.length > 0 ? xCol2 : margemX;
      doc.setFont("helvetica", "bold");
      doc.setFontSize(11);
      doc.setTextColor(20, 99, 132);
      doc.text("Idiomas", xIdiomas, yCol2);
      yCol2 += 5.5;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      doc.setTextColor(38, 50, 56);
      for (const i of previa.idiomas) {
        const txt = i.nivel ? `${i.idioma} — ${i.nivel}` : i.idioma;
        const linhas = doc.splitTextToSize(txt, larguraCol);
        for (const l of linhas) {
          doc.text(l, xIdiomas, yCol2);
          yCol2 += 4.2;
        }
      }
    }

    y = Math.max(yCol1, yCol2) + 4;
  }
}

// ============================================================================
// 7. MODELO PRIMEIRO EMPREGO (FAIXA ROXA #5A3DB5 + GRADE INTERMEDIÁRIA)
// ============================================================================
function renderizarModeloPrimeiroEmprego(
  doc: jsPDF,
  previa: PreviaCurriculo,
): void {
  const margemX = 20;
  const larguraUtil = LARGURA_PAGINA - margemX * 2;
  const paddingInternoBanner = 6;
  const larguraTextoBanner = larguraUtil - paddingInternoBanner * 2;

  const contatos = obterItensContato(previa).join("   ");
  doc.setFont("helvetica", "normal");
  doc.setFontSize(8.5);
  const linhasContato = contatos
    ? doc.splitTextToSize(contatos, larguraTextoBanner)
    : [];

  const alturaBanner = 26 + linhasContato.length * 4;
  const yTopoBanner = 18;

  // Faixa de cabeçalho roxa #5a3db5
  preencherRetangulo(
    doc,
    margemX,
    yTopoBanner,
    larguraUtil,
    alturaBanner,
    90,
    61,
    181,
  );

  let yBanner = yTopoBanner + 6;
  const xBanner = margemX + paddingInternoBanner;

  doc.setFont("helvetica", "bold");
  doc.setFontSize(8);
  doc.setTextColor(255, 255, 255);
  doc.text("CURRÍCULO", xBanner, yBanner);
  yBanner += 6.5;

  doc.setFont("helvetica", "bold");
  doc.setFontSize(19);
  doc.setTextColor(255, 255, 255);
  doc.text((previa.estudante?.nome || "Currículo").trim(), xBanner, yBanner);
  yBanner += 5.2;

  if (previa.titulo_versao) {
    doc.setFont("helvetica", "bold");
    doc.setFontSize(9.5);
    doc.setTextColor(255, 255, 255);
    doc.text(previa.titulo_versao, xBanner, yBanner);
    yBanner += 5;
  }

  if (linhasContato.length > 0) {
    doc.setFont("helvetica", "normal");
    doc.setFontSize(8.5);
    doc.setTextColor(243, 232, 255);
    for (const linha of linhasContato) {
      doc.text(linha, xBanner, yBanner);
      yBanner += 4;
    }
  }

  let y = yTopoBanner + alturaBanner + 8;

  const verificarQuebra = (espaco: number) => {
    if (y + espaco > ALTURA_PAGINA - MARGEM_INFERIOR) {
      doc.addPage();
      y = 20;
    }
  };

  // Título com sublinhado curto roxo #5a3db5
  const desenharTituloPrimeiroEmprego = (
    titulo: string,
    x: number,
    yAtual: number,
  ): number => {
    doc.setFont("helvetica", "bold");
    doc.setFontSize(11);
    doc.setTextColor(31, 41, 55); // #1f2937
    doc.text(titulo, x, yAtual);
    const larguraLinha = medirLarguraTextoMm(doc, titulo, 11);
    doc.setDrawColor(90, 61, 181); // #5a3db5
    doc.setLineWidth(0.7);
    doc.line(x, yAtual + 1.5, x + larguraLinha, yAtual + 1.5);
    return yAtual + 6.5;
  };

  // 1. Formação acadêmica
  if (previa.formacoes.length > 0) {
    verificarQuebra(15);
    y = desenharTituloPrimeiroEmprego("Formação acadêmica", margemX, y);
    for (const f of previa.formacoes) {
      verificarQuebra(13);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(31, 41, 55);
      doc.text(f.curso, margemX, y);
      y += 4.3;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9.2);
      doc.setTextColor(31, 41, 55);
      doc.text(f.instituicao, margemX, y);
      y += 4.2;

      doc.text(
        `${f.nivel} · ${f.status} · ${formatarPeriodoPdf(f.inicio, f.fim)}`,
        margemX,
        y,
      );
      y += 5.5;
    }
  }

  // 2. Projetos acadêmicos
  if (previa.projetos.length > 0) {
    verificarQuebra(14);
    y += 1.5;
    y = desenharTituloPrimeiroEmprego("Projetos acadêmicos", margemX, y);
    for (const p of previa.projetos) {
      verificarQuebra(12);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(31, 41, 55);
      doc.text(p.titulo, margemX, y);
      y += 4.3;

      if (p.descricao) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9.2);
        doc.setTextColor(31, 41, 55);
        const linhas = doc.splitTextToSize(p.descricao, larguraUtil);
        for (const l of linhas) {
          verificarQuebra(4.3);
          doc.text(l, margemX, y);
          y += 4.2;
        }
      }
      if (p.tecnologias) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8.8);
        doc.setTextColor(71, 85, 105);
        doc.text(`Tecnologias: ${p.tecnologias}`, margemX, y);
        y += 4.5;
      }
      y += 2;
    }
  }

  // 3. Grade dupla intermediária: Competências | Idiomas (antes de Documentos e Experiência!)
  if (previa.competencias.length > 0 || previa.idiomas.length > 0) {
    verificarQuebra(18);
    y += 2;
    const yTopoGrade = y;
    let yCol1 = yTopoGrade;
    let yCol2 = yTopoGrade;
    const xCol2 = margemX + larguraUtil / 2 + 4;
    const larguraCol = larguraUtil / 2 - 4;

    if (previa.competencias.length > 0) {
      yCol1 = desenharTituloPrimeiroEmprego("Competências", margemX, yCol1);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(9.2);
      doc.setTextColor(31, 41, 55);
      for (const c of previa.competencias) {
        const txt = c.nivel ? `${c.descricao} — ${c.nivel}` : c.descricao;
        const linhas = doc.splitTextToSize(txt, larguraCol);
        for (const l of linhas) {
          doc.text(l, margemX, yCol1);
          yCol1 += 4.2;
        }
      }
    }

    if (previa.idiomas.length > 0) {
      const xIdiomas = previa.competencias.length > 0 ? xCol2 : margemX;
      yCol2 = desenharTituloPrimeiroEmprego("Idiomas", xIdiomas, yCol2);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(9.2);
      doc.setTextColor(31, 41, 55);
      for (const i of previa.idiomas) {
        const txt = i.nivel ? `${i.idioma} — ${i.nivel}` : i.idioma;
        const linhas = doc.splitTextToSize(txt, larguraCol);
        for (const l of linhas) {
          doc.text(l, xIdiomas, yCol2);
          yCol2 += 4.2;
        }
      }
    }

    y = Math.max(yCol1, yCol2) + 4;
  }

  // 4. Documentos complementares
  if (previa.documentos.length > 0) {
    verificarQuebra(14);
    y += 1.5;
    y = desenharTituloPrimeiroEmprego("Documentos complementares", margemX, y);
    for (const d of previa.documentos) {
      verificarQuebra(5);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(9.2);
      doc.setTextColor(31, 41, 55);
      const linhas = doc.splitTextToSize(formatarDocumentoPdf(d), larguraUtil);
      for (const l of linhas) {
        doc.text(l, margemX, y);
        y += 4.3;
      }
    }
    y += 1.5;
  }

  // 5. Experiência profissional (ao final no modelo Primeiro Emprego!)
  if (previa.experiencias.length > 0) {
    verificarQuebra(15);
    y += 1.5;
    y = desenharTituloPrimeiroEmprego("Experiência profissional", margemX, y);
    for (const e of previa.experiencias) {
      verificarQuebra(14);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(31, 41, 55);
      doc.text(e.cargo, margemX, y);
      y += 4.3;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9.2);
      doc.setTextColor(31, 41, 55);
      doc.text(
        `${e.empresa} · ${formatarPeriodoPdf(e.inicio, e.fim)}`,
        margemX,
        y,
      );
      y += 4.3;

      if (e.descricao) {
        const linhas = doc.splitTextToSize(e.descricao, larguraUtil);
        for (const l of linhas) {
          verificarQuebra(4.3);
          doc.text(l, margemX, y);
          y += 4.2;
        }
      }
      y += 2.5;
    }
  }
}

/**
 * Converte os dados estruturados da prévia do currículo em um arquivo PDF vetorial nativo
 * com texto real, selecionável, com paginação automática e fidelidade estrutural exata
 * a cada um dos 7 modelos do catálogo.
 */
export async function exportarElementoParaPdf({
  elemento,
  previa,
  nomeArquivo = "curriculo",
}: OpcoesExportacaoPdf): Promise<void> {
  const doc = new jsPDF({
    orientation: "portrait",
    unit: "mm",
    format: "a4",
  });

  // Fallback baseado em elemento HTML caso a prévia estruturada não seja fornecida
  if (!previa && elemento) {
    const margemX = 20;
    const larguraDisponivel = LARGURA_PAGINA - margemX * 2;
    let y = 22;

    const verificarQuebra = (espaco: number) => {
      if (y + espaco > ALTURA_PAGINA - MARGEM_INFERIOR) {
        doc.addPage();
        y = 20;
      }
    };

    const tituloH1 = elemento.querySelector("h1")?.textContent?.trim() || "";
    const textos = Array.from(elemento.querySelectorAll("p, li, h2, span"))
      .map((el) => el.textContent?.trim())
      .filter((t): t is string => Boolean(t && t.length > 0));

    doc.setFont("helvetica", "bold");
    doc.setFontSize(18);
    doc.setTextColor(17, 24, 39);
    doc.text(tituloH1 || "CURRÍCULO", LARGURA_PAGINA / 2, y, {
      align: "center",
    });
    y += 8;

    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.setTextColor(51, 65, 85);
    for (const texto of textos) {
      const linhas = doc.splitTextToSize(texto, larguraDisponivel);
      for (const linha of linhas) {
        verificarQuebra(5);
        doc.text(linha, margemX, y);
        y += 5;
      }
    }

    const nomeFinal = nomeArquivo.replace(/\.pdf$/i, "");
    doc.save(`${nomeFinal}.pdf`);
    return;
  }

  if (!previa) {
    return;
  }

  const layout = (previa.layout || "classico") as ModeloApresentacaoCurriculo;

  switch (layout) {
    case "criativo":
      renderizarModeloCriativo(doc, previa);
      break;
    case "moderno":
      renderizarModeloModerno(doc, previa);
      break;
    case "compacto":
      renderizarModeloCompacto(doc, previa);
      break;
    case "ats-simples":
      renderizarModeloAtsSimples(doc, previa);
      break;
    case "academico":
      renderizarModeloAcademico(doc, previa);
      break;
    case "primeiro-emprego":
      renderizarModeloPrimeiroEmprego(doc, previa);
      break;
    case "classico":
    default:
      renderizarModeloClassico(doc, previa);
      break;
  }

  const nomeFinal = nomeArquivo.replace(/\.pdf$/i, "");
  doc.save(`${nomeFinal}.pdf`);
}
