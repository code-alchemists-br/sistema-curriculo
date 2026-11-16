import { describe, expect, it } from "vitest";

import { resumirPerfilParaIa } from "./recomendacao-modelo";

describe("resumirPerfilParaIa", () => {
  it("começa pelo objetivo e avisa quando não há experiência", () => {
    expect(resumirPerfilParaIa(undefined, "Estágio")).toEqual([
      { pergunta: "Objetivo do currículo", resposta: "Estágio" },
    ]);
    expect(resumirPerfilParaIa({}, "Estágio")).toContainEqual({
      pergunta: "Experiência profissional",
      resposta: "Nenhuma informada",
    });
  });

  it("descreve experiências e formação sem nome nem contatos", () => {
    const linhas = resumirPerfilParaIa(
      {
        experiencias: [
          {
            empresa: "Empresa X",
            cargo: "Dev",
            inicio: "2024-01-01",
            fim: "",
            empregoAtual: true,
            descricao: "APIs",
          },
        ],
        formacoes: [
          {
            nivel: "tecnologo",
            curso: "ADS",
            instituicao: "Fatec",
            status: "em_andamento",
          },
        ],
      },
      "Tecnologia",
    );

    expect(linhas).toContainEqual({
      pergunta: "Experiências (1)",
      resposta: "Dev - Empresa X - 2024-01-01 a atual - APIs",
    });
    expect(linhas).toContainEqual({
      pergunta: "Formação",
      resposta: "tecnologo - ADS - Fatec - em_andamento",
    });
    expect(JSON.stringify(linhas)).not.toMatch(/@|telefone/i);
    expect(linhas.length).toBeLessThanOrEqual(10);
  });
});
