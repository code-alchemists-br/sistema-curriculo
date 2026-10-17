import type { ReactNode } from "react";

import type {
  DocumentoPreviaCurriculo,
  PreviaCurriculo,
} from "../../../entities/curriculo";
import "./ModeloClassico.css";

/**
 * Propriedades recebidas pelo componente ModeloClassico.
 */
export interface ModeloClassicoProps {
  /** Dados estruturados do currículo para visualização. */
  previa: PreviaCurriculo;
}

/**
 * Apresenta uma versão de currículo em layout clássico e tradicional.
 *
 * - O que faz: Renderiza todas as seções e dados do currículo do estudante em uma organização tradicional, legível e sóbria.
 * - Como faz: Mapeia o contrato `PreviaCurriculo` em elementos HTML5 semânticos (`article`, `header`, `section`, `ul`, `li`, `p`), sem recorrer a frameworks externos ou dependências de fornecedor.
 * - Qual finalidade atende: Oferece aos estudantes uma alternativa de layout clássico profissional, com excelente legibilidade para recrutadores, impressão adequada e acessibilidade nativa.
 *
 * @param props Propriedades contendo o objeto de prévia do currículo.
 * @returns Elemento JSX representando o currículo formatado no modelo clássico.
 */
export function ModeloClassico({ previa }: ModeloClassicoProps) {
  const { estudante } = previa;
  const contato = estudante.contato;

  return (
    <article
      aria-label={`Currículo de ${estudante.nome}`}
      className="modelo-classico"
    >
      <header className="modelo-classico__cabecalho">
        <h1 className="modelo-classico__nome">{estudante.nome}</h1>
        <ul
          aria-label="Informações de contato"
          className="modelo-classico__contato"
        >
          <li>{estudante.email}</li>
          {contato?.telefones.map((telefone) => (
            <li key={telefone}>{telefone}</li>
          ))}
          {contato?.endereco && <li>{contato.endereco}</li>}
          {contato?.linkedin && (
            <li>
              <a
                href={contato.linkedin}
                rel="noopener noreferrer"
                target="_blank"
              >
                LinkedIn
              </a>
            </li>
          )}
          {contato?.curriculo_lattes && (
            <li>
              <a
                href={contato.curriculo_lattes}
                rel="noopener noreferrer"
                target="_blank"
              >
                Currículo Lattes
              </a>
            </li>
          )}
        </ul>
      </header>

      <SecaoClassica
        possuiConteudo={previa.formacoes.length > 0}
        slug="formacao-academica"
        titulo="Formação acadêmica"
      >
        <ul className="modelo-classico__lista">
          {previa.formacoes.map((formacao) => (
            <li className="modelo-classico__item" key={formacao.id}>
              <div className="modelo-classico__linha-cabecalho">
                <strong className="modelo-classico__titulo-item">
                  {formacao.curso}
                </strong>
                <span className="modelo-classico__periodo">
                  {formatarPeriodo(formacao.inicio, formacao.fim)}
                </span>
              </div>
              <div className="modelo-classico__linha-subtitulo">
                <span>{formacao.instituicao}</span>
                <span className="modelo-classico__separador">•</span>
                <span>
                  {formacao.nivel} — {formacao.status}
                </span>
              </div>
            </li>
          ))}
        </ul>
      </SecaoClassica>

      <SecaoClassica
        possuiConteudo={previa.experiencias.length > 0}
        slug="experiencia-profissional"
        titulo="Experiência profissional"
      >
        <ul className="modelo-classico__lista">
          {previa.experiencias.map((experiencia) => (
            <li className="modelo-classico__item" key={experiencia.id}>
              <div className="modelo-classico__linha-cabecalho">
                <strong className="modelo-classico__titulo-item">
                  {experiencia.cargo}
                </strong>
                <span className="modelo-classico__periodo">
                  {formatarPeriodo(experiencia.inicio, experiencia.fim)}
                </span>
              </div>
              <div className="modelo-classico__linha-subtitulo">
                <span>{experiencia.empresa}</span>
              </div>
              <p className="modelo-classico__descricao">
                {experiencia.descricao}
              </p>
            </li>
          ))}
        </ul>
      </SecaoClassica>

      <SecaoClassica
        possuiConteudo={previa.projetos.length > 0}
        slug="projetos-academicos"
        titulo="Projetos acadêmicos"
      >
        <ul className="modelo-classico__lista">
          {previa.projetos.map((projeto) => (
            <li className="modelo-classico__item" key={projeto.id}>
              <strong className="modelo-classico__titulo-item">
                {projeto.titulo}
              </strong>
              <p className="modelo-classico__descricao">{projeto.descricao}</p>
              {projeto.tecnologias && (
                <p className="modelo-classico__tecnologias">
                  <strong>Tecnologias:</strong> {projeto.tecnologias}
                </p>
              )}
            </li>
          ))}
        </ul>
      </SecaoClassica>

      <SecaoClassica
        possuiConteudo={previa.competencias.length > 0}
        slug="competencias"
        titulo="Competências"
      >
        <ul className="modelo-classico__grid-duas-colunas">
          {previa.competencias.map((competencia) => (
            <li key={competencia.id}>
              <strong>{competencia.descricao}</strong>
              {competencia.nivel && <span> ({competencia.nivel})</span>}
            </li>
          ))}
        </ul>
      </SecaoClassica>

      <SecaoClassica
        possuiConteudo={previa.idiomas.length > 0}
        slug="idiomas"
        titulo="Idiomas"
      >
        <ul className="modelo-classico__grid-duas-colunas">
          {previa.idiomas.map((idioma) => (
            <li key={idioma.id}>
              <strong>{idioma.idioma}</strong>
              {idioma.nivel && <span> — {idioma.nivel}</span>}
            </li>
          ))}
        </ul>
      </SecaoClassica>

      <SecaoClassica
        possuiConteudo={previa.documentos.length > 0}
        slug="documentos-complementares"
        titulo="Documentos complementares"
      >
        <ul className="modelo-classico__lista-documentos">
          {previa.documentos.map((documento) => (
            <li key={documento.id}>{formatarDocumento(documento)}</li>
          ))}
        </ul>
      </SecaoClassica>
    </article>
  );
}

