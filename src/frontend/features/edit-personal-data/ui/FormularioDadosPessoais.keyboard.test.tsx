import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ClienteDadosPessoais } from "../api/cliente-dados-pessoais";
import { FormularioDadosPessoais } from "./FormularioDadosPessoais";

afterEach(cleanup);

/** Cria um cliente isolado porque a navegação por teclado não deve chamar a API. */
function criarCliente(): ClienteDadosPessoais {
  return { salvar: vi.fn().mockResolvedValue(undefined) };
}

describe("FormularioDadosPessoais — navegação por teclado", () => {
  /**
   * Mantém a continuidade do foco ao incluir um telefone sem usar o mouse.
   *
   * O teste percorre os primeiros controles com Tab, aciona o botão com Enter
   * e confirma que o novo campo recebe foco antes do próximo Tab seguir ao
   * e-mail. Ele existe para proteger a navegação integral do formulário.
   */
  it("foca o telefone adicionado ao acionar o botão por teclado", async () => {
    const usuario = userEvent.setup();
    render(<FormularioDadosPessoais cliente={criarCliente()} />);

    await usuario.tab();
    expect(screen.getByLabelText("Nome Completo")).toHaveFocus();

    await usuario.tab();
    expect(screen.getByLabelText("E-mail")).toHaveFocus();

    await usuario.tab();
    expect(screen.getByLabelText("Telefone 1")).toHaveFocus();

    await usuario.tab();
    expect(
      screen.getByRole("button", { name: "+ Adicionar telefone" }),
    ).toHaveFocus();

    await usuario.keyboard("{Enter}");

    expect(screen.getByLabelText("Telefone 2")).toHaveFocus();

    await usuario.tab();
    expect(
      screen.getByRole("button", { name: "+ Adicionar telefone" }),
    ).toHaveFocus();

    await usuario.tab();
    expect(screen.getByLabelText("Endereço")).toHaveFocus();
  });
});
