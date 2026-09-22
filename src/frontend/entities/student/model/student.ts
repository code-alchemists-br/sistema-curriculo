/** Representa os dados pessoais e de contato que pertencem a um estudante. */
export interface Student {
  nomeCompleto: string;
  enderecoCompleto: string;
  telefones: string[];
  email: string;
  linkedIn?: string;
  curriculoLattes?: string;
}
