import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

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
