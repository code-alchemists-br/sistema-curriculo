import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { PaginaCursosIdiomas } from "./PaginaCursosIdiomas";

describe("PaginaCursosIdiomas", () => {
  it("compõe as seções de cursos e certificações como alias retrocompatível", () => {
    render(<PaginaCursosIdiomas />);

    expect(
      screen.getByRole("heading", {
        level: 1,
        name: "Cursos e Certificações",
      }),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { level: 2, name: "Cursos" }),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { level: 2, name: "Certificações" }),
    ).toBeInTheDocument();

    expect(screen.getByLabelText("Nome do curso")).toBeInTheDocument();
    expect(screen.getByLabelText("Nome da certificação")).toBeInTheDocument();
  });
});
