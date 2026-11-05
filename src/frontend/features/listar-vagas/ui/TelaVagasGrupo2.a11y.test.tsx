// Proveniência: decision-analysis prompts/frontend/20261019-073800-vagas-leitor-tela-teclado-v001.md#v001
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

const sugestaoExemplo: SugestaoVaga = {
  curriculoId: "curriculo-407",
  ranque: 1,
  pontuacaoCompatibilidade: 95,
  vaga: {
    id: "vaga-407",
    titulo: "Desenvolvedor Frontend Acessível",
    empresa: "Tech Inclusiva",
    descricao: "Construção de interfaces acessíveis em conformidade com WCAG.",
    requisitos: ["TypeScript", "React", "ARIA"],
    localizacao: "São Paulo - SP",
    modalidade: "Remoto",
    urlCandidatura: "https://exemplo.com/vagas/407",
  },
};

const segundaSugestao: SugestaoVaga = {
  curriculoId: "curriculo-407",
  ranque: 2,
  pontuacaoCompatibilidade: 88,
  vaga: {
    id: "vaga-408",
    titulo: "Engenheiro de Qualidade Web",
    empresa: "Sistemas Seguros",
    descricao: "Automação de testes e validação de acessibilidade.",
    requisitos: ["Vitest", "Playwright"],
    localizacao: "Campinas - SP",
    modalidade: "Híbrido",
    urlCandidatura: "https://exemplo.com/vagas/408",
  },
};

/**
 * Cria um dublê de ClienteVagasGrupo2 para testes isolados de interface.
 */
function criarClienteMock(sugestoes: SugestaoVaga[]): ClienteVagasGrupo2 {
  return { listarSugestoes: vi.fn().mockResolvedValue(sugestoes) };
}

describe("TelaVagasGrupo2 — Acessibilidade e Navegação por Teclado (a11y)", () => {
  it("garante regiões semânticas, lista rotulada e ação principal acessível", async () => {
    const cliente = criarClienteMock([sugestaoExemplo]);
    render(<TelaVagasGrupo2 cliente={cliente} />);

    expect(
      await screen.findByRole("heading", {
        name: sugestaoExemplo.vaga.titulo,
      }),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("region", {
        name: "Oportunidades compatíveis com o seu perfil",
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("list", { name: "Vagas sugeridas" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("list", { name: "Competências e requisitos" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "Acessar vaga original" }),
    ).toBeInTheDocument();
  });

  it("percorre os links de ação dos cartões na ordem lógica via tecla Tab", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteMock([sugestaoExemplo, segundaSugestao]);

    render(<TelaVagasGrupo2 cliente={cliente} />);

    expect(
      await screen.findByRole("heading", {
        name: sugestaoExemplo.vaga.titulo,
      }),
    ).toBeInTheDocument();

    const links = screen.getAllByRole("link", {
      name: "Acessar vaga original",
    });
    expect(links).toHaveLength(2);

    await usuario.tab();
    expect(links[0]).toHaveFocus();

    await usuario.tab();
    expect(links[1]).toHaveFocus();
  });

  it("anuncia o estado de carregamento via live region acessível (role=status)", () => {
    const cliente: ClienteVagasGrupo2 = {
      listarSugestoes: vi.fn(() => new Promise(() => {})),
    };

    render(<TelaVagasGrupo2 cliente={cliente} />);

    const indicadorCarregamento = screen.getByRole("status");
    expect(indicadorCarregamento).toHaveTextContent(
      "Carregando vagas sugeridas...",
    );
  });

  it("comunica o estado vazio com role=status quando nenhuma vaga for localizada", async () => {
    const cliente = criarClienteMock([]);
    render(<TelaVagasGrupo2 cliente={cliente} />);

    await screen.findByRole("heading", {
      name: "Nenhuma vaga compatível no momento",
    });
    const regiaoVazia = screen.getByRole("status");
    expect(regiaoVazia).toBeInTheDocument();
    expect(regiaoVazia).toHaveTextContent("Nenhuma vaga compatível no momento");
    expect(regiaoVazia).toHaveTextContent(
      "Ainda não encontramos oportunidades alinhadas ao seu currículo.",
    );
  });

  it("comunica o estado de erro com role=alert e permite retentativa via teclado", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteVagasGrupo2 = {
      listarSugestoes: vi
        .fn()
        .mockRejectedValueOnce(
          new FalhaVagasGrupo2(
            "indisponivel",
            "Serviço temporariamente fora do ar.",
          ),
        )
        .mockResolvedValueOnce([sugestaoExemplo]),
    };

    render(<TelaVagasGrupo2 cliente={cliente} />);

    const alertaErro = await screen.findByRole("alert");
    expect(alertaErro).toBeInTheDocument();
    expect(alertaErro).toHaveTextContent("Não foi possível carregar as vagas");
    expect(alertaErro).toHaveTextContent(
      "O serviço de vagas está temporariamente indisponível. Tente novamente mais tarde.",
    );

    const botaoTentarNovamente = screen.getByRole("button", {
      name: "Tentar novamente",
    });

    await usuario.tab();
    expect(botaoTentarNovamente).toHaveFocus();

    await usuario.keyboard("{Enter}");

    expect(
      await screen.findByRole("heading", {
        name: sugestaoExemplo.vaga.titulo,
      }),
    ).toBeInTheDocument();
  });
});
