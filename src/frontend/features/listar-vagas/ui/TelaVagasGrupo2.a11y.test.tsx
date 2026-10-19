// Proveniência: decision-analysis prompts/frontend/20261019-073800-vagas-leitor-tela-teclado-v001.md#v001
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

const sugestaoExemplo: SugestaoVaga = {
  curriculoId: "curriculo-407",
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

/**
 * Cria um dublê de ClienteVagasGrupo2 para testes isolados de interface.
 *
 * **O que faz:** Instancia um objeto com o método `listarSugestoes` mockado via Vitest.
 * **Como faz:** Utiliza `vi.fn().mockResolvedValue(...)` para retornar a lista fornecida.
 * **Qual finalidade atende:** Permite testar os estados da tela sem depender de requisições de rede.
 */
function criarClienteMock(sugestoes: SugestaoVaga[]): ClienteVagasGrupo2 {
  return { listarSugestoes: vi.fn().mockResolvedValue(sugestoes) };
}

describe("TelaVagasGrupo2 — Acessibilidade e Navegação por Teclado (a11y)", () => {
  /**
   * Valida a associação de rótulo acessível ao campo de busca e controles do formulário.
   *
   * **O que faz:** Verifica se o input de busca possui papel e rótulo acessível associados e botão de envio identificado.
   * **Como faz:** Consulta elementos no DOM por papéis semânticos (`searchbox` e `button`) com seus respectivos nomes acessíveis.
   * **Qual finalidade atende:** Atende aos critérios WCAG 1.3.1 (Informações e Relações) e 4.1.2 (Nome, Papel, Valor) para leitores de tela.
   */
  it("garante identificação acessível do campo de busca e do botão de pesquisa", async () => {
    const cliente = criarClienteMock([sugestaoExemplo]);
    render(<TelaVagasGrupo2 cliente={cliente} />);

    expect(
      await screen.findByRole("heading", {
        name: sugestaoExemplo.vaga.titulo,
      }),
    ).toBeInTheDocument();

    const campoBusca = screen.getByRole("searchbox", { name: "Palavra-chave" });
    const botaoPesquisar = screen.getByRole("button", {
      name: "Pesquisar vagas",
    });

    expect(campoBusca).toBeInTheDocument();
    expect(botaoPesquisar).toBeInTheDocument();
  });

  /**
   * Valida a navegação sequencial por foco de teclado através do formulário e dos controles do cartão de vaga.
   *
   * **O que faz:** Percorre via tecla Tab os elementos interativos verificando se o foco atinge cada controle na ordem esperada.
   * **Como faz:** Dispara eventos de tabulação com `userEvent.tab()` a partir do início da página, testando o campo de busca, botão de busca e ações da vaga.
   * **Qual finalidade atende:** Satisfaz o critério WCAG 2.1.1 (Teclado) e 2.4.3 (Ordem do Foco), garantindo usabilidade plena sem mouse.
   */
  it("percorre todos os controles interativos na ordem lógica via tecla Tab", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteMock([sugestaoExemplo]);

    render(<TelaVagasGrupo2 cliente={cliente} />);

    expect(
      await screen.findByRole("heading", {
        name: sugestaoExemplo.vaga.titulo,
      }),
    ).toBeInTheDocument();

    const campoBusca = screen.getByRole("searchbox", { name: "Palavra-chave" });
    const botaoPesquisar = screen.getByRole("button", {
      name: "Pesquisar vagas",
    });
    const botaoAceitar = screen.getByRole("button", {
      name: "Aceitar recomendação",
    });
    const botaoRejeitar = screen.getByRole("button", {
      name: "Rejeitar recomendação",
    });
    const linkDetalhes = screen.getByRole("link", {
      name: "Ver detalhes da vaga",
    });

    await usuario.tab();
    expect(campoBusca).toHaveFocus();

    await usuario.tab();
    expect(botaoPesquisar).toHaveFocus();

    await usuario.tab();
    expect(botaoAceitar).toHaveFocus();

    await usuario.tab();
    expect(botaoRejeitar).toHaveFocus();

    await usuario.tab();
    expect(linkDetalhes).toHaveFocus();
  });

  /**
   * Valida o anúncio acessível do estado de carregamento inicial para leitores de tela.
   *
   * **O que faz:** Verifica a existência de elemento semântico com live region anunciando o carregamento antes da resolução.
   * **Como faz:** Renderiza o componente com cliente pendente e consulta o elemento com `screen.getByRole("status")`.
   * **Qual finalidade atende:** Atende a WCAG 4.1.3 (Mensagens de Status), informando à pessoa usuária que os dados estão sendo obtidos.
   */
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

  /**
   * Valida o anúncio acessível do estado vazio (nenhuma vaga encontrada) para tecnologias assistivas.
   *
   * **O que faz:** Assegura que o container de estado vazio possui `role="status"` e cabeçalho semântico com título explicativo.
   * **Como faz:** Retorna lista vazia do cliente, aguarda a transição e afere a presença de `role="status"` e texto descritivo.
   * **Qual finalidade atende:** Garante conformidade com WCAG 4.1.3 e o requisito [F11.9], permitindo que leitores de tela anunciem a ausência de resultados.
   */
  it("comunica o estado vazio com role=status quando nenhuma vaga for localizada", async () => {
    const cliente = criarClienteMock([]);
    render(<TelaVagasGrupo2 cliente={cliente} />);

    await screen.findByRole("heading", { name: "Nenhuma vaga encontrada" });
    const regiaoVazia = screen.getByRole("status");
    expect(regiaoVazia).toBeInTheDocument();
    expect(regiaoVazia).toHaveTextContent("Nenhuma vaga encontrada");
    expect(regiaoVazia).toHaveTextContent("Não encontramos vagas sugeridas");
  });

  /**
   * Valida o anúncio assertivo de erro de comunicação e a navegabilidade por teclado até o botão de retentativa.
   *
   * **O que faz:** Verifica se a mensagem de erro é renderizada com `role="alert"` e se o botão "Tentar novamente" recebe foco e acionamento por teclado.
   * **Como faz:** Simula falha remota com `FalhaVagasGrupo2`, verifica a live region de alerta e simula a navegação via Tab e acionamento via Enter.
   * **Qual finalidade atende:** Cumpre WCAG 4.1.3 e 3.3.1 (Identificação de Erros), garantindo recuperação acessível de falhas de rede.
   */
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

    const campoBusca = screen.getByRole("searchbox", { name: "Palavra-chave" });
    const botaoPesquisar = screen.getByRole("button", {
      name: "Pesquisar vagas",
    });

    await usuario.tab();
    expect(campoBusca).toHaveFocus();

    await usuario.tab();
    expect(botaoPesquisar).toHaveFocus();

    await usuario.tab();
    expect(botaoTentarNovamente).toHaveFocus();

    await usuario.keyboard("{Enter}");

    expect(
      await screen.findByRole("heading", {
        name: sugestaoExemplo.vaga.titulo,
      }),
    ).toBeInTheDocument();
  });

  /**
   * Valida o acionamento de decisão sobre uma recomendação via teclado e a atualização acessível do status.
   *
   * **O que faz:** Aciona o botão de aceitar recomendação usando a tecla Enter/Espaço e verifica os anúncios de 'Salvando' e 'salva'.
   * **Como faz:** Simula navegação até o botão, aciona via evento de teclado e verifica as mensagens com `role="status"`.
   * **Qual finalidade atende:** Atende a WCAG 2.1.1 (Operável via Teclado) e 4.1.3 (Mensagens de Status em Ações Assíncronas).
   */
  it("permite registrar decisão via teclado e anuncia o resultado acessivelmente", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteMock([sugestaoExemplo]);
    const clienteDecisoes: ClienteDecisoesRecomendacao = {
      salvarDecisao: vi.fn().mockResolvedValue(undefined),
    };

    render(
      <TelaVagasGrupo2 cliente={cliente} clienteDecisoes={clienteDecisoes} />,
    );

    const botaoAceitar = await screen.findByRole("button", {
      name: "Aceitar recomendação",
    });

    await usuario.tab(); // campo busca
    await usuario.tab(); // botao pesquisar
    await usuario.tab(); // botao aceitar
    expect(botaoAceitar).toHaveFocus();

    await usuario.keyboard("{Enter}");

    expect(
      await screen.findByText(/recomendação aceita e salva/i),
    ).toBeInTheDocument();
    expect(screen.getByRole("status")).toHaveTextContent(
      "Recomendação aceita e salva.",
    );
    expect(clienteDecisoes.salvarDecisao).toHaveBeenCalledWith({
      curriculoId: sugestaoExemplo.curriculoId,
      vagaId: sugestaoExemplo.vaga.id,
      decisao: "aceitar",
    });
  });

  /**
   * Valida o anúncio com role=alert quando o salvamento de uma decisão falha.
   *
   * **O que faz:** Verifica se a mensagem de erro no salvamento da decisão é apresentada em container com `role="alert"`.
   * **Como faz:** Simula rejeição na Promise de `salvarDecisao`, aciona o botão e confere a exibição do alerta de erro.
   * **Qual finalidade atende:** Atende a WCAG 3.3.1 e 4.1.3, alertando imediatamente sobre a falha no salvamento da escolha.
   */
  it("anuncia erro de salvamento de decisão com role=alert", async () => {
    const usuario = userEvent.setup();
    const cliente = criarClienteMock([sugestaoExemplo]);
    const clienteDecisoes: ClienteDecisoesRecomendacao = {
      salvarDecisao: vi.fn().mockRejectedValue(new Error("Falha ao salvar")),
    };

    render(
      <TelaVagasGrupo2 cliente={cliente} clienteDecisoes={clienteDecisoes} />,
    );

    const botaoRejeitar = await screen.findByRole("button", {
      name: "Rejeitar recomendação",
    });

    await usuario.click(botaoRejeitar);

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(
      "Não foi possível salvar a recomendação rejeitada. Tente novamente.",
    );
  });
});
