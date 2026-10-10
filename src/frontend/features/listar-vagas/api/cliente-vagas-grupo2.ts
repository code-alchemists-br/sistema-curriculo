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

/** Enumera as falhas que a tela consegue comunicar ao estudante. */
export type CodigoFalhaVagasGrupo2 = "indisponivel" | "resposta-invalida";

/**
 * Representa uma falha conhecida da fronteira de vagas externas.
 *
 * A classe carrega um código estável, sem propagar detalhes internos da
 * integração. Ela existe para que a interface ofereça uma recuperação clara
 * quando o Grupo 2 estiver indisponível ou responder fora do contrato.
 */
export class FalhaVagasGrupo2 extends Error {
  constructor(public readonly codigo: CodigoFalhaVagasGrupo2) {
    super(codigo);
    this.name = "FalhaVagasGrupo2";
  }
}

/** Define o contrato consumido pela tela para obter sugestões de vagas. */
export interface ClienteVagasGrupo2 {
  listarSugestoes(): Promise<SugestaoVaga[]>;
}

/**
 * Cria um cliente de interface a partir de uma função que consulta o Grupo 2.
 *
 * A fábrica recebe uma função assíncrona para que o futuro adaptador HTTP fique
 * fora da UI, valida o JSON devolvido e o converte para o modelo interno. Ela
 * existe para manter a página independente de endpoint, autenticação e rede.
 */
export function criarClienteVagasGrupo2(
  requisitarResposta: () => Promise<unknown>,
): ClienteVagasGrupo2 {
  return {
    async listarSugestoes() {
      try {
        const resposta = await requisitarResposta();
        return adaptarRespostaGrupo2(resposta);
      } catch (erro: unknown) {
        if (erro instanceof FalhaVagasGrupo2) throw erro;
        throw new FalhaVagasGrupo2("indisponivel");
      }
    },
  };
}

/**
 * Cria o cliente padrão enquanto o endpoint real do Grupo 2 não está definido.
 *
 * A implementação falha de modo controlado em vez de inventar uma URL ou uma
 * resposta local. Ela existe para tornar explícita a dependência pendente e
 * permitir que os testes injetem doubles determinísticos.
 */
export function criarClienteVagasGrupo2Indisponivel(): ClienteVagasGrupo2 {
  return {
    async listarSugestoes() {
      throw new FalhaVagasGrupo2("indisponivel");
    },
  };
}

/**
 * Valida e converte a resposta externa na entidade usada pela interface.
 *
 * A função confere o envelope `associacoes`, preserva o currículo associado e
 * transforma `url_candidatura` em `urlCandidatura`. Ela existe para impedir que
 * o DTO externo se espalhe para os componentes visuais.
 */
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
