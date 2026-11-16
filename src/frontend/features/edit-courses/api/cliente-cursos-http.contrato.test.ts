import { afterEach, describe, expect, it, vi } from "vitest";
import { criarClienteCursosHttp, FalhaCurso } from "./cliente-cursos-http";
import type { Curso } from "../model/cursos";
const a: Curso = { nome: "Curso A", instituicao: "Escola", cargaHoraria: "20" };
const b: Curso = { ...a, nome: "Outro" };
const vazio: Curso = { nome: "", instituicao: "", cargaHoraria: "" };
const parcial: Curso = { nome: "", instituicao: "Escola", cargaHoraria: "" };
afterEach(() => vi.restoreAllMocks());
describe("contrato e retry por instância de cursos", () => {
  it("ignora somente registros totalmente vazios", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    await criarClienteCursosHttp("http://api/").salvar([vazio, a, vazio]);
    expect(requisitar).toHaveBeenCalledTimes(1);
  });
  it("não exige API nem faz requests para lote totalmente vazio", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch");
    await expect(
      criarClienteCursosHttp("").salvar([vazio]),
    ).resolves.toBeUndefined();
    expect(requisitar).not.toHaveBeenCalled();
  });
  it.each([0, 1])(
    "rejeita parcial no índice %i antes de qualquer POST",
    async (indice) => {
      const requisitar = vi
        .spyOn(globalThis, "fetch")
        .mockResolvedValue(new Response(null, { status: 201 }));
      const lote = indice === 0 ? [parcial, a] : [a, parcial];
      await expect(
        criarClienteCursosHttp("http://api").salvar(lote),
      ).rejects.toMatchObject({ codigo: "resposta-invalida" });
      expect(requisitar).not.toHaveBeenCalled();
    },
  );
  it("normaliza o payload antes de persistir e deduplicar", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteCursosHttp("http://api///");
    await cliente.salvar([
      { nome: " Curso A ", instituicao: " Escola ", cargaHoraria: " 20 " },
    ]);
    expect(requisitar).toHaveBeenCalledWith("http://api/cursos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        nome: "Curso A",
        instituicao: "Escola",
        carga_horaria: 20,
      }),
    });
    await cliente.salvar([a]);
    expect(requisitar).toHaveBeenCalledTimes(1);
  });
  it("não reenvia A confirmado quando retorna à etapa e adiciona B", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteCursosHttp("http://api");
    await cliente.salvar([a]);
    await cliente.salvar([a, b, a]);
    await cliente.salvar([a, b]);
    expect(requisitar).toHaveBeenCalledTimes(2);
  });
  it.each([409, 422, 503])(
    "retenta só pendência após sucesso parcial e HTTP %i",
    async (status) => {
      const requisitar = vi
        .spyOn(globalThis, "fetch")
        .mockResolvedValueOnce(new Response(null, { status: 201 }))
        .mockResolvedValueOnce(new Response(null, { status }))
        .mockResolvedValue(new Response(null, { status: 201 }));
      const cliente = criarClienteCursosHttp("http://api");
      await expect(cliente.salvar([a, b])).rejects.toMatchObject({
        codigo: status >= 500 ? "indisponivel" : "resposta-invalida",
      });
      await cliente.salvar([a, b]);
      expect(requisitar).toHaveBeenCalledTimes(3);
      expect(requisitar.mock.calls[2]?.[1]?.body).toBe(
        requisitar.mock.calls[1]?.[1]?.body,
      );
      expect(requisitar.mock.calls[2]?.[1]?.body).not.toBe(
        requisitar.mock.calls[0]?.[1]?.body,
      );
    },
  );
  it("não confirma falha de rede mesmo após sucesso parcial", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(null, { status: 201 }))
      .mockRejectedValueOnce(new TypeError("offline"))
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteCursosHttp("http://api");
    await expect(cliente.salvar([a, b])).rejects.toThrow(
      new FalhaCurso("rede"),
    );
    await cliente.salvar([a, b]);
    expect(requisitar).toHaveBeenCalledTimes(3);
    expect(requisitar.mock.calls[2]?.[1]?.body).toBe(
      requisitar.mock.calls[1]?.[1]?.body,
    );
  });
  it("não compartilha confirmações entre instâncias", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    await criarClienteCursosHttp("http://api").salvar([a]);
    await criarClienteCursosHttp("http://api").salvar([a]);
    expect(requisitar).toHaveBeenCalledTimes(2);
  });
  it("persiste alteração de payload em vez de ignorar pelo nome", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteCursosHttp("http://api");
    await cliente.salvar([a]);
    await cliente.salvar([{ ...a, cargaHoraria: "40" }]);
    expect(requisitar).toHaveBeenCalledTimes(2);
  });
  it("classifica API ausente sem iniciar request", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch");
    await expect(criarClienteCursosHttp("").salvar([a])).rejects.toThrow(
      new FalhaCurso("indisponivel"),
    );
    expect(requisitar).not.toHaveBeenCalled();
  });
});

it.each(["1.5", "1.0", "1e2", "Infinity", "0x10", "10001", "0"])(
  "barra carga inválida %s sem arredondar nem enviar lote",
  async (cargaHoraria) => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    await expect(
      criarClienteCursosHttp("http://api").salvar([a, { ...a, cargaHoraria }]),
    ).rejects.toMatchObject({ codigo: "resposta-invalida" });
    expect(requisitar).not.toHaveBeenCalled();
  },
);
it("envia carga ausente explicitamente como null", async () => {
  const requisitar = vi
    .spyOn(globalThis, "fetch")
    .mockResolvedValue(new Response(null, { status: 201 }));
  await criarClienteCursosHttp("http://api").salvar([
    { ...a, cargaHoraria: " " },
  ]);
  expect(JSON.parse(requisitar.mock.calls[0]?.[1]?.body as string)).toEqual({
    nome: "Curso A",
    instituicao: "Escola",
    carga_horaria: null,
  });
});
it.each(["nome", "instituicao"] as const)(
  "barra %s longo antes de POST",
  async (campo) => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    await expect(
      criarClienteCursosHttp("http://api").salvar([
        a,
        { ...a, [campo]: "A".repeat(201) },
      ]),
    ).rejects.toMatchObject({ codigo: "resposta-invalida" });
    expect(requisitar).not.toHaveBeenCalled();
  },
);
