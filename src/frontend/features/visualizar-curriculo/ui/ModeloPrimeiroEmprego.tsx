import type { ReactNode } from "react";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import {
  formatarDocumento,
  formatarPeriodo,
  ListaContato,
  SecaoModelo,
} from "./partes-modelo-curriculo";
import "./ModeloPrimeiroEmprego.css";

/** Define os dados recebidos pelo modelo Primeiro emprego. */
export interface ModeloPrimeiroEmpregoProps {
  /** Prévia estruturada que será apresentada sem transformação de conteúdo. */
  previa: PreviaCurriculo;
}

/**
 * Exibe o currículo priorizando formação, projetos e competências antes de experiências.
 *
 * - O que faz: Reorganiza visualmente os itens já selecionados para valorizar evidências relevantes de quem inicia a carreira.
 * - Como faz: Mostra as coleções existentes em ordem própria e omite grupos vazios sem criar objetivos ou experiências fictícias.
 * - Qual finalidade atende: Ajuda estudantes e pessoas em estágio a apresentarem formação e projetos antes de experiência profissional.
 */
export function ModeloPrimeiroEmprego({
  previa,
}: ModeloPrimeiroEmpregoProps): ReactNode {
  const { estudante } = previa;

  return (
    <article
      aria-label={`Currículo de ${estudante.nome}`}
      className="modelo-primeiro-emprego"
    >
      <header className="modelo-primeiro-emprego__cabecalho">
        <p>Currículo</p>
        <h1>{estudante.nome}</h1>
        <strong>{previa.titulo_versao}</strong>
        <ListaContato
          classe="modelo-primeiro-emprego__contato"
          estudante={estudante}
        />
      </header>

      <SecaoModelo
        classe="modelo-primeiro-emprego__secao"
        id="primeiro-emprego-formacao-academica"
        possuiConteudo={previa.formacoes.length > 0}
        titulo="Formação acadêmica"
      >
        <ul className="modelo-primeiro-emprego__lista">
          {previa.formacoes.map((formacao) => (
            <li key={formacao.id}>
              <h3>{formacao.curso}</h3>
              <p>{formacao.instituicao}</p>
              <p>
                {formacao.nivel} · {formacao.status} ·{" "}
                {formatarPeriodo(formacao.inicio, formacao.fim)}
              </p>
            </li>
          ))}
        </ul>
      </SecaoModelo>

      <SecaoModelo
        classe="modelo-primeiro-emprego__secao"
        id="primeiro-emprego-projetos"
        possuiConteudo={previa.projetos.length > 0}
        titulo="Projetos acadêmicos"
      >
        <ul className="modelo-primeiro-emprego__lista">
          {previa.projetos.map((projeto) => (
            <li key={projeto.id}>
              <h3>{projeto.titulo}</h3>
              <p>{projeto.descricao}</p>
              {projeto.tecnologias && <p>Tecnologias: {projeto.tecnologias}</p>}
            </li>
          ))}
        </ul>
      </SecaoModelo>

      <div className="modelo-primeiro-emprego__grade">
        <SecaoModelo
          classe="modelo-primeiro-emprego__secao"
          id="primeiro-emprego-competencias"
          possuiConteudo={previa.competencias.length > 0}
          titulo="Competências"
        >
          <ul className="modelo-primeiro-emprego__lista-curta">
            {previa.competencias.map((competencia) => (
              <li key={competencia.id}>
                {competencia.descricao}
                {competencia.nivel && ` — ${competencia.nivel}`}
              </li>
            ))}
          </ul>
        </SecaoModelo>

        <SecaoModelo
          classe="modelo-primeiro-emprego__secao"
          id="primeiro-emprego-idiomas"
          possuiConteudo={previa.idiomas.length > 0}
          titulo="Idiomas"
        >
          <ul className="modelo-primeiro-emprego__lista-curta">
            {previa.idiomas.map((idioma) => (
              <li key={idioma.id}>
                {idioma.idioma}
                {idioma.nivel && ` — ${idioma.nivel}`}
              </li>
            ))}
          </ul>
        </SecaoModelo>
      </div>

      <SecaoModelo
        classe="modelo-primeiro-emprego__secao"
        id="primeiro-emprego-documentos"
        possuiConteudo={previa.documentos.length > 0}
        titulo="Documentos complementares"
      >
        <ul className="modelo-primeiro-emprego__lista-curta">
          {previa.documentos.map((documento) => (
            <li key={documento.id}>{formatarDocumento(documento)}</li>
          ))}
        </ul>
      </SecaoModelo>

      <SecaoModelo
        classe="modelo-primeiro-emprego__secao"
        id="primeiro-emprego-experiencia-profissional"
        possuiConteudo={previa.experiencias.length > 0}
        titulo="Experiência profissional"
      >
        <ul className="modelo-primeiro-emprego__lista">
          {previa.experiencias.map((experiencia) => (
            <li key={experiencia.id}>
              <h3>{experiencia.cargo}</h3>
              <p>
                {experiencia.empresa} ·{" "}
                {formatarPeriodo(experiencia.inicio, experiencia.fim)}
              </p>
              <p>{experiencia.descricao}</p>
            </li>
          ))}
        </ul>
      </SecaoModelo>
    </article>
  );
}
