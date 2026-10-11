import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { MensagemEstado } from "./MensagemEstado";

afterEach(cleanup);


describe("MensagemEstado", () => {
  it("renderiza o estado de carregamento com role status e texto padrão", () => {
    render(<MensagemEstado tipo="carregando" />);

    const elementoStatus = screen.getByRole("status");
    expect(elementoStatus).toBeInTheDocument();
    expect(elementoStatus).toHaveTextContent("Carregando...");
  });

  it("renderiza o estado de carregamento com título e mensagem personalizados", () => {
    render(
      <MensagemEstado
        mensagem="Buscando informações no servidor..."
        tipo="carregando"
        titulo="Aguarde um momento"
      />,
    );

    expect(
      screen.getByRole("heading", { level: 3, name: "Aguarde um momento" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Buscando informações no servidor..."),
    ).toBeInTheDocument();
  });

  it("renderiza o estado vazio com título e mensagem descritiva", () => {
    render(
      <MensagemEstado
        mensagem="Não há itens cadastrados nesta lista."
        tipo="vazio"
        titulo="Nenhum registro"
      />,
    );

    expect(
      screen.getByRole("heading", { level: 3, name: "Nenhum registro" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Não há itens cadastrados nesta lista."),
    ).toBeInTheDocument();
  });

  it("renderiza o estado de erro com role alert e título", () => {
    render(
      <MensagemEstado
        mensagem="Serviço temporariamente indisponível."
        tipo="erro"
        titulo="Falha na conexão"
      />,
    );

    const alerta = screen.getByRole("alert");
    expect(alerta).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { level: 3, name: "Falha na conexão" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Serviço temporariamente indisponível."),
    ).toBeInTheDocument();
  });

  it("renderiza botão de ação no estado de erro e dispara onAcao ao clicar", async () => {
    const usuario = userEvent.setup();
    const aoClicar = vi.fn();

    render(
      <MensagemEstado
        mensagem="Erro de rede"
        onAcao={aoClicar}
        tipo="erro"
      />,
    );

    const botao = screen.getByRole("button", { name: "Tentar novamente" });
    expect(botao).toBeInTheDocument();

    await usuario.click(botao);
    expect(aoClicar).toHaveBeenCalledTimes(1);
  });

  it("permite personalizar o rótulo do botão de ação através de textoAcao", async () => {
    const usuario = userEvent.setup();
    const aoClicar = vi.fn();

    render(
      <MensagemEstado
        onAcao={aoClicar}
        textoAcao="Recarregar dados"
        tipo="vazio"
        titulo="Lista vazia"
      />,
    );

    const botao = screen.getByRole("button", { name: "Recarregar dados" });
    expect(botao).toBeInTheDocument();

    await usuario.click(botao);
    expect(aoClicar).toHaveBeenCalledTimes(1);
  });

  it("não exibe botão de ação se onAcao não for informado", () => {
    render(
      <MensagemEstado
        mensagem="Falha sem ação"
        tipo="erro"
      />,
    );

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("renderiza children customizado quando fornecido", () => {
    render(
      <MensagemEstado tipo="vazio" titulo="Sem dados">
        <span data-testid="extra-info">Informação adicional</span>
      </MensagemEstado>,
    );

    expect(screen.getByTestId("extra-info")).toBeInTheDocument();
  });
});
