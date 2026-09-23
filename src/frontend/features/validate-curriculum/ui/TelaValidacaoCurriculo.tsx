import { validarCurriculo, type CurriculoParaValidacao } from "../model/validacao-curriculo";

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
  onConfirmarCurriculo
}: TelaValidacaoCurriculoProps) {
  const resultado = validarCurriculo(dados);

  return (
    <main>
      <section aria-labelledby="titulo-validacao-curriculo">
        <p>Revisão final</p>
        <h1 id="titulo-validacao-curriculo">Valide os dados do currículo</h1>
        <p>
          Confira as seções obrigatórias antes de visualizar ou exportar seu currículo.
        </p>

        <div aria-live="polite">
          {resultado.valido ? (
            <p role="status">Todas as seções obrigatórias estão válidas.</p>
          ) : (
            <p role="alert">Há pendências que precisam ser corrigidas antes de continuar.</p>
          )}
        </div>

        <ul aria-label="Status das seções obrigatórias">
          {resultado.secoes.map((secao) => (
            <li key={secao.id}>
              <strong>{secao.titulo}</strong>: {textoStatus(secao.status)}
              {secao.mensagens.length > 0 && (
                <ul>
                  {secao.mensagens.map((mensagem, indice) => (
                    <li key={`${secao.id}-${indice}`}>{mensagem}</li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>

        <div>
          <button
            disabled={!resultado.podeVisualizarPreview}
            type="button"
            onClick={onVisualizarPreview}
          >
            Visualizar prévia
          </button>
          <button
            disabled={!resultado.podeExportarPdf}
            type="button"
            onClick={onConfirmarCurriculo}
          >
            Confirmar currículo
          </button>
          <button
            disabled={!resultado.podeExportarPdf}
            type="button"
            onClick={onExportarPdf}
          >
            Exportar PDF
          </button>
        </div>
      </section>
    </main>
  );
}

/** Traduz o status técnico da validação para uma mensagem de interface. */
function textoStatus(status: "valida" | "pendente" | "erro"): string {
  if (status === "valida") return "Válida";
  if (status === "pendente") return "Pendente";
  return "Com erro";
}
