import { describe, expect, it } from "vitest";

import { montarPreviaCurriculo } from "./montar-previa";

describe("montarPreviaCurriculo", () => {
  it("converte os dados do formulário na estrutura PreviaCurriculo de forma completa", () => {
    const previa = montarPreviaCurriculo({
      dadosPessoais: {
        nomeCompleto: "Ricardo Santos",
        email: "ricardo@fatec.sp.gov.br",
        enderecoCompleto: "Rua Teste, 100",
        telefones: ["(11) 98888-7777"],
        linkedIn: "https://linkedin.com/in/ricardo",
        curriculoLattes: "http://lattes.cnpq.br/123456",
      },
      formacoes: [
        {
          instituicao: "FATEC",
          curso: "ADS",
          nivel: "tecnologo",
          status: "concluido",
          dataInicio: "2021-02-01",
          dataFim: "2024-06-30",
        },
      ],
      experiencias: [
        {
          empresa: "Tech Corp",
          cargo: "Desenvolvedor Frontend",
          descricao: "Criação de interfaces acessíveis.",
          inicio: "2023-01-01",
          fim: "",
          empregoAtual: true,
        },
      ],
      competencias: {
        hardSkills: ["React", "TypeScript"],
        softSkills: ["Comunicação"],
      },
      idiomas: [{ nome: "Inglês", nivel: "avancado" }],
      cursos: [
        {
          nome: "UI/UX Design",
          instituicao: "Design Lab",
          cargaHoraria: 40,
        },
      ],
      certificacoes: [
        {
          nome: "AWS Cloud Practitioner",
          organizacaoEmissora: "Amazon Web Services",
        },
      ],
      modelo: "moderno",
    });

    expect(previa.layout).toBe("moderno");
    expect(previa.estudante.nome).toBe("Ricardo Santos");
    expect(previa.estudante.contato?.curriculo_lattes).toBe(
      "http://lattes.cnpq.br/123456",
    );
    expect(previa.formacoes).toHaveLength(1);
    expect(previa.formacoes[0].instituicao).toBe("FATEC");
    expect(previa.experiencias).toHaveLength(1);
    expect(previa.experiencias[0].fim).toBeNull();
    expect(previa.competencias).toHaveLength(3);
    expect(previa.idiomas).toHaveLength(1);
    expect(previa.idiomas[0].nivel).toBe("Avançado");
    expect(previa.documentos).toHaveLength(2);
  });

  it("atribui valores seguros por padrão quando os dados estão vazios ou parciais", () => {
    const previa = montarPreviaCurriculo({});

    expect(previa.layout).toBe("classico");
    expect(previa.estudante.nome).toBe("Estudante");
    expect(previa.formacoes).toEqual([]);
    expect(previa.experiencias).toEqual([]);
    expect(previa.competencias).toEqual([]);
    expect(previa.documentos).toEqual([]);
  });
});
