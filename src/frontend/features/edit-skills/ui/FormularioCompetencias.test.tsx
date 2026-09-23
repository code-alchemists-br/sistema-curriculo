import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { FormularioCompetencias } from "./FormularioCompetencias";

afterEach(cleanup);

describe("FormularioCompetencias", () => {
  it("renderiza Hard Skills e Soft Skills separadamente", () => {
    render(<FormularioCompetencias />);

    expect(
      screen.getByRole("heading", { name: "Hard Skills" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Soft Skills" }),
    ).toBeInTheDocument();
  });

  it("transforma o texto digitado em tag ao pressionar Enter", async () => {
    const usuario = userEvent.setup();

    render(<FormularioCompetencias />);

    const input = screen.getByRole("textbox", {
      name: "Adicionar competência técnica",
    });

    await usuario.type(input, "React");
    await usuario.keyboard("{Enter}");

    const hardSkills = screen.getByLabelText("Hard Skills selecionadas");

    expect(hardSkills).toHaveTextContent("React");
    expect(input).toHaveValue("");
  });

  it("permite remover uma tag pelo botão de exclusão", async () => {
    const usuario = userEvent.setup();

    render(
      <FormularioCompetencias
        habilidadesIniciais={{
          hardSkills: ["React"],
          softSkills: [],
        }}
      />,
    );

    const hardSkills = screen.getByLabelText("Hard Skills selecionadas");

    expect(hardSkills).toHaveTextContent("React");

    await usuario.click(screen.getByRole("button", { name: "Remover React" }));

    expect(hardSkills).not.toHaveTextContent("React");
  });

  it("permite adicionar uma habilidade pré-definida por clique", async () => {
    const usuario = userEvent.setup();

    render(<FormularioCompetencias />);

    await usuario.click(screen.getByRole("button", { name: "Python" }));

    const hardSkills = screen.getByLabelText("Hard Skills selecionadas");

    expect(hardSkills).toHaveTextContent("Python");
  });

  it("não cria uma tag vazia ao pressionar Enter", async () => {
    const usuario = userEvent.setup();

    render(<FormularioCompetencias />);

    const input = screen.getByRole("textbox", {
      name: "Adicionar competência técnica",
    });

    await usuario.type(input, "   ");
    await usuario.keyboard("{Enter}");

    const hardSkills = screen.getByLabelText("Hard Skills selecionadas");

    expect(hardSkills).toBeEmptyDOMElement();
  });

  it("não permite adicionar a mesma habilidade duas vezes", async () => {
    const usuario = userEvent.setup();

    render(<FormularioCompetencias />);

    const input = screen.getByRole("textbox", {
      name: "Adicionar competência técnica",
    });

    await usuario.type(input, "Java");
    await usuario.keyboard("{Enter}");

    await usuario.type(input, "Java");
    await usuario.keyboard("{Enter}");

    const hardSkills = screen.getByLabelText("Hard Skills selecionadas");

    expect(hardSkills).toHaveTextContent("Java");
    expect(hardSkills.querySelectorAll(".skill-chip")).toHaveLength(1);
  });

  it("envia as competências separadas ao salvar", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi.fn();

    render(<FormularioCompetencias onSalvar={onSalvar} />);

    const hardInput = screen.getByRole("textbox", {
      name: "Adicionar competência técnica",
    });

    const softInput = screen.getByRole("textbox", {
      name: "Adicionar competência comportamental",
    });

    await usuario.type(hardInput, "Java");
    await usuario.keyboard("{Enter}");

    await usuario.type(softInput, "Comunicação");
    await usuario.keyboard("{Enter}");

    await usuario.click(
      screen.getByRole("button", { name: "Salvar competências" }),
    );

    expect(onSalvar).toHaveBeenCalledWith({
      hardSkills: ["Java"],
      softSkills: ["Comunicação"],
    });
  });
});
