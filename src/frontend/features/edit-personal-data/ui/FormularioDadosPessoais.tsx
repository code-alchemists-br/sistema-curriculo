import { useRef, useState, type FormEvent } from "react";

import {
  FalhaDadosPessoais,
  type ClienteDadosPessoais,
} from "../api/cliente-dados-pessoais";
import {
  criarStudent,
  criarValoresIniciais,
  traduzirFalhaDadosPessoais,
  validarDadosPessoais,
  type ErrosDadosPessoais,
  type ValoresDadosPessoais,
} from "../model/formulario-dados-pessoais";

/** Define o cliente usado para manter os dados pessoais do estudante. */
export interface FormularioDadosPessoaisProps {
  cliente: ClienteDadosPessoais;
}

/** Renderiza e controla o formulário de dados pessoais e contato. */
export function FormularioDadosPessoais({
  cliente,
}: FormularioDadosPessoaisProps) {
  const [valores, setValores] =
    useState<ValoresDadosPessoais>(criarValoresIniciais);
  const [erros, setErros] = useState<ErrosDadosPessoais>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const focoNoNovoTelefone = useRef(false);

  /** Move o foco para o telefone recém-adicionado, depois que ele for renderizado. */
  function definirUltimoTelefone(elemento: HTMLInputElement | null): void {
    if (elemento !== null && focoNoNovoTelefone.current) {
      elemento.focus();
      focoNoNovoTelefone.current = false;
    }
  }

  /** Atualiza um campo simples e remove o feedback anterior daquele campo. */
  function atualizarCampo(
    campo: Exclude<keyof ValoresDadosPessoais, "telefones">,
    valor: string,
  ): void {
    setValores((atuais) => ({ ...atuais, [campo]: valor }));
    setErros((atuais) => ({ ...atuais, [campo]: undefined }));
    setMensagem(null);
  }

  /** Atualiza um telefone específico e remove somente seu erro associado. */
  function atualizarTelefone(indice: number, telefone: string): void {
    setValores((atuais) => ({
      ...atuais,
      telefones: atuais.telefones.map((valor, indiceAtual) =>
        indiceAtual === indice ? telefone : valor,
      ),
    }));
    setErros((atuais) => {
      const errosDeTelefone = { ...atuais.telefones };
      delete errosDeTelefone[indice];

      return {
        ...atuais,
        telefones:
          Object.keys(errosDeTelefone).length === 0
            ? undefined
            : errosDeTelefone,
      };
    });
    setMensagem(null);
  }

  /** Inclui um novo telefone e sinaliza que ele deve receber foco. */
  function adicionarTelefone(): void {
    focoNoNovoTelefone.current = true;
    setValores((atuais) => ({
      ...atuais,
      telefones: [...atuais.telefones, ""],
    }));
  }

  /** Valida e salva os dados, preservando os valores para uma tentativa posterior em caso de falha. */
  async function enviarFormulario(
    evento: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    evento.preventDefault();
    const novosErros = validarDadosPessoais(valores);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      return;
    }

    setEnviando(true);
    setMensagem(null);

    try {
      await cliente.salvar(criarStudent(valores));
      setMensagem("Dados pessoais salvos com sucesso.");
    } catch (erro: unknown) {
      const codigo =
        erro instanceof FalhaDadosPessoais ? erro.codigo : "resposta-invalida";
      setMensagem(traduzirFalhaDadosPessoais(codigo));
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form aria-busy={enviando} noValidate onSubmit={enviarFormulario}>
      <CampoTexto
        erro={erros.nomeCompleto}
        id="nome-completo"
        label="Nome completo"
        onChange={(valor) => atualizarCampo("nomeCompleto", valor)}
        required
        value={valores.nomeCompleto}
      />
      <CampoTexto
        erro={erros.enderecoCompleto}
        id="endereco-completo"
        label="Endereço completo"
        onChange={(valor) => atualizarCampo("enderecoCompleto", valor)}
        required
        value={valores.enderecoCompleto}
      />
      <div className="field">
        <span>Telefones</span>
        {valores.telefones.map((telefone, indice) => {
          const id = `telefone-${indice}`;
          const erro = erros.telefones?.[indice];
          const idErro = `${id}-erro`;
          const eUltimoTelefone = indice === valores.telefones.length - 1;

          return (
            <div key={id}>
              <label htmlFor={id}>Telefone {indice + 1}</label>
              <input
                aria-describedby={erro === undefined ? undefined : idErro}
                aria-invalid={erro === undefined ? undefined : true}
                autoComplete="tel"
                id={id}
                onChange={(evento) =>
                  atualizarTelefone(indice, evento.target.value)
                }
                ref={eUltimoTelefone ? definirUltimoTelefone : undefined}
                required
                type="tel"
                value={telefone}
              />
              {erro !== undefined && (
                <p className="field__error" id={idErro}>
                  {erro}
                </p>
              )}
            </div>
          );
        })}
        <button onClick={adicionarTelefone} type="button">
          + Adicionar telefone
        </button>
      </div>
      <CampoTexto
        erro={erros.email}
        id="email"
        label="E-mail"
        onChange={(valor) => atualizarCampo("email", valor)}
        required
        type="email"
        value={valores.email}
      />
      <CampoTexto
        ajuda="Informe o endereço público do seu perfil profissional, se possuir um."
        id="linkedin"
        label="LinkedIn (opcional)"
        onChange={(valor) => atualizarCampo("linkedIn", valor)}
        type="url"
        value={valores.linkedIn}
      />
      <CampoTexto
        ajuda="Informe o endereço público do seu currículo na Plataforma Lattes, se possuir um."
        id="curriculo-lattes"
        label="Currículo Lattes (opcional)"
        onChange={(valor) => atualizarCampo("curriculoLattes", valor)}
        type="url"
        value={valores.curriculoLattes}
      />
      {enviando && <p role="status">Salvando dados pessoais...</p>}
      {mensagem !== null && (
        <p
          className="form-message"
          role={mensagem.includes("sucesso") ? "status" : "alert"}
        >
          {mensagem}
        </p>
      )}
      <button disabled={enviando} type="submit">
        {enviando ? "Salvando dados..." : "Salvar dados pessoais"}
      </button>
    </form>
  );
}

/** Define os valores de um campo textual do formulário. */
interface CampoTextoProps {
  ajuda?: string;
  erro?: string;
  id: string;
  label: string;
  onChange: (valor: string) => void;
  required?: boolean;
  type?: "email" | "text" | "url";
  value: string;
}

/** Renderiza um campo textual, incluindo ajuda e feedback de erro acessíveis. */
function CampoTexto({
  ajuda,
  erro,
  id,
  label,
  onChange,
  required = false,
  type = "text",
  value,
}: CampoTextoProps) {
  const idErro = `${id}-erro`;
  const idAjuda = `${id}-ajuda`;

  return (
    <div className="field">
      <label htmlFor={id}>
        {label}
        {ajuda !== undefined && (
          <span
            aria-describedby={idAjuda}
            aria-label={`Ajuda: ${ajuda}`}
            title={ajuda}
          >
            {" "}
            ?
          </span>
        )}
      </label>
      {ajuda !== undefined && (
        <span hidden id={idAjuda}>
          {ajuda}
        </span>
      )}
      <input
        aria-describedby={erro === undefined ? undefined : idErro}
        aria-invalid={erro === undefined ? undefined : true}
        id={id}
        onChange={(evento) => onChange(evento.target.value)}
        required={required}
        type={type}
        value={value}
      />
      {erro !== undefined && (
        <p className="field__error" id={idErro}>
          {erro}
        </p>
      )}
    </div>
  );
}
