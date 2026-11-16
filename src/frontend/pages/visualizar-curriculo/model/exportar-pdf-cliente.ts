import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";

export interface OpcoesExportacaoPdf {
  elemento: HTMLElement;
  nomeArquivo?: string;
}

/** Largura de uma folha A4 em pixels CSS (210 mm a 96 dpi). */
const LARGURA_A4_PX = 794;

/**
 * Converte a folha do currículo em PDF A4 e aciona o download no navegador.
 *
 * Como faz: copia a folha para uma área fora da tela, com fundo branco e
 * largura exata de uma folha A4, e só então a captura com o html2canvas. Assim
 * o PDF não herda a moldura escura, o espaçamento nem a largura da tela, e fica
 * igual em qualquer tamanho de janela. Conteúdo maior que uma página é dividido
 * em páginas A4.
 */
export async function exportarElementoParaPdf({
  elemento,
  nomeArquivo = "curriculo.pdf",
}: OpcoesExportacaoPdf): Promise<void> {
  const area = document.createElement("div");
  Object.assign(area.style, {
    position: "fixed",
    left: "-10000px",
    top: "0",
    width: `${LARGURA_A4_PX}px`,
    background: "#ffffff",
  });
  const copia = elemento.cloneNode(true) as HTMLElement;
  Object.assign(copia.style, {
    width: "100%",
    maxWidth: "none",
    margin: "0",
    boxShadow: "none",
    borderRadius: "0",
  });
  area.appendChild(copia);
  document.body.appendChild(area);

  let canvas: HTMLCanvasElement;
  try {
    canvas = await html2canvas(area, {
      scale: 2,
      useCORS: true,
      logging: false,
      backgroundColor: "#ffffff",
      windowWidth: LARGURA_A4_PX,
    });
  } finally {
    area.remove();
  }

  const imgData = canvas.toDataURL("image/png");
  const pdf = new jsPDF({
    orientation: "portrait",
    unit: "mm",
    format: "a4",
  });

  const larguraPdf = pdf.internal.pageSize.getWidth();
  const alturaPdf = pdf.internal.pageSize.getHeight();
  const alturaTotal = (canvas.height || 1) * (larguraPdf / (canvas.width || 1));

  let alturaRestante = alturaTotal;
  let pagina = 0;

  while (alturaRestante > 0.5) {
    if (pagina > 0) {
      pdf.addPage();
    }
    pdf.addImage(imgData, "PNG", 0, -(pagina * alturaPdf), larguraPdf, alturaTotal);
    alturaRestante -= alturaPdf;
    pagina++;
  }

  const nomeFinal = nomeArquivo.endsWith(".pdf")
    ? nomeArquivo
    : `${nomeArquivo}.pdf`;

  pdf.save(nomeFinal);
}
