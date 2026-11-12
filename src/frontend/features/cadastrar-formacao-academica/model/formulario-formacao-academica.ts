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
  curriculoLattes?: string;
  naoPossuiLattes?: boolean;
}

/** Limites de caracteres para os campos de formação acadêmica. */
export const LIMITES_FORMACAO_ACADEMICA = {
  instituicaoMax: 100,
  cursoMax: 100,
} as const;

/** Retorna a data atual local no formato YYYY-MM-DD. */
export function obterDataAtualIso(): string {
  const agora = new Date();
  const ano = agora.getFullYear();
  const mes = String(agora.getMonth() + 1).padStart(2, "0");
  const dia = String(agora.getDate()).padStart(2, "0");
  return `${ano}-${mes}-${dia}`;
}

/** Restringe o ano de uma data no formato ISO para conter no máximo 4 dígitos. */
export function restringirAno4Digitos(valorData: string): string {
  if (!valorData) return valorData;
  const partes = valorData.split("-");
  if (partes[0] && partes[0].length > 4) {
    partes[0] = partes[0].slice(0, 4);
    return partes.join("-");
  }
  return valorData;
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
    curriculoLattes: "",
    naoPossuiLattes: false,
  };
}

/**
 * Valida apenas as regras locais necessárias para orientar o preenchimento.
 *
 * A função exige textos, enumerações e datas coerentes, incluindo data final
 * para formação concluída e Currículo Lattes obrigatório para mestrado/doutorado
 * a menos que o estudante assinale que não possui cadastro na plataforma.
 */
export function validarFormacaoAcademica(
  valores: ValoresFormacaoAcademica,
  validarLattes: boolean = true,
  dataReferencia?: string,
): ErrosFormacaoAcademica {
  const erros: ErrosFormacaoAcademica = {};
  const dataHoje = dataReferencia ?? obterDataAtualIso();
  const obterLimite = (valorData: string) =>
    valorData.length === 7 ? dataHoje.slice(0, 7) : dataHoje;

  if (valores.instituicao.trim() === "") {
    erros.instituicao = "Informe a instituição.";
  } else if (
    valores.instituicao.trim().length >
    LIMITES_FORMACAO_ACADEMICA.instituicaoMax
  ) {
    erros.instituicao = `A instituição deve ter no máximo ${LIMITES_FORMACAO_ACADEMICA.instituicaoMax} caracteres.`;
  }

  const ehEnsinoBasico =
    valores.nivel === "ensino_fundamental" || valores.nivel === "ensino_medio";

  if (!ehEnsinoBasico) {
    if (valores.curso.trim() === "") {
      erros.curso = "Informe o curso.";
    } else if (
      valores.curso.trim().length > LIMITES_FORMACAO_ACADEMICA.cursoMax
    ) {
      erros.curso = `O curso deve ter no máximo ${LIMITES_FORMACAO_ACADEMICA.cursoMax} caracteres.`;
    }
  } else if (
    valores.curso.trim().length > LIMITES_FORMACAO_ACADEMICA.cursoMax
  ) {
    erros.curso = `O curso deve ter no máximo ${LIMITES_FORMACAO_ACADEMICA.cursoMax} caracteres.`;
  }

  if (valores.nivel === "") erros.nivel = "Selecione o nível de formação.";
  if (valores.status === "") erros.status = "Selecione a situação da formação.";

  if (valores.dataInicio === "") {
    erros.dataInicio = "Informe a data de início.";
  } else {
    const anoInicio = valores.dataInicio.split("-")[0] ?? "";
    if (anoInicio.length > 4 || Number(anoInicio) > 9999) {
      erros.dataInicio = "O ano de início deve ter no máximo 4 dígitos.";
    } else if (valores.dataInicio > obterLimite(valores.dataInicio)) {
      erros.dataInicio =
        "A data de início não pode ser posterior à data atual.";
    }
  }

  if (valores.status === "concluido" && valores.dataFim === "") {
    erros.dataFim = "Informe a data de conclusão.";
  } else if (valores.dataFim !== "") {
    const anoFim = valores.dataFim.split("-")[0] ?? "";
    if (anoFim.length > 4 || Number(anoFim) > 9999) {
      erros.dataFim = "O ano deve ter no máximo 4 dígitos.";
    } else if (
      valores.dataInicio !== "" &&
      valores.dataFim < valores.dataInicio
    ) {
      erros.dataFim = "A data final não pode ser anterior à data de início.";
    } else if (
      valores.status === "concluido" &&
      valores.dataFim > obterLimite(valores.dataFim)
    ) {
      erros.dataFim =
        "A data de conclusão não pode ser posterior à data atual.";
    }
  }

  if (validarLattes) {
    const ehPosGraduacaoAcademica =
      valores.nivel === "mestrado" || valores.nivel === "doutorado";

    if (ehPosGraduacaoAcademica) {
      if (!valores.naoPossuiLattes) {
        const lattes = valores.curriculoLattes?.trim() ?? "";
        if (lattes === "") {
          erros.curriculoLattes =
            "Informe o link do Currículo Lattes ou marque que não possui.";
        } else {
          try {
            const url = new URL(lattes);
            if (url.protocol !== "http:" && url.protocol !== "https:") {
              erros.curriculoLattes =
                "Informe um link válido (iniciando com http:// ou https://).";
            }
          } catch {
            erros.curriculoLattes =
              "Informe um link válido (ex.: http://lattes.cnpq.br/...).";
          }
        }
      }
    } else if (
      valores.curriculoLattes &&
      valores.curriculoLattes.trim().length > 0
    ) {
      try {
        const url = new URL(valores.curriculoLattes.trim());
        if (url.protocol !== "http:" && url.protocol !== "https:") {
          erros.curriculoLattes =
            "Informe um link válido (iniciando com http:// ou https://).";
        }
      } catch {
        erros.curriculoLattes =
          "Informe um link válido (ex.: http://lattes.cnpq.br/...).";
      }
    }
  }

  return erros;
}

