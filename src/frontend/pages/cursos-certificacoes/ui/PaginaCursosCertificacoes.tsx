import { useState } from "react";

import {
  FormularioCertificacao,
  type ValoresCertificacao,
} from "../../../features/cadastro-certificacoes";
import { FormularioCursos, type Curso } from "../../../features/edit-courses";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaCursosCertificacoes.css";

/** Propriedades da página de cadastro de cursos e certificações. */
export interface PaginaCursosCertificacoesProps {
  onAvancar?: () => void;
  onVoltar?: () => void;
  cursosIniciais?: Curso[];
  certificacoesIniciais?: ValoresCertificacao[];
  aoAlterarCursos?: (cursos: Curso[]) => void;
  aoAlterarCertificacoes?: (certificacoes: ValoresCertificacao[]) => void;
}

/**
 * Compõe a página de cadastro de cursos e certificações (Etapa 4 de 9).
 *
 * Apresenta o painel visual com o título 'Cursos e Certificações' e agrupa
 * os formulários de Cursos Livres e Certificações Complementares.
 */
export function PaginaCursosCertificacoes({
  onAvancar,
  onVoltar,
  cursosIniciais,
  certificacoesIniciais,
  aoAlterarCursos,
  aoAlterarCertificacoes,
}: PaginaCursosCertificacoesProps = {}) {
  const [progressoCursos, setProgressoCursos] = useState(0);
  const [progressoCertificacao, setProgressoCertificacao] = useState(0);

  function handleAvancar(): void {
    if (onAvancar) {
      onAvancar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=idiomas";
    }
  }

  function handleVoltar(): void {
    if (onVoltar) {
      onVoltar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=experiencias-profissionais";
    }
  }

  const progresso =
    progressoCertificacao > 0
      ? Math.round(progressoCursos * 0.6 + progressoCertificacao * 0.4)
      : progressoCursos;

  return (
    <LayoutCadastroCurriculo
      subtitulo="Cursos e Certificações"
      etapaAtual={4}
      totalEtapas={9}
      progressoEtapaAtual={progresso}
    >
      <section
        aria-labelledby="titulo-cursos-certificacoes"
        className="pagina-cursos-certificacoes__conteudo"
      >
        <h1
          id="titulo-cursos-certificacoes"
          className="pagina-cursos-certificacoes__sr-only"
        >
          Cursos e Certificações
        </h1>

        <FormularioCursos
          aoAlterarProgresso={setProgressoCursos}
          cursosIniciais={cursosIniciais}
          aoAlterarCursos={aoAlterarCursos}
          exibirBotaoSalvar={false}
        />

        <FormularioCertificacao
          aoAlterarProgresso={setProgressoCertificacao}
          certificacoesIniciais={certificacoesIniciais}
          aoAlterarCertificacoes={aoAlterarCertificacoes}
          exibirBotaoSalvar={false}
        />

        <div className="botoes-navegacao">
          <button
            type="button"
            className="btn-voltar"
            onClick={handleVoltar}
            aria-label="Voltar para a etapa anterior"
          >
            Voltar
          </button>
          <button
            aria-label="Avançar para próxima etapa"
            className="pagina-cursos-certificacoes__btn-proximo"
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
