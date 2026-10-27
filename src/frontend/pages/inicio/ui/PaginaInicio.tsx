import { CabecalhoPublico } from "../../../widgets/cabecalho-publico";
import { Destaques } from "../../../widgets/destaques";
import { Hero } from "../../../widgets/hero";
import "./PaginaInicio.css";

export interface PaginaInicioProps {
  onNavegarCadastro?: () => void;
  onNavegarLogin?: () => void;
  onNavegarInicio?: () => void;
  onCriarCurriculo?: () => void;
}

export function PaginaInicio({
  onNavegarCadastro,
  onNavegarLogin,
  onNavegarInicio,
  onCriarCurriculo,
}: PaginaInicioProps) {
  return (
    <div className="pagina-inicio">
      <CabecalhoPublico
        onNavegarCadastro={onNavegarCadastro}
        onNavegarLogin={onNavegarLogin}
        onNavegarInicio={onNavegarInicio}
      />
      <main>
        <Hero onCriarCurriculo={onCriarCurriculo ?? onNavegarCadastro} />
        <Destaques />
      </main>
    </div>
  );
}
