// Proveniência: decision-analysis prompts/frontend/20261012-095000-roteiro-teclado-dialogo-retorno-foco-v001.md#v001
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { ModalConfirmacao } from "./ModalConfirmacao";

afterEach(cleanup);

/**
 * Componente hospedeiro de teste que simula o fluxo completo de abertura e fechamento de diálogo.
 *
 * **O que faz:** Renderiza um botão disparador externo que alterna a visibilidade do `ModalConfirmacao`.
 * **Como faz:** Mantém o estado `aberto` local e passa callbacks de confirmação e cancelamento ao modal.
 * **Qual finalidade atende:** Permite verificar a captura e a restauração real de foco no elemento disparador.
 */
function HospedeiroModalTeste({
  aoConfirmar = vi.fn(),
}: {
  aoConfirmar?: () => void;
}) {
  const [aberto, setAberto] = useState(false);

  return (
    <div>
      <button
        id="btn-disparador-exclusao"
        onClick={() => setAberto(true)}
        type="button"
      >
        Disparar Diálogo
      </button>
      <ModalConfirmacao
        aberto={aberto}
        descricao="Esta operação não pode ser revertida após confirmação."
        onCancelar={() => setAberto(false)}
        onConfirmar={() => {
          aoConfirmar();
          setAberto(false);
        }}
        titulo="Confirmar exclusão de item"
      />
    </div>
  );
}