/**
 * Valida o link do Currículo Lattes para a etapa de formação acadêmica.
 */
export function validarCurriculoLattes(
  curriculoLattes: string,
  naoPossuiLattes: boolean,
  ehObrigatorio: boolean,
): string | undefined {
  if (ehObrigatorio) {
    if (!naoPossuiLattes) {
      const lattes = curriculoLattes.trim();
      if (lattes === "") {
        return "Informe o link do Currículo Lattes ou marque que não possui.";
      }
      try {
        const url = new URL(lattes);
        if (url.protocol !== "http:" && url.protocol !== "https:") {
          return "Informe um link válido (iniciando com http:// ou https://).";
        }
      } catch {
        return "Informe um link válido (ex.: http://lattes.cnpq.br/...).";
      }
    }
  } else if (curriculoLattes && curriculoLattes.trim().length > 0) {
    try {
      const url = new URL(curriculoLattes.trim());
      if (url.protocol !== "http:" && url.protocol !== "https:") {
        return "Informe um link válido (iniciando com http:// ou https://).";
      }
    } catch {
      return "Informe um link válido (ex.: http://lattes.cnpq.br/...).";
    }
  }

  return undefined;
}

/**
 * Valida uma lista de formações acadêmicas, retornando um mapa com os erros por índice.
 */
export function validarListaFormacoes(
  formacoes: ValoresFormacaoAcademica[],
  dataReferencia?: string,
): Record<number, ErrosFormacaoAcademica> {
  const mapaErros: Record<number, ErrosFormacaoAcademica> = {};

  formacoes.forEach((formacao, indice) => {
    // Para formações em lista, o Lattes é gerenciado e validado no escopo global da etapa
    const erros = validarFormacaoAcademica(formacao, false, dataReferencia);
    if (Object.keys(erros).length > 0) {
      mapaErros[indice] = erros;
    }
  });

  return mapaErros;
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

  const ehEnsinoBasico =
    valores.nivel === "ensino_fundamental" || valores.nivel === "ensino_medio";

  const nomeCursoPadrao =
    valores.nivel === "ensino_fundamental"
      ? "Ensino Fundamental"
      : "Ensino Médio";

  const cursoFinal =
    ehEnsinoBasico && valores.curso.trim() === ""
      ? nomeCursoPadrao
      : valores.curso.trim();

  const lattesTrim = valores.naoPossuiLattes
    ? undefined
    : valores.curriculoLattes?.trim();

  return {
    instituicao: valores.instituicao.trim(),
    curso: cursoFinal,
    nivel: valores.nivel,
    dataInicio: valores.dataInicio,
    ...(valores.dataFim === "" ? {} : { dataFim: valores.dataFim }),
    status: valores.status,
    ...(lattesTrim && lattesTrim.length > 0
      ? { curriculoLattes: lattesTrim }
      : {}),
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
