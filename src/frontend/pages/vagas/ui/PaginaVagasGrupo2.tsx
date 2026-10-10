import {
  criarClienteVagasGrupo2Indisponivel,
  TelaVagasGrupo2,
  type ClienteVagasGrupo2,
} from "../../../features/listar-vagas-grupo2";

const clientePadrao = criarClienteVagasGrupo2Indisponivel();

/** Define o cliente opcional recebido pela composição da página de vagas. */
export interface PaginaVagasGrupo2Props {
  cliente?: ClienteVagasGrupo2;
}

/**
 * Compõe a página de sugestões de vagas associadas a um currículo.
 *
 * A página escolhe o cliente padrão indisponível quando nenhum adaptador foi
 * conectado e delega toda a consulta à feature. Ela existe para deixar a tela
 * preparada para o futuro roteamento sem concentrar lógica de integração em
 * `app` ou em componentes de página.
 */
export function PaginaVagasGrupo2({ cliente = clientePadrao }: PaginaVagasGrupo2Props) {
  return (
    <main className="app-shell">
      <div className="app-shell__content">
        <TelaVagasGrupo2 cliente={cliente} />
      </div>
    </main>
  );
}
