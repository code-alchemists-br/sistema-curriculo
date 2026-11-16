import { act, renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import type { ClienteAssistenteIa } from "../api/cliente-assistente-ia";
import type { RevisaoTexto } from "./tipos";
import { useRevisoesIa, type TextoParaRevisar } from "./useRevisoesIa";

/** Cria um cliente de IA falso que devolve as revisões na ordem dada. */
function clienteFalso(...respostas: Array<RevisaoTexto | Error>) {
  const revisar = vi.fn(async () => {
    const resposta = respostas.shift();
    if (!resposta || resposta instanceof Error)
      throw resposta ?? new Error("fim");
    return resposta;
  });
  const cliente: ClienteAssistenteIa = {
    revisar,
    recomendarModelo: vi.fn(),
  };
  return { cliente, revisar };
}

const revisao = (situacao: RevisaoTexto["situacao"]): RevisaoTexto => ({
  situacao,
  motivo: "motivo",
  sugestoes: ["s1"],
  podeManterTexto: situacao !== "invalido",
});

const item = (texto: string): TextoParaRevisar => ({
  texto,
  campo: "descricao_projeto",
});

describe("useRevisoesIa", () => {
  it("bloqueia texto inválido com erro e texto melhorável com aviso", async () => {
    const { cliente } = clienteFalso(revisao("invalido"), revisao("melhorado"));
    const { result } = renderHook(() => useRevisoesIa(cliente));

    let pendencias = {};
    await act(async () => {
      pendencias = await result.current.revisarAntesDeSalvar([
        item("fazia coisas"),
        item("Fiz um app"),
      ]);
    });

    expect(pendencias).toEqual({
      0: expect.objectContaining({ tipo: "erro" }),
      1: expect.objectContaining({ tipo: "aviso" }),
    });
  });

  it("para uma vez também quando o texto é válido, para mostrar a aprovação", async () => {
    const { cliente } = clienteFalso(revisao("valido"));
    const { result } = renderHook(() => useRevisoesIa(cliente));

    let pendencias = {};
    await act(async () => {
      pendencias = await result.current.revisarAntesDeSalvar([
        item("Criei uma API em Python para controlar o estoque da loja."),
      ]);
    });

    expect(pendencias).toEqual({
      0: expect.objectContaining({
        tipo: "aviso",
        mensagem: expect.stringMatching(/aprovado/),
      }),
    });
  });

  it("revisa os textos em paralelo, sem esperar um terminar para mandar o outro", async () => {
    let liberar: () => void = () => {};
    const espera = new Promise<void>((resolver) => {
      liberar = resolver;
    });
    const revisar = vi.fn(async () => {
      await espera;
      return revisao("valido");
    });
    const cliente: ClienteAssistenteIa = {
      revisar,
      recomendarModelo: vi.fn(),
    };
    const { result } = renderHook(() => useRevisoesIa(cliente));

    let andamento: Promise<unknown> = Promise.resolve();
    act(() => {
      andamento = result.current.revisarAntesDeSalvar([
        item("Primeiro texto"),
        item("Segundo texto"),
      ]);
    });

    expect(revisar).toHaveBeenCalledTimes(2);
    liberar();
    await act(async () => {
      await andamento;
    });
  });

  it("no segundo clique segue com o texto já aprovado sem chamar a IA de novo", async () => {
    const { cliente, revisar } = clienteFalso(revisao("melhorado"));
    const { result } = renderHook(() => useRevisoesIa(cliente));

    await act(async () => {
      await result.current.revisarAntesDeSalvar([item("Fiz um app")]);
    });
    let segunda = {};
    await act(async () => {
      segunda = await result.current.revisarAntesDeSalvar([item("Fiz um app")]);
    });

    expect(segunda).toEqual({});
    expect(revisar).toHaveBeenCalledTimes(1);
  });

  it("não bloqueia quando a IA está indisponível e ignora textos vazios", async () => {
    const { cliente, revisar } = clienteFalso(new Error("sem IA"));
    const { result } = renderHook(() => useRevisoesIa(cliente));

    let pendencias = {};
    await act(async () => {
      pendencias = await result.current.revisarAntesDeSalvar([
        item("Fiz um app"),
        item("   "),
      ]);
    });

    expect(pendencias).toEqual({});
    expect(revisar).toHaveBeenCalledTimes(1);
    expect(result.current.memoriaDe(0).iaIndisponivel).toBe(true);
  });
});
