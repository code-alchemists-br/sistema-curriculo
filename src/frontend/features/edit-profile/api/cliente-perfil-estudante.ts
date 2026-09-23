import type { Student } from "../../../entities/student";

/** Enumera falhas que a interface pode explicar sem revelar detalhes técnicos. */
export type CodigoFalhaPerfilEstudante =
  | "indisponivel"
  | "resposta-invalida"
  | "nao-autorizado";

/**
 * Representa uma falha conhecida ao operar sobre o perfil do estudante.
 *
 * A classe transporta apenas um código estável para a interface. Ela existe
 * para separar a mensagem exibida ao estudante de futuros detalhes de HTTP,
 * persistência ou backend.
 */
export class FalhaPerfilEstudante extends Error {
  constructor(public readonly codigo: CodigoFalhaPerfilEstudante) {
    super(codigo);
    this.name = "FalhaPerfilEstudante";
  }
}

/**
 * Define as operações de manutenção do perfil usadas pela tela de configurações.
 *
 * O contrato recebe a entidade já normalizada e omite transporte e banco. Ele
 * existe para permitir testes com doubles e futura troca por um cliente HTTP
 * sem acoplar o componente visual à API.
 */
export interface ClientePerfilEstudante {
  atualizar(dados: Student): Promise<void>;
  excluir(): Promise<void>;
}

/**
 * Cria o cliente provisório para o estado em que não existe API disponível.
 *
 * A implementação devolve falhas controladas em ambas as operações. Isso evita
 * prometer ao estudante que os dados foram alterados ou excluídos antes de
 * existir contrato de backend.
 */
export function criarClientePerfilIndisponivel(): ClientePerfilEstudante {
  return {
    async atualizar() {
      throw new FalhaPerfilEstudante("indisponivel");
    },
    async excluir() {
      throw new FalhaPerfilEstudante("indisponivel");
    }
  };
}
