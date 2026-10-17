import { useState, type FormEvent } from "react";

import "./FormularioRecuperacaoSenha.css";

import {
  FalhaRecuperacaoSenha,
  type ClienteRecuperacaoSenha,
} from "../api/cliente-recuperacao-senha";
import {
  criarEntradaRecuperacaoSenha,
  traduzirFalhaRecuperacaoSenha,
  validarEmailRecuperacao,
} from "../model/formulario-recuperacao-senha";

/** Define o cliente usado pelo formulário para solicitar a recuperação. */
export interface FormularioRecuperacaoSenhaProps {
  cliente: ClienteRecuperacaoSenha;
}

/**
 * Renderiza o formulário acessível de solicitação de recuperação de senha.
 *
 * O componente guarda e valida o e-mail localmente, delegando a solicitação ao
 * cliente injetado e preservando o valor em caso de falha. Ele existe para que
 * a interface possa ser testada com doubles antes da integração de backend.
 */
export function FormularioRecuperacaoSenha({
  cliente,
}: FormularioRecuperacaoSenhaProps) {
  const [email, setEmail] = useState("");
  const [erroEmail, setErroEmail] = useState<string | undefined>();
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  /** Atualiza o e-mail e remove feedback que já não corresponde ao valor atual. */
  function atualizarEmail(valor: string): void {
    setEmail(valor);
    setErroEmail(undefined);
    setMensagem(null);
  }

  /** Valida e solicita a recuperação, sem revelar se há conta para o e-mail. */
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
      setMensagem(
        "Se houver uma conta associada a este e-mail, você receberá as instruções de recuperação.",
      );
    } catch (erro: unknown) {
      setMensagem(
        traduzirFalhaRecuperacaoSenha(
          erro instanceof FalhaRecuperacaoSenha ? erro.codigo : "rede",
        ),
      );
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
          id="email-recuperacao"
          onChange={(evento) => atualizarEmail(evento.target.value)}
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
      <p>Informe seu e-mail para receber instruções de recuperação de senha.</p>
      {enviando && <p role="status">Enviando solicitação de recuperação...</p>}
      {mensagem !== null && (
        <p
          className="form-message"
          role={mensagem.startsWith("Se houver") ? "status" : "alert"}
        >
          {mensagem}
        </p>
      )}
      <button disabled={enviando} type="submit">
        {enviando ? "Enviando..." : "Enviar instruções"}
      </button>
    </form>
  );
}
