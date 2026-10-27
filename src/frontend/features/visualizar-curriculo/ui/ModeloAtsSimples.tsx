import type { ReactNode } from "react";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import {
  formatarDocumento,
  formatarPeriodo,
  ListaContato,
  SecaoModelo,
} from "./partes-modelo-curriculo";
import "./ModeloAtsSimples.css";

/** Define os dados recebidos pelo modelo ATS simples. */
export interface ModeloAtsSimplesProps {
  /** Dados estruturados da versão de currículo que serão apenas apresentados. */
  previa: PreviaCurriculo;
}

/**
 * Exibe a prévia em uma estrutura textual de coluna única compatível com leitura ATS.
 *
 * - O que faz: Apresenta identificação e seções com títulos claros, sem barras, cartões ou elementos decorativos gráficos.
 * - Como faz: Mapeia exclusivamente o contrato `PreviaCurriculo` para HTML semântico e omite coleções vazias.
 * - Qual finalidade atende: Oferece uma alternativa de leitura direta para candidaturas em plataformas de recrutamento.
 */
export function ModeloAtsSimples({ previa }: ModeloAtsSimplesProps): ReactNode {
  const { estudante } = previa;

  return (
    <article
      aria-label={`Currículo de ${estudante.nome}`}
      className="modelo-ats-simples"
    >
      <header className="modelo-ats-simples__cabecalho">
        <h1>{estudante.nome}</h1>
        <p>{previa.titulo_versao}</p>
        <ListaContato
          classe="modelo-ats-simples__contato"
          estudante={estudante}
        />
      </header>

      <SecaoModelo
        classe="modelo-ats-simples__secao"
        id="ats-experiencia-profissional"
        possuiConteudo={previa.experiencias.length > 0}
        titulo="Experiência profissional"
      >
        <ul className="modelo-ats-simples__lista">
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

      <SecaoModelo
        classe="modelo-ats-simples__secao"
        id="ats-formacao-academica"
        possuiConteudo={previa.formacoes.length > 0}
        titulo="Formação acadêmica"
      >
        <ul className="modelo-ats-simples__lista">
          {previa.formacoes.map((formacao) => (
            <li key={formacao.id}>
              <h3>{formacao.curso}</h3>
              <p>
                {formacao.instituicao} · {formacao.nivel} · {formacao.status}
              </p>
              <p>{formatarPeriodo(formacao.inicio, formacao.fim)}</p>
            </li>
          ))}
        </ul>
      </SecaoModelo>

      <SecaoModelo
        classe="modelo-ats-simples__secao"
        id="ats-projetos-academicos"
        possuiConteudo={previa.projetos.length > 0}
        titulo="Projetos acadêmicos"
      >
        <ul className="modelo-ats-simples__lista">
          {previa.projetos.map((projeto) => (
            <li key={projeto.id}>
              <h3>{projeto.titulo}</h3>
              <p>{projeto.descricao}</p>
              {projeto.tecnologias && <p>Tecnologias: {projeto.tecnologias}</p>}
            </li>
          ))}
        </ul>
      </SecaoModelo>

      <SecaoModelo
        classe="modelo-ats-simples__secao"
        id="ats-competencias"
        possuiConteudo={previa.competencias.length > 0}
        titulo="Competências"
      >
        <ul className="modelo-ats-simples__lista-textual">
          {previa.competencias.map((competencia) => (
            <li key={competencia.id}>
              {competencia.descricao}
              {competencia.nivel && ` — ${competencia.nivel}`}
            </li>
          ))}
        </ul>
      </SecaoModelo>

      <SecaoModelo
        classe="modelo-ats-simples__secao"
        id="ats-idiomas"
        possuiConteudo={previa.idiomas.length > 0}
        titulo="Idiomas"
      >
        <ul className="modelo-ats-simples__lista-textual">
          {previa.idiomas.map((idioma) => (
            <li key={idioma.id}>
              {idioma.idioma}
              {idioma.nivel && ` — ${idioma.nivel}`}
            </li>
          ))}
        </ul>
      </SecaoModelo>

      <SecaoModelo
        classe="modelo-ats-simples__secao"
        id="ats-documentos-complementares"
        possuiConteudo={previa.documentos.length > 0}
        titulo="Documentos complementares"
      >
        <ul className="modelo-ats-simples__lista-textual">
          {previa.documentos.map((documento) => (
            <li key={documento.id}>{formatarDocumento(documento)}</li>
          ))}
        </ul>
      </SecaoModelo>
    </article>
  );
}
