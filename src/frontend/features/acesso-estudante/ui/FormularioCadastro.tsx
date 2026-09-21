// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
import { useState, type FormEvent } from "react";

import { FalhaAcessoEstudante, type ClienteAcessoEstudante } from "../api/cliente-acesso-estudante";
import { traduzirFalhaAcesso, validarCadastro, type ErrosFormulario, type ValoresCadastro } from "../model/formulario-acesso";

/** Define os colaboradores e a consequência local de um cadastro concluído. */
export interface FormularioCadastroProps {
  cliente: ClienteAcessoEstudante;
  aoCadastrar: (email: string) => void;
}

const valoresIniciais: ValoresCadastro = {
  nome: "",
  email: "",
  senha: "",
  confirmacaoSenha: ""
};

/**
 * Renderiza e controla o formulário isolado de criação de conta.
 *
 * O componente mantém valores e erros locais, valida antes do envio e chama o
 * contrato injetado, sem conhecer fetch ou status HTTP. Ele existe para permitir
 * o cadastro acessível e testável enquanto o backend é substituído por doubles.
 */
export function FormularioCadastro({ cliente, aoCadastrar }: FormularioCadastroProps) {
  const [valores, setValores] = useState(valoresIniciais);
  const [erros, setErros] = useState<ErrosFormulario>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  /** Atualiza somente o campo alterado e remove seu feedback anterior. */
  function atualizarCampo(campo: keyof ValoresCadastro, valor: string): void {
    setValores((atuais) => ({ ...atuais, [campo]: valor }));
    setErros((atuais) => ({ ...atuais, [campo]: undefined }));
    setMensagem(null);
  }

  /**
   * Valida e envia o cadastro, preservando valores em caso de falha.
   *
   * O manipulador interrompe o submit nativo, delega o transporte ao cliente e
   * descarta senhas somente após sucesso. Ele existe para coordenar o fluxo de
   * criação de conta sem transformar o componente em cliente HTTP.
   */
  async function enviarCadastro(evento: FormEvent<HTMLFormElement>): Promise<void> {
    evento.preventDefault();
    const novosErros = validarCadastro(valores);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      return;
    }

    setEnviando(true);
    setMensagem(null);

    try {
      const estudante = await cliente.cadastrar({
        nome: valores.nome.trim(),
        email: valores.email.trim(),
        senha: valores.senha
      });

      setValores(valoresIniciais);
      aoCadastrar(estudante.email);
    } catch (erro: unknown) {
      setMensagem(traduzirFalhaAcesso(erro instanceof FalhaAcessoEstudante ? erro.codigo : "rede"));
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form noValidate onSubmit={enviarCadastro}>
      <Campo autoComplete="name" erro={erros.nome} id="nome" label="Nome" onChange={(valor) => atualizarCampo("nome", valor)} value={valores.nome} />
      <Campo autoComplete="email" erro={erros.email} id="email-cadastro" label="E-mail" onChange={(valor) => atualizarCampo("email", valor)} type="email" value={valores.email} />
      <Campo autoComplete="new-password" erro={erros.senha} id="senha-cadastro" label="Senha" onChange={(valor) => atualizarCampo("senha", valor)} type="password" value={valores.senha} />
      <Campo autoComplete="new-password" erro={erros.confirmacaoSenha} id="confirmacao-senha" label="Confirme a senha" onChange={(valor) => atualizarCampo("confirmacaoSenha", valor)} type="password" value={valores.confirmacaoSenha} />
      {mensagem !== null && <p className="form-message form-message--error" role="alert">{mensagem}</p>}
      <button disabled={enviando} type="submit">{enviando ? "Criando conta..." : "Criar conta"}</button>
    </form>
  );
}

/** Define a configuração de um campo de formulário com rótulo e erro associado. */
interface CampoProps {
  autoComplete: string;
  erro?: string;
  id: string;
  label: string;
  onChange: (valor: string) => void;
  type?: "email" | "password" | "text";
  value: string;
}

/**
 * Renderiza um campo semântico e associa seu erro ao controle correspondente.
 *
 * O componente recebe toda a configuração por props, produz label nativo e usa
 * aria-describedby apenas quando há erro. Ele existe para manter a estrutura
 * acessível consistente sem concentrar regras de negócio nos campos.
 */
function Campo({ autoComplete, erro, id, label, onChange, type = "text", value }: CampoProps) {
  const idErro = `${id}-erro`;

  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <input aria-describedby={erro === undefined ? undefined : idErro} aria-invalid={erro === undefined ? undefined : true} autoComplete={autoComplete} id={id} onChange={(evento) => onChange(evento.target.value)} required type={type} value={value} />
      {erro !== undefined && <p className="field__error" id={idErro}>{erro}</p>}
    </div>
  );
}
