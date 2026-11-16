import {
  estadoDoTexto,
  registrarSugestaoUsada,
  type MemoriaRevisao,
} from "../model/revisao";
import "./AssistenteIa.css";

const ROTULO_SITUACAO = {
  valido: "Texto aprovado",
  melhorado: "Dá para melhorar",
  invalido: "Texto não serve para esta pergunta",
} as const;

/** Props do painel de revisão encaixado abaixo de um campo de texto. */
export interface PainelRevisaoIaProps {
  id: string;
  texto: string;
  /** Revisão guardada pela página (vem de `useRevisoesIa`). */
  memoria: MemoriaRevisao;
  aoMudarMemoria: (memoria: MemoriaRevisao) => void;
  /** Substitui o texto do campo pela sugestão escolhida. */
  aoAplicarTexto: (texto: string) => void;
}

/**
 * Mostra o resultado da revisão automática (feita ao clicar em Próximo): o
 * veredito, o motivo e 3 sugestões de texto que o estudante pode usar.
 */
export function PainelRevisaoIa({
  id,
  texto,
  memoria,
  aoMudarMemoria,
  aoAplicarTexto,
}: PainelRevisaoIaProps) {
  const estado = estadoDoTexto(memoria, texto);
  const revisao = memoria.revisao;

  /**
   * Aplica a sugestão escolhida no campo e registra que ela foi usada.
   *
   * Sugestões de texto aceito passam a contar como aprovadas; modelos de texto
   * inválido continuam pedindo revisão. Existe para o botão "Usar sugestão".
   */
  function usar(sugestao: string): void {
    aoMudarMemoria(registrarSugestaoUsada(memoria, sugestao));
    aoAplicarTexto(sugestao);
  }

  return (
    <div className="painel-revisao-ia">
      <p
        aria-live="polite"
        className={`painel-revisao-ia__status painel-revisao-ia__status--${estado}`}
        id={`${id}-status`}
      >
        {estado === "aprovado"
          ? revisao?.sugestoes.length && memoria.revisadoPara === texto
            ? "✓ Texto aprovado pela IA. As sugestões abaixo são opcionais."
            : "✓ Texto aprovado pela IA."
          : estado === "invalido"
            ? "Reescreva o texto ou use um modelo abaixo."
            : estado === "nao-revisado" && texto.trim()
              ? "✦ A IA revisa este texto quando você clicar em Próximo."
              : ""}
      </p>

      {revisao && (
        <section
          aria-label="Revisão da IA"
          className={`painel-revisao-ia__revisao painel-revisao-ia__revisao--${revisao.situacao}`}
        >
          <p>
            <strong>{ROTULO_SITUACAO[revisao.situacao]}.</strong>{" "}
            {revisao.motivo}
          </p>
          {revisao.sugestoes.length > 0 && (
            <ol className="painel-revisao-ia__sugestoes">
              {revisao.sugestoes.map((sugestao, indice) => (
                <li key={sugestao}>
                  <p>{sugestao}</p>
                  <button
                    className="painel-revisao-ia__usar"
                    onClick={() => usar(sugestao)}
                    type="button"
                  >
                    {revisao.podeManterTexto
                      ? `Usar sugestão ${indice + 1}`
                      : `Usar modelo ${indice + 1}`}
                  </button>
                </li>
              ))}
            </ol>
          )}
        </section>
      )}
    </div>
  );
}
