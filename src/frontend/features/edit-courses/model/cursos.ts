/** Limites de tamanho e carga para os campos de curso. */
export const LIMITES_CURSO = {
  nome: 200,
  instituicao: 200,
  cargaHoraria: 5,
  cargaHorariaMaxima: 10000,
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
 * A função verifica presença dos campos obrigatórios e um formato numérico
 * decimal inteiro entre 1 e 10000 para a carga opcional. Ela oferece feedback imediato
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

  for (const campo of ["nome", "instituicao"] as const) {
    const texto = curso[campo].trim();
    if (Array.from(texto).length > LIMITES_CURSO[campo]) {
      erros[campo] = `Informe no máximo ${LIMITES_CURSO[campo]} caracteres.`;
    } else if (/\p{C}/u.test(texto.replace(/[\n\t\x0d]/g, ""))) {
      erros[campo] = "Remova os caracteres de controle inválidos.";
    }
  }

  const textoCarga = curso.cargaHoraria.trim();
  const carga = Number(textoCarga);
  if (
    textoCarga !== "" &&
    (!/^[0-9]+$/.test(textoCarga) ||
      !Number.isInteger(carga) ||
      carga < 1 ||
      carga > LIMITES_CURSO.cargaHorariaMaxima)
  ) {
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

/**
 * Identifica um rascunho totalmente vazio comparando os três campos aparados.
 * Distingue ausência opcional de preenchimento parcial, sem perder dados na submissão.
 */
export function cursoEstaVazio(curso: Curso): boolean {
  return (
    curso.nome.trim() === "" &&
    curso.instituicao.trim() === "" &&
    curso.cargaHoraria.trim() === ""
  );
}
