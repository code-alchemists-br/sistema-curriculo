import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaPerfilEstudante,
  type ClientePerfilEstudante,
} from "../api/cliente-perfil-estudante";
import { FormularioEdicaoPerfil } from "./FormularioEdicaoPerfil";

afterEach(cleanup);

const studentExistente = {
  nomeCompleto: "Ricardo Galdino",
  enderecoCompleto: "Av. Paulista, 1000",
  telefones: ["(11) 99999-0000"],
  email: "ricardo@exemplo.com",
};

function criarClienteDeSucesso(): ClientePerfilEstudante {
  return {
    atualizar: vi.fn().mockResolvedValue(undefined),
    excluir: vi.fn().mockResolvedValue(undefined),
  };
}

function criarClienteComFalha(): ClientePerfilEstudante {
  return {
    atualizar: vi
      .fn()
      .mockRejectedValue(new FalhaPerfilEstudante("indisponivel")),
    excluir: vi
      .fn()
      .mockRejectedValue(new FalhaPerfilEstudante("indisponivel")),
  };
}

describe("FormularioEdicaoPerfil", () => {
  it("exibe os dados iniciais do estudante nos campos do formulário", () => {
    render(
      <FormularioEdicaoPerfil
        cliente={criarClienteDeSucesso()}
        valoresIniciais={studentExistente}
      />,
    );

    expect(screen.getByLabelText("Nome completo")).toHaveValue(
      "Ricardo Galdino",
    );
    expect(screen.getByLabelText("E-mail")).toHaveValue("ricardo@exemplo.com");
    expect(screen.getByLabelText("Telefone 1")).toHaveValue("(11) 99999-0000");
  });

  it("salva alterações e exibe mensagem de sucesso com o double", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteDeSucesso();

    render(
      <FormularioEdicaoPerfil
        cliente={cliente}
        valoresIniciais={studentExistente}
      />,
    );

    await usuario.clear(screen.getByLabelText("Nome completo"));
    await usuario.type(screen.getByLabelText("Nome completo"), "Ricardo Silva");
    await usuario.type(
      screen.getByLabelText(/linkedin/i),
      "https://portfolio.exemplo.dev/ricardo",
    );
    await usuario.click(
      screen.getByRole("button", { name: "Salvar alterações" }),
    );

    expect(await screen.findByRole("status")).toHaveTextContent(
      "Perfil atualizado com sucesso.",
    );
    expect(cliente.atualizar).toHaveBeenCalledTimes(1);
    expect(cliente.atualizar).toHaveBeenCalledWith({
      ...studentExistente,
      nomeCompleto: "Ricardo Silva",
      linkedIn: "https://portfolio.exemplo.dev/ricardo",
    });
  });

  it("bloqueia o envio e associa o erro quando o link profissional é inválido", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteDeSucesso();

    render(
      <FormularioEdicaoPerfil
        cliente={cliente}
        valoresIniciais={studentExistente}
      />,
    );

    const campoLinkedIn = screen.getByLabelText(/linkedin/i);
    await usuario.type(campoLinkedIn, "portfolio.exemplo.dev/ricardo");
    await usuario.click(
      screen.getByRole("button", { name: "Salvar alterações" }),
    );

    expect(
      await screen.findByText("Informe uma URL absoluta válida."),
    ).toHaveAttribute("id", "perfil-linkedin-erro");
    expect(campoLinkedIn).toHaveAttribute(
      "aria-describedby",
      "perfil-linkedin-erro",
    );
    expect(campoLinkedIn).toHaveAttribute("aria-invalid", "true");
    expect(campoLinkedIn).toHaveValue("portfolio.exemplo.dev/ricardo");
    expect(cliente.atualizar).not.toHaveBeenCalled();
  });

  it("impede submissões duplicadas enquanto o salvamento está pendente", async () => {
    const usuario = userEvent.setup();
    let concluirSalvamento: (() => void) | undefined;
    const cliente: ClientePerfilEstudante = {
      atualizar: vi.fn(
        () =>
          new Promise<void>((resolve) => {
            concluirSalvamento = resolve;
          }),
      ),
      excluir: vi.fn().mockResolvedValue(undefined),
    };

    render(
      <FormularioEdicaoPerfil
        cliente={cliente}
        valoresIniciais={studentExistente}
      />,
    );

    const botaoSalvar = screen.getByRole("button", {
      name: "Salvar alterações",
    });
    await usuario.click(botaoSalvar);
    await usuario.click(botaoSalvar);

    expect(cliente.atualizar).toHaveBeenCalledTimes(1);
    expect(botaoSalvar).toBeDisabled();

    concluirSalvamento?.();

    expect(await screen.findByRole("status")).toHaveTextContent(
      "Perfil atualizado com sucesso.",
    );
  });

  it("preserva os dados e exibe erro quando o double de atualização falha", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteComFalha();

    render(
      <FormularioEdicaoPerfil
        cliente={cliente}
        valoresIniciais={studentExistente}
      />,
    );

    await usuario.click(
      screen.getByRole("button", { name: "Salvar alterações" }),
    );

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Não foi possível completar a operação no momento.",
    );
    expect(screen.getByLabelText("Nome completo")).toHaveValue(
      "Ricardo Galdino",
    );
  });

  it("permite adicionar, formatar e remover um telefone adicional antes de salvar", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteDeSucesso();

    render(
      <FormularioEdicaoPerfil
        cliente={cliente}
        valoresIniciais={studentExistente}
      />,
    );

    await usuario.click(
      screen.getByRole("button", { name: "+ Adicionar telefone" }),
    );

    const segundoTelefone = screen.getByLabelText("Telefone 2");
    await usuario.type(segundoTelefone, "11988887777");
    expect(segundoTelefone).toHaveValue("(11) 98888-7777");

    await usuario.click(
      screen.getByRole("button", { name: "Remover Telefone 2" }),
    );

    expect(screen.queryByLabelText("Telefone 2")).not.toBeInTheDocument();
  });
});
