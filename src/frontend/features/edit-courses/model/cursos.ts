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
 * Valida os campos de um único curso.
 *
 * A função verifica presença dos campos obrigatórios e um formato numérico
 * positivo para a carga horária. Ela existe para oferecer feedback imediato
 * sem substituir as regras definitivas que serão aplicadas pelo backend.
 */
export function validarCurso(curso: Curso): ErrosCurso {
  const erros: ErrosCurso = {};

  if (curso.nome.trim() === "") {
    erros.nome = "Informe o nome do curso.";
  }

  if (curso.instituicao.trim() === "") {
    erros.instituicao = "Informe a instituição.";
  }

  const carga = Number(curso.cargaHoraria);
  if (curso.cargaHoraria.trim() === "" || Number.isNaN(carga) || carga <= 0) {
    erros.cargaHoraria = "Informe uma carga horária válida (em horas).";
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
