/** Campos de texto livre que o backend sabe revisar com IA. */
export type CampoRevisavel =
  | "descricao_experiencia"
  | "descricao_projeto"
  | "descricao_curso"
  | "descricao_certificacao"
  | "objetivo_profissional"
  | "outro";

/** Veredito da IA sobre um texto. */
export type SituacaoTexto = "valido" | "melhorado" | "invalido";

/** Revisão de um campo já convertida para o modelo da interface. */
export interface RevisaoTexto {
  situacao: SituacaoTexto;
  motivo: string;
  sugestoes: string[];
  podeManterTexto: boolean;
}

/** Modelos de currículo aceitos pelo backend. */
export type ModeloSugerido =
  | "classico"
  | "compacto"
  | "ats-simples"
  | "criativo"
  | "moderno"
  | "academico"
  | "primeiro-emprego";

/** Modelo recomendado pela IA, o motivo e uma segunda opção. */
export interface RecomendacaoModelo {
  modelo: ModeloSugerido;
  motivo: string;
  alternativa: ModeloSugerido | null;
}

/** Um dado do perfil enviado à IA para recomendar o modelo. */
export interface InformacaoPerfil {
  pergunta: string;
  resposta: string;
}

/** Estado de um texto revisado, informado à página para bloquear o salvamento. */
export type EstadoTextoIa = "nao-revisado" | "aprovado" | "invalido" | "ia-indisponivel";
