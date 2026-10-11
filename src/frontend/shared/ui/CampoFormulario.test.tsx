import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { CampoFormulario } from "./CampoFormulario";

afterEach(cleanup);

describe("CampoFormulario", () => {
  it("associa o rótulo ao input correspondente através de htmlFor e id", () => {
    render(
      <CampoFormulario
        id="campo-nome"
        rotulo="Nome completo"
        valor="Ricardo"
      />,
    );

    const input = screen.getByLabelText("Nome completo");
    expect(input).toBeInTheDocument();
    expect(input).toHaveAttribute("id", "campo-nome");
  });

  it("associa a mensagem de erro ao input via aria-describedby e aria-invalid", () => {
    render(
      <CampoFormulario
        erro="O campo nome é obrigatório."
        id="campo-nome"
        rotulo="Nome completo"
      />,
    );

    const input = screen.getByLabelText("Nome completo");
    expect(input).toHaveAttribute("aria-invalid", "true");
    expect(input).toHaveAttribute("aria-describedby", "campo-nome-erro");

    const mensagemErro = screen.getByText("O campo nome é obrigatório.");
    expect(mensagemErro).toBeInTheDocument();
    expect(mensagemErro).toHaveAttribute("id", "campo-nome-erro");
    expect(mensagemErro).toHaveClass("field__error");
  });

  it("não adiciona aria-describedby nem aria-invalid quando não há erro", () => {
    render(
      <CampoFormulario
        id="campo-email"
        rotulo="E-mail"
        valor="teste@exemplo.com"
      />,
    );

    const input = screen.getByLabelText("E-mail");
    expect(input).not.toHaveAttribute("aria-invalid");
    expect(input).not.toHaveAttribute("aria-describedby");
    expect(screen.queryByRole("paragraph")).not.toBeInTheDocument();
  });

  it("dispara callback onChange com o novo valor digitado", async () => {
    const usuario = userEvent.setup();
    const aoMudar = vi.fn();

    render(
      <CampoFormulario id="campo-cidade" onChange={aoMudar} rotulo="Cidade" />,
    );

    const input = screen.getByLabelText("Cidade");
    await usuario.type(input, "São Paulo");

    expect(aoMudar).toHaveBeenCalled();
  });

  it("aplica atributos tipo, required, disabled e placeholder ao input", () => {
    render(
      <CampoFormulario
        desabilitado
        id="campo-senha"
        obrigatorio
        placeholder="Digite sua senha"
        rotulo="Senha"
        tipo="password"
      />,
    );

    const input = screen.getByLabelText("Senha");
    expect(input).toHaveAttribute("type", "password");
    expect(input).toBeRequired();
    expect(input).toBeDisabled();
    expect(input).toHaveAttribute("placeholder", "Digite sua senha");
  });

  it("renderiza texto de ajuda e o associa via aria-describedby", () => {
    render(
      <CampoFormulario
        ajuda="Informe seu e-mail principal para contato."
        id="campo-email-ajuda"
        rotulo="E-mail"
      />,
    );

    const input = screen.getByLabelText(/E-mail/);
    expect(input).toHaveAttribute(
      "aria-describedby",
      "campo-email-ajuda-ajuda",
    );
    expect(
      screen.getByText("Informe seu e-mail principal para contato."),
    ).toBeInTheDocument();
  });

  it("permite renderização de elemento filho customizado via children", () => {
    render(
      <CampoFormulario id="campo-nivel" rotulo="Nível de proficiência">
        <select id="campo-nivel">
          <option value="basico">Básico</option>
          <option value="avancado">Avançado</option>
        </select>
      </CampoFormulario>,
    );

    const select = screen.getByLabelText("Nível de proficiência");
    expect(select).toBeInTheDocument();
    expect(select.tagName).toBe("SELECT");
  });
});
