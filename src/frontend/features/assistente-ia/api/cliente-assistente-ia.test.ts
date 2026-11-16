import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaAssistenteIa,
  criarClienteAssistenteIa,
} from "./cliente-assistente-ia";

afterEach(() => vi.restoreAllMocks());

/** Substitui o fetch por uma resposta JSON fixa e devolve o espião. */
function responder(status: number, corpo?: unknown) {
  return vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(corpo === undefined ? null : JSON.stringify(corpo), {
      status,
    }),
  );
}

describe("criarClienteAssistenteIa", () => {
  it("envia a revisão e converte a resposta para o formato da tela", async () => {
    const espiao = responder(200, {
      situacao: "melhorado",
      motivo: "Pode melhorar.",
      sugestoes: ["a", "b", "c", "d"],
      pode_manter_texto: true,
    });

    const revisao = await criarClienteAssistenteIa("http://api.test/").revisar({
      campo: "descricao_projeto",
      texto: "Fiz um app.",
    });

    expect(espiao.mock.calls[0][0]).toBe("http://api.test/assistente/revisoes");
    expect(JSON.parse(espiao.mock.calls[0][1]?.body as string)).toEqual({
      campo: "descricao_projeto",
      texto: "Fiz um app.",
      contexto: {},
    });
    expect(revisao).toEqual({
      situacao: "melhorado",
      motivo: "Pode melhorar.",
      sugestoes: ["a", "b", "c"],
      podeManterTexto: true,
    });
  });

  it("limita os extras da recomendação a dez e lê a alternativa", async () => {
    const espiao = responder(200, {
      modelo: "moderno",
      motivo: "Perfil técnico.",
      alternativa: "compacto",
    });
    const perfil = Array.from({ length: 12 }, (_, i) => ({
      pergunta: `P${i}`,
      resposta: "R",
    }));

    const recomendacao =
      await criarClienteAssistenteIa("http://api.test").recomendarModelo(
        perfil,
      );

    expect(
      JSON.parse(espiao.mock.calls[0][1]?.body as string).extras,
    ).toHaveLength(10);
    expect(recomendacao).toEqual({
      modelo: "moderno",
      motivo: "Perfil técnico.",
      alternativa: "compacto",
    });
  });

  it.each([
    [401, undefined, /Entre na sua conta/],
    [503, { detail: "Defina GEMINI_API_KEY." }, /GEMINI_API_KEY/],
    [500, undefined, /erro 500/],
  ])(
    "traduz a resposta %i em FalhaAssistenteIa",
    async (status, corpo, mensagem) => {
      responder(status, corpo);

      const falha = criarClienteAssistenteIa("http://api.test").revisar({
        campo: "outro",
        texto: "x",
      });

      await expect(falha).rejects.toBeInstanceOf(FalhaAssistenteIa);
      await expect(falha).rejects.toThrow(mensagem);
    },
  );

  it("recusa resposta fora do formato e falta de URL da API", async () => {
    responder(200, { qualquer: "coisa" });
    await expect(
      criarClienteAssistenteIa("http://api.test").recomendarModelo([]),
    ).rejects.toThrow(/formato inesperado/);

    await expect(
      criarClienteAssistenteIa("").revisar({ campo: "outro", texto: "x" }),
    ).rejects.toThrow(/VITE_API_URL/);
  });
});
