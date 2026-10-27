import type { ReactNode } from "react";

import gradienteCadastro from "../../../assets/images/gradiente_cadastro.webp";
import "./LayoutCadastroCurriculo.css";

export interface LayoutCadastroCurriculoProps {
  /** Subtítulo indicando os dados que estão sendo coletados (ex.: 'Dados Pessoais') */
  subtitulo: string;
  /** Número da etapa atual (1 a totalEtapas) */
  etapaAtual?: number;
  /** Total de etapas do cadastro (padrão 8) */
  totalEtapas?: number;
  /** Porcentagem de preenchimento da etapa atual (0 a 100) */
  progressoEtapaAtual?: number;
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
  totalEtapas = 8,
  progressoEtapaAtual = 0,
  children,
}: LayoutCadastroCurriculoProps) {
  const etapas = Array.from({ length: totalEtapas }, (_, index) => index + 1);

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
      <main className="layout-cadastro__conteudo">
        <div className="layout-cadastro__container">
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
          <div className="layout-cadastro__formulario">{children}</div>
        </div>
      </main>
    </div>
  );
}
