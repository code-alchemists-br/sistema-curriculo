import {
  TelaValidacaoCurriculo,
  type CurriculoParaValidacao
} from "../../../features/validate-curriculum";

/** Define os dados e ações recebidos pela página de validação final. */
export interface PaginaValidacaoCurriculoProps {
  dados: CurriculoParaValidacao;
  onVisualizarPreview?: () => void;
  onExportarPdf?: () => void;
  onConfirmarCurriculo?: () => void;
}

/**
 * Compõe a página de validação final e delega a regra transversal à feature.
 * A página recebe o estado do Wizard por propriedades, sem criar uma segunda
 * fonte de verdade nem assumir um roteador inexistente no frontend atual.
 */
export function PaginaValidacaoCurriculo(props: PaginaValidacaoCurriculoProps) {
  return <TelaValidacaoCurriculo {...props} />;
}
