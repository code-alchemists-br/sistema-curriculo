import {
  certificacaoEstaVazia,
  normalizarCertificacao,
  validarCertificacao,
  type ValoresCertificacao,
} from "../model/certificacao";

export type CodigoFalhaCertificacao =
  "indisponivel" | "rede" | "resposta-invalida";

/**
 * Encapsula um código estável em Error para classificar configuração, rede e
 * rejeição do lote sem expor detalhes internos do servidor à interface.
 */
export class FalhaCertificacao extends Error {
  /** Registra o código e identifica a classe para permitir tratamento tipado da falha. */
  constructor(
    public readonly codigo: CodigoFalhaCertificacao,
    public readonly statusHttp?: number,
  ) {
    super(codigo);
    this.name = "FalhaCertificacao";
  }
}

/** Define a porta de persistência de listas para manter a UI independente de HTTP. */
export interface ClienteCertificacoes {
  /** Persiste o lote por promessa para permitir avanço somente após confirmação. */
  salvar(
    certificacoes: ValoresCertificacao[],
    signal?: AbortSignal,
  ): Promise<void>;
}

/**
 * Cria o cliente HTTP para persistência de certificações no backend.
 *
 * Valida todo o lote e envia os payloads normalizados por POST /certificacoes com cookies.
 * Um Set por instância evita reenviar payloads confirmados ao retornar ou repetir
 * após sucesso parcial. O chamador deve manter uma instância por identidade;
 * não há sincronização remota nem atualização dos registros já cadastrados.
 */
export function criarClienteCertificacoesHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteCertificacoes {
  const confirmados = new Set<string>();

  return {
    /**
     * Valida o lote inteiro antes de qualquer POST e registra somente confirmações.
     * Assim, rascunhos parciais não são perdidos e o retry preserva sucessos anteriores.
     */
    async salvar(
      certificacoes: ValoresCertificacao[],
      signal?: AbortSignal,
    ): Promise<void> {
      const preenchidos = certificacoes.filter(
        (item) => !certificacaoEstaVazia(item),
      );
      if (
        preenchidos.some(
          (item) => Object.keys(validarCertificacao(item)).length > 0,
        )
      ) {
        throw new FalhaCertificacao("resposta-invalida");
      }
      const normalizados = preenchidos.map(normalizarCertificacao);
      if (normalizados.length === 0) return;

      if (!urlDaApi || urlDaApi.trim() === "") {
        throw new FalhaCertificacao("indisponivel");
      }

      const baseUrl = urlDaApi.replace(/\/+$/, "");

      for (const item of normalizados) {
        signal?.throwIfAborted();
        const payload = {
          nome: item.nome,
          organizacao_emissora: item.organizacaoEmissora,
        };
        const body = JSON.stringify(payload);
        if (confirmados.has(body)) continue;

        try {
          const resposta = await fetch(`${baseUrl}/certificacoes`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
            ...(signal ? { signal } : {}),
            body,
          });

          signal?.throwIfAborted();
          if (resposta.ok) {
            confirmados.add(body);
            continue;
          }

          if (resposta.status >= 500) {
            throw new FalhaCertificacao("indisponivel");
          }

          throw new FalhaCertificacao("resposta-invalida", resposta.status);
        } catch (erro: unknown) {
          if (erro instanceof FalhaCertificacao) {
            throw erro;
          }
          throw new FalhaCertificacao("rede");
        }
      }
    },
  };
}
