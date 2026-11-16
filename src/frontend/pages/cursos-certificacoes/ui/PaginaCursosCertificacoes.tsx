import { useRef, useState } from "react";

import {
  FormularioCertificacao,
  type ValoresCertificacao,
} from "../../../features/cadastro-certificacoes";
import { FormularioCursos, type Curso } from "../../../features/edit-courses";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaCursosCertificacoes.css";

/** Propriedades da página de cadastro de cursos e certificações. */
export interface PaginaCursosCertificacoesProps {
  onAvancar?: (
    cursos: Curso[],
    certificacoes: ValoresCertificacao[],
  ) => void | Promise<void>;
  /** Permite prosseguir por decisão explícita sem afirmar sincronização com o perfil. */
  onContinuarLocal?: (
    cursos: Curso[],
    certificacoes: ValoresCertificacao[],
  ) => void;
  onVoltar?: () => void;
  onVoltarInicio?: () => void;
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
  onContinuarLocal,
  onVoltar,
  onVoltarInicio,
  cursosIniciais,
  certificacoesIniciais,
  aoAlterarCursos,
  aoAlterarCertificacoes,
}: PaginaCursosCertificacoesProps = {}) {
  const [progressoCursos, setProgressoCursos] = useState(0);
  const [progressoCertificacao, setProgressoCertificacao] = useState(0);
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const envioEmCurso = useRef(false);
  const formularioCursos = useRef<{ validar: () => Curso[] | null }>(null);
  const formularioCertificacoes = useRef<{
    validar: () => ValoresCertificacao[] | null;
  }>(null);

  /** Delega validação às features e aguarda persistência para avançar sem ocultar falhas nem perder o rascunho. */
  async function handleAvancar(): Promise<void> {
    if (envioEmCurso.current) return;
    setErro(null);
    const cursos = formularioCursos.current?.validar();
    if (!cursos) return;
    const certificacoes = formularioCertificacoes.current?.validar();
    if (!certificacoes) return;
    envioEmCurso.current = true;
    setEnviando(true);
    try {
      if (onAvancar) {
        await onAvancar(cursos, certificacoes);
      } else if (typeof window !== "undefined") {
        window.location.search = "?etapa=idiomas";
      }
    } catch (falha) {
      const duplicado =
        typeof falha === "object" &&
        falha !== null &&
        "statusHttp" in falha &&
        falha.statusHttp === 409;
      setErro(
        duplicado
          ? "Este cadastro já existe no perfil. Este fluxo cria registros, mas não atualiza os existentes. Restaure os valores anteriores ou continue apenas com o rascunho local, sem sincronizar estas alterações."
          : "Não foi possível salvar cursos e certificações. Seus dados foram preservados no rascunho. Verifique sua conexão ou sessão e tente novamente.",
      );
    } finally {
      envioEmCurso.current = false;
      setEnviando(false);
    }
  }

  /** Retorna por callback ou URL à etapa anterior para preservar a navegação e o rascunho existentes. */
  function handleVoltar(): void {
    if (onVoltar) {
      onVoltar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=experiencias-profissionais";
    }
  }

  /** Valida o rascunho atual e executa a opção local explícita sem fingir confirmação do servidor. */
  function continuarLocal(): void {
    if (enviando) return;
    const cursos = formularioCursos.current?.validar();
    if (!cursos) return;
    const certificacoes = formularioCertificacoes.current?.validar();
    if (!certificacoes) return;
    onContinuarLocal?.(cursos, certificacoes);
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
      onVoltarInicio={onVoltarInicio}
    >
      <section
        aria-busy={enviando}
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
          aoAvancar={handleAvancar}
          ref={formularioCursos}
          permitirVazios
          desabilitado={enviando}
          aoAlterarProgresso={setProgressoCursos}
          cursosIniciais={cursosIniciais}
          aoAlterarCursos={aoAlterarCursos}
          exibirBotaoSalvar={false}
        />

        <FormularioCertificacao
          aoAvancar={handleAvancar}
          ref={formularioCertificacoes}
          permitirVazios
          desabilitado={enviando}
          aoAlterarProgresso={setProgressoCertificacao}
          certificacoesIniciais={certificacoesIniciais}
          aoAlterarCertificacoes={aoAlterarCertificacoes}
          exibirBotaoSalvar={false}
        />

        {erro && (
          <p className="form-message form-message--erro" role="alert">
            {erro}
          </p>
        )}
        {enviando && <p role="status">Salvando cursos e certificações...</p>}
        {erro && onContinuarLocal && (
          <div>
            <p>
              Esta opção mantém os dados apenas no rascunho e não atualiza os
              cadastros do perfil.
            </p>
            <button type="button" disabled={enviando} onClick={continuarLocal}>
              Continuar apenas com rascunho local
            </button>
          </div>
        )}
        <div className="botoes-navegacao">
          <button
            disabled={enviando}
            type="button"
            className="btn-voltar"
            onClick={handleVoltar}
            aria-label="Voltar para a etapa anterior"
          >
            Voltar
          </button>
          <button
            disabled={enviando}
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
