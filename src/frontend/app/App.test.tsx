import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it } from "vitest";

import { App } from "./App";

afterEach(() => {
  cleanup();
  window.history.replaceState({}, "", "/");
});

describe("App", () => {
  it("apresenta a porta de entrada com a seção hero e permite acessar a conta", async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(
      screen.getByRole("heading", { name: "O currículo que abre portas" }),
    ).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Fazer login" }));

    expect(
      screen.getByRole("heading", { name: "Conecte-se na LIMINAL" }),
    ).toBeInTheDocument();
  });

  it("navega entre os documentos públicos pela URL e pelos controles da tela", async () => {
    const user = userEvent.setup();
    window.history.replaceState({}, "", "/?etapa=termos-de-uso");

    render(<App />);

    expect(
      screen.getByRole("heading", { level: 1, name: "Termos de Uso" }),
    ).toBeInTheDocument();

    await user.click(
      screen.getByRole("button", { name: "Ler Política de Privacidade" }),
    );

    expect(
      screen.getByRole("heading", {
        level: 1,
        name: "Política de Privacidade",
      }),
    ).toBeInTheDocument();
  });
});
