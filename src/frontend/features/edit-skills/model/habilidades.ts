/**
 * Define as categorias de competência aceitas pela tela.
 */
export type TipoHabilidade = "hard" | "soft";

/**
 * Representa as competências técnicas e comportamentais informadas pelo estudante.
 */
export interface Habilidades {
  hardSkills: string[];
  softSkills: string[];
}

/**
 * Lista sugestões de competências técnicas que podem ser adicionadas por clique.
 */
export const HARD_SKILLS_SUGERIDAS = [
  "Java",
  "Python",
  "JavaScript",
  "TypeScript",
  "SQL",
  "Git",
  "React"
];

/**
 * Lista sugestões de competências comportamentais que podem ser adicionadas por clique.
 */
export const SOFT_SKILLS_SUGERIDAS = [
  "Comunicação",
  "Trabalho em equipe",
  "Liderança",
  "Organização",
  "Proatividade",
  "Criatividade",
  "Resolução de problemas"
];

/**
 * Remove espaços desnecessários do início e do fim de uma competência.
 */
export function normalizarHabilidade(habilidade: string): string {
  return habilidade.trim();
}

/**
 * Verifica se uma competência já está presente, ignorando maiúsculas e minúsculas.
 */
export function habilidadeJaExiste(
  habilidades: string[],
  habilidade: string
): boolean {
  const habilidadeNormalizada = normalizarHabilidade(habilidade).toLowerCase();

  return habilidades.some(
    (item) => item.toLowerCase() === habilidadeNormalizada
  );
}

/**
 * Adiciona uma competência válida sem permitir valores vazios ou duplicados.
 */
export function adicionarHabilidade(
  habilidades: string[],
  habilidade: string
): string[] {
  const habilidadeNormalizada = normalizarHabilidade(habilidade);

  if (habilidadeNormalizada === "") {
    return habilidades;
  }

  if (habilidadeJaExiste(habilidades, habilidadeNormalizada)) {
    return habilidades;
  }

  return [...habilidades, habilidadeNormalizada];
}

/**
 * Remove uma competência específica da lista informada.
 */
export function removerHabilidade(
  habilidades: string[],
  habilidade: string
): string[] {
  return habilidades.filter((item) => item !== habilidade);
}
