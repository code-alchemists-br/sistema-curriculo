// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
import { useState, type FormEvent } from "react";

import {
  FalhaAcessoEstudante,
  type ClienteAcessoEstudante
} from "../api/cliente-acesso-estudante";
import { traduzirFalhaAcesso, validarAcesso, type ErrosFormulario } from "../model/formulario-acesso";

/** Define os colaboradores e o e-mail inicial do formulário de acesso. */
export interface FormularioAcessoProps {
  cliente: ClienteAcessoEstudante;
  emailInicial: string;
}

/**
 * Renderiza e controla o formulário de confirmação de credenciais.
 *
 * O componente mantém os valores no estado local, valida a experiência antes
 * do envio e usa o cliente injetado para isolar transporte. Ele existe para
 * informar o resultado de 204 sem inventar sessão, token ou navegação protegida.
 */
export function FormularioAcesso({ cliente, emailInicial }: FormularioAcessoProps) {
  const [email, setEmail] = useState(emailInicial);
  const [senha, setSenha] = useState("");
  const [erros, setErros] = useState<ErrosFormulario>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  /** Atualiza o e-mail e remove feedback que já não descreve o valor atual. */
  function atualizarEmail(valor: string): void {
    setEmail(valor);
    setErros((atuais) => ({ ...atuais, email: undefined }));
    setMensagem(null);
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
   * após 204 ele limpa a senha e informa que não há sessão criada. Ele existe para
   * representar precisamente o contrato atual de acesso do backend.
   */
  async function enviarAcesso(evento: FormEvent<HTMLFormElement>): Promise<void> {
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
      setMensagem("Credenciais confirmadas. Uma sessão ainda não foi criada.");
    } catch (erro: unknown) {
      setMensagem(
        traduzirFalhaAcesso(
          erro instanceof FalhaAcessoEstudante ? erro.codigo : "rede"
        )
      );
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form noValidate onSubmit={enviarAcesso}>
      <div className="field">
        <label htmlFor="email-acesso">E-mail</label>
        <input
          aria-describedby={erros.email === undefined ? undefined : "email-acesso-erro"}
          aria-invalid={erros.email === undefined ? undefined : true}
          autoComplete="email"
          id="email-acesso"
          onChange={(evento) => atualizarEmail(evento.target.value)}
          required
          type="email"
          value={email}
        />
        {erros.email !== undefined && <p className="field__error" id="email-acesso-erro">{erros.email}</p>}
      </div>
      <div className="field">
        <label htmlFor="senha-acesso">Senha</label>
        <input
          aria-describedby={erros.senha === undefined ? undefined : "senha-acesso-erro"}
          aria-invalid={erros.senha === undefined ? undefined : true}
          autoComplete="current-password"
          id="senha-acesso"
          onChange={(evento) => atualizarSenha(evento.target.value)}
          required
          type="password"
          value={senha}
        />
        {erros.senha !== undefined && <p className="field__error" id="senha-acesso-erro">{erros.senha}</p>}
      </div>
      {mensagem !== null && <p className="form-message" role="status">{mensagem}</p>}
      <button disabled={enviando} type="submit">
        {enviando ? "Confirmando..." : "Entrar"}
      </button>
    </form>
  );
}
