import {
  CabecalhoPublico,
  type UsuarioAutenticado,
} from "../../../widgets/cabecalho-publico";
import { Destaques } from "../../../widgets/destaques";
import { Hero } from "../../../widgets/hero";
import "./PaginaInicio.css";

export interface PaginaInicioProps {
  onNavegarCadastro?: () => void;
  onNavegarLogin?: () => void;
  onNavegarInicio?: () => void;
  onNavegarPoliticaDePrivacidade?: () => void;
  onNavegarTermosDeUso?: () => void;
  onCriarCurriculo?: () => void;
  onNavegarVagas?: () => void;
  onNavegarPerfil?: () => void;
  usuarioLogado?: UsuarioAutenticado | null;
  temProgressoCurriculo?: boolean;
  onLogout?: () => void;
}

export function PaginaInicio({
  onNavegarCadastro,
  onNavegarLogin,
  onNavegarInicio,
  onNavegarPoliticaDePrivacidade,
  onNavegarTermosDeUso,
  onCriarCurriculo,
  onNavegarVagas,
  onNavegarPerfil,
  usuarioLogado,
  temProgressoCurriculo,
  onLogout,
}: PaginaInicioProps) {
  const textoBotaoHero =
    usuarioLogado && temProgressoCurriculo
      ? "CONTINUAR CURRÍCULO"
      : "CRIAR CURRÍCULO";

  return (
    <div className="pagina-inicio">
      <CabecalhoPublico
        onNavegarCadastro={onNavegarCadastro}
        onNavegarLogin={onNavegarLogin}
        onNavegarInicio={onNavegarInicio}
        onNavegarVagas={onNavegarVagas}
        onNavegarPerfil={onNavegarPerfil}
        usuarioLogado={usuarioLogado}
        onLogout={onLogout}
      />
      <main>
        <Hero
          onCriarCurriculo={onCriarCurriculo ?? onNavegarCadastro}
          textoBotao={textoBotaoHero}
        />
        <Destaques />
      </main>
      {(onNavegarTermosDeUso || onNavegarPoliticaDePrivacidade) && (
        <footer className="pagina-inicio__rodape">
          <nav aria-label="Informações legais">
            {onNavegarTermosDeUso && (
              <button onClick={onNavegarTermosDeUso} type="button">
                Termos de Uso
              </button>
            )}
            {onNavegarPoliticaDePrivacidade && (
              <button onClick={onNavegarPoliticaDePrivacidade} type="button">
                Política de Privacidade
              </button>
            )}
          </nav>
        </footer>
      )}
    </div>
  );
}
