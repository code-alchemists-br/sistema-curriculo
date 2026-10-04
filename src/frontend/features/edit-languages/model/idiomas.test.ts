import { describe, expect, it } from "vitest";

import {
  criarIdiomaVazio,
  validarIdioma,
  validarListaIdiomas,
  type Idioma
} from "./idiomas";

const idiomaValido: Idioma = {
  nome: "Inglês",
  nivel: "avancado"
};

describe("validarIdioma", () => {
  it("retorna objeto vazio quando todos os campos são válidos", () => {
    const erros = validarIdioma(idiomaValido);
    expect(Object.keys(erros)).toHaveLength(0);
  });

  it("reporta nome ausente", () => {
    const erros = validarIdioma({ ...idiomaValido, nome: "  " });
    expect(erros.nome).toBe("Informe o idioma.");
  });

  it("reporta nível não selecionado", () => {
    const erros = validarIdioma({ ...idiomaValido, nivel: "" });
    expect(erros.nivel).toBe("Selecione o nível de proficiência.");
  });
});

describe("validarListaIdiomas", () => {
  it("retorna mapa vazio quando todos os idiomas são válidos", () => {
    const erros = validarListaIdiomas([idiomaValido, { nome: "Espanhol", nivel: "basico" }]);
    expect(Object.keys(erros)).toHaveLength(0);
  });

  it("indexa erros pela posição do idioma inválido", () => {
    const erros = validarListaIdiomas([idiomaValido, { nome: "", nivel: "" }]);
    expect(erros[0]).toBeUndefined();
    expect(erros[1]).toHaveProperty("nome");
    expect(erros[1]).toHaveProperty("nivel");
  });
});

describe("criarIdiomaVazio", () => {
  it("retorna nome vazio e nível vazio", () => {
    const idioma = criarIdiomaVazio();
    expect(idioma.nome).toBe("");
    expect(idioma.nivel).toBe("");
  });
});
