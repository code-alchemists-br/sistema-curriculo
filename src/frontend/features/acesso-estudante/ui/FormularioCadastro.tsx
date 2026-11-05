// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
import { useState, type FormEvent } from "react";

import {
  FalhaAcessoEstudante,
  type ClienteAcessoEstudante,
} from "../api/cliente-acesso-estudante";
import {
  traduzirFalhaAcesso,
  validarCadastro,
  type ErrosFormulario,
  type ValoresCadastro,
} from "../model/formulario-acesso";
import { BotaoHero } from "../../../shared";
import "./FormularioCadastro.css";

/** Define os colaboradores e a consequência local de um cadastro concluído. */
export interface FormularioCadastroProps {
  cliente: ClienteAcessoEstudante;
  aoCadastrar: (email: string, nome?: string) => void;
  emailInicial?: string;
  aoAlterarEmail?: (email: string) => void;
}

const valoresIniciais: ValoresCadastro = {
  nome: "",
  email: "",
  senha: "",
  confirmacaoSenha: "",
};

/**
 * Renderiza e controla o formulário isolado de criação de conta.
 *
 * O componente mantém valores e erros locais, valida antes do envio e chama o
 * contrato injetado, sem conhecer fetch ou status HTTP. Ele existe para permitir
 * o cadastro acessível e testável enquanto o backend é substituído por doubles.
 */
export function FormularioCadastro({
  cliente,
  aoCadastrar,
  emailInicial,
  aoAlterarEmail,
}: FormularioCadastroProps) {
  const [valores, setValores] = useState<ValoresCadastro>(() => ({
    ...valoresIniciais,
    email: emailInicial || "",
  }));
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [mostrarConfirmacao, setMostrarConfirmacao] = useState(false);
  const [erros, setErros] = useState<ErrosFormulario>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  /** Atualiza somente o campo alterado e remove seu feedback anterior. */
  function atualizarCampo(campo: keyof ValoresCadastro, valor: string): void {
    setValores((atuais) => ({ ...atuais, [campo]: valor }));
    setErros((atuais) => ({ ...atuais, [campo]: undefined }));
    setMensagem(null);
    if (campo === "email") {
      aoAlterarEmail?.(valor);
    }
  }

  /**
   * Valida e submete os dados de cadastro comunicando feedbacks acessíveis.
   *
   * O manipulador interrompe o envio nativo do formulário, valida os valores
   * via `validarCadastro`, emite alerta sonoro acessível via live region quando
   * há pendências locais e, em caso de sucesso, delega a criação ao cliente injetado.
   * Ele existe para coordenar o fluxo acessível de criação de conta sem acoplar a
   * interface ao transporte HTTP.
   */
  async function enviarCadastro(
    evento: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    evento.preventDefault();
    const novosErros = validarCadastro(valores);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      setMensagem(
        "Há pendências que precisam ser corrigidas antes de criar a conta.",
      );
      return;
    }

    setEnviando(true);
    setMensagem(null);

    try {
      const estudante = await cliente.cadastrar({
        nome: valores.nome.trim(),
        email: valores.email.trim(),
        senha: valores.senha,
      });

      setValores(valoresIniciais);
      aoCadastrar(estudante.email, estudante.nome);
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
    <form className="formulario-cadastro" noValidate onSubmit={enviarCadastro}>
      <Campo
        autoComplete="name"
        erro={erros.nome}
        id="nome"
        label="Nome"
        onChange={(valor) => atualizarCampo("nome", valor)}
        value={valores.nome}
      />
      <Campo
        autoComplete="email"
        erro={erros.email}
        id="email-cadastro"
        label="E-mail"
        onChange={(valor) => atualizarCampo("email", valor)}
        type="email"
        value={valores.email}
      />
      <Campo
        autoComplete="new-password"
        dica="Mínimo de 8 caracteres."
        erro={erros.senha}
        id="senha-cadastro"
        label="Senha"
        mostrarAlternadorSenha
        onAlternarVisibilidadeSenha={() => setMostrarSenha((v) => !v)}
        onChange={(valor) => atualizarCampo("senha", valor)}
        senhaVisivel={mostrarSenha}
        type="password"
        value={valores.senha}
      />
      <Campo
        autoComplete="new-password"
        erro={erros.confirmacaoSenha}
        id="confirmacao-senha"
        label="Confirme a senha"
        mostrarAlternadorSenha
        onAlternarVisibilidadeSenha={() => setMostrarConfirmacao((v) => !v)}
        onChange={(valor) => atualizarCampo("confirmacaoSenha", valor)}
        senhaVisivel={mostrarConfirmacao}
        type="password"
        value={valores.confirmacaoSenha}
      />
      {mensagem !== null && (
        <p className="form-message form-message--error" role="alert">
          {mensagem}
        </p>
      )}
      <BotaoHero
        disabled={enviando}
        mostrarIcone={false}
        type="submit"
        wrapperClassName="formulario-cadastro__botao-wrapper botao-hero-wrapper--full-width"
      >
        {enviando ? "Criando conta..." : "Criar conta"}
      </BotaoHero>
    </form>
  );
}

/** Define a configuração de um campo de formulário com rótulo e erro associado. */
interface CampoProps {
  autoComplete: string;
  dica?: string;
  erro?: string;
  id: string;
  label: string;
  mostrarAlternadorSenha?: boolean;
  onAlternarVisibilidadeSenha?: () => void;
  onChange: (valor: string) => void;
  senhaVisivel?: boolean;
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
function Campo({
  autoComplete,
  dica,
  erro,
  id,
  label,
  mostrarAlternadorSenha,
  onAlternarVisibilidadeSenha,
  onChange,
  senhaVisivel,
  type = "text",
  value,
}: CampoProps) {
  const idErro = `${id}-erro`;
  const tipoInput = mostrarAlternadorSenha
    ? senhaVisivel
      ? "text"
      : "password"
    : type;

  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <div className="field__input-container">
        <input
          aria-describedby={erro === undefined ? undefined : idErro}
          aria-invalid={erro === undefined ? undefined : true}
          autoComplete={autoComplete}
          id={id}
          onChange={(evento) => onChange(evento.target.value)}
          required
          type={tipoInput}
          value={value}
        />
        {mostrarAlternadorSenha && (
          <button
            type="button"
            className="field__btn-toggle-senha"
            onClick={onAlternarVisibilidadeSenha}
            tabIndex={-1}
            aria-label={
              senhaVisivel
                ? `Ocultar ${label.toLowerCase()}`
                : `Mostrar ${label.toLowerCase()}`
            }
            title={senhaVisivel ? "Ocultar senha" : "Ver senha"}
          >
            {senhaVisivel ? (
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
        )}
      </div>
      {dica && !erro && <span className="field__hint">{dica}</span>}
      {erro !== undefined && (
        <p className="field__error" id={idErro}>
          {erro}
        </p>
      )}
    </div>
  );
}
