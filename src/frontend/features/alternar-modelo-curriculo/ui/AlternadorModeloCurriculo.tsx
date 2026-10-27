import type { ReactNode } from "react";

import "./AlternadorModeloCurriculo.css";

/** Identifica os modelos reconhecidos pelo frontend, incluindo o compacto legado. */
export type ModeloApresentacaoCurriculo =
  | "classico"
  | "compacto"
  | "ats-simples"
  | "criativo"
  | "moderno"
  | "academico"
  | "primeiro-emprego";

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
    valor: "ats-simples",
    rotulo: "ATS simples",
    descricao:
      "Uma coluna textual, adequada a sistemas de rastreamento de candidaturas.",
  },
  {
    valor: "classico",
    rotulo: "Profissional clássico",
    descricao: "Hierarquia sóbria com foco em experiência e formação.",
  },
  {
    valor: "compacto",
    rotulo: "Compacto",
    descricao: "Apresentação condensada das mesmas informações do currículo.",
  },
  {
    valor: "moderno",
    rotulo: "Moderno",
    descricao: "Equilíbrio entre competências, projetos e experiência.",
  },
  {
    valor: "criativo",
    rotulo: "Criativo",
    descricao: "Maior destaque visual para identidade e projetos.",
  },
  {
    valor: "academico",
    rotulo: "Acadêmico",
    descricao: "Prioriza formação e projetos acadêmicos disponíveis.",
  },
  {
    valor: "primeiro-emprego",
    rotulo: "Primeiro emprego",
    descricao:
      "Valoriza formação, projetos e competências antes da experiência.",
  },
];

/**
 * Permite escolher, por controles nativos acessíveis, um modelo de currículo.
 *
 * - O que faz: Exibe todos os modelos reconhecidos e comunica a escolha ao componente pai.
 * - Como faz: Usa rádios nativos e miniaturas estáticas sem dados pessoais reais ou dependência de hover.
 * - Qual finalidade atende: Orienta a escolha visual sem restringir a autonomia do estudante.
 */
export function AlternadorModeloCurriculo({
  modeloSelecionado,
  onSelecionarModelo,
}: AlternadorModeloCurriculoProps): ReactNode {
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
              className={`alternador-modelo-curriculo__opcao ${
                modeloSelecionado === opcao.valor
                  ? "alternador-modelo-curriculo__opcao--selecionada"
                  : ""
              }`}
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
              <MiniaturaModelo modelo={opcao.valor} />
              <p id={descricaoId}>{opcao.descricao}</p>
            </div>
          );
        })}
      </div>
    </fieldset>
  );
}

/**
 * Exibe uma miniatura estrutural não interativa do modelo indicado.
 *
 * - O que faz: Representa visualmente a hierarquia real de cada layout sem conteúdo pessoal.
 * - Como faz: Seleciona uma composição estática por modelo e oculta a decoração dos leitores de tela.
 * - Qual finalidade atende: Permite comparar modelos por mouse, toque ou teclado sem depender de uma descrição apenas visual.
 */
function MiniaturaModelo({
  modelo,
}: {
  modelo: ModeloApresentacaoCurriculo;
}): ReactNode {
  switch (modelo) {
    case "ats-simples":
      return <MiniaturaAtsSimples />;
    case "classico":
      return <MiniaturaClassica />;
    case "compacto":
      return <MiniaturaCompacta />;
    case "moderno":
      return <MiniaturaModerna />;
    case "criativo":
      return <MiniaturaCriativa />;
    case "academico":
      return <MiniaturaAcademica />;
    case "primeiro-emprego":
      return <MiniaturaPrimeiroEmprego />;
  }
}

/** Cria linhas neutras que representam texto de currículo nas miniaturas. */
function LinhasMiniatura({
  quantidade = 2,
}: {
  quantidade?: number;
}): ReactNode {
  return (
    <span className="miniatura-modelo__linhas">
      {Array.from({ length: quantidade }, (_, indice) => (
        <i key={indice} />
      ))}
    </span>
  );
}

/** Renderiza uma seção textual decorativa com o título recebido. */
function SecaoMiniatura({ titulo }: { titulo: string }): ReactNode {
  return (
    <section className="miniatura-modelo__secao">
      <b>{titulo}</b>
      <LinhasMiniatura />
    </section>
  );
}

/** Representa a leitura linear e de uma coluna do modelo ATS simples. */
function MiniaturaAtsSimples(): ReactNode {
  return (
    <div
      aria-hidden="true"
      className="miniatura-modelo miniatura-modelo--ats-simples"
    >
      <header className="miniatura-modelo__cabecalho-linear">
        <strong>NOME COMPLETO</strong>
        <span>e-mail · telefone · cidade · LinkedIn</span>
      </header>
      <div className="miniatura-modelo__coluna-linear">
        <SecaoMiniatura titulo="EXPERIÊNCIA PROFISSIONAL" />
        <SecaoMiniatura titulo="FORMAÇÃO ACADÊMICA" />
        <SecaoMiniatura titulo="PROJETOS" />
        <SecaoMiniatura titulo="COMPETÊNCIAS · IDIOMAS · DOCUMENTOS" />
      </div>
    </div>
  );
}

/** Representa a identificação centralizada e as seções tradicionais do clássico. */
function MiniaturaClassica(): ReactNode {
  return (
    <div
      aria-hidden="true"
      className="miniatura-modelo miniatura-modelo--classico"
    >
      <header className="miniatura-modelo__cabecalho-classico">
        <strong>NOME COMPLETO</strong>
        <span>e-mail · telefone · cidade</span>
        <span>LinkedIn · Currículo Lattes</span>
      </header>
      <div className="miniatura-modelo__coluna-classica">
        <SecaoMiniatura titulo="FORMAÇÃO ACADÊMICA" />
        <SecaoMiniatura titulo="EXPERIÊNCIA PROFISSIONAL" />
        <SecaoMiniatura titulo="PROJETOS ACADÊMICOS" />
        <div className="miniatura-modelo__grade-classica">
          <SecaoMiniatura titulo="COMPETÊNCIAS" />
          <SecaoMiniatura titulo="IDIOMAS" />
        </div>
      </div>
    </div>
  );
}

