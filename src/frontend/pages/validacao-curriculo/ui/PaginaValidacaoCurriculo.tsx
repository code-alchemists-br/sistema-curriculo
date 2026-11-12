import {
  TelaValidacaoCurriculo,
  type CurriculoParaValidacao,
  type IdSecaoCurriculo,
} from "../../../features/validate-curriculum";
import { LayoutCadastroCurriculo } from "../../../shared/ui/layout-cadastro";
import "./PaginaValidacaoCurriculo.css";

/** Define os dados e ações recebidos pela página de validação final. */
export interface PaginaValidacaoCurriculoProps {
  dados?: CurriculoParaValidacao;
  onVisualizarPreview?: () => void;
  onExportarPdf?: () => void;
  onExportarDocx?: () => void;
  onConfirmarCurriculo?: () => void;
  onVoltar?: () => void;
  onVoltarInicio?: () => void;
  onCorrigirSecao?: (secaoId: IdSecaoCurriculo) => void;
}

const DADOS_VALIDACAO_PADRAO: CurriculoParaValidacao = {
  dadosPessoais: {
    nomeCompleto: "Rafael Mendes",
    enderecoCompleto: "Avenida Paulista, 1000 - São Paulo, SP",
    cidade: "São Paulo",
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
      descricao:
        "Plataforma web para criação e exportação de currículos universitários.",
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
  onExportarDocx,
  onConfirmarCurriculo,
  onVoltar,
  onVoltarInicio,
  onCorrigirSecao,
}: PaginaValidacaoCurriculoProps) {
  return (
    <LayoutCadastroCurriculo
      subtitulo="Validação e Revisão"
      etapaAtual={9}
      totalEtapas={9}
      progressoEtapaAtual={100}
      onVoltarInicio={onVoltarInicio}
    >
      <section
        aria-labelledby="titulo-pagina-validacao"
        className="pagina-validacao__conteudo"
      >
        <h1 id="titulo-pagina-validacao" className="pagina-validacao__sr-only">
          Validação e Revisão do Currículo
        </h1>

        <TelaValidacaoCurriculo
          dados={dados}
          onVisualizarPreview={onVisualizarPreview}
          onExportarPdf={onExportarPdf}
          onExportarDocx={onExportarDocx}
          onConfirmarCurriculo={onConfirmarCurriculo}
          onVoltar={onVoltar}
          onCorrigirSecao={onCorrigirSecao}
        />
      </section>
    </LayoutCadastroCurriculo>
  );
}
