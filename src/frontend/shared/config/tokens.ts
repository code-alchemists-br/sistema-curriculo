/**
 * Definições tipadas dos tokens de cor semânticos do sistema.
 *
 * Cada valor segue estritamente os critérios de contraste da WCAG 2.1 AA:
 * - Texto normal: razão mínima de 4.5:1 contra fundos adjacentes.
 * - Indicadores visuais e foco: razão mínima de 3.0:1 contra fundos adjacentes.
 */
export const TOKENS_COR = {
  texto: {
    principal: "#0f172a",
    secundario: "#334155",
    suave: "#475569",
    inverso: "#ffffff",
  },
  fundo: {
    pagina: "#f8fafc",
    superficie: "#ffffff",
  },
  foco: {
    anel: "#1d4ed8",
    borda: "#1d4ed8",
  },
  erro: {
    texto: "#991b1b",
    fundo: "#fef2f2",
    borda: "#dc2626",
  },
  sucesso: {
    texto: "#166534",
    fundo: "#f0fdf4",
    borda: "#16a34a",
  },
  acao: {
    primaria: "#2563eb",
    primariaHover: "#1d4ed8",
  },
} as const;

/**
 * Define a escala de espaçamento modular usada pela interface.
 *
 * O objeto mapeia múltiplos de quatro pixels em valores CSS rem. Ele existe para
 * preservar ritmo visual consistente entre componentes sem fixar pixels locais.
 */
export const TOKENS_ESPACO = {
  espaco0: "0",
  espaco1: "0.25rem",
  espaco2: "0.5rem",
  espaco3: "0.75rem",
  espaco4: "1rem",
  espaco5: "1.25rem",
  espaco6: "1.5rem",
  espaco8: "2rem",
  espaco10: "2.5rem",
  espaco12: "3rem",
  espaco16: "4rem",
} as const;

/**
 * Define famílias, tamanhos, pesos e alturas de linha padronizados.
 *
 * O objeto agrupa uma escala tipográfica acessível e baseada em fontes do
 * sistema. Ele existe para dar hierarquia legível às telas de forma consistente.
 */
export const TOKENS_TIPOGRAFIA = {
  familia: {
    base: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    mono: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
  },
  tamanho: {
    xs: "0.75rem",
    sm: "0.875rem",
    base: "1rem",
    md: "1.125rem",
    lg: "1.25rem",
    xl: "1.5rem",
    "2xl": "1.875rem",
    "3xl": "2.25rem",
  },
  peso: { regular: 400, medium: 500, semibold: 600, bold: 700 },
  alturaLinha: { tight: 1.25, normal: 1.5, relaxed: 1.75 },
} as const;

/** Representa a estrutura pública dos tokens de cor. */
export type TokensCor = typeof TOKENS_COR;
/** Representa a estrutura pública dos tokens de espaçamento. */
export type TokensEspaco = typeof TOKENS_ESPACO;
/** Representa a estrutura pública dos tokens tipográficos. */
export type TokensTipografia = typeof TOKENS_TIPOGRAFIA;

/**
 * Converte um valor CSS em rem para pixels usando a base de 16 pixels.
 *
 * A função valida a representação textual e multiplica seu fator pela base.
 * Ela existe para verificar programaticamente as escalas de design nos testes.
 */
export function remParaPixels(valorRem: string): number {
  if (valorRem === "0") return 0;
  const match = /^(\d+(?:\.\d+)?)rem$/.exec(valorRem.trim());
  if (!match) throw new Error(`Valor de rem inválido: ${valorRem}`);
  return Number.parseFloat(match[1]) * 16;
}

/**
 * Informa se os valores de uma escala são estritamente crescentes.
 *
 * A função compara cada item ao anterior e falha em repetições ou regressões.
 * Ela existe para proteger a progressão visual dos tokens de espaçamento e tipo.
 */
export function validarEscalaCrescente(valores: number[]): boolean {
  return valores.every(
    (valor, indice) => indice === 0 || valor > valores[indice - 1],
  );
}

/**
 * Converte uma representação hexadecimal de cor (#RGB ou #RRGGBB) em valores inteiros RGB.
 *
 * **O que faz:** Decodifica a string hexadecimal em três canais numéricos de 0 a 255.
 * **Como faz:** Remove o caractere '#' inicial, normaliza formatos curtos de 3 caracteres duplicando-os,
 * e converte cada par em inteiros na base 16.
 * **Qual finalidade atende:** Viabiliza o cálculo matemático de luminância e contraste conforme a especificação WCAG.
 */
export function hexParaRgb(hex: string): { r: number; g: number; b: number } {
  let sanitizado = hex.replace("#", "").trim();

  if (sanitizado.length === 3) {
    sanitizado = sanitizado
      .split("")
      .map((char) => char + char)
      .join("");
  }

  const inteiro = parseInt(sanitizado, 16);
  return {
    r: (inteiro >> 16) & 255,
    g: (inteiro >> 8) & 255,
    b: inteiro & 255,
  };
}

/**
 * Calcula a luminância relativa de uma cor no espaço sRGB.
 *
 * **O que faz:** Computa o brilho relativo de uma cor em escala de 0 (preto absoluto) a 1 (branco absoluto).
 * **Como faz:** Aplica a curva de decodificação gama do padrão sRGB em cada canal linear e combina
 * os fatores de luminosidade espectral humana (0.2126 R + 0.7152 G + 0.0722 B).
 * **Qual finalidade atende:** Serve de base para determinar com precisão a razão de contraste da WCAG 2.1.
 */
export function calcularLuminanciaRelativa(
  r: number,
  g: number,
  b: number,
): number {
  const normalizados = [r, g, b].map((canal) => {
    const srgb = canal / 255;
    return srgb <= 0.04045
      ? srgb / 12.92
      : Math.pow((srgb + 0.055) / 1.055, 2.4);
  });

  const [rl = 0, gl = 0, bl = 0] = normalizados;
  return 0.2126 * rl + 0.7152 * gl + 0.0722 * bl;
}

/**
 * Calcula a razão de contraste entre duas cores hexadecimais de acordo com a fórmula da WCAG 2.1.
 *
 * **O que faz:** Retorna a proporção de contraste relativa entre o primeiro plano e o segundo plano.
 * **Como faz:** Extrai a luminância de ambas as cores e calcula a razão `(L_claro + 0.05) / (L_escuro + 0.05)`,
 * devolvendo um número arredondado para duas casas decimais.
 * **Qual finalidade atende:** Permite que testes e componentes afiram a conformidade estrita com
 * os níveis de acessibilidade AA (mínimo 4.5:1 para texto e 3.0:1 para foco/elementos gráficos).
 */
export function calcularRazaoContraste(cor1: string, cor2: string): number {
  const rgb1 = hexParaRgb(cor1);
  const rgb2 = hexParaRgb(cor2);

  const lum1 = calcularLuminanciaRelativa(rgb1.r, rgb1.g, rgb1.b);
  const lum2 = calcularLuminanciaRelativa(rgb2.r, rgb2.g, rgb2.b);

  const maisClaro = Math.max(lum1, lum2);
  const maisEscuro = Math.min(lum1, lum2);

  const razao = (maisClaro + 0.05) / (maisEscuro + 0.05);
  return Math.round(razao * 100) / 100;
}
