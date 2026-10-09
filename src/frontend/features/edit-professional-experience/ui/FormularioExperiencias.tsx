import { useState, type FormEvent } from "react";

import {
  criarExperienciaVazia,
  ordenarPorDataDecrescente,
  validarListaExperiencias,
  type ErrosExperiencia,
  type Experiencia,
} from "../model/experiencias";

/** Define os valores iniciais e o callback de persistência da tela. */
export interface FormularioExperienciasProps {
  experienciasIniciais?: Experiencia[];
  onSalvar?: (experiencias: Experiencia[]) => void;
}

/**
 * Renderiza e controla o formulário de cadastro de experiências profissionais.
 *
 * O componente mantém um array de experiências no estado local, permite
 * adicionar e remover entradas dinamicamente, desabilita o campo Fim quando
 * "Emprego atual" está marcado, e ordena as experiências cronologicamente
 * antes de chamar o callback de persistência.
 */
export function FormularioExperiencias({
  experienciasIniciais = [criarExperienciaVazia()],
  onSalvar,
}: FormularioExperienciasProps) {
  const [experiencias, setExperiencias] =
    useState<Experiencia[]>(experienciasIniciais);
  const [erros, setErros] = useState<Record<number, ErrosExperiencia>>({});
  const [mensagem, setMensagem] = useState<string | null>(null);

  /** Atualiza um campo de texto de uma experiência pela sua posição. */
  function atualizarCampo(
    indice: number,
    campo: keyof Omit<Experiencia, "empregoAtual">,
    valor: string,
  ): void {
    setExperiencias((atuais) =>
      atuais.map((exp, i) => (i === indice ? { ...exp, [campo]: valor } : exp)),
    );
    limparErroDoCampo(indice, campo as keyof ErrosExperiencia);
  }

  /** Alterna o checkbox de emprego atual e limpa o campo Fim quando ativado. */
  function alternarEmpregoAtual(indice: number): void {
    setExperiencias((atuais) =>
      atuais.map((exp, i) => {
        if (i !== indice) return exp;
        const novoValor = !exp.empregoAtual;
        return {
          ...exp,
          empregoAtual: novoValor,
          fim: novoValor ? "" : exp.fim,
        };
      }),
    );
    limparErroDoCampo(indice, "fim");
  }

  /** Remove o erro de um campo específico de uma experiência. */
  function limparErroDoCampo(
    indice: number,
    campo: keyof ErrosExperiencia,
  ): void {
    setErros((atuais) => {
      const errosExp = { ...atuais[indice] };
      delete errosExp[campo];
      const novoMapa = { ...atuais };

      if (Object.keys(errosExp).length === 0) {
        delete novoMapa[indice];
      } else {
        novoMapa[indice] = errosExp;
      }

      return novoMapa;
    });
    setMensagem(null);
  }

  /** Inclui uma nova entrada vazia no final da lista. */
  function adicionarExperiencia(): void {
    setExperiencias((atuais) => [...atuais, criarExperienciaVazia()]);
  }

  /** Remove uma experiência pela sua posição no array. */
  function removerExperiencia(indice: number): void {
    setExperiencias((atuais) => atuais.filter((_, i) => i !== indice));
    setErros((atuais) => {
      const novoMapa: Record<number, ErrosExperiencia> = {};

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

  /**
   * Valida, ordena cronologicamente e comunica o status de envio do formulário.
   *
   * O manipulador impede o envio nativo, verifica inconsistências de preenchimento
   * através de `validarListaExperiencias`, emite alerta acessível quando há campos
   * inválidos e, em caso de sucesso, normaliza e ordena as experiências antes de
   * acionar o callback `onSalvar`. Ele existe para assegurar feedback imediato e
   * acessível para usuários de tecnologias assistivas e de navegação por teclado.
   */
  function enviarFormulario(evento: FormEvent<HTMLFormElement>): void {
    evento.preventDefault();
    const novosErros = validarListaExperiencias(experiencias);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      setMensagem("Há pendências que precisam ser corrigidas antes de salvar.");
      return;
    }

    const experienciasNormalizadas = experiencias.map((exp) => ({
      empresa: exp.empresa.trim(),
      cargo: exp.cargo.trim(),
      inicio: exp.inicio,
      fim: exp.fim,
      empregoAtual: exp.empregoAtual,
      descricao: exp.descricao.trim(),
    }));

    const experienciasOrdenadas = ordenarPorDataDecrescente(
      experienciasNormalizadas,
    );
    onSalvar?.(experienciasOrdenadas);
    setMensagem("Experiências salvas com sucesso.");
  }

  return (
    <form noValidate onSubmit={enviarFormulario}>
      <h2>Experiências Profissionais</h2>

      {experiencias.map((exp, indice) => {
        const errosExp = erros[indice];
        const prefixo = `exp-${indice}`;

        return (
          <fieldset aria-label={`Experiência ${indice + 1}`} key={prefixo}>
            <legend>Experiência {indice + 1}</legend>

            <div className="field">
              <label htmlFor={`${prefixo}-empresa`}>Nome da empresa</label>
              <input
                aria-describedby={
                  errosExp?.empresa !== undefined
                    ? `${prefixo}-empresa-erro`
                    : undefined
                }
                aria-invalid={
                  errosExp?.empresa !== undefined ? true : undefined
                }
                id={`${prefixo}-empresa`}
                onChange={(e) =>
                  atualizarCampo(indice, "empresa", e.target.value)
                }
                required
                type="text"
                value={exp.empresa}
              />
              {errosExp?.empresa !== undefined && (
                <p className="field__error" id={`${prefixo}-empresa-erro`}>
                  {errosExp.empresa}
                </p>
              )}
            </div>

            <div className="field">
              <label htmlFor={`${prefixo}-cargo`}>Cargo</label>
              <input
                aria-describedby={
                  errosExp?.cargo !== undefined
                    ? `${prefixo}-cargo-erro`
                    : undefined
                }
                aria-invalid={errosExp?.cargo !== undefined ? true : undefined}
                id={`${prefixo}-cargo`}
                onChange={(e) =>
                  atualizarCampo(indice, "cargo", e.target.value)
                }
                required
                type="text"
                value={exp.cargo}
              />
              {errosExp?.cargo !== undefined && (
                <p className="field__error" id={`${prefixo}-cargo-erro`}>
                  {errosExp.cargo}
                </p>
              )}
            </div>

            <div className="field">
              <label htmlFor={`${prefixo}-inicio`}>Início (Mês/Ano)</label>
              <input
                aria-describedby={
                  errosExp?.inicio !== undefined
                    ? `${prefixo}-inicio-erro`
                    : undefined
                }
                aria-invalid={errosExp?.inicio !== undefined ? true : undefined}
                id={`${prefixo}-inicio`}
                onChange={(e) =>
                  atualizarCampo(indice, "inicio", e.target.value)
                }
                required
                type="month"
                value={exp.inicio}
              />
              {errosExp?.inicio !== undefined && (
                <p className="field__error" id={`${prefixo}-inicio-erro`}>
                  {errosExp.inicio}
                </p>
              )}
            </div>

            <div className="field">
              <label htmlFor={`${prefixo}-fim`}>Fim (Mês/Ano)</label>
              <input
                aria-describedby={
                  errosExp?.fim !== undefined
                    ? `${prefixo}-fim-erro`
                    : undefined
                }
                aria-invalid={errosExp?.fim !== undefined ? true : undefined}
                disabled={exp.empregoAtual}
                id={`${prefixo}-fim`}
                onChange={(e) => atualizarCampo(indice, "fim", e.target.value)}
                required={!exp.empregoAtual}
                type="month"
                value={exp.fim}
              />
              {errosExp?.fim !== undefined && (
                <p className="field__error" id={`${prefixo}-fim-erro`}>
                  {errosExp.fim}
                </p>
              )}
            </div>

            <div className="field">
              <label htmlFor={`${prefixo}-emprego-atual`}>
                <input
                  checked={exp.empregoAtual}
                  id={`${prefixo}-emprego-atual`}
                  onChange={() => alternarEmpregoAtual(indice)}
                  type="checkbox"
                />{" "}
                Emprego atual
              </label>
            </div>

            <div className="field">
              <label htmlFor={`${prefixo}-descricao`}>
                Descrição das atividades (opcional)
              </label>
              <textarea
                id={`${prefixo}-descricao`}
                onChange={(e) =>
                  atualizarCampo(indice, "descricao", e.target.value)
                }
                rows={4}
                value={exp.descricao}
              />
            </div>

            {experiencias.length > 1 && (
              <button
                aria-label={`Remover experiência ${indice + 1}`}
                onClick={() => removerExperiencia(indice)}
                type="button"
              >
                Remover experiência
              </button>
            )}
          </fieldset>
        );
      })}

      <button onClick={adicionarExperiencia} type="button">
        + Adicionar experiência
      </button>

      {mensagem !== null && (
        <p
          className="form-message"
          role={mensagem.includes("sucesso") ? "status" : "alert"}
        >
          {mensagem}
        </p>
      )}

      <button type="submit">Salvar experiências</button>
    </form>
  );
}
