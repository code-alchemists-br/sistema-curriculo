/** Representa a escolha explícita do estudante para uma vaga sugerida. */
export type DecisaoRecomendacao = "aceitar" | "rejeitar";

/** Identifica a sugestão cuja decisão deve ser registrada. */
export interface DecisaoRecomendacaoEntrada {
  curriculoId: string;
  vagaId: string;
  decisao: DecisaoRecomendacao;
}

/** Define a fronteira usada pela interface para persistir a decisão. */
export interface ClienteDecisoesRecomendacao {
  salvarDecisao(entrada: DecisaoRecomendacaoEntrada): Promise<void>;
}

/**
 * Cria um cliente temporariamente indisponível para decisões de recomendação.
 *
 * A implementação rejeita a operação até existir uma integração confirmada de
 * associação currículo-vaga. Ela existe para impedir que a UI confirme como
 * salva uma decisão que ainda não foi persistida pelo sistema.
 */
export function criarClienteDecisoesRecomendacaoIndisponivel(): ClienteDecisoesRecomendacao {
  return {
    async salvarDecisao() {
      throw new Error("indisponivel");
    },
  };
}
