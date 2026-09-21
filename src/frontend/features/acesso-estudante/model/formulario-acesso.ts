// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001

import type {
  AcessoEstudanteEntrada,
  CadastroEstudanteEntrada,
  CodigoFalhaAcessoEstudante
} from "../api/cliente-acesso-estudante";

/** Representa os valores locais do formulário de criação de conta. */
export interface ValoresCadastro extends CadastroEstudanteEntrada {
  confirmacaoSenha: string;
}

/** Representa erros locais indexados pelo campo que o estudante pode corrigir. */
export type ErrosFormulario = Partial<Record<keyof ValoresCadastro, string>>;

/**
 * Valida os dados locais de criação de conta antes de chamar o cliente.
 *
 * A função aplica apenas regras de experiência — presença, formato básico e
 * confirmação — e não tenta substituir a validação do backend. Ela existe para
 * orientar correções imediatas sem enviar uma requisição evidentemente inválida.
 */
export function validarCadastro(valores: ValoresCadastro): ErrosFormulario {
  const erros: ErrosFormulario = {};

  if (valores.nome.trim() === "") erros.nome = "Informe seu nome.";
  if (!emailPareceValido(valores.email)) erros.email = "Informe um e-mail válido.";
  if (valores.senha.length < 8) erros.senha = "A senha deve ter ao menos 8 caracteres.";
  if (valores.confirmacaoSenha !== valores.senha) {
    erros.confirmacaoSenha = "As senhas não coincidem.";
  }

  return erros;
}

/**
 * Valida os dados locais de confirmação de credenciais antes do envio.
 *
 * A função reutiliza a checagem mínima de formato e tamanho sem inferir se uma
 * conta existe. Ela existe para reduzir tentativas incompletas mantendo o
 * backend como fonte de verdade para as credenciais.
 */
export function validarAcesso(entrada: AcessoEstudanteEntrada): ErrosFormulario {
  const erros: ErrosFormulario = {};

  if (!emailPareceValido(entrada.email)) erros.email = "Informe um e-mail válido.";
  if (entrada.senha.length < 8) erros.senha = "A senha deve ter ao menos 8 caracteres.";

  return erros;
}

/**
 * Converte uma categoria da fronteira HTTP em uma mensagem acionável.
 *
 * A função usa vocabulário de interface, sem mostrar status ou detalhes
 * internos do servidor. Ela existe para informar o estudante preservando os
 * valores já preenchidos quando uma dependência externa falha.
 */
export function traduzirFalhaAcesso(codigo: CodigoFalhaAcessoEstudante): string {
  const mensagens: Record<CodigoFalhaAcessoEstudante, string> = {
    "credenciais-invalidas": "E-mail ou senha não conferem.",
    "email-ja-cadastrado": "Este e-mail já possui uma conta.",
    "dados-invalidos": "Revise os dados informados e tente novamente.",
    indisponivel: "O serviço está indisponível no momento. Tente novamente mais tarde.",
    rede: "Não foi possível conectar ao serviço. Verifique sua conexão e tente novamente.",
    "resposta-invalida": "Recebemos uma resposta inesperada. Tente novamente mais tarde."
  };

  return mensagens[codigo];
}

/**
 * Verifica um formato mínimo de e-mail para o feedback imediato do formulário.
 *
 * A expressão exige texto antes e depois de @ e não tenta validar a gramática
 * completa de endereços. Ela existe para equilibrar orientação rápida e a
 * validação definitiva mantida no backend.
 */
function emailPareceValido(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}
