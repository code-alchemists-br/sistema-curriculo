import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { BotaoHero } from "./BotaoHero";

afterEach(cleanup);

describe("BotaoHero", () => {
  it("renderiza o rótulo de texto e o ícone de seta", () => {
    render(<BotaoHero>Entrar</BotaoHero>);

    const botao = screen.getByRole("button", { name: "Entrar" });
    expect(botao).toBeInTheDocument();
    expect(botao.querySelector(".botao-hero__icon")).toBeInTheDocument();
  });

  it("permite omitir o ícone de seta via mostrarIcone={false}", () => {
    render(<BotaoHero mostrarIcone={false}>Salvar</BotaoHero>);

    const botao = screen.getByRole("button", { name: "Salvar" });
    expect(botao).toBeInTheDocument();
    expect(botao.querySelector(".botao-hero__icon")).toBeNull();
  });

  it("chama o manipulador onClick quando acionado", async () => {
    const onClick = vi.fn();
    const usuario = userEvent.setup();

    render(<BotaoHero onClick={onClick}>Acessar</BotaoHero>);

    await usuario.click(screen.getByRole("button", { name: "Acessar" }));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it("respeita o estado disabled e não executa o callback", async () => {
    const onClick = vi.fn();
    const usuario = userEvent.setup();

    render(
      <BotaoHero disabled onClick={onClick}>
        Confirmando...
      </BotaoHero>,
    );

    const botao = screen.getByRole("button", { name: "Confirmando..." });
    expect(botao).toBeDisabled();

    await usuario.click(botao);
    expect(onClick).not.toHaveBeenCalled();
  });
});
