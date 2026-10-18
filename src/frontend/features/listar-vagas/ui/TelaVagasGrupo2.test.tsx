import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { SugestaoVaga } from "../../../entities/vaga";
import type { ClienteDecisoesRecomendacao } from "../api/cliente-decisoes-recomendacao";
import {
  FalhaVagasGrupo2,
  type ClienteVagasGrupo2,
} from "../api/cliente-vagas-grupo2";
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

  it("apresenta estado de erro com mensagem amigável sem expor detalhes técnicos da integração", async () => {
    const cliente: ClienteVagasGrupo2 = {
      listarSugestoes: vi
        .fn()
        .mockRejectedValue(
          new Error(
            "HTTP 500: Falha interna no endpoint http://integracao.parceiro:8080/vagas - stacktrace trace_id_abc123",
          ),
        ),
    };

    render(<TelaVagasGrupo2 cliente={cliente} />);

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent("Não foi possível carregar as vagas");
    expect(alerta).toHaveTextContent(
      "Não foi possível carregar as vagas no momento. Tente novamente mais tarde.",
    );

    expect(screen.queryByText(/HTTP 500/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/endpoint/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/http:\/\//i)).not.toBeInTheDocument();
    expect(screen.queryByText(/stacktrace/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/trace_id/i)).not.toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: "Tentar novamente" }),
    ).toBeEnabled();
  });

  it("recupera da falha de busca ao clicar em tentar novamente com os critérios preservados", async () => {
    const usuario = userEvent.setup();
    const listarSugestoes = vi
      .fn()
      .mockRejectedValueOnce(new FalhaVagasGrupo2("tempo-limite"))
      .mockResolvedValueOnce([sugestao]);

    const cliente: ClienteVagasGrupo2 = { listarSugestoes };

    render(<TelaVagasGrupo2 cliente={cliente} />);

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(
      "O serviço de vagas demorou para responder. Verifique sua conexão e tente novamente.",
    );

    const botaoRecuperar = screen.getByRole("button", {
      name: "Tentar novamente",
    });
    await usuario.click(botaoRecuperar);

    expect(
      await screen.findByRole("heading", { name: sugestao.vaga.titulo }),
    ).toBeInTheDocument();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
    expect(listarSugestoes).toHaveBeenCalledTimes(2);
    expect(listarSugestoes).toHaveBeenLastCalledWith({ termo: "" });
  });

  it("preserva a palavra-chave informada no formulário durante o estado de erro e reexecuta com ela", async () => {
    const usuario = userEvent.setup();
    const listarSugestoes = vi
      .fn()
      .mockResolvedValueOnce([])
      .mockRejectedValueOnce(new FalhaVagasGrupo2("resposta-invalida"))
      .mockResolvedValueOnce([sugestao]);

    const cliente: ClienteVagasGrupo2 = { listarSugestoes };

    render(<TelaVagasGrupo2 cliente={cliente} />);
    await screen.findByRole("heading", { name: "Nenhuma vaga encontrada" });

    const campo = screen.getByRole("searchbox", { name: "Palavra-chave" });
    await usuario.type(campo, "Backend");
    await usuario.click(
      screen.getByRole("button", { name: "Pesquisar vagas" }),
    );

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(
      "Recebemos uma resposta inesperada ao consultar as vagas. Tente novamente mais tarde.",
    );
    expect(campo).toHaveValue("Backend");

    const botaoRecuperar = screen.getByRole("button", {
      name: "Tentar novamente",
    });
    await usuario.click(botaoRecuperar);

    expect(
      await screen.findByRole("heading", { name: sugestao.vaga.titulo }),
    ).toBeInTheDocument();
    expect(campo).toHaveValue("Backend");
    expect(listarSugestoes).toHaveBeenLastCalledWith({ termo: "Backend" });
  });
});
