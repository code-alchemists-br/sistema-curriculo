import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaDadosPessoais,
  type ClienteDadosPessoais
} from "../api/cliente-dados-pessoais";
import { FormularioDadosPessoais } from "./FormularioDadosPessoais";

afterEach(cleanup);

async function preencherCamposObrigatorios(usuario: ReturnType<typeof userEvent.setup>): Promise<void> {
  await usuario.type(screen.getByLabelText("Nome completo"), "Ana Silva");
  await usuario.type(screen.getByLabelText("Endereço completo"), "Rua das Flores, 10");
  await usuario.type(screen.getByLabelText("Telefone 1"), "(11) 99999-0000");
  await usuario.type(screen.getByLabelText("E-mail"), "ana@exemplo.com");
}

describe("FormularioDadosPessoais", () => {
  it("adiciona telefones e envia todos os valores ao double de sucesso", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteDadosPessoais = { salvar: vi.fn().mockResolvedValue(undefined) };

    render(<FormularioDadosPessoais cliente={cliente} />);

    await preencherCamposObrigatorios(usuario);
    await usuario.click(screen.getByRole("button", { name: "+ Adicionar telefone" }));
    await usuario.type(screen.getByLabelText("Telefone 2"), "(11) 98888-0000");
    await usuario.click(screen.getByRole("button", { name: "Salvar dados pessoais" }));

    expect(await screen.findByRole("status")).toHaveTextContent("salvos com sucesso");
    expect(cliente.salvar).toHaveBeenCalledWith({
      nomeCompleto: "Ana Silva",
      enderecoCompleto: "Rua das Flores, 10",
      telefones: ["(11) 99999-0000", "(11) 98888-0000"],
      email: "ana@exemplo.com"
    });
  });

  it("preserva os dados quando o double informa indisponibilidade", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteDadosPessoais = {
      salvar: vi.fn().mockRejectedValue(new FalhaDadosPessoais("indisponivel"))
    };

    render(<FormularioDadosPessoais cliente={cliente} />);

    await preencherCamposObrigatorios(usuario);
    await usuario.click(screen.getByRole("button", { name: "Salvar dados pessoais" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Não foi possível salvar");
    expect(screen.getByLabelText("Nome completo")).toHaveValue("Ana Silva");
    expect(screen.getByLabelText("Telefone 1")).toHaveValue("(11) 99999-0000");
  });
});
