// Proveniência: decision-analysis prompts/frontend/20261009-153000-correcao-acessibilidade-formulario-experiencias-v001.md#v001
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { FormularioExperiencias } from "./FormularioExperiencias";
import type { Experiencia } from "../model/experiencias";

afterEach(cleanup);

const experienciaValida: Experiencia = {
  empresa: "Tech Corp",
  cargo: "Desenvolvedor Frontend",
  inicio: "2023-01",
  fim: "2024-05",
  empregoAtual: false,
  descricao: "Desenvolvimento de interfaces acessíveis.",
};

describe("FormularioExperiencias — Testes de Acessibilidade (a11y)", () => {
  /**
   * Valida a associação de rótulos acessíveis a todos os controles interativos.
   *
   * **O que faz:** Verifica se inputs de texto, mês, checkbox, textarea e botões possuem nomes acessíveis.
   * **Como faz:** Realiza consultas por papel semântico (`textbox`, `checkbox`, `button`) e nomes acessíveis via RegExp.
   * **Qual finalidade atende:** Garante que pessoas cegas ou com baixa visão que utilizam leitores de tela compreendam a finalidade de cada campo.
   */
  it("garante que todos os campos de entrada e botões possuem rótulos acessíveis associados", () => {
    render(<FormularioExperiencias />);

    const campoEmpresa = screen.getByRole("textbox", {
      name: /nome da empresa/i,
    });
    const campoCargo = screen.getByRole("textbox", { name: /cargo/i });
    const campoInicio = screen.getByLabelText(/início \(mês\/ano\)/i);
    const campoFim = screen.getByLabelText(/fim \(mês\/ano\)/i);
    const checkboxEmpregoAtual = screen.getByRole("checkbox", {
      name: /emprego atual/i,
    });
    const campoDescricao = screen.getByRole("textbox", {
      name: /descrição das atividades/i,
    });
    const botaoAdicionar = screen.getByRole("button", {
      name: /\+ adicionar experiência/i,
    });
    const botaoSalvar = screen.getByRole("button", {
      name: /salvar experiências/i,
    });

    expect(campoEmpresa).toBeInTheDocument();
    expect(campoCargo).toBeInTheDocument();
    expect(campoInicio).toBeInTheDocument();
    expect(campoFim).toBeInTheDocument();
    expect(checkboxEmpregoAtual).toBeInTheDocument();
    expect(campoDescricao).toBeInTheDocument();
    expect(botaoAdicionar).toBeInTheDocument();
    expect(botaoSalvar).toBeInTheDocument();
  });

  /**
   * Valida a navegação sequencial por teclado através da tecla Tab.
   *
   * **O que faz:** Avalia se o foco navega por todos os campos de forma lógica e sem armadilhas de teclado.
   * **Como faz:** Executa eventos sequenciais de tabulação com `userEvent.tab()` e afere o elemento ativo no documento.
   * **Qual finalidade atende:** Atende ao critério CRITICAL de acessibilidade motora para quem navega exclusivamente pelo teclado.
   */
  it("garante ordem de foco sequencial e previsível via teclado (Tab)", async () => {
    const usuario = userEvent.setup();
    render(<FormularioExperiencias />);

    const campoEmpresa = screen.getByRole("textbox", {
      name: /nome da empresa/i,
    });
    const campoCargo = screen.getByRole("textbox", { name: /cargo/i });
    const campoInicio = screen.getByLabelText(/início \(mês\/ano\)/i);
    const campoFim = screen.getByLabelText(/fim \(mês\/ano\)/i);
    const checkboxEmpregoAtual = screen.getByRole("checkbox", {
      name: /emprego atual/i,
    });
    const campoDescricao = screen.getByRole("textbox", {
      name: /descrição das atividades/i,
    });
    const botaoAdicionar = screen.getByRole("button", {
      name: /\+ adicionar experiência/i,
    });
    const botaoSalvar = screen.getByRole("button", {
      name: /salvar experiências/i,
    });

    await usuario.tab();
    expect(campoEmpresa).toHaveFocus();

    await usuario.tab();
    expect(campoCargo).toHaveFocus();

    await usuario.tab();
    expect(campoInicio).toHaveFocus();

    await usuario.tab();
    expect(campoFim).toHaveFocus();

    await usuario.tab();
    expect(checkboxEmpregoAtual).toHaveFocus();

    await usuario.tab();
    expect(campoDescricao).toHaveFocus();

    await usuario.tab();
    expect(botaoAdicionar).toHaveFocus();

    await usuario.tab();
    expect(botaoSalvar).toHaveFocus();
  });

  /**
   * Valida a vinculação programática de mensagens de erro aos respectivos campos.
   *
   * **O que faz:** Confirma que campos com falha de validação apresentam `aria-invalid="true"` e `aria-describedby`.
   * **Como faz:** Submete o formulário vazio, consulta os atributos ARIA e verifica se o ID referenciado existe no DOM.
   * **Qual finalidade atende:** Assegura que o leitor de tela verbalize imediatamente a razão da inconsistência ao focalizar o campo inválido.
   */
  it("associa mensagens de erro aos respectivos campos via aria-invalid e aria-describedby", async () => {
    const usuario = userEvent.setup();
    render(<FormularioExperiencias />);

    await usuario.click(
      screen.getByRole("button", { name: /salvar experiências/i }),
    );

    const campoEmpresa = screen.getByRole("textbox", {
      name: /nome da empresa/i,
    });
    const campoCargo = screen.getByRole("textbox", { name: /cargo/i });
    const campoInicio = screen.getByLabelText(/início \(mês\/ano\)/i);

    expect(campoEmpresa).toHaveAttribute("aria-invalid", "true");
    expect(campoCargo).toHaveAttribute("aria-invalid", "true");
    expect(campoInicio).toHaveAttribute("aria-invalid", "true");

    const idDescritoEmpresa = campoEmpresa.getAttribute("aria-describedby");
    expect(idDescritoEmpresa).toBeTruthy();
    const elementoErroEmpresa = document.getElementById(idDescritoEmpresa!);
    expect(elementoErroEmpresa).toHaveTextContent("Informe o nome da empresa.");

    const idDescritoCargo = campoCargo.getAttribute("aria-describedby");
    expect(idDescritoCargo).toBeTruthy();
    const elementoErroCargo = document.getElementById(idDescritoCargo!);
    expect(elementoErroCargo).toHaveTextContent("Informe o cargo exercido.");

    const idDescritoInicio = campoInicio.getAttribute("aria-describedby");
    expect(idDescritoInicio).toBeTruthy();
    const elementoErroInicio = document.getElementById(idDescritoInicio!);
    expect(elementoErroInicio).toHaveTextContent("Informe a data de início.");
  });

  /**
   * Valida a comunicação assertiva de erro global e cortês de sucesso.
   *
   * **O que faz:** Verifica se a mensagem de retorno utiliza `role="alert"` em caso de erro e `role="status"` em caso de sucesso.
   * **Como faz:** Submete o formulário com dados inválidos para verificar o alerta, e em seguida com dados válidos para verificar o status.
   * **Qual finalidade atende:** Garante conformidade com WCAG 4.1.3 (Status Messages) e 3.3.1 (Error Identification), orientando o usuário de tecnologia assistiva.
   */
  it("comunica mensagens globais com roles acessíveis de alert no erro e status no sucesso", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi.fn();
    render(<FormularioExperiencias onSalvar={onSalvar} />);

    // 1. Submissão inválida: deve anunciar alert assertivo
    await usuario.click(
      screen.getByRole("button", { name: /salvar experiências/i }),
    );

    const alertaErro = await screen.findByRole("alert");
    expect(alertaErro).toHaveTextContent(
      "Há pendências que precisam ser corrigidas antes de salvar.",
    );
    expect(onSalvar).not.toHaveBeenCalled();

    // 2. Preenchimento válido: deve anunciar status de confirmação
    await usuario.type(
      screen.getByRole("textbox", { name: /nome da empresa/i }),
      "Tech Corp",
    );
    await usuario.type(
      screen.getByRole("textbox", { name: /cargo/i }),
      "Desenvolvedor",
    );
    await usuario.type(
      screen.getByLabelText(/início \(mês\/ano\)/i),
      "2023-01",
    );
    await usuario.type(screen.getByLabelText(/fim \(mês\/ano\)/i), "2024-05");

    await usuario.click(
      screen.getByRole("button", { name: /salvar experiências/i }),
    );

    const statusSucesso = await screen.findByRole("status");
    expect(statusSucesso).toHaveTextContent("Experiências salvas com sucesso.");
    expect(onSalvar).toHaveBeenCalledTimes(1);
  });

  /**
   * Valida a desabilitação e reabilitação acessível do campo de data de término.
   *
   * **O que faz:** Confirma que o campo de data de fim é desabilitado quando "Emprego atual" é selecionado e reabilitado ao desmarcar.
   * **Como faz:** Alterna o estado do checkbox via clique do usuário e verifica a propriedade `toBeDisabled()`.
   * **Qual finalidade atende:** Assegura que o leitor de tela informe o estado desabilitado de campos condicionalmente irrelevantes.
   */
  it("controla o estado acessível de desabilitação do campo Fim ao alternar Emprego atual", async () => {
    const usuario = userEvent.setup();
    render(<FormularioExperiencias />);

    const checkbox = screen.getByRole("checkbox", { name: /emprego atual/i });
    const campoFim = screen.getByLabelText(/fim \(mês\/ano\)/i);

    expect(campoFim).toBeEnabled();

    await usuario.click(checkbox);
    expect(campoFim).toBeDisabled();

    await usuario.click(checkbox);
    expect(campoFim).toBeEnabled();
  });

  /**
   * Valida a estrutura semântica de grupos quando múltiplas experiências são adicionadas.
   *
   * **O que faz:** Verifica que cada experiência adicionada é agrupada em um fieldset rotulado e possui botão de remoção acessível.
   * **Como faz:** Adiciona uma segunda experiência e consulta os elementos agrupados por rótulo acessível (`Experiência 1`, `Experiência 2`).
   * **Qual finalidade atende:** Permite que tecnologias assistivas anunciem a entrada e saída de blocos lógicos estruturados.
   */
  it("agrupa múltiplas experiências em fieldsets com rótulos e botões de remoção acessíveis", async () => {
    const usuario = userEvent.setup();
    render(
      <FormularioExperiencias
        experienciasIniciais={[
          experienciaValida,
          { ...experienciaValida, empresa: "Segunda Empresa" },
        ]}
      />,
    );

    const grupo1 = screen.getByRole("group", { name: "Experiência 1" });
    const grupo2 = screen.getByRole("group", { name: "Experiência 2" });

    expect(grupo1).toBeInTheDocument();
    expect(grupo2).toBeInTheDocument();

    const botaoRemover1 = screen.getByRole("button", {
      name: "Remover experiência 1",
    });
    const botaoRemover2 = screen.getByRole("button", {
      name: "Remover experiência 2",
    });

    expect(botaoRemover1).toBeInTheDocument();
    expect(botaoRemover2).toBeInTheDocument();

    await usuario.click(botaoRemover2);
    expect(
      screen.queryByRole("group", { name: "Experiência 2" }),
    ).not.toBeInTheDocument();
  });
});
