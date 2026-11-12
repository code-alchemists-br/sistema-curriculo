import {
  criarClienteRecuperacaoSenhaIndisponivel,
  FormularioRecuperacaoSenha,
  type ClienteRecuperacaoSenha,
} from "../../../features/recuperar-senha";
import gradienteLogin from "../../../shared/assets/images/gradiente_login.webp";
import "./PaginaRecuperacaoSenha.css";

/** Define os callbacks e colaboradores da página de recuperação de senha. */
export interface PaginaRecuperacaoSenhaProps {
  cliente?: ClienteRecuperacaoSenha;
  emailInicial?: string;
  onVoltarLogin?: () => void;
  onVoltarInicio?: () => void;
  onSucessoSolicitacao?: (email: string) => void;
}

/**
 * Compõe a tela de recuperação de senha com a identidade visual LIMINAL.
 *
 * Utiliza o mesmo padrão de layout, fundo com glow degradê, card glassmorphic
 * e tipografia da página de login e cadastro.
 */
export function PaginaRecuperacaoSenha({
  cliente,
  emailInicial = "",
  onVoltarLogin,
  onVoltarInicio,
  onSucessoSolicitacao,
}: PaginaRecuperacaoSenhaProps) {
  const clienteEfetivo = cliente ?? criarClienteRecuperacaoSenhaIndisponivel();

  const handleVoltar = onVoltarLogin ?? onVoltarInicio;

  return (
    <main className="pagina-recuperar-senha app-shell">
      <img
        alt=""
        aria-hidden="true"
        className="pagina-recuperar-senha__glow"
        src={gradienteLogin}
      />
      <div className="pagina-recuperar-senha__container">
        {handleVoltar && (
          <button
            className="pagina-recuperar-senha__voltar"
            onClick={handleVoltar}
            type="button"
          >
            ← Voltar para o {onVoltarLogin ? "login" : "início"}
          </button>
        )}

        <section
          aria-labelledby="titulo-recuperacao"
          className="pagina-recuperar-senha__card app-shell__content"
        >
          <span className="pagina-recuperar-senha__eyebrow eyebrow">
            LIMINAL
          </span>
          <h1
            className="pagina-recuperar-senha__titulo"
            id="titulo-recuperacao"
          >
            Recupere sua senha
          </h1>
          <p className="pagina-recuperar-senha__subtitulo">
            Informe seu e-mail cadastrado para enviarmos as instruções de
            redefinição de acesso.
          </p>

          <section
            aria-label="Formulário de recuperação de senha"
            className="pagina-recuperar-senha__formulario-wrapper account-form"
          >
            <FormularioRecuperacaoSenha
              aoConcluirSolicitacao={onSucessoSolicitacao}
              cliente={clienteEfetivo}
              emailInicial={emailInicial}
            />
          </section>
        </section>

        {onVoltarLogin && (
          <footer className="pagina-recuperar-senha__alternador">
            <p className="pagina-recuperar-senha__alternador-texto">
              Lembrou sua senha?{" "}
              <button
                className="pagina-recuperar-senha__alternador-botao"
                onClick={onVoltarLogin}
                type="button"
              >
                Entrar
              </button>
            </p>
          </footer>
        )}
      </div>
    </main>
  );
}
