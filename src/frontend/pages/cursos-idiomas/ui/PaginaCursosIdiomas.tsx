import { useState } from "react";

import { FormularioCertificacao } from "../../../features/cadastro-certificacoes";
import { FormularioCursos } from "../../../features/edit-courses";
import { FormularioIdiomas } from "../../../features/edit-languages";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaCursosIdiomas.css";

/** Propriedades da página de cadastro de cursos, certificações e idiomas. */
export interface PaginaCursosIdiomasProps {
  onAvancar?: () => void;
}

/**
 * Compõe a página de cadastro de cursos, certificações e idiomas (Etapa 4 de 8).
 *
 * Utiliza o layout compartilhado de cadastro de currículo, com o painel visual
 * retangular degradê e a barra de progresso segmentada na quarta etapa.
 */
export function PaginaCursosIdiomas({
  onAvancar,
}: PaginaCursosIdiomasProps = {}) {
  const [progressoCursos, setProgressoCursos] = useState(0);
  const [progressoCertificacao, setProgressoCertificacao] = useState(0);
  const [progressoIdiomas, setProgressoIdiomas] = useState(0);

  function handleAvancar(): void {
    if (onAvancar) {
      onAvancar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=competencias";
    }
  }

  const progresso =
    progressoCertificacao > 0
      ? Math.round(
          progressoCursos * 0.4 +
            progressoIdiomas * 0.4 +
            progressoCertificacao * 0.2,
        )
      : Math.round(progressoCursos * 0.5 + progressoIdiomas * 0.5);

  return (
    <LayoutCadastroCurriculo
      subtitulo="Cursos e Idiomas"
      etapaAtual={4}
      totalEtapas={8}
      progressoEtapaAtual={progresso}
    >
      <section
        aria-labelledby="titulo-cursos-idiomas"
        className="pagina-cursos-idiomas__conteudo"
      >
        <h1
          id="titulo-cursos-idiomas"
          className="pagina-cursos-idiomas__sr-only"
        >
          Cursos, Certificações e Idiomas
        </h1>

        <FormularioCursos aoAlterarProgresso={setProgressoCursos} />
        <hr className="pagina-cursos-idiomas__divider" />
        <FormularioCertificacao aoAlterarProgresso={setProgressoCertificacao} />
        <hr className="pagina-cursos-idiomas__divider" />
        <FormularioIdiomas aoAlterarProgresso={setProgressoIdiomas} />

        <button
          aria-label="Avançar para próxima etapa"
          className="pagina-cursos-idiomas__btn-proximo"
          onClick={handleAvancar}
          type="button"
        >
          Próximo
        </button>
      </section>
    </LayoutCadastroCurriculo>
  );
}
