/* eslint-disable react-refresh/only-export-components */
import type { ReactNode } from "react";

import type {
  DocumentoPreviaCurriculo,
  EstudantePreviaCurriculo,
} from "../../../entities/curriculo";

/**
 * Formata o intervalo de uma formação ou experiência para leitura humana.
 *
 * - O que faz: Produz um texto com início e fim, ou "Atual" quando não há término.
 * - Como faz: Delega cada data à formatação localizada em UTC, sem modificar a prévia recebida.
 * - Qual finalidade atende: Mantém períodos consistentes em todos os novos modelos do catálogo.
 */
export function formatarPeriodo(inicio: string, fim: string | null): string {
  return `${formatarData(inicio)} — ${fim === null ? "Atual" : formatarData(fim)}`;
}

/**
 * Converte uma data ISO em uma data legível para o público brasileiro.
 *
 * - O que faz: Retorna a data no padrão pt-BR.
 * - Como faz: Usa `Intl.DateTimeFormat` em UTC para evitar deslocamento causado pelo fuso local.
 * - Qual finalidade atende: Evita que a visualização de períodos varie entre computadores.
 */
export function formatarData(data: string): string {
  return new Intl.DateTimeFormat("pt-BR", { timeZone: "UTC" }).format(
    new Date(`${data}T00:00:00Z`),
  );
}

/**
 * Produz o texto público de um documento complementar.
 *
 * - O que faz: Combina nome e tipo de arquivo quando o tipo estiver disponível.
 * - Como faz: Usa apenas os metadados presentes na prévia, sem acessar URL ou armazenamento.
 * - Qual finalidade atende: Exibe anexos sem revelar caminhos internos ou inventar links de download.
 */
export function formatarDocumento(documento: DocumentoPreviaCurriculo): string {
  return documento.tipo_arquivo
    ? `${documento.nome_arquivo} (${documento.tipo_arquivo})`
    : documento.nome_arquivo;
}

/** Define as propriedades de uma seção semântica usada pelos modelos do catálogo. */
interface SecaoModeloProps {
  classe: string;
  id: string;
  titulo: string;
  possuiConteudo: boolean;
  children: ReactNode;
}

/**
 * Renderiza uma seção somente quando a coleção correspondente possui itens.
 *
 * - O que faz: Associa um título de segundo nível ao conteúdo de uma seção.
 * - Como faz: Omitindo a seção vazia e conectando `<section>` e `<h2>` por `aria-labelledby`.
 * - Qual finalidade atende: Preserva hierarquia acessível sem apresentar títulos sem conteúdo.
 */
export function SecaoModelo({
  classe,
  id,
  titulo,
  possuiConteudo,
  children,
}: SecaoModeloProps): ReactNode {
  if (!possuiConteudo) {
    return null;
  }

  return (
    <section aria-labelledby={id} className={classe}>
      <h2 id={id}>{titulo}</h2>
      {children}
    </section>
  );
}

/** Define as propriedades da lista de identificação e contatos de um currículo. */
interface ListaContatoProps {
  classe: string;
  estudante: EstudantePreviaCurriculo;
}

/**
 * Exibe os contatos públicos presentes no contrato de prévia.
 *
 * - O que faz: Mostra e-mail e, quando disponíveis, telefone, endereço, LinkedIn e Currículo Lattes.
 * - Como faz: Lê o contato opcional sem criar informações ausentes e aplica proteção nos links externos.
 * - Qual finalidade atende: Reutiliza o mesmo tratamento de dados pessoais em modelos diferentes.
 */
export function ListaContato({
  classe,
  estudante,
}: ListaContatoProps): ReactNode {
  const contato = estudante.contato;
  const linkedin = contato?.linkedin;
  const curriculoLattes = contato?.curriculo_lattes;

  return (
    <ul aria-label="Informações de contato" className={classe}>
      <li>{estudante.email}</li>
      {contato?.telefones.map((telefone) => (
        <li key={telefone}>{telefone}</li>
      ))}
      {contato !== null && <li>{contato.endereco}</li>}
      {linkedin !== null && linkedin !== undefined && (
        <li>
          <a href={linkedin} rel="noopener noreferrer" target="_blank">
            LinkedIn
          </a>
        </li>
      )}
      {curriculoLattes !== null && curriculoLattes !== undefined && (
        <li>
          <a href={curriculoLattes} rel="noopener noreferrer" target="_blank">
            Currículo Lattes
          </a>
        </li>
      )}
    </ul>
  );
}
