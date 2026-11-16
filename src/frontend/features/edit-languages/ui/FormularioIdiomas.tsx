import {
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
  type FormEvent,
  type Ref,
} from "react";

import {
  criarIdiomaVazio,
  idiomaEstaVazio,
  normalizarIdioma,
  NIVEIS_IDIOMA,
  validarIdioma,
  type ErrosIdioma,
  type Idioma,
  type NivelIdioma,
} from "../model/idiomas";
import "./FormularioIdiomas.css";

/** Define os valores iniciais e o callback de persistência da tela. */
export interface FormularioIdiomasProps {
  /** Encaminha o submit ao coordenador da página para não anunciar persistência local como remota. */
  aoAvancar?: () => void | Promise<void>;
  /** Valida e normaliza os dados para a página impedir avanço com entradas parciais. */
  ref?: Ref<{ validar: () => Idioma[] | null }>;
  /** Ignora somente entradas inteiramente vazias nas etapas opcionais. */
  permitirVazios?: boolean;
  /** Impede alterações enquanto a página aguarda persistência. */
  desabilitado?: boolean;
  idiomasIniciais?: Idioma[];
  onSalvar?: (idiomas: Idioma[]) => void;
  /** Notifica a porcentagem de campos preenchidos nesta seção (0 a 100). */
  aoAlterarProgresso?: (progresso: number) => void;
  /** Notifica a lista atual de idiomas preenchidos para preservação de estado. */
  aoAlterarDados?: (idiomas: Idioma[]) => void;
  /** Controla a exibição do subtítulo interno (padrão: true). */
  exibirTitulo?: boolean;
  /** Controla a exibição do botão interno de salvar (padrão: true). */
  exibirBotaoSalvar?: boolean;
}

/**
 * Renderiza e controla o formulário de cadastro de idiomas.
 *
 * O componente mantém um array de idiomas no estado local, permite adicionar
 * e remover entradas dinamicamente, e valida todos os itens antes de chamar
 * o callback de persistência. Cada entrada usa input de texto para o nome do
 * idioma e um select para o nível de proficiência.
 */
