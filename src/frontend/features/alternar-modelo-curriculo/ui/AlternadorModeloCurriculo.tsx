import type { ReactElement } from "react";
import "./AlternadorModeloCurriculo.css";

export type ModeloApresentacaoCurriculo = "classico" | "compacto";

interface AlternadorModeloCurriculoProps {
  modeloSelecionado: ModeloApresentacaoCurriculo;
  onSelecionarModelo: (modelo: ModeloApresentacaoCurriculo) => void;
}

const opcoes: ReadonlyArray<{
  valor: ModeloApresentacaoCurriculo;
  rotulo: string;
  descricao: string;
}> = [
  {
    valor: "classico",
    rotulo: "Clássico",
    descricao: "Apresentação tradicional das informações do currículo.",
  },
  {
    valor: "compacto",
    rotulo: "Compacto",
    descricao: "Apresentação com organização visual mais condensada.",
  },
];

/**
 * Permite escolher, por controles nativos acessíveis, o modelo exibido na prévia.
 *
 * Além dos rádios, apresenta uma miniatura estrutural de cada modelo para
 * orientar a escolha sem depender apenas do hover do mouse.
 */
export function AlternadorModeloCurriculo({
  modeloSelecionado,
  onSelecionarModelo,
}: AlternadorModeloCurriculoProps): ReactElement {
  return (
    <fieldset className="alternador-modelo-curriculo">
      <legend>Modelo de apresentação</legend>
      <p id="ajuda-modelo-curriculo">
        Escolha como o currículo será apresentado na prévia.
      </p>

      <div className="alternador-modelo-curriculo__opcoes">
        {opcoes.map((opcao) => {
          const id = `modelo-curriculo-${opcao.valor}`;
          const descricaoId = `${id}-descricao`;

          return (
            <div
              className="alternador-modelo-curriculo__opcao"
              key={opcao.valor}
            >
              <input
                aria-describedby={`ajuda-modelo-curriculo ${descricaoId}`}
                checked={modeloSelecionado === opcao.valor}
                id={id}
                name="modelo-apresentacao-curriculo"
                onChange={() => onSelecionarModelo(opcao.valor)}
                type="radio"
                value={opcao.valor}
              />

              <label htmlFor={id}>{opcao.rotulo}</label>

              <PreviaEstruturalModelo modelo={opcao.valor} />

              <p id={descricaoId}>{opcao.descricao}</p>
            </div>
          );
        })}
      </div>
    </fieldset>
  );
}

/**
 * Exibe uma representação estrutural estática do modelo escolhido.
 *
 * Não há dados reais nem elementos interativos nesta miniatura. Ela apenas
 * mostra a hierarquia visual das seções que o currículo suporta.
 */
function PreviaEstruturalModelo({
  modelo,
}: {
  modelo: ModeloApresentacaoCurriculo;
}): ReactElement {
  if (modelo === "classico") {
    return <PreviaModeloClassico />;
  }

  return <PreviaModeloCompacto />;
}

/**
 * Representa o modelo clássico com cabeçalho central e seções separadas.
 */
function PreviaModeloClassico(): ReactElement {
  return (
    <div
      aria-hidden="true"
      className="previsao-modelo previsao-modelo--classico"
    >
      <div className="previsao-modelo__cabecalho-classico">
        <span className="previsao-modelo__nome">NOME COMPLETO</span>
        <span className="previsao-modelo__contato">
          e-mail · telefone · cidade
        </span>
        <span className="previsao-modelo__links">LinkedIn · Lattes</span>
      </div>

      <SecaoMiniaturaClassica titulo="EXPERIÊNCIA" linhas={2} />
      <SecaoMiniaturaClassica titulo="FORMAÇÃO" linhas={2} />
      <SecaoMiniaturaClassica titulo="PROJETOS" linhas={1} />

      <div className="previsao-modelo__grade-classica">
        <SecaoMiniaturaClassica titulo="COMPETÊNCIAS" linhas={2} />
        <SecaoMiniaturaClassica titulo="IDIOMAS" linhas={2} />
      </div>

      <SecaoMiniaturaClassica titulo="DOCUMENTOS" linhas={1} />
    </div>
  );
}

/**
 * Representa o modelo compacto com cabeçalho à esquerda e conteúdo condensado.
 */
function PreviaModeloCompacto(): ReactElement {
  return (
    <div
      aria-hidden="true"
      className="previsao-modelo previsao-modelo--compacto"
    >
      <div className="previsao-modelo__cabecalho-compacto">
        <span className="previsao-modelo__nome">NOME COMPLETO</span>
        <span className="previsao-modelo__contato">
          e-mail · telefone · cidade
        </span>
        <span className="previsao-modelo__links">LinkedIn · Lattes</span>
      </div>

      <SecaoMiniaturaCompacta titulo="Experiência profissional" linhas={2} />
      <SecaoMiniaturaCompacta titulo="Formação acadêmica" linhas={2} />
      <SecaoMiniaturaCompacta titulo="Projetos acadêmicos" linhas={1} />

      <div className="previsao-modelo__itens-inline">
        <span>
          <strong>Competências:</strong>
        </span>
        <span>
          <strong>Idiomas:</strong>
        </span>
      </div>

      <SecaoMiniaturaCompacta titulo="Documentos complementares" linhas={1} />
    </div>
  );
}

/**
 * Representa uma seção com divisória usada no modelo clássico.
 */
function SecaoMiniaturaClassica({
  titulo,
  linhas,
}: {
  titulo: string;
  linhas: number;
}): ReactElement {
  return (
    <div className="previsao-modelo__secao-classica">
      <span className="previsao-modelo__titulo-classico">{titulo}</span>
      <LinhasMiniatura quantidade={linhas} />
    </div>
  );
}

/**
 * Representa uma seção compacta usada no modelo de mesmo nome.
 */
function SecaoMiniaturaCompacta({
  titulo,
  linhas,
}: {
  titulo: string;
  linhas: number;
}): ReactElement {
  return (
    <div className="previsao-modelo__secao-compacta">
      <span className="previsao-modelo__titulo-compacto">{titulo}</span>
      <LinhasMiniatura quantidade={linhas} />
    </div>
  );
}

/**
 * Gera linhas decorativas que representam itens de uma seção.
 */
function LinhasMiniatura({ quantidade }: { quantidade: number }): ReactElement {
  return (
    <div className="previsao-modelo__linhas">
      {Array.from({ length: quantidade }, (_, indice) => (
        <span
          className={`previsao-modelo__linha previsao-modelo__linha--${
            indice % 2 === 0 ? "longa" : "media"
          }`}
          key={indice}
        />
      ))}
    </div>
  );
}
