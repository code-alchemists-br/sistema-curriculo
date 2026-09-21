// Proveniência: decision-analysis prompts/frontend/20260921-120136-tela-cadastro-projetos-academicos-v001.md#v001
import { describe, expect, it } from "vitest";

import {
  traduzirFalhaCadastroProjeto,
  validarProjetoAcademico
} from "./formulario-projeto-academico";

describe("validarProjetoAcademico", () => {
  it("indica título e descrição ausentes sem impor formato de tecnologias", () => {
    expect(
      validarProjetoAcademico({ titulo: " ", descricao: "", tecnologias: "" })
    ).toEqual({
      titulo: "Informe o título do projeto.",
      descricao: "Descreva o objetivo ou sua contribuição no projeto."
    });
  });
});

describe("traduzirFalhaCadastroProjeto", () => {
  it("orienta o estudante quando o cadastro ainda está indisponível", () => {
    expect(traduzirFalhaCadastroProjeto("indisponivel")).toContain("indisponível");
  });
});
