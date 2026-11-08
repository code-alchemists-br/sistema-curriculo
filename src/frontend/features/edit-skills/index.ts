export { FormularioCompetencias } from "./ui/FormularioCompetencias";

export {
  adicionarHabilidade,
  habilidadeJaExiste,
  normalizarHabilidade,
  removerHabilidade,
  HARD_SKILLS_SUGERIDAS,
  SOFT_SKILLS_SUGERIDAS,
} from "./model/habilidades";

export type { Habilidades, TipoHabilidade } from "./model/habilidades";

export type { FormularioCompetenciasProps } from "./ui/FormularioCompetencias";

export {
  criarClienteCompetenciasHttp,
  FalhaCompetencias,
} from "./api/cliente-competencias-http";
export type {
  ClienteCompetencias,
  CodigoFalhaCompetencias,
} from "./api/cliente-competencias-http";
