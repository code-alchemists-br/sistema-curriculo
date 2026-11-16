import { useMemo, useState } from "react";

import {
  criarClienteAssistenteIa,
  PainelRevisaoIa,
  useRevisoesIa,
} from "../../../features/assistente-ia";
import {
  criarClienteProjetosAcademicosEmMemoria,
  FormularioCadastroProjetoAcademico,
  type ClienteProjetosAcademicos,
  type ValoresProjetoAcademico,
} from "../../../features/cadastro-projeto-academico";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaCadastroProjetosAcademicos.css";

/** Define as propriedades para compor a página de projetos acadêmicos. */
export interface PaginaCadastroProjetosAcademicosProps {
  cliente?: ClienteProjetosAcademicos;
  onAvancar?: () => void;
  onVoltar?: () => void;
  onVoltarInicio?: () => void;
  projetosIniciais?: ValoresProjetoAcademico[];
  aoAlterarProjetos?: (projetos: ValoresProjetoAcademico[]) => void;
}

/**
 * Compõe a página de cadastro de projetos acadêmicos (Etapa 7 de 9).
 *
 * Utiliza o layout compartilhado de cadastro de currículo, com o painel visual
 * retangular degradê e a barra de progresso segmentada na sétima etapa.
 */
export function PaginaCadastroProjetosAcademicos({
  cliente = criarClienteProjetosAcademicosEmMemoria(),
  onAvancar,
  onVoltar,
  onVoltarInicio,
  projetosIniciais,
  aoAlterarProjetos,
}: PaginaCadastroProjetosAcademicosProps) {
  const [progresso, setProgresso] = useState(0);
  const clienteIa = useMemo(() => criarClienteAssistenteIa(), []);
  const revisoes = useRevisoesIa(clienteIa);
  const pergunta = "O que o projeto faz, qual foi a sua parte e qual foi o resultado?";

  function handleAvancar(): void {
    if (onAvancar) {
      onAvancar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=selecionar-modelo";
    }
  }

  function handleVoltar(): void {
    if (onVoltar) {
      onVoltar();
      return;
    }
    if (typeof window !== "undefined") {
      window.location.search = "?etapa=competencias";
    }
  }

  return (
    <LayoutCadastroCurriculo
      subtitulo="Projetos Acadêmicos"
      etapaAtual={7}
      totalEtapas={9}
      progressoEtapaAtual={progresso}
      onVoltarInicio={onVoltarInicio}
    >
      <section
        aria-labelledby="titulo-pagina-projetos"
        className="pagina-projetos__conteudo"
      >
        <h1 id="titulo-pagina-projetos" className="pagina-projetos__sr-only">
          Projetos acadêmicos
        </h1>

        <FormularioCadastroProjetoAcademico
          cliente={cliente}
          aoAlterarProgresso={setProgresso}
          aoAvancar={handleAvancar}
          onVoltar={handleVoltar}
          projetosIniciais={projetosIniciais}
          aoAlterarProjetos={aoAlterarProjetos}
          validarDescricoes={(projetos) =>
            revisoes.revisarAntesDeSalvar(
              projetos.map((p) => ({
                texto: p.descricao,
                campo: "descricao_projeto",
                pergunta,
                contexto: { titulo: p.titulo, tecnologias: p.tecnologias },
              })),
            )
          }
          renderizarAssistenteDescricao={({ indice, projeto, aplicarDescricao }) => (
            <PainelRevisaoIa
              aoAplicarTexto={aplicarDescricao}
              aoMudarMemoria={(memoria) => revisoes.atualizar(indice, memoria)}
              id={`projeto-${indice}-ia`}
              memoria={revisoes.memoriaDe(indice)}
              texto={projeto.descricao}
            />
          )}
        />
      </section>
    </LayoutCadastroCurriculo>
  );
}
