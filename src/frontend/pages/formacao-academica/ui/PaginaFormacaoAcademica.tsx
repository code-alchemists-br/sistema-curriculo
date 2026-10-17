import {
  criarClienteFormacaoAcademicaIndisponivel,
  FormularioFormacaoAcademica,
  type ClienteFormacaoAcademica,
} from "../../../features/cadastrar-formacao-academica";

/** Define a dependência opcional usada pela página de formação acadêmica. */
export interface PaginaFormacaoAcademicaProps {
  cliente?: ClienteFormacaoAcademica;
}

/**
 * Compõe a tela de cadastro de formação acadêmica.
 *
 * A página fornece um cliente indisponível enquanto não houver integração e
 * delega o formulário à feature por sua API pública. Ela existe para oferecer
 * a tela sem acoplar a página a HTTP, sessão ou navegação ainda não definidos.
 */
export function PaginaFormacaoAcademica({
  cliente,
}: PaginaFormacaoAcademicaProps) {
  return (
    <main className="app-shell">
      <section aria-labelledby="titulo-formacao" className="app-shell__content">
        <p className="eyebrow">Currículo</p>
        <h1 id="titulo-formacao">Formação acadêmica</h1>
        <p>
          Informe uma formação por vez para organizar as informações do seu
          currículo.
        </p>
        <FormularioFormacaoAcademica
          cliente={cliente ?? criarClienteFormacaoAcademicaIndisponivel()}
        />
      </section>
    </main>
  );
}
