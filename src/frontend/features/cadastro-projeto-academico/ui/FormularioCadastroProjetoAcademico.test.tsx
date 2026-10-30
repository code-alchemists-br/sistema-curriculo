// Proveniência: decision-analysis prompts/frontend/20260921-120136-tela-cadastro-projetos-academicos-v001.md#v001
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaCadastroProjeto,
  type ClienteProjetosAcademicos,
} from "../api/cliente-projetos-academicos";
import { FormularioCadastroProjetoAcademico } from "./FormularioCadastroProjetoAcademico";

afterEach(cleanup);

describe("FormularioCadastroProjetoAcademico", () => {
  it("preserva dados quando o double informa indisponibilidade", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteProjetosAcademicos = {
      cadastrar: vi
        .fn()
        .mockRejectedValue(new FalhaCadastroProjeto("indisponivel")),
    };

    render(<FormularioCadastroProjetoAcademico cliente={cliente} />);

    await usuario.type(
      screen.getByLabelText("Título do projeto"),
      "Sistema Currículo",
    );
    await usuario.type(
      screen.getByLabelText("Descrição"),
      "Aplicação para organizar currículos.",
    );
    await usuario.type(
      screen.getByLabelText("Tecnologias utilizadas"),
      "React e TypeScript",
    );
    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar projeto" }),
    );

    expect(await screen.findByRole("alert")).toHaveTextContent("indisponível");
    expect(screen.getByLabelText("Título do projeto")).toHaveValue(
      "Sistema Currículo",
    );
    expect(screen.getByLabelText("Tecnologias utilizadas")).toHaveValue(
      "React e TypeScript",
    );
  });

  it("limpa os campos após sucesso retornado pelo double", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteProjetosAcademicos = {
      cadastrar: vi.fn().mockResolvedValue(undefined),
    };

    render(<FormularioCadastroProjetoAcademico cliente={cliente} />);

    await usuario.type(
      screen.getByLabelText("Título do projeto"),
      "Sistema Currículo",
    );
    await usuario.type(
      screen.getByLabelText("Descrição"),
      "Aplicação para organizar currículos.",
    );
    await usuario.type(
      screen.getByLabelText("Tecnologias utilizadas"),
      "React e TypeScript",
    );
    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar projeto" }),
    );

    expect(await screen.findByRole("status")).toHaveTextContent(
      "enviados para processamento",
    );
    expect(screen.getByLabelText("Título do projeto")).toHaveValue("");
    expect(screen.getByLabelText("Descrição")).toHaveValue("");
    expect(screen.getByLabelText("Tecnologias utilizadas")).toHaveValue("");
  });

  it("exibe erro acessível e não cadastra ao deixar tecnologias em branco", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteProjetosAcademicos = {
      cadastrar: vi.fn(),
    };

    render(<FormularioCadastroProjetoAcademico cliente={cliente} />);

    await usuario.type(
      screen.getByLabelText("Título do projeto"),
      "Sistema Currículo",
    );
    await usuario.type(
      screen.getByLabelText("Descrição"),
      "Aplicação para organizar currículos.",
    );
    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar projeto" }),
    );

    const inputTecnologias = screen.getByLabelText("Tecnologias utilizadas");
    expect(inputTecnologias).toHaveAttribute("aria-invalid", "true");
    expect(
      await screen.findByText("Informe as tecnologias utilizadas no projeto."),
    ).toBeInTheDocument();
    expect(cliente.cadastrar).not.toHaveBeenCalled();
  });

  it("exibe mensagem de vazio ao clicar em 'Não possuo projetos acadêmicos' e permite restaurar os campos", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteProjetosAcademicos = {
      cadastrar: vi.fn(),
    };

    render(<FormularioCadastroProjetoAcademico cliente={cliente} />);

    await usuario.click(
      screen.getByRole("button", { name: "Não possuo projetos acadêmicos" }),
    );

    expect(
      screen.getByText("Nenhum projeto acadêmico cadastrado."),
    ).toBeInTheDocument();
    expect(
      screen.queryByLabelText("Título do projeto"),
    ).not.toBeInTheDocument();

    await usuario.click(
      screen.getByRole("button", { name: "+ Adicionar projeto acadêmico" }),
    );

    expect(screen.getByLabelText("Título do projeto")).toBeInTheDocument();
  });

  it("chama aoAvancar ao clicar em Próximo com estado sem projetos ativo", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteProjetosAcademicos = {
      cadastrar: vi.fn(),
    };
    const aoAvancar = vi.fn();

    render(
      <FormularioCadastroProjetoAcademico
        aoAvancar={aoAvancar}
        cliente={cliente}
      />,
    );

    await usuario.click(
      screen.getByRole("button", { name: "Não possuo projetos acadêmicos" }),
    );
    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar projeto" }),
    );

    expect(aoAvancar).toHaveBeenCalledTimes(1);
  });

  it("adiciona uma nova entrada de projeto ao clicar no botão", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteProjetosAcademicos = {
      cadastrar: vi.fn(),
    };

    render(<FormularioCadastroProjetoAcademico cliente={cliente} />);

    expect(
      screen.getByRole("group", { name: "Projeto acadêmico 1" }),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("group", { name: "Projeto acadêmico 2" }),
    ).not.toBeInTheDocument();

    await usuario.click(
      screen.getByRole("button", { name: "+ Adicionar projeto acadêmico" }),
    );

    expect(
      screen.getByRole("group", { name: "Projeto acadêmico 2" }),
    ).toBeInTheDocument();
  });

  it("remove uma entrada de projeto ao clicar no botão de remoção", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteProjetosAcademicos = {
      cadastrar: vi.fn(),
    };

    render(<FormularioCadastroProjetoAcademico cliente={cliente} />);

    await usuario.click(
      screen.getByRole("button", { name: "+ Adicionar projeto acadêmico" }),
    );
    expect(
      screen.getByRole("group", { name: "Projeto acadêmico 2" }),
    ).toBeInTheDocument();

    await usuario.click(
      screen.getByRole("button", { name: "Remover Projeto acadêmico 2" }),
    );

    expect(
      screen.queryByRole("group", { name: "Projeto acadêmico 2" }),
    ).not.toBeInTheDocument();
  });

  it("envia múltiplos projetos chamando o cliente para cada item", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteProjetosAcademicos = {
      cadastrar: vi.fn().mockResolvedValue(undefined),
    };
    const aoAvancar = vi.fn();

    render(
      <FormularioCadastroProjetoAcademico
        aoAvancar={aoAvancar}
        cliente={cliente}
      />,
    );

    await usuario.type(
      screen.getByLabelText("Título do projeto"),
      "Sistema de Biblioteca",
    );
    await usuario.type(
      screen.getByLabelText("Descrição"),
      "Controle de empréstimos acadêmicos.",
    );
    await usuario.type(
      screen.getByLabelText("Tecnologias utilizadas"),
      "Java e Spring",
    );

    await usuario.click(
      screen.getByRole("button", { name: "+ Adicionar projeto acadêmico" }),
    );

    const camposTitulo = screen.getAllByLabelText("Título do projeto");
    const camposDescricao = screen.getAllByLabelText("Descrição");
    const camposTecnologias = screen.getAllByLabelText(
      "Tecnologias utilizadas",
    );

    await usuario.type(camposTitulo[1], "App de Gestão");
    await usuario.type(camposDescricao[1], "App móvel de estágio.");
    await usuario.type(camposTecnologias[1], "React Native");

    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar projeto" }),
    );

    expect(cliente.cadastrar).toHaveBeenCalledTimes(2);
    expect(aoAvancar).toHaveBeenCalledTimes(1);
  });
});
