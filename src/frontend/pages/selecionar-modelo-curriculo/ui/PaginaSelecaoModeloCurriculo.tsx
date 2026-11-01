import { useState } from "react";

import {
  AlternadorModeloCurriculo,
  obterModeloRecomendadoPorObjetivo,
  obterRecomendacaoModelo,
  OPCOES_OBJETIVO_CURRICULO,
  type ModeloApresentacaoCurriculo,
  type ObjetivoCurriculo,
} from "../../../features/alternar-modelo-curriculo";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaSelecaoModeloCurriculo.css";

/** Define os dados necessários para confirmar a escolha de modelo na página. */
export interface PaginaSelecaoModeloCurriculoProps {
  /** Modelo inicialmente marcado ao abrir a tela. */
  modeloInicial?: ModeloApresentacaoCurriculo;
  /** Ação que a composição da rota usa para associar o modelo ao currículo. */
  aoConfirmar: (modelo: ModeloApresentacaoCurriculo) => void;
  /** Ação para retornar à etapa anterior. */
  onVoltar?: () => void;
}

/**
 * Compõe a tela que orienta e confirma o modelo de apresentação do currículo.
 *
 * - O que faz: Mostra o objetivo profissional e todos os modelos reconhecidos pelo catálogo.
 * - Como faz: Mantém somente a seleção visual local e entrega o valor confirmado por callback, sem realizar HTTP ou simular persistência.
 * - Qual finalidade atende: Permite que a rota de criação associe um modelo válido à versão de currículo sem duplicar o seletor já existente na feature.
 */
export function PaginaSelecaoModeloCurriculo({
  modeloInicial = "classico",
  aoConfirmar,
  onVoltar,
}: PaginaSelecaoModeloCurriculoProps) {
  const [objetivo, setObjetivo] = useState<ObjetivoCurriculo>("outro");
  const [modeloSelecionado, setModeloSelecionado] =
    useState<ModeloApresentacaoCurriculo>(modeloInicial);
  const recomendacao = obterRecomendacaoModelo(objetivo);

  function aoAlterarObjetivo(novoObjetivo: ObjetivoCurriculo): void {
    setObjetivo(novoObjetivo);
    const modeloSugerido = obterModeloRecomendadoPorObjetivo(novoObjetivo);
    setModeloSelecionado(modeloSugerido);
  }

  return (
    <LayoutCadastroCurriculo
      subtitulo="Seleção de Modelo"
      etapaAtual={8}
      totalEtapas={9}
      progressoEtapaAtual={modeloSelecionado ? 100 : 0}
    >
      <section
        aria-labelledby="titulo-selecao-modelo"
        className="pagina-selecao-modelo__conteudo"
      >
        <h1
          id="titulo-selecao-modelo"
          className="pagina-selecao-modelo__sr-only"
        >
          Escolha um modelo de currículo
        </h1>
        <p className="pagina-selecao-modelo__descricao">
          O modelo altera somente a apresentação visual. Suas informações
          permanecem salvas e você poderá alternar entre os modelos a qualquer
          momento.
        </p>

        <div className="pagina-selecao-modelo__campo">
          <label className="titulo-campo" htmlFor="objetivo-curriculo">
            Objetivo do currículo
          </label>
          <select
            id="objetivo-curriculo"
            onChange={(evento) =>
              aoAlterarObjetivo(evento.target.value as ObjetivoCurriculo)
            }
            value={objetivo}
          >
            {OPCOES_OBJETIVO_CURRICULO.map((opcao) => (
              <option key={opcao.valor} value={opcao.valor}>
                {opcao.rotulo}
              </option>
            ))}
          </select>
        </div>

        <p className="pagina-selecao-modelo__recomendacao" role="status">
          {recomendacao}
        </p>

        <AlternadorModeloCurriculo
          modeloSelecionado={modeloSelecionado}
          onSelecionarModelo={setModeloSelecionado}
        />

        <div className="botoes-navegacao">
          <button
            aria-label="Voltar para a etapa anterior"
            className="btn-voltar"
            onClick={onVoltar}
            type="button"
          >
            Voltar
          </button>
          <button
            aria-label="Continuar com o modelo selecionado"
            className="btn-proximo"
            onClick={() => aoConfirmar(modeloSelecionado)}
            type="button"
          >
            Próximo
          </button>
        </div>
      </section>
    </LayoutCadastroCurriculo>
  );
}
