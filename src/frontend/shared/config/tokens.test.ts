import { describe, expect, it } from "vitest";
import {
  TOKENS_COR,
  TOKENS_ESPACO,
  TOKENS_TIPOGRAFIA,
  calcularLuminanciaRelativa,
  calcularRazaoContraste,
  remParaPixels,
  validarEscalaCrescente,
} from "./tokens";

describe("Design Tokens — Espaçamento", () => {
  it("deve conter escala modular de espaçamento crescente e baseada em 4px/8px", () => {
    const chaves = [
      "espaco1",
      "espaco2",
      "espaco3",
      "espaco4",
      "espaco5",
      "espaco6",
      "espaco8",
      "espaco10",
      "espaco12",
      "espaco16",
    ] as const;

    const valoresPx = chaves.map((k) => remParaPixels(TOKENS_ESPACO[k]));

    expect(validarEscalaCrescente(valoresPx)).toBe(true);

    valoresPx.forEach((px) => {
      expect(px % 4).toBe(0);
    });
  });

  it("deve converter remParaPixels corretamente", () => {
    expect(remParaPixels("0")).toBe(0);
    expect(remParaPixels("0.25rem")).toBe(4);
    expect(remParaPixels("1rem")).toBe(16);
    expect(remParaPixels("1.5rem")).toBe(24);
    expect(remParaPixels("2rem")).toBe(32);
    expect(() => remParaPixels("invalido")).toThrow("Valor de rem inválido");
  });

  it("deve validar escala crescente corretamente", () => {
    expect(validarEscalaCrescente([4, 8, 12, 16])).toBe(true);
    expect(validarEscalaCrescente([4, 8, 8, 16])).toBe(false);
    expect(validarEscalaCrescente([16, 12, 8])).toBe(false);
  });
});

describe("Design Tokens — Tipografia", () => {
  it("deve incluir pilha de fontes de sistema acessível", () => {
    expect(TOKENS_TIPOGRAFIA.familia.base).toContain("sans-serif");
    expect(TOKENS_TIPOGRAFIA.familia.mono).toContain("monospace");
  });

  it("deve possuir escala modular de tamanho de fonte estritamente crescente", () => {
    const chaves = [
      "xs",
      "sm",
      "base",
      "md",
      "lg",
      "xl",
      "2xl",
      "3xl",
    ] as const;

    const valoresPx = chaves.map((k) =>
      remParaPixels(TOKENS_TIPOGRAFIA.tamanho[k]),
    );

    expect(validarEscalaCrescente(valoresPx)).toBe(true);
  });

  it("deve respeitar pesos de fonte numéricos padronizados", () => {
    expect(TOKENS_TIPOGRAFIA.peso.regular).toBe(400);
    expect(TOKENS_TIPOGRAFIA.peso.medium).toBe(500);
    expect(TOKENS_TIPOGRAFIA.peso.semibold).toBe(600);
    expect(TOKENS_TIPOGRAFIA.peso.bold).toBe(700);
  });

  it("deve cumprir o critério WCAG 2.1 (1.4.12) para altura de linha normal >= 1.5", () => {
    expect(TOKENS_TIPOGRAFIA.alturaLinha.normal).toBeGreaterThanOrEqual(1.5);
    expect(TOKENS_TIPOGRAFIA.alturaLinha.relaxed).toBeGreaterThan(
      TOKENS_TIPOGRAFIA.alturaLinha.normal,
    );
    expect(TOKENS_TIPOGRAFIA.alturaLinha.tight).toBeLessThan(
      TOKENS_TIPOGRAFIA.alturaLinha.normal,
    );
  });
});

describe("Design Tokens — Cores e Contraste WCAG", () => {
  it("deve calcular luminância relativa de preto e branco", () => {
    expect(calcularLuminanciaRelativa("#000000")).toBeCloseTo(0, 4);
    expect(calcularLuminanciaRelativa("#ffffff")).toBeCloseTo(1, 4);
    expect(() => calcularLuminanciaRelativa("#xyz")).toThrow(
      "Cor hexadecimal inválida",
    );
  });

  it("deve calcular razão de contraste máxima para preto e branco", () => {
    const contraste = calcularRazaoContraste("#000000", "#ffffff");
    expect(contraste).toBeCloseTo(21, 0);
  });

  it("deve garantir contraste WCAG AA (>= 4.5:1) para texto primário e secundário", () => {
    const contrastePrimario = calcularRazaoContraste(
      TOKENS_COR.texto.primario,
      TOKENS_COR.fundo.superficie,
    );
    expect(contrastePrimario).toBeGreaterThanOrEqual(4.5);

    const contrasteSecundario = calcularRazaoContraste(
      TOKENS_COR.texto.secundario,
      TOKENS_COR.fundo.superficie,
    );
    expect(contrasteSecundario).toBeGreaterThanOrEqual(4.5);
  });

  it("deve garantir contraste WCAG AA (>= 3:1) para foco interativo", () => {
    const contrasteFoco = calcularRazaoContraste(
      TOKENS_COR.foco.outline,
      TOKENS_COR.fundo.superficie,
    );
    expect(contrasteFoco).toBeGreaterThanOrEqual(3.0);
  });

  it("deve garantir contraste WCAG AA (>= 4.5:1) para mensagens de erro e sucesso", () => {
    const contrasteErro = calcularRazaoContraste(
      TOKENS_COR.erro.texto,
      TOKENS_COR.erro.fundo,
    );
    expect(contrasteErro).toBeGreaterThanOrEqual(4.5);

    const contrasteSucesso = calcularRazaoContraste(
      TOKENS_COR.sucesso.texto,
      TOKENS_COR.sucesso.fundo,
    );
    expect(contrasteSucesso).toBeGreaterThanOrEqual(4.5);
  });
});
