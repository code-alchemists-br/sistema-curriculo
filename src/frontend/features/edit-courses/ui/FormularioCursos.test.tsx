import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { FormularioCursos } from "./FormularioCursos";

afterEach(cleanup);

describe("FormularioCursos", () => {
  it("renderiza um curso vazio por padrão", () => {
    render(<FormularioCursos />);

    expect(screen.getByLabelText("Nome do curso")).toHaveValue("");
    expect(screen.getByLabelText("Instituição")).toHaveValue("");
    expect(screen.getByLabelText("Carga horária (horas)")).toHaveValue("");
  });

  it("adiciona uma nova entrada de curso ao clicar no botão", async () => {
    const usuario = userEvent.setup();
    render(<FormularioCursos />);

    await usuario.click(screen.getByText("+ Adicionar curso"));

    const campos = screen.getAllByLabelText("Nome do curso");
    expect(campos).toHaveLength(2);
  });

  it("remove uma entrada de curso ao clicar no botão de remoção", async () => {
    const usuario = userEvent.setup();
    render(
      <FormularioCursos
        cursosIniciais={[
          { nome: "React", instituicao: "Alura", cargaHoraria: "40" },
          { nome: "Node", instituicao: "Udemy", cargaHoraria: "20" }
        ]}
      />
    );

    await usuario.click(screen.getByLabelText("Remover curso 1"));

    const campos = screen.getAllByLabelText("Nome do curso");
    expect(campos).toHaveLength(1);
    expect(campos[0]).toHaveValue("Node");
  });

  it("exibe erros de validação quando campos obrigatórios estão vazios", async () => {
    const usuario = userEvent.setup();
    render(<FormularioCursos />);

    await usuario.click(screen.getByText("Salvar cursos"));

    expect(screen.getByText("Informe o nome do curso.")).toBeInTheDocument();
    expect(screen.getByText("Informe a instituição.")).toBeInTheDocument();
    expect(screen.getByText("Informe uma carga horária válida (em horas).")).toBeInTheDocument();
  });

  it("chama onSalvar com cursos normalizados quando válidos", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi.fn();

    render(<FormularioCursos onSalvar={onSalvar} />);

    await usuario.type(screen.getByLabelText("Nome do curso"), "  React Avançado  ");
    await usuario.type(screen.getByLabelText("Instituição"), " Alura ");
    await usuario.type(screen.getByLabelText("Carga horária (horas)"), "40");
    await usuario.click(screen.getByText("Salvar cursos"));

    expect(onSalvar).toHaveBeenCalledWith([
      { nome: "React Avançado", instituicao: "Alura", cargaHoraria: "40" }
    ]);
    expect(screen.getByRole("status")).toHaveTextContent("Cursos salvos com sucesso.");
  });

  it("não chama onSalvar quando há erros de validação", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi.fn();

    render(<FormularioCursos onSalvar={onSalvar} />);

    await usuario.click(screen.getByText("Salvar cursos"));

    expect(onSalvar).not.toHaveBeenCalled();
  });
});
