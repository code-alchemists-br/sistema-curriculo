import { afterEach, describe, expect, it, vi } from "vitest";

import { criarClienteFormacaoAcademicaHttp } from "./cliente-formacao-academica-http";
import { FalhaFormacaoAcademica } from "./cliente-formacao-academica";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criarClienteFormacaoAcademicaHttp", () => {
  it("envia dados normalizados com credentials include para POST /formacoes-academicas", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteFormacaoAcademicaHttp("http://127.0.0.1:8000");

    await cliente.cadastrar({
      instituicao: "FATEC São Paulo",
      curso: "Análise e Desenvolvimento de Sistemas",
      nivel: "graduacao",
      dataInicio: "2023-02-01",
      dataFim: "2025-12-01",
      status: "em_andamento",
    });

    expect(requisitar).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/formacoes-academicas",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          instituicao: "FATEC São Paulo",
          curso: "Análise e Desenvolvimento de Sistemas",
          nivel: "graduacao",
          data_inicio: "2023-02-01",
          data_fim: "2025-12-01",
          status: "em_andamento",
        }),
      },
    );
  });

  it("normaliza mês YYYY-MM para YYYY-MM-01", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteFormacaoAcademicaHttp("http://127.0.0.1:8000");

    await cliente.cadastrar({
      instituicao: "FATEC São Paulo",
      curso: "ADS",
      nivel: "graduacao",
      dataInicio: "2023-02",
      status: "em_andamento",
    });

    expect(requisitar).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/formacoes-academicas",
      expect.objectContaining({
        body: JSON.stringify({
          instituicao: "FATEC São Paulo",
          curso: "ADS",
          nivel: "graduacao",
          data_inicio: "2023-02-01",
          data_fim: null,
          status: "em_andamento",
        }),
      }),
    );
  });

  it("lança FalhaFormacaoAcademica com codigo rede em falha de conexão", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(
      new Error("Failed to fetch"),
    );
    const cliente = criarClienteFormacaoAcademicaHttp("http://127.0.0.1:8000");

    await expect(
      cliente.cadastrar({
        instituicao: "FATEC",
        curso: "ADS",
        nivel: "graduacao",
        dataInicio: "2023-02-01",
        status: "em_andamento",
      }),
    ).rejects.toThrow(new FalhaFormacaoAcademica("rede"));
  });
});
