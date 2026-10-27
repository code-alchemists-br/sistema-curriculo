import {
  validarCurriculo,
  type CurriculoParaValidacao,
} from "../model/validacao-curriculo";
import "./TelaValidacaoCurriculo.css";

/** Define os callbacks das ações finais do fluxo de currículo. */
export interface TelaValidacaoCurriculoProps {
  dados: CurriculoParaValidacao;
  onVisualizarPreview?: () => void;
  onExportarPdf?: () => void;
  onConfirmarCurriculo?: () => void;
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
  onConfirmarCurriculo,
}: TelaValidacaoCurriculoProps) {
  const resultado = validarCurriculo(dados);

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
              <span className={`status-badge status-badge--${secao.status}`}>
                {textoStatus(secao.status)}
              </span>
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
        <button
          className="btn-proximo"
          disabled={!resultado.podeExportarPdf}
          onClick={onConfirmarCurriculo}
          type="button"
        >
          Confirmar currículo
        </button>

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
