import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ClienteVersoesCurriculo } from "../api/cliente-versoes-curriculo";
import type { AtualizacaoVersaoCurriculo } from "../model/versao-curriculo-perfil";
import { PainelCurriculosPerfil } from "./PainelCurriculosPerfil";

afterEach(cleanup);

/** Cria um double com duas versões para os testes de comportamento do painel. */
function criarClienteDeSucesso(): ClienteVersoesCurriculo {
  return {
    listar: vi.fn().mockResolvedValue([
      {
        id: "curriculo-1",
        tituloVersao: "Currículo para estágio",
        modelo: "primeiro-emprego",
        visibilidade: "privado",
        totalItens: 8,
      },
      {
        id: "curriculo-2",
        tituloVersao: "Currículo para vagas de tecnologia",
        modelo: "moderno",
        visibilidade: "publico",
        totalItens: 12,
      },
    ]),
    atualizar: vi
      .fn()
      .mockImplementation(
        async (id: string, dados: AtualizacaoVersaoCurriculo) => ({
          id,
          ...dados,
          totalItens: 8,
        }),
      ),
  };
}

/** Renderiza uma miniatura simples para isolar o comportamento do painel. */
function renderizarMiniatura() {
  return <div aria-hidden="true" />;
}

describe("PainelCurriculosPerfil", () => {
  it("lista versões com o título e o modelo, sem expor dados técnicos", async () => {
    render(
      <PainelCurriculosPerfil
        cliente={criarClienteDeSucesso()}
        renderizarMiniatura={renderizarMiniatura}
      />,
    );

    expect(
      await screen.findByRole("heading", { name: "Currículo para estágio" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Modelo: Primeiro emprego")).toBeInTheDocument();
    expect(screen.queryByText(/itens incluídos/i)).not.toBeInTheDocument();
    expect(screen.queryByText("Pública")).not.toBeInTheDocument();
  });

  it("altera os metadados de uma versão sem modificar as demais", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteDeSucesso();

    render(
      <PainelCurriculosPerfil
        cliente={cliente}
        renderizarMiniatura={renderizarMiniatura}
      />,
    );

    await screen.findByText("Currículo para estágio");
    await usuario.click(
      screen.getByRole("button", {
        name: "Editar versão Currículo para estágio",
      }),
    );
    await usuario.clear(screen.getByLabelText("Título da versão"));
    await usuario.type(
      screen.getByLabelText("Título da versão"),
      "Currículo para trainee",
    );
    await usuario.selectOptions(screen.getByLabelText("Modelo"), "moderno");
    await usuario.click(screen.getByRole("button", { name: "Salvar versão" }));

    expect(await screen.findByRole("status")).toHaveTextContent(
      "Versão atualizada com sucesso.",
    );
    expect(cliente.atualizar).toHaveBeenCalledWith("curriculo-1", {
      tituloVersao: "Currículo para trainee",
      modelo: "moderno",
      visibilidade: "privado",
    });
    expect(
      screen.getByRole("heading", { name: "Currículo para trainee" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", {
        name: "Currículo para vagas de tecnologia",
      }),
    ).toBeInTheDocument();
  });

  it("permite iniciar a criação de uma nova versão", async () => {
    const usuario = userEvent.setup();
    const onCriarNovaVersao = vi.fn();

    render(
      <PainelCurriculosPerfil
        cliente={criarClienteDeSucesso()}
        onCriarNovaVersao={onCriarNovaVersao}
        renderizarMiniatura={renderizarMiniatura}
      />,
    );

    await usuario.click(
      await screen.findByRole("button", { name: "Criar nova versão" }),
    );

    expect(onCriarNovaVersao).toHaveBeenCalledTimes(1);
  });
});
