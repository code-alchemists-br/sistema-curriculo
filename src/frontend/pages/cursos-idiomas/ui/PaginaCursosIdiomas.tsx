import {
  PaginaCursosCertificacoes,
  type PaginaCursosCertificacoesProps,
} from "../../cursos-certificacoes";

/** Propriedades mantidas para retrocompatibilidade. */
export type PaginaCursosIdiomasProps = PaginaCursosCertificacoesProps;

/**
 * Componente de retrocompatibilidade para a rota anterior.
 *
 * Delega a renderização para a nova PaginaCursosCertificacoes.
 */
export function PaginaCursosIdiomas(props: PaginaCursosIdiomasProps = {}) {
  return <PaginaCursosCertificacoes {...props} />;
}
