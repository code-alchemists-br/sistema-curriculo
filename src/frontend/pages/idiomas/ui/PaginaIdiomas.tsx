import { useRef, useState } from "react";

import {
  FormularioIdiomas,
  type Idioma,
} from "../../../features/edit-languages";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaIdiomas.css";

/** Propriedades da página de cadastro de idiomas. */
export interface PaginaIdiomasProps {
  onAvancar?: (idiomas: Idioma[]) => void | Promise<void>;
  /** Permite prosseguir por decisão explícita sem afirmar sincronização com o perfil. */
  onContinuarLocal?: (idiomas: Idioma[]) => void;
  onVoltar?: () => void;
  onVoltarInicio?: () => void;
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
  onContinuarLocal,
  onVoltar,
  onVoltarInicio,
  idiomasIniciais,
  onSalvar,
}: PaginaIdiomasProps = {}) {
  const [progressoIdiomas, setProgressoIdiomas] = useState(0);
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const envioEmCurso = useRef(false);
  const formulario = useRef<{ validar: () => Idioma[] | null }>(null);

  /** Delega validação às features e aguarda persistência para avançar sem ocultar falhas nem perder o rascunho. */
  async function handleAvancar(): Promise<void> {
    if (envioEmCurso.current) return;
    setErro(null);
    const idiomas = formulario.current?.validar();
    if (!idiomas) return;
    envioEmCurso.current = true;
    setEnviando(true);
    try {
      if (onAvancar) {
        await onAvancar(idiomas);
      } else if (typeof window !== "undefined") {
        window.location.search = "?etapa=competencias";
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
          : "Não foi possível salvar idiomas. Seus dados foram preservados no rascunho. Verifique sua conexão ou sessão e tente novamente.",
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
      window.location.search = "?etapa=cursos-certificacoes";
    }
  }

  /** Valida o rascunho atual e executa a opção local explícita sem fingir confirmação do servidor. */
  function continuarLocal(): void {
    if (enviando) return;
    const idiomas = formulario.current?.validar();
    if (!idiomas) return;
    onContinuarLocal?.(idiomas);
  }

  return (
    <LayoutCadastroCurriculo
      subtitulo="Idiomas"
      etapaAtual={5}
      totalEtapas={9}
      progressoEtapaAtual={progressoIdiomas}
      onVoltarInicio={onVoltarInicio}
    >
      <section
        aria-busy={enviando}
        aria-labelledby="titulo-idiomas"
        className="pagina-idiomas__conteudo"
      >
        <h1 id="titulo-idiomas" className="pagina-idiomas__sr-only">
          Idiomas
        </h1>

        <FormularioIdiomas
          aoAvancar={handleAvancar}
          ref={formulario}
          permitirVazios
          desabilitado={enviando}
          aoAlterarProgresso={setProgressoIdiomas}
          aoAlterarDados={onSalvar}
          exibirBotaoSalvar={false}
          exibirTitulo={false}
          idiomasIniciais={idiomasIniciais}
          onSalvar={onSalvar}
        />

        {erro && (
          <p className="form-message form-message--erro" role="alert">
            {erro}
          </p>
        )}
        {enviando && <p role="status">Salvando idiomas...</p>}
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
            aria-label="Voltar para a etapa anterior"
            className="btn-voltar"
            onClick={handleVoltar}
            type="button"
          >
            Voltar
          </button>
          <button
            disabled={enviando}
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
