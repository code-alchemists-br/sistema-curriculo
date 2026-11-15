import { afterEach, describe, expect, it, vi } from "vitest";

import { criarClienteRecuperacaoSenha } from "./cliente-recuperacao-senha";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criarClienteRecuperacaoSenha", () => {
  it("solicita instruções no endpoint contratado pelo backend", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ mensagem: "Instruções enviadas." }), {
        status: 202,
        headers: { "Content-Type": "application/json" },
      }),
    );
    const cliente = criarClienteRecuperacaoSenha("http://127.0.0.1:8000/");

    await cliente.solicitar({ email: "aluna@example.test" });

    expect(requisitar).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/recuperacoes-senha",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: "aluna@example.test" }),
      },
    );
  });

  it("confirma token e senha no endpoint de redefinição", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 204 }));
    const cliente = criarClienteRecuperacaoSenha("http://127.0.0.1:8000");

    await cliente.redefinir({
      token: "token-seguro",
      senha: "senha-segura-123",
    });

    expect(requisitar).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/recuperacoes-senha/confirmacao",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          token: "token-seguro",
          senha: "senha-segura-123",
        }),
      },
    );
  });
});
