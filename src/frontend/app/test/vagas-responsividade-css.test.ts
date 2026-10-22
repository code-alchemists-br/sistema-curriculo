// Proveniência: decision-analysis prompts/frontend/20261021-205543-validacao-vagas-largura-movel-f11-v002.md#v002
// @ts-expect-error TS2591: @types/node ausente; o builtin é fornecido pelo Node do Nix e recebe assinatura local abaixo.
import { readFileSync as lerArquivoNode } from "node:fs";
// @ts-expect-error TS2591: mesma fronteira builtin sem tipos instalados; não exige dependência nova.
import { URL as URLArquivoNode } from "node:url";
import { beforeAll, describe, expect, it, type TestContext } from "vitest";

/** Limita a leitura builtin a URL e UTF-8; tipa sua saída para verificar o restante da suíte sem @types/node. */
const readFileSync: (url: URL, codificacao: "utf8") => string = lerArquivoNode;
/** Tipifica o construtor builtin com a interface URL do DOM para resolver arquivos sem transformação de assets. */
const URLArquivo: typeof URL = URLArquivoNode;

/** Descreve um alvo CSS; associa seletor e propriedade para limitar a caracterização. */
interface Alvo {
  seletor: string;
  propriedade: string;
  base: string;
  movel: string;
}

/** Guarda declarações extraídas em ordem; conserva a mídia para avaliar o regime sem layout. */
interface Declaracao {
  seletor: string;
  propriedade: string;
  valor: string;
  media: string | null;
}

/** Identifica cada folha e seus oráculos literais para verificar somente o CSS autorizado. */
interface Fonte {
  nome: string;
  url: URL;
  alvos: Alvo[];
  esperados: Record<number, string[]>;
}

/** Registra a entrada e a seleção estática para evidenciar o que foi efetivamente avaliado. */
interface Avaliacao {
  larguraPx: number;
  baseRemPx: number;
  mediaText: string;
  limiarPx: number;
  ativa: boolean;
  valores: string[];
}

type CaminhoCssom = "CSSStyleSheet.replaceSync" | "style.sheet.cssRules";

const BASE_REM_PX = 16;
const LARGURAS_F11 = [360, 480, 640];
const FIXTURE =
  ".calibracao { padding: 2rem } @media (max-width: 30rem) { .calibracao { padding: 1rem } }";
const MOTIVO_CSSOM = "CSSOM indisponível para caracterização";
const FONTES: Fonte[] = [
  {
    nome: "vagas",
    // O alias Node evita que o Vite transforme new URL de CSS em URL HTTP de asset.
    url: new URLArquivo(
      "../../features/listar-vagas/ui/TelaVagasGrupo2.css",
      import.meta.url,
    ),
    alvos: [
      {
        seletor: ".vagas-grupo2__pesquisa",
        propriedade: "grid-template-columns",
        base: "minmax(0, 1fr) auto",
        movel: "1fr",
      },
      {
        seletor: ".vagas-grupo2__pesquisa label",
        propriedade: "grid-column",
        base: "1 / -1",
        movel: "auto",
      },
    ],
    // Caracterização literal do CSS atual, não aceite de produto.
    esperados: {
      360: ["1fr", "auto"],
      480: ["1fr", "auto"],
      640: ["minmax(0, 1fr) auto", "1 / -1"],
    },
  },
  {
    nome: "shell",
    url: new URLArquivo("../styles/global.css", import.meta.url),
    alvos: [
      {
        seletor: ".app-shell",
        propriedade: "padding",
        base: "1.5rem",
        movel: "0.75rem",
      },
      {
        seletor: ".app-shell__content",
        propriedade: "padding",
        base: "2rem",
        movel: "1.25rem",
      },
    ],
    esperados: {
      360: ["0.75rem", "1.25rem"],
      480: ["0.75rem", "1.25rem"],
      640: ["1.5rem", "2rem"],
    },
  },
];

let caminho: CaminhoCssom | null = null;

/**
 * Identifica uma divergência de caracterização; inclui alvo, entrada e valores
 * na mensagem para distinguir falhas esperadas dos mutantes de erros de parsing.
 */
