import { useId, type ReactNode } from "react";
import {
  agruparRevisaoPorSecaoESeveridade,
  calcularTotaisRevisao,
  type ItemRevisao,
  type ResultadoRevisao,
  type SecaoRevisao,
} from "../model/revisao-curriculo";
import "./PainelRevisao.css";

/**
 * Propriedades para configuração do componente PainelRevisao.
 */
export interface PainelRevisaoProps {
  /** Lista de itens/pendências identificadas na revisão. */
  itens?: ItemRevisao[];
  /** Objeto consolidado de resultado da revisão (alternativa à prop itens). */
  resultado?: ResultadoRevisao;
  /** Título principal do painel (padrão: 'Painel de revisão do currículo'). */
  titulo?: string;
  /** Callback acionado quando o usuário solicita navegar ou corrigir uma seção. */
  onNavegarSecao?: (secao: SecaoRevisao) => void;
  /** Elementos visuais ou ações adicionais inseridas no rodapé do painel. */
  children?: ReactNode;
}

/**
 * Apresenta o painel de revisão do currículo agrupando resultados por seção e severidade.
 *
 * - O que faz: Exibe de forma clara e acessível as pendências do currículo, agrupadas por seção e categorizadas entre erros impeditivos e avisos recomendatórios.
 * - Como faz: Processa os itens via `agruparRevisaoPorSecaoESeveridade`, computa totais com `calcularTotaisRevisao`, e renderiza estrutura HTML5 semântica com regiões ARIA, avisos ao vivo (`aria-live`) e badges textuais acessíveis.
 * - Qual finalidade atende: Orienta o estudante sobre o que precisa ser corrigido antes da exportação, garantindo total conformidade com WCAG 2.1 AA sem depender apenas de cores.
 *
 * @param props Propriedades contendo os itens ou o resultado da revisão.
 * @returns Elemento JSX representando o painel de revisão acessível.
 */
export function PainelRevisao({
  itens: itensProp,
  resultado: resultadoProp,
  titulo = "Painel de revisão do currículo",
  onNavegarSecao,
  children,
}: PainelRevisaoProps) {
  const idPainel = useId();
  const idTitulo = `${idPainel}-titulo`;

  const listaItens: ItemRevisao[] = itensProp ?? resultadoProp?.itens ?? [];

  const { totalErros, totalAvisos, aprovado } =
    calcularTotaisRevisao(listaItens);
  const grupos = agruparRevisaoPorSecaoESeveridade(listaItens);

  return (
    <section aria-labelledby={idTitulo} className="painel-revisao">
      <header className="painel-revisao__cabecalho">
        <h2 className="painel-revisao__titulo" id={idTitulo}>
          {titulo}
        </h2>

        <div
          aria-live="polite"
          className={`painel-revisao__resumo ${
            aprovado
              ? totalAvisos > 0
                ? "painel-revisao__resumo--aviso"
                : "painel-revisao__resumo--aprovado"
              : "painel-revisao__resumo--erro"
          }`}
          role={aprovado ? "status" : "alert"}
        >
          {aprovado && totalAvisos === 0 && (
            <p className="painel-revisao__resumo-texto">
              Nenhuma pendência encontrada. Seu currículo está completo e pronto
              para exportação.
            </p>
          )}

          {aprovado && totalAvisos > 0 && (
            <p className="painel-revisao__resumo-texto">
              Currículo aprovado para exportação, com {totalAvisos}{" "}
              {totalAvisos === 1
                ? "recomendação de melhoria"
                : "recomendações de melhoria"}
              .
            </p>
          )}

          {!aprovado && (
            <p className="painel-revisao__resumo-texto">
              Há {totalErros}{" "}
              {totalErros === 1 ? "erro impeditivo" : "erros impeditivos"} que
              bloqueiam a aprovação
              {totalAvisos > 0 &&
                ` e ${totalAvisos} ${
                  totalAvisos === 1 ? "recomendação" : "recomendações"
                }`}
              .
            </p>
          )}
        </div>
      </header>

      {grupos.length === 0 ? (
        <div className="painel-revisao__vazio">
          <p>Nenhuma seção possui pendências registradas.</p>
        </div>
      ) : (
        <div className="painel-revisao__grupos">
          {grupos.map((grupo) => {
            const idSecao = `${idPainel}-secao-${grupo.secao}`;

            return (
              <article
                aria-labelledby={idSecao}
                className={`painel-revisao__cartao-secao ${
                  grupo.temErros
                    ? "painel-revisao__cartao-secao--com-erros"
                    : "painel-revisao__cartao-secao--apenas-avisos"
                }`}
                key={grupo.secao}
              >
                <header className="painel-revisao__secao-topo">
                  <div className="painel-revisao__secao-identificacao">
                    <h3 className="painel-revisao__secao-titulo" id={idSecao}>
                      {grupo.tituloSecao}
                    </h3>
                    <div className="painel-revisao__badges">
                      {grupo.erros.length > 0 && (
                        <span className="painel-revisao__badge painel-revisao__badge--erro">
                          <span className="painel-revisao__sr-only">
                            Severidade:{" "}
                          </span>
                          {grupo.erros.length}{" "}
                          {grupo.erros.length === 1 ? "erro" : "erros"}
                        </span>
                      )}
                      {grupo.avisos.length > 0 && (
                        <span className="painel-revisao__badge painel-revisao__badge--aviso">
                          <span className="painel-revisao__sr-only">
                            Severidade:{" "}
                          </span>
                          {grupo.avisos.length}{" "}
                          {grupo.avisos.length === 1 ? "aviso" : "avisos"}
                        </span>
                      )}
                    </div>
                  </div>

                  {onNavegarSecao && (
                    <button
                      className="painel-revisao__botao-navegar"
                      onClick={() => onNavegarSecao(grupo.secao)}
                      type="button"
                    >
                      Corrigir {grupo.tituloSecao.toLowerCase()}
                    </button>
                  )}
                </header>

                <div className="painel-revisao__listas">
                  {grupo.erros.length > 0 && (
                    <div className="painel-revisao__bloco-severidade painel-revisao__bloco-severidade--erro">
                      <h4 className="painel-revisao__subtitulo-severidade">
                        Erros impeditivos
                      </h4>
                      <ul
                        aria-label={`Erros impeditivos em ${grupo.tituloSecao}`}
                        className="painel-revisao__lista-itens"
                      >
                        {grupo.erros.map((item) => (
                          <li
                            className="painel-revisao__item painel-revisao__item--erro"
                            key={item.codigo}
                          >
                            <span
                              aria-hidden="true"
                              className="painel-revisao__icone-status"
                            >
                              ✕
                            </span>
                            <span className="painel-revisao__mensagem-item">
                              {item.mensagem}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {grupo.avisos.length > 0 && (
                    <div className="painel-revisao__bloco-severidade painel-revisao__bloco-severidade--aviso">
                      <h4 className="painel-revisao__subtitulo-severidade">
                        Recomendações de melhoria
                      </h4>
                      <ul
                        aria-label={`Recomendações em ${grupo.tituloSecao}`}
                        className="painel-revisao__lista-itens"
                      >
                        {grupo.avisos.map((item) => (
                          <li
                            className="painel-revisao__item painel-revisao__item--aviso"
                            key={item.codigo}
                          >
                            <span
                              aria-hidden="true"
                              className="painel-revisao__icone-status"
                            >
                              !
                            </span>
                            <span className="painel-revisao__mensagem-item">
                              {item.mensagem}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </article>
            );
          })}
        </div>
      )}

      {children && (
        <footer className="painel-revisao__rodape">{children}</footer>
      )}
    </section>
  );
}
