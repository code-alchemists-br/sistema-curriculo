import { useState, type FormEvent } from "react";

import {
  criarIdiomaVazio,
  NIVEIS_IDIOMA,
  validarListaIdiomas,
  type ErrosIdioma,
  type Idioma,
  type NivelIdioma,
} from "../model/idiomas";

/** Define os valores iniciais e o callback de persistência da tela. */
export interface FormularioIdiomasProps {
  idiomasIniciais?: Idioma[];
  onSalvar?: (idiomas: Idioma[]) => void;
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
  idiomasIniciais = [criarIdiomaVazio()],
  onSalvar,
}: FormularioIdiomasProps) {
  const [idiomas, setIdiomas] = useState<Idioma[]>(idiomasIniciais);
  const [erros, setErros] = useState<Record<number, ErrosIdioma>>({});
  const [mensagem, setMensagem] = useState<string | null>(null);

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

  /** Remove um idioma pela sua posição no array. */
  function removerIdioma(indice: number): void {
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

  /** Valida todos os idiomas e chama o callback se não houver erros. */
  function enviarFormulario(evento: FormEvent<HTMLFormElement>): void {
    evento.preventDefault();
    const novosErros = validarListaIdiomas(idiomas);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      return;
    }

    const idiomasNormalizados = idiomas.map((idioma) => ({
      nome: idioma.nome.trim(),
      nivel: idioma.nivel,
    })) as Idioma[];

    onSalvar?.(idiomasNormalizados);
    setMensagem("Idiomas salvos com sucesso.");
  }

  return (
    <form noValidate onSubmit={enviarFormulario}>
      <h2>Idiomas</h2>

      {idiomas.map((idioma, indice) => {
        const errosIdioma = erros[indice];
        const prefixo = `idioma-${indice}`;

        return (
          <fieldset aria-label={`Idioma ${indice + 1}`} key={prefixo}>
            <legend>Idioma {indice + 1}</legend>

            <div className="field">
              <label htmlFor={`${prefixo}-nome`}>Idioma</label>
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
              <label htmlFor={`${prefixo}-nivel`}>Nível de proficiência</label>
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

            {idiomas.length > 1 && (
              <button
                aria-label={`Remover idioma ${indice + 1}`}
                onClick={() => removerIdioma(indice)}
                type="button"
              >
                Remover idioma
              </button>
            )}
          </fieldset>
        );
      })}

      <button onClick={adicionarIdioma} type="button">
        + Adicionar idioma
      </button>

      {mensagem !== null && (
        <p className="form-message" role="status">
          {mensagem}
        </p>
      )}

      <button type="submit">Salvar idiomas</button>
    </form>
  );
}
