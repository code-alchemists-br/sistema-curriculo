import { useState } from "react";

import {
  criarClienteFormacaoAcademicaIndisponivel,
  FormularioFormacaoAcademica,
  type ClienteFormacaoAcademica,
} from "../../../features/cadastrar-formacao-academica";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaFormacaoAcademica.css";

/** Define a dependência opcional usada pela página de formação acadêmica. */
export interface PaginaFormacaoAcademicaProps {
  cliente?: ClienteFormacaoAcademica;
}

/**
 * Compõe a tela de cadastro de formação acadêmica (Etapa 2 de 8).
 *
 * Utiliza o layout compartilhado de cadastro de currículo, com o painel visual
 * retangular degradê e a barra de progresso segmentada na segunda etapa.
 */
export function PaginaFormacaoAcademica({
  cliente,
}: PaginaFormacaoAcademicaProps) {
  const [progresso, setProgresso] = useState(0);

  return (
    <LayoutCadastroCurriculo
      subtitulo="Formação Acadêmica"
      etapaAtual={2}
      totalEtapas={8}
      progressoEtapaAtual={progresso}
    >
      <section
        aria-labelledby="titulo-formacao"
        className="pagina-formacao-academica__conteudo"
      >
        <h1 id="titulo-formacao" className="pagina-formacao-academica__sr-only">
          Formação acadêmica
        </h1>
        <FormularioFormacaoAcademica
          aoAlterarProgresso={setProgresso}
          cliente={cliente ?? criarClienteFormacaoAcademicaIndisponivel()}
        />
      </section>
    </LayoutCadastroCurriculo>
  );
}
