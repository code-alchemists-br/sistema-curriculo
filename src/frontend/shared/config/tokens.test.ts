import { describe, expect, it } from "vitest";

import {
  calcularRazaoContraste,
  hexParaRgb,
  remParaPixels,
  TOKENS_COR,
  TOKENS_ESPACO,
  TOKENS_TIPOGRAFIA,
  validarEscalaCrescente,
} from "./tokens";

describe("Tokens de espaçamento e tipografia", () => {
  it("mantém escalas modulares e crescentes", () => {
    const espacos = Object.values(TOKENS_ESPACO).map(remParaPixels);
    const tamanhos = Object.values(TOKENS_TIPOGRAFIA.tamanho).map(
      remParaPixels,
    );

    expect(validarEscalaCrescente(espacos)).toBe(true);
    expect(validarEscalaCrescente(tamanhos)).toBe(true);
    espacos.slice(1).forEach((valor) => expect(valor % 4).toBe(0));
  });

  it("converte rem e rejeita valores inválidos", () => {
    expect(remParaPixels("1.5rem")).toBe(24);
    expect(() => remParaPixels("invalido")).toThrow("Valor de rem inválido");
  });

  it("fornece tipografia legível e fontes de fallback", () => {
    expect(TOKENS_TIPOGRAFIA.familia.base).toContain("sans-serif");
    expect(TOKENS_TIPOGRAFIA.familia.mono).toContain("monospace");
    expect(TOKENS_TIPOGRAFIA.alturaLinha.normal).toBeGreaterThanOrEqual(1.5);
  });
});

