import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { PaginaTermosDeUso } from "./PaginaTermosDeUso";

describe("PaginaTermosDeUso", () => {
  it("apresenta a estrutura semântica e o aviso sobre a versão informativa", () => {
    render(<PaginaTermosDeUso />);

    expect(
      screen.getByRole("heading", { level: 1, name: "Termos de Uso" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", {
        level: 2,
        name: "1. Finalidade da plataforma",
      }),
    ).toBeInTheDocument();
    expect(screen.getByRole("note")).toHaveTextContent(
      "Versão em desenvolvimento.",
    );
    expect(screen.getByRole("main")).toBeInTheDocument();
  });

  it("encaminha a pessoa para a política de privacidade", async () => {
    const usuario = userEvent.setup();
    const onNavegarPoliticaDePrivacidade = vi.fn();

    render(
      <PaginaTermosDeUso
        onNavegarPoliticaDePrivacidade={onNavegarPoliticaDePrivacidade}
      />,
    );

    await usuario.click(
      screen.getByRole("button", { name: "Ler Política de Privacidade" }),
    );

    expect(onNavegarPoliticaDePrivacidade).toHaveBeenCalledTimes(1);
  });
});
