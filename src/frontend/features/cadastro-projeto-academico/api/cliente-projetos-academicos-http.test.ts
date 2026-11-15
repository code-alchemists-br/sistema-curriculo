import { afterEach, describe, expect, it, vi } from "vitest";

import { criarClienteProjetosAcademicosHttp } from "./cliente-projetos-academicos-http";
import { FalhaCadastroProjeto } from "./cliente-projetos-academicos";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criarClienteProjetosAcademicosHttp", () => {
  it("envia POST para /projetos-academicos com credentials include", async () => {
    const requisitar = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(null, { status: 201 }));
    const cliente = criarClienteProjetosAcademicosHttp("http://127.0.0.1:8000");

    await cliente.cadastrar({
      titulo: "Sistema de Currículo",
      descricao:
        "Plataforma de criação e exportação de currículos para estudantes",
      tecnologias: "React, TypeScript, FastAPI",
    });

    expect(requisitar).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/projetos-academicos",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          titulo: "Sistema de Currículo",
          descricao:
            "Plataforma de criação e exportação de currículos para estudantes",
          tecnologias: "React, TypeScript, FastAPI",
        }),
      },
    );
  });

  it("lança FalhaCadastroProjeto com codigo indisponivel em erro de rede", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("Erro de rede"));
    const cliente = criarClienteProjetosAcademicosHttp("http://127.0.0.1:8000");

    await expect(
      cliente.cadastrar({
        titulo: "Projeto Teste",
        descricao: "Descrição do projeto",
        tecnologias: "Python",
      }),
    ).rejects.toThrow(new FalhaCadastroProjeto("indisponivel"));
  });
});
