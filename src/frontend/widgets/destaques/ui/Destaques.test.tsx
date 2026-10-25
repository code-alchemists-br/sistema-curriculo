import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { Destaques } from "./Destaques";

afterEach(cleanup);

describe("Destaques", () => {
  it("renderiza o título da seção de métricas com destaque e fechamento", () => {
    render(<Destaques />);

    expect(
      screen.getByRole("heading", {
        name: /CONSTRUÍMOS A PONTE ENTRE O SEU TALENTO/i,
        level: 2,
      }),
    ).toBeInTheDocument();
  });

  it("renderiza os 3 blocos de métricas com seus valores e descrições", () => {
    render(<Destaques />);

    expect(screen.getByText("< 10 min")).toBeInTheDocument();
    expect(screen.getByText(/Do cadastro ao currículo/i)).toBeInTheDocument();

    expect(screen.getByText("100%")).toBeInTheDocument();
    expect(screen.getByText(/Gratuito e sem/i)).toBeInTheDocument();

    expect(screen.getByText("2 formatos")).toBeInTheDocument();
    expect(screen.getByText(/Prontos para envio:/i)).toBeInTheDocument();
  });
});
