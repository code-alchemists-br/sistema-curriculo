import type { ReactNode } from "react";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import {
  formatarDocumento,
  formatarPeriodo,
  ListaContato,
  SecaoModelo,
} from "./partes-modelo-curriculo";
import "./ModeloAcademico.css";

/** Define os dados recebidos pelo modelo Acadêmico. */
export interface ModeloAcademicoProps {
  /** Prévia estruturada e já filtrada pelos itens selecionados da versão. */
  previa: PreviaCurriculo;
}

/**
 * Exibe uma prévia acadêmica com formação e projetos antes da experiência profissional.
 *
 * - O que faz: Organiza as seções disponíveis conforme a prioridade do currículo acadêmico.
 * - Como faz: Mostra somente dados existentes no contrato e omite seções acadêmicas que o domínio ainda não representa.
 * - Qual finalidade atende: Apoia candidaturas acadêmicas sem inventar publicações, linhas de pesquisa ou atividades de docência.
 */
export function ModeloAcademico({ previa }: ModeloAcademicoProps): ReactNode {
  const { estudante } = previa;

  return (
    <article
      aria-label={`Currículo de ${estudante.nome}`}
      className="modelo-academico"
    >
      <header className="modelo-academico__cabecalho">
        <div>
          <h1>{estudante.nome}</h1>
          <p>{previa.titulo_versao}</p>
        </div>
        <ListaContato
          classe="modelo-academico__contato"
          estudante={estudante}
        />
      </header>

      <SecaoModelo
        classe="modelo-academico__secao"
        id="academico-formacao-academica"
        possuiConteudo={previa.formacoes.length > 0}
        titulo="Formação acadêmica"
      >
        <ul className="modelo-academico__lista">
          {previa.formacoes.map((formacao) => (
            <li key={formacao.id}>
              <div>
                <h3>{formacao.curso}</h3>
                <p>{formacao.instituicao}</p>
                <p>
                  {formacao.nivel} · {formacao.status}
                </p>
              </div>
              <p className="modelo-academico__periodo">
                {formatarPeriodo(formacao.inicio, formacao.fim)}
              </p>
            </li>
          ))}
        </ul>
      </SecaoModelo>

      <SecaoModelo
        classe="modelo-academico__secao"
        id="academico-projetos"
        possuiConteudo={previa.projetos.length > 0}
        titulo="Projetos acadêmicos"
      >
        <ul className="modelo-academico__lista">
          {previa.projetos.map((projeto) => (
            <li key={projeto.id}>
              <div>
                <h3>{projeto.titulo}</h3>
                <p>{projeto.descricao}</p>
                {projeto.tecnologias && (
                  <p>Tecnologias: {projeto.tecnologias}</p>
                )}
              </div>
            </li>
          ))}
        </ul>
      </SecaoModelo>

      <SecaoModelo
        classe="modelo-academico__secao"
        id="academico-documentos"
        possuiConteudo={previa.documentos.length > 0}
        titulo="Documentos complementares"
      >
        <ul className="modelo-academico__documentos">
          {previa.documentos.map((documento) => (
            <li key={documento.id}>{formatarDocumento(documento)}</li>
          ))}
        </ul>
      </SecaoModelo>

      <SecaoModelo
        classe="modelo-academico__secao"
        id="academico-experiencia-profissional"
        possuiConteudo={previa.experiencias.length > 0}
        titulo="Experiência profissional relevante"
      >
        <ul className="modelo-academico__lista">
          {previa.experiencias.map((experiencia) => (
            <li key={experiencia.id}>
              <div>
                <h3>{experiencia.cargo}</h3>
                <p>{experiencia.empresa}</p>
                <p>{experiencia.descricao}</p>
              </div>
              <p className="modelo-academico__periodo">
                {formatarPeriodo(experiencia.inicio, experiencia.fim)}
              </p>
            </li>
          ))}
        </ul>
      </SecaoModelo>

      <div className="modelo-academico__grade-final">
        <SecaoModelo
          classe="modelo-academico__secao"
          id="academico-competencias"
          possuiConteudo={previa.competencias.length > 0}
          titulo="Competências"
        >
          <ul className="modelo-academico__lista-curta">
            {previa.competencias.map((competencia) => (
              <li key={competencia.id}>
                {competencia.descricao}
                {competencia.nivel && ` — ${competencia.nivel}`}
              </li>
            ))}
          </ul>
        </SecaoModelo>

        <SecaoModelo
          classe="modelo-academico__secao"
          id="academico-idiomas"
          possuiConteudo={previa.idiomas.length > 0}
          titulo="Idiomas"
        >
          <ul className="modelo-academico__lista-curta">
            {previa.idiomas.map((idioma) => (
              <li key={idioma.id}>
                {idioma.idioma}
                {idioma.nivel && ` — ${idioma.nivel}`}
              </li>
            ))}
          </ul>
        </SecaoModelo>
      </div>
    </article>
  );
}