class FalhaVerificacao extends Error {
  /** Constrói o diagnóstico comparando valores do alvo para provar a sensibilidade do ensaio. */
  constructor(alvo: Alvo, largura: number, detalhe: string) {
    super(`${alvo.seletor} | ${alvo.propriedade} | ${largura}px | ${detalhe}`);
    this.name = "FalhaVerificacao";
  }
}

/** Normaliza apenas espaços dos valores; preserva o conteúdo para comparar serializações CSSOM. */
function normalizar(valor: string): string {
  return valor.trim().replace(/\s+/g, " ");
}

/**
 * Analisa texto pelas APIs públicas; retira somente o import conhecido de tokens
 * e limpa o style alternativo para não buscar recursos nem deixar estado entre casos.
 */
function analisarCss(texto: string, modo: CaminhoCssom): CSSRule[] {
  const semImport = texto.replace(
    /^\s*@import\s+["']\.\.\/\.\.\/shared\/styles\/tokens\.css["'];\s*$/m,
    "",
  );
  if (/@import\b/i.test(semImport)) {
    throw new Error(
      "Método não suportado: @import diferente do token local conhecido",
    );
  }
  if (modo === "CSSStyleSheet.replaceSync") {
    const folha = new CSSStyleSheet();
    folha.replaceSync(semImport);
    return Array.from(folha.cssRules);
  }
  const estilo = document.createElement("style");
  try {
    estilo.textContent = semImport;
    document.head.append(estilo);
    if (!estilo.sheet) throw new Error("Folha CSSOM não criada");
    return Array.from(estilo.sheet.cssRules);
  } finally {
    estilo.remove();
  }
}

/**
 * Seleciona um caminho público com a fixture válida; tenta construção e depois
 * style, registrando indisponibilidade para permitir somente skips justificados.
 */
function detectarCssom(): CaminhoCssom | null {
  const tentativas: CaminhoCssom[] = [
    "CSSStyleSheet.replaceSync",
    "style.sheet.cssRules",
  ];
  for (const modo of tentativas) {
    try {
      const regras = analisarCss(FIXTURE, modo);
      const base = regras[0] as CSSStyleRule;
      const media = regras[1] as CSSMediaRule;
      const movel = media.cssRules[0] as CSSStyleRule;
      if (
        regras.length !== 2 ||
        base.type !== CSSRule.STYLE_RULE ||
        base.style.getPropertyValue("padding") !== "2rem" ||
        media.type !== CSSRule.MEDIA_RULE ||
        normalizar(media.media.mediaText) !== "(max-width: 30rem)" ||
        movel.style.getPropertyValue("padding") !== "1rem"
      ) {
        throw new Error("Fixture válida não preservada no CSSOM");
      }
      return modo;
    } catch (erro) {
      console.info("S0 caminho indisponível", modo, String(erro));
    }
  }
  return null;
}

/** Exige a calibração pública; usa o motivo explícito no contexto para não aprovar casos sem CSSOM. */
function exigirCssom(contexto: TestContext): CaminhoCssom {
  if (caminho === null) return contexto.skip(MOTIVO_CSSOM);
  return caminho;
}

/**
 * Avalia apenas max-width em rem/px; usa largura e base explícitas com limite
 * inclusivo para caracterizar a condição sem simular o motor de mídia do jsdom.
 */
function avaliarMedia(media: string, larguraPx: number, baseRemPx: number) {
  const partes = /^\(\s*max-width\s*:\s*(\d+(?:\.\d+)?)(rem|px)\s*\)$/i.exec(
    media,
  );
  if (
    !partes ||
    !Number.isFinite(larguraPx) ||
    !Number.isFinite(baseRemPx) ||
    larguraPx <= 0 ||
    baseRemPx <= 0
  ) {
    throw new Error(`Método não suportado: condição ou entrada ${media}`);
  }
  const limiarPx =
    Number(partes[1]) * (partes[2].toLowerCase() === "rem" ? baseRemPx : 1);
  return { larguraPx, baseRemPx, limiarPx, ativa: larguraPx <= limiarPx };
}

/**
 * Detecta propriedades e shorthands que podem concorrer; examina nomes CSSOM
 * para recusar cascata fora do contrato em vez de ignorar overrides relevantes.
 */
function propriedadesRelacionadas(
  estilo: CSSStyleDeclaration,
  propriedade: string,
): string[] {
  const relacionadas: string[] = [];
  // jsdom enumera os quatro longhands mesmo quando a origem é `padding: 2rem`.
  // Aceitamos só a recomposição uniforme; override desigual exige método novo.
  const padding = estilo.getPropertyValue("padding");
  if (propriedade === "padding" && padding) {
    if (/\s/.test(padding.trim())) {
      throw new Error("Método não suportado: padding com lados distintos");
    }
    relacionadas.push("padding");
  }
  for (const nome of Array.from(estilo)) {
    if (
      propriedade === "padding" &&
      padding &&
      [
        "padding",
        "padding-top",
        "padding-right",
        "padding-bottom",
        "padding-left",
      ].includes(nome)
    )
      continue;
    if (
      nome === "all" ||
      nome === propriedade ||
      (propriedade === "padding" && nome.startsWith("padding-")) ||
      (propriedade === "grid-template-columns" &&
        ["grid", "grid-template"].includes(nome)) ||
      (propriedade === "grid-column" &&
        ["grid", "grid-area", "grid-column-start", "grid-column-end"].includes(
          nome,
        ))
    ) {
      relacionadas.push(nome);
    }
  }
  return relacionadas;
}

/**
 * Verifica possível concorrência de seletor; cruza classes exatas e uma sonda
 * sem layout para rejeitar seletores amplos ou variantes sem implementar especificidade.
 */
function podeConcorrer(seletor: string, alvo: Alvo): boolean {
  const classesAlvo: string[] = alvo.seletor.match(/\.[\w-]+/g) ?? [];
  const classesRegra: string[] = seletor.match(/\.[\w-]+/g) ?? [];
  for (const classe of classesAlvo) {
    if (classesRegra.includes(classe)) return true;
  }
  const sonda = document.createElement("main");
  sonda.className = "app-shell";
  sonda.innerHTML =
    '<div class="app-shell__content"><section class="vagas-grupo2"><form class="vagas-grupo2__pesquisa"><label></label></form></section></div>';
  const elemento = sonda.matches(alvo.seletor)
    ? sonda
    : sonda.querySelector(alvo.seletor);
  if (elemento?.matches(seletor)) return true;
  // A calibração também possui um alvo próprio, sem montar a página de produção.
  const calibracao = document.createElement("div");
  calibracao.className = "calibracao";
  return alvo.seletor === ".calibracao" && calibracao.matches(seletor);
}

/**
 * Extrai declarações na ordem de origem; aceita só base e uma mídia simples,
 * recusando concorrência, prioridades, nesting e at-rules não modeladas para não dar falso verde.
 */
function extrair(
  regras: CSSRule[],
  alvos: Alvo[],
  media: string | null = null,
): Declaracao[] {
  const declaracoes: Declaracao[] = [];
  for (const regra of regras) {
    if (regra.type === CSSRule.MEDIA_RULE) {
      if (media !== null)
        throw new Error("Método não suportado: mídia aninhada");
      const bloco = regra as CSSMediaRule;
      avaliarMedia(bloco.media.mediaText, 1, BASE_REM_PX);
      declaracoes.push(
        ...extrair(Array.from(bloco.cssRules), alvos, bloco.media.mediaText),
      );
      continue;
    }
    if (regra.type !== CSSRule.STYLE_RULE) {
      throw new Error(`Método não suportado: at-rule tipo ${regra.type}`);
    }
    const estilo = regra as CSSStyleRule;
    if ("cssRules" in estilo && (estilo as CSSGroupingRule).cssRules.length) {
      throw new Error("Método não suportado: nesting CSS");
    }
    for (const alvo of alvos) {
      for (const seletorBruto of estilo.selectorText.split(",")) {
        const seletor = normalizar(seletorBruto);
        if (!podeConcorrer(seletor, alvo)) continue;
        const propriedades = propriedadesRelacionadas(
          estilo.style,
          alvo.propriedade,
        );
        if (!propriedades.length) continue;
        if (seletor !== alvo.seletor) {
          throw new Error(
            `Método não suportado: seletor concorrente ${seletor}`,
          );
        }
        for (const propriedade of propriedades) {
          if (
            propriedade !== alvo.propriedade ||
            estilo.style.getPropertyPriority(propriedade)
          ) {
            throw new Error(
              `Método não suportado: propriedade/prioridade ${seletor} ${propriedade}`,
            );
          }
          declaracoes.push({
            seletor,
            propriedade,
            media,
            valor: normalizar(estilo.style.getPropertyValue(propriedade)),
          });
        }
      }
    }
  }
  return declaracoes;
}

/**
 * Seleciona valores por ordem de origem e condição; devolve entradas e mídia
 * extraídas para comprovar a avaliação estática, sem largura ou geometria fictícia.
 */
function avaliar(
  declaracoes: Declaracao[],
  alvos: Alvo[],
  larguraPx: number,
  baseRemPx: number,
): Avaliacao {
  const valores: string[] = [];
  let mediaText = "";
  let limiarPx = 0;
  let ativa = false;
  for (const alvo of alvos) {
    let valor = "";
    for (const declaracao of declaracoes) {
      if (
        declaracao.seletor !== alvo.seletor ||
        declaracao.propriedade !== alvo.propriedade
      )
        continue;
      if (declaracao.media === null) {
        valor = declaracao.valor;
      } else {
        if (mediaText && mediaText !== declaracao.media)
          throw new Error(
            "Método não suportado: múltiplas condições para os alvos",
          );
        mediaText = declaracao.media;
        const condicao = avaliarMedia(mediaText, larguraPx, baseRemPx);
        limiarPx = condicao.limiarPx;
        ativa = condicao.ativa;
        if (ativa) valor = declaracao.valor;
      }
    }
    valores.push(valor);
  }
  return { larguraPx, baseRemPx, mediaText, limiarPx, ativa, valores };
}

/** Compara um campo do contrato; lança diagnóstico tipado com alvo e largura para validar os mutantes. */
function conferir(
  alvo: Alvo,
  largura: number,
  campo: string,
  obtido: unknown,
  esperado: unknown,
): void {
  if (obtido !== esperado) {
    throw new FalhaVerificacao(
      alvo,
      largura,
      `${campo}: esperado ${String(esperado)}, obtido ${String(obtido)}`,
    );
  }
}

/**
 * Verifica original e mutantes com os mesmos oráculos literais; compara valores
 * antes dos metadados para demonstrar que 40rem seleciona o regime errado em 640px.
 */
function verificar(
  regras: CSSRule[],
  fonte: Fonte,
  largura: number,
  base: number,
): Avaliacao {
  const declaracoes = extrair(regras, fonte.alvos);
  const resultado = avaliar(declaracoes, fonte.alvos, largura, base);
  for (let indice = 0; indice < fonte.alvos.length; indice++) {
    const alvo = fonte.alvos[indice];
    conferir(
      alvo,
      largura,
      "valor selecionado",
      resultado.valores[indice],
      fonte.esperados[largura][indice],
    );
    let valorBase = "";
    let valorMovel = "";
    for (const declaracao of declaracoes) {
      if (
        declaracao.seletor === alvo.seletor &&
        declaracao.propriedade === alvo.propriedade
      ) {
        if (declaracao.media === null) valorBase = declaracao.valor;
        else valorMovel = declaracao.valor;
      }
    }
    conferir(alvo, largura, "base preservada", valorBase, alvo.base);
    conferir(
      alvo,
      largura,
      "declaração dentro da mídia",
      valorMovel,
      alvo.movel,
    );
    conferir(alvo, largura, "entrada largura", resultado.larguraPx, largura);
    conferir(alvo, largura, "entrada base", resultado.baseRemPx, 16);
    conferir(
      alvo,
      largura,
      "mediaText",
      normalizar(resultado.mediaText),
      "(max-width: 30rem)",
    );
    conferir(alvo, largura, "limiar", resultado.limiarPx, 480);
    conferir(
      alvo,
      largura,
      "regime",
      resultado.ativa,
      largura === 360 || largura === 480,
    );
  }
  return resultado;
}

/**
 * Serializa uma cópia das regras com uma única mutação; exige atingir o bloco
 * 30rem e mantém disco intacto para controlar sensibilidade com parsing válido.
 */
function adulterar(regras: CSSRule[], tipo: "sem mídia" | "40rem"): string {
  let atingidos = 0;
  let texto = "";
  for (const regra of regras) {
    if (
      regra.type === CSSRule.MEDIA_RULE &&
      normalizar((regra as CSSMediaRule).media.mediaText) ===
        "(max-width: 30rem)"
    ) {
      atingidos++;
      if (tipo === "40rem")
        texto += regra.cssText.replace("30rem", "40rem") + "\n";
    } else texto += regra.cssText + "\n";
  }
  expect(atingidos, "a mutação deve atingir exatamente um bloco real").toBe(1);
  return texto;
}

/**
 * Caracteriza S0–S3 sem renderizar a página; calibra a API antes dos casos e
 * verifica somente CSS declarado para não atribuir layout real ao jsdom.
 */
describe("Vagas — caracterização estática do CSS móvel de F1.1", function caracterizarCss() {
  /** Calibra as APIs públicas com fixture válida; registra o caminho para impedir skips arbitrários. */
  beforeAll(function calibrarApi() {
    caminho = detectarCssom();
    console.info(
      "S0 recursos",
      JSON.stringify({
        matchMedia: typeof window.matchMedia,
        CSSStyleSheet: typeof CSSStyleSheet,
        replaceSync:
          typeof CSSStyleSheet === "function"
            ? typeof CSSStyleSheet.prototype.replaceSync
            : "undefined",
        caminho,
        importCss:
          "não executado: leitura direta com fs; import lateral não é prova de CSS no runner (v002, F10–F11)",
      }),
    );
  });

  /** Confirma leitura e calibração inclusiva; usa oráculos literais para distinguir F1.1 do controle 481px. */
  it("S0 — preserva CSSOM e avalia 360, 480, 640 e o controle 481px com base explícita", function calibrarEnsaio(contexto) {
    for (const fonte of FONTES) {
      const texto = readFileSync(fonte.url, "utf8");
      expect(texto).toContain(fonte.alvos[0].seletor);
      expect(texto).toContain("@media (max-width: 30rem)");
    }
    const modo = exigirCssom(contexto);
    const alvos = [
      {
        seletor: ".calibracao",
        propriedade: "padding",
        base: "2rem",
        movel: "1rem",
      },
    ];
    const declaracoes = extrair(analisarCss(FIXTURE, modo), alvos);
    expect(declaracoes).toEqual([
      {
        seletor: ".calibracao",
        propriedade: "padding",
        valor: "2rem",
        media: null,
      },
      {
        seletor: ".calibracao",
        propriedade: "padding",
        valor: "1rem",
        media: "(max-width: 30rem)",
      },
    ]);
    const casos = [
      { largura: 360, ativa: true, valor: "1rem", papel: "F1.1" },
      { largura: 480, ativa: true, valor: "1rem", papel: "F1.1: igualdade" },
      { largura: 640, ativa: false, valor: "2rem", papel: "F1.1" },
      {
        largura: 481,
        ativa: false,
        valor: "2rem",
        papel: "controle S0; não F1.1",
      },
    ];
    for (const caso of casos) {
      const resultado = avaliar(declaracoes, alvos, caso.largura, 16);
      expect(resultado).toEqual({
        larguraPx: caso.largura,
        baseRemPx: 16,
        mediaText: "(max-width: 30rem)",
        limiarPx: 480,
        ativa: caso.ativa,
        valores: [caso.valor],
      });
      console.info("S0 calibração", caso.papel, JSON.stringify(resultado));
    }
    expect(avaliarMedia("(max-width: 480px)", 480, 16)).toEqual({
      larguraPx: 480,
      baseRemPx: 16,
      limiarPx: 480,
      ativa: true,
    });
  });

  for (const css of [
    "@media (min-width: 30rem) { .calibracao { padding: 1rem } }",
    ".calibracao { padding: 1rem !important }",
    ".calibracao:hover { padding: 1rem }",
    "@supports (display: grid) { .calibracao { padding: 1rem } }",
    ".calibracao { padding-left: 1rem }",
    ".calibracao { padding: 1rem; padding-left: 2rem }",
  ]) {
    /** Rejeita sintaxe e cascata não modeladas; exercita os guardas para que método restrito não vire parser permissivo. */
    it(`S0 — recusa método não suportado: ${css}`, function recusarSintaxe(contexto) {
      const regras = analisarCss(css, exigirCssom(contexto));
      const alvos = [
        {
          seletor: ".calibracao",
          propriedade: "padding",
          base: "2rem",
          movel: "1rem",
        },
      ];
      /** Executa a extração restrita para demonstrar rejeição explícita da sintaxe recebida. */
      function extrairIncompativel() {
        extrair(regras, alvos);
      }
      expect(extrairIncompativel).toThrowError(/Método não suportado/);
    });
  }

  for (let indice = 0; indice < FONTES.length; indice++) {
    const fonte = FONTES[indice];
    for (const largura of LARGURAS_F11) {
      /** Verifica a folha real por largura; registra entradas e seleção para caracterizar busca ou shell sem duplicar interações. */
      it(`S${indice + 1} — ${fonte.nome}: caracteriza declarações em ${largura}px`, function caracterizarLargura(contexto) {
        const regras = analisarCss(
          readFileSync(fonte.url, "utf8"),
          exigirCssom(contexto),
        );
        const resultado = verificar(regras, fonte, largura, 16);
        console.info(`S${indice + 1} ${fonte.nome}`, JSON.stringify(resultado));
      });
    }

    for (const tipo of ["sem mídia", "40rem"] as const) {
      /** Controla a sensibilidade por mutante; exige falha tipada de valor com alvo/largura e confirma original e arquivo intactos. */
      it(`S3 — ${fonte.nome}: rejeita cópia ${tipo}`, function controlarSensibilidade(contexto) {
        const modo = exigirCssom(contexto);
        const original = readFileSync(fonte.url, "utf8");
        const regras = analisarCss(original, modo);
        for (const largura of LARGURAS_F11)
          verificar(regras, fonte, largura, 16);
        const mutante = adulterar(regras, tipo);
        const regrasMutantes = analisarCss(mutante, modo);
        expect(regrasMutantes.length).toBeGreaterThan(0);
        // Extração fora do catch: sintaxe inválida ou método não suportado não provam sensibilidade.
        extrair(regrasMutantes, fonte.alvos);
        const larguras = tipo === "sem mídia" ? [360, 480] : [640];
        for (const largura of larguras) {
          let falha: unknown;
          try {
            verificar(regrasMutantes, fonte, largura, 16);
          } catch (erro) {
            falha = erro;
          }
          expect(falha).toBeInstanceOf(FalhaVerificacao);
          if (!(falha instanceof FalhaVerificacao))
            throw new Error(
              "Mutante não apresentou a divergência de valor esperada",
            );
          expect(falha.message).toContain(fonte.alvos[0].seletor);
          expect(falha.message).toContain(fonte.alvos[0].propriedade);
          expect(falha.message).toContain(`${largura}px`);
          expect(falha.message).toContain("valor selecionado");
          console.info(`S3 ${fonte.nome} ${tipo}`, falha.message);
        }
        expect(readFileSync(fonte.url, "utf8")).toBe(original);
        for (const largura of LARGURAS_F11)
          verificar(analisarCss(original, modo), fonte, largura, 16);
        console.info(
          `S3 ${fonte.nome} ${tipo}`,
          "original intacto e novamente concordante",
        );
      });
    }
  }
});
