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
});

describe("traduzirFalhaCadastroProjeto", () => {
  it("orienta o estudante quando o cadastro ainda está indisponível", () => {
    expect(traduzirFalhaCadastroProjeto("indisponivel")).toContain(
      "indisponível",
    );
  });
});
