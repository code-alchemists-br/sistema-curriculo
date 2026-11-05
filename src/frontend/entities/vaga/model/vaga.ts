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
  nivelSenioridade?: string | null;
  salario?: string | null;
  moeda?: string | null;
  palavrasChave?: string[];
  dataPublicacao?: string | null;
}

/** Vincula uma sugestão de vaga ao currículo consultado na integração. */
export interface SugestaoVaga {
  curriculoId: string;
  vaga: Vaga;
  ranque?: number;
  pontuacaoCompatibilidade?: number;
}
