import { FormularioCursos } from "../../../features/edit-courses";
import { FormularioIdiomas } from "../../../features/edit-languages";

/**
 * Compõe a página de cadastro de cursos, certificações e idiomas.
 *
 * A página reúne as duas features independentes em uma única tela do Wizard,
 * delegando toda a lógica de formulário para cada feature. Ela existe para
 * manter a composição de página separada das regras de validação e estado.
 */
export function PaginaCursosIdiomas() {
  return (
    <main className="app-shell">
      <section
        aria-labelledby="titulo-cursos-idiomas"
        className="app-shell__content"
      >
        <h1 id="titulo-cursos-idiomas">Cursos, Certificações e Idiomas</h1>
        <p>
          Cadastre seus cursos complementares, certificações profissionais e
          idiomas que domina.
        </p>
        <FormularioCursos />
        <FormularioIdiomas />
      </section>
    </main>
  );
}
