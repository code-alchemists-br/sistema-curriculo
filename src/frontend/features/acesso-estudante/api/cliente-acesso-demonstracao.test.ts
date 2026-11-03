import { describe, expect, it } from "vitest";

import { criarClienteAcessoDemonstracao } from "./cliente-acesso-demonstracao";
import { FalhaAcessoEstudante } from "./cliente-acesso-estudante";

describe("cliente-acesso-demonstracao", () => {
  it("permite cadastrar um novo estudante e consultar por login", async () => {
    const cliente = criarClienteAcessoDemonstracao([]);

    const cadastrado = await cliente.cadastrar({
      nome: "Ricardo Silva",
      email: "ricardo@teste.com",
      senha: "SenhaSegura123!",
    });

    expect(cadastrado.nome).toBe("Ricardo Silva");
    expect(cadastrado.email).toBe("ricardo@teste.com");
    expect(cadastrado.id).toBeDefined();

    await expect(
      cliente.acessar({
        email: "ricardo@teste.com",
        senha: "SenhaSegura123!",
      }),
    ).resolves.toBeUndefined();
  });

  it("recusa cadastro com e-mail duplicado", async () => {
    const cliente = criarClienteAcessoDemonstracao([
      {
        id: "1",
        nome: "Existente",
        email: "existente@teste.com",
        senha: "123",
      },
    ]);

    await expect(
      cliente.cadastrar({
        nome: "Outro",
        email: "existente@teste.com",
        senha: "456",
      }),
    ).rejects.toThrow(new FalhaAcessoEstudante("email-ja-cadastrado"));
  });

  it("recusa login com senha incorreta ou e-mail inexistente", async () => {
    const cliente = criarClienteAcessoDemonstracao([
      {
        id: "1",
        nome: "Existente",
        email: "existente@teste.com",
        senha: "SenhaCorreta123!",
      },
    ]);

    await expect(
      cliente.acessar({
        email: "existente@teste.com",
        senha: "SenhaErrada",
      }),
    ).rejects.toThrow(new FalhaAcessoEstudante("credenciais-invalidas"));

    await expect(
      cliente.acessar({
        email: "inexistente@teste.com",
        senha: "SenhaCorreta123!",
      }),
    ).rejects.toThrow(new FalhaAcessoEstudante("credenciais-invalidas"));
  });
});
