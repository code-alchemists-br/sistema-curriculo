import { useEffect, useState, type FormEvent } from "react";

import "./FormularioFormacaoAcademica.css";

import {
  FalhaFormacaoAcademica,
  type ClienteFormacaoAcademica,
  type NivelFormacaoAcademica,
  type StatusFormacaoAcademica,
} from "../api/cliente-formacao-academica";
import {
  criarEntradaFormacaoAcademica,
  criarValoresIniciaisFormacao,
  traduzirFalhaFormacaoAcademica,
  validarFormacaoAcademica,
  type ErrosFormacaoAcademica,
  type ValoresFormacaoAcademica,
} from "../model/formulario-formacao-academica";

/** Define a dependência usada pelo formulário para solicitar o cadastro. */
export interface FormularioFormacaoAcademicaProps {
  cliente: ClienteFormacaoAcademica;
  /** Notifica a porcentagem de campos preenchidos nesta etapa (0 a 100). */
  aoAlterarProgresso?: (progresso: number) => void;
}

const niveis: ReadonlyArray<{ valor: NivelFormacaoAcademica; rotulo: string }> =
  [
    { valor: "ensino_fundamental", rotulo: "Ensino fundamental" },
    { valor: "ensino_medio", rotulo: "Ensino médio" },
    { valor: "tecnico", rotulo: "Técnico" },
    { valor: "tecnologo", rotulo: "Tecnólogo" },
    { valor: "graduacao", rotulo: "Graduação" },
    { valor: "especializacao", rotulo: "Especialização" },
    { valor: "mestrado", rotulo: "Mestrado" },
    { valor: "doutorado", rotulo: "Doutorado" },
  ];

const situacoes: ReadonlyArray<{
  valor: StatusFormacaoAcademica;
  rotulo: string;
}> = [
  { valor: "em_andamento", rotulo: "Em andamento" },
  { valor: "concluido", rotulo: "Concluído" },
  { valor: "interrompido", rotulo: "Interrompido" },
];

/**
 * Renderiza o cadastro acessível de uma formação acadêmica.
 *
 * O componente controla valores, erros e estados de envio localmente, e usa o
 * cliente injetado para manter a interface livre de HTTP. Ele existe para
 * permitir testar o preenchimento e substituir a integração futuramente.
 */
export function FormularioFormacaoAcademica({
  cliente,
  aoAlterarProgresso,
}: FormularioFormacaoAcademicaProps) {
  const [valores, setValores] = useState<ValoresFormacaoAcademica>(
    criarValoresIniciaisFormacao,
  );
  const [erros, setErros] = useState<ErrosFormacaoAcademica>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    if (aoAlterarProgresso) {
      let preenchidos = 0;
      const totalObrigatorios = valores.status === "concluido" ? 6 : 5;
      if (valores.instituicao.trim().length > 0) preenchidos++;
      if (valores.curso.trim().length > 0) preenchidos++;
      if (valores.nivel.trim().length > 0) preenchidos++;
      if (valores.dataInicio.trim().length > 0) preenchidos++;
      if (valores.status.trim().length > 0) preenchidos++;
      if (valores.status === "concluido" && valores.dataFim.trim().length > 0) {
        preenchidos++;
      }

      const porcentagem = Math.round((preenchidos / totalObrigatorios) * 100);
      aoAlterarProgresso(porcentagem);
    }
  }, [valores, aoAlterarProgresso]);

  /** Atualiza um campo e remove apenas o feedback anterior desse campo. */
  function atualizarCampo<Campo extends keyof ValoresFormacaoAcademica>(
    campo: Campo,
    valor: ValoresFormacaoAcademica[Campo],
  ): void {
    setValores((atuais) => ({ ...atuais, [campo]: valor }));
    setErros((atuais) => ({ ...atuais, [campo]: undefined }));
    setMensagem(null);
  }

  /** Valida os dados e solicita o cadastro sem apagar valores em caso de falha. */
  async function enviarFormulario(
    evento: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    evento.preventDefault();
    const novosErros = validarFormacaoAcademica(valores);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      setMensagem("Revise os campos destacados antes de continuar.");
      return;
    }

    setEnviando(true);
    setMensagem(null);

    try {
      await cliente.cadastrar(criarEntradaFormacaoAcademica(valores));
      setMensagem("Formação acadêmica enviada para registro.");
    } catch (erro: unknown) {
      setMensagem(
        traduzirFalhaFormacaoAcademica(
          erro instanceof FalhaFormacaoAcademica ? erro.codigo : "rede",
        ),
      );
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form
      aria-busy={enviando}
      className="formulario-formacao-academica"
      noValidate
      onSubmit={enviarFormulario}
    >
      <CampoTexto
        erro={erros.instituicao}
        id="instituicao-formacao"
        label="Instituição"
        onChange={(valor) => atualizarCampo("instituicao", valor)}
        placeholder="Ex: USP, FATEC, PUC..."
        required
        value={valores.instituicao}
      />
      <CampoTexto
        erro={erros.curso}
        id="curso-formacao"
        label="Curso"
        onChange={(valor) => atualizarCampo("curso", valor)}
        placeholder="Ex: Análise e Desenvolvimento de Sistemas..."
        required
        value={valores.curso}
      />
      <CampoSelecao
        erro={erros.nivel}
        id="nivel-formacao"
        label="Nível de formação"
        onChange={(valor) =>
          atualizarCampo("nivel", valor as NivelFormacaoAcademica)
        }
        opcoes={niveis}
        required
        value={valores.nivel}
      />
      <CampoData
        erro={erros.dataInicio}
        id="data-inicio-formacao"
        label="Data de início"
        onChange={(valor) => atualizarCampo("dataInicio", valor)}
        required
        value={valores.dataInicio}
      />
      <CampoSelecao
        erro={erros.status}
        id="status-formacao"
        label="Situação"
        onChange={(valor) =>
          atualizarCampo("status", valor as StatusFormacaoAcademica)
        }
        opcoes={situacoes}
        required
        value={valores.status}
      />
      <CampoData
        ajuda="Para formação em andamento, informe a previsão de conclusão se ela estiver disponível."
        erro={erros.dataFim}
        id="data-fim-formacao"
        label={
          valores.status === "concluido"
            ? "Data de conclusão"
            : "Data final ou previsão de conclusão"
        }
        onChange={(valor) => atualizarCampo("dataFim", valor)}
        required={valores.status === "concluido"}
        value={valores.dataFim}
      />
      {mensagem !== null && (
        <p
          className="form-message"
          role={mensagem.startsWith("Formação") ? "status" : "alert"}
        >
          {mensagem}
        </p>
      )}
      <button
        aria-label={enviando ? "Enviando..." : "Cadastrar formação"}
        className="btn-proximo"
        disabled={enviando}
        type="submit"
      >
        {enviando ? "Enviando..." : "Próximo"}
      </button>
    </form>
  );
}

