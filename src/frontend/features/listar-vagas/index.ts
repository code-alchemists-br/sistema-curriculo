export {
  adaptarRespostaGrupo2,
  criarClienteVagasGrupo2,
  criarClienteVagasGrupo2Indisponivel,
  FalhaVagasGrupo2,
} from "./api/cliente-vagas-grupo2";
export type {
  ClienteVagasGrupo2,
  CodigoFalhaVagasGrupo2,
  CriteriosPesquisaVagas,
} from "./api/cliente-vagas-grupo2";
export { criarClienteDecisoesRecomendacaoIndisponivel } from "./api/cliente-decisoes-recomendacao";
export type {
  ClienteDecisoesRecomendacao,
  DecisaoRecomendacao,
  DecisaoRecomendacaoEntrada,
} from "./api/cliente-decisoes-recomendacao";
export { obterMensagemErroVagas } from "./model/mensagem-erro-vagas";
export { TelaVagasGrupo2 } from "./ui/TelaVagasGrupo2";
export type { TelaVagasGrupo2Props } from "./ui/TelaVagasGrupo2";
