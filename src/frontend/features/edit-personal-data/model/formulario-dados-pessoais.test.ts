import { describe, expect, it } from "vitest";

import {
  criarStudent,
  criarValoresIniciais,
  validarDadosPessoais
} from "./formulario-dados-pessoais";

describe("validarDadosPessoais", () => {
  it("indica os campos obrigatórios e cada telefone vazio", () => {
    expect(
      validarDadosPessoais({
        ...criarValoresIniciais(),
        telefones: ["", ""],
        email: "email-invalido"
      })
    ).toEqual({
      nomeCompleto: "Informe seu nome completo.",
      enderecoCompleto: "Informe seu endereço completo.",
      email: "Informe um e-mail válido.",
      telefones: {
        0: "Informe um telefone.",
        1: "Informe um telefone."
      }
    });
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
        curriculoLattes: " "
      })
    ).toEqual({
      nomeCompleto: "Ana Silva",
      enderecoCompleto: "Rua das Flores, 10",
      telefones: ["(11) 99999-0000"],
      email: "ana@exemplo.com"
    });
  });
});
