import { FormularioExperiencias } from "../../../features/edit-professional-experience";

/**
 * Compõe a página de cadastro de experiências profissionais.
 *
 * A página delega toda a lógica de formulário para a feature, mantendo a
 * composição separada das regras de validação, estado e ordenação.
 */
export function PaginaExperienciasProfissionais() {
  return (
    <main className="app-shell">
      <section
        aria-labelledby="titulo-experiencias"
        className="app-shell__content"
      >
        <h1 id="titulo-experiencias">Experiências Profissionais</h1>
        <p>
          Cadastre suas experiências de trabalho em ordem. Elas serão
          organizadas automaticamente da mais recente para a mais antiga.
        </p>
        <FormularioExperiencias />
      </section>
    </main>
  );
}
