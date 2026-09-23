import { describe, expect, it } from "vitest";

import {
  adicionarHabilidade,
  habilidadeJaExiste,
  normalizarHabilidade,
  removerHabilidade
} from "./habilidades";

describe("normalizarHabilidade", () => {
  it("remove espaços no início e no final", () => {
    expect(normalizarHabilidade("  JavaScript  ")).toBe("JavaScript");
  });
});

describe("adicionarHabilidade", () => {
  it("adiciona uma nova habilidade", () => {
    expect(adicionarHabilidade(["Java"], "Python")).toEqual(["Java", "Python"]);
  });

  it("não adiciona uma habilidade vazia", () => {
    expect(adicionarHabilidade(["Java"], "   ")).toEqual(["Java"]);
  });

  it("não adiciona habilidades duplicadas", () => {
    expect(adicionarHabilidade(["Java"], "Java")).toEqual(["Java"]);
  });

  it("não adiciona duplicada ignorando maiúsculas e minúsculas", () => {
    expect(adicionarHabilidade(["JavaScript"], "javascript")).toEqual([
      "JavaScript"
    ]);
  });
});

describe("habilidadeJaExiste", () => {
  it("identifica uma habilidade existente", () => {
    expect(habilidadeJaExiste(["Java", "Python"], "Python")).toBe(true);
  });

  it("identifica quando a habilidade não existe", () => {
    expect(habilidadeJaExiste(["Java", "Python"], "React")).toBe(false);
  });
});

describe("removerHabilidade", () => {
  it("remove a habilidade informada", () => {
    expect(removerHabilidade(["Java", "Python"], "Java")).toEqual(["Python"]);
  });
});
