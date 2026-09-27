import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { FormularioExperiencias } from "./FormularioExperiencias";
import type { Experiencia } from "../model/experiencias";

afterEach(cleanup);

const experienciaCompleta: Experiencia = {
  empresa: "Tech Corp",
  cargo: "Desenvolvedor",
  inicio: "2024-01",
  fim: "2025-06",
  empregoAtual: false,
  descricao: "Desenvolvimento frontend."
};

describe("FormularioExperiencias", () => {
  it("renderiza uma experiência vazia por padrão", () => {
    render(<FormularioExperiencias />);

    expect(screen.getByLabelText("Nome da empresa")).toHaveValue("");
    expect(screen.getByLabelText("Cargo")).toHaveValue("");
  });

  it("adiciona uma nova entrada ao clicar no botão", async () => {
    const usuario = userEvent.setup();
    render(<FormularioExperiencias />);

    await usuario.click(screen.getByText("+ Adicionar experiência"));

    const campos = screen.getAllByLabelText("Nome da empresa");
    expect(campos).toHaveLength(2);
  });

  it("remove uma entrada ao clicar no botão de remoção", async () => {
    const usuario = userEvent.setup();
    render(
      <FormularioExperiencias
        experienciasIniciais={[
          experienciaCompleta,
          { ...experienciaCompleta, empresa: "Outra Empresa" }
        ]}
      />
    );

    await usuario.click(screen.getByLabelText("Remover experiência 1"));

    const campos = screen.getAllByLabelText("Nome da empresa");
    expect(campos).toHaveLength(1);
    expect(campos[0]).toHaveValue("Outra Empresa");
  });

  it("desabilita o campo Fim quando Emprego atual é marcado", async () => {
    const usuario = userEvent.setup();
    render(<FormularioExperiencias />);

    const checkbox = screen.getByLabelText("Emprego atual");
    await usuario.click(checkbox);

    expect(screen.getByLabelText("Fim (Mês/Ano)")).toBeDisabled();
  });

  it("reabilita o campo Fim quando Emprego atual é desmarcado", async () => {
    const usuario = userEvent.setup();
    render(
      <FormularioExperiencias
        experienciasIniciais={[{ ...experienciaCompleta, empregoAtual: true, fim: "" }]}
      />
    );

    const checkbox = screen.getByLabelText("Emprego atual");
    await usuario.click(checkbox);

    expect(screen.getByLabelText("Fim (Mês/Ano)")).not.toBeDisabled();
  });

  it("exibe erros de validação quando campos obrigatórios estão vazios", async () => {
    const usuario = userEvent.setup();
    render(<FormularioExperiencias />);

    await usuario.click(screen.getByText("Salvar experiências"));

    expect(screen.getByText("Informe o nome da empresa.")).toBeInTheDocument();
    expect(screen.getByText("Informe o cargo exercido.")).toBeInTheDocument();
    expect(screen.getByText("Informe a data de início.")).toBeInTheDocument();
  });

  it("chama onSalvar com experiências ordenadas quando válidas", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi.fn();

    render(
      <FormularioExperiencias
        experienciasIniciais={[
          { ...experienciaCompleta, empresa: "Antiga", inicio: "2020-01", fim: "2021-12" },
          { ...experienciaCompleta, empresa: "Recente", inicio: "2024-01", fim: "2025-06" }
        ]}
        onSalvar={onSalvar}
      />
    );

    await usuario.click(screen.getByText("Salvar experiências"));

    expect(onSalvar).toHaveBeenCalledTimes(1);
    const resultado = onSalvar.mock.calls[0][0] as Experiencia[];
    expect(resultado[0].empresa).toBe("Recente");
    expect(resultado[1].empresa).toBe("Antiga");
    expect(screen.getByRole("status")).toHaveTextContent("Experiências salvas com sucesso.");
  });

  it("não chama onSalvar quando há erros de validação", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi.fn();

    render(<FormularioExperiencias onSalvar={onSalvar} />);

    await usuario.click(screen.getByText("Salvar experiências"));

    expect(onSalvar).not.toHaveBeenCalled();
  });
});
