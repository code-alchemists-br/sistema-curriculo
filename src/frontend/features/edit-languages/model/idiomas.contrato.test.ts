import { describe, expect, it } from "vitest";
import * as modelo from "./idiomas";
import type { Idioma } from "./idiomas";
describe("contrato de idiomas", () => {
  it.each(["basico", "intermediario", "avancado", "fluente"] as const)(
    "aceita nível %s",
    (nivel) => {
      expect(modelo.validarIdioma({ nome: "Inglês", nivel })).toEqual({});
    },
  );
  it.each(["nativo", "toString", "__proto__", " "])(
    "rejeita nível externo %j",
    (nivel) => {
      expect(
        modelo.validarIdioma({ nome: "Inglês", nivel } as Idioma).nivel,
      ).toBeTruthy();
    },
  );
  it("limita nome a 200 caracteres", () => {
    expect(
      modelo.validarIdioma({ nome: "A".repeat(200), nivel: "basico" }),
    ).toEqual({});
    expect(
      modelo.validarIdioma({ nome: "A".repeat(201), nivel: "basico" }).nome,
    ).toBeTruthy();
  });
  it("normaliza sem modificar o idioma informado", () => {
    const original: Idioma = { nome: " Inglês ", nivel: "basico" };
    expect(modelo.normalizarIdioma(original)).toEqual({
      nome: "Inglês",
      nivel: "basico",
    });
    expect(original.nome).toBe(" Inglês ");
  });
  it("distingue vazio total de nome ou nível isolado", () => {
    expect(modelo.idiomaEstaVazio({ nome: " ", nivel: "" })).toBe(true);
    expect(modelo.idiomaEstaVazio({ nome: "Inglês", nivel: "" })).toBe(false);
    expect(modelo.idiomaEstaVazio({ nome: "", nivel: "basico" })).toBe(false);
  });
});
