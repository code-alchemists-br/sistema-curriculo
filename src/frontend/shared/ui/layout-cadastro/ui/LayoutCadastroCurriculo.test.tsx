import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { LayoutCadastroCurriculo } from "./LayoutCadastroCurriculo";

afterEach(cleanup);

describe("LayoutCadastroCurriculo", () => {
  it("renderiza o subtítulo e a barra de progresso da etapa atual", () => {
    render(
      <LayoutCadastroCurriculo
        etapaAtual={2}
        progressoEtapaAtual={50}
        subtitulo="Formação Acadêmica"
        totalEtapas={9}
      >
        <div>Conteúdo do formulário</div>
      </LayoutCadastroCurriculo>,
    );

    expect(screen.getByText("Formação Acadêmica")).toBeInTheDocument();
    expect(screen.getByText("Conteúdo do formulário")).toBeInTheDocument();
    expect(
      screen.getByRole("progressbar", { name: "Etapa 2 de 9" }),
    ).toBeInTheDocument();
  });

  it("aciona onVoltarInicio ao clicar no botão de voltar ao início", () => {
    const onVoltarInicio = vi.fn();
    render(
      <LayoutCadastroCurriculo
        etapaAtual={9}
        onVoltarInicio={onVoltarInicio}
        subtitulo="Validação e Revisão"
      >
        <div>Etapa Final</div>
      </LayoutCadastroCurriculo>,
    );

    const btnVoltarInicio = screen.getByRole("button", {
      name: "Voltar para a página inicial",
    });
    fireEvent.click(btnVoltarInicio);
    expect(onVoltarInicio).toHaveBeenCalledTimes(1);
  });

  it("redefine o scroll do contêiner de conteúdo ao alterar de etapa", () => {
    const { rerender } = render(
      <LayoutCadastroCurriculo etapaAtual={1} subtitulo="Dados Pessoais">
        <div>Etapa 1</div>
      </LayoutCadastroCurriculo>,
    );

    const main = screen.getByRole("main");
    main.scrollTop = 450;

    rerender(
      <LayoutCadastroCurriculo etapaAtual={2} subtitulo="Formação Acadêmica">
        <div>Etapa 2</div>
      </LayoutCadastroCurriculo>,
    );

    expect(main.scrollTop).toBe(0);
  });
});
