/**
 * Integra página, feature, cliente e Zod reais em jsdom para U01–U07.
 * Controla somente a função remota, com estados reais, spies e contraprovas,
 * para caracterizar critérios inferidos do título sem aceite oficial do card.
 * Não é E2E integrado: não há navegador nem página roteada no App; associacoes
 * e vagas/total são incompatíveis, main não liga o executor e o provedor é
 * simulado. Não certifica main.app, login persistido, integração front↔back,
 * layout, responsividade, leitor de tela, acessibilidade integral ou desempenho.
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
const TITULO_VAZIO = "Nenhuma vaga encontrada";
const CARREGANDO = "Carregando vagas sugeridas...";

/**
 * Exige cards completos e exclusivos do estado preenchido.
 * Compara conteúdo, ordem e links no DOM real, excluindo loading/vazio/erro,
 * para não aprovar uma lista residual ou apenas a presença genérica da página.
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
      expect(card.getByText("Requisitos não informados.")).toBeInTheDocument();
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
        card.getByRole("link", { name: "Ver detalhes da vaga" }),
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
 * Exige status vazio com título, critério e orientação específicos.
 * Verifica a conjunção dos textos e ausência de cards/erro/loading para provar
 * que nenhuma vaga é um resultado válido, distinto de estado inicial ou falha.
 */
function verificarVazio(termo = ""): void {
  const estado = screen.getByRole("status", { name: TITULO_VAZIO });
  expect(
    within(estado).getByRole("heading", { name: TITULO_VAZIO }),
  ).toBeInTheDocument();
  expect(estado).toHaveTextContent(
    `Não encontramos vagas sugeridas${termo ? ` para “${termo}”` : ""}.`,
  );
  expect(estado).toHaveTextContent(
    "Você pode ajustar a palavra-chave e pesquisar novamente.",
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
 * Exclui cards, status e vazamento técnico para distinguir cada modalidade
 * de indisponibilidade dos estados saudáveis e das outras mensagens de erro.
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
 * Combina o texto exclusivo com exclusões para não confundir status vazio
 * com consulta pendente, sem inferir tempo de resposta ou latência real.
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
 * Exige toThrow para cada contraste após estabilização e nomeia o controle,
 * impedindo aprovação por coincidência sem fabricar DOM ou ocultar falha principal.
 */
function verificarSensibilidade(
  estado: "resultado" | "vazio" | "erro" | "carregando",
  termo = "",
  vagas: VagaSintetica[] = VAGAS,
  mensagem = MENSAGENS.indisponivel,
): void {
  const verificadores = {
    /** Reaplica o oráculo de resultado à árvore atual para detectar contraste inválido. */
    resultado: () => verificarResultado(vagas),
    /** Reaplica o oráculo de vazio com os critérios da consulta para medir sensibilidade. */
    vazio: () => verificarVazio(termo),
    /** Reaplica o oráculo de falha literal para excluir aprovação em estado saudável. */
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
          /** Reaplica a mensagem errada ao alert real para distinguir modalidades de falha. */
          () => verificarIndisponibilidade(outra),
          "Controle aprovado: mensagem de outra modalidade é rejeitada",
        ).toThrow();
      }
    }
  }
}

/**
 * Estabiliza resultado após concluir a função remota prevista.
 * Resolve a promise dentro de act e aguarda o heading antes do oráculo síncrono
 * para que sucesso e seus contrastes observem somente o DOM de produção atualizado.
 */
async function concluirResultado(
  pendente: RespostaPendente,
  vagas = VAGAS,
): Promise<void> {
  await act(
    /** Conclui a resposta remota para descarregar os efeitos React sem timers. */
    async () => pendente.resolver(respostaResultado(vagas)),
  );
  await screen.findByRole("heading", { name: vagas[0].titulo });
  verificarResultado(vagas);
  verificarSensibilidade("resultado", "", vagas);
}

/**
 * Monta a página com cliente real e resposta inicial pendente.
 * Conecta somente a função remota simulada e aguarda loading para estabelecer
 * controles de estado e passagem da busca automática pelo cliente/schema reais.
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
 * Submete uma palavra-chave mantendo o transporte pendente controlável.
 * Enfileira antes do clique e usa formulário real para verificar trim sem
 * substituir handlers, cliente ou regras de apresentação da feature.
 */
