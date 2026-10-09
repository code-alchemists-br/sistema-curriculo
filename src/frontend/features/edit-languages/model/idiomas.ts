/** Enumera os níveis de proficiência aceitos pela tela. */
export type NivelIdioma = "basico" | "intermediario" | "avancado" | "fluente";

/** Mapeia os valores internos para rótulos legíveis na interface. */
export const NIVEIS_IDIOMA: Record<NivelIdioma, string> = {
  basico: "Básico",
  intermediario: "Intermediário",
  avancado: "Avançado",
  fluente: "Fluente",
};

/** Representa um idioma informado pelo estudante. */
export interface Idioma {
  nome: string;
  nivel: NivelIdioma | "";
}

/** Agrupa erros associados a cada campo de um idioma. */
export interface ErrosIdioma {
  nome?: string;
  nivel?: string;
}

/** Cria uma entrada de idioma vazia para adição dinâmica. */
export function criarIdiomaVazio(): Idioma {
  return {
    nome: "",
    nivel: "",
  };
}

/**
 * Valida os campos de um único idioma.
 *
 * A função verifica presença do nome e seleção do nível de proficiência.
 * Ela existe para oferecer feedback imediato sem substituir as regras
 * definitivas que serão aplicadas pelo backend.
 */
export function validarIdioma(idioma: Idioma): ErrosIdioma {
  const erros: ErrosIdioma = {};

  if (idioma.nome.trim() === "") {
    erros.nome = "Informe o idioma.";
  }

  if (idioma.nivel === "") {
    erros.nivel = "Selecione o nível de proficiência.";
  }

  return erros;
}

/**
 * Valida uma lista de idiomas e retorna um mapa de erros indexado pela posição.
 *
 * A função aplica validarIdioma a cada entrada e somente inclui no resultado
 * as posições que apresentam pelo menos um campo inválido.
 */
export function validarListaIdiomas(
  idiomas: Idioma[],
): Record<number, ErrosIdioma> {
  const erros: Record<number, ErrosIdioma> = {};

  idiomas.forEach((idioma, indice) => {
    const errosIdioma = validarIdioma(idioma);
    if (Object.keys(errosIdioma).length > 0) {
      erros[indice] = errosIdioma;
    }
  });

  return erros;
}
