import { useState } from "react";

import {
  criarClienteFormacaoAcademicaEmMemoria,
  FormularioFormacaoAcademica,
  type CadastroFormacaoAcademicaEntrada,
  type ClienteFormacaoAcademica,
} from "../../../features/cadastrar-formacao-academica";
import type { ValoresFormacaoAcademica } from "../../../features/cadastrar-formacao-academica/model/formulario-formacao-academica";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaFormacaoAcademica.css";

/** Define as propriedades da página de formação acadêmica. */
export interface PaginaFormacaoAcademicaProps {
  cliente?: ClienteFormacaoAcademica;
  onAvancar?: () => void;
  onVoltar?: () => void;
  formacoesIniciais?: ValoresFormacaoAcademica[];
  aoCadastrar?: (entrada: CadastroFormacaoAcademicaEntrada) => void;
  aoAlterarFormacoes?: (formacoes: ValoresFormacaoAcademica[]) => void;
}

/**
 * Compõe a tela de cadastro de formação acadêmica (Etapa 2 de 9).
 *
 * Utiliza o layout compartilhado de cadastro de currículo, com o painel visual
 * retangular degradê e a barra de progresso segmentada na segunda etapa.
 */
export function PaginaFormacaoAcademica({
  cliente,
  onAvancar,
  onVoltar,
  formacoesIniciais,
  aoCadastrar,
  aoAlterarFormacoes,
}: PaginaFormacaoAcademicaProps) {
  const [progresso, setProgresso] = useState(0);

  const clienteEfetivo =
    cliente ??
    criarClienteFormacaoAcademicaEmMemoria((entrada) => {
      aoCadastrar?.(entrada);
    });

  function handleAvancar(): void {
    if (onAvancar) {
      onAvancar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=experiencias-profissionais";
    }
  }

  function handleVoltar(): void {
    if (onVoltar) {
      onVoltar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=dados-pessoais";
    }
  }

  return (
    <LayoutCadastroCurriculo
      subtitulo="Formação Acadêmica"
      etapaAtual={2}
      totalEtapas={9}
      progressoEtapaAtual={progresso}
    >
      <section
        aria-labelledby="titulo-formacao"
        className="pagina-formacao-academica__conteudo"
      >
        <h1 id="titulo-formacao" className="pagina-formacao-academica__sr-only">
          Formação acadêmica
        </h1>
        <FormularioFormacaoAcademica
          aoAlterarProgresso={setProgresso}
          aoAvancar={handleAvancar}
          cliente={clienteEfetivo}
          formacoesIniciais={formacoesIniciais}
          onVoltar={handleVoltar}
          aoAlterarFormacoes={aoAlterarFormacoes}
        />
      </section>
    </LayoutCadastroCurriculo>
  );
}