async function pesquisar(
  transporte: TransporteVagasRegistrado,
  termo: string,
): Promise<RespostaPendente> {
  const usuario = userEvent.setup();
  const pendente = transporte.enfileirar();
  const campo = screen.getByRole("searchbox", { name: "Palavra-chave" });
  await usuario.clear(campo);
  await usuario.type(campo, termo);
  await usuario.click(screen.getByRole("button", { name: "Pesquisar vagas" }));
  await screen.findByText(CARREGANDO);
  verificarCarregando();
  verificarSensibilidade("carregando", termo.trim());
  return pendente;
}

/**
 * Exercita controle positivo, falha e recuperação para U03–U06.
 * Submete Python, conclui a promise com rejeição ou payload inválido e repete
 * via botão real para provar causa, preservação de critérios e sensibilidade.
 */
async function exercitarFalha(
  resposta: unknown,
  mensagem: string,
  rejeitar: boolean,
): Promise<void> {
  const { transporte, inicial } = await iniciarPagina();
  await concluirResultado(inicial);
  const pendente = await pesquisar(transporte, "Python");
  await act(
    /** Entrega a falha prevista à fronteira remota sem interceptar o cliente real. */
    async () => {
      if (rejeitar) pendente.rejeitar(resposta);
      else pendente.resolver(resposta);
    },
  );
  await screen.findByRole("alert", { name: TITULO_ERRO });
  verificarIndisponibilidade(mensagem);
  verificarSensibilidade("erro", "Python", VAGAS, mensagem);
  expect(screen.getByRole("searchbox", { name: "Palavra-chave" })).toHaveValue(
    "Python",
  );
  expect(transporte.chamadas).toEqual([{ termo: "" }, { termo: "Python" }]);
  const recuperacao = transporte.enfileirar();
  await userEvent
    .setup()
    .click(screen.getByRole("button", { name: "Tentar novamente" }));
  await screen.findByText(CARREGANDO);
  verificarCarregando();
  verificarSensibilidade("carregando", "Python");
  await concluirResultado(recuperacao);
  expect(screen.getByRole("searchbox", { name: "Palavra-chave" })).toHaveValue(
    "Python",
  );
  expect(transporte.chamadas).toEqual([
    { termo: "" },
    { termo: "Python" },
    { termo: "Python" },
  ]);
  expect(transporte.consultar).toHaveBeenCalledTimes(3);
}

/**
 * Agrupa U01–U07 com página e cliente reais em integração DOM.
 * Isola rede, DOM e mocks por método para provar os três desfechos e seus
 * controles, sem reivindicar navegador ou contrato produtivo entre as pontas.
 */