export function FormularioIdiomas({
  aoAvancar,
  ref,
  permitirVazios = false,
  desabilitado = false,
  idiomasIniciais = [criarIdiomaVazio()],
  onSalvar,
  aoAlterarProgresso,
  aoAlterarDados,
  exibirTitulo = true,
  exibirBotaoSalvar = true,
}: FormularioIdiomasProps) {
  const [idiomas, setIdiomas] = useState<Idioma[]>(idiomasIniciais);
  const [erros, setErros] = useState<Record<number, ErrosIdioma>>({});
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

  const [idiomaRemovido, setIdiomaRemovido] = useState<{
    item: Idioma;
    indice: number;
  } | null>(null);

  useEffect(() => {
    if (idiomaRemovido) {
      const timer = setTimeout(() => {
        setIdiomaRemovido(null);
      }, 7000);
      return () => clearTimeout(timer);
    }
  }, [idiomaRemovido]);

  useEffect(() => {
    aoAlterarDados?.(idiomas);
  }, [idiomas, aoAlterarDados]);

  useEffect(() => {
    if (!aoAlterarProgresso) return;
    if (idiomas.length === 0) {
      aoAlterarProgresso(0);
      return;
    }

    let totalCampos = 0;
    let preenchidos = 0;

    idiomas.forEach((item) => {
      totalCampos += 2;
      if (item.nome.trim().length > 0) preenchidos++;
      if (item.nivel.trim().length > 0) preenchidos++;
    });

    const porcentagem =
      totalCampos > 0 ? Math.round((preenchidos / totalCampos) * 100) : 0;
    aoAlterarProgresso(porcentagem);
  }, [idiomas, aoAlterarProgresso]);

  /** Atualiza o nome de um idioma pela sua posição no array. */
  function atualizarNome(indice: number, nome: string): void {
    setIdiomas((atuais) =>
      atuais.map((idioma, i) => (i === indice ? { ...idioma, nome } : idioma)),
    );
    limparErroDoCampo(indice, "nome");
  }

  /** Atualiza o nível de proficiência de um idioma pela sua posição. */
  function atualizarNivel(indice: number, nivel: NivelIdioma | ""): void {
    setIdiomas((atuais) =>
      atuais.map((idioma, i) => (i === indice ? { ...idioma, nivel } : idioma)),
    );
    limparErroDoCampo(indice, "nivel");
  }

  /** Remove o erro de um campo específico de um idioma. */
  function limparErroDoCampo(indice: number, campo: keyof ErrosIdioma): void {
    setErros((atuais) => {
      const errosIdioma = { ...atuais[indice] };
      delete errosIdioma[campo];
      const novoMapa = { ...atuais };

      if (Object.keys(errosIdioma).length === 0) {
        delete novoMapa[indice];
      } else {
        novoMapa[indice] = errosIdioma;
      }

      return novoMapa;
    });
    setMensagem(null);
  }

  /** Inclui uma nova entrada vazia no final da lista. */
  function adicionarIdioma(): void {
    setIdiomas((atuais) => [...atuais, criarIdiomaVazio()]);
  }

  /** Remove um idioma pela sua posição no array com suporte a desfazer. */
  function removerIdioma(indice: number): void {
    const item = idiomas[indice];
    if (item && (item.nome.trim() || item.nivel)) {
      setIdiomaRemovido({ item, indice });
    } else {
      setIdiomaRemovido(null);
    }

    setIdiomas((atuais) => atuais.filter((_, i) => i !== indice));
    setErros((atuais) => {
      const novoMapa: Record<number, ErrosIdioma> = {};

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

  /** Restaura o último idioma removido na mesma posição. */
  function desfazerRemocaoIdioma(): void {
    if (!idiomaRemovido) return;
    setIdiomas((atuais) => {
      const copia = [...atuais];
      copia.splice(idiomaRemovido.indice, 0, idiomaRemovido.item);
      return copia;
    });
    setIdiomaRemovido(null);
  }

  /** Valida cada entrada por índice e normaliza o lote para impedir cadastro parcial sem perder o vínculo dos erros. */
  function validarFormulario(): Idioma[] | null {
    const novosErros: Record<number, ErrosIdioma> = {};
    idiomas.forEach((item, indice) => {
      if (permitirVazios && idiomaEstaVazio(item)) return;
      const errosItem = validarIdioma(item);
      if (Object.keys(errosItem).length > 0) novosErros[indice] = errosItem;
    });
    setErros(novosErros);
    if (Object.keys(novosErros).length > 0) {
      focarErro.current = true;
      return null;
    }
    return idiomas
      .filter((item) => !permitirVazios || !idiomaEstaVazio(item))
      .map(normalizarIdioma);
  }

  /** Reutiliza a validação do avanço ao submeter para manter feedback e dados enviados coerentes. */
  function enviarFormulario(evento: FormEvent<HTMLFormElement>): void {
    evento.preventDefault();
    if (desabilitado) return;
    if (aoAvancar) {
      void aoAvancar();
      return;
    }
    const idiomasNormalizados = validarFormulario();
    if (idiomasNormalizados === null || desabilitado) return;

    onSalvar?.(idiomasNormalizados);
    setMensagem("Idiomas salvos com sucesso.");
  }

  return (
    <form
      ref={formularioRef}
      className="formulario-idiomas"
      noValidate
      onSubmit={enviarFormulario}
    >
      {exibirTitulo && <h2 className="secao-titulo">Idiomas</h2>}

      {idiomas.map((idioma, indice) => {
        const errosIdioma = erros[indice];
        const prefixo = `idioma-${indice}`;

        return (
          <fieldset
            disabled={desabilitado}
            aria-label={`Idioma ${indice + 1}`}
            key={prefixo}
          >
            <legend className="sr-only">Idioma {indice + 1}</legend>

            {idiomas.length > 0 && (
              <div className="item-sublista__topo">
                <span className="label-subtitulo">Idioma {indice + 1}</span>
                <button
                  aria-label={`Remover idioma ${indice + 1}`}
                  className="btn-remover-item"
                  onClick={() => removerIdioma(indice)}
                  type="button"
                >
                  Remover
                </button>
              </div>
            )}

            <div className="field">
              <label
                className="titulo-campo titulo-campo--obrigatorio"
                htmlFor={`${prefixo}-nome`}
              >
                Idioma
              </label>
              <input
                aria-describedby={
                  errosIdioma?.nome !== undefined
                    ? `${prefixo}-nome-erro`
                    : undefined
                }
                aria-invalid={
                  errosIdioma?.nome !== undefined ? true : undefined
                }
                id={`${prefixo}-nome`}
                onChange={(e) => atualizarNome(indice, e.target.value)}
                placeholder="Ex.: Inglês, Espanhol, Francês..."
                required
                type="text"
                value={idioma.nome}
              />
              {errosIdioma?.nome !== undefined && (
                <p className="field__error" id={`${prefixo}-nome-erro`}>
                  {errosIdioma.nome}
                </p>
              )}
            </div>

            <div className="field">
              <label
                className="titulo-campo titulo-campo--obrigatorio"
                htmlFor={`${prefixo}-nivel`}
              >
                Nível de proficiência
              </label>
              <select
                aria-describedby={
                  errosIdioma?.nivel !== undefined
                    ? `${prefixo}-nivel-erro`
                    : undefined
                }
                aria-invalid={
                  errosIdioma?.nivel !== undefined ? true : undefined
                }
                id={`${prefixo}-nivel`}
                onChange={(e) =>
                  atualizarNivel(indice, e.target.value as NivelIdioma | "")
                }
                required
                value={idioma.nivel}
              >
                <option value="">Selecione um nível</option>
                {(Object.entries(NIVEIS_IDIOMA) as [NivelIdioma, string][]).map(
                  ([valor, rotulo]) => (
                    <option key={valor} value={valor}>
                      {rotulo}
                    </option>
                  ),
                )}
              </select>
              {errosIdioma?.nivel !== undefined && (
                <p className="field__error" id={`${prefixo}-nivel-erro`}>
                  {errosIdioma.nivel}
                </p>
              )}
            </div>
          </fieldset>
        );
      })}

      {idiomaRemovido && (
        <div className="alerta-desfazer" role="status">
          <span>
            Idioma{" "}
            {idiomaRemovido.item.nome ? `"${idiomaRemovido.item.nome}"` : ""}{" "}
            removido.
          </span>
          <button
            aria-label="Desfazer remoção do idioma"
            disabled={desabilitado}
            className="btn-desfazer"
            onClick={desfazerRemocaoIdioma}
            type="button"
          >
            Desfazer
          </button>
        </div>
      )}

      <button
        disabled={desabilitado}
        className="btn-adicionar-item"
        onClick={adicionarIdioma}
        type="button"
      >
        + Adicionar idioma
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
          Salvar idiomas
        </button>
      )}
    </form>
  );
}
