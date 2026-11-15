import type { ValoresCertificacao } from "../model/certificacao";

export type CodigoFalhaCertificacao =
  "indisponivel" | "rede" | "resposta-invalida";

export class FalhaCertificacao extends Error {
  constructor(public readonly codigo: CodigoFalhaCertificacao) {
    super(codigo);
    this.name = "FalhaCertificacao";
  }
}

export interface ClienteCertificacoes {
  salvar(certificacoes: ValoresCertificacao[]): Promise<void>;
}

/**
 * Cria o cliente HTTP para persistência de certificações no backend.
 *
 * Envia cada certificação preenchida para POST /certificacoes com credentials: "include".
 */
export function criarClienteCertificacoesHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteCertificacoes {
  return {
    async salvar(certificacoes: ValoresCertificacao[]): Promise<void> {
      if (!urlDaApi || urlDaApi.trim() === "") {
        throw new FalhaCertificacao("indisponivel");
      }

      const baseUrl = urlDaApi.replace(/\/+$/, "");

      if (certificacoes.length === 0) {
        return;
      }

      for (const item of certificacoes) {
        if (!item.nome.trim() || !item.organizacaoEmissora.trim()) continue;

        const payload = {
          nome: item.nome.trim(),
          organizacao_emissora: item.organizacaoEmissora.trim(),
        };

        try {
          const resposta = await fetch(`${baseUrl}/certificacoes`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(payload),
          });

          if (resposta.status === 201 || resposta.ok) {
            continue;
          }

          if (resposta.status >= 500) {
            throw new FalhaCertificacao("indisponivel");
          }

          throw new FalhaCertificacao("resposta-invalida");
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
