import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type ComponentType,
} from "react";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import type { ModeloApresentacaoCurriculo } from "../../../features/alternar-modelo-curriculo";
import {
  ModeloAcademico,
  ModeloAtsSimples,
  ModeloClassico,
  ModeloCompacto,
  ModeloCriativo,
  ModeloModerno,
  ModeloPrimeiroEmprego,
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
  /** Permite alternar o modelo diretamente na tela de visualização. */
  aoTrocarModelo?: (novoModelo: ModeloApresentacaoCurriculo) => void;
  /** Ação opcional para retornar à etapa de validação. */
  onVoltar?: () => void;
  /** Ação opcional para retornar à página inicial / hero. */
  onVoltarInicio?: () => void;
  /** Ação opcional disparada após acionar o download do PDF. */
  onExportarPdf?: () => void;
  /** Dispara o download automático do PDF assim que a tela for montada. */
  autoBaixar?: boolean;
}

interface OpcaoModeloCatalogo {
  id: ModeloApresentacaoCurriculo;
  nome: string;
  tag: string;
  descricao: string;
}

const opcoesCatalogo: OpcaoModeloCatalogo[] = [
  {
    id: "classico",
    nome: "Profissional clássico",
    tag: "Corporativo & Tradicional",
    descricao:
      "Layout cronológico tradicional com divisores elegantes em azul marinho.",
  },
  {
    id: "moderno",
    nome: "Moderno",
    tag: "Tecnologia & Inovação",
    descricao: "Cabeçalho com tipografia marcante e divisão em duas colunas.",
  },
  {
    id: "criativo",
    nome: "Criativo",
    tag: "Design & Comunicação",
    descricao:
      "Barra lateral verde esmeralda com destaque a projetos e competências.",
  },
  {
    id: "compacto",
    nome: "Compacto",
    tag: "Síntese em 1 Página",
    descricao:
      "Alta densidade visual para resumir trajetória em uma única folha.",
  },
  {
    id: "ats-simples",
    nome: "ATS simples",
    tag: "Triagem Automatizada",
    descricao:
      "100% linear e sem colunas, otimizado para sistemas de triagem ATS.",
  },
  {
    id: "academico",
    nome: "Acadêmico",
    tag: "Pesquisa & Pós-Graduação",
    descricao:
      "Tipografia serifada nobre com prioridade para formação e Lattes.",
  },
  {
    id: "primeiro-emprego",
    nome: "Primeiro emprego",
    tag: "Estágio & Trainee",
    descricao:
      "Destaca formação, projetos acadêmicos e competências para iniciantes.",
  },
];

const rotulosModelo: Readonly<Record<ModeloApresentacaoCurriculo, string>> = {
  classico: "Profissional clássico",
  compacto: "Compacto",
  "ats-simples": "ATS simples",
  criativo: "Criativo",
  moderno: "Moderno",
  academico: "Acadêmico",
  "primeiro-emprego": "Primeiro emprego",
};

const modelos: Readonly<
  Record<
    ModeloApresentacaoCurriculo,
    ComponentType<{ previa: PreviaCurriculo }>
  >
> = {
  classico: ModeloClassico,
  compacto: ModeloCompacto,
  "ats-simples": ModeloAtsSimples,
  criativo: ModeloCriativo,
  moderno: ModeloModerno,
  academico: ModeloAcademico,
  "primeiro-emprego": ModeloPrimeiroEmprego,
};

/**
 * Compõe a tela de visualização e exportação do currículo.
 *
 * Apresenta a folha em formato A4 centralizada com estética de estúdio profissional,
 * navegação segregada e ações de download rápido em Word (.docx) e PDF vetorial.
 */
