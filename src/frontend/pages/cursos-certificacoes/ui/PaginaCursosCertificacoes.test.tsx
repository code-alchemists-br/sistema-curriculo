import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { PaginaCursosCertificacoes } from "./PaginaCursosCertificacoes";

describe("PaginaCursosCertificacoes", () => {
  it("compõe as seções de cursos e certificações com seus títulos e formulários", () => {
    render(<PaginaCursosCertificacoes />);

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
    expect(screen.getByLabelText("Organização emissora")).toBeInTheDocument();

    expect(
      screen.getByPlaceholderText(
        "Ex.: AWS Certified Solutions Architect, Scrum Master...",
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Ex.: Amazon Web Services, Scrum.org..."),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: "+ Adicionar curso" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "+ Adicionar certificação" }),
    ).toBeInTheDocument();

    expect(
      screen.queryByRole("button", { name: "Salvar cursos" }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: "Salvar certificação" }),
    ).not.toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: "Avançar para próxima etapa" }),
    ).toBeInTheDocument();
  });
});
