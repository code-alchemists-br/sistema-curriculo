import { describe, expect, it } from "vitest";

import {
  estadoDoTexto,
  registrarRevisao,
  registrarSugestaoUsada,
  type MemoriaRevisao,
} from "./revisao";
import type { RevisaoTexto } from "./tipos";

const MELHORADO: RevisaoTexto = {
  situacao: "melhorado",
  motivo: "Pode melhorar.",
  sugestoes: ["Sugestão 1"],
  podeManterTexto: true,
};
const INVALIDO: RevisaoTexto = {
  situacao: "invalido",
  motivo: "Vago.",
  sugestoes: ["Modelo com [colchetes]"],
  podeManterTexto: false,
};

describe("estado da revisão de um texto", () => {
  it("começa não revisado e fica indisponível quando a IA falha", () => {
    expect(estadoDoTexto({ iaIndisponivel: false }, "texto")).toBe(
      "nao-revisado",
    );
    expect(estadoDoTexto({ iaIndisponivel: true }, "texto")).toBe(
      "ia-indisponivel",
    );
  });

  it("aprova o texto revisado enquanto ele não muda", () => {
    const memoria = registrarRevisao("texto", MELHORADO);

    expect(estadoDoTexto(memoria, "texto")).toBe("aprovado");
    expect(estadoDoTexto(memoria, "texto editado")).toBe("nao-revisado");
  });

  it("mantém o texto inválido bloqueado mesmo depois de editado", () => {
    const memoria = registrarRevisao("fazia coisas", INVALIDO);

    expect(estadoDoTexto(memoria, "fazia coisas")).toBe("invalido");
    expect(estadoDoTexto(memoria, "fazia outras coisas")).toBe("invalido");
  });

  it("aprova a sugestão usada só quando a revisão permitia manter o texto", () => {
    const aprovada = registrarSugestaoUsada(
      registrarRevisao("texto", MELHORADO),
      "Sugestão 1",
    );
    const modelo: MemoriaRevisao = registrarSugestaoUsada(
      registrarRevisao("vago", INVALIDO),
      "Modelo com [colchetes]",
    );

    expect(estadoDoTexto(aprovada, "Sugestão 1")).toBe("aprovado");
    expect(estadoDoTexto(modelo, "Modelo com [colchetes]")).toBe("invalido");
  });
});
