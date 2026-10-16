import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import { ModeloCompacto } from "./ModeloCompacto";

afterEach(cleanup);

/** Cria uma prévia completa e determinística para os testes do modelo. */
function criarPrevia(): PreviaCurriculo {
  return {
    curriculo_id: "curriculo-1",
    titulo_versao: "Estágio em TI",
    layout: "compacto",
    estudante: {
      nome: "Ana Carolina da Silva",
      email: "ana.silva@fatec.sp.gov.br",
      contato: {
        endereco: "Avenida Tiradentes, 615",
        telefones: ["(11) 98765-4321"],
        linkedin: "https://linkedin.com/in/ana",
        curriculo_lattes: null,
      },
    },
    formacoes: [
      {
        id: "formacao-1",
        instituicao: "FATEC-SP",
        curso: "Análise e Desenvolvimento de Sistemas",
        nivel: "Tecnólogo",
        status: "Em andamento",
        inicio: "2023-02-01",
        fim: null,
      },
    ],
    experiencias: [
      {
        id: "experiencia-1",
        empresa: "Empresa Exemplo",
        cargo: "Estagiária de Desenvolvimento",
        descricao: "Desenvolvimento de aplicações web.",
        inicio: "2024-01-15",
        fim: null,
      },
    ],
    projetos: [
      {
        id: "projeto-1",
        titulo: "Sistema Currículo",
        descricao: "Plataforma para elaboração de currículos.",
        tecnologias: "React, TypeScript",
      },
    ],
    competencias: [
      { id: "competencia-1", descricao: "TypeScript", nivel: "Intermediário" },
    ],
    idiomas: [{ id: "idioma-1", idioma: "Inglês", nivel: "Avançado" }],
    documentos: [
      {
        id: "documento-1",
        nome_arquivo: "certificado.pdf",
        tipo_arquivo: "application/pdf",
      },
    ],
  };
}

describe("ModeloCompacto", () => {
  it("apresenta todas as informações recebidas pelo contrato de prévia", () => {
    render(<ModeloCompacto previa={criarPrevia()} />);

    expect(
      screen.getByRole("heading", { name: "Ana Carolina da Silva" }),
    ).toBeInTheDocument();
    expect(screen.getByText("ana.silva@fatec.sp.gov.br")).toBeInTheDocument();
    expect(screen.getByText("FATEC-SP")).toBeInTheDocument();
    expect(screen.getByText("Empresa Exemplo")).toBeInTheDocument();
    expect(screen.getByText("Sistema Currículo")).toBeInTheDocument();
    expect(screen.getByText("TypeScript — Intermediário")).toBeInTheDocument();
    expect(screen.getByText("Inglês — Avançado")).toBeInTheDocument();
    expect(
      screen.getByText("certificado.pdf (application/pdf)"),
    ).toBeInTheDocument();
  });

  it("oculta seções vazias e contato opcional ausente", () => {
    const previa = criarPrevia();
    previa.estudante.contato = null;
    previa.formacoes = [];
    previa.experiencias = [];
    previa.projetos = [];
    previa.competencias = [];
    previa.idiomas = [];
    previa.documentos = [];

    render(<ModeloCompacto previa={previa} />);

    expect(
      screen.queryByRole("heading", { name: "Formação acadêmica" }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("heading", { name: "Experiência profissional" }),
    ).not.toBeInTheDocument();
    expect(screen.queryByText("(11) 98765-4321")).not.toBeInTheDocument();
    expect(screen.getByText("ana.silva@fatec.sp.gov.br")).toBeInTheDocument();
  });

  it("não altera os dados recebidos", () => {
    const previa = criarPrevia();
    const original = JSON.parse(JSON.stringify(previa)) as PreviaCurriculo;

    render(<ModeloCompacto previa={previa} />);

    expect(previa).toEqual(original);
  });

  it("renderiza visualização de estado vazio nas seções quando exibirSecoesVazias for true", () => {
    const previa = criarPrevia();
    previa.formacoes = [];
    previa.experiencias = [];

    render(<ModeloCompacto exibirSecoesVazias previa={previa} />);

    expect(
      screen.getByRole("heading", { name: "Formação acadêmica" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        "Nenhum item selecionado ou cadastrado para formação acadêmica.",
      ),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { name: "Experiência profissional" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        "Nenhum item selecionado ou cadastrado para experiência profissional.",
      ),
    ).toBeInTheDocument();
  });
});
