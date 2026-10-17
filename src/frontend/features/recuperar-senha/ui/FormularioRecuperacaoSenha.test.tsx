import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaRecuperacaoSenha,
  type ClienteRecuperacaoSenha,
} from "../api/cliente-recuperacao-senha";
import { FormularioRecuperacaoSenha } from "./FormularioRecuperacaoSenha";

afterEach(cleanup);

describe("FormularioRecuperacaoSenha", () => {
  it("associa o erro ao campo quando o e-mail é inválido", async () => {
    const usuario = userEvent.setup();
    render(<FormularioRecuperacaoSenha cliente={{ solicitar: vi.fn() }} />);

    await usuario.click(
      screen.getByRole("button", { name: "Enviar instruções" }),
    );

    expect(
      await screen.findByText("Informe um e-mail válido."),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("E-mail")).toHaveAttribute(
      "aria-invalid",
      "true",
    );
  });

  it("solicita o e-mail normalizado e evita confirmar se existe conta", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteRecuperacaoSenha = {
      solicitar: vi.fn().mockResolvedValue(undefined),
    };
    render(<FormularioRecuperacaoSenha cliente={cliente} />);

    await usuario.type(
      screen.getByLabelText("E-mail"),
      "  ana@fatec.sp.gov.br ",
    );
    await usuario.click(
      screen.getByRole("button", { name: "Enviar instruções" }),
    );

    expect(cliente.solicitar).toHaveBeenCalledWith({
      email: "ana@fatec.sp.gov.br",
    });
    expect(await screen.findByRole("status")).toHaveTextContent(
      "Se houver uma conta",
    );
  });

  it("preserva o e-mail e apresenta falha recuperável", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteRecuperacaoSenha = {
      solicitar: vi
        .fn()
        .mockRejectedValue(new FalhaRecuperacaoSenha("indisponivel")),
    };
    render(<FormularioRecuperacaoSenha cliente={cliente} />);

    await usuario.type(screen.getByLabelText("E-mail"), "ana@fatec.sp.gov.br");
    await usuario.click(
      screen.getByRole("button", { name: "Enviar instruções" }),
    );

    expect(await screen.findByRole("alert")).toHaveTextContent("indisponível");
    expect(screen.getByLabelText("E-mail")).toHaveValue("ana@fatec.sp.gov.br");
  });
});
