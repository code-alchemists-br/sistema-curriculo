import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { Hero } from "./Hero";

afterEach(cleanup);

describe("Hero", () => {
  it("renderiza o título principal, subtítulo e o botão de ação", () => {
    render(<Hero />);

    expect(
      screen.getByRole("heading", {
        name: "O currículo que abre portas",
        level: 1,
      }),
    ).toBeInTheDocument();

    expect(
      screen.getByText(/Você já aprendeu muita coisa na faculdade/i),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: /CRIAR CURRÍCULO →/i }),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("img", {
        name: /Demonstração visual do currículo gerado pela plataforma LIMINAL/i,
      }),
    ).toBeInTheDocument();
  });

  it("chama o callback onCriarCurriculo ao acionar o CTA", async () => {
    const onCriarCurriculo = vi.fn();
    const user = userEvent.setup();

    render(<Hero onCriarCurriculo={onCriarCurriculo} />);

    await user.click(
      screen.getByRole("button", { name: /CRIAR CURRÍCULO →/i }),
    );

    expect(onCriarCurriculo).toHaveBeenCalledTimes(1);
  });
});
