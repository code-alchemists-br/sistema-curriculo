import { afterEach, describe, expect, it, vi } from "vitest";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import { exportarPreviaParaDocx } from "./exportar-docx-cliente";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("exportarPreviaParaDocx", () => {
  const previaExemplo: PreviaCurriculo = {
    curriculo_id: "curr-1",
    titulo_versao: "Versão Principal",
    layout: "classico",
    estudante: {
      nome: "Maria Oliveira",
      email: "maria@fatec.sp.gov.br",
      contato: {
        endereco: "São Paulo, SP",
        telefones: ["(11) 98888-7777"],
        linkedin: "https://linkedin.com/in/maria",
        curriculo_lattes: null,
      },
    },
    formacoes: [
      {
        id: "f-1",
        instituicao: "FATEC",
        curso: "ADS",
        nivel: "Graduação",
        status: "Em andamento",
        inicio: "2023",
        fim: "2025",
      },
    ],
    experiencias: [
      {
        id: "e-1",
        empresa: "Empresa ABC",
        cargo: "Estagiária",
        descricao: "Desenvolvimento React",
        inicio: "2023",
        fim: null,
      },
    ],
    competencias: [
      {
        id: "c-1",
        descricao: "React",
        nivel: "avancado",
      },
    ],
    idiomas: [
      {
        id: "i-1",
        idioma: "Inglês",
        nivel: "Avançado",
      },
    ],
    projetos: [
      {
        id: "p-1",
        titulo: "App Liminal",
        descricao: "Gerador de currículo",
        tecnologias: "TypeScript",
      },
    ],
    documentos: [],
  };

  it("cria um link com blob Word e aciona o clique para download", () => {
    const createObjectURLSpy = vi
      .spyOn(URL, "createObjectURL")
      .mockReturnValue("blob:mock-url");
    const revokeObjectURLSpy = vi
      .spyOn(URL, "revokeObjectURL")
      .mockImplementation(() => {});

    const clickSpy = vi.fn();
    const originalCreateElement = document.createElement.bind(document);
    let capturedLink: HTMLAnchorElement | null = null;

    vi.spyOn(document, "createElement").mockImplementation((tagName: string) => {
      const el = originalCreateElement(tagName);
      if (tagName.toLowerCase() === "a") {
        capturedLink = el as HTMLAnchorElement;
        capturedLink.click = clickSpy;
      }
      return el;
    });

    const appendChildSpy = vi.spyOn(document.body, "appendChild");
    const removeChildSpy = vi.spyOn(document.body, "removeChild");

    exportarPreviaParaDocx({
      previa: previaExemplo,
      nomeArquivo: "Curriculo - Maria Oliveira",
    });

    expect(capturedLink).not.toBeNull();
    expect(capturedLink?.download).toBe("Curriculo - Maria Oliveira.doc");
    expect(capturedLink?.href).toBe("blob:mock-url");
    expect(appendChildSpy).toHaveBeenCalledWith(capturedLink);
    expect(clickSpy).toHaveBeenCalled();
    expect(removeChildSpy).toHaveBeenCalledWith(capturedLink);
    expect(revokeObjectURLSpy).toHaveBeenCalledWith("blob:mock-url");

    createObjectURLSpy.mockRestore();
    revokeObjectURLSpy.mockRestore();
  });
});

