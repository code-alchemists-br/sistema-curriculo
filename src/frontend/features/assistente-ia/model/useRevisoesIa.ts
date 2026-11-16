import { useCallback, useRef, useState } from "react";

import type { ClienteAssistenteIa } from "../api/cliente-assistente-ia";
import { estadoDoTexto, registrarRevisao, type MemoriaRevisao } from "./revisao";
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
 * `revisarAntesDeSalvar` devolve, por índice, a pendência que impede salvar:
 * - texto inválido (tipo "erro"): precisa ser reescrito;
 * - texto que acabou de receber sugestões de melhoria (tipo "aviso"): para
 *   uma vez, para o estudante ver as sugestões; no próximo clique ele segue
 *   com o próprio texto.
 * Se a IA falhar, o item segue sem bloqueio (a IA é opcional).
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
    async (itens: TextoParaRevisar[]): Promise<Record<number, PendenciaRevisao>> => {
      const bloqueios: Record<number, PendenciaRevisao> = {};
      for (const [indice, item] of itens.entries()) {
        const texto = item.texto.trim();
        if (!texto) continue;
        const memoria = atual.current[indice] ?? MEMORIA_VAZIA;
        const estado = estadoDoTexto(memoria, item.texto);
        if (estado === "aprovado" || estado === "ia-indisponivel") continue;
        try {
          const revisao = await cliente.revisar({
            campo: item.campo,
            texto: item.texto,
            pergunta: item.pergunta,
            contexto: item.contexto,
          });
          atualizar(indice, registrarRevisao(item.texto, revisao));
          if (revisao.situacao === "invalido") {
            bloqueios[indice] = {
              tipo: "erro",
              mensagem: "A IA marcou este texto como inválido. Reescreva ou use um modelo sugerido.",
            };
          } else if (revisao.situacao === "melhorado") {
            bloqueios[indice] = {
              tipo: "aviso",
              mensagem: "Texto aprovado. Veja as sugestões da IA ou clique em Próximo de novo para manter o seu.",
            };
          }
        } catch {
          atualizar(indice, { ...memoria, iaIndisponivel: true });
        }
      }
      return bloqueios;
    },
    [cliente, atualizar],
  );

  return { memoriaDe, atualizar, revisarAntesDeSalvar };
}
