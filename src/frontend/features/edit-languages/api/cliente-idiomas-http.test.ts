import { afterEach, describe, expect, it, vi } from "vitest";

import { criarClienteIdiomasHttp, FalhaIdioma } from "./cliente-idiomas-http";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criarClienteIdiomasHttp", () => {
  it("envia POST para /idiomas com campos mapeados e credentials include", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteIdiomasHttp("http://127.0.0.1:8000");

    await cliente.salvar([
      {
        nome: "Inglês",
        nivel: "avancado",
      },
    ]);

    expect(requisitar).toHaveBeenCalledWith("http://127.0.0.1:8000/idiomas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        idioma: "Inglês",
        nivel: "avancado",
      }),
    });
  });

  it("não envia requisição para lista vazia", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch");
    const cliente = criarClienteIdiomasHttp("http://127.0.0.1:8000");

    await cliente.salvar([]);
    expect(requisitar).not.toHaveBeenCalled();
  });

  it("lança FalhaIdioma com codigo rede em falha de conexão", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("Erro de rede"));
    const cliente = criarClienteIdiomasHttp("http://127.0.0.1:8000");

    await expect(
      cliente.salvar([
        {
          nome: "Espanhol",
          nivel: "intermediario",
        },
      ]),
    ).rejects.toThrow(new FalhaIdioma("rede"));
  });
});
