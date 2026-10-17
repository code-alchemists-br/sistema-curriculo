import { describe, expect, it } from "vitest";

import { FalhaVagasGrupo2 } from "../api/cliente-vagas-grupo2";
import { obterMensagemErroVagas } from "./mensagem-erro-vagas";

describe("obterMensagemErroVagas", () => {
  it("retorna mensagem amigável para resposta inválida", () => {
    const erro = new FalhaVagasGrupo2("resposta-invalida");
    expect(obterMensagemErroVagas(erro)).toBe(
      "Recebemos uma resposta inesperada ao consultar as vagas. Tente novamente mais tarde.",
    );
  });

  it("retorna mensagem amigável para tempo limite excedido", () => {
    const erro = new FalhaVagasGrupo2("tempo-limite");
    expect(obterMensagemErroVagas(erro)).toBe(
      "O serviço de vagas demorou para responder. Verifique sua conexão e tente novamente.",
    );
  });

  it("retorna mensagem amigável para serviço indisponível", () => {
    const erro = new FalhaVagasGrupo2("indisponivel");
    expect(obterMensagemErroVagas(erro)).toBe(
      "O serviço de vagas está temporariamente indisponível. Tente novamente mais tarde.",
    );
  });

  it("retorna mensagem neutra e oculta detalhes técnicos para erros genéricos", () => {
    const erro = new Error("Connection refused: 192.168.1.1:5000/internal-api");
    expect(obterMensagemErroVagas(erro)).toBe(
      "Não foi possível carregar as vagas no momento. Tente novamente mais tarde.",
    );
  });

  it("retorna mensagem neutra para valores não-Error", () => {
    expect(obterMensagemErroVagas("erro em formato de string")).toBe(
      "Não foi possível carregar as vagas no momento. Tente novamente mais tarde.",
    );
    expect(obterMensagemErroVagas(null)).toBe(
      "Não foi possível carregar as vagas no momento. Tente novamente mais tarde.",
    );
  });
});
