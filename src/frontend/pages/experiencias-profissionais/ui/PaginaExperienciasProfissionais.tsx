import { useMemo, useState } from "react";

import {
  criarClienteAssistenteIa,
  PainelRevisaoIa,
  useRevisoesIa,
} from "../../../features/assistente-ia";
import {
  FormularioExperiencias,
  type Experiencia,
} from "../../../features/edit-professional-experience";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaExperienciasProfissionais.css";

/** Define as propriedades da página de experiências profissionais. */
export interface PaginaExperienciasProfissionaisProps {
  experienciasIniciais?: Experiencia[];
  onSalvar?: (experiencias: Experiencia[]) => void;
  onVoltar?: () => void;
  onVoltarInicio?: () => void;
  aoAlterarExperiencias?: (experiencias: Experiencia[]) => void;
}

/**
 * Compõe a página de cadastro de experiências profissionais (Etapa 3 de 9).
 *
 * Utiliza o layout compartilhado de cadastro de currículo, com o painel visual
 * retangular degradê e a barra de progresso segmentada na terceira etapa.
 */
export function PaginaExperienciasProfissionais({
  experienciasIniciais,
  onSalvar,
  onVoltar,
  onVoltarInicio,
  aoAlterarExperiencias,
}: PaginaExperienciasProfissionaisProps) {
  const [progresso, setProgresso] = useState(0);
  const clienteIa = useMemo(() => criarClienteAssistenteIa(), []);
  const revisoes = useRevisoesIa(clienteIa);
  const pergunta = "O que você fazia nessa experiência e com quais tecnologias?";

  return (
    <LayoutCadastroCurriculo
      subtitulo="Experiência Profissional"
      etapaAtual={3}
      totalEtapas={9}
      progressoEtapaAtual={progresso}
      onVoltarInicio={onVoltarInicio}
    >
      <section
        aria-labelledby="titulo-experiencias"
        className="pagina-experiencias-profissionais__conteudo"
      >
        <h1
          id="titulo-experiencias"
          className="pagina-experiencias-profissionais__sr-only"
        >
          Experiências profissionais
        </h1>
        <FormularioExperiencias
          aoAlterarProgresso={setProgresso}
          experienciasIniciais={experienciasIniciais}
          onSalvar={onSalvar}
          onVoltar={onVoltar}
          aoAlterarExperiencias={aoAlterarExperiencias}
          validarDescricoes={(experiencias) =>
            revisoes.revisarAntesDeSalvar(
              experiencias.map((e) => ({
                texto: e.descricao,
                campo: "descricao_experiencia",
                pergunta,
                contexto: { cargo: e.cargo, empresa: e.empresa },
              })),
            )
          }
          renderizarAssistenteDescricao={({ indice, experiencia, aplicarDescricao }) => (
            <PainelRevisaoIa
              aoAplicarTexto={aplicarDescricao}
              aoMudarMemoria={(memoria) => revisoes.atualizar(indice, memoria)}
              id={`experiencia-${indice}-ia`}
              memoria={revisoes.memoriaDe(indice)}
              texto={experiencia.descricao}
            />
          )}
        />
      </section>
    </LayoutCadastroCurriculo>
  );
}
