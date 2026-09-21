// Proveniência: decision-analysis prompts/frontend/20260921-120136-tela-cadastro-projetos-academicos-v001.md#v001

import type { CodigoFalhaCadastroProjeto, ProjetoAcademicoEntrada } from "../api/cliente-projetos-academicos";

/** Representa os valores locais que o estudante informa para cadastrar um projeto. */
export type ValoresProjetoAcademico = ProjetoAcademicoEntrada;

/** Representa erros locais vinculados aos campos do formulário de projeto. */
export type ErrosProjetoAcademico = Partial<Record<keyof ValoresProjetoAcademico, string>>;

/**
 * Valida presença mínima para orientar o preenchimento antes do envio.
 *
 * A função trata título e descrição em branco como informação insuficiente e
 * preserva tecnologias como texto livre, sem determinar regras do domínio. Ela
 * existe para dar feedback imediato sem substituir as validações do backend.
 */
export function validarProjetoAcademico(valores: ValoresProjetoAcademico): ErrosProjetoAcademico {
  const erros: ErrosProjetoAcademico = {};

  if (valores.titulo.trim() === "") erros.titulo = "Informe o título do projeto.";
  if (valores.descricao.trim() === "") erros.descricao = "Descreva o objetivo ou sua contribuição no projeto.";

  return erros;
}

/**
 * Traduz uma falha do cliente para uma mensagem compreensível ao estudante.
 *
 * A função não revela detalhes do backend e diferencia indisponibilidade de
 * resposta incompatível. Ela existe para preservar os valores locais e indicar
 * uma próxima ação clara enquanto a integração ainda está pendente.
 */
export function traduzirFalhaCadastroProjeto(codigo: CodigoFalhaCadastroProjeto): string {
  const mensagens: Record<CodigoFalhaCadastroProjeto, string> = {
    indisponivel: "O cadastro de projetos está indisponível no momento. Tente novamente mais tarde.",
    "resposta-invalida": "Recebemos uma resposta inesperada. Tente novamente mais tarde."
  };

  return mensagens[codigo];
}
