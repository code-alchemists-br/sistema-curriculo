import type { EstadoTextoIa, RevisaoTexto } from "./tipos";

/** Última revisão feita e o texto a que ela se refere. */
export interface MemoriaRevisao {
  revisao?: RevisaoTexto;
  revisadoPara?: string;
  /** Texto aprovado por ter vindo de uma sugestão de texto válido. */
  aprovadoPara?: string;
  iaIndisponivel: boolean;
}

/**
 * Calcula o estado do texto atual.
 *
 * - aprovado: a IA aceitou este texto, ou ele veio de uma sugestão válida.
 * - invalido: a última revisão recusou o texto; vale até uma nova revisão
 *   aprovar, mesmo que o estudante edite o campo.
 * - nao-revisado: ainda não passou pela IA (não bloqueia: a IA é opcional).
 */
export function estadoDoTexto(memoria: MemoriaRevisao, texto: string): EstadoTextoIa {
  if (memoria.iaIndisponivel) return "ia-indisponivel";
  if (memoria.aprovadoPara !== undefined && memoria.aprovadoPara === texto) return "aprovado";
  if (memoria.revisao && !memoria.revisao.podeManterTexto) return "invalido";
  if (memoria.revisao && memoria.revisadoPara === texto) return "aprovado";
  return "nao-revisado";
}

/** Guarda o resultado de uma revisão do texto atual. */
export function registrarRevisao(texto: string, revisao: RevisaoTexto): MemoriaRevisao {
  return {
    revisao,
    revisadoPara: texto,
    aprovadoPara: revisao.podeManterTexto ? texto : undefined,
    iaIndisponivel: false,
  };
}

/** Registra que o estudante usou uma sugestão; modelos de texto inválido ainda pedem revisão. */
export function registrarSugestaoUsada(memoria: MemoriaRevisao, sugestao: string): MemoriaRevisao {
  return memoria.revisao?.podeManterTexto ? { ...memoria, aprovadoPara: sugestao } : memoria;
}
