import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { App } from "./App";

vi.mock("../pages/visualizar-curriculo/model/exportar-pdf-cliente", () => ({
  exportarElementoParaPdf: vi.fn().mockResolvedValue(undefined),
}));

afterEach(() => {
  cleanup();
  window.history.replaceState({}, "", "/");
  sessionStorage.clear();
  localStorage.clear();
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

  it("permite visualizar o curriculo renderizado no modelo ativo e baixar PDF", async () => {
    window.history.replaceState({}, "", "/?etapa=visualizar-curriculo");

    const user = userEvent.setup();
    render(<App />);

    expect(
      await screen.findByRole("heading", {
        name: "Visualização do currículo",
      }),
    ).toBeInTheDocument();

    const btnBaixar = screen.getByRole("button", {
      name: "Baixar PDF",
    });
    await user.click(btnBaixar);

    const btnVoltar = screen.getByRole("button", {
      name: "← Voltar para validação",
    });
    await user.click(btnVoltar);

    expect(
      await screen.findByRole("heading", {
        name: "Valide os dados do currículo",
      }),
    ).toBeInTheDocument();
  });

  it("permite navegar diretamente para corrigir uma etapa pendente a partir da tela de validação", async () => {
    window.history.replaceState({}, "", "/?etapa=validacao-curriculo");

    const user = userEvent.setup();
    render(<App />);

    expect(
      await screen.findByRole("heading", {
        name: "Valide os dados do currículo",
      }),
    ).toBeInTheDocument();

    const btnCorrigir = screen.getByRole("button", {
      name: "Corrigir Dados pessoais",
    });
    await user.click(btnCorrigir);

    expect(
      await screen.findByRole("heading", {
        name: "Conte um pouco sobre você",
      }),
    ).toBeInTheDocument();
  });

  it("permite retornar diretamente à página inicial a partir do topo do layout de cadastro", async () => {
    window.history.replaceState({}, "", "/?etapa=validacao-curriculo");

    const user = userEvent.setup();
    render(<App />);

    expect(
      await screen.findByRole("heading", {
        name: "Valide os dados do currículo",
      }),
    ).toBeInTheDocument();

    const btnVoltarInicio = screen.getByRole("button", {
      name: "Voltar para a página inicial",
    });
    await user.click(btnVoltarInicio);

    expect(
      await screen.findByRole("button", {
        name: /CRIAR CURRÍCULO/i,
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", {
        name: "O currículo que abre portas",
      }),
    ).toBeInTheDocument();
  });

  it("restaura rascunho persistido em sessionStorage ao inicializar", async () => {
    sessionStorage.setItem(
      "liminal_curriculo_rascunho",
      JSON.stringify({
        dadosPessoais: {
          nomeCompleto: "Carlos Drummond",
          enderecoCompleto: "Rua Minas, 123",
          telefones: ["(31) 98765-4321"],
          email: "carlos@example.com",
        },
      }),
    );
    window.history.replaceState({}, "", "/?etapa=dados-pessoais");

    render(<App />);

    expect(
      await screen.findByDisplayValue("Carlos Drummond"),
    ).toBeInTheDocument();
    expect(screen.getByDisplayValue("carlos@example.com")).toBeInTheDocument();

    sessionStorage.removeItem("liminal_curriculo_rascunho");
  });

  it("permite navegar para a tela de recuperação de senha a partir do login e retornar", async () => {
    window.history.replaceState({}, "", "/?etapa=acesso");
    const user = userEvent.setup();

    render(<App />);

    expect(
      screen.getByRole("heading", { name: "Conecte-se na LIMINAL" }),
    ).toBeInTheDocument();

    const btnEsqueceuSenha = screen.getByRole("button", {
      name: "Esqueceu sua senha?",
    });
    await user.click(btnEsqueceuSenha);

    expect(
      await screen.findByRole("heading", { name: "Recupere sua senha" }),
    ).toBeInTheDocument();

    const btnVoltarLogin = screen.getByRole("button", {
      name: "← Voltar para o login",
    });
    await user.click(btnVoltarLogin);

    expect(
      await screen.findByRole("heading", { name: "Conecte-se na LIMINAL" }),
    ).toBeInTheDocument();
  });
});
