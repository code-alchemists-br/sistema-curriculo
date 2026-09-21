// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { App } from "./App";

describe("App", () => {
  it("apresenta a porta de entrada para a conta do estudante", () => {
    render(<App />);

    expect(
      screen.getByRole("heading", { name: "Acesse sua conta" })
    ).toBeInTheDocument();
  });
});
