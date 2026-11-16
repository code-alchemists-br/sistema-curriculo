import {
  CabecalhoPublico,
  type UsuarioAutenticado,
} from "../../../widgets/cabecalho-publico";
import { Destaques } from "../../../widgets/destaques";
import { Hero } from "../../../widgets/hero";
import "./PaginaInicio.css";

/** Define as ações de navegação e o estado do estudante usados pela página inicial. */
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
  /** O estudante já concluiu o currículo (chegou a escolher o modelo). */
  temCurriculoPronto?: boolean;
  onLogout?: () => void;
}

/**
 * Página inicial pública.
 *
 * - O que faz: mostra cabeçalho, abertura (Hero), destaques e rodapé legal.
 * - Como faz: para quem está logado e já tem o currículo pronto, a abertura
 *   troca o convite "criar currículo" por "ver vagas", com "Ver meu currículo"
 *   como ação secundária; nos demais casos, convida a criar ou continuar.
 * - Qual finalidade atende: depois de montar o currículo, o próximo passo do
 *   estudante é se candidatar, então as vagas ganham o destaque principal.
 */
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
  temCurriculoPronto,
  onLogout,
}: PaginaInicioProps) {
  const focoEmVagas = Boolean(
    usuarioLogado && temCurriculoPronto && onNavegarVagas,
  );
  const textoBotaoHero =
    usuarioLogado && temProgressoCurriculo
      ? "CONTINUAR CURRÍCULO"
      : "CRIAR CURRÍCULO";
  const primeiroNome = usuarioLogado?.nome?.trim().split(/\s+/)[0];

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
        {focoEmVagas ? (
          <Hero
            sobretitulo={`✓ ${primeiroNome ? `${primeiroNome}, seu` : "Seu"} currículo está pronto`}
            titulo="Agora é hora de encontrar sua vaga"
            subtitulo="Veja as vagas abertas que combinam com o seu perfil e candidate-se usando o currículo que você acabou de montar."
            textoBotao="VER VAGAS"
            onCriarCurriculo={onNavegarVagas}
            acaoSecundaria={
              onNavegarPerfil
                ? { texto: "Ver meu currículo", aoClicar: onNavegarPerfil }
                : undefined
            }
          />
        ) : (
          <Hero
            onCriarCurriculo={onCriarCurriculo ?? onNavegarCadastro}
            textoBotao={textoBotaoHero}
          />
        )}
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
