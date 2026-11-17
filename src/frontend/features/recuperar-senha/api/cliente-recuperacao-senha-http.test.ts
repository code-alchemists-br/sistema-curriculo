import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { FalhaRecuperacaoSenha } from "./cliente-recuperacao-senha";
import {
  criarClienteRecuperacaoSenhaDemonstracao,
  criarClienteRecuperacaoSenhaHttp,
} from "./cliente-recuperacao-senha-http";

describe("cliente-recuperacao-senha-http", () => {
  const urlBase = "http://api.test";

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("submete com sucesso quando o backend responde 202 Accepted", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      status: 202,
      ok: true,
      json: async () => ({
        mensagem: "Se houver uma conta associada, enviaremos instruções.",
      }),
    });
    vi.stubGlobal("fetch", fetchMock);

    const cliente = criarClienteRecuperacaoSenhaHttp(urlBase);
    await expect(
      cliente.solicitar({ email: "estudante@fatec.sp.gov.br" }),
    ).resolves.toBeUndefined();

    expect(fetchMock).toHaveBeenCalledWith(
      "http://api.test/recuperacoes-senha",
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: "estudante@fatec.sp.gov.br" }),
        credentials: "include",
      }),
    );
  });

  it("lança falha de rede quando fetch falha por erro de conexão", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new TypeError("Failed to fetch")),
    );

    const cliente = criarClienteRecuperacaoSenhaHttp(urlBase);
    await expect(
      cliente.solicitar({ email: "estudante@fatec.sp.gov.br" }),
    ).rejects.toThrow(FalhaRecuperacaoSenha);
  });

  it("lança falha indisponivel quando backend responde status 500+", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        status: 503,
        ok: false,
      }),
    );

    const cliente = criarClienteRecuperacaoSenhaHttp(urlBase);
    await expect(
      cliente.solicitar({ email: "estudante@fatec.sp.gov.br" }),
    ).rejects.toMatchObject({
      codigo: "indisponivel",
    });
  });

  it("lança falha indisponivel quando urlDaApi não foi informada", async () => {
    const cliente = criarClienteRecuperacaoSenhaHttp("");
    await expect(
      cliente.solicitar({ email: "estudante@fatec.sp.gov.br" }),
    ).rejects.toMatchObject({
      codigo: "indisponivel",
    });
  });

  it("cliente de demonstração conclui solicitação com sucesso", async () => {
    const clienteDemo = criarClienteRecuperacaoSenhaDemonstracao();
    await expect(
      clienteDemo.solicitar({ email: "qualquer@exemplo.com" }),
    ).resolves.toBeUndefined();
  });
});
