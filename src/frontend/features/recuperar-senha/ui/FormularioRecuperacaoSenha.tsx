import { useState, type FormEvent } from "react";

import { BotaoHero } from "../../../shared";
import {
  FalhaRecuperacaoSenha,
  type ClienteRecuperacaoSenha,
} from "../api/cliente-recuperacao-senha";
import {
  criarEntradaRecuperacaoSenha,
  traduzirFalhaRecuperacaoSenha,
  validarEmailRecuperacao,
} from "../model/formulario-recuperacao-senha";
import "./FormularioRecuperacaoSenha.css";

/** Define as propriedades do formulário de recuperação de senha. */
export interface FormularioRecuperacaoSenhaProps {
  cliente: ClienteRecuperacaoSenha;
  emailInicial?: string;
  aoAlterarEmail?: (email: string) => void;
  aoConcluirSolicitacao?: (email: string) => void;
}

/**
 * Renderiza o formulário acessível e estilizado de recuperação de senha.
 *
 * Utiliza o mesmo padrão visual, tipografia e tratamento de estados dos formulários
 * de acesso e cadastro da LIMINAL.
 */
export function FormularioRecuperacaoSenha({
  cliente,
  emailInicial = "",
  aoAlterarEmail,
  aoConcluirSolicitacao,
}: FormularioRecuperacaoSenhaProps) {
  const [email, setEmail] = useState(emailInicial);
  const [erroEmail, setErroEmail] = useState<string | undefined>();
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [solicitadoComSucesso, setSolicitadoComSucesso] = useState(false);

  function atualizarEmail(valor: string): void {
    setEmail(valor);
    setErroEmail(undefined);
    setMensagem(null);
    aoAlterarEmail?.(valor);
  }

  async function enviarFormulario(
    evento: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    evento.preventDefault();
    const erros = validarEmailRecuperacao(email);

    if (erros.email !== undefined) {
      setErroEmail(erros.email);
      return;
    }

    setEnviando(true);
    setMensagem(null);

    try {
      await cliente.solicitar(criarEntradaRecuperacaoSenha(email));
      setSolicitadoComSucesso(true);
      setMensagem(
        "Se houver uma conta associada a este e-mail, você receberá as instruções para redefinir sua senha em instantes.",
      );
      aoConcluirSolicitacao?.(email.trim());
    } catch (erro: unknown) {
      const codigo =
        erro instanceof FalhaRecuperacaoSenha ? erro.codigo : "rede";
      setMensagem(traduzirFalhaRecuperacaoSenha(codigo));
    } finally {
      setEnviando(false);
    }
  }

  const idErro = "email-recuperacao-erro";

  return (
    <form
      aria-busy={enviando}
      className="formulario-recuperacao-senha"
      noValidate
      onSubmit={enviarFormulario}
    >
      <div className="field">
        <label htmlFor="email-recuperacao">E-mail</label>
        <input
          aria-describedby={erroEmail === undefined ? undefined : idErro}
          aria-invalid={erroEmail === undefined ? undefined : true}
          autoComplete="email"
          disabled={enviando || solicitadoComSucesso}
          id="email-recuperacao"
          onChange={(evento) => atualizarEmail(evento.target.value)}
          placeholder="seu.email@exemplo.com"
          required
          type="email"
          value={email}
        />
        {erroEmail !== undefined && (
          <p className="field__error" id={idErro}>
            {erroEmail}
          </p>
        )}
      </div>

      {mensagem !== null && (
        <p
          className={`form-message ${
            solicitadoComSucesso
              ? "form-message--status-info"
              : "form-message--status-error"
          }`}
          role={solicitadoComSucesso ? "status" : "alert"}
        >
          {mensagem}
        </p>
      )}

      {!solicitadoComSucesso && (
        <BotaoHero
          disabled={enviando}
          mostrarIcone={false}
          type="submit"
          wrapperClassName="formulario-recuperacao-senha__botao-wrapper botao-hero-wrapper--full-width"
        >
          {enviando ? "Enviando instruções..." : "Enviar instruções"}
        </BotaoHero>
      )}
    </form>
  );
}
