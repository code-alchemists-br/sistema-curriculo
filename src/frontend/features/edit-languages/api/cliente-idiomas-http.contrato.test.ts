import { afterEach, describe, expect, it, vi } from "vitest";
import { criarClienteIdiomasHttp, FalhaIdioma } from "./cliente-idiomas-http";
import type { Idioma } from "../model/idiomas";
const a: Idioma = { nome: "Inglês", nivel: "basico" };
const b: Idioma = { ...a, nome: "Outro" };
const vazio: Idioma = { nome: "", nivel: "" };
const parcial: Idioma = { nome: "", nivel: "basico" };
afterEach(() => vi.restoreAllMocks());
describe("contrato e retry por instância de idiomas", () => {
  it("ignora somente registros totalmente vazios", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    await criarClienteIdiomasHttp("http://api/").salvar([vazio, a, vazio]);
    expect(requisitar).toHaveBeenCalledTimes(1);
  });
  it("não exige API nem faz requests para lote totalmente vazio", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch");
    await expect(
      criarClienteIdiomasHttp("").salvar([vazio]),
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
        criarClienteIdiomasHttp("http://api").salvar(lote),
      ).rejects.toMatchObject({ codigo: "resposta-invalida" });
      expect(requisitar).not.toHaveBeenCalled();
    },
  );
  it("normaliza o payload antes de persistir e deduplicar", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteIdiomasHttp("http://api///");
    await cliente.salvar([{ nome: " Inglês ", nivel: "basico" }]);
    expect(requisitar).toHaveBeenCalledWith("http://api/idiomas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ idioma: "Inglês", nivel: "basico" }),
    });
    await cliente.salvar([a]);
    expect(requisitar).toHaveBeenCalledTimes(1);
  });
  it("não reenvia A confirmado quando retorna à etapa e adiciona B", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteIdiomasHttp("http://api");
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
      const cliente = criarClienteIdiomasHttp("http://api");
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
    const cliente = criarClienteIdiomasHttp("http://api");
    await expect(cliente.salvar([a, b])).rejects.toThrow(
      new FalhaIdioma("rede"),
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
    await criarClienteIdiomasHttp("http://api").salvar([a]);
    await criarClienteIdiomasHttp("http://api").salvar([a]);
    expect(requisitar).toHaveBeenCalledTimes(2);
  });
  it("persiste alteração de payload em vez de ignorar pelo nome", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteIdiomasHttp("http://api");
    await cliente.salvar([a]);
    await cliente.salvar([{ ...a, nivel: "fluente" }]);
    expect(requisitar).toHaveBeenCalledTimes(2);
  });
  it("classifica API ausente sem iniciar request", async () => {
    const requisitar = vi.spyOn(globalThis, "fetch");
    await expect(criarClienteIdiomasHttp("").salvar([a])).rejects.toThrow(
      new FalhaIdioma("indisponivel"),
    );
    expect(requisitar).not.toHaveBeenCalled();
  });
});

it("barra nível não pertencente ao vocabulário antes de POST", async () => {
  const requisitar = vi
    .spyOn(globalThis, "fetch")
    .mockResolvedValue(new Response(null, { status: 201 }));
  await expect(
    criarClienteIdiomasHttp("http://api").salvar([
      a,
      { ...a, nivel: "nativo" } as unknown as Idioma,
    ]),
  ).rejects.toMatchObject({ codigo: "resposta-invalida" });
  expect(requisitar).not.toHaveBeenCalled();
});
