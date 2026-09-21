// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { FalhaAcessoEstudante, type ClienteAcessoEstudante } from "../api/cliente-acesso-estudante";
import { FormularioAcesso } from "./FormularioAcesso";

afterEach(cleanup);

describe("FormularioAcesso", () => {
  it("mantém os dados ao receber a indisponibilidade fornecida pelo double", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteAcessoEstudante = {
      cadastrar: vi.fn(),
      acessar: vi.fn().mockRejectedValue(new FalhaAcessoEstudante("indisponivel"))
    };

    render(<FormularioAcesso cliente={cliente} emailInicial="aluna@fatec.sp.gov.br" />);

    await usuario.type(screen.getByLabelText("Senha"), "segredo123");
    await usuario.click(screen.getByRole("button", { name: "Entrar" }));

    expect(await screen.findByRole("status")).toHaveTextContent("indisponível");
    expect(screen.getByLabelText("E-mail")).toHaveValue("aluna@fatec.sp.gov.br");
    expect(screen.getByLabelText("Senha")).toHaveValue("segredo123");
  });

  it("limpa a senha e não afirma que uma sessão foi criada após 204 simulado", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteAcessoEstudante = {
      cadastrar: vi.fn(),
      acessar: vi.fn().mockResolvedValue(undefined)
    };

    render(<FormularioAcesso cliente={cliente} emailInicial="aluna@fatec.sp.gov.br" />);

    await usuario.type(screen.getByLabelText("Senha"), "segredo123");
    await usuario.click(screen.getByRole("button", { name: "Entrar" }));

    expect(await screen.findByRole("status")).toHaveTextContent("Uma sessão ainda não foi criada.");
    expect(screen.getByLabelText("Senha")).toHaveValue("");
  });
});
