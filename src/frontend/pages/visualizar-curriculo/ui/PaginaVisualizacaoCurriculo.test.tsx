import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import { PaginaVisualizacaoCurriculo } from "./PaginaVisualizacaoCurriculo";

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
});
