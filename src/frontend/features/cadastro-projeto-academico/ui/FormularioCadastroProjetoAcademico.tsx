// Proveniência: decision-analysis prompts/frontend/20260921-120136-tela-cadastro-projetos-academicos-v001.md#v001
import { useEffect, useState, type FormEvent } from "react";

import {
  FalhaCadastroProjeto,
  type ClienteProjetosAcademicos,
} from "../api/cliente-projetos-academicos";
import {
  traduzirFalhaCadastroProjeto,
  validarListaProjetosAcademicos,
  validarProjetoAcademico,
  type ErrosProjetoAcademico,
  type ValoresProjetoAcademico,
} from "../model/formulario-projeto-academico";

import "./FormularioCadastroProjetoAcademico.css";

/** Define o cliente usado pelo formulário de cadastro de projeto acadêmico. */
export interface FormularioCadastroProjetoAcademicoProps {
  cliente: ClienteProjetosAcademicos;
  /** Notifica a porcentagem de campos preenchidos nesta etapa (0 a 100). */
  aoAlterarProgresso?: (progresso: number) => void;
  /** Permite avançar caso o usuário não possua projetos ou conclua o cadastro. */
  aoAvancar?: () => void;
  /** Callback para voltar à etapa anterior. */
  onVoltar?: () => void;
  /** Projetos iniciais opcionais para restauração de estado. */
  projetosIniciais?: ValoresProjetoAcademico[];
  /** Notifica a lista de projetos sempre que houver alteração. */
  aoAlterarProjetos?: (projetos: ValoresProjetoAcademico[]) => void;
}

const valoresIniciais: ValoresProjetoAcademico = {
  titulo: "",
  descricao: "",
  tecnologias: "",
};

/**
 * Renderiza e controla a entrada de um ou mais projetos acadêmicos do estudante.
 *
 * O componente mantém valores e feedback no estado local em lista, valida antes de
 * chamar o cliente injetado e preserva o formulário em falhas.
 */
