import {
  criarClienteVagasGrupo2Indisponivel,
  TelaVagasGrupo2,
  type ClienteDecisoesRecomendacao,
  type ClienteVagasGrupo2,
} from "../../../features/listar-vagas";

const clientePadrao = criarClienteVagasGrupo2Indisponivel();

/** Define as dependências opcionais usadas pela página de vagas. */
export interface PaginaVagasGrupo2Props {
  cliente?: ClienteVagasGrupo2;
  clienteDecisoes?: ClienteDecisoesRecomendacao;
}

/** Compõe a página e repassa clientes injetáveis para a feature de vagas. */
export function PaginaVagasGrupo2({
  cliente = clientePadrao,
  clienteDecisoes,
}: PaginaVagasGrupo2Props) {
  return (
    <main className="app-shell">
      <div className="app-shell__content">
        <TelaVagasGrupo2 cliente={cliente} clienteDecisoes={clienteDecisoes} />
      </div>
    </main>
  );
}
