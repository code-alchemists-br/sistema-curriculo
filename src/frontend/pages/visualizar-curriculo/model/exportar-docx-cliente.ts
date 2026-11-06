import type { PreviaCurriculo } from "../../../entities/curriculo";

export interface OpcoesExportacaoDocx {
  previa: PreviaCurriculo;
  nomeArquivo?: string;
}

/** Escapa caracteres especiais de HTML para renderização segura no documento. */
function escaparHtml(texto: string | null | undefined): string {
  if (!texto) return "";
  return texto
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/**
 * Gera um documento estruturado compatível com Microsoft Word / LibreOffice / Google Docs
 * e aciona o download direto no navegador.
 */
export function exportarPreviaParaDocx({
  previa,
  nomeArquivo = "curriculo",
}: OpcoesExportacaoDocx): void {
  const estudante = previa.estudante;
  const contato = estudante?.contato;
  const telefones = contato?.telefones?.filter(Boolean).join(" • ") || "";
  const emails = estudante?.email || "";
  const endereco = contato?.endereco || "";
  const linkedin = contato?.linkedin || "";
  const lattes = contato?.curriculo_lattes || "";

  const contatosFormatados = [endereco, telefones, emails, linkedin, lattes]
    .filter(Boolean)
    .map((c) => escaparHtml(c))
    .join(" | ");

  let secoesHtml = "";

  // 1. Formação Acadêmica
  if (previa.formacoes && previa.formacoes.length > 0) {
    const itensFormacao = previa.formacoes
      .map((f) => {
        const periodo = [f.inicio, f.fim || "Atual"].filter(Boolean).join(" - ");
        return `
          <div class="item">
            <p><strong>${escaparHtml(f.curso)}</strong> — ${escaparHtml(f.instituicao)}</p>
            <p class="detalhes">${escaparHtml(f.nivel)} | ${escaparHtml(f.status)} (${escaparHtml(periodo)})</p>
          </div>
        `;
      })
      .join("");

    secoesHtml += `
      <h2>Formação Acadêmica</h2>
      ${itensFormacao}
    `;
  }

  // 2. Experiências Profissionais
  if (previa.experiencias && previa.experiencias.length > 0) {
    const itensExperiencia = previa.experiencias
      .map((e) => {
        const periodo = [e.inicio, e.fim || "Atual"].filter(Boolean).join(" - ");
        return `
          <div class="item">
            <p><strong>${escaparHtml(e.cargo)}</strong> — ${escaparHtml(e.empresa)} <span class="detalhes">(${escaparHtml(periodo)})</span></p>
            <p class="descricao">${escaparHtml(e.descricao)}</p>
          </div>
        `;
      })
      .join("");

    secoesHtml += `
      <h2>Experiência Profissional</h2>
      ${itensExperiencia}
    `;
  }

  // 3. Competências
  if (previa.competencias && previa.competencias.length > 0) {
    const listaComp = previa.competencias
      .map((c) => `<li>${escaparHtml(c.descricao)}</li>`)
      .join("");

    secoesHtml += `
      <h2>Competências e Habilidades</h2>
      <ul>${listaComp}</ul>
    `;
  }

  // 4. Idiomas
  if (previa.idiomas && previa.idiomas.length > 0) {
    const listaIdiomas = previa.idiomas
      .map(
        (i) =>
          `<li><strong>${escaparHtml(i.idioma)}:</strong> ${escaparHtml(i.nivel)}</li>`,
      )
      .join("");

    secoesHtml += `
      <h2>Idiomas</h2>
      <ul>${listaIdiomas}</ul>
    `;
  }

  // 5. Projetos Acadêmicos
  if (previa.projetos && previa.projetos.length > 0) {
    const itensProjetos = previa.projetos
      .map((p) => {
        return `
          <div class="item">
            <p><strong>${escaparHtml(p.titulo)}</strong></p>
            <p class="descricao">${escaparHtml(p.descricao)}</p>
            ${p.tecnologias ? `<p class="detalhes"><em>Tecnologias:</em> ${escaparHtml(p.tecnologias)}</p>` : ""}
          </div>
        `;
      })
      .join("");

    secoesHtml += `
      <h2>Projetos Acadêmicos e Relevantes</h2>
      ${itensProjetos}
    `;
  }

  const conteudoDocumento = `
    <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
    <head>
      <!--[if gte mso 9]>
      <xml>
        <w:WordDocument>
          <w:View>Print</w:View>
          <w:Zoom>100</w:Zoom>
          <w:DoNotOptimizeForBrowser/>
        </w:WordDocument>
      </xml>
      <![endif]-->
      <meta charset="utf-8">
      <title>Currículo - ${escaparHtml(estudante?.nome || "Estudante")}</title>
      <style>
        @page {
          size: A4 portrait;
          margin: 20mm;
        }
        body {
          font-family: Calibri, 'Segoe UI', Arial, sans-serif;
          font-size: 11pt;
          line-height: 1.4;
          color: #222222;
        }
        h1 {
          font-size: 20pt;
          color: #0f172a;
          margin: 0 0 4pt 0;
          font-weight: bold;
        }
        h2 {
          font-size: 12pt;
          color: #0284c7;
          border-bottom: 1.5pt solid #0284c7;
          padding-bottom: 2pt;
          margin-top: 14pt;
          margin-bottom: 6pt;
          text-transform: uppercase;
          letter-spacing: 0.5pt;
        }
        p {
          margin: 0 0 4pt 0;
        }
        .contato {
          font-size: 9.5pt;
          color: #475569;
          margin-bottom: 12pt;
        }
        .item {
          margin-bottom: 8pt;
        }
        .detalhes {
          font-size: 9.5pt;
          color: #64748b;
        }
        .descricao {
          margin-top: 2pt;
          color: #334155;
        }
        ul {
          margin: 0 0 8pt 18pt;
          padding: 0;
        }
        li {
          margin-bottom: 2pt;
        }
      </style>
    </head>
    <body>
      <h1>${escaparHtml(estudante?.nome || "Nome não informado")}</h1>
      <p class="contato">${contatosFormatados}</p>
      ${secoesHtml}
    </body>
    </html>
  `;

  const blob = new Blob(["\ufeff", conteudoDocumento], {
    type: "application/msword;charset=utf-8",
  });

  let url = "";
  let precisaRevogar = false;

  if (typeof URL !== "undefined" && typeof URL.createObjectURL === "function") {
    try {
      url = URL.createObjectURL(blob);
      precisaRevogar = true;
    } catch {
      url = `data:application/msword;charset=utf-8,${encodeURIComponent(conteudoDocumento)}`;
    }
  } else {
    url = `data:application/msword;charset=utf-8,${encodeURIComponent(conteudoDocumento)}`;
  }

  const link = document.createElement("a");
  const nomeLimpo = nomeArquivo.replace(/\.(docx|doc)$/i, "");
  link.href = url;
  link.download = `${nomeLimpo}.doc`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  if (precisaRevogar && typeof URL.revokeObjectURL === "function") {
    URL.revokeObjectURL(url);
  }
}

