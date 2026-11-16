import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterAll, afterEach, describe, expect, it, vi } from "vitest";

vi.hoisted(() => {
  vi.stubEnv("VITE_API_URL", "http://127.0.0.1:8000");
});

import { App } from "./App";

const API = "http://127.0.0.1:8000/estudantes/me/curriculo";

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

/** Currículo que o banco simulado devolve ao abrir o App, igual ao rascunho. */
function curriculoSalvo(email: string) {
  return {
    dados_pessoais: { nome: "Estudante de teste", email, telefones: [] },
    formacoes: [],
    experiencias: [],
    projetos: [],
    competencias: [],
    cursos: [{ nome: "React", instituicao: "Fatec", carga_horaria: 40 }],
    certificacoes: [{ nome: "AWS", organizacao_emissora: "Amazon" }],
    idiomas: [{ idioma: "Inglês", nivel: "avancado" }],
    modelo: null,
  };
}

/**
 * Substitui a API: o GET devolve o currículo salvo e cada PUT consome a
 * próxima resposta da fila (204 quando a fila acaba).
 */
function simularApi(respostasPut: Response[] = [], email?: string) {
  const fila = [...respostasPut];
  return vi
    .spyOn(globalThis, "fetch")
    .mockImplementation(async (_url, init) => {
      if ((init?.method ?? "GET") === "GET") {
        return new Response(
          JSON.stringify(curriculoSalvo(email ?? "estudante@example.invalid")),
          { status: 200 },
        );
      }
      return fila.shift() ?? new Response(null, { status: 204 });
    });
}

/** Lista as chamadas PUT feitas ao salvar etapas. */
function puts(requisitar: ReturnType<typeof simularApi>) {
  return requisitar.mock.calls.filter(([, init]) => init?.method === "PUT");
}

const avancar = () =>
  screen.findByRole("button", { name: "Avançar para próxima etapa" });

describe("App: cadastros da issue 33 salvos por substituição no banco", () => {
  it("não navega nem perde o rascunho quando salvar cursos falha", async () => {
    preparar("cursos-certificacoes");
    const requisitar = simularApi([new Response(null, { status: 503 })]);
    render(<App />);
    await userEvent.click(await avancar());
    expect(await screen.findByRole("alert")).toHaveTextContent(
      /não foi possível salvar/i,
    );
    expect(window.location.search).toBe("?etapa=cursos-certificacoes");
    expect(screen.getByLabelText("Nome do curso")).toHaveValue("React");
    expect(puts(requisitar)).toHaveLength(1);
    expect(localStorage.getItem("liminal_curriculo_rascunho")).toContain(
      "React",
    );
  });

  it("repete o salvamento das duas seções após falha parcial, sem duplicar", async () => {
    preparar("cursos-certificacoes");
    const requisitar = simularApi([
      new Response(null, { status: 204 }),
      new Response(null, { status: 503 }),
    ]);
    render(<App />);
    const proximo = await avancar();
    await userEvent.click(proximo);
    expect(await screen.findByRole("alert")).toBeInTheDocument();
    await userEvent.click(proximo);
    await screen.findByRole("heading", { name: "Idiomas", level: 1 });
    expect(puts(requisitar).map(([url]) => url)).toEqual([
      `${API}/cursos`,
      `${API}/certificacoes`,
      `${API}/cursos`,
      `${API}/certificacoes`,
    ]);
  });

  it("mantém idioma e rota quando a API rejeita e avança após nova tentativa", async () => {
    preparar("idiomas");
    const requisitar = simularApi([
      new Response(JSON.stringify({ detail: "inválido" }), { status: 422 }),
    ]);
    render(<App />);
    const proximo = await avancar();
    await userEvent.click(proximo);
    expect(await screen.findByRole("alert")).toBeInTheDocument();
    expect(window.location.search).toBe("?etapa=idiomas");
    await userEvent.click(proximo);
    await waitFor(() =>
      expect(window.location.search).toBe("?etapa=competencias"),
    );
    expect(JSON.parse(puts(requisitar)[1][1]?.body as string)).toEqual({
      itens: [{ idioma: "Inglês", nivel: "avancado" }],
    });
  });

  it("cada conta salva os próprios idiomas", async () => {
    const requisitar = simularApi();
    preparar("idiomas", "conta-a@example.invalid");
    const primeira = render(<App />);
    await userEvent.click(await avancar());
    await waitFor(() =>
      expect(window.location.search).toBe("?etapa=competencias"),
    );
    primeira.unmount();
    preparar("idiomas", "conta-b@example.invalid");
    render(<App />);
    await userEvent.click(await avancar());
    await waitFor(() =>
      expect(window.location.search).toBe("?etapa=competencias"),
    );
    expect(
      puts(requisitar).filter(([url]) => String(url).endsWith("/idiomas")),
    ).toHaveLength(2);
  });
});