describe("ModalConfirmacao — Roteiro de Operação por Teclado e Retorno de Foco", () => {
  /**
   * Valida a captura inicial de foco no botão de cancelamento ao abrir o diálogo.
   *
   * **O que faz:** Verifica se o foco é transferido imediatamente para dentro do modal ao ser renderizado.
   * **Como faz:** Renderiza o modal com `aberto={true}` e afere que `getByRole("button", { name: "Cancelar" })` possui o foco ativo.
   * **Qual finalidade atende:** Satisfaz o critério WCAG 2.4.3 (Ordem do Foco), garantindo que o usuário de teclado não perca o contexto.
   */
  it("transfere o foco inicial imediatamente para o botão de cancelamento ao abrir", () => {
    render(
      <ModalConfirmacao
        aberto={true}
        descricao="Deseja prosseguir?"
        onCancelar={vi.fn()}
        onConfirmar={vi.fn()}
        titulo="Título de teste"
      />,
    );

    const botaoCancelar = screen.getByRole("button", { name: "Cancelar" });
    expect(botaoCancelar).toHaveFocus();
  });

  /**
   * Valida o fechamento acessível via tecla Escape.
   *
   * **O que faz:** Confirma que pressionar a tecla Escape emite o evento de cancelamento do diálogo.
   * **Como faz:** Dispara evento `Escape` via `userEvent.keyboard` e afere a invocação do callback `onCancelar`.
   * **Qual finalidade atende:** Cumpre o padrão WAI-ARIA Modal Dialog Pattern e WCAG 2.1.2 para cancelamento rápido por teclado.
   */
  it("fecha o diálogo ao pressionar a tecla Escape e aciona onCancelar", async () => {
    const usuario = userEvent.setup();
    const aoCancelar = vi.fn();

    render(
      <ModalConfirmacao
        aberto={true}
        descricao="Deseja prosseguir?"
        onCancelar={aoCancelar}
        onConfirmar={vi.fn()}
        titulo="Título de teste"
      />,
    );

    await usuario.keyboard("{Escape}");
    expect(aoCancelar).toHaveBeenCalledTimes(1);
  });

  /**
   * Valida a contenção de foco (focus trap) para manter o foco restrito aos botões do modal.
   *
   * **O que faz:** Garante que a navegação por Tab e Shift+Tab cicla entre os botões internos do modal.
   * **Como faz:** Foca no botão Confirmar e dispara Tab (conferindo retorno ao Cancelar); e foca no Cancelar disparando Shift+Tab (conferindo salto ao Confirmar).
   * **Qual finalidade atende:** Satisfaz o critério WCAG 2.1.2 (Sem Armadilha de Teclado fora do modal / Focus Trap).
   */
  it("contém o foco ciclando entre os botões internos via Tab e Shift+Tab (focus trap)", () => {
    render(
      <ModalConfirmacao
        aberto={true}
        descricao="Deseja prosseguir?"
        onCancelar={vi.fn()}
        onConfirmar={vi.fn()}
        titulo="Título de teste"
      />,
    );

    const botaoCancelar = screen.getByRole("button", { name: "Cancelar" });
    const botaoConfirmar = screen.getByRole("button", { name: "Confirmar" });

    botaoConfirmar.focus();
    expect(botaoConfirmar).toHaveFocus();

    fireEvent.keyDown(document, { key: "Tab" });
    expect(botaoCancelar).toHaveFocus();

    fireEvent.keyDown(document, { key: "Tab", shiftKey: true });
    expect(botaoConfirmar).toHaveFocus();
  });

  /**
   * Valida o retorno de foco ao elemento disparador original após fechamento via Escape.
   *
   * **O que faz:** Confirma que o foco retorna exatamente para o botão que abriu o diálogo quando este fecha via Escape.
   * **Como faz:** Clica no botão disparador com `userEvent`, fecha o modal com Escape e afere `expect(botaoDisparador).toHaveFocus()`.
   * **Qual finalidade atende:** Garante o cumprimento estrito do critério WCAG 2.4.3 (Ordem do Foco) e da issue #396.
   */
  it("restaura o foco no elemento disparador original quando fechado via tecla Escape", async () => {
    const usuario = userEvent.setup();
    render(<HospedeiroModalTeste />);

    const botaoDisparador = screen.getByRole("button", {
      name: "Disparar Diálogo",
    });

    await usuario.click(botaoDisparador);

    const botaoCancelar = screen.getByRole("button", { name: "Cancelar" });
    expect(botaoCancelar).toHaveFocus();

    await usuario.keyboard("{Escape}");

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(botaoDisparador).toHaveFocus();
  });

  /**
   * Valida o retorno de foco ao disparador original após fechamento via clique no botão Cancelar.
   *
   * **O que faz:** Confirma a restauração de foco no disparador após ação de cancelamento com o botão.
   * **Como faz:** Abre o diálogo a partir do disparador, clica em Cancelar e afere que o disparador recupera o foco.
   * **Qual finalidade atende:** Assegura continuidade de navegação por teclado para usuários de leitores de tela e teclado.
   */
  it("restaura o foco no disparador original quando fechado pelo botão Cancelar", async () => {
    const usuario = userEvent.setup();
    render(<HospedeiroModalTeste />);

    const botaoDisparador = screen.getByRole("button", {
      name: "Disparar Diálogo",
    });

    await usuario.click(botaoDisparador);

    const botaoCancelar = screen.getByRole("button", { name: "Cancelar" });
    await usuario.click(botaoCancelar);

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(botaoDisparador).toHaveFocus();
  });

  /**
   * Valida o retorno de foco ao disparador original após confirmação da ação.
   *
   * **O que faz:** Confirma que a confirmação da operação também restaura o foco no botão de origem.
   * **Como faz:** Abre o diálogo, aciona o botão Confirmar e valida a chamada da ação e o foco ativo no disparador.
   * **Qual finalidade atende:** Garante consistência de foco em todos os caminhos de saída do diálogo modal.
   */
  it("restaura o foco no disparador original quando a ação é confirmada", async () => {
    const usuario = userEvent.setup();
    const aoConfirmar = vi.fn();
    render(<HospedeiroModalTeste aoConfirmar={aoConfirmar} />);

    const botaoDisparador = screen.getByRole("button", {
      name: "Disparar Diálogo",
    });

    await usuario.click(botaoDisparador);

    const botaoConfirmar = screen.getByRole("button", { name: "Confirmar" });
    await usuario.click(botaoConfirmar);

    expect(aoConfirmar).toHaveBeenCalledTimes(1);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(botaoDisparador).toHaveFocus();
  });

  /**
   * Valida a restauração de foco quando o elemento disparador é fornecido explicitamente via props.
   *
   * **O que faz:** Permite que componentes passem uma referência explícita para retorno de foco.
   * **Como faz:** Renderiza com `elementoDisparador`, fecha o modal e verifica se o elemento indicado recebe foco.
   * **Qual finalidade atende:** Suporta casos em que a abertura do modal ocorre fora do evento síncrono de clique direto.
   */
  it("restaura o foco no elementoDisparador fornecido explicitamente nas props", () => {
    const elementoCustomizado = document.createElement("button");
    elementoCustomizado.textContent = "Disparador Externo";
    document.body.appendChild(elementoCustomizado);

    const { rerender } = render(
      <ModalConfirmacao
        aberto={true}
        descricao="Teste com disparador explícito"
        elementoDisparador={elementoCustomizado}
        onCancelar={vi.fn()}
        onConfirmar={vi.fn()}
        titulo="Confirmação"
      />,
    );

    expect(screen.getByRole("button", { name: "Cancelar" })).toHaveFocus();

    rerender(
      <ModalConfirmacao
        aberto={false}
        descricao="Teste com disparador explícito"
        elementoDisparador={elementoCustomizado}
        onCancelar={vi.fn()}
        onConfirmar={vi.fn()}
        titulo="Confirmação"
      />,
    );

    expect(elementoCustomizado).toHaveFocus();
    document.body.removeChild(elementoCustomizado);
  });
});
