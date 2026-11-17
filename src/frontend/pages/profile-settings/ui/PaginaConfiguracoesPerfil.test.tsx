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

const clienteCurriculosComDados: ClienteVersoesCurriculo = {
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

const clienteCurriculosVazio: ClienteVersoesCurriculo = {
  listar: vi.fn().mockResolvedValue([]),
  atualizar: vi.fn(),
};

describe("PaginaConfiguracoesPerfil", () => {
  it("reúne os dados pessoais e as opções de modelo do currículo na tela", async () => {
    render(
      <PaginaConfiguracoesPerfil
        cliente={clientePerfil}
        clienteCurriculos={clienteCurriculosComDados}
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
      screen.getByRole("heading", { name: "Perfil e modelo do currículo" }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Endereço completo")).toHaveValue(
      "Rua das Flores, 20",
    );
    expect(
      await screen.findByRole("heading", { name: "Currículo de estágio" }),
    ).toBeInTheDocument();
    expect(screen.getByText(/Modelo ativo:/i)).toHaveTextContent(
      "Primeiro emprego",
    );
    expect(
      screen.getByRole("img", {
        name: "Prévia visual do modelo Primeiro emprego",
      }),
    ).toBeInTheDocument();
  });

  it("permite navegar para criação de currículo quando não há nenhum cadastrado", async () => {
    const usuario = userEvent.setup();
    const onCriarNovaVersao = vi.fn();

    render(
      <PaginaConfiguracoesPerfil
        cliente={clientePerfil}
        clienteCurriculos={clienteCurriculosVazio}
        onCriarNovaVersao={onCriarNovaVersao}
      />,
    );

    const botaoCriar = await screen.findByRole("button", {
      name: "Criar meu currículo",
    });
    await usuario.click(botaoCriar);

    expect(onCriarNovaVersao).toHaveBeenCalledTimes(1);
  });
});
