import type { ComponentType } from "react";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import type { ModeloApresentacaoCurriculo } from "../../../features/alternar-modelo-curriculo";
import {
  ModeloAcademico,
  ModeloAtsSimples,
  ModeloClassico,
  ModeloCompacto,
  ModeloCriativo,
  ModeloModerno,
  ModeloPrimeiroEmprego,
} from "../../../features/visualizar-curriculo";
import "./PaginaVisualizacaoCurriculo.css";

/** Define os dados de composição para a tela de visualização do currículo. */
export interface PaginaVisualizacaoCurriculoProps {
  /** Dados estruturados retornados para a prévia da versão de currículo. */
  previa: PreviaCurriculo;
  /** Modelo que será aplicado aos dados recebidos. */
  modelo: ModeloApresentacaoCurriculo;
  /** Ação opcional que devolve o estudante à seleção de modelos. */
  aoAlterarModelo?: () => void;
}

const rotulosModelo: Readonly<Record<ModeloApresentacaoCurriculo, string>> = {
  classico: "Profissional clássico",
  compacto: "Compacto",
  "ats-simples": "ATS simples",
  criativo: "Criativo",
  moderno: "Moderno",
  academico: "Acadêmico",
  "primeiro-emprego": "Primeiro emprego",
};

const modelos: Readonly<
  Record<
    ModeloApresentacaoCurriculo,
    ComponentType<{ previa: PreviaCurriculo }>
  >
> = {
  classico: ModeloClassico,
  compacto: ModeloCompacto,
  "ats-simples": ModeloAtsSimples,
  criativo: ModeloCriativo,
  moderno: ModeloModerno,
  academico: ModeloAcademico,
  "primeiro-emprego": ModeloPrimeiroEmprego,
};

/**
 * Compõe a tela de visualização do currículo no modelo escolhido.
 *
 * - O que faz: Exibe a prévia recebida em um dos modelos reconhecidos pelo catálogo.
 * - Como faz: Seleciona somente o componente visual e repassa a mesma referência de `previa`, sem transformar dados.
 * - Qual finalidade atende: Permite comparar apresentações diferentes preservando integralmente as informações escolhidas pelo estudante.
 */
export function PaginaVisualizacaoCurriculo({
  previa,
  modelo,
  aoAlterarModelo,
}: PaginaVisualizacaoCurriculoProps) {
  const ModeloSelecionado = modelos[modelo];

  return (
    <main className="pagina-visualizacao-curriculo">
      <section
        aria-labelledby="titulo-visualizacao-curriculo"
        className="pagina-visualizacao-curriculo__conteudo"
      >
        <header className="pagina-visualizacao-curriculo__cabecalho">
          <div>
            <p className="pagina-visualizacao-curriculo__sobretitulo">
              Currículo
            </p>
            <h1 id="titulo-visualizacao-curriculo">
              Visualização do currículo
            </h1>
            <p>
              Modelo selecionado: <strong>{rotulosModelo[modelo]}</strong>
            </p>
          </div>
          {aoAlterarModelo !== undefined && (
            <button onClick={aoAlterarModelo} type="button">
              Alterar modelo
            </button>
          )}
        </header>

        <ModeloSelecionado previa={previa} />
      </section>
    </main>
  );
}
