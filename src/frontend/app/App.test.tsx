import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it } from "vitest";

import { App } from "./App";

afterEach(cleanup);

describe("App", () => {
  it("apresenta a porta de entrada com a seção hero e permite acessar a conta", async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(
      screen.getByRole("heading", { name: "O currículo que abre portas" }),
    ).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Fazer login" }));

    expect(
      screen.getByRole("heading", { name: "Acesse sua conta" }),
    ).toBeInTheDocument();
  });
});
