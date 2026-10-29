import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { AlternadorModeloCurriculo } from "./AlternadorModeloCurriculo";

afterEach(cleanup);

describe("AlternadorModeloCurriculo", () => {
  it("expõe todos os sete modelos com uma miniatura estrutural própria", () => {
    const { container } = render(
      <AlternadorModeloCurriculo
        modeloSelecionado="moderno"
        onSelecionarModelo={vi.fn()}
      />,
    );

    expect(
      screen.getByRole("radio", { name: "ATS simples" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("radio", { name: "Profissional clássico" }),
    ).toBeInTheDocument();
    expect(screen.getByRole("radio", { name: "Compacto" })).toBeInTheDocument();
    expect(screen.getByRole("radio", { name: "Moderno" })).toBeChecked();
    expect(screen.getByRole("radio", { name: "Criativo" })).toBeInTheDocument();
    expect(
      screen.getByRole("radio", { name: "Acadêmico" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("radio", { name: "Primeiro emprego" }),
    ).toBeInTheDocument();
    expect(
      container.querySelector(".miniatura-modelo--ats-simples"),
    ).toBeInTheDocument();
    expect(
      container.querySelector(".miniatura-modelo--classico"),
    ).toBeInTheDocument();
    expect(
      container.querySelector(".miniatura-modelo--compacto"),
    ).toBeInTheDocument();
    expect(
      container.querySelector(".miniatura-modelo--moderno"),
    ).toBeInTheDocument();
    expect(
      container.querySelector(".miniatura-modelo--criativo"),
    ).toBeInTheDocument();
    expect(
      container.querySelector(".miniatura-modelo--academico"),
    ).toBeInTheDocument();
    expect(
      container.querySelector(".miniatura-modelo--primeiro-emprego"),
    ).toBeInTheDocument();
    expect(
      container.querySelector(".miniatura-modelo__lateral-criativa"),
    ).toBeInTheDocument();
    expect(
      container.querySelector(".miniatura-modelo__duas-colunas"),
    ).toBeInTheDocument();
  });

  it("comunica a seleção de um modelo do catálogo", async () => {
    const usuario = userEvent.setup();
    const aoSelecionarModelo = vi.fn();

    render(
      <AlternadorModeloCurriculo
        modeloSelecionado="classico"
        onSelecionarModelo={aoSelecionarModelo}
      />,
    );

    await usuario.click(screen.getByRole("radio", { name: "Acadêmico" }));

    expect(aoSelecionarModelo).toHaveBeenCalledWith("academico");
  });
});
