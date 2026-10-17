import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ItemRevisao } from "../model/revisao-curriculo";
import { PainelRevisao } from "./PainelRevisao";

afterEach(cleanup);

const pendenciasMistas: ItemRevisao[] = [
  {
    codigo: "TELEFONE_AUSENTE",
    secao: "dados-pessoais",
    mensagem: "Informe pelo menos um telefone para contato.",
    severidade: "erro",
  },
  {
    codigo: "LINKEDIN_RECOMENDADO",
    secao: "dados-pessoais",
    mensagem: "Adicionar o perfil do LinkedIn aumenta sua visibilidade.",
    severidade: "aviso",
  },
  {
    codigo: "FORMACAO_SEM_STATUS",
    secao: "formacao-academica",
    mensagem: "Informe a situação atual do seu curso superior.",
    severidade: "erro",
  },
  {
    codigo: "DESCRICAO_EXPERIENCIA_CURTA",
    secao: "experiencias-profissionais",
    mensagem: "Considere detalhar melhor as tecnologias utilizadas.",
    severidade: "aviso",
  },
];

describe("PainelRevisao", () => {
  it("agrupa os resultados por seção e subdivide por severidade (erros e avisos)", () => {
    render(<PainelRevisao itens={pendenciasMistas} />);

    expect(
      screen.getByRole("heading", {
        level: 2,
        name: "Painel de revisão do currículo",
      }),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { level: 3, name: "Dados pessoais" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { level: 3, name: "Formação acadêmica" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", {
        level: 3,
        name: "Experiência profissional",
      }),
    ).toBeInTheDocument();

    expect(
      screen.getByText("Informe pelo menos um telefone para contato."),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        "Adicionar o perfil do LinkedIn aumenta sua visibilidade.",
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Informe a situação atual do seu curso superior."),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Considere detalhar melhor as tecnologias utilizadas."),
    ).toBeInTheDocument();

    expect(
      screen.getAllByRole("heading", { level: 4, name: "Erros impeditivos" }),
    ).toHaveLength(2);
    expect(
      screen.getAllByRole("heading", {
        level: 4,
        name: "Recomendações de melhoria",
      }),
    ).toHaveLength(2);
  });

  it("exibe alerta no resumo quando há erros impeditivos", () => {
    render(<PainelRevisao itens={pendenciasMistas} />);

    const alerta = screen.getByRole("alert");
    expect(alerta).toBeInTheDocument();
    expect(alerta).toHaveTextContent(
      "Há 2 erros impeditivos que bloqueiam a aprovação e 2 recomendações.",
    );
  });

  it("exibe status de aprovação quando há apenas recomendações", () => {
    const apenasAvisos: ItemRevisao[] = [
      {
        codigo: "LINKEDIN_RECOMENDADO",
        secao: "dados-pessoais",
        mensagem: "Adicionar LinkedIn é uma boa prática.",
        severidade: "aviso",
      },
    ];

    render(<PainelRevisao itens={apenasAvisos} />);

    const status = screen.getByRole("status");
    expect(status).toHaveTextContent(
      "Currículo aprovado para exportação, com 1 recomendação de melhoria.",
    );
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("exibe mensagem de currículo completo e aprovado quando não há pendências", () => {
    render(<PainelRevisao itens={[]} />);

    const status = screen.getByRole("status");
    expect(status).toHaveTextContent(
      "Nenhuma pendência encontrada. Seu currículo está completo e pronto para exportação.",
    );
    expect(
      screen.getByText("Nenhuma seção possui pendências registradas."),
    ).toBeInTheDocument();
  });

  it("aciona callback onNavegarSecao com a seção correta ao clicar em corrigir", async () => {
    const handleNavegar = vi.fn();
    const user = userEvent.setup();

    render(
      <PainelRevisao itens={pendenciasMistas} onNavegarSecao={handleNavegar} />,
    );

    const botaoDadosPessoais = screen.getByRole("button", {
      name: "Corrigir dados pessoais",
    });
    await user.click(botaoDadosPessoais);

    expect(handleNavegar).toHaveBeenCalledTimes(1);
    expect(handleNavegar).toHaveBeenCalledWith("dados-pessoais");
  });

  it("renderiza ações adicionais em children no rodapé", () => {
    render(
      <PainelRevisao itens={[]}>
        <button type="button">Prosseguir para exportação</button>
      </PainelRevisao>,
    );

    expect(
      screen.getByRole("button", { name: "Prosseguir para exportação" }),
    ).toBeInTheDocument();
  });
});
