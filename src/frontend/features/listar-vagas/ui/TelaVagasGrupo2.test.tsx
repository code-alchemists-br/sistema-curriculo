import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { SugestaoVaga } from "../../../entities/vaga";
import {
  FalhaVagasGrupo2,
  type ClienteVagasGrupo2,
} from "../api/cliente-vagas-grupo2";
import { TelaVagasGrupo2 } from "./TelaVagasGrupo2";

afterEach(cleanup);

const sugestao: SugestaoVaga = {
  curriculoId: "curriculo-001",
  vaga: {
    id: "vaga-001",
    titulo: "Estágio em Desenvolvimento",
    empresa: "Empresa Exemplo",
    descricao: "Desenvolvimento de aplicações web.",
    requisitos: ["TypeScript", "React"],
    localizacao: "São Paulo - SP",
    modalidade: "Híbrido",
    urlCandidatura: "https://grupo2.exemplo.com/vagas/001",
  },
};

describe("TelaVagasGrupo2", () => {
  it(
    "mostra carregamento e apresenta as vagas devolvidas pelo double",
    async () => {
      const cliente: ClienteVagasGrupo2 = {
        listarSugestoes: vi.fn().mockResolvedValue([sugestao]),
      };

      render(<TelaVagasGrupo2 cliente={cliente} />);

      expect(screen.getByRole("status")).toHaveTextContent(
        "Carregando vagas",
      );
      expect(
        await screen.findByRole("heading", { name: sugestao.vaga.titulo }),
      ).toBeInTheDocument();
      expect(screen.getByText("Empresa Exemplo")).toBeInTheDocument();
      expect(
        screen.getByRole("link", { name: "Ver detalhes da vaga" }),
      ).toHaveAttribute("href", sugestao.vaga.urlCandidatura);
    },
  );

  it(
    "apresenta estado vazio quando o double não devolve sugestões",
    async () => {
      const cliente: ClienteVagasGrupo2 = {
        listarSugestoes: vi.fn().mockResolvedValue([]),
      };

      render(<TelaVagasGrupo2 cliente={cliente} />);

      expect(
        await screen.findByRole("heading", {
          name: "Nenhuma vaga encontrada",
        }),
      ).toBeInTheDocument();
    },
  );

  it("mostra erro seguro e permite tentar a consulta novamente", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteVagasGrupo2 = {
      listarSugestoes: vi
        .fn()
        .mockRejectedValueOnce(new FalhaVagasGrupo2("indisponivel"))
        .mockResolvedValueOnce([sugestao]),
    };

    render(<TelaVagasGrupo2 cliente={cliente} />);

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "integração de vagas está indisponível",
    );
    await usuario.click(
      screen.getByRole("button", { name: "Tentar novamente" }),
    );

    expect(
      await screen.findByRole("heading", { name: sugestao.vaga.titulo }),
    ).toBeInTheDocument();
    expect(cliente.listarSugestoes).toHaveBeenCalledTimes(2);
  });
});
