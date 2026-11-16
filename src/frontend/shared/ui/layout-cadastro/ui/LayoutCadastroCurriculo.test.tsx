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

  it("não exibe a etiqueta de status por padrão em formulário em branco", () => {
    localStorage.clear();
    sessionStorage.clear();
    render(
      <LayoutCadastroCurriculo etapaAtual={1} subtitulo="Dados Pessoais">
        <h1>Conte um pouco sobre você</h1>
      </LayoutCadastroCurriculo>,
    );

    expect(
      screen.queryByLabelText("Status do rascunho"),
    ).not.toBeInTheDocument();
  });

  it("exibe 'Rascunho restaurado' ao iniciar com dados previamente salvos", () => {
    localStorage.setItem(
      "liminal_curriculo_rascunho",
      JSON.stringify({ dadosPessoais: { nomeCompleto: "Carlos Silva" } }),
    );

    render(
      <LayoutCadastroCurriculo etapaAtual={1} subtitulo="Dados Pessoais">
        <h1>Conte um pouco sobre você</h1>
      </LayoutCadastroCurriculo>,
    );

    const status = screen.getByLabelText("Status do rascunho");
    expect(status).toHaveTextContent("Rascunho restaurado");
    localStorage.clear();
  });

  it("exibe 'Rascunho salvo' quando o usuário digita no formulário", () => {
    localStorage.clear();
    sessionStorage.clear();

    render(
      <LayoutCadastroCurriculo etapaAtual={1} subtitulo="Dados Pessoais">
        <h1>Conte um pouco sobre você</h1>
        <input aria-label="Nome" id="campo-teste" />
      </LayoutCadastroCurriculo>,
    );

    expect(
      screen.queryByLabelText("Status do rascunho"),
    ).not.toBeInTheDocument();

    const input = screen.getByLabelText("Nome");
    fireEvent.input(input, { target: { value: "Carlos" } });

    const status = screen.getByLabelText("Status do rascunho");
    expect(status).toHaveTextContent("Rascunho salvo");
  });

  it("permite ocultar a etiqueta de status quando exibirStatusSalvo é falso", () => {
    render(
      <LayoutCadastroCurriculo
        etapaAtual={1}
        subtitulo="Dados Pessoais"
        exibirStatusSalvo={false}
        textoStatusSalvo="Rascunho salvo"
      >
        <h1>Conte um pouco sobre você</h1>
      </LayoutCadastroCurriculo>,
    );

    expect(
      screen.queryByLabelText("Status do rascunho"),
    ).not.toBeInTheDocument();
  });

  it("gerencia o foco acessível direcionando-o para o título h1 da etapa", () => {
    const { rerender } = render(
      <LayoutCadastroCurriculo etapaAtual={1} subtitulo="Dados Pessoais">
        <h1>Etapa 1: Dados Pessoais</h1>
      </LayoutCadastroCurriculo>,
    );

    const titulo1 = screen.getByRole("heading", {
      level: 1,
      name: "Etapa 1: Dados Pessoais",
    });
    expect(document.activeElement).toBe(titulo1);

    rerender(
      <LayoutCadastroCurriculo etapaAtual={2} subtitulo="Formação Acadêmica">
        <h1>Etapa 2: Formação Acadêmica</h1>
      </LayoutCadastroCurriculo>,
    );

    const titulo2 = screen.getByRole("heading", {
      level: 1,
      name: "Etapa 2: Formação Acadêmica",
    });
    expect(document.activeElement).toBe(titulo2);
  });
});
