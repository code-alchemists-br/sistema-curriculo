import type { SugestaoVaga } from "../../../entities/vaga";
import {
  FalhaVagasGrupo2,
  formatarDataPublicacao,
  formatarModalidade,
  formatarSenioridade,
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
  ranque?: number | null;
  pontuacao_compatibilidade?: number | null;
  elegivel?: boolean | null;
  nivel_senioridade?: string | null;
  salario?: string | null;
  moeda?: string | null;
  palavras_chave?: string[] | null;
  data_publicacao?: string | null;
  requisitos_atendidos?: string[] | null;
  requisitos_faltantes?: string[] | null;
}

interface ResultadoBuscaBackend {
  termo: string;
  total: number;
  vagas: VagaBackendResposta[];
}

function normalizarTexto(valor?: string | null): string | null {
  if (typeof valor !== "string") return null;
  const limpo = valor.trim();
  return limpo.length > 0 ? limpo : null;
}

/**
 * Cria o cliente HTTP para consulta de vagas no backend do sistema.
 *
 * **O que faz:** Consulta `GET /vagas` no backend autenticado e devolve `SugestaoVaga[]`.
 * **Como faz:** Envia os critérios com `credentials: "include"`, traduz status HTTP
 * de erro para `FalhaVagasGrupo2` e normaliza os campos opcionais retornados do cvmatch.
 * **Qual finalidade atende:** Conecta a interface web ao endpoint do próprio backend sem expor o cvmatch ao navegador.
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

        if (resposta.status === 429 || resposta.status >= 500) {
          throw new FalhaVagasGrupo2("indisponivel");
        }

        if (!resposta.ok) {
          throw new FalhaVagasGrupo2("resposta-invalida");
        }

        const dados = (await resposta.json()) as ResultadoBuscaBackend;
        const listaVagas = Array.isArray(dados?.vagas) ? dados.vagas : [];

        return listaVagas.map((v, index) => {
          const nivelSenioridade = formatarSenioridade(v.nivel_senioridade);
          const salario = normalizarTexto(v.salario);
          const moeda = normalizarTexto(v.moeda);
          const dataPublicacao = formatarDataPublicacao(v.data_publicacao);
          const palavrasChave = Array.isArray(v.palavras_chave)
            ? v.palavras_chave.filter(
                (item): item is string =>
                  typeof item === "string" && item.trim().length > 0,
              )
            : [];
          const requisitosAtendidos = Array.isArray(v.requisitos_atendidos)
            ? v.requisitos_atendidos
            : undefined;
          const requisitosFaltantes = Array.isArray(v.requisitos_faltantes)
            ? v.requisitos_faltantes
            : undefined;

          return {
            curriculoId: "curriculo-ativo",
            ranque:
              typeof v.ranque === "number" && v.ranque >= 1
                ? v.ranque
                : index + 1,
            ...(typeof v.pontuacao_compatibilidade === "number"
              ? { pontuacaoCompatibilidade: v.pontuacao_compatibilidade }
              : {}),
            vaga: {
              id: v.id,
              titulo: v.titulo,
              empresa: v.empresa,
              descricao: v.descricao,
              requisitos: Array.isArray(v.requisitos) ? v.requisitos : [],
              localizacao: normalizarTexto(v.localizacao),
              modalidade: formatarModalidade(v.modalidade),
              urlCandidatura: normalizarTexto(v.url_candidatura),
              ...(nivelSenioridade !== null ? { nivelSenioridade } : {}),
              ...(salario !== null ? { salario } : {}),
              ...(moeda !== null ? { moeda } : {}),
              ...(palavrasChave.length > 0 ? { palavrasChave } : {}),
              ...(dataPublicacao !== null ? { dataPublicacao } : {}),
              ...(typeof v.elegivel === "boolean"
                ? { elegivel: v.elegivel }
                : {}),
              ...(requisitosAtendidos ? { requisitosAtendidos } : {}),
              ...(requisitosFaltantes ? { requisitosFaltantes } : {}),
            },
          };
        });
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
