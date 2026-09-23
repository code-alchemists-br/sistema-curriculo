import type { Student } from "../../../entities/student";

/** Enumera falhas que a interface pode explicar sem revelar detalhes técnicos. */
export type CodigoFalhaDadosPessoais = "indisponivel" | "resposta-invalida";

/**
 * Representa uma falha conhecida ao salvar os dados pessoais.
 *
 * A classe transporta apenas um código estável para a interface. Ela existe
 * para separar a mensagem exibida ao estudante de futuros detalhes de HTTP,
 * persistência ou backend.
 */
export class FalhaDadosPessoais extends Error {
  constructor(public readonly codigo: CodigoFalhaDadosPessoais) {
    super(codigo);
    this.name = "FalhaDadosPessoais";
  }
}

/**
 * Define a operação de manutenção de dados pessoais usada pelo formulário.
 *
 * O contrato recebe a entidade já normalizada e omite transporte e banco. Ele
 * existe para permitir testes com doubles e futura troca por um cliente HTTP
 * sem acoplar o componente visual à API.
 */
export interface ClienteDadosPessoais {
  salvar(dados: Student): Promise<void>;
}

/**
 * Cria o cliente provisório para o estado em que não existe API disponível.
 *
 * A implementação não persiste nem simula sucesso: ela devolve uma falha
 * controlada. Isso evita prometer ao estudante que os dados foram salvos antes
 * de existir contrato de backend.
 */
export function criarClienteDadosPessoaisIndisponivel(): ClienteDadosPessoais {
  return {
    async salvar() {
      throw new FalhaDadosPessoais("indisponivel");
    }
  };
}
