import { useEffect, useRef, useState, type ReactNode } from "react";

import {
  FalhaVersaoCurriculo,
  type ClienteVersoesCurriculo,
} from "../api/cliente-versoes-curriculo";
import {
  obterRotuloModeloVersao,
  OPCOES_MODELO_VERSAO,
  type ModeloVersaoCurriculo,
  type ResumoVersaoCurriculo,
} from "../model/versao-curriculo-perfil";
import "./PainelCurriculosPerfil.css";

/** Define as dependências e ações disponíveis no painel de modelo do currículo. */
export interface PainelCurriculosPerfilProps {
  cliente: ClienteVersoesCurriculo;
  onCriarCurriculo?: () => void;
  onCriarNovaVersao?: () => void;
  aoBaixarCurriculo?: (formato: "pdf" | "docx") => Promise<void> | void;
  renderizarMiniatura: (modelo: ModeloVersaoCurriculo) => ReactNode;
}

/** Representa os estados de carregamento que o painel pode comunicar. */
type EstadoPainel = "carregando" | "erro" | "sucesso";

/**
 * Exibe o currículo cadastrado e salva automaticamente a alteração do modelo na seleção,
 * disponibilizando a exportação imediata em PDF ou Word.
 */
export function PainelCurriculosPerfil({
  cliente,
  onCriarCurriculo,
  onCriarNovaVersao,
  aoBaixarCurriculo,
  renderizarMiniatura,
}: PainelCurriculosPerfilProps) {
  const [estado, setEstado] = useState<EstadoPainel>("carregando");
  const [versoes, setVersoes] = useState<ResumoVersaoCurriculo[]>([]);
  const [modeloSelecionado, setModeloSelecionado] =
    useState<ModeloVersaoCurriculo | null>(null);
  const [salvando, setSalvando] = useState(false);
  const [baixando, setBaixando] = useState<"pdf" | "docx" | null>(null);
  const [erroSalvamento, setErroSalvamento] = useState<string | null>(null);
  const [menuDownloadAberto, setMenuDownloadAberto] = useState(false);
  const menuDownloadRef = useRef<HTMLDivElement | null>(null);

  const acaoCriarCurriculo = onCriarCurriculo ?? onCriarNovaVersao;

  useEffect(() => {
    let componenteAtivo = true;

    void cliente
      .listar()
      .then((versoesCarregadas) => {
        if (!componenteAtivo) return;
        setVersoes(versoesCarregadas);
        if (versoesCarregadas.length > 0) {
          setModeloSelecionado(versoesCarregadas[0].modelo);
        }
        setEstado("sucesso");
      })
      .catch(() => {
        if (!componenteAtivo) return;
        setEstado("erro");
      });

    return () => {
      componenteAtivo = false;
    };
  }, [cliente]);

  // Fecha o menu de download ao clicar fora ou apertar Esc
  useEffect(() => {
    if (!menuDownloadAberto) return;

    function aoClicarFora(evento: MouseEvent): void {
      if (!menuDownloadRef.current?.contains(evento.target as Node)) {
        setMenuDownloadAberto(false);
      }
    }

    function aoApertarTecla(evento: KeyboardEvent): void {
      if (evento.key === "Escape") {
        setMenuDownloadAberto(false);
      }
    }

    document.addEventListener("mousedown", aoClicarFora);
    document.addEventListener("keydown", aoApertarTecla);
    return () => {
      document.removeEventListener("mousedown", aoClicarFora);
      document.removeEventListener("keydown", aoApertarTecla);
    };
  }, [menuDownloadAberto]);

  const curriculo = versoes[0];

  async function aoMudarModelo(
    novoModelo: ModeloVersaoCurriculo,
  ): Promise<void> {
    if (!curriculo || novoModelo === curriculo.modelo || salvando) return;

    const modeloAnterior = curriculo.modelo;
    setModeloSelecionado(novoModelo);
    setSalvando(true);
    setErroSalvamento(null);

    try {
      const versaoAtualizada = await cliente.atualizar(curriculo.id, {
        tituloVersao: curriculo.tituloVersao,
        modelo: novoModelo,
        visibilidade: curriculo.visibilidade,
      });
      setVersoes([versaoAtualizada]);
      setModeloSelecionado(versaoAtualizada.modelo);
    } catch (erro: unknown) {
      setModeloSelecionado(modeloAnterior);
      setErroSalvamento(obterMensagemFalha(erro));
    } finally {
      setSalvando(false);
    }
  }

  async function executarDownload(formato: "pdf" | "docx"): Promise<void> {
    setMenuDownloadAberto(false);
    if (!aoBaixarCurriculo || baixando !== null) return;

    setBaixando(formato);
    setErroSalvamento(null);
    try {
      await aoBaixarCurriculo(formato);
    } catch {
      setErroSalvamento(
        `Não foi possível gerar o arquivo ${formato === "pdf" ? "PDF" : "Word"}. Tente novamente.`,
      );
    } finally {
      setBaixando(null);
    }
  }

  return (
    <section
      aria-labelledby="titulo-modelo-curriculo"
      className="painel-curriculos-perfil"
    >
      <header className="painel-curriculos-perfil__cabecalho">
        <div>
          <h2 id="titulo-modelo-curriculo">Modelo do currículo</h2>
          <p>
            Altere o modelo visual de apresentação do seu currículo salvo quando
            desejar e exporte os arquivos diretamente.
          </p>
        </div>
      </header>

      {erroSalvamento !== null && (
        <p className="painel-curriculos-perfil__mensagem" role="alert">
          {erroSalvamento}
        </p>
      )}

      {estado === "carregando" && (
        <p className="painel-curriculos-perfil__estado" role="status">
          Carregando informações do currículo...
        </p>
      )}

      {estado === "erro" && (
        <p className="painel-curriculos-perfil__estado" role="alert">
          Não foi possível carregar o currículo agora. Tente novamente mais
          tarde.
        </p>
      )}

      {estado === "sucesso" && versoes.length === 0 && (
        <div className="painel-curriculos-perfil__vazio">
          <h3>Nenhum currículo cadastrado</h3>
          <p>
            Você ainda não criou um currículo. Monte suas informações
            profissionais para poder escolher e alterar o modelo de
            apresentação.
          </p>
          {acaoCriarCurriculo && (
            <button
              className="painel-curriculos-perfil__btn-criar"
              onClick={acaoCriarCurriculo}
              type="button"
            >
              Criar meu currículo
            </button>
          )}
        </div>
      )}

      {estado === "sucesso" && curriculo && modeloSelecionado && (
        <article className="painel-curriculos-perfil__cartao">
          <div className="painel-curriculos-perfil__cabecalho-cartao">
            <h3 className="painel-curriculos-perfil__titulo-curriculo">
              {curriculo.tituloVersao}
            </h3>
            <p className="painel-curriculos-perfil__modelo-ativo">
              Modelo ativo:{" "}
              <strong>{obterRotuloModeloVersao(curriculo.modelo)}</strong>
              {salvando && (
                <span className="painel-curriculos-perfil__indicador-salvando">
                  Salvando...
                </span>
              )}
            </p>
          </div>

          <div
            aria-label={`Prévia visual do modelo ${obterRotuloModeloVersao(modeloSelecionado)}`}
            className="painel-curriculos-perfil__frame-modelo"
            key={modeloSelecionado}
            role="img"
          >
            {renderizarMiniatura(modeloSelecionado)}
          </div>

          <div className="painel-curriculos-perfil__controles">
            <div className="painel-curriculos-perfil__campo">
              <label htmlFor={`seletor-modelo-${curriculo.id}`}>
                Selecione o modelo de apresentação:
              </label>
              <select
                disabled={salvando || baixando !== null}
                id={`seletor-modelo-${curriculo.id}`}
                onChange={(evento) =>
                  void aoMudarModelo(
                    evento.target.value as ModeloVersaoCurriculo,
                  )
                }
                value={modeloSelecionado}
              >
                {OPCOES_MODELO_VERSAO.map((opcao) => (
                  <option key={opcao.valor} value={opcao.valor}>
                    {opcao.rotulo}
                  </option>
                ))}
              </select>
            </div>

            {aoBaixarCurriculo && (
              <div className="painel-curriculos-perfil__acoes">
                <div
                  className="painel-curriculos-perfil__download-container"
                  ref={menuDownloadRef}
                >
                  <button
                    aria-controls="menu-download-modelo"
                    aria-expanded={menuDownloadAberto}
                    aria-haspopup="menu"
                    className="painel-curriculos-perfil__btn-download"
                    disabled={salvando || baixando !== null}
                    onClick={() => setMenuDownloadAberto((aberto) => !aberto)}
                    type="button"
                  >
                    {baixando !== null
                      ? `Gerando ${baixando === "pdf" ? "PDF" : "Word"}...`
                      : "Baixar currículo ▾"}
                  </button>

                  {menuDownloadAberto && (
                    <div
                      className="painel-curriculos-perfil__menu-download"
                      id="menu-download-modelo"
                      role="menu"
                    >
                      <button
                        className="painel-curriculos-perfil__opcao-download"
                        onClick={() => executarDownload("pdf")}
                        role="menuitem"
                        type="button"
                      >
                        <strong>PDF</strong>
                        <span>Pronto para enviar ou imprimir</span>
                      </button>
                      <button
                        className="painel-curriculos-perfil__opcao-download"
                        onClick={() => executarDownload("docx")}
                        role="menuitem"
                        type="button"
                      >
                        <strong>Word (.docx)</strong>
                        <span>Editável no Word ou Docs</span>
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </article>
      )}
    </section>
  );
}

function obterMensagemFalha(erro: unknown): string {
  if (
    erro instanceof FalhaVersaoCurriculo &&
    erro.codigo === "nao-encontrado"
  ) {
    return "O currículo não foi localizado. Atualize a página e tente novamente.";
  }

  return "Não foi possível salvar o novo modelo no momento. Tente novamente mais tarde.";
}
