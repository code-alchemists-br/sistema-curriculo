import { useState } from "react";

import type { Student } from "../../../entities/student";
import {
  criarClienteDadosPessoaisEmMemoria,
  FormularioDadosPessoais,
  type ClienteDadosPessoais,
} from "../../../features/edit-personal-data";
import type { ValoresDadosPessoais } from "../../../features/edit-personal-data/model/formulario-dados-pessoais";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaDadosPessoais.css";

/** Define as propriedades da página de dados pessoais. */
export interface PaginaDadosPessoaisProps {
  cliente?: ClienteDadosPessoais;
  aoAvancar?: () => void;
  onVoltar?: () => void;
  valoresIniciais?: ValoresDadosPessoais;
  aoSalvar?: (dados: Student) => void;
  aoAlterarValores?: (valores: ValoresDadosPessoais) => void;
}

/**
 * Compõe a primeira etapa de dados do Wizard de currículo.
 *
 * Apresenta a interface com o painel visual à esquerda e o formulário
 * com barra de progresso segmentada à direita.
 */
export function PaginaDadosPessoais({
  cliente,
  aoAvancar,
  onVoltar,
  valoresIniciais,
  aoSalvar,
  aoAlterarValores,
}: PaginaDadosPessoaisProps) {
  const [progresso, setProgresso] = useState(0);

  const clienteEfetivo =
    cliente ??
    criarClienteDadosPessoaisEmMemoria((dados) => {
      aoSalvar?.(dados);
    });

  function handleAvancar(): void {
    if (aoAvancar) {
      aoAvancar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=formacao-academica";
    }
  }

  return (
    <LayoutCadastroCurriculo
      subtitulo="Dados Pessoais"
      etapaAtual={1}
      totalEtapas={9}
      progressoEtapaAtual={progresso}
    >
      <section
        aria-labelledby="titulo-dados-pessoais"
        className="pagina-dados-pessoais__conteudo"
      >
        <h1
          id="titulo-dados-pessoais"
          className="pagina-dados-pessoais__sr-only"
        >
          Conte um pouco sobre você
        </h1>
        <FormularioDadosPessoais
          cliente={clienteEfetivo}
          aoAlterarProgresso={setProgresso}
          aoAvancar={handleAvancar}
          onVoltar={onVoltar}
          valoresIniciais={valoresIniciais}
          aoAlterarValores={aoAlterarValores}
        />
      </section>
    </LayoutCadastroCurriculo>
  );
}
