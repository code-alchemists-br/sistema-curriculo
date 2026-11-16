import { afterEach, describe, expect, it, vi } from "vitest";

import {
  criarClienteAcessoEstudante,
  encerrarSessao,
} from "./cliente-acesso-estudante";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criarClienteAcessoEstudante", () => {
  it("inclui credenciais ao iniciar uma sessão", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 204 }));
    const cliente = criarClienteAcessoEstudante("http://127.0.0.1:8000");

    await cliente.acessar({
      email: "aluna@fatec.sp.gov.br",
      senha: "segredo123",
    });

    expect(requisitar).toHaveBeenCalledWith("http://127.0.0.1:8000/acessos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: "aluna@fatec.sp.gov.br",
        senha: "segredo123",
      }),
      credentials: "include",
    });
  });
});

describe("encerrarSessao", () => {
  it("envia DELETE /sessao/atual com credenciais", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 204 }));

    const encerrada = await encerrarSessao("http://127.0.0.1:8000/");

    expect(encerrada).toBe(true);
    expect(requisitar).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/sessao/atual",
      { method: "DELETE", credentials: "include" },
    );
  });

  it("não lança erro quando a API está fora do ar", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new TypeError("fetch"));

    await expect(encerrarSessao("http://127.0.0.1:8000")).resolves.toBe(false);
  });

  it("não chama a API quando a URL não está configurada", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch");

    await expect(encerrarSessao("")).resolves.toBe(true);
    expect(requisitar).not.toHaveBeenCalled();
  });
});
