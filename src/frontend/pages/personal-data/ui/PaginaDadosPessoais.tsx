import { useState } from "react";

import {
  criarClienteDadosPessoaisIndisponivel,
  FormularioDadosPessoais,
  type ClienteDadosPessoais,
} from "../../../features/edit-personal-data";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaDadosPessoais.css";

/** Define o cliente opcional usado ao compor a página de dados pessoais. */
export interface PaginaDadosPessoaisProps {
  cliente?: ClienteDadosPessoais;
}

/**
 * Compõe a primeira etapa de dados do Wizard de currículo.
 *
 * Apresenta a interface remodelada com o painel visual de degradê alaranjado à esquerda (~46%)
 * e o formulário com barra de progresso segmentada à direita (~54%).
 */
export function PaginaDadosPessoais({
  cliente = criarClienteDadosPessoaisIndisponivel(),
}: PaginaDadosPessoaisProps) {
  const [progresso, setProgresso] = useState(0);

  return (
    <LayoutCadastroCurriculo
      subtitulo="Dados Pessoais"
      etapaAtual={1}
      totalEtapas={8}
      progressoEtapaAtual={progresso}
    >
      <section
        aria-labelledby="titulo-dados-pessoais"
        className="pagina-dados-pessoais__conteudo"
      >
        <h1 id="titulo-dados-pessoais" className="pagina-dados-pessoais__sr-only">
          Conte um pouco sobre você
        </h1>
        <FormularioDadosPessoais
          cliente={cliente}
          aoAlterarProgresso={setProgresso}
        />
      </section>
    </LayoutCadastroCurriculo>
  );
}
