import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { FormularioExperiencias } from "./FormularioExperiencias";
import {
  LIMITES_EXPERIENCIA,
  obterDataAtualIso,
  type Experiencia,
} from "../model/experiencias";

afterEach(cleanup);

const experienciaCompleta: Experiencia = {
  empresa: "Tech Corp",
  cargo: "Desenvolvedor",
  inicio: "2024-01",
  fim: "2025-06",
  empregoAtual: false,
  descricao: "Desenvolvimento frontend.",
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
          { ...experienciaCompleta, empresa: "Outra Empresa" },
        ]}
      />,
    );

    await usuario.click(screen.getByLabelText("Remover experiência 1"));

    const campos = screen.getAllByLabelText("Nome da empresa");
    expect(campos).toHaveLength(1);
    expect(campos[0]).toHaveValue("Outra Empresa");

    await usuario.click(screen.getByRole("button", { name: /Desfazer/i }));
    const camposAposDesfazer = screen.getAllByLabelText("Nome da empresa");
    expect(camposAposDesfazer).toHaveLength(2);
    expect(camposAposDesfazer[0]).toHaveValue(experienciaCompleta.empresa);
  });

  it("desabilita o campo Fim quando Emprego atual é marcado", async () => {
    const usuario = userEvent.setup();
    render(<FormularioExperiencias />);

    const checkbox = screen.getByLabelText("Emprego atual");
    await usuario.click(checkbox);

    expect(screen.getByLabelText("Fim")).toBeDisabled();
  });

  it("reabilita o campo Fim quando Emprego atual é desmarcado", async () => {
    const usuario = userEvent.setup();
    render(
      <FormularioExperiencias
        experienciasIniciais={[
          { ...experienciaCompleta, empregoAtual: true, fim: "" },
        ]}
      />,
    );

    const checkbox = screen.getByLabelText("Emprego atual");
    await usuario.click(checkbox);

    expect(screen.getByLabelText("Fim")).not.toBeDisabled();
  });

  it("aplica atributos max e min nos campos de data para impedir datas futuras", () => {
    const hoje = obterDataAtualIso();
    render(
      <FormularioExperiencias
        experienciasIniciais={[
          {
            ...experienciaCompleta,
            inicio: "2024-01-01",
            fim: "2024-06-01",
          },
        ]}
      />,
    );

    const campoInicio = screen.getByLabelText("Início");
    const campoFim = screen.getByLabelText("Fim");

    expect(campoInicio).toHaveAttribute("max", hoje);
    expect(campoFim).toHaveAttribute("max", hoje);
    expect(campoFim).toHaveAttribute("min", "2024-01-01");
  });

  it("aplica atributos maxLength e exibe contador de caracteres da descrição", async () => {
    const usuario = userEvent.setup();
    render(<FormularioExperiencias />);

    const campoEmpresa = screen.getByLabelText("Nome da empresa");
    const campoCargo = screen.getByLabelText("Cargo");
    const campoDescricao = screen.getByLabelText("Descrição das atividades");

    expect(campoEmpresa).toHaveAttribute(
      "maxLength",
      String(LIMITES_EXPERIENCIA.empresaMax),
    );
    expect(campoCargo).toHaveAttribute(
      "maxLength",
      String(LIMITES_EXPERIENCIA.cargoMax),
    );
    expect(campoDescricao).toHaveAttribute(
      "maxLength",
      String(LIMITES_EXPERIENCIA.descricaoMax),
    );

    expect(screen.getByText("0/1500 caracteres")).toBeInTheDocument();

    await usuario.type(campoDescricao, "React");
    expect(screen.getByText("5/1500 caracteres")).toBeInTheDocument();
  });

  it("exibe erros de validação quando campos obrigatórios estão vazios", async () => {
    const usuario = userEvent.setup();
    render(<FormularioExperiencias />);

    await usuario.click(
      screen.getByRole("button", { name: "Salvar experiências" }),
    );

    expect(screen.getByText("Informe o nome da empresa.")).toBeInTheDocument();
    expect(screen.getByText("Informe o cargo exercido.")).toBeInTheDocument();
    expect(screen.getByText("Informe a data de início.")).toBeInTheDocument();
    expect(
      screen.getByText("Informe a descrição das atividades."),
    ).toBeInTheDocument();
  });

  it("chama onSalvar com experiências ordenadas quando válidas", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi.fn();

    render(
      <FormularioExperiencias
        experienciasIniciais={[
          {
            ...experienciaCompleta,
            empresa: "Antiga",
            inicio: "2020-01",
            fim: "2021-12",
          },
          {
            ...experienciaCompleta,
            empresa: "Recente",
            inicio: "2024-01",
            fim: "2025-06",
          },
        ]}
        onSalvar={onSalvar}
      />,
    );

    await usuario.click(
      screen.getByRole("button", { name: "Salvar experiências" }),
    );

    expect(onSalvar).toHaveBeenCalledTimes(1);
    const resultado = onSalvar.mock.calls[0][0] as Experiencia[];
    expect(resultado[0].empresa).toBe("Recente");
    expect(resultado[1].empresa).toBe("Antiga");
    expect(screen.getByRole("status")).toHaveTextContent(
      "Experiências salvas com sucesso.",
    );
  });

  it("não chama onSalvar quando há erros de validação", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi.fn();

    render(<FormularioExperiencias onSalvar={onSalvar} />);

    await usuario.click(
      screen.getByRole("button", { name: "Salvar experiências" }),
    );

    expect(onSalvar).not.toHaveBeenCalled();
  });

  it("permite desfazer a limpeza em massa ao clicar em Não possuo experiência profissional", async () => {
    const usuario = userEvent.setup();
    render(
      <FormularioExperiencias experienciasIniciais={[experienciaCompleta]} />,
    );

    expect(screen.getByLabelText("Nome da empresa")).toHaveValue(
      experienciaCompleta.empresa,
    );

    await usuario.click(
      screen.getByRole("button", {
        name: "Não possuo experiência profissional",
      }),
    );

    expect(screen.queryByLabelText("Nome da empresa")).not.toBeInTheDocument();

    await usuario.click(
      screen.getByRole("button", {
        name: "Desfazer remoção de todas as experiências",
      }),
    );

    expect(screen.getByLabelText("Nome da empresa")).toHaveValue(
      experienciaCompleta.empresa,
    );
  });

  it("aplica classes de alerta progressivo no contador de caracteres da descrição", () => {
    render(<FormularioExperiencias />);

    const campoDescricao = screen.getByLabelText("Descrição das atividades");
    const contador = screen.getByText(/0\/1500 caracteres/i);

    expect(contador).not.toHaveClass(
      "formulario-experiencias__contador-caracteres--alerta",
    );
    expect(contador).not.toHaveClass(
      "formulario-experiencias__contador-caracteres--limite",
    );

    // 80% de 1500 = 1200 -> alerta
    fireEvent.change(campoDescricao, { target: { value: "a".repeat(1250) } });
    expect(contador).toHaveClass(
      "formulario-experiencias__contador-caracteres--alerta",
    );
    expect(screen.getByText("1250/1500 caracteres")).toBeInTheDocument();

    // 100% de 1500 = 1500 -> limite
    fireEvent.change(campoDescricao, { target: { value: "b".repeat(1500) } });
    expect(contador).toHaveClass(
      "formulario-experiencias__contador-caracteres--limite",
    );
    expect(screen.getByText("1500/1500 caracteres")).toBeInTheDocument();
  });
});
