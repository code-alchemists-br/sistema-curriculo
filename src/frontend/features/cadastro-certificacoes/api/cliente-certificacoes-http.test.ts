import { afterEach, describe, expect, it, vi } from "vitest";

import {
  criarClienteCertificacoesHttp,
  FalhaCertificacao,
} from "./cliente-certificacoes-http";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criarClienteCertificacoesHttp", () => {
  it("envia POST para /certificacoes com campos snake_case e credentials include", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteCertificacoesHttp("http://127.0.0.1:8000");

    await cliente.salvar([
      {
        nome: "AWS Certified Practitioner",
        organizacaoEmissora: "Amazon Web Services",
      },
    ]);

    expect(requisitar).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/certificacoes",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          nome: "AWS Certified Practitioner",
          organizacao_emissora: "Amazon Web Services",
        }),
      },
    );
  });

  it("não envia requisição para lista vazia", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch");
    const cliente = criarClienteCertificacoesHttp("http://127.0.0.1:8000");

    await cliente.salvar([]);
    expect(requisitar).not.toHaveBeenCalled();
  });

  it("lança FalhaCertificacao com codigo rede em falha de conexão", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("Erro de rede"));
    const cliente = criarClienteCertificacoesHttp("http://127.0.0.1:8000");

    await expect(
      cliente.salvar([
        {
          nome: "Certificado",
          organizacaoEmissora: "Org",
        },
      ]),
    ).rejects.toThrow(new FalhaCertificacao("rede"));
  });
});
