import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { PaginaCursosIdiomas } from "./PaginaCursosIdiomas";

describe("PaginaCursosIdiomas", () => {
  it("compõe as seções de cursos, certificações e idiomas com seus títulos e formulários", () => {
    render(<PaginaCursosIdiomas />);

    expect(
      screen.getByRole("heading", {
        level: 1,
        name: "Cursos, Certificações e Idiomas",
      }),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { level: 2, name: "Cursos e Certificações" }),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { level: 2, name: "Certificações" }),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { level: 2, name: "Idiomas" }),
    ).toBeInTheDocument();

    expect(screen.getByLabelText("Nome da certificação")).toBeInTheDocument();
    expect(screen.getByLabelText("Organização emissora")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Salvar certificação" }),
    ).toBeInTheDocument();
  });
});
