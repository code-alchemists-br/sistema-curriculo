/** Enumera os modelos que já podem ser associados a uma versão de currículo. */
export type ModeloVersaoCurriculo =
  | "ats-simples"
  | "classico"
  | "compacto"
  | "moderno"
  | "criativo"
  | "academico"
  | "primeiro-emprego";

/** Define uma opção disponível para a apresentação de uma versão existente. */
export interface OpcaoModeloVersaoCurriculo {
  valor: ModeloVersaoCurriculo;
  rotulo: string;
}

/** Lista os modelos já reconhecidos pela seleção de currículo. */
export const OPCOES_MODELO_VERSAO: readonly OpcaoModeloVersaoCurriculo[] = [
  { valor: "ats-simples", rotulo: "ATS simples" },
  { valor: "classico", rotulo: "Profissional clássico" },
  { valor: "compacto", rotulo: "Compacto" },
  { valor: "moderno", rotulo: "Moderno" },
  { valor: "criativo", rotulo: "Criativo" },
  { valor: "academico", rotulo: "Acadêmico" },
  { valor: "primeiro-emprego", rotulo: "Primeiro emprego" },
];

/** Indica se uma versão pode ser localizada fora do perfil do estudante. */
export type VisibilidadeVersaoCurriculo = "privado" | "publico";

/** Representa os metadados de uma versão já criada pelo estudante. */
export interface ResumoVersaoCurriculo {
  id: string;
  tituloVersao: string;
  modelo: ModeloVersaoCurriculo;
  visibilidade: VisibilidadeVersaoCurriculo;
  totalItens: number;
}

/** Agrupa os metadados que a pessoa pode alterar em uma versão existente. */
export interface EdicaoVersaoCurriculo {
  tituloVersao: string;
  modelo: ModeloVersaoCurriculo;
}

/**
 * Reúne os dados enviados ao contrato técnico de atualização de versão.
 *
 * A visibilidade permanece aqui porque o endpoint atual a exige na atualização,
 * mas não é apresentada como escolha da interface: não existe requisito de
 * busca pública de currículos que justifique expor essa configuração ao aluno.
 */
export interface AtualizacaoVersaoCurriculo extends EdicaoVersaoCurriculo {
  visibilidade: VisibilidadeVersaoCurriculo;
}

/** Retorna o rótulo legível do modelo associado a uma versão. */
export function obterRotuloModeloVersao(
  modelo: ModeloVersaoCurriculo,
): string {
  return (
    OPCOES_MODELO_VERSAO.find((opcao) => opcao.valor === modelo)?.rotulo ??
    "Modelo não identificado"
  );
}
