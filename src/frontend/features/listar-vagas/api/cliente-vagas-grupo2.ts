import { z } from "zod";

import type { SugestaoVaga } from "../../../entities/vaga";

const vagaExternaAssociacaoSchema = z.object({
  id: z.string().trim().min(1),
  titulo: z.string().trim().min(1),
  empresa: z.string().trim().min(1),
  descricao: z.string().trim().min(1),
  requisitos: z.array(z.string()),
  localizacao: z.string().nullable(),
  modalidade: z.string().nullable(),
  url_candidatura: z.string().url().nullable(),
});

const respostaAssociacoesGrupo2Schema = z.object({
  associacoes: z.array(
    z.object({
      curriculo_id: z.string().trim().min(1),
      vaga: vagaExternaAssociacaoSchema,
    }),
  ),
});

const jobMatchGrupo2Schema = z.object({
  id: z.string().trim().min(1).optional(),
  company: z.string().nullable().optional(),
  title: z.string().trim().min(1),
  description: z.string().trim().min(1),
  keywords: z.array(z.string()).nullable().optional(),
  location: z
    .union([z.string(), z.record(z.string(), z.unknown())])
    .nullable()
    .optional(),
  work_arrangement: z.string().nullable().optional(),
  seniority_level: z.string().nullable().optional(),
  skills: z.array(z.string()).nullable().optional(),
  salary: z
    .union([z.number(), z.string(), z.record(z.string(), z.unknown())])
    .nullable()
    .optional(),
  currency: z.string().nullable().optional(),
  job_url: z.string().url(),
  publication_date: z.string().nullable().optional(),
});

const respostaMatchesGrupo2Schema = z.object({
  curriculo_id: z.string().trim().min(1).optional(),
  matches: z.array(
    z.object({
      rank: z.number().int().positive().optional(),
      job: jobMatchGrupo2Schema,
      score: z.number().min(0).optional(),
      embedding_model: z.string().nullable().optional(),
      algorithm_version: z.string().nullable().optional(),
    }),
  ),
});

const TRADUCAO_MODALIDADE: Record<string, string> = {
  REMOTE: "Remoto",
  HYBRID: "Híbrido",
  ONSITE: "Presencial",
  ON_SITE: "Presencial",
  IN_PERSON: "Presencial",
  PRESENCIAL: "Presencial",
  REMOTO: "Remoto",
  HIBRIDO: "Híbrido",
};

const TRADUCAO_SENIORIDADE: Record<string, string> = {
  INTERN: "Estágio",
  INTERNSHIP: "Estágio",
  TRAINEE: "Trainee",
  JUNIOR: "Júnior",
  JR: "Júnior",
  MID: "Pleno",
  MID_LEVEL: "Pleno",
  PLENO: "Pleno",
  SENIOR: "Sênior",
  SR: "Sênior",
  LEAD: "Líder Técnico",
};

function limparValorOpcional(valor: unknown): string | null {
  if (typeof valor !== "string") return null;
  const limpo = valor.trim();
  if (!limpo || limpo.toLowerCase() === "string") return null;
  return limpo;
}

function formatarModalidade(valor?: string | null): string | null {
  const limpo = limparValorOpcional(valor);
  if (!limpo) return null;
  return TRADUCAO_MODALIDADE[limpo.toUpperCase()] ?? limpo;
}

function formatarSenioridade(valor?: string | null): string | null {
  const limpo = limparValorOpcional(valor);
  if (!limpo) return null;
  return TRADUCAO_SENIORIDADE[limpo.toUpperCase()] ?? limpo;
}

function formatarLocalizacao(
  localizacao?: string | Record<string, unknown> | null,
): string | null {
  if (!localizacao) return null;
  if (typeof localizacao === "string") {
    return limparValorOpcional(localizacao);
  }
  const partes = Object.values(localizacao)
    .map((item) => limparValorOpcional(item))
    .filter((item): item is string => item !== null);
  return partes.length > 0 ? partes.join(" - ") : null;
}

function obterSimboloMoeda(moeda?: string | null): string {
  const limpa = limparValorOpcional(moeda)?.toUpperCase();
  if (!limpa || limpa === "BRL") return "R$";
  if (limpa === "USD") return "US$";
  if (limpa === "EUR") return "€";
  return limpa;
}

function formatarNumeroMonetario(valor: number): string {
  return new Intl.NumberFormat("pt-BR", {
    maximumFractionDigits: 2,
  }).format(valor);
}

