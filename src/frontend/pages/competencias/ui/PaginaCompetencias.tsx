import { FormularioCompetencias } from "../../../features/edit-skills";

/**
 * Compõe a página de cadastro de competências sem assumir persistência,
 * roteamento ou integração externa.
 */
export function PaginaCompetencias() {
  return (
    <main>
      <section aria-labelledby="titulo-pagina-competencias">
        <p>Informações complementares</p>
        <h1 id="titulo-pagina-competencias">Competências</h1>
        <p>
          Informe suas competências técnicas e comportamentais para compor seu
          currículo.
        </p>

        <FormularioCompetencias />
      </section>
    </main>
  );
}
