import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import { ModeloClassico } from "./ModeloClassico";

afterEach(cleanup);

/** Cria uma prévia de currículo completa e determinística para os testes unitários. */
function criarPrevia(): PreviaCurriculo {
  return {
    curriculo_id: "curriculo-1",
    titulo_versao: "Estágio em TI",
    layout: "classico",
    estudante: {
      nome: "Ricardo Galdino de Sampaio",
      email: "ricardo.sampaio@fatec.sp.gov.br",
      contato: {
        endereco: "Avenida Tiradentes, 615, Bom Retiro, São Paulo - SP",
        telefones: ["(11) 98765-4321", "(11) 91234-5678"],
        linkedin: "https://linkedin.com/in/ricardosampaio",
        curriculo_lattes: "https://lattes.cnpq.br/1234567890",
      },
    },
    formacoes: [
      {
        id: "formacao-1",
        instituicao: "FATEC São Paulo",
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
        empresa: "Empresa de Tecnologia Ltda",
        cargo: "Estagiário de Frontend",
        descricao:
          "Desenvolvimento de interfaces acessíveis utilizando React e TypeScript.",
        inicio: "2024-01-15",
        fim: "2024-12-20",
      },
    ],
    projetos: [
      {
        id: "projeto-1",
        titulo: "Sistema Currículo",
        descricao:
          "Plataforma de preparação e construção de currículos profissionais.",
        tecnologias: "React, TypeScript, CSS",
      },
    ],
    competencias: [
      { id: "comp-1", descricao: "TypeScript", nivel: "Avançado" },
      { id: "comp-2", descricao: "Acessibilidade Web (WCAG)", nivel: null! },
    ],
    idiomas: [{ id: "idioma-1", idioma: "Inglês", nivel: "Intermediário" }],
    documentos: [
      {
        id: "doc-1",
        nome_arquivo: "certificado-react.pdf",
        tipo_arquivo: "application/pdf",
      },
      {
        id: "doc-2",
        nome_arquivo: "declaracao-matricula.pdf",
        tipo_arquivo: "",
      },
    ],
  };
}

describe("ModeloClassico", () => {
  it("apresenta todas as seções e dados recebidos pelo contrato de prévia", () => {
    render(<ModeloClassico previa={criarPrevia()} />);

    expect(
      screen.getByRole("heading", {
        level: 1,
        name: "Ricardo Galdino de Sampaio",
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("ricardo.sampaio@fatec.sp.gov.br"),
    ).toBeInTheDocument();
    expect(screen.getByText("(11) 98765-4321")).toBeInTheDocument();
    expect(screen.getByText("(11) 91234-5678")).toBeInTheDocument();
    expect(
      screen.getByText("Avenida Tiradentes, 615, Bom Retiro, São Paulo - SP"),
    ).toBeInTheDocument();

    const linkLinkedin = screen.getByRole("link", { name: "LinkedIn" });
    expect(linkLinkedin).toHaveAttribute(
      "href",
      "https://linkedin.com/in/ricardosampaio",
    );
    expect(linkLinkedin).toHaveAttribute("target", "_blank");

    const linkLattes = screen.getByRole("link", { name: "Currículo Lattes" });
    expect(linkLattes).toHaveAttribute(
      "href",
      "https://lattes.cnpq.br/1234567890",
    );

    expect(
      screen.getByRole("heading", { level: 2, name: "Formação acadêmica" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Análise e Desenvolvimento de Sistemas"),
    ).toBeInTheDocument();
    expect(screen.getByText("FATEC São Paulo")).toBeInTheDocument();
    expect(screen.getByText("Tecnólogo — Em andamento")).toBeInTheDocument();
    expect(screen.getByText(/01\/02\/2023 — Atual/)).toBeInTheDocument();

    expect(
      screen.getByRole("heading", {
        level: 2,
        name: "Experiência profissional",
      }),
    ).toBeInTheDocument();
    expect(screen.getByText("Estagiário de Frontend")).toBeInTheDocument();
    expect(screen.getByText("Empresa de Tecnologia Ltda")).toBeInTheDocument();
    expect(
      screen.getByText(
        "Desenvolvimento de interfaces acessíveis utilizando React e TypeScript.",
      ),
    ).toBeInTheDocument();
    expect(screen.getByText(/15\/01\/2024 — 20\/12\/2024/)).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { level: 2, name: "Projetos acadêmicos" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Sistema Currículo")).toBeInTheDocument();
    expect(
      screen.getByText(
        "Plataforma de preparação e construção de currículos profissionais.",
      ),
    ).toBeInTheDocument();
    expect(screen.getByText("React, TypeScript, CSS")).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { level: 2, name: "Competências" }),
    ).toBeInTheDocument();
    expect(screen.getByText("TypeScript")).toBeInTheDocument();
    expect(screen.getByText("(Avançado)")).toBeInTheDocument();
    expect(screen.getByText("Acessibilidade Web (WCAG)")).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { level: 2, name: "Idiomas" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Inglês")).toBeInTheDocument();
    expect(screen.getByText("— Intermediário")).toBeInTheDocument();

    expect(
      screen.getByRole("heading", {
        level: 2,
        name: "Documentos complementares",
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("certificado-react.pdf (application/pdf)"),
    ).toBeInTheDocument();
    expect(screen.getByText("declaracao-matricula.pdf")).toBeInTheDocument();
  });

  it("oculta seções vazias e contatos opcionais não informados", () => {
    const previa = criarPrevia();
    previa.estudante.contato = null;
    previa.formacoes = [];
    previa.experiencias = [];
    previa.projetos = [];
    previa.competencias = [];
    previa.idiomas = [];
    previa.documentos = [];

    render(<ModeloClassico previa={previa} />);

    expect(
      screen.queryByRole("heading", { level: 2, name: "Formação acadêmica" }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("heading", {
        level: 2,
        name: "Experiência profissional",
      }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("heading", { level: 2, name: "Projetos acadêmicos" }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("heading", { level: 2, name: "Competências" }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("heading", { level: 2, name: "Idiomas" }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("heading", {
        level: 2,
        name: "Documentos complementares",
      }),
    ).not.toBeInTheDocument();

    expect(
      screen.queryByRole("link", { name: "LinkedIn" }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("link", { name: "Currículo Lattes" }),
    ).not.toBeInTheDocument();
  });

  it("não altera os dados recebidos (imutabilidade)", () => {
    const previa = criarPrevia();
    const previaOriginal = JSON.parse(
      JSON.stringify(previa),
    ) as PreviaCurriculo;

    render(<ModeloClassico previa={previa} />);

    expect(previa).toEqual(previaOriginal);
  });
});
