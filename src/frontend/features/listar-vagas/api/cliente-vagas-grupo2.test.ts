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

const respostaMatchesCompleta = {
  matches: [
    {
      rank: 1,
      job: {
        company: "Tech Corp",
        title: "Estágio em Engenharia de Dados",
        description: "Pipelines de dados e integração com Python.",
        keywords: ["ETL", "Big Data"],
        location: {
          city: "São Paulo",
          state: "SP",
        },
        work_arrangement: "REMOTE",
        seniority_level: "INTERN",
        skills: ["Python", "SQL"],
        salary: {
          min: 2000,
          max: 2800,
        },
        currency: "BRL",
        job_url: "https://grupo2.exemplo.com/jobs/101",
        publication_date: "2026-11-01T04:11:59.870Z",
      },
      score: 100,
      embedding_model: "text-embedding-3-small",
      algorithm_version: "1.0",
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

  it("converte o schema matches do Grupo 2 com todos os campos extraídos", () => {
    expect(adaptarRespostaGrupo2(respostaMatchesCompleta)).toEqual([
      {
        curriculoId: "curriculo-padrao",
        ranque: 1,
        pontuacaoCompatibilidade: 100,
        vaga: {
          id: "vaga-1-https://grupo2.exemplo.com/jobs/101",
          titulo: "Estágio em Engenharia de Dados",
          empresa: "Tech Corp",
          descricao: "Pipelines de dados e integração com Python.",
          requisitos: ["Python", "SQL"],
          palavrasChave: ["ETL", "Big Data"],
          localizacao: "São Paulo - SP",
          modalidade: "Remoto",
          nivelSenioridade: "Estágio",
          salario: "R$ 2.000 – R$ 2.800",
          moeda: "BRL",
          urlCandidatura: "https://grupo2.exemplo.com/jobs/101",
          dataPublicacao: "01/11/2026",
        },
      },
    ]);
  });

  it("aceita vaga no schema matches apenas com os campos garantidos (title, description e job_url)", () => {
    const apenasGarantidos = {
      matches: [
        {
          job: {
            title: "Desenvolvedor Backend",
            description: "Atuação em APIs REST.",
            job_url: "https://grupo2.exemplo.com/jobs/minimo",
            salary: {
              additionalProp1: 0,
              additionalProp2: 0,
            },
          },
        },
      ],
    };

    expect(adaptarRespostaGrupo2(apenasGarantidos)).toEqual([
      {
        curriculoId: "curriculo-padrao",
        vaga: {
          id: "vaga-1-https://grupo2.exemplo.com/jobs/minimo",
          titulo: "Desenvolvedor Backend",
          empresa: "Empresa confidencial",
          descricao: "Atuação em APIs REST.",
          requisitos: [],
          localizacao: null,
          modalidade: null,
          urlCandidatura: "https://grupo2.exemplo.com/jobs/minimo",
        },
      },
    ]);
  });

  it("recusa uma resposta que não respeita o contrato", () => {
    expect(() =>
      adaptarRespostaGrupo2({ associacoes: [{ vaga: {} }] }),
    ).toThrow(new FalhaVagasGrupo2("resposta-invalida"));

    expect(() =>
      adaptarRespostaGrupo2({ matches: [{ job: { title: "Sem URL" } }] }),
    ).toThrow(new FalhaVagasGrupo2("resposta-invalida"));
  });
});

describe("criarClienteVagasGrupo2", () => {
  it("encaminha o termo pesquisado ao adaptador de transporte", async () => {
    const requisitarResposta = vi.fn().mockResolvedValue(respostaValida);
    const cliente = criarClienteVagasGrupo2(requisitarResposta);

    await cliente.listarSugestoes({ termo: "react" });

    expect(requisitarResposta).toHaveBeenCalledWith({ termo: "react" });
  });

  it("traduz falha de transporte para indisponibilidade", async () => {
    const requisitarResposta = vi
      .fn()
      .mockRejectedValue(new Error("falha generica de rede"));
    const cliente = criarClienteVagasGrupo2(requisitarResposta);

    await expect(cliente.listarSugestoes({ termo: "" })).rejects.toEqual(
      new FalhaVagasGrupo2("indisponivel"),
    );
  });

  it("traduz falha com timeout para tempo-limite", async () => {
    const requisitarResposta = vi
      .fn()
      .mockRejectedValue(new Error("Request timed out"));
    const cliente = criarClienteVagasGrupo2(requisitarResposta);

    await expect(cliente.listarSugestoes({ termo: "" })).rejects.toEqual(
      new FalhaVagasGrupo2("tempo-limite"),
    );
  });
});
