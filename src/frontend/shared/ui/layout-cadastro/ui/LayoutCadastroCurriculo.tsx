import { useEffect, useRef, useState, type ReactNode } from "react";

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
  /** Controla a visibilidade do indicador de rascunho persistido (padrão: true) */
  exibirStatusSalvo?: boolean;
  /** Texto personalizado para a indicação de rascunho salvo (padrão: 'Rascunho salvo') */
  textoStatusSalvo?: string;
  /** Conteúdo do formulário a ser exibido no lado direito */
  children: ReactNode;
}

/**
 * Layout compartilhado para todas as telas de cadastro das informações do currículo.
 *
 * Divide a tela entre o painel visual com gradiente alaranjado (40%) e
 * o painel de formulário com barra de progresso segmentada (60%).
 */
const CHAVE_RASCUNHO = "liminal_curriculo_rascunho";

function verificarRascunhoExistente(): boolean {
  if (typeof window === "undefined") return false;
  try {
    const raw =
      localStorage.getItem(CHAVE_RASCUNHO) ||
      sessionStorage.getItem(CHAVE_RASCUNHO);
    if (!raw) return false;
    const obj = JSON.parse(raw);
    return Object.values(obj).some((v) => {
      if (Array.isArray(v)) return v.length > 0;
      if (typeof v === "object" && v !== null) {
        return Object.values(v).some(
          (val) => typeof val === "string" && val.trim().length > 0,
        );
      }
      return Boolean(v);
    });
  } catch {
    return false;
  }
}

export function LayoutCadastroCurriculo({
  subtitulo,
  etapaAtual = 1,
  totalEtapas = 9,
  progressoEtapaAtual = 0,
  onVoltarInicio,
  exibirStatusSalvo = true,
  textoStatusSalvo,
  children,
}: LayoutCadastroCurriculoProps) {
  const conteudoRef = useRef<HTMLElement | null>(null);
  const formularioRef = useRef<HTMLDivElement | null>(null);
  const timerOcultacaoRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const timerRemocaoRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const [statusAtivo, setStatusAtivo] = useState<string | null>(() => {
    if (textoStatusSalvo) return textoStatusSalvo;
    if (verificarRascunhoExistente()) {
      return "Rascunho restaurado";
    }
    return null;
  });
  const [desvanecendo, setDesvanecendo] = useState(false);

  const limparTimers = () => {
    if (timerOcultacaoRef.current) clearTimeout(timerOcultacaoRef.current);
    if (timerRemocaoRef.current) clearTimeout(timerRemocaoRef.current);
  };

  // Se iniciou com "Rascunho restaurado" (ao recarregar com dados), inicia fade-out suave
  useEffect(() => {
    if (statusAtivo === "Rascunho restaurado") {
      timerOcultacaoRef.current = setTimeout(() => {
        setDesvanecendo(true);
        timerRemocaoRef.current = setTimeout(() => {
          setStatusAtivo(null);
          setDesvanecendo(false);
        }, 600);
      }, 3500);
    }
    return () => {
      limparTimers();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Monitora digitação nos campos do formulário para exibir "Rascunho salvo" temporariamente com fade-out suave
  useEffect(() => {
    const el = formularioRef.current;
    if (!el) return;

    function aoDigitar() {
      limparTimers();
      setDesvanecendo(false);
      setStatusAtivo("Rascunho salvo");

      timerOcultacaoRef.current = setTimeout(() => {
        setDesvanecendo(true);
        timerRemocaoRef.current = setTimeout(() => {
          setStatusAtivo(null);
          setDesvanecendo(false);
        }, 600);
      }, 2500);
    }

    el.addEventListener("input", aoDigitar);
    return () => {
      el.removeEventListener("input", aoDigitar);
    };
  }, [etapaAtual]);

  useEffect(() => {
    if (conteudoRef.current) {
      conteudoRef.current.scrollTop = 0;
    }
    if (formularioRef.current) {
      const tituloH1 = formularioRef.current.querySelector<HTMLElement>("h1");
      if (tituloH1) {
        if (!tituloH1.hasAttribute("tabindex")) {
          tituloH1.setAttribute("tabindex", "-1");
        }
        tituloH1.focus({ preventScroll: true });
      } else {
        formularioRef.current.focus({ preventScroll: true });
      }
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
              <span
                className="layout-cadastro__btn-voltar-icone"
                aria-hidden="true"
              >
                ←
              </span>
              <span className="layout-cadastro__btn-voltar-texto-completo">
                Voltar ao início
              </span>
              <span className="layout-cadastro__btn-voltar-texto-curto">
                Início
              </span>
            </button>

            <div className="layout-cadastro__topo-direita">
              {exibirStatusSalvo && (statusAtivo || textoStatusSalvo) && (
                <span
                  className={`layout-cadastro__status-salvo ${
                    desvanecendo ? "layout-cadastro__status-salvo--saindo" : ""
                  }`}
                  aria-label="Status do rascunho"
                >
                  <svg
                    className="layout-cadastro__status-salvo-icone"
                    viewBox="0 0 16 16"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    aria-hidden="true"
                  >
                    <circle
                      cx="8"
                      cy="8"
                      r="6.5"
                      stroke="currentColor"
                      strokeWidth="1.2"
                    />
                    <path
                      d="M5 8.2L7 10.2L11 6.2"
                      stroke="currentColor"
                      strokeWidth="1.4"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                  <span>{textoStatusSalvo || statusAtivo}</span>
                </span>
              )}

              <span className="layout-cadastro__indicador-etapa">
                Etapa {etapaAtual} de {totalEtapas}
              </span>
            </div>
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
