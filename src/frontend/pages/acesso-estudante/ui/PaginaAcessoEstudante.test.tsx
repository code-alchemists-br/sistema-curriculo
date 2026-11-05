// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ClienteAcessoEstudante } from "../../../features/acesso-estudante";
import { PaginaAcessoEstudante } from "./PaginaAcessoEstudante";

afterEach(cleanup);

describe("PaginaAcessoEstudante", () => {
  it("preenche o acesso com o e-mail após cadastro bem-sucedido do double", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteAcessoEstudante = {
      cadastrar: vi.fn().mockResolvedValue({
        id: "1",
        nome: "Ana Estudante",
        email: "ana@fatec.sp.gov.br",
      }),
      acessar: vi.fn(),
    };

    render(<PaginaAcessoEstudante cliente={cliente} />);

    await usuario.click(screen.getByRole("button", { name: "Criar conta" }));
    await usuario.type(screen.getByLabelText("Nome"), "Ana Estudante");
    await usuario.type(screen.getByLabelText("E-mail"), "ana@fatec.sp.gov.br");
    await usuario.type(screen.getByLabelText("Senha"), "segredo123");
    await usuario.type(screen.getByLabelText("Confirme a senha"), "segredo123");
    await usuario.click(screen.getByRole("button", { name: "Criar conta" }));

    expect(
      await screen.findByRole("heading", { name: "Conecte-se na LIMINAL" }),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Entrar" })).toBeInTheDocument();
    expect(screen.getByLabelText("E-mail")).toHaveValue("ana@fatec.sp.gov.br");
    expect(screen.getByLabelText("Senha")).toHaveValue("");
  });

  it("preserva o e-mail digitado ao alternar entre as abas de cadastro e login", async () => {
    const usuario = userEvent.setup();
    render(<PaginaAcessoEstudante abaInicial="cadastro" />);

    await usuario.type(
      screen.getByLabelText("E-mail"),
      "estudante@fatec.sp.gov.br",
    );
    await usuario.click(screen.getByRole("button", { name: "Entrar" }));

    expect(
      screen.getByRole("heading", { name: "Conecte-se na LIMINAL" }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("E-mail")).toHaveValue(
      "estudante@fatec.sp.gov.br",
    );

    await usuario.click(screen.getByRole("button", { name: "Criar conta" }));
    expect(
      screen.getByRole("heading", { name: "Crie uma nova conta" }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("E-mail")).toHaveValue(
      "estudante@fatec.sp.gov.br",
    );
  });
});
