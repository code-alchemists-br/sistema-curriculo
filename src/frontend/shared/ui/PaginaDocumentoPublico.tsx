import type { ReactNode } from "react";

import "./PaginaDocumentoPublico.css";

/** Define os elementos de apresentação de uma página pública de documento. */
export interface PaginaDocumentoPublicoProps {
  cabecalho: ReactNode;
  sobrancelha: string;
  titulo: string;
  descricao: string;
  aviso: ReactNode;
  children: ReactNode;
  rodape: ReactNode;
}

/**
 * Estrutura uma página pública de conteúdo informativo extenso.
 *
 * Como faz: recebe o cabeçalho, o conteúdo semântico e o rodapé como
 * composição, mantendo uma única hierarquia de marcos, títulos e estilos.
 *
 * Qual finalidade atende: evita que documentos públicos repitam uma estrutura
 * visual e acessível, sem fazer a camada shared conhecer seus textos legais.
 */
export function PaginaDocumentoPublico({
  cabecalho,
  sobrancelha,
  titulo,
  descricao,
  aviso,
  children,
  rodape,
}: PaginaDocumentoPublicoProps) {
  return (
    <div className="pagina-documento-publico">
      {cabecalho}
      <main className="pagina-documento-publico__conteudo">
        <div className="pagina-documento-publico__introducao">
          <p className="pagina-documento-publico__sobrancelha">{sobrancelha}</p>
          <h1 id="titulo-documento-publico">{titulo}</h1>
          <p className="pagina-documento-publico__descricao">{descricao}</p>
        </div>

        <aside className="pagina-documento-publico__aviso" role="note">
          {aviso}
        </aside>

        <article
          aria-labelledby="titulo-documento-publico"
          className="pagina-documento-publico__artigo"
        >
          {children}
        </article>
      </main>

      <footer className="pagina-documento-publico__rodape">{rodape}</footer>
    </div>
  );
}
