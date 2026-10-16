import type { ReactNode } from "react";

import type {
  DocumentoPreviaCurriculo,
  PreviaCurriculo,
} from "../../../entities/curriculo";
import "./ModeloCompacto.css";

/** Define os dados recebidos pelo modelo compacto. */
export interface ModeloCompactoProps {
  previa: PreviaCurriculo;
}

/**
 * Apresenta uma versão de currículo em organização visual compacta.
 *
 * O componente recebe a prévia pronta e somente a transforma em elementos
 * semânticos de interface. Ele existe para oferecer uma alternativa de layout
 * sem alterar dados, chamar serviços ou criar um contrato próprio.
 */
export function ModeloCompacto({ previa }: ModeloCompactoProps) {
  const { estudante } = previa;
  const contato = estudante.contato;

  return (
    <article
      aria-label={`Currículo de ${estudante.nome}`}
      className="modelo-compacto"
    >
      <header className="modelo-compacto__cabecalho">
        <h1>{estudante.nome}</h1>
        <ul
          aria-label="Informações de contato"
          className="modelo-compacto__contato"
        >
          <li>{estudante.email}</li>
          {contato?.telefones.map((telefone) => (
            <li key={telefone}>{telefone}</li>
          ))}
          {contato?.endereco && <li>{contato.endereco}</li>}
          {contato?.linkedin && (
            <li>
              <a href={contato.linkedin}>{contato.linkedin}</a>
            </li>
          )}
          {contato?.curriculo_lattes && (
            <li>
              <a href={contato.curriculo_lattes}>{contato.curriculo_lattes}</a>
            </li>
          )}
        </ul>
      </header>

      <Secao
        titulo="Formação acadêmica"
        possuiConteudo={previa.formacoes.length > 0}
      >
        <ul className="modelo-compacto__lista">
          {previa.formacoes.map((formacao) => (
            <li key={formacao.id}>
              <strong>{formacao.curso}</strong>
              <span>{formacao.instituicao}</span>
              <span>
                {formacao.nivel} · {formacao.status}
              </span>
              <span>{formatarPeriodo(formacao.inicio, formacao.fim)}</span>
            </li>
          ))}
        </ul>
      </Secao>

      <Secao
        titulo="Experiência profissional"
        possuiConteudo={previa.experiencias.length > 0}
      >
        <ul className="modelo-compacto__lista">
          {previa.experiencias.map((experiencia) => (
            <li key={experiencia.id}>
              <strong>{experiencia.cargo}</strong>
              <span>{experiencia.empresa}</span>
              <span>
                {formatarPeriodo(experiencia.inicio, experiencia.fim)}
              </span>
              <p>{experiencia.descricao}</p>
            </li>
          ))}
        </ul>
      </Secao>

      <Secao
        titulo="Projetos acadêmicos"
        possuiConteudo={previa.projetos.length > 0}
      >
        <ul className="modelo-compacto__lista">
          {previa.projetos.map((projeto) => (
            <li key={projeto.id}>
              <strong>{projeto.titulo}</strong>
              <p>{projeto.descricao}</p>
              {projeto.tecnologias && <span>{projeto.tecnologias}</span>}
            </li>
          ))}
        </ul>
      </Secao>

      <Secao
        titulo="Competências"
        possuiConteudo={previa.competencias.length > 0}
      >
        <ul className="modelo-compacto__itens-inline">
          {previa.competencias.map((competencia) => (
            <li key={competencia.id}>
              {competencia.descricao}
              {competencia.nivel && ` — ${competencia.nivel}`}
            </li>
          ))}
        </ul>
      </Secao>

      <Secao titulo="Idiomas" possuiConteudo={previa.idiomas.length > 0}>
        <ul className="modelo-compacto__itens-inline">
          {previa.idiomas.map((idioma) => (
            <li key={idioma.id}>
              {idioma.idioma}
              {idioma.nivel && ` — ${idioma.nivel}`}
            </li>
          ))}
        </ul>
      </Secao>

      <Secao
        titulo="Documentos complementares"
        possuiConteudo={previa.documentos.length > 0}
      >
        <ul className="modelo-compacto__itens-inline">
          {previa.documentos.map((documento) => (
            <li key={documento.id}>{formatarDocumento(documento)}</li>
          ))}
        </ul>
      </Secao>
    </article>
  );
}

/** Agrupa uma seção somente quando a prévia possui conteúdo para ela. */
function Secao({
  titulo,
  possuiConteudo,
  children,
}: {
  titulo: string;
  possuiConteudo: boolean;
  children: ReactNode;
}) {
  if (!possuiConteudo) return null;

  return (
    <section
      aria-labelledby={`secao-${titulo}`}
      className="modelo-compacto__secao"
    >
      <h2 id={`secao-${titulo}`}>{titulo}</h2>
      {children}
    </section>
  );
}

/** Formata o período sem alterar as datas recebidas da API. */
function formatarPeriodo(inicio: string, fim: string | null): string {
  return `${formatarData(inicio)} — ${fim ? formatarData(fim) : "—"}`;
}

/** Converte uma data ISO da API para uma forma legível em pt-BR. */
function formatarData(data: string): string {
  return new Intl.DateTimeFormat("pt-BR", { timeZone: "UTC" }).format(
    new Date(`${data}T00:00:00Z`),
  );
}

/** Produz o texto público de um documento sem expor sua URL de armazenamento. */
function formatarDocumento(documento: DocumentoPreviaCurriculo): string {
  return documento.tipo_arquivo
    ? `${documento.nome_arquivo} (${documento.tipo_arquivo})`
    : documento.nome_arquivo;
}
