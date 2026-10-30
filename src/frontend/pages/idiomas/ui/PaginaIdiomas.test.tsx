import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { PaginaIdiomas } from "./PaginaIdiomas";

describe("PaginaIdiomas", () => {
  it("compõe a seção de idiomas com título e formulário", () => {
    render(<PaginaIdiomas />);

    expect(
      screen.getByRole("heading", {
        level: 1,
        name: "Idiomas",
      }),
    ).toBeInTheDocument();

    expect(
      screen.queryByRole("heading", { level: 2, name: "Idiomas" }),
    ).not.toBeInTheDocument();

    expect(
      screen.queryByRole("button", { name: "Salvar idiomas" }),
    ).not.toBeInTheDocument();

    expect(screen.getByLabelText("Idioma")).toBeInTheDocument();
    expect(screen.getByLabelText("Nível de proficiência")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Avançar para próxima etapa" }),
    ).toBeInTheDocument();
  });
});
