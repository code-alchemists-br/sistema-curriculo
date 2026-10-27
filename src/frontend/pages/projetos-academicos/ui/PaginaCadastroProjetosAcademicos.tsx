import { useState } from "react";

import {
  criarClienteProjetosAcademicosIndisponivel,
  FormularioCadastroProjetoAcademico,
  type ClienteProjetosAcademicos,
} from "../../../features/cadastro-projeto-academico";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaCadastroProjetosAcademicos.css";

/** Define as propriedades para compor a página de projetos acadêmicos. */
export interface PaginaCadastroProjetosAcademicosProps {
  cliente?: ClienteProjetosAcademicos;
  onAvancar?: () => void;
}

/**
 * Compõe a página de cadastro de projetos acadêmicos (Etapa 6 de 8).
 *
 * Utiliza o layout compartilhado de cadastro de currículo, com o painel visual
 * retangular degradê e a barra de progresso segmentada na sexta etapa.
 */
export function PaginaCadastroProjetosAcademicos({
  cliente = criarClienteProjetosAcademicosIndisponivel(),
  onAvancar,
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

  return (
    <LayoutCadastroCurriculo
      subtitulo="Projetos Acadêmicos"
      etapaAtual={6}
      totalEtapas={8}
      progressoEtapaAtual={progresso}
    >
      <section
        aria-labelledby="titulo-pagina-projetos"
        className="pagina-projetos__conteudo"
      >
        <h1
          id="titulo-pagina-projetos"
          className="pagina-projetos__sr-only"
        >
          Projetos acadêmicos
        </h1>

        <FormularioCadastroProjetoAcademico
          cliente={cliente}
          aoAlterarProgresso={setProgresso}
          aoAvancar={handleAvancar}
        />
      </section>
    </LayoutCadastroCurriculo>
  );
}

