// Proveniência: decision-analysis prompts/frontend/20260921-120136-tela-cadastro-projetos-academicos-v001.md#v001
import { useState, type FormEvent } from "react";

import { FalhaCadastroProjeto, type ClienteProjetosAcademicos } from "../api/cliente-projetos-academicos";
import {
  traduzirFalhaCadastroProjeto,
  validarProjetoAcademico,
  type ErrosProjetoAcademico,
  type ValoresProjetoAcademico
} from "../model/formulario-projeto-academico";

/** Define o cliente usado pelo formulário de cadastro de projeto acadêmico. */
export interface FormularioCadastroProjetoAcademicoProps {
  cliente: ClienteProjetosAcademicos;
}

const valoresIniciais: ValoresProjetoAcademico = {
  titulo: "",
  descricao: "",
  tecnologias: ""
};

/**
 * Renderiza e controla a entrada de um projeto acadêmico do estudante.
 *
 * O componente mantém valores e feedback no estado local, valida antes de
 * chamar o cliente injetado e preserva o formulário em falhas. Ele existe para
 * oferecer o cadastro acessível sem conhecer HTTP, usuário autenticado ou banco.
 */
export function FormularioCadastroProjetoAcademico({
  cliente
}: FormularioCadastroProjetoAcademicoProps) {
  const [valores, setValores] = useState(valoresIniciais);
  const [erros, setErros] = useState<ErrosProjetoAcademico>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  /** Atualiza um valor e remove feedback que já não descreve o campo editado. */
  function atualizarCampo(campo: keyof ValoresProjetoAcademico, valor: string): void {
    setValores((atuais) => ({ ...atuais, [campo]: valor }));
    setErros((atuais) => ({ ...atuais, [campo]: undefined }));
    setMensagem(null);
  }

  /**
   * Valida e encaminha o projeto pelo contrato injetado da feature.
   *
   * O manipulador evita o submit nativo, envia somente os três valores do
   * projeto e distingue sucesso de falhas controladas. Ele existe para manter
   * regras de experiência na feature e transporte fora do componente visual.
   */
  async function enviarProjeto(evento: FormEvent<HTMLFormElement>): Promise<void> {
    evento.preventDefault();
    const novosErros = validarProjetoAcademico(valores);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      return;
    }

    setEnviando(true);
    setMensagem(null);

    try {
      await cliente.cadastrar({
        titulo: valores.titulo.trim(),
        descricao: valores.descricao.trim(),
        tecnologias: valores.tecnologias.trim()
      });
      setValores(valoresIniciais);
      setMensagem("Dados do projeto enviados para processamento.");
    } catch (erro: unknown) {
      setMensagem(
        traduzirFalhaCadastroProjeto(
          erro instanceof FalhaCadastroProjeto ? erro.codigo : "resposta-invalida"
        )
      );
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form noValidate onSubmit={enviarProjeto}>
      <CampoTexto
        erro={erros.titulo}
        id="titulo-projeto"
        label="Título do projeto"
        onChange={(valor) => atualizarCampo("titulo", valor)}
        value={valores.titulo}
      />
      <CampoTexto
        erro={erros.descricao}
        id="descricao-projeto"
        label="Descrição"
        multiline
        onChange={(valor) => atualizarCampo("descricao", valor)}
        value={valores.descricao}
      />
      <CampoTexto
        erro={erros.tecnologias}
        id="tecnologias-projeto"
        label="Tecnologias utilizadas"
        onChange={(valor) => atualizarCampo("tecnologias", valor)}
        value={valores.tecnologias}
      />
      {mensagem !== null && (
        <p className="form-message" role={mensagem.includes("processamento") ? "status" : "alert"}>
          {mensagem}
        </p>
      )}
      <button disabled={enviando} type="submit">
        {enviando ? "Enviando projeto..." : "Cadastrar projeto"}
      </button>
    </form>
  );
}

/** Define a configuração de campo textual do formulário de projeto. */
interface CampoTextoProps {
  erro?: string;
  id: string;
  label: string;
  multiline?: boolean;
  onChange: (valor: string) => void;
  value: string;
}

/**
 * Renderiza um campo textual com rótulo e erro acessivelmente associado.
 *
 * O componente escolhe input ou textarea conforme o conteúdo, mantendo o
 * mesmo vínculo semântico com o erro. Ele existe para reduzir repetição visual
 * sem mover validações ou regras de projeto para uma camada de UI genérica.
 */
function CampoTexto({ erro, id, label, multiline = false, onChange, value }: CampoTextoProps) {
  const idErro = `${id}-erro`;
  const atributosDeAcesso = {
    "aria-describedby": erro === undefined ? undefined : idErro,
    "aria-invalid": erro === undefined ? undefined : true
  };

  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      {multiline ? (
        <textarea {...atributosDeAcesso} id={id} onChange={(evento) => onChange(evento.target.value)} required rows={5} value={value} />
      ) : (
        <input {...atributosDeAcesso} id={id} onChange={(evento) => onChange(evento.target.value)} type="text" value={value} />
      )}
      {erro !== undefined && <p className="field__error" id={idErro}>{erro}</p>}
    </div>
  );
}
