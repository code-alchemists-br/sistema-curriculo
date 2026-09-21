// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
import { describe, expect, it } from "vitest";

import { traduzirFalhaAcesso, validarCadastro } from "./formulario-acesso";

describe("validarCadastro", () => {
  it("informa cada correção local sem substituir a validação do servidor", () => {
    expect(
      validarCadastro({ nome: "", email: "invalido", senha: "curta", confirmacaoSenha: "diferente" })
    ).toEqual({
      nome: "Informe seu nome.",
      email: "Informe um e-mail válido.",
      senha: "A senha deve ter ao menos 8 caracteres.",
      confirmacaoSenha: "As senhas não coincidem."
    });
  });
});

describe("traduzirFalhaAcesso", () => {
  it("converte indisponibilidade em uma orientação compreensível", () => {
    expect(traduzirFalhaAcesso("indisponivel")).toContain("indisponível");
  });
});
