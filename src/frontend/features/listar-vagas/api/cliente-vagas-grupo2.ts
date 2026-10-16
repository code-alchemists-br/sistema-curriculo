import { z } from "zod";

import type { SugestaoVaga } from "../../../entities/vaga";

const vagaExternaSchema = z.object({
  id: z.string().trim().min(1),
  titulo: z.string().trim().min(1),
  empresa: z.string().trim().min(1),
  descricao: z.string().trim().min(1),
  requisitos: z.array(z.string()),
  localizacao: z.string().nullable(),
  modalidade: z.string().nullable(),
  url_candidatura: z.string().url().nullable(),
});

const respostaGrupo2Schema = z.object({
  associacoes: z.array(
    z.object({
      curriculo_id: z.string().trim().min(1),
      vaga: vagaExternaSchema,
    }),
  ),
});

/** Representa o único critério de pesquisa confirmado pela interface atual. */
export interface CriteriosPesquisaVagas {
  termo: string;
}

/**
 * Enumera os códigos das falhas que a tela de vagas comunica ao estudante de modo controlado.
 */
export type CodigoFalhaVagasGrupo2 =
  "indisponivel" | "resposta-invalida" | "tempo-limite";

/**
 * Representa uma falha conhecida e controlada da fronteira de vagas externas.
 *
 * **O que faz:** Encapsula o código de erro mapeado da comunicação externa.
 * **Como faz:** Estende a classe Error padrão atribuindo o código tipado à propriedade imutável `codigo`.
 * **Qual finalidade atende:** Permite que a camada de UI identifique o tipo de falha sem receber exceções brutas ou detalhes de rede.
 */
export class FalhaVagasGrupo2 extends Error {
  constructor(public readonly codigo: CodigoFalhaVagasGrupo2) {
    super(codigo);
    this.name = "FalhaVagasGrupo2";
  }
}

/** Define o contrato consumido pela tela para obter sugestões de vagas. */
export interface ClienteVagasGrupo2 {
  listarSugestoes(criterios: CriteriosPesquisaVagas): Promise<SugestaoVaga[]>;
}

/**
 * Cria um cliente de interface a partir de uma função que consulta o Grupo 2.
 *
 * **O que faz:** Encapsula a chamada remota e adapta respostas ou falhas para o contrato da interface.
 * **Como faz:** Recebe os critérios, delega a consulta para o adaptador injetado, valida a resposta externa via `adaptarRespostaGrupo2` e intercepta erros de transporte ou timeout para instâncias de `FalhaVagasGrupo2`.
 * **Qual finalidade atende:** Preserva o filtro informado e isola a tela de detalhes de rede, HTTP e serialização externa sem vazar termos técnicos.
 */
export function criarClienteVagasGrupo2(
  requisitarResposta: (criterios: CriteriosPesquisaVagas) => Promise<unknown>,
): ClienteVagasGrupo2 {
  return {
    async listarSugestoes(criterios) {
      try {
        const resposta = await requisitarResposta(criterios);
        return adaptarRespostaGrupo2(resposta);
      } catch (erro: unknown) {
        if (erro instanceof FalhaVagasGrupo2) throw erro;
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

/**
 * Cria o cliente padrão enquanto o endpoint real do Grupo 2 não está definido.
 *
 * A implementação falha de modo controlado em vez de inventar uma URL ou uma
 * resposta local. Ela existe para tornar explícita a dependência pendente.
 */
export function criarClienteVagasGrupo2Indisponivel(): ClienteVagasGrupo2 {
  return {
    async listarSugestoes() {
      throw new FalhaVagasGrupo2("indisponivel");
    },
  };
}

/** Valida e converte a resposta externa na entidade usada pela interface. */
export function adaptarRespostaGrupo2(resposta: unknown): SugestaoVaga[] {
  const resultado = respostaGrupo2Schema.safeParse(resposta);

  if (!resultado.success) {
    throw new FalhaVagasGrupo2("resposta-invalida");
  }

  return resultado.data.associacoes.map(({ curriculo_id, vaga }) => ({
    curriculoId: curriculo_id,
    vaga: {
      id: vaga.id,
      titulo: vaga.titulo,
      empresa: vaga.empresa,
      descricao: vaga.descricao,
      requisitos: vaga.requisitos,
      localizacao: vaga.localizacao,
      modalidade: vaga.modalidade,
      urlCandidatura: vaga.url_candidatura,
    },
  }));
}
