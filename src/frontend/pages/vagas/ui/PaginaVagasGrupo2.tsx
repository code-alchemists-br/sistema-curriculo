import {
  criarClienteVagasGrupo2Indisponivel,
  TelaVagasGrupo2,
  type ClienteDecisoesRecomendacao,
  type ClienteVagasGrupo2,
} from "../../../features/listar-vagas";
import { CabecalhoPublico } from "../../../widgets/cabecalho-publico";
import "./PaginaVagasGrupo2.css";

const clientePadrao = criarClienteVagasGrupo2Indisponivel();

/** Define as dependências opcionais usadas pela página de vagas. */
export interface PaginaVagasGrupo2Props {
  cliente?: ClienteVagasGrupo2;
  clienteDecisoes?: ClienteDecisoesRecomendacao;
  onVoltar?: () => void;
}

/** Compõe a página e repassa clientes injetáveis para a feature de vagas. */
export function PaginaVagasGrupo2({
  cliente = clientePadrao,
  clienteDecisoes,
  onVoltar,
}: PaginaVagasGrupo2Props) {
  return (
    <div className="pagina-vagas">
      <div className="pagina-vagas__fundo-fixo" aria-hidden="true" />
      <div className="pagina-vagas__shade" aria-hidden="true" />

      {onVoltar && (
        <CabecalhoPublico
          onNavegarInicio={onVoltar}
          onNavegarVagas={onVoltar}
          textoBotaoRetorno="← Voltar ao início"
        />
      )}

      <main className="app-shell">
        <div className="app-shell__content">
          <TelaVagasGrupo2
            cliente={cliente}
            clienteDecisoes={clienteDecisoes}
          />
        </div>
      </main>
    </div>
  );
}
