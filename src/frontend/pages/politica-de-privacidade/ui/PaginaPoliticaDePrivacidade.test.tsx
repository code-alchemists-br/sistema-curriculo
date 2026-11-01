import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { PaginaPoliticaDePrivacidade } from "./PaginaPoliticaDePrivacidade";

describe("PaginaPoliticaDePrivacidade", () => {
  it("apresenta os dados tratados e os limites conhecidos da política", () => {
    render(<PaginaPoliticaDePrivacidade />);

    expect(
      screen.getByRole("heading", {
        level: 1,
        name: "Política de Privacidade",
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { level: 2, name: "1. Dados tratados" }),
    ).toBeInTheDocument();
    expect(screen.getByText(/prazo geral de retenção/i)).toBeInTheDocument();
    expect(screen.getByRole("note")).toBeInTheDocument();
  });

  it("encaminha a pessoa para os termos de uso", async () => {
    const usuario = userEvent.setup();
    const onNavegarTermosDeUso = vi.fn();

    render(
      <PaginaPoliticaDePrivacidade
        onNavegarTermosDeUso={onNavegarTermosDeUso}
      />,
    );

    await usuario.click(
      screen.getByRole("button", { name: "Ler Termos de Uso" }),
    );

    expect(onNavegarTermosDeUso).toHaveBeenCalledTimes(1);
  });
});
