/**
 * Limite máximo de caracteres permitido para os campos textuais de certificação.
 */
export const LIMITE_CARACTERES_CERTIFICACAO = 200;

/**
 * Representa uma certificação profissional cadastrada.
 */
export interface Certificacao {
  id?: string;
  nome: string;
  organizacaoEmissora: string;
}

/**
 * Representa os valores capturados pelo formulário de cadastro de certificação.
 */
export interface ValoresCertificacao {
  nome: string;
  organizacaoEmissora: string;
}

/**
 * Mapeia os erros de validação por campo do formulário de certificação.
 */
export interface ErrosCertificacao {
  nome?: string;
  organizacaoEmissora?: string;
}

/**
 * Cria um objeto com os valores iniciais vazios para o formulário de certificação.
 *
 * **O que faz:** Inicializa os campos do formulário em branco.
 * **Como faz:** Retorna um objeto literal com `nome` e `organizacaoEmissora` como strings vazias.
 * **Qual finalidade atende:** Facilita a inicialização e o reset controlado do estado local do formulário.
 */
export function criarCertificacaoVazia(): ValoresCertificacao {
  return {
    nome: "",
    organizacaoEmissora: "",
  };
}

/**
 * Valida os dados informados para uma certificação profissional.
 *
 * **O que faz:** Verifica se os campos obrigatórios estão preenchidos e não excedem o tamanho máximo.
 * **Como faz:** Avalia a presença de caracteres não brancos e o comprimento de cada string contra `LIMITE_CARACTERES_CERTIFICACAO`.
 * **Qual finalidade atende:** Fornece feedback imediato de acessibilidade ao estudante antes do envio à API.
 */
export function validarCertificacao(
  valores: ValoresCertificacao,
): ErrosCertificacao {
  const erros: ErrosCertificacao = {};

  const nomeLimpo = valores.nome.trim();
  if (nomeLimpo === "") {
    erros.nome = "Informe o nome da certificação.";
  } else if (nomeLimpo.length > LIMITE_CARACTERES_CERTIFICACAO) {
    erros.nome = `O nome da certificação deve ter no máximo ${LIMITE_CARACTERES_CERTIFICACAO} caracteres.`;
  }

  const emissorLimpo = valores.organizacaoEmissora.trim();
  if (emissorLimpo === "") {
    erros.organizacaoEmissora =
      "Informe a instituição ou organização emissora.";
  } else if (emissorLimpo.length > LIMITE_CARACTERES_CERTIFICACAO) {
    erros.organizacaoEmissora = `A organização emissora deve ter no máximo ${LIMITE_CARACTERES_CERTIFICACAO} caracteres.`;
  }

  return erros;
}

/**
 * Normaliza os textos de uma certificação removendo espaços redundantes.
 *
 * **O que faz:** Higieniza os campos textuais antes da submissão.
 * **Como faz:** Remove espaços no início/fim e substitui múltiplos espaços internos por um único espaço.
 * **Qual finalidade atende:** Garante dados padronizados e consistentes com as regras de normalização do backend.
 */
export function normalizarCertificacao(
  valores: ValoresCertificacao,
): ValoresCertificacao {
  return {
    nome: valores.nome.trim().replace(/\s+/g, " "),
    organizacaoEmissora: valores.organizacaoEmissora
      .trim()
      .replace(/\s+/g, " "),
  };
}
