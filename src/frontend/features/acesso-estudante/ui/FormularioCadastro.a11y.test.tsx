// Proveniência: decision-analysis prompts/frontend/20261012-094000-varredura-rotulos-foco-cadastro-v001.md#v001
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaAcessoEstudante,
  type ClienteAcessoEstudante,
} from "../api/cliente-acesso-estudante";
import { FormularioCadastro } from "./FormularioCadastro";

afterEach(cleanup);

describe("FormularioCadastro — Testes de Acessibilidade (a11y)", () => {
  /**
   * Valida a associação programática de rótulos acessíveis a todos os campos e controles.
   *
   * **O que faz:** Verifica se os 4 inputs e o botão de submissão possuem nomes acessíveis válidos no DOM.
   * **Como faz:** Consulta elementos por papel semântico (`textbox`, `button`) e rótulo acessível com `screen.getByRole` e `screen.getByLabelText`.
   * **Qual finalidade atende:** Garante a conformidade com WCAG 1.3.1 (Informações e Relações) e 4.1.2 (Nome, Papel, Valor) para tecnologias assistivas.
   */
  it("garante que todos os campos de entrada e botões possuem rótulos acessíveis associados", () => {
    const cliente: ClienteAcessoEstudante = {
      cadastrar: vi.fn(),
      acessar: vi.fn(),
    };

    render(<FormularioCadastro aoCadastrar={vi.fn()} cliente={cliente} />);

    const campoNome = screen.getByRole("textbox", { name: "Nome" });
    const campoEmail = screen.getByRole("textbox", { name: "E-mail" });
    const campoSenha = screen.getByLabelText("Senha");
    const campoConfirmacao = screen.getByLabelText("Confirme a senha");
    const botaoCriarConta = screen.getByRole("button", { name: "Criar conta" });

    expect(campoNome).toBeInTheDocument();
    expect(campoEmail).toBeInTheDocument();
    expect(campoSenha).toBeInTheDocument();
    expect(campoConfirmacao).toBeInTheDocument();
    expect(botaoCriarConta).toBeInTheDocument();
  });

  /**
   * Valida a sequência de navegação por foco de teclado via tecla Tab.
   *
   * **O que faz:** Percorre o formulário com a tecla Tab avaliando a ordem sequencial dos elementos ativos.
   * **Como faz:** Dispara eventos de tabulação através de `userEvent.tab()` e afere que o foco atinge sucessivamente Nome, E-mail, Senha, Confirmação e Botão.
   * **Qual finalidade atende:** Satisfaz o critério WCAG 2.1.1 (Teclado) e 2.4.3 (Ordem do Foco), impedindo desvios ou armadilhas de teclado.
   */
  it("garante ordem de foco sequencial e previsível via teclado (Tab)", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteAcessoEstudante = {
      cadastrar: vi.fn(),
      acessar: vi.fn(),
    };

    render(<FormularioCadastro aoCadastrar={vi.fn()} cliente={cliente} />);

    const campoNome = screen.getByRole("textbox", { name: "Nome" });
    const campoEmail = screen.getByRole("textbox", { name: "E-mail" });
    const campoSenha = screen.getByLabelText("Senha");
    const campoConfirmacao = screen.getByLabelText("Confirme a senha");
    const botaoCriarConta = screen.getByRole("button", { name: "Criar conta" });

    await usuario.tab();
    expect(campoNome).toHaveFocus();

    await usuario.tab();
    expect(campoEmail).toHaveFocus();

    await usuario.tab();
    expect(campoSenha).toHaveFocus();

    await usuario.tab();
    expect(campoConfirmacao).toHaveFocus();

    await usuario.tab();
    expect(botaoCriarConta).toHaveFocus();
  });

  /**
   * Valida a vinculação programática de mensagens de erro aos respectivos campos inválidos.
   *
   * **O que faz:** Submete o formulário com dados inválidos e afere a presença de `aria-invalid` e `aria-describedby`.
   * **Como faz:** Preenche senhas divergentes, clica em "Criar conta" e verifica se os inputs recebem `aria-invalid="true"` e apontam para os elementos de erro no DOM.
   * **Qual finalidade atende:** Cumpre o critério WCAG 3.3.1 (Identificação de Erros) e 1.3.1 (Relações), permitindo que leitores de tela anunciem o motivo da inconsistência.
   */
  it("associa mensagens de erro individuais aos campos correspondentes via aria-invalid e aria-describedby", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteAcessoEstudante = {
      cadastrar: vi.fn(),
      acessar: vi.fn(),
    };

    render(<FormularioCadastro aoCadastrar={vi.fn()} cliente={cliente} />);

    const campoSenha = screen.getByLabelText("Senha");
    const campoConfirmacao = screen.getByLabelText("Confirme a senha");
    await usuario.type(campoSenha, "senha123");
    await usuario.type(campoConfirmacao, "outrasenha");

    const botaoCriarConta = screen.getByRole("button", { name: "Criar conta" });
    await usuario.click(botaoCriarConta);

    const campoNome = screen.getByRole("textbox", { name: "Nome" });
    const campoEmail = screen.getByRole("textbox", { name: "E-mail" });

    expect(campoNome).toHaveAttribute("aria-invalid", "true");
    expect(campoNome).toHaveAttribute("aria-describedby", "nome-erro");
    expect(screen.getByText("Informe seu nome.")).toHaveAttribute(
      "id",
      "nome-erro",
    );

    expect(campoEmail).toHaveAttribute("aria-invalid", "true");
    expect(campoEmail).toHaveAttribute("aria-describedby", "email-cadastro-erro");
    expect(screen.getByText("Informe um e-mail válido.")).toHaveAttribute(
      "id",
      "email-cadastro-erro",
    );

    expect(campoConfirmacao).toHaveAttribute("aria-invalid", "true");
    expect(campoConfirmacao).toHaveAttribute(
      "aria-describedby",
      "confirmacao-senha-erro",
    );
    expect(screen.getByText("As senhas não coincidem.")).toHaveAttribute(
      "id",
      "confirmacao-senha-erro",
    );
  });

  /**
   * Valida o anúncio assertivo global na live region ao tentar submeter com pendências.
   *
   * **O que faz:** Confirma que a tentativa frustrada de envio gera aviso em elemento com `role="alert"`.
   * **Como faz:** Dispara submissão com dados em branco e consulta elemento com `role="alert"` contendo o texto informativo de pendência.
   * **Qual finalidade atende:** Satisfaz o critério WCAG 4.1.3 (Mensagens de Status) e 3.3.1, evitando falhas silenciosas na submissão.
   */
  it("emite feedback global acessível com role='alert' ao tentar submeter com pendências locais", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteAcessoEstudante = {
      cadastrar: vi.fn(),
      acessar: vi.fn(),
    };

    render(<FormularioCadastro aoCadastrar={vi.fn()} cliente={cliente} />);

    const botaoCriarConta = screen.getByRole("button", { name: "Criar conta" });
    await usuario.click(botaoCriarConta);

    const alertaGlobal = await screen.findByRole("alert");
    expect(alertaGlobal).toHaveTextContent(
      "Há pendências que precisam ser corrigidas antes de criar a conta.",
    );
    expect(cliente.cadastrar).not.toHaveBeenCalled();
  });

  /**
   * Valida a comunicação assertiva de erro retornado pela chamada da API de cadastro.
   *
   * **O que faz:** Simula rejeição remota por e-mail já existente e verifica a mensagem no alerta.
   * **Como faz:** Configura o double com `FalhaAcessoEstudante("email-ja-cadastrado")`, submete dados válidos e afere o elemento com `role="alert"`.
   * **Qual finalidade atende:** Garante que erros de regras de negócio remotas sejam anunciados de forma clara e acessível aos usuários.
   */
  it("anuncia erro de API de forma acessível com role='alert' quando o e-mail já está cadastrado", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteAcessoEstudante = {
      cadastrar: vi
        .fn()
        .mockRejectedValue(new FalhaAcessoEstudante("email-ja-cadastrado")),
      acessar: vi.fn(),
    };

    render(<FormularioCadastro aoCadastrar={vi.fn()} cliente={cliente} />);

    await usuario.type(screen.getByRole("textbox", { name: "Nome" }), "Ana Silva");
    await usuario.type(
      screen.getByRole("textbox", { name: "E-mail" }),
      "ana@fatec.sp.gov.br",
    );
    await usuario.type(screen.getByLabelText("Senha"), "senhaSegura123");
    await usuario.type(screen.getByLabelText("Confirme a senha"), "senhaSegura123");

    await usuario.click(screen.getByRole("button", { name: "Criar conta" }));

    const alertaGlobal = await screen.findByRole("alert");
    expect(alertaGlobal).toHaveTextContent(
      "Este e-mail já possui uma conta.",
    );
  });

  /**
   * Valida a limpeza de feedback de erro e remoção de atributos aria-invalid ao alterar campos.
   *
   * **O que faz:** Confirma que digitar em um campo inválido remove o erro associado e o alerta global.
   * **Como faz:** Gera erro de submissão, digita no campo Nome e afere que `aria-invalid` é removido e o alerta global é limpo.
   * **Qual finalidade atende:** Garante que estados de erro desatualizados não confundam usuários de leitores de tela.
   */
  it("limpa erros e atualiza o estado acessível do campo assim que o usuário digita", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteAcessoEstudante = {
      cadastrar: vi.fn(),
      acessar: vi.fn(),
    };

    render(<FormularioCadastro aoCadastrar={vi.fn()} cliente={cliente} />);

    await usuario.click(screen.getByRole("button", { name: "Criar conta" }));
    expect(screen.getByRole("textbox", { name: "Nome" })).toHaveAttribute(
      "aria-invalid",
      "true",
    );
    expect(screen.getByRole("alert")).toBeInTheDocument();

    await usuario.type(screen.getByRole("textbox", { name: "Nome" }), "Carlos");
    expect(screen.getByRole("textbox", { name: "Nome" })).not.toHaveAttribute(
      "aria-invalid",
    );
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});
