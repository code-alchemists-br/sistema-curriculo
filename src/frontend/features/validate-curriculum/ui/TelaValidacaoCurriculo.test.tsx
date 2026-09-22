import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { TelaValidacaoCurriculo } from "./TelaValidacaoCurriculo";
import type { CurriculoParaValidacao } from "../model/validacao-curriculo";

afterEach(() => {
  cleanup();
});

const dadosFicticios: CurriculoParaValidacao = {
  dadosPessoais: {
    nomeCompleto: "Rafael Mendes",
    enderecoCompleto: "Avenida Central, 45",
    telefones: ["11988887777"],
    email: "rafael.mendes@example.com"
  },
  formacaoAcademica: { status: "preenchida" },
  experienciasProfissionais: { status: "preenchida" },
  competencias: {
    hardSkills: ["Python"],
    softSkills: ["Organização"]
  },
  projetosAcademicos: []
};

describe("TelaValidacaoCurriculo", () => {
  it("mantém prévia e PDF bloqueados quando há etapa pulada", () => {
    render(
      <TelaValidacaoCurriculo
        dados={{
          ...dadosFicticios,
          formacaoAcademica: {
            status: "pulada",
            mensagemErro: "A formação acadêmica ainda não foi preenchida."
          }
        }}
      />
    );

    expect(screen.getByText("Formação acadêmica")).toBeInTheDocument();
    expect(screen.getByText(/Pendente/)).toBeInTheDocument();
    expect(screen.getByText("A formação acadêmica ainda não foi preenchida.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Visualizar prévia" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Exportar PDF" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Confirmar currículo" })).toBeDisabled();
  });

  it("libera as ações e chama os doubles quando o currículo está válido", async () => {
    const user = userEvent.setup();
    const onVisualizarPreview = vi.fn();
    const onExportarPdf = vi.fn();
    const onConfirmarCurriculo = vi.fn();

    render(
      <TelaValidacaoCurriculo
        dados={dadosFicticios}
        onVisualizarPreview={onVisualizarPreview}
        onExportarPdf={onExportarPdf}
        onConfirmarCurriculo={onConfirmarCurriculo}
      />
    );

    await user.click(screen.getByRole("button", { name: "Visualizar prévia" }));
    await user.click(screen.getByRole("button", { name: "Exportar PDF" }));
    await user.click(screen.getByRole("button", { name: "Confirmar currículo" }));

    expect(onVisualizarPreview).toHaveBeenCalledTimes(1);
    expect(onExportarPdf).toHaveBeenCalledTimes(1);
    expect(onConfirmarCurriculo).toHaveBeenCalledTimes(1);
  });
});
