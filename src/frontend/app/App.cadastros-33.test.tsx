import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterAll, afterEach, describe, expect, it, vi } from "vitest";

vi.hoisted(() => {
  vi.stubEnv("VITE_API_URL", "http://127.0.0.1:8000");
});

import { App } from "./App";

afterAll(() => vi.unstubAllEnvs());
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
  localStorage.clear();
  sessionStorage.clear();
  window.history.replaceState({}, "", "/");
});

/** Inicializa somente armazenamento e rota locais para exercitar o App real sem depender de conta ou rede externas. */
function preparar(etapa: string, email = "estudante@example.invalid"): void {
  window.history.replaceState({}, "", `/?etapa=${etapa}`);
  sessionStorage.setItem(
    "liminal_usuario_sessao",
    JSON.stringify({ nome: "Estudante de teste", email }),
  );
  localStorage.setItem(
    "liminal_curriculo_rascunho",
    JSON.stringify({
      cursos: [{ nome: " React ", instituicao: " Fatec ", cargaHoraria: "40" }],
      certificacoes: [{ nome: " AWS ", organizacaoEmissora: " Amazon " }],
      idiomas: [{ nome: " Inglês ", nivel: "avancado" }],
    }),
  );
}

describe("App: cadastros da issue 33 com HTTP substituído por doubles", () => {
  it("não navega nem perde o rascunho quando o cadastro de curso falha", async () => {
    preparar("cursos-certificacoes");
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 401 }));
    render(<App />);
    await userEvent.click(
      screen.getByRole("button", { name: "Avançar para próxima etapa" }),
    );
    expect(await screen.findByRole("alert")).toHaveTextContent(
      /não foi possível salvar/i,
    );
    expect(window.location.search).toBe("?etapa=cursos-certificacoes");
    expect(screen.getByLabelText("Nome do curso")).toHaveValue(" React ");
    expect(requisitar).toHaveBeenCalledTimes(1);
    expect(localStorage.getItem("liminal_curriculo_rascunho")).toContain(
      "React",
    );
  });

  it("preserva sucesso parcial e tenta somente certificações pendentes ao repetir", async () => {
    preparar("cursos-certificacoes");
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(null, { status: 201 }))
      .mockResolvedValueOnce(new Response(null, { status: 503 }))
      .mockResolvedValueOnce(new Response(null, { status: 201 }));
    render(<App />);
    const proximo = screen.getByRole("button", {
      name: "Avançar para próxima etapa",
    });
    await userEvent.click(proximo);
    expect(await screen.findByRole("alert")).toBeInTheDocument();
    await userEvent.click(proximo);
    await screen.findByRole("heading", { name: "Idiomas", level: 1 });
    expect(requisitar.mock.calls.map(([url]) => url)).toEqual([
      "http://127.0.0.1:8000/cursos",
      "http://127.0.0.1:8000/certificacoes",
      "http://127.0.0.1:8000/certificacoes",
    ]);
  });

  it("mantém idioma e rota quando HTTP rejeita e avança após nova tentativa bem-sucedida", async () => {
    preparar("idiomas");
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(null, { status: 422 }))
      .mockResolvedValueOnce(new Response(null, { status: 201 }));
    render(<App />);
    const proximo = screen.getByRole("button", {
      name: "Avançar para próxima etapa",
    });
    await userEvent.click(proximo);
    expect(await screen.findByRole("alert")).toBeInTheDocument();
    expect(window.location.search).toBe("?etapa=idiomas");
    await userEvent.click(proximo);
    await waitFor(() =>
      expect(window.location.search).toBe("?etapa=competencias"),
    );
    expect(JSON.parse(requisitar.mock.calls[1][1]?.body as string)).toEqual({
      idioma: "Inglês",
      nivel: "avancado",
    });
  });

  it("não compartilha confirmações de cadastro entre instâncias de contas distintas", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockImplementation(async () => new Response(null, { status: 201 }));
    preparar("idiomas", "conta-a@example.invalid");
    const primeira = render(<App />);
    await userEvent.click(
      screen.getByRole("button", { name: "Avançar para próxima etapa" }),
    );
    await waitFor(() =>
      expect(window.location.search).toBe("?etapa=competencias"),
    );
    primeira.unmount();
    preparar("idiomas", "conta-b@example.invalid");
    render(<App />);
    await userEvent.click(
      screen.getByRole("button", { name: "Avançar para próxima etapa" }),
    );
    await waitFor(() =>
      expect(window.location.search).toBe("?etapa=competencias"),
    );
    expect(
      requisitar.mock.calls.filter(([url]) => String(url).endsWith("/idiomas")),
    ).toHaveLength(2);
  });
});
