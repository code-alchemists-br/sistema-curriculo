// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
import { useEffect, useState, type FormEvent } from "react";

import {
  FalhaAcessoEstudante,
  type ClienteAcessoEstudante,
} from "../api/cliente-acesso-estudante";
import {
  traduzirFalhaAcesso,
  validarAcesso,
  type ErrosFormulario,
} from "../model/formulario-acesso";
import { BotaoHero } from "../../../shared";
import "./FormularioAcesso.css";

/** Define os colaboradores e o e-mail inicial do formulário de acesso. */
export interface FormularioAcessoProps {
  cliente: ClienteAcessoEstudante;
  emailInicial: string;
  aoAcessar?: (email?: string) => void;
  aoAlterarEmail?: (email: string) => void;
}

/**
 * Renderiza e controla o formulário de confirmação de credenciais.
 *
 * O componente mantém os valores no estado local, valida a experiência antes
 * do envio e usa o cliente injetado para isolar transporte. Ele existe para
 * comunicar o início da sessão criada pelo backend sem acoplar a tela a token
 * ou a uma rota protegida específica.
 */
export function FormularioAcesso({
  cliente,
  emailInicial,
  aoAcessar,
  aoAlterarEmail,
}: FormularioAcessoProps) {
  const [email, setEmail] = useState(emailInicial);
  const [senha, setSenha] = useState("");
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [erros, setErros] = useState<ErrosFormulario>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    if (emailInicial !== undefined) {
      setEmail(emailInicial);
    }
  }, [emailInicial]);

  /** Atualiza o e-mail e remove feedback que já não descreve o valor atual. */
  function atualizarEmail(valor: string): void {
    setEmail(valor);
    setErros((atuais) => ({ ...atuais, email: undefined }));
    setMensagem(null);
    aoAlterarEmail?.(valor);
  }

  /** Atualiza a senha somente no estado transitório da unidade. */
  function atualizarSenha(valor: string): void {
    setSenha(valor);
    setErros((atuais) => ({ ...atuais, senha: undefined }));
    setMensagem(null);
  }

  /**
   * Confirma credenciais e comunica somente o nível de sucesso oferecido pela API.
   *
   * O manipulador valida antes de delegar ao cliente e preserva valores em erros;
   * após 204 ele limpa a senha e informa que a sessão foi iniciada. Ele existe
   * para representar precisamente o contrato de acesso persistido pelo backend.
   */
  async function enviarAcesso(
    evento: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    evento.preventDefault();
    const novosErros = validarAcesso({ email, senha });

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      return;
    }

    setEnviando(true);
    setMensagem(null);

    try {
      await cliente.acessar({ email: email.trim(), senha });
      setSenha("");
      if (aoAcessar) {
        aoAcessar(email.trim());
      } else {
        setMensagem("Acesso realizado. Sua sessão foi iniciada.");
      }
    } catch (erro: unknown) {
      setMensagem(
        traduzirFalhaAcesso(
          erro instanceof FalhaAcessoEstudante ? erro.codigo : "rede",
        ),
      );
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form className="formulario-acesso" noValidate onSubmit={enviarAcesso}>
      <div className="field">
        <label htmlFor="email-acesso">E-mail</label>
        <input
          aria-describedby={
            erros.email === undefined ? undefined : "email-acesso-erro"
          }
          aria-invalid={erros.email === undefined ? undefined : true}
          autoComplete="email"
          id="email-acesso"
          onChange={(evento) => atualizarEmail(evento.target.value)}
          required
          type="email"
          value={email}
        />
        {erros.email !== undefined && (
          <p className="field__error" id="email-acesso-erro">
            {erros.email}
          </p>
        )}
      </div>
      <div className="field">
        <label htmlFor="senha-acesso">Senha</label>
        <div className="field__input-container">
          <input
            aria-describedby={
              erros.senha === undefined ? undefined : "senha-acesso-erro"
            }
            aria-invalid={erros.senha === undefined ? undefined : true}
            autoComplete="current-password"
            id="senha-acesso"
            onChange={(evento) => atualizarSenha(evento.target.value)}
            required
            type={mostrarSenha ? "text" : "password"}
            value={senha}
          />
          <button
            type="button"
            className="field__btn-toggle-senha"
            onClick={() => setMostrarSenha((v) => !v)}
            tabIndex={-1}
            aria-label={mostrarSenha ? "Ocultar senha" : "Ver senha"}
            title={mostrarSenha ? "Ocultar senha" : "Ver senha"}
          >
            {mostrarSenha ? (
              <svg
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <path
                  d="M3 3L17 17M8.5 8.5A3 3 0 0012.7 12.7M9.88 5.04C9.92 5.04 9.96 5.04 10 5.04C14.5 5.04 18 10 18 10C17.43 10.98 16.64 12.02 15.65 12.93M6.53 6.53C4.42 7.57 3 10 3 10C3 10 6.5 15 10 15C11.31 15 12.52 14.36 13.53 13.53"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            ) : (
              <svg
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <path
                  d="M10 5C5.5 5 2 10 2 10C2 10 5.5 15 10 15C14.5 15 18 10 18 10C18 10 14.5 5 10 5Z"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <circle
                  cx="10"
                  cy="10"
                  r="3"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            )}
          </button>
        </div>
        {erros.senha !== undefined && (
          <p className="field__error" id="senha-acesso-erro">
            {erros.senha}
          </p>
        )}
      </div>
      {mensagem !== null && (
        <p
          className={`form-message ${
            mensagem.includes("sessão")
              ? "form-message--status-info"
              : "form-message--status-error"
          }`}
          role="status"
        >
          {mensagem}
        </p>
      )}
      <BotaoHero
        disabled={enviando}
        mostrarIcone={false}
        type="submit"
        wrapperClassName="formulario-acesso__botao-wrapper botao-hero-wrapper--full-width"
      >
        {enviando ? "Confirmando..." : "Entrar"}
      </BotaoHero>
    </form>
  );
}
