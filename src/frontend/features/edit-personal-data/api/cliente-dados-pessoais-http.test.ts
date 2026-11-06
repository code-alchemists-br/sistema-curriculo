import { afterEach, describe, expect, it, vi } from "vitest";

import { criarClienteDadosPessoaisHttp } from "./cliente-dados-pessoais-http";
import { FalhaDadosPessoais } from "./cliente-dados-pessoais";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criarClienteDadosPessoaisHttp", () => {
  it("envia dados normalizados com credentials include para PUT /estudantes/me/perfil", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 200 }));
    const cliente = criarClienteDadosPessoaisHttp("http://127.0.0.1:8000");

    await cliente.salvar({
      nomeCompleto: "Ricardo Sampaio",
      email: "ricardo@fatec.sp.gov.br",
      enderecoCompleto: "Rua das Flores 123, São Paulo",
      telefones: ["(11) 99999-0000"],
      linkedIn: "https://linkedin.com/in/ricardo",
    });

    expect(requisitar).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/estudantes/me/perfil",
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          nome: "Ricardo Sampaio",
          email: "ricardo@fatec.sp.gov.br",
          endereco: "Rua das Flores 123",
          cidade: "São Paulo",
          telefones: ["(11) 99999-0000"],
          linkedin: "https://linkedin.com/in/ricardo",
          curriculo_lattes: null,
        }),
      },
    );
  });

  it("lança FalhaDadosPessoais com codigo indisponivel em erro de rede ou 500", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(null, { status: 500 }),
    );
    const cliente = criarClienteDadosPessoaisHttp("http://127.0.0.1:8000");

    await expect(
      cliente.salvar({
        nomeCompleto: "Ricardo Sampaio",
        email: "ricardo@fatec.sp.gov.br",
        enderecoCompleto: "São Paulo",
        telefones: ["(11) 99999-0000"],
      }),
    ).rejects.toThrow(new FalhaDadosPessoais("indisponivel"));
  });

  it("lança FalhaDadosPessoais com codigo resposta-invalida em status 422 ou 400", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(null, { status: 422 }),
    );
    const cliente = criarClienteDadosPessoaisHttp("http://127.0.0.1:8000");

    await expect(
      cliente.salvar({
        nomeCompleto: "Ricardo Sampaio",
        email: "ricardo@fatec.sp.gov.br",
        enderecoCompleto: "São Paulo",
        telefones: ["(11) 99999-0000"],
      }),
    ).rejects.toThrow(new FalhaDadosPessoais("resposta-invalida"));
  });
});
