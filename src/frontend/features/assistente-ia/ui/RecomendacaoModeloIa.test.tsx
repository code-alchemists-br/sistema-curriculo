import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ClienteAssistenteIa } from "../api/cliente-assistente-ia";
import { RecomendacaoModeloIa } from "./RecomendacaoModeloIa";

afterEach(cleanup);

/** Cria um cliente de IA falso com a recomendação (ou falha) informada. */
function clienteFalso(
  resposta:
    Awaited<ReturnType<ClienteAssistenteIa["recomendarModelo"]>> | Error,
) {
  const recomendarModelo = vi.fn(async () => {
    if (resposta instanceof Error) throw resposta;
    return resposta;
  });
  return {
    cliente: { revisar: vi.fn(), recomendarModelo } as ClienteAssistenteIa,
    recomendarModelo,
  };
}

describe("RecomendacaoModeloIa", () => {
  it("pede a recomendação sozinha ao aparecer e informa o modelo escolhido", async () => {
    const { cliente, recomendarModelo } = clienteFalso({
      modelo: "moderno",
      motivo: "Seu perfil é técnico.",
      alternativa: "compacto",
    });
    const aoRecomendar = vi.fn();
    render(
      <RecomendacaoModeloIa
        automatico
        aoRecomendar={aoRecomendar}
        cliente={cliente}
        nomeDoModelo={(m) => m.toUpperCase()}
        perfil={[{ pergunta: "Objetivo", resposta: "Estágio" }]}
      />,
    );

    expect(
      await screen.findByText("IA recomenda: MODERNO."),
    ).toBeInTheDocument();
    expect(screen.getByText("Segunda opção: COMPACTO.")).toBeInTheDocument();
    expect(aoRecomendar).toHaveBeenCalledWith("moderno");
    expect(recomendarModelo).toHaveBeenCalledTimes(1);
    expect(
      screen.getByRole("button", { name: "✦ Recomendar de novo" }),
    ).toBeInTheDocument();
  });

  it("só pede ao clicar quando não é automática e mostra a falha", async () => {
    const { cliente, recomendarModelo } = clienteFalso(
      new Error("IA desligada."),
    );
    render(
      <RecomendacaoModeloIa
        aoRecomendar={vi.fn()}
        cliente={cliente}
        nomeDoModelo={(m) => m}
        perfil={[]}
      />,
    );

    expect(recomendarModelo).not.toHaveBeenCalled();
    await userEvent.click(
      screen.getByRole("button", { name: "✦ Recomendar modelo com IA" }),
    );

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "IA desligada. Escolha o modelo abaixo.",
    );
  });
});
