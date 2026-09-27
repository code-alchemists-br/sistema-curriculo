import { describe, expect, it } from "vitest";

import {
  criarCursoVazio,
  normalizarCurso,
  validarCurso,
  validarListaCursos,
  type Curso
} from "./cursos";

const cursoValido: Curso = {
  nome: "React Avançado",
  instituicao: "Alura",
  cargaHoraria: "40"
};

describe("validarCurso", () => {
  it("retorna objeto vazio quando todos os campos são válidos", () => {
    const erros = validarCurso(cursoValido);
    expect(Object.keys(erros)).toHaveLength(0);
  });

  it("reporta nome ausente", () => {
    const erros = validarCurso({ ...cursoValido, nome: "  " });
    expect(erros.nome).toBe("Informe o nome do curso.");
  });

  it("reporta instituição ausente", () => {
    const erros = validarCurso({ ...cursoValido, instituicao: "" });
    expect(erros.instituicao).toBe("Informe a instituição.");
  });

  it("reporta carga horária vazia", () => {
    const erros = validarCurso({ ...cursoValido, cargaHoraria: "" });
    expect(erros.cargaHoraria).toBe("Informe uma carga horária válida (em horas).");
  });

  it("reporta carga horária não numérica", () => {
    const erros = validarCurso({ ...cursoValido, cargaHoraria: "abc" });
    expect(erros.cargaHoraria).toBe("Informe uma carga horária válida (em horas).");
  });

  it("reporta carga horária negativa", () => {
    const erros = validarCurso({ ...cursoValido, cargaHoraria: "-10" });
    expect(erros.cargaHoraria).toBe("Informe uma carga horária válida (em horas).");
  });

  it("reporta carga horária zero", () => {
    const erros = validarCurso({ ...cursoValido, cargaHoraria: "0" });
    expect(erros.cargaHoraria).toBe("Informe uma carga horária válida (em horas).");
  });
});

describe("validarListaCursos", () => {
  it("retorna mapa vazio quando todos os cursos são válidos", () => {
    const erros = validarListaCursos([cursoValido, cursoValido]);
    expect(Object.keys(erros)).toHaveLength(0);
  });

  it("indexa erros pela posição do curso inválido", () => {
    const erros = validarListaCursos([cursoValido, { nome: "", instituicao: "X", cargaHoraria: "10" }]);
    expect(erros[0]).toBeUndefined();
    expect(erros[1]).toHaveProperty("nome");
  });
});

describe("criarCursoVazio", () => {
  it("retorna todos os campos como strings vazias", () => {
    const curso = criarCursoVazio();
    expect(curso.nome).toBe("");
    expect(curso.instituicao).toBe("");
    expect(curso.cargaHoraria).toBe("");
  });
});

describe("normalizarCurso", () => {
  it("remove espaços excedentes de todos os campos", () => {
    const curso = normalizarCurso({
      nome: "  React Avançado  ",
      instituicao: " Alura ",
      cargaHoraria: " 40 "
    });

    expect(curso.nome).toBe("React Avançado");
    expect(curso.instituicao).toBe("Alura");
    expect(curso.cargaHoraria).toBe("40");
  });
});
