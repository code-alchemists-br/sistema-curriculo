import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { Dialogo } from "./Dialogo";

afterEach(cleanup);

describe("Dialogo — Componente de Diálogo Acessível", () => {
  /**
   * Valida a ausência do diálogo no DOM quando a prop aberto for falsa.
   *
   * **O que faz:** Renderiza o componente com `aberto={false}` e verifica a ausência da role dialog.
   * **Como faz:** Consulta `queryByRole("dialog")` e assegura que retorna nulo.
   * **Qual finalidade atende:** Garante que o diálogo não ocupe espaço visual nem interfira na árvore de acessibilidade quando inativo.
   */
  it("não renderiza nenhum elemento no DOM quando aberto é false", () => {
    render(
      <Dialogo aberto={false} onFechar={vi.fn()} titulo="Diálogo Fechado">
        <p>Conteúdo interno</p>
      </Dialogo>,
    );

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  /**
   * Valida atributos ARIA e renderização semântica do diálogo aberto.
   *
   * **O que faz:** Confirma que o diálogo renderiza com role dialog, aria-modal, aria-labelledby e aria-describedby corretos.
   * **Como faz:** Renderiza com título e descrição e compara os IDs e valores retornados por getByRole e getByText.
   * **Qual finalidade atende:** Assegura conformidade com WCAG 2.1 e tecnologias assistivas para identificação imediata do propósito do modal.
   */
  it("renderiza atributos ARIA e elementos semânticos quando aberto é true", () => {
    render(
      <Dialogo
        aberto={true}
        descricao="Descrição explicativa do modal"
        onFechar={vi.fn()}
        titulo="Título de Exemplo"
      >
        <p>Conteúdo do diálogo</p>
      </Dialogo>,
    );

    const dialog = screen.getByRole("dialog");
    expect(dialog).toBeInTheDocument();
    expect(dialog).toHaveAttribute("aria-modal", "true");

    const titulo = screen.getByRole("heading", { name: "Título de Exemplo" });
    expect(titulo).toBeInTheDocument();
    expect(dialog).toHaveAttribute("aria-labelledby", titulo.id);

    const descricao = screen.getByText("Descrição explicativa do modal");
    expect(descricao).toBeInTheDocument();
    expect(dialog).toHaveAttribute("aria-describedby", descricao.id);

    expect(screen.getByText("Conteúdo do diálogo")).toBeInTheDocument();
  });

  /**
   * Valida acionamento do callback onFechar via botão de fechar.
   *
   * **O que faz:** Clica no botão dedicado de fechar o diálogo e afere se a função onFechar é invocada.
   * **Como faz:** Utiliza userEvent para clicar no botão com aria-label "Fechar diálogo".
   * **Qual finalidade atende:** Oferece mecanismo visual e explícito de encerramento do diálogo.
   */
  it("executa onFechar ao clicar no botão de fechar", async () => {
    const usuario = userEvent.setup();
    const mockFechar = vi.fn();

    render(
      <Dialogo aberto={true} onFechar={mockFechar} titulo="Fechar com Botão" />,
    );

    const botaoFechar = screen.getByRole("button", {
      name: /fechar diálogo/i,
    });
    await usuario.click(botaoFechar);

    expect(mockFechar).toHaveBeenCalledTimes(1);
  });

  /**
   * Valida acionamento do callback onFechar ao pressionar Escape.
   *
   * **O que faz:** Pressiona a tecla Escape e afere se o modal solicita encerramento.
   * **Como faz:** Envia evento de teclado "{Escape}" e verifica se mockFechar foi chamado.
   * **Qual finalidade atende:** Atende ao critério de acessibilidade WCAG para fechamento facilitado por teclado.
   */
  it("executa onFechar ao pressionar a tecla Escape", async () => {
    const usuario = userEvent.setup();
    const mockFechar = vi.fn();

    render(
      <Dialogo
        aberto={true}
        onFechar={mockFechar}
        titulo="Fechar com Teclado"
      />,
    );

    await usuario.keyboard("{Escape}");

    expect(mockFechar).toHaveBeenCalledTimes(1);
  });

  /**
   * Valida acionamento do callback onFechar ao clicar no overlay de fundo.
   *
   * **O que faz:** Testa o encerramento do diálogo por clique na área externa (backdrop overlay).
   * **Como faz:** Dispara evento de clique no container .dialogo-overlay e valida que cliques internos não fecham o diálogo.
   * **Qual finalidade atende:** Garante usabilidade intuitiva para usuários com mouse e dispositivos de toque.
   */
  it("executa onFechar ao clicar no backdrop, mas não ao clicar no conteúdo", async () => {
    const usuario = userEvent.setup();
    const mockFechar = vi.fn();

    const { container } = render(
      <Dialogo aberto={true} onFechar={mockFechar} titulo="Clique Backdrop">
        <button type="button">Ação interna</button>
      </Dialogo>,
    );

    const conteudoInterno = screen.getByRole("dialog");
    await usuario.click(conteudoInterno);
    expect(mockFechar).not.toHaveBeenCalled();

    const backdrop = container.querySelector(".dialogo-overlay");
    expect(backdrop).not.toBeNull();
    if (backdrop) {
      await usuario.click(backdrop);
      expect(mockFechar).toHaveBeenCalledTimes(1);
    }
  });

  /**
   * Valida a restauração de foco no elemento disparador após o fechamento.
   *
   * **O que faz:** Confirma que o foco retorna ao botão disparador quando o modal se fecha.
   * **Como faz:** Monta componente de teste com estado e botão disparador, abre o diálogo e fecha via Escape, verificando document.activeElement.
   * **Qual finalidade atende:** Atende ao Critério de Sucesso 2.4.3 da WCAG (Focus Order), preservando a orientação do usuário no fluxo de navegação.
   */
  it("restaura o foco no elemento disparador após o diálogo ser fechado", async () => {
    const usuario = userEvent.setup();

    function TesteRestauracaoFoco() {
      const [aberto, setAberto] = useState(false);
      return (
        <div>
          <button
            id="botao-disparador"
            onClick={() => setAberto(true)}
            type="button"
          >
            Abrir Modal
          </button>
          <Dialogo
            aberto={aberto}
            onFechar={() => setAberto(false)}
            titulo="Modal com Restauração"
          >
            <button type="button">Confirmar Ação</button>
          </Dialogo>
        </div>
      );
    }

    render(<TesteRestauracaoFoco />);

    const botaoDisparador = screen.getByRole("button", { name: "Abrir Modal" });
    await usuario.click(botaoDisparador);

    const botaoFechar = screen.getByRole("button", { name: /fechar diálogo/i });
    expect(botaoFechar).toHaveFocus();

    await usuario.keyboard("{Escape}");

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(botaoDisparador).toHaveFocus();
  });

  /**
   * Valida a contenção de foco (focus trap) para manter a navegação dentro do modal com Tab e Shift+Tab.
   *
   * **O que faz:** Impede que o foco do teclado escape para o restante da página enquanto o diálogo estiver ativo.
   * **Como faz:** Foca no último elemento e dispara Tab, conferindo se cicla para o primeiro; e foca no primeiro elemento disparando Shift+Tab, conferindo se cicla para o último.
   * **Qual finalidade atende:** Satisfaz o Critério 2.1.2 da WCAG (Sem Armadilha de Teclado fora do modal / Focus Trapping).
   */
  it("contém o foco ciclando entre o primeiro e o último elemento com Tab e Shift+Tab", () => {
    render(
      <Dialogo
        aberto={true}
        onFechar={vi.fn()}
        titulo="Diálogo com Foco Contido"
      >
        <button id="btn-primeira-acao" type="button">
          Ação 1
        </button>
        <button id="btn-ultima-acao" type="button">
          Ação 2
        </button>
      </Dialogo>,
    );

    const botaoFechar = screen.getByRole("button", { name: /fechar diálogo/i });
    const btnAcao2 = screen.getByRole("button", { name: "Ação 2" });

    btnAcao2.focus();
    expect(btnAcao2).toHaveFocus();

    fireEvent.keyDown(document, { key: "Tab" });
    expect(botaoFechar).toHaveFocus();

    fireEvent.keyDown(document, { key: "Tab", shiftKey: true });
    expect(btnAcao2).toHaveFocus();
  });
});
