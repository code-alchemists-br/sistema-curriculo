import { describe, expect, it, vi } from "vitest";

import {
  adaptarRespostaGrupo2,
  criarClienteVagasGrupo2,
  FalhaVagasGrupo2,
} from "./cliente-vagas-grupo2";

const respostaValida = {
  associacoes: [
    {
      curriculo_id: "curriculo-001",
      vaga: {
        id: "vaga-g2-001",
        titulo: "Estágio em Desenvolvimento",
        empresa: "Empresa Exemplo",
        descricao: "Desenvolvimento de aplicações web.",
        requisitos: ["TypeScript", "React"],
        localizacao: "São Paulo - SP",
        modalidade: "Híbrido",
        url_candidatura: "https://grupo2.exemplo.com/vagas/001",
      },
    },
  ],
};

describe("adaptarRespostaGrupo2", () => {
  it("converte o contrato externo em sugestões internas de vaga", () => {
    expect(adaptarRespostaGrupo2(respostaValida)).toEqual([
      {
        curriculoId: "curriculo-001",
        vaga: {
          id: "vaga-g2-001",
          titulo: "Estágio em Desenvolvimento",
          empresa: "Empresa Exemplo",
          descricao: "Desenvolvimento de aplicações web.",
          requisitos: ["TypeScript", "React"],
          localizacao: "São Paulo - SP",
          modalidade: "Híbrido",
          urlCandidatura: "https://grupo2.exemplo.com/vagas/001",
        },
      },
    ]);
  });

  it("recusa uma resposta que não respeita o contrato", () => {
    expect(() => adaptarRespostaGrupo2({ associacoes: [{ vaga: {} }] })).toThrow(
      new FalhaVagasGrupo2("resposta-invalida"),
    );
  });
});

describe("criarClienteVagasGrupo2", () => {
  it("traduz falha de transporte para indisponibilidade", async () => {
    const requisitarResposta = vi.fn().mockRejectedValue(new Error("timeout"));
    const cliente = criarClienteVagasGrupo2(requisitarResposta);

    await expect(cliente.listarSugestoes()).rejects.toEqual(
      new FalhaVagasGrupo2("indisponivel"),
    );
  });
});
