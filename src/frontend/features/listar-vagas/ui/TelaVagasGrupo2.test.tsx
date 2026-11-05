import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { SugestaoVaga } from "../../../entities/vaga";
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
  it("consulta recomendações automaticamente sem exibir barra de busca aberta e apresenta o estado vazio quando aplicável", async () => {
    const cliente: ClienteVagasGrupo2 = {
      listarSugestoes: vi.fn().mockResolvedValue([]),
    };

    render(<TelaVagasGrupo2 cliente={cliente} />);
    await screen.findByRole("heading", {
      name: "Nenhuma vaga compatível no momento",
    });

    expect(screen.queryByRole("searchbox")).not.toBeInTheDocument();
    expect(
      screen.getByText(
        "Ainda não encontramos oportunidades alinhadas ao seu currículo.",
      ),
    ).toBeInTheDocument();
    expect(cliente.listarSugestoes).toHaveBeenCalledWith({
      termo: "",
    });
  });

  it("apresenta sugestões, tags de requisitos e ação principal com nomes acessíveis", async () => {
    render(<TelaVagasGrupo2 cliente={criarCliente([sugestao])} />);

    expect(
      await screen.findByRole("heading", { name: sugestao.vaga.titulo }),
    ).toBeInTheDocument();
    expect(screen.getByText("TypeScript")).toBeInTheDocument();
    expect(screen.getByText("React")).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "Acessar vaga original" }),
    ).toHaveAttribute("href", sugestao.vaga.urlCandidatura);
  });

  it("exibe campos opcionais extraídos do schema matches quando presentes no card", async () => {
    const sugestaoCompleta: SugestaoVaga = {
      curriculoId: "curriculo-001",
      ranque: 1,
      pontuacaoCompatibilidade: 98,
      vaga: {
        ...sugestao.vaga,
        requisitos: [],
        nivelSenioridade: "Estágio",
        salario: "R$ 2.000 – R$ 2.800",
        palavrasChave: ["Frontend", "Acessibilidade"],
        dataPublicacao: "01/11/2026",
      },
    };

    render(<TelaVagasGrupo2 cliente={criarCliente([sugestaoCompleta])} />);

    expect(await screen.findByText("#1 em relevância")).toBeInTheDocument();
    expect(screen.getByText("98% compatível")).toBeInTheDocument();
    expect(screen.getByText("Publicada em 01/11/2026")).toBeInTheDocument();
    expect(screen.getByText("Estágio")).toBeInTheDocument();
    expect(screen.getByText("R$ 2.000 – R$ 2.800")).toBeInTheDocument();
    expect(screen.getByText("Frontend")).toBeInTheDocument();
    expect(screen.getByText("Acessibilidade")).toBeInTheDocument();
  });

  it("oculta silenciosamente a lista de requisitos quando a vaga não informar skills", async () => {
    const sugestaoMinima: SugestaoVaga = {
      curriculoId: "curriculo-001",
      vaga: {
        ...sugestao.vaga,
        requisitos: [],
      },
    };

    render(<TelaVagasGrupo2 cliente={criarCliente([sugestaoMinima])} />);
    await screen.findByRole("heading", { name: sugestaoMinima.vaga.titulo });

    expect(
      screen.queryByRole("list", { name: "Competências e requisitos" }),
    ).not.toBeInTheDocument();
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

  it("recupera da falha de busca ao clicar em tentar novamente", async () => {
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

  it("aplica atraso de animacao sequencial em cascata para cada vaga da lista", async () => {
    const lista = [
      sugestao,
      {
        ...sugestao,
        vaga: { ...sugestao.vaga, id: "vaga-002", titulo: "Vaga 2" },
      },
      {
        ...sugestao,
        vaga: { ...sugestao.vaga, id: "vaga-003", titulo: "Vaga 3" },
      },
    ];

    render(<TelaVagasGrupo2 cliente={criarCliente(lista)} />);
    await screen.findByRole("heading", { name: "Vaga 2" });

    const listaVagas = screen.getByRole("list", { name: "Vagas sugeridas" });
    const itens = Array.from(listaVagas.children);
    expect(itens[0]).toHaveStyle({ animationDelay: "0ms" });
    expect(itens[1]).toHaveStyle({ animationDelay: "90ms" });
    expect(itens[2]).toHaveStyle({ animationDelay: "180ms" });
  });
});
