import { describe, expect, it } from "vitest";

import { validarCurriculo, type CurriculoParaValidacao } from "./validacao-curriculo";

const curriculoValido: CurriculoParaValidacao = {
  dadosPessoais: {
    nomeCompleto: "Marina Alves",
    enderecoCompleto: "Rua das Acácias, 120",
    telefones: ["11999990000"],
    email: "marina.alves@example.com"
  },
  formacaoAcademica: { status: "preenchida" },
  experienciasProfissionais: { status: "preenchida" },
  competencias: {
    hardSkills: ["TypeScript"],
    softSkills: ["Comunicação"]
  },
  projetosAcademicos: [
    {
      titulo: "Portal de Biblioteca",
      descricao: "Aplicação acadêmica para consulta de acervo.",
      tecnologias: "React, TypeScript"
    }
  ]
};

describe("validarCurriculo", () => {
  it("libera prévia e PDF quando todas as seções obrigatórias estão válidas", () => {
    const resultado = validarCurriculo(curriculoValido);

    expect(resultado.valido).toBe(true);
    expect(resultado.podeVisualizarPreview).toBe(true);
    expect(resultado.podeExportarPdf).toBe(true);
    expect(resultado.secoes.every((secao) => secao.status === "valida")).toBe(true);
  });

  it("identifica uma etapa pulada como pendência e bloqueia as ações finais", () => {
    const resultado = validarCurriculo({
      ...curriculoValido,
      experienciasProfissionais: {
        status: "pulada",
        mensagemErro: "A etapa de experiências profissionais foi ignorada."
      }
    });

    const experiencia = resultado.secoes.find(
      (secao) => secao.id === "experiencias-profissionais"
    );

    expect(resultado.valido).toBe(false);
    expect(resultado.podeVisualizarPreview).toBe(false);
    expect(resultado.podeExportarPdf).toBe(false);
    expect(experiencia).toMatchObject({
      status: "pendente",
      mensagens: ["A etapa de experiências profissionais foi ignorada."]
    });
  });

  it("lista erros de dados pessoais e competências", () => {
    const resultado = validarCurriculo({
      ...curriculoValido,
      dadosPessoais: {
        nomeCompleto: "",
        enderecoCompleto: "",
        telefones: [""],
        email: "email-invalido"
      },
      competencias: { hardSkills: [], softSkills: [] }
    });

    expect(resultado.valido).toBe(false);
    expect(resultado.secoes.find((secao) => secao.id === "dados-pessoais")).toMatchObject({
      status: "erro"
    });
    expect(resultado.secoes.find((secao) => secao.id === "competencias")).toMatchObject({
      status: "erro"
    });
  });

  it("preserva projetos acadêmicos como opcionais, sem bloquear a revisão final", () => {
    const resultado = validarCurriculo({
      ...curriculoValido,
      projetosAcademicos: []
    });

    expect(resultado.valido).toBe(true);
  });

  it("usa dados fictícios no double de uma etapa preenchida com erro", () => {
    const resultado = validarCurriculo({
      ...curriculoValido,
      formacaoAcademica: {
        status: "preenchida",
        mensagemErro: "A formação cadastrada está incompleta."
      }
    });

    expect(resultado.secoes.find((secao) => secao.id === "formacao-academica")).toMatchObject({
      status: "erro",
      mensagens: ["A formação cadastrada está incompleta."]
    });
  });
});
