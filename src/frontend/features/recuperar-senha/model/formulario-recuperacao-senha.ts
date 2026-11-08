import type {
  CodigoFalhaRecuperacaoSenha,
  SolicitarRecuperacaoSenhaEntrada,
} from "../api/cliente-recuperacao-senha";

/** Agrupa os erros de validação local do formulário de recuperação. */
export interface ErrosRecuperacaoSenha {
  email?: string;
}

/**
 * Valida o formato de e-mail antes de submeter a recuperação.
 *
 * A função verifica presença e estrutura básica sem confirmar se a conta existe,
 * preservando a segurança contra enumeração de usuários.
 */
export function validarEmailRecuperacao(email: string): ErrosRecuperacaoSenha {
  const emailLimpo = email.trim();
  if (emailLimpo === "") {
    return { email: "Informe seu e-mail." };
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailLimpo)) {
    return { email: "Informe um e-mail válido." };
  }

  return {};
}

/** Normaliza o e-mail para o contrato de solicitação de recuperação. */
export function criarEntradaRecuperacaoSenha(
  email: string,
): SolicitarRecuperacaoSenhaEntrada {
  return { email: email.trim() };
}

/** Traduz falhas da comunicação remota para mensagens claras ao usuário. */
export function traduzirFalhaRecuperacaoSenha(
  codigo: CodigoFalhaRecuperacaoSenha,
): string {
  const mensagens: Record<CodigoFalhaRecuperacaoSenha, string> = {
    indisponivel:
      "A recuperação de senha está indisponível no momento. Tente novamente mais tarde.",
    rede: "Não foi possível conectar ao serviço. Verifique sua conexão e tente novamente.",
    "resposta-invalida":
      "Recebemos uma resposta inesperada do servidor. Tente novamente mais tarde.",
  };

  return mensagens[codigo];
}
