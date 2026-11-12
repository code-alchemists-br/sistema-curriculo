import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import { exportarElementoParaPdf } from "../model/exportar-pdf-cliente";
import { PaginaVisualizacaoCurriculo } from "./PaginaVisualizacaoCurriculo";

vi.mock("../model/exportar-pdf-cliente", () => ({
  exportarElementoParaPdf: vi.fn().mockResolvedValue(undefined),
}));

afterEach(cleanup);

const previa: PreviaCurriculo = {
  curriculo_id: "curriculo-1",
  titulo_versao: "Currículo principal",
  layout: "classico",
  estudante: {
    nome: "Ana Silva",
    email: "ana@example.com",
    contato: null,
  },
  formacoes: [],
  experiencias: [],
  projetos: [],
  competencias: [],
  idiomas: [],
  documentos: [],
};

describe("PaginaVisualizacaoCurriculo", () => {
  it.each([
    ["classico", "Profissional clássico"],
    ["compacto", "Compacto"],
    ["ats-simples", "ATS simples"],
    ["criativo", "Criativo"],
    ["moderno", "Moderno"],
    ["academico", "Acadêmico"],
    ["primeiro-emprego", "Primeiro emprego"],
  ] as const)("apresenta o currículo no modelo %s", (modelo, rotulo) => {
    render(<PaginaVisualizacaoCurriculo modelo={modelo} previa={previa} />);

    expect(screen.getByText(/Modelo selecionado:/)).toHaveTextContent(rotulo);
    expect(
      screen.getByRole("heading", { name: "Ana Silva" }),
    ).toBeInTheDocument();
  });

  it("permite retornar à seleção quando a ação é fornecida", async () => {
    const usuario = userEvent.setup();
    const aoAlterarModelo = vi.fn();

    render(
      <PaginaVisualizacaoCurriculo
        aoAlterarModelo={aoAlterarModelo}
        modelo="classico"
        previa={previa}
      />,
    );

    await usuario.click(screen.getByRole("button", { name: "Alterar modelo" }));

    expect(aoAlterarModelo).toHaveBeenCalledOnce();
  });

  it("permite retornar para validação, início e disparar exportação quando as ações são fornecidas", async () => {
    const usuario = userEvent.setup();
    const onVoltar = vi.fn();
    const onVoltarInicio = vi.fn();
    const onExportarPdf = vi.fn();

    render(
      <PaginaVisualizacaoCurriculo
        modelo="classico"
        onExportarPdf={onExportarPdf}
        onVoltar={onVoltar}
        onVoltarInicio={onVoltarInicio}
        previa={previa}
      />,
    );

    await usuario.click(
      screen.getByRole("button", { name: "← Voltar para validação" }),
    );
    expect(onVoltar).toHaveBeenCalledOnce();

    await usuario.click(screen.getByRole("button", { name: "Início" }));
    expect(onVoltarInicio).toHaveBeenCalledOnce();

    await usuario.click(screen.getByRole("button", { name: "Baixar PDF" }));
    expect(onExportarPdf).toHaveBeenCalledOnce();
    expect(
      await screen.findByText(
        "Currículo baixado com sucesso em seu dispositivo!",
      ),
    ).toBeInTheDocument();
  });

  it("exibe mensagem de erro acessível quando a exportação falha", async () => {
    vi.mocked(exportarElementoParaPdf).mockRejectedValueOnce(
      new Error("Falha simulada de exportação"),
    );
    const usuario = userEvent.setup();

    render(<PaginaVisualizacaoCurriculo modelo="classico" previa={previa} />);

    await usuario.click(screen.getByRole("button", { name: "Baixar PDF" }));
    expect(await screen.findByRole("alert")).toHaveTextContent(
      /Não foi possível gerar o arquivo PDF/i,
    );
  });
});
