import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { CabecalhoPublico } from "./CabecalhoPublico";

afterEach(cleanup);

describe("CabecalhoPublico", () => {
  it("renderiza a marca LIMINAL e as ações públicas de login e cadastro", () => {
    render(<CabecalhoPublico />);

    expect(screen.getByText("LIMINAL")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Fazer login" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Criar conta" }),
    ).toBeInTheDocument();
  });

  it("aciona callbacks correspondentes nos botões de navegação", async () => {
    const onLogin = vi.fn();
    const onCadastro = vi.fn();
    const user = userEvent.setup();

    render(
      <CabecalhoPublico
        onNavegarLogin={onLogin}
        onNavegarCadastro={onCadastro}
      />,
    );

    await user.click(screen.getByRole("button", { name: "Fazer login" }));
    expect(onLogin).toHaveBeenCalledTimes(1);

    await user.click(screen.getByRole("button", { name: "Criar conta" }));
    expect(onCadastro).toHaveBeenCalledTimes(1);
  });

  it("aciona callback ao clicar na logo LIMINAL para voltar ao início", async () => {
    const onInicio = vi.fn();
    const user = userEvent.setup();

    render(<CabecalhoPublico onNavegarInicio={onInicio} />);

    await user.click(screen.getByRole("button", { name: /LIMINAL/i }));
    expect(onInicio).toHaveBeenCalledTimes(1);
  });
});
