import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { AlternadorModeloCurriculo } from "./AlternadorModeloCurriculo";

afterEach(cleanup);

describe("AlternadorModeloCurriculo", () => {
  it("expõe opções rotuladas e marca o modelo selecionado", () => {
    render(
      <AlternadorModeloCurriculo
        modeloSelecionado="compacto"
        onSelecionarModelo={vi.fn()}
      />,
    );

    expect(screen.getByRole("radio", { name: "Clássico" })).not.toBeChecked();
    expect(screen.getByRole("radio", { name: "Compacto" })).toBeChecked();
  });

  it("comunica a seleção de outro modelo", async () => {
    const usuario = userEvent.setup();
    const aoSelecionarModelo = vi.fn();

    render(
      <AlternadorModeloCurriculo
        modeloSelecionado="classico"
        onSelecionarModelo={aoSelecionarModelo}
      />,
    );

    await usuario.click(screen.getByRole("radio", { name: "Compacto" }));

    expect(aoSelecionarModelo).toHaveBeenCalledWith("compacto");
  });
});
