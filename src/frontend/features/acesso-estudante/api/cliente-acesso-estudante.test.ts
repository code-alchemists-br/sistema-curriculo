import { afterEach, describe, expect, it, vi } from "vitest";

import { criarClienteAcessoEstudante } from "./cliente-acesso-estudante";

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
