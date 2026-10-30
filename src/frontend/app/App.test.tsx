import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it } from "vitest";

import { App } from "./App";

afterEach(cleanup);

describe("App", () => {
  it("apresenta a porta de entrada com a seção hero e permite acessar a conta", async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(
      screen.getByRole("heading", { name: "O currículo que abre portas" }),
    ).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Fazer login" }));

    expect(
      screen.getByRole("heading", { name: "Acesse sua conta" }),
    ).toBeInTheDocument();
  });

  it("permite preencher dados pessoais, avançar para a próxima etapa, voltar e verificar que os dados continuam preenchidos", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(
      screen.getByRole("button", { name: "CRIAR CURRÍCULO →" }),
    );

    expect(
      screen.getByRole("heading", { name: "Conte um pouco sobre você" }),
    ).toBeInTheDocument();

    await user.type(screen.getByLabelText("Nome Completo"), "Ricardo Santos");
    await user.type(screen.getByLabelText("Endereço"), "Rua das Acácias, 123");
    await user.type(screen.getByLabelText("Telefone 1"), "(11) 98765-4321");
    await user.type(screen.getByLabelText("E-mail"), "ricardo@fatec.sp.gov.br");

    await user.click(
      screen.getByRole("button", { name: "Salvar dados pessoais" }),
    );

    expect(
      await screen.findByRole("heading", { name: "Formação acadêmica" }),
    ).toBeInTheDocument();

    // Clica no botão Voltar para retornar à etapa 1 (Dados Pessoais)
    await user.click(
      screen.getByRole("button", { name: "Voltar para a etapa anterior" }),
    );

    expect(
      screen.getByRole("heading", { name: "Conte um pouco sobre você" }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Nome Completo")).toHaveValue("Ricardo Santos");
    expect(screen.getByLabelText("Endereço")).toHaveValue("Rua das Acácias, 123");
    expect(screen.getByLabelText("Telefone 1")).toHaveValue("(11) 98765-4321");
    expect(screen.getByLabelText("E-mail")).toHaveValue("ricardo@fatec.sp.gov.br");

    // Avança novamente para a etapa 2
    await user.click(
      screen.getByRole("button", { name: "Salvar dados pessoais" }),
    );

    expect(
      await screen.findByRole("heading", { name: "Formação acadêmica" }),
    ).toBeInTheDocument();
  });
});
