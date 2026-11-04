import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";

describe("Animações LIMINAL — animations.css", () => {
  const cssPath = path.resolve(__dirname, "animations.css");
  const cssContent = fs.readFileSync(cssPath, "utf-8");

  it("define as keyframes essenciais aceleradas por GPU", () => {
    expect(cssContent).toContain("@keyframes animacaoEntradaFadeUp");
    expect(cssContent).toContain("@keyframes animacaoEntradaFadeIn");
    expect(cssContent).toContain("@keyframes animacaoEntradaScaleUp");
  });

  it("utiliza exclusivamente opacity e transform nas animações principais", () => {
    // Garante que propriedades que causam reflow/layout shift (top, left, margin, width, height) não estão nas keyframes
    const keyframesMatches =
      cssContent.match(/@keyframes[^{]+{(?:[^{}]+|{[^{}]*})*}/g) || [];
    expect(keyframesMatches.length).toBeGreaterThanOrEqual(3);

    for (const kf of keyframesMatches) {
      expect(kf).toMatch(/opacity/);
      expect(kf).not.toMatch(
        /(\btop\b|\bleft\b|\bright\b|\bbottom\b|\bmargin\b)\s*:/,
      );
    }
  });

  it("respeita a diretriz de acessibilidade com prefers-reduced-motion", () => {
    expect(cssContent).toContain("@media (prefers-reduced-motion: reduce)");
    expect(cssContent).toContain("animation-duration: 0.01ms !important");
    expect(cssContent).toContain("transition-duration: 0.01ms !important");
  });
});
