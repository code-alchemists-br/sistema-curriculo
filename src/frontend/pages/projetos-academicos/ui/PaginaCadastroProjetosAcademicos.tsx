import { useState } from "react";

import {
  criarClienteProjetosAcademicosEmMemoria,
  FormularioCadastroProjetoAcademico,
  type ClienteProjetosAcademicos,
  type ValoresProjetoAcademico,
} from "../../../features/cadastro-projeto-academico";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaCadastroProjetosAcademicos.css";

/** Define as propriedades para compor a página de projetos acadêmicos. */
export interface PaginaCadastroProjetosAcademicosProps {
  cliente?: ClienteProjetosAcademicos;
  onAvancar?: () => void;
  onVoltar?: () => void;
  projetosIniciais?: ValoresProjetoAcademico[];
  aoAlterarProjetos?: (projetos: ValoresProjetoAcademico[]) => void;
}

/**
 * Compõe a página de cadastro de projetos acadêmicos (Etapa 7 de 9).
 *
 * Utiliza o layout compartilhado de cadastro de currículo, com o painel visual
 * retangular degradê e a barra de progresso segmentada na sétima etapa.
 */
export function PaginaCadastroProjetosAcademicos({
  cliente = criarClienteProjetosAcademicosEmMemoria(),
  onAvancar,
  onVoltar,
  projetosIniciais,
  aoAlterarProjetos,
}: PaginaCadastroProjetosAcademicosProps) {
  const [progresso, setProgresso] = useState(0);

  function handleAvancar(): void {
    if (onAvancar) {
      onAvancar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=selecionar-modelo";
    }
  }

  function handleVoltar(): void {
    if (onVoltar) {
      onVoltar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=competencias";
    }
  }

  return (
    <LayoutCadastroCurriculo
      subtitulo="Projetos Acadêmicos"
      etapaAtual={7}
      totalEtapas={9}
      progressoEtapaAtual={progresso}
    >
      <section
        aria-labelledby="titulo-pagina-projetos"
        className="pagina-projetos__conteudo"
      >
        <h1 id="titulo-pagina-projetos" className="pagina-projetos__sr-only">
          Projetos acadêmicos
        </h1>

        <FormularioCadastroProjetoAcademico
          cliente={cliente}
          aoAlterarProgresso={setProgresso}
          aoAvancar={handleAvancar}
          onVoltar={handleVoltar}
          projetosIniciais={projetosIniciais}
          aoAlterarProjetos={aoAlterarProjetos}
        />
      </section>
    </LayoutCadastroCurriculo>
  );
}
