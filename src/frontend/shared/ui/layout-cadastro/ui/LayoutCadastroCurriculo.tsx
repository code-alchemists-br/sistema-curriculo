import { useEffect, useRef, type ReactNode } from "react";

import gradienteCadastro from "../../../assets/images/gradiente_cadastro.webp";
import "./LayoutCadastroCurriculo.css";

export interface LayoutCadastroCurriculoProps {
  /** Subtítulo indicando os dados que estão sendo coletados (ex.: 'Dados Pessoais') */
  subtitulo: string;
  /** Número da etapa atual (1 a totalEtapas) */
  etapaAtual?: number;
  /** Total de etapas do cadastro (padrão 9) */
  totalEtapas?: number;
  /** Porcentagem de preenchimento da etapa atual (0 a 100) */
  progressoEtapaAtual?: number;
  /** Ação opcional para retornar à página inicial / hero */
  onVoltarInicio?: () => void;
  /** Conteúdo do formulário a ser exibido no lado direito */
  children: ReactNode;
}

/**
 * Layout compartilhado para todas as telas de cadastro das informações do currículo.
 *
 * Divide a tela entre o painel visual com gradiente alaranjado (40%) e
 * o painel de formulário com barra de progresso segmentada (60%).
 */
export function LayoutCadastroCurriculo({
  subtitulo,
  etapaAtual = 1,
  totalEtapas = 9,
  progressoEtapaAtual = 0,
  onVoltarInicio,
  children,
}: LayoutCadastroCurriculoProps) {
  const conteudoRef = useRef<HTMLElement | null>(null);
  const formularioRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (conteudoRef.current) {
      conteudoRef.current.scrollTop = 0;
    }
    if (formularioRef.current) {
      formularioRef.current.focus();
    }
  }, [etapaAtual]);

  const etapas = Array.from({ length: totalEtapas }, (_, index) => index + 1);

  function lidarVoltarInicio(): void {
    if (onVoltarInicio) {
      onVoltarInicio();
      return;
    }
    if (typeof window !== "undefined") {
      const url = new URL(window.location.href);
      url.searchParams.delete("etapa");
      url.searchParams.delete("aba");
      url.searchParams.delete("intencao");
      window.history.pushState({}, "", url.toString());
      window.dispatchEvent(new PopStateEvent("popstate"));
    }
  }

  return (
    <div className="layout-cadastro">
      {/* Coluna Esquerda: 40% */}
      <aside className="layout-cadastro__visual" aria-hidden="true">
        <div className="layout-cadastro__card">
          <img
            src={gradienteCadastro}
            alt=""
            className="layout-cadastro__bg-image"
            loading="eager"
          />

          <h1 className="layout-cadastro__titulo">
            Vamos criar seu currículo juntos!
          </h1>

          <p className="layout-cadastro__subtitulo">{subtitulo}</p>
        </div>
      </aside>

      {/* Coluna Direita: 60% */}
      <main ref={conteudoRef} className="layout-cadastro__conteudo">
        <div className="layout-cadastro__container">
          {/* Barra superior com navegação de saída e indicador da etapa */}
          <div className="layout-cadastro__topo">
            <button
              type="button"
              className="layout-cadastro__btn-voltar-inicio"
              onClick={lidarVoltarInicio}
              aria-label="Voltar para a página inicial"
            >
              ← Voltar ao início
            </button>
            <span className="layout-cadastro__indicador-etapa">
              Etapa {etapaAtual} de {totalEtapas}
            </span>
          </div>

          {/* Barra de progresso segmentada */}
          <div
            className="layout-cadastro__progresso"
            role="progressbar"
            aria-label={`Etapa ${etapaAtual} de ${totalEtapas}`}
            aria-valuenow={etapaAtual}
            aria-valuemin={1}
            aria-valuemax={totalEtapas}
          >
            {etapas.map((etapa) => {
              const completa = etapa < etapaAtual;
              const ativa = etapa === etapaAtual;

              return (
                <div key={etapa} className="layout-cadastro__progresso-trilha">
                  <div
                    className={`layout-cadastro__progresso-preenchimento ${
                      completa ? "completa" : ativa ? "ativa" : ""
                    }`}
                    style={{
                      width: completa
                        ? "100%"
                        : ativa
                          ? `${Math.max(0, Math.min(100, progressoEtapaAtual))}%`
                          : "0%",
                    }}
                  />
                </div>
              );
            })}
          </div>

          {/* Área do formulário da seção */}
          <div
            key={etapaAtual}
            ref={formularioRef}
            tabIndex={-1}
            className="layout-cadastro__formulario"
          >
            {children}
          </div>
        </div>
      </main>
    </div>
  );
}
