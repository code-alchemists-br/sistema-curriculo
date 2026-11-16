/** Limites de tamanho e carga para os campos de curso. */
export const LIMITES_CURSO = {
  nome: 100,
  instituicao: 100,
  cargaHoraria: 4,
  cargaHorariaMaxima: 9999,
} as const;

/** Representa um curso ou certificação informado pelo estudante. */
export interface Curso {
  nome: string;
  instituicao: string;
  cargaHoraria: string;
}

/** Agrupa erros associados a cada campo de um curso. */
export interface ErrosCurso {
  nome?: string;
  instituicao?: string;
  cargaHoraria?: string;
}

/** Cria uma entrada de curso vazia para adição dinâmica. */
export function criarCursoVazio(): Curso {
  return {
    nome: "",
    instituicao: "",
    cargaHoraria: "",
  };
}

/**
 * Valida os campos de um único curso e seus limites de caracteres.
 *
 * A função verifica presença dos campos obrigatórios, formato numérico
 * positivo para a carga horária e limites máximos de tamanho.
 */
export function validarCurso(curso: Curso): ErrosCurso {
  const erros: ErrosCurso = {};

  if (curso.nome.trim() === "") {
    erros.nome = "Informe o nome do curso.";
  } else if (curso.nome.length > LIMITES_CURSO.nome) {
    erros.nome = `O nome do curso deve ter no máximo ${LIMITES_CURSO.nome} caracteres.`;
  }

  if (curso.instituicao.trim() === "") {
    erros.instituicao = "Informe a instituição.";
  } else if (curso.instituicao.length > LIMITES_CURSO.instituicao) {
    erros.instituicao = `A instituição deve ter no máximo ${LIMITES_CURSO.instituicao} caracteres.`;
  }

  const carga = Number(curso.cargaHoraria);
  if (curso.cargaHoraria.trim() === "" || Number.isNaN(carga) || carga <= 0) {
    erros.cargaHoraria = "Informe uma carga horária válida (em horas).";
  } else if (carga > LIMITES_CURSO.cargaHorariaMaxima) {
    erros.cargaHoraria = `A carga horária não pode ultrapassar ${LIMITES_CURSO.cargaHorariaMaxima} horas.`;
  }

  return erros;
}

/**
 * Valida uma lista de cursos e retorna um mapa de erros indexado pela posição.
 *
 * A função aplica validarCurso a cada entrada e somente inclui no resultado
 * as posições que apresentam pelo menos um campo inválido.
 */
export function validarListaCursos(
  cursos: Curso[],
): Record<number, ErrosCurso> {
  const erros: Record<number, ErrosCurso> = {};

  cursos.forEach((curso, indice) => {
    const errosCurso = validarCurso(curso);
    if (Object.keys(errosCurso).length > 0) {
      erros[indice] = errosCurso;
    }
  });

  return erros;
}

/**
 * Normaliza os valores de um curso removendo espaços excedentes.
 *
 * A função existe para impedir que espaços em branco desnecessários sejam
 * tratados como dados significativos pela futura fronteira de API.
 */
export function normalizarCurso(curso: Curso): Curso {
  return {
    nome: curso.nome.trim(),
    instituicao: curso.instituicao.trim(),
    cargaHoraria: curso.cargaHoraria.trim(),
  };
}
