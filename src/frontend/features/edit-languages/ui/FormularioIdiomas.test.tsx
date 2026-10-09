import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { FormularioIdiomas } from "./FormularioIdiomas";

afterEach(cleanup);

describe("FormularioIdiomas", () => {
  it("renderiza um idioma vazio por padrão", () => {
    render(<FormularioIdiomas />);

    expect(screen.getByLabelText("Idioma")).toHaveValue("");
    expect(screen.getByLabelText("Nível de proficiência")).toHaveValue("");
  });

  it("adiciona uma nova entrada de idioma ao clicar no botão", async () => {
    const usuario = userEvent.setup();
    render(<FormularioIdiomas />);

    await usuario.click(screen.getByText("+ Adicionar idioma"));

    const campos = screen.getAllByLabelText("Idioma");
    expect(campos).toHaveLength(2);
  });

  it("remove uma entrada de idioma ao clicar no botão de remoção", async () => {
    const usuario = userEvent.setup();
    render(
      <FormularioIdiomas
        idiomasIniciais={[
          { nome: "Inglês", nivel: "avancado" },
          { nome: "Espanhol", nivel: "basico" },
        ]}
      />,
    );

    await usuario.click(screen.getByLabelText("Remover idioma 1"));

    const campos = screen.getAllByLabelText("Idioma");
    expect(campos).toHaveLength(1);
    expect(campos[0]).toHaveValue("Espanhol");
  });

  it("exibe erros de validação quando campos obrigatórios estão vazios", async () => {
    const usuario = userEvent.setup();
    render(<FormularioIdiomas />);

    await usuario.click(screen.getByText("Salvar idiomas"));

    expect(screen.getByText("Informe o idioma.")).toBeInTheDocument();
    expect(
      screen.getByText("Selecione o nível de proficiência."),
    ).toBeInTheDocument();
  });

  it("chama onSalvar com idiomas quando válidos", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi.fn();

    render(<FormularioIdiomas onSalvar={onSalvar} />);

    await usuario.type(screen.getByLabelText("Idioma"), "Inglês");
    await usuario.selectOptions(
      screen.getByLabelText("Nível de proficiência"),
      "avancado",
    );
    await usuario.click(screen.getByText("Salvar idiomas"));

    expect(onSalvar).toHaveBeenCalledWith([
      { nome: "Inglês", nivel: "avancado" },
    ]);
    expect(screen.getByRole("status")).toHaveTextContent(
      "Idiomas salvos com sucesso.",
    );
  });

  it("não chama onSalvar quando há erros de validação", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi.fn();

    render(<FormularioIdiomas onSalvar={onSalvar} />);

    await usuario.click(screen.getByText("Salvar idiomas"));

    expect(onSalvar).not.toHaveBeenCalled();
  });

  it("exibe as quatro opções de nível no select", () => {
    render(<FormularioIdiomas />);

    const select = screen.getByLabelText("Nível de proficiência");
    const opcoes = select.querySelectorAll("option");

    expect(opcoes).toHaveLength(5);
    expect(opcoes[0]).toHaveTextContent("Selecione um nível");
    expect(opcoes[1]).toHaveTextContent("Básico");
    expect(opcoes[2]).toHaveTextContent("Intermediário");
    expect(opcoes[3]).toHaveTextContent("Avançado");
    expect(opcoes[4]).toHaveTextContent("Fluente");
  });
});
