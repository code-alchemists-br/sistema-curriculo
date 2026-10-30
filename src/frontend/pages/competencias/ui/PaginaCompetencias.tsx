import { useState } from "react";

import { FormularioCompetencias, type Habilidades } from "../../../features/edit-skills";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaCompetencias.css";

/** Propriedades da página de cadastro de competências. */
export interface PaginaCompetenciasProps {
  onAvancar?: () => void;
  onVoltar?: () => void;
  competenciasIniciais?: Habilidades;
  onSalvar?: (habilidades: Habilidades) => void;
}

/**
 * Compõe a página de cadastro de competências (Etapa 6 de 9).
 *
 * Utiliza o layout compartilhado de cadastro de currículo, com o painel visual
 * retangular degradê e a barra de progresso segmentada na sexta etapa.
 */
export function PaginaCompetencias({
  onAvancar,
  onVoltar,
  competenciasIniciais,
  onSalvar,
}: PaginaCompetenciasProps = {}) {
  const [progresso, setProgresso] = useState(0);

  function handleAvancar(): void {
    if (onAvancar) {
      onAvancar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=projetos-academicos";
    }
  }

  function handleVoltar(): void {
    if (onVoltar) {
      onVoltar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=idiomas";
    }
  }

  return (
    <LayoutCadastroCurriculo
      subtitulo="Competências"
      etapaAtual={6}
      totalEtapas={9}
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

        <FormularioCompetencias
          aoAlterarProgresso={setProgresso}
          aoAvancar={handleAvancar}
          habilidadesIniciais={competenciasIniciais}
          onSalvar={onSalvar}
          onVoltar={handleVoltar}
          aoAlterarHabilidades={onSalvar}
        />
      </section>
    </LayoutCadastroCurriculo>
  );
}
