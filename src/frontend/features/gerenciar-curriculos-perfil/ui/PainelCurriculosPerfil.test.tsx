import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ClienteVersoesCurriculo } from "../api/cliente-versoes-curriculo";
import type { AtualizacaoVersaoCurriculo } from "../model/versao-curriculo-perfil";
import { PainelCurriculosPerfil } from "./PainelCurriculosPerfil";

afterEach(cleanup);

/** Cria um double com um currículo para os testes de alteração de modelo. */
function criarClienteComCurriculo(): ClienteVersoesCurriculo {
  return {
    listar: vi.fn().mockResolvedValue([
      {
        id: "curriculo-1",
        tituloVersao: "Currículo de Ricardo Silveira",
        modelo: "primeiro-emprego",
        visibilidade: "privado",
        totalItens: 8,
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

/** Cria um double sem currículo cadastrado. */
function criarClienteSemCurriculo(): ClienteVersoesCurriculo {
  return {
    listar: vi.fn().mockResolvedValue([]),
    atualizar: vi.fn(),
  };
}

/** Renderiza uma miniatura simples com identificador do modelo para validar preview dinâmico. */
function renderizarMiniatura(modelo: string) {
  return <div data-testid={`miniatura-${modelo}`}>{modelo}</div>;
}

describe("PainelCurriculosPerfil", () => {
  it("exibe estado vazio e botão de criar currículo quando não há currículo cadastrado", async () => {
    const onCriarCurriculo = vi.fn();

    render(
      <PainelCurriculosPerfil
        cliente={criarClienteSemCurriculo()}
        onCriarCurriculo={onCriarCurriculo}
        renderizarMiniatura={renderizarMiniatura}
      />,
    );

    expect(
      await screen.findByRole("heading", {
        name: "Nenhum currículo cadastrado",
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/você ainda não criou um currículo/i),
    ).toBeInTheDocument();

    const botaoCriar = screen.getByRole("button", {
      name: "Criar meu currículo",
    });
    expect(botaoCriar).toBeInTheDocument();

    const usuario = userEvent.setup();
    await usuario.click(botaoCriar);
    expect(onCriarCurriculo).toHaveBeenCalledTimes(1);
  });

  it("exibe o currículo com o modelo ativo e miniatura correspondente", async () => {
    render(
      <PainelCurriculosPerfil
        cliente={criarClienteComCurriculo()}
        renderizarMiniatura={renderizarMiniatura}
      />,
    );

    expect(
      await screen.findByRole("heading", {
        name: "Currículo de Ricardo Silveira",
      }),
    ).toBeInTheDocument();
    expect(screen.getByText(/Modelo ativo:/i)).toHaveTextContent(
      "Primeiro emprego",
    );
    expect(
      screen.getByRole("combobox", {
        name: /selecione o modelo de apresentação:/i,
      }),
    ).toHaveValue("primeiro-emprego");
    expect(
      screen.getByTestId("miniatura-primeiro-emprego"),
    ).toBeInTheDocument();
  });

  it("salva automaticamente ao selecionar um novo modelo, atualizando a miniatura", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteComCurriculo();

    render(
      <PainelCurriculosPerfil
        cliente={cliente}
        renderizarMiniatura={renderizarMiniatura}
      />,
    );

    await screen.findByRole("heading", {
      name: "Currículo de Ricardo Silveira",
    });

    const seletor = screen.getByLabelText(
      "Selecione o modelo de apresentação:",
    );
    await usuario.selectOptions(seletor, "moderno");

    expect(cliente.atualizar).toHaveBeenCalledWith("curriculo-1", {
      tituloVersao: "Currículo de Ricardo Silveira",
      modelo: "moderno",
      visibilidade: "privado",
    });

    expect(screen.getByTestId("miniatura-moderno")).toBeInTheDocument();
    expect(screen.getByText(/Modelo ativo:/i)).toHaveTextContent("Moderno");
  });

  it("exibe mensagem de alerta amigável quando a atualização do modelo falha", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteVersoesCurriculo = {
      listar: vi.fn().mockResolvedValue([
        {
          id: "curriculo-1",
          tituloVersao: "Currículo de Ricardo Silveira",
          modelo: "primeiro-emprego",
          visibilidade: "privado",
          totalItens: 8,
        },
      ]),
      atualizar: vi.fn().mockRejectedValue(new Error("Erro de conexão")),
    };

    render(
      <PainelCurriculosPerfil
        cliente={cliente}
        renderizarMiniatura={renderizarMiniatura}
      />,
    );

    await screen.findByRole("heading", {
      name: "Currículo de Ricardo Silveira",
    });

    const seletor = screen.getByLabelText(
      "Selecione o modelo de apresentação:",
    );
    await usuario.selectOptions(seletor, "criativo");

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Não foi possível salvar o novo modelo no momento. Tente novamente mais tarde.",
    );
  });

  it("permite abrir o menu de download e acionar a exportação em PDF diretamente", async () => {
    const usuario = userEvent.setup();
    const aoBaixarCurriculo = vi.fn().mockResolvedValue(undefined);

    render(
      <PainelCurriculosPerfil
        aoBaixarCurriculo={aoBaixarCurriculo}
        cliente={criarClienteComCurriculo()}
        renderizarMiniatura={renderizarMiniatura}
      />,
    );

    await screen.findByRole("heading", {
      name: "Currículo de Ricardo Silveira",
    });

    const botaoDownload = screen.getByRole("button", {
      name: "Baixar currículo ▾",
    });
    await usuario.click(botaoDownload);

    const opcaoPdf = screen.getByRole("menuitem", { name: /PDF/i });
    expect(opcaoPdf).toBeInTheDocument();

    await usuario.click(opcaoPdf);
    expect(aoBaixarCurriculo).toHaveBeenCalledWith("pdf");
  });
});
