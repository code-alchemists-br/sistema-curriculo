import { useEffect, useRef, useState } from "react";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import {
  CurriculoNoModelo,
  ROTULOS_MODELO_CURRICULO,
} from "../../../features/visualizar-curriculo";
import "./PaginaMeuPerfil.css";

/** Dados e ações recebidos pela página de perfil. */
export interface PaginaMeuPerfilProps {
  /** Currículo atual do estudante, montado com os dados das etapas. */
  previa: PreviaCurriculo;
  /** Chave do modelo visual escolhido para o currículo. */
  modelo: string;
  /** Indica se o estudante já preencheu alguma parte do currículo. */
  possuiCurriculo: boolean;
  onEditarPerfil: () => void;
  onEditarCurriculo: () => void;
  onVoltarInicio: () => void;
  /**
   * Gera e baixa o currículo no formato escolhido. O PDF é feito a partir da
   * folha mostrada na página; o Word, a partir dos dados da prévia.
   */
  aoBaixarCurriculo?: (
    formato: FormatoDownload,
    folha: HTMLElement,
  ) => Promise<void> | void;
}

/** Formatos em que o currículo pode ser baixado. */
export type FormatoDownload = "pdf" | "docx";

const OPCOES_FORMATO: ReadonlyArray<{ formato: FormatoDownload; rotulo: string; dica: string }> = [
  { formato: "pdf", rotulo: "PDF", dica: "Igual ao que você vê, pronto para enviar" },
  { formato: "docx", rotulo: "Word", dica: "Para editar no Word ou Google Docs" },
];

/** Iniciais do nome para o avatar (ex.: "Ana Teste Fluxo" → "AF"). */
function iniciais(nome: string): string {
  const partes = nome.trim().split(/\s+/).filter(Boolean);
  if (partes.length === 0) return "?";
  const primeira = partes[0][0];
  const ultima = partes.length > 1 ? partes[partes.length - 1][0] : "";
  return (primeira + ultima).toUpperCase();
}

/** Um item da lista de dados do perfil; não aparece quando está vazio. */
function Dado({ rotulo, valor }: { rotulo: string; valor?: string | null }) {
  if (!valor || !valor.trim()) return null;
  return (
    <div className="pagina-meu-perfil__dado">
      <dt>{rotulo}</dt>
      <dd>{valor}</dd>
    </div>
  );
}

/**
 * Mostra o perfil do estudante só para leitura, ao lado do currículo atual.
 *
 * - O que faz: à esquerda, os dados pessoais e um resumo do que já foi
 *   preenchido; à direita, o currículo no modelo escolhido; no topo, os botões
 *   para editar o perfil ou o currículo e para baixar o currículo em PDF
 *   ou Word, escolhendo o formato num menu.
 * - Como faz: lê tudo da mesma prévia usada na visualização do currículo, sem
 *   chamadas HTTP e sem campos editáveis; as edições são delegadas por callback.
 * - Qual finalidade atende: dá ao estudante um lugar para conferir os próprios
 *   dados e o currículo de uma vez, antes de decidir o que alterar.
 */
