import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { SugestaoVaga } from "../../../entities/vaga";
import type { ClienteDecisoesRecomendacao } from "../api/cliente-decisoes-recomendacao";
import type { ClienteVagasGrupo2 } from "../api/cliente-vagas-grupo2";
import { TelaVagasGrupo2 } from "./TelaVagasGrupo2";

afterEach(cleanup);

const sugestao: SugestaoVaga = {
  curriculoId: "curriculo-001",
  vaga: {
    id: "vaga-001",
    titulo: "Estágio em Desenvolvimento",
    empresa: "Empresa Exemplo",
    descricao: "Desenvolvimento de aplicações web.",
    requisitos: ["TypeScript", "React"],
    localizacao: "São Paulo - SP",
    modalidade: "Híbrido",
    urlCandidatura: "https://grupo2.exemplo.com/vagas/001",
  },
};

function criarCliente(sugestoes: SugestaoVaga[]): ClienteVagasGrupo2 {
  return { listarSugestoes: vi.fn().mockResolvedValue(sugestoes) };
}

describe("TelaVagasGrupo2", () => {
  it("preserva a palavra-chave depois de uma busca sem resultados", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteVagasGrupo2 = {
      listarSugestoes: vi.fn().mockResolvedValue([]),
    };

    render(<TelaVagasGrupo2 cliente={cliente} />);
    await screen.findByRole("heading", { name: "Nenhuma vaga encontrada" });

    const campo = screen.getByRole("searchbox", { name: "Palavra-chave" });
    await usuario.type(campo, "React");
    await usuario.click(
      screen.getByRole("button", { name: "Pesquisar vagas" }),
    );

    expect(await screen.findByText(/para “React”/)).toBeInTheDocument();
    expect(campo).toHaveValue("React");
    expect(cliente.listarSugestoes).toHaveBeenLastCalledWith({
      termo: "React",
    });
  });

  it("apresenta sugestões e controles com nomes acessíveis", async () => {
    render(<TelaVagasGrupo2 cliente={criarCliente([sugestao])} />);

    expect(
      await screen.findByRole("heading", { name: sugestao.vaga.titulo }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Aceitar recomendação" }),
    ).toBeEnabled();
    expect(
      screen.getByRole("button", { name: "Rejeitar recomendação" }),
    ).toBeEnabled();
  });

  it("confirma uma decisão somente após o cliente concluir o salvamento", async () => {
    const usuario = userEvent.setup();
    let concluirSalvamento: (() => void) | undefined;
    const clienteDecisoes: ClienteDecisoesRecomendacao = {
      salvarDecisao: vi.fn(
        () =>
          new Promise<void>((resolve) => {
            concluirSalvamento = resolve;
          }),
      ),
    };

    render(
      <TelaVagasGrupo2
        cliente={criarCliente([sugestao])}
        clienteDecisoes={clienteDecisoes}
      />,
    );
    await screen.findByRole("heading", { name: sugestao.vaga.titulo });

    await usuario.click(
      screen.getByRole("button", { name: "Aceitar recomendação" }),
    );

    expect(screen.getByRole("status")).toHaveTextContent("Salvando decisão");
    expect(
      screen.queryByText("Recomendação aceita e salva."),
    ).not.toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Rejeitar recomendação" }),
    ).toBeDisabled();

    concluirSalvamento?.();

    expect(
      await screen.findByText("Recomendação aceita e salva."),
    ).toBeInTheDocument();
    expect(clienteDecisoes.salvarDecisao).toHaveBeenCalledWith({
      curriculoId: "curriculo-001",
      vagaId: "vaga-001",
      decisao: "aceitar",
    });
  });

  it("não confirma sucesso se salvar falhar e permite nova tentativa", async () => {
    const usuario = userEvent.setup();
    const clienteDecisoes: ClienteDecisoesRecomendacao = {
      salvarDecisao: vi.fn().mockRejectedValueOnce(new Error("indisponivel")),
    };

    render(
      <TelaVagasGrupo2
        cliente={criarCliente([sugestao])}
        clienteDecisoes={clienteDecisoes}
      />,
    );
    await screen.findByRole("heading", { name: sugestao.vaga.titulo });

    await usuario.click(
      screen.getByRole("button", { name: "Rejeitar recomendação" }),
    );

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Não foi possível salvar a recomendação rejeitada",
    );
    expect(
      screen.queryByText("Recomendação rejeitada e salva."),
    ).not.toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Rejeitar recomendação" }),
    ).toBeEnabled();
  });
});
