import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaFormacaoAcademica,
  type ClienteFormacaoAcademica,
} from "../api/cliente-formacao-academica";
import { FormularioFormacaoAcademica } from "./FormularioFormacaoAcademica";

afterEach(cleanup);

async function preencherFormacao(
  usuario: ReturnType<typeof userEvent.setup>,
): Promise<void> {
  await usuario.type(screen.getByLabelText("Instituição"), "FATEC São Paulo");
  await usuario.type(
    screen.getByLabelText("Curso"),
    "Análise e Desenvolvimento de Sistemas",
  );
  await usuario.selectOptions(
    screen.getByLabelText("Nível de formação"),
    "tecnologo",
  );
  await usuario.type(screen.getByLabelText("Data de início"), "2024-02-01");
  await usuario.selectOptions(
    screen.getByLabelText("Situação"),
    "em_andamento",
  );
}

describe("FormularioFormacaoAcademica", () => {
  it("mostra erros associados aos campos obrigatórios", async () => {
    const usuario = userEvent.setup();
    render(<FormularioFormacaoAcademica cliente={{ cadastrar: vi.fn() }} />);

    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(
      await screen.findByText("Informe a instituição."),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Instituição")).toHaveAttribute(
      "aria-invalid",
      "true",
    );
    expect(screen.getByRole("alert")).toHaveTextContent(
      "Revise os campos destacados",
    );
  });

  it("envia valores normalizados ao cliente injetado", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteFormacaoAcademica = {
      cadastrar: vi.fn().mockResolvedValue(undefined),
    };
    render(<FormularioFormacaoAcademica cliente={cliente} />);

    await preencherFormacao(usuario);
    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(cliente.cadastrar).toHaveBeenCalledWith({
      instituicao: "FATEC São Paulo",
      curso: "Análise e Desenvolvimento de Sistemas",
      nivel: "tecnologo",
      dataInicio: "2024-02-01",
      status: "em_andamento",
    });
    expect(await screen.findByRole("status")).toHaveTextContent(
      "enviada para registro",
    );
  });

  it("preserva os valores e informa falha compreensível", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteFormacaoAcademica = {
      cadastrar: vi
        .fn()
        .mockRejectedValue(new FalhaFormacaoAcademica("indisponivel")),
    };
    render(<FormularioFormacaoAcademica cliente={cliente} />);

    await preencherFormacao(usuario);
    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(await screen.findByRole("alert")).toHaveTextContent("indisponível");
    expect(screen.getByLabelText("Instituição")).toHaveValue("FATEC São Paulo");
  });

  it("trata Currículo Lattes como opcional para níveis de graduação ou tecnólogo", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteFormacaoAcademica = {
      cadastrar: vi.fn().mockResolvedValue(undefined),
    };
    render(<FormularioFormacaoAcademica cliente={cliente} />);

    await preencherFormacao(usuario);
    expect(screen.getByLabelText("Currículo Lattes")).not.toHaveAttribute(
      "required",
    );
    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(cliente.cadastrar).toHaveBeenCalledWith({
      instituicao: "FATEC São Paulo",
      curso: "Análise e Desenvolvimento de Sistemas",
      nivel: "tecnologo",
      dataInicio: "2024-02-01",
      status: "em_andamento",
    });
  });

  it("exige Currículo Lattes ao selecionar mestrado ou doutorado", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteFormacaoAcademica = {
      cadastrar: vi.fn().mockResolvedValue(undefined),
    };
    render(<FormularioFormacaoAcademica cliente={cliente} />);

    await preencherFormacao(usuario);
    await usuario.selectOptions(
      screen.getByLabelText("Nível de formação"),
      "mestrado",
    );

    expect(screen.getByLabelText("Currículo Lattes")).toHaveAttribute(
      "required",
    );

    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(
      await screen.findByText(
        "Informe o link do Currículo Lattes ou marque que não possui.",
      ),
    ).toBeInTheDocument();
    expect(cliente.cadastrar).not.toHaveBeenCalled();

    await usuario.type(
      screen.getByLabelText("Currículo Lattes"),
      "http://lattes.cnpq.br/1234567890123456",
    );

    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(cliente.cadastrar).toHaveBeenCalledWith({
      instituicao: "FATEC São Paulo",
      curso: "Análise e Desenvolvimento de Sistemas",
      nivel: "mestrado",
      dataInicio: "2024-02-01",
      status: "em_andamento",
      curriculoLattes: "http://lattes.cnpq.br/1234567890123456",
    });
  });

  it("permite cadastrar mestrado sem Lattes ao marcar a opção 'Não possuo Currículo Lattes'", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteFormacaoAcademica = {
      cadastrar: vi.fn().mockResolvedValue(undefined),
    };
    render(<FormularioFormacaoAcademica cliente={cliente} />);

    await preencherFormacao(usuario);
    await usuario.selectOptions(
      screen.getByLabelText("Nível de formação"),
      "mestrado",
    );

    const checkboxDispensa = screen.getByLabelText(
      "Não possuo Currículo Lattes",
    );
    expect(checkboxDispensa).toBeInTheDocument();
    expect(checkboxDispensa).not.toBeChecked();

    await usuario.click(checkboxDispensa);
    expect(checkboxDispensa).toBeChecked();

    const campoLattes = screen.getByLabelText("Currículo Lattes");
    expect(campoLattes).toBeDisabled();
    expect(campoLattes).not.toHaveAttribute("required");

    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(cliente.cadastrar).toHaveBeenCalledWith({
      instituicao: "FATEC São Paulo",
      curso: "Análise e Desenvolvimento de Sistemas",
      nivel: "mestrado",
      dataInicio: "2024-02-01",
      status: "em_andamento",
    });
  });

  it("torna o campo Curso opcional ao selecionar Ensino Médio", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteFormacaoAcademica = {
      cadastrar: vi.fn().mockResolvedValue(undefined),
    };
    render(<FormularioFormacaoAcademica cliente={cliente} />);

    await usuario.type(
      screen.getByLabelText("Instituição"),
      "Escola Estadual Prof. Silva",
    );
    await usuario.selectOptions(
      screen.getByLabelText("Nível de formação"),
      "ensino_medio",
    );
    await usuario.type(screen.getByLabelText("Data de início"), "2020-02-01");
    await usuario.selectOptions(
      screen.getByLabelText("Situação"),
      "em_andamento",
    );

    const campoCurso = screen.getByLabelText("Curso");
    expect(campoCurso).not.toHaveAttribute("required");

    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(cliente.cadastrar).toHaveBeenCalledWith({
      instituicao: "Escola Estadual Prof. Silva",
      curso: "Ensino Médio",
      nivel: "ensino_medio",
      dataInicio: "2020-02-01",
      status: "em_andamento",
    });
  });

  it("adiciona uma nova entrada de formação ao clicar no botão", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteFormacaoAcademica = {
      cadastrar: vi.fn(),
    };
    render(<FormularioFormacaoAcademica cliente={cliente} />);

    expect(
      screen.getByRole("group", { name: "Formação acadêmica 1" }),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("group", { name: "Formação acadêmica 2" }),
    ).not.toBeInTheDocument();

    await usuario.click(
      screen.getByRole("button", { name: "+ Adicionar formação acadêmica" }),
    );

    expect(
      screen.getByRole("group", { name: "Formação acadêmica 2" }),
    ).toBeInTheDocument();
  });

  it("remove uma entrada de formação ao clicar no botão de remoção", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteFormacaoAcademica = {
      cadastrar: vi.fn(),
    };
    render(<FormularioFormacaoAcademica cliente={cliente} />);

    await usuario.click(
      screen.getByRole("button", { name: "+ Adicionar formação acadêmica" }),
    );
    expect(
      screen.getByRole("group", { name: "Formação acadêmica 2" }),
    ).toBeInTheDocument();

    await usuario.click(
      screen.getByRole("button", { name: "Remover Formação acadêmica 2" }),
    );

    expect(
      screen.queryByRole("group", { name: "Formação acadêmica 2" }),
    ).not.toBeInTheDocument();
  });

  it("envia todas as formações cadastradas chamando o cliente para cada item", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteFormacaoAcademica = {
      cadastrar: vi.fn().mockResolvedValue(undefined),
    };
    const aoAvancar = vi.fn();
    render(
      <FormularioFormacaoAcademica
        aoAvancar={aoAvancar}
        cliente={cliente}
      />,
    );

    await preencherFormacao(usuario);

    await usuario.click(
      screen.getByRole("button", { name: "+ Adicionar formação acadêmica" }),
    );

    const camposInstituicao = screen.getAllByLabelText("Instituição");
    const camposNivel = screen.getAllByLabelText("Nível de formação");
    const camposCurso = screen.getAllByLabelText("Curso");
    const camposInicio = screen.getAllByLabelText("Data de início");
    const camposStatus = screen.getAllByLabelText("Situação");

    await usuario.type(camposInstituicao[1], "USP");
    await usuario.selectOptions(camposNivel[1], "graduacao");
    await usuario.type(camposCurso[1], "Sistemas de Informação");
    await usuario.type(camposInicio[1], "2018-02-01");
    await usuario.selectOptions(camposStatus[1], "em_andamento");

    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(cliente.cadastrar).toHaveBeenCalledTimes(2);
    expect(aoAvancar).toHaveBeenCalledTimes(1);
  });

  it("exige Lattes quando uma das múltiplas formações é mestrado e repassa aos itens enviados", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteFormacaoAcademica = {
      cadastrar: vi.fn().mockResolvedValue(undefined),
    };
    render(<FormularioFormacaoAcademica cliente={cliente} />);

    // Primeira formação: tecnólogo
    await preencherFormacao(usuario);

    // Adiciona segunda formação: mestrado
    await usuario.click(
      screen.getByRole("button", { name: "+ Adicionar formação acadêmica" }),
    );

    const camposInstituicao = screen.getAllByLabelText("Instituição");
    const camposNivel = screen.getAllByLabelText("Nível de formação");
    const camposCurso = screen.getAllByLabelText("Curso");
    const camposInicio = screen.getAllByLabelText("Data de início");
    const camposStatus = screen.getAllByLabelText("Situação");

    await usuario.type(camposInstituicao[1], "USP");
    await usuario.selectOptions(camposNivel[1], "mestrado");
    await usuario.type(camposCurso[1], "Ciência da Computação");
    await usuario.type(camposInicio[1], "2023-03-01");
    await usuario.selectOptions(camposStatus[1], "em_andamento");

    // Lattes passa a ser obrigatório na etapa
    const campoLattes = screen.getByLabelText("Currículo Lattes");
    expect(campoLattes).toHaveAttribute("required");

    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(
      await screen.findByText(
        "Informe o link do Currículo Lattes ou marque que não possui.",
      ),
    ).toBeInTheDocument();
    expect(cliente.cadastrar).not.toHaveBeenCalled();

    // Preenche o Lattes único
    await usuario.type(campoLattes, "http://lattes.cnpq.br/9876543210987654");

    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(cliente.cadastrar).toHaveBeenCalledTimes(2);
    expect(cliente.cadastrar).toHaveBeenNthCalledWith(
      1,
      expect.objectContaining({
        curso: "Análise e Desenvolvimento de Sistemas",
        curriculoLattes: "http://lattes.cnpq.br/9876543210987654",
      }),
    );
    expect(cliente.cadastrar).toHaveBeenNthCalledWith(
      2,
      expect.objectContaining({
        curso: "Ciência da Computação",
        curriculoLattes: "http://lattes.cnpq.br/9876543210987654",
      }),
    );
  });
});
