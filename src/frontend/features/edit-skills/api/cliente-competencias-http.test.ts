import { afterEach, describe, expect, it, vi } from "vitest";

import {
  criarClienteCompetenciasHttp,
  FalhaCompetencias,
} from "./cliente-competencias-http";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criarClienteCompetenciasHttp", () => {
  it("envia POST para /competencias com categorias tecnica e comportamental", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteCompetenciasHttp("http://127.0.0.1:8000");

    await cliente.salvar({
      hardSkills: ["React", "TypeScript"],
      softSkills: ["Comunicação"],
    });

    expect(requisitar).toHaveBeenCalledTimes(3);
    expect(requisitar).toHaveBeenNthCalledWith(
      1,
      "http://127.0.0.1:8000/competencias",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          categoria: "tecnica",
          descricao: "React",
          nivel: "padrao",
        }),
      },
    );
    expect(requisitar).toHaveBeenNthCalledWith(
      3,
      "http://127.0.0.1:8000/competencias",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          categoria: "comportamental",
          descricao: "Comunicação",
          nivel: "padrao",
        }),
      },
    );
  });

  it("não dispara requisição quando ambas as listas estão vazias", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch");
    const cliente = criarClienteCompetenciasHttp("http://127.0.0.1:8000");

    await cliente.salvar({ hardSkills: [], softSkills: [] });
    expect(requisitar).not.toHaveBeenCalled();
  });

  it("lança FalhaCompetencias com codigo rede em falha de conexão", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("Erro de rede"));
    const cliente = criarClienteCompetenciasHttp("http://127.0.0.1:8000");

    await expect(
      cliente.salvar({ hardSkills: ["Python"], softSkills: [] }),
    ).rejects.toThrow(new FalhaCompetencias("rede"));
  });
});
