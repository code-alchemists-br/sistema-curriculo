// Proveniência: decision-analysis prompts/frontend/20261007-080500-teste-acessibilidade-formulario-curriculo-v001.md#v001
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaDadosPessoais,
  type ClienteDadosPessoais,
} from "../api/cliente-dados-pessoais";
import { FormularioDadosPessoais } from "./FormularioDadosPessoais";

afterEach(cleanup);

/**
 * Cria um dublê de cliente configurado para sucesso imediato.
 *
 * A função retorna um objeto com o método `salvar` mockado via Vitest. Ela existe
 * para isolar a renderização visual e as interações acessíveis de chamadas externas.
 */
function criarClienteSucesso(): ClienteDadosPessoais {
  return { salvar: vi.fn().mockResolvedValue(undefined) };
}

describe("FormularioDadosPessoais — Testes de Acessibilidade (a11y)", () => {
  it("garante que todos os campos de entrada possuem rótulos acessíveis associados", () => {
    /**
     * O que faz: Verifica se todos os inputs do formulário têm nomes acessíveis (labels).
     * Como faz: Consulta cada controle pelo papel 'textbox' e nome acessível via RegExp.
     * Qual finalidade atende: Assegura que leitores de tela identifiquem corretamente
     * cada campo de entrada conforme exigido pelas diretrizes WCAG e pelo AGENTS.md.
     */
    render(<FormularioDadosPessoais cliente={criarClienteSucesso()} />);

    const campoNome = screen.getByRole("textbox", { name: /nome completo/i });
    const campoEndereco = screen.getByRole("textbox", {
      name: /endereço completo/i,
    });
    const campoTelefone = screen.getByRole("textbox", { name: /telefone 1/i });
    const campoEmail = screen.getByRole("textbox", { name: /e-mail/i });
    const campoLinkedIn = screen.getByRole("textbox", { name: /linkedin/i });
    const campoLattes = screen.getByRole("textbox", {
      name: /currículo lattes/i,
    });
    const botaoAdicionarTelefone = screen.getByRole("button", {
      name: /\+ adicionar telefone/i,
    });
    const botaoSalvar = screen.getByRole("button", {
      name: /salvar dados pessoais/i,
    });

    expect(campoNome).toBeInTheDocument();
    expect(campoEndereco).toBeInTheDocument();
    expect(campoTelefone).toBeInTheDocument();
    expect(campoEmail).toBeInTheDocument();
    expect(campoLinkedIn).toBeInTheDocument();
    expect(campoLattes).toBeInTheDocument();
    expect(botaoAdicionarTelefone).toBeInTheDocument();
    expect(botaoSalvar).toBeInTheDocument();
  });

  it("garante ordem de foco sequencial e previsível via navegação por teclado (Tab)", async () => {
    /**
     * O que faz: Testa a ordem de tabulação do formulário usando a tecla Tab.
     * Como faz: Dispara eventos sequenciais de tabulação com userEvent.tab() e confere
     * se o elemento ativo corresponde à ordem lógica de leitura e preenchimento.
     * Qual finalidade atende: Valida o requisito CRITICAL de navegabilidade por teclado
     * para usuários que não utilizam mouse.
     */
    const usuario = userEvent.setup();
    render(<FormularioDadosPessoais cliente={criarClienteSucesso()} />);

    const campoNome = screen.getByRole("textbox", { name: /nome completo/i });
    const campoEndereco = screen.getByRole("textbox", {
      name: /endereço completo/i,
    });
    const campoTelefone = screen.getByRole("textbox", { name: /telefone 1/i });
    const botaoAdicionarTelefone = screen.getByRole("button", {
      name: /\+ adicionar telefone/i,
    });
    const campoEmail = screen.getByRole("textbox", { name: /e-mail/i });
    const campoLinkedIn = screen.getByRole("textbox", { name: /linkedin/i });
    const campoLattes = screen.getByRole("textbox", {
      name: /currículo lattes/i,
    });
    const botaoSalvar = screen.getByRole("button", {
      name: /salvar dados pessoais/i,
    });

    // Inicia a tabulação a partir do topo do documento
    await usuario.tab();
    expect(campoNome).toHaveFocus();

    await usuario.tab();
    expect(campoEndereco).toHaveFocus();

    await usuario.tab();
    expect(campoTelefone).toHaveFocus();

    await usuario.tab();
    expect(botaoAdicionarTelefone).toHaveFocus();

    await usuario.tab();
    expect(campoEmail).toHaveFocus();

    await usuario.tab();
    expect(campoLinkedIn).toHaveFocus();

    await usuario.tab();
    expect(campoLattes).toHaveFocus();

    await usuario.tab();
    expect(botaoSalvar).toHaveFocus();
  });

  it("associa mensagens de erro aos respectivos campos via aria-invalid e aria-describedby", async () => {
    /**
     * O que faz: Verifica se erros de validação são vinculados aos campos por atributos ARIA.
     * Como faz: Submete o formulário em branco, captura os campos com erro e afere se possuem
     * aria-invalid="true" e aria-describedby apontando para o elemento de mensagem de erro.
     * Qual finalidade atende: Permite que tecnologias assistivas leiam a mensagem de erro
     * imediatamente quando o usuário focaliza o campo inválido.
     */
    const usuario = userEvent.setup();
    render(<FormularioDadosPessoais cliente={criarClienteSucesso()} />);

    // Tenta salvar com campos obrigatórios vazios para forçar a exibição de erros
    await usuario.click(
      screen.getByRole("button", { name: /salvar dados pessoais/i }),
    );

    const campoNome = screen.getByRole("textbox", { name: /nome completo/i });
    const campoEndereco = screen.getByRole("textbox", {
      name: /endereço completo/i,
    });
    const campoTelefone = screen.getByRole("textbox", { name: /telefone 1/i });
    const campoEmail = screen.getByRole("textbox", { name: /e-mail/i });

    // Todos os campos obrigatórios vazios devem indicar estado inválido
    expect(campoNome).toHaveAttribute("aria-invalid", "true");
    expect(campoEndereco).toHaveAttribute("aria-invalid", "true");
    expect(campoTelefone).toHaveAttribute("aria-invalid", "true");
    expect(campoEmail).toHaveAttribute("aria-invalid", "true");

    // Os atributos aria-describedby devem apontar para IDs válidos no DOM
    const idErroNome = campoNome.getAttribute("aria-describedby");
    const idErroEndereco = campoEndereco.getAttribute("aria-describedby");
    const idErroTelefone = campoTelefone.getAttribute("aria-describedby");
    const idErroEmail = campoEmail.getAttribute("aria-describedby");

    expect(idErroNome).toBeTruthy();
    expect(idErroEndereco).toBeTruthy();
    expect(idErroTelefone).toBeTruthy();
    expect(idErroEmail).toBeTruthy();

    // As mensagens de erro referenciadas devem existir e conter texto explicativo
    expect(document.getElementById(idErroNome!)).toHaveTextContent(/nome/i);
    expect(document.getElementById(idErroEndereco!)).toHaveTextContent(
      /endereço/i,
    );
    expect(document.getElementById(idErroTelefone!)).toHaveTextContent(
      /telefone/i,
    );
    expect(document.getElementById(idErroEmail!)).toHaveTextContent(/e-mail/i);
  });

  it("remove aria-invalid e aria-describedby quando o campo com erro é corrigido", async () => {
    /**
     * O que faz: Confirma que o estado de erro é limpo quando o estudante digita no campo.
     * Como faz: Força o erro, digita um valor no campo 'Nome completo' e checa a remoção
     * de aria-invalid e aria-describedby.
     * Qual finalidade atende: Evita que tecnologias assistivas continuem informando erro
     * após a correção pelo usuário.
     */
    const usuario = userEvent.setup();
    render(<FormularioDadosPessoais cliente={criarClienteSucesso()} />);

    await usuario.click(
      screen.getByRole("button", { name: /salvar dados pessoais/i }),
    );

    const campoNome = screen.getByRole("textbox", { name: /nome completo/i });
    expect(campoNome).toHaveAttribute("aria-invalid", "true");

    // Ao digitar um nome válido, o erro daquele campo deve sumir
    await usuario.type(campoNome, "Maria Souza");

    expect(campoNome).not.toHaveAttribute("aria-invalid");
    expect(campoNome).not.toHaveAttribute("aria-describedby");
    expect(document.getElementById("nome-completo-erro")).toBeNull();
  });

  it("comunica mensagens globais de retorno com roles acessíveis de status e alerta", async () => {
    /**
     * O que faz: Verifica os papéis ARIA das mensagens globais de feedback do formulário.
     * Como faz: Testa cenário de sucesso (espera role='status') e cenário de falha (espera role='alert').
     * Qual finalidade atende: Garante que o resultado da operação seja anunciado como
     * live region acessível para leitores de tela.
     */
    const usuario = userEvent.setup();
    const clienteFalha: ClienteDadosPessoais = {
      salvar: vi.fn().mockRejectedValue(new FalhaDadosPessoais("indisponivel")),
    };

    const { rerender } = render(
      <FormularioDadosPessoais cliente={criarClienteSucesso()} />,
    );

    // Preenche dados válidos e envia para gerar sucesso
    await usuario.type(
      screen.getByRole("textbox", { name: /nome completo/i }),
      "Carlos Silva",
    );
    await usuario.type(
      screen.getByRole("textbox", { name: /endereço completo/i }),
      "Rua A, 100",
    );
    await usuario.type(
      screen.getByRole("textbox", { name: /telefone 1/i }),
      "(11) 97777-0000",
    );
    await usuario.type(
      screen.getByRole("textbox", { name: /e-mail/i }),
      "carlos@fatec.sp.gov.br",
    );
    await usuario.click(
      screen.getByRole("button", { name: /salvar dados pessoais/i }),
    );

    const mensagemSucesso = await screen.findByRole("status");
    expect(mensagemSucesso).toHaveTextContent(/salvos com sucesso/i);

    // Agora renderiza formulário que falha na submissão
    rerender(<FormularioDadosPessoais cliente={clienteFalha} />);
    await usuario.click(
      screen.getByRole("button", { name: /salvar dados pessoais/i }),
    );

    const mensagemAlerta = await screen.findByRole("alert");
    expect(mensagemAlerta).toHaveTextContent(/não foi possível salvar/i);
  });
});
