import { describe, expect, it } from "vitest";

import {
  LIMITES_FORMACAO_ACADEMICA,
  criarValoresIniciaisFormacao,
  restringirAno4Digitos,
  validarFormacaoAcademica,
  type ValoresFormacaoAcademica,
} from "./formulario-formacao-academica";

const formacaoValida: ValoresFormacaoAcademica = {
  instituicao: "FATEC São Paulo",
  curso: "Análise e Desenvolvimento de Sistemas",
  nivel: "tecnologo",
  dataInicio: "2022-02-01",
  dataFim: "2024-12-01",
  status: "concluido",
  curriculoLattes: "",
  naoPossuiLattes: false,
};

describe("formulario-formacao-academica — limites e validação de datas", () => {
  it("valida formação correta sem retornar erros", () => {
    const erros = validarFormacaoAcademica(formacaoValida, false, "2026-11-08");
    expect(Object.keys(erros)).toHaveLength(0);
  });

  describe("LIMITES_FORMACAO_ACADEMICA", () => {
    it("estabelece 100 caracteres como limite máximo de instituição e curso", () => {
      expect(LIMITES_FORMACAO_ACADEMICA.instituicaoMax).toBe(100);
      expect(LIMITES_FORMACAO_ACADEMICA.cursoMax).toBe(100);
    });

    it("rejeita instituição com mais de 100 caracteres", () => {
      const erros = validarFormacaoAcademica({
        ...formacaoValida,
        instituicao: "A".repeat(101),
      });
      expect(erros.instituicao).toBe(
        "A instituição deve ter no máximo 100 caracteres.",
      );
    });

    it("rejeita curso com mais de 100 caracteres", () => {
      const erros = validarFormacaoAcademica({
        ...formacaoValida,
        curso: "B".repeat(101),
      });
      expect(erros.curso).toBe("O curso deve ter no máximo 100 caracteres.");
    });
  });

  describe("restringirAno4Digitos", () => {
    it("trunca anos digitados com mais de 4 dígitos", () => {
      expect(restringirAno4Digitos("20265-02-01")).toBe("2026-02-01");
      expect(restringirAno4Digitos("19999-10")).toBe("1999-10");
    });

    it("mantém inalteradas datas válidas com ano de 4 dígitos", () => {
      expect(restringirAno4Digitos("2024-02-01")).toBe("2024-02-01");
      expect(restringirAno4Digitos("2023-08")).toBe("2023-08");
    });

    it("retorna string vazia quando informado valor vazio", () => {
      expect(restringirAno4Digitos("")).toBe("");
    });
  });

  describe("Restrição de ano para no máximo 4 dígitos na validação", () => {
    it("rejeita data de início com ano superior a 4 dígitos", () => {
      const erros = validarFormacaoAcademica({
        ...formacaoValida,
        dataInicio: "20261-01-01",
      });
      expect(erros.dataInicio).toBe(
        "O ano de início deve ter no máximo 4 dígitos.",
      );
    });

    it("rejeita data final com ano superior a 4 dígitos", () => {
      const erros = validarFormacaoAcademica({
        ...formacaoValida,
        dataFim: "20261-12-01",
      });
      expect(erros.dataFim).toBe("O ano deve ter no máximo 4 dígitos.");
    });
  });

  describe("Regras temporais de início e término", () => {
    it("rejeita data de início no futuro", () => {
      const erros = validarFormacaoAcademica(
        {
          ...formacaoValida,
          dataInicio: "2030-01-01",
        },
        false,
        "2026-11-08",
      );
      expect(erros.dataInicio).toBe(
        "A data de início não pode ser posterior à data atual.",
      );
    });

    it("rejeita data de conclusão no futuro para formação concluída", () => {
      const erros = validarFormacaoAcademica(
        {
          ...formacaoValida,
          status: "concluido",
          dataFim: "2030-12-01",
        },
        false,
        "2026-11-08",
      );
      expect(erros.dataFim).toBe(
        "A data de conclusão não pode ser posterior à data atual.",
      );
    });

    it("rejeita data final anterior à data de início", () => {
      const erros = validarFormacaoAcademica(
        {
          ...formacaoValida,
          dataInicio: "2024-01-01",
          dataFim: "2022-01-01",
        },
        false,
        "2026-11-08",
      );
      expect(erros.dataFim).toBe(
        "A data final não pode ser anterior à data de início.",
      );
    });
  });

  describe("criarValoresIniciaisFormacao", () => {
    it("retorna estrutura com todos os campos limpos", () => {
      const inicial = criarValoresIniciaisFormacao();
      expect(inicial.instituicao).toBe("");
      expect(inicial.curso).toBe("");
      expect(inicial.status).toBe("");
      expect(inicial.naoPossuiLattes).toBe(false);
    });
  });
});
