import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaDadosPessoais,
  type ClienteDadosPessoais,
} from "../api/cliente-dados-pessoais";
import { FormularioDadosPessoais } from "./FormularioDadosPessoais";

afterEach(cleanup);

async function preencherCamposObrigatorios(
  usuario: ReturnType<typeof userEvent.setup>,
): Promise<void> {
  await usuario.type(screen.getByLabelText("Nome completo"), "Ana Silva");
  await usuario.type(
    screen.getByLabelText("Endereço completo"),
    "Rua das Flores, 10",
  );
  await usuario.type(screen.getByLabelText("Telefone 1"), "(11) 99999-0000");
  await usuario.type(screen.getByLabelText("E-mail"), "ana@exemplo.com");
}

describe("FormularioDadosPessoais", () => {
  it("informa o envio em andamento e evita um segundo envio", async () => {
    const usuario = userEvent.setup();
    let concluirSalvamento: (() => void) | undefined;
    const cliente: ClienteDadosPessoais = {
      salvar: vi.fn(
        () =>
          new Promise<void>((resolve) => {
            concluirSalvamento = resolve;
          }),
      ),
    };

    const { container } = render(<FormularioDadosPessoais cliente={cliente} />);
    await preencherCamposObrigatorios(usuario);
    await usuario.click(
      screen.getByRole("button", { name: "Salvar dados pessoais" }),
    );

    expect(screen.getByRole("status")).toHaveTextContent(
      "Salvando dados pessoais",
    );
    expect(
      screen.getByRole("button", { name: "Salvando dados..." }),
    ).toBeDisabled();
    expect(container.querySelector("form")).toHaveAttribute(
      "aria-busy",
      "true",
    );

    concluirSalvamento?.();

    expect(
      await screen.findByText("Dados pessoais salvos com sucesso."),
    ).toBeInTheDocument();
  });

  it("preserva os dados, informa a falha e permite tentar novamente", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteDadosPessoais = {
      salvar: vi
        .fn()
        .mockRejectedValueOnce(new FalhaDadosPessoais("indisponivel"))
        .mockResolvedValueOnce(undefined),
    };

    render(<FormularioDadosPessoais cliente={cliente} />);
    await preencherCamposObrigatorios(usuario);
    await usuario.click(
      screen.getByRole("button", { name: "Salvar dados pessoais" }),
    );

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Não foi possível salvar",
    );
    expect(screen.getByLabelText("Nome completo")).toHaveValue("Ana Silva");
    expect(
      screen.getByRole("button", { name: "Salvar dados pessoais" }),
    ).toBeEnabled();

    await usuario.click(
      screen.getByRole("button", { name: "Salvar dados pessoais" }),
    );

    expect(await screen.findByRole("status")).toHaveTextContent(
      "salvos com sucesso",
    );
    expect(cliente.salvar).toHaveBeenCalledTimes(2);
  });
});
