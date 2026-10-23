import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { PaginaSelecaoModeloCurriculo } from "./PaginaSelecaoModeloCurriculo";

afterEach(cleanup);

describe("PaginaSelecaoModeloCurriculo", () => {
  it("orienta pelo objetivo e confirma um modelo já suportado", async () => {
    const usuario = userEvent.setup();
    const aoConfirmar = vi.fn();

    render(<PaginaSelecaoModeloCurriculo aoConfirmar={aoConfirmar} />);

    await usuario.selectOptions(
      screen.getByLabelText("Objetivo do currículo"),
      "tecnologia",
    );
    expect(screen.getByRole("status")).toHaveTextContent("Compacto");

    await usuario.click(screen.getByRole("radio", { name: "Compacto" }));
    await usuario.click(
      screen.getByRole("button", {
        name: "Continuar com o modelo selecionado",
      }),
    );

    expect(aoConfirmar).toHaveBeenCalledWith("compacto");
  });
});
