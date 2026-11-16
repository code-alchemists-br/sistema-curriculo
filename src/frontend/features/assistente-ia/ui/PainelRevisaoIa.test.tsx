import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { registrarRevisao } from "../model/revisao";
import { PainelRevisaoIa } from "./PainelRevisaoIa";

afterEach(cleanup);

describe("PainelRevisaoIa", () => {
  it("avisa que a revisão acontece ao avançar quando ainda não revisou", () => {
    render(
      <PainelRevisaoIa
        aoAplicarTexto={vi.fn()}
        aoMudarMemoria={vi.fn()}
        id="p"
        memoria={{ iaIndisponivel: false }}
        texto="Fiz um app."
      />,
    );

    expect(
      screen.getByText(/revisa este texto quando você clicar em Próximo/),
    ).toBeInTheDocument();
  });

  it("mostra o texto aprovado com sugestões opcionais e aplica a escolhida", async () => {
    const aoAplicarTexto = vi.fn();
    const aoMudarMemoria = vi.fn();
    const memoria = registrarRevisao("Fiz um app.", {
      situacao: "melhorado",
      motivo: "Dá para detalhar.",
      sugestoes: ["Desenvolvi um app.", "Criei um aplicativo."],
      podeManterTexto: true,
    });
    render(
      <PainelRevisaoIa
        aoAplicarTexto={aoAplicarTexto}
        aoMudarMemoria={aoMudarMemoria}
        id="p"
        memoria={memoria}
        texto="Fiz um app."
      />,
    );

    expect(
      screen.getByText(/As sugestões abaixo são opcionais/),
    ).toBeInTheDocument();
    await userEvent.click(
      screen.getByRole("button", { name: "Usar sugestão 2" }),
    );

    expect(aoAplicarTexto).toHaveBeenCalledWith("Criei um aplicativo.");
    expect(aoMudarMemoria).toHaveBeenCalledWith(
      expect.objectContaining({ aprovadoPara: "Criei um aplicativo." }),
    );
  });

  it("pede reescrita e oferece modelos quando o texto é inválido", () => {
    const memoria = registrarRevisao("fazia coisas", {
      situacao: "invalido",
      motivo: "Muito vago.",
      sugestoes: ["Atuei em [área]."],
      podeManterTexto: false,
    });
    render(
      <PainelRevisaoIa
        aoAplicarTexto={vi.fn()}
        aoMudarMemoria={vi.fn()}
        id="p"
        memoria={memoria}
        texto="fazia coisas"
      />,
    );

    expect(
      screen.getByText("Reescreva o texto ou use um modelo abaixo."),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Usar modelo 1" }),
    ).toBeInTheDocument();
  });
});
