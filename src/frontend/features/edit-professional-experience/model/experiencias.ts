/** Representa uma experiência profissional informada pelo estudante. */
export interface Experiencia {
  empresa: string;
  cargo: string;
  inicio: string;
  fim: string;
  empregoAtual: boolean;
  descricao: string;
}

/** Agrupa erros associados a cada campo de uma experiência. */
export interface ErrosExperiencia {
  empresa?: string;
  cargo?: string;
  inicio?: string;
  fim?: string;
}

/** Cria uma entrada de experiência vazia para adição dinâmica. */
export function criarExperienciaVazia(): Experiencia {
  return {
    empresa: "",
    cargo: "",
    inicio: "",
    fim: "",
    empregoAtual: false,
    descricao: ""
  };
}

/**
 * Valida os campos de uma única experiência profissional.
 *
 * A função verifica presença dos campos obrigatórios e ignora o campo Fim
 * quando o checkbox de emprego atual está marcado. Ela existe para oferecer
 * feedback imediato sem substituir as regras definitivas do backend.
 */
export function validarExperiencia(experiencia: Experiencia): ErrosExperiencia {
  const erros: ErrosExperiencia = {};

  if (experiencia.empresa.trim() === "") {
    erros.empresa = "Informe o nome da empresa.";
  }

  if (experiencia.cargo.trim() === "") {
    erros.cargo = "Informe o cargo exercido.";
  }

  if (experiencia.inicio === "") {
    erros.inicio = "Informe a data de início.";
  }

  if (!experiencia.empregoAtual && experiencia.fim === "") {
    erros.fim = "Informe a data de término ou marque como emprego atual.";
  }

  if (
    !experiencia.empregoAtual &&
    experiencia.inicio !== "" &&
    experiencia.fim !== "" &&
    experiencia.fim < experiencia.inicio
  ) {
    erros.fim = "A data de término deve ser posterior à data de início.";
  }

  return erros;
}

/**
 * Valida uma lista de experiências e retorna um mapa de erros por posição.
 *
 * A função aplica validarExperiencia a cada entrada e somente inclui no
 * resultado as posições que apresentam pelo menos um campo inválido.
 */
export function validarListaExperiencias(
  experiencias: Experiencia[]
): Record<number, ErrosExperiencia> {
  const erros: Record<number, ErrosExperiencia> = {};

  experiencias.forEach((experiencia, indice) => {
    const errosExperiencia = validarExperiencia(experiencia);
    if (Object.keys(errosExperiencia).length > 0) {
      erros[indice] = errosExperiencia;
    }
  });

  return erros;
}

/**
 * Ordena experiências da mais recente para a mais antiga.
 *
 * Experiências marcadas como emprego atual são posicionadas primeiro. Entre
 * as demais, a comparação usa o campo inicio no formato YYYY-MM, que permite
 * ordenação lexicográfica direta. A função retorna um novo array sem alterar
 * o original.
 */
export function ordenarPorDataDecrescente(experiencias: Experiencia[]): Experiencia[] {
  return [...experiencias].sort((a, b) => {
    if (a.empregoAtual && !b.empregoAtual) return -1;
    if (!a.empregoAtual && b.empregoAtual) return 1;

    return b.inicio.localeCompare(a.inicio);
  });
}
