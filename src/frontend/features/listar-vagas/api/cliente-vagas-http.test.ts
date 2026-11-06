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
});

