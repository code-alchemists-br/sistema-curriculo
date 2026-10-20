import type { PreviaCurriculo } from "../../../entities/curriculo";
import type { ModeloApresentacaoCurriculo } from "../../../features/alternar-modelo-curriculo";
import {
  ModeloClassico,
  ModeloCompacto,
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

/**
 * Compõe a tela de visualização do currículo no modelo escolhido.
 *
 * O que faz: Exibe a prévia recebida usando o componente Clássico ou Compacto
 * que já existe no projeto.
 * Como faz: Escolhe exclusivamente entre os dois valores suportados pelo
 * contrato atual e repassa a mesma referência de `previa` ao modelo.
 * Por que existe: Separa a página do layout e garante que uma troca de modelo
 * não remove ou transforma os dados selecionados pelo estudante.
 */
export function PaginaVisualizacaoCurriculo({
  previa,
  modelo,
  aoAlterarModelo,
}: PaginaVisualizacaoCurriculoProps) {
  const rotuloModelo = modelo === "classico" ? "Clássico" : "Compacto";

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
              Modelo selecionado: <strong>{rotuloModelo}</strong>
            </p>
          </div>
          {aoAlterarModelo !== undefined && (
            <button onClick={aoAlterarModelo} type="button">
              Alterar modelo
            </button>
          )}
        </header>

        {modelo === "classico" ? (
          <ModeloClassico previa={previa} />
        ) : (
          <ModeloCompacto previa={previa} />
        )}
      </section>
    </main>
  );
}
