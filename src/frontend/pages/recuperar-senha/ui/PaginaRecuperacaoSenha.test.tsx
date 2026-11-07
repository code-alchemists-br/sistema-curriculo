import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ClienteRecuperacaoSenha } from "../../../features/recuperar-senha";
import { PaginaRecuperacaoSenha } from "./PaginaRecuperacaoSenha";

afterEach(cleanup);

describe("PaginaRecuperacaoSenha", () => {
  it("renderiza os elementos visuais principais e o formulário", () => {
    render(<PaginaRecuperacaoSenha />);

    expect(screen.getByText("LIMINAL")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Recupere sua senha" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        /Informe seu e-mail cadastrado para enviarmos as instruções/i,
      ),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("E-mail")).toBeInTheDocument();
  });

  it("permite acionar o retorno ao login pelo botão de voltar e pelo rodapé", async () => {
    const usuario = userEvent.setup();
    const onVoltarLogin = vi.fn();

    render(<PaginaRecuperacaoSenha onVoltarLogin={onVoltarLogin} />);

    await usuario.click(
      screen.getByRole("button", { name: "← Voltar para o login" }),
    );
    expect(onVoltarLogin).toHaveBeenCalledTimes(1);

    await usuario.click(screen.getByRole("button", { name: "Entrar" }));
    expect(onVoltarLogin).toHaveBeenCalledTimes(2);
  });

  it("permite submeter solicitação com sucesso na página", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteRecuperacaoSenha = {
      solicitar: vi.fn().mockResolvedValue(undefined),
    };
    const onSucesso = vi.fn();

    render(
      <PaginaRecuperacaoSenha
        cliente={cliente}
        onSucessoSolicitacao={onSucesso}
      />,
    );

    await usuario.type(
      screen.getByLabelText("E-mail"),
      "estudante@fatec.sp.gov.br",
    );
    await usuario.click(
      screen.getByRole("button", { name: "Enviar instruções" }),
    );

    expect(cliente.solicitar).toHaveBeenCalledWith({
      email: "estudante@fatec.sp.gov.br",
    });
    expect(onSucesso).toHaveBeenCalledWith("estudante@fatec.sp.gov.br");
  });
});
