import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { EstadoVazioSecao } from "./EstadoVazioSecao";

afterEach(cleanup);

describe("EstadoVazioSecao", () => {
  it("renderiza a mensagem padrão baseada no título da seção", () => {
    render(<EstadoVazioSecao titulo="Formação acadêmica" />);

    expect(
      screen.getByText(
        "Nenhum item selecionado ou cadastrado para formação acadêmica.",
      ),
    ).toBeInTheDocument();
  });

  it("renderiza mensagem customizada quando fornecida", () => {
    render(
      <EstadoVazioSecao
        mensagem="Você ainda não adicionou nenhuma experiência a este currículo."
        titulo="Experiência profissional"
      />,
    );

    expect(
      screen.getByText(
        "Você ainda não adicionou nenhuma experiência a este currículo.",
      ),
    ).toBeInTheDocument();
  });

  it("possui atributos de acessibilidade semânticos (role=status e aria-label)", () => {
    render(<EstadoVazioSecao titulo="Competências" />);

    const container = screen.getByRole("status");
    expect(container).toBeInTheDocument();
    expect(container).toHaveAttribute(
      "aria-label",
      "Seção Competências sem itens",
    );
  });

  it("renderiza botão de ação e dispara callback ao ser clicado", async () => {
    const handleAcao = vi.fn();
    const user = userEvent.setup();

    render(
      <EstadoVazioSecao
        onAcao={handleAcao}
        textoAcao="Adicionar curso"
        titulo="Cursos"
      />,
    );

    const botao = screen.getByRole("button", { name: "Adicionar curso" });
    expect(botao).toBeInTheDocument();

    await user.click(botao);
    expect(handleAcao).toHaveBeenCalledTimes(1);
  });

  it("utiliza rótulo padrão no botão quando textoAcao não for informado", () => {
    render(
      <EstadoVazioSecao
        onAcao={() => undefined}
        titulo="Projetos acadêmicos"
      />,
    );

    expect(
      screen.getByRole("button", { name: "Adicionar projetos acadêmicos" }),
    ).toBeInTheDocument();
  });

  it("não renderiza botão quando onAcao não for informado", () => {
    render(<EstadoVazioSecao titulo="Idiomas" />);

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("renderiza children customizados quando fornecidos", () => {
    render(
      <EstadoVazioSecao titulo="Documentos complementares">
        <span data-testid="conteudo-extra">Orientação adicional</span>
      </EstadoVazioSecao>,
    );

    expect(screen.getByTestId("conteudo-extra")).toBeInTheDocument();
  });
});
