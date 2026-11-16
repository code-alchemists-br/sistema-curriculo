import { cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import { PaginaMeuPerfil, type PaginaMeuPerfilProps } from "./PaginaMeuPerfil";

afterEach(cleanup);

const PREVIA: PreviaCurriculo = {
  curriculo_id: "c1",
  titulo_versao: "Currículo de Ana Souza",
  layout: "moderno",
  estudante: {
    nome: "Ana Souza",
    email: "ana@example.com",
    contato: {
      endereco: "São Paulo, SP",
      telefones: ["(11) 91234-5678"],
      linkedin: null,
      curriculo_lattes: null,
    },
  },
  formacoes: [
    {
      id: "f1",
      instituicao: "Fatec",
      curso: "ADS",
      nivel: "Tecnólogo",
      status: "Em andamento",
      inicio: "2024-02-01",
      fim: null,
    },
  ],
  experiencias: [],
  projetos: [],
  competencias: [{ id: "c1", descricao: "Python", nivel: "Técnica" }],
  idiomas: [],
  documentos: [],
};

/** Renderiza a página com callbacks espiões e as props informadas. */
function renderizar(props: Partial<PaginaMeuPerfilProps> = {}) {
  const callbacks = {
    onEditarPerfil: vi.fn(),
    onEditarCurriculo: vi.fn(),
    onVoltarInicio: vi.fn(),
    aoBaixarCurriculo: vi.fn(async () => {}),
  };
  render(
    <PaginaMeuPerfil
      modelo="moderno"
      possuiCurriculo
      previa={PREVIA}
      {...callbacks}
      {...props}
    />,
  );
  return callbacks;
}

describe("PaginaMeuPerfil", () => {
  it("mostra os dados do perfil, o resumo e o currículo no modelo escolhido", () => {
    renderizar();

    expect(
      screen.getByRole("heading", { name: "Meu perfil", level: 1 }),
    ).toBeInTheDocument();
    const cartao = within(
      screen.getByRole("complementary", { name: "Ana Souza" }),
    );
    expect(cartao.getByText("(11) 91234-5678")).toBeInTheDocument();
    expect(cartao.queryByText("LinkedIn")).not.toBeInTheDocument();
    expect(cartao.getByText("Moderno")).toBeInTheDocument();
    expect(
      screen.getByRole("region", { name: "Currículo atual" }),
    ).toBeInTheDocument();
  });

  it("leva para editar o perfil e o currículo", async () => {
    const callbacks = renderizar();

    await userEvent.click(
      screen.getByRole("button", { name: "Editar perfil" }),
    );
    await userEvent.click(
      screen.getByRole("button", { name: "Editar currículo" }),
    );

    expect(callbacks.onEditarPerfil).toHaveBeenCalledTimes(1);
    expect(callbacks.onEditarCurriculo).toHaveBeenCalledTimes(1);
  });

  it("baixa o currículo no formato escolhido no menu", async () => {
    const callbacks = renderizar();
    const baixar = screen.getByRole("button", { name: /Baixar currículo/ });

    await userEvent.click(baixar);
    expect(baixar).toHaveAttribute("aria-expanded", "true");
    await userEvent.click(screen.getByRole("menuitem", { name: /Word/ }));
    await userEvent.click(baixar);
    await userEvent.click(screen.getByRole("menuitem", { name: /PDF/ }));

    expect(
      callbacks.aoBaixarCurriculo.mock.calls.map(([formato]) => formato),
    ).toEqual(["docx", "pdf"]);
    expect(callbacks.aoBaixarCurriculo.mock.calls[0][1]).toBeInstanceOf(
      HTMLElement,
    );
  });

  it("fecha o menu com Esc e avisa quando a geração do arquivo falha", async () => {
    renderizar({
      aoBaixarCurriculo: vi.fn(async () => Promise.reject(new Error("falhou"))),
    });
    const baixar = screen.getByRole("button", { name: /Baixar currículo/ });

    await userEvent.click(baixar);
    await userEvent.keyboard("{Escape}");
    expect(screen.queryByRole("menu")).not.toBeInTheDocument();

    await userEvent.click(baixar);
    await userEvent.click(screen.getByRole("menuitem", { name: /PDF/ }));
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Não foi possível gerar o arquivo PDF.",
    );
  });

  it("sem currículo convida a criar e não oferece download", async () => {
    const callbacks = renderizar({ possuiCurriculo: false });

    expect(
      screen.queryByRole("button", { name: /Baixar currículo/ }),
    ).not.toBeInTheDocument();
    await userEvent.click(
      screen.getAllByRole("button", { name: "Criar currículo" })[0],
    );
    expect(callbacks.onEditarCurriculo).toHaveBeenCalledTimes(1);
  });
});
