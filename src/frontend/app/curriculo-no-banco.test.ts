import { afterEach, describe, expect, it, vi } from "vitest";

import {
  FalhaCurriculoNoBanco,
  criarClienteCurriculoNoBanco,
} from "./curriculo-no-banco";

const API = "http://api.test/estudantes/me/curriculo";

afterEach(() => vi.restoreAllMocks());

/** Substitui o fetch por uma resposta fixa e devolve o espião. */
function responder(resposta: Response | Error) {
  return vi.spyOn(globalThis, "fetch").mockImplementation(async () => {
    if (resposta instanceof Error) throw resposta;
    return resposta;
  });
}

/** Corpo JSON enviado na chamada indicada. */
function corpo(espiao: ReturnType<typeof responder>, indice = 0) {
  return JSON.parse(espiao.mock.calls[indice][1]?.body as string);
}

describe("criarClienteCurriculoNoBanco", () => {
  it("converte o currículo da API para o formato das telas", async () => {
    responder(
      new Response(
        JSON.stringify({
          dados_pessoais: {
            nome: "Ana",
            email: "ana@x.com",
            endereco: "São Paulo",
            cidade: "SP",
            telefones: ["(11) 9999-0000"],
            linkedin: null,
            curriculo_lattes: "http://lattes/1",
          },
          formacoes: [
            {
              instituicao: "Fatec",
              curso: "ADS",
              nivel: "tecnologo",
              status: "em_andamento",
              data_inicio: "2024-02-01",
              data_fim: null,
            },
          ],
          experiencias: [
            {
              empresa: "X",
              cargo: "Dev",
              descricao: "APIs",
              data_inicio: "2024-01-01",
              data_fim: null,
            },
          ],
          projetos: [],
          competencias: [
            { categoria: "tecnica", descricao: "Python", nivel: "padrao" },
            {
              categoria: "comportamental",
              descricao: "Comunicação",
              nivel: "padrao",
            },
          ],
          idiomas: [{ idioma: "Inglês", nivel: "avancado" }],
          cursos: [{ nome: "React", instituicao: "Alura", carga_horaria: 40 }],
          certificacoes: [{ nome: "AWS", organizacao_emissora: "Amazon" }],
          modelo: "moderno",
        }),
        { status: 200 },
      ),
    );

    const curriculo =
      await criarClienteCurriculoNoBanco("http://api.test/").carregar();

    expect(curriculo.dadosPessoais).toMatchObject({
      nomeCompleto: "Ana",
      enderecoCompleto: "São Paulo, SP",
      telefones: ["(11) 9999-0000"],
      curriculoLattes: "http://lattes/1",
    });
    expect(curriculo.formacoes[0]).toMatchObject({
      dataFim: "",
      curriculoLattes: "http://lattes/1",
      naoPossuiLattes: false,
    });
    expect(curriculo.experiencias[0]).toMatchObject({
      empregoAtual: true,
      fim: "",
    });
    expect(curriculo.competencias).toEqual({
      hardSkills: ["Python"],
      softSkills: ["Comunicação"],
    });
    expect(curriculo.idiomas).toEqual([{ nome: "Inglês", nivel: "avancado" }]);
    expect(curriculo.cursos).toEqual([
      { nome: "React", instituicao: "Alura", cargaHoraria: "40" },
    ]);
    expect(curriculo.modelo).toBe("moderno");
  });

  it("substitui a seção com os itens limpos e as datas completas", async () => {
    const espiao = responder(new Response(null, { status: 204 }));
    const cliente = criarClienteCurriculoNoBanco("http://api.test");

    await cliente.salvarExperiencias([
      {
        empresa: " X ",
        cargo: "Dev",
        inicio: "2024-01",
        fim: "2024-06",
        empregoAtual: false,
        descricao: " APIs ",
      },
      {
        empresa: "",
        cargo: "",
        inicio: "",
        fim: "",
        empregoAtual: false,
        descricao: "",
      },
    ]);

    expect(espiao.mock.calls[0][0]).toBe(`${API}/experiencias`);
    expect(espiao.mock.calls[0][1]?.method).toBe("PUT");
    expect(corpo(espiao)).toEqual({
      itens: [
        {
          empresa: "X",
          cargo: "Dev",
          descricao: "APIs",
          data_inicio: "2024-01-01",
          data_fim: "2024-06-01",
        },
      ],
    });
  });

  it("envia o Lattes junto com as formações, salvo quando a pessoa não tem", async () => {
    const espiao = responder(new Response(null, { status: 204 }));
    const cliente = criarClienteCurriculoNoBanco("http://api.test");
    const formacao = {
      instituicao: "Fatec",
      curso: "ADS",
      nivel: "tecnologo" as const,
      dataInicio: "2024-02-01",
      dataFim: "",
      status: "em_andamento" as const,
      curriculoLattes: " http://lattes/1 ",
    };

    await cliente.salvarFormacoes([formacao]);
    await cliente.salvarFormacoes([{ ...formacao, naoPossuiLattes: true }]);

    expect(corpo(espiao, 0).curriculo_lattes).toBe("http://lattes/1");
    expect(corpo(espiao, 0).itens[0].data_fim).toBeNull();
    expect(corpo(espiao, 1).curriculo_lattes).toBeNull();
  });

  it("separa competências por categoria e repassa o sinal de cancelamento", async () => {
    const espiao = responder(new Response(null, { status: 204 }));
    const controle = new AbortController();

    await criarClienteCurriculoNoBanco("http://api.test").salvarCompetencias(
      { hardSkills: ["Python", " "], softSkills: ["Comunicação"] },
      controle.signal,
    );

    expect(corpo(espiao)).toEqual({
      itens: [
        { categoria: "tecnica", descricao: "Python" },
        { categoria: "comportamental", descricao: "Comunicação" },
      ],
    });
    expect(espiao.mock.calls[0][1]?.signal).toBe(controle.signal);
  });

  it.each([
    [401, /sessão expirou/i],
    [409, /repetidos/i],
    [503, /servidor não conseguiu salvar/i],
  ])(
    "traduz a resposta %i em mensagem para o estudante",
    async (status, mensagem) => {
      responder(new Response(null, { status }));

      const falha = await criarClienteCurriculoNoBanco("http://api.test")
        .salvarIdiomas([{ nome: "Inglês", nivel: "basico" }])
        .catch((erro: unknown) => erro);

      expect(falha).toBeInstanceOf(FalhaCurriculoNoBanco);
      expect((falha as FalhaCurriculoNoBanco).status).toBe(status);
      expect((falha as Error).message).toMatch(mensagem);
    },
  );

  it("usa o detalhe da API em 422 e avisa quando não há conexão", async () => {
    responder(
      new Response(JSON.stringify({ detail: "Nome vazio." }), { status: 422 }),
    );
    await expect(
      criarClienteCurriculoNoBanco("http://api.test").salvarModelo("moderno"),
    ).rejects.toThrow("Não foi possível salvar: Nome vazio.");

    responder(new TypeError("Failed to fetch"));
    await expect(
      criarClienteCurriculoNoBanco("http://api.test").carregar(),
    ).rejects.toMatchObject({
      status: null,
      message: expect.stringMatching(/Sem conexão/),
    });
  });
});
