/** Representa o contato público disponível para apresentação no currículo. */
export interface ContatoPreviaCurriculo {
  endereco: string;
  telefones: string[];
  linkedin: string | null;
  curriculo_lattes: string | null;
}

/** Representa a identificação pública do estudante na prévia. */
export interface EstudantePreviaCurriculo {
  nome: string;
  email: string;
  contato: ContatoPreviaCurriculo | null;
}

/** Representa uma formação acadêmica já selecionada para a versão. */
export interface FormacaoPreviaCurriculo {
  id: string;
  instituicao: string;
  curso: string;
  nivel: string;
  status: string;
  inicio: string;
  fim: string | null;
}

/** Representa uma experiência profissional já selecionada para a versão. */
export interface ExperienciaPreviaCurriculo {
  id: string;
  empresa: string;
  cargo: string;
  descricao: string;
  inicio: string;
  fim: string | null;
}

/** Representa um projeto acadêmico já selecionado para a versão. */
export interface ProjetoPreviaCurriculo {
  id: string;
  titulo: string;
  descricao: string;
  tecnologias: string;
}

/** Representa uma competência já selecionada para a versão. */
export interface CompetenciaPreviaCurriculo {
  id: string;
  descricao: string;
  nivel: string;
}

/** Representa um idioma já selecionado para a versão. */
export interface IdiomaPreviaCurriculo {
  id: string;
  idioma: string;
  nivel: string;
}

/** Representa o metadado público de um documento complementar. */
export interface DocumentoPreviaCurriculo {
  id: string;
  nome_arquivo: string;
  tipo_arquivo: string;
}

/**
 * Define o contrato único de entrada para modelos de apresentação de currículo.
 *
 * Os campos espelham a resposta pública da rota de prévia do backend. O tipo
 * existe para permitir que os modelos clássico e compacto recebam os mesmos
 * dados, sem criar formatos específicos ou duplicar transformações.
 */
export interface PreviaCurriculo {
  curriculo_id: string;
  titulo_versao: string;
  layout: string;
  estudante: EstudantePreviaCurriculo;
  formacoes: FormacaoPreviaCurriculo[];
  experiencias: ExperienciaPreviaCurriculo[];
  projetos: ProjetoPreviaCurriculo[];
  competencias: CompetenciaPreviaCurriculo[];
  idiomas: IdiomaPreviaCurriculo[];
  documentos: DocumentoPreviaCurriculo[];
}
