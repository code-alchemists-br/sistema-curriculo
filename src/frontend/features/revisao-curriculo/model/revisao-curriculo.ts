/**
 * Proveniência: F6.15 - Painel Acessível de Revisão.
 * Camada: features/revisao-curriculo/model.
 */

/**
 * Seções suportadas no processo de revisão do currículo.
 */
export type SecaoRevisao =
  | "dados-pessoais"
  | "formacao-academica"
  | "experiencias-profissionais"
  | "competencias"
  | "projetos-academicos"
  | "idiomas";

/**
 * Severidade atribuída a uma pendência de revisão.
 *
 * - erro: pendência impeditiva que bloqueia a aprovação ou exportação final.
 * - aviso: recomendação ou sugestão de melhoria que não impede a aprovação.
 */
export type SeveridadeRevisao = "erro" | "aviso";

/**
 * Representa um item ou pendência identificada durante a revisão do currículo.
 */
export interface ItemRevisao {
  /** Código técnico estável da regra avaliada (ex: 'FORMACAO_AUSENTE'). */
  codigo: string;
  /** Identificador da seção associada à pendência. */
  secao: SecaoRevisao;
  /** Mensagem amigável legível explicando o motivo ou a orientação. */
  mensagem: string;
  /** Nível de severidade: 'erro' ou 'aviso'. */
  severidade: SeveridadeRevisao;
}

/**
 * Representa o conjunto consolidado da revisão de um currículo.
 */
export interface ResultadoRevisao {
  /** Lista de todas as pendências identificadas. */
  itens: ItemRevisao[];
  /** Indica se o currículo está aprovado (verdadeiro quando não há pendências de erro). */
  aprovado: boolean;
}

/**
 * Agrupamento de itens de revisão pertencentes a uma mesma seção do currículo.
 */
export interface GrupoSecaoRevisao {
  /** Identificador da seção. */
  secao: SecaoRevisao;
  /** Rótulo textual legível da seção em pt-BR. */
  tituloSecao: string;
  /** Itens de severidade 'erro' pertencentes à seção. */
  erros: ItemRevisao[];
  /** Itens de severidade 'aviso' pertencentes à seção. */
  avisos: ItemRevisao[];
  /** Total de pendências (erros + avisos) na seção. */
  total: number;
  /** Indica se a seção contém erros impeditivos. */
  temErros: boolean;
}

/**
 * Mapeamento determinístico de identificadores de seção para rótulos legíveis.
 */
export const ROTULOS_SECAO: Record<SecaoRevisao, string> = {
  "dados-pessoais": "Dados pessoais",
  "formacao-academica": "Formação acadêmica",
  "experiencias-profissionais": "Experiência profissional",
  competencias: "Competências",
  "projetos-academicos": "Projetos acadêmicos",
  idiomas: "Idiomas",
};

/**
 * Ordem canônica de apresentação das seções no painel de revisão.
 */
export const ORDEM_CANONICA_SECOES: readonly SecaoRevisao[] = [
  "dados-pessoais",
  "formacao-academica",
  "experiencias-profissionais",
  "competencias",
  "projetos-academicos",
  "idiomas",
];

/**
 * Retorna o rótulo amigável em português para uma seção de revisão.
 *
 * - O que faz: Traduz o identificador kebab-case para o nome formatado da seção.
 * - Como faz: Consulta a tabela constante `ROTULOS_SECAO`.
 * - Qual finalidade atende: Padroniza a apresentação dos nomes das seções na interface.
 *
 * @param secao Identificador da seção.
 * @returns Nome legível da seção.
 */
export function obterRotuloSecao(secao: SecaoRevisao): string {
  return ROTULOS_SECAO[secao] ?? secao;
}

/**
 * Avalia se a lista de itens de revisão confere aprovação ao currículo.
 *
 * - O que faz: Verifica se existe alguma pendência classificada com severidade 'erro'.
 * - Como faz: Percorre o array e retorna falso se encontrar algum item com severidade igual a 'erro'.
 * - Qual finalidade atende: Determina se o currículo cumpre todos os requisitos obrigatórios para liberação.
 *
 * @param itens Lista de itens de revisão.
 * @returns Verdadeiro se não houver erros impeditivos.
 */
export function isCurriculoAprovado(itens: ItemRevisao[]): boolean {
  return !itens.some((item) => item.severidade === "erro");
}

/**
 * Calcula os totais acumulados de erros e avisos da revisão.
 *
 * - O que faz: Contabiliza o número total de erros impeditivos e avisos recomendatórios.
 * - Como faz: Itera sobre os itens acumulando os contadores de acordo com a propriedade `severidade`.
 * - Qual finalidade atende: Alimenta resumos estatísticos e anúncios de acessibilidade no painel.
 *
 * @param itens Lista de itens de revisão.
 * @returns Objeto com contadores e status de aprovação.
 */
export function calcularTotaisRevisao(itens: ItemRevisao[]): {
  totalErros: number;
  totalAvisos: number;
  aprovado: boolean;
} {
  let totalErros = 0;
  let totalAvisos = 0;

  for (const item of itens) {
    if (item.severidade === "erro") {
      totalErros += 1;
    } else {
      totalAvisos += 1;
    }
  }

  return {
    totalErros,
    totalAvisos,
    aprovado: totalErros === 0,
  };
}

/**
 * Agrupa os itens de revisão por seção e os subdivide por severidade.
 *
 * - O que faz: Organiza as pendências recebidas agrupando-as por seção e separando erros de avisos.
 * - Como faz: Itera pelas seções na ordem canônica e filtra os itens correspondentes a cada uma, populando as listas de erros e avisos.
 * - Qual finalidade atende: Fornece a estrutura de dados necessária para que o painel de revisão apresente as pendências de forma clara e acessível.
 *
 * @param itens Lista de pendências a agrupar.
 * @param incluirSecoesVazias Se verdadeiro, inclui no retorno seções sem pendências (padrão: false).
 * @returns Lista de grupos ordenados por seção.
 */
export function agruparRevisaoPorSecaoESeveridade(
  itens: ItemRevisao[],
  incluirSecoesVazias = false,
): GrupoSecaoRevisao[] {
  const grupos: GrupoSecaoRevisao[] = [];

  for (const secao of ORDEM_CANONICA_SECOES) {
    const itensSecao = itens.filter((item) => item.secao === secao);
    const erros = itensSecao.filter((item) => item.severidade === "erro");
    const avisos = itensSecao.filter((item) => item.severidade === "aviso");
    const total = itensSecao.length;

    if (total > 0 || incluirSecoesVazias) {
      grupos.push({
        secao,
        tituloSecao: obterRotuloSecao(secao),
        erros,
        avisos,
        total,
        temErros: erros.length > 0,
      });
    }
  }

  return grupos;
}