function formatarSalario(
  salario?: number | string | Record<string, unknown> | null,
  moeda?: string | null,
): string | null {
  if (salario === null || salario === undefined) return null;
  const simbolo = obterSimboloMoeda(moeda);

  if (typeof salario === "string") {
    const limpo = limparValorOpcional(salario);
    return limpo ? `${simbolo} ${limpo}` : null;
  }

  if (typeof salario === "number") {
    return salario > 0 ? `${simbolo} ${formatarNumeroMonetario(salario)}` : null;
  }

  const valoresNumericos = Object.values(salario)
    .filter((v): v is number => typeof v === "number" && Number.isFinite(v) && v > 0)
    .sort((a, b) => a - b);

  if (valoresNumericos.length === 0) return null;

  const menor = valoresNumericos[0];
  const maior = valoresNumericos[valoresNumericos.length - 1];

  if (menor === maior) {
    return `${simbolo} ${formatarNumeroMonetario(menor)}`;
  }

  return `${simbolo} ${formatarNumeroMonetario(menor)} – ${simbolo} ${formatarNumeroMonetario(maior)}`;
}

function formatarDataPublicacao(dataIso?: string | null): string | null {
  const limpa = limparValorOpcional(dataIso);
  if (!limpa) return null;
  const data = new Date(limpa);
  if (Number.isNaN(data.getTime())) return null;
  const dia = String(data.getUTCDate()).padStart(2, "0");
  const mes = String(data.getUTCMonth() + 1).padStart(2, "0");
  const ano = data.getUTCFullYear();
  return `${dia}/${mes}/${ano}`;
}

function limparListaStrings(lista?: string[] | null): string[] {
  if (!Array.isArray(lista)) return [];
  return lista
    .map((item) => limparValorOpcional(item))
    .filter((item): item is string => item !== null);
}

/** Representa o único critério de pesquisa confirmado pela interface atual. */
export interface CriteriosPesquisaVagas {
  termo: string;
}

/**
 * Enumera os códigos das falhas que a tela de vagas comunica ao estudante de modo controlado.
 */
export type CodigoFalhaVagasGrupo2 =
  | "indisponivel"
  | "resposta-invalida"
  | "tempo-limite";

/**
 * Representa uma falha conhecida e controlada da fronteira de vagas externas.
 *
 * **O que faz:** Encapsula o código de erro mapeado da comunicação externa.
 * **Como faz:** Estende a classe Error padrão atribuindo o código tipado à propriedade imutável `codigo`.
 * **Qual finalidade atende:** Permite que a camada de UI identifique o tipo de falha sem receber exceções brutas ou detalhes de rede.
 */
export class FalhaVagasGrupo2 extends Error {
  constructor(
    public readonly codigo: CodigoFalhaVagasGrupo2,
    mensagem?: string,
  ) {
    super(mensagem ?? codigo);
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
  const resultadoMatches = respostaMatchesGrupo2Schema.safeParse(resposta);
  if (resultadoMatches.success) {
    const curriculoPadrao =
      resultadoMatches.data.curriculo_id ?? "curriculo-padrao";

    return resultadoMatches.data.matches.map((match, indice) => {
      const { job } = match;
      const empresaLimpa =
        limparValorOpcional(job.company) ?? "Empresa confidencial";
      const requisitos = limparListaStrings(job.skills);
      const palavrasChave = limparListaStrings(job.keywords);
      const nivelSenioridade = formatarSenioridade(job.seniority_level);
      const salario = formatarSalario(job.salary, job.currency);
      const moeda = limparValorOpcional(job.currency);
      const dataPublicacao = formatarDataPublicacao(job.publication_date);

      return {
        curriculoId: curriculoPadrao,
        ...(match.rank !== undefined ? { ranque: match.rank } : {}),
        ...(match.score !== undefined
          ? { pontuacaoCompatibilidade: match.score }
          : {}),
        vaga: {
          id: job.id ?? `vaga-${match.rank ?? indice + 1}-${job.job_url}`,
          titulo: job.title.trim(),
          empresa: empresaLimpa,
          descricao: job.description.trim(),
          requisitos,
          localizacao: formatarLocalizacao(job.location),
          modalidade: formatarModalidade(job.work_arrangement),
          urlCandidatura: job.job_url,
          ...(nivelSenioridade !== null ? { nivelSenioridade } : {}),
          ...(salario !== null ? { salario } : {}),
          ...(moeda !== null ? { moeda } : {}),
          ...(palavrasChave.length > 0 ? { palavrasChave } : {}),
          ...(dataPublicacao !== null ? { dataPublicacao } : {}),
        },
      };
    });
  }

  const resultadoAssociacoes =
    respostaAssociacoesGrupo2Schema.safeParse(resposta);

  if (!resultadoAssociacoes.success) {
    throw new FalhaVagasGrupo2("resposta-invalida");
  }

  return resultadoAssociacoes.data.associacoes.map(({ curriculo_id, vaga }) => ({
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
