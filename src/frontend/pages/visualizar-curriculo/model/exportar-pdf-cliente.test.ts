import { describe, expect, it, vi } from "vitest";

import { exportarElementoParaPdf } from "./exportar-pdf-cliente";

vi.mock("html2canvas", () => ({
  default: vi.fn().mockResolvedValue({
    width: 800,
    height: 1100,
    toDataURL: vi.fn().mockReturnValue("data:image/png;base64,mock"),
  }),
}));

const mockSave = vi.fn();
const mockAddImage = vi.fn();
const mockAddPage = vi.fn();

vi.mock("jspdf", () => {
  return {
    jsPDF: class MockJsPDF {
      internal = {
        pageSize: {
          getWidth: () => 210,
          getHeight: () => 297,
        },
      };
      addImage = mockAddImage;
      addPage = mockAddPage;
      save = mockSave;
    },
  };
});

describe("exportarElementoParaPdf", () => {
  it("captura o elemento e aciona o download direto com nome de arquivo formatado", async () => {
    const el = document.createElement("div");
    el.innerHTML = "<h1>Currículo</h1>";

    await exportarElementoParaPdf({
      elemento: el,
      nomeArquivo: "Curriculo - Rafael Mendes",
    });

    expect(mockAddImage).toHaveBeenCalled();
    expect(mockSave).toHaveBeenCalledWith("Curriculo - Rafael Mendes.pdf");
  });
});
