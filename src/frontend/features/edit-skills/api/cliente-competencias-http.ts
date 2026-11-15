import type { Habilidades } from "../model/habilidades";

export type CodigoFalhaCompetencias =
  "indisponivel" | "rede" | "resposta-invalida";

export class FalhaCompetencias extends Error {
  constructor(public readonly codigo: CodigoFalhaCompetencias) {
    super(codigo);
    this.name = "FalhaCompetencias";
  }
}

export interface ClienteCompetencias {
  salvar(competencias: Habilidades): Promise<void>;
}

/**
 * Cria o cliente HTTP para persistência de competências no backend.
 *
 * Mapeia hard skills para a categoria "tecnica" e soft skills para "comportamental",
 * enviando requisições POST para /competencias com credentials: "include".
 */
export function criarClienteCompetenciasHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteCompetencias {
  return {
    async salvar(competencias: Habilidades): Promise<void> {
      if (!urlDaApi || urlDaApi.trim() === "") {
        throw new FalhaCompetencias("indisponivel");
      }

      const baseUrl = urlDaApi.replace(/\/+$/, "");

      const itens = [
        ...competencias.hardSkills.map((desc) => ({
          categoria: "tecnica",
          descricao: desc.trim(),
          nivel: "padrao",
        })),
        ...competencias.softSkills.map((desc) => ({
          categoria: "comportamental",
          descricao: desc.trim(),
          nivel: "padrao",
        })),
      ].filter((item) => item.descricao.length > 0);

      if (itens.length === 0) {
        return;
      }

      for (const item of itens) {
        try {
          const resposta = await fetch(`${baseUrl}/competencias`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(item),
          });

          if (resposta.status === 201 || resposta.ok) {
            continue;
          }

          if (resposta.status >= 500) {
            throw new FalhaCompetencias("indisponivel");
          }

          throw new FalhaCompetencias("resposta-invalida");
        } catch (erro: unknown) {
          if (erro instanceof FalhaCompetencias) {
            throw erro;
          }
          throw new FalhaCompetencias("rede");
        }
      }
    },
  };
}
