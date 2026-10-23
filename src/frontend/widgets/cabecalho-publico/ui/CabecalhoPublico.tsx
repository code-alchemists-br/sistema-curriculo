import "./CabecalhoPublico.css";

export interface CabecalhoPublicoProps {
  onNavegarCadastro?: () => void;
  onNavegarLogin?: () => void;
  onNavegarInicio?: () => void;
}

export function CabecalhoPublico({
  onNavegarCadastro,
  onNavegarLogin,
  onNavegarInicio,
}: CabecalhoPublicoProps) {
  return (
    <header className="cabecalho-publico" aria-label="Navegação principal">
      <div className="cabecalho-publico__container">
        <div className="cabecalho-publico__brand">
          <button
            type="button"
            className="cabecalho-publico__logo-btn"
            onClick={onNavegarInicio}
            aria-label="LIMINAL - Voltar para o início"
          >
            LIMINAL
          </button>
        </div>

        <nav
          className="cabecalho-publico__actions"
          aria-label="Acesso e cadastro"
        >
          <button
            type="button"
            className="cabecalho-publico__btn-login"
            onClick={onNavegarLogin}
          >
            Fazer login
          </button>
          <button
            type="button"
            className="cabecalho-publico__btn-criar-conta"
            onClick={onNavegarCadastro}
          >
            Criar conta
          </button>
        </nav>
      </div>
    </header>
  );
}
