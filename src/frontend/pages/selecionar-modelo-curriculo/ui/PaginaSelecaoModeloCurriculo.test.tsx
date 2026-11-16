import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { PaginaSelecaoModeloCurriculo } from "./PaginaSelecaoModeloCurriculo";

afterEach(cleanup);

describe("PaginaSelecaoModeloCurriculo", () => {
  it("orienta pelo objetivo sem restringir a escolha e confirma um modelo oficial", async () => {
    const usuario = userEvent.setup();
    const aoConfirmar = vi.fn();

    render(<PaginaSelecaoModeloCurriculo aoConfirmar={aoConfirmar} />);

    await usuario.selectOptions(
      screen.getByLabelText("Objetivo do currículo"),
      "tecnologia",
    );

    expect(screen.getByRole("status")).toHaveTextContent("Moderno");

    await usuario.click(screen.getByRole("radio", { name: "Acadêmico" }));
    await usuario.click(
      screen.getByRole("button", {
        name: "Continuar com o modelo selecionado",
      }),
    );

    expect(aoConfirmar).toHaveBeenCalledWith("academico");
  });

  it("preserva o compacto quando ele é o modelo inicialmente selecionado", () => {
    render(
      <PaginaSelecaoModeloCurriculo
        aoConfirmar={vi.fn()}
        modeloInicial="compacto"
      />,
    );

    expect(screen.getByRole("radio", { name: "Compacto" })).toBeChecked();
  });

  it("pré-seleciona automaticamente o modelo Primeiro emprego para perfil sem experiência prévia", () => {
    render(
      <PaginaSelecaoModeloCurriculo
        aoConfirmar={vi.fn()}
        perfilEstudante={{
          experiencias: [],
          formacoes: [{ nivel: "graduacao" }],
        }}
      />,
    );

    expect(
      screen.getByRole("radio", { name: "Primeiro emprego" }),
    ).toBeChecked();
    expect(screen.getByText("★ Recomendado")).toBeInTheDocument();
  });

  it("sincroniza o seletor de objetivo com o modeloInicial e atualiza ao clicar nos cards", async () => {
    const usuario = userEvent.setup();
    const aoAlterarInstantaneo = vi.fn();

    render(
      <PaginaSelecaoModeloCurriculo
        aoAlterarModeloInstantaneo={aoAlterarInstantaneo}
        aoConfirmar={vi.fn()}
        modeloInicial="criativo"
        perfilEstudante={{
          experiencias: [],
          formacoes: [{ nivel: "doutorado" }],
        }}
      />,
    );

    const selectObjetivo = screen.getByLabelText(
      "Objetivo do currículo",
    ) as HTMLSelectElement;
    expect(selectObjetivo.value).toBe("criativo-design");
    expect(screen.getByRole("radio", { name: "Criativo" })).toBeChecked();

    // Mesmo tendo vindo com Criativo selecionado, o usuário pode selecionar Acadêmico pelo select ou card
    await usuario.selectOptions(selectObjetivo, "academico-pesquisador");
    expect(screen.getByRole("radio", { name: "Acadêmico" })).toBeChecked();
    expect(aoAlterarInstantaneo).toHaveBeenCalledWith("academico");
  });
});
