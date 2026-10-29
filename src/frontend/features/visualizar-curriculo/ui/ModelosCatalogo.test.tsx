import type { ComponentType } from "react";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import { ModeloAcademico } from "./ModeloAcademico";
import { ModeloAtsSimples } from "./ModeloAtsSimples";
import { ModeloCriativo } from "./ModeloCriativo";
import { ModeloModerno } from "./ModeloModerno";
import { ModeloPrimeiroEmprego } from "./ModeloPrimeiroEmprego";

afterEach(cleanup);

/** Cria uma prévia completa e válida para testar modelos que compartilham o contrato público. */
function criarPrevia(): PreviaCurriculo {
  return {
    curriculo_id: "curriculo-1",
    titulo_versao: "Desenvolvedora front-end",
    layout: "moderno",
    estudante: {
      nome: "Ana Silva",
      email: "ana@example.com",
      contato: {
        endereco: "São Paulo, SP",
        telefones: ["(11) 99999-0000"],
        linkedin: "https://www.linkedin.com/in/ana-silva",
        curriculo_lattes: "https://lattes.cnpq.br/123456789",
      },
    },
    formacoes: [
      {
        id: "formacao-1",
        instituicao: "Universidade Exemplo",
        curso: "Sistemas de Informação",
        nivel: "Graduação",
        status: "Concluído",
        inicio: "2019-01-01",
        fim: "2022-12-01",
      },
    ],
    experiencias: [
      {
        id: "experiencia-1",
        empresa: "Empresa Exemplo",
        cargo: "Desenvolvedora front-end",
        descricao: "Desenvolvimento de interfaces acessíveis.",
        inicio: "2023-01-01",
        fim: null,
      },
    ],
    projetos: [
      {
        id: "projeto-1",
        titulo: "Sistema Currículo",
        descricao: "Aplicação para criação de currículos.",
        tecnologias: "React, TypeScript",
      },
    ],
    competencias: [
      { id: "competencia-1", descricao: "React", nivel: "Avançado" },
    ],
    idiomas: [{ id: "idioma-1", idioma: "Inglês", nivel: "Intermediário" }],
    documentos: [
      {
        id: "documento-1",
        nome_arquivo: "certificado.pdf",
        tipo_arquivo: "PDF",
      },
    ],
  };
}

const modelos: ReadonlyArray<
  [string, ComponentType<{ previa: PreviaCurriculo }>]
> = [
  ["ATS simples", ModeloAtsSimples],
  ["Acadêmico", ModeloAcademico],
  ["Primeiro emprego", ModeloPrimeiroEmprego],
  ["Criativo", ModeloCriativo],
  ["Moderno", ModeloModerno],
];

describe("modelos do catálogo", () => {
  it.each(modelos)(
    "apresenta todos os dados disponíveis no modelo %s",
    (_, Modelo) => {
      render(<Modelo previa={criarPrevia()} />);

      expect(
        screen.getByRole("heading", { level: 1, name: "Ana Silva" }),
      ).toBeInTheDocument();
      expect(screen.getByText("ana@example.com")).toBeInTheDocument();
      expect(screen.getAllByText(/Empresa Exemplo/)[0]).toBeInTheDocument();
      expect(
        screen.getAllByText(/Universidade Exemplo/)[0],
      ).toBeInTheDocument();
      expect(screen.getAllByText(/Sistema Currículo/)[0]).toBeInTheDocument();
      expect(screen.getAllByText(/React/)[0]).toBeInTheDocument();
      expect(screen.getAllByText(/Inglês/)[0]).toBeInTheDocument();
      expect(screen.getByText("certificado.pdf (PDF)")).toBeInTheDocument();
    },
  );

  it.each(modelos)(
    "omite grupos vazios no modelo %s sem esconder o e-mail",
    (_, Modelo) => {
      const previa = criarPrevia();
      previa.estudante.contato = null;
      previa.formacoes = [];
      previa.experiencias = [];
      previa.projetos = [];
      previa.competencias = [];
      previa.idiomas = [];
      previa.documentos = [];

      render(<Modelo previa={previa} />);

      expect(screen.getByText("ana@example.com")).toBeInTheDocument();
      expect(screen.queryByText("(11) 99999-0000")).not.toBeInTheDocument();
      expect(
        screen.queryByRole("heading", { level: 2, name: "Formação acadêmica" }),
      ).not.toBeInTheDocument();
    },
  );

  it.each(modelos)("não altera a prévia recebida no modelo %s", (_, Modelo) => {
    const previa = criarPrevia();
    const copia = structuredClone(previa);

    render(<Modelo previa={previa} />);

    expect(previa).toEqual(copia);
  });

  it("mantém o ATS em uma estrutura sem elementos decorativos de nível", () => {
    const { container } = render(<ModeloAtsSimples previa={criarPrevia()} />);

    expect(container.querySelector(".modelo-ats-simples")).toBeInTheDocument();
    expect(
      container.querySelector('[aria-hidden="true"]'),
    ).not.toBeInTheDocument();
  });

  it("prioriza formação e projetos antes da experiência no modelo Acadêmico", () => {
    render(<ModeloAcademico previa={criarPrevia()} />);

    expect(
      screen
        .getAllByRole("heading", { level: 2 })
        .map((elemento) => elemento.textContent),
    ).toEqual([
      "Formação acadêmica",
      "Projetos acadêmicos",
      "Documentos complementares",
      "Experiência profissional relevante",
      "Competências",
      "Idiomas",
    ]);
  });

  it("prioriza formação, projetos e competências antes da experiência no modelo Primeiro emprego", () => {
    render(<ModeloPrimeiroEmprego previa={criarPrevia()} />);

    expect(
      screen
        .getAllByRole("heading", { level: 2 })
        .map((elemento) => elemento.textContent),
    ).toEqual([
      "Formação acadêmica",
      "Projetos acadêmicos",
      "Competências",
      "Idiomas",
      "Documentos complementares",
      "Experiência profissional",
    ]);
  });
});
