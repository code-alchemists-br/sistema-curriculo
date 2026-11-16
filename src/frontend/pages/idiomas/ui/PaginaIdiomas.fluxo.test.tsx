import { act, cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

afterEach(cleanup);

import { PaginaIdiomas } from "./PaginaIdiomas";

const idioma = { nome: " Inglês ", nivel: "avancado" as const };

describe("cadastro de idiomas pelo Próximo real", () => {
  it("permite pular seção vazia com lista vazia", async () => {
    const onAvancar = vi.fn();
    render(<PaginaIdiomas onAvancar={onAvancar} />);
    await userEvent.click(
      screen.getByRole("button", { name: "Avançar para próxima etapa" }),
    );
    expect(onAvancar).toHaveBeenCalledExactlyOnceWith([]);
  });

  it("bloqueia idioma parcial e associa a mensagem ao nível inválido", async () => {
    const onAvancar = vi.fn();
    render(
      <PaginaIdiomas
        idiomasIniciais={[{ nome: "Inglês", nivel: "" }]}
        onAvancar={onAvancar}
      />,
    );
    await userEvent.click(
      screen.getByRole("button", { name: "Avançar para próxima etapa" }),
    );
    expect(onAvancar).not.toHaveBeenCalled();
    expect(screen.getByLabelText("Nível de proficiência")).toHaveAttribute(
      "aria-invalid",
      "true",
    );
    expect(
      screen.getByLabelText("Nível de proficiência"),
    ).toHaveAccessibleDescription("Selecione o nível de proficiência.");
    expect(screen.getByLabelText("Nível de proficiência")).toHaveFocus();
  });

  it("valida também a segunda entrada e permite corrigi-la", async () => {
    const usuario = userEvent.setup();
    const onAvancar = vi.fn();
    render(
      <PaginaIdiomas
        idiomasIniciais={[idioma, { nome: "Espanhol", nivel: "" }]}
        onAvancar={onAvancar}
      />,
    );
    const proximo = screen.getByRole("button", {
      name: "Avançar para próxima etapa",
    });
    await usuario.click(proximo);
    expect(onAvancar).not.toHaveBeenCalled();
    await usuario.selectOptions(
      screen.getAllByLabelText("Nível de proficiência")[1],
      "basico",
    );
    await usuario.click(proximo);
    expect(onAvancar).toHaveBeenCalledExactlyOnceWith([
      { nome: "Inglês", nivel: "avancado" },
      { nome: "Espanhol", nivel: "basico" },
    ]);
  });

  it("normaliza dados ao avançar e preserva rascunho a cada alteração", async () => {
    const onAvancar = vi.fn();
    const onSalvar = vi.fn();
    render(
      <PaginaIdiomas
        idiomasIniciais={[idioma]}
        onAvancar={onAvancar}
        onSalvar={onSalvar}
      />,
    );
    await userEvent.click(
      screen.getByRole("button", { name: "Avançar para próxima etapa" }),
    );
    expect(onAvancar).toHaveBeenCalledExactlyOnceWith([
      { nome: "Inglês", nivel: "avancado" },
    ]);
    expect(onSalvar).toHaveBeenCalledWith([idioma]);
  });

  it("permite remover e desfazer o último idioma", async () => {
    const usuario = userEvent.setup();
    render(<PaginaIdiomas idiomasIniciais={[idioma]} />);
    await usuario.click(
      screen.getByRole("button", { name: "Remover idioma 1" }),
    );
    expect(screen.queryByLabelText("Idioma")).not.toBeInTheDocument();
    await usuario.click(
      screen.getByRole("button", { name: "Desfazer remoção do idioma" }),
    );
    expect(screen.getByLabelText("Idioma")).toHaveValue(" Inglês ");
  });

  it("bloqueia envio concorrente e edição enquanto a persistência não conclui", async () => {
    let concluir!: () => void;
    const pendente = new Promise<void>((resolve) => {
      concluir = resolve;
    });
    const onAvancar = vi.fn(() => pendente);
    render(<PaginaIdiomas idiomasIniciais={[idioma]} onAvancar={onAvancar} />);
    const proximo = screen.getByRole("button", {
      name: "Avançar para próxima etapa",
    });
    await userEvent.dblClick(proximo);
    expect(onAvancar).toHaveBeenCalledTimes(1);
    expect(proximo).toBeDisabled();
    expect(screen.getByLabelText("Idioma")).toBeDisabled();
    await act(async () => concluir());
    await waitFor(() => expect(proximo).toBeEnabled());
  });

  it("mostra erro de persistência sem perder o idioma e permite nova tentativa", async () => {
    const onAvancar = vi
      .fn()
      .mockRejectedValueOnce(new Error("401"))
      .mockResolvedValueOnce(undefined);
    render(<PaginaIdiomas idiomasIniciais={[idioma]} onAvancar={onAvancar} />);
    const proximo = screen.getByRole("button", {
      name: "Avançar para próxima etapa",
    });
    await userEvent.click(proximo);
    expect(await screen.findByRole("alert")).toHaveTextContent(
      /não foi possível salvar/i,
    );
    expect(screen.getByLabelText("Idioma")).toHaveValue(" Inglês ");
    await userEvent.click(proximo);
    expect(onAvancar).toHaveBeenCalledTimes(2);
    await waitFor(() =>
      expect(screen.queryByRole("alert")).not.toBeInTheDocument(),
    );
  });
});