/** Define os dados comuns de um campo textual ou de data obrigatório. */
interface CampoBaseProps {
  ajuda?: string;
  erro?: string;
  id: string;
  label: string;
  placeholder?: string;
  required?: boolean;
  value: string;
}

/** Renderiza um campo textual com rótulo e erro associado. */
function CampoTexto({
  erro,
  id,
  label,
  onChange,
  placeholder,
  required = true,
  value,
}: CampoBaseProps & { onChange: (valor: string) => void }) {
  const idErro = `${id}-erro`;
  return (
    <div className="field">
      <label
        htmlFor={id}
        className={`titulo-campo ${required ? "titulo-campo--obrigatorio" : ""}`}
      >
        {label}
      </label>
      <input
        aria-describedby={erro === undefined ? undefined : idErro}
        aria-invalid={erro === undefined ? undefined : true}
        id={id}
        maxLength={200}
        onChange={(evento) => onChange(evento.target.value)}
        placeholder={placeholder}
        required={required}
        type="text"
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

/** Renderiza uma lista de seleção com opção inicial vazia e erro associado. */
function CampoSelecao({
  erro,
  id,
  label,
  onChange,
  opcoes,
  required = true,
  value,
}: CampoBaseProps & {
  onChange: (valor: string) => void;
  opcoes: ReadonlyArray<{ valor: string; rotulo: string }>;
}) {
  const idErro = `${id}-erro`;
  return (
    <div className="field">
      <label
        htmlFor={id}
        className={`titulo-campo ${required ? "titulo-campo--obrigatorio" : ""}`}
      >
        {label}
      </label>
      <select
        aria-describedby={erro === undefined ? undefined : idErro}
        aria-invalid={erro === undefined ? undefined : true}
        id={id}
        onChange={(evento) => onChange(evento.target.value)}
        required={required}
        value={value}
      >
        <option value="">Selecione uma opção</option>
        {opcoes.map((opcao) => (
          <option key={opcao.valor} value={opcao.valor}>
            {opcao.rotulo}
          </option>
        ))}
      </select>
      {erro !== undefined && (
        <p className="field__error" id={idErro}>
          {erro}
        </p>
      )}
    </div>
  );
}

/** Renderiza um campo de data, com ajuda opcional e mensagem de erro associada. */
function CampoData({
  ajuda,
  erro,
  id,
  label,
  onChange,
  required = false,
  value,
}: CampoBaseProps & { onChange: (valor: string) => void }) {
  const idErro = `${id}-erro`;
  const idAjuda = `${id}-ajuda`;
  return (
    <div className="field">
      <label
        htmlFor={id}
        className={`titulo-campo ${required ? "titulo-campo--obrigatorio" : ""}`}
      >
        {label}
      </label>
      {ajuda !== undefined && (
        <p className="field__ajuda" id={idAjuda}>
          {ajuda}
        </p>
      )}
      <input
        aria-describedby={
          [
            ajuda === undefined ? undefined : idAjuda,
            erro === undefined ? undefined : idErro,
          ]
            .filter(Boolean)
            .join(" ") || undefined
        }
        aria-invalid={erro === undefined ? undefined : true}
        id={id}
        onChange={(evento) => onChange(evento.target.value)}
        required={required}
        type="date"
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
