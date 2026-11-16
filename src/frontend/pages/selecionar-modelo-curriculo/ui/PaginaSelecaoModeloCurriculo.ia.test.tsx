import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterAll, afterEach, describe, expect, it, vi } from "vitest";

vi.hoisted(() => {
  vi.stubEnv("VITE_API_URL", "http://127.0.0.1:8000");
});

import { PaginaSelecaoModeloCurriculo } from "./PaginaSelecaoModeloCurriculo";

afterAll(() => vi.unstubAllEnvs());
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("PaginaSelecaoModeloCurriculo com recomendação da IA", () => {
  it("mostra só a recomendação da IA e seleciona o modelo indicado", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(
        JSON.stringify({
          modelo: "primeiro-emprego",
          motivo: "Seu perfil tem pouca experiência.",
          alternativa: "moderno",
        }),
        { status: 200 },
      ),
    );
    render(
      <PaginaSelecaoModeloCurriculo
        aoConfirmar={vi.fn()}
        perfilEstudante={{ experiencias: [] }}
      />,
    );

    expect(
      await screen.findByText(/IA recomenda: Primeiro emprego/),
    ).toBeInTheDocument();
    expect(
      screen.queryByText(/^Recomendamos o modelo/),
    ).not.toBeInTheDocument();
    expect(requisitar).toHaveBeenCalledTimes(1);
  });

  it("volta à recomendação por regras ao trocar o objetivo, sem nova chamada", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(
        JSON.stringify({
          modelo: "moderno",
          motivo: "Técnico.",
          alternativa: null,
        }),
        { status: 200 },
      ),
    );
    render(
      <PaginaSelecaoModeloCurriculo
        aoConfirmar={vi.fn()}
        perfilEstudante={{}}
      />,
    );
    await screen.findByText(/IA recomenda: Moderno/);

    await userEvent.selectOptions(
      screen.getByLabelText("Objetivo do currículo"),
      "academico-pesquisador",
    );

    await waitFor(() =>
      expect(
        screen.getByText(/^Recomendamos o modelo Acadêmico/),
      ).toBeInTheDocument(),
    );
    expect(screen.queryByText(/IA recomenda/)).not.toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "✦ Recomendar modelo com IA" }),
    ).toBeInTheDocument();
    expect(requisitar).toHaveBeenCalledTimes(1);
  });

  it("mantém a recomendação por regras quando a IA está indisponível", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ detail: "Sem chave." }), { status: 503 }),
    );
    render(
      <PaginaSelecaoModeloCurriculo
        aoConfirmar={vi.fn()}
        perfilEstudante={{}}
      />,
    );

    expect(await screen.findByRole("alert")).toHaveTextContent("Sem chave.");
    expect(screen.getByText(/^Recomendamos o modelo/)).toBeInTheDocument();
  });
});
