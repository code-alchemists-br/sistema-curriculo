import { FormularioCertificacao } from "../../../features/cadastro-certificacoes";
import { FormularioCursos } from "../../../features/edit-courses";
import { FormularioIdiomas } from "../../../features/edit-languages";

/**
 * Compõe a página de cadastro de cursos, certificações e idiomas.
 *
 * A página reúne as features independentes de cursos, certificações e idiomas em uma
 * única tela do Wizard, delegando a lógica de formulário para cada feature. Ela existe para
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
        <FormularioCertificacao />
        <FormularioIdiomas />
      </section>
    </main>
  );
}
