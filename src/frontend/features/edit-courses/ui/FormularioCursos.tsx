import {
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
  type FormEvent,
  type Ref,
} from "react";

import {
  LIMITES_CURSO,
  criarCursoVazio,
  cursoEstaVazio,
  normalizarCurso,
  validarCurso,
  type Curso,
  type ErrosCurso,
} from "../model/cursos";
import "./FormularioCursos.css";

/** Define os valores iniciais e o callback de persistência da tela. */
export interface FormularioCursosProps {
  /** Encaminha o submit ao coordenador da página para não anunciar persistência local como remota. */
  aoAvancar?: () => void | Promise<void>;
  /** Valida e normaliza os dados para a página impedir avanço com entradas parciais. */
  ref?: Ref<{ validar: () => Curso[] | null }>;
  /** Ignora somente entradas inteiramente vazias nas etapas opcionais. */
  permitirVazios?: boolean;
  /** Impede alterações enquanto a página aguarda persistência. */
  desabilitado?: boolean;
  cursosIniciais?: Curso[];
  onSalvar?: (cursos: Curso[]) => void;
  /** Notifica a porcentagem de campos preenchidos nesta seção (0 a 100). */
  aoAlterarProgresso?: (progresso: number) => void;
  /** Notifica alterações nos cursos para preservação de estado. */
  aoAlterarCursos?: (cursos: Curso[]) => void;
  /** Controla a exibição do botão interno de salvar (padrão: true). */
  exibirBotaoSalvar?: boolean;
}

/**
 * Renderiza e controla o formulário de cadastro de cursos e certificações.
 *
 * O componente mantém um array de cursos no estado local, permite adicionar
 * e remover entradas dinamicamente, e valida todos os itens antes de chamar
 * o callback de persistência. Ele existe para isolar a lógica de cadastro
 * de cursos sem depender de HTTP ou backend.
 */
