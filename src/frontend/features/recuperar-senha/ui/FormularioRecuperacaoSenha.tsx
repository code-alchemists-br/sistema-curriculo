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
  token?: string;
  aoAlterarEmail?: (email: string) => void;
  aoConcluirSolicitacao?: (email: string) => void;
}

/**
 * Renderiza a solicitação ou a redefinição de senha conforme exista token.
 *
 * Envia operações por meio do cliente da feature, valida os campos localmente
 * e comunica carregamento, sucesso e erro de forma acessível. Existe para ligar
 * a interação pública de recuperação à API sem chamadas HTTP na UI.
 */
export function FormularioRecuperacaoSenha({
  cliente,
  emailInicial = "",
  token,
  aoAlterarEmail,
  aoConcluirSolicitacao,
}: FormularioRecuperacaoSenhaProps) {
  const [email, setEmail] = useState(emailInicial);
  const [erroEmail, setErroEmail] = useState<string | undefined>();
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [solicitadoComSucesso, setSolicitadoComSucesso] = useState(false);
  const [senha, setSenha] = useState("");
  const [confirmacaoSenha, setConfirmacaoSenha] = useState("");
  const [erroSenha, setErroSenha] = useState<string | undefined>();
  const [erroConfirmacao, setErroConfirmacao] = useState<string | undefined>();
  const [redefinidoComSucesso, setRedefinidoComSucesso] = useState(false);

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

  /**
   * Valida a nova senha e envia a credencial vinculada ao token.
   *
   * Compara as duas senhas e chama o cliente somente quando os campos atendem
   * ao contrato. Existe para evitar requisições inválidas e dar retorno claro.
   */
  async function redefinirSenha(
    evento: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    evento.preventDefault();
    const erroSenhaAtual =
      senha.length < 8 ? "A senha deve ter ao menos 8 caracteres." : undefined;
    const erroConfirmacaoAtual =
      confirmacaoSenha !== senha ? "As senhas não coincidem." : undefined;
    setErroSenha(erroSenhaAtual);
    setErroConfirmacao(erroConfirmacaoAtual);
    if (erroSenhaAtual || erroConfirmacaoAtual || !token) return;

    setEnviando(true);
    setMensagem(null);
    try {
      await cliente.redefinir({ token, senha });
      setRedefinidoComSucesso(true);
      setMensagem("Senha redefinida. Você já pode entrar com a nova senha.");
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
      onSubmit={token ? redefinirSenha : enviarFormulario}
    >
      {!token && (
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
      )}

      {token && !redefinidoComSucesso && (
        <>
          <div className="field">
            <label htmlFor="senha-nova-recuperacao">Nova senha</label>
            <input
              aria-describedby={
                erroSenha === undefined
                  ? undefined
                  : "senha-nova-recuperacao-erro"
              }
              aria-invalid={erroSenha === undefined ? undefined : true}
              autoComplete="new-password"
              disabled={enviando}
              id="senha-nova-recuperacao"
              onChange={(evento) => {
                setSenha(evento.target.value);
                setErroSenha(undefined);
              }}
              type="password"
              value={senha}
            />
            {erroSenha && (
              <p className="field__error" id="senha-nova-recuperacao-erro">
                {erroSenha}
              </p>
            )}
          </div>
          <div className="field">
            <label htmlFor="confirmacao-senha-recuperacao">
              Confirme a nova senha
            </label>
            <input
              aria-describedby={
                erroConfirmacao === undefined
                  ? undefined
                  : "confirmacao-senha-recuperacao-erro"
              }
              aria-invalid={erroConfirmacao === undefined ? undefined : true}
              autoComplete="new-password"
              disabled={enviando}
              id="confirmacao-senha-recuperacao"
              onChange={(evento) => {
                setConfirmacaoSenha(evento.target.value);
                setErroConfirmacao(undefined);
              }}
              type="password"
              value={confirmacaoSenha}
            />
            {erroConfirmacao && (
              <p
                className="field__error"
                id="confirmacao-senha-recuperacao-erro"
              >
                {erroConfirmacao}
              </p>
            )}
          </div>
        </>
      )}

      {mensagem !== null && (
        <p
          className={`form-message ${
            solicitadoComSucesso || redefinidoComSucesso
              ? "form-message--status-info"
              : "form-message--status-error"
          }`}
          role={
            solicitadoComSucesso || redefinidoComSucesso ? "status" : "alert"
          }
        >
          {mensagem}
        </p>
      )}

      {!solicitadoComSucesso && !redefinidoComSucesso && (
        <BotaoHero
          disabled={enviando}
          mostrarIcone={false}
          type="submit"
          wrapperClassName="formulario-recuperacao-senha__botao-wrapper botao-hero-wrapper--full-width"
        >
          {enviando
            ? token
              ? "Redefinindo senha..."
              : "Enviando instruções..."
            : token
              ? "Redefinir senha"
              : "Enviar instruções"}
        </BotaoHero>
      )}
    </form>
  );
}
