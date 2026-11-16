import { describe, expect, it } from "vitest";
import * as modelo from "./certificacao";
describe("contrato de certificações", () => {
  it("distingue vazio total de cada campo isolado", () => {
    expect(
      modelo.certificacaoEstaVazia({ nome: " ", organizacaoEmissora: "\t" }),
    ).toBe(true);
    expect(
      modelo.certificacaoEstaVazia({ nome: "AWS", organizacaoEmissora: "" }),
    ).toBe(false);
    expect(
      modelo.certificacaoEstaVazia({ nome: "", organizacaoEmissora: "AWS" }),
    ).toBe(false);
  });
  it.each(["nome", "organizacaoEmissora"] as const)(
    "valida limites e controles de %s",
    (campo) => {
      const valido = { nome: "AWS", organizacaoEmissora: "Amazon" };
      expect(
        modelo.validarCertificacao({ ...valido, [campo]: "A".repeat(200) }),
      ).toEqual({});
      expect(
        modelo.validarCertificacao({ ...valido, [campo]: "A".repeat(201) })[
          campo
        ],
      ).toBeTruthy();
      expect(
        modelo.validarCertificacao({ ...valido, [campo]: "A\u0000B" })[campo],
      ).toBeTruthy();
      expect(
        modelo.validarCertificacao({ ...valido, [campo]: "\tAWS" })[campo],
      ).toBeTruthy();
    },
  );
});