export function FormularioCursos({
  aoAvancar,
  ref,
  permitirVazios = false,
  desabilitado = false,
  cursosIniciais = [criarCursoVazio()],
  onSalvar,
  aoAlterarProgresso,
  aoAlterarCursos,
  exibirBotaoSalvar = true,
}: FormularioCursosProps) {
  const [cursos, setCursos] = useState<Curso[]>(cursosIniciais);
  const [erros, setErros] = useState<Record<number, ErrosCurso>>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const formularioRef = useRef<HTMLFormElement>(null);
  const focarErro = useRef(false);

  useImperativeHandle(ref, () => ({ validar: validarFormulario }));

  useEffect(() => {
    if (focarErro.current) {
      formularioRef.current
        ?.querySelector<HTMLElement>('[aria-invalid="true"]')
        ?.focus();
      focarErro.current = false;
    }
  }, [erros]);

  const [cursoRemovido, setCursoRemovido] = useState<{
    item: Curso;
    indice: number;
  } | null>(null);

  useEffect(() => {
    if (cursoRemovido) {
      const timer = setTimeout(() => {
        setCursoRemovido(null);
      }, 7000);
      return () => clearTimeout(timer);
    }
  }, [cursoRemovido]);

  useEffect(() => {
    aoAlterarCursos?.(cursos);
  }, [cursos, aoAlterarCursos]);

  useEffect(() => {
    if (!aoAlterarProgresso) return;
    if (cursos.length === 0) {
      aoAlterarProgresso(0);
      return;
    }

    let totalCampos = 0;
    let preenchidos = 0;

    cursos.forEach((c) => {
      totalCampos += 3;
      if (c.nome.trim().length > 0) preenchidos++;
      if (c.instituicao.trim().length > 0) preenchidos++;
      if (c.cargaHoraria.trim().length > 0) preenchidos++;
    });

    const porcentagem =
      totalCampos > 0 ? Math.round((preenchidos / totalCampos) * 100) : 0;
    aoAlterarProgresso(porcentagem);
  }, [cursos, aoAlterarProgresso]);

  /** Atualiza um campo específico de um curso pela sua posição no array. */
  function atualizarCurso(
    indice: number,
    campo: keyof Curso,
    valor: string,
  ): void {
    setCursos((atuais) =>
      atuais.map((curso, i) =>
        i === indice ? { ...curso, [campo]: valor } : curso,
      ),
    );
    setErros((atuais) => {
      const errosCurso = { ...atuais[indice] };
      delete errosCurso[campo];
      const novoMapa = { ...atuais };

      if (Object.keys(errosCurso).length === 0) {
        delete novoMapa[indice];
      } else {
        novoMapa[indice] = errosCurso;
      }

      return novoMapa;
    });
    setMensagem(null);
  }

  /** Inclui uma nova entrada vazia no final da lista. */
  function adicionarCurso(): void {
    setCursos((atuais) => [...atuais, criarCursoVazio()]);
  }

  /** Remove um curso pela sua posição no array com suporte a desfazer. */
  function removerCurso(indice: number): void {
    const item = cursos[indice];
    if (
      item &&
      (item.nome.trim() || item.instituicao.trim() || item.cargaHoraria.trim())
    ) {
      setCursoRemovido({ item, indice });
    } else {
      setCursoRemovido(null);
    }

    setCursos((atuais) => atuais.filter((_, i) => i !== indice));
    setErros((atuais) => {
      const novoMapa: Record<number, ErrosCurso> = {};

      Object.entries(atuais).forEach(([chave, valor]) => {
        const indiceOriginal = Number(chave);
        if (indiceOriginal < indice) {
          novoMapa[indiceOriginal] = valor;
        } else if (indiceOriginal > indice) {
          novoMapa[indiceOriginal - 1] = valor;
        }
      });

      return novoMapa;
    });
    setMensagem(null);
  }

  /** Restaura o último curso removido na mesma posição. */
  function desfazerRemocaoCurso(): void {
    if (!cursoRemovido) return;
    setCursos((atuais) => {
      const copia = [...atuais];
      copia.splice(cursoRemovido.indice, 0, cursoRemovido.item);
      return copia;
    });
    setCursoRemovido(null);
  }

  /** Valida cada entrada por índice e normaliza o lote para impedir cadastro parcial sem perder o vínculo dos erros. */
  function validarFormulario(): Curso[] | null {
    const novosErros: Record<number, ErrosCurso> = {};
    cursos.forEach((item, indice) => {
      if (permitirVazios && cursoEstaVazio(item)) return;
      const errosItem = validarCurso(item);
      if (Object.keys(errosItem).length > 0) novosErros[indice] = errosItem;
    });
    setErros(novosErros);
    if (Object.keys(novosErros).length > 0) {
      focarErro.current = true;
      return null;
    }
    return cursos
      .filter((item) => !permitirVazios || !cursoEstaVazio(item))
      .map(normalizarCurso);
  }

  /** Reutiliza a validação do avanço ao submeter para manter feedback e dados enviados coerentes. */
  function enviarFormulario(evento: FormEvent<HTMLFormElement>): void {
    evento.preventDefault();
    if (desabilitado) return;
    if (aoAvancar) {
      void aoAvancar();
      return;
    }
    const cursosNormalizados = validarFormulario();
    if (cursosNormalizados === null || desabilitado) return;
    onSalvar?.(cursosNormalizados);
    setMensagem("Cursos salvos com sucesso.");
  }

  return (
    <form
      ref={formularioRef}
      className="formulario-cursos"
      noValidate
      onSubmit={enviarFormulario}
    >
      <h2 className="secao-titulo">Cursos</h2>

      {cursos.map((curso, indice) => {
        const errosCurso = erros[indice];
        const prefixo = `curso-${indice}`;

        return (
          <fieldset
            disabled={desabilitado}
            aria-label={`Curso ${indice + 1}`}
            key={prefixo}
          >
            <legend className="sr-only">Curso {indice + 1}</legend>

            {cursos.length > 0 && (
              <div className="item-sublista__topo">
                <span className="label-subtitulo">Curso {indice + 1}</span>
                <button
                  aria-label={`Remover curso ${indice + 1}`}
                  className="btn-remover-item"
                  onClick={() => removerCurso(indice)}
                  type="button"
                >
                  Remover
                </button>
              </div>
            )}

            <div className="field">
              <label className="titulo-campo" htmlFor={`${prefixo}-nome`}>
                Nome do curso
              </label>
              <input
                aria-describedby={
                  errosCurso?.nome !== undefined
                    ? `${prefixo}-nome-erro`
                    : undefined
                }
                aria-invalid={errosCurso?.nome !== undefined ? true : undefined}
                id={`${prefixo}-nome`}
                maxLength={LIMITES_CURSO.nome}
                onChange={(e) => atualizarCurso(indice, "nome", e.target.value)}
                placeholder="Ex.: Formação React, Node.js do Zero..."
                type="text"
                value={curso.nome}
              />
              {errosCurso?.nome !== undefined && (
                <p className="field__error" id={`${prefixo}-nome-erro`}>
                  {errosCurso.nome}
                </p>
              )}
            </div>

            <div className="field">
              <label
                className="titulo-campo"
                htmlFor={`${prefixo}-instituicao`}
              >
                Instituição
              </label>
              <input
                aria-describedby={
                  errosCurso?.instituicao !== undefined
                    ? `${prefixo}-instituicao-erro`
                    : undefined
                }
                aria-invalid={
                  errosCurso?.instituicao !== undefined ? true : undefined
                }
                id={`${prefixo}-instituicao`}
                maxLength={LIMITES_CURSO.instituicao}
                onChange={(e) =>
                  atualizarCurso(indice, "instituicao", e.target.value)
                }
                placeholder="Ex.: Alura, Udemy, Coursera..."
                type="text"
                value={curso.instituicao}
              />
              {errosCurso?.instituicao !== undefined && (
                <p className="field__error" id={`${prefixo}-instituicao-erro`}>
                  {errosCurso.instituicao}
                </p>
              )}
            </div>

            <div className="field">
              <label className="titulo-campo" htmlFor={`${prefixo}-carga`}>
                Carga horária (horas)
              </label>
              <input
                aria-describedby={
                  errosCurso?.cargaHoraria !== undefined
                    ? `${prefixo}-carga-erro`
                    : undefined
                }
                aria-invalid={
                  errosCurso?.cargaHoraria !== undefined ? true : undefined
                }
                id={`${prefixo}-carga`}
                inputMode="numeric"
                maxLength={LIMITES_CURSO.cargaHoraria}
                onChange={(e) =>
                  atualizarCurso(indice, "cargaHoraria", e.target.value)
                }
                placeholder="Ex.: 40"
                type="text"
                value={curso.cargaHoraria}
              />
              {errosCurso?.cargaHoraria !== undefined && (
                <p className="field__error" id={`${prefixo}-carga-erro`}>
                  {errosCurso.cargaHoraria}
                </p>
              )}
            </div>
          </fieldset>
        );
      })}

      {cursoRemovido && (
        <div className="alerta-desfazer" role="status">
          <span>
            Curso{" "}
            {cursoRemovido.item.nome ? `"${cursoRemovido.item.nome}"` : ""}{" "}
            removido.
          </span>
          <button
            aria-label="Desfazer remoção do curso"
            disabled={desabilitado}
            className="btn-desfazer"
            onClick={desfazerRemocaoCurso}
            type="button"
          >
            Desfazer
          </button>
        </div>
      )}

      <button
        disabled={desabilitado}
        className="btn-adicionar-item"
        onClick={adicionarCurso}
        type="button"
      >
        + Adicionar curso
      </button>

      {mensagem !== null && (
        <p className="form-message" role="status">
          {mensagem}
        </p>
      )}

      {exibirBotaoSalvar && (
        <button
          disabled={desabilitado}
          className="btn-salvar-secao"
          type="submit"
        >
          Salvar cursos
        </button>
      )}
    </form>
  );
}
