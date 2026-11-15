import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";

export interface OpcoesExportacaoPdf {
  elemento: HTMLElement;
  nomeArquivo?: string;
}

/**
 * Converte um elemento do DOM em arquivo PDF vetorial/rasterizado de alta densidade
 * e aciona o download direto no navegador, sem abrir a janela de impressão.
 */
export async function exportarElementoParaPdf({
  elemento,
  nomeArquivo = "curriculo.pdf",
}: OpcoesExportacaoPdf): Promise<void> {
  const canvas = await html2canvas(elemento, {
    scale: 2,
    useCORS: true,
    logging: false,
    backgroundColor: "#ffffff",
  });

  const imgData = canvas.toDataURL("image/png");
  const pdf = new jsPDF({
    orientation: "portrait",
    unit: "mm",
    format: "a4",
  });

  const larguraPdf = pdf.internal.pageSize.getWidth();
  const alturaPdf = pdf.internal.pageSize.getHeight();

  const larguraImg = canvas.width || 1;
  const alturaImg = canvas.height || 1;
  const ratio = larguraImg / larguraPdf;
  const alturaTotal = alturaImg / ratio;

  let alturaRestante = alturaTotal;
  let pagina = 0;

  while (alturaRestante > 0) {
    if (pagina > 0) {
      pdf.addPage();
    }
    const posicaoY = -(pagina * alturaPdf);
    pdf.addImage(imgData, "PNG", 0, posicaoY, larguraPdf, alturaTotal);
    alturaRestante -= alturaPdf;
    pagina++;
  }

  const nomeFinal = nomeArquivo.endsWith(".pdf")
    ? nomeArquivo
    : `${nomeArquivo}.pdf`;

  pdf.save(nomeFinal);
}
