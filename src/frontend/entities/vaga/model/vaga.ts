/** Representa uma vaga sugerida pela integração externa do Grupo 2. */
export interface Vaga {
  id: string;
  titulo: string;
  empresa: string;
  descricao: string;
  requisitos: string[];
  localizacao: string | null;
  modalidade: string | null;
  urlCandidatura: string | null;
}

/** Vincula uma sugestão de vaga ao currículo consultado na integração. */
export interface SugestaoVaga {
  curriculoId: string;
  vaga: Vaga;
}