export function PaginaVisualizacaoCurriculo({
  previa,
  modelo,
  aoAlterarModelo,
  aoTrocarModelo,
  onVoltar,
  onVoltarInicio,
  onExportarPdf,
  autoBaixar = false,
}: PaginaVisualizacaoCurriculoProps) {
  const ModeloSelecionado = modelos[modelo] || ModeloClassico;
  const folhaRef = useRef<HTMLDivElement | null>(null);
  const [baixando, setBaixando] = useState(false);
  const [sucessoDownload, setSucessoDownload] = useState(false);
  const [erroDownload, setErroDownload] = useState<string | null>(null);
  const [modalModelosAberto, setModalModelosAberto] = useState(false);

  useEffect(() => {
    function aoPressionarTecla(e: KeyboardEvent) {
      if (e.key === "Escape" && modalModelosAberto) {
        setModalModelosAberto(false);
      }
    }
    if (modalModelosAberto) {
      window.addEventListener("keydown", aoPressionarTecla);
      return () => window.removeEventListener("keydown", aoPressionarTecla);
    }
  }, [modalModelosAberto]);

  const handleBaixarPdf = useCallback(async (): Promise<void> => {
    if (baixando) return;
    const el = folhaRef.current;
    if (!el && !previa) return;

    try {
      setBaixando(true);
      setErroDownload(null);
      const nomeEstudante = previa.estudante?.nome?.trim() || "Estudante";
      const nomeArquivo = `Curriculo - ${nomeEstudante}`;
      const previaSincronizada: PreviaCurriculo = {
        ...previa,
        layout: modelo,
      };
      await exportarElementoParaPdf({
        elemento: el,
        previa: previaSincronizada,
        nomeArquivo,
      });
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
  }, [baixando, modelo, onExportarPdf, previa]);

  const handleBaixarDocx = useCallback(async (): Promise<void> => {
    try {
      setErroDownload(null);
      const nomeEstudante = previa.estudante?.nome?.trim() || "Estudante";
      const nomeArquivo = `Curriculo - ${nomeEstudante}`;
      const previaSincronizada: PreviaCurriculo = {
        ...previa,
        layout: modelo,
      };
      await exportarPreviaParaDocx({
        previa: previaSincronizada,
        nomeArquivo,
      });
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
  }, [modelo, previa]);

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
      <div className="pagina-visualizacao-curriculo__container">
        {/* Barra Superior: Navegação e Retorno */}
        <nav
          className="pagina-visualizacao-curriculo__topo"
          aria-label="Navegação da visualização"
        >
          {onVoltar !== undefined ? (
            <button
              className="pagina-visualizacao-curriculo__btn-voltar"
              onClick={onVoltar}
              type="button"
            >
              ← Voltar para validação
            </button>
          ) : (
            <span />
          )}

          {onVoltarInicio !== undefined && (
            <button
              className="pagina-visualizacao-curriculo__btn-inicio"
              onClick={onVoltarInicio}
              type="button"
            >
              Início
            </button>
          )}
        </nav>

        {/* Toolbar de Controle e Ações Principais */}
        <header className="pagina-visualizacao-curriculo__cabecalho">
          <div className="pagina-visualizacao-curriculo__titulos">
            <span className="pagina-visualizacao-curriculo__sobretitulo">
              Currículo
            </span>
            <h1
              id="titulo-visualizacao-curriculo"
              className="pagina-visualizacao-curriculo__titulo"
            >
              Visualização do currículo
            </h1>
            <p className="pagina-visualizacao-curriculo__meta">
              Modelo selecionado:{" "}
              <strong className="pagina-visualizacao-curriculo__meta-valor">
                {rotulosModelo[modelo]}
              </strong>
              {(aoAlterarModelo !== undefined ||
                aoTrocarModelo !== undefined) && (
                <button
                  className="pagina-visualizacao-curriculo__btn-alterar-modelo"
                  onClick={() => {
                    if (aoTrocarModelo) {
                      setModalModelosAberto(true);
                    } else if (aoAlterarModelo) {
                      aoAlterarModelo();
                    }
                  }}
                  type="button"
                  aria-haspopup="dialog"
                  aria-expanded={modalModelosAberto}
                >
                  <svg
                    className="pagina-visualizacao-curriculo__icone-alterar-modelo"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    aria-hidden="true"
                  >
                    <rect x="3" y="3" width="7" height="7" rx="1" />
                    <rect x="14" y="3" width="7" height="7" rx="1" />
                    <rect x="14" y="14" width="7" height="7" rx="1" />
                    <rect x="3" y="14" width="7" height="7" rx="1" />
                  </svg>
                  <span>Alterar modelo</span>
                </button>
              )}
            </p>
          </div>

          <div className="pagina-visualizacao-curriculo__acoes">
            <button
              className="pagina-visualizacao-curriculo__btn-exportar-word"
              onClick={handleBaixarDocx}
              type="button"
            >
              <svg
                className="pagina-visualizacao-curriculo__icone-btn"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
                <line x1="16" y1="13" x2="8" y2="13" />
                <line x1="16" y1="17" x2="8" y2="17" />
                <line x1="10" y1="9" x2="8" y2="9" />
              </svg>
              <span>Baixar Word (DOCX)</span>
            </button>

            <button
              className="pagina-visualizacao-curriculo__btn-exportar-pdf"
              onClick={() => void handleBaixarPdf()}
              disabled={baixando}
              type="button"
            >
              {baixando ? (
                <>
                  <svg
                    className="pagina-visualizacao-curriculo__icone-spinner"
                    viewBox="0 0 24 24"
                    fill="none"
                    aria-hidden="true"
                  >
                    <circle
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="3"
                      strokeDasharray="30 60"
                    />
                  </svg>
                  <span>Baixando PDF...</span>
                </>
              ) : (
                <>
                  <svg
                    className="pagina-visualizacao-curriculo__icone-btn"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    aria-hidden="true"
                  >
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="7 10 12 15 17 10" />
                    <line x1="12" y1="15" x2="12" y2="3" />
                  </svg>
                  <span>Baixar PDF</span>
                </>
              )}
            </button>
          </div>
        </header>

        {/* Mensagens de Feedback Acessíveis */}
        {sucessoDownload && (
          <div
            role="status"
            className="pagina-visualizacao-curriculo__feedback-sucesso"
          >
            <svg
              className="pagina-visualizacao-curriculo__feedback-icone"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            <span>Currículo baixado com sucesso em seu dispositivo!</span>
          </div>
        )}

        {erroDownload && (
          <div
            role="alert"
            className="pagina-visualizacao-curriculo__feedback-erro"
          >
            <svg
              className="pagina-visualizacao-curriculo__feedback-icone"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                clipRule="evenodd"
              />
            </svg>
            <span>{erroDownload}</span>
          </div>
        )}

        {/* Estúdio de Visualização da Folha (Studio Canvas) */}
        <div className="pagina-visualizacao-curriculo__palco-studio">
          <div className="pagina-visualizacao-curriculo__palco-barra">
            <span className="pagina-visualizacao-curriculo__palco-tag">
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                aria-hidden="true"
              >
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
              </svg>
              <span>Formato A4 • Prévia Real de Impressão e Exportação</span>
            </span>
            <span className="pagina-visualizacao-curriculo__palco-info">
              100% de escala
            </span>
          </div>

          <section
            aria-label="Prévia do currículo no modelo selecionado"
            className="pagina-visualizacao-curriculo__moldura-previa"
          >
            <div
              className="pagina-visualizacao-curriculo__folha-a4"
              ref={folhaRef}
            >
              <ModeloSelecionado previa={previa} />
            </div>
          </section>
        </div>

        {/* Modal de seleção rápida de modelos */}
        {modalModelosAberto && (
          <div
            className="pagina-visualizacao-curriculo__modal-overlay"
            onClick={(e) => {
              if (e.target === e.currentTarget) {
                setModalModelosAberto(false);
              }
            }}
            role="presentation"
          >
            <div
              className="pagina-visualizacao-curriculo__modal-container"
              role="dialog"
              aria-modal="true"
              aria-labelledby="titulo-modal-modelos"
            >
              <div className="pagina-visualizacao-curriculo__modal-topo">
                <div>
                  <h2
                    id="titulo-modal-modelos"
                    className="pagina-visualizacao-curriculo__modal-titulo"
                  >
                    Alterar modelo do currículo
                  </h2>
                  <p className="pagina-visualizacao-curriculo__modal-subtitulo">
                    Selecione o modelo desejado para atualizar a visualização e
                    os arquivos baixados.
                  </p>
                </div>
                <button
                  className="pagina-visualizacao-curriculo__modal-btn-fechar"
                  onClick={() => setModalModelosAberto(false)}
                  type="button"
                  aria-label="Fechar modal de seleção de modelo"
                >
                  ✕
                </button>
              </div>

              <div className="pagina-visualizacao-curriculo__modal-grid">
                {opcoesCatalogo.map((opcao) => {
                  const estaAtivo = opcao.id === modelo;
                  return (
                    <button
                      key={opcao.id}
                      type="button"
                      className={`pagina-visualizacao-curriculo__modal-card ${
                        estaAtivo
                          ? "pagina-visualizacao-curriculo__modal-card--ativo"
                          : ""
                      }`}
                      onClick={() => {
                        aoTrocarModelo?.(opcao.id);
                        setModalModelosAberto(false);
                      }}
                    >
                      <div className="pagina-visualizacao-curriculo__modal-card-topo">
                        <span className="pagina-visualizacao-curriculo__modal-card-nome">
                          {opcao.nome}
                        </span>
                        {estaAtivo && (
                          <span className="pagina-visualizacao-curriculo__modal-card-badge">
                            Ativo
                          </span>
                        )}
                      </div>
                      <span className="pagina-visualizacao-curriculo__modal-card-tag">
                        {opcao.tag}
                      </span>
                      <p className="pagina-visualizacao-curriculo__modal-card-descricao">
                        {opcao.descricao}
                      </p>
                    </button>
                  );
                })}
              </div>

              {aoAlterarModelo && (
                <div className="pagina-visualizacao-curriculo__modal-rodape">
                  <button
                    type="button"
                    className="pagina-visualizacao-curriculo__modal-link-guia"
                    onClick={() => {
                      setModalModelosAberto(false);
                      aoAlterarModelo();
                    }}
                  >
                    Abrir guia com recomendação por objetivo profissional →
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