describe("Busca de vagas — página e cliente reais, remoto simulado", () => {
  let fetchBloqueado: ReturnType<typeof vi.fn>;

  /** Bloqueia egress com mock verificado para detectar até chamadas capturadas pelo produto. */
  beforeEach(() => {
    fetchBloqueado = vi.fn(
      /** Recusa HTTP real para preservar o isolamento das respostas simuladas. */
      () => {
        throw new Error("Egress HTTP proibido na busca de vagas.");
      },
    );
    vi.stubGlobal("fetch", fetchBloqueado);
  });

  /**
   * Limpa a página e restaura mocks de cada cenário.
   * Verifica egress e executa cleanup em finally para manter o isolamento
   * mesmo quando uma asserção detecta HTTP inesperado.
   */
  afterEach(() => {
    try {
      expect(fetchBloqueado).not.toHaveBeenCalled();
    } finally {
      cleanup();
      vi.unstubAllGlobals();
      vi.restoreAllMocks();
    }
  });

  /**
   * Verifica U01: carregamento, resultado e refinamento positivo.
   * Resolve promises antes/depois do submit real e confere DOM e spy,
   * para provar trim do critério sem apagar os espaços digitados no input.
   */
  it("U01 — carrega resultado e refina termo pelo formulário e cliente reais", async () => {
    const { transporte, inicial } = await iniciarPagina();
    await concluirResultado(inicial);
    const pesquisa = await pesquisar(transporte, "  Python  ");
    expect(
      screen.getByRole("searchbox", { name: "Palavra-chave" }),
    ).toHaveValue("  Python  ");
    await concluirResultado(pesquisa, [VAGAS[0]]);
    expect(
      screen.getByRole("searchbox", { name: "Palavra-chave" }),
    ).toHaveValue("  Python  ");
    expect(transporte.chamadas).toEqual([{ termo: "" }, { termo: "Python" }]);
    expect(transporte.consultar).toHaveBeenCalledTimes(2);
  });

  /**
   * Verifica U02: vazio válido e refinamento para QA.
   * Alterna resultado/vazio/resultado na página e reaplica oráculos errados,
   * para provar preservação do termo e exclusão de cards residuais ou erro.
   */
  it("U02 — aceita vazio válido, preserva termo e refina para QA sem resíduos", async () => {
    const { transporte, inicial } = await iniciarPagina();
    await concluirResultado(inicial);
    const termo = "sem-correspondencia-sintetica";
    const vazio = await pesquisar(transporte, termo);
    await act(
      /** Resolve lista vazia válida para exercitar o estado de ausência da página real. */
      async () => vazio.resolver(RESPOSTA_VAZIA),
    );
    await screen.findByRole("heading", { name: TITULO_VAZIO });
    verificarVazio(termo);
    verificarSensibilidade("vazio", termo);
    expect(
      screen.getByRole("searchbox", { name: "Palavra-chave" }),
    ).toHaveValue(termo);
    await concluirResultado(await pesquisar(transporte, "QA"), [VAGAS[1]]);
    expect(
      screen.queryByRole("heading", { name: VAGAS[0].titulo }),
    ).not.toBeInTheDocument();
    expect(transporte.chamadas).toEqual([
      { termo: "" },
      { termo },
      { termo: "QA" },
    ]);
    expect(transporte.consultar).toHaveBeenCalledTimes(3);
  });

  /**
   * Verifica U03: indisponibilidade remota sanitizada.
   * Rejeita a promise com erro técnico e repete a consulta pelo botão real,
   * para provar mensagem segura, critérios preservados e recuperação positiva.
   */
  it("U03 — comunica indisponibilidade e recupera com os mesmos critérios", async () => {
    await exercitarFalha(
      new Error("falha-sintetica https://interno.invalid"),
      MENSAGENS.indisponivel,
      true,
    );
  });

  /**
   * Verifica U04: timeout com mensagem específica de demora.
   * Rejeita a função remota com texto reconhecido pelo cliente e tenta de novo,
   * para distinguir timeout de falha genérica e provar recuperação sem espera.
   */
  it("U04 — distingue tempo limite e recupera depois da falha", async () => {
    await exercitarFalha(
      new Error("Request timed out"),
      MENSAGENS.timeout,
      true,
    );
  });

  /**
   * Verifica U05: schema malformado recusado pelo cliente real.
   * Resolve a função remota com objeto incompleto e depois com resposta válida,
   * para provar a recusa do Zod sem cards corrompidos e com recuperação.
   */
  it("U05 — recusa payload malformado sem cards corrompidos e permite recuperar", async () => {
    await exercitarFalha(RESPOSTA_MALFORMADA, MENSAGENS.invalida, false);
  });

  /**
   * Caracteriza U06: incompatibilidade entre os dois contratos atuais.
   * Entrega o envelope vagas/total e depois o envelope aceito pela mesma página,
   * para provar a causa da recusa sem implementar ponte ou alegar parceiro real.
   */
  it("U06 — caracteriza incompatibilidade de vagas/total com associacoes", async () => {
    await exercitarFalha(RESPOSTA_API_INCOMPATIVEL, MENSAGENS.invalida, false);
  });

  /**
   * Caracteriza U07: busca inicial automática com termo vazio.
   * Mantém a promise pendente e depois resolve sem sugestões, verificando spy,
   * para distinguir loading e resposta vazia de um suposto estado ocioso.
   */
  it("U07 — busca automaticamente com termo vazio e depois apresenta vazio válido", async () => {
    const { transporte, inicial } = await iniciarPagina();
    await act(
      /** Conclui a consulta automática como vazio para distinguir resposta de ausência de pesquisa. */
      async () => inicial.resolver(RESPOSTA_VAZIA),
    );
    await screen.findByRole("heading", { name: TITULO_VAZIO });
    verificarVazio();
    verificarSensibilidade("vazio");
    expect(transporte.chamadas).toEqual([{ termo: "" }]);
    expect(transporte.consultar).toHaveBeenCalledTimes(1);
  });

  /**
   * Caracteriza U07: default indisponível sem chamada HTTP.
   * Monta a página default e contrasta com montagem de cliente real saudável,
   * para provar a limitação da composição local sem uma tela que sempre falha.
   */
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
