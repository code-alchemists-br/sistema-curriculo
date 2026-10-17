import { describe, expect, it } from "vitest";

import {
  criarCertificacaoVazia,
  LIMITE_CARACTERES_CERTIFICACAO,
  normalizarCertificacao,
  validarCertificacao,
  type ValoresCertificacao,
} from "./certificacao";

describe("certificacao model", () => {
  describe("criarCertificacaoVazia", () => {
    it("retorna objeto inicial com campos vazios", () => {
      expect(criarCertificacaoVazia()).toEqual({
        nome: "",
        organizacaoEmissora: "",
      });
    });
  });

  describe("validarCertificacao", () => {
    it("aceita certificação com dados válidos", () => {
      const valores: ValoresCertificacao = {
        nome: "AWS Certified Solutions Architect",
        organizacaoEmissora: "Amazon Web Services",
      };
      expect(validarCertificacao(valores)).toEqual({});
    });

    it("rejeita campos vazios ou contendo apenas espaços", () => {
      const valores: ValoresCertificacao = {
        nome: "   ",
        organizacaoEmissora: "\t\n  ",
      };
      const erros = validarCertificacao(valores);

      expect(erros.nome).toBe("Informe o nome da certificação.");
      expect(erros.organizacaoEmissora).toBe(
        "Informe a instituição ou organização emissora.",
      );
    });

    it("rejeita campos que excedem o limite de caracteres", () => {
      const textoLongo = "A".repeat(LIMITE_CARACTERES_CERTIFICACAO + 1);
      const valores: ValoresCertificacao = {
        nome: textoLongo,
        organizacaoEmissora: textoLongo,
      };
      const erros = validarCertificacao(valores);

      expect(erros.nome).toBe(
        `O nome da certificação deve ter no máximo ${LIMITE_CARACTERES_CERTIFICACAO} caracteres.`,
      );
      expect(erros.organizacaoEmissora).toBe(
        `A organização emissora deve ter no máximo ${LIMITE_CARACTERES_CERTIFICACAO} caracteres.`,
      );
    });
  });

  describe("normalizarCertificacao", () => {
    it("apara espaços das extremidades e comprime espaços internos múltiplos", () => {
      const valores: ValoresCertificacao = {
        nome: "   AWS    Certified    Solutions   Architect   ",
        organizacaoEmissora: "   Amazon    Web    Services   ",
      };
      expect(normalizarCertificacao(valores)).toEqual({
        nome: "AWS Certified Solutions Architect",
        organizacaoEmissora: "Amazon Web Services",
      });
    });
  });
});
