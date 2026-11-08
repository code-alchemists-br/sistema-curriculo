import { afterEach, describe, expect, it, vi } from "vitest";

import {
  criarClienteExperienciasHttp,
  FalhaExperiencia,
} from "./cliente-experiencias-http";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criarClienteExperienciasHttp", () => {
  it("envia POST para /experiencias-profissionais com credentials include e data_fim null se empregoAtual", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteExperienciasHttp("http://127.0.0.1:8000");

    await cliente.salvar([
      {
        empresa: "Empresa XPTO",
        cargo: "Desenvolvedor Frontend",
        descricao: "Desenvolvimento de interfaces React acessíveis",
        inicio: "2023-01",
        fim: "",
        empregoAtual: true,
      },
    ]);

    expect(requisitar).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/experiencias-profissionais",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          empresa: "Empresa XPTO",
          cargo: "Desenvolvedor Frontend",
          descricao: "Desenvolvimento de interfaces React acessíveis",
          data_inicio: "2023-01-01",
          data_fim: null,
        }),
      },
    );
  });

  it("não dispara requisição quando a lista está vazia", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch");
    const cliente = criarClienteExperienciasHttp("http://127.0.0.1:8000");

    await cliente.salvar([]);
    expect(requisitar).not.toHaveBeenCalled();
  });

  it("lança FalhaExperiencia com codigo rede em falha de conexão", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("Network error"));
    const cliente = criarClienteExperienciasHttp("http://127.0.0.1:8000");

    await expect(
      cliente.salvar([
        {
          empresa: "Empresa Teste",
          cargo: "Estagiário",
          descricao: "Atividades de estágio",
          inicio: "2023-01-01",
          fim: "2023-12-01",
          empregoAtual: false,
        },
      ]),
    ).rejects.toThrow(new FalhaExperiencia("rede"));
  });
});
