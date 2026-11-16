import { act, cleanup, render, screen, waitFor } from "@testing-library/react";
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

/** Prepara um rascunho sintético para observar corridas e conflitos no App real sem rede externa. */
function preparar(etapa: string): void {
  window.history.replaceState({}, "", `/?etapa=${etapa}`);
  sessionStorage.setItem(
    "liminal_usuario_sessao",
    JSON.stringify({ nome: "Conta A", email: "a@example.invalid" }),
  );
  localStorage.setItem(
    "liminal_curriculo_rascunho",
    JSON.stringify({
      cursos: [
        { nome: "Curso A", instituicao: "Fatec", cargaHoraria: "20" },
        { nome: "Curso B", instituicao: "Fatec", cargaHoraria: "30" },
      ],
      certificacoes: [{ nome: "Certificado", organizacaoEmissora: "Emissor" }],
      idiomas: [{ nome: "Inglês", nivel: "basico" }],
    }),
  );
}

const avancar = () =>
  screen.getByRole("button", { name: "Avançar para próxima etapa" });

describe("regressões da revisão da issue 33", () => {
  it.each(["idiomas", "cursos-certificacoes"])(
    "invalida resposta e itens pendentes após sair e fazer logout em %s",
    async (etapa) => {
      preparar(etapa);
      let concluir!: (value: Response) => void;
      const requisitar = vi.spyOn(globalThis, "fetch").mockImplementationOnce(
        () =>
          new Promise<Response>((resolve) => {
            concluir = resolve;
          }),
      );
      render(<App />);
      await userEvent.click(avancar());
      await userEvent.click(
        screen.getByRole("button", { name: "Voltar para a página inicial" }),
      );
      await userEvent.click(
        screen.getByRole("button", { name: "Menu de navegação e perfil" }),
      );
      await userEvent.click(
        screen.getByRole("menuitem", { name: "Sair da conta" }),
      );
      const rotaDepoisLogout = window.location.search;
      await act(async () => concluir(new Response(null, { status: 201 })));
      expect(window.location.search).toBe(rotaDepoisLogout);
      expect(sessionStorage.getItem("liminal_usuario_sessao")).toBeNull();
      expect(localStorage.getItem("liminal_curriculo_rascunho")).not.toMatch(
        /Inglês|Curso A|Certificado/,
      );
      expect(requisitar).toHaveBeenCalledTimes(1);
      expect(requisitar.mock.calls[0][1]?.signal?.aborted).toBe(true);
    },
  );

  it("invalida envio ao mudar de etapa pelo histórico, sem sequestrar navegação", async () => {
    preparar("idiomas");
    let concluir!: (value: Response) => void;
    vi.spyOn(globalThis, "fetch").mockImplementationOnce(
      () =>
        new Promise<Response>((resolve) => {
          concluir = resolve;
        }),
    );
    render(<App />);
    await userEvent.click(avancar());
    await act(async () => {
      window.history.pushState({}, "", "/?etapa=cursos-certificacoes");
      window.dispatchEvent(new PopStateEvent("popstate"));
    });
    await act(async () => concluir(new Response(null, { status: 201 })));
    expect(window.location.search).toBe("?etapa=cursos-certificacoes");
  });

  it("Enter no input de idioma usa o cadastro aguardado, não uma confirmação local falsa", async () => {
    preparar("idiomas");
    let concluir!: (value: Response) => void;
    const requisitar = vi.spyOn(globalThis, "fetch").mockImplementationOnce(
      () =>
        new Promise<Response>((resolve) => {
          concluir = resolve;
        }),
    );
    render(<App />);
    screen.getByLabelText("Idioma").focus();
    await userEvent.keyboard("{Enter}");
    expect(requisitar).toHaveBeenCalledTimes(1);
    expect(avancar()).toBeDisabled();
    expect(
      screen.queryByText("Idiomas salvos com sucesso."),
    ).not.toBeInTheDocument();
    await act(async () => concluir(new Response(null, { status: 201 })));
    await waitFor(() =>
      expect(window.location.search).toBe("?etapa=competencias"),
    );
  });

  it("explica conflito ao editar idioma cadastrado e permite continuação explicitamente local", async () => {
    preparar("idiomas");
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(null, { status: 201 }))
      .mockResolvedValueOnce(new Response(null, { status: 409 }));
    render(<App />);
    await userEvent.click(avancar());
    await screen.findByRole("heading", { name: "Competências", level: 1 });
    await userEvent.click(
      screen.getByRole("button", { name: "Voltar para a etapa anterior" }),
    );
    await userEvent.selectOptions(
      screen.getByLabelText("Nível de proficiência"),
      "fluente",
    );
    await userEvent.click(avancar());
    expect(await screen.findByRole("alert")).toHaveTextContent(/não atualiza/i);
    await userEvent.click(
      screen.getByRole("button", {
        name: "Continuar apenas com rascunho local",
      }),
    );
    await waitFor(() =>
      expect(window.location.search).toBe("?etapa=competencias"),
    );
    expect(requisitar).toHaveBeenCalledTimes(2);
    expect(localStorage.getItem("liminal_curriculo_rascunho")).toContain(
      "fluente",
    );
  });

  it("explica conflito de carga alterada sem tratá-lo como sucesso remoto", async () => {
    preparar("cursos-certificacoes");
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockImplementation(async () => new Response(null, { status: 201 }));
    render(<App />);
    await userEvent.click(avancar());
    await screen.findByRole("heading", { name: "Idiomas", level: 1 });
    await userEvent.click(
      screen.getByRole("button", { name: "Voltar para a etapa anterior" }),
    );
    const carga = screen.getAllByLabelText("Carga horária (horas)")[0];
    await userEvent.clear(carga);
    await userEvent.type(carga, "40");
    requisitar.mockResolvedValueOnce(new Response(null, { status: 409 }));
    await userEvent.click(avancar());
    expect(await screen.findByRole("alert")).toHaveTextContent(/não atualiza/i);
    const quantidade = requisitar.mock.calls.length;
    await userEvent.click(
      screen.getByRole("button", {
        name: "Continuar apenas com rascunho local",
      }),
    );
    await screen.findByRole("heading", { name: "Idiomas", level: 1 });
    expect(requisitar).toHaveBeenCalledTimes(quantidade);
    expect(localStorage.getItem("liminal_curriculo_rascunho")).toContain(
      '"cargaHoraria":"40"',
    );
  });
});
