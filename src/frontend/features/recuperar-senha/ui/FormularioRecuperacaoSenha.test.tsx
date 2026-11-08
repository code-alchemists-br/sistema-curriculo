import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaRecuperacaoSenha,
  type ClienteRecuperacaoSenha,
} from "../api/cliente-recuperacao-senha";
import { FormularioRecuperacaoSenha } from "./FormularioRecuperacaoSenha";

afterEach(cleanup);

function criarClienteSucesso(): ClienteRecuperacaoSenha {
  return {
    solicitar: vi.fn().mockResolvedValue(undefined),
  };
}

describe("FormularioRecuperacaoSenha", () => {
  it("renderiza o campo de e-mail e o botão de envio", () => {
    const cliente = criarClienteSucesso();
    render(<FormularioRecuperacaoSenha cliente={cliente} />);

    expect(screen.getByLabelText("E-mail")).toHaveValue("");
    expect(
      screen.getByRole("button", { name: "Enviar instruções" }),
    ).toBeInTheDocument();
  });

  it("exibe erro ao tentar submeter com e-mail vazio", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteSucesso();
    render(<FormularioRecuperacaoSenha cliente={cliente} />);

    await usuario.click(
      screen.getByRole("button", { name: "Enviar instruções" }),
    );

    expect(screen.getByText("Informe seu e-mail.")).toBeInTheDocument();
    expect(cliente.solicitar).not.toHaveBeenCalled();
  });

  it("exibe erro com formato de e-mail inválido", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteSucesso();
    render(<FormularioRecuperacaoSenha cliente={cliente} />);

    await usuario.type(screen.getByLabelText("E-mail"), "invalido@");
    await usuario.click(
      screen.getByRole("button", { name: "Enviar instruções" }),
    );

    expect(screen.getByText("Informe um e-mail válido.")).toBeInTheDocument();
    expect(cliente.solicitar).not.toHaveBeenCalled();
  });

  it("envia e exibe mensagem de sucesso com e-mail válido", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteSucesso();
    const aoConcluir = vi.fn();

    render(
      <FormularioRecuperacaoSenha
        aoConcluirSolicitacao={aoConcluir}
        cliente={cliente}
      />,
    );

    await usuario.type(
      screen.getByLabelText("E-mail"),
      "aluno@fatec.sp.gov.br",
    );
    await usuario.click(
      screen.getByRole("button", { name: "Enviar instruções" }),
    );

    expect(cliente.solicitar).toHaveBeenCalledWith({
      email: "aluno@fatec.sp.gov.br",
    });
    expect(
      await screen.findByText(/Se houver uma conta associada a este e-mail/i),
    ).toBeInTheDocument();
    expect(aoConcluir).toHaveBeenCalledWith("aluno@fatec.sp.gov.br");
  });

  it("trata erro do cliente e exibe feedback amigável", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteRecuperacaoSenha = {
      solicitar: vi
        .fn()
        .mockRejectedValue(new FalhaRecuperacaoSenha("indisponivel")),
    };

    render(<FormularioRecuperacaoSenha cliente={cliente} />);

    await usuario.type(
      screen.getByLabelText("E-mail"),
      "aluno@fatec.sp.gov.br",
    );
    await usuario.click(
      screen.getByRole("button", { name: "Enviar instruções" }),
    );

    expect(
      await screen.findByText(
        "A recuperação de senha está indisponível no momento. Tente novamente mais tarde.",
      ),
    ).toBeInTheDocument();
  });
});
