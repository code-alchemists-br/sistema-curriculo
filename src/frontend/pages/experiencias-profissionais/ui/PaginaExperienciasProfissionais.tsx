import { useState } from "react";

import {
  FormularioExperiencias,
  type Experiencia,
} from "../../../features/edit-professional-experience";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaExperienciasProfissionais.css";

/** Define as propriedades da página de experiências profissionais. */
export interface PaginaExperienciasProfissionaisProps {
  experienciasIniciais?: Experiencia[];
  onSalvar?: (experiencias: Experiencia[]) => void;
}

/**
 * Compõe a página de cadastro de experiências profissionais (Etapa 3 de 8).
 *
 * Utiliza o layout compartilhado de cadastro de currículo, com o painel visual
 * retangular degradê e a barra de progresso segmentada na terceira etapa.
 */
export function PaginaExperienciasProfissionais({
  experienciasIniciais,
  onSalvar,
}: PaginaExperienciasProfissionaisProps) {
  const [progresso, setProgresso] = useState(0);

  return (
    <LayoutCadastroCurriculo
      subtitulo="Experiência Profissional"
      etapaAtual={3}
      totalEtapas={8}
      progressoEtapaAtual={progresso}
    >
      <section
        aria-labelledby="titulo-experiencias"
        className="pagina-experiencias-profissionais__conteudo"
      >
        <h1
          id="titulo-experiencias"
          className="pagina-experiencias-profissionais__sr-only"
        >
          Experiências profissionais
        </h1>
        <FormularioExperiencias
          aoAlterarProgresso={setProgresso}
          experienciasIniciais={experienciasIniciais}
          onSalvar={onSalvar}
        />
      </section>
    </LayoutCadastroCurriculo>
  );
}
