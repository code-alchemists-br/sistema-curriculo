import { describe, expect, it } from "vitest";

import {
  criarExperienciaVazia,
  ordenarPorDataDecrescente,
  validarExperiencia,
  validarListaExperiencias,
  type Experiencia
} from "./experiencias";

const experienciaValida: Experiencia = {
  empresa: "Tech Corp",
  cargo: "Desenvolvedor Frontend",
  inicio: "2024-01",
  fim: "2025-06",
  empregoAtual: false,
  descricao: "Desenvolvimento de interfaces com React."
};

describe("validarExperiencia", () => {
  it("retorna objeto vazio quando todos os campos são válidos", () => {
    const erros = validarExperiencia(experienciaValida);
    expect(Object.keys(erros)).toHaveLength(0);
  });

  it("reporta empresa ausente", () => {
    const erros = validarExperiencia({ ...experienciaValida, empresa: "  " });
    expect(erros.empresa).toBe("Informe o nome da empresa.");
  });

  it("reporta cargo ausente", () => {
    const erros = validarExperiencia({ ...experienciaValida, cargo: "" });
    expect(erros.cargo).toBe("Informe o cargo exercido.");
  });

  it("reporta data de início ausente", () => {
    const erros = validarExperiencia({ ...experienciaValida, inicio: "" });
    expect(erros.inicio).toBe("Informe a data de início.");
  });

  it("reporta data de término ausente quando não é emprego atual", () => {
    const erros = validarExperiencia({ ...experienciaValida, fim: "" });
    expect(erros.fim).toBe("Informe a data de término ou marque como emprego atual.");
  });

  it("ignora data de término quando é emprego atual", () => {
    const erros = validarExperiencia({ ...experienciaValida, fim: "", empregoAtual: true });
    expect(erros.fim).toBeUndefined();
  });

  it("reporta data de término anterior à data de início", () => {
    const erros = validarExperiencia({ ...experienciaValida, inicio: "2025-06", fim: "2024-01" });
    expect(erros.fim).toBe("A data de término deve ser posterior à data de início.");
  });

  it("aceita descrição vazia sem erro", () => {
    const erros = validarExperiencia({ ...experienciaValida, descricao: "" });
    expect(Object.keys(erros)).toHaveLength(0);
  });
});

describe("validarListaExperiencias", () => {
  it("retorna mapa vazio quando todas as experiências são válidas", () => {
    const erros = validarListaExperiencias([experienciaValida]);
    expect(Object.keys(erros)).toHaveLength(0);
  });

  it("indexa erros pela posição da experiência inválida", () => {
    const erros = validarListaExperiencias([
      experienciaValida,
      { ...experienciaValida, empresa: "" }
    ]);
    expect(erros[0]).toBeUndefined();
    expect(erros[1]).toHaveProperty("empresa");
  });
});

describe("ordenarPorDataDecrescente", () => {
  it("posiciona emprego atual antes das demais experiências", () => {
    const resultado = ordenarPorDataDecrescente([
      { ...experienciaValida, inicio: "2020-01", empregoAtual: false },
      { ...experienciaValida, inicio: "2023-01", empregoAtual: true }
    ]);

    expect(resultado[0].empregoAtual).toBe(true);
  });

  it("ordena experiências não atuais da mais recente para a mais antiga", () => {
    const resultado = ordenarPorDataDecrescente([
      { ...experienciaValida, inicio: "2020-01" },
      { ...experienciaValida, inicio: "2023-06" },
      { ...experienciaValida, inicio: "2021-03" }
    ]);

    expect(resultado[0].inicio).toBe("2023-06");
    expect(resultado[1].inicio).toBe("2021-03");
    expect(resultado[2].inicio).toBe("2020-01");
  });

  it("não altera o array original", () => {
    const original = [
      { ...experienciaValida, inicio: "2020-01" },
      { ...experienciaValida, inicio: "2023-06" }
    ];
    const copia = [...original];
    ordenarPorDataDecrescente(original);

    expect(original[0].inicio).toBe(copia[0].inicio);
    expect(original[1].inicio).toBe(copia[1].inicio);
  });
});

describe("criarExperienciaVazia", () => {
  it("retorna todos os campos vazios e emprego atual como false", () => {
    const exp = criarExperienciaVazia();
    expect(exp.empresa).toBe("");
    expect(exp.cargo).toBe("");
    expect(exp.inicio).toBe("");
    expect(exp.fim).toBe("");
    expect(exp.empregoAtual).toBe(false);
    expect(exp.descricao).toBe("");
  });
});
