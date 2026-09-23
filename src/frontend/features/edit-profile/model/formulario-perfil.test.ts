import { describe, expect, it } from "vitest";

import {
  criarStudentDeValoresPerfil,
  criarValoresDeStudent,
  validarPerfilEstudante,
  type ValoresPerfilEstudante
} from "./formulario-perfil";

const valoresValidos: ValoresPerfilEstudante = {
  nomeCompleto: "Ricardo Galdino",
  enderecoCompleto: "Av. Paulista, 1000",
  telefones: ["(11) 99999-0000"],
  email: "ricardo@exemplo.com",
  linkedIn: "https://linkedin.com/in/ricardo",
  curriculoLattes: ""
};

describe("validarPerfilEstudante", () => {
  it("retorna objeto vazio quando todos os campos obrigatórios são válidos", () => {
    const erros = validarPerfilEstudante(valoresValidos);
    expect(Object.keys(erros)).toHaveLength(0);
  });

  it("reporta nome completo ausente", () => {
    const erros = validarPerfilEstudante({ ...valoresValidos, nomeCompleto: "  " });
    expect(erros.nomeCompleto).toBe("Informe seu nome completo.");
  });

  it("reporta endereço completo ausente", () => {
    const erros = validarPerfilEstudante({ ...valoresValidos, enderecoCompleto: "" });
    expect(erros.enderecoCompleto).toBe("Informe seu endereço completo.");
  });

  it("reporta e-mail com formato inválido", () => {
    const erros = validarPerfilEstudante({ ...valoresValidos, email: "invalido" });
    expect(erros.email).toBe("Informe um e-mail válido.");
  });

  it("reporta telefone vazio pelo índice correspondente", () => {
    const erros = validarPerfilEstudante({
      ...valoresValidos,
      telefones: ["(11) 99999-0000", ""]
    });
    expect(erros.telefones).toEqual({ 1: "Informe um telefone." });
  });
});

describe("criarStudentDeValoresPerfil", () => {
  it("omite linkedIn e curriculoLattes quando vazios", () => {
    const student = criarStudentDeValoresPerfil({
      ...valoresValidos,
      linkedIn: "  ",
      curriculoLattes: ""
    });

    expect(student).not.toHaveProperty("linkedIn");
    expect(student).not.toHaveProperty("curriculoLattes");
  });

  it("inclui linkedIn quando preenchido", () => {
    const student = criarStudentDeValoresPerfil(valoresValidos);
    expect(student.linkedIn).toBe("https://linkedin.com/in/ricardo");
  });

  it("remove espaços excedentes de todos os campos", () => {
    const student = criarStudentDeValoresPerfil({
      ...valoresValidos,
      nomeCompleto: "  Ricardo Galdino  ",
      email: " ricardo@exemplo.com "
    });

    expect(student.nomeCompleto).toBe("Ricardo Galdino");
    expect(student.email).toBe("ricardo@exemplo.com");
  });
});

describe("criarValoresDeStudent", () => {
  it("preenche campos opcionais como strings vazias quando ausentes", () => {
    const valores = criarValoresDeStudent({
      nomeCompleto: "Ricardo Galdino",
      enderecoCompleto: "Av. Paulista, 1000",
      telefones: ["(11) 99999-0000"],
      email: "ricardo@exemplo.com"
    });

    expect(valores.linkedIn).toBe("");
    expect(valores.curriculoLattes).toBe("");
  });

  it("cria um telefone vazio quando a lista de entrada está vazia", () => {
    const valores = criarValoresDeStudent({
      nomeCompleto: "Ricardo Galdino",
      enderecoCompleto: "Av. Paulista, 1000",
      telefones: [],
      email: "ricardo@exemplo.com"
    });

    expect(valores.telefones).toEqual([""]);
  });
});
