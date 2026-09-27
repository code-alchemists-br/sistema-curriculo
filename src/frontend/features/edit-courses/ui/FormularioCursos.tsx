import { useState, type FormEvent } from "react";

import {
  criarCursoVazio,
  normalizarCurso,
  validarListaCursos,
  type Curso,
  type ErrosCurso
} from "../model/cursos";

/** Define os valores iniciais e o callback de persistência da tela. */
export interface FormularioCursosProps {
  cursosIniciais?: Curso[];
  onSalvar?: (cursos: Curso[]) => void;
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
  cursosIniciais = [criarCursoVazio()],
  onSalvar
}: FormularioCursosProps) {
  const [cursos, setCursos] = useState<Curso[]>(cursosIniciais);
  const [erros, setErros] = useState<Record<number, ErrosCurso>>({});
  const [mensagem, setMensagem] = useState<string | null>(null);

  /** Atualiza um campo específico de um curso pela sua posição no array. */
  function atualizarCurso(indice: number, campo: keyof Curso, valor: string): void {
    setCursos((atuais) =>
      atuais.map((curso, i) => (i === indice ? { ...curso, [campo]: valor } : curso))
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

  /** Remove um curso pela sua posição no array. */
  function removerCurso(indice: number): void {
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

  /** Valida todos os cursos e chama o callback se não houver erros. */
  function enviarFormulario(evento: FormEvent<HTMLFormElement>): void {
    evento.preventDefault();
    const novosErros = validarListaCursos(cursos);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      return;
    }

    const cursosNormalizados = cursos.map(normalizarCurso);
    onSalvar?.(cursosNormalizados);
    setMensagem("Cursos salvos com sucesso.");
  }

  return (
    <form noValidate onSubmit={enviarFormulario}>
      <h2>Cursos e Certificações</h2>

      {cursos.map((curso, indice) => {
        const errosCurso = erros[indice];
        const prefixo = `curso-${indice}`;

        return (
          <fieldset aria-label={`Curso ${indice + 1}`} key={prefixo}>
            <legend>Curso {indice + 1}</legend>

            <div className="field">
              <label htmlFor={`${prefixo}-nome`}>Nome do curso</label>
              <input
                aria-describedby={errosCurso?.nome !== undefined ? `${prefixo}-nome-erro` : undefined}
                aria-invalid={errosCurso?.nome !== undefined ? true : undefined}
                id={`${prefixo}-nome`}
                onChange={(e) => atualizarCurso(indice, "nome", e.target.value)}
                required
                type="text"
                value={curso.nome}
              />
              {errosCurso?.nome !== undefined && (
                <p className="field__error" id={`${prefixo}-nome-erro`}>{errosCurso.nome}</p>
              )}
            </div>

            <div className="field">
              <label htmlFor={`${prefixo}-instituicao`}>Instituição</label>
              <input
                aria-describedby={errosCurso?.instituicao !== undefined ? `${prefixo}-instituicao-erro` : undefined}
                aria-invalid={errosCurso?.instituicao !== undefined ? true : undefined}
                id={`${prefixo}-instituicao`}
                onChange={(e) => atualizarCurso(indice, "instituicao", e.target.value)}
                required
                type="text"
                value={curso.instituicao}
              />
              {errosCurso?.instituicao !== undefined && (
                <p className="field__error" id={`${prefixo}-instituicao-erro`}>{errosCurso.instituicao}</p>
              )}
            </div>

            <div className="field">
              <label htmlFor={`${prefixo}-carga`}>Carga horária (horas)</label>
              <input
                aria-describedby={errosCurso?.cargaHoraria !== undefined ? `${prefixo}-carga-erro` : undefined}
                aria-invalid={errosCurso?.cargaHoraria !== undefined ? true : undefined}
                id={`${prefixo}-carga`}
                inputMode="numeric"
                onChange={(e) => atualizarCurso(indice, "cargaHoraria", e.target.value)}
                required
                type="text"
                value={curso.cargaHoraria}
              />
              {errosCurso?.cargaHoraria !== undefined && (
                <p className="field__error" id={`${prefixo}-carga-erro`}>{errosCurso.cargaHoraria}</p>
              )}
            </div>

            {cursos.length > 1 && (
              <button
                aria-label={`Remover curso ${indice + 1}`}
                onClick={() => removerCurso(indice)}
                type="button"
              >
                Remover curso
              </button>
            )}
          </fieldset>
        );
      })}

      <button onClick={adicionarCurso} type="button">+ Adicionar curso</button>

      {mensagem !== null && (
        <p className="form-message" role="status">{mensagem}</p>
      )}

      <button type="submit">Salvar cursos</button>
    </form>
  );
}
