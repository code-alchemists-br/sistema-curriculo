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
    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar projeto" }),
    );

    expect(await screen.findByRole("status")).toHaveTextContent(
      "enviados para processamento",
    );
    expect(screen.getByLabelText("Título do projeto")).toHaveValue("");
    expect(screen.getByLabelText("Descrição")).toHaveValue("");
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
    await usuario.click(screen.getByRole("button", { name: "Cadastrar projeto" }));

    expect(aoAvancar).toHaveBeenCalledTimes(1);
  });
});
