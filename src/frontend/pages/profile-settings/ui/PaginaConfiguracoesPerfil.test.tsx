import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ClientePerfilEstudante } from "../../../features/edit-profile";
import type { ClienteVersoesCurriculo } from "../../../features/gerenciar-curriculos-perfil";
import { PaginaConfiguracoesPerfil } from "./PaginaConfiguracoesPerfil";

afterEach(cleanup);

const clientePerfil: ClientePerfilEstudante = {
  atualizar: vi.fn().mockResolvedValue(undefined),
  excluir: vi.fn().mockRejectedValue(new Error("indisponível")),
};

const clienteCurriculos: ClienteVersoesCurriculo = {
  listar: vi.fn().mockResolvedValue([
    {
      id: "versao-1",
      tituloVersao: "Currículo de estágio",
      modelo: "primeiro-emprego",
      visibilidade: "privado",
      totalItens: 7,
    },
  ]),
  atualizar: vi.fn(),
};

describe("PaginaConfiguracoesPerfil", () => {
  it("reúne os dados pessoais e as versões de currículo em uma única tela", async () => {
    render(
      <PaginaConfiguracoesPerfil
        cliente={clientePerfil}
        clienteCurriculos={clienteCurriculos}
        valoresIniciais={{
          nomeCompleto: "Ana Silva",
          enderecoCompleto: "Rua das Flores, 20",
          telefones: ["(11) 90000-0000"],
          email: "ana@exemplo.com",
          linkedIn: "https://www.linkedin.com/in/ana-silva",
        }}
      />,
    );

    expect(
      screen.getByRole("heading", { name: "Seu perfil e seus currículos" }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Endereço completo")).toHaveValue(
      "Rua das Flores, 20",
    );
    expect(
      await screen.findByRole("heading", { name: "Currículo de estágio" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Modelo: Primeiro emprego")).toBeInTheDocument();
    expect(
      screen.getByRole("img", {
        name: "Prévia estrutural do modelo Primeiro emprego",
      }),
    ).toBeInTheDocument();
  });

  it("direciona a pessoa para criar uma nova versão quando a ação é escolhida", async () => {
    const usuario = userEvent.setup();
    const onCriarNovaVersao = vi.fn();

    render(
      <PaginaConfiguracoesPerfil
        cliente={clientePerfil}
        clienteCurriculos={clienteCurriculos}
        onCriarNovaVersao={onCriarNovaVersao}
      />,
    );

    await usuario.click(
      await screen.findByRole("button", { name: "Criar nova versão" }),
    );

    expect(onCriarNovaVersao).toHaveBeenCalledTimes(1);
  });
});
