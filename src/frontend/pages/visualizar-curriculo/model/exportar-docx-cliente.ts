import { strToU8, zipSync } from "fflate";
import type { PreviaCurriculo } from "../../../entities/curriculo";
import type { ModeloApresentacaoCurriculo } from "../../../features/alternar-modelo-curriculo";
import {
  formatarDocumentoPdf,
  formatarPeriodoPdf,
} from "./exportar-pdf-cliente";

export interface OpcoesExportacaoDocx {
  previa: PreviaCurriculo;
  nomeArquivo?: string;
}

/** Escapa caracteres reservados para renderização XML segura. */
function escaparXml(texto: string | null | undefined): string {
  if (!texto) return "";
  return texto
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function obterItensContatoDocx(
  previa: PreviaCurriculo,
  mostrarUrlCompleta = false,
): string[] {
  const { estudante } = previa;
  const contato = estudante?.contato;
  const itens: string[] = [];

  if (estudante?.email?.trim()) itens.push(estudante.email.trim());
  if (contato?.telefones) {
    for (const t of contato.telefones) {
      if (t && t.trim()) itens.push(t.trim());
    }
  }
  if (contato?.endereco?.trim()) itens.push(contato.endereco.trim());
  if (contato?.linkedin?.trim()) {
    itens.push(
      mostrarUrlCompleta
        ? contato.linkedin.trim()
        : `LinkedIn: ${contato.linkedin.trim()}`,
    );
  }
  if (contato?.curriculo_lattes?.trim()) {
    itens.push(
      mostrarUrlCompleta
        ? contato.curriculo_lattes.trim()
        : `Currículo Lattes: ${contato.curriculo_lattes.trim()}`,
    );
  }
  return itens;
}

function criarParagrafoXml(
  texto: string,
  opcoes: {
    fonte?: string;
    tamanhoMeiosPontos?: number;
    corHex?: string;
    negrito?: boolean;
    italico?: boolean;
    alinhamento?: "left" | "center" | "right";
    espacoAntes?: number;
    espacoDepois?: number;
    bordaInferiorHex?: string;
    bordaSuperiorHex?: string;
    fundoHex?: string;
  } = {},
): string {
  const {
    fonte = "Calibri",
    tamanhoMeiosPontos = 20,
    corHex = "1F2937",
    negrito = false,
    italico = false,
    alinhamento = "left",
    espacoAntes = 0,
    espacoDepois = 80,
    bordaInferiorHex,
    bordaSuperiorHex,
    fundoHex,
  } = opcoes;

  const bordasXml =
    bordaInferiorHex || bordaSuperiorHex
      ? `<w:pBdr>
          ${bordaSuperiorHex ? `<w:top w:val="single" w:sz="8" w:space="4" w:color="${bordaSuperiorHex}"/>` : ""}
          ${bordaInferiorHex ? `<w:bottom w:val="single" w:sz="8" w:space="4" w:color="${bordaInferiorHex}"/>` : ""}
        </w:pBdr>`
      : "";

  const shdXml = fundoHex
    ? `<w:shd w:val="clear" w:color="auto" w:fill="${fundoHex}"/>`
    : "";

  return `
    <w:p>
      <w:pPr>
        <w:jc w:val="${alinhamento}"/>
        <w:spacing w:before="${espacoAntes}" w:after="${espacoDepois}"/>
        ${bordasXml}
        ${shdXml}
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="${fonte}" w:hAnsi="${fonte}" w:cs="${fonte}"/>
          ${negrito ? "<w:b/>" : ""}
          ${italico ? "<w:i/>" : ""}
          <w:sz w:val="${tamanhoMeiosPontos}"/>
          <w:szCs w:val="${tamanhoMeiosPontos}"/>
          <w:color w:val="${corHex}"/>
        </w:rPr>
        <w:t xml:space="preserve">${escaparXml(texto)}</w:t>
      </w:r>
    </w:p>
  `;
}

function construirSecoesPrincipaisXml(
  previa: PreviaCurriculo,
  opcoes: {
    fonteTitulo: string;
    fonteCorpo: string;
    corTituloHex: string;
    corTextoHex: string;
    corSubtextoHex: string;
    maiusculoTitulo: boolean;
    bordaInferiorTituloHex?: string;
    bordaSuperiorTituloHex?: string;
    usarTracoQuandoAtual?: boolean;
    tituloExperiencia?: string;
    ordem: ReadonlyArray<
      | "formacao"
      | "experiencia"
      | "projetos"
      | "competencias"
      | "idiomas"
      | "documentos"
      | "competencias-idiomas-inline"
    >;
  },
): string {
  let xml = "";

  const adicionarTitulo = (t: string) => {
    xml += criarParagrafoXml(opcoes.maiusculoTitulo ? t.toUpperCase() : t, {
      fonte: opcoes.fonteTitulo,
      tamanhoMeiosPontos: 22,
      corHex: opcoes.corTituloHex,
      negrito: true,
      espacoAntes: 220,
      espacoDepois: 100,
      bordaInferiorHex: opcoes.bordaInferiorTituloHex,
      bordaSuperiorHex: opcoes.bordaSuperiorTituloHex,
    });
  };

  for (const secao of opcoes.ordem) {
    if (secao === "formacao" && previa.formacoes.length > 0) {
      adicionarTitulo("Formação acadêmica");
      for (const f of previa.formacoes) {
        const periodo = formatarPeriodoPdf(
          f.inicio,
          f.fim,
          opcoes.usarTracoQuandoAtual,
        );
        xml += criarParagrafoXml(`${f.curso} — ${periodo}`, {
          fonte: opcoes.fonteCorpo,
          tamanhoMeiosPontos: 20,
          corHex: opcoes.corTextoHex,
          negrito: true,
          espacoAntes: 60,
          espacoDepois: 30,
        });
        xml += criarParagrafoXml(
          `${f.instituicao} • ${f.nivel} · ${f.status}`,
          {
            fonte: opcoes.fonteCorpo,
            tamanhoMeiosPontos: 18,
            corHex: opcoes.corSubtextoHex,
            espacoDepois: 90,
          },
        );
      }
    }

    if (secao === "experiencia" && previa.experiencias.length > 0) {
      adicionarTitulo(opcoes.tituloExperiencia || "Experiência profissional");
      for (const e of previa.experiencias) {
        const periodo = formatarPeriodoPdf(
          e.inicio,
          e.fim,
          opcoes.usarTracoQuandoAtual,
        );
        xml += criarParagrafoXml(`${e.cargo} — ${periodo}`, {
          fonte: opcoes.fonteCorpo,
          tamanhoMeiosPontos: 20,
          corHex: opcoes.corTextoHex,
          negrito: true,
          espacoAntes: 60,
          espacoDepois: 30,
        });
        xml += criarParagrafoXml(e.empresa, {
          fonte: opcoes.fonteCorpo,
          tamanhoMeiosPontos: 19,
          corHex: opcoes.corSubtextoHex,
          espacoDepois: 40,
        });
        if (e.descricao) {
          xml += criarParagrafoXml(e.descricao, {
            fonte: opcoes.fonteCorpo,
            tamanhoMeiosPontos: 18,
            corHex: opcoes.corTextoHex,
            espacoDepois: 100,
          });
        }
      }
    }

    if (secao === "projetos" && previa.projetos.length > 0) {
      adicionarTitulo("Projetos acadêmicos");
      for (const p of previa.projetos) {
        xml += criarParagrafoXml(p.titulo, {
          fonte: opcoes.fonteCorpo,
          tamanhoMeiosPontos: 20,
          corHex: opcoes.corTextoHex,
          negrito: true,
          espacoAntes: 60,
          espacoDepois: 30,
        });
        if (p.descricao) {
          xml += criarParagrafoXml(p.descricao, {
            fonte: opcoes.fonteCorpo,
            tamanhoMeiosPontos: 18,
            corHex: opcoes.corTextoHex,
            espacoDepois: 40,
          });
        }
        if (p.tecnologias) {
          xml += criarParagrafoXml(`Tecnologias: ${p.tecnologias}`, {
            fonte: opcoes.fonteCorpo,
            tamanhoMeiosPontos: 18,
            corHex: opcoes.corSubtextoHex,
            italico: true,
            espacoDepois: 90,
          });
        }
      }
    }

    if (secao === "competencias" && previa.competencias.length > 0) {
      adicionarTitulo("Competências");
      for (const c of previa.competencias) {
        const txt = c.nivel ? `${c.descricao} — ${c.nivel}` : c.descricao;
        xml += criarParagrafoXml(`• ${txt}`, {
          fonte: opcoes.fonteCorpo,
          tamanhoMeiosPontos: 18,
          corHex: opcoes.corTextoHex,
          espacoDepois: 45,
        });
      }
    }

    if (secao === "idiomas" && previa.idiomas.length > 0) {
      adicionarTitulo("Idiomas");
      for (const i of previa.idiomas) {
        const txt = i.nivel ? `${i.idioma} — ${i.nivel}` : i.idioma;
        xml += criarParagrafoXml(`• ${txt}`, {
          fonte: opcoes.fonteCorpo,
          tamanhoMeiosPontos: 18,
          corHex: opcoes.corTextoHex,
          espacoDepois: 45,
        });
      }
    }

    if (secao === "competencias-idiomas-inline") {
      if (previa.competencias.length > 0) {
        adicionarTitulo("Competências");
        const txt = previa.competencias
          .map((c) => (c.nivel ? `${c.descricao} — ${c.nivel}` : c.descricao))
          .join("  •  ");
        xml += criarParagrafoXml(txt, {
          fonte: opcoes.fonteCorpo,
          tamanhoMeiosPontos: 18,
          corHex: opcoes.corTextoHex,
          espacoDepois: 80,
        });
      }
      if (previa.idiomas.length > 0) {
        adicionarTitulo("Idiomas");
        const txt = previa.idiomas
          .map((i) => (i.nivel ? `${i.idioma} — ${i.nivel}` : i.idioma))
          .join("  •  ");
        xml += criarParagrafoXml(txt, {
          fonte: opcoes.fonteCorpo,
          tamanhoMeiosPontos: 18,
          corHex: opcoes.corTextoHex,
          espacoDepois: 80,
        });
      }
    }

    if (secao === "documentos" && previa.documentos.length > 0) {
      adicionarTitulo("Documentos complementares");
      for (const d of previa.documentos) {
        xml += criarParagrafoXml(formatarDocumentoPdf(d), {
          fonte: opcoes.fonteCorpo,
          tamanhoMeiosPontos: 18,
          corHex: opcoes.corTextoHex,
          espacoDepois: 50,
        });
      }
    }
  }

  return xml;
}

/**
 * Gera um documento Office Open XML (.docx) genuíno compatível com Microsoft Word,
 * LibreOffice, Google Docs e sistemas de triagem ATS, respeitando a estrutura e paleta
 * visual do modelo selecionado.
 */
export async function exportarPreviaParaDocx({
  previa,
  nomeArquivo = "curriculo",
}: OpcoesExportacaoDocx): Promise<void> {
  const layout = (previa.layout || "classico") as ModeloApresentacaoCurriculo;
  const nomeEstudante = (previa.estudante?.nome || "Currículo").trim();
  const contatos = obterItensContatoDocx(previa, layout === "compacto");

  let corpoXml = "";

  if (layout === "criativo") {
    // Tabela de 2 colunas com barra lateral verde esmeralda #075647 à esquerda
    let lateralXml = "";
    lateralXml += criarParagrafoXml(nomeEstudante, {
      fonte: "Georgia",
      tamanhoMeiosPontos: 32,
      corHex: "FFFFFF",
      negrito: true,
      alinhamento: "center",
      espacoDepois: 60,
    });
    if (previa.titulo_versao) {
      lateralXml += criarParagrafoXml(previa.titulo_versao.toUpperCase(), {
        fonte: "Calibri",
        tamanhoMeiosPontos: 16,
        corHex: "A8DDD0",
        negrito: true,
        alinhamento: "center",
        espacoDepois: 200,
      });
    }
    if (contatos.length > 0) {
      lateralXml += criarParagrafoXml("Dados de contato", {
        fonte: "Georgia",
        tamanhoMeiosPontos: 21,
        corHex: "FFFFFF",
        negrito: true,
        espacoAntes: 140,
        espacoDepois: 80,
      });
      for (const c of contatos) {
        lateralXml += criarParagrafoXml(c, {
          fonte: "Calibri",
          tamanhoMeiosPontos: 17,
          corHex: "FFFFFF",
          espacoDepois: 50,
        });
      }
    }
    if (previa.competencias.length > 0) {
      lateralXml += criarParagrafoXml("Competências", {
        fonte: "Georgia",
        tamanhoMeiosPontos: 21,
        corHex: "FFFFFF",
        negrito: true,
        espacoAntes: 180,
        espacoDepois: 80,
      });
      for (const c of previa.competencias) {
        lateralXml += criarParagrafoXml(c.descricao, {
          fonte: "Calibri",
          tamanhoMeiosPontos: 18,
          corHex: "FFFFFF",
          negrito: true,
          espacoDepois: 20,
        });
        if (c.nivel) {
          lateralXml += criarParagrafoXml(c.nivel, {
            fonte: "Calibri",
            tamanhoMeiosPontos: 16,
            corHex: "A8DDD0",
            bordaInferiorHex: "A8DDD0",
            espacoDepois: 70,
          });
        }
      }
    }
    if (previa.idiomas.length > 0) {
      lateralXml += criarParagrafoXml("Idiomas", {
        fonte: "Georgia",
        tamanhoMeiosPontos: 21,
        corHex: "FFFFFF",
        negrito: true,
        espacoAntes: 180,
        espacoDepois: 80,
      });
      for (const i of previa.idiomas) {
        lateralXml += criarParagrafoXml(i.idioma, {
          fonte: "Calibri",
          tamanhoMeiosPontos: 18,
          corHex: "FFFFFF",
          negrito: true,
          espacoDepois: 20,
        });
        if (i.nivel) {
          lateralXml += criarParagrafoXml(i.nivel, {
            fonte: "Calibri",
            tamanhoMeiosPontos: 16,
            corHex: "A8DDD0",
            bordaInferiorHex: "A8DDD0",
            espacoDepois: 70,
          });
        }
      }
    }

    const principalXml = construirSecoesPrincipaisXml(previa, {
      fonteTitulo: "Georgia",
      fonteCorpo: "Calibri",
      corTituloHex: "1E293B",
      corTextoHex: "1E293B",
      corSubtextoHex: "52606D",
      maiusculoTitulo: false,
      bordaSuperiorTituloHex: "075647",
      ordem: ["projetos", "experiencia", "formacao", "documentos"],
    });

    corpoXml = `
      <w:tbl>
        <w:tblPr>
          <w:tblW w:w="5000" w:type="pct"/>
          <w:tblCellMar>
            <w:top w:w="220" w:type="dxa"/>
            <w:left w:w="200" w:type="dxa"/>
            <w:bottom w:w="220" w:type="dxa"/>
            <w:right w:w="200" w:type="dxa"/>
          </w:tblCellMar>
        </w:tblPr>
        <w:tr>
          <w:tc>
            <w:tcPr>
              <w:tcW w:w="1500" w:type="pct"/>
              <w:shd w:val="clear" w:color="auto" w:fill="075647"/>
            </w:tcPr>
            ${lateralXml}
          </w:tc>
          <w:tc>
            <w:tcPr>
              <w:tcW w:w="3500" w:type="pct"/>
            </w:tcPr>
            ${principalXml || criarParagrafoXml("")}
          </w:tc>
        </w:tr>
      </w:tbl>
    `;
  } else if (layout === "moderno") {
    // Cabeçalho largo em maiúsculas + tabela de 2 colunas com divisor vertical #D5D9DF
    corpoXml += criarParagrafoXml(nomeEstudante.toUpperCase(), {
      fonte: "Arial",
      tamanhoMeiosPontos: 42,
      corHex: "16181D",
      negrito: true,
      espacoDepois: 40,
    });
    if (previa.titulo_versao) {
      corpoXml += criarParagrafoXml(previa.titulo_versao, {
        fonte: "Arial",
        tamanhoMeiosPontos: 20,
        corHex: "5E6672",
        bordaInferiorHex: "D5D9DF",
        espacoDepois: 180,
      });
    }

    let lateralXml = "";
    if (contatos.length > 0) {
      lateralXml += criarParagrafoXml("INFORMAÇÕES", {
        fonte: "Arial",
        tamanhoMeiosPontos: 20,
        corHex: "16181D",
        negrito: true,
        bordaInferiorHex: "16181D",
        espacoDepois: 80,
      });
      for (const c of contatos) {
        lateralXml += criarParagrafoXml(c, {
          fonte: "Arial",
          tamanhoMeiosPontos: 17,
          corHex: "16181D",
          espacoDepois: 50,
        });
      }
    }
    if (previa.competencias.length > 0) {
      lateralXml += criarParagrafoXml("COMPETÊNCIAS", {
        fonte: "Arial",
        tamanhoMeiosPontos: 20,
        corHex: "16181D",
        negrito: true,
        bordaInferiorHex: "16181D",
        espacoAntes: 160,
        espacoDepois: 80,
      });
      for (const c of previa.competencias) {
        lateralXml += criarParagrafoXml(
          c.nivel ? `${c.descricao} (${c.nivel})` : c.descricao,
          {
            fonte: "Arial",
            tamanhoMeiosPontos: 17,
            corHex: "16181D",
            negrito: true,
            bordaInferiorHex: "1B1D21",
            espacoDepois: 60,
          },
        );
      }
    }
    if (previa.idiomas.length > 0) {
      lateralXml += criarParagrafoXml("IDIOMAS", {
        fonte: "Arial",
        tamanhoMeiosPontos: 20,
        corHex: "16181D",
        negrito: true,
        bordaInferiorHex: "16181D",
        espacoAntes: 160,
        espacoDepois: 80,
      });
      for (const i of previa.idiomas) {
        lateralXml += criarParagrafoXml(
          i.nivel ? `${i.idioma} (${i.nivel})` : i.idioma,
          {
            fonte: "Arial",
            tamanhoMeiosPontos: 17,
            corHex: "16181D",
            negrito: true,
            bordaInferiorHex: "1B1D21",
            espacoDepois: 60,
          },
        );
      }
    }

    const principalXml = construirSecoesPrincipaisXml(previa, {
      fonteTitulo: "Arial",
      fonteCorpo: "Arial",
      corTituloHex: "16181D",
      corTextoHex: "16181D",
      corSubtextoHex: "5E6672",
      maiusculoTitulo: true,
      bordaInferiorTituloHex: "16181D",
      ordem: ["experiencia", "projetos", "formacao", "documentos"],
    });

    corpoXml += `
      <w:tbl>
        <w:tblPr>
          <w:tblW w:w="5000" w:type="pct"/>
          <w:tblCellMar>
            <w:top w:w="120" w:type="dxa"/>
            <w:left w:w="140" w:type="dxa"/>
            <w:bottom w:w="120" w:type="dxa"/>
            <w:right w:w="140" w:type="dxa"/>
          </w:tblCellMar>
        </w:tblPr>
        <w:tr>
          <w:tc>
            <w:tcPr>
              <w:tcW w:w="1400" w:type="pct"/>
              <w:tcBorders>
                <w:right w:val="single" w:sz="6" w:space="0" w:color="D5D9DF"/>
              </w:tcBorders>
            </w:tcPr>
            ${lateralXml || criarParagrafoXml("")}
          </w:tc>
          <w:tc>
            <w:tcPr>
              <w:tcW w:w="3600" w:type="pct"/>
            </w:tcPr>
            ${principalXml || criarParagrafoXml("")}
          </w:tc>
        </w:tr>
      </w:tbl>
    `;
  } else if (layout === "primeiro-emprego") {
    // Faixa roxa #5A3DB5 no cabeçalho + Formação -> Projetos -> Competências/Idiomas -> Documentos -> Experiência
    corpoXml += criarParagrafoXml("CURRÍCULO", {
      fonte: "Arial",
      tamanhoMeiosPontos: 16,
      corHex: "FFFFFF",
      negrito: true,
      fundoHex: "5A3DB5",
      espacoDepois: 20,
    });
    corpoXml += criarParagrafoXml(nomeEstudante, {
      fonte: "Arial",
      tamanhoMeiosPontos: 36,
      corHex: "FFFFFF",
      negrito: true,
      fundoHex: "5A3DB5",
      espacoDepois: 40,
    });
    if (previa.titulo_versao) {
      corpoXml += criarParagrafoXml(previa.titulo_versao, {
        fonte: "Arial",
        tamanhoMeiosPontos: 20,
        corHex: "FFFFFF",
        negrito: true,
        fundoHex: "5A3DB5",
        espacoDepois: 40,
      });
    }
    if (contatos.length > 0) {
      corpoXml += criarParagrafoXml(contatos.join("  •  "), {
        fonte: "Arial",
        tamanhoMeiosPontos: 17,
        corHex: "F3E8FF",
        fundoHex: "5A3DB5",
        espacoDepois: 180,
      });
    }

    corpoXml += construirSecoesPrincipaisXml(previa, {
      fonteTitulo: "Arial",
      fonteCorpo: "Arial",
      corTituloHex: "1F2937",
      corTextoHex: "1F2937",
      corSubtextoHex: "475569",
      maiusculoTitulo: false,
      bordaInferiorTituloHex: "5A3DB5",
      ordem: [
        "formacao",
        "projetos",
        "competencias",
        "idiomas",
        "documentos",
        "experiencia",
      ],
    });
  } else if (layout === "academico") {
    // Cabeçalho azul-petróleo #146384 + ordem acadêmica com "Experiência profissional relevante"
    corpoXml += criarParagrafoXml(nomeEstudante, {
      fonte: "Arial",
      tamanhoMeiosPontos: 36,
      corHex: "146384",
      negrito: true,
      espacoDepois: 40,
    });
    if (previa.titulo_versao) {
      corpoXml += criarParagrafoXml(previa.titulo_versao, {
        fonte: "Arial",
        tamanhoMeiosPontos: 19,
        corHex: "63707A",
        negrito: true,
        espacoDepois: 60,
      });
    }
    if (contatos.length > 0) {
      corpoXml += criarParagrafoXml(contatos.join("  |  "), {
        fonte: "Arial",
        tamanhoMeiosPontos: 17,
        corHex: "263238",
        bordaInferiorHex: "CBD5DC",
        espacoDepois: 160,
      });
    }

    corpoXml += construirSecoesPrincipaisXml(previa, {
      fonteTitulo: "Arial",
      fonteCorpo: "Arial",
      corTituloHex: "146384",
      corTextoHex: "263238",
      corSubtextoHex: "63707A",
      maiusculoTitulo: false,
      tituloExperiencia: "Experiência profissional relevante",
      ordem: [
        "formacao",
        "projetos",
        "documentos",
        "experiencia",
        "competencias",
        "idiomas",
      ],
    });
  } else if (layout === "ats-simples") {
    // 100% linear ATS azul #397BD1, Experiência profissional primeiro
    corpoXml += criarParagrafoXml(nomeEstudante, {
      fonte: "Arial",
      tamanhoMeiosPontos: 36,
      corHex: "397BD1",
      negrito: true,
      espacoDepois: 40,
    });
    if (previa.titulo_versao) {
      corpoXml += criarParagrafoXml(previa.titulo_versao, {
        fonte: "Arial",
        tamanhoMeiosPontos: 20,
        corHex: "29435D",
        negrito: true,
        espacoDepois: 50,
      });
    }
    if (contatos.length > 0) {
      corpoXml += criarParagrafoXml(contatos.join("   "), {
        fonte: "Arial",
        tamanhoMeiosPontos: 18,
        corHex: "29435D",
        bordaInferiorHex: "B9CCE5",
        espacoDepois: 160,
      });
    }

    corpoXml += construirSecoesPrincipaisXml(previa, {
      fonteTitulo: "Arial",
      fonteCorpo: "Arial",
      corTituloHex: "397BD1",
      corTextoHex: "29435D",
      corSubtextoHex: "29435D",
      maiusculoTitulo: true,
      ordem: [
        "experiencia",
        "formacao",
        "projetos",
        "competencias-idiomas-inline",
        "documentos",
      ],
    });
  } else if (layout === "compacto") {
    // Compacto alinhado à esquerda com borda #2563EB e listas inline
    corpoXml += criarParagrafoXml(nomeEstudante, {
      fonte: "Calibri",
      tamanhoMeiosPontos: 32,
      corHex: "1F2937",
      negrito: true,
      espacoDepois: 40,
    });
    if (contatos.length > 0) {
      corpoXml += criarParagrafoXml(contatos.join("  •  "), {
        fonte: "Calibri",
        tamanhoMeiosPontos: 18,
        corHex: "475569",
        bordaInferiorHex: "2563EB",
        espacoDepois: 140,
      });
    }

    corpoXml += construirSecoesPrincipaisXml(previa, {
      fonteTitulo: "Calibri",
      fonteCorpo: "Calibri",
      corTituloHex: "1E3A8A",
      corTextoHex: "1F2937",
      corSubtextoHex: "475569",
      maiusculoTitulo: false,
      usarTracoQuandoAtual: true,
      ordem: [
        "formacao",
        "experiencia",
        "projetos",
        "competencias-idiomas-inline",
        "documentos",
      ],
    });
  } else {
    // Clássico centralizado
    corpoXml += criarParagrafoXml(nomeEstudante.toUpperCase(), {
      fonte: "Calibri",
      tamanhoMeiosPontos: 36,
      corHex: "111827",
      negrito: true,
      alinhamento: "center",
      espacoDepois: 50,
    });
    if (contatos.length > 0) {
      corpoXml += criarParagrafoXml(contatos.join("  •  "), {
        fonte: "Calibri",
        tamanhoMeiosPontos: 18,
        corHex: "475569",
        alinhamento: "center",
        bordaInferiorHex: "111827",
        espacoDepois: 180,
      });
    }

    corpoXml += construirSecoesPrincipaisXml(previa, {
      fonteTitulo: "Calibri",
      fonteCorpo: "Calibri",
      corTituloHex: "111827",
      corTextoHex: "1F2937",
      corSubtextoHex: "475569",
      maiusculoTitulo: true,
      bordaInferiorTituloHex: "CBD5E1",
      ordem: [
        "formacao",
        "experiencia",
        "projetos",
        "competencias",
        "idiomas",
        "documentos",
      ],
    });
  }

  const contentTypesXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>`;

  const rootRelsXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>`;

  const documentRelsXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>`;

  const stylesXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
        <w:sz w:val="20"/>
        <w:szCs w:val="20"/>
        <w:lang w:val="pt-BR"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="100" w:line="276" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>`;

  const documentXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    ${corpoXml}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1020" w:right="1020" w:bottom="1020" w:left="1020" w:header="708" w:footer="708" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>`;

  const zipBytes = zipSync({
    "[Content_Types].xml": strToU8(contentTypesXml),
    "_rels/.rels": strToU8(rootRelsXml),
    "word/_rels/document.xml.rels": strToU8(documentRelsXml),
    "word/styles.xml": strToU8(stylesXml),
    "word/document.xml": strToU8(documentXml),
  });

  const blob = new Blob([zipBytes as unknown as BlobPart], {
    type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  });

  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  const nomeLimpo = nomeArquivo.replace(/\.(docx|doc)$/i, "");
  link.href = url;
  link.download = `${nomeLimpo}.docx`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
