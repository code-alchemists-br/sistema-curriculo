import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { PaginaPoliticaDePrivacidade } from "./PaginaPoliticaDePrivacidade";

afterEach(cleanup);

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
    expect(
      screen.getAllByText(/prazo geral de retenção/i).length,
    ).toBeGreaterThan(0);
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

  it("permite voltar ao início pelo botão de retorno no cabeçalho", async () => {
    const usuario = userEvent.setup();
    const onNavegarInicio = vi.fn();

    render(<PaginaPoliticaDePrivacidade onNavegarInicio={onNavegarInicio} />);

    expect(
      screen.getByRole("button", { name: "← Voltar ao início" }),
    ).toBeInTheDocument();

    await usuario.click(
      screen.getByRole("button", { name: "← Voltar ao início" }),
    );

    expect(onNavegarInicio).toHaveBeenCalledTimes(1);
  });
});
