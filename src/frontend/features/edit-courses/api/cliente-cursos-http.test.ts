import { afterEach, describe, expect, it, vi } from "vitest";

import { criarClienteCursosHttp, FalhaCurso } from "./cliente-cursos-http";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criarClienteCursosHttp", () => {
  it("envia POST para /cursos com carga_horaria inteira e credentials include", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteCursosHttp("http://127.0.0.1:8000");

    await cliente.salvar([
      {
        nome: "Clean Code",
        instituicao: "Udemy",
        cargaHoraria: "20",
      },
    ]);

    expect(requisitar).toHaveBeenCalledWith("http://127.0.0.1:8000/cursos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        nome: "Clean Code",
        instituicao: "Udemy",
        carga_horaria: 20,
      }),
    });
  });

  it("não envia requisição para lista vazia", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch");
    const cliente = criarClienteCursosHttp("http://127.0.0.1:8000");

    await cliente.salvar([]);
    expect(requisitar).not.toHaveBeenCalled();
  });

  it("lança FalhaCurso com codigo rede em falha de conexão", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(
      new Error("Erro de conexão"),
    );
    const cliente = criarClienteCursosHttp("http://127.0.0.1:8000");

    await expect(
      cliente.salvar([
        {
          nome: "Git",
          instituicao: "FATEC",
          cargaHoraria: "10",
        },
      ]),
    ).rejects.toThrow(new FalhaCurso("rede"));
  });
});
