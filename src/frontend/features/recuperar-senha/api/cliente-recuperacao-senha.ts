/** Define o dado mínimo necessário para solicitar a recuperação de senha. */
export interface SolicitarRecuperacaoSenhaEntrada {
  email: string;
}

/** Enumera falhas que podem ser apresentadas sem expor detalhes internos. */
export type CodigoFalhaRecuperacaoSenha =
  "indisponivel" | "rede" | "resposta-invalida";

/** Representa uma falha conhecida no pedido de recuperação de senha. */
export class FalhaRecuperacaoSenha extends Error {
  constructor(public readonly codigo: CodigoFalhaRecuperacaoSenha) {
    super(codigo);
    this.name = "FalhaRecuperacaoSenha";
  }
}

/** Define a operação remota usada pela tela sem acoplar a UI a HTTP. */
export interface ClienteRecuperacaoSenha {
  solicitar(entrada: SolicitarRecuperacaoSenhaEntrada): Promise<void>;
}

/**
 * Cria um cliente provisório que declara a integração como indisponível.
 *
 * A implementação nunca armazena e-mails nem simula envio de mensagem. Ela
 * existe para compor a tela sem declarar um backend inexistente como pronto.
 */
export function criarClienteRecuperacaoSenhaIndisponivel(): ClienteRecuperacaoSenha {
  return {
    async solicitar() {
      throw new FalhaRecuperacaoSenha("indisponivel");
    },
  };
}
