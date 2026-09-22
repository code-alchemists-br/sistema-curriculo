import {
  criarClienteDadosPessoaisIndisponivel,
  FormularioDadosPessoais,
  type ClienteDadosPessoais
} from "../../../features/edit-personal-data";

/** Define o cliente opcional usado ao compor a página de dados pessoais. */
export interface PaginaDadosPessoaisProps {
  cliente?: ClienteDadosPessoais;
}

/**
 * Compõe a primeira etapa de dados do Wizard de currículo.
 *
 * A página fornece contexto e entrega a interação para a feature por sua API
 * pública. Ela existe para manter a composição de página separada das regras
 * de formulário, sem decidir roteamento ou persistência ainda indisponíveis.
 */
export function PaginaDadosPessoais({
  cliente = criarClienteDadosPessoaisIndisponivel()
}: PaginaDadosPessoaisProps) {
  return (
    <main className="app-shell">
      <section aria-labelledby="titulo-dados-pessoais" className="app-shell__content">
        <p className="eyebrow">Dados pessoais e contato</p>
        <h1 id="titulo-dados-pessoais">Conte um pouco sobre você</h1>
        <p>Essas informações serão usadas no cabeçalho do seu currículo.</p>
        <FormularioDadosPessoais cliente={cliente} />
      </section>
    </main>
  );
}
