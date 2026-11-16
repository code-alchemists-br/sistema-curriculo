import { useEffect, useRef, useState } from "react";

import type { ClienteAssistenteIa } from "../api/cliente-assistente-ia";
import type {
  InformacaoPerfil,
  ModeloSugerido,
  RecomendacaoModelo,
} from "../model/tipos";
import "./AssistenteIa.css";

/** Props do botão que pede à IA o modelo de currículo. */
export interface RecomendacaoModeloIaProps {
  cliente: ClienteAssistenteIa;
  perfil: InformacaoPerfil[];
  /** Nome exibido de cada modelo (vem do catálogo da página). */
  nomeDoModelo: (modelo: ModeloSugerido) => string;
  aoRecomendar: (modelo: ModeloSugerido) => void;
  /** Pede a recomendação sozinho, uma vez, quando o componente aparece. */
  automatico?: boolean;
}

/**
 * Pede à IA o modelo que combina com o perfil e mostra o motivo.
 * A escolha final continua com o estudante.
 */
export function RecomendacaoModeloIa({
  cliente,
  perfil,
  nomeDoModelo,
  aoRecomendar,
  automatico = false,
}: RecomendacaoModeloIaProps) {
  const [recomendacao, setRecomendacao] = useState<RecomendacaoModelo | null>(
    null,
  );
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const jaPediu = useRef(false);

  useEffect(() => {
    if (!automatico || jaPediu.current) return;
    jaPediu.current = true;
    void recomendar();
    // Só na primeira exibição; depois o estudante pede de novo pelo botão.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [automatico]);

  /**
   * Pede a recomendação à IA e informa o modelo escolhido à página.
   *
   * Mostra o carregamento, guarda a resposta e, em falha, exibe o motivo com a
   * orientação de escolher manualmente. Existe para a chamada automática e
   * para o botão "Recomendar de novo".
   */
  async function recomendar(): Promise<void> {
    setCarregando(true);
    setErro(null);
    try {
      const resultado = await cliente.recomendarModelo(perfil);
      setRecomendacao(resultado);
      aoRecomendar(resultado.modelo);
    } catch (falha) {
      setErro(
        `${falha instanceof Error ? falha.message : "IA indisponível."} Escolha o modelo abaixo.`,
      );
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="recomendacao-modelo-ia">
      <button
        className="painel-revisao-ia__botao"
        disabled={carregando}
        onClick={recomendar}
        type="button"
      >
        {carregando
          ? "A IA está analisando seu perfil..."
          : recomendacao
            ? "✦ Recomendar de novo"
            : "✦ Recomendar modelo com IA"}
      </button>
      <div aria-live="polite">
        {recomendacao && (
          <div className="painel-revisao-ia__revisao painel-revisao-ia__revisao--valido">
            <p>
              <strong>
                IA recomenda: {nomeDoModelo(recomendacao.modelo)}.
              </strong>{" "}
              {recomendacao.motivo}
            </p>
            {recomendacao.alternativa && (
              <p>Segunda opção: {nomeDoModelo(recomendacao.alternativa)}.</p>
            )}
          </div>
        )}
      </div>
      {erro && (
        <p className="painel-revisao-ia__erro" role="alert">
          {erro}
        </p>
      )}
    </div>
  );
}
