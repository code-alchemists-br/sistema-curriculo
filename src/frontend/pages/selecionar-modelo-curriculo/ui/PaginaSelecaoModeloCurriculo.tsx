import { useState } from "react";

import {
  AlternadorModeloCurriculo,
  obterRecomendacaoModelo,
  OPCOES_OBJETIVO_CURRICULO,
  type ModeloApresentacaoCurriculo,
  type ObjetivoCurriculo,
} from "../../../features/alternar-modelo-curriculo";
import "./PaginaSelecaoModeloCurriculo.css";

/** Define os dados necessários para confirmar a escolha de modelo na página. */
export interface PaginaSelecaoModeloCurriculoProps {
  /** Modelo inicialmente marcado ao abrir a tela. */
  modeloInicial?: ModeloApresentacaoCurriculo;
  /** Ação que a composição da rota usa para associar o modelo ao currículo. */
  aoConfirmar: (modelo: ModeloApresentacaoCurriculo) => void;
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
}: PaginaSelecaoModeloCurriculoProps) {
  const [objetivo, setObjetivo] = useState<ObjetivoCurriculo>("outro");
  const [modeloSelecionado, setModeloSelecionado] =
    useState<ModeloApresentacaoCurriculo>(modeloInicial);
  const recomendacao = obterRecomendacaoModelo(objetivo);

  return (
    <main className="pagina-selecao-modelo">
      <section
        aria-labelledby="titulo-selecao-modelo"
        className="pagina-selecao-modelo__conteudo"
      >
        <p className="pagina-selecao-modelo__sobretitulo">Currículo</p>
        <h1 id="titulo-selecao-modelo">Escolha um modelo de currículo</h1>
        <p>
          O modelo altera somente a apresentação. Suas informações continuam as
          mesmas e você poderá trocar a escolha depois.
        </p>

        <div className="pagina-selecao-modelo__campo">
          <label htmlFor="objetivo-curriculo">Objetivo do currículo</label>
          <select
            id="objetivo-curriculo"
            onChange={(evento) =>
              setObjetivo(evento.target.value as ObjetivoCurriculo)
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

        <button
          className="pagina-selecao-modelo__confirmar"
          onClick={() => aoConfirmar(modeloSelecionado)}
          type="button"
        >
          Continuar com o modelo selecionado
        </button>
      </section>
    </main>
  );
}
