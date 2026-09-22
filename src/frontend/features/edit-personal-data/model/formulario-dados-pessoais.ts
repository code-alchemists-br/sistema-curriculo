import type { Student } from "../../../entities/student";
import type { CodigoFalhaDadosPessoais } from "../api/cliente-dados-pessoais";

/** Representa os valores controlados pelo formulário antes da normalização. */
export interface ValoresDadosPessoais {
  nomeCompleto: string;
  enderecoCompleto: string;
  telefones: string[];
  email: string;
  linkedIn: string;
  curriculoLattes: string;
}

/** Agrupa erros locais associados a cada campo do formulário. */
export interface ErrosDadosPessoais {
  nomeCompleto?: string;
  enderecoCompleto?: string;
  telefones?: Record<number, string>;
  email?: string;
}

/** Cria valores vazios com um campo de telefone obrigatório inicial. */
export function criarValoresIniciais(): ValoresDadosPessoais {
  return {
    nomeCompleto: "",
    enderecoCompleto: "",
    telefones: [""],
    email: "",
    linkedIn: "",
    curriculoLattes: ""
  };
}

/**
 * Valida somente as informações mínimas necessárias para orientar o estudante.
 *
 * A função verifica presença dos campos obrigatórios, um formato básico de
 * e-mail e cada telefone existente. Ela existe para oferecer feedback imediato
 * sem substituir as regras definitivas que serão aplicadas pelo backend.
 */
export function validarDadosPessoais(valores: ValoresDadosPessoais): ErrosDadosPessoais {
  const erros: ErrosDadosPessoais = {};

  if (valores.nomeCompleto.trim() === "") {
    erros.nomeCompleto = "Informe seu nome completo.";
  }

  if (valores.enderecoCompleto.trim() === "") {
    erros.enderecoCompleto = "Informe seu endereço completo.";
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(valores.email.trim())) {
    erros.email = "Informe um e-mail válido.";
  }

  const errosDeTelefone: Record<number, string> = {};
  valores.telefones.forEach((telefone, indice) => {
    if (telefone.trim() === "") {
      errosDeTelefone[indice] = "Informe um telefone.";
    }
  });

  if (Object.keys(errosDeTelefone).length > 0) {
    erros.telefones = errosDeTelefone;
  }

  return erros;
}

/**
 * Converte os valores controlados em uma entidade pronta para persistência.
 *
 * A função remove espaços excedentes e omite contatos profissionais vazios. Ela
 * existe para impedir que o estado de campos opcionais em branco seja tratado
 * como dado significativo pela futura fronteira de API.
 */
export function criarStudent(valores: ValoresDadosPessoais): Student {
  const linkedIn = valores.linkedIn.trim();
  const curriculoLattes = valores.curriculoLattes.trim();

  return {
    nomeCompleto: valores.nomeCompleto.trim(),
    enderecoCompleto: valores.enderecoCompleto.trim(),
    telefones: valores.telefones.map((telefone) => telefone.trim()),
    email: valores.email.trim(),
    ...(linkedIn === "" ? {} : { linkedIn }),
    ...(curriculoLattes === "" ? {} : { curriculoLattes })
  };
}

/** Traduz uma falha estável do cliente para uma orientação compreensível. */
export function traduzirFalhaDadosPessoais(codigo: CodigoFalhaDadosPessoais): string {
  const mensagens: Record<CodigoFalhaDadosPessoais, string> = {
    indisponivel: "Não foi possível salvar os dados pessoais no momento. Tente novamente mais tarde.",
    "resposta-invalida": "Recebemos uma resposta inesperada. Tente novamente mais tarde."
  };

  return mensagens[codigo];
}
