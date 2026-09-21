// Proveniência: decision-analysis prompts/frontend/20260921-120136-tela-cadastro-projetos-academicos-v001.md#v001
import {
  criarClienteProjetosAcademicosIndisponivel,
  FormularioCadastroProjetoAcademico,
  type ClienteProjetosAcademicos
} from "../../../features/cadastro-projeto-academico";

/** Define o cliente opcional que permite compor a página em cenários distintos. */
export interface PaginaCadastroProjetosAcademicosProps {
  cliente?: ClienteProjetosAcademicos;
}

/**
 * Compõe a página isolada de cadastro de projetos acadêmicos.
 *
 * A página fornece orientação estática e delega interação ao formulário da
 * feature por sua API pública; sem integração real, usa cliente que informa
 * indisponibilidade. Ela existe para disponibilizar a unidade de tela sem
 * inventar sessão, rota protegida, persistência ou navegação global.
 */
export function PaginaCadastroProjetosAcademicos({
  cliente = criarClienteProjetosAcademicosIndisponivel()
}: PaginaCadastroProjetosAcademicosProps) {
  return (
    <main className="app-shell">
      <section aria-labelledby="titulo-pagina-projetos" className="app-shell__content">
        <p className="eyebrow">Projetos acadêmicos</p>
        <h1 id="titulo-pagina-projetos">Cadastre seu projeto acadêmico</h1>
        <p>
          Explique o objetivo do projeto, sua contribuição e as principais tecnologias utilizadas.
        </p>
        <FormularioCadastroProjetoAcademico cliente={cliente} />
      </section>
    </main>
  );
}
