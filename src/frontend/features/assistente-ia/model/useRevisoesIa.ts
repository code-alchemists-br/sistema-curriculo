import { useCallback, useRef, useState } from "react";

import type { ClienteAssistenteIa } from "../api/cliente-assistente-ia";
import {
  estadoDoTexto,
  registrarRevisao,
  type MemoriaRevisao,
} from "./revisao";
import type { CampoRevisavel } from "./tipos";

/** Um texto da lista que deve passar pela IA antes de salvar. */
export interface TextoParaRevisar {
  texto: string;
  campo: CampoRevisavel;
  pergunta?: string;
  contexto?: Record<string, string>;
}

/**
 * Motivo para o formulário não avançar ainda.
 *
 * "erro" é texto inválido, que precisa ser reescrito. "aviso" é texto aceito
 * com sugestões de melhoria: o formulário para uma vez, sem visual de erro,
 * só para o estudante ver as sugestões.
 */
export interface PendenciaRevisao {
  mensagem: string;
  tipo: "erro" | "aviso";
}

const MEMORIA_VAZIA: MemoriaRevisao = { iaIndisponivel: false };

/**
 * Guarda a revisão de cada item de uma lista (experiências, projetos...) e
 * revisa automaticamente os textos ainda não aprovados quando o estudante
 * tenta avançar.
 *
 * `revisarAntesDeSalvar` envia ao mesmo tempo (em paralelo) todos os textos
 * que ainda precisam de revisão, para o estudante esperar uma só resposta da
 * IA em vez de uma por item. Devolve, por índice, a pendência que impede
 * salvar:
 * - texto inválido (tipo "erro"): precisa ser reescrito;
 * - texto aceito, válido ou melhorável (tipo "aviso"): para uma vez, para o
 *   estudante ver que a IA aprovou e conferir as sugestões; no próximo clique
 *   ele segue com o próprio texto, sem nova chamada à IA;
 * - IA que não respondeu (tipo "aviso"): para uma vez, avisando que o texto
 *   não foi revisado; no próximo clique o item segue sem revisão, porque a IA
 *   é opcional e não pode travar o cadastro.
 */
export function useRevisoesIa(cliente: ClienteAssistenteIa) {
  const [memorias, setMemorias] = useState<Record<number, MemoriaRevisao>>({});
  // Cópia síncrona para a revisão em lote ler o valor mais recente entre awaits.
  const atual = useRef(memorias);

  const atualizar = useCallback((indice: number, memoria: MemoriaRevisao) => {
    atual.current = { ...atual.current, [indice]: memoria };
    setMemorias(atual.current);
  }, []);

  const memoriaDe = useCallback(
    (indice: number) => memorias[indice] ?? MEMORIA_VAZIA,
    [memorias],
  );

  const revisarAntesDeSalvar = useCallback(
    async (
      itens: TextoParaRevisar[],
    ): Promise<Record<number, PendenciaRevisao>> => {
      const bloqueios: Record<number, PendenciaRevisao> = {};
      await Promise.all(
        itens.map(async (item, indice) => {
          if (!item.texto.trim()) return;
          const memoria = atual.current[indice] ?? MEMORIA_VAZIA;
          const estado = estadoDoTexto(memoria, item.texto);
          if (estado === "aprovado" || estado === "ia-indisponivel") return;
          try {
            const revisao = await cliente.revisar({
              campo: item.campo,
              texto: item.texto,
              pergunta: item.pergunta,
              contexto: item.contexto,
            });
            atualizar(indice, registrarRevisao(item.texto, revisao));
            bloqueios[indice] =
              revisao.situacao === "invalido"
                ? {
                    tipo: "erro",
                    mensagem:
                      "A IA marcou este texto como inválido. Reescreva ou use um modelo sugerido.",
                  }
                : {
                    tipo: "aviso",
                    mensagem:
                      "Texto aprovado pela IA. Veja as sugestões, se quiser, e clique em Próximo de novo para continuar.",
                  };
          } catch {
            atualizar(indice, { ...memoria, iaIndisponivel: true });
            bloqueios[indice] = {
              tipo: "aviso",
              mensagem:
                "A IA não conseguiu revisar o texto agora. Clique em Próximo de novo para continuar sem a revisão.",
            };
          }
        }),
      );
      return bloqueios;
    },
    [cliente, atualizar],
  );

  return { memoriaDe, atualizar, revisarAntesDeSalvar };
}
