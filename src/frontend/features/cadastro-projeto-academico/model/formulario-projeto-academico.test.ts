// Proveniência: decision-analysis prompts/frontend/20260921-120136-tela-cadastro-projetos-academicos-v001.md#v001
import { describe, expect, it } from "vitest";

import {
  traduzirFalhaCadastroProjeto,
  validarProjetoAcademico,
} from "./formulario-projeto-academico";

describe("validarProjetoAcademico", () => {
  it("indica título, descrição e tecnologias ausentes quando vazios", () => {
    expect(
      validarProjetoAcademico({ titulo: " ", descricao: "", tecnologias: "" }),
    ).toEqual({
      titulo: "Informe o título do projeto.",
      descricao: "Descreva o objetivo ou sua contribuição no projeto.",
      tecnologias: "Informe as tecnologias utilizadas no projeto.",
    });
  });

  it("não aponta erros quando todos os campos obrigatórios estão preenchidos", () => {
    expect(
      validarProjetoAcademico({
        titulo: "Sistema Currículo",
        descricao: "Plataforma para elaboração de currículos.",
        tecnologias: "React, TypeScript",
      }),
    ).toEqual({});
  });

  it("rejeita campos que excedem os limites máximos de caracteres", () => {
    const erros = validarProjetoAcademico({
      titulo: "a".repeat(101),
      descricao: "b".repeat(1501),
      tecnologias: "c".repeat(201),
    });

    expect(erros.titulo).toBe("O título deve ter no máximo 100 caracteres.");
    expect(erros.descricao).toBe(
      "A descrição deve ter no máximo 1500 caracteres.",
    );
    expect(erros.tecnologias).toBe(
      "As tecnologias devem ter no máximo 200 caracteres.",
    );
  });
});

describe("traduzirFalhaCadastroProjeto", () => {
  it("orienta o estudante quando o cadastro ainda está indisponível", () => {
    expect(traduzirFalhaCadastroProjeto("indisponivel")).toContain(
      "indisponível",
    );
  });
});
