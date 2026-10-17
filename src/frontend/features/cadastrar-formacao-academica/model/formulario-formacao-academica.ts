import type {
  CadastroFormacaoAcademicaEntrada,
  CodigoFalhaFormacaoAcademica,
  NivelFormacaoAcademica,
  StatusFormacaoAcademica,
} from "../api/cliente-formacao-academica";

/** Representa os valores controlados pelo formulário de formação acadêmica. */
export interface ValoresFormacaoAcademica {
  instituicao: string;
  curso: string;
  nivel: NivelFormacaoAcademica | "";
  dataInicio: string;
  dataFim: string;
  status: StatusFormacaoAcademica | "";
}

/** Agrupa mensagens de validação associadas a cada campo da formação. */
export type ErrosFormacaoAcademica = Partial<
  Record<keyof ValoresFormacaoAcademica, string>
>;

/** Fornece valores vazios para uma nova formação acadêmica. */
export function criarValoresIniciaisFormacao(): ValoresFormacaoAcademica {
  return {
    instituicao: "",
    curso: "",
    nivel: "",
    dataInicio: "",
    dataFim: "",
    status: "",
  };
}

/**
 * Valida apenas as regras locais necessárias para orientar o preenchimento.
 *
 * A função exige textos, enumerações e datas coerentes, incluindo data final
 * para formação concluída. Ela existe para evitar envios evidentemente
 * incompletos, preservando o backend como fonte definitiva das regras.
 */
export function validarFormacaoAcademica(
  valores: ValoresFormacaoAcademica,
): ErrosFormacaoAcademica {
  const erros: ErrosFormacaoAcademica = {};

  if (valores.instituicao.trim() === "") {
    erros.instituicao = "Informe a instituição.";
  } else if (valores.instituicao.trim().length > 200) {
    erros.instituicao = "A instituição deve ter no máximo 200 caracteres.";
  }

  if (valores.curso.trim() === "") {
    erros.curso = "Informe o curso.";
  } else if (valores.curso.trim().length > 200) {
    erros.curso = "O curso deve ter no máximo 200 caracteres.";
  }

  if (valores.nivel === "") erros.nivel = "Selecione o nível de formação.";
  if (valores.status === "") erros.status = "Selecione a situação da formação.";
  if (valores.dataInicio === "") erros.dataInicio = "Informe a data de início.";

  if (valores.status === "concluido" && valores.dataFim === "") {
    erros.dataFim = "Informe a data de conclusão.";
  }

  if (
    valores.dataInicio !== "" &&
    valores.dataFim !== "" &&
    valores.dataFim < valores.dataInicio
  ) {
    erros.dataFim = "A data final não pode ser anterior à data de início.";
  }

  return erros;
}

/**
 * Normaliza os valores da tela para o contrato de cadastro da feature.
 *
 * A função remove espaços externos e omite data final vazia antes de devolver
 * somente dados já validados. Ela existe para separar o estado editável da
 * entrada transmitida ao cliente injetado.
 */
export function criarEntradaFormacaoAcademica(
  valores: ValoresFormacaoAcademica,
): CadastroFormacaoAcademicaEntrada {
  if (valores.nivel === "" || valores.status === "") {
    throw new Error("A formação precisa estar validada antes da conversão.");
  }

  return {
    instituicao: valores.instituicao.trim(),
    curso: valores.curso.trim(),
    nivel: valores.nivel,
    dataInicio: valores.dataInicio,
    ...(valores.dataFim === "" ? {} : { dataFim: valores.dataFim }),
    status: valores.status,
  };
}

/** Traduz uma falha do cliente para uma mensagem acionável na interface. */
export function traduzirFalhaFormacaoAcademica(
  codigo: CodigoFalhaFormacaoAcademica,
): string {
  const mensagens: Record<CodigoFalhaFormacaoAcademica, string> = {
    indisponivel:
      "O cadastro de formação está indisponível no momento. Tente novamente mais tarde.",
    rede: "Não foi possível conectar ao serviço. Verifique sua conexão e tente novamente.",
    "resposta-invalida":
      "Recebemos uma resposta inesperada. Tente novamente mais tarde.",
  };

  return mensagens[codigo];
}
