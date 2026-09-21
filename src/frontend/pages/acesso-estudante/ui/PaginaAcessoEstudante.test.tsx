// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import type { ClienteAcessoEstudante } from "../../../features/acesso-estudante";
import { PaginaAcessoEstudante } from "./PaginaAcessoEstudante";

describe("PaginaAcessoEstudante", () => {
  it("preenche o acesso com o e-mail após cadastro bem-sucedido do double", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteAcessoEstudante = {
      cadastrar: vi.fn().mockResolvedValue({
        id: "1",
        nome: "Ana Estudante",
        email: "ana@fatec.sp.gov.br"
      }),
      acessar: vi.fn()
    };

    render(<PaginaAcessoEstudante cliente={cliente} />);

    await usuario.click(screen.getByRole("tab", { name: "Criar conta" }));
    await usuario.type(screen.getByLabelText("Nome"), "Ana Estudante");
    await usuario.type(screen.getByLabelText("E-mail"), "ana@fatec.sp.gov.br");
    await usuario.type(screen.getByLabelText("Senha"), "segredo123");
    await usuario.type(screen.getByLabelText("Confirme a senha"), "segredo123");
    await usuario.click(screen.getByRole("button", { name: "Criar conta" }));

    expect(await screen.findByRole("tab", { name: "Entrar", selected: true })).toBeInTheDocument();
    expect(screen.getByLabelText("E-mail")).toHaveValue("ana@fatec.sp.gov.br");
    expect(screen.getByLabelText("Senha")).toHaveValue("");
  });
});
