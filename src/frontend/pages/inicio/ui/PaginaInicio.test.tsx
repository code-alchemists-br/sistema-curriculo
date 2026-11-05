import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { PaginaInicio } from "./PaginaInicio";

afterEach(cleanup);

describe("PaginaInicio", () => {
  it("compõe o cabeçalho, a seção hero e a seção de destaques", () => {
    render(<PaginaInicio />);

    expect(screen.getByText("LIMINAL")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "O currículo que abre portas" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", {
        name: /CONSTRUÍMOS A PONTE ENTRE O SEU TALENTO/i,
      }),
    ).toBeInTheDocument();
  });

  it("repassa ações de cadastro e login", async () => {
    const onCadastro = vi.fn();
    const onLogin = vi.fn();
    const user = userEvent.setup();

    render(
      <PaginaInicio onNavegarCadastro={onCadastro} onNavegarLogin={onLogin} />,
    );

    await user.click(
      screen.getByRole("button", { name: /CRIAR CURRÍCULO →/i }),
    );
    expect(onCadastro).toHaveBeenCalledTimes(1);

    await user.click(screen.getByRole("button", { name: "Fazer login" }));
    expect(onLogin).toHaveBeenCalledTimes(1);
  });

  it("expõe os documentos públicos quando as navegações são disponibilizadas", async () => {
    const usuario = userEvent.setup();
    const onNavegarTermosDeUso = vi.fn();
    const onNavegarPoliticaDePrivacidade = vi.fn();

    render(
      <PaginaInicio
        onNavegarPoliticaDePrivacidade={onNavegarPoliticaDePrivacidade}
        onNavegarTermosDeUso={onNavegarTermosDeUso}
      />,
    );

    await usuario.click(screen.getByRole("button", { name: "Termos de Uso" }));
    await usuario.click(
      screen.getByRole("button", { name: "Política de Privacidade" }),
    );

    expect(onNavegarTermosDeUso).toHaveBeenCalledTimes(1);
    expect(onNavegarPoliticaDePrivacidade).toHaveBeenCalledTimes(1);
  });
});
