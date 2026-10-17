import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaFormacaoAcademica,
  type ClienteFormacaoAcademica,
} from "../api/cliente-formacao-academica";
import { FormularioFormacaoAcademica } from "./FormularioFormacaoAcademica";

afterEach(cleanup);

async function preencherFormacao(
  usuario: ReturnType<typeof userEvent.setup>,
): Promise<void> {
  await usuario.type(screen.getByLabelText("Instituição"), "FATEC São Paulo");
  await usuario.type(
    screen.getByLabelText("Curso"),
    "Análise e Desenvolvimento de Sistemas",
  );
  await usuario.selectOptions(
    screen.getByLabelText("Nível de formação"),
    "tecnologo",
  );
  await usuario.type(screen.getByLabelText("Data de início"), "2024-02-01");
  await usuario.selectOptions(
    screen.getByLabelText("Situação"),
    "em_andamento",
  );
}

describe("FormularioFormacaoAcademica", () => {
  it("mostra erros associados aos campos obrigatórios", async () => {
    const usuario = userEvent.setup();
    render(<FormularioFormacaoAcademica cliente={{ cadastrar: vi.fn() }} />);

    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(
      await screen.findByText("Informe a instituição."),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Instituição")).toHaveAttribute(
      "aria-invalid",
      "true",
    );
    expect(screen.getByRole("alert")).toHaveTextContent(
      "Revise os campos destacados",
    );
  });

  it("envia valores normalizados ao cliente injetado", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteFormacaoAcademica = {
      cadastrar: vi.fn().mockResolvedValue(undefined),
    };
    render(<FormularioFormacaoAcademica cliente={cliente} />);

    await preencherFormacao(usuario);
    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(cliente.cadastrar).toHaveBeenCalledWith({
      instituicao: "FATEC São Paulo",
      curso: "Análise e Desenvolvimento de Sistemas",
      nivel: "tecnologo",
      dataInicio: "2024-02-01",
      status: "em_andamento",
    });
    expect(await screen.findByRole("status")).toHaveTextContent(
      "enviada para registro",
    );
  });

  it("preserva os valores e informa falha compreensível", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteFormacaoAcademica = {
      cadastrar: vi
        .fn()
        .mockRejectedValue(new FalhaFormacaoAcademica("indisponivel")),
    };
    render(<FormularioFormacaoAcademica cliente={cliente} />);

    await preencherFormacao(usuario);
    await usuario.click(
      screen.getByRole("button", { name: "Cadastrar formação" }),
    );

    expect(await screen.findByRole("alert")).toHaveTextContent("indisponível");
    expect(screen.getByLabelText("Instituição")).toHaveValue("FATEC São Paulo");
  });
});