export function FormularioCadastroProjetoAcademico({
  cliente,
  aoAlterarProgresso,
  aoAvancar,
  onVoltar,
  projetosIniciais = [valoresIniciais],
  aoAlterarProjetos,
}: FormularioCadastroProjetoAcademicoProps) {
  const [projetos, setProjetos] =
    useState<ValoresProjetoAcademico[]>(projetosIniciais);
  const [erros, setErros] = useState<Record<number, ErrosProjetoAcademico>>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [semProjetos, setSemProjetos] = useState(false);

  useEffect(() => {
    aoAlterarProjetos?.(projetos);
  }, [projetos, aoAlterarProjetos]);

  useEffect(() => {
    if (!aoAlterarProgresso) return;
    if (semProjetos) {
      aoAlterarProgresso(100);
      return;
    }
    let preenchidos = 0;
    const total = projetos.length * 3;
    projetos.forEach((proj) => {
      if (proj.titulo.trim().length > 0) preenchidos++;
      if (proj.descricao.trim().length > 0) preenchidos++;
      if (proj.tecnologias.trim().length > 0) preenchidos++;
    });

    const porcentagem =
      total > 0 ? Math.round((preenchidos / total) * 100) : 100;
    aoAlterarProgresso(porcentagem);
  }, [projetos, semProjetos, aoAlterarProgresso]);

  /** Atualiza um campo de um projeto pela sua posição. */
  function atualizarCampo(
    indice: number,
    campo: keyof ValoresProjetoAcademico,
    valor: string,
  ): void {
    setProjetos((atuais) =>
      atuais.map((proj, i) =>
        i === indice ? { ...proj, [campo]: valor } : proj,
      ),
    );
    setErros((atuais) => {
      const errosProj = { ...atuais[indice] };
      delete errosProj[campo];
      const novoMapa = { ...atuais };
      if (Object.keys(errosProj).length === 0) {
        delete novoMapa[indice];
      } else {
        novoMapa[indice] = errosProj;
      }
      return novoMapa;
    });
    setMensagem(null);
  }

  /** Adiciona um novo projeto acadêmico no final da lista. */
  function adicionarProjeto(): void {
    setProjetos((atuais) => [...atuais, { ...valoresIniciais }]);
  }

  /** Remove um projeto acadêmico pela sua posição na lista. */
  function removerProjeto(indice: number): void {
    if (projetos.length <= 1) return;
    setProjetos((atuais) => atuais.filter((_, i) => i !== indice));
    setErros((atuais) => {
      const novoMapa: Record<number, ErrosProjetoAcademico> = {};
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

  /**
   * Valida e encaminha os projetos pelo contrato injetado da feature.
   */
  async function enviarProjeto(
    evento: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    evento.preventDefault();

    if (semProjetos) {
      aoAvancar?.();
      return;
    }

    const todosVazios = projetos.every(
      (p) =>
        p.titulo.trim() === "" &&
        p.descricao.trim() === "" &&
        p.tecnologias.trim() === "",
    );

    if (todosVazios) {
      aoAvancar?.();
      return;
    }

    const novosErros = validarListaProjetosAcademicos(projetos);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      return;
    }

    setEnviando(true);
    setMensagem(null);

    try {
      for (const proj of projetos) {
        await cliente.cadastrar({
          titulo: proj.titulo.trim(),
          descricao: proj.descricao.trim(),
          tecnologias: proj.tecnologias.trim(),
        });
      }
      setMensagem("Dados do projeto enviados para processamento.");
      if (!aoAvancar) {
        setProjetos([{ ...valoresIniciais }]);
      }
      setErros({});
      aoAvancar?.();
    } catch (erro: unknown) {
      setMensagem(
        traduzirFalhaCadastroProjeto(
          erro instanceof FalhaCadastroProjeto
            ? erro.codigo
            : "resposta-invalida",
        ),
      );
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form
      className="formulario-projeto-academico"
      noValidate
      onSubmit={enviarProjeto}
    >
      {semProjetos && (
        <div className="projetos-vazio" role="status">
          <p className="projetos-vazio__texto">
            Nenhum projeto acadêmico cadastrado.
          </p>
          <p className="projetos-vazio__subtexto">
            Se você não possui projetos acadêmicos ou de extensão para destacar
            no momento, pode avançar para a próxima etapa.
          </p>
          <button
            className="btn-adicionar-projeto"
            onClick={() => {
              setSemProjetos(false);
              setProjetos([{ ...valoresIniciais }]);
              setMensagem(null);
            }}
            type="button"
          >
            + Adicionar projeto acadêmico
          </button>
        </div>
      )}

      {!semProjetos && (
        <>
          {projetos.map((valores, indice) => {
            const prefixo = `projeto-${indice}`;
            const errosItem = erros[indice] ?? {};

            return (
              <fieldset
                aria-label={`Projeto acadêmico ${indice + 1}`}
                key={`projeto-${indice}`}
              >
                <legend className="sr-only">
                  Projeto acadêmico {indice + 1}
                </legend>
                {projetos.length > 1 && (
                  <div className="item-sublista__topo">
                    <span className="label-subtitulo">
                      Projeto acadêmico {indice + 1}
                    </span>
                    <button
                      type="button"
                      className="btn-remover-item"
                      onClick={() => removerProjeto(indice)}
                      aria-label={`Remover Projeto acadêmico ${indice + 1}`}
                    >
                      Remover
                    </button>
                  </div>
                )}

                <CampoTexto
                  erro={errosItem.titulo}
                  id={`${prefixo}-titulo`}
                  label="Título do projeto"
                  obrigatorio
                  onChange={(valor) => atualizarCampo(indice, "titulo", valor)}
                  placeholder="Ex.: Sistema de Gestão Acadêmica"
                  value={valores.titulo}
                />
                <CampoTexto
                  erro={errosItem.descricao}
                  id={`${prefixo}-descricao`}
                  label="Descrição"
                  multiline
                  obrigatorio
                  onChange={(valor) =>
                    atualizarCampo(indice, "descricao", valor)
                  }
                  placeholder="Explique o objetivo do projeto, sua contribuição e os principais desafios..."
                  value={valores.descricao}
                />
                <CampoTexto
                  erro={errosItem.tecnologias}
                  id={`${prefixo}-tecnologias`}
                  label="Tecnologias utilizadas"
                  obrigatorio
                  onChange={(valor) =>
                    atualizarCampo(indice, "tecnologias", valor)
                  }
                  placeholder="Ex.: React, TypeScript, Python"
                  value={valores.tecnologias}
                />
              </fieldset>
            );
          })}

          <button
            type="button"
            className="btn-adicionar-item"
            onClick={adicionarProjeto}
          >
            + Adicionar projeto acadêmico
          </button>
        </>
      )}

      {mensagem !== null && (
        <p
          className="form-message"
          role={mensagem.includes("processamento") ? "status" : "alert"}
        >
          {mensagem}
        </p>
      )}

      <div className="botoes-navegacao">
        <button
          aria-label="Voltar para a etapa anterior"
          className="btn-voltar"
          onClick={onVoltar}
          type="button"
        >
          Voltar
        </button>
        <button
          aria-label="Cadastrar projeto"
          className="btn-proximo"
          disabled={enviando}
          type="submit"
        >
          {enviando ? "Enviando projeto..." : "Próximo"}
        </button>
      </div>

      {!semProjetos && (
        <button
          className="btn-pular-projeto"
          onClick={() => {
            setSemProjetos(true);
            setProjetos([{ ...valoresIniciais }]);
            setErros({});
            setMensagem(null);
          }}
          type="button"
        >
          Não possuo projetos acadêmicos
        </button>
      )}
    </form>
  );
}

/** Define a configuração de campo textual do formulário de projeto. */
interface CampoTextoProps {
  erro?: string;
  id: string;
  label: string;
  multiline?: boolean;
  obrigatorio?: boolean;
  onChange: (valor: string) => void;
  placeholder?: string;
  value: string;
}

/**
 * Renderiza um campo textual com rótulo e erro acessivelmente associado.
 *
 * O componente escolhe input ou textarea conforme o conteúdo, mantendo o
 * mesmo vínculo semântico com o erro. Ele existe para reduzir repetição visual
 * sem mover validações ou regras de projeto para uma camada de UI genérica.
 */
function CampoTexto({
  erro,
  id,
  label,
  multiline = false,
  obrigatorio = false,
  onChange,
  placeholder,
  value,
}: CampoTextoProps) {
  const idErro = `${id}-erro`;
  const atributosDeAcesso = {
    "aria-describedby": erro === undefined ? undefined : idErro,
    "aria-invalid": erro === undefined ? undefined : true,
  };

  return (
    <div className="field">
      <label
        className={`titulo-campo ${obrigatorio ? "titulo-campo--obrigatorio" : ""}`}
        htmlFor={id}
      >
        {label}
      </label>
      {multiline ? (
        <textarea
          {...atributosDeAcesso}
          id={id}
          onChange={(evento) => onChange(evento.target.value)}
          placeholder={placeholder}
          required={obrigatorio}
          rows={5}
          value={value}
        />
      ) : (
        <input
          {...atributosDeAcesso}
          id={id}
          onChange={(evento) => onChange(evento.target.value)}
          placeholder={placeholder}
          required={obrigatorio}
          type="text"
          value={value}
        />
      )}
      {erro !== undefined && (
        <p className="field__error" id={idErro}>
          {erro}
        </p>
      )}
    </div>
  );
}
