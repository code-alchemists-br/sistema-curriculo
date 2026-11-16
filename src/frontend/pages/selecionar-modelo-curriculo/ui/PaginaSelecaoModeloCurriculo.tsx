import { useMemo, useState } from "react";

import {
  criarClienteAssistenteIa,
  RecomendacaoModeloIa,
  type ModeloSugerido,
} from "../../../features/assistente-ia";
import {
  AlternadorModeloCurriculo,
  inferirObjetivoDoPerfil,
  obterModeloRecomendadoPorObjetivo,
  obterRecomendacaoModelo,
  OPCOES_OBJETIVO_CURRICULO,
  resumirPerfilParaIa,
  type ModeloApresentacaoCurriculo,
  type ObjetivoCurriculo,
  type PerfilParaRecomendacao,
} from "../../../features/alternar-modelo-curriculo";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaSelecaoModeloCurriculo.css";

const NOMES_MODELO: Record<ModeloSugerido, string> = {
  classico: "Clássico",
  compacto: "Compacto",
  "ats-simples": "ATS simples",
  criativo: "Criativo",
  moderno: "Moderno",
  academico: "Acadêmico",
  "primeiro-emprego": "Primeiro emprego",
};

/** Define os dados necessários para confirmar a escolha de modelo na página. */
export interface PaginaSelecaoModeloCurriculoProps {
  /** Modelo inicialmente marcado ao abrir a tela. */
  modeloInicial?: ModeloApresentacaoCurriculo;
  /** Ação que a composição da rota usa para associar o modelo ao currículo. */
  aoConfirmar: (modelo: ModeloApresentacaoCurriculo) => void;
  /** Ação para retornar à etapa anterior. */
  onVoltar?: () => void;
  /** Ação opcional para retornar à página inicial / hero. */
  onVoltarInicio?: () => void;
  /** Dados estruturados do estudante preenchidos nas etapas anteriores para inferência inteligente. */
  perfilEstudante?: PerfilParaRecomendacao;
}

/**
 * Compõe a tela que orienta e confirma o modelo de apresentação do currículo.
 *
 * - O que faz: Mostra o objetivo profissional e todos os modelos reconhecidos pelo catálogo.
 * - Como faz: Mantém somente a seleção visual local e entrega o valor confirmado por callback, sem realizar HTTP ou simular persistência. Mostra uma única recomendação: a da IA quando ela responde para o objetivo atual, ou a das regras fixas quando a IA ainda não respondeu ou está indisponível.
 * - Qual finalidade atende: Permite que a rota de criação associe um modelo válido à versão de currículo sem duplicar o seletor já existente na feature.
 */
export function PaginaSelecaoModeloCurriculo({
  modeloInicial = "classico",
  aoConfirmar,
  onVoltar,
  onVoltarInicio,
  perfilEstudante,
}: PaginaSelecaoModeloCurriculoProps) {
  const objetivoInferido = useMemo(
    () =>
      perfilEstudante ? inferirObjetivoDoPerfil(perfilEstudante) : "outro",
    [perfilEstudante],
  );
  const modeloInferido = useMemo(
    () => obterModeloRecomendadoPorObjetivo(objetivoInferido),
    [objetivoInferido],
  );

  const [objetivo, setObjetivo] = useState<ObjetivoCurriculo>(() =>
    perfilEstudante ? objetivoInferido : "outro",
  );
  const [modeloSelecionado, setModeloSelecionado] =
    useState<ModeloApresentacaoCurriculo>(() => {
      if (modeloInicial && modeloInicial !== "classico") {
        return modeloInicial;
      }
      return perfilEstudante ? modeloInferido : modeloInicial;
    });

  const clienteIa = useMemo(() => criarClienteAssistenteIa(), []);
  const perfilParaIa = useMemo(
    () =>
      resumirPerfilParaIa(
        perfilEstudante,
        OPCOES_OBJETIVO_CURRICULO.find((o) => o.valor === objetivo)?.rotulo ??
          objetivo,
      ),
    [objetivo, perfilEstudante],
  );
  // Recomendação da IA para o objetivo atual. Quando existe, substitui a
  // recomendação por regras fixas, para a tela não mostrar duas indicações.
  const [modeloIa, setModeloIa] = useState<ModeloSugerido | null>(null);
  // A IA roda sozinha só ao abrir a tela; depois de trocar o objetivo o
  // estudante pede de novo pelo botão (evita gastar chamadas a cada troca).
  const [iaAutomatica, setIaAutomatica] = useState(true);
  const recomendacao = obterRecomendacaoModelo(objetivo);
  const modeloRecomendado =
    modeloIa ?? obterModeloRecomendadoPorObjetivo(objetivo);

  function aoAlterarObjetivo(novoObjetivo: ObjetivoCurriculo): void {
    setObjetivo(novoObjetivo);
    setModeloIa(null);
    setIaAutomatica(false);
    const modeloSugerido = obterModeloRecomendadoPorObjetivo(novoObjetivo);
    setModeloSelecionado(modeloSugerido);
  }

  function aoRecomendarComIa(modelo: ModeloSugerido): void {
    setModeloIa(modelo);
    setModeloSelecionado(modelo);
  }

  return (
    <LayoutCadastroCurriculo
      subtitulo="Seleção de Modelo"
      etapaAtual={8}
      totalEtapas={9}
      progressoEtapaAtual={modeloSelecionado ? 100 : 0}
      onVoltarInicio={onVoltarInicio}
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

        {modeloIa === null && (
          <p className="pagina-selecao-modelo__recomendacao" role="status">
            {recomendacao}
          </p>
        )}

        <RecomendacaoModeloIa
          key={objetivo}
          automatico={iaAutomatica}
          aoRecomendar={aoRecomendarComIa}
          cliente={clienteIa}
          nomeDoModelo={(modelo) => NOMES_MODELO[modelo] ?? modelo}
          perfil={perfilParaIa}
        />

        <AlternadorModeloCurriculo
          modeloRecomendado={modeloRecomendado}
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