describe("Tokens de Cor — Acessibilidade e Contraste WCAG 2.1", () => {
  describe("Cálculo de Contraste e Conversão", () => {
    /**
     * Valida a decodificação de cores hexadecimais em canais RGB.
     *
     * **O que faz:** Confirma que valores #RGB e #RRGGBB são convertidos corretamente para 0-255.
     * **Como faz:** Executa `hexParaRgb` com preto, branco e valores parciais.
     * **Qual finalidade atende:** Garante precisão na base numérica dos cálculos de luminância.
     */
    it("converte hexadecimais de 3 e 6 dígitos em canais RGB com exatidão", () => {
      expect(hexParaRgb("#000000")).toEqual({ r: 0, g: 0, b: 0 });
      expect(hexParaRgb("#ffffff")).toEqual({ r: 255, g: 255, b: 255 });
      expect(hexParaRgb("#fff")).toEqual({ r: 255, g: 255, b: 255 });
      expect(hexParaRgb("#0f172a")).toEqual({ r: 15, g: 23, b: 42 });
    });

    /**
     * Valida os extremos teóricos da razão de contraste da WCAG.
     *
     * **O que faz:** Confirma 21:1 entre preto e branco e 1:1 entre cores idênticas.
     * **Como faz:** Executa `calcularRazaoContraste` com os pares limítrofes.
     * **Qual finalidade atende:** Assegura conformidade estrita com a fórmula oficial da W3C.
     */
    it("calcula razões conhecidas da fórmula da WCAG", () => {
      expect(calcularRazaoContraste("#ffffff", "#000000")).toBe(21);
      expect(calcularRazaoContraste("#ffffff", "#ffffff")).toBe(1);
    });
  });

  describe("Critério 1.4.3 — Contraste de Texto (Mínimo 4.5:1)", () => {
    /**
     * Valida que todos os tokens de texto atendem ao mínimo de 4.5:1 para nível AA.
     *
     * **O que faz:** Compara cada token de texto contra os fundos padrão de tela e superfície.
     * **Como faz:** Calcula a razão de contraste e assegura que seja >= 4.5.
     * **Qual finalidade atende:** Garante legibilidade para pessoas com baixa visão e em telas de variadas resoluções.
     */
    it("garante contraste de texto principal, secundário e suave >= 4.5:1 contra fundos claros", () => {
      const { texto, fundo, acao } = TOKENS_COR;

      // Texto principal
      expect(
        calcularRazaoContraste(texto.principal, fundo.superficie),
      ).toBeGreaterThanOrEqual(4.5);
      expect(
        calcularRazaoContraste(texto.principal, fundo.pagina),
      ).toBeGreaterThanOrEqual(4.5);

      // Texto secundário
      expect(
        calcularRazaoContraste(texto.secundario, fundo.superficie),
      ).toBeGreaterThanOrEqual(4.5);
      expect(
        calcularRazaoContraste(texto.secundario, fundo.pagina),
      ).toBeGreaterThanOrEqual(4.5);

      // Texto suave (muted)
      expect(
        calcularRazaoContraste(texto.suave, fundo.superficie),
      ).toBeGreaterThanOrEqual(4.5);
      expect(
        calcularRazaoContraste(texto.suave, fundo.pagina),
      ).toBeGreaterThanOrEqual(4.5);

      // Texto inverso sobre botão de ação primária
      expect(
        calcularRazaoContraste(texto.inverso, acao.primaria),
      ).toBeGreaterThanOrEqual(4.5);
      expect(
        calcularRazaoContraste(texto.inverso, acao.primariaHover),
      ).toBeGreaterThanOrEqual(4.5);
    });
  });

  describe("Critério 1.4.11 — Contraste de Foco Não Textual (Mínimo 3.0:1)", () => {
    /**
     * Valida que o anel de foco possui contraste visível aprovado.
     *
     * **O que faz:** Avalia a cor do anel de foco visível contra os fundos da aplicação.
     * **Como faz:** Calcula a razão de contraste da cor de foco contra superfícies e exige >= 3.0.
     * **Qual finalidade atende:** Elimina falhas onde o indicador de foco é invisível ou fraco para navegação por teclado.
     */
    it("garante contraste do indicador de foco >= 3.0:1 contra fundos adjacentes", () => {
      const { foco, fundo } = TOKENS_COR;

      expect(
        calcularRazaoContraste(foco.anel, fundo.superficie),
      ).toBeGreaterThanOrEqual(3.0);
      expect(
        calcularRazaoContraste(foco.anel, fundo.pagina),
      ).toBeGreaterThanOrEqual(3.0);
    });
  });

  describe("Tokens de Erro — Contraste de Texto e Borda", () => {
    /**
     * Valida que as cores de erro atendem aos critérios de leitura e identificação.
     *
     * **O que faz:** Confere o contraste do texto de erro e da borda contra fundo branco e o fundo do card de erro.
     * **Como faz:** Exige >= 4.5:1 para o texto de erro e >= 3.0:1 para o delimitador gráfico de erro.
     * **Qual finalidade atende:** Garante que erros de validação sejam imediatamente distinguíveis e legíveis.
     */
    it("garante contraste de texto de erro >= 4.5:1 e borda >= 3.0:1", () => {
      const { erro, fundo } = TOKENS_COR;

      // Texto de erro contra fundo branco e fundo do card
      expect(
        calcularRazaoContraste(erro.texto, fundo.superficie),
      ).toBeGreaterThanOrEqual(4.5);
      expect(
        calcularRazaoContraste(erro.texto, erro.fundo),
      ).toBeGreaterThanOrEqual(4.5);

      // Borda de erro contra fundo branco e fundo do card
      expect(
        calcularRazaoContraste(erro.borda, fundo.superficie),
      ).toBeGreaterThanOrEqual(3.0);
      expect(
        calcularRazaoContraste(erro.borda, erro.fundo),
      ).toBeGreaterThanOrEqual(3.0);
    });
  });

  describe("Tokens de Sucesso — Contraste de Texto e Borda", () => {
    /**
     * Valida que as cores de sucesso atendem aos critérios de leitura e identificação.
     *
     * **O que faz:** Confere o contraste do texto de sucesso e da borda contra fundo branco e fundo do card de sucesso.
     * **Como faz:** Exige >= 4.5:1 para o texto e >= 3.0:1 para o delimitador gráfico.
     * **Qual finalidade atende:** Assegura que mensagens de confirmação e status positivos sejam legíveis.
     */
    it("garante contraste de texto de sucesso >= 4.5:1 e borda >= 3.0:1", () => {
      const { sucesso, fundo } = TOKENS_COR;

      // Texto de sucesso contra fundo branco e fundo do card
      expect(
        calcularRazaoContraste(sucesso.texto, fundo.superficie),
      ).toBeGreaterThanOrEqual(4.5);
      expect(
        calcularRazaoContraste(sucesso.texto, sucesso.fundo),
      ).toBeGreaterThanOrEqual(4.5);

      // Borda de sucesso contra fundo branco e fundo do card
      expect(
        calcularRazaoContraste(sucesso.borda, fundo.superficie),
      ).toBeGreaterThanOrEqual(3.0);
      expect(
        calcularRazaoContraste(sucesso.borda, sucesso.fundo),
      ).toBeGreaterThanOrEqual(3.0);
    });
  });
});
