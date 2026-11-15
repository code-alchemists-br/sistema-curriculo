import type { Idioma } from "../model/idiomas";

export type CodigoFalhaIdioma = "indisponivel" | "rede" | "resposta-invalida";

export class FalhaIdioma extends Error {
  constructor(public readonly codigo: CodigoFalhaIdioma) {
    super(codigo);
    this.name = "FalhaIdioma";
  }
}

export interface ClienteIdiomas {
  salvar(idiomas: Idioma[]): Promise<void>;
}

/**
 * Cria o cliente HTTP para persistência de idiomas no backend.
 *
 * Envia cada idioma preenchido para POST /idiomas com credentials: "include".
 */
export function criarClienteIdiomasHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteIdiomas {
  return {
    async salvar(idiomas: Idioma[]): Promise<void> {
      if (!urlDaApi || urlDaApi.trim() === "") {
        throw new FalhaIdioma("indisponivel");
      }

      const baseUrl = urlDaApi.replace(/\/+$/, "");

      if (idiomas.length === 0) {
        return;
      }

      for (const item of idiomas) {
        if (!item.nome.trim() || !item.nivel) continue;

        const payload = {
          idioma: item.nome.trim(),
          nivel: item.nivel,
        };

        try {
          const resposta = await fetch(`${baseUrl}/idiomas`, {
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
            throw new FalhaIdioma("indisponivel");
          }

          throw new FalhaIdioma("resposta-invalida");
        } catch (erro: unknown) {
          if (erro instanceof FalhaIdioma) {
            throw erro;
          }
          throw new FalhaIdioma("rede");
        }
      }
    },
  };
}
