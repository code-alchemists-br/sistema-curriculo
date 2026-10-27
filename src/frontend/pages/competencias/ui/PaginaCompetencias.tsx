import { useState } from "react";

import { FormularioCompetencias } from "../../../features/edit-skills";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaCompetencias.css";

/**
 * Compõe a página de cadastro de competências (Etapa 5 de 8).
 *
 * Utiliza o layout compartilhado de cadastro de currículo, com o painel visual
 * retangular degradê e a barra de progresso segmentada na quinta etapa.
 */
export function PaginaCompetencias() {
  const [progresso, setProgresso] = useState(0);

  return (
    <LayoutCadastroCurriculo
      subtitulo="Competências"
      etapaAtual={5}
      totalEtapas={8}
      progressoEtapaAtual={progresso}
    >
      <section
        aria-labelledby="titulo-pagina-competencias"
        className="pagina-competencias__conteudo"
      >
        <h1
          id="titulo-pagina-competencias"
          className="pagina-competencias__sr-only"
        >
          Competências
        </h1>

        <FormularioCompetencias aoAlterarProgresso={setProgresso} />
      </section>
    </LayoutCadastroCurriculo>
  );
}
