import { useState } from "react";

import { FormularioIdiomas, type Idioma } from "../../../features/edit-languages";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaIdiomas.css";

/** Propriedades da página de cadastro de idiomas. */
export interface PaginaIdiomasProps {
  onAvancar?: () => void;
  onVoltar?: () => void;
  idiomasIniciais?: Idioma[];
  onSalvar?: (idiomas: Idioma[]) => void;
}

/**
 * Compõe a página de cadastro de idiomas (Etapa 5 de 9).
 *
 * Apresenta o painel visual com o título 'Idiomas' e o formulário
 * para adição e controle de línguas e níveis de proficiência.
 */
export function PaginaIdiomas({
  onAvancar,
  onVoltar,
  idiomasIniciais,
  onSalvar,
}: PaginaIdiomasProps = {}) {
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

  function handleVoltar(): void {
    if (onVoltar) {
      onVoltar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=cursos-certificacoes";
    }
  }

  return (
    <LayoutCadastroCurriculo
      subtitulo="Idiomas"
      etapaAtual={5}
      totalEtapas={9}
      progressoEtapaAtual={progressoIdiomas}
    >
      <section
        aria-labelledby="titulo-idiomas"
        className="pagina-idiomas__conteudo"
      >
        <h1 id="titulo-idiomas" className="pagina-idiomas__sr-only">
          Idiomas
        </h1>

        <FormularioIdiomas
          aoAlterarProgresso={setProgressoIdiomas}
          aoAlterarDados={onSalvar}
          exibirBotaoSalvar={false}
          exibirTitulo={false}
          idiomasIniciais={idiomasIniciais}
          onSalvar={onSalvar}
        />

        <div className="botoes-navegacao">
          <button
            aria-label="Voltar para a etapa anterior"
            className="btn-voltar"
            onClick={handleVoltar}
            type="button"
          >
            Voltar
          </button>
          <button
            aria-label="Avançar para próxima etapa"
            className="pagina-idiomas__btn-proximo"
            onClick={handleAvancar}
            type="button"
          >
            Próximo
          </button>
        </div>
      </section>
    </LayoutCadastroCurriculo>
  );
}
