export {
  criarClienteFormacaoAcademicaEmMemoria,
  criarClienteFormacaoAcademicaIndisponivel,
  FalhaFormacaoAcademica,
} from "./api/cliente-formacao-academica";
export { criarClienteFormacaoAcademicaHttp } from "./api/cliente-formacao-academica-http";
export type {
  CadastroFormacaoAcademicaEntrada,
  ClienteFormacaoAcademica,
  NivelFormacaoAcademica,
  StatusFormacaoAcademica,
} from "./api/cliente-formacao-academica";
export {
  LIMITES_FORMACAO_ACADEMICA,
  criarEntradaFormacaoAcademica,
  criarValoresIniciaisFormacao,
  obterDataAtualIso,
  restringirAno4Digitos,
  validarCurriculoLattes,
  validarFormacaoAcademica,
  validarListaFormacoes,
} from "./model/formulario-formacao-academica";
export type {
  ErrosFormacaoAcademica,
  ValoresFormacaoAcademica,
} from "./model/formulario-formacao-academica";
export { FormularioFormacaoAcademica } from "./ui/FormularioFormacaoAcademica";
