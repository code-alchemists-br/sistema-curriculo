import type { SugestaoVaga } from "../../../entities/vaga";
import {
  FalhaVagasGrupo2,
  type ClienteVagasGrupo2,
  type CriteriosPesquisaVagas,
} from "./cliente-vagas-grupo2";

interface VagaBackendResposta {
  id: string;
  titulo: string;
  empresa: string;
  descricao: string;
  requisitos?: string[];
  localizacao?: string | null;
  modalidade?: string | null;
  url_candidatura?: string | null;
}

interface ResultadoBuscaBackend {
  termo: string;
  total: number;
  vagas: VagaBackendResposta[];
}

/**
 * Cria o cliente HTTP para consulta de vagas no backend do sistema.
 *
 * Envia os critérios de pesquisa para GET /vagas com credentials: "include",
 * adaptando o resultado para o contrato SugestaoVaga[] consumido pela interface.
 */
export function criarClienteVagasHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteVagasGrupo2 {
  return {
    async listarSugestoes(
      criterios: CriteriosPesquisaVagas,
    ): Promise<SugestaoVaga[]> {
      if (!urlDaApi || urlDaApi.trim() === "") {
        throw new FalhaVagasGrupo2("indisponivel");
      }

      const baseUrl = urlDaApi.replace(/\/+$/, "");
      const params = new URLSearchParams();
      if (criterios.termo.trim()) {
        params.set("termo", criterios.termo.trim());
      }

      const url = `${baseUrl}/vagas${params.toString() ? `?${params.toString()}` : ""}`;

      try {
        const resposta = await fetch(url, {
          method: "GET",
          headers: {
            Accept: "application/json",
          },
          credentials: "include",
        });

        if (resposta.status === 504) {
          throw new FalhaVagasGrupo2("tempo-limite");
        }

        if (resposta.status >= 500) {
          throw new FalhaVagasGrupo2("indisponivel");
        }

        if (!resposta.ok) {
          throw new FalhaVagasGrupo2("resposta-invalida");
        }

        const dados = (await resposta.json()) as ResultadoBuscaBackend;
        const listaVagas = Array.isArray(dados?.vagas) ? dados.vagas : [];

        return listaVagas.map((v, index) => ({
          curriculoId: "curriculo-ativo",
          ranque: index + 1,
          vaga: {
            id: v.id,
            titulo: v.titulo,
            empresa: v.empresa,
            descricao: v.descricao,
            requisitos: Array.isArray(v.requisitos) ? v.requisitos : [],
            localizacao: v.localizacao ?? null,
            modalidade: v.modalidade ?? null,
            urlCandidatura: v.url_candidatura ?? null,
          },
        }));
      } catch (erro: unknown) {
        if (erro instanceof FalhaVagasGrupo2) {
          throw erro;
        }
        if (
          erro instanceof Error &&
          /timeout|tempo[- ]limite|timed?[\s_-]?out/i.test(erro.message)
        ) {
          throw new FalhaVagasGrupo2("tempo-limite");
        }
        throw new FalhaVagasGrupo2("indisponivel");
      }
    },
  };
}

