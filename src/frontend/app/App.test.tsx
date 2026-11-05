import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { App } from "./App";

afterEach(() => {
  cleanup();
  window.history.replaceState({}, "", "/");
  sessionStorage.clear();
});

describe("App", () => {
  it("apresenta a porta de entrada com a seção hero e permite acessar a conta", async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(
      screen.getByRole("heading", { name: "O currículo que abre portas" }),
    ).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Fazer login" }));

    expect(
      screen.getByRole("heading", { name: "Conecte-se na LIMINAL" }),
    ).toBeInTheDocument();
  });

  it("navega entre os documentos públicos pela URL e pelos controles da tela", async () => {
    const user = userEvent.setup();
    window.history.replaceState({}, "", "/?etapa=termos-de-uso");

    render(<App />);

    expect(
      screen.getByRole("heading", { level: 1, name: "Termos de Uso" }),
    ).toBeInTheDocument();

    await user.click(
      screen.getByRole("button", { name: "Ler Política de Privacidade" }),
    );

    expect(
      screen.getByRole("heading", {
        level: 1,
        name: "Política de Privacidade",
      }),
    ).toBeInTheDocument();
  });

  it("permite preencher dados pessoais, avançar para a próxima etapa, voltar e verificar que os dados continuam preenchidos", async () => {
    sessionStorage.setItem(
      "liminal_usuario_sessao",
      JSON.stringify({
        nome: "Ricardo Santos",
        email: "ricardo@fatec.sp.gov.br",
      }),
    );
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole("button", { name: "CRIAR CURRÍCULO →" }));

    expect(
      screen.getByRole("heading", { name: "Conte um pouco sobre você" }),
    ).toBeInTheDocument();

    await user.type(screen.getByLabelText("Nome Completo"), "Ricardo Santos");
    await user.type(screen.getByLabelText("Endereço"), "Rua das Acácias, 123");
    await user.type(screen.getByLabelText("Telefone 1"), "(11) 98765-4321");
    await user.type(screen.getByLabelText("E-mail"), "ricardo@fatec.sp.gov.br");

    await user.click(
      screen.getByRole("button", { name: "Salvar dados pessoais" }),
    );

    expect(
      await screen.findByRole("heading", { name: "Formação acadêmica" }),
    ).toBeInTheDocument();

    await user.click(
      screen.getByRole("button", { name: "Voltar para a etapa anterior" }),
    );

    expect(
      screen.getByRole("heading", { name: "Conte um pouco sobre você" }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Nome Completo")).toHaveValue(
      "Ricardo Santos",
    );
    expect(screen.getByLabelText("Endereço")).toHaveValue(
      "Rua das Acácias, 123",
    );
    expect(screen.getByLabelText("Telefone 1")).toHaveValue("(11) 98765-4321");
    expect(screen.getByLabelText("E-mail")).toHaveValue(
      "ricardo@fatec.sp.gov.br",
    );

    await user.click(
      screen.getByRole("button", { name: "Salvar dados pessoais" }),
    );

    expect(
      await screen.findByRole("heading", { name: "Formação acadêmica" }),
    ).toBeInTheDocument();
  });

  it("permite navegar para a tela de vagas sugeridas e exibe vagas fictícias por padrão", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(
      screen.getByRole("button", { name: /Menu de navegação e perfil/i }),
    );
    await user.click(screen.getByRole("menuitem", { name: /Vagas/i }));

    expect(
      await screen.findByRole("heading", {
        name: "Oportunidades compatíveis com o seu perfil",
      }),
    ).toBeInTheDocument();

    expect(
      await screen.findByRole("heading", {
        name: "Desenvolvedor(a) Frontend Júnior",
      }),
    ).toBeInTheDocument();

    await user.click(
      screen.getByRole("button", { name: "← Voltar ao início" }),
    );

    expect(
      screen.getByRole("heading", { name: "O currículo que abre portas" }),
    ).toBeInTheDocument();
  });

  it("redireciona para o inicio com cabecalho atualizado ao criar conta a partir do cabecalho", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole("button", { name: "Criar conta" }));

    expect(
      screen.getByRole("heading", { name: "Crie uma nova conta" }),
    ).toBeInTheDocument();

    await user.type(screen.getByLabelText("Nome"), "Carlos Eduardo");
    await user.type(screen.getByLabelText("E-mail"), "carlos@exemplo.com");
    await user.type(screen.getByLabelText("Senha"), "senha123");
    await user.type(screen.getByLabelText("Confirme a senha"), "senha123");

    await user.click(screen.getByRole("button", { name: "Criar conta" }));

    expect(
      await screen.findByRole("heading", {
        name: "O currículo que abre portas",
      }),
    ).toBeInTheDocument();

    expect(screen.getByText("Carlos")).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: "Fazer login" }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: "Criar conta" }),
    ).not.toBeInTheDocument();

    await user.click(
      screen.getByRole("button", { name: /Menu de navegação e perfil/i }),
    );
    await user.click(screen.getByRole("menuitem", { name: /Sair da conta/i }));

    expect(
      screen.getByRole("button", { name: "Fazer login" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Criar conta" }),
    ).toBeInTheDocument();
  });

  it("redireciona para cadastro e depois para criacao do curriculo ao clicar em 'Criar curriculo' sem conta", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole("button", { name: "CRIAR CURRÍCULO →" }));

    expect(
      screen.getByRole("heading", { name: "Crie uma nova conta" }),
    ).toBeInTheDocument();

    await user.type(screen.getByLabelText("Nome"), "Mariana Silva");
    await user.type(screen.getByLabelText("E-mail"), "mariana@fatec.sp.gov.br");
    await user.type(screen.getByLabelText("Senha"), "segredo123");
    await user.type(screen.getByLabelText("Confirme a senha"), "segredo123");

    await user.click(screen.getByRole("button", { name: "Criar conta" }));

    expect(
      await screen.findByRole("heading", {
        name: "Conte um pouco sobre você",
      }),
    ).toBeInTheDocument();

    expect(screen.getByLabelText("Nome Completo")).toHaveValue("Mariana Silva");
    expect(screen.getByLabelText("E-mail")).toHaveValue(
      "mariana@fatec.sp.gov.br",
    );
  });

  it("redefine a rolagem da janela para o topo ao navegar entre rotas", async () => {
    const scrollToMock = vi.fn();
    window.scrollTo = scrollToMock;

    const user = userEvent.setup();
    render(<App />);

    expect(scrollToMock).toHaveBeenCalledWith(0, 0);
    scrollToMock.mockClear();

    await user.click(screen.getByRole("button", { name: "Termos de Uso" }));

    expect(
      screen.getByRole("heading", { level: 1, name: "Termos de Uso" }),
    ).toBeInTheDocument();
    expect(scrollToMock).toHaveBeenCalledWith(0, 0);
  });
});