/** Representa a leitura condensada e direta do modelo compacto já existente. */
function MiniaturaCompacta(): ReactNode {
  return (
    <div
      aria-hidden="true"
      className="miniatura-modelo miniatura-modelo--compacto"
    >
      <header className="miniatura-modelo__cabecalho-compacto">
        <strong>NOME COMPLETO</strong>
        <span>e-mail · telefone · LinkedIn</span>
      </header>
      <div className="miniatura-modelo__coluna-compacta">
        <SecaoMiniatura titulo="FORMAÇÃO · EXPERIÊNCIA" />
        <SecaoMiniatura titulo="PROJETOS ACADÊMICOS" />
        <div className="miniatura-modelo__grade-compacta">
          <SecaoMiniatura titulo="COMPETÊNCIAS" />
          <SecaoMiniatura titulo="IDIOMAS" />
        </div>
        <SecaoMiniatura titulo="DOCUMENTOS" />
      </div>
    </div>
  );
}

/** Representa a lateral de informações e o conteúdo principal do moderno. */
function MiniaturaModerna(): ReactNode {
  return (
    <div
      aria-hidden="true"
      className="miniatura-modelo miniatura-modelo--moderno"
    >
      <header className="miniatura-modelo__cabecalho-moderno">
        <strong>NOME COMPLETO</strong>
        <span>TÍTULO DA VERSÃO</span>
      </header>
      <div className="miniatura-modelo__duas-colunas">
        <aside className="miniatura-modelo__lateral-moderna">
          <SecaoMiniatura titulo="INFORMAÇÕES" />
          <SecaoMiniatura titulo="COMPETÊNCIAS" />
          <SecaoMiniatura titulo="IDIOMAS" />
        </aside>
        <div className="miniatura-modelo__corpo-moderno">
          <SecaoMiniatura titulo="EXPERIÊNCIA PROFISSIONAL" />
          <SecaoMiniatura titulo="PROJETOS ACADÊMICOS" />
          <SecaoMiniatura titulo="FORMAÇÃO ACADÊMICA" />
        </div>
      </div>
    </div>
  );
}

/** Representa a faixa lateral verde e a ênfase em projetos do criativo. */
function MiniaturaCriativa(): ReactNode {
  return (
    <div
      aria-hidden="true"
      className="miniatura-modelo miniatura-modelo--criativo"
    >
      <aside className="miniatura-modelo__lateral-criativa">
        <strong>NOME COMPLETO</strong>
        <span>TÍTULO DA VERSÃO</span>
        <SecaoMiniatura titulo="DADOS DE CONTATO" />
        <SecaoMiniatura titulo="COMPETÊNCIAS" />
        <SecaoMiniatura titulo="IDIOMAS" />
      </aside>
      <div className="miniatura-modelo__corpo-criativo">
        <SecaoMiniatura titulo="PROJETOS ACADÊMICOS" />
        <SecaoMiniatura titulo="EXPERIÊNCIA PROFISSIONAL" />
        <SecaoMiniatura titulo="FORMAÇÃO ACADÊMICA" />
      </div>
    </div>
  );
}

/** Representa o cabeçalho azul e a ordem acadêmica de conteúdos disponíveis. */
function MiniaturaAcademica(): ReactNode {
  return (
    <div
      aria-hidden="true"
      className="miniatura-modelo miniatura-modelo--academico"
    >
      <header className="miniatura-modelo__cabecalho-academico">
        <strong>NOME COMPLETO</strong>
        <span>e-mail · telefone · LinkedIn · Lattes</span>
      </header>
      <div className="miniatura-modelo__coluna-academica">
        <SecaoMiniatura titulo="FORMAÇÃO ACADÊMICA" />
        <SecaoMiniatura titulo="PROJETOS ACADÊMICOS" />
        <SecaoMiniatura titulo="DOCUMENTOS COMPLEMENTARES" />
        <SecaoMiniatura titulo="EXPERIÊNCIA RELEVANTE" />
        <div className="miniatura-modelo__grade-academica">
          <SecaoMiniatura titulo="COMPETÊNCIAS" />
          <SecaoMiniatura titulo="IDIOMAS" />
        </div>
      </div>
    </div>
  );
}

/** Representa a prioridade de formação e projetos para quem inicia a carreira. */
function MiniaturaPrimeiroEmprego(): ReactNode {
  return (
    <div
      aria-hidden="true"
      className="miniatura-modelo miniatura-modelo--primeiro-emprego"
    >
      <header className="miniatura-modelo__cabecalho-primeiro-emprego">
        <span>CURRÍCULO</span>
        <strong>NOME COMPLETO</strong>
        <span>TÍTULO DA VERSÃO · CONTATO</span>
      </header>
      <div className="miniatura-modelo__coluna-primeiro-emprego">
        <SecaoMiniatura titulo="FORMAÇÃO ACADÊMICA" />
        <SecaoMiniatura titulo="PROJETOS ACADÊMICOS" />
        <div className="miniatura-modelo__grade-primeiro-emprego">
          <SecaoMiniatura titulo="COMPETÊNCIAS" />
          <SecaoMiniatura titulo="IDIOMAS" />
        </div>
        <SecaoMiniatura titulo="EXPERIÊNCIA PROFISSIONAL" />
      </div>
    </div>
  );
}
