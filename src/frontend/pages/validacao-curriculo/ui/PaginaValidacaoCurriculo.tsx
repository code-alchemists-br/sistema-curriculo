import {
  TelaValidacaoCurriculo,
  type CurriculoParaValidacao,
} from "../../../features/validate-curriculum";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaValidacaoCurriculo.css";

/** Define os dados e ações recebidos pela página de validação final. */
export interface PaginaValidacaoCurriculoProps {
  dados?: CurriculoParaValidacao;
  onVisualizarPreview?: () => void;
  onExportarPdf?: () => void;
  onConfirmarCurriculo?: () => void;
}

const DADOS_VALIDACAO_PADRAO: CurriculoParaValidacao = {
  dadosPessoais: {
    nomeCompleto: "Rafael Mendes",
    enderecoCompleto: "Avenida Paulista, 1000 - São Paulo, SP",
    telefones: ["(11) 98888-7777"],
    email: "rafael.mendes@fatec.sp.gov.br",
  },
  formacaoAcademica: { status: "preenchida" },
  experienciasProfissionais: { status: "preenchida" },
  competencias: {
    hardSkills: ["React", "TypeScript", "Node.js"],
    softSkills: ["Comunicação", "Trabalho em equipe"],
  },
  projetosAcademicos: [
    {
      titulo: "Sistema Currículo",
      descricao: "Plataforma web para criação e exportação de currículos universitários.",
      tecnologias: "React, TypeScript, CSS3",
    },
  ],
};

/**
 * Compõe a página de validação final e revisão do currículo (Etapa 8 de 8).
 *
 * Utiliza o layout compartilhado de cadastro de currículo com 100% das barras
 * de progresso preenchidas e subtítulo "Validação e Revisão".
 */
export function PaginaValidacaoCurriculo({
  dados = DADOS_VALIDACAO_PADRAO,
  onVisualizarPreview,
  onExportarPdf,
  onConfirmarCurriculo,
}: PaginaValidacaoCurriculoProps) {
  return (
    <LayoutCadastroCurriculo
      subtitulo="Validação e Revisão"
      etapaAtual={8}
      totalEtapas={8}
      progressoEtapaAtual={100}
    >
      <section
        aria-labelledby="titulo-pagina-validacao"
        className="pagina-validacao__conteudo"
      >
        <h1
          id="titulo-pagina-validacao"
          className="pagina-validacao__sr-only"
        >
          Validação e Revisão do Currículo
        </h1>

        <TelaValidacaoCurriculo
          dados={dados}
          onVisualizarPreview={onVisualizarPreview}
          onExportarPdf={onExportarPdf}
          onConfirmarCurriculo={onConfirmarCurriculo}
        />
      </section>
    </LayoutCadastroCurriculo>
  );
}
