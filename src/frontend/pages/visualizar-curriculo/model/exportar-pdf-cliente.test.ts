import { beforeEach, describe, expect, it, vi } from "vitest";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import { exportarElementoParaPdf } from "./exportar-pdf-cliente";

const mockSave = vi.fn();
const mockText = vi.fn();
const mockLine = vi.fn();
const mockRect = vi.fn();
const mockAddPage = vi.fn();
const mockSetFont = vi.fn();
const mockSetFontSize = vi.fn();
const mockSetTextColor = vi.fn();
const mockSetDrawColor = vi.fn();
const mockSetFillColor = vi.fn();
const mockSetLineWidth = vi.fn();
const mockGetTextWidth = vi.fn((texto: string) => texto.length * 2.2);
const mockSplitTextToSize = vi.fn((texto: string) => [texto]);

vi.mock("jspdf", () => {
  return {
    jsPDF: class MockJsPDF {
      setFont = mockSetFont;
      setFontSize = mockSetFontSize;
      setTextColor = mockSetTextColor;
      setDrawColor = mockSetDrawColor;
      setFillColor = mockSetFillColor;
      setLineWidth = mockSetLineWidth;
      getTextWidth = mockGetTextWidth;
      text = mockText;
      line = mockLine;
      rect = mockRect;
      splitTextToSize = mockSplitTextToSize;
      addPage = mockAddPage;
      save = mockSave;
    },
  };
});

describe("exportarElementoParaPdf", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  const previaExemplo: PreviaCurriculo = {
    curriculo_id: "curr-1",
    titulo_versao: "Versão Principal",
    layout: "classico",
    estudante: {
      nome: "Rafael Mendes",
      email: "rafael@exemplo.com",
      contato: {
        endereco: "São Paulo, SP",
        telefones: ["(11) 99999-8888"],
        linkedin: "https://linkedin.com/in/rafael",
        curriculo_lattes: null,
      },
    },
    formacoes: [
      {
        id: "f-1",
        instituicao: "FATEC",
        curso: "Engenharia de Software",
        nivel: "Graduação",
        status: "Em andamento",
        inicio: "2023-02-01",
        fim: null,
      },
    ],
    experiencias: [
      {
        id: "e-1",
        empresa: "Empresa XPTO",
        cargo: "Desenvolvedor",
        descricao: "Criação de micro frontends.",
        inicio: "2023-05-01",
        fim: null,
      },
    ],
    competencias: [
      {
        id: "c-1",
        descricao: "TypeScript",
        nivel: "Avançado",
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
        titulo: "Portal Liminal",
        descricao: "Assistente de currículo",
        tecnologias: "React, Vite",
      },
    ],
    documentos: [
      {
        id: "d-1",
        nome_arquivo: "Certificado AWS",
        tipo_arquivo: "Emissão: Amazon",
      },
    ],
  };

  it("gera PDF vetorial do modelo Clássico com texto pesquisável e cabeçalho centralizado", async () => {
    await exportarElementoParaPdf({
      previa: previaExemplo,
      nomeArquivo: "Curriculo - Rafael Mendes",
    });

    expect(mockText).toHaveBeenCalledWith(
      "RAFAEL MENDES",
      105,
      expect.any(Number),
      { align: "center" },
    );
    expect(mockText).toHaveBeenCalledWith(
      "FORMAÇÃO ACADÊMICA",
      20,
      expect.any(Number),
    );
    expect(mockText).toHaveBeenCalledWith(
      "EXPERIÊNCIA PROFISSIONAL",
      20,
      expect.any(Number),
    );
    expect(mockSave).toHaveBeenCalledWith("Curriculo - Rafael Mendes.pdf");
  });

  it("renderiza cada um dos 7 modelos do catálogo com sua estrutura e paleta próprias", async () => {
    // 1. Criativo: barra lateral verde #075647 (7, 86, 71) e seção "Dados de contato"
    await exportarElementoParaPdf({
      previa: { ...previaExemplo, layout: "criativo" },
    });
    expect(mockSetFillColor).toHaveBeenCalledWith(7, 86, 71);
    expect(mockText).toHaveBeenCalledWith(
      "Dados de contato",
      expect.any(Number),
      expect.any(Number),
    );

    vi.clearAllMocks();

    // 2. Moderno: coluna lateral "INFORMAÇÕES" (x=20) e coluna principal "EXPERIÊNCIA PROFISSIONAL" (x=78)
    await exportarElementoParaPdf({
      previa: { ...previaExemplo, layout: "moderno" },
    });
    expect(mockText).toHaveBeenCalledWith(
      "INFORMAÇÕES",
      20,
      expect.any(Number),
    );
    expect(mockText).toHaveBeenCalledWith(
      "EXPERIÊNCIA PROFISSIONAL",
      78,
      expect.any(Number),
    );

    vi.clearAllMocks();

    // 3. Primeiro emprego: faixa de cabeçalho roxa #5a3db5 (90, 61, 181)
    await exportarElementoParaPdf({
      previa: { ...previaExemplo, layout: "primeiro-emprego" },
    });
    expect(mockSetFillColor).toHaveBeenCalledWith(90, 61, 181);
    expect(mockText).toHaveBeenCalledWith(
      "CURRÍCULO",
      expect.any(Number),
      expect.any(Number),
    );

    vi.clearAllMocks();

    // 4. Acadêmico: destaque azul-petróleo #146384 (20, 99, 132) e "Experiência profissional relevante"
    await exportarElementoParaPdf({
      previa: { ...previaExemplo, layout: "academico" },
    });
    expect(mockSetTextColor).toHaveBeenCalledWith(20, 99, 132);
    expect(mockText).toHaveBeenCalledWith(
      "Experiência profissional relevante",
      20,
      expect.any(Number),
    );

    vi.clearAllMocks();

    // 5. ATS simples: destaque azul #397bd1 (57, 123, 209) e Experiência profissional no topo
    await exportarElementoParaPdf({
      previa: { ...previaExemplo, layout: "ats-simples" },
    });
    expect(mockSetTextColor).toHaveBeenCalledWith(57, 123, 209);
    expect(mockText).toHaveBeenCalledWith(
      "EXPERIÊNCIA PROFISSIONAL",
      22,
      expect.any(Number),
    );

    vi.clearAllMocks();

    // 6. Compacto: cabeçalho com linha azul #2563eb (37, 99, 235) e títulos sem uppercase
    await exportarElementoParaPdf({
      previa: { ...previaExemplo, layout: "compacto" },
    });
    expect(mockSetDrawColor).toHaveBeenCalledWith(37, 99, 235);
    expect(mockText).toHaveBeenCalledWith(
      "Formação acadêmica",
      16,
      expect.any(Number),
    );
  });

  it("permite fallback baseado em elemento HTML quando a prévia estruturada não é fornecida", async () => {
    const el = document.createElement("div");
    el.innerHTML = "<h1>Currículo de Teste</h1><p>Desenvolvedor Fullstack</p>";

    await exportarElementoParaPdf({
      elemento: el,
      nomeArquivo: "Curriculo - Fallback.pdf",
    });

    expect(mockText).toHaveBeenCalledWith(
      "Currículo de Teste",
      105,
      expect.any(Number),
      { align: "center" },
    );
    expect(mockSave).toHaveBeenCalledWith("Curriculo - Fallback.pdf");
  });
});
