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
      enderecoCompleto: "Informe seu endereço.",
      cidade: "Informe sua cidade.",
      email: "Informe um e-mail válido.",
      telefones: {
        0: "Informe um telefone.",
        1: "Informe um telefone.",
      },
    });
  });

  it("rejeita mais de cinco telefones, mesmo quando os valores chegam por estado restaurado", () => {
    const erros = validarDadosPessoais({
      nomeCompleto: "Ana Silva",
      enderecoCompleto: "Rua das Flores, 10",
      cidade: "São Paulo",
      telefones: ["1", "2", "3", "4", "5", "6"],
      email: "ana@exemplo.com",
      linkedIn: "",
      curriculoLattes: "",
    });

    expect(erros.telefones).toEqual({
      5: "Informe no máximo 5 telefones.",
    });
  });
});

describe("criarStudent", () => {
  it("remove campos opcionais vazios e normaliza os valores", () => {
    expect(
      criarStudent({
        nomeCompleto: "  Ana Silva  ",
        enderecoCompleto: " Rua das Flores, 10 ",
        cidade: " São Paulo ",
        telefones: [" (11) 99999-0000 "],
        email: " ana@exemplo.com ",
        linkedIn: " ",
        curriculoLattes: " ",
      }),
    ).toEqual({
      nomeCompleto: "Ana Silva",
      enderecoCompleto: "Rua das Flores, 10",
      cidade: "São Paulo",
      telefones: ["(11) 99999-0000"],
      email: "ana@exemplo.com",
    });
  });
});
