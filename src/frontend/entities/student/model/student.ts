/** Define o máximo de telefones que um perfil de estudante pode manter. */
export const LIMITE_TELEFONES_ESTUDANTE = 5;

/** Representa os dados pessoais e de contato que pertencem a um estudante. */
export interface Student {
  nomeCompleto: string;
  enderecoCompleto: string;
  cidade: string;
  telefones: string[];
  email: string;
  linkedIn?: string;
  curriculoLattes?: string;
}
