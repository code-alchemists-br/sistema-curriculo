import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { PaginaTermosDeUso } from "./PaginaTermosDeUso";

afterEach(cleanup);

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

  it("permite voltar ao início pelo botão de retorno no cabeçalho", async () => {
    const usuario = userEvent.setup();
    const onNavegarInicio = vi.fn();

    render(<PaginaTermosDeUso onNavegarInicio={onNavegarInicio} />);

    expect(
      screen.getByRole("button", { name: "← Voltar ao início" }),
    ).toBeInTheDocument();

    await usuario.click(
      screen.getByRole("button", { name: "← Voltar ao início" }),
    );

    expect(onNavegarInicio).toHaveBeenCalledTimes(1);
  });
});
