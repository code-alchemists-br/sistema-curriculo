// Proveniência: decision-analysis prompts/frontend/20260921-120136-tela-cadastro-projetos-academicos-v001.md#v001
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaCadastroProjeto,
  type ClienteProjetosAcademicos
} from "../api/cliente-projetos-academicos";
import { FormularioCadastroProjetoAcademico } from "./FormularioCadastroProjetoAcademico";

afterEach(cleanup);

describe("FormularioCadastroProjetoAcademico", () => {
  it("preserva dados quando o double informa indisponibilidade", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteProjetosAcademicos = {
      cadastrar: vi.fn().mockRejectedValue(new FalhaCadastroProjeto("indisponivel"))
    };

    render(<FormularioCadastroProjetoAcademico cliente={cliente} />);

    await usuario.type(screen.getByLabelText("Título do projeto"), "Sistema Currículo");
    await usuario.type(screen.getByLabelText("Descrição"), "Aplicação para organizar currículos.");
    await usuario.type(screen.getByLabelText("Tecnologias utilizadas"), "React e TypeScript");
    await usuario.click(screen.getByRole("button", { name: "Cadastrar projeto" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("indisponível");
    expect(screen.getByLabelText("Título do projeto")).toHaveValue("Sistema Currículo");
    expect(screen.getByLabelText("Tecnologias utilizadas")).toHaveValue("React e TypeScript");
  });

  it("limpa os campos após sucesso retornado pelo double", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteProjetosAcademicos = {
      cadastrar: vi.fn().mockResolvedValue(undefined)
    };

    render(<FormularioCadastroProjetoAcademico cliente={cliente} />);

    await usuario.type(screen.getByLabelText("Título do projeto"), "Sistema Currículo");
    await usuario.type(screen.getByLabelText("Descrição"), "Aplicação para organizar currículos.");
    await usuario.click(screen.getByRole("button", { name: "Cadastrar projeto" }));

    expect(await screen.findByRole("status")).toHaveTextContent("enviados para processamento");
    expect(screen.getByLabelText("Título do projeto")).toHaveValue("");
    expect(screen.getByLabelText("Descrição")).toHaveValue("");
  });
});
