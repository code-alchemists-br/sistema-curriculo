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

/** Prepara um rascunho sintético para observar corridas e edições no App real sem rede externa. */
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

/** Currículo que o banco simulado devolve ao abrir o App, igual ao rascunho. */
const CURRICULO_SALVO = {
  dados_pessoais: {
    nome: "Conta A",
    email: "a@example.invalid",
    telefones: [],
  },
  formacoes: [],
  experiencias: [],
  projetos: [],
  competencias: [],
  cursos: [
    { nome: "Curso A", instituicao: "Fatec", carga_horaria: 20 },
    { nome: "Curso B", instituicao: "Fatec", carga_horaria: 30 },
  ],
  certificacoes: [{ nome: "Certificado", organizacao_emissora: "Emissor" }],
  idiomas: [{ idioma: "Inglês", nivel: "basico" }],
  modelo: null,
};

/**
 * Substitui a API: o GET devolve o currículo salvo e cada PUT chama
 * `responderPut`, que decide a resposta (204 por padrão).
 */
function simularApi(
  responderPut: () => Promise<Response> = async () =>
    new Response(null, { status: 204 }),
) {
  return vi
    .spyOn(globalThis, "fetch")
    .mockImplementation(async (_url, init) =>
      (init?.method ?? "GET") === "GET"
        ? new Response(JSON.stringify(CURRICULO_SALVO), { status: 200 })
        : responderPut(),
    );
}

/** Lista as chamadas PUT feitas ao salvar etapas. */
function puts(requisitar: ReturnType<typeof simularApi>) {
  return requisitar.mock.calls.filter(([, init]) => init?.method === "PUT");
}

/** Cria uma resposta de PUT que só termina quando o teste mandar. */
function respostaPendente() {
  let concluir!: (value: Response) => void;
  const responder = () =>
    new Promise<Response>((resolve) => {
      concluir = resolve;
    });
  return { responder, concluir: (r: Response) => concluir(r) };
}

const avancar = () =>
  screen.findByRole("button", { name: "Avançar para próxima etapa" });

describe("regressões da revisão da issue 33", () => {
  it.each(["idiomas", "cursos-certificacoes"])(
    "cancela o envio e não navega após sair e fazer logout em %s",
    async (etapa) => {
      preparar(etapa);
      const pendente = respostaPendente();
      const requisitar = simularApi(pendente.responder);
      render(<App />);
      await userEvent.click(await avancar());
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
      await act(async () =>
        pendente.concluir(new Response(null, { status: 204 })),
      );
      expect(window.location.search).toBe(rotaDepoisLogout);
      expect(sessionStorage.getItem("liminal_usuario_sessao")).toBeNull();
      expect(localStorage.getItem("liminal_curriculo_rascunho")).not.toMatch(
        /Inglês|Curso A|Certificado/,
      );
      expect(puts(requisitar)).toHaveLength(1);
      expect(puts(requisitar)[0][1]?.signal?.aborted).toBe(true);
    },
  );

  it("cancela o envio ao mudar de etapa pelo histórico, sem sequestrar navegação", async () => {
    preparar("idiomas");
    const pendente = respostaPendente();
    simularApi(pendente.responder);
    render(<App />);
    await userEvent.click(await avancar());
    await act(async () => {
      window.history.pushState({}, "", "/?etapa=cursos-certificacoes");
      window.dispatchEvent(new PopStateEvent("popstate"));
    });
    await act(async () =>
      pendente.concluir(new Response(null, { status: 204 })),
    );
    expect(window.location.search).toBe("?etapa=cursos-certificacoes");
  });

  it("Enter no input de idioma espera a gravação, sem confirmação local falsa", async () => {
    preparar("idiomas");
    const pendente = respostaPendente();
    const requisitar = simularApi(pendente.responder);
    render(<App />);
    await avancar();
    screen.getByLabelText("Idioma").focus();
    await userEvent.keyboard("{Enter}");
    expect(puts(requisitar)).toHaveLength(1);
    expect(await avancar()).toBeDisabled();
    expect(
      screen.queryByText("Idiomas salvos com sucesso."),
    ).not.toBeInTheDocument();
    await act(async () =>
      pendente.concluir(new Response(null, { status: 204 })),
    );
    await waitFor(() =>
      expect(window.location.search).toBe("?etapa=competencias"),
    );
  });

  it("editar um idioma já salvo substitui a seção, sem conflito", async () => {
    preparar("idiomas");
    const requisitar = simularApi();
    render(<App />);
    await userEvent.click(await avancar());
    await screen.findByRole("heading", { name: "Competências", level: 1 });
    await userEvent.click(
      screen.getByRole("button", { name: "Voltar para a etapa anterior" }),
    );
    await userEvent.selectOptions(
      await screen.findByLabelText("Nível de proficiência"),
      "fluente",
    );
    await userEvent.click(await avancar());
    await screen.findByRole("heading", { name: "Competências", level: 1 });
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
    expect(puts(requisitar)).toHaveLength(2);
    expect(JSON.parse(puts(requisitar)[1][1]?.body as string)).toEqual({
      itens: [{ idioma: "Inglês", nivel: "fluente" }],
    });
  });

  it("alterar a carga de um curso já salvo substitui a seção, sem conflito", async () => {
    preparar("cursos-certificacoes");
    const requisitar = simularApi();
    render(<App />);
    await userEvent.click(await avancar());
    await screen.findByRole("heading", { name: "Idiomas", level: 1 });
    await userEvent.click(
      screen.getByRole("button", { name: "Voltar para a etapa anterior" }),
    );
    const carga = (await screen.findAllByLabelText("Carga horária (horas)"))[0];
    await userEvent.clear(carga);
    await userEvent.type(carga, "40");
    await userEvent.click(await avancar());
    await screen.findByRole("heading", { name: "Idiomas", level: 1 });
    const cursos = puts(requisitar).filter(([url]) =>
      String(url).endsWith("/cursos"),
    );
    expect(cursos).toHaveLength(2);
    expect(JSON.parse(cursos[1][1]?.body as string).itens[0]).toMatchObject({
      nome: "Curso A",
      carga_horaria: 40,
    });
  });

  it("itens repetidos (409) mostram o erro e não avançam", async () => {
    preparar("idiomas");
    simularApi(async () => new Response(null, { status: 409 }));
    render(<App />);
    await userEvent.click(await avancar());
    expect(await screen.findByRole("alert")).toBeInTheDocument();
    expect(window.location.search).toBe("?etapa=idiomas");
  });
});
