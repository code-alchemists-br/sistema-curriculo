/**
 * Integra página, feature, cliente e Zod reais em jsdom para U01–U07.
 * Controla somente a função remota, com estados reais, spies e contraprovas,
 * para caracterizar os desfechos da tela de recomendações de vagas.
 */
// Proveniência: decision-analysis prompts/frontend/20261024-181303-cenario-busca-vagas-tres-desfechos-v001.md#v001
import { act, cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { criarClienteVagasGrupo2 } from "../features/listar-vagas";
import { PaginaVagasGrupo2 } from "../pages/vagas";
import {
  RESPOSTA_API_INCOMPATIVEL,
  RESPOSTA_MALFORMADA,
  RESPOSTA_VAZIA,
  respostaResultado,
  TransporteVagasRegistrado,
  VAGAS,
  type RespostaPendente,
  type VagaSintetica,
} from "./test/fixtures/busca-vagas";

const MENSAGENS = {
  indisponivel:
    "O serviço de vagas está temporariamente indisponível. Tente novamente mais tarde.",
  timeout:
    "O serviço de vagas demorou para responder. Verifique sua conexão e tente novamente.",
  invalida:
    "Recebemos uma resposta inesperada ao consultar as vagas. Tente novamente mais tarde.",
};
const TITULO_ERRO = "Não foi possível carregar as vagas";
const TITULO_VAZIO = "Nenhuma vaga compatível no momento";
const CARREGANDO = "Carregando vagas sugeridas...";

/**
 * Exige cards completos e exclusivos do estado preenchido.
 */
function verificarResultado(vagas: VagaSintetica[] = VAGAS): void {
  const lista = screen.getByRole("list", { name: "Vagas sugeridas" });
  const cards = within(lista).getAllByRole("article");
  expect(cards).toHaveLength(vagas.length);
  expect(lista.children).toHaveLength(vagas.length);
  expect(vagas.length).toBeGreaterThan(0);
  for (const [indice, vaga] of vagas.entries()) {
    const card = within(cards[indice]);
    expect(
      card.getByRole("heading", { level: 2, name: vaga.titulo }),
    ).toBeInTheDocument();
    expect(card.getByText(vaga.empresa, { exact: true })).toBeInTheDocument();
    expect(card.getByText(vaga.descricao, { exact: true })).toBeInTheDocument();
    for (const requisito of vaga.requisitos) {
      expect(card.getByText(requisito, { exact: true })).toBeInTheDocument();
    }
    if (!vaga.requisitos.length) {
      expect(card.queryByRole("list")).not.toBeInTheDocument();
    } else {
      expect(
        within(card.getByRole("list")).getAllByRole("listitem"),
      ).toHaveLength(vaga.requisitos.length);
    }
    if (vaga.localizacao !== null) {
      expect(
        card.getByText(vaga.localizacao, { exact: true }),
      ).toBeInTheDocument();
    }
    if (vaga.modalidade !== null) {
      expect(
        card.getByText(vaga.modalidade, { exact: true }),
      ).toBeInTheDocument();
    }
    if (vaga.url_candidatura === null) {
      expect(card.queryByRole("link")).not.toBeInTheDocument();
    } else {
      expect(
        card.getByRole("link", { name: "Acessar vaga original" }),
      ).toHaveAttribute("href", vaga.url_candidatura);
    }
  }
  expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  expect(screen.queryByRole("status")).not.toBeInTheDocument();
  expect(
    screen.queryByRole("heading", { name: TITULO_VAZIO }),
  ).not.toBeInTheDocument();
}

/**
 * Exige status vazio com título e orientação específicos.
 */
function verificarVazio(): void {
  const estado = screen.getByRole("status", { name: TITULO_VAZIO });
  expect(
    within(estado).getByRole("heading", { name: TITULO_VAZIO }),
  ).toBeInTheDocument();
  expect(estado).toHaveTextContent(
    "Ainda não encontramos oportunidades alinhadas ao seu currículo.",
  );
  expect(estado).toHaveTextContent(
    "Adicione mais competências ou experiências para ampliar suas correspondências.",
  );
  expect(
    screen.queryByRole("list", { name: "Vagas sugeridas" }),
  ).not.toBeInTheDocument();
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  expect(screen.queryByText(CARREGANDO)).not.toBeInTheDocument();
}

/**
 * Exige alert de falha com mensagem literal e retentativa habilitada.
 */
function verificarIndisponibilidade(mensagem = MENSAGENS.indisponivel): void {
  const alerta = screen.getByRole("alert", { name: TITULO_ERRO });
  expect(
    within(alerta).getByRole("heading", { name: TITULO_ERRO }),
  ).toBeInTheDocument();
  expect(
    within(alerta).getByText(mensagem, { exact: true }),
  ).toBeInTheDocument();
  expect(
    within(alerta).getByRole("button", { name: "Tentar novamente" }),
  ).toBeEnabled();
  expect(
    screen.queryByRole("list", { name: "Vagas sugeridas" }),
  ).not.toBeInTheDocument();
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  expect(screen.queryByRole("status")).not.toBeInTheDocument();
  expect(
    screen.queryByRole("heading", { name: TITULO_VAZIO }),
  ).not.toBeInTheDocument();
  expect(alerta).not.toHaveTextContent(
    /https?:|falha-sintetica|Request timed out|stacktrace/,
  );
}

/**
 * Exige status de carregamento e ausência dos três desfechos finais.
 */
function verificarCarregando(): void {
  expect(screen.getByRole("status")).toHaveTextContent(CARREGANDO);
  expect(
    screen.queryByRole("heading", { name: TITULO_VAZIO }),
  ).not.toBeInTheDocument();
  expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
  expect(
    screen.queryByRole("list", { name: "Vagas sugeridas" }),
  ).not.toBeInTheDocument();
}

/**
 * Aplica os mesmos oráculos síncronos aos estados reais incompatíveis.
 */
function verificarSensibilidade(
  estado: "resultado" | "vazio" | "erro" | "carregando",
  vagas: VagaSintetica[] = VAGAS,
  mensagem = MENSAGENS.indisponivel,
): void {
  const verificadores = {
    resultado: () => verificarResultado(vagas),
    vazio: () => verificarVazio(),
    erro: () => verificarIndisponibilidade(mensagem),
    carregando: verificarCarregando,
  };
  for (const [nome, verificar] of Object.entries(verificadores)) {
    if (nome !== estado) {
      expect(
        verificar,
        `Controle aprovado: ${nome} recusa ${estado}`,
      ).toThrow();
    }
  }
  if (estado === "erro") {
    for (const outra of [
      ...Object.values(MENSAGENS),
      "Não foi possível carregar as vagas no momento. Tente novamente mais tarde.",
    ]) {
      if (outra !== mensagem) {
        expect(
          () => verificarIndisponibilidade(outra),
          "Controle aprovado: mensagem de outra modalidade é rejeitada",
        ).toThrow();
      }
    }
  }
}

/**
 * Estabiliza resultado após concluir a função remota prevista.
 */
async function concluirResultado(
  pendente: RespostaPendente,
  vagas = VAGAS,
): Promise<void> {
  await act(async () => pendente.resolver(respostaResultado(vagas)));
  await screen.findByRole("heading", { name: vagas[0].titulo });
  verificarResultado(vagas);
  verificarSensibilidade("resultado", vagas);
}

/**
 * Monta a página com cliente real e resposta inicial pendente.
 */
async function iniciarPagina() {
  const transporte = new TransporteVagasRegistrado();
  const inicial = transporte.enfileirar();
  render(
    <PaginaVagasGrupo2
      cliente={criarClienteVagasGrupo2(transporte.consultar)}
    />,
  );
  await screen.findByText(CARREGANDO);
  verificarCarregando();
  verificarSensibilidade("carregando");
  expect(transporte.chamadas).toEqual([{ termo: "" }]);
  return { transporte, inicial };
}

/**
 * Exercita falha remota e recuperação via botão "Tentar novamente" para U03–U06.
 */
async function exercitarFalha(
  resposta: unknown,
  mensagem: string,
  rejeitar: boolean,
): Promise<void> {
  const { transporte, inicial } = await iniciarPagina();
  await act(async () => {
    if (rejeitar) inicial.rejeitar(resposta);
    else inicial.resolver(resposta);
  });
  await screen.findByRole("alert", { name: TITULO_ERRO });
  verificarIndisponibilidade(mensagem);
  verificarSensibilidade("erro", VAGAS, mensagem);
  expect(transporte.chamadas).toEqual([{ termo: "" }]);

  const recuperacao = transporte.enfileirar();
  await userEvent
    .setup()
    .click(screen.getByRole("button", { name: "Tentar novamente" }));
  await screen.findByText(CARREGANDO);
  verificarCarregando();
  verificarSensibilidade("carregando");
  await concluirResultado(recuperacao);
  expect(transporte.chamadas).toEqual([{ termo: "" }, { termo: "" }]);
  expect(transporte.consultar).toHaveBeenCalledTimes(2);
}

describe("Busca de vagas — página e cliente reais, remoto simulado", () => {
  let fetchBloqueado: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchBloqueado = vi.fn(() => {
      throw new Error("Egress HTTP proibido na busca de vagas.");
    });
    vi.stubGlobal("fetch", fetchBloqueado);
  });

  afterEach(() => {
    try {
      expect(fetchBloqueado).not.toHaveBeenCalled();
    } finally {
      cleanup();
      vi.unstubAllGlobals();
      vi.restoreAllMocks();
    }
  });

  it("U01 — carrega recomendações completas pela página e cliente reais", async () => {
    const { transporte, inicial } = await iniciarPagina();
    await concluirResultado(inicial);
    expect(transporte.chamadas).toEqual([{ termo: "" }]);
    expect(transporte.consultar).toHaveBeenCalledTimes(1);
  });

  it("U02 — aceita estado vazio válido sem resíduos de cartões ou alertas", async () => {
    const { transporte, inicial } = await iniciarPagina();
    await act(async () => inicial.resolver(RESPOSTA_VAZIA));
    await screen.findByRole("heading", { name: TITULO_VAZIO });
    verificarVazio();
    verificarSensibilidade("vazio");
    expect(transporte.chamadas).toEqual([{ termo: "" }]);
    expect(transporte.consultar).toHaveBeenCalledTimes(1);
  });

  it("U03 — comunica indisponibilidade e recupera ao tentar novamente", async () => {
    await exercitarFalha(
      new Error("falha-sintetica https://interno.invalid"),
      MENSAGENS.indisponivel,
      true,
    );
  });

  it("U04 — distingue tempo limite e recupera depois da falha", async () => {
    await exercitarFalha(
      new Error("Request timed out"),
      MENSAGENS.timeout,
      true,
    );
  });

  it("U05 — recusa payload malformado sem cards corrompidos e permite recuperar", async () => {
    await exercitarFalha(RESPOSTA_MALFORMADA, MENSAGENS.invalida, false);
  });

  it("U06 — caracteriza incompatibilidade de vagas/total com associacoes", async () => {
    await exercitarFalha(RESPOSTA_API_INCOMPATIVEL, MENSAGENS.invalida, false);
  });

  it("U07 — default indisponível sem HTTP tem controle positivo com cliente real", async () => {
    render(<PaginaVagasGrupo2 />);
    await screen.findByRole("alert", { name: TITULO_ERRO });
    verificarIndisponibilidade();
    verificarSensibilidade("erro");
    cleanup();
    const { inicial } = await iniciarPagina();
    await concluirResultado(inicial);
  });
});
