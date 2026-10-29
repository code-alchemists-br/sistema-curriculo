import type { ReactNode } from "react";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import {
  formatarDocumento,
  formatarPeriodo,
  ListaContato,
  SecaoModelo,
} from "./partes-modelo-curriculo";
import "./ModeloCriativo.css";

/** Define os dados recebidos pelo modelo Criativo. */
export interface ModeloCriativoProps {
  /** Dados públicos e estruturados da prévia de currículo. */
  previa: PreviaCurriculo;
}

/**
 * Exibe uma prévia visualmente expressiva, destacando identidade, competências e projetos.
 *
 * - O que faz: Organiza contatos e capacidades na lateral e prioriza projetos no conteúdo principal.
 * - Como faz: Reaproveita o contrato comum de prévia, sem incluir fotografia, resumo ou informações que não existam no domínio.
 * - Qual finalidade atende: Oferece apresentação diferenciada para áreas criativas, comunicação e portfólio.
 */
export function ModeloCriativo({ previa }: ModeloCriativoProps): ReactNode {
  const { estudante } = previa;

  return (
    <article
      aria-label={`Currículo de ${estudante.nome}`}
      className="modelo-criativo"
    >
      <aside className="modelo-criativo__lateral">
        <header className="modelo-criativo__cabecalho-lateral">
          <h1>{estudante.nome}</h1>
          <p>{previa.titulo_versao}</p>
        </header>

        <section
          aria-labelledby="criativo-dados-contato"
          className="modelo-criativo__secao-lateral"
        >
          <h2 id="criativo-dados-contato">Dados de contato</h2>
          <ListaContato
            classe="modelo-criativo__contato"
            estudante={estudante}
          />
        </section>

        <SecaoModelo
          classe="modelo-criativo__secao-lateral"
          id="criativo-competencias"
          possuiConteudo={previa.competencias.length > 0}
          titulo="Competências"
        >
          <ul className="modelo-criativo__lista-lateral">
            {previa.competencias.map((competencia) => (
              <li key={competencia.id}>
                <strong>{competencia.descricao}</strong>
                {competencia.nivel && <span>{competencia.nivel}</span>}
              </li>
            ))}
          </ul>
        </SecaoModelo>

        <SecaoModelo
          classe="modelo-criativo__secao-lateral"
          id="criativo-idiomas"
          possuiConteudo={previa.idiomas.length > 0}
          titulo="Idiomas"
        >
          <ul className="modelo-criativo__lista-lateral">
            {previa.idiomas.map((idioma) => (
              <li key={idioma.id}>
                <strong>{idioma.idioma}</strong>
                {idioma.nivel && <span>{idioma.nivel}</span>}
              </li>
            ))}
          </ul>
        </SecaoModelo>
      </aside>

      <div className="modelo-criativo__conteudo">
        <SecaoModelo
          classe="modelo-criativo__secao"
          id="criativo-projetos"
          possuiConteudo={previa.projetos.length > 0}
          titulo="Projetos acadêmicos"
        >
          <ul className="modelo-criativo__lista-principal">
            {previa.projetos.map((projeto) => (
              <li key={projeto.id}>
                <h3>{projeto.titulo}</h3>
                <p>{projeto.descricao}</p>
                {projeto.tecnologias && (
                  <p>Tecnologias: {projeto.tecnologias}</p>
                )}
              </li>
            ))}
          </ul>
        </SecaoModelo>

        <SecaoModelo
          classe="modelo-criativo__secao"
          id="criativo-experiencia"
          possuiConteudo={previa.experiencias.length > 0}
          titulo="Experiência profissional"
        >
          <ul className="modelo-criativo__lista-principal">
            {previa.experiencias.map((experiencia) => (
              <li key={experiencia.id}>
                <p className="modelo-criativo__periodo">
                  {formatarPeriodo(experiencia.inicio, experiencia.fim)}
                </p>
                <h3>{experiencia.cargo}</h3>
                <p>{experiencia.empresa}</p>
                <p>{experiencia.descricao}</p>
              </li>
            ))}
          </ul>
        </SecaoModelo>

        <SecaoModelo
          classe="modelo-criativo__secao"
          id="criativo-formacao"
          possuiConteudo={previa.formacoes.length > 0}
          titulo="Formação acadêmica"
        >
          <ul className="modelo-criativo__lista-principal">
            {previa.formacoes.map((formacao) => (
              <li key={formacao.id}>
                <p className="modelo-criativo__periodo">
                  {formatarPeriodo(formacao.inicio, formacao.fim)}
                </p>
                <h3>{formacao.curso}</h3>
                <p>{formacao.instituicao}</p>
                <p>
                  {formacao.nivel} · {formacao.status}
                </p>
              </li>
            ))}
          </ul>
        </SecaoModelo>

        <SecaoModelo
          classe="modelo-criativo__secao"
          id="criativo-documentos"
          possuiConteudo={previa.documentos.length > 0}
          titulo="Documentos complementares"
        >
          <ul className="modelo-criativo__documentos">
            {previa.documentos.map((documento) => (
              <li key={documento.id}>{formatarDocumento(documento)}</li>
            ))}
          </ul>
        </SecaoModelo>
      </div>
    </article>
  );
}
