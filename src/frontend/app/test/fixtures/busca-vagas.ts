/**
 * Fornece massas e transporte remoto controlado para integrar página e cliente.
 * Usa fila de promises e critérios copiados para tornar estados determinísticos.
 * Não é E2E integrado: sem navegador, rota no App ou ligação com main/provedor;
 * associacoes é incompatível com vagas/total e não há conversão entre as pontas.
 */
// Proveniência: decision-analysis prompts/frontend/20261024-181303-cenario-busca-vagas-tres-desfechos-v001.md#v001
import { vi } from "vitest";

import type { CriteriosPesquisaVagas } from "../../../features/listar-vagas";

/**
 * Define os campos externos da massa sintética.
 * Tipifica strings, requisitos e opcionais nulos conforme o contrato da UI,
 * para preparar respostas que exercitem o schema real sem dados pessoais.
 */
export interface VagaSintetica {
  id: string;
  titulo: string;
  empresa: string;
  descricao: string;
  requisitos: string[];
  localizacao: string | null;
  modalidade: string | null;
  url_candidatura: string | null;
}

export const VAGAS: VagaSintetica[] = [
  {
    id: "vaga-e2e-001",
    titulo: "Estágio Python Sintético",
    empresa: "Empresa Sintética",
    descricao: "Atividades sintéticas de teste.",
    requisitos: ["Python", "Git"],
    localizacao: "Cidade Sintética",
    modalidade: "REMOTO",
    url_candidatura: "https://vagas.invalid/001",
  },
  {
    id: "vaga-e2e-002",
    titulo: "QA Sintético",
    empresa: "Empresa Sintética",
    descricao: "Atividades sintéticas de teste.",
    requisitos: [],
    localizacao: null,
    modalidade: "REMOTO",
    url_candidatura: null,
  },
];

/**
 * Cria resposta do contrato específico da UI, sem consumir resposta da API.
 * Envolve cópias das vagas em sugestões com currículo sintético para que Zod
 * e o cliente de produção façam a única adaptação exercitada pela integração.
 */
export function respostaResultado(vagas: VagaSintetica[] = VAGAS) {
  return {
    associacoes: vagas.map(
      /** Copia os campos e requisitos para isolar a massa sem alterar seu contrato. */
      (vaga) => ({
        curriculo_id: "curriculo-sintetico-001",
        vaga: { ...vaga, requisitos: [...vaga.requisitos] },
      }),
    ),
  };
}

export const RESPOSTA_VAZIA = { associacoes: [] };
export const RESPOSTA_MALFORMADA = { associacoes: [{ vaga: {} }] };
// Massa incompatível intencional: não é adapter e nunca é convertida para a UI.
export const RESPOSTA_API_INCOMPATIVEL = {
  termo: "Python",
  filtros: {},
  total: 2,
  vagas: VAGAS,
};

/**
 * Representa uma resposta pendente e seus controles explícitos de conclusão.
 * Expõe resolver/rejeitar da promise para testar loading e falha sem relógio,
 * rede ou atrasos arbitrários, mantendo o mesmo cliente de produção.
 */
export interface RespostaPendente {
  promise: Promise<unknown>;
  resolver: (valor: unknown) => void;
  rejeitar: (erro: unknown) => void;
}

/**
 * Prepara promise pendente com controles de sucesso e falha.
 * Captura os callbacks nativos sem timers para estabilizar transições reais
 * da página e tornar verificável o estado anterior à conclusão remota.
 */
function criarPendente(): RespostaPendente {
  let resolver!: RespostaPendente["resolver"];
  let rejeitar!: RespostaPendente["rejeitar"];
  const promise = new Promise<unknown>(
    /** Captura os controles nativos para concluir a resposta quando o teste decidir. */
    (resolve, reject) => {
      resolver = resolve;
      rejeitar = reject;
    },
  );
  return { promise, resolver, rejeitar };
}

/**
 * Simula apenas a função remota injetada, registrando critérios imutáveis.
 * Consome uma fila de promises com vi.fn para provar chamadas e retentativas
 * sem substituir listarSugestoes, schema, mensagens ou componentes reais.
 */
export class TransporteVagasRegistrado {
  private fila: RespostaPendente[] = [];
  private registros: Readonly<CriteriosPesquisaVagas>[] = [];

  /**
   * Registra a consulta e entrega a próxima promise prevista.
   * Copia os critérios antes de consumir a fila para detectar chamadas extras
   * e comprovar que formulário e cliente realmente alcançam a função remota.
   */
  readonly consultar = vi.fn(
    /** Encaminha uma chamada à fila registrada para controlar somente a fronteira remota. */
    (criterios: CriteriosPesquisaVagas): Promise<unknown> => {
      this.registros.push(Object.freeze({ ...criterios }));
      const proxima = this.fila.shift();
      if (!proxima) throw new Error("Consulta sem resposta remota prevista.");
      return proxima.promise;
    },
  );

  /**
   * Expõe cópia do histórico para comparar parâmetros e ordem das chamadas.
   * Retorna array novo de registros congelados para impedir alteração da prova
   * pelo consumidor e preservar a identidade causal das retentativas.
   */
  get chamadas(): readonly Readonly<CriteriosPesquisaVagas>[] {
    return [...this.registros];
  }

  /**
   * Acrescenta uma resposta pendente e devolve seus controles ao teste.
   * Cria uma promise por consulta para que cada transição seja concluída
   * explicitamente, sem concorrência acidental ou dependência de relógio.
   */
  enfileirar(): RespostaPendente {
    const pendente = criarPendente();
    this.fila.push(pendente);
    return pendente;
  }
}
