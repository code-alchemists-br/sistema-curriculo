import { describe, expect, it } from "vitest";

import {
  criarStudent,
  criarValoresIniciais,
  validarDadosPessoais,
} from "./formulario-dados-pessoais";

describe("validarDadosPessoais", () => {
  it("indica os campos obrigatórios e cada telefone vazio", () => {
    expect(
      validarDadosPessoais({
        ...criarValoresIniciais(),
        telefones: ["", ""],
        email: "email-invalido",
      }),
    ).toEqual({
      nomeCompleto: "Informe seu nome completo.",
      email: "Informe um e-mail válido.",
      telefones: {
        0: "Informe um telefone.",
        1: "Informe um telefone.",
      },
    });
  });

  it("rejeita campos que excedem os limites máximos de caracteres", () => {
    const erros = validarDadosPessoais({
      nomeCompleto: "a".repeat(101),
      email: `${"b".repeat(95)}@teste.com`,
      enderecoCompleto: "c".repeat(151),
      telefones: ["(11) 99999-9999"],
      linkedIn: "",
      curriculoLattes: "",
    });

    expect(erros.nomeCompleto).toBe(
      "O nome deve ter no máximo 100 caracteres.",
    );
    expect(erros.email).toBe("O e-mail deve ter no máximo 100 caracteres.");
    expect(erros.enderecoCompleto).toBe(
      "O endereço deve ter no máximo 150 caracteres.",
    );
  });
});

describe("criarStudent", () => {
  it("remove campos opcionais vazios e normaliza os valores", () => {
    expect(
      criarStudent({
        nomeCompleto: "  Ana Silva  ",
        enderecoCompleto: " Rua das Flores, 10 ",
        telefones: [" (11) 99999-0000 "],
        email: " ana@exemplo.com ",
        linkedIn: " ",
        curriculoLattes: " ",
      }),
    ).toEqual({
      nomeCompleto: "Ana Silva",
      enderecoCompleto: "Rua das Flores, 10",
      telefones: ["(11) 99999-0000"],
      email: "ana@exemplo.com",
    });
  });
});
