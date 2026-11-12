import {
  validarCurriculo,
  type CurriculoParaValidacao,
  type IdSecaoCurriculo,
} from "../model/validacao-curriculo";
import "./TelaValidacaoCurriculo.css";

/** Define os callbacks das ações finais do fluxo de currículo. */
export interface TelaValidacaoCurriculoProps {
  dados: CurriculoParaValidacao;
  onVisualizarPreview?: () => void;
  onExportarPdf?: () => void;
  onExportarDocx?: () => void;
  onConfirmarCurriculo?: () => void;
  onVoltar?: () => void;
  onCorrigirSecao?: (secaoId: IdSecaoCurriculo) => void;
}

/**
 * Apresenta a revisão final das seções obrigatórias antes da prévia ou do PDF.
 * Calcula a validação a partir do estado recebido, exibe pendências e somente
 * dispara as ações finais quando o resultado permite. A tela existe para ser
 * encaixada no Wizard sem duplicar regras de validação em cada etapa.
 */
export function TelaValidacaoCurriculo({
  dados,
  onVisualizarPreview,
  onExportarPdf,
  onExportarDocx,
  onConfirmarCurriculo,
  onVoltar,
  onCorrigirSecao,
}: TelaValidacaoCurriculoProps) {
  const resultado = validarCurriculo(dados);
  const modoLegadoConfirmacao = Boolean(
    onConfirmarCurriculo || !onVisualizarPreview,
  );

  return (
    <div className="tela-validacao-curriculo">
      <div className="tela-validacao-curriculo__cabecalho">
        <h2
          id="titulo-validacao-curriculo"
          className="tela-validacao-curriculo__titulo"
        >
          Valide os dados do currículo
        </h2>
        <p className="tela-validacao-curriculo__descricao">
          Confira as seções obrigatórias antes de visualizar ou exportar seu
          currículo.
        </p>
      </div>

      <div
        aria-live="polite"
        className="tela-validacao-curriculo__status-container"
      >
        {resultado.valido ? (
          <p
            role="status"
            className="tela-validacao-curriculo__mensagem tela-validacao-curriculo__mensagem--sucesso"
          >
            Todas as seções obrigatórias estão válidas.
          </p>
        ) : (
          <p
            role="alert"
            className="tela-validacao-curriculo__mensagem tela-validacao-curriculo__mensagem--erro"
          >
            Há pendências que precisam ser corrigidas antes de continuar.
          </p>
        )}
      </div>

      <ul
        aria-label="Status das seções obrigatórias"
        className="tela-validacao-curriculo__secoes"
      >
        {resultado.secoes.map((secao) => (
          <li
            key={secao.id}
            className={`tela-validacao-curriculo__secao tela-validacao-curriculo__secao--${secao.status}`}
          >
            <div className="tela-validacao-curriculo__secao-info">
              <span>
                <strong>{secao.titulo}</strong>:
              </span>
              <div className="tela-validacao-curriculo__secao-status-grupo">
                <span className={`status-badge status-badge--${secao.status}`}>
                  {textoStatus(secao.status)}
                </span>
                {secao.status !== "valida" && onCorrigirSecao && (
                  <button
                    type="button"
                    className="tela-validacao-curriculo__btn-corrigir"
                    onClick={() => onCorrigirSecao(secao.id)}
                    aria-label={`Corrigir ${secao.titulo}`}
                  >
                    Corrigir →
                  </button>
                )}
              </div>
            </div>
            {secao.mensagens.length > 0 && (
              <ul className="tela-validacao-curriculo__mensagens-erro">
                {secao.mensagens.map((mensagem, indice) => (
                  <li key={`${secao.id}-${indice}`}>{mensagem}</li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>

      <div className="tela-validacao-curriculo__acoes">
        {modoLegadoConfirmacao ? (
          <>
            <div className="botoes-navegacao">
              {onVoltar && (
                <button
                  aria-label="Voltar para a etapa anterior"
                  className="btn-voltar"
                  onClick={onVoltar}
                  type="button"
                >
                  Voltar
                </button>
              )}
              <button
                className="btn-proximo"
                disabled={!resultado.podeExportarPdf}
                onClick={onConfirmarCurriculo}
                type="button"
              >
                Confirmar currículo
              </button>
            </div>

            <div className="tela-validacao-curriculo__acoes-secundarias">
              <button
                className="btn-secundario"
                disabled={!resultado.podeVisualizarPreview}
                onClick={onVisualizarPreview}
                type="button"
              >
                Visualizar prévia
              </button>
              <button
                className="btn-secundario"
                disabled={!resultado.podeExportarPdf}
                onClick={onExportarPdf}
                type="button"
              >
                Exportar PDF
              </button>
            </div>
          </>
        ) : (
          <div className="tela-validacao-curriculo__acoes-wrapper">
            <div className="tela-validacao-curriculo__exportacao-botoes">
              <button
                className="btn-secundario tela-validacao-curriculo__btn-exportar"
                disabled={!resultado.podeExportarPdf}
                onClick={onExportarPdf}
                type="button"
              >
                <svg
                  aria-hidden="true"
                  className="tela-validacao-curriculo__icone-exportar"
                  fill="none"
                  height="18"
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  width="18"
                >
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" x2="12" y1="15" y2="3" />
                </svg>
                <span>Exportar PDF</span>
              </button>
              {onExportarDocx && (
                <button
                  className="btn-secundario tela-validacao-curriculo__btn-exportar"
                  disabled={!resultado.podeExportarPdf}
                  onClick={onExportarDocx}
                  type="button"
                >
                  <svg
                    aria-hidden="true"
                    className="tela-validacao-curriculo__icone-exportar"
                    fill="none"
                    height="18"
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    width="18"
                  >
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <polyline points="14 2 14 8 20 8" />
                    <line x1="16" x2="8" y1="13" />
                    <line x1="16" x2="8" y1="17" />
                    <line x1="10" x2="8" y1="9" />
                  </svg>
                  <span>Exportar Word (DOCX)</span>
                </button>
              )}
            </div>

            <div className="botoes-navegacao tela-validacao-curriculo__barra-navegacao">
              {onVoltar && (
                <button
                  aria-label="Voltar para a etapa anterior"
                  className="btn-voltar tela-validacao-curriculo__btn-voltar"
                  onClick={onVoltar}
                  type="button"
                >
                  Voltar
                </button>
              )}
              <button
                aria-label="Visualizar prévia"
                className="btn-proximo tela-validacao-curriculo__btn-proximo"
                disabled={!resultado.podeVisualizarPreview}
                onClick={onVisualizarPreview}
                type="button"
              >
                Visualizar prévia →
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

/** Traduz o status técnico da validação para uma mensagem de interface. */
function textoStatus(status: "valida" | "pendente" | "erro"): string {
  if (status === "valida") return "Válida";
  if (status === "pendente") return "Pendente";
  return "Com erro";
}
