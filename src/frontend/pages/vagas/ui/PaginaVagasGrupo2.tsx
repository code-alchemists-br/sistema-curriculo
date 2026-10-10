import {
  criarClienteVagasGrupo2Indisponivel,
  TelaVagasGrupo2,
  type ClienteVagasGrupo2,
} from "../../../features/listar-vagas";

const clientePadrao = criarClienteVagasGrupo2Indisponivel();

export interface PaginaVagasGrupo2Props {
  cliente?: ClienteVagasGrupo2;
}

export function PaginaVagasGrupo2({
  cliente = clientePadrao,
}: PaginaVagasGrupo2Props) {
  return (
    <main className="app-shell">
      <div className="app-shell__content">
        <TelaVagasGrupo2 cliente={cliente} />
      </div>
    </main>
  );
}