export function PaginaMeuPerfil({
  previa,
  modelo,
  possuiCurriculo,
  onEditarPerfil,
  onEditarCurriculo,
  onVoltarInicio,
  aoBaixarCurriculo,
}: PaginaMeuPerfilProps) {
  const folhaRef = useRef<HTMLDivElement | null>(null);
  const menuRef = useRef<HTMLDivElement | null>(null);
  const [menuAberto, setMenuAberto] = useState(false);
  const [baixando, setBaixando] = useState<FormatoDownload | null>(null);
  const [erroDownload, setErroDownload] = useState<string | null>(null);

  // Fecha o menu de formatos ao clicar fora dele ou apertar Esc.
  useEffect(() => {
    if (!menuAberto) return;
    function aoClicarFora(evento: MouseEvent): void {
      if (!menuRef.current?.contains(evento.target as Node)) setMenuAberto(false);
    }
    function aoApertarTecla(evento: KeyboardEvent): void {
      if (evento.key === "Escape") setMenuAberto(false);
    }
    document.addEventListener("mousedown", aoClicarFora);
    document.addEventListener("keydown", aoApertarTecla);
    return () => {
      document.removeEventListener("mousedown", aoClicarFora);
      document.removeEventListener("keydown", aoApertarTecla);
    };
  }, [menuAberto]);

  /** Baixa o currículo no formato escolhido, avisando se a geração falhar. */
  async function baixarCurriculo(formato: FormatoDownload): Promise<void> {
    setMenuAberto(false);
    if (!aoBaixarCurriculo || !folhaRef.current || baixando) return;
    setBaixando(formato);
    setErroDownload(null);
    try {
      await aoBaixarCurriculo(formato, folhaRef.current);
    } catch {
      setErroDownload(
        `Não foi possível gerar o arquivo ${formato === "pdf" ? "PDF" : "Word"}. Tente novamente.`,
      );
    } finally {
      setBaixando(null);
    }
  }

  const { estudante } = previa;
  const contato = estudante.contato;
  const formacaoPrincipal = previa.formacoes[0];
  const resumo = [
    { rotulo: "Experiências", total: previa.experiencias.length },
    { rotulo: "Projetos", total: previa.projetos.length },
    { rotulo: "Competências", total: previa.competencias.length },
    { rotulo: "Idiomas", total: previa.idiomas.length },
    { rotulo: "Cursos e certificações", total: previa.documentos.length },
  ];

  return (
    <main className="pagina-meu-perfil">
      <div className="pagina-meu-perfil__conteudo">
        <header className="pagina-meu-perfil__cabecalho">
          <div>
            <button
              className="pagina-meu-perfil__voltar"
              onClick={onVoltarInicio}
              type="button"
            >
              ← Voltar ao início
            </button>
            <p className="pagina-meu-perfil__sobretitulo">Perfil</p>
            <h1 id="titulo-meu-perfil">Meu perfil</h1>
          </div>
          <div className="pagina-meu-perfil__acoes">
            <button
              className="pagina-meu-perfil__btn-secundario"
              onClick={onEditarPerfil}
              type="button"
            >
              Editar perfil
            </button>
            <button
              className={
                possuiCurriculo && aoBaixarCurriculo
                  ? "pagina-meu-perfil__btn-secundario"
                  : "pagina-meu-perfil__btn-primario"
              }
              onClick={onEditarCurriculo}
              type="button"
            >
              {possuiCurriculo ? "Editar currículo" : "Criar currículo"}
            </button>
            {possuiCurriculo && aoBaixarCurriculo && (
              <div className="pagina-meu-perfil__download" ref={menuRef}>
                <button
                  aria-controls="menu-formato-curriculo"
                  aria-expanded={menuAberto}
                  aria-haspopup="menu"
                  className="pagina-meu-perfil__btn-primario"
                  disabled={baixando !== null}
                  onClick={() => setMenuAberto((aberto) => !aberto)}
                  type="button"
                >
                  {baixando
                    ? `Gerando ${baixando === "pdf" ? "PDF" : "Word"}...`
                    : "Baixar currículo ▾"}
                </button>
                {menuAberto && (
                  <div
                    aria-label="Formato do arquivo"
                    className="pagina-meu-perfil__menu-formato"
                    id="menu-formato-curriculo"
                    role="menu"
                  >
                    {OPCOES_FORMATO.map((opcao) => (
                      <button
                        className="pagina-meu-perfil__opcao-formato"
                        key={opcao.formato}
                        onClick={() => void baixarCurriculo(opcao.formato)}
                        role="menuitem"
                        type="button"
                      >
                        <strong>{opcao.rotulo}</strong>
                        <span>{opcao.dica}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </header>

        {erroDownload && (
          <p className="pagina-meu-perfil__erro" role="alert">
            {erroDownload}
          </p>
        )}

        <div className="pagina-meu-perfil__grade">
          <aside
            aria-labelledby="titulo-dados-perfil"
            className="pagina-meu-perfil__cartao"
          >
            <div className="pagina-meu-perfil__identidade">
              <span aria-hidden="true" className="pagina-meu-perfil__avatar">
                {iniciais(estudante.nome)}
              </span>
              <div>
                <h2 id="titulo-dados-perfil">{estudante.nome}</h2>
                {formacaoPrincipal && (
                  <p>
                    {formacaoPrincipal.curso} · {formacaoPrincipal.instituicao}
                  </p>
                )}
              </div>
            </div>

            <dl className="pagina-meu-perfil__dados">
              <Dado rotulo="E-mail" valor={estudante.email} />
              <Dado rotulo="Telefone" valor={contato?.telefones.join(" · ")} />
              <Dado rotulo="Endereço" valor={contato?.endereco} />
              <Dado rotulo="LinkedIn" valor={contato?.linkedin} />
              <Dado rotulo="Currículo Lattes" valor={contato?.curriculo_lattes} />
            </dl>

            <h3 className="pagina-meu-perfil__subtitulo">Seu currículo</h3>
            <p className="pagina-meu-perfil__modelo">
              Modelo:{" "}
              <strong>{ROTULOS_MODELO_CURRICULO[modelo] ?? modelo}</strong>
            </p>
            <ul className="pagina-meu-perfil__resumo">
              {resumo.map((item) => (
                <li key={item.rotulo}>
                  <strong>{item.total}</strong>
                  <span>{item.rotulo}</span>
                </li>
              ))}
            </ul>
          </aside>

          <section
            aria-label="Currículo atual"
            className="pagina-meu-perfil__moldura"
          >
            {possuiCurriculo ? (
              // Só a folha é exportada, sem a moldura escura da página.
              <div ref={folhaRef}>
                <CurriculoNoModelo modelo={modelo} previa={previa} />
              </div>
            ) : (
              <div className="pagina-meu-perfil__vazio">
                <p>Você ainda não montou seu currículo.</p>
                <button
                  className="pagina-meu-perfil__btn-primario"
                  onClick={onEditarCurriculo}
                  type="button"
                >
                  Criar currículo
                </button>
              </div>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}
