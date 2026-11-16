import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { PaginaInicio } from "./PaginaInicio";

afterEach(cleanup);

describe("PaginaInicio com currículo pronto", () => {
  it("dá destaque às vagas e leva ao perfil para quem já tem currículo", async () => {
    const onNavegarVagas = vi.fn();
    const onNavegarPerfil = vi.fn();
    render(
      <PaginaInicio
        onNavegarPerfil={onNavegarPerfil}
        onNavegarVagas={onNavegarVagas}
        temCurriculoPronto
        usuarioLogado={{ nome: "Ana Souza", email: "ana@example.com" }}
      />,
    );

    expect(
      screen.getByText("✓ Ana, seu currículo está pronto"),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", {
        name: "Agora é hora de encontrar sua vaga",
      }),
    ).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: "VER VAGAS →" }));
    await userEvent.click(
      screen.getByRole("button", { name: "Ver meu currículo" }),
    );

    expect(onNavegarVagas).toHaveBeenCalled();
    expect(onNavegarPerfil).toHaveBeenCalled();
  });

  it("mantém o convite para criar o currículo quando ele ainda não está pronto", () => {
    render(
      <PaginaInicio
        onNavegarVagas={vi.fn()}
        temCurriculoPronto={false}
        usuarioLogado={{ nome: "Ana", email: "ana@example.com" }}
      />,
    );

    expect(
      screen.getByRole("heading", { name: "O currículo que abre portas" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "CRIAR CURRÍCULO →" }),
    ).toBeInTheDocument();
  });
});
