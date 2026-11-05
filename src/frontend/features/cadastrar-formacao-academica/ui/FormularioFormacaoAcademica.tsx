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
  validarCurriculoLattes,
  validarFormacaoAcademica,
  validarListaFormacoes,
  type ErrosFormacaoAcademica,
  type ValoresFormacaoAcademica,
} from "../model/formulario-formacao-academica";

/** Define a dependência usada pelo formulário para solicitar o cadastro. */
export interface FormularioFormacaoAcademicaProps {
  cliente: ClienteFormacaoAcademica;
  /** Notifica a porcentagem de campos preenchidos nesta etapa (0 a 100). */
  aoAlterarProgresso?: (progresso: number) => void;
  /** Callback para avançar para a próxima etapa ao salvar. */
  aoAvancar?: () => void;
  /** Valores iniciais opcionais para restauração de estado. */
  formacoesIniciais?: ValoresFormacaoAcademica[];
  /** Callback para retornar para a etapa anterior. */
  onVoltar?: () => void;
  /** Notifica alterações nas formações para preservação de estado. */
  aoAlterarFormacoes?: (formacoes: ValoresFormacaoAcademica[]) => void;
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
 * Renderiza o cadastro acessível de uma ou mais formações acadêmicas.
 *
 * O componente controla valores, erros e estados de envio localmente em lista,
 * permite adicionar e remover entradas de formação dinamicamente e usa o
 * cliente injetado para persistência.
 */
export function FormularioFormacaoAcademica({
  cliente,
  aoAlterarProgresso,
  aoAvancar,
  onVoltar,
  formacoesIniciais = [criarValoresIniciaisFormacao()],
  aoAlterarFormacoes,
}: FormularioFormacaoAcademicaProps) {
  const lattesInicial =
    formacoesIniciais.find((f) => f.curriculoLattes)?.curriculoLattes ?? "";
  const naoPossuiLattesInicial = formacoesIniciais.some(
    (f) => f.naoPossuiLattes,
  );

  const [formacoes, setFormacoes] =
    useState<ValoresFormacaoAcademica[]>(formacoesIniciais);
  const [curriculoLattes, setCurriculoLattes] = useState<string>(lattesInicial);
  const [naoPossuiLattes, setNaoPossuiLattes] = useState<boolean>(
    naoPossuiLattesInicial,
  );
  const [erroLattes, setErroLattes] = useState<string | undefined>(undefined);
  const [erros, setErros] = useState<Record<number, ErrosFormacaoAcademica>>(
    {},
  );
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    const lattesFinal = naoPossuiLattes
      ? undefined
      : curriculoLattes.trim() || undefined;
    const formacoesComLattes = formacoes.map((f) => ({
      ...f,
      curriculoLattes: lattesFinal,
      naoPossuiLattes,
    }));
    aoAlterarFormacoes?.(formacoesComLattes);
  }, [formacoes, curriculoLattes, naoPossuiLattes, aoAlterarFormacoes]);

  const algumMestradoOuDoutorado = formacoes.some(
    (f) => f.nivel === "mestrado" || f.nivel === "doutorado",
  );

  useEffect(() => {
    if (aoAlterarProgresso) {
      if (formacoes.length === 0) {
        aoAlterarProgresso(100);
        return;
      }

      let totalObrigatorios = 0;
      let preenchidos = 0;

      formacoes.forEach((valores) => {
        const ehEnsinoBasico =
          valores.nivel === "ensino_fundamental" ||
          valores.nivel === "ensino_medio";

        totalObrigatorios +=
          (valores.status === "concluido" ? 6 : 5) - (ehEnsinoBasico ? 1 : 0);

        if (valores.instituicao.trim().length > 0) preenchidos++;
        if (!ehEnsinoBasico && valores.curso.trim().length > 0) preenchidos++;
        if (valores.nivel.trim().length > 0) preenchidos++;
        if (valores.dataInicio.trim().length > 0) preenchidos++;
        if (valores.status.trim().length > 0) preenchidos++;
        if (
          valores.status === "concluido" &&
          valores.dataFim.trim().length > 0
        ) {
          preenchidos++;
        }
      });

      const temPos = formacoes.some(
        (f) => f.nivel === "mestrado" || f.nivel === "doutorado",
      );

      if (temPos) {
        totalObrigatorios += 1;
        if (naoPossuiLattes || curriculoLattes.trim().length > 0) {
          preenchidos++;
        }
      }

      const porcentagem =
        totalObrigatorios > 0
          ? Math.round((preenchidos / totalObrigatorios) * 100)
          : 100;
      aoAlterarProgresso(porcentagem);
    }
  }, [formacoes, curriculoLattes, naoPossuiLattes, aoAlterarProgresso]);

  /** Atualiza um campo de uma formação específica e remove seu erro. */
  function atualizarCampo<Campo extends keyof ValoresFormacaoAcademica>(
    indice: number,
    campo: Campo,
    valor: ValoresFormacaoAcademica[Campo],
  ): void {
    setFormacoes((atuais) => {
      const atualizados = atuais.map((item, i) =>
        i === indice ? { ...item, [campo]: valor } : item,
      );
      if (campo === "nivel") {
        const aindaTemPos = atualizados.some(
          (f) => f.nivel === "mestrado" || f.nivel === "doutorado",
        );
        if (!aindaTemPos) {
          setErroLattes((erroAtual) =>
            erroAtual?.includes("ou marque que não possui")
              ? undefined
              : erroAtual,
          );
        }
      }
      return atualizados;
    });
    setErros((atuais) => {
      const errosItem = { ...atuais[indice] };
      delete errosItem[campo];
      const novoMapa = { ...atuais };
      if (Object.keys(errosItem).length === 0) {
        delete novoMapa[indice];
      } else {
        novoMapa[indice] = errosItem;
      }
      return novoMapa;
    });
    setMensagem(null);
  }

  /** Adiciona um novo bloco de formação acadêmica no final da lista. */
  function adicionarFormacao(): void {
    setFormacoes((atuais) => [...atuais, criarValoresIniciaisFormacao()]);
  }

  /** Remove um bloco de formação acadêmica pela sua posição na lista. */
  function removerFormacao(indice: number): void {
    if (formacoes.length <= 1) return;
    setFormacoes((atuais) => atuais.filter((_, i) => i !== indice));
    setErros((atuais) => {
      const novoMapa: Record<number, ErrosFormacaoAcademica> = {};
      Object.entries(atuais).forEach(([chave, valor]) => {
        const idx = Number(chave);
        if (idx < indice) {
          novoMapa[idx] = valor;
        } else if (idx > indice) {
          novoMapa[idx - 1] = valor;
        }
      });
      return novoMapa;
    });
    setMensagem(null);
  }

  /** Valida todas as formações e envia para cadastro. */
  async function enviarFormulario(
    evento: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    evento.preventDefault();
    const novosErros = validarListaFormacoes(formacoes);
    const erroDoLattes = validarCurriculoLattes(
      curriculoLattes,
      naoPossuiLattes,
      algumMestradoOuDoutorado,
    );

    if (erroDoLattes) {
      setErroLattes(erroDoLattes);
    } else {
      setErroLattes(undefined);
    }

    if (Object.keys(novosErros).length > 0 || erroDoLattes) {
      setErros(novosErros);
      setMensagem("Revise os campos destacados antes de continuar.");
      return;
    }

    setEnviando(true);
    setMensagem(null);

    try {
      const lattesFinal = naoPossuiLattes
        ? undefined
        : curriculoLattes.trim() || undefined;

      for (const formacao of formacoes) {
        await cliente.cadastrar(
          criarEntradaFormacaoAcademica({
            ...formacao,
            curriculoLattes: lattesFinal,
            naoPossuiLattes,
          }),
        );
      }
      setMensagem("Formação acadêmica enviada para registro.");
      aoAvancar?.();
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
      {formacoes.map((valores, indice) => {
        const prefixo = `formacao-${indice}`;
        const errosItem = erros[indice] ?? {};
        const ehEnsinoBasico =
          valores.nivel === "ensino_fundamental" ||
          valores.nivel === "ensino_medio";

        return (
          <fieldset
            aria-label={`Formação acadêmica ${indice + 1}`}
            key={`formacao-${indice}`}
          >
            <legend className="sr-only">Formação acadêmica {indice + 1}</legend>
            {formacoes.length > 1 && (
              <div className="item-sublista__topo">
                <span className="label-subtitulo">
                  Formação acadêmica {indice + 1}
                </span>
                <button
                  type="button"
                  className="btn-remover-item"
                  onClick={() => removerFormacao(indice)}
                  aria-label={`Remover Formação acadêmica ${indice + 1}`}
                >
                  Remover
                </button>
              </div>
            )}

            <CampoTexto
              erro={errosItem.instituicao}
              id={`${prefixo}-instituicao`}
              label="Instituição"
              onChange={(valor) => atualizarCampo(indice, "instituicao", valor)}
              placeholder="Ex: USP, FATEC, PUC..."
              required
              value={valores.instituicao}
            />
            <CampoTexto
              ajuda={
                ehEnsinoBasico
                  ? "Opcional. Preencha apenas se houver habilitação específica (ex.: Regular, Técnico integrado)."
                  : undefined
              }
              erro={errosItem.curso}
              id={`${prefixo}-curso`}
              label="Curso"
              onChange={(valor) => atualizarCampo(indice, "curso", valor)}
              placeholder={
                ehEnsinoBasico
                  ? "Opcional (ex.: Regular, Técnico integrado)..."
                  : "Ex: Análise e Desenvolvimento de Sistemas..."
              }
              required={!ehEnsinoBasico}
              value={valores.curso}
            />
            <CampoSelecao
              erro={errosItem.nivel}
              id={`${prefixo}-nivel`}
              label="Nível de formação"
              onChange={(valor) =>
                atualizarCampo(indice, "nivel", valor as NivelFormacaoAcademica)
              }
              opcoes={niveis}
              required
              value={valores.nivel}
            />
            <CampoData
              erro={errosItem.dataInicio}
              id={`${prefixo}-data-inicio`}
              label="Data de início"
              onChange={(valor) => atualizarCampo(indice, "dataInicio", valor)}
              required
              value={valores.dataInicio}
            />
            <CampoSelecao
              erro={errosItem.status}
              id={`${prefixo}-status`}
              label="Situação"
              onChange={(valor) =>
                atualizarCampo(
                  indice,
                  "status",
                  valor as StatusFormacaoAcademica,
                )
              }
              opcoes={situacoes}
              required
              value={valores.status}
            />
            <CampoData
              ajuda="Para formação em andamento, informe a previsão de conclusão se ela estiver disponível."
              erro={errosItem.dataFim}
              id={`${prefixo}-data-fim`}
              label={
                valores.status === "concluido"
                  ? "Data de conclusão"
                  : "Data final ou previsão de conclusão"
              }
              onChange={(valor) => atualizarCampo(indice, "dataFim", valor)}
              required={valores.status === "concluido"}
              value={valores.dataFim}
            />
          </fieldset>
        );
      })}

      <button
        type="button"
        className="btn-adicionar-item"
        onClick={adicionarFormacao}
      >
        + Adicionar formação acadêmica
      </button>

      <div className="secao-lattes">
        <CampoTexto
          ajuda={
            algumMestradoOuDoutorado
              ? naoPossuiLattes
                ? "Opção de dispensa selecionada para pós-graduação acadêmica."
                : "Obrigatório para pós-graduação acadêmica (Mestrado e Doutorado)."
              : "Opcional. Informe caso possua cadastro na Plataforma Lattes."
          }
          disabled={naoPossuiLattes}
          erro={erroLattes}
          id="curriculo-lattes"
          label="Currículo Lattes"
          onChange={(valor) => {
            setCurriculoLattes(valor);
            setErroLattes(undefined);
            setMensagem(null);
          }}
          placeholder={
            naoPossuiLattes
              ? "Não possuo Currículo Lattes"
              : "http://lattes.cnpq.br/..."
          }
          required={algumMestradoOuDoutorado && !naoPossuiLattes}
          type="url"
          value={naoPossuiLattes ? "" : curriculoLattes}
        />
        {algumMestradoOuDoutorado && (
          <div className="campo-dispensa-lattes">
            <label className="checkbox-lattes-label" htmlFor="dispensa-lattes">
              <input
                checked={naoPossuiLattes}
                id="dispensa-lattes"
                onChange={(evento) => {
                  const marcado = evento.target.checked;
                  setNaoPossuiLattes(marcado);
                  if (marcado) {
                    setCurriculoLattes("");
                    setErroLattes(undefined);
                  }
                  setMensagem(null);
                }}
                type="checkbox"
              />
              <span>Não possuo Currículo Lattes</span>
            </label>
          </div>
        )}
      </div>

      {mensagem !== null && (
        <p
          className="form-message"
          role={mensagem.startsWith("Formação") ? "status" : "alert"}
        >
          {mensagem}
        </p>
      )}
      <div className="botoes-navegacao">
        {onVoltar && (
          <button
            type="button"
            className="btn-voltar"
            onClick={onVoltar}
            aria-label="Voltar para a etapa anterior"
          >
            Voltar
          </button>
        )}
        <button
          aria-label={enviando ? "Enviando..." : "Cadastrar formação"}
          className="btn-proximo"
          disabled={enviando}
          type="submit"
        >
          {enviando ? "Enviando..." : "Próximo"}
        </button>
      </div>
    </form>
  );
}

/** Define os dados comuns de um campo textual ou de data obrigatório. */
interface CampoBaseProps {
  ajuda?: string;
  disabled?: boolean;
  erro?: string;
  id: string;
  label: string;
  placeholder?: string;
  required?: boolean;
  value: string;
}

/** Renderiza um campo textual com rótulo, ajuda opcional e erro associado. */
function CampoTexto({
  ajuda,
  disabled = false,
  erro,
  id,
  label,
  onChange,
  placeholder,
  required = true,
  type = "text",
  value,
}: CampoBaseProps & { onChange: (valor: string) => void; type?: string }) {
  const idErro = `${id}-erro`;
  const idAjuda = `${id}-ajuda`;
  return (
    <div className={`field ${disabled ? "field--disabled" : ""}`}>
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
        disabled={disabled}
        id={id}
        maxLength={200}
        onChange={(evento) => onChange(evento.target.value)}
        placeholder={placeholder}
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
