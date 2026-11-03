import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { CabecalhoPublico } from "./CabecalhoPublico";

afterEach(cleanup);

describe("CabecalhoPublico", () => {
  it("renderiza a marca LIMINAL e as ações públicas de login e cadastro", () => {
    render(<CabecalhoPublico />);

    expect(screen.getByText("LIMINAL")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Fazer login" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Criar conta" }),
    ).toBeInTheDocument();
  });

  it("aciona callbacks correspondentes nos botões de navegação", async () => {
    const onLogin = vi.fn();
    const onCadastro = vi.fn();
    const user = userEvent.setup();

    render(
      <CabecalhoPublico
        onNavegarLogin={onLogin}
        onNavegarCadastro={onCadastro}
      />,
    );

    await user.click(screen.getByRole("button", { name: "Fazer login" }));
    expect(onLogin).toHaveBeenCalledTimes(1);

    await user.click(screen.getByRole("button", { name: "Criar conta" }));
    expect(onCadastro).toHaveBeenCalledTimes(1);
  });

  it("aciona callback ao clicar na logo LIMINAL para voltar ao início", async () => {
    const onInicio = vi.fn();
    const user = userEvent.setup();

    render(<CabecalhoPublico onNavegarInicio={onInicio} />);

    await user.click(screen.getByRole("button", { name: /LIMINAL/i }));
    expect(onInicio).toHaveBeenCalledTimes(1);
  });

  it("abre o menu de acesso rápido e aciona navegação para Meu perfil e Vagas", async () => {
    const onPerfil = vi.fn();
    const onVagas = vi.fn();
    const user = userEvent.setup();

    render(
      <CabecalhoPublico onNavegarPerfil={onPerfil} onNavegarVagas={onVagas} />,
    );

    const gatilhoMenu = screen.getByRole("button", {
      name: /Menu de navegação e perfil/i,
    });

    await user.click(gatilhoMenu);
    await user.click(screen.getByRole("menuitem", { name: /Meu perfil/i }));
    expect(onPerfil).toHaveBeenCalledTimes(1);

    await user.click(gatilhoMenu);
    await user.click(screen.getByRole("menuitem", { name: /Vagas/i }));
    expect(onVagas).toHaveBeenCalledTimes(1);
  });

  it("exibe saudacao do usuario e oculta botoes publicos quando autenticado", () => {
    render(
      <CabecalhoPublico
        usuarioLogado={{
          nome: "Ricardo Santos",
          email: "ricardo@fatec.sp.gov.br",
        }}
      />,
    );

    expect(screen.getByText("Ricardo")).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: "Fazer login" }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: "Criar conta" }),
    ).not.toBeInTheDocument();
  });

  it("permite acionar logout atraves do menu quando autenticado", async () => {
    const onLogout = vi.fn();
    const user = userEvent.setup();

    render(
      <CabecalhoPublico
        usuarioLogado={{ nome: "Ana Paula", email: "ana@fatec.sp.gov.br" }}
        onLogout={onLogout}
      />,
    );

    const gatilhoMenu = screen.getByRole("button", {
      name: /Menu de navegação e perfil/i,
    });
    await user.click(gatilhoMenu);

    const botaoLogout = screen.getByRole("menuitem", {
      name: /Sair da conta/i,
    });
    expect(botaoLogout).toBeInTheDocument();

    await user.click(botaoLogout);
    expect(onLogout).toHaveBeenCalledTimes(1);
  });
});
