import type {
  CodigoFalhaRecuperacaoSenha,
  SolicitarRecuperacaoSenhaEntrada,
} from "../api/cliente-recuperacao-senha";

/** Agrupa o único erro local que pode ser corrigido no formulário. */
export interface ErrosRecuperacaoSenha {
  email?: string;
}

/**
 * Valida o formato mínimo de e-mail antes de solicitar a recuperação.
 *
 * A função apenas verifica presença e estrutura básica, sem indicar se a conta
 * existe. Ela existe para orientar o preenchimento e preservar o servidor como
 * fonte de verdade para contas e fluxo de recuperação.
 */
export function validarEmailRecuperacao(email: string): ErrosRecuperacaoSenha {
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
    return { email: "Informe um e-mail válido." };
  }

  return {};
}

/** Normaliza o campo local para o contrato do cliente de recuperação. */
export function criarEntradaRecuperacaoSenha(
  email: string,
): SolicitarRecuperacaoSenhaEntrada {
  return { email: email.trim() };
}

/** Traduz falhas da fronteira para mensagens compreensíveis e acionáveis. */
export function traduzirFalhaRecuperacaoSenha(
  codigo: CodigoFalhaRecuperacaoSenha,
): string {
  const mensagens: Record<CodigoFalhaRecuperacaoSenha, string> = {
    indisponivel:
      "A recuperação de senha está indisponível no momento. Tente novamente mais tarde.",
    rede: "Não foi possível conectar ao serviço. Verifique sua conexão e tente novamente.",
    "resposta-invalida":
      "Recebemos uma resposta inesperada. Tente novamente mais tarde.",
  };

  return mensagens[codigo];
}
