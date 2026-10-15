import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ClientePerfilEstudante } from "../api/cliente-perfil-estudante";
import { FormularioEdicaoPerfil } from "./FormularioEdicaoPerfil";

afterEach(cleanup);

const valoresIniciais = {
  nomeCompleto: "Ana Souza",
  enderecoCompleto: "Rua Exemplo, 100",
  telefones: ["(11) 99999-0000"],
  email: "ana@exemplo.com",
};

/** Cria um double de sucesso para isolar as verificações de acessibilidade. */
function criarClienteDeSucesso(): ClientePerfilEstudante {
  return {
    atualizar: vi.fn().mockResolvedValue(undefined),
    excluir: vi.fn().mockResolvedValue(undefined),
  };
}

describe("FormularioEdicaoPerfil — acessibilidade dos links profissionais", () => {
  it("associa os rótulos aos campos de LinkedIn e Currículo Lattes", () => {
    render(
      <FormularioEdicaoPerfil
        cliente={criarClienteDeSucesso()}
        valoresIniciais={valoresIniciais}
      />,
    );

    expect(screen.getByLabelText(/linkedin/i)).toHaveAttribute(
      "id",
      "perfil-linkedin",
    );
    expect(screen.getByLabelText(/currículo lattes/i)).toHaveAttribute(
      "id",
      "perfil-curriculo-lattes",
    );
  });

  it("associa cada erro de URL inválida ao respectivo campo", async () => {
    const usuario = userEvent.setup();

    render(
      <FormularioEdicaoPerfil
        cliente={criarClienteDeSucesso()}
        valoresIniciais={valoresIniciais}
      />,
    );

    const campoLinkedIn = screen.getByLabelText(/linkedin/i);
    const campoLattes = screen.getByLabelText(/currículo lattes/i);
    await usuario.type(campoLinkedIn, "linkedin.exemplo.dev/ana");
    await usuario.type(campoLattes, "lattes.exemplo.dev/ana");
    await usuario.click(
      screen.getByRole("button", { name: "Salvar alterações" }),
    );

    expect(
      await screen.findAllByText("Informe uma URL absoluta válida."),
    ).toHaveLength(2);
    expect(campoLinkedIn).toHaveAttribute(
      "aria-describedby",
      "perfil-linkedin-erro",
    );
    expect(campoLattes).toHaveAttribute(
      "aria-describedby",
      "perfil-curriculo-lattes-erro",
    );
  });
});
