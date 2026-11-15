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
  descricao?: string;
}

/** Limites de caracteres para os campos de experiência profissional. */
export const LIMITES_EXPERIENCIA = {
  empresaMax: 100,
  cargoMax: 100,
  descricaoMax: 1500,
} as const;

/** Retorna a data atual local no formato YYYY-MM-DD. */
export function obterDataAtualIso(): string {
  const agora = new Date();
  const ano = agora.getFullYear();
  const mes = String(agora.getMonth() + 1).padStart(2, "0");
  const dia = String(agora.getDate()).padStart(2, "0");
  return `${ano}-${mes}-${dia}`;
}

/**
 * Restringe o ano de uma data no formato ISO para conter no máximo 4 dígitos.
 */
export function restringirAno4Digitos(valorData: string): string {
  if (!valorData) return valorData;
  const partes = valorData.split("-");
  if (partes[0] && partes[0].length > 4) {
    partes[0] = partes[0].slice(0, 4);
    return partes.join("-");
  }
  return valorData;
}

/** Cria uma entrada de experiência vazia para adição dinâmica. */
export function criarExperienciaVazia(): Experiencia {
  return {
    empresa: "",
    cargo: "",
    inicio: "",
    fim: "",
    empregoAtual: false,
    descricao: "",
  };
}

/**
 * Valida os campos de uma única experiência profissional.
 *
 * A função verifica presença dos campos obrigatórios (empresa, cargo, início,
 * descrição e fim se não for emprego atual), limites de caracteres e se as
 * datas de início e término não ultrapassam o dia atual nem apresentam ordem invertida.
 */
export function validarExperiencia(
  experiencia: Experiencia,
  dataReferencia?: string,
): ErrosExperiencia {
  const erros: ErrosExperiencia = {};
  const dataHoje = dataReferencia ?? obterDataAtualIso();

  const obterLimite = (valorData: string) =>
    valorData.length === 7 ? dataHoje.slice(0, 7) : dataHoje;

  if (experiencia.empresa.trim() === "") {
    erros.empresa = "Informe o nome da empresa.";
  } else if (experiencia.empresa.length > LIMITES_EXPERIENCIA.empresaMax) {
    erros.empresa = `O nome da empresa deve ter no máximo ${LIMITES_EXPERIENCIA.empresaMax} caracteres.`;
  }

  if (experiencia.cargo.trim() === "") {
    erros.cargo = "Informe o cargo exercido.";
  } else if (experiencia.cargo.length > LIMITES_EXPERIENCIA.cargoMax) {
    erros.cargo = `O cargo deve ter no máximo ${LIMITES_EXPERIENCIA.cargoMax} caracteres.`;
  }

  if (experiencia.inicio === "") {
    erros.inicio = "Informe a data de início.";
  } else {
    const anoInicio = experiencia.inicio.split("-")[0] ?? "";
    if (anoInicio.length > 4 || Number(anoInicio) > 9999) {
      erros.inicio = "O ano de início deve ter no máximo 4 dígitos.";
    } else if (experiencia.inicio > obterLimite(experiencia.inicio)) {
      erros.inicio = "A data de início não pode ser posterior à data atual.";
    }
  }

  if (experiencia.descricao.trim() === "") {
    erros.descricao = "Informe a descrição das atividades.";
  } else if (experiencia.descricao.length > LIMITES_EXPERIENCIA.descricaoMax) {
    erros.descricao = `A descrição deve ter no máximo ${LIMITES_EXPERIENCIA.descricaoMax} caracteres.`;
  }

  if (!experiencia.empregoAtual && experiencia.fim === "") {
    erros.fim = "Informe a data de término ou marque como emprego atual.";
  } else if (!experiencia.empregoAtual && experiencia.fim !== "") {
    const anoFim = experiencia.fim.split("-")[0] ?? "";
    if (anoFim.length > 4 || Number(anoFim) > 9999) {
      erros.fim = "O ano de término deve ter no máximo 4 dígitos.";
    } else if (
      experiencia.inicio !== "" &&
      experiencia.fim < experiencia.inicio
    ) {
      erros.fim = "A data de término deve ser posterior à data de início.";
    } else if (experiencia.fim > obterLimite(experiencia.fim)) {
      erros.fim = "A data de término não pode ser posterior à data atual.";
    }
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
  experiencias: Experiencia[],
  dataReferencia?: string,
): Record<number, ErrosExperiencia> {
  const erros: Record<number, ErrosExperiencia> = {};

  experiencias.forEach((experiencia, indice) => {
    const errosExperiencia = validarExperiencia(experiencia, dataReferencia);
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
export function ordenarPorDataDecrescente(
  experiencias: Experiencia[],
): Experiencia[] {
  return [...experiencias].sort((a, b) => {
    if (a.empregoAtual && !b.empregoAtual) return -1;
    if (!a.empregoAtual && b.empregoAtual) return 1;

    return b.inicio.localeCompare(a.inicio);
  });
}
