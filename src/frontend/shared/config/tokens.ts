/**
 * Proveniência: F8.2 - Design Tokens de Espaçamento, Tipografia e Cores.
 * Camada: shared/config.
 */

/**
 * Tokens de cores da aplicação em conformidade com critérios de contraste WCAG 2.1 AA.
 *
 * - O que faz: Fornece constantes hexadecimais para cores de texto, fundo, foco, erro e sucesso.
 * - Como faz: Mapeia cada propriedade de cor em um objeto estruturado e imutável.
 * - Qual finalidade atende: Centraliza a paleta acessível e garante conformidade com WCAG AA.
 */
export const TOKENS_COR = {
  texto: {
    primario: "#111827",
    secundario: "#4b5563",
  },
  fundo: {
    corpo: "#f8fafc",
    superficie: "#ffffff",
  },
  borda: {
    sutil: "#e2e8f0",
    padrao: "#94a3b8",
  },
  foco: {
    outline: "#2563eb",
    anel: "#93c5fd",
  },
  erro: {
    texto: "#b91c1c",
    fundo: "#fef2f2",
    borda: "#f87171",
  },
  sucesso: {
    texto: "#15803d",
    fundo: "#f0fdf4",
    borda: "#86efac",
  },
} as const;

/**
 * Tokens de espaçamento da aplicação baseados em escala modular de 4px/8px.
 *
 * - O que faz: Mapeia valores em rem para a escala de espaçamento do design system.
 * - Como faz: Define um objeto congelado com múltiplos de 0.25rem (4px).
 * - Qual finalidade atende: Garante consistência visual em margens, preenchimentos e lacunas nas telas principais.
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
 * Tokens de tipografia da aplicação com escala modular e conformidade com WCAG 2.1 Critério 1.4.12.
 *
 * - O que faz: Define famílias de fonte do sistema, tamanhos de fonte, pesos e alturas de linha.
 * - Como faz: Estrutura valores CSS padronizados com altura de linha normal >= 1.5 para leitura confortável.
 * - Qual finalidade atende: Estabelece hierarquia tipográfica consistente e acessível em todas as telas.
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
  peso: {
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  alturaLinha: {
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75,
  },
} as const;

/**
 * Tipo que representa a estrutura de tokens de cor da aplicação.
 */
export type TokensCor = typeof TOKENS_COR;

/**
 * Tipo que representa a estrutura de tokens de espaçamento da aplicação.
 */
export type TokensEspaco = typeof TOKENS_ESPACO;

/**
 * Tipo que representa a estrutura de tokens de tipografia da aplicação.
 */
export type TokensTipografia = typeof TOKENS_TIPOGRAFIA;

/**
 * Converte valor em formato rem para pixels assumindo 16px como tamanho base.
 *
 * - O que faz: Converte uma string no formato "Xrem" para o valor numérico equivalente em pixels.
 * - Como faz: Extrai a parte numérica via expressão regular e multiplica pela base de 16px.
 * - Qual finalidade atende: Facilita cálculos programáticos e validações automatizadas de escala modular em testes.
 *
 * @param valorRem Valor com sufixo rem (ex.: "1rem").
 * @returns Valor numérico equivalente em pixels.
 */
export function remParaPixels(valorRem: string): number {
  if (valorRem === "0") {
    return 0;
  }
  const match = /^([\d.]+)rem$/.exec(valorRem.trim());
  if (!match) {
    throw new Error(`Valor de rem inválido: ${valorRem}`);
  }
  return parseFloat(match[1]) * 16;
}

/**
 * Valida se uma escala numérica de tokens é estritamente crescente.
 *
 * - O que faz: Verifica se cada elemento de um array ordenado de números é estritamente maior que o anterior.
 * - Como faz: Itera pelos valores comparando cada elemento com seu antecessor imediato.
 * - Qual finalidade atende: Garante em tempo de execução ou teste que a escala modular não possui regressões ou saltos inválidos.
 *
 * @param valores Lista de números ordenados a validar.
 * @returns Verdadeiro se a escala for estritamente crescente.
 */
export function validarEscalaCrescente(valores: number[]): boolean {
  for (let i = 1; i < valores.length; i++) {
    if (valores[i] <= valores[i - 1]) {
      return false;
    }
  }
  return true;
}

/**
 * Converte canal de cor sRGB de 8 bits para luminância linear conforme a especificação WCAG 2.1.
 *
 * - O que faz: Lineariza o valor de um componente RGB (0 a 255) corrigindo a curva gama sRGB.
 * - Como faz: Normaliza para 0–1 e aplica divisão por 12.92 para valores baixos ou potência 2.4 para valores mais altos.
 * - Qual finalidade atende: Fornece o valor de intensidade luminosa linear necessário para cálculo de contraste WCAG.
 *
 * @param canal Valor inteiro de 0 a 255.
 * @returns Luminância linearizada entre 0.0 e 1.0.
 */
function linearizarCanalSRGB(canal: number): number {
  const norm = canal / 255;
  if (norm <= 0.04045) {
    return norm / 12.92;
  }
  return Math.pow((norm + 0.055) / 1.055, 2.4);
}

/**
 * Calcula a luminância relativa de uma cor hexadecimal conforme a fórmula WCAG 2.1.
 *
 * - O que faz: Extrai os componentes R, G e B de uma cor hexadecimal e calcula sua luminância relativa.
 * - Como faz: Lineariza cada canal sRGB e aplica os coeficientes ponderados padrão (0.2126*R + 0.7152*G + 0.0722*B).
 * - Qual finalidade atende: Base matemática indispensável para calcular razões de contraste entre fundo e primeiro plano.
 *
 * @param hex Cor no formato hexadecimal (#RRGGBB).
 * @returns Luminância relativa entre 0.0 (preto) e 1.0 (branco).
 */
export function calcularLuminanciaRelativa(hex: string): number {
  const sanitizado = hex.replace("#", "").trim();
  if (sanitizado.length !== 6) {
    throw new Error(`Cor hexadecimal inválida: ${hex}`);
  }
  const r = parseInt(sanitizado.slice(0, 2), 16);
  const g = parseInt(sanitizado.slice(2, 4), 16);
  const b = parseInt(sanitizado.slice(4, 6), 16);

  const rLin = linearizarCanalSRGB(r);
  const gLin = linearizarCanalSRGB(g);
  const bLin = linearizarCanalSRGB(b);

  return 0.2126 * rLin + 0.7152 * gLin + 0.0722 * bLin;
}

/**
 * Calcula a razão de contraste entre duas cores hexadecimais conforme WCAG 2.1.
 *
 * - O que faz: Determina a proporção de contraste de luminância entre duas cores.
 * - Como faz: Obtém a luminância relativa de ambas as cores e calcula a razão (L1 + 0.05) / (L2 + 0.05), onde L1 >= L2.
 * - Qual finalidade atende: Valida programaticamente se elementos de texto ou componentes interativos atendem ao contraste mínimo legal.
 *
 * @param hex1 Primeira cor em formato hexadecimal (#RRGGBB).
 * @param hex2 Segunda cor em formato hexadecimal (#RRGGBB).
 * @returns Proporção de contraste numérica (mínimo 1.0, máximo 21.0).
 */
export function calcularRazaoContraste(hex1: string, hex2: string): number {
  const lum1 = calcularLuminanciaRelativa(hex1);
  const lum2 = calcularLuminanciaRelativa(hex2);
  const maisClaro = Math.max(lum1, lum2);
  const maisEscuro = Math.min(lum1, lum2);
  return (maisClaro + 0.05) / (maisEscuro + 0.05);
}
