import { describe, expect, it } from "vitest";
import * as modelo from "./cursos";
const valido = {
  nome: "Curso",
  instituicao: "Instituição",
  cargaHoraria: "20",
};
describe("contrato de cursos", () => {
  it.each(["", "  ", "1", "10000", " 20 ", "00020"])(
    "aceita carga opcional/inteira %j",
    (cargaHoraria) => {
      expect(modelo.validarCurso({ ...valido, cargaHoraria })).toEqual({});
    },
  );
  it.each([
    "0",
    "10001",
    "-1",
    "1.5",
    "1.0",
    "Infinity",
    "NaN",
    "1e2",
    "0x10",
    "+10",
    "1,5",
    "999999999999999999999",
    "abc",
  ])("rejeita carga não decimal inteira %j", (cargaHoraria) => {
    expect(
      modelo.validarCurso({ ...valido, cargaHoraria }).cargaHoraria,
    ).toBeTruthy();
  });
  it.each(["nome", "instituicao"] as const)(
    "valida limite de 200 em %s",
    (campo) => {
      expect(
        modelo.validarCurso({ ...valido, [campo]: "A".repeat(200) })[campo],
      ).toBeUndefined();
      expect(
        modelo.validarCurso({ ...valido, [campo]: "A".repeat(201) })[campo],
      ).toBeTruthy();
    },
  );
  it.each(["nome", "instituicao"] as const)(
    "rejeita controles inválidos em %s",
    (campo) => {
      expect(
        modelo.validarCurso({ ...valido, [campo]: "A\u0000B" })[campo],
      ).toBeTruthy();
      expect(
        modelo.validarCurso({ ...valido, [campo]: "A\u200bB" })[campo],
      ).toBeTruthy();
    },
  );
  it("distingue vazio total de cada entrada parcial sem mutar", () => {
    expect(
      modelo.cursoEstaVazio({
        nome: " ",
        instituicao: "\t",
        cargaHoraria: " ",
      }),
    ).toBe(true);
    for (const campo of ["nome", "instituicao", "cargaHoraria"] as const) {
      expect(
        modelo.cursoEstaVazio({
          nome: "",
          instituicao: "",
          cargaHoraria: "",
          [campo]: "1",
        }),
      ).toBe(false);
    }
  });
});
