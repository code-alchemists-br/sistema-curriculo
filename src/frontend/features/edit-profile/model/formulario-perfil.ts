import type { Student } from "../../../entities/student";
import type { CodigoFalhaPerfilEstudante } from "../api/cliente-perfil-estudante";

/** Representa os valores controlados pelo formulário de edição do perfil. */
export interface ValoresPerfilEstudante {
  nomeCompleto: string;
  enderecoCompleto: string;
  telefones: string[];
  email: string;
  linkedIn: string;
  curriculoLattes: string;
}

/** Agrupa erros locais associados a cada campo do formulário de perfil. */
export interface ErrosPerfilEstudante {
  nomeCompleto?: string;
  enderecoCompleto?: string;
  telefones?: Record<number, string>;
  email?: string;
}

/**
 * Cria valores iniciais a partir de uma entidade Student existente.
 *
 * A função preenche os campos opcionais com strings vazias quando ausentes no
 * modelo de entrada. Ela existe para converter o formato da entidade para o
 * formato controlado pelo formulário sem perder dados do perfil carregado.
 */
export function criarValoresDeStudent(student: Student): ValoresPerfilEstudante {
  return {
    nomeCompleto: student.nomeCompleto,
    enderecoCompleto: student.enderecoCompleto,
    telefones: student.telefones.length > 0 ? [...student.telefones] : [""],
    email: student.email,
    linkedIn: student.linkedIn ?? "",
    curriculoLattes: student.curriculoLattes ?? ""
  };
}

/**
 * Valida as informações mínimas do perfil antes de permitir o envio.
 *
 * A função verifica presença dos campos obrigatórios, formato básico de e-mail
 * e cada telefone existente. Ela existe para oferecer feedback imediato sem
 * substituir as regras definitivas que serão aplicadas pelo backend.
 */
export function validarPerfilEstudante(valores: ValoresPerfilEstudante): ErrosPerfilEstudante {
  const erros: ErrosPerfilEstudante = {};

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
export function criarStudentDeValoresPerfil(valores: ValoresPerfilEstudante): Student {
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
export function traduzirFalhaPerfil(codigo: CodigoFalhaPerfilEstudante): string {
  const mensagens: Record<CodigoFalhaPerfilEstudante, string> = {
    indisponivel: "Não foi possível completar a operação no momento. Tente novamente mais tarde.",
    "resposta-invalida": "Recebemos uma resposta inesperada. Tente novamente mais tarde.",
    "nao-autorizado": "Você não tem permissão para realizar esta ação. Faça login novamente."
  };

  return mensagens[codigo];
}
