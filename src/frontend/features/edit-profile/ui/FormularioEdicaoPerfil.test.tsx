import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaPerfilEstudante,
  type ClientePerfilEstudante
} from "../api/cliente-perfil-estudante";
import { FormularioEdicaoPerfil } from "./FormularioEdicaoPerfil";

afterEach(cleanup);

const studentExistente = {
  nomeCompleto: "Ricardo Galdino",
  enderecoCompleto: "Av. Paulista, 1000",
  telefones: ["(11) 99999-0000"],
  email: "ricardo@exemplo.com"
};

function criarClienteDeSucesso(): ClientePerfilEstudante {
  return {
    atualizar: vi.fn().mockResolvedValue(undefined),
    excluir: vi.fn().mockResolvedValue(undefined)
  };
}

function criarClienteComFalha(): ClientePerfilEstudante {
  return {
    atualizar: vi.fn().mockRejectedValue(new FalhaPerfilEstudante("indisponivel")),
    excluir: vi.fn().mockRejectedValue(new FalhaPerfilEstudante("indisponivel"))
  };
}

describe("FormularioEdicaoPerfil", () => {
  it("exibe os dados iniciais do estudante nos campos do formulário", () => {
    render(
      <FormularioEdicaoPerfil
        cliente={criarClienteDeSucesso()}
        valoresIniciais={studentExistente}
      />
    );

    expect(screen.getByLabelText("Nome completo")).toHaveValue("Ricardo Galdino");
    expect(screen.getByLabelText("E-mail")).toHaveValue("ricardo@exemplo.com");
    expect(screen.getByLabelText("Telefone 1")).toHaveValue("(11) 99999-0000");
  });

  it("salva alterações e exibe mensagem de sucesso com o double", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteDeSucesso();

    render(
      <FormularioEdicaoPerfil
        cliente={cliente}
        valoresIniciais={studentExistente}
      />
    );

    await usuario.clear(screen.getByLabelText("Nome completo"));
    await usuario.type(screen.getByLabelText("Nome completo"), "Ricardo Silva");
    await usuario.click(screen.getByRole("button", { name: "Salvar alterações" }));

    expect(await screen.findByRole("status")).toHaveTextContent("Perfil atualizado com sucesso.");
    expect(cliente.atualizar).toHaveBeenCalledTimes(1);
  });

  it("preserva os dados e exibe erro quando o double de atualização falha", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteComFalha();

    render(
      <FormularioEdicaoPerfil
        cliente={cliente}
        valoresIniciais={studentExistente}
      />
    );

    await usuario.click(screen.getByRole("button", { name: "Salvar alterações" }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Não foi possível completar a operação no momento."
    );
    expect(screen.getByLabelText("Nome completo")).toHaveValue("Ricardo Galdino");
  });

  it("exige confirmação no modal antes de chamar o double de exclusão", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteDeSucesso();

    render(
      <FormularioEdicaoPerfil
        cliente={cliente}
        valoresIniciais={studentExistente}
      />
    );

    await usuario.click(screen.getByRole("button", { name: "Excluir minha conta" }));

    const botoesExcluir = screen.getAllByRole("button", { name: "Excluir minha conta" });
    await usuario.click(botoesExcluir[1]);

    expect(await screen.findByRole("status")).toHaveTextContent(
      "Sua conta foi excluída com sucesso."
    );
    expect(cliente.excluir).toHaveBeenCalledTimes(1);
  });

  it("não chama o double de exclusão quando o estudante cancela o modal", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteDeSucesso();

    render(
      <FormularioEdicaoPerfil
        cliente={cliente}
        valoresIniciais={studentExistente}
      />
    );

    await usuario.click(screen.getByRole("button", { name: "Excluir minha conta" }));
    await usuario.click(screen.getByRole("button", { name: "Cancelar" }));

    expect(cliente.excluir).not.toHaveBeenCalled();
  });
});
