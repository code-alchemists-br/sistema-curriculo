import { useCallback, useEffect, useRef, useState } from "react";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import type { ModeloApresentacaoCurriculo } from "../../../features/alternar-modelo-curriculo";
import {
  CurriculoNoModelo,
  ROTULOS_MODELO_CURRICULO,
} from "../../../features/visualizar-curriculo";
import { exportarElementoParaPdf } from "../model/exportar-pdf-cliente";
import { exportarPreviaParaDocx } from "../model/exportar-docx-cliente";
import "./PaginaVisualizacaoCurriculo.css";

/** Define os dados de composição para a tela de visualização do currículo. */
export interface PaginaVisualizacaoCurriculoProps {
  /** Dados estruturados retornados para a prévia da versão de currículo. */
  previa: PreviaCurriculo;
  /** Modelo que será aplicado aos dados recebidos. */
  modelo: ModeloApresentacaoCurriculo;
  /** Ação opcional que devolve o estudante à seleção de modelos. */
  aoAlterarModelo?: () => void;
  /** Ação opcional para retornar à etapa de validação. */
  onVoltar?: () => void;
  /** Ação opcional para retornar à página inicial / hero. */
  onVoltarInicio?: () => void;
  /** Ação opcional disparada após acionar o download do PDF. */
  onExportarPdf?: () => void;
  /** Dispara o download automático do PDF assim que a tela for montada. */
  autoBaixar?: boolean;
}

/**
 * Compõe a tela de visualização do currículo no modelo escolhido.
 *
 * - O que faz: Exibe a prévia recebida em um dos modelos reconhecidos pelo catálogo.
 * - Como faz: Seleciona somente o componente visual e repassa a mesma referência de `previa`, sem transformar dados.
 * - Qual finalidade atende: Permite comparar apresentações diferentes preservando integralmente as informações escolhidas pelo estudante.
 */
export function PaginaVisualizacaoCurriculo({
  previa,
  modelo,
  aoAlterarModelo,
  onVoltar,
  onVoltarInicio,
  onExportarPdf,
  autoBaixar = false,
}: PaginaVisualizacaoCurriculoProps) {
  const folhaRef = useRef<HTMLDivElement | null>(null);
  const [baixando, setBaixando] = useState(false);
  const [sucessoDownload, setSucessoDownload] = useState(false);
  const [erroDownload, setErroDownload] = useState<string | null>(null);

  const handleBaixarPdf = useCallback(async (): Promise<void> => {
    if (baixando) return;
    const el = folhaRef.current;
    if (!el) return;

    try {
      setBaixando(true);
      setErroDownload(null);
      const nomeEstudante = previa.estudante?.nome?.trim() || "Estudante";
      const nomeArquivo = `Curriculo - ${nomeEstudante}`;
      await exportarElementoParaPdf({ elemento: el, nomeArquivo });
      onExportarPdf?.();
      setSucessoDownload(true);
      setTimeout(() => {
        setSucessoDownload(false);
      }, 4000);
    } catch (erro) {
      console.error("Falha ao exportar PDF:", erro);
      setErroDownload(
        "Não foi possível gerar o arquivo PDF. Tente novamente em instantes.",
      );
      setTimeout(() => {
        setErroDownload(null);
      }, 6000);
    } finally {
      setBaixando(false);
    }
  }, [baixando, onExportarPdf, previa.estudante]);

  const handleBaixarDocx = useCallback((): void => {
    try {
      setErroDownload(null);
      const nomeEstudante = previa.estudante?.nome?.trim() || "Estudante";
      const nomeArquivo = `Curriculo - ${nomeEstudante}`;
      exportarPreviaParaDocx({ previa, nomeArquivo });
      setSucessoDownload(true);
      setTimeout(() => {
        setSucessoDownload(false);
      }, 4000);
    } catch (erro) {
      console.error("Falha ao exportar Word (DOCX):", erro);
      setErroDownload(
        "Não foi possível gerar o arquivo Word. Tente novamente em instantes.",
      );
      setTimeout(() => {
        setErroDownload(null);
      }, 6000);
    }
  }, [previa]);

  useEffect(() => {
    if (autoBaixar) {
      const timer = setTimeout(() => {
        void handleBaixarPdf();
      }, 350);
      return () => clearTimeout(timer);
    }
  }, [autoBaixar, handleBaixarPdf]);

  return (
    <main className="pagina-visualizacao-curriculo">
      <section
        aria-labelledby="titulo-visualizacao-curriculo"
        className="pagina-visualizacao-curriculo__conteudo"
      >
        <header className="pagina-visualizacao-curriculo__cabecalho">
          <div>
            <p className="pagina-visualizacao-curriculo__sobretitulo">
              Currículo
            </p>
            <h1 id="titulo-visualizacao-curriculo">
              Visualização do currículo
            </h1>
            <p>
              Modelo selecionado:{" "}
              <strong>{ROTULOS_MODELO_CURRICULO[modelo]}</strong>
            </p>
          </div>
          <div className="pagina-visualizacao-curriculo__acoes">
            {onVoltarInicio !== undefined && (
              <button
                className="pagina-visualizacao-curriculo__btn-secundario"
                onClick={onVoltarInicio}
                type="button"
              >
                Início
              </button>
            )}
            {onVoltar !== undefined && (
              <button
                className="pagina-visualizacao-curriculo__btn-secundario"
                onClick={onVoltar}
                type="button"
              >
                ← Voltar para validação
              </button>
            )}
            {aoAlterarModelo !== undefined && (
              <button
                className="pagina-visualizacao-curriculo__btn-secundario"
                onClick={aoAlterarModelo}
                type="button"
              >
                Alterar modelo
              </button>
            )}
            <button
              className="pagina-visualizacao-curriculo__btn-secundario"
              onClick={handleBaixarDocx}
              type="button"
            >
              Baixar Word (DOCX)
            </button>
            <button
              className="pagina-visualizacao-curriculo__btn-primario"
              onClick={() => void handleBaixarPdf()}
              disabled={baixando}
              type="button"
            >
              {baixando ? "Baixando PDF..." : "Baixar PDF"}
            </button>
          </div>
        </header>

        <section
          aria-label="Prévia do currículo no modelo selecionado"
          className="pagina-visualizacao-curriculo__moldura-previa"
        >
          {sucessoDownload && (
            <div
              role="status"
              className="pagina-visualizacao-curriculo__feedback-sucesso"
            >
              Currículo baixado com sucesso em seu dispositivo!
            </div>
          )}

          {erroDownload && (
            <div
              role="alert"
              className="pagina-visualizacao-curriculo__feedback-erro"
            >
              {erroDownload}
            </div>
          )}

          {/* Só a folha do currículo é exportada, sem a moldura escura da tela. */}
          <div ref={folhaRef}>
            <CurriculoNoModelo modelo={modelo} previa={previa} />
          </div>
        </section>
      </section>
    </main>
  );
}
