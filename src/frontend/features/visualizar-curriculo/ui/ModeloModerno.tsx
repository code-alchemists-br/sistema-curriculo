import type { ReactNode } from "react";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import {
  formatarDocumento,
  formatarPeriodo,
  ListaContato,
  SecaoModelo,
} from "./partes-modelo-curriculo";
import "./ModeloModerno.css";

/** Define os dados recebidos pelo modelo Moderno. */
export interface ModeloModernoProps {
  /** Prévia estruturada do currículo, compartilhada por todos os modelos. */
  previa: PreviaCurriculo;
}

/**
 * Exibe uma prévia contemporânea com equilíbrio entre competências, projetos e experiências.
 *
 * - O que faz: Distribui informações de apoio na lateral e conteúdo profissional no corpo principal.
 * - Como faz: Usa os mesmos dados de entrada dos demais modelos e aplica somente composição visual responsiva.
 * - Qual finalidade atende: Atende perfis de tecnologia, produto, marketing e negócios sem criar um contrato próprio.
 */
export function ModeloModerno({ previa }: ModeloModernoProps): ReactNode {
  const { estudante } = previa;

  return (
    <article
      aria-label={`Currículo de ${estudante.nome}`}
      className="modelo-moderno"
    >
      <header className="modelo-moderno__cabecalho">
        <h1>{estudante.nome}</h1>
        <p>{previa.titulo_versao}</p>
      </header>

      <div className="modelo-moderno__estrutura">
        <aside className="modelo-moderno__lateral">
          <section
            aria-labelledby="moderno-informacoes"
            className="modelo-moderno__secao-lateral"
          >
            <h2 id="moderno-informacoes">Informações</h2>
            <ListaContato
              classe="modelo-moderno__contato"
              estudante={estudante}
            />
          </section>

          <SecaoModelo
            classe="modelo-moderno__secao-lateral"
            id="moderno-competencias"
            possuiConteudo={previa.competencias.length > 0}
            titulo="Competências"
          >
            <ul className="modelo-moderno__lista-lateral">
              {previa.competencias.map((competencia) => (
                <li key={competencia.id}>
                  <strong>{competencia.descricao}</strong>
                  {competencia.nivel && <span>{competencia.nivel}</span>}
                </li>
              ))}
            </ul>
          </SecaoModelo>

          <SecaoModelo
            classe="modelo-moderno__secao-lateral"
            id="moderno-idiomas"
            possuiConteudo={previa.idiomas.length > 0}
            titulo="Idiomas"
          >
            <ul className="modelo-moderno__lista-lateral">
              {previa.idiomas.map((idioma) => (
                <li key={idioma.id}>
                  <strong>{idioma.idioma}</strong>
                  {idioma.nivel && <span>{idioma.nivel}</span>}
                </li>
              ))}
            </ul>
          </SecaoModelo>
        </aside>

        <div className="modelo-moderno__conteudo">
          <SecaoModelo
            classe="modelo-moderno__secao"
            id="moderno-experiencia"
            possuiConteudo={previa.experiencias.length > 0}
            titulo="Experiência profissional"
          >
            <ul className="modelo-moderno__lista-principal">
              {previa.experiencias.map((experiencia) => (
                <li key={experiencia.id}>
                  <div>
                    <h3>{experiencia.cargo}</h3>
                    <p>{experiencia.empresa}</p>
                  </div>
                  <p className="modelo-moderno__periodo">
                    {formatarPeriodo(experiencia.inicio, experiencia.fim)}
                  </p>
                  <p className="modelo-moderno__descricao">
                    {experiencia.descricao}
                  </p>
                </li>
              ))}
            </ul>
          </SecaoModelo>

          <SecaoModelo
            classe="modelo-moderno__secao"
            id="moderno-projetos"
            possuiConteudo={previa.projetos.length > 0}
            titulo="Projetos acadêmicos"
          >
            <ul className="modelo-moderno__lista-principal modelo-moderno__lista-principal--projetos">
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
            classe="modelo-moderno__secao"
            id="moderno-formacao"
            possuiConteudo={previa.formacoes.length > 0}
            titulo="Formação acadêmica"
          >
            <ul className="modelo-moderno__lista-principal">
              {previa.formacoes.map((formacao) => (
                <li key={formacao.id}>
                  <div>
                    <h3>{formacao.curso}</h3>
                    <p>{formacao.instituicao}</p>
                  </div>
                  <p className="modelo-moderno__periodo">
                    {formatarPeriodo(formacao.inicio, formacao.fim)}
                  </p>
                  <p className="modelo-moderno__descricao">
                    {formacao.nivel} · {formacao.status}
                  </p>
                </li>
              ))}
            </ul>
          </SecaoModelo>

          <SecaoModelo
            classe="modelo-moderno__secao"
            id="moderno-documentos"
            possuiConteudo={previa.documentos.length > 0}
            titulo="Documentos complementares"
          >
            <ul className="modelo-moderno__documentos">
              {previa.documentos.map((documento) => (
                <li key={documento.id}>{formatarDocumento(documento)}</li>
              ))}
            </ul>
          </SecaoModelo>
        </div>
      </div>
    </article>
  );
}
