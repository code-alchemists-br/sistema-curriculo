import { afterEach, describe, expect, it, vi } from "vitest";

import { criarClienteVagasHttp } from "./cliente-vagas-http";
import { FalhaVagasGrupo2 } from "./cliente-vagas-grupo2";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criarClienteVagasHttp", () => {
  it("envia GET para /vagas com query param termo e credentials include", async () => {
    const dadosMock = {
      termo: "React",
      total: 1,
      vagas: [
        {
          id: "vaga-123",
          titulo: "Desenvolvedor React",
          empresa: "Tech Solutions",
          descricao: "Desenvolvimento frontend com React e TypeScript",
          requisitos: ["React", "TypeScript", "Git"],
          localizacao: "São Paulo, SP",
          modalidade: "Remoto",
          url_candidatura: "https://exemplo.com/vaga/123",
        },
      ],
    };

    const requisitar = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify(dadosMock), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    const cliente = criarClienteVagasHttp("http://127.0.0.1:8000");
    const sugestoes = await cliente.listarSugestoes({ termo: "React" });

    expect(requisitar).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/vagas?termo=React",
      {
        method: "GET",
        headers: { Accept: "application/json" },
        credentials: "include",
      },
    );
    expect(sugestoes).toHaveLength(1);
    expect(sugestoes[0].vaga.titulo).toBe("Desenvolvedor React");
    expect(sugestoes[0].vaga.empresa).toBe("Tech Solutions");
    expect(sugestoes[0].vaga.modalidade).toBe("Remoto");
    expect(sugestoes[0].vaga.urlCandidatura).toBe(
      "https://exemplo.com/vaga/123",
    );
  });

  it("lança FalhaVagasGrupo2 com codigo tempo-limite em resposta 504", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(null, { status: 504 }),
    );
    const cliente = criarClienteVagasHttp("http://127.0.0.1:8000");

    await expect(cliente.listarSugestoes({ termo: "Java" })).rejects.toThrow(
      new FalhaVagasGrupo2("tempo-limite"),
    );
  });

  it("lança FalhaVagasGrupo2 com codigo indisponivel em erro de conexão", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("Network error"));
    const cliente = criarClienteVagasHttp("http://127.0.0.1:8000");

    await expect(cliente.listarSugestoes({ termo: "Node" })).rejects.toThrow(
      new FalhaVagasGrupo2("indisponivel"),
    );
  });

  it("mapeia metadados enriquecidos do cvmatch e trata 429 como indisponivel", async () => {
    const dadosEnriquecidos = {
      termo: "",
      total: 1,
      vagas: [
        {
          id: "42",
          titulo: "Engenheiro de Dados Júnior",
          empresa: "Data Co",
          descricao: "Pipelines Python.",
          requisitos: ["Python", "SQL"],
          localizacao: "",
          modalidade: "HYBRID",
          url_candidatura: "",
          ranque: 1,
          pontuacao_compatibilidade: 91.5,
          elegivel: false,
          nivel_senioridade: "SPECIALIST",
          salario: "R$ 5.000",
          moeda: "BRL",
          palavras_chave: ["ETL"],
          data_publicacao: "2026-11-01T10:00:00Z",
          requisitos_atendidos: ["Python"],
          requisitos_faltantes: ["SQL"],
        },
      ],
    };

    vi.spyOn(globalThis, "fetch").mockResolvedValueOnce(
      new Response(JSON.stringify(dadosEnriquecidos), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    const cliente = criarClienteVagasHttp("http://127.0.0.1:8000");
    const sugestoes = await cliente.listarSugestoes({ termo: "" });

    expect(sugestoes).toEqual([
      {
        curriculoId: "curriculo-ativo",
        ranque: 1,
        pontuacaoCompatibilidade: 91.5,
        vaga: {
          id: "42",
          titulo: "Engenheiro de Dados Júnior",
          empresa: "Data Co",
          descricao: "Pipelines Python.",
          requisitos: ["Python", "SQL"],
          localizacao: null,
          modalidade: "Híbrido",
          urlCandidatura: null,
          nivelSenioridade: "Especialista",
          salario: "R$ 5.000",
          moeda: "BRL",
          palavrasChave: ["ETL"],
          dataPublicacao: "01/11/2026",
          elegivel: false,
          requisitosAtendidos: ["Python"],
          requisitosFaltantes: ["SQL"],
        },
      },
    ]);

    vi.spyOn(globalThis, "fetch").mockResolvedValueOnce(
      new Response(null, { status: 429 }),
    );
    await expect(cliente.listarSugestoes({ termo: "" })).rejects.toThrow(
      new FalhaVagasGrupo2("indisponivel"),
    );
  });
});