/**
 * Propriedades do componente auxiliar SecaoClassica.
 */
interface SecaoClassicaProps {
  titulo: string;
  slug: string;
  possuiConteudo: boolean;
  children: ReactNode;
}

/**
 * Seção delimitada do currículo clássico com cabeçalho semântico e separador visual sóbrio.
 *
 * - O que faz: Renderiza o título da seção e seus filhos quando houver conteúdo disponível.
 * - Como faz: Utiliza a tag `<section>` associada a um `<h2>` com `aria-labelledby`, omitindo a seção caso vazia.
 * - Qual finalidade atende: Garante hierarquia semântica acessível e visual clássico bem segmentado.
 */
function SecaoClassica({
  titulo,
  slug,
  possuiConteudo,
  children,
}: SecaoClassicaProps) {
  if (!possuiConteudo) {
    return null;
  }

  const idTitulo = `secao-classica-${slug}`;

  return (
    <section aria-labelledby={idTitulo} className="modelo-classico__secao">
      <h2 className="modelo-classico__titulo-secao" id={idTitulo}>
        {titulo}
      </h2>
      {children}
    </section>
  );
}

/**
 * Formata o período com datas de início e término no padrão legível pt-BR.
 *
 * - O que faz: Produz texto no formato "Início — Fim" ou "Início — —" para períodos sem data final.
 * - Como faz: Converte strings de data ISO para datas formatadas via `formatarData`.
 * - Qual finalidade atende: Exibe períodos de experiência e formação de modo legível para o usuário final.
 */
function formatarPeriodo(inicio: string, fim: string | null): string {
  return `${formatarData(inicio)} — ${fim ? formatarData(fim) : "Atual"}`;
}

/**
 * Converte data ISO (AAAA-MM-DD) para formato legível brasileiro com mês e ano ou data completa.
 *
 * - O que faz: Formata uma data no fuso UTC para "dd/mm/aaaa".
 * - Como faz: Instancia objeto Date e aplica `Intl.DateTimeFormat` com localização pt-BR.
 * - Qual finalidade atende: Evita discrepâncias de fuso horário local e padroniza a exibição de datas.
 */
function formatarData(data: string): string {
  return new Intl.DateTimeFormat("pt-BR", { timeZone: "UTC" }).format(
    new Date(`${data}T00:00:00Z`),
  );
}

/**
 * Produz a exibição do documento complementar preservando a privacidade da URL de armazenamento.
 *
 * - O que faz: Retorna o nome do arquivo anexado acompanhado de seu tipo MIME, quando disponível.
 * - Como faz: Concatena o nome e o tipo do arquivo em formato legível.
 * - Qual finalidade atende: Apresenta certificados e anexos de forma informativa sem expor rotas internas.
 */
function formatarDocumento(documento: DocumentoPreviaCurriculo): string {
  return documento.tipo_arquivo
    ? `${documento.nome_arquivo} (${documento.tipo_arquivo})`
    : documento.nome_arquivo;
}
