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

/** Permite escolher, por controles nativos acessíveis, o modelo exibido na prévia. */
export function AlternadorModeloCurriculo({
  modeloSelecionado,
  onSelecionarModelo,
}: AlternadorModeloCurriculoProps): JSX.Element {
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
              <p id={descricaoId}>{opcao.descricao}</p>
            </div>
          );
        })}
      </div>
    </fieldset>
  );
}
