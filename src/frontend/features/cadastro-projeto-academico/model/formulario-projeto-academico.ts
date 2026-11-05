// Proveniência: decision-analysis prompts/frontend/20260921-120136-tela-cadastro-projetos-academicos-v001.md#v001

import type {
  CodigoFalhaCadastroProjeto,
  ProjetoAcademicoEntrada,
} from "../api/cliente-projetos-academicos";

/** Representa os valores locais que o estudante informa para cadastrar um projeto. */
export type ValoresProjetoAcademico = ProjetoAcademicoEntrada;

/** Representa erros locais vinculados aos campos do formulário de projeto. */
export type ErrosProjetoAcademico = Partial<
  Record<keyof ValoresProjetoAcademico, string>
>;

/**
 * Valida presença mínima para orientar o preenchimento antes do envio.
 *
 * A função exige título, descrição e tecnologias utilizadas para garantir
 * informações suficientes sobre a participação e competências aplicadas no projeto.
 */
export function validarProjetoAcademico(
  valores: ValoresProjetoAcademico,
): ErrosProjetoAcademico {
  const erros: ErrosProjetoAcademico = {};

  if (valores.titulo.trim() === "")
    erros.titulo = "Informe o título do projeto.";
  if (valores.descricao.trim() === "")
    erros.descricao = "Descreva o objetivo ou sua contribuição no projeto.";
  if (valores.tecnologias.trim() === "")
    erros.tecnologias = "Informe as tecnologias utilizadas no projeto.";

  return erros;
}

/**
 * Valida uma lista de projetos acadêmicos, retornando um mapa de erros por índice.
 */
export function validarListaProjetosAcademicos(
  projetos: ValoresProjetoAcademico[],
): Record<number, ErrosProjetoAcademico> {
  const mapaErros: Record<number, ErrosProjetoAcademico> = {};

  projetos.forEach((projeto, indice) => {
    const erros = validarProjetoAcademico(projeto);
    if (Object.keys(erros).length > 0) {
      mapaErros[indice] = erros;
    }
  });

  return mapaErros;
}

/**
 * Traduz uma falha do cliente para uma mensagem compreensível ao estudante.
 *
 * A função não revela detalhes do backend e diferencia indisponibilidade de
 * resposta incompatível. Ela existe para preservar os valores locais e indicar
 * uma próxima ação clara enquanto a integração ainda está pendente.
 */
export function traduzirFalhaCadastroProjeto(
  codigo: CodigoFalhaCadastroProjeto,
): string {
  const mensagens: Record<CodigoFalhaCadastroProjeto, string> = {
    indisponivel:
      "O cadastro de projetos está indisponível no momento. Tente novamente mais tarde.",
    "resposta-invalida":
      "Recebemos uma resposta inesperada. Tente novamente mais tarde.",
  };

  return mensagens[codigo];
}
